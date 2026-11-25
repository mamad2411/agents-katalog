---
name: tpl-situacao-security-audit
description: Template do pack (situacao/04-security-audit.md). Orienta o agente em tarefas situacionais como debug, seguranca e refactor alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: situacao/04-security-audit.md
  generated_by: install_pack_templates_as_claude_skills
---

# SITUATION: Security Audit & Vulnerability Review

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `situacao/04-security-audit.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## CONTEXT
Use this configuration when reviewing code for security vulnerabilities — either as a pre-launch audit, after a dependency alert, during a penetration test, or as part of a compliance requirement (SOC2, GDPR, PCI-DSS). This is a systematic, adversarial review: think like an attacker, not a developer. Every input is malicious until proven otherwise.

## OBJECTIVES
- Identify all OWASP Top 10 vulnerability classes present in the codebase
- Find secrets and credentials in code or version history
- Verify authentication and authorization logic is sound
- Detect insecure dependencies with known CVEs
- Produce a prioritized remediation plan with severity ratings

## APPROACH RULES

1. **Think like an attacker.** For every user input, ask: what happens if I send 10,000 characters? A null byte? SQL syntax? A script tag? A relative path like `../../etc/passwd`?

2. **Never trust client-side validation.** Always verify that server-side validation exists for every constraint enforced on the frontend.

3. **Defense in depth.** A vulnerability that requires two mistakes to exploit is better than one, but both should still be fixed. Do not accept "it's protected by X" as a reason not to fix Y.

4. **Severity before quantity.** A single Critical/High vulnerability matters more than 20 Low/Informational ones. Prioritize ruthlessly.

5. **Authentication vs Authorization.** AuthN = who are you? AuthZ = what can you do? Test both independently. Broken AuthZ (IDOR, privilege escalation) is often harder to find than AuthN bugs.

6. **Secret scanning is mandatory.** Run `git log --all -p | grep -E "(password|secret|key|token)" --no-index` or use `trufflehog`/`gitleaks` on the full repo history, not just HEAD.

## ROUTING TABLE

| If you encounter | Then |
|-----------------|------|
| User input going to SQL query | Check for parameterized queries. If string interpolation exists anywhere, it's CRITICAL. Flag immediately. |
| User input rendered in HTML | Check for `innerHTML`, `dangerouslySetInnerHTML`, `eval`. If unescaped, it's XSS — CRITICAL |
| File path constructed from user input | Path traversal risk. Must use `path.basename()` + allowlist of directories. Never concatenate directly |
| Passwords in code, config, or git history | Rotate immediately. Move to environment variables. Audit who had access to the repo |
| JWT implementation | Check: algorithm validation (reject `alg: none`), expiry enforced, signature verified on every request |
| CORS configuration | `Access-Control-Allow-Origin: *` is OK for public APIs, never for authenticated APIs. Check credentials header |
| Dependencies with CVEs | Classify by CVSS score. ≥7.0 = High (fix within sprint). ≥9.0 = Critical (fix today) |
| Authentication token in URL parameter | High severity. Tokens in URLs end up in logs, browser history, Referer headers. Move to headers |
| Missing rate limiting on auth endpoints | Brute force risk. Add rate limiting: max 5 attempts per IP per minute on login/reset |
| `eval()` or `Function()` with user data | Remote Code Execution potential. Critical. Remove immediately. |

## OWASP Top 10 Checklist

- [ ] **A01 Broken Access Control** — Test every endpoint: can user A access user B's data? Can regular user access admin endpoints?
- [ ] **A02 Cryptographic Failures** — Is sensitive data encrypted at rest and in transit? Is TLS enforced? Are weak algorithms (MD5, SHA1) used for passwords?
- [ ] **A03 Injection** — SQL, NoSQL, LDAP, OS command injection. All user inputs in queries must use parameterized statements.
- [ ] **A04 Insecure Design** — Are there rate limits? Are security controls part of the design or bolted on?
- [ ] **A05 Security Misconfiguration** — Default credentials? Verbose error messages in production? Unnecessary open ports?
- [ ] **A06 Vulnerable Components** — Run `npm audit`, `pip audit`, or Snyk. Any CVSS ≥ 7.0 must be addressed.
- [ ] **A07 Auth & Session Management** — Session fixation? Long-lived tokens without rotation? Weak password policy?
- [ ] **A08 Software Integrity Failures** — Unsigned dependencies? Unverified auto-update mechanisms?
- [ ] **A09 Logging Failures** — Are authentication failures logged? Are logs tamper-proof? Are PII data in logs?
- [ ] **A10 SSRF** — Any user-controlled URLs fetched server-side? Must validate against allowlist of internal IPs.

## DO NOT

- **DO NOT** fix security issues silently — document every finding even if you fix it immediately
- **DO NOT** downgrade severity to make the report look better
- **DO NOT** check only the application code — check infrastructure config, CI/CD pipelines, Docker files
- **DO NOT** trust that a framework prevents all injection — verify the actual queries/templates used
- **DO NOT** mark a finding as "accepted risk" without explicit sign-off from a named decision maker
- **DO NOT** leave secrets in `.env.example` files — use `KEY=` (no value) as placeholders
- **DO NOT** confuse `httpOnly` cookie as complete XSS protection — it prevents JS access but not all XSS impact

## OUTPUT FORMAT

**Security Audit Report** format:

```
## Security Audit Report
Date: [date]
Scope: [what was reviewed]
Auditor: [name]

### Executive Summary
[2-3 sentences: overall posture, critical count, recommendation]

### Findings

#### [CRITICAL-001] SQL Injection in /api/search
- Severity: Critical (CVSS 9.8)
- Location: src/api/search.ts:47
- Description: User input `q` parameter concatenated directly into SQL query
- Proof of Concept: GET /api/search?q='; DROP TABLE users; --
- Remediation: Use parameterized query: db.query("SELECT * FROM items WHERE name = $1", [q])
- Status: Open / Fixed / Accepted

### Remediation Priority
| Finding | Severity | Effort | Fix By |
|---------|----------|--------|--------|
| SQL Injection | Critical | 1h | Immediately |
```

## QUALITY GATES

- [ ] All OWASP Top 10 categories reviewed (not just whichever are easiest)
- [ ] Full git history scanned for secrets (not just current HEAD)
- [ ] All dependencies scanned with CVE score > 0 documented
- [ ] Every Critical/High finding has a specific file location and line number
- [ ] Remediation for every finding is specific ("use parameterized queries") not generic ("fix injection")
- [ ] Auth bypass tested: can unauthenticated user access authenticated endpoints?
- [ ] IDOR tested: can authenticated user access another user's resources by changing IDs?
- [ ] Report signed off by technical lead before sharing externally
