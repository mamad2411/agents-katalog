<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-darkder101
description: CTF writeups and security challenges by Darkder101.
---

# Writeups by Darkder101

Source repository: `/repos/Darkder101`

## Repository Index

- Pentest-And-Reports/readme.md
- Pentest-And-Reports/CrAPI/Broken_object_level_Authorization.md
- Pentest-And-Reports/juice-shop/Improper Input Validation/zero-stars.md
- Pentest-And-Reports/juice-shop/Sensitive Data Exposure/confidential-Document.md

## Writeup Content


### File: Pentest-And-Reports/CrAPI/Broken_object_level_Authorization.md

# Broken Object Level Authorization - CrAPI

**Scope:** Local lab instance — `http://localhost:8888`.
**Tested on:** 15/11/2025, Browser: Chrome (Proxy: Burp Suite).
**Tools:** Burp Suite (Proxy + Repeater/Intercept), Browser devtools, screenshots.

## Summary

The lab was solved by abusing an unrestricted `/ftp` directory listing. Intercepting a GET for `/ftp/legal.md`, changing the request to `/ftp` returned a directory listing that revealed `/ftp/acquisitions.md`. Requesting `/ftp/acquisitions.md` returned the file contents (sensitive document) — demonstrating sensitive data exposure due to directory listing and lack of access controls.

## Steps to reproduce
1. Start Juice Shop and open the about us page: `http://localhost:3000`.
2. click on the link given in paragraph which says `Check out our boring terms of use if you are interested in such lame stuff.`
3. In Burp Suite with Intercept enabled, capture the GET request to the `/ftp/lgeal.md` endpoint and send it to the repeater. 
4. edit the intercepted request body and change the endpoint to the `/ftp` endpoint. 
5. from the response body , copy the path of acquisitions.md. (`/ftp/acquisitions.md`)
6. again edit the intercepted request body and change the endpoint to the `/ftp/acquisitions.md`
7. forward the request and you will able to see acquisitions.md sensitve file in response body. 

## PoC (captured request)

```
GET /ftp/acquisitions.md HTTP/1.1
Host: localhost:3000
sec-ch-ua-platform: "Linux"
Accept-Language: en-US
Upgrade-Insecure-Requests: 1
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: http://localhost:3000/
Accept-Encoding: gzip, deflate, br
Connection: keep-alive

```
## Sanitized response snippet :

```
HTTP/1.1 200 OK
Access-Control-Allow-Origin: *
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
Feature-Policy: payment 'self'
X-Recruiting: /#/jobs
Date: Wed, 05 Nov 2025 19:41:32 GMT
Connection: keep-alive
Keep-Alive: timeout=5

# Planned Acquisitions

> This document is confidential! Do not distribute!
[... redacted ...]

```

**Observed behavior** A GET to /ftp/acquisitions.md returned the file contents in the response body without authentication or authorization.

