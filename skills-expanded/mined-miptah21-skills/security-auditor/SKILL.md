---
name: security-auditor
description: Security vulnerability scanner for codebases. Use when auditing code for security issues, before deployments, or when evaluating third-party code/skills for safety. Covers command injection, XSS, auth bypass, secret exposure, supply chain risks, and prompt injection.
---

# Security Auditor

**Category:** Security / Quality Assurance

## Overview

Scan codebases for security vulnerabilities before deployment. Produces a clear **PASS / WARN / FAIL** verdict with findings and remediation guidance.

## When to Use

- Before deploying to production
- After adding new dependencies
- When handling auth, payments, or PII
- When evaluating third-party code
- After a security incident — audit similar patterns

## Scan Categories

### 1. Code Execution Risks

Scan all `.py`, `.sh`, `.js`, `.ts` files for:

| Category | Patterns | Severity |
|----------|----------|----------|
| Command injection | `os.system()`, `subprocess.call(shell=True)`, backtick execution | 🔴 CRITICAL |
| Code execution | `eval()`, `exec()`, `compile()`, `__import__()` | 🔴 CRITICAL |
| Obfuscation | base64-encoded payloads, hex strings, `chr()` chains | 🔴 CRITICAL |
| Network exfil | `requests.post()` to unknown hosts, `socket.connect()` | 🔴 CRITICAL |
| Credential harvest | reads from `~/.ssh`, `~/.aws`, env var extraction | 🔴 CRITICAL |
| File system abuse | writes outside project dir, modifies `~/.bashrc` | 🟡 HIGH |
| Privilege escalation | `sudo`, `chmod 777`, cron manipulation | 🔴 CRITICAL |
| Unsafe deserialization | `pickle.loads()`, `yaml.load()` without SafeLoader | 🟡 HIGH |

### 2. Web Application Vulnerabilities

| Category | Pattern to Find | Severity |
|----------|----------------|----------|
| SQL injection | String interpolation in queries | 🔴 CRITICAL |
| XSS | `dangerouslySetInnerHTML`, `innerHTML =` | 🔴 CRITICAL |
| CSRF | Missing CSRF tokens on state-changing endpoints | 🟡 HIGH |
| Auth bypass | Missing auth middleware on routes | 🔴 CRITICAL |
| Hardcoded secrets | API keys, passwords, tokens in source | 🔴 CRITICAL |
| Insecure hashing | `md5()`, `sha1()` for security | 🟡 HIGH |
| Path traversal | User input in `path.join()`, `readFile()` | 🟡 HIGH |
| SSRF | User-controlled URLs in server requests | 🟡 HIGH |
| Open redirect | Unvalidated redirect URLs | 🟡 MEDIUM |

### 3. Dependency Supply Chain

| Check | What to Look For | Severity |
|-------|-----------------|----------|
| Known CVEs | Packages with published vulnerabilities | 🔴 CRITICAL |
| Typosquatting | Packages with names similar to popular ones | 🟡 HIGH |
| Unpinned versions | `>=2.0` vs `==2.31.0` | ⚪ INFO |
| Install in code | `pip install` or `bun add` inside scripts | 🟡 HIGH |
| Suspicious packages | Low downloads, recent creation | ⚪ INFO |

### 4. Configuration Security

| Check | What to Look For | Severity |
|-------|-----------------|----------|
| CORS misconfiguration | `Access-Control-Allow-Origin: *` | 🟡 HIGH |
| Debug mode in production | `DEBUG=true`, verbose error pages | 🟡 HIGH |
| Default credentials | Admin/admin, test accounts | 🔴 CRITICAL |
| Missing rate limiting | No rate limits on auth endpoints | 🟡 HIGH |
| Insecure cookies | Missing `HttpOnly`, `Secure`, `SameSite` | 🟡 MEDIUM |

## How to Run an Audit

### Quick Scan (5 min)

Use grep to check for critical patterns:

```bash
# Hardcoded secrets
rtk grep -rnE "(password|secret|api_key|token)\s*=\s*['\"][^'\"]{8,}" src/

# SQL injection
rtk grep -rn "query\|execute" src/ | rtk grep -E '\$\{|f"|%s|format\('

# XSS
rtk grep -rn "dangerouslySetInnerHTML\|innerHTML\s*=" src/

# eval/exec
rtk grep -rnE "\beval\(|\bexec\(" src/

# AWS keys
rtk grep -rnE "AKIA[0-9A-Z]{16}" .
```

### Full Audit

1. **Scan source code** using rtk grep patterns above
2. **Check dependencies** — `rtk bun audit` / `pip audit`
3. **Review auth flows** — trace login, session, permission checks
4. **Check configurations** — CORS, CSP, cookie settings
5. **Review error handling** — ensure no sensitive data in error messages
6. **Check logging** — no PII, tokens, or passwords in logs

## Report Format

```
╔══════════════════════════════════════════════╗
║  SECURITY AUDIT REPORT                       ║
║  Project: [name]                             ║
║  Verdict: ❌ FAIL / ⚠️ WARN / ✅ PASS        ║
╠══════════════════════════════════════════════╣
║  🔴 CRITICAL: N  🟡 HIGH: N  ⚪ INFO: N     ║
╚══════════════════════════════════════════════╝

🔴 CRITICAL [category] file:line
   Pattern: [what was found]
   Risk: [what could happen]
   Fix: [how to remediate]
```

## Verdict Rules

- **✅ PASS** — No critical or high findings
- **⚠️ WARN** — High findings detected, review manually
- **❌ FAIL** — Critical findings, do NOT deploy without remediation
