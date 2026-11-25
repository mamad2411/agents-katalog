---
name: security-audit
description: Static Analysis and Threat Modeling skill to detect OWASP Top 10 vulnerabilities.
---

# Security Audit Skill

## Purpose

To act as an automated **SAST (Static Application Security Testing)** scanner.
**Goal**: Identify vulnerabilities in the *implementation* phase, before the code reaches the `review` phase.

**ROI Metric**: Detecting a hardcoded secret here takes 5 seconds. Rotating a compromised key in production takes 5 hours.

## When to Use

- **Trigger**: When `backend` implements an endpoint involving `users`, `auth`, or `payments`.
- **Trigger**: When `frontend` uses `dangerouslySetInnerHTML` or similar raw HTML rendering.
- **Trigger**: When `pm-agent` flags a task as "High Risk."
- **Agent**: Primary skill for the `security` agent; secondary skill for `backend`/`review` modes.

## The Audit Protocol (The Scanner)

### 1. Pattern Scanning (The Grep Check)

*Scan the code for these specific "smells":*

| Risk Category | Keywords/Patterns to Flag |
| :--- | :--- |
| **Injection (RCE/XSS)** | `eval()`, `exec()`, `system()`, `dangerouslySetInnerHTML`, `innerHTML` |
| **SQL Injection** | String concatenation inside queries (`"SELECT... " + input`), `${var}` inside SQL strings |
| **Weak Crypto** | `md5`, `sha1`, `Math.random()` (for secrets), `http://` (non-TLS) |
| **Secrets** | `API_KEY`, `SECRET`, `PASSWORD` (assigned to hard strings) |
| **Debug Leftovers** | `console.log(userObj)`, `debugger`, `0.0.0.0` (binding to all interfaces) |

### 2. Logic Analysis (STRIDE)

*Ask these questions about the flow:*
- **Spoofing**: Does this verify *who* the user is? (Check: Auth Middleware presence).
- **Tampering**: Can I modify the payload? (Check: Zod/Joi validation `strip()` on unknown keys).
- **Information Disclosure**: Does the error return the stack trace? (Check: `try/catch` blocks).
- **Elevation of Privilege**: Does it check `user.id === resource.ownerId`? (Check: Authorization logic).

### 3. Dependency Check (Supply Chain)

* If `package.json` was modified:
  - Are versions pinned? (Good: `1.2.3`, Bad: `^1.2.3`).
  - Are there known CVEs? (Trigger `tavily` search).

## Execution Template

*Use this scratchpad to document the audit findings.*

```markdown
## 🔐 Security Audit Report: [File/Component]

### 1. Static Scan
- [ ] Checked for hardcoded secrets.
- [ ] Checked for raw SQL/HTML injection.
- [ ] Checked for dangerous functions (`eval`, `exec`).

### 2. Logic Check (OWASP)
- **AuthZ**: [ Verify BOLA/IDOR protection ]
- **Input**: [ Verify Schema Validation ]
- **Output**: [ Verify Data Sanitization ]

### 3. Vulnerability Findings
| Severity | Line | Issue | CWE ID | Remediation |
| :--- | :--- | :--- | :--- | :--- |
| 🔴 **Critical** | 42 | SQL Injection (`${id}`) | CWE-89 | Use Param: `WHERE id = $1` |
| 🟡 **Medium** | 15 | Missing Rate Limit | CWE-799 | Add `RateLimitMiddleware` |

### 🏁 Verdict
[ PASS / FAIL ] - *If Fail, do not commit.*
```

## Remediation Patterns (The "Fix It" Guide)

**Problem:** SQL Injection
❌ `db.query("SELECT * FROM users WHERE name = '" + name + "'")`
✅ `db.query("SELECT * FROM users WHERE name = $1", [name])`

**Problem:** XSS (React)
❌ `<div dangerouslySetInnerHTML={{ __html: userInput }} />`
✅ `<div>{userInput}</div>` or use `DOMPurify.sanitize(userInput)`

**Problem:** Broken Auth (IDOR)
❌ `return await db.orders.find(req.params.id)`
✅ `return await db.orders.find({ id: req.params.id, ownerId: req.user.id })`

## Integration with Agents

- **`security` agent**: Uses this skill as its primary method of interaction.
- **`backend` agent**: Must invoke `security-audit` before marking an API task as "Complete."
- **`review` mode**: Uses the *Findings Table* as the basis for "Critical" comments.
