---
name: security-review
description: >
  Security review and hardening patterns. OWASP Top 10 checklist, secrets scanning, auth patterns,
  input validation, and container security. Use when auditing code, reviewing PRs for security,
  or implementing auth/authz.
---

# security-review

Security review and hardening patterns.

## how to use

- `/security-review`
  Apply these security constraints to all code in this conversation.

- `/security-review <file>`
  Review the file against all rules below and report:
  - violations (quote the exact line or snippet)
  - severity (critical / high / medium / low)
  - a concrete fix (code-level suggestion)

Do not rewrite entire files. Prefer minimal, targeted fixes.

## when to apply

Reference these guidelines when:
- reviewing code for security vulnerabilities
- implementing authentication or authorization
- handling user input or external data
- configuring CORS, CSP, or CSRF protections
- writing Dockerfiles or container configs
- managing secrets or credentials
- setting up API endpoints

## rule categories by priority

| priority | category | impact |
|----------|----------|--------|
| 1 | secrets management | critical |
| 2 | input validation | critical |
| 3 | authentication | critical |
| 4 | authorization | critical |
| 5 | injection prevention | critical |
| 6 | transport security | high |
| 7 | container security | high |
| 8 | headers and policies | medium |
| 9 | logging and monitoring | medium |

## quick reference

### 1. secrets management (critical)

- never hardcode secrets, API keys, tokens, or passwords in source code
- use environment variables or dedicated secrets managers (AWS Secrets Manager, Vault)
- add sensitive file patterns to `.gitignore`: `.env`, `*.pem`, `*.key`, `credentials.*`
- rotate credentials immediately if committed to version control
- use `git-secrets` or `trufflehog` for pre-commit scanning
- separate secrets by environment (dev/staging/prod)

### 2. input validation (critical)

- validate ALL external input at system boundaries (user input, API payloads, query params, headers)
- use allowlists over denylists
- validate type, length, range, and format
- sanitize output based on context (HTML, SQL, shell, URL)
- reject unexpected input early; fail closed
- never trust client-side validation alone

### 3. authentication (critical)

- use established libraries (passport, next-auth, django-auth) over custom implementations
- enforce strong password policies (min 12 chars, complexity)
- implement rate limiting on login endpoints
- use bcrypt/argon2 for password hashing (never MD5/SHA1)
- implement account lockout after repeated failures
- use secure session management (HttpOnly, Secure, SameSite cookies)
- implement MFA where possible

### 4. authorization (critical)

- enforce least privilege principle
- validate permissions server-side on every request
- use role-based (RBAC) or attribute-based (ABAC) access control
- never rely on hidden URLs or client-side role checks
- verify resource ownership before access (IDOR prevention)
- log authorization failures

### 5. injection prevention (critical)

- **SQL**: use parameterized queries / prepared statements; never string concatenation
- **XSS**: escape output by context; use framework auto-escaping (React JSX, Jinja2 autoescape)
- **Command injection**: avoid `os.system()`, `exec()`, `eval()`; use subprocess with argument lists
- **Path traversal**: validate and canonicalize file paths; reject `..` sequences
- **SSRF**: validate and allowlist outbound URLs; block internal network ranges
- **Template injection**: never pass user input to template engines as template code

### 6. transport security (high)

- enforce HTTPS everywhere; redirect HTTP to HTTPS
- use TLS 1.2+ only; disable older protocols
- implement HSTS with long max-age
- validate SSL certificates; never disable verification in production
- use certificate pinning for mobile apps

### 7. container security (high)

- use minimal base images (alpine, distroless)
- run as non-root user
- pin image versions with digest hashes
- scan images for vulnerabilities (trivy, snyk)
- never store secrets in Docker images or layers
- use multi-stage builds to exclude build tools
- set read-only filesystem where possible
- limit container capabilities and resources

### 8. headers and policies (medium)

- set `Content-Security-Policy` to restrict resource loading
- set `X-Content-Type-Options: nosniff`
- set `X-Frame-Options: DENY` (or use CSP frame-ancestors)
- configure CORS with specific origins; never use `*` in production
- implement CSRF tokens for state-changing requests
- set `Referrer-Policy: strict-origin-when-cross-origin`

