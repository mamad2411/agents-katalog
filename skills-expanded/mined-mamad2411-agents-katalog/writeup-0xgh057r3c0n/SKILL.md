<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-0xgh057r3c0n
description: CTF writeups and security challenges by 0xgh057r3c0n.
---

# Writeups by 0xgh057r3c0n

Source repository: `/repos/0xgh057r3c0n`

## Repository Index

- CODEALPHA-BUG-BOUNTY/README.md

## Writeup Content


### File: CODEALPHA-BUG-BOUNTY/README.md

# CODEALPHA BUG BOUNTY 🐞

## Description
CODEALPHA Bug Bounty is a web-based platform that allows users to report and track software bugs. It provides an authentication system for users to register and log in, submit bugs, and view reported issues. 🛠️

## Features 🚀
- ✅ User authentication (Login & Registration)
- 📝 Bug submission form
- 🔍 Bug tracking and viewing
- 🗄️ Database connectivity for storing reports
- 🎨 Simple and clean UI with CSS styling

## Installation 💻
1. **Clone or Download the Repository** 📥
   ```sh
   git clone https://github.com/0xgh057r3c0n/CODEALPHA-BUG-BOUNTY.git
   cd CODEALPHA-BUG-BOUNTY
   ```

2. **Set Up a Local Server** 🌐
   - Install **XAMPP** or **WAMP** (if not already installed).
   - Move the project folder to the `htdocs` directory (for XAMPP) or `www` directory (for WAMP).

3. **Database Configuration** 🗃️
   - Open `phpMyAdmin` and create a new database (e.g., `bug_bounty.db`).
   - Click on the "Import" tab 📂.
   - Select the SQL file (if provided) and click "Go" ✅ to import the database schema.
   - Configure database credentials in `db_config.php`:
     ```php
     $servername = "localhost";
     $username = "root";
     $password = "";
     $dbname = "bug_bounty.db";
     ```

4. **Start the Server** 🚦
   - Run Apache and MySQL from XAMPP/WAMP.
   - Open a web browser and go to `http://localhost/CODEALPHA_BUG_BOUNTY/`.

## Usage 🖥️
- **Register** a new account 🆕.
- **Login** to access bug submission 🔑.
- **Submit a bug** through `submit_bug.html` 🐛.
- **View reported bugs** via `view_bugs.html` 📋.

## Contributing 🤝
Feel free to contribute by submitting pull requests or reporting issues.

## License 📜
This project is open-source and available under the MIT License.

## Author ✍️
Developed by [0xgh057r3c0n]. Contact: [gauravbhattacharjee54@gmail.com] 📧


