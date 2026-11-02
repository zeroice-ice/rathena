"""Batch adapter for the existing early combat kernel.
Only the blessed Novice/Knife and adjacent G_PORING profile is supported.
CLI: python batch_combat.py input.json > result.json
Input: {"state": <previous output state>, "duration_ms": 5000,
        "stop_hp_ratio": 0.5}
Create state with new_state; valid_until MUST be the next buff expiration,
regen tick or other unimplemented world event. Stop before that boundary.
No saves are modified. GM persists returned state once per command.
Defeat stops combat; rewards, death and quest handlers remain external.
"""
import copy, heapq, json, sys
from early_combat import RNG, Scheduler, attack, novice2_blessed, poring, Unsupported

def new_state(now, seed, counter, valid_until, player_hp=45, mob_hp=55,
              next_player_start=None, next_mob_start=None):
    if valid_until <= now:
        raise Unsupported("Prepare the next world event before combat")
    q = Scheduler(now)
    q.add(now if next_player_start is None else next_player_start, "player_start")
    if next_mob_start is not None:
        q.add(next_mob_start, "mob_start")
    return dict(version=1, now=now, seed=seed, counter=counter,
                valid_until=valid_until, player_hp=player_hp, mob_hp=mob_hp,
                engaged=next_mob_start is not None, queue=q.dump(), sequence=q.sequence)

def run(state, duration_ms, stop_hp_ratio=0.5):
    if type(duration_ms) is not int or not 0 < duration_ms <= 60000:
        raise ValueError("duration_ms must be 1..60000")
    if not 0 <= stop_hp_ratio <= 1:
        raise ValueError("stop_hp_ratio must be 0..1")
    s = copy.deepcopy(state)
    if s["version"] != 1:
        raise Unsupported("state version")
    p, m = novice2_blessed(), poring()
    if not 0 <= s["player_hp"] <= p["hp"] or not 0 <= s["mob_hp"] <= m["hp"]:
        raise Unsupported("HP outside supported profile")
    q = Scheduler(s["now"], s["queue"], s["sequence"])
    kinds = {"player_start", "mob_start", "player_damage", "mob_damage"}
    if any(e.kind not in kinds or e.at < q.now for e in q.events):
        raise Unsupported("invalid queue")
    r = RNG(s["seed"], s["counter"])
    end = q.now + duration_ms
    summary = {actor: dict(attacks=0, hits=0, damage=0) for actor in ("player", "mob")}
    reason = "duration"
    while True:
        if not s["player_hp"] or not s["mob_hp"]:
            reason = "defeat"; q.events.clear(); break
        if s["player_hp"] <= p["hp"] * stop_hp_ratio:
            reason = "hp_threshold"; break
        if not q.events or q.events[0].at > end:
            q.now = min(end, s["valid_until"])
            if q.now == s["valid_until"]: reason = "world_event"
            break
        if q.events[0].at >= s["valid_until"]:
            q.now = s["valid_until"]; reason = "world_event"; break
        e = heapq.heappop(q.events); q.now = e.at
        actor = e.kind.split("_")[0]
        stats = p if actor == "player" else m
        if e.kind.endswith("_start"):
            q.add(e.at + stats["amotion"], actor + "_damage")
            q.add(e.at + stats["adelay"], actor + "_start")
        else:
            target = "mob" if actor == "player" else "player"
            result = attack(stats, m if actor == "player" else p, r, actor == "player")
            s[target + "_hp"] = max(0, s[target + "_hp"] - result["damage"])
            summary[actor]["attacks"] += 1
            summary[actor]["hits"] += int(result["damage"] > 0)
            summary[actor]["damage"] += result["damage"]
            if actor == "player" and s["mob_hp"] and not s["engaged"]:
                s["engaged"] = True
                q.add(((e.at + 99)//100)*100, "mob_start")
    s.update(now=q.now, queue=q.dump(), sequence=q.sequence, counter=r.counter)
    return dict(state=s, elapsed_ms=q.now-state["now"], reason=reason, summary=summary)

if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as f:
        request = json.load(f)
    print(json.dumps(run(**request), ensure_ascii=False))
