<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-het-desai
description: CTF writeups and security challenges by het-desai.
---

# Writeups by het-desai

Source repository: `/repos/het-desai`

## Repository Index

- Automate-PenTest-Report/README.md
- Automate-PenTest-Report/reports/PenTest_Report_Numeric Corp.md

## Writeup Content


### File: Automate-PenTest-Report/README.md

# AutomatePenTestReport
Automate Pentest Report Program



### File: Automate-PenTest-Report/reports/PenTest_Report_Numeric Corp.md

# Penetration Test Report: Numeric Corp

![Logo](./screenshots/image.png)

**Report Date:** 2024-08-13 12:28:32.404122

## Introduction
This penetration test report provides a detailed analysis of the vulnerabilities discovered during the security assessment of Numeric Corp. The vulnerabilities are categorized based on their severity, and recommendations for remediation are provided.

## Technical Findings

| Finding            | Severity    | Recommendation                          |
|--------------------|-------------|------------------------------------------|
| SQL Injection Vulnerability      | High    | Use parameterized queries and prepared statements to prevent SQL injection. |
| Insecure Direct Object References (IDOR)      | High    | Implement proper access control checks to ensure that users can only access resources they are authorized to view. |
| Cross-Site Scripting (XSS)      | Medium    | Sanitize all user inputs and encode output to prevent XSS attacks. |
| Security Misconfiguration      | Medium    | Review and harden the application's configuration settings to remove unnecessary services and secure the administrative interfaces. |

## Vulnerability Details

### SQL Injection Vulnerability

**Severity:** High

**Description:**
The application is vulnerable to SQL injection. This allows attackers to execute arbitrary SQL code on the database.


**Step:** Step 1: Enter ' OR '1'='1 in the login form to bypass authentication.

```bash
SELECT * FROM users WHERE username = 'admin' -- ' AND password = 'password';
```
![Screenshot](././screenshots/image.png)

**Step:** Step 2: Observe that the application logs in without proper credentials.
![Screenshot](././screenshots/image.png)

### Insecure Direct Object References (IDOR)

**Severity:** High

**Description:**
The application allows access to unauthorized resources by modifying the URL parameters.


**Step:** Step 1: Change the user ID parameter in the URL to access another user's data.

```bash
GET /user?id=1234 HTTP/1.1
```
![Screenshot](././screenshots/image.png)

**Step:** Step 2: Observe that the application allows access to unauthorized data.
![Screenshot](././screenshots/image.png)

### Cross-Site Scripting (XSS)

**Severity:** Medium

**Description:**
The application allows users to input scripts that are executed in the browser, potentially leading to account takeover.


**Step:** Step 1: Enter <script>alert('XSS')</script> in the comment box and submit.

```bash
<script>alert('XSS')</script>
```
![Screenshot](././screenshots/image.png)

**Step:** Step 2: Observe the alert box triggered by the script.
![Screenshot](././screenshots/image.png)

### Security Misconfiguration

**Severity:** Medium

**Description:**
The application is running with default configurations, which exposes sensitive information and administrative interfaces.


**Step:** Step 1: Access the application at /admin without authentication.

**Step:** Step 2: Observe that the administrative interface is accessible without login credentials.
![Screenshot](././screenshots/image.png)

## Recommendations

The following recommendations should be implemented to mitigate the identified vulnerabilities:

- Use parameterized queries and prepared statements to prevent SQL injection.
- Implement proper access control checks to ensure that users can only access resources they are authorized to view.
- Sanitize all user inputs and encode output to prevent XSS attacks.
- Review and harden the application's configuration settings to remove unnecessary services and secure the administrative interfaces.

## References

### SQL Injection Vulnerability References
- [ref1](https://owasp.org/www-community/attacks/SQL_Injection)
- [ref2](https://cwe.mitre.org/data/definitions/89.html)
- [ref3](https://example.com/sql-injection-prevention)
### Insecure Direct Object References (IDOR) References
- [ref1](https://owasp.org/www-community/attacks/Insecure_Direct_Object_References)
- [ref2](https://cwe.mitre.org/data/definitions/639.html)
### Cross-Site Scripting (XSS) References
- [ref1](https://owasp.org/www-community/attacks/xss/)
- [ref2](https://cwe.mitre.org/data/definitions/79.html)
### Security Misconfiguration References
- [ref1](https://owasp.org/www-project-top-ten/2017/A6_2017-Security_Misconfiguration)
- [ref2](https://cwe.mitre.org/data/definitions/933.html)

