<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-abd151201
description: CTF writeups and security challenges by abd151201.
---

# Writeups by abd151201

Source repository: `/repos/abd151201`

## Repository Index

- Penetration-test-report-/README.md

## Writeup Content


### File: Penetration-test-report-/README.md

# Comprehensive Penetration Testing Report

**Assessment Type:** Black / Grey Box Web & Network Penetration Test
**Scope:** Web Applications, APIs, Backend Infrastructure (Windows Server, RDP)

---

## 📌 Overview

This repository contains a **comprehensive penetration testing assessment** conducted against a web platform and its supporting backend infrastructure.
The engagement followed a **hybrid black-box and grey-box methodology**, simulating realistic attacker behavior against exposed services, authentication mechanisms, APIs, and server-side components.

The assessment identified **critical and high-risk vulnerabilities** affecting access control, session management, API authorization, and infrastructure hardening.

> ⚠️ **Note:** All sensitive identifiers, domains, and client-specific details have been sanitized or redacted.

---

## 🎯 Scope of Assessment

### In-Scope Components

* Frontend Web Applications
* Authentication & Identity Portal
* Backend APIs
* Windows Server Infrastructure
* Remote Desktop Protocol (RDP)
* Cloudflare-protected endpoints

### Out-of-Scope

* Physical security
* Social engineering (unless noted)
* Denial-of-Service attacks

---

## 🧠 Methodology

The following testing techniques and tools were used:

### Reconnaissance & Enumeration

* WHOIS, crt.sh
* DNSRecon, Amass, Sublist3r
* Dig, Nslookup

### Active Scanning

* Nmap
* Nikto
* Gobuster
* SSL Labs (Qualys)

### Manual & Exploitation Testing

* Burp Suite
* Hydra
* SQLMap
* Metasploit
* CrackMapExec

### Focus Areas

* Authentication & Authorization
* API Security (IDOR, CSRF)
* Session Management
* Input Validation
* SSL/TLS Configuration
* Cloudflare Bypass
* Dependency & Library Security

---

## 🚨 Executive Summary of Findings

The overall security posture of the platform is assessed as **Moderate to High Risk**.

### Critical & High-Risk Issues Identified

* **Insecure Direct Object Reference (IDOR)** in backend API endpoints
* **No brute-force protection** on authentication mechanisms
* **Stored XSS vulnerabilities** due to improper input sanitization
* **Cloudflare origin IP exposure**, enabling protection bypass
* **Missing Multi-Factor Authentication (MFA)**
* **CSRF protections inconsistently enforced**
* **Outdated JavaScript libraries** (jQuery v1.17.0)
* **Weak SSL/TLS configuration** (TLS 1.0/1.1 enabled)

Immediate remediation is strongly recommended.

---

## 🔍 Key Vulnerabilities Summary

| Vulnerability                  | Severity     |
| ------------------------------ | ------------ |
| IDOR in Backend API            | **Critical** |
| Stored XSS                     | **High**     |
| No Brute-Force Protection      | **High**     |
| CSRF-Unprotected API Endpoints | **High**     |
| Missing MFA                    | **High**     |
| Cloudflare Origin IP Exposure  | Medium       |
| Open Redirect via `ReturnUrl`  | Medium       |
| Missing CSP Header             | Medium       |
| Session Fixation Potential     | Medium       |
| Weak TLS Configuration         | Medium       |
| Verbose Technology Disclosure  | Low          |

---

## 🌐 Network & Infrastructure Findings

* RDP service detected (`9381/tcp`) — filtered but reachable
* Domain and OS information exposed via CrackMapExec
* No evidence of exploitable BlueKeep (CVE-2019-0708)
* Weak TLS cipher suites and deprecated protocols enabled
* No enforced HSTS

---

## 🔐 Authentication & Session Security

* CSRF tokens present but **not enforced consistently**
* Cookies relied upon instead of Authorization headers
* Session reuse observed before forced re-authentication
* No CAPTCHA, lockout, or rate-limiting mechanisms
* Potential user enumeration via login error messages

---

## ☁️ Cloudflare Bypass

* Origin server IP successfully identified
* Direct requests to origin returned **200 OK**
* Cloudflare protections effectively bypassed
* Increased exposure to direct exploitation and scanning

---

## 🛠 Recommendations (High-Level)

* Enforce **strict server-side authorization** for all API endpoints
* Implement **MFA / 2FA**
* Add **rate limiting and CAPTCHA**
* Sanitize all user inputs to prevent XSS
* Disable TLS 1.0 / 1.1 and weak ciphers
* Enforce HSTS and modern security headers
* Restrict origin IP access to Cloudflare only
* Upgrade outdated frontend libraries
* Strengthen CSRF validation across all state-changing requests

---

## ⚖️ Legal & Ethical Disclaimer

This penetration test was conducted **with explicit authorization**.
All testing followed ethical guidelines and industry best practices.
This repository is intended **for educational, reporting, and portfolio purposes only**.

---


Just tell me what you want next.


