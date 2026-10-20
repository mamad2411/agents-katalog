---
name: security-and-auth
description: >
  Secure systems and design authentication/authorization. Use for OAuth 2.0,
  OIDC, SSO, JWT, sessions vs tokens vs cookies, passkeys, MFA/2FA, password
  storage, TLS/HTTPS, encryption (symmetric/asymmetric), digital signatures,
  hashing vs encryption vs tokenization, VPN/SSH/firewalls, permission models
  (RBAC/ABAC/ACL), secrets and sensitive data, and DevSecOps. Triggers:
  "authentication", "OAuth", "JWT", "SSO", "passwords", "encryption", "RBAC",
  "secure the system".
---

# Security and Authentication

Security is a design constraint, not a feature added at the end.

## When to use
- Any login, session, token, or permission design.
- Protecting data at rest/in transit.
- Reviewing a system's threat model.
- Compliance and secrets handling.

## Authentication
| Mechanism | Use |
|---|---|
| Session cookie | Server-rendered apps, easy revocation |
| JWT | Stateless APIs; short-lived + refresh; hard to revoke |
| OIDC / OAuth 2.0 | Third-party login, delegated authorization |
| SSO | One identity across many apps (SAML/OIDC) |
| Passkeys (WebAuthn) | Phishing-resistant, passwordless |
| MFA/TOTP | Second factor (Google Authenticator-style) |

Rules: never roll your own crypto; store passwords with a slow KDF
(bcrypt/scrypt/Argon2) + per-user salt; never store plaintext or fast hashes.
Tokens in `HttpOnly`+`Secure`+`SameSite` cookies, not localStorage.

## Authorization
- Models: ACL, DAC, MAC, RBAC, ABAC. Map to real access model, not one-size.
- Enforce server-side, deny by default, least privilege.
- Validate every object access (avoid IDOR/BOLA).

## Data protection
- **Encoding vs encryption vs tokenization:** encoding is not security;
  encryption protects confidentiality; tokenization replaces sensitive data.
- Encryption in transit (TLS/HTTPS) and at rest (KMS, disk/column encryption).
- Symmetric (fast, shared key) vs asymmetric (key exchange, signatures).
- Digital signatures for integrity/authenticity.
- Classify data; minimize collection; mask/tokenize PII; rotate keys.

## Network & platform
- Firewalls, VPN, SSH, NAT; segmentation and zero trust.
- Secrets management (vault/KMS); never commit secrets.
- DevSecOps: shift-left scanning, dependency pinning, SBOM.

## Checklist
- [ ] AuthN mechanism chosen; sessions/tokens revocable as needed.
- [ ] Passwords hashed with modern KDF + salt.
- [ ] AuthZ model defined; least privilege; object-level checks.
- [ ] TLS everywhere; HSTS; secure cookie flags.
- [ ] Sensitive data classified, minimized, encrypted, tokenized.
- [ ] Secrets in a manager; rotation plan.
- [ ] Input validation, rate limits, audit logging.
- [ ] Threat model + dependency scanning.

## Common pitfalls
- Fast hashes (MD5/SHA) for passwords.
- JWTs with long expiry and no refresh/revocation.
- Secrets in code/env committed to git.
- Authorization only on the UI, not the API (IDOR).
- Custom crypto.

## References
- `...\session-cookie-jwt-token-sso-and-oauth-2.md`, `...\jwt-101-key-to-stateless-authentication.md`, `...\explaining-json-web-token-jwt-to-a-10-year-old-kid.md`
- `...\oauth-2-explained-with-siple-terms.md`, `...\oauth-20-flows.md`, `...\v1what-is-sso-single-sign-on.md`
- `...\cookies-vs-sessions-vs-jwt-vs-paseto.md`, `...\what's-the-difference-between-session-based-authentication-and-jwts.md`, `...\what-are-the-differences-between-cookies-and-sessions.md`
- `...\how-to-store-passwords-in-the-database.md`, `...\is-passkey-shaping-a-passwordless-future.md`, `...\how-does-google-authenticator-or-other-types-of-2-factor-authenticators-work.md`
- `...\how-do-we-design-a-permission-system.md`, `...\how-do-we-design-a-secure-system.md`, `...\how-do-we-manage-sensitive-data-in-a-system.md`
- `...\encoding-vs-encryption-vs-tokenization.md`, `...\symmetric-encryption-vs-asymmetric-encryption.md`, `...\how-digital-signatures-work.md`
- `...\how-does-https-work.md`, `...\https-ssl-handshake-and-data-encryption-explained-to-kids.md`, `...\is-https-safe.md`
- `...\how-does-a-vpn-work.md`, `...\how-does-ssh-work.md`, `...\firewall-explained-to-kids-and-adults.md`
- `...\cybersecurity-101-in-one-picture.md`, `...\top-network-security-cheatsheet.md`, `...\what-is-devsecops.md`
Base: `D:\Agent-Assets\system-design-101\data\guides\`

## Related skills
`api-design`, `networking-fundamentals`, `system-design-method`.
