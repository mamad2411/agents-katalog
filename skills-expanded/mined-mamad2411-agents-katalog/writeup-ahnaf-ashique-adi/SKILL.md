<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-ahnaf-ashique-adi
description: CTF writeups and security challenges by Ahnaf-Ashique-Adi.
---

# Writeups by Ahnaf-Ashique-Adi

Source repository: `/repos/Ahnaf-Ashique-Adi`

## Repository Index

- DarkFlameBlaze-BugBounty-Portfolio/README.md
- DarkFlameBlaze-BugBounty-Portfolio/01-authentication/password-reset-bypass.md
- DarkFlameBlaze-BugBounty-Portfolio/notes/vulnerability-map.md

## Writeup Content


### File: DarkFlameBlaze-BugBounty-Portfolio/README.md

# 🔥 DarkFlameBlaze - Bug Bounty Portfolio

**Ethical Hacker | Security Researcher | Bug Bounty Hunter**

This repository documents my bug bounty hunting journey, vulnerabilities discovered, and security research.

---

## 📊 Stats

- **Total Bugs Found:** [will update]
- **Valid Reports:** [will update]
- **Total Bounty Earned:** ৳[will update]
- **Platforms:** HackerOne, Bugcrowd, Intigriti
- **Started:** November 2025

---

## 📂 Repository Structure

```
├─ 01-authentication/      # Auth vulnerabilities
├─ 02-authorization/       # Authorization bypasses
├─ 03-api-security/        # API security issues
├─ 04-data-security/       # Data exposure bugs
├─ 05-client-side/         # XSS, CSRF, etc.
├─ 06-infrastructure/      # Misconfigurations
├─ 07-business-logic/      # Business logic flaws
├─ tools/                  # Hunting tools & scripts
├─ notes/                  # Learning notes
└─ reports/                # Submitted reports (sanitized)
```

---

## 🎓 Learning Path

### Month 1: Authentication Vulnerabilities
- [ ] Password Reset Token Prediction
- [ ] Session Fixation
- [ ] JWT Vulnerabilities
- [ ] OAuth Misconfiguration
- [ ] MFA Bypass

### Month 2: API & Authorization
- [ ] BOLA (Broken Object Level Authorization)
- [ ] Privilege Escalation
- [ ] Mass Assignment
- [ ] API Endpoint Discovery
- [ ] Rate Limiting Bypass

### Month 3+: Advanced
- [ ] Data Exposure
- [ ] SQL/NoSQL Injection
- [ ] XSS Vulnerabilities
- [ ] Business Logic Flaws
- [ ] Race Conditions

---

## 🐛 Vulnerabilities Found

| # | Type | Platform | Status | Bounty |
|---|------|----------|--------|--------|
| 1 | [To be filled] | [Platform] | [Status] | ৳[Amount] |

---

## 🛠️ Tools & Scripts

- Custom vulnerability scanners
- Exploitation scripts
- Reconnaissance tools
- Payload collections

---

## 📖 Resources

- OWASP Top 10
- PortSwigger Web Security Academy
- HackerOne Reports
- Security Blogs

---

## ⚖️ Disclaimer

All testing is done on programs within scope of their bug bounty programs. No unauthorized access is performed.

---

**Last Updated:** November 11, 2025


### File: DarkFlameBlaze-BugBounty-Portfolio/01-authentication/password-reset-bypass.md

# Password Reset Token Prediction - [Company Name]

**Platform:** HackerOne
**Severity:** High
**Status:** Submitted / Accepted / Rejected
**Bounty:** ৳[Amount]

---

## Vulnerability Details

### Summary
The password reset functionality uses predictable tokens that can be brute-forced.

### Steps to Reproduce

1. Create account on [app.com]
2. Go to forgot password page
3. Enter email: `test@example.com`
4. Click reset link, get token: `67890`
5. In incognito window, manually try: `67891`, `67892`, `67893`
6. Token `67891` also works!
7. You can now reset any account by guessing tokens

### Proof of Concept

