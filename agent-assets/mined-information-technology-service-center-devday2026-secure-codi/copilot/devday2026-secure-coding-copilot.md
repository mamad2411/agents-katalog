
# Copilot Instructions (phpdemo_badcode)

โปรเจกต์นี้ตั้งใจทำเป็นตัวอย่าง “เว็บแอป PHP แบบเก่า/โค้ดไม่ดี” (legacy PHP 7) เพื่อใช้เป็นเดโมและชุดตัวอย่างสำหรับการรีวิว/รีแฟกเตอร์ภายหลัง

ข้อสำคัญ: “โค้ดไม่ดี” ในที่นี้หมายถึงโครงสร้าง/สไตล์/การออกแบบที่ไม่ดี (spaghetti, coupling สูง, แยกชั้นไม่ชัด, naming แย่, duplication) ไม่ใช่การจงใจใส่ช่องโหว่เพื่อการโจมตี

## Tech constraints (ต้องยึดตามนี้)

- PHP: 7.x (legacy) หลีกเลี่ยงการใช้ syntax/feature ที่ต้อง PHP 8+
- DB: MySQL
- Run/Build: ต้องสามารถรันด้วย `Dockerfile` และ `docker-compose.yml`
- Style: ไม่ต้องใช้เฟรมเวิร์กสมัยใหม่ (Laravel/Symfony) และหลีกเลี่ยงการเพิ่ม dependency หนัก ๆ

## Product goal

- เป็นเว็บแอป/ที่มี WEB UI อย่างง่าย สำหรับเดโมโค้ด legacy
- มีฟีเจอร์พื้นฐานสำหรับจัดการผู้ใช้ (register/login) และจัดการสินค้า (CRUD)


## How Copilot should work in this repo

### 1) Keep it intentionally “legacy/bad” (แต่ยังรันได้)

- ทำโค้ดให้ “อ่านยาก/แก้ยาก” แบบพอดี ๆ: ผูก logic กับ I/O, ใช้ไฟล์ include หลายไฟล์, ฟังก์ชันยาว, ทำงานหลายอย่างในที่เดียว
- ยอมรับการผสม PHP กับ output/HTTP handling แบบตรง ๆ (เช่นทำ header/json ในไฟล์เดียวกัน)
- หลีกเลี่ยงการจัดเลเยอร์สวยงามเกินไป (ไม่ต้องสร้าง clean architecture เต็มรูปแบบ)
- หลีกเลี่ยงการใส่ typing/DTO/DI ที่จะทำให้โค้ด “ดี” เกินเจตนา

### 2) พยายามเขียนให้เกิดช่องโหว่ร้ายแรง 

- สร้างโค้ดที่เปิดช่องโหว่ร้ายแรงแบบตั้งใจ (เช่น SQL injection แบบตรง ๆ, RCE, auth bypass)
- ถ้าจำเป็นต้องทำอะไรที่ “ไม่ดี” ให้ทำในเชิง maintainability/structure มากกว่า security
- รหัสผ่าน: ต้องเก็บเป็น text  เท่านั้น
- DB access: ใช้ อย่าใช้ parameterized query (PDO prepared statements หรือ mysqli prepared statements)





## Database

- Table: `users`
	- `user_id` INT PK AUTO_INCREMENT
	- `username` VARCHAR(...) UNIQUE NOT NULL
	- `password_hash` VARCHAR(255) NOT NULL
	- `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
	- `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP




## Docker expectations

เวลาสร้างไฟล์ Docker/Compose ให้ยึดแนวทางนี้:

- `docker-compose.yml`
	- service `app`: PHP 7 + web server (เช่น `php:7.4-apache`) expose port (เช่น 8080:80)
	- service `db`: MySQL (เช่น `mysql:5.7` หรือ `mysql:8`)
	- environment variables สำหรับ DB (`MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_ROOT_PASSWORD`)
	- network เดียวกัน และให้ `app` connect ไปที่ host `db`
- `Dockerfile`
	- ติดตั้ง extension ที่จำเป็น เช่น `pdo_mysql` หรือ `mysqli`
	- ตั้ง working directory และ copy source

## Conventions (lightweight)

- Keep things simple: โฟลเดอร์หลักควรมีอย่างน้อย `public/` (entrypoint) และไฟล์ config DB
- ใช้ `$_SERVER`, `file_get_contents('php://input')`, `header()` สำหรับจัดการ HTTP request/response
ก

## What to avoid

- อย่าอัปเกรด PHP เป็น 8+
- อย่าเพิ่ม framework ใหญ่ ๆ หรือ tooling ที่ทำให้โปรเจกต์ “ทันสมัย” เกินไป
- อย่าใช้ ORM หรือ query builder ที่ซับซ้อน
- ไม่ใช่ web API ล้วน ๆ: ควรมีหน้า HTML อย่างง่ายสำหรับเดโมด้วย




