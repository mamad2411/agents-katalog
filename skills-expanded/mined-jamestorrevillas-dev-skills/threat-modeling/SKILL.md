---
name: threat-modeling
description: Use this skill when identifying security threats, designing secure systems, thinking like an attacker, performing security assessments, or applying STRIDE threat modeling. Trigger on keywords: threat model, security design, attack surface, STRIDE, vulnerabilities by design, security review, who can attack this, what could go wrong security-wise.
---

# Threat Modeling

## Core Mindset

**Think like an attacker, build like a defender.**

Threat modeling is done BEFORE building, not after. Security retrofitted is always weaker and more expensive than security designed in.

---

## The STRIDE Framework

For every component, ask: can an attacker do this?

| Threat | Definition | Example |
|---|---|---|
| **S**poofing | Pretend to be someone else | Forged JWT token |
| **T**ampering | Modify data in transit or at rest | SQL injection, request body modification |
| **R**epudiation | Deny performing an action | No audit log of who deleted a record |
| **I**nformation Disclosure | Access data they shouldn't | Over-fetching API, verbose error messages |
| **D**enial of Service | Make system unavailable | No rate limiting on auth endpoint |
| **E**levation of Privilege | Gain unauthorized access level | IDOR (accessing other users' data) |

---

## Threat Modeling Process

```
1. DEFINE SCOPE       — What are we modeling? (feature, service, system)
2. IDENTIFY ASSETS    — What are we protecting? (data, services, credentials)
3. DRAW DATA FLOWS    — How does data move through the system?
4. IDENTIFY THREATS   — Apply STRIDE to each component and data flow
5. ASSESS RISK        — Likelihood × Impact for each threat
6. MITIGATE           — For each high-risk threat, define a control
7. VERIFY             — Confirm controls are implemented and working
```

---

## Attack Surface Analysis

For any new feature, identify:
- **Entry points** — Where does user input enter the system?
- **Trust boundaries** — Where does data cross privilege levels?
- **Data stores** — What sensitive data is stored and where?
- **External dependencies** — What third-party services are called?

---

## OWASP Top 10 (Quick Reference)

| # | Threat | Quick Check |
|---|---|---|
| A01 | Broken Access Control | Is every endpoint checking authorization? |
| A02 | Cryptographic Failures | Is sensitive data encrypted at rest and in transit? |
| A03 | Injection | Are all queries parameterized? All inputs validated? |
| A04 | Insecure Design | Was security considered in the design phase? |
| A05 | Security Misconfiguration | Are defaults hardened? Are secrets in env vars? |
| A06 | Vulnerable Components | Are dependencies up to date? Any known CVEs? |
| A07 | Auth Failures | Is auth implemented correctly? Session management secure? |
| A08 | Software Integrity | Are supply chain and build pipeline trusted? |
| A09 | Logging Failures | Are security events logged? Are logs protected? |
| A10 | SSRF | Can users cause server to make requests to internal resources? |

---

## Security Design Principles

- **Least Privilege** — Every component gets only the permissions it needs
- **Defense in Depth** — Multiple layers of security, no single point of failure
- **Fail Secure** — When something breaks, it should fail closed (deny access), not open
- **Zero Trust** — Never trust, always verify — even internal services
- **Minimize Attack Surface** — Less exposed = less exploitable
