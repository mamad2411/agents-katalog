---
name: security-patching
description: Automated security vulnerability remediation, CVE patching, cryptographic hardening, Zero-Trust protocol implementation, and compliance upgrades.
version: 1.0.0
---

# Security Protocol Implementation & Automated Patching Skill

This skill defines the methodology for automatically detecting vulnerabilities, applying surgical security patches, upgrading dependencies safely, and hardening enterprise security protocols.

---

## 1. Automated Security Protocol Implementation

### A. Authentication & Zero-Trust Protocols
- **mTLS (Mutual TLS)**: Enforce bi-directional certificate verification between internal microservices.
- **Strict OIDC / OAuth 2.1**: Implement PKCE (Proof Key for Code Exchange), refresh token rotation, and asymmetric token signing (RS256/ES256).
- **Zero-Trust Network Access (ZTNA)**: Never trust requests by network perimeter; validate tenant identity and role token on every RPC/HTTP hop.

### B. Cryptographic Standards & Key Management
- **Password Hashing**: Enforce Argon2id or bcrypt (cost factor >= 12).
- **Data Encryption**:
  - In Transit: TLS 1.3 only (disable TLS 1.0/1.1 and insecure ciphers).
  - At Rest: AES-256-GCM with cloud KMS (AWS KMS, GCP Cloud KMS, HashiCorp Vault) and automated key rotation.
  - Sensitive Field Masking: Hash or encrypt PII (SSN, credit card, health data) before database storage.

### C. Web & API Boundary Hardening
- **Enterprise Security Headers**:
  ```http
  Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
  Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none'; frame-ancestors 'none';
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), microphone=(), camera=()
  ```
- **Rate Limiting & Anti-DDoS**: Distributed token bucket (Redis) per IP and authenticated tenant.
- **Strict CORS Policy**: Disallow wildcard `*` with credentials; whitelist explicit verified origins.

---

## 2. Automated CVE Patching & Dependency Upgrades

When a vulnerability or CVE is flagged (via SAST, Snyk, Dependabot, or Trivy):

```
[Step 1: CVE Impact Assessment]
  ↳ Extract CVE identifier, severity (CVSS), and vulnerable call stack
          ↓
[Step 2: Dependency Graph Resolution]
  ↳ Identify direct vs transitive dependency path
          ↓
[Step 3: Surgical In-Place Patch or Version Bump]
  ↳ Bump package version or patch package via lockfile override
          ↓
[Step 4: Breaking Change & Contract Verification]
  ↳ Run typecheck, unit tests, and API contract tests to guarantee zero regressions
```

---

## 3. Security Remediation Checklist
- [ ] Direct and transitive dependencies patched against Critical/High CVEs
- [ ] Parameterized SQL / NoSQL queries (zero string-concatenated queries)
- [ ] IDOR authorization checks added to all route parameters
- [ ] Secrets removed from Git history and injected via environment/Secrets Manager
- [ ] Security event audit logging enabled for failed auth, privilege changes, and data exports
