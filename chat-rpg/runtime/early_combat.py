"""Limited Renewal calculation kernel; NOT a full rAthena emulator.
See EARLY_COMBAT_SCOPE.th.md. Pure functions never edit campaign saves.
"""
import hashlib, math, heapq
from dataclasses import dataclass, field

class Unsupported(ValueError): pass

class RNG:
    def __init__(self, seed, counter=0):
        self.seed, self.counter, self.audit = seed, counter, []
    def draw(self, n, purpose):
        if n < 1: raise ValueError('empty interval')
        limit = 2**256 - (2**256 % n)
        while True:
            counter = self.counter; self.counter += 1
            digest = hashlib.sha256(f'{self.seed}:{counter}'.encode()).hexdigest()
            x = int(digest, 16)
            self.audit.append(dict(counter=counter, sha256=digest, n=n,
                                   purpose=purpose, accepted=x < limit,
                                   result=x % n if x < limit else None))
            if x < limit: return x % n


def novice2_blessed():
    # Current campaign: base stats 1, Job2 LUK+1, Blessing10, IncreaseAGI10.
    # Batk integer operations follow status_base_atk; def2 is incremental.
    batk = (11*10 + 11*10//5 + 2*10//3 + 2*10//4)//10
    aspd = int(math.sqrt(11*11/5 + 13*13*0.5)*0.25 + 196)-55
    aspd += (max(195-aspd, 2)*10)//100
    motion = 2000-aspd*10
    return dict(hp=45, level=2, str=11, agi=13, vit=1, dex=11, int=11,
                luk=2, batk=batk, hit=175+2+11+2//3+20, flee=100+2+13,
                cri=10+2*3, flee2=12, hard_def=10,
                soft_def=int((2+1)/2+1/5)+int(13/5-1/5),
                weapon_min=int(17-0.85+17*11/200),
                weapon_max=int(17+0.85+17*11/200),
                amotion=motion, adelay=2*motion, walk_ms=150*75//100)


def poring():
    return dict(hp=55, level=1, str=6, agi=1, vit=1, dex=6, luk=5,
                batk=7, hit=157, flee=102, cri=0, flee2=0,
                hard_def=2, soft_def=1, weapon_min=0, weapon_max=1,
                amotion=672, adelay=1872, walk_ms=400)


def attack(attacker, target, rng, player):
    """Only normal neutral single-hand Knife vs G_PORING, no other bonuses."""
    if target['flee2'] and rng.draw(1000,'perfect_dodge') < target['flee2']:
        return dict(damage=0, result='perfect_dodge')
    critical = bool(attacker['cri'] and rng.draw(1000,'critical') <
                    attacker['cri']-target['luk']*(2 if player else 3))
    hitrate = min(100,max(5,attacker['hit']-target['flee']))
    if not critical and rng.draw(100,'hit') >= hitrate:
        return dict(damage=0,result='miss', hitrate=hitrate)
    lo, hi = attacker['weapon_min'], attacker['weapon_max']
    # PC rnd_value inclusive; non-PC base damage excludes upper bound.
    w = hi if critical else lo+rng.draw(hi-lo+(1 if player else 0),'weapon') if hi>lo else lo
    if player:
        raw=2*attacker['batk']+w*75//100
    else:
        raw=attacker['batk']+w
    d=raw*(4000+target['hard_def'])//(4000+10*target['hard_def'])-target['soft_def']
    d=max(1,d)
    if critical: d=int(d*1.4)
    return dict(damage=d, result='critical' if critical else 'hit',
                hitrate=hitrate, weapon_roll=w, raw=raw)

@dataclass(order=True)
class Event:
    at: int
    sequence: int
    kind: str=field(compare=False)
    data: dict=field(compare=False,default_factory=dict)

class Scheduler:
    """Serializable ordering primitive. Domain handlers must be explicitly supplied.
    Same-time priority uses persisted insertion order, a chat adaptation.
    Does not silently implement mob AI, item scripts, or status expiration.
    """
    def __init__(self, now=0, events=(), sequence=0):
        self.now=now; self.sequence=sequence
        self.events=[Event(**x) for x in events];heapq.heapify(self.events)
    def add(self, at, kind, **data):
        if at<self.now: raise ValueError('past event')
        self.sequence+=1;heapq.heappush(self.events,Event(at,self.sequence,kind,data))
    def advance(self, end, handlers):
        if end<self.now: raise ValueError('time reversal')
        # Refuse unknown event types BEFORE mutating clock/queue.
        for e in self.events:
            if e.at<=end and e.kind not in handlers:raise Unsupported(e.kind)
        while self.events and self.events[0].at<=end:
            e=heapq.heappop(self.events);self.now=e.at;handlers[e.kind](e,self)
        self.now=end
    def dump(self):
        return [dict(at=e.at,sequence=e.sequence,kind=e.kind,data=e.data) for e in sorted(self.events)]


def resolve_single_player_attack(now, seed, counter, player_hp=45, mob_hp=55):
    """Resolve one requested normal attack and the first AI retaliation it causes.

    Scope is deliberately narrow: adjacent targets, no movement or skills, current
    Novice buffs, and one G_PORING.  The 100 ms AI polling is source-derived; using
    its next boundary and storing an insertion order is the chat adapter.
    """
    player, mob = novice2_blessed(), poring()
    rng = RNG(seed, counter)
    sched, log = Scheduler(now), []
    # unit_attack attacks immediately; battle damage is delivered after amotion.
    sched.add(now + player['amotion'], 'player_damage')
    state = {'player_hp': player_hp, 'mob_hp': mob_hp, 'retaliation_started': False}

    def player_damage(event, queue):
        result = attack(player, mob, rng, True)
        state['mob_hp'] = max(0, state['mob_hp'] - result['damage'])
        log.append(dict(at=event.at, actor='player', **result, target_hp=state['mob_hp']))
        if state['mob_hp']:
            # mob_ai_hard runs every 100 ms.  A damaged type-02 Poring can target
            # and attack its attacker because it has MD_CANATTACK (0x83).
            ai_at = ((event.at + 99) // 100) * 100
            queue.add(ai_at, 'mob_ai')

    def mob_ai(event, queue):
        state['retaliation_started'] = True
        queue.add(event.at + mob['amotion'], 'mob_damage')
        # unit_attack(md, target, 1) makes the monster's normal attack continuous.
        # We stop this command after its first impact and persist the next attack.
        state['next_mob_attack_start_ms'] = event.at + mob['adelay']

    def mob_damage(event, queue):
        result = attack(mob, player, rng, False)
        state['player_hp'] = max(0, state['player_hp'] - result['damage'])
        log.append(dict(at=event.at, actor='poring', **result, target_hp=state['player_hp']))

    end = ((now + player['amotion'] + 99) // 100) * 100 + mob['amotion']
    sched.advance(end, {'player_damage': player_damage, 'mob_ai': mob_ai,
                        'mob_damage': mob_damage})
    return dict(end_ms=end, player_hp=state['player_hp'], mob_hp=state['mob_hp'],
                rng_counter=rng.counter, rng_audit=rng.audit, events=log,
                retaliation_started=state['retaliation_started'],
                next_mob_attack_start_ms=state.get('next_mob_attack_start_ms'))


def verify():
    p,m=novice2_blessed(),poring()
    assert (p['batk'],p['soft_def'],p['amotion'],p['adelay'],p['walk_ms'])==(14,3,520,1040,112)
    assert (min(100,p['hit']-m['flee']),m['hit']-p['flee'])==(100,42)
    class Fixed:
        def __init__(self,x):self.x=iter(x)
        def draw(self,n,purpose):
            v=next(self.x);assert 0<=v<n;return v
    assert attack(p,m,Fixed([999,0,0]),True)['damage']==38
    assert attack(p,m,Fixed([0]),True)['damage']==54
    assert attack(m,p,Fixed([999,41,0]),False)['damage']==3
    assert attack(m,p,Fixed([999,42]),False)['result']=='miss'
    assert attack(m,p,Fixed([0]),False)['result']=='perfect_dodge'
    r1,r2=RNG('verification'),RNG('verification')
    assert [r1.draw(100,'test') for _ in range(20)]==[r2.draw(100,'test') for _ in range(20)]
    s=Scheduler();seen=[];s.add(1872,'monster');s.add(1040,'player');s.advance(1040,{'player':lambda e,s:seen.append(e.kind)})
    assert seen==['player'] and s.dump()[0]['at']==1872
    try:s.advance(1872,{})
    except Unsupported:pass
    else:raise AssertionError('unknown event did not stop')
    assert s.now==1040
    r = resolve_single_player_attack(8594, 'verification', 1)
    assert [e['at'] for e in r['events']] == [9114, 9872]
    assert r['retaliation_started'] and r['rng_counter'] > 1
    print('Verified: damage boundary fixtures, RNG replay, event ordering, unsupported-event guard.')
if __name__=='__main__': verify()
