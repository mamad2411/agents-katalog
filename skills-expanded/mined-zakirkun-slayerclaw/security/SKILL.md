# 🔒 Cybersecurity & Privacy Skill

You are a cybersecurity expert. Give practical, actionable security advice. Never help with malicious activities — only defense, hardening, and education.

## Core Security Principles
1. **Defense in depth** — Multiple layers, no single point of failure
2. **Least privilege** — Grant minimum permissions needed
3. **Zero trust** — Verify everything, trust nothing by default
4. **Security by design** — Build it in from the start, not bolt it on
5. **Assume breach** — Plan for "when" not "if" you get compromised

## OWASP Top 10 (Web Security)
| # | Vulnerability | Prevention |
|---|---|---|
| A01 | Broken Access Control | Enforce RBAC, validate server-side |
| A02 | Cryptographic Failures | Use TLS, hash passwords with bcrypt/argon2 |
| A03 | Injection (SQL, XSS) | Parameterized queries, sanitize input |
| A04 | Insecure Design | Threat modeling, secure defaults |
| A05 | Security Misconfiguration | Harden defaults, disable debug in prod |
| A06 | Vulnerable Components | Keep dependencies updated, use SBOM |
| A07 | Auth Failures | MFA, secure session management |
| A08 | Data Integrity Failures | Verify software integrity (checksums) |
| A09 | Logging Failures | Log security events, monitor anomalies |
| A10 | SSRF | Validate/restrict outbound requests |

## Password & Authentication Best Practices
```
Passwords:
- Minimum 12 characters, ideally 16+
- Use a passphrase: "correct-horse-battery-staple"
- Unique per service — use a password manager (Bitwarden, 1Password)
- Never store in plaintext — use bcrypt (cost 12+) or Argon2id

Authentication:
- Enable 2FA/MFA everywhere (prefer TOTP/hardware key, not SMS)
- Use OAuth2/OIDC for SSO — don't build your own auth
- JWT: short expiry (15-60 min), refresh tokens in httpOnly cookies
- Rate limit login attempts + account lockout after N failures
- Hash with salt: bcrypt.hash(password, 12) — never MD5/SHA1 alone
```

## Secure Coding Patterns

### SQL Injection Prevention
```typescript
// ❌ VULNERABLE
const query = `SELECT * FROM users WHERE email = '${email}'`;

// ✅ SAFE (parameterized)
const result = await db.query('SELECT * FROM users WHERE email = $1', [email]);
```

### XSS Prevention
```typescript
// ❌ VULNERABLE
element.innerHTML = userInput;

// ✅ SAFE
element.textContent = userInput;
// Or sanitize HTML with DOMPurify before innerHTML
```

### Environment Variables & Secrets
```bash
# Never commit secrets to git
# Use .env files (add to .gitignore)
# For production: use secret managers
# AWS Secrets Manager, Vault, Doppler, or env vars in CI/CD

# Scan for leaked secrets:
git log --all --full-diff -p | grep -E "(password|secret|key|token)" -i
# Or use: truffleHog, gitleaks, detect-secrets
```

## Network Security
```bash
# Check open ports
nmap -sV -p- hostname
ss -tlnp

# Firewall rules (UFW)
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw enable

# Fail2ban — block brute force
apt install fail2ban
# Config: /etc/fail2ban/jail.local
```

## SSL/TLS
```nginx
# Strong TLS configuration for Nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
ssl_prefer_server_ciphers off;
ssl_session_cache shared:SSL:10m;
add_header Strict-Transport-Security "max-age=63072000" always;
add_header X-Frame-Options DENY;
add_header X-Content-Type-Options nosniff;
add_header Referrer-Policy strict-origin-when-cross-origin;
```

## Incident Response Framework (PICERL)
1. **Prepare**: Policies, tools, contacts ready
2. **Identify**: Detect the breach — what's affected?
3. **Contain**: Isolate affected systems immediately
4. **Eradicate**: Remove malware, patch vulnerability
5. **Recover**: Restore from clean backups, verify
6. **Lessons Learned**: Post-mortem + improve defenses

## Privacy Best Practices
- Collect minimum required data (data minimization)
- Encrypt data at rest (AES-256) and in transit (TLS 1.3)
- Set data retention policies — delete what you don't need
- For EU users: GDPR compliance (consent, right to deletion, DPA)
- For Indonesian users: UU PDP (Perlindungan Data Pribadi) compliance
- Use privacy-respecting analytics (Plausible, Fathom) instead of GA

## Security Audit Checklist
### Web Application
- [ ] All inputs validated server-side
- [ ] Authentication + authorization on every endpoint
- [ ] HTTPS everywhere, HTTP redirects to HTTPS
- [ ] Security headers set (CSP, HSTS, X-Frame-Options)
- [ ] Dependency vulnerabilities: `npm audit`, `pip-audit`
- [ ] No secrets in source code (use `gitleaks`)
- [ ] Rate limiting on auth endpoints
- [ ] Error messages don't leak stack traces in production
- [ ] Logs don't contain PII or secrets
- [ ] Database user has minimal permissions

### Server
- [ ] SSH key auth only (no passwords)
- [ ] Root login disabled
- [ ] Automatic security updates enabled
- [ ] Unnecessary services disabled
- [ ] Fail2ban installed
- [ ] Backups encrypted and tested
- [ ] Firewall rules reviewed

## Tools Reference
| Purpose | Tool |
|---|---|
| Password manager | Bitwarden (free, open source) |
| Secrets scanning | gitleaks, detect-secrets |
| Dependency audit | npm audit, pip-audit, trivy |
| Port scanning | nmap |
| SSL testing | ssllabs.com, testssl.sh |
| Web vuln scanning | OWASP ZAP, Nikto |
| Brute force protection | fail2ban |
| VPN | WireGuard, OpenVPN |
| 2FA App | Aegis (Android), Raivo (iOS) |
