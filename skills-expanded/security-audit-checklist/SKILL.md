---
name: security-audit-checklist
description: Run a comprehensive security audit across application code, cloud infrastructure, containers, CI/CD pipelines, and infrastructure-as-code. Covers privacy compliance, OWASP basics, secret leakage, API security, IAM misconfigurations, storage exposure, Kubernetes hardening, and network security. Use when the user asks to audit, review, or harden app or cloud security, check for secrets, scan for XSS/SQLi, verify security headers, review Terraform/CloudFormation, audit AWS/GCP/Azure configs, or perform any security-focused review.
---

# Security Audit Checklist

Run these checks on any system before shipping to production or after major changes.

## Before you start

The checklist itself is prose and needs nothing. The three scanners under
`scripts/` are Python, so running those needs **Python 3** on your machine
(`python3 --version`). Without it you can still work the checklist by hand; you
just do not get the automated secret scan, header check and IaC read.

## 1. Privacy & Data Governance

- [ ] **Privacy policy exists** if the app collects, stores, or processes any user data. Link it in the footer and signup flows.
- [ ] **Know where user data is stored**: document the primary database, caches, logs, backups, and third-party services. Check data residency requirements (GDPR, CCPA).
- [ ] **Data minimization**: only collect what you need. Delete or anonymize data you do not use.

## 2. Secret & Key Hygiene

- [ ] **.env values are not leaking**: scan the full repo for hardcoded secrets.
- [ ] **Never expose API keys in frontend code**: no keys in JS bundles, no sensitive values in public env prefixes (`REACT_APP_`, `NEXT_PUBLIC_`, `VITE_`).
- [ ] **Move keys server-side or behind a proxy**: all third-party API calls that require secrets must go through a backend endpoint.
- [ ] **Remove secrets from logs**: grep logs and error reporters for keys, tokens, and passwords. Mask or redact them before output.
- [ ] **Rotate leaked credentials immediately** if anything is found.

**Quick scan commands:**

```bash
# Run the bundled secret scanner
python3 scripts/scan_secrets.py .

# Manual ripgrep patterns
grep -rE '(api[_-]?key|secret|token|password)\s*[:=]\s*["\047][a-zA-Z0-9_\-]{16,}' --include='*.{js,ts,py,go,rb,php,java,json,yaml,yml,env,sh,tf,hcl}' .
grep -rE 'AKIA[0-9A-Z]{16}' .  # AWS keys
grep -rE 'ghp_[a-zA-Z0-9]{36}' .  # GitHub tokens
grep -rE 'sk-[a-zA-Z0-9]{48}' .   # OpenAI keys
```

## 3. Security Headers

- [ ] `Content-Security-Policy` restricts script sources and blocks inline execution where possible.
- [ ] `X-Frame-Options` or `frame-ancestors` prevents clickjacking.
- [ ] `Strict-Transport-Security` enforces HTTPS.
- [ ] `X-Content-Type-Options: nosniff` is present.
- [ ] `Referrer-Policy` limits referrer leakage.

**Check headers on a live URL:**

```bash
python3 scripts/check_headers.py https://your-app.com
```

## 4. OWASP Top 10 Basics

| # | Risk | What to check |
|---|------|---------------|
| A01 | Broken Access Control | Every endpoint checks auth and authorization. No IDOR bugs. |
| A02 | Cryptographic Failures | Passwords hashed with bcrypt/Argon2. TLS 1.2+ enforced. No sensitive data in URLs. |
| A03 | Injection | SQL uses parameterized statements. No raw string concatenation into queries. |
| A04 | Insecure Design | Rate limits on auth and sensitive actions. Business logic has abuse checks. |
| A05 | Security Misconfiguration | Default credentials removed. Debug mode off in prod. Error messages do not leak stack traces. |
| A06 | Vulnerable Components | Dependency audit: `npm audit`, `pip-audit`, `cargo audit`, `snyk test`. |
| A07 | Auth Failures | Session tokens are random and rotated on privilege change. MFA for sensitive accounts. |
| A08 | Data Integrity | Lockfiles present, signed commits where possible. |
| A09 | Logging Failures | Security events logged without secrets. |
| A10 | SSRF | Server-side requests use an allowlist. No user-controlled URLs hitting internal services. |

## 5. Input Validation & Injection

- [ ] **SQL Injection**: all queries use ORM parameters or prepared statements.
- [ ] **XSS**: user output is HTML-escaped. `dangerouslySetInnerHTML` and similar bypasses are audited.
- [ ] **Command Injection**: no `exec()`, `system()`, or `eval()` with user input.
- [ ] **Path Traversal**: file paths are sanitized and restricted to an allowlist directory.
- [ ] **NoSQL Injection**: MongoDB queries use parameterized objects.

