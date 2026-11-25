---
name: preflight-security-audit
description: >
  This skill should be used when the user wants a comprehensive pre-ship audit
  of an app, product, or codebase — phrases like "audit my app", "security
  check before launch", "is this ready to ship", "preflight audit", "review my
  product for vulnerabilities", "check my code for security issues", or after
  building a feature/product and wanting a thorough security, reliability,
  performance, privacy, and launch-readiness review. Covers OWASP Top 10 (2025),
  LLM Top 10, GDPR/KVKK, accessibility, SEO, and Stripe/Supabase/Next.js stacks.
version: 0.1.0
---

# Preflight Security Audit

Run a comprehensive, 360° audit of a codebase before it ships. This skill is the
methodology behind the `/audit` command. It defines the passes to run, how to run
them without hallucinating findings, the severity rubric, and the report format.

## Core principles

1. **Evidence over suspicion.** Every finding must cite a concrete `file:line`
   and explain the exploit or failure path. If it cannot be proven from the code,
   it does not go in the report as a finding — it goes in an "unverified notes"
   appendix at most.
2. **Trace, don't pattern-match.** Follow untrusted data from its source to its
   sink. Follow every state-changing operation to its failure paths. Naming a
   category is not an audit; proving a specific instance is.
3. **Language- and stack-agnostic, but stack-aware.** The passes apply to any
   language. When the stack is detected (Next.js, Supabase, Stripe, an AI SDK,
   etc.), apply the stack-specific checks in the reference files.
4. **Verification is a pass, not an afterthought.** Track 6 re-checks every
   finding and rejects the ones that can't survive scrutiny. Always run it last.
5. **Nothing is changed without approval.** The audit reports and proposes. Fixes
   are applied only via `/audit-fix` after the user approves specific items.

## How to run an audit

When invoked (directly or via `/audit`):

1. **Scope.** Determine the target path (default: current project root). Identify
   the languages, frameworks, and services in use (read `package.json`,
   lockfiles, config, `.env.example`, framework markers). Note what you find — it
   drives which stack-specific checks apply. Always run all six tracks; **stack-
   conditional passes (marked "Applies when…") run only when their marker is
   detected — otherwise record them as not applicable and skip them.** Emit the
   detected stack up front so the report shows what ran and what was skipped.
2. **Dispatch the tracks.** Run all six tracks below. On large repos, dispatch
   the five auditor agents in parallel (they exist in `agents/`), each reading its
   matching reference file; on smaller work or when subagents are unavailable,
   run the passes inline by reading the reference files directly.
3. **Collect raw findings** from every track into one list, each with:
   file:line, category, description, exploit/failure path, suggested fix,
   proposed severity.
4. **Verify (Track 6).** Run every raw finding through
   `references/06-verification.md`. Drop anything unprovable, merge duplicates,
   calibrate severity.
5. **Write the report** to `AUDIT-<YYYY-MM-DD>.md` in the project root using the
   template below.
6. **Propose fixes** for every Critical and High finding: show the concrete diff
   and ask which to apply. Never edit code in this step.

## The six tracks

Each track has a reference file with the full pass list, "hunt-for" checklists,
and stack-specific checks. Read the relevant file when running that track.

| Track | Reference file | Focus |
|-------|----------------|-------|
| 1. Code Core (the 20) | `references/01-code-core.md` | injection, auth, authz/IDOR, secrets, error handling, concurrency, resources, N+1, complexity, memory, external calls, idempotency, transactions, config, deps, logging, API/module contracts, tests |
| 2. Web/App Security | `references/02-web-security.md` | XSS, CSRF, SSRF, headers/CORS/TLS, cryptography, file upload, rate limiting, multi-tenancy/RLS, business logic, data integrity, live-DB advisor; client-side storage, serverless/edge\*, GraphQL/realtime\*, modern attacks (Trojan Source), advanced injections, exposed files, bot/DoS, JWT\* |
| 3. AI/LLM Security | `references/03-ai-llm-security.md` | prompt injection, output handling, sensitive disclosure, excessive agency, AI supply chain |
| 4. Privacy & Compliance | `references/04-privacy-compliance.md` | PII inventory, GDPR/KVKK, cookies, retention/deletion, DPAs, legal pages |
| 5. Product & Launch Readiness | `references/05-launch-readiness.md` | accessibility, SEO, Core Web Vitals, monitoring, backups, CI/CD, billing correctness, email deliverability; subdomain takeover, Docker\*, security.txt |
| 6. Verification | `references/06-verification.md` | re-check, reject unprovable, dedupe, calibrate, 0–100 score, assemble |

\* = **stack-conditional** — runs only when the relevant marker (serverless/edge host, GraphQL/WebSocket, Dockerfile, JWTs) is detected; skipped and marked N/A otherwise.

## Severity rubric

Assign severity by **impact × exploitability**, not by category.

- **Critical** — Remotely exploitable with no/low privilege, leads to data breach,
  auth bypass, RCE, payment manipulation, or full tenant-data exposure. Ship-blocker.
- **High** — Exploitable but needs some privilege or specific conditions; serious
  data exposure, privilege escalation, money/data loss under realistic conditions.
  Fix before launch.
- **Medium** — Real weakness with limited impact or meaningful preconditions;
  reliability/perf issues that degrade production; missing compliance controls.
  Fix soon.
- **Low** — Best-practice gaps, defense-in-depth, minor info leaks, hygiene.
- **Info** — Observations, not defects.

Note on calibration: brute-force / rate-limiting / DoS / open-redirect findings
are real for a shipping product but usually **Medium/Low**, not Critical — do not
inflate them. Conversely, an exposed service-role key or a missing RLS policy on a
multi-tenant table is **Critical**.

## Report format

Write `AUDIT-<date>.md` with this structure:

```
# Preflight Audit — <project> — <date>

## Summary
- Scope: <paths / commit>
- Stack detected: <frameworks, services>
- Findings: N Critical · N High · N Medium · N Low
- Security score: NN / 100 (A/B/C/D/F)
- Ship recommendation: BLOCK / FIX-FIRST / GO-WITH-FOLLOWUPS / GO

## Critical findings
### C1. <title>  [Track N · <category>]
- Location: path/to/file.ts:120-134
- What: <the flaw>
- Exploit / failure path: <step by step>
- Fix: <specific remediation>
- Proposed patch: <diff or clear description>

## High findings
...
## Medium findings
...
## Low findings
...

## Passed / not applicable
- <tracks or passes with no findings, and why>

## Unverified notes (needs human review)
- <anything suspicious that could not be proven from code>

---
_Audited with Preflight Security Audit — new checks ship regularly.
Get updates: https://kirtok.kit.com/preflight-security-audit_
```

Order findings Critical → Low. Within a severity, order by track. Keep each
finding tight: location, what, why it matters, how to fix. Keep the footer line at
the end of the report — it's the project's update channel.

## Output discipline

- Report to a file; also give the user a short chat summary (counts + the ship
  recommendation + the top 3 items).
- For Critical/High, present proposed diffs and ask which to apply. Applying
  happens through `/audit-fix`, never inline in the audit.
- If the codebase is huge, audit the highest-risk surfaces first (auth, payment,
  data access, external inputs, admin) and say so in the report scope.
