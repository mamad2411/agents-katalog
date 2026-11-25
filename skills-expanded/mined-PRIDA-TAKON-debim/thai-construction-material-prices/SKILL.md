---
name: thai_construction_material_prices
description: Query, search, and benchmark Thai construction material prices (ราคาวัสดุก่อสร้างกระทรวงพาณิชย์) by material keyword, province, year, and month using official data from yotathai.com / TPSO.
---

# 🏗️ Thai Construction Material Prices Skill (ราคาวัสดุก่อสร้างกระทรวงพาณิชย์)

Skill นี้ใช้สำหรับค้นหาและตรวจสอบราคาวัสดุก่อสร้างมาตรฐานในประเทศไทย อ้างอิงจากฐานข้อมูลดัชนีราคาของกระทรวงพาณิชย์ (สำนักงานนโยบายและยุทธศาสตร์การค้า - TPSO) ผ่าน `yotathai.com`

---

## 🎯 กรณีที่ควรเรียกใช้ Skill นี้:
1. เมื่อผู้ใช้ต้องการทราบราคาวัสดุก่อสร้าง เช่น หินคลุก, ดินถม, คอนกรีตผสมเสร็จ, เหล็กเส้น, ไวร์เมช, ท่อ HDPE, สายไฟ ฯลฯ
2. เมื่อผู้ใช้ต้องการทำประมาณการราคา (Estimate), คิดราคากลางราชการ, หรือจัดทำเอกสาร BOQ
3. เมื่อต้องการเปรียบเทียบราคาวัสดุก่อสร้างระหว่างจังหวัด หรือตรวจเช็คราคาของจังหวัดใดจังหวัดหนึ่งโดยเฉพาะ

---

## 💻 วิธีการรันคำสั่ง (CLI Tool):
สคริปต์หลักตั้งอยู่ที่:
`python skills/thai_construction_material_prices/scripts/search_material_price.py [keyword] [options]`
*(หรืออ้างอิงผ่าน global config: `python "%USERPROFILE%\.gemini\config\skills\thai_construction_material_prices\scripts\search_material_price.py"`)*

### ตัวเลือกที่สามารถใช้ได้:
* `[keyword]`: คำค้นหาชื่อวัสดุ (เช่น `หินคลุก`, `คอนกรีต 240`, `เหล็กข้ออ้อย`, `HDPE`)
* `-p, --province`: ชื่อจังหวัดหรือรหัสจังหวัด (ค่าเริ่มต้นคือ `ส่วนกลาง` / กรุงเทพฯ รองรับทั้ง 77 จังหวัด เช่น `-p เชียงใหม่`, `-p ชลบุรี`, `-p โคราช`)
* `-y, --year`: ปี พ.ศ. (ค่าเริ่มต้นคือปีปัจจุบัน เช่น `-y 2567`)
* `-m, --month`: เดือน 1-12 (ค่าเริ่มต้นคือ `6`)
* `-l, --limit`: จำนวนรายการสูงสุดที่แสดงผล (ค่าเริ่มต้นคือ `20`)
* `--json`: แสดงผลลัพธ์ในรูปแบบ JSON สำหรับนำไปประมวลผลต่อ

---

## 📌 ตัวอย่างการใช้งานสำหรับ AI Agent:
1. **ค้นหาคอนกรีตในชลบุรี:**
   ```powershell
   python skills/thai_construction_material_prices/scripts/search_material_price.py "คอนกรีต 240" -p "ชลบุรี"
   ```
2. **ค้นหาหินคลุกส่วนกลาง:**
   ```powershell
   python skills/thai_construction_material_prices/scripts/search_material_price.py "หินคลุก" -p "ส่วนกลาง"
   ```
3. **ค้นหาเหล็กเส้นและดึงแบบ JSON เพื่อนำไปคิด BOQ:**
   ```powershell
   python skills/thai_construction_material_prices/scripts/search_material_price.py "เหล็กข้ออ้อย DB12" --json
   ```

---

## 🛡️ ฟีเจอร์พิเศษ:
* **Auto-Fallback to Central:** หากค้นหาในจังหวัดที่เลือกแล้วไม่พบรายการ (เนื่องจากพาณิชย์จังหวัดนั้นไม่ได้สำรวจวัสดุเฉพาะทางตัวนั้น) สคริปต์จะค้นหาราคาของ "ส่วนกลาง" มาแสดงเป็นราคาอ้างอิงให้ทันที พร้อมแจ้งเตือนให้ทราบ
* **Local Caching:** มีระบบ Cache ข้อมูลรายเดือน/จังหวัดในโฟลเดอร์ `cache/` เพื่อลดโหลด API และทำให้การค้นหาซ้ำทำได้อย่างรวดเร็ว
