<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-ghooost411
description: CTF writeups and security challenges by GhOoOsT411.
---

# Writeups by GhOoOsT411

Source repository: `/repos/GhOoOsT411`

## Repository Index

- bug-bounty-reports/README.md
- bug-bounty-reports/Web/Authentication-Bypass/client-side-authentication-bypass.md
- bug-bounty-reports/Web/IDOR/idor-vertical-privilege-escalation-company-update.md
- bug-bounty-reports/Web/IDOR/idor-vertical-privilege-escalation-user-name-update.md

## Writeup Content


### File: bug-bounty-reports/README.md

# Bug Bounty Reports

This repository contains **real-world bug bounty style reports** demonstrating security vulnerabilities discovered during legal security testing, labs, and security research.

All reports are written in a **professional penetration testing format**, focusing on clear reproduction steps, impact analysis, and remediation guidance.

---

## 📌 Scope

The reports cover vulnerabilities in:

- 🌐 Web Applications
- 📱 Mobile Applications (Android)
- 🔗 APIs

Common vulnerability classes include:
- IDOR / Broken Access Control
- Authentication & Authorization Issues
- XSS
- Business Logic Flaws
- Insecure Data Storage
- API Security Issues (OWASP API Top 10)

---

## ⚠️ Disclaimer

All information in this repository is provided **for educational purposes only**.

- No real company names, domains, or sensitive data are disclosed
- Any sensitive information has been redacted
- Reports do not violate any bug bounty program NDA

---

## 👤 Author

**Hossam Mohamed Abo Khaleel**  
Junior Penetration Tester | Bug Bounty Hunter  

🔗 LinkedIn: https://www.linkedin.com/in/hossam-mohameddd



### File: bug-bounty-reports/Web/Authentication-Bypass/client-side-authentication-bypass.md

# Client-Side Authentication Bypass via Modified Login Response

## Severity
High (P2)

## Vulnerability Type
Broken Authentication / Authentication Bypass

## Description
The application fully trusts authentication status and role information provided by the client.

By intercepting and modifying the login API response, an attacker can manipulate the authentication status and assigned roles, resulting in **full administrative access without valid credentials**.

This vulnerability allows **unauthenticated attackers** to gain privileged access by tampering with client-side controlled values.

---

## Affected Component
Authentication API response handling

---

## Steps to Reproduce

1. Navigate to the application login page { https://example.com/login }

2. Enter any **invalid credentials** (e.g. `admin / admin`)

3. Intercept the login response using **Burp Suite**

4. Observe the original server response:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
"fullName": "REDACTED",
"status": false,
"errorType": "No Roles on this application",
"errorMessage": "You do not have access to this application.",
"userId": "REDACTED",
"roles": ""
}
``` 
5. Modify the response to:
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "fullName": "REDACTED",
  "status": true,
  "errorType": "No Roles on this application",
  "errorMessage": "You do not have access to this application.",
  "userId": "REDACTED",
  "roles": "admin"
}
```
6. Forward the modified response to the browser
7. The application grants full administrative access without validating credentials

## Proof of Concept (PoC)
Authentication and authorization decisions are performed entirely on client-controlled data.
By modifying the login response parameters (status and roles), an attacker can gain administrative access without valid credentials.

## Impact

- An unauthenticated attacker can:

- Bypass authentication completely

- Log in as any user role, including Administrator

- Gain full administrative access without credentials

- Perform privileged administrative actions

- Fully compromise the application and its data



### File: bug-bounty-reports/Web/IDOR/idor-vertical-privilege-escalation-company-update.md

# IDOR Leading to Vertical Privilege Escalation via Company Update Endpoint

## Severity
Medium (P3)

## Vulnerability Type
Broken Access Control / Insecure Direct Object Reference (IDOR)

## Description
A low-privileged user with no assigned role is able to update sensitive company information by reusing an owner-level company update endpoint.

The backend does not properly validate the user’s privilege level before processing the request. As a result, unauthorized users can modify company data, leading to **vertical privilege escalation**.

---

## Affected Component
Company management API endpoint (company update functionality)

---

## Attack Scenario
The application contains multiple user roles with different privilege levels:
- **Owner** (high-privileged user)
- **No-role user** (low-privileged user)

A low-privileged user can reuse the same endpoint used by an owner to update company information without proper authorization checks.

---

## Steps to Reproduce

1. Authenticate as a **low-privileged (no-role) user**
2. Intercept any authenticated request and keep the session active
3. Authenticate as an **owner** in a separate session
4. Capture the request used by the owner to update the company name:
```http
PUT /api/company/{company_id}
Content-Type: application/json

{
  "new_name": "Company Name Updated by Owner"
}
```
5. Reuse the same endpoint and request structure using the low-privileged user session
6. Modify the request body: 
```http
PUT /api/company/{company_id}
Content-Type: application/json

{
  "new_name": "Company Name Updated by Low Privileged User"
}
```
7. Send the request
8. The company name is successfully updated despite insufficient privileges

## Proof of Concept (PoC)

The backend does not enforce role-based authorization checks on the company update endpoint.
Any authenticated user can modify company information by directly referencing the company identifier and reusing owner-level functionality.

## Impact

- A low-privileged attacker can:
- Modify sensitive company information
- Tamper with internal business records
- Cause loss of data integrity
- Lead to reputational damage
- Potentially introduce compliance or regulatory risks



### File: bug-bounty-reports/Web/IDOR/idor-vertical-privilege-escalation-user-name-update.md

# IDOR Leading to Vertical Privilege Escalation via User Name Update Endpoint

## Severity
Medium (P3)

## Vulnerability Type
Broken Access Control / Insecure Direct Object Reference (IDOR)

## Description
A low-privileged user with no assigned role is able to update another user’s profile name by reusing an owner-level endpoint.

The backend does not properly enforce authorization checks to validate the user’s privilege level before processing the request. As a result, unauthorized users can modify sensitive user attributes, leading to **vertical privilege escalation**.

---

## Affected Component
User profile management API (user attribute update functionality)

---

## Attack Scenario
The application contains multiple user roles with different privilege levels:
- **Owner** (high-privileged user)
- **No-role user** (low-privileged user)

Both roles interact with the same backend endpoint for updating user profile attributes, without proper role-based access control enforcement.

---

## Steps to Reproduce

1. Authenticate as an **owner** and capture the request used to update a user’s name:
```http
POST /api/user/update-name
Content-Type: application/json

{
  "user_id": "REDACTED",
  "name": "Updated by Owner"
}
```
2. Authenticate as a low-privileged (no-role) user
3. Reuse the same endpoint and request structure
4. Modify the request body:
```http
POST /api/user/update-name
Content-Type: application/json

{
  "user_id": "REDACTED",
  "name": "Updated by Low Privileged User"
}
```

5. Send the request using the low-privileged session
6. The user name is successfully updated despite insufficient privileges

## Proof of Concept (PoC)

The backend fails to verify whether the authenticated user has sufficient privileges to update another user’s profile attributes.
Any authenticated user can reuse an owner-level endpoint to modify user information.

## Impact

A low-privileged attacker can:
- Modify other users’ profile information
- Tamper with user identity data
- Cause loss of data integrity
- Abuse trusted account functionality
- Undermine access control mechanisms

