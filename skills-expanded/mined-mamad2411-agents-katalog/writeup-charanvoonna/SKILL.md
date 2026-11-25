<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-charanvoonna
description: CTF writeups and security challenges by charanvoonna.
---

# Writeups by charanvoonna

Source repository: `/repos/charanvoonna`

## Repository Index

- VAPT-HTB-pentest-lab-reports/README.md
- VAPT-HTB-pentest-lab-reports/Starting-Point/Meow/report.md

## Writeup Content


### File: VAPT-HTB-pentest-lab-reports/README.md

# VAPT-HTB-pentest-lab-reports


### File: VAPT-HTB-pentest-lab-reports/Starting-Point/Meow/report.md

# Meow — Hack The Box

## Overview
The Meow machine is a beginner-level Hack The Box target designed to introduce basic penetration testing concepts such as service discovery and insecure services.

The objective was to identify open ports, access the service running on the system, and retrieve the root flag.

---

## Information Gathering

First, connectivity to the target machine was verified using ping.

Command used:

ping 10.129.16.148

The host responded successfully.

An Nmap scan was then performed to discover open ports and services.

Command used:

nmap -sV 10.129.16.148

Result:

23/tcp open  telnet  Linux telnetd

The scan revealed that the Telnet service was running on port 23.

---

## Enumeration

Since Telnet was discovered, the service was tested for remote login access.

Command used:

telnet 10.129.16.148

The service displayed a login prompt.

---

## Vulnerability

The system allowed login using the root account with a blank password.

This is a critical misconfiguration that allows unauthorized access.

---

## Exploitation

The attacker connected to the Telnet service and logged in using:

Username: root  
Password: (blank)

After logging in successfully, a shell was obtained.

Commands executed:

ls  
cat flag.txt

The root flag was retrieved.

---

## Privilege Escalation

No privilege escalation was required because the attacker logged in directly as root.

---

## Impact

An attacker could gain full control over the system and access sensitive files.

---

## Mitigation

Disable Telnet and replace it with SSH.

Implement strong password policies.

Disable root login for remote services.

---

## Lessons Learned

- Basic port scanning using Nmap
- Identifying insecure services
- Exploiting weak authentication


## Screenshots

![Screenshot 1](screenshots/Screenshot_2026-03-12_15_06_00.png)

![Screenshot 2](screenshots/Screenshot_2026-03-12_15_06_13.png)

![Screenshot 3](screenshots/Screenshot_2026-03-12_15_06_13.png)

![Screenshot 4](screenshots/Screenshot_2026-03-12_15_06_20.png)

![Screenshot 5](screenshots/Screenshot_2026-03-12_15_06_20.png)

![Screenshot 6](screenshots/Screenshot_2026-03-12_15_06_36.png)

![Screenshot 7](screenshots/Screenshot_2026-03-12_15_06_39.png)

![Screenshot 8](screenshots/Screenshot_2026-03-12_15_06_46.png)