**Screenshot:** 
![acquisitions.md exposure](https://raw.githubusercontent.com/Darkder101/juice-shop-pentest/refs/heads/main/images/Screenshot_2025-11-05_14_55_33.png)

## Impact

* **Sensitive Data Exposure:** Internal/confidential documents are accessible to anyone who can reach the endpoint. Exposed files may contain business plans, credentials, or other sensitive information.

* **Risk:** Attackers can harvest internal documents, leak them publicly, or use information for targeted attacks (social engineering, financial fraud, competitive harm).

## Severity

**Medium → High**, (depending on contents of the file.)

## Remediation

1. **Disable directory listing:** Configure the web server (e.g., nginx, Apache, Express static middleware) to disallow directory listings. Do not expose raw directory contents.
2. **Remove sensitive files from webroot** Move confidential documents outside the publicly served directory or into protected storage.



### File: Pentest-And-Reports/juice-shop/Improper Input Validation/zero-stars.md

# Zero Stars — Improper Input Validation

**Scope:** Local lab instance — `http://localhost:3000` (Zero Stars lab).
**Tested on:** 5/11/2025, Browser: Chrome (Proxy: Burp Suite).
**Tools:** Burp Suite (Proxy + Repeater/Intercept), Browser devtools, screenshots.

## Summary

The lab was solved by exploiting improper input validation on the feedback form. By intercepting the POST request and changing the `rating` value from `1` to `0`, the application accepted the out-of-range value and the lab completed.

## Observed form fields

* `author` (string) — name of reviewer
* `comment` (string) — review text
* `rating` (numeric) — visible UI offered 1–5 stars (lowest selectable value was 1)

## Steps to reproduce

1. Start Juice Shop and open the feedback/review form for any product: `http://localhost:3000`.
2. Fill `comment`. In the UI select the lowest rating (1 star). Submit the form.
3. In Burp Suite with Intercept enabled, capture the POST request that sends the review to the server. Locate the JSON body containing `"rating": 1`.
4. Edit the intercepted request body and change the rating value:

   ```
   "rating": 1
   ```

   to

   ```
   "rating": 0
   ```
5. Forward the modified request. The server accepted the `rating: 0` value and the lab was marked solved.

## PoC (captured request)

```
POST /api/Feedbacks/ HTTP/1.1
Host: localhost:3000
Content-Length: 109
Accept-Language: en-US
sec-ch-ua-mobile: ?0
Authorization: Bearer 
Content-Type: application/json
Accept: application/json, text/plain, */*
sec-ch-ua-platform: "Linux"
Origin: http://localhost:3000
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: http://localhost:3000/
Accept-Encoding: gzip, deflate, br
Connection: keep-alive

{"UserId":23,"captchaId":5,"captcha":"45","comment":"testing the app (***nyking100700@gmail.com)","rating":0}
```

**Observed behavior:** Server accepted the submitted rating `0` even though the UI only allowed selecting 1–5. The lab validated this as solved.

**Screenshot:** 
![rating zero](https://raw.githubusercontent.com/Darkder101/juice-shop-pentest/refs/heads/main/images/Screenshot_2025-11-05_06_44_24.png)

## Impact

* **Integrity / business logic issue:** Users can submit ratings outside the intended range, allowing rating manipulation (inflating/deflating scores).
* While this specific issue is low risk for remote code execution or data leakage, it undermines application correctness and can be used to skew metrics or bypass client-side restrictions.

## Severity

**Low → Medium** (Low for strictly UI/metrics abuse; Medium if rating values are used by other logic that grants rewards, triggers workflows, or influences decision-making).

## Remediation

1. **Server-side validation:** Enforce allowed ranges and types for `rating` on the server (e.g., accept only integers 1–5). Never trust client-side controls.
2. **Input schema validation:** Use a validation layer or schema (e.g., Joi, JSON Schema, or framework validators) to reject invalid values with `400 Bad Request`.
3. **Canonicalization & normalization:** Normalize incoming data and log/reject unexpected values for monitoring.
4. **Unit tests / integration tests:** Add tests to verify that out-of-range ratings are rejected.
5. **Rate-limit / audit:** Log anomalous submissions and consider rate-limiting suspicious activity.



### File: Pentest-And-Reports/juice-shop/Sensitive Data Exposure/confidential-Document.md

# confidential-Document — Sensitive Data Exposure

**Scope:** Local lab instance — `http://localhost:3000`.
**Tested on:** 6/11/2025, Browser: Chrome (Proxy: Burp Suite).
**Tools:** Burp Suite (Proxy + Repeater/Intercept), Browser devtools, screenshots.

## Summary

The lab was solved by abusing an unrestricted `/ftp` directory listing. Intercepting a GET for `/ftp/legal.md`, changing the request to `/ftp` returned a directory listing that revealed `/ftp/acquisitions.md`. Requesting `/ftp/acquisitions.md` returned the file contents (sensitive document) — demonstrating sensitive data exposure due to directory listing and lack of access controls.

## Steps to reproduce
1. Start Juice Shop and open the about us page: `http://localhost:3000`.
2. click on the link given in paragraph which says `Check out our boring terms of use if you are interested in such lame stuff.`
3. In Burp Suite with Intercept enabled, capture the GET request to the `/ftp/lgeal.md` endpoint and send it to the repeater. 
4. edit the intercepted request body and change the endpoint to the `/ftp` endpoint. 
5. from the response body , copy the path of acquisitions.md. (`/ftp/acquisitions.md`)
6. again edit the intercepted request body and change the endpoint to the `/ftp/acquisitions.md`
7. forward the request and you will able to see acquisitions.md sensitve file in response body. 

## PoC (captured request)

```
GET /ftp/acquisitions.md HTTP/1.1
Host: localhost:3000
sec-ch-ua-platform: "Linux"
Accept-Language: en-US
Upgrade-Insecure-Requests: 1
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: http://localhost:3000/
Accept-Encoding: gzip, deflate, br
Connection: keep-alive

```
## Sanitized response snippet :

```
HTTP/1.1 200 OK
Access-Control-Allow-Origin: *
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
Feature-Policy: payment 'self'
X-Recruiting: /#/jobs
Date: Wed, 05 Nov 2025 19:41:32 GMT
Connection: keep-alive
Keep-Alive: timeout=5

# Planned Acquisitions

> This document is confidential! Do not distribute!
[... redacted ...]

```

**Observed behavior** A GET to /ftp/acquisitions.md returned the file contents in the response body without authentication or authorization.

**Screenshot:** 
![acquisitions.md exposure](https://raw.githubusercontent.com/Darkder101/juice-shop-pentest/refs/heads/main/images/Screenshot_2025-11-05_14_55_33.png)

## Impact

* **Sensitive Data Exposure:** Internal/confidential documents are accessible to anyone who can reach the endpoint. Exposed files may contain business plans, credentials, or other sensitive information.

* **Risk:** Attackers can harvest internal documents, leak them publicly, or use information for targeted attacks (social engineering, financial fraud, competitive harm).

## Severity

**Medium → High**, (depending on contents of the file.)

## Remediation

1. **Disable directory listing:** Configure the web server (e.g., nginx, Apache, Express static middleware) to disallow directory listings. Do not expose raw directory contents.
2. **Remove sensitive files from webroot** Move confidential documents outside the publicly served directory or into protected storage.



### File: Pentest-And-Reports/readme.md

# Pentest-And-Reports  

A collection of practical web application penetration testing reports , methodology and Bug hunting artifacts starting with **OWASP Juice Shop**,**OWASP CrAPI** and **Bug Hunting** with more labs and CTF-based case studies to be added progressively.

> **Status:** Actively growing. Current focus: full web-app pentest documentation and reporting workflow.

---

## 📌 Summary

This repository showcases my web application security testing approach through real-world style assessments of deliberately vulnerable applications & Bug hunting.  
Each project includes methodology, verified Proof-of-Concepts, risk ratings, and actionable remediation guidance.

---

## 🎯 Current Scope

| Target | Focus Areas | Status |
|--------|-------------|--------|
| OWASP Juice Shop | End-to-end functional + business logic testing | In Progress |
| OWASP CrAPI | API security testing: auth, rate limits, IDOR, injections | In Progress |
| Bug Hunting | Full Web-app Pentesting | In Progress |

Planned future additions:

- TryHackMe or HackTheBox vulnerable labs
- API-only test cases
- CTF-style exploit breakdowns

---

## 📂 Repository Structure

* `juice-shop/` — reports, notes, PoCs, configs for Juice Shop assessment
* `crapi/` — API pentesting findings and exploitation workflows
* `Yeswehack/` - Bug Hunting reports
* `notes/` — methodology notes, references, testing checklists
* `scripts/` — automation / verification helper scripts
* `README.md` — this file

---

## 🔍 Methodology & Tools

Testing follows industry standards and hybrid methodology:

- OWASP Web Security Testing Guide (WSTG)
- OWASP API Security Top 10
- Manual verification and business logic exploration

Tools involved:

- Burp Suite Pro (proxy, Repeater, Intruder)
- Browser DevTools
- Small custom automation tools/scripts
- Optional scanning: ZAP, ffuf, nuclei (clearly labeled when used)

---

## 📌 Goal

Provide clear, professional pentest documentation that reflects:

✔ Real exploitability  
✔ Reproducible PoCs  
✔ Proper risk classification  
✔ Practical remediation  

This repo is continuously evolving as I learn and demonstrate deeper offensive security concepts.

---

### ✨ Feedback & Collaboration

Suggestions to improve methodology, reporting clarity, or target selection are always welcome.

