<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-abd1rax1m0v
description: CTF writeups and security challenges by abd1rax1m0v.
---

# Writeups by abd1rax1m0v

Source repository: `/repos/abd1rax1m0v`

## Repository Index

- ctf-writeups/README.md
- ctf-writeups/xss-daryo-search.md

## Writeup Content


### File: ctf-writeups/README.md

# Daryo.uz Pentest Report

This repository contains the results of a penetration test performed on [daryo.uz](https://daryo.uz) for educational and research purposes. The assessment was conducted using several open-source tools to identify potential web vulnerabilities.

## 🔧 Tools Used
- Wapiti
- XSStrike
- ZAP Proxy
- WhatWeb
- Dalfox

## 📑 Summary
The test revealed several possible weaknesses, including:
- XSS vulnerabilities
- Server and framework information disclosure
- Misconfigured headers

> ⚠️ This project is intended **strictly for ethical and educational use only**. Unauthorized access or exploitation of websites is illegal and against responsible disclosure policies.

## 📂 Contents
- `report.md` — Full details of findings
- `tools-used.md` — Command usage examples
- `screenshots/` — Visual proof of findings



### File: ctf-writeups/xss-daryo-search.md

# XSS on daryo.uz search endpoint

## Target:
`https://daryo.uz/search?q=test`

## Vulnerability:
Reflected Cross Site Scripting (XSS)

## Tools Used:
- XSStrike
- Google Chrome DevTools
- View-source

## Steps to Reproduce:
1. Visit the URL and inject:
2. Script executes, confirming XSS.

## Impact:
Attacker can run arbitrary JS in user’s browser.

## Recommendation:
- Escape user input
- Validate query params
- Implement CSP headers

