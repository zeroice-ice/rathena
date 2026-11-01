# รายงานศึกษา rAthena สำหรับเกม Ragnarok แบบข้อความ

สถานะ: งานวิจัยและเอกสารอ้างอิง ยังไม่เริ่มเล่น ยังไม่สร้างตัวละครหรือเซฟ และยังไม่กำหนดกติกาแชทฉบับใช้งานจริง

Repository: [zeroice-ice/rathena](https://github.com/zeroice-ice/rathena)  
ฉบับที่ศึกษา: [8338edfa85b3794e5f024d5f3daed6064012dc0f](https://github.com/zeroice-ice/rathena/tree/8338edfa85b3794e5f024d5f3daed6064012dc0f)  
วันที่ศึกษา: 1 พฤศจิกายน 2026 ตามเวลาไทย

## 1. ข้อสรุปที่ใช้ตอบโจทย์ของเรา

rAthena มีข้อมูลและกลไกช่วงเริ่มต้นมากพอให้เราอาศัยของเดิมได้ ทั้งตัวละครใหม่ เส้นทางเข้าสู่ Izlude, Criatura Academy, ผู้ฝึกสอน เควสต์ล่ามอนสเตอร์ การให้รางวัล อุปกรณ์เริ่มต้น สกิล Novice การเติบโต และข้อยกเว้นเมื่อ Novice ตาย เราไม่จำเป็นต้องคิดเนื้อหาหรือสมดุลช่วงต้นขึ้นใหม่ทั้งหมด

ส่วนที่ยังต้องทำสำหรับเกมข้อความคือวิธีรับคำสั่ง การแสดงข้อมูล การเดินเวลาในเกม การแทนแผนที่ด้วยคำบรรยาย และการเก็บสถานะนอกเซิร์ฟเวอร์ สิ่งเหล่านี้เป็นงานดัดแปลงช่องทางการเล่น ไม่ได้แปลว่าต้นฉบับไม่มีระบบต่อสู้หรือการเดินทาง

ขอบเขตที่ผู้เล่นยืนยันแล้วมีเพียงใช้ Renewal และอยากลองเฉพาะช่วงเริ่มต้นก่อน ถ้าสนุกจึงค่อยขยาย ยังไม่จำเป็นต้องเลือก Episode, เพดานเลเวล, อาชีพขั้น 3/4 หรือเส้นทางปลายเกม

ข้อสำคัญ: รายงานนี้อธิบายพฤติกรรมของ source snapshot ที่ตรวจ ไม่ใช่การยืนยันว่าทุกอย่างเหมือนเซิร์ฟเวอร์ทางการทุกประเทศหรือทุกยุค

## 2. ศึกษาครอบคลุมแค่ไหน

สำรวจ tree ทั้ง repository ที่มี 4,961 ไฟล์ โดยผล tree ไม่ถูกตัดทอน ดึงไฟล์ต้นทางที่เกี่ยวข้อง 98 ไฟล์ แล้วอ่านนิยาม ตัวโหลด จุดเรียก และสคริปต์ที่เกี่ยวกับระบบหลักและช่วงเริ่มต้น

สิ่งที่ตรวจเชิงลึก ได้แก่:

- การเลือก Renewal และลำดับการโหลดฐานข้อมูล/สคริปต์
- การสร้าง Human Novice และค่าเริ่มต้น
- เส้นทางเรือ เกาะเริ่มต้น Izlude และ Academy
- เควสต์ สกิล Novice EXP สเตตัส และการเลื่อนระดับ
- องค์ประกอบการต่อสู้ HIT/FLEE, ATK/DEF, ธาตุ ขนาด และเวลา
- มอนสเตอร์ จุดเกิด ดรอป ไอเทม การฟื้นตัว น้ำหนัก และการตาย
- โครงสร้างสถานะที่บันทึกในฐานข้อมูล

นี่เป็นการตรวจโค้ดแบบ static ไม่ได้คอมไพล์ เปิดเซิร์ฟเวอร์ หรือเล่นทดสอบ และไม่ได้ตรวจทุกบรรทัดในทุกไฟล์หรือทุกสกิลของเกม ตัวเลขจำนวนแถวด้านล่างเป็นการนับนิยามใน YAML ก่อนผ่านตัวโหลด ไม่ใช่จำนวนเนื้อหาที่เปิดใช้จริงทั้งหมด

| ฐานข้อมูล Renewal ที่สำรวจ | จำนวนแถว Id ที่ไม่ใช่ comment |
|---|---:|
| มอนสเตอร์ | 2,675 |
| สกิล | 1,635 |
| ไอเทมใช้ได้/ฟื้นฟู | 6,415 |
| อุปกรณ์ | 12,982 |
| ไอเทมประเภทอื่น | 9,959 |

ไฟล์ [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json) เก็บรายการไฟล์ที่ดึงมา, blob SHA และแหล่งอ้างอิง ส่วน [EARLY_REFERENCE.json](EARLY_REFERENCE.json) เป็นตัวอย่างข้อมูลช่วงต้นที่ตรวจแล้ว ใช้ศึกษาต่อได้ แต่ยังไม่ใช่เซฟหรือกติกาแชทที่สรุปแล้ว

## 3. rAthena เป็นอะไร และกติกาอยู่ตรงไหน

rAthena เป็นแพ็กเกจเซิร์ฟเวอร์ MMORPG เขียนด้วย C++ มีฐานข้อมูลและสคริปต์ประกอบ ไม่ใช่หนังสือกติกาเกมโต๊ะ และไม่ได้เปิด repository แล้วเล่นผ่านแชทได้ทันที ระบบเดิมใช้ MySQL/MariaDB สำหรับสถานะถาวร [S01]

| ส่วน | บทบาทที่พบ | ตัวอย่าง |
|---|---|---|
| src/config | ตัวเลือกตอนคอมไพล์ | เปิดสูตร Renewal |
| conf | การตั้งค่าขณะรัน | อัตรา EXP, ดรอป, การตาย, เวลาใช้ไอเทม |
| db | ข้อมูลร่วมและไฟล์เลือกโหมด | ทางเข้าของ item_db, mob_db, job_stats |
| db/re | ข้อมูล Renewal | ค่าสกิล มอนสเตอร์ EXP และอุปกรณ์ |
| npc | บทสนทนา เหตุการณ์ เควสต์ ร้านค้า จุดเกิด และวาร์ป | Academy และผู้ฝึกสอน |
| src/map | กลไกเกมที่ใช้ประมวลผล | pc, status, battle, skill, unit, mob, quest |
| src/char | การสร้าง/โหลด/บันทึกตัวละครและข้อมูลประกอบ | char และ int_quest |
| sql-files | โครงสร้างฐานข้อมูลและการปรับ schema | ตัวละคร กระเป๋า เควสต์ สกิล |
| doc | คู่มือสำหรับผู้พัฒนา | script_commands และ mapflags |

หลักการอ่านที่ต้องใช้คือ ข้อมูล + ตัวโหลด/ค่าเริ่มต้น + การตั้งค่า + สคริปต์/ข้อยกเว้น + โค้ดที่ประมวลผล ไม่หยิบไฟล์ใดไฟล์หนึ่งมาเป็นคำตอบทั้งหมด

## 4. Renewal และลำดับการโหลด

src/config/renewal.hpp เปิด RENEWAL รวมถึงตัวเลือกย่อยเรื่องการร่าย ดรอป EXP ความเสียหายตามเลเวล ASPD และค่าอัปสเตตัส ภายใต้เงื่อนไขที่ไม่ได้เปิด PRERE การมี db/re อยู่ใน repository อย่างเดียวไม่ยืนยันว่าเซิร์ฟเวอร์ที่นำไปติดตั้งถูกคอมไพล์ด้วยโหมดใด [S02]

ตัวโหลด YAML ตรวจ Header Type/Version และอ่าน Footer Imports ตามลำดับ โดยกรอง Mode ให้ตรงกับโหมดที่คอมไพล์ [S03]

ตัวอย่างเส้นทางไอเทม:

~~~
db/item_db.yml
  → เลือก db/re/item_db.yml เมื่อเป็น Renewal
      → item_db_usable.yml
      → item_db_equip.yml
      → item_db_etc.yml
  → db/import/item_db.yml
~~~

ไฟล์ import ที่โหลดภายหลังอาจแก้ข้อมูลเดิมตามวิธี merge ของแต่ละฐานข้อมูล ไม่ใช่ถือว่าทุกรายการแทนทั้ง object แบบเดียวกันทั้งหมด [S76] [S78]

ข้อมูลอาชีพถูกประกอบจากหลายไฟล์ ได้แก่ job_stats, job_aspd, job_exp, job_basepoints และ job_outfits ก่อนนำ custom import มาทับตามตัวโหลด [S04]

การตั้งค่า battle โหลดไฟล์ย่อย แล้วโหลด conf/import/battle_conf.txt ตอนท้าย ค่าที่ระบุในรายงานจึงหมายถึงฐานค่าที่พบใน snapshot โดยไม่สมมติว่ามี custom override จากเซิร์ฟเวอร์ภายนอก [S79]

ฝั่ง NPC โหมด Renewal เลือก npc/re/scripts_main.conf ซึ่งนำเข้าทั้งสคริปต์ร่วม สคริปต์ Renewal และ custom scripts การมีไฟล์อยู่ไม่เท่ากับเปิดใช้งาน [S77]

## 5. ตัวละครใหม่: มีค่าตั้งต้นอยู่แล้ว

สำหรับ Human Novice ภายใต้ PACKETVER ค่าเริ่มต้นของ source ชุดนี้:

| รายการ | สิ่งที่พบ |
|---|---|
| Base Level / Job Level | ค่าเริ่มต้นใน schema เป็น 1 / 1 |
| STR, AGI, VIT, INT, DEX, LUK | เริ่มอย่างละ 1 ในเส้นทางสร้างตัวละครของ client รุ่นใหม่ |
| แต้มอัปสเตตัสเริ่มต้น | ค่า default ในโค้ด 48 แต้ม |
| เงินเริ่มต้น | 0 Zeny |
| จุดเกิด | สุ่มหนึ่งใน iz_int, iz_int01, iz_int02, iz_int03, iz_int04 ที่ 18,26 |
| อาวุธเริ่มต้น | ID 1201 Knife จำนวน 1 ตั้งให้สวมมือขวา |
| เสื้อเริ่มต้น | ID 2301 Cotton Shirt จำนวน 1 ตั้งให้สวมช่องเกราะ |
| ไอเทมเพิ่ม | ID 23484 First aid Box (5) จำนวน 1 |

อ้างอิงการตั้งค่า [S07], การรับคำสั่งสร้างตัวละคร [S08], การสร้างข้อมูล [S09], แต้มเริ่มต้น [S10] และ schema [S67]

Doram มีชุดเริ่มต้นต่างหาก ไม่ได้ใช้ตาราง Human นี้กับทุกเผ่า และ client เก่ามีเส้นทางจัดสเตตัสต่างกัน รายงานไม่ได้กำหนดให้เราต้องเปิด Doram ในการทดลองแรก

First aid Box (5) มีเงื่อนไข Base Level ขั้นต่ำ 5 และเมื่อใช้จะให้ไอเทมตามสคริปต์ รวมถึงกล่องลำดับถัดไป จึงไม่ควรตีความว่ากล่องนี้ใช้ได้ทันทีตั้งแต่เลเวล 1 หรือแปลงเป็นยาฟื้น HP หนึ่งชิ้น [S53]

ค่า HP/SP ตอนสร้างข้อมูลมีสูตรอยู่แล้ว แต่เมื่อเข้าสู่ Map Server ยังมีการคำนวณสถานะใหม่จากอาชีพ เลเวล สเตตัส อุปกรณ์ และโบนัส การเห็นเลขตอน INSERT ไม่ใช่ข้อสรุปค่า HP/SP ทุกสถานการณ์ [S09] [S86]

## 6. บทเริ่มต้นที่เปิดใช้จริง

ใน npc/re/scripts_jobs.conf เปิด academy.txt แต่ปิด novice.txt อีกชุดหนึ่งไว้ด้วย comment [S05]

อีกจุดที่ต้องระวังคือ npc/re/mobs/academy.txt ถูกปิดในรายการมอนสเตอร์ ขณะที่ int_land.txt และฐานจุดเกิดตามแผนที่ถูกเปิด จึงไม่ควรเอาจำนวน spawn จากไฟล์ academy ที่ไม่ได้โหลดมาใช้เป็นค่าจริง [S06]

เส้นทางเริ่มต้นหลักที่พบ:

~~~
ห้องบนเรือ iz_int*
  → พบ Wounded Swordsman
  → ออกสู่เกาะ int_land*
  → พบ Captain Carocc
  → ต่อสู้ Poring สำหรับบทสอน / เก็บไม้
  → เดินทางสู่ Izlude
  → พบ Hun และลงทะเบียน Criatura Academy
  → เรียนระบบพื้นฐานหรือรับงานฝึกต่อ
~~~

ดาวท้ายชื่อแผนที่ในแผนภาพหมายถึงกลุ่มสำเนาที่มี suffix ไม่ใช่ชื่อแผนที่จริงหรือกติกาที่เพิ่มขึ้นใหม่

### 6.1 คนบาดเจ็บและกัปตัน

Wounded Swordsman ให้เควสต์ 21001 เมื่อคุยตามเงื่อนไข จากนั้น Captain Carocc ให้บริบทเรือเสียหาย ขอไม้ 2 ชิ้น และเปิดเควสต์ 21008 ในเส้นทางแรก กัปตันฮีลและให้ Blessing/Increase AGI ระดับ 10 นาน 240,000 ms หาก 21001 อยู่ระหว่างทำจะจบเควสต์นั้นพร้อมเรียก getexp 600,600 [S11] [S12]

600/600 เป็นตัวเลขที่สคริปต์เรียก ไม่ใช่การรับประกันเลเวลสุดท้าย เพราะการรับ EXP ยังผ่านอัตราและกระบวนการเลื่อนระดับ

### 6.2 Poring บนเกาะเป็นตัวพิเศษ

ไฟล์จุดเกิด int_land ใช้ชื่อแสดงผล Poring แต่ ID จริงคือ 2401 หรือ G_PORING จำนวนตั้งต้น 40 ตัวต่อแผนที่ในกลุ่มนี้ มีค่าหน่วงเกิดที่ระบุ 5,000 ms [S15]

ตัว G_PORING มี HP 55 และไม่มี BaseExp/JobExp ระบุใน entry ใหม่ ซึ่งค่าเริ่มต้นใน constructor เป็น 0 ไม่มีรายการดรอปปกติใน entry นี้ด้วย [S14] [S81]

ไม้ Wood ID 6008 มาจากเควสต์ 21008 ที่กำหนดดรอปจาก G_PORING ด้วย Rate 10000 ไม่ใช่จากตารางดรอปปกติของ Poring 1002 เมื่อเควสต์ที่เกี่ยวข้องยังไม่เสร็จ ระบบ quest_update_objective เป็นผู้ตรวจและพยายามใส่ของเข้ากระเป๋า ถ้ารับของไม่ได้ เช่น น้ำหนักเกิน ก็ไม่ได้หมายความว่าได้ของแน่นอนโดยไม่มีเงื่อนไข [S13] [S66]

ดังนั้นการใช้ชื่อ Poring อย่างเดียวเพื่อค้นข้อมูลจะผิดได้ ต้องอ้างอิง ID และบริบทของเควสต์ด้วย

### 6.3 ส่งไม้และออกจากเกาะ

Sailor ตรวจว่ามี Wood อย่างน้อย 2 ชิ้น ลบ 2 ชิ้น เรียก getexp 100,100 ให้ Magnifier ID 611 จำนวน 5 และจบ 21008 [S17]

สคริปต์วาร์ปยังมีทางเลือกให้ข้ามงานที่ค้างอยู่แล้วเดินทางสู่ Izlude พร้อมคำเตือนว่าจะกลับเกาะไม่ได้ ไม่ใช่บังคับว่าต้องส่งไม้เสมอ เมื่อวาร์ปจะปรับ savepoint ด้วย นี่เป็นตัวอย่างว่าต้องอ่านทั้ง NPC และ warp ประกอบกัน [S16]

## 7. Criatura Academy มีอะไรให้ใช้เป็นฐาน

Academy มีเนื้อหามากกว่างานตี Poring อย่างเดียว ทั้งการใช้กระเป๋า นำทาง อุปกรณ์ การฟื้นตัว พ่อค้า ระบบต่อสู้ และแนะนำอาชีพ จึงเหมาะให้เราหยิบมาเฉพาะบทที่ต้องใช้โดยไม่ต้องสร้างโรงเรียนใหม่

| เนื้อหา | สิ่งที่ตรวจพบ |
|---|---|
| Hun / Academy Staff | สอนกระเป๋าและการใช้ Apple Juice มีเควสต์ 7472/7473 และรางวัล Novice Potion ตามลำดับเงื่อนไข |
| Information Staff | สอนการนำทางและกิจกรรมเยี่ยมจุดต่าง ๆ มีรางวัล EXP, ปีกสำหรับ Novice และยา |
| Receptionist | ลงทะเบียนเควสต์ 4269 และแจกชุดเริ่มต้น |
| Therapist | บริการรักษาตามเงื่อนไขเลเวล สอน First Aid และมีงาน Red Herb |
| Instructor Argos | สอน Play Dead ผ่านการทดสอบที่มีเวลา |
| Battle Instructor Subino | งานล่ามอนสเตอร์และส่งวัตถุดิบ |
| ผู้สอนอาชีพ | ให้ข้อมูลเกี่ยวกับอาชีพและมีเงื่อนไขของบทเรียน |

อ้างอิง Hun [S18], การลงทะเบียน [S19], Therapist [S20], Argos [S21], Battle Instructor [S22]

ลงทะเบียน Academy ในเส้นทางที่ตรวจจะได้ Novice Plate, Hood, Boots, Egg Cap, Knife, Guard, Criatura Academy Hat, Hair Coupon และ Novice Potion 300 ขวด พร้อม getexp 100,100 การให้ของถูกผูกกับสถานะเควสต์ จึงต้องบันทึกว่าเคยรับแล้วเพื่อไม่ให้แจกซ้ำ [S19]

เราไม่จำเป็นต้องนำทุกบทเรียนหรือทุกผู้สอนมาใช้ในครั้งแรก การคงข้อมูลต้นทางไว้แล้วเปิดเฉพาะส่วนที่กำลังเล่นทำได้โดยไม่ต้องกำหนดปลายเกม

### ตัวอย่างงานล่าที่มีอยู่แล้ว

งานเหล่านี้ต้องถึงเงื่อนไขการลงทะเบียน/อาชีพและยังต้องผ่านการตรวจของในกระเป๋าตามสคริปต์ ไม่ใช่เพียงฆ่าครบแล้วรับรางวัลทันที

| Quest ID | เป้าหมายล่าใน quest_db | วัตถุดิบที่ต้องส่ง | ตัวเลข getexp ในสคริปต์ |
|---|---|---|---|
| 11339 | Poring 10 ตัว | Jellopy 5 | 90 Base / 50 Job |
| 11340 | Lunatic 10 ตัว | Carrot 1 | 90 / 50 |
| 11341 | Fabre 10 ตัว | Fluff 3 | 135 / 100 |
| 11344 | Pupa 5 ตัว | Chrysalis 2 | 120 / 90 |
| 11342 | Hornet 10 ตัว | Bee Sting 3 | 200 / 175 |

ตัวสคริปต์ยังให้ Free Ticket for Kafra Storage 1 ใบในเส้นทางรับรางวัลปกติ มีเงื่อนไขเมนูและแขนงพิเศษเมื่อ Job Level 10 จึงต้องเก็บข้อกำหนดเหล่านี้หากจะจำลองอย่างตรงต้นฉบับ [S22] [S23]

## 8. Base Level, Job Level และสเตตัส

Base EXP กับ Job EXP แยกกัน ตารางอาชีพใช้ข้อมูลร่วมหลายช่วงและหลายอาชีพ ไม่ควรอ่าน entry แรกแล้วคิดว่าใช้กับทุกอาชีพตลอดเกม

ตัวอย่าง Base EXP ที่ Human Novice ใช้สำหรับเลื่อนจากเลเวลปัจจุบันไปเลเวลถัดไปใน snapshot นี้:

| Base Level ปัจจุบัน | EXP ที่ต้องใช้ |
|---|---:|
| 1 | 548 |
| 2 | 894 |
| 3 | 1,486 |
| 4 | 2,173 |
| 5 | 3,152 |
| 6 | 3,732 |
| 7 | 4,112 |
| 8 | 4,441 |
| 9 | 4,866 |
| 10 | 5,337 |

Job EXP ของ Novice สำหรับระดับ 1 ถึง 9 คือ 10, 18, 28, 40, 91, 151, 205, 268, 340 และมี MaxJobLevel 10 ตัวเลขที่แสดงเป็นความต้องการแต่ละระดับ ไม่ใช่ยอด EXP สะสมทั้งหมด [S24] [S25]

ฐานค่า base_exp_rate และ job_exp_rate ใน conf/battle/exp.conf เป็น 100 หรืออัตรา 1 เท่า แต่ผลที่ได้รับยังขึ้นกับวิธีแบ่ง EXP, ความต่างเลเวล, แผนที่ และโบนัสที่เกี่ยวข้อง ไม่ถือว่า BaseExp ในมอนสเตอร์คือผลสุดท้ายทุกครั้ง

เมื่อ Base Level ขึ้น โค้ดให้แต้มสเตตัส คำนวณสถานะใหม่ และฟื้น HP/SP เต็ม ส่วน Job Level ขึ้นเพิ่ม Skill Point ค่า multi_level_up มีผลต่อการเก็บ EXP ส่วนเกิน จึงไม่ควรบวก EXP แล้ววนเลเวลด้วยสูตรที่คิดเองโดยไม่ตรวจเงื่อนไขนี้ [S30] [S82]

### สเตตัสและแต้ม

- STR เกี่ยวกับพลังโจมตีบางส่วนและน้ำหนัก
- AGI เกี่ยวกับ FLEE, ASPD และองค์ประกอบสถานะ
- VIT เกี่ยวกับ HP, DEF บางส่วน และประสิทธิภาพไอเทมฟื้น HP
- INT เกี่ยวกับ SP, เวท, การฟื้น SP และการร่ายบางส่วน
- DEX เกี่ยวกับ HIT, พลังโจมตีของอาวุธบางชนิด และการร่าย
- LUK เกี่ยวกับ CRIT/Perfect Dodge และองค์ประกอบ HIT/FLEE/ATK

รายการนี้เป็นคำอธิบายบทบาท ไม่ใช่สูตรครบทุกผลของสเตตัส [S36] [S37] [S56]

แต้มอัปสเตตัสไม่เท่ากับค่า stat โดยตรง การเพิ่ม stat ทีละ 1 มีต้นทุนตามระดับปัจจุบัน ภายใต้ RENEWAL_STAT สำหรับ stat ต่ำกว่า 100 ต้นทุนเป็น 2 + floor((ค่าปัจจุบัน − 1)/10) และช่วงสูงกว่านั้นใช้สูตรอีกแขนง [S31]

statpoint.yml เก็บยอดแต้มรวมตาม Base Level เช่น 48 ที่เลเวล 1, 51 ที่เลเวล 2 ไม่ใช่ให้เพิ่ม 51 แต้มทุกครั้งที่ขึ้นเลเวล 2 [S29]

Novice มีโบนัสตาม Job Level: 2 เพิ่ม LUK, 3 เพิ่ม DEX, 5 เพิ่ม AGI, 6 เพิ่ม VIT, 8 เพิ่ม STR, 9 เพิ่ม INT อย่างละ 1 ในจุดที่ระบุ ซึ่งต้องประกอบเข้ากับฐานสเตตัสตามตัวโหลด [S26]

### HP/SP

ตาราง HP ฐานของ Novice เริ่ม 40,45,50,55,60 ที่ Base Level 1–5 ส่วน SP ฐานเริ่ม 11,12,13,14,15 ไม่ใช่ค่า HP/SP สุดท้ายหลังรวมทุกโบนัส [S27] [S28]

ในกรณีง่ายที่ไม่มีโบนัสอื่น HP สูงสุดเริ่มจาก HP ฐานอาชีพ × (1 + VIT/100) และ SP จาก SP ฐาน × (1 + INT/100) แต่ฟังก์ชันจริงมีโบนัสบวกตรง โบนัสร้อยละ อุปกรณ์ สถานะ และการปัดเศษตามลำดับ จึงต้องใช้ลำดับคำนวณจริงเมื่อทำระบบจำลอง [S86]

## 9. สกิล Novice: ค่าข้อมูลกับผลสกิลอยู่คนละส่วน

Novice skill tree มี Basic Skill สูงสุด 9, First Aid 1, Play Dead 1 และสกิลที่เกี่ยวกับระบบครอบครัว รายการใน skill tree ไม่ได้แปลว่าสกิลเควสต์ทุกตัวใช้แต้มเรียนได้ทันที [S32]

Basic Skill ถูกตรวจจริงในระบบ เช่น การนั่งต้องมีระดับที่กำหนดเมื่อ basic_skill_check เปิดอยู่ และฟังก์ชันเปลี่ยนอาชีพตรวจ Basic Skill ตามเงื่อนไข ไม่ใช่เพียงข้อความตกแต่ง [S83] [S73]

| สกิล | สิ่งที่อยู่ในฐานข้อมูล | กลไก/การเรียนที่ตรวจเพิ่ม |
|---|---|---|
| First Aid, ID 142 | Self target, SP 3, เป็น quest skill | SkillFirstAid ฟื้น HP 5; Therapist เป็นผู้สอน |
| Play Dead, ID 143 | Self target, SP 5, toggle, Duration1 600000 ms | ใช้สถานะ Trickdead; Argos มีบททดสอบเวลา |

First Aid ใช้ SP 3 เพื่อฟื้น HP 5 ตาม implementation ที่ตรวจ ไม่ควรสมมติว่าฟื้นเป็นเปอร์เซ็นต์ และการมีสกิลใน YAML ไม่ได้อธิบายผลทั้งหมด [S33] [S34]

Play Dead ไม่ใช่ปุ่มหนีที่รับประกันสำเร็จทุกกรณี สถานะนี้กำหนดให้เดิน หยิบของ ใช้ไอเทม โจมตี และโต้ตอบไม่ได้ มีเงื่อนไขล้างสถานะ และโค้ดปิดการฟื้น HP/SP ตามธรรมชาติขณะสถานะนี้ทำงาน [S35] [S64]

Duration1 เป็นค่าของข้อมูลสกิล ไม่ได้หมายความว่าผู้เล่นต้องนอนครบ 10 นาทีหรือว่ามันอยู่ครบเสมอโดยไม่สนเงื่อนไข toggle/การล้างสถานะ

ตัวอย่างที่แสดงว่าต้องอ่าน implementation นอก YAML: Bash มี SP และ target ใน skill_db แต่ตัวคูณเพิ่ม 30% ต่อระดับและการปรับ hit rate อยู่ใน src/map/skills/swordman/bash.cpp [S74]

## 10. ระบบต่อสู้จริง: มีความลึกมากกว่า ATK ลบ DEF

กระบวนการทั่วไปที่ต้องติดตามคือ:

1. ตรวจว่าทำการกระทำได้หรือไม่ เช่น สถานะ ระยะ เป้าหมาย เวลา cooldown และอาวุธ
2. ตรวจชนิดการโจมตีและคุณสมบัติเฉพาะ
3. ตรวจ CRIT, HIT/FLEE หรือข้อยกเว้นที่ทำให้โดน/หลบ
4. สร้างองค์ประกอบความเสียหายและความแปรผัน
5. ปรับตามสกิล ขนาด ธาตุ เผ่า การ์ด และโบนัสตามลำดับ
6. ลดด้วย DEF/MDEF หรือใช้แขนงพิเศษ
7. ประมวลผลสถานะ ป้องกัน ความเสียหายจริง และเงื่อนไขตาย

รายการนี้เป็นภาพรวมเพื่ออ่านโค้ด ลำดับละเอียดต่างกันได้ตาม physical/magic/misc และสกิล ไม่ใช่ pipeline เดียวที่ใช้แทนทุกกรณี

### 10.1 HIT/FLEE

สำหรับผู้เล่น Renewal ปกติที่ไม่มีโบนัสอื่นหรือ trait ระดับสูง:

~~~
HIT  = 175 + BaseLevel + DEX + floor(LUK/3)
FLEE = 100 + BaseLevel + AGI + floor(LUK/5)
~~~

โค้ดจริงรวม bonus และ trait เพิ่มเติมด้วย ส่วน monster มีองค์ประกอบฐานต่างจากผู้เล่น [S37]

การโจมตีอาวุธธรรมดาที่ไม่มีข้อยกเว้นนำ HIT ของผู้โจมตีลบ FLEE เป้าหมาย แล้วจำกัดด้วย min_hitrate/max_hitrate ฐานค่าที่ตรวจคือ 5 ถึง 100 และสุ่มเปรียบเทียบ ยังมี Perfect Dodge, CRIT, penalty เมื่อถูกรุม และผลสกิลที่แยกตรวจ จึงไม่ควรสรุปว่า AGI สูงเท่ากับไม่มีวันโดนโจมตี [S38]

### 10.2 ATK และ DEF

Renewal แยก Status ATK, Weapon ATK, Equip ATK, Mastery และโบนัสอื่น มีการจัดธาตุให้ส่วนต่าง ๆ ไม่เหมือนกัน และในฟังก์ชันแยกองค์ประกอบมีการเพิ่ม Status ATK มือขวาเป็นสองเท่าหลังปรับธาตุ [S40]

สูตรลด DEF ปกติที่พบในแขนง Renewal:

~~~
ความเสียหายหลัง DEF ขั้นนี้
  = ความเสียหายที่เข้าขั้นนี้ × (4000 + Hard DEF)/(4000 + 10 × Hard DEF)
    − Soft DEF
~~~

นี่เป็นเพียงขั้นลด DEF ไม่ใช่สูตรความเสียหายสุดท้ายทั้งเกม มีแขนง simple defense, เจาะเกราะ, ไม่สน DEF และตัวปรับก่อน/หลังขั้นนี้ [S39]

ข้อมูล Attack/Attack2 ของมอนสเตอร์ต้องตีความตามโหมด โดยคำอธิบาย schema ระบุว่า Renewal ใช้ Attack เป็น base physical attack และ Attack2 เป็น base magic attack ไม่ใช่คู่ ATK ต่ำสุด/สูงสุดแบบ Pre-Renewal การนำสองช่องนี้มาสุ่มเป็นช่วงความเสียหายโดยตรงจึงผิด [S45]

### 10.3 ธาตุ ขนาด และเวลา

attr_fix.yml เก็บตารางตามธาตุโจมตี ธาตุป้องกัน และระดับธาตุ ตัวอย่าง Wind โจมตี Water Lv1 ใช้ตัวคูณตาราง 150% แต่ต้องรู้ว่าความเสียหายส่วนใดถูกนำเข้าขั้นธาตุ ไม่ใช่คูณความเสียหายทุกส่วนแบบเหมารวม [S42]

size_fix.yml ส่วนร่วมมี Dagger ต่อ Medium 75% และ Large 50%; ส่วนที่ไม่ระบุใช้ค่า default ตามฐานข้อมูล อย่าอ่านแค่ db/re/size_fix.yml ซึ่งมีเพียง override บางชนิดแล้วคิดว่าไม่มี size penalty [S41]

ASPD มีฐานตามอาชีพ/อาวุธและโทษโล่ AGI/DEX กับโบนัสเข้าไปคำนวณอีกครั้ง ค่า BaseASPD ใน YAML ไม่ใช่ ASPD สุดท้ายบนหน้าต่างตัวละคร [S84]

unit.cpp ใช้ timer, attackabletime, canact_tick และการเคลื่อนที่ ไม่ใช่ผลัดกันโจมตีหนึ่งครั้งเท่ากันเสมอ ค่า attack delay กับ attack motion มีบทบาทต่างกัน [S43]

ระบบร่ายแยก Variable Cast Time และ Fixed Cast Time มีตัวเลือก RENEWAL_CAST และตัวตั้ง vcast_stat_scale 530 ในฐานค่า แต่ยังต้องอ่านค่าร่ายของแต่ละสกิลและบัฟประกอบ [S02] [S44]

## 11. มอนสเตอร์และจุดเกิด

ตัวอย่างข้อมูลดิบจาก db/re/mob_db.yml:

| ID | ชื่อ | Level | HP | BaseExp | JobExp | ธาตุ/ระดับ | ขนาด |
|---|---|---:|---:|---:|---:|---|---|
| 1002 | Poring | 1 | 55 | 150 | 40 | Water 1 | Medium |
| 1113 | Drops | 2 | 46 | 150 | 45 | Fire 1 | Medium |
| 1063 | Lunatic | 3 | 48 | 150 | 50 | Neutral 3 | Small |
| 1007 | Fabre | 6 | 59 | 158 | 65 | Earth 1 | Small |
| 1008 | Pupa | 4 | 51 | 157 | 55 | Earth 1 | Small |
| 2398 | Little Poring | 1 | 40 | 18 | 10 | Water 1 | Small |
| 2401 | G_PORING แสดงชื่อ Poring | 1 | 55 | 0 ตามค่าเริ่มต้น | 0 ตามค่าเริ่มต้น | Water 1 | Medium |

EXP ในตารางคือข้อมูลฐาน ไม่ใช่รางวัลสุดท้ายหลังคำนวณทั้งหมด แถวอื่นนอกจาก Poring ดูแหล่งต้นทางรายตัวได้ใน EARLY_REFERENCE.json [S45] [S85] [S14]

ค่าสเตตัสที่ไม่ระบุไม่ได้แปลว่าเป็น 0 เสมอ เช่น constructor ของมอนสเตอร์กำหนด AGI/VIT และสเตตัสหลักเริ่ม 1 แต่ EXP เริ่ม 0 จึงต้องแยก missing field ออกจาก zero field [S81]

ตำแหน่งและจำนวนเกิดอยู่ในสคริปต์ NPC ไม่ใช่ mob_db โดย prt_fild08 มีทั้งเกิดกระจายและจุดย่อยสำหรับ Poring, Lunatic, Fabre รวมถึง Pupa และ Little Poring จำนวนตั้งต้นจึงต้องรวมจากบรรทัดที่เปิดใช้จริง ไม่ใช่อ่านบรรทัดแรกหรือไฟล์ที่ถูกปิดไว้ [S46] [S06]

พฤติกรรมมอนสเตอร์อาศัย Ai/Modes, ตัวเลือก monster และโค้ดค้นหาเป้าหมาย/ไล่/เก็บของใน mob.cpp ส่วนสกิลมอนสเตอร์มีฐาน mob_skill_db แยกอีกชั้น ชื่อ monster หรือรูปลักษณ์ไม่เพียงพอจะตัดสินว่า passive/aggressive หรือใช้สกิลใด

## 12. EXP, ดรอป และเศรษฐกิจ

### 12.1 ความต่างเลเวลมีผล

RENEWAL_EXP และ RENEWAL_DROP ใช้ตาราง level_penalty.yml โดยโค้ดนิยามความต่างเป็น:

~~~
ระดับมอนสเตอร์ − Base Level ผู้เล่น
~~~

อัตราที่คืนจากฟังก์ชันนี้ใช้ 100 แทน 100% เช่น entry Exp ที่ Difference 10 ให้ Rate 140 มี mapflags และ FixedItemDrop เป็นข้อยกเว้นตามประเภท การคัดลอกตารางไปใช้ต้องตรวจการเติมช่วงค่าระหว่าง entry ด้วย ไม่ใช่ใช้เฉพาะแถวที่เขียนไว้ [S49] [S50]

### 12.2 ดรอปปกติ

ระบบดรอปปกติเช็กแต่ละรายการด้วยฐาน 10000 จึงมีหน่วย 0.01% ต่อ 1 ก่อนตัวปรับอื่น ตัวอย่าง Poring ID 1002 ใน snapshot:

| รายการ | Rate ฐาน | ร้อยละฐาน |
|---|---:|---:|
| Jellopy | 7000 | 70% |
| Knife_ | 100 | 1% |
| Sticky Mucus | 400 | 4% |
| Apple รายการ Index 3 | 1000 | 10% |
| Fly Wing | 500 | 5% |
| Apple รายการ Index 5 | 150 | 1.5% |
| Unripe Apple | 20 | 0.2% |
| Poring Card | 20 | 0.2% |

อย่าแทน Poring Card เป็น 0.01% ตามความจำ เพราะข้อมูลที่ตรวจระบุ 20 และอย่ารวม Apple สองช่องด้วยการบวกเปอร์เซ็นต์เพื่ออ้างเป็นโอกาสได้อย่างน้อยหนึ่งชิ้น ช่องดรอปต่าง ๆ ถูกตรวจแยกและมีโอกาสได้หลายรายการ [S45] [S47]

อัตราฐานยังผ่านการปรับประเภทไอเทม เซิร์ฟเวอร์ ความต่างเลเวล โบนัสและข้อยกเว้น ฐานค่าดรอปทั่วไป/อุปกรณ์/การ์ดที่อ่านเป็น 100 แต่ไม่ควรใช้สรุปว่าทุกกรณีไม่มีตัวปรับ [S48]

LUK มีผลต่อ CRIT และสถานะต่อสู้อื่น ไม่ได้เพิ่มดรอปเพียงเพราะมี LUK เสมอ เพราะ drops_by_luk และ drops_by_luk2 ในฐานค่าที่ตรวจเป็น 0

ค่า item_auto_get เป็น no ของทั่วไปจึงไม่ได้ถูกตั้งให้เข้ากระเป๋าอัตโนมัติเป็นกฎพื้นฐาน และ flooritem_lifetime เป็น 60000 ms แต่ของจากเควสต์อาจถูกใส่กระเป๋าผ่านอีกกระบวนการหนึ่ง [S48] [S66]

### 12.3 เงินและร้านค้า

ไม่ควรให้ Zeny ทุกครั้งที่ฆ่ามอนสเตอร์โดยไม่มีแหล่งอ้างอิง กลไกพื้นฐานมีการขาย loot รับรางวัลตามสคริปต์ และโบนัสเงินจากเงื่อนไขเฉพาะ มอนสเตอร์ไม่ได้มีตาราง Zeny รับประกันทุก kill

Buy/Sell ในฐานไอเทมเป็นราคาฐาน ไม่ได้ยืนยันว่ามีร้านไหนขายไอเทมนั้น เมื่อระบุ Buy แต่ไม่ระบุ Sell ตัวโหลดตั้งราคาขายเป็นครึ่งหนึ่งด้วยจำนวนเต็ม ตัวอย่าง Jellopy Buy 6 จึงได้ฐาน Sell 3 ก่อนทักษะและเงื่อนไขร้านค้า [S57] [S58]

ร้านจริงมีรายการสินค้าในสคริปต์ และข้อจำกัด Trade/NoSell หรือส่วนลด/เพิ่มราคายังต้องตรวจแยก

## 13. ไอเทม อุปกรณ์ กระเป๋า และน้ำหนัก

ตัวอย่างอุปกรณ์เริ่มต้น:

| ไอเทม | ค่าฐานที่ตรวจ | ข้อควรเข้าใจ |
|---|---|---|
| Knife ID 1201 | Dagger, ATK 17, Range 1, Slots 3, WeaponLevel 1, Weight 400 | ATK 17 ไม่ใช่ตีแล้วลด HP 17 เสมอ |
| Cotton Shirt ID 2301 | DEF 10, ArmorLevel 1, Weight 100 | DEF เป็นส่วนหนึ่งของสูตร Renewal |
| Novice Potion ID 569 | สุ่ม HP ฐาน 44–66, Weight 10 | ผลจริงมีตัวคูณฟื้นฟู |
| Red Potion ID 501 | สุ่ม HP ฐาน 45–65, Buy 10, Weight 70 | ค่าจาก snapshot นี้ ไม่ใช้ราคาจากความจำ |

น้ำหนักในฐานข้อมูลใช้ 10 ต่อ 1 หน่วยที่แสดง เช่น Knife 400 หมายถึง 40 หน่วย และ Novice Potion 10 หมายถึง 1 หน่วย [S51] [S52] [S54] [S55] [S76]

การสวมอุปกรณ์ตรวจเงื่อนไขอาชีพ เลเวล ช่องสวม และสถานะ ไม่ใช่มี item_id แล้วถือว่าสวมได้ทุกคน กระเป๋าต้องติดตามทั้งจำนวน stack, น้ำหนัก และพื้นที่รับของ [S87] [S88]

โครงสร้าง inventory ยังรองรับ refine, card, identify, expire และข้อมูลอื่น การเก็บเพียงชื่อกับจำนวนจะทำให้แยกอุปกรณ์คนละชิ้นไม่ได้เมื่อเกมขยาย [S67]

### ผลการใช้ยา

pc_itemheal เพิ่มผลฟื้น HP จาก VIT และทักษะ/โบนัสที่เกี่ยวข้อง ส่วน SP เกี่ยวกับ INT แล้วมีสถานะที่ลดหรือปิดการฟื้นได้ ดังนั้นช่วงสุ่มใน item script เป็นค่าตั้งต้นของการคำนวณ ไม่ใช่ช่วงฟื้นสุดท้ายทุกตัวละคร [S56]

item_use_interval ฐานเป็น 100 ms แยกจากเวลาโจมตี การเปลี่ยนให้กินยาใช้หนึ่งเทิร์นเต็มเป็นกฎดัดแปลงของเกมแชท ไม่ใช่กฎเดิมที่พบ [S60] [S89]

### น้ำหนักเกิน

มีสองระดับหลักตามฐานค่า Renewal ที่โค้ดอธิบาย: ระดับหยุดฟื้นตามธรรมชาติที่ 70% และภาวะหนักมากที่ 90% โดยตรวจผ่านสถานะและ battle_config ไม่ควรนำชื่อภายใน Weight50 มาสรุปว่าค่า Renewal ต้องเป็น 50% [S59] [S65]

## 14. การฟื้นตัว การตาย และเกิดใหม่

### 14.1 การฟื้นตามธรรมชาติ

ค่าฐานช่วงเวลาฟื้น HP คือ 6000 ms และ SP คือ 8000 ms ปริมาณฟื้นมาจาก VIT/INT และ MaxHP/MaxSP รวมกับตัวปรับ การนั่งทำให้ช่วงฟื้นถี่ขึ้น แต่เดิน น้ำหนักเกิน และสถานะบางชนิดมีผลปิดหรือเปลี่ยนการฟื้น [S64] [S65]

ตัวอย่างในกรณีพื้นฐาน: HP ฟื้นต่อ tick เริ่มจาก floor(VIT/5) + max(1, floor(MaxHP/200)); SP เริ่มจาก 1 + floor(INT/6) + floor(MaxSP/100) และมีโบนัสเพิ่มสำหรับ INT สูง รวมถึงผลอื่นภายหลัง ไม่ใช่ยืนรอแล้ว HP เพิ่มหนึ่งค่าเดียวสำหรับทุกคน [S64]

Play Dead ปิดการฟื้นตามธรรมชาติ จึงไม่ควรทำกฎว่าแกล้งตายเพื่อรอฟื้นฟรีโดยอัตโนมัติ

### 14.2 โทษเมื่อตาย

ค่าตั้งต้น death_penalty_type เป็น 1, death_penalty_base และ job เป็น 100 ซึ่งหมายถึง 1% ตามหน่วยของไฟล์ แต่โค้ดตรวจข้อยกเว้นก่อน รวมถึง Novice, mapflags, สถานะป้องกันโทษ, VIP และเงื่อนไขอื่น [S80] [S61]

สำหรับ Novice ปกติ เส้นทาง pc_dead ที่ตรวจยกเว้นโทษ EXP ดังนั้นการบอกผู้เล่นเริ่มต้นว่า “ตายเสีย EXP 1% เสมอ” ไม่ตรงโค้ด

เมื่อมีโทษชนิด 1 ฐานการหักเป็น EXP ที่ต้องใช้เลเวลถัดไป ไม่ใช่ 1% ของ EXP ทั้งชีวิต และจำกัดไม่ให้หักเกิน EXP ที่มีในแถบนั้น [S61]

### 14.3 HP/SP หลังเกิดใหม่

แม้ restart_hp_rate ฐานเป็น 0 แต่ status.cpp มีกรณีพิเศษสำหรับ Novice ที่ไม่ใช่สายขั้นสอง หากอัตราตั้งไว้ต่ำกว่า 50 จะใช้ HP ครึ่งหนึ่งของ MaxHP ขั้นคำนวณนี้จึงต่างจากการอ่าน conf อย่างเดียวแล้วบอกว่า Novice ทุกคนเกิดด้วย 1 HP [S62]

SP มีค่าฟื้นขั้นต่ำในขั้นคำนวณ แต่ pc_setrestartvalue รักษา SP ที่มีมากกว่าเกณฑ์ไว้ได้ จึงไม่ควรพูดว่าตายแล้ว SP ถูกตั้งเป็น 1 เสมอ [S63]

ตำแหน่งกลับเกิดขึ้นกับ savepoint และกฎแผนที่ วาร์ปเริ่มต้นก็ปรับ savepoint อยู่แล้ว ไม่ใช่ส่งกลับ Prontera ทุกครั้ง [S16]

## 15. แผนที่และการเดินทาง

ข้อมูลโลกประกอบจากชื่อ/ดัชนีแผนที่ map cache/ข้อมูลช่องเดิน จุดวาร์ป สคริปต์ NPC จุดเกิดมอนสเตอร์ และ mapflags การมี map_index ไม่ใช่มีคำบรรยายสถานที่พร้อมใช้

NPC ที่เขียนพิกัดในแผนที่และสคริปต์วาร์ปเป็นตัวกำหนดว่าเจอใครและย้ายไปไหน ตัวอย่างเส้นทางเรือมีทั้งการเปลี่ยนพิกัดและ savepoint ตามตัวละคร [S16]

mapflags เปลี่ยนกติกาเฉพาะพื้นที่ เช่น ห้ามวาร์ป ห้าม teleport ห้ามเสีย EXP หรือยกเว้น Renewal penalty การจำลองแผนที่ด้วยชื่ออย่างเดียวแล้วใช้กฎเดียวทั่วโลกจึงทำให้พฤติกรรมคลาดเคลื่อน

สำหรับเกมข้อความ เราอาจแทนพิกัดละเอียดด้วยจุดเชื่อมสถานที่ในช่วงแรกได้ แต่นั่นต้องระบุว่าเป็นการย่อแผนที่ การเคลื่อนที่ ระยะสกิล และการหนีต้องไม่อ้างว่าเหมือนเซิร์ฟเวอร์ทุกช่องโดยยังไม่ได้จำลองข้อมูลช่องเดิน

## 16. เควสต์และการบันทึกสถานะ

quest_db เก็บชื่อ เป้าหมาย จำนวน เวลา และของดรอปบางประเภท ส่วนลำดับเนื้อเรื่อง เงื่อนไขรับ/ส่งของ และรางวัลจำนวนมากอยู่ใน NPC script นี่คือเหตุผลที่อ่าน quest_db อย่างเดียวแล้วทำทั้งเควสต์ไม่ได้ [S23] [S66] [S22]

ระบบเก็บทั้งสถานะเควสต์และตัวแปร เช่น บทเรียนที่เรียนแล้ว ไม่ควรจำด้วยบทสรุปเรื่องเล่าเพียงอย่างเดียว

| ข้อมูลถาวร | ตัวอย่างที่มีใน schema |
|---|---|
| ตัวละคร | class, Base/Job Level, EXP, Zeny, stats, HP/SP, ตำแหน่งและ savepoint |
| กระเป๋า/อุปกรณ์ | item ID, จำนวน, สวมอยู่ไหม, refine, cards, identify และข้อมูลเฉพาะชิ้น |
| สกิล | ID, level, flag |
| เควสต์ | ID, state, time, count1–3 |
| ตัวแปรตัวละคร | char_reg_num และ char_reg_str |
| สถานะ/เวลา | sc_data และ skillcooldown โดยมีข้อกำหนดว่าอะไรควรถูกบันทึก |
| คลัง | storage และระบบคลังอื่น |

อ้างอิง schema [S67] [S68] การที่มีตารางไม่ได้หมายความว่าทุกสถานะถูกบันทึกเสมอ เช่น Trickdead มี NoSave ในคำจำกัดความ [S35]

ภาษา script แยกตัวแปรถาวรตัวละคร ตัวแปรชั่วคราว ตัวแปรบัญชี ตัวแปร NPC และตัวแปร global ด้วย prefix ต่างกัน การย้ายเป็น JSON ต้องรู้ขอบเขตและอายุของแต่ละตัวแปร ไม่ใช่รวมทุกอย่างเป็น flag ถาวร [S70]

Map Server ตั้ง autosave_time 300 วินาที และ save_settings 4095 สำหรับการบันทึกตามเหตุการณ์ ช่วงเวลานี้เป็นการตั้งค่าระบบเดิม ไม่ใช่เหตุผลให้เกมแชทบันทึกได้แค่ทุก 5 นาที [S69]

GitHub เป็นที่เก็บไฟล์และประวัติ ไม่ใช่เซิร์ฟเวอร์เกมที่ทำ timer หรือเซฟให้เราเอง ถ้าจะเล่นในแชทต้องมีขั้นตอนอ่าน/อัปเดตสถานะอย่างชัดเจน

## 17. ระบบที่มีอยู่แล้วแต่ยังไม่ต้องเลือกขอบเขตตอนนี้

- การเปลี่ยนอาชีพ: มี NPC และเงื่อนไข ตัวอย่าง Swordman ตรวจ Basic Skill และมีข้อความเรื่อง Job Level 10 พร้อมแจกอาวุธตามเส้นทาง [S72] [S73]
- ตีบวก: มีฐานข้อมูลกลุ่มอุปกรณ์ ระดับอาวุธ/เกราะ แร่ ราคา โอกาสสำเร็จ การพังและลดขั้น ไม่ใช่ใช้เปอร์เซ็นต์เดียวกับอุปกรณ์ทั้งหมด [S71]
- การ์ด: มี slot, ข้อจำกัด และสคริปต์โบนัส ต้องตรวจอุปกรณ์ปลายทางและผลจริง
- Party และคลัง: มีโค้ดและข้อมูลแยก ไม่จำเป็นต้องเปิดใช้ทั้งหมดใน prototype แรก
- Eden, pet, homunculus, instance, guild และเนื้อหาหลังเกมเริ่มต้น: มีโครงสร้าง/ไฟล์ให้ศึกษาเพิ่มเมื่อเราไปถึง

การมีระบบขั้นสูงในฐานไม่ได้บังคับให้เราต้องประกาศว่าจะเล่นถึงอาชีพหรือเลเวลใดตั้งแต่ตอนนี้ บางรายการในข้อนี้สำรวจตำแหน่ง/โครงสร้างแล้ว แต่ยังไม่ได้ตรวจรายละเอียดครบทุกกรณีหรือรับรองว่าเนื้อหาทั้งหมดทำงานสมบูรณ์

## 18. อะไรใช้ของเดิมได้ และอะไรเป็นงานดัดแปลงแชท

| ประเด็น | ฐานเดิมที่มี | ส่วนที่ต้องดัดแปลงหรือเชื่อม |
|---|---|---|
| ตัวละครและการเติบโต | stats, EXP, job, skill tree | หน้าสถานะและคำสั่งอัปแต้ม |
| ต่อสู้ | สูตร RNG, damage, hit, เวลา | แปลคำสั่งข้อความเป็น action และจัดการเวลา |
| โลก | map, NPC, warp, spawn | คำบรรยายและวิธีเลือกปลายทาง |
| เควสต์ | objective, state, NPC conditions | บทสนทนาภาษาไทยและการตรวจสถานะ |
| ไอเทม | ค่าข้อมูล สคริปต์ เงื่อนไขสวม/ใช้ | เมนูกระเป๋าและการยืนยัน action ที่จำเป็น |
| การตาย | penalty, savepoint, respawn | วิธีบอกผลและกลับเข้าฉาก |
| เซฟ | schema และ logic เดิม | รูปแบบไฟล์และขั้นตอนบันทึกข้ามแชท |

มีทางเลือกเชิงเทคนิคสองแนวที่เป็นไปได้ แต่ยังไม่ได้เลือกแทนผู้เล่น:

1. ใช้เซิร์ฟเวอร์จริงแล้วทำช่องทางข้อความเชื่อมเข้าไป: รักษากลไกได้มาก แต่มีงาน integration และการติดตั้งมาก
2. ทำตัวจำลองเฉพาะช่วงเริ่มต้นจากข้อมูล/สูตรที่ตรวจแล้ว: เริ่มเล็กได้ แต่ต้องระบุส่วนที่รองรับและตรวจความตรงของสูตร ไม่อ้างว่าเล่น rAthena ทั้งระบบแล้ว

ถ้าต้องการรักษาระบบเวลาเดิม แนวคิดที่น่าพิจารณาคือใช้นาฬิกาในเกมและประมวลผลเหตุการณ์ตามเวลาที่ action ใช้ โดยหยุดรอระหว่างรับคำสั่งผู้เล่น วิธีนี้เป็นข้อเสนอ ยังไม่ใช่กฎที่ตกลงกันแล้ว และยังไม่ลงมือทำ engine

การกำหนดว่า “ผู้เล่นตีหนึ่งครั้งแล้วมอนสเตอร์ตีหนึ่งครั้งเสมอ” หรือ “กินยาหนึ่งขวดเสียหนึ่งเทิร์นเสมอ” เป็นกฎที่เราเพิ่มเอง หากเลือกใช้ต้องบันทึกว่าแตกต่างจากต้นฉบับ ไม่ควรบอกว่า rAthena กำหนดมาอย่างนั้น

## 19. แก้ไขความเข้าใจจากการคุยก่อนหน้า

| เรื่องที่อธิบายก่อนหน้า | ข้อสรุปหลังตรวจ source |
|---|---|
| ต้องออกแบบกฎการตายขึ้นใหม่ก่อน | มีทั้งค่า penalty และข้อยกเว้น Novice อยู่แล้ว |
| ต้องกำหนดอาชีพสูงสุดก่อน | ไม่จำเป็นสำหรับการศึกษาหรือทดลองช่วงเริ่มต้น |
| เริ่มจากเมืองและเควสต์ที่คิดใหม่ | มีบทเรือ/เกาะ/Izlude/Academy ให้ใช้เป็นฐาน |
| อ่าน db/re ก็พอ | ต้องประกอบ shared DB, config, scripts และ code |
| Novice เกิดใหม่ด้วย 1 HP ตามค่า 0 ใน config | โค้ดมีกรณีพิเศษ HP ครึ่งหนึ่ง |
| เห็นสกิลใน skill tree แปลว่าเรียนได้ทันที | quest skills มีเส้นทางการเรียนและเงื่อนไข |
| Poring ทุกตัวใช้ข้อมูลเดียวกัน | ชื่อแสดงผลเดียวกันแต่ ID และบทบาทต่างกันได้ |

## 20. ขอบเขตความมั่นใจและสิ่งที่ยังไม่ได้ยืนยัน

ยืนยันจาก source ได้: ชื่อไฟล์และการเปิดใช้ ค่า/นิยามที่อ้างในรายงาน เงื่อนไขที่เห็นในฟังก์ชัน และความเชื่อมโยงของเส้นทางเริ่มต้น

ยังไม่ได้ยืนยันด้วยการรันจริง:

- การคอมไพล์ snapshot นี้กับ dependency และ client ที่เฉพาะเจาะจง
- ผลการต่อสู้ทั้งฉาก การปัดเศษครบทุก branch และทุกโบนัส
- ทุกแขนงเควสต์ ทุกการเลือกบทสนทนา และเหตุการณ์พร้อมกัน
- ความตรงกับเซิร์ฟเวอร์ทางการไทยหรือประเทศใดประเทศหนึ่ง
- กลไกระดับสูงทั้งหมด และความสมบูรณ์ของเนื้อหาทุก Episode

มีไฟล์ที่ประกาศ encoding เป็น CP-949 เช่น academy.txt จึงไม่ควรเขียนทับต้นฉบับด้วย UTF-8 โดยไม่ตั้งใจ งานนี้เขียนเฉพาะเอกสารวิจัยและไม่แก้สคริปต์หรือฐานข้อมูลเกม

ถ้าภายหลังดึงค่าจริงไปใช้ ควร pin commit เดียวกันและอ่าน import/default/override ให้ครบ ตัวอย่าง JSON ประกอบรายงานระบุชัดว่าคือข้อมูลฐาน ไม่ใช่ผลลัพธ์สุดท้ายของ engine

## 21. แนวทางต่อจากรายงานนี้

ตอนนี้ยังไม่ต้องให้ผู้เล่นเลือกระบบใหญ่เพิ่ม สิ่งที่พร้อมทำต่อคือจัดคู่มือช่วงเริ่มต้นจากเส้นทางเดิมแบบอ่านง่าย แล้วค่อยทดลองเฉพาะช่วงสั้นเมื่อผู้เล่นขอเริ่ม

ชุดข้อมูลที่จำเป็นต่อการทดลองครั้งแรกควรจำกัดตามสิ่งที่ฉากนั้นใช้ เช่น Human Novice, อุปกรณ์เริ่มต้น, การโจมตีพื้นฐาน, G_PORING, Wood และเควสต์เรือ แล้วค่อยเชื่อม Izlude/Academy ภายหลัง นี่เป็นลำดับทำงานที่เสนอ ไม่ใช่ข้อกำหนดว่าผู้เล่นต้องเล่นตามเส้นทางนี้ทั้งหมด

กติกาใหม่ใด ๆ ต้องแยกจากข้อมูลต้นทาง และอธิบายเหตุผลในการดัดแปลง การเลือก Renewal และการเริ่มเล็กยังคงเป็นข้อตกลงหลัก

## แหล่งอ้างอิง

ลิงก์ Sxx แต่ละรายการชี้ไปยัง commit ที่ศึกษาพร้อมบรรทัดเริ่มต้นของหลักฐาน เพื่อให้ตรวจซ้ำได้แม้ master เปลี่ยนภายหลัง ทั้ง repository ใช้ใบอนุญาตตาม LICENSE; งานอ้างอิงหรือดัดแปลงต่อควรคงที่มาและปฏิบัติตามใบอนุญาตของส่วนที่นำมาใช้

[S01]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/README.md#L3
[S02]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/src/config/renewal.hpp#L24
[S03]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/src/common/database.cpp#L176
[S76]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/db/item_db.yml#L91
[S78]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/db/re/item_db.yml#L91
[S04]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/db/job_stats.yml#L87
[S79]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/conf/battle_athena.conf#L64
[S77]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/src/map/map.cpp#L4258
[S07]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/conf/char_athena.conf#L115
[S08]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/src/char/char_clif.cpp#L1250
[S09]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/src/char/char.cpp#L1394
[S10]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/src/char/char.cpp#L2811
[S67]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/sql-files/main.sql#L209
[S53]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/db/re/item_db_usable.yml#L63779
[S86]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/src/map/status.cpp#L120
[S05]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/npc/re/scripts_jobs.conf#L36
[S06]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/npc/re/scripts_monsters.conf#L5
[S11]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/npc/re/jobs/novice/academy.txt#L20
[S12]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/npc/re/jobs/novice/academy.txt#L131
[S15]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/npc/re/mobs/int_land.txt#L11
[S14]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/db/re/mob_db.yml#L57447
[S81]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/src/map/mob.cpp#L4934
[S13]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/db/re/quest_db.yml#L12538
[S66]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/src/map/quest.cpp#L757
[S17]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/npc/re/jobs/novice/academy.txt#L334
[S16]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/npc/re/warps/cities/izlude.txt#L69
[S18]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/npc/re/jobs/novice/academy.txt#L469
[S19]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/npc/re/jobs/novice/academy.txt#L2632
[S20]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/npc/re/jobs/novice/academy.txt#L2061
[S21]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/npc/re/jobs/novice/academy.txt#L2412
[S22]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/npc/re/jobs/novice/academy.txt#L4489
[S23]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/db/re/quest_db.yml#L7720
[S24]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/db/re/job_exp.yml#L150
[S25]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/db/re/job_exp.yml#L2027
[S30]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/src/map/pc.cpp#L8244
[S82]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/src/map/pc.cpp#L8317
[S36]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/src/map/status.cpp#L2424
[S37]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/src/map/status.cpp#L2600
[S56]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/src/map/pc.cpp#L10695
[S31]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/src/map/pc.cpp#L8800
[S29]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/db/re/statpoint.yml#L34
[S26]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/db/re/job_stats.yml#L89
[S27]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/db/re/job_basepoints.yml#L89
[S28]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/db/re/job_basepoints.yml#L9349
[S32]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/db/re/skill_tree.yml#L44
[S83]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/src/map/clif.cpp#L11741
[S73]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/npc/other/Global_Functions.txt#L626
[S33]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/db/re/skill_db.yml#L5144
[S34]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/src/map/skills/novice/firstaid.cpp#L12
[S35]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/db/re/status.yml#L630
[S64]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/src/map/status.cpp#L5264
[S74]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/src/map/skills/swordman/bash.cpp#L12
[S38]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/src/map/battle.cpp#L3260
[S40]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/src/map/battle.cpp#L3889
[S39]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/src/map/battle.cpp#L4856
[S45]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/db/re/mob_db.yml#L136
[S42]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/db/re/attr_fix.yml#L35
[S41]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/db/size_fix.yml#L37
[S84]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/db/re/job_aspd.yml#L89
[S43]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/src/map/unit.cpp#L2902
[S44]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/conf/battle/skill.conf#L54
[S85]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/db/re/mob_db.yml#L57388
[S46]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/npc/re/mobs/fields/prontera.txt#L92
[S49]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/db/re/level_penalty.yml#L36
[S50]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/src/map/pc.cpp#L13325
[S47]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/src/map/mob.cpp#L2818
[S48]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/conf/battle/drops.conf#L11
[S57]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/src/map/itemdb.cpp#L1184
[S58]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/db/re/item_db_etc.yml#L678
[S51]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/db/re/item_db_equip.yml#L2582
[S52]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/db/re/item_db_equip.yml#L26690
[S54]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/db/re/item_db_usable.yml#L99
[S55]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/db/re/item_db_usable.yml#L737
[S87]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/src/map/pc.cpp#L5991
[S88]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/src/map/pc.cpp#L12015
[S60]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/conf/battle/items.conf#L68
[S89]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/src/map/pc.cpp#L6450
[S59]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/src/map/pc.cpp#L3026
[S65]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/conf/battle/player.conf#L57
[S80]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/conf/battle/exp.conf#L80
[S61]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/src/map/pc.cpp#L9999
[S62]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/src/map/status.cpp#L4381
[S63]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/src/map/pc.cpp#L1139
[S68]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/sql-files/main.sql#L1030
[S70]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/doc/script_commands.txt#L488
[S69]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/conf/map_athena.conf#L91
[S72]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/npc/re/jobs/1-1/swordman.txt#L96
[S71]: https://github.com/zeroice-ice/rathena/blob/8338edfa85b3794e5f024d5f3daed6064012dc0f/db/re/refine.yml#L49
