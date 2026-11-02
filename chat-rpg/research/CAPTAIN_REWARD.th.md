# รับรางวัลกัปตันครั้งแรก

Snapshot 8338edfa85b3794e5f024d5f3daed6064012dc0f; source rAthena Development Team, repository LICENSE.

academy.txt:133–194: เลือกรายงานคนที่ยังต้องการความช่วยเหลือ กัปตันบอกว่าจะส่งทีมช่วย; ขอ Wood 2 ชิ้นให้ลูกเรือทางใต้ ให้ heal 9999 HP, Blessing 10 และ Increase AGI 10 นาน 240000 ms; หาก 21001 active ให้ completequest และ getexp 600,600 จากนั้นเปิด 21008.

script.cpp:11142–11180 ใช้ quest_exp_rate; conf/battle/exp.conf quest_exp_rate=100, multi_level_up=no. pc.cpp:8244–8270 และ 8317–8344 จำกัด EXP ส่วนเกินเหลือความต้องการระดับเดิมลบ 1 เมื่อปิด multi_level_up. จาก Base1/Job1 EXP0 รับ600: Base2 EXP52/894, Job2 EXP9/18 (600-10 ถูก cap ที่9). ไม่ใช่ Job ขึ้นหลายระดับ. แต้มสถานะ48->51, skill point0->1. db/re/job_stats.yml:89 โบนัส Job2 LUK+1.

status.cpp:10846–10855 Increase AGI val2=2+level =12; :11567 Blessing val2=level=10 เพิ่ม STR/INT/DEX ผ่าน status calc. db/re/job_basepoints.yml Novice Base2 HP45 SP12; status_calc_maxhp_pc/maxsp_pc: VIT1 -> HP45, INT11 -> SP13 (truncate). Base level up recalc+full heal ก่อน job recalc. โบนัส Job2 เฉพาะ LUK ไม่เปลี่ยน HP/SP. สเตตัสจริงพร้อมบัฟ STR11 AGI13 VIT1 INT11 DEX11 LUK2; แต้มฐานยังอย่างละ1.

ข้อจำกัด: ตรวจเฉพาะแขนงรางวัลนี้ ไม่รับรอง combat engine. บทสนทนาหยุดเวลาเป็นส่วนดัดแปลงแชท. บัฟเริ่มที่นาฬิกาเกมปัจจุบันและหมดเมื่อเดินเวลาเกมอีก240000ms; เก็บ event หมดอายุในเซฟ. คำพูดส่งทีมช่วยไม่ใช่หลักฐานว่า NPC บาดเจ็บหายแล้ว.
