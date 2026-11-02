# ห้องเริ่มต้น: การตรวจเพิ่มเติม

Source: rAthena Development Team, repository LICENSE applies. Snapshot `8338edfa85b3794e5f024d5f3daed6064012dc0f`.

- `npc/re/warps/cities/izlude.txt:57–67`: room_out at (27,30) sends to (51,30) on same map copy. Wounded Swordsman at (56,32) is beyond this room transition, not established as visible from spawn (18,26). Correct earlier narration that placed him near the visible exit.
- `npc/re/jobs/novice/academy.txt:20–130`: intro navigation and timed UI tips; wounded NPC dialogue/quest 21001 requires approaching/interacting. Looking around from spawn does not grant the quest.
- No map geometry/art inspection performed: do not assert furniture, containers, hidden loot, or visibility through room boundaries from these scripts.

Chat adapter ruling: bare 'สำรวจห้อง' means a stationary visual overview, like a free scene/status inspection: 0 ms, no movement, no RNG, no quest changes. Searching a specific object or walking is a separate action. This is a chat adaptation, not an rAthena timed search mechanic. UI rotation/click tutorials summarized rather than simulated as world events.
