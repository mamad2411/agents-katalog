---
name: sast-semgrep-hunting
description: "Static Application Security Testing using Semgrep MCP for white-box source code vulnerability discovery. Use when source code is available for review, when performing code audit, when validating dynamic findings against source, when hunting for injection sinks, insecure deserialization, hardcoded secrets, cryptographic weaknesses, authentication bypass patterns, or any taint-flow analysis from user input to dangerous sink. Integrates with hunt-* skills to confirm dynamic findings statically or discover candidates for dynamic validation. Keywords: source code review, static analysis, SAST, code audit, taint analysis, input validation, sink analysis, secure code review, white-box testing, semgrep rules."
---

## SAST WITH SEMGREP — WHITE-BOX VULNERABILITY HUNTING

> Use when source code is available. SAST findings guide dynamic testing — they are NOT reportable alone. Every static finding must be validated with a real HTTP request.

### When to Use

- Source code available (cloned repo, shared codebase, decompiled APK via `jadx`)
- Confirming a dynamic finding has a real vulnerable code path
- Discovering injection points invisible from black-box (internal routes, admin panels, cron jobs, message queue handlers)
- Finding hardcoded secrets, API keys, weak crypto
- Mapping user-input → dangerous-sink taint flows before crafting targeted payloads
- Prioritizing attack surface — which endpoints handle user input unsafely?

---

### Semgrep MCP Tools

| Tool | What It Does | When to Use |
|---|---|---|
| `security_check` | Quick scan of a code snippet | Fast check on suspicious code block |
| `semgrep_scan` | Scan files with a named config | Broad or class-specific scanning |
| `semgrep_scan_with_custom_rule` | Scan with your own YAML rule | App-specific pattern hunting |
| `get_abstract_syntax_tree` | Output AST of code | Complex taint/flow analysis |
| `supported_languages` | List supported languages | Verify target language coverage |

---

### Hunting Workflow

#### Phase 1: Broad Sweep

```
semgrep_scan with config: "p/security-audit"
→ Catches OWASP Top 10 patterns across all supported languages
```

#### Phase 2: Class-Specific Deep Scan

Based on the target's tech stack, run targeted configs:

| Target Pattern | Semgrep Config |
|---|---|
| SQL queries with user input | `p/sql-injection` |
| HTML output without encoding | `p/xss` |
| URL/HTTP requests with user input | `p/ssrf` |
| API keys, tokens, passwords | `p/secrets` |
| JWT handling | `p/jwt` |
| Object deserialization | `p/deserialization` |
| Command execution | `p/command-injection` |
| Path traversal | `p/path-traversal` |
| Crypto weaknesses | `p/crypto` |
| Django-specific | `p/django` |
| Flask-specific | `p/flask` |
| Express/Node | `p/nodejs` |
| Java/Spring | `p/java` |
| React | `p/react` |

#### Phase 3: Custom Rules for App-Specific Patterns

Write targeted rules when the app uses patterns not covered by public rulesets:

**Find unvalidated redirects:**
```yaml
rules:
  - id: open-redirect-user-input
    patterns:
      - pattern: redirect(request.$METHOD(...))
    message: "Redirect using user-controlled input"
    languages: [python]
    severity: WARNING
```

**Find raw SQL via string formatting:**
```yaml
rules:
  - id: sqli-fstring
    pattern: |
      cursor.execute(f"...{$INPUT}...")
    message: "SQL injection via f-string interpolation"
    languages: [python]
    severity: ERROR
```

**Find missing auth decorators:**
```yaml
rules:
  - id: missing-auth-decorator
    patterns:
      - pattern: |
          @app.route(...)
          def $FUNC(...):
              ...
      - pattern-not: |
          @login_required
          @app.route(...)
          def $FUNC(...):
              ...
    message: "Route handler without @login_required"
    languages: [python]
    severity: WARNING
```

#### Phase 4: Validate Dynamically

**Critical rule:** SAST findings alone are NOT reportable findings.

| SAST Finding | Dynamic Validation Step |
|---|---|
| SQLi sink with user input | Craft payload targeting that parameter via Burp |
| Hardcoded API key/secret | Test key permissions against the service |
| Missing auth on route | Access route unauthenticated via curl/Playwright |
| SSRF sink with partial filter | Craft bypass using filter gaps visible in source |
| Insecure deserialization | Build serialized payload for the specific gadget chain |
| Open redirect | Confirm redirect works with external domain |
| Command injection sink | Confirm with time-delay or OOB payload |

---

### Integration with Dynamic Hunt Skills

| When hunt-* skill finds... | Use Semgrep to... |
|---|---|
| Reflected XSS but filtered | Read source to find the filter logic and craft bypass |
| IDOR on `/api/users/{id}` | Check source for authorization checks on that handler |
| Error-based SQLi hint | Confirm the query construction pattern in source |
| JWT accepted without verification | Find the JWT validation code (or lack thereof) |
| SSRF partially blocked | Read the URL validation function to find bypass |
| Race condition suspected | Confirm no mutex/lock in the critical section code |

---

### AST Analysis for Complex Flows

Use `get_abstract_syntax_tree` when:
- Taint flow crosses multiple files/functions
- Need to understand custom sanitization logic
- Mapping class inheritance for deserialization gadgets
- Understanding middleware/decorator chains that apply auth

---

### Triage Integration

Before reporting any SAST-assisted finding, confirm:

1. ✓ **Reachable** — user-controlled input actually reaches the sink (not dead code, not behind impossible conditions)
2. ✓ **Exploitable** — no intervening sanitization that blocks the payload
3. ✓ **Validated dynamically** — real HTTP request demonstrates the impact
4. ✓ **7-Question Gate passed** — as always, run through triage-validation

**SAST evidence enhances reports** — include the vulnerable code snippet + source file/line as supplementary evidence alongside the dynamic PoC. This helps triagers confirm the root cause and accelerates fixes.

---

### Related Skills & Chains

- **`hunt-sqli`** — Use Semgrep to find SQL construction patterns, then validate with injection payloads from the hunt-sqli pattern library.
- **`hunt-rce`** — Find `exec()`, `eval()`, `system()`, `Runtime.exec()` sinks via Semgrep, confirm reachability, then exploit.
- **`hunt-ssrf`** — Map all HTTP request functions that accept user input. Semgrep finds them faster than black-box fuzzing.
- **`hunt-auth-bypass`** — `missing-auth-decorator` rule pattern reveals unprotected routes instantly.
- **`hunt-api-misconfig`** — Find mass assignment by checking which model fields are writable without allowlists.
- **`supply-chain-attack-recon`** — Semgrep can scan for known-vulnerable dependency usage patterns.
- **`hunt-xss`** — Find template rendering without auto-escaping, raw HTML insertion, `dangerouslySetInnerHTML` usage.
- **`apk-redteam-pipeline`** — After jadx decompile, scan the Java/Kotlin source with Semgrep for hardcoded secrets, insecure crypto, exported components.
