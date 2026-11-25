---
name: security-audit
description: Focused security pass for code changes and codebases. Use when code handles user input, authentication, sessions, permissions, secrets, file uploads or paths, payments, SQL, shell commands, templates, deserialization, redirects, outbound requests (SSRF), webhooks, or LLM and agent tool calls (prompt injection), before shipping anything exposed to the internet, and when the user asks for a security review or audit. Traces untrusted input to dangerous sinks, checks authorization on every path, and reports only verified, exploitable findings with severity and a fix.
license: MIT
metadata:
  category: craft
  version: "1.2.0"
---

# Security Audit

Security review is not a checklist recital; it's tracing how an attacker's input flows through the system and finding the places where it can do something it shouldn't. Report findings that are real and reachable, with a concrete exploit path. A short list of verified issues gets fixed; a long list of maybes gets ignored.

**Scope and ethics:** review code you've been asked to review. Don't probe production systems or third-party services, and don't write weaponized exploits. A clear description of the attack path and a failing test are enough to prove a finding.

## Method

1. **Map trust boundaries.** Where does untrusted data enter? HTTP params, headers, cookies, bodies, file uploads, webhooks, queue messages, environment and config files, third-party API responses, LLM outputs, and content an agent reads (web pages, issues, documents).
2. **Find the dangerous sinks.** SQL and NoSQL queries, shell execution, file system paths, template rendering and HTML output, deserializers, redirects, outbound HTTP, cryptographic operations, privilege changes, and LLM tool calls with side effects.
3. **Trace sources to sinks.** For each path, check what validation, encoding, parameterization, or authorization sits in between, and whether it's applied on *every* path, including error handlers, background jobs, and admin endpoints.
4. **Check authorization separately from authentication.** "Logged in" isn't "allowed". For every object access, confirm the code checks that *this* user may act on *this* object (IDOR is the most common serious web bug).
5. **Verify reachability** before reporting. Is the endpoint exposed? Is the input actually attacker-controlled? Is there an upstream control you missed?

## What to look for

| Area | Typical bugs |
|---|---|
| Injection | String-built SQL, shell commands with interpolated input, template injection, LDAP and XPath injection |
| Access control | Missing ownership checks (IDOR), privilege escalation via mass assignment, admin routes without role checks, tenant isolation gaps |
| Authentication and sessions | Weak password storage (fast or unsalted hashes such as MD5 or SHA-256; acceptable choices are argon2id, scrypt, bcrypt, or PBKDF2 with a high iteration count), missing rate limits on login and reset, predictable tokens, sessions not invalidated on logout or password change, JWT `alg` confusion |
| Secrets | Keys in code, config, logs, error messages, or client bundles; overly broad tokens |
| Web | XSS (unescaped output, `dangerouslySetInnerHTML`, `v-html`), CSRF on state-changing requests, open redirects, permissive CORS with credentials |
| Files | Path traversal (`../`), unrestricted upload types, zip slip, serving user files from the app's origin |
| Server-side requests | SSRF to internal addresses and cloud metadata (`169.254.169.254`) via user-supplied URLs or webhooks |
| Deserialization | `pickle`, Java native serialization, YAML `load`, or `eval` on untrusted data |
| Crypto | Home-made crypto, ECB mode, static IVs, `Math.random` for tokens, non-constant-time secret comparison |
| Money and limits | Race conditions in balance updates, negative quantities, client-trusted prices, missing idempotency keys |
| LLM and agents | Prompt injection from retrieved content steering tool calls; tools that act (send, delete, pay) without confirmation; data exfiltration via rendered links or images; model output passed to shells, SQL, or HTML unescaped |
| Dependencies | Known-vulnerable versions (`npm audit`, `pip-audit`, `cargo audit`, `govulncheck`, `osv-scanner`) that are actually reachable |
| Logging | Passwords, tokens, or personal data in logs; missing audit trail for sensitive actions |

## Finding format

```markdown
**[high] IDOR: any user can read any invoice**: `api/invoices.ts:42`
`GET /invoices/:id` loads by ID without checking `invoice.accountId === session.accountId`.
Attack: authenticated user iterates IDs and downloads other customers' invoices.
Fix: scope the query by account (`where: { id, accountId: session.accountId }`) and add a test that a second account gets 404.
```

Severity: **critical** (remote, unauthenticated, broad impact), **high** (authenticated user can access or modify others' data, or significant secrets exposed), **medium** (needs unusual conditions or limited impact), **low** (defense in depth). Score findings with `bug-triage` (security bugs score likelihood by reachability and attacker motivation). Report them, and change code only when the user asked for fixes.

## Fixing

- Fix the class, not the instance: parameterized queries everywhere, a single authorization helper, output encoding by default.
- Add a test that demonstrates the attack fails.
- Prefer well-vetted libraries for crypto, auth, sanitization, and parsing over custom code.
- Don't break legitimate behavior: verify the fix with the existing suite.