## 6. API Security

- [ ] **Check API responses for sensitive data**: no internal IDs, password hashes, tokens, or unnecessary PII.
- [ ] **Authentication on all non-public endpoints**: no open admin or debug routes.
- [ ] **Rate limits before someone burns your API bill**: per-IP and per-user rate limiting on expensive or auth endpoints. Return `429` with `Retry-After`.
- [ ] **CORS is tight**: `Access-Control-Allow-Origin` is not `*`. Preflight required for state-changing methods.

## 7. Auth & Session

- [ ] **Password policy**: minimum 8 characters, no max length that prevents passphrases.
- [ ] **Brute-force protection**: exponential backoff or CAPTCHA after failed logins.
- [ ] **Session management**: secure, httpOnly, SameSite cookies. JWTs have short expiry and refresh rotation.
- [ ] **Password reset**: tokens are single-use, random, and expire quickly.

---

## 8. Cloud Provider Security

Applies to AWS, GCP, Azure, and any other cloud platform.

### 8.1 Identity & Access Management (IAM)

- [ ] **No root account access keys** exist. Root MFA is enabled.
- [ ] **Least privilege principle**: every role, user, and service account has the minimum permissions required. No wildcard (`*`) actions or resources unless absolutely necessary.
- [ ] **No long-lived access keys** for users. Prefer IAM roles with temporary credentials (STS, instance profiles, workload identity).
- [ ] **MFA enforced** for all human users, especially admins and billing access.
- [ ] **Inactive identities removed**: delete or disable users, roles, and service accounts unused for 90+ days.
- [ ] **Cross-account access** uses explicit role assumptions with external ID where applicable. No trust policies with `Principal: *`.

### 8.2 Storage (S3 / GCS / Azure Blob)

- [ ] **No public buckets/containers** unless intentionally hosting public static assets. Block public access at the account level.
- [ ] **Encryption at rest** enabled (AES-256 or KMS). No unencrypted storage volumes or snapshots.
- [ ] **Encryption in transit** enforced (HTTPS/TLS only). No `http` allowed.
- [ ] **Lifecycle policies** delete or transition old data. Versioning enabled for critical buckets.
- [ ] **Bucket policies** do not grant `Principal: *` or `AllUsers`. Access is via IAM roles, not hardcoded keys.
- [ ] **Logging enabled** for access logs and object-level events (S3 Server Access Logs, CloudTrail data events).

### 8.3 Compute (EC2 / GCE / Azure VM / Lambda / Cloud Run)

- [ ] **No default security groups** allowing 0.0.0.0/0 on sensitive ports (22, 3389, 3306, 5432, 6379, 27017).
- [ ] **SSM / Session Manager** used instead of direct SSH where possible. No port 22 open to the internet.
- [ ] **IMDSv2 required** on AWS EC2 (disable IMDSv1).
- [ ] **Instance metadata** is not exposed to containers or untrusted code.
- [ ] **Function runtime** uses minimal privileges. Lambda/GCP Cloud Functions do not run with admin roles.
- [ ] **Function environment variables** do not contain plaintext secrets. Use secrets manager (AWS Secrets Manager, GCP Secret Manager, Azure Key Vault).

### 8.4 Database & Cache

- [ ] **No public access**: databases are in private subnets or VPCs. No `0.0.0.0/0` in security groups.
- [ ] **Encryption at rest and in transit** enabled.
- [ ] **Automated backups** with point-in-time recovery.
- [ ] **Strong authentication**: no default passwords. Use IAM database auth or TLS client certs where supported.
- [ ] **Audit logging** enabled for connections and schema changes.

### 8.5 Networking

- [ ] **VPC / network segmentation**: prod, staging, and dev are in separate networks or at least separate subnets.
- [ ] **Security groups / firewalls** are deny-by-default. Only required ports are open.
- [ ] **No overly permissive CIDRs**: `0.0.0.0/0` is avoided except for HTTPS (443) on public-facing load balancers.
- [ ] **Private subnets** for databases, caches, and internal services. NAT Gateway or VPC endpoints for outbound internet.
- [ ] **DDoS protection** enabled where applicable (AWS Shield, Cloud Armor, Azure DDoS Protection).
- [ ] **DNS / Domain**: DNSSEC enabled if the registrar supports it. No dangling DNS records pointing to expired IPs or deleted resources (subdomain takeover risk).

### 8.6 Logging, Monitoring & Alerting

- [ ] **CloudTrail / Audit Logs / Activity Logs** enabled across all regions and services.
- [ ] **Log integrity**: logs are immutable or stored in a separate account with write-once permissions.
- [ ] **Sensitive data not logged**: cloud logs do not include passwords, tokens, or PII.
- [ ] **Alerts configured** for root login, IAM policy changes, public bucket creation, security group changes, and failed auth spikes.
- [ ] **Log retention** meets compliance requirements (typically 1 year).

