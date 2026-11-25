---
name: viper-secrets-audit
description: Hardcoded Secret, Credential Entropy & Git History Leak Auditor (modeled on Gitleaks & TruffleHog). Scans codebases, configs, and CI files for exposed API keys and private tokens.
---

# Hardcoded Secret, Credential Entropy & Git History Auditor (`viper-secrets-audit`)

## 1. Executive Scope, Standards & CWE/OWASP Mapping
- **Frameworks & Standards:** OWASP Top 10:2025 A02/A07, OWASP Secrets Management Cheat Sheet, Gitleaks / TruffleHog Rulesets, CWE-798
- **Primary CWE Mapping:** CWE-798 (Use of Hard-coded Credentials), CWE-540 (Inclusion of Sensitive Information in Source Code), CWE-312 (Cleartext Storage of Sensitive Information)
- **ViperClaw MCP Tools:** `viper_harvest_js`, `viper_taint_scan`, `viper_verify_and_report`
- **ViperClaw CLI Command:** `viperclaw harvest-js . --output secrets_audit.json`

---

## 2. Threat Model & Root-Cause Architecture

```mermaid
flowchart LR
  Repo["Source Code / Git History / Docker Image"] --> Scan["Regex + Shannon Entropy Scanner"] --> Verify["Scope & Active Key Classification"] --> Vault["Remediation: KMS / OIDC / Secret Manager"]
```

### Root-Cause Analysis
Developers commit `.env` files, fallback default secrets (`os.getenv('JWT_SECRET', 'prod-secret-123')`), database URLs with inline passwords, or Docker `ENV`/`ARG` build secrets into version control—and deleting the file in a later commit leaves the secret permanently readable in `.git` commit history.

---

## 3. Deterministic Discovery & Grep/AST Audit Commands

Run the following discovery commands across the target repository before manual code review:

```bash
# 1. Automated ViperClaw analysis
viperclaw harvest-js . --output secrets_audit.json

# 2. Rapid static pattern discovery (ripgrep)
rg -n "(AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{80,}|sk_live_[A-Za-z0-9]{24,})"
rg -n "-----BEGIN (RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----"
rg -n "(postgres|mysql|mongodb|redis)://[^/\s]+:[^@\s]+@"
```

---

## 4. Senior Security Engineer 8-Point Audit Checklist

| Control ID | Audit Verification Target | Pass Criteria | Fail / Vulnerability Indicator |
| :---: | :--- | :--- | :--- |
| `SEC-01` | **Zero Hardcoded API Keys & Private Keys** | No cloud keys, PATs, webhook URLs, or PEM private keys exist in tracked files or commit history. | Plaintext credentials committed in source files, config YAML, or test scripts. |
| `SEC-02` | **No Insecure Default Fallback Secrets** | `os.environ['SECRET_KEY']` fails fast at startup if the variable is unset in production. | `os.getenv('JWT_SECRET', 'default_secret_key')` falls back to a known string when env var is missing. |
| `SEC-03` | **Git History & Reflog Cleanliness** | `git log -S` / `git log -G` confirms no historical commits contain revoked or active secrets. | Secret was committed in an earlier commit and only removed via a subsequent `git rm` without rotation. |
| `SEC-04` | **`.gitignore` & `.dockerignore` Coverage** | `.env`, `.env.*`, `*.pem`, `*.key`, `*.p12`, and `kubeconfig` are blocked in both `.gitignore` and `.dockerignore`. | `COPY . .` in `Dockerfile` bakes local `.env` or `.git` history into published container layers. |
| `SEC-05` | **Database & Broker Connection Strings** | Connection URLs inject credentials dynamically from secret mounts or IAM auth (`RDS IAM`, `Workload Identity`). | Plaintext `DATABASE_URL=postgres://admin:pass@...` committed in `docker-compose.yml` or `settings.py`. |
| `SEC-06` | **Client Mobile & Web Bundle Separation** | Backend secrets never appear in `NEXT_PUBLIC_*`, `VITE_*`, Android `strings.xml`, or iOS `Info.plist`. | Private third-party API key shipped inside client bundle or mobile APK. |
| `SEC-07` | **Pre-Commit & Push Protection Gate** | GitHub Secret Scanning Push Protection and local `pre-commit` secret hooks enabled. | No automated gate preventing accidental secret commits. |
| `SEC-08` | **Automated Rotation & Least-Privilege Scope** | Any exposed credential is immediately revoked/rotated and replaced with short-lived OIDC tokens. | Exposed key deleted from branch without revoking it at the provider. |

---

## 5. False-Positive Elimination & CVSS v3.1 Triage Rubric

### False-Positive Gate
1. Verify whether an upstream API Gateway, global middleware, or ORM hook already enforces the control before flagging a controller.
2. Confirm the code path is reachable from an external entrypoint (not dead code, CLI-only admin script, or unit-test fixture).

| Severity Tier | Baseline CVSS v3.1 Vector | Qualifying Security Impact |
| :--- | :--- | :--- |
| **CRITICAL (9.8)** | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` | Active production cloud IAM key, database password, or JWT signing key exposed in repository. |
| **HIGH (7.5)** | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` | Read-only third-party API token or internal Slack/webhook secret exposed in repository or bundle. |
| **MEDIUM (5.3)** | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N` | Hardcoded fallback secret in code where production environment variable is currently set. |

---

## 6. Production Remediation Patterns (Vulnerable vs. Hardened Code)

```python
# ❌ VULNERABLE: Silent fallback to hardcoded secret if environment variable is missing
JWT_SIGNING_KEY = os.getenv("JWT_SIGNING_KEY", "viper-prod-fallback-key-998877")

# ✅ HARDENED: Fails fast on missing secret & enforces minimum 32-byte cryptographic entropy
def load_signing_key() -> str:
    key = os.environ.get("JWT_SIGNING_KEY", "")
    if len(key.encode("utf-8")) < 32:
        raise RuntimeError("FATAL: JWT_SIGNING_KEY environment variable must be set and >= 32 bytes")
    return key
```

---

## 7. Regression Testing & Continuous Verification
1. Write a **Positive Unit Test** confirming authorized, schema-valid requests succeed.
2. Write a **Negative Security Regression Test** confirming unauthorized, cross-tenant, or malformed inputs are deterministically rejected.
3. Re-run `viperclaw taint` and `viperclaw verify` to confirm zero remaining unmitigated flows in `.viperclaw/graph.db`.
