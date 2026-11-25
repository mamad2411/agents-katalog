---
name: owasp-top-10-review
description: Walks a codebase category by category through the OWASP Top 10 and reports each confirmed weakness with file, line and a concrete fix.
---

# OWASP Top 10 review

Review the code against the current OWASP Top 10, one category at a time. Report only what you confirmed by reading the code.

## Steps

1. Map the surface first: entry points (routes, handlers, queue consumers), the auth layer, data stores and every place user input enters. Note the framework and its built-in protections.
2. For each category, search for its typical patterns, then open every hit:
   - Broken access control: handlers that load a record by id without checking the owner or role, missing checks on admin routes.
   - Cryptographic failures: MD5 or SHA-1 for passwords, hard-coded keys, plain HTTP, weak random for tokens.
   - Injection: queries, shell calls, templates and file paths built from input.
   - Insecure design: no rate limit on login or reset, no limits on expensive operations.
   - Misconfiguration: debug mode, default credentials, open CORS, verbose errors.
   - Vulnerable components: outdated packages with known advisories.
   - Authentication failures, integrity failures (unsigned updates, unsafe deserialization), logging gaps, and server-side request forgery.
3. Trace each suspect from input to the dangerous call. If a check on the path stops it, drop the finding.

## Rules

- Never claim a vulnerability you could not trace end to end.
- Do not run exploits or hit live systems. Read and reason only.
- Do not change code unless asked; propose patches.

## Report

Group by category. Per finding: `path:line`, severity, how it is exploited, the fix. List categories with no findings under "Checked, clean".