### 9. logging and monitoring (medium)

- log authentication events (login, logout, failures)
- log authorization failures and privilege escalation attempts
- never log sensitive data (passwords, tokens, PII)
- implement alerting for anomalous patterns
- retain logs with appropriate rotation and access controls
- use structured logging (JSON) for machine parsing

## common fixes

| problem | fix |
|---------|-----|
| hardcoded API key | move to env var, add to .gitignore, rotate key |
| SQL concatenation | switch to parameterized query |
| `eval()` with user input | remove eval; use safe alternatives |
| missing CSRF token | add CSRF middleware/token to forms |
| HTTP-only endpoint | add TLS, redirect HTTP to HTTPS |
| root container user | add `USER nonroot` to Dockerfile |
| `CORS: *` | specify allowed origins explicitly |
| bare except clause | catch specific exceptions; log details |

## secrets scanning in repositories (gitGraber patterns)

### GitHub Dork Patterns
Search for accidentally committed secrets using targeted queries:

```
# API keys
"api_key" OR "apikey" OR "api-key" filename:.env
"AKIA" filename:.py OR filename:.js  # AWS access keys
"sk-" filename:.py  # OpenAI keys
"ghp_" OR "ghu_" OR "ghs_" filename:.env  # GitHub tokens

# Database credentials
"DB_PASSWORD" OR "DATABASE_URL" filename:.env
"mongodb+srv://" filename:.py OR filename:.js
"postgres://" filename:.yml

# Private keys
"BEGIN RSA PRIVATE KEY" OR "BEGIN EC PRIVATE KEY"
"BEGIN OPENSSH PRIVATE KEY"
```

### Pre-Commit Secret Prevention
```bash
# Install git-secrets
brew install git-secrets

# Register AWS patterns
git secrets --register-aws

# Add custom patterns
git secrets --add 'AKIA[0-9A-Z]{16}'  # AWS access key
git secrets --add 'sk-[a-zA-Z0-9]{48}'  # OpenAI key
git secrets --add 'ghp_[a-zA-Z0-9]{36}'  # GitHub PAT

# Install hooks
git secrets --install
```

### Automated Scanning
```bash
# TruffleHog: scan git history for secrets
trufflehog git file://. --only-verified

# Scan specific branch
trufflehog git file://. --branch main --only-verified

# Trivy: scan filesystem
trivy fs --scanners secret .
```

## CI/CD security rules (from awesome-cicd-security)

### pipeline hardening checklist

- [ ] Pin all GitHub Action versions to full SHA (not tags)
- [ ] Set minimum `permissions` block in workflows (never use `write-all`)
- [ ] Use OIDC for cloud authentication (no long-lived secrets)
- [ ] Enable branch protection: require reviews + status checks
- [ ] Scan dependencies: Dependabot/Renovate + vulnerability alerts
- [ ] Run SAST (Semgrep/CodeQL) on every PR
- [ ] Scan container images (Trivy) before pushing
- [ ] Never log secrets — use masking in CI output
- [ ] Separate build and deploy with approval gates
- [ ] Audit third-party actions before using (check source, publisher)
- [ ] Sign artifacts and container images
- [ ] Use ephemeral runners when possible

### supply chain security

| Attack Vector | Mitigation |
|--------------|------------|
| Dependency confusion | Pin versions, use lock files, verify checksums |
| Compromised action | Pin to SHA, audit source code |
| Stolen CI secrets | OIDC, short-lived tokens, secret rotation |
| Build tampering | Reproducible builds, SLSA provenance |
| Registry poisoning | Image signing (cosign), digest pinning |

## cross-references

- **offensive-security** skill: Penetration testing methodology
- **osint-recon** skill: OSINT investigation workflows
- **SECURITY_PLAYBOOK.md**: 36 security rules
- **SECURITY_ARSENAL.md**: Complete tool inventory
- **devops-patterns** skill: CI/CD pipeline patterns
