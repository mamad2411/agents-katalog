---
name: security-audit
description: >
  Audit a file, directory, repository, or PR diff for security vulnerabilities.
  Use when reviewing code for OWASP Top 10 / CWE Top 25 issues, identifying
  injection / XSS / SSRF / IDOR / authentication flaws, scanning for hardcoded
  secrets, reviewing infrastructure-as-code (Terraform, Kubernetes manifests,
  Dockerfiles), auditing CI/CD configurations (GitHub Actions, GitLab CI), or
  performing a pre-merge security review. Outputs a structured report with
  severity, CWE/OWASP mapping, file:line references, exploitable scenario, and
  fix recommendations.
license: MIT
metadata:
  author: bridgemind
  version: "1.0.0"
context: fork
agent: security-auditor
argument-hint: "[file, directory, PR diff, or scope description]"
---

## Security Audit

Audit the code at `$ARGUMENTS` against production-quality security standards.

If no path is provided, audit the most recently changed files:
!`git diff --name-only HEAD~1 2>/dev/null | head -30`

### Scope

- Single file → audit that file deeply
- Directory → recurse, prioritize entry points (routes, handlers, IaC, CI configs, Dockerfiles)
- PR diff → audit only changed lines + their surrounding context
- "the whole repo" → full audit (warn about runtime; suggest tooling)

### Audit Categories

For each piece of code, run the categories below. **Only report actual issues.** Calibrate severity by exploitability + blast radius (see [threat-modeling.md](../bridgesecurity/references/threat-modeling.md)).

#### 1. Injection (CWE-79, CWE-89, CWE-78, CWE-94, CWE-77)
SQL / NoSQL / OS command / code / template / expression-language / LDAP / XPath. Look for: string concat into queries, `eval`, `child_process.exec`, `dangerouslySetInnerHTML`, `pickle.loads`, ORM `raw`/`literal`/`Unsafe` APIs.

#### 2. Broken Access Control (CWE-862, CWE-863, CWE-639, CWE-352)
IDOR, BOLA, BOPLA, missing auth on routes, mass assignment, missing CSRF, client-only checks, Server Actions without `auth()` call. Trace every state-changing handler — what's the first non-trivial line?

#### 3. Cryptographic Failures (CWE-327, CWE-328, CWE-330, CWE-916)
Weak hashes (MD5, SHA1, bcrypt < 12), `Math.random()` for tokens, ECB mode, hardcoded IVs/keys, JWT `alg: none`, HS256/RS256 confusion, `===` for HMAC compare, `rejectUnauthorized: false`.

#### 4. SSRF (CWE-918)
`fetch`/`requests.get`/`http.get` with user-controllable URL without allowlist + private-IP block + protocol pin.

#### 5. Path Traversal (CWE-22)
`fs.readFile(userPath)`, `send_file`, `path.join(base, userInput)` without resolve+prefix-check.

#### 6. Insecure Deserialization (CWE-502)
`pickle.loads`, `yaml.load` (not safe_load), `ObjectInputStream`, `node-serialize`, `Marshal.load`, vm2 sandbox use.

#### 7. XSS (CWE-79)
`dangerouslySetInnerHTML`, `innerHTML=`, `v-html`, `{@html}`, unsafe markdown render, DOM-based XSS via `location.hash`/query.

#### 8. Authentication & Session (CWE-287, CWE-384, CWE-521)
Plaintext password compare, JWT in localStorage, missing rate limit on login, missing MFA, weak password policy, sessions not regenerated on auth, predictable reset tokens.

#### 9. Hardcoded Secrets (CWE-798)
AWS keys, GitHub tokens, Stripe keys, OpenAI/Anthropic keys, JWTs, private keys, DB connection strings, generic high-entropy strings. **Skip the .env files themselves; scan source / configs / CI / Docker.**

#### 10. Cloud Misconfiguration
S3 public, IAM `*:*`, security group 0.0.0.0/0:22, RDS public, IMDSv1 enabled, missing encryption, missing audit logging.

#### 11. Container & Kubernetes Misconfiguration
`privileged: true`, `runAsUser: 0`, `hostNetwork: true`, `/var/run/docker.sock` mount, missing resource limits, `image:latest`, missing `securityContext`.

#### 12. CI/CD Risks
`pull_request_target` + checkout fork code, `${{ github.event.pull_request.title }}` in shell, mutable Action tags, `permissions: write-all`, secrets passed to fork PRs.

