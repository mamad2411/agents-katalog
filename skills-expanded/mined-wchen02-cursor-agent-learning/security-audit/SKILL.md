---
name: security-audit
description: Run a security audit (dependencies, secrets, auth, inputs). Use when the user asks for a security review, dependency audit, or to check for vulnerabilities and hardcoded secrets.
---

# Security Audit

When the user asks for a security audit or review, follow this workflow.

## 1. Determine scope

- **Full audit** → Do all steps below (dependencies, secrets, auth, inputs, report).
- **Quick check** (e.g. before PR) → Run only **Secrets** and **Dependencies** from [reference.md](reference.md).

Ask or infer from the request; if unclear, do a quick check and offer to run a full audit.

## 2. Full audit steps

1. **Dependencies** — Check for known vulnerabilities (e.g. `npm audit`, `pip audit`, or project-equivalent). List high/critical and suggest upgrades or mitigations.
2. **Secrets** — Search for hardcoded secrets, API keys, passwords. See [reference.md](reference.md) for patterns and paths to exclude.
3. **Auth and authorization** — Identify auth boundaries; note any endpoints that should require auth but don’t, or missing role checks.
4. **Inputs** — Note places that accept user/s external input (forms, API params, file upload). Ensure validation and sanitization are present; flag SQL/command injection or XSS risks where relevant.
5. **Report** — Summarize findings using the severity format in [examples.md](examples.md): Critical / High / Medium / Low, with file/line or area and a short recommendation.

## 3. Output format

Use the same severity labels and structure as in [examples.md](examples.md) so the report is consistent and actionable.

## Additional resources

- Full checklist and patterns: [reference.md](reference.md)
- Example findings and wording: [examples.md](examples.md)
