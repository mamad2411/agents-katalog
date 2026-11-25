---
name: security-review
description: Security-focused review of code changes - authorization gaps, injection, secrets exposure, unsafe deserialization, weak crypto. Use when the user asks for a security review, security audit of changes, or asks whether code is safe.
---

# Security Review

Review the requested scope for vulnerabilities. Report exploitable issues,
not stylistic preferences or theoretical patterns with no attack path.

## Checklist, in priority order

1. **Authorization** — every state-changing or data-returning path checks
   the caller's permission, not just authentication. Look for IDOR
   (object IDs taken from the request without ownership checks).
2. **Injection** — SQL/NoSQL built by string concatenation, shell commands
   with interpolated input, path traversal via user-supplied filenames,
   template injection, unsafe `eval`-likes.
3. **Secrets** — credentials, tokens, or private keys in code, config,
   logs, error messages, or test fixtures.
4. **Deserialization & parsing** — untrusted input fed to permissive
   parsers (pickle, yaml.load, XML with entities enabled).
5. **Crypto & transport** — homemade crypto, MD5/SHA1 for security
   purposes, disabled TLS verification, predictable randomness for tokens.
6. **Unsafe defaults** — debug endpoints, permissive CORS, missing rate
   limits on auth paths.

## Output format

For each finding:

```
[severity: critical|high|medium|low] file:line — title
  Attack path: how an attacker reaches and exploits this
  Fix: the concrete change
```

End with a verdict and the single most important fix. If the scope is
clean, say so explicitly — do not pad with non-findings.
