<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-hexwyrm
description: CTF writeups and security challenges by hexwyrm.
---

# Writeups by hexwyrm

Source repository: `/repos/hexwyrm`

## Repository Index

- security-findings/README.md
- security-findings/case-studies/case-study-Information-Disclosure-in-an-API.md
- security-findings/reports/report-2025-Information-Disclosure-in-an-API.md
- security-findings/reports/report-2025-login-enumeration.md

## Writeup Content


### File: security-findings/README.md

# Bug Bounty & Security Research Portfolio

Welcome to my collection of responsibly documented security research reports.  
This repository highlights my methodology, technical skills, and ability to communicate findings in a professional format suitable for recruiters and security teams.

---

## 📂 Contents
- **Reports/** — Redacted vulnerability reports demonstrating real-world testing and responsible disclosure practices.
- **Update-Scripts/** — Automation scripts I’ve built to streamline tool installation and environment maintenance.
- **Case Studies/** — Generalized write-ups of security concepts and lessons learned.

---

## 🛡️ Purpose
The goal of this repository is to:
- Showcase my ability to identify, reproduce, and document vulnerabilities.
- Demonstrate professional reporting practices without exposing sensitive business or asset details.
- Provide recruiters and collaborators with evidence of my technical growth and readiness for industry roles.

---

## 🔑 Key Skills Demonstrated
- Web application testing with tools like BurpSuite and custom scripts.
- Evidence-based reporting with reproducible steps.
- Responsible disclosure practices (redacting sensitive data).
- Markdown documentation for recruiter-friendly presentation.

---

## 📅 Timeline
Reports and case studies are added as I continue my security research journey.  
I graduate in **April 2026** and am actively building a portfolio to transition into professional cybersecurity roles.

---

## ⚠️ Disclaimer
All reports are responsibly redacted.  
No sensitive business names, domains, or asset details are disclosed.  
These documents are for demonstration and educational purposes only.


## Copyright (c) 2025 hexwyrm

All rights reserved. This repository is provided solely for the purpose of 
demonstrating security research and reporting skills to potential employers 
and recruiters. No permission is granted to copy, modify, distribute, or 
otherwise use the contents for any other purpose.





### File: security-findings/case-studies/case-study-Information-Disclosure-in-an-API.md

# Case Study: Information Disclosure in API Endpoints

**Researcher:** hexwyrm  
**Date:** December 2025  

---

## Summary
During testing of a SaaS productivity platform, I identified an information disclosure issue affecting multiple API endpoints.  
The `getPublicPageData` and `loadCachedPageChunkV2` endpoints leaked sensitive workspace and page metadata when queried with unauthorized identifiers.  

Although full page content was not returned, the responses revealed workspace names, domains, and confirmation of private page existence.  
This type of vulnerability can be leveraged for reconnaissance, enumeration of private resources, and targeted social engineering campaigns.

---

## Activities Performed
- Configured a browser to route traffic through **BurpSuite** for interception.  
- Captured API requests while logged in as Account A.  
- Identified key request parameters (`spaceId`, `blockId`, `page.id`) tied to workspace and page identifiers.  
- Substituted values from Account B’s private workspace into Account A’s captured requests.  
- Replayed modified requests in Burp Repeater.  
- Observed HTTP 200 OK responses containing unauthorized metadata.  
- Documented findings with four screenshots (original and modified requests/responses for both endpoints).  

---

## Impact
- Confirms existence of private pages and workspaces belonging to other accounts.  
- Leaks workspace names (e.g., *Brian’s Space*) and domains (e.g., *wild-trombone-d10*).  
- Enables attackers to enumerate page IDs and map organizational structures.  
- Provides reconnaissance data that could be chained with other vulnerabilities (predictable IDs, phishing, privilege escalation).  
- Expected secure behavior would be a 403 Unauthorized or 404 Not Found response.

---

## Suggested Mitigation
- Enforce strict access controls on `getPublicPageData` and `loadCachedPageChunkV2`.  
- Return 403 Unauthorized or 404 Not Found when a user queries a page they do not have access to.  
- Avoid returning workspace names, domains, or privacy settings for unauthorized requests.  
- Normalize API responses to prevent metadata leakage across endpoints.

---

## Notes
- Testing was performed with disposable accounts created for research purposes.  
- No production data was modified or accessed beyond metadata leakage.  
- This report has been responsibly redacted for portfolio purposes.  
- Screenshots and logs have been archived to demonstrate the unauthorized metadata exposure.  

---

**Disclaimer:** This case study is for demonstration only. Sensitive business names, domains, and asset details have been removed.



### File: security-findings/reports/report-2025-Information-Disclosure-in-an-API.md

# Case Study: Information Disclosure in Notion API

**Researcher:** hexwyrm  
**Date:** December 2025  

---

## Summary
During testing of an SaaS platform, I identified an information disclosure issue affecting multiple API endpoints.  
The `getPublicPageData` and `loadCachedPageChunkV2` endpoints leaked sensitive workspace and page metadata when queried with unauthorized `spaceId` and `blockId` values.  

Although full page content was not returned, the responses revealed workspace names, domains, and confirmation of private page existence.  
This type of vulnerability can be leveraged for reconnaissance, enumeration of private resources, and targeted social engineering campaigns.

---

## Activities Performed
- Configured a browser to route traffic through **BurpSuite** for interception.  
- Captured API requests while logged in as Account A (hexwyrm).  
- Identified key request parameters (`spaceId`, `blockId`, `page.id`) tied to workspace and page identifiers.  
- Substituted values from Account B’s private workspace into Account A’s captured requests.  
- Replayed modified requests in Burp Repeater.  
- Observed HTTP 200 OK responses containing unauthorized metadata.  
- Documented findings with four screenshots (original and modified requests/responses for both endpoints).  

---

## Impact
- Confirms existence of private pages and workspaces belonging to other accounts.  
- Leaks workspace names (e.g., *Brian’s Space*) and domains (e.g., *wild-trombone-d10*).  
- Enables attackers to enumerate page IDs and map organizational structures.  
- Provides reconnaissance data that could be chained with other vulnerabilities (predictable IDs, phishing, privilege escalation).  
- Expected secure behavior would be a 403 Unauthorized or 404 Not Found response.

---

## Suggested Mitigation
- Enforce strict access controls on `getPublicPageData` and `loadCachedPageChunkV2`.  
- Return 403 Unauthorized or 404 Not Found when a user queries a page they do not have access to.  
- Avoid returning workspace names, domains, or privacy settings for unauthorized requests.  
- Normalize API responses to prevent metadata leakage across endpoints.

---

## Notes
- Testing was performed with disposable accounts created for research purposes (Account A: hexwyrm@outlook.com, Account B: brianscottcasey1@outlook.com).  
- No production data was modified or accessed beyond metadata leakage.  
- This report has been responsibly redacted for portfolio purposes.  
- Screenshots and logs have been archived to demonstrate the unauthorized metadata exposure.  

---

**Disclaimer:** This case study is for demonstration only. Sensitive business names, domains, and asset details have been removed.



### File: security-findings/reports/report-2025-login-enumeration.md

# Case Study: Information Disclosure in Login Flow

**Researcher:** hexwyrm  
**Date:** December 2025  

---

## Summary
During testing of a SaaS login system, I identified an information disclosure issue.  
The API endpoint responsible for handling login options revealed whether an email domain was classified as "enterprise" or "non-enterprise."  

By toggling a request parameter and observing response differences, it was possible to enumerate which domains were eligible for enterprise login flows.  
This type of vulnerability can be leveraged for reconnaissance and targeted phishing campaigns.

---

## Activities Performed
- Configured a browser to route traffic through **BurpSuite** for interception.  
- Captured login requests during the authentication flow.  
- Modified request parameters to test how the system classified different email domains.  
- Compared responses between enterprise and non-enterprise domains.  
- Documented findings with screenshots and structured notes.  

---

## Impact
- Attackers could enumerate enterprise customers of the platform.  
- This information could be used to target organizations with phishing or social engineering attacks.  

---

## Suggested Mitigation
- Normalize error responses to avoid revealing domain classification.  
- Suppress domain-specific error messages in client-facing APIs.  

---

## Notes
- Testing was performed with disposable accounts and non-sensitive email addresses.  
- No production data was accessed or modified.  
- This report has been responsibly redacted for portfolio purposes.  

---

**Disclaimer:** This case study is for demonstration only. Sensitive business names, domains, and asset details have been removed.