---

## 9. Container & Orchestration Security

### 9.1 Docker / Container Images

- [ ] **No secrets in images**: scan Dockerfiles and layers for `.env`, `config.json`, or hardcoded credentials.
- [ ] **Minimal base images**: use distroless, Alpine, or scratch instead of full Ubuntu/Debian where possible.
- [ ] **No running as root**: Dockerfile sets `USER` to a non-root UID/GID.
- [ ] **Image scanning**: enable vulnerability scanning in the registry (ECR, GCR, ACR, Docker Hub) and block critical CVEs in CI.
- [ ] **Immutable tags**: do not use `latest` in production. Pin to digest or specific semver.
- [ ] **Multi-stage builds**: build artifacts and dev dependencies do not end up in the final image.

### 9.2 Kubernetes

- [ ] **RBAC**: least-privilege roles and role bindings. No cluster-admin for service accounts.
- [ ] **No default service account tokens** mounted into pods that do not need them (`automountServiceAccountToken: false`).
- [ ] **Network policies**: default-deny ingress/egress, then explicitly allow required traffic.
- [ ] **Pod security standards**: enforce `restricted` or `baseline` profile. No privileged containers, no hostPath, no hostNetwork.
- [ ] **Secrets encryption**: etcd encryption at rest is enabled. No plaintext secrets in Git.
- [ ] **Container runtime security**: seccomp, AppArmor, or SELinux profiles applied.
- [ ] **Admission controllers**: use OPA/Gatekeeper or Kyverno to enforce policies (no latest tag, required labels, resource limits).
- [ ] **Resource limits**: every pod has CPU and memory limits to prevent DoS via resource exhaustion.

---

## 10. Infrastructure as Code (IaC)

- [ ] **No secrets in Terraform / CloudFormation / Pulumi / CDK**: state files do not contain plaintext passwords or keys. Remote state is encrypted and access-controlled.
- [ ] **Terraform state backend** is secure: S3 with SSE-KMS, DynamoDB locking, and no public read access.
- [ ] **IaC scanning**: run `checkov`, `tfsec`, or `terrascan` on Terraform/CloudFormation before merge.
- [ ] **Drift detection**: scheduled scans detect manual console changes that diverge from IaC.
- [ ] **Modules are version-pinned**: do not pull modules from branches or unversioned sources.

**Quick IaC scan:**

```bash
python3 scripts/scan_iac.py .

# Or use dedicated tools if installed:
checkov -d . --framework terraform,cloudformation,dockerfile
# tfsec .
```

---

## 11. CI/CD Pipeline Security

- [ ] **No secrets in pipeline configs**: no hardcoded tokens in `.github/workflows`, `.gitlab-ci.yml`, Azure Pipelines, or Jenkinsfiles.
- [ ] **Secrets are injected** from the CI platform's native secrets manager (GitHub Secrets, GitLab CI Variables, Azure DevOps Library).
- [ ] **Pipeline permissions are minimal**: CI service accounts have only the permissions needed to deploy.
- [ ] **Branch protection**: direct pushes to main/master are blocked. All changes require PR/MR + review.
- [ ] **Signed commits or merge requirements**: require signed commits or at least verified merge commits for sensitive repos.
- [ ] **Dependency scanning**: SCA tools (Snyk, Dependabot, Renovate) run on every PR.
- [ ] **SAST**: static analysis (Semgrep, CodeQL, SonarQube) runs on every PR.
- [ ] **Container scanning**: images are scanned for CVEs before deployment.
- [ ] **No self-hosted runners** exposed to the public internet without VPN or IP allowlisting.
- [ ] **Pipeline does not run untrusted code** from forks without manual approval (prevent pwn requests).

---

## 12. Domain & DNS Security

- [ ] **DNSSEC** enabled at the registrar if supported.
- [ ] **No dangling CNAME / A / NS records** pointing to expired services (subdomain takeover risk).
- [ ] **Wildcard certificates** or per-subject certificates from a trusted CA. No self-signed certs in production.
- [ ] **Certificate expiry monitoring**: alerts 30 and 7 days before expiry.
- [ ] **CDN / WAF** configured with sensible rules (SQLi, XSS, LFI blocks). Rate limiting enabled at the edge.

---

## Audit Output

After running the checklist, produce a concise markdown report with:

1. **Summary** — Pass / Fail / Needs Review per category.
2. **Critical findings** — Anything that must be fixed before production.
3. **Recommended fixes** — Specific code changes, config updates, or library upgrades.
4. **Risk matrix** — Likelihood × Impact for each finding.
5. **Remediation timeline** — Suggest priority order and deadlines.
