# ขอบเขตตัวคำนวณช่วงต้น v0.1

ที่มา: rAthena Development Team, repository LICENSE. Source pin 8338edfa85b3794e5f024d5f3daed6064012dc0f.

runtime/early_combat.py เป็น calculation kernel และ queue primitive ยังไม่ใช่ combat engine ครบชุด: ยังต้องเชื่อม damage callbacks, AI response, death/quest inventory, regeneration และบัฟหมดอายุ ก่อนตัดสินการต่อสู้จริง. ห้ามตั้ง combat_ready=true เพียงเพราะ fixtures ผ่าน. ไม่รันเซิร์ฟเวอร์และไม่ตรวจเทียบกับ live server.

ตรวจ source: battle.cpp:2443–2503 ช่วง WeaponATK มี variance และ STR bonus, Dagger Medium75% จาก db/size_fix.yml:37; status.cpp:2424–2495 StatusATK; :2600–2750 HIT/FLEE/soft DEF/CRIT; :5970–6055 incremental battle status (soft DEF3 เมื่อบัฟเพิ่ม AGI12; ไม่ใช่4จากนำ effective stats ไปเข้าฐานสูตรใหม่); :7584 Blessing เพิ่ม HIT20. battle.cpp:3017–3330 critical/hit และ :5424 perfect dodge ก่อน critical; :4856 DEF; :5646 critical1.4 หลังDEF. ค่าปัจจุบัน StatusATK14, HIT208, FLEE115, softDEF3; Knife weapon roll17–18 -> sizefix12–13 -> normal hit38–39 กับ G_PORING. CRIT6/1000 หลัง target LUK penalty. Monster HIT157 FLEE102, CRIT0 ตาม enable_critical17 (PC/PET), perfect dodge0 ตาม enable_perfect_flee1. Monster physical rangeมาจาก0.8/1.2ของ Attack1 ไม่ใช่ Attack2; batk7; หลังDEFผู้เล่น3 damageถ้าโดน. ค่าตัวอย่างไม่ได้เป็นผลที่ทอยจริง.

เวลา: status_base_amotion_pc และ status_calc_bl ASPD: Dagger55, AGI13 DEX11 และ IncreaseAGI10 -> amotion520ms, adelay1040ms; G_PORING amotion672 adelay1872. status_calc_speed IncreaseAGI หัก25จากspeed_rate100: 150*75/100 ปัดลง112msต่อก้าวตรง. ยังไม่กำหนด timing ผลตอบโต้ NPC หรือ delayed hit โดยใช้ตัวเลขเหล่านี้อย่างเดียว. mob.hpp MIN_MOBTHINKTIME100 เป็น tick ไม่ใช่คำรับรองว่าตอบโต้หลัง100msเสมอ.

การทดสอบ: python chat-rpg/runtime/early_combat.py ตรวจ normal/critical/PD/miss fixture, ขอบเขต hit42%, seed replay, queueเรียง1040ก่อน1872 และไม่เดินเวลาถ้าขาด handler. ยังไม่ทดสอบ fight end-to-end.

ส่วนดัดแปลงโลกแชท: encounter node `island_training_01` เป็นพื้นที่ย่อสำหรับเผชิญหน้า ไม่ใช่พิกัด spawnจริง. ระยะทางจากกัปตันกำหนด12ก้าวตรงเทียบเท่า ใช้เวลา1344msขณะมีบัฟ; ไม่อ้างว่าตรวจ collision หรือจำลอง40มอนสเตอร์เดินจริง. มอนสเตอร์เป้าหมาย `intro_poring_01`, ID2401 HP55 ใช้สมาชิกใน spawn budget40ของ int_land02 ตาม npc/re/mobs/int_land.txt; ไม่ได้เพิ่มโอกาสดรอป. รอคำสั่งโจมตีจากผู้เล่น ไม่เริ่มต่อสู้อัตโนมัติ. ไม่สุ่มหาตำแหน่งที่ source ไม่ระบุ. ระหว่างอยู่ node ใช้ชื่อ node แทนพิกัดที่ยังไม่ตรวจ; เก็บตำแหน่ง anchor ไว้สำหรับกลับไปกัปตัน.


## การโจมตีจริงครั้งที่ 1 — มิสเตอร์ไอซ์

ต่อยอด kernel ด้วย `resolve_single_player_attack` สำหรับคำสั่งโจมตีปกติหนึ่งครั้งในเงื่อนไขนี้เท่านั้น: เป้าหมายประชิด, Human Novice ปัจจุบันที่ได้รับ Blessing/Increase AGI, Knife และ G_PORING ID 2401. ลำดับที่ใช้: unit_attack เริ่มโจมตีทันที → `battle_delay_damage_sub` ส่ง damage หลัง player amotion 520ms → `mob_ai_hard` รอบถัดไปทุก 100ms เห็นผู้โจมตีและเริ่มโจมตีตอบโต้ → ส่ง damage หลัง Poring amotion 672ms. `mob.cpp` ทำให้ Poring Type 02 (`0x83`, มี MD_CANATTACK) เปลี่ยนเป้าหมายไปยังผู้โจมตีแม้ไม่มี MD_AGGRESSIVE.

ผลคำสั่งที่เวลา 8594ms ใช้ seed/counter จากเซฟ: ผู้เล่นโจมตีโดน 39 ที่ 9114ms (Poring เหลือ 16/55); AI เริ่มที่ 9200ms; Poring ตีโดน 3 ที่ 9872ms (ผู้เล่นเหลือ 42/45). การโจมตีของ Poring เป็น continuous ผ่าน `unit_attack(md, target, 1)` จึงบันทึกจุดเริ่มตีถัดไป 11072ms และกำหนดผลกระทบที่ 11744ms เป็น pending event; นาฬิกาแชทหยุดที่ 9872ms เพื่อรอคำสั่งผู้เล่น จึงยังไม่ทอยครั้งถัดไป.

การตรวจ: `python chat-rpg/runtime/early_combat.py` ผ่าน fixtures ของ damage, RNG replay, queue order/unknown-event guard และลำดับเวลาจริงข้างต้น. ขอบเขตที่ยังไม่มี: combat หลายคำสั่งต่อเนื่อง, ตาย, EXP/quest objective/wood, item pickup/use, regeneration, เคลื่อนที่/หนีระหว่างสู้ และบัฟหมดอายุระหว่าง combat. ห้ามใช้ผลของส่วนเหล่านี้ก่อนตรวจและเชื่อมเพิ่ม.
