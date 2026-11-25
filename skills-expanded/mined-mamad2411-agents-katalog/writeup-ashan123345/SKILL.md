<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-ashan123345
description: CTF writeups and security challenges by ashan123345.
---

# Writeups by ashan123345

Source repository: `/repos/ashan123345`

## Repository Index

- Bug-Bounty-Report-Web-Security-Vulnerabilities/README.md

## Writeup Content


### File: Bug-Bounty-Report-Web-Security-Vulnerabilities/README.md

# Bug Bounty Vulnerability Report and Analysis

This repository contains a collection of bug bounty vulnerability reports and findings, covering various common security issues discovered during web application security assessments. The reports detail vulnerabilities like Sensitive Data Exposure, Cross-Site Scripting (XSS), Weak Ciphers, Outdated Components, and more.

## Vulnerabilities Identified

- **Sensitive Data Exposure**
- **Cross-Site Scripting (XSS)** (Reflected, Stored, DOM-based)
- **Weak Ciphers Enabled**
- **Outdated Components** (ASP.NET MVC, IIS, jQuery)
- **Missing HTTP Strict Transport Security (HSTS)**
- **Cookies Not Marked as Secure**
- **Missing X-Frame-Options Header** (Clickjacking vulnerability)
- **BREACH Attack Detected**
- **SSL Certificate Expiry**
- **Outdated Software (ASP.NET MVC, IIS, jQuery)**

## Tools Used

- **Burp Suite**: Used for inspecting and intercepting traffic, identifying components, and analyzing headers for vulnerabilities like outdated software and missing security headers.
- **Netspacker**: A web scanner for detecting weak ciphers and security misconfigurations, such as missing HSTS or outdated components.
- **SSLSCAN**: Analyzes SSL/TLS configurations and identifies weak cipher suites.
- **SSLdump**: Captures and analyzes SSL/TLS traffic, useful for identifying weak cipher suites.
- **Nikto**: A web scanner that identifies vulnerabilities like outdated components and misconfigurations.
- **Shcheck**: Checks HTTP headers for security features like X-Frame-Options, HSTS, etc., related to clickjacking or XSS/CSRF protection.
- **SSLYze**: A Python tool for scanning SSL configurations, especially useful for detecting SSL certificate expiration.

## Objective

The goal of this repository is to provide an in-depth analysis of web application vulnerabilities that impact security. Each report includes:
- **Impact Assessments**
- **Steps to Reproduce**
- **Proof of Concept**
- **Proposed Mitigation or Fixes**

## How to Use

Clone this repository to explore the detailed vulnerability reports for each of the vulnerabilities listed above. You can use the provided tools to reproduce the findings or to understand the steps for mitigating similar vulnerabilities in your own applications.

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Netspacker Vulnerability Scanner](https://www.invicti.com)
- [Portswigger Web Security](https://portswigger.net/web-security)
- [HackerOne Bug Bounty Programs](https://hackerone.com/directory/programs?order_direction=DESC&order_field=launched_at)
- [Nikto Web Scanner](https://cirt.net/Nikto2)
- [SSLYze](https://github.com/pyOpenSSL/SSLYze)
- [Shcheck](https://github.com/shcheck)

---

**Note:** Please ensure to use these tools responsibly and always follow legal and ethical guidelines while performing security assessments or penetration testing.


