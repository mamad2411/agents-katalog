---
name: security-scan
description: Scans the codebase for injection, broken auth, unsafe deserialization and similar flaws, then ranks each finding by severity.
disable-model-invocation: true
---

Scan for security vulnerabilities in: $ARGUMENTS (the whole repository if empty).

1. Map the entry points first: HTTP routes, queue consumers, CLI args, file uploads, webhooks.
2. Trace each input toward its sinks. Look for SQL or NoSQL built with string concatenation, shell calls with interpolated values, unescaped HTML output, path joins using user text, unsafe deserialization (pickle, yaml.load, eval), SSRF through fetched URLs, open redirects, weak hashing (md5, sha1 for passwords), and hard-coded keys.
3. Check session and token handling: cookie flags, expiry, JWT algorithm checks, CSRF protection on state-changing routes.
4. Run the project's own linters or scanners if installed (semgrep, bandit, gosec, eslint-plugin-security). Quote their output, do not trust it blindly.
5. Do not edit files and do not run exploits against anything live.

Report a table: severity (critical, high, medium, low), file:line, the flaw, how an attacker would use it, and the smallest fix. Put critical items first. End by asking which finding to fix first.