```
Original token: 67890
Sequential pattern found: tokens increment by 1

Test tokens:
- 67889: ✓ Valid (previous user)
- 67890: ✓ Valid (target user)
- 67891: ✓ Valid (next user)
- 67892: ✓ Valid (pattern continues)
```

### Impact
- Attacker can reset ANY user's password
- Full account takeover possible
- No rate limiting prevents brute force

### Suggested Fix
- Use cryptographically random tokens (not sequential)
- Implement rate limiting on reset attempts
- Add expiration time to tokens
- Invalidate token after use

---

## Resources
- [Link to my notes on this technique]
- [Reference: OWASP](link)
- [Reference: PortSwigger](link)


### File: DarkFlameBlaze-BugBounty-Portfolio/notes/vulnerability-map.md

# 🗺️ Vulnerability Map - DarkFlameBlaze's Guide

## LAYER 1: Authentication Vulnerabilities

### 1.1 Weak Password Reset Tokens
**What it is:**
- Reset tokens are predictable or guessable
- Can reset anyone's password

**How to find:**
1. Request password reset for your account
2. Get reset link/token
3. Test if token is sequential (123, 124, 125...)
4. Test if token is timestamp-based
5. Try common patterns

**Example:**
```
https://app.com/reset?token=12345
Try: token=12346, token=12344
If it works: VALID BUG
```

**Impact:** Account takeover
**Severity:** High 

---

### 1.2 Session Fixation
**What it is:**
- Attacker fixes user's session ID before login
- User logs in with attacker's session
- Attacker can hijack account

**How to find:**
1. Login to application
2. Note your session cookie
3. Clear cookies
4. Try accessing site with old session
5. If still logged in: BUG

**Impact:** Session hijacking
**Severity:** High 

---

### 1.3 JWT Vulnerabilities
**What it is:**
- JWT tokens are signed incorrectly
- Can forge valid tokens

**Common issues:**
1. Algorithm: None (signature bypassed)
2. Weak secret (can brute force)
3. Key confusion (RSA private used as HMAC secret)

**How to find:**
1. Get JWT token
2. Decode it (jwt.io)
3. Try changing payload
4. Try changing algorithm to "none"
5. If accepted: BUG

**Impact:** Privilege escalation, account takeover
**Severity:** Critical 

---

### 1.4 OAuth Misconfiguration
**What it is:**
- OAuth implementation is broken
- Can login as someone else

**How to find:**
1. Login with OAuth (Google, GitHub, etc.)
2. Check redirect URL
3. Try modifying email parameter
4. Try changing user ID
5. See if you can hijack someone else's account

**Impact:** Account takeover
**Severity:** High 

---

### 1.5 MFA Bypass
**What it is:**
- Two-factor authentication can be bypassed

**Common bypasses:**
1. Race condition (send request twice)
2. Status code bypass (401 to 200)
3. Parameter bypass (mfa=false)
4. Response manipulation

**How to find:**
1. Enable MFA
2. Start login
3. Get MFA prompt
4. Try bypassing with techniques above

**Impact:** MFA rendered useless
**Severity:** High 

---

## LAYER 2: Authorization Vulnerabilities

### 2.1 BOLA (Broken Object Level Authorization)
**What it is:**
- Can access other users' data by changing ID
- Most common vulnerability

**Example:**
```
GET /api/users/123/profile
Returns YOUR profile

GET /api/users/456/profile  
Returns OTHER USER's profile (BUG!)
```

**How to find:**
1. Do any action that shows YOUR data
2. Intercept request
3. Change ID parameter
4. Try accessing others' data
5. If it works: CRITICAL BUG

**Impact:** Data breach, privacy violation
**Severity:** Critical 

---

### 2.2 Privilege Escalation
**What it is:**
- Regular user becomes admin
- Or admin user, perform unauthorized actions

**How to find:**
1. Create normal user account
2. Intercept requests as normal user
3. Change role parameter (user=admin)
4. Try accessing admin endpoints
5. See if you can perform admin actions

**Impact:** Full system compromise
**Severity:** Critical 

---

(Continue with more layers...later)
