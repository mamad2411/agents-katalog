<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-guru200616
description: CTF writeups and security challenges by Guru200616.
---

# Writeups by Guru200616

Source repository: `/repos/Guru200616`

## Repository Index

- FUTURE_CS_01/README.md
- FUTURE_CS_01/report_task1.md
- FUTURE_CS_01/vulnerable_app/README.md
- FUTURE_CS_01/vulnerable_app/templates/vulnerable_app/templates/vulnerable_app/EXPLOITS.md
- FUTURE_CS_01/vulnerable_app/templates/vulnerable_app/templates/vulnerable_app/vulnerable_app/SECURE_FIX.md

## Writeup Content


### File: FUTURE_CS_01/README.md

# FUTURE_CS_01
Web application security testing — pentest notes, reports, PoCs and remediation for Task 1 (Future Interns CS).



### File: FUTURE_CS_01/vulnerable_app/README.md

# Vulnerable Web App - FUTURE_CS_01

This small Flask app intentionally includes vulnerabilities for learning:
- SQL Injection (login endpoint)
- Persistent XSS (comment posting, renders raw HTML)
- Weak authentication (plain-text password, no lockout)

## Run
1. Create a venv and install:
 2. Initialize DB and run:3. App served at http://127.0.0.1:5000



### File: FUTURE_CS_01/report_task1.md

# Task 1 - Web Application Security Testing

## 🔹 Objective
Perform security testing on a sample web application to identify vulnerabilities such as **SQL Injection, XSS, and Authentication flaws**.

## 🔹 Tools Used
- **Burp Suite Community Edition** – Proxy-based vulnerability scanning
- **OWASP ZAP** – Automated vulnerability scanner
- **SQLMap** – Automated SQL Injection testing tool
- **Browser DevTools** – Manual testing

---

## 🔹 Methodology

### 1. Reconnaissance
- Mapped application endpoints and parameters using Burp Suite Proxy.
- Identified login, search, and profile management pages as primary attack points.

### 2. SQL Injection Testing
- Used **SQLMap** against the login form.
- Payload used: `' OR '1'='1 --`
- Login bypassed successfully.

### 3. Cross-Site Scripting (XSS)
- Injected test payloads into search and comment fields:
  ```html
  <script>alert("XSS Test")</script>



### File: FUTURE_CS_01/vulnerable_app/templates/vulnerable_app/templates/vulnerable_app/EXPLOITS.md

# Exploits and Testing (PoC)

## SQL Injection (login)
The login endpoint is vulnerable because input is directly formatted into SQL.

Using sqlmap:To test authentication bypass:
You can also use curl to try inject:
## Stored XSS (comments)
1. Log in as `admin` / `admin123`.
2. Post this in comment box:
3. 3. The script will run for any visitor (stored XSS).

## Notes
- Use Burp or OWASP ZAP for automated scanning.
- Do not run these tests against systems you don't own.



### File: FUTURE_CS_01/vulnerable_app/templates/vulnerable_app/templates/vulnerable_app/vulnerable_app/SECURE_FIX.md

# Secure Fixes

1. Prevent SQL Injection
   - Use parameterized queries (do NOT format user input into SQL).
   - Example:
     ```python
     cur.execute("SELECT id FROM users WHERE username=? AND password=?", (uname, pwd))
     ```

2. Prevent Stored XSS
   - Remove `|safe` from templates so Jinja2 auto-escapes user input.
   - Sanitize input server-side where appropriate.

3. Use secure authentication
   - Store password hashes (bcrypt) instead of plain text.
   - Implement rate-limiting and account lockouts.

4. Example secure login snippet:
   ```python
   import sqlite3
   from werkzeug.security import generate_password_hash, check_password_hash

   # when creating user:
   hashed = generate_password_hash('admin123')

   # when checking login:
   cur.execute("SELECT password FROM users WHERE username=?", (uname,))
   row = cur.fetchone()
   if row and check_password_hash(row[0], pwd):
       # success

