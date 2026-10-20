---
name: cybersecurity-master
description: >-
  Master hub for professional cybersecurity — protect websites & apps from hackers and build a strong
  security program. Use for threat modeling (STRIDE), OWASP Top 10 secure coding, web hardening (CSP,
  HSTS, TLS, cookies, CORS), auth/session/account-takeover defense, secrets & software-supply-chain
  security (SCA/SBOM/signing), cloud & network security (IAM least-privilege, zero-trust, mTLS),
  penetration testing & vulnerability management (Burp/ZAP/semgrep/nuclei, SAST/DAST), DDoS/WAF/bot
  protection, and security operations (logging/SIEM, incident response, SOC2/ISO/PCI/GDPR).
  Bundles 9 specialized skills (in skills/<name>/GUIDE.md). Use for any security/hardening/pentest task.
---

# Cybersecurity — Master Hub (defend + attack + operate)

Secure web/app systems like a senior application-security/AppSec + offensive-security engineer:
prevent, detect, and respond. **Defense by construction**, verified by testing, run as a program.

> Ethics: offensive techniques here are for **authorized** testing of systems you own or are
> permitted to test. Never attack third-party systems without written authorization.

## How to use this hub

1. Start with **cybersecurity-foundations** (threat model, principles, attack surface).
2. Harden the app: OWASP, headers/TLS, auth, secrets/supply-chain.
3. Secure the infra: cloud/network; protect the edge: DDoS/WAF/bot.
4. Verify with pentesting/vuln-management; run security-operations + compliance.

## Bundled skills

- **cybersecurity-foundations** ⭐ — Threat modeling (STRIDE/attack trees), security principles
  (least privilege, defense in depth, fail secure), attack surface mapping, risk prioritization.  
  → `skills/cybersecurity-foundations/GUIDE.md`
- **appsec-owasp-top10** ⭐ — OWASP Top 10 with real exploit→fix: broken access control, injection
  (SQLi/NoSQLi/cmd), SSRF, XSS, insecure deserialization, secure-coding patterns.  
  → `skills/appsec-owasp-top10/GUIDE.md`
- **web-hardening-headers-tls** ⭐ — CSP (nonce/strict-dynamic), HSTS, security headers, cookies
  (HttpOnly/Secure/SameSite), CORS done right, TLS config, clickjacking/MIME defenses.  
  → `skills/web-hardening-headers-tls/GUIDE.md`
- **auth-session-account-security** ⭐ — Password hashing (argon2id), session vs JWT pitfalls, MFA,
  OAuth/OIDC security, account-takeover & credential-stuffing defense, rate-limit/lockout.  
  → `skills/auth-session-account-security/GUIDE.md`
- **secrets-supply-chain-security** — Secrets (Vault/KMS, no secrets in code), dependency security
  (SCA), SBOM, signing/provenance (SLSA/cosign), CI/CD hardening, dependency confusion.  
  → `skills/secrets-supply-chain-security/GUIDE.md`
- **infra-cloud-network-security** — IAM least-privilege, network segmentation, zero-trust, mTLS,
  cloud security (AWS/GCP/Azure), container/k8s security, key management.  
  → `skills/infra-cloud-network-security/GUIDE.md`
- **pentesting-vuln-management** ⭐ — Methodology, recon, Burp/ZAP/nuclei, SAST/DAST (semgrep/CodeQL),
  vuln triage/CVSS, responsible disclosure, remediation tracking.  
  → `skills/pentesting-vuln-management/GUIDE.md`
- **ddos-waf-bot-protection** — DDoS mitigation (Cloudflare), WAF rules, bot management, rate limiting,
  CAPTCHA/turnstile, edge defenses, abuse prevention.  
  → `skills/ddos-waf-bot-protection/GUIDE.md`
- **security-operations-ir-compliance** — Logging/SIEM, detection, incident-response playbooks,
  forensics basics, and compliance (SOC 2, ISO 27001, PCI DSS, GDPR).  
  → `skills/security-operations-ir-compliance/GUIDE.md`

## Pairs well with

`code-quality-master` (security code review/find-bugs), `backend-api-master` (auth, MFA),
`devops-master` (CI/CD, Docker/K8s), `systems-platforms-master` + `integrations-master`
(secure data/webhooks), `cross-platform-apps-master` (mobile security).

## Note

Bundled skills use `GUIDE.md` so only this master appears in Cursor's skills list.