#### 13. Supply Chain
Unpinned Action tags, `:latest` Docker tags, missing SRI on `<script src>`, `curl … | sh` in setup scripts, postinstall scripts, vulnerable deps from `npm audit`.

#### 14. Open Redirect (CWE-601)
`router.push(searchParams.get('next'))` without allowlist; bypasses like `//evil.com`.

#### 15. ReDoS (CWE-1333)
Catastrophic backtracking patterns: `(a+)+`, `(a*)*`, `(a|aa)+`.

#### 16. Server Action / RPC Authorization
Every `'use server'` function — first line auth check + ownership verification + input schema?

#### 17. Sensitive Data Exposure (CWE-200)
Stack traces in responses, full user objects hydrated to client, secrets in logs, error messages with file paths.

#### 18. CSRF / CORS / Cookies (CWE-352)
Missing CSRF token, `cors({ origin: '*', credentials: true })`, cookies without `httpOnly` / `Secure` / `SameSite`.

#### 19. Markdown / Output Rendering Hazards
Image URL constructed from secrets / untrusted content (exfil channel — see [BridgeWard](https://github.com/bridge-mind/BridgeWard)).

#### 20. LLM-Specific (when applicable)
LLM05 (output passed to dangerous sink), LLM06 (excessive agency), LLM07 (secrets in system prompt).

### Output Format

```markdown
# BridgeSecurity Audit Report

**Target**: <path or scope>
**Scanned**: <N files / X bytes>
**Date**: <ISO date>

## Summary

| Severity | Count |
|---|---|
| Critical | N |
| High | N |
| Medium | N |
| Low | N |
| Info | N |

## Findings

### [Critical] <Title — concrete, not "potential issue">
- **File**: `path/to/file.ts:42`
- **Class**: <category — Injection / Broken Access Control / etc.>
- **CWE**: CWE-89 (SQL Injection)
- **OWASP**: A03 Injection
- **Code**:
  ```ts
  const result = await db.query(`SELECT * FROM users WHERE email = '${email}'`);
  ```
- **Why it's a problem**: <one paragraph — concrete exploit scenario, not generic theory>
- **Fix**:
  ```ts
  const result = await db.query('SELECT * FROM users WHERE email = $1', [email]);
  ```
- **References**: [CWE-89](https://cwe.mitre.org/data/definitions/89.html), [BridgeSecurity language-patterns](../bridgesecurity/references/language-patterns.md#sql--orm-injection)

[next finding...]

## Conclusion

<overall verdict — block merge / fix before release / good enough to ship>
<top 3 priority items for immediate action>
```

### Severity Levels

- **Critical**: direct RCE / full data exposure / auth bypass / mass exfiltration. Fix before merge.
- **High**: significant data exposure / privilege escalation / DoS / IDOR. Fix this sprint.
- **Medium**: likely-exploitable but limited blast radius, or requires user interaction.
- **Low**: defense-in-depth gap.
- **Info**: best-practice deviation worth noting.

Calibrate to **production impact**, not theoretical purity. A `Math.random()` for an unguessable element ID is `Info`. The same code generating a session token is `Critical`.

### Important Rules for Auditor

1. **Read-only**. Suggest fixes; don't apply them unless explicitly asked.
2. **Quote, don't paraphrase**. Show the exact vulnerable code.
3. **Concrete fixes**. Show the patched code, not just "use parameterized queries".
4. **Map to CWE + OWASP**. Use canonical IDs.
5. **No false positives if avoidable**. Verify before flagging:
   - Is the input actually user-controllable, or constant?
   - Is this a test fixture / example?
   - Is there sanitization on the way to the sink?
6. **Calibrate severity by reachability**. Unreachable vuln in dead code = Info.
7. **Don't dump tool output**. If you ran `semgrep` / `trivy` / `gitleaks`, synthesize. Deduplicate. Prioritize.
8. **Respect environment files**. Never read or display `.env*` contents (project rule). You can flag *references* to env files (e.g., a Dockerfile that copies `.env`).

### Default behavior when `$ARGUMENTS` is empty

Audit the most recently changed files (last commit / current diff). If outside a git repo, ask the user:

> "What would you like me to audit? Options: (1) a file or directory path, (2) `git diff HEAD~1`, (3) the whole repo (slower), (4) a specific concern (e.g., 'all server actions', 'all SQL queries', 'all Dockerfiles')."
