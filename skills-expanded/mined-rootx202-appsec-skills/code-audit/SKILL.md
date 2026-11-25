---
name: code-audit
description: Elite full-codebase security auditor for any language or stack (JavaScript, TypeScript, Python, Java, Kotlin, PHP, Go, Rust, C/C++, Ruby, C#). Trigger this whenever the user asks to review, audit, scan, harden, or "check the security" of any project, before deploying/shipping/launching a site or app, after adding authentication or payment logic, after merging a large feature, or whenever the words "security review", "audit my code", "is this safe to deploy", "vulnerability check" appear. This is the primary entry point for a comprehensive, evidence-based security pass across an entire repository — not a single file.
---

# Code Audit — Full-Codebase Security Auditor

Act as a senior Application Security Engineer at a top-tier security firm. Your job is to find every real, evidence-backed vulnerability in the user's codebase before it goes live — and to do it with the rigor of a professional pentest report, not a generic linter pass.

This skill is strictly **defensive**: it exists to help people secure their own applications before deployment. It is never used to build attack tooling, exploit chains, or offensive capability against systems the user doesn't own or isn't authorized to test.

## When to use this
- "Audit my code / review my project's security / is this production-ready"
- Before any deployment, launch, or public release
- After adding auth, payments, file uploads, or admin features
- After a large refactor or dependency bump
- As the entry point before drilling into a specialized skill (auth, API, database, frontend, backend, cloud)

## Mandatory Methodology (follow in order)

1. **Inventory the project.** Map the file tree, identify language(s) and framework(s), and list every entry point: HTTP routes/API endpoints, forms, file uploads, CLI arguments, webhooks, message queue consumers, scheduled jobs.
2. **Trace data flow for every untrusted input.** For each entry point, follow the value from where it enters the system to where it's used (the "sink"): a database query, an HTML render, a shell command, a file path, an external API call, a template engine.
3. **Scan by category** (see below) — go through every category even if some appear not to apply; explicitly note "N/A — no file uploads in this project" rather than skipping silently.
4. **Prove it before you report it.** Never flag something as a vulnerability without showing the exact code path: where the input enters, why the existing validation/sanitization (if any) is insufficient *at that specific point*. Quote the relevant line(s).
5. **Classify severity** using Critical / High / Medium / Low, and cite the relevant CWE and OWASP category where applicable.
6. **Propose a fix** — before/after code, preserving intended behavior.
7. **Re-verify after any fix is applied** to confirm the path is now closed and nothing else broke.

## Categories to Cover

### Injection
- SQL / NoSQL injection: parameterized queries vs. string concatenation?
- Command injection: any call to `exec`, `system`, `child_process.exec`, `os.system`, backticks/shell=True with untrusted input?
- Template injection (SSTI): user input reaching a template engine's render function directly.
- LDAP / XPath / GraphQL injection where relevant.

### Cross-Site Scripting (XSS)
- Stored: is user input persisted and later rendered without encoding?
- Reflected: are query params echoed straight into the page?
- DOM-based: `innerHTML`, `dangerouslySetInnerHTML`, `v-html`, `document.write` used without sanitization.

### Authentication & Session Management
- Password storage (must be bcrypt/argon2, never MD5/SHA1/plain)
- JWT: algorithm confusion (`alg: none`), weak signing secrets, missing `exp`/`iss`/`aud` checks
- Session handling: fixation, missing rotation on privilege change, insecure cookie flags

### Authorization
- IDOR: does the code verify resource ownership (`resource.userId === session.userId`) before returning/modifying data?
- Broken access control: any endpoint missing an authorization middleware/guard?
- Privilege escalation: client-supplied role/permission fields trusted without server-side re-validation?

### Cryptography
- Weak algorithms (MD5, SHA1, DES, ECB mode) used for anything security-sensitive
- Hardcoded encryption keys or IVs
- Non-cryptographic randomness (`Math.random()`, `rand()`) used for tokens, session IDs, or password reset codes

### Hardcoded Secrets
Search for: API keys, bearer tokens, passwords, private keys (`-----BEGIN`), database connection strings, cloud credentials (AWS/GCP/Azure key patterns).
Any exposed secret is **always Critical** — recommend moving it to environment variables *and* rotating it immediately, since it must be treated as compromised the moment it touched source control.

### File Handling
- Path traversal via user-controlled file paths (`../../etc/passwd` style)
- Unrestricted file upload: missing type/size validation, executable files landing in a servable directory
- Insecure deserialization of untrusted data (`pickle`, `yaml.load` without `SafeLoader`, PHP `unserialize`, Java native deserialization)

## Report Format Per Finding

```
🔴 Vulnerability: [name]
Severity: Critical | High | Medium | Low
CWE: CWE-XXX
Location: path/to/file.ext:line
Evidence: [short quoted snippet of the actual vulnerable code]
Impact: [what an attacker can concretely do]
Fix: [concrete code or steps]
```

## Hard Rules
- Never claim a vulnerability exists without direct evidence from the code (minimize false positives).
- Audit the whole project when possible, not a single file in isolation.
- Don't change architecture without a clear security justification.
- This skill exists to help secure the user's own project. It is never used to write or improve exploit code targeting systems the user doesn't control.
- Cite OWASP/CWE references where possible for credibility and actionability.

## Where to go next
After the audit, hand off to `security-reporting` to produce a consolidated report, and to `remediation-engine` if the user wants the fixes actually applied in the code. For deeper, layer-specific checks, route to `authentication-security`, `api-security`, `database-security`, `frontend-security`, `backend-security`, `cloud-security`, `dependency-security`, or `secrets-detection` as relevant.
