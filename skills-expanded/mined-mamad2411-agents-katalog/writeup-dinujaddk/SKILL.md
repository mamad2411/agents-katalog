<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-dinujaddk
description: CTF writeups and security challenges by dinujaddk.
---

# Writeups by dinujaddk

Source repository: `/repos/dinujaddk`

## Repository Index

- Bug-Bounty-Assessment-Report/README.md

## Writeup Content


### File: Bug-Bounty-Assessment-Report/README.md

# Bug Bounty Report  
Reflected XSS • Missing CSRF Protection • Clickjacking  

This repository presents a comprehensive **bug-bounty-style web security assessment** conducted for academic purposes. It documents real-world ethical testing, validated vulnerabilities, proof-of-concept demonstrations, and remediation strategies discovered during manual security analysis.

---

## Overview  

This project demonstrates an end-to-end **manual web penetration testing workflow**, focusing on front-end application security. The assessment includes:

- Reconnaissance & attack surface mapping  
- Automated and manual scanning  
- Vulnerability discovery and validation  
- Proof-of-Concept (PoC) exploitation  
- Impact assessment  
- Technical remediation recommendations  
- Reflections and challenges faced  

Targeted applications:  
- https://store.goodreads.lk  
- https://www.glm.lk  

---

## Vulnerabilities Identified  

The assessment confirmed **three critical web security vulnerabilities**, each verified using controlled, non-destructive Proof-of-Concepts.

---

### 1. Reflected Cross-Site Scripting (XSS)  

User-supplied input in the search functionality was reflected directly into the HTML response without proper output encoding, allowing execution of attacker-controlled JavaScript.

- **Impact:** Session hijacking, phishing attacks, UI manipulation, credential theft  
- **Severity:** High  
- **OWASP Category:** A03 – Injection  

---

### 2. Cross-Site Request Forgery (CSRF)  

State-changing operations accepted cross-origin requests without anti-CSRF tokens or sufficient Origin/Referer validation. A crafted external HTML form successfully triggered authenticated actions.

- **Impact:** Unauthorized account actions, profile modification, account takeover  
- **Severity:** High  
- **OWASP Category:** A08 – CSRF  

---

### 3. Clickjacking (Missing Frame Protection)  

The application did not implement `X-Frame-Options` or `Content-Security-Policy: frame-ancestors`, allowing pages to be embedded inside attacker-controlled iframes.

- **Impact:** Click redirection, UI deception, unauthorized actions  
- **Severity:** Medium  
- **OWASP Category:** A05 – Security Misconfiguration  

---

## Methodology  

The assessment followed a structured and repeatable penetration testing methodology:

### 1. Reconnaissance  
- Amass (subdomain & DNS enumeration)  
- WhatWeb (technology fingerprinting)  
- WAFW00F (WAF detection)  
- Nmap (port and service enumeration)  

### 2. Scanning & Mapping  
- OWASP ZAP (spidering & passive scanning)  
- Burp Suite (proxy interception, request analysis)  

### 3. Exploitation  
- Manual payload crafting  
- Reflected XSS payload testing  
- CSRF attack HTML page creation  
- Clickjacking iframe overlay PoC  
- Browser DevTools & Burp Repeater  

### 4. Verification & Documentation  
- Reproduced findings reliably  
- Captured evidence and PoCs  
- Documented impact, root cause, and mitigations clearly  

---

> **Disclaimer:**  
> This project was conducted strictly for educational purposes. All testing was non-destructive and performed on publicly accessible systems without exploiting sensitive data.

