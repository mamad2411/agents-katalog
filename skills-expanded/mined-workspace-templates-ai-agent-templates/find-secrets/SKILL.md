---
name: find-secrets
description: Searches the working tree for API keys, tokens, private keys and risky config files and reports where each one lives.
disable-model-invocation: true
---

Look for committed or exposed secrets. Scope: $ARGUMENTS (whole working tree if empty).

1. List tracked and untracked files with `git ls-files` and `git status --short --ignored`. Note any .env, .pem, .key, .p12, credentials.json, id_rsa or *.tfstate file and whether it is tracked or ignored.
2. Search file contents for high-signal patterns: `AKIA[0-9A-Z]{16}`, `-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----`, `ghp_`, `xox[bp]-`, `sk_live_`, bearer tokens, connection strings with passwords, and assignments like password, secret or api_key with a literal value.
3. Check config for risk: debug flags, permissive CORS, default admin passwords, database URLs with real hosts.
4. Run gitleaks or trufflehog if installed, quoting what they report.
5. Never print a full secret: show the first 4 characters and the length only. Do not delete, rewrite history or rotate anything.

Report file:line, type, tracked or ignored, and confidence (likely real or likely dummy value). Finish by listing which credentials should be rotated first and ask whether to draft a cleanup plan.
