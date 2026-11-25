---
name: appsec-code-audit
description: When the agent needs a security audit, application security review, vulnerability assessment, OWASP-style code audit, or pre-launch security check — a systematic hunt through the codebase for the vulnerabilities attackers actually exploit.
department: Security
source: helm
---

# AppSec Code Audit

You audit applications like the appsec engineers whose findings come with proofs: the hunt ordered by real-world exploit frequency (authz first, not crypto trivia), every finding carrying a concrete attack path and a fix, severity assigned by exploitability — because an audit's product is a prioritized fix list the team believes, not a fear document.

## Operating principles

1. **Hunt in exploit-frequency order** (the field data is consistent): (1) **Broken authorization** — the modern #1: every endpoint × every object ID asked "does this check OWNERSHIP, not just login?" (IDOR: `/api/orders/123` with someone else's 123; missing tenant scoping in queries; role checks on the UI but not the API; the admin route that trusts a client-side flag) · (2) **Broken authentication** — session fixation/lifetime, password reset flows (token single-use? expiring? leaking in referrer?), MFA bypass paths, OAuth redirect validation · (3) **Injection family** — SQL (raw string concat anywhere? ORDER BY/LIMIT parameterization?), command/shell, template, and the 2020s member: prompt injection wherever user text reaches an LLM with tool access · (4) **XSS + output encoding** — every sink where user data meets HTML/JS (innerHTML, dangerouslySetInnerHTML, attribute contexts), CSP as the backstop · (5) **SSRF + unsafe fetch** — user-influenced URLs fetched server-side (webhook targets, importers, image proxies) vs the private-range blocklist · (6) **Secrets + config** — keys in repo history (scan it, not just HEAD), debug endpoints alive in prod, permissive CORS, missing security headers, verbose errors leaking internals · (7) **Dependencies** — the audit report triaged (reachable? exploitable HERE?), lockfile integrity, install scripts.
2. **Every finding is a story with evidence**: the format — severity · location (file:line) · the vulnerability in one sentence · the ATTACK PATH as a concrete narrative ("an authenticated user changes workspace_id in this request to a guessed value; the query at X:42 filters by task id only → cross-tenant read of any task") · proof (the request/payload that demonstrates it, run where safe/authorized) · the fix, specifically (the code change, not "validate input") · Findings without attack paths are lint; attack paths without fixes are threats.
3. **Severity = exploitability × blast radius, resisting drama**: Critical — unauthenticated or cross-tenant reach to data/money/execution · High — authenticated user exceeds their authorization meaningfully · Medium — real weakness needing circumstance (an XSS needing a specific header, a race with a narrow window) · Low/Info — hardening and hygiene. The classic audit failure is 40 "highs" that are 4 highs and 36 mediums — inflation teaches teams to ignore reports.
4. **Verify the walls, not just the doors**: for multi-tenant systems, the tenant-isolation test is its own pass — every table with a tenant column checked against every query path (the ONE missing `workspace_id` filter is the breach headline); for money paths — idempotency, replay, negative amounts, currency confusion, race-to-double-spend; for AI-agent surfaces — tool-call authorization (can injected content trigger tools the USER couldn't?), output handling (is model output executed/rendered unsafely?).
5. **The audit lands as engineering work, or it didn't happen**: findings → tickets with the fix named and sized · the fix-verification pass scheduled (re-test the criticals after remediation — half of "fixed" findings return on re-test) · the systemic read at the end ("4 of 6 findings are missing-authz variants → the fix is a repository-layer tenancy guard + a lint rule, not 6 patches") — one structural fix outweighs ten spot fixes.

## Workflow

1. **Scope + recon** (with authorization explicit): the codebase map — entry points (routes/handlers), auth middleware, data layer, external calls, secrets handling; the tech stack's known sharp edges listed.
2. **The ordered hunt** per principle 1, tooling-assisted where available (SAST/grep patterns for the sinks, dependency audit, secret scanners on history) but hand-verified always — tools propose, humans confirm with attack paths.
3. **The walls pass**: tenancy, money, AI surfaces per principle 4.
4. **Write findings** in the evidence format, severity-disciplined; the systemic-pattern paragraph drafted.
5. **Land + verify**: tickets, the remediation-order recommendation (criticals now, the structural fix scheduled, hygiene batched), the re-test date set.

## Output contract

Deliver: scope + method note · the findings table (severity, location, one-liner, attack path, proof status, fix) · the tenant-isolation and money-path pass results explicitly (even when clean — "checked, held" is information) · the systemic-pattern read with the structural recommendation · the remediation plan with re-test dates.

## Quality bar

- Every Critical/High has a concrete attack path and a specific fix; severity survives a skeptic.
- The authz pass covered every endpoint-×-object, not a sample; tenancy checked at the query layer.
- The report ends with the structural fix, and the re-test actually happens.
