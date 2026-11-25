<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-faveezy
description: CTF writeups and security challenges by Faveezy.
---

# Writeups by Faveezy

Source repository: `/repos/Faveezy`

## Repository Index

- Bug-Hunt-101/README.md

## Writeup Content


### File: Bug-Hunt-101/README.md

# Bug-Hunt-101
beginner bug bounty project using DVWA (Recon - Exploit - Report)
# Bug Hunt 101 — Recon to Report

This repository contains an introductory cybersecurity project with a focus on reconnaissance, vulnerability, discovery, exploitation, and professional report using a vulnerable web application. The aim is to demonstrate process.

## Objectives
- Perform reconnaissance using Nmap
- Identify and exploit common web vulnerabilities
- Document findings professionally

## Vulnerabilities Identified
- Reflected Cross-Site Scripting (XSS)
- SQL Injection

## Tools Used
- DVWA
- Nmap
- Burp Suite (Community Edition)
- Firefox
- Kali Linux
- SQLMAP

## Repository Structure
- /report — vulnerability report
- /recon — reconnaissance results
- /screenshots — proof of exploitation

  ## Method Used
  1. ## Environment Setup
     confirm the vulnerable application is working.
  2. ## Reconnaissance
     Identify the target and perform basic network scanning.
  3. ## Vulnerability Discovery
     Test application inputs for common web vulnerabilities.
  4. ## Exploitation & Proof
     Craft payloads to confirm the vulnerability exists.
  5. ## Reporting
     Document the vulnerability with reproduction steps, proof, impact, and mitigation.

     ## Project Structure
     bug-hunt-101/
│
├── README.md
├── report/
│   └── bug_hunt_report.md
├── recon/
│   └── nmap_scan.txt
└── screenshots/
    ├── xss_alert.png
    ├── burp_proxy.png
    └── sqli_dump.png

## Disclaimer
This project was performed in a local lab environment for assessment purpose only.

