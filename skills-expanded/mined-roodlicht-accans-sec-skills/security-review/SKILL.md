---
name: security-review
description: Security review workflow for a PR, feature or codebase — scope, automated scans, manual OWASP/CWE pattern-check, prioritize and report. Uses secure-coding as pattern library.
---

# Security Review

## When to use

Use this skill when a bounded chunk of code is being checked systematically for security and a report is the deliverable. It is the workflow; the patterns themselves live in `secure-coding`, where phase 4 hands off.

Activates on:

- A request like "do a security review on <PR/branch/feature/service>", "review this code for security issues", "audit against OWASP Top 10", "is this safe to merge", "security audit before production".
- A PR that touches auth, crypto, user-input handling, session management, PII storage, deserialization, file upload, or external integrations. Then reviewing is not optional.
- A new service before it goes live, or an existing one touched again after an incident.
- A quarterly or release-cycle audit of high-risk subsystems on an older codebase.

### When NOT to use (handoff)

- Automated pre-merge gate → `security-gate` (command). That's a blocker with a policy. This skill is the substantive review behind it.
- Design-level threats before code exists → `threat-modeler` (agent). STRIDE, attack trees, and trust-boundary diagrams belong there.
- Offensive assessment with active exploitation → pentest skills (`web-exploit-triage`, `recon-agent`, `payload-crafter`). This skill flags; it does not exploit.
- Framework-deep review → start with the framework skill (`django-security`, `spring-security`, `rails-security`, `nextjs-security`, `api-security`), then come back here for the umbrella report.
- Standalone code-pattern question ("is this query safe?") → straight to `secure-coding`. This skill is the process around the patterns, not the patterns themselves.
- Dep-vuln triage only → `cve-triage`. It weighs exploitability (reachable path, EPSS) more finely than this skill.
- Secrets in git history only → `secrets-scanner`. This skill calls it, not the other way around.

This skill calls `secrets-scanner`, `sast-orchestrator`, `cve-triage` in phase 3, and `verification-loop` as the final step before the report ships.

## Approach

Seven phases. Don't skip them. Phases that "don't seem to apply" are often exactly where issues stay invisible. For a very small PR scope phase 2 may be brief and phase 5 limited, but the phase structure stays.

### 1. Set scope

Before opening a single file: know what you're reviewing and why.

- **Object of review.** PR diff, branch delta, specific directory, full service, a flow cross-section (e.g. "all code in the login path"). Note exactly which files/ranges are in scope.
- **Trigger.** Pre-merge, periodic audit, post-incident, compliance prep (ISO/SOC2/DORA). This determines which severities are blockers.
- **Depth.** *Light* = only the diff hunks plus what they directly call. *Medium* = diff plus first-order callers plus related tests and config. *Deep* = entire subsystem with control/data-flow analysis. Light is fine for small, isolated PRs. Anything touching auth, crypto, or untrusted input is at least medium.
- **Out-of-scope explicitly.** Infra/IaC outside this skill (handoff), UI-text changes, docs-only changes, third-party code outside the direct consumption path.
- **Deadline.** Influences how much depth, and whether a second reviewer is needed.

If scope after this phase doesn't summarize in one line, it's too broad. Narrow it or split it.

### 2. Recon: understand what you're looking at

A review without a mental model of the system is symptom-hunting. Build the model first.

- **Read the docs.** README, architecture diagrams, ADRs, API docs. They often state which claims the system makes (which threats are in scope).
- **Locate entry points.** HTTP routes (`grep` on route decorators, middleware chain), CLI handlers, message consumers, webhooks, scheduled jobs, event triggers. List them — these are your trust boundaries.
- **Mark sensitive call-sites.** Search for common foot-gun patterns: `eval`, `exec`, `subprocess.*shell=True`, `pickle.loads`, `yaml.load` without SafeLoader, `ObjectInputStream`, `innerHTML`, `dangerouslySetInnerHTML`, `verify=False`, `disable-ssl`, hardcoded AWS/GitHub token formats. They are not necessarily wrong, but each warrants attention.
- **Config and secrets handling.** Where do credentials come from? Env vars? Vault? Hardcoded? Config file? Rotation schedule known?
- **Auth model.** Who is a user? How is identity proven? Which roles and permissions? Where is authorization checked: middleware, per endpoint, per resource?

Output of this phase: a bullet list of entry points, trust boundaries, sensitive call-sites, and an auth-model summary. That's your map for phases 4–5.

### 3. Automated scan: what tools give you for free

Let the machine catch the flat patterns before you read by hand. Handoffs:

- **Secrets** → `secrets-scanner` (gitleaks, trufflehog, detect-secrets). Scan both working tree and git history. Every match is serious until proven otherwise — a key from git history stays leaked even when it's gone now.
- **SAST** → `sast-orchestrator` (Semgrep with community + language-specific rulesets, CodeQL for depth, SonarQube for trend). Run Semgrep at minimum; CodeQL on deep-mode reviews.
- **SCA / dep-vulns** → `cve-triage` (osv-scanner, grype, Dependabot/Renovate alerts). Filter for reachable path and EPSS before raising as a finding.
- **IaC/container/k8s if in scope** → `iac-security`, `container-hardening`, `k8s-security`.

Triage the raw tool output immediately: false positives written off with a reason; real findings forwarded to phase 6. Don't paste full tool dumps in the report — that's lazy and unreadable.

### 4. Manual pattern review

Walk the call-sites you marked in phase 2 through the six-phase walk from `secure-coding`: trust boundaries → input/output → identity → secrets/crypto → robustness → dependencies. For each finding note file, line, classification, and a short description.

What this phase adds on top of phase 3: context. SAST doesn't know that `get_document(id)` is called from an admin endpoint without an ownership check. You do, because phase 2 worked out the auth model.

Things SAST rarely catches:

- **Authorization gaps (IDOR).** Endpoint checks authentication but not whether the actor may see or modify the resource. Classic on `/api/<resource>/<id>` routes.
- **Auth-logic bugs.** Race condition between `check` and `act`, login side-channels (timing, error difference between "user doesn't exist" and "wrong password"), password-reset flow that allows account enumeration.
- **Session management.** Session not rotated after privilege change, logout that doesn't invalidate server-side state, cookie flags (HttpOnly/Secure/SameSite) not set.
- **Rate limiting and abuse.** Login, password reset, 2FA verify, payment retry: each without rate limit is a free brute-force or abuse target.
- **JWT misconfig.** `alg: none` accepted, algorithm confusion (HS256 with RSA pubkey as secret), expiry infinite, no `kid` rotation.
- **Deserialization and file upload.** Pickle/YAML/Java serialization on user paths, file upload without MIME / magic-byte validation, path traversal in filename.

### 5. Design and business-logic review

Issues that only become visible with system-level thinking. Not every review reaches this phase. Light/medium scope may skip it as long as phase 1 records the choice.

- **Holistic authorization model.** Are there privilege-escalation paths? Can a tenant-A user reach tenant-B data via an indirect endpoint? Are admin functions reachable via a non-admin route (cross-role pollution)?
- **Business-logic flaws.** Workflow bypass (jump to step 5 without going through 1–4), negative amounts, coupon stacking, double refunds, replay on idempotency keys.
- **Race conditions and TOCTOU.** Check-then-act on resource state (e.g. "is user still premium" → "execute premium action"), concurrent writes without locking, double-spend-style patterns in financial flows.
- **State-machine gaps.** Which transitions are enforced? What happens on an API call in a state that doesn't expect it?
- **Trust-boundary separation.** Does per-user code run in the same process space as cross-tenant admin code? Which config values are tenant-scoped, which are global?

If design depth is genuinely needed (e.g. new architecture, new external integration): hand off to `threat-modeler` for a STRIDE pass. This skill then notes in the report "threat model recommended for X, performed by <agent/person>".

### 6. Prioritize

Severity is impact × likelihood × compensating controls. CVSS v3.1 is the formal system, but a blocker/high/medium/low label is often faster for dev teams. Use both when the report goes to engineering and to compliance.

**Severity matrix:**

- **Blocker.** Pre-auth RCE, authentication bypass, secret/credential exposure that grants system access, mass PII leak, SQLi with OS-command reach, reachable dep-vuln with public exploit on an externally-exposed path. **Don't merge, don't deploy.**
- **High.** Authenticated RCE, IDOR on PII or financial data, stored XSS in admin context, SSRF to cloud-metadata endpoint, hardcoded production credential, JWT signature verification off, deserialization of user-controlled input on a critical path. **Merge blocked until fixed.**
- **Medium.** Reflected XSS outside admin context, self-XSS, missing rate limit on auth endpoint, verbose errors with internal paths, weak-but-not-broken crypto choice, outdated lib without reachable exploit, missing security headers in sensitive routes. **Fix this sprint or next.**
- **Low.** Missing HSTS/CSP/X-Content-Type-Options, version disclosure, verbose logging without PII, missing best practice without direct risk increase. **Backlog ticket; not a merge blocker.**

Exploitability weights in: a blocker behind a non-routable internal network can drop to high; a medium that's publicly reachable and unauthenticated can rise to high. Document the weighting — otherwise it's indefensible.

CVE-ID or CWE-ID always present where you can. See `verification-loop` Layer 2 for CVE/CVSS verification — no fabricated IDs.

### 7. Report + verification-loop

Build the draft report in the structure below. Then run `verification-loop` over it:

- **Layer 1**: scope check (does the report match the scope agreed in phase 1?), assumptions (every "reachable" or "exploitable" claim substantiated?), gap analysis (which entry points from phase 2 are unaddressed?), adversarial reader (what would the submitter attack as the weakest finding?), failure modes (do your fix suggestions work?), consistency (severities internally coherent?).
- **Layer 2**: CVE/CVSS verification against NVD/FIRST, payload-level (no ready-to-fire exploits for production targets in the report), substantiated claims, primary sources.

Adjust. Deliver only when verdict is pass (or revise with fixes applied).

## Output

Report template:

```
Security review — <scope>
Date: YYYY-MM-DD | Reviewer: <name/tool> | Depth: <light|medium|deep>

Scope:
  In: <files, ranges, flow>
  Out: <explicitly out-of-scope>
  Trigger: <pre-merge | periodic | post-incident | compliance>

Executive summary (3–5 lines):
  <status in one sentence>
  Blockers: N | High: N | Medium: N | Low: N
  Recommendation: <merge | merge-after-fixes | don't merge | wider scope needed>

Automated scan (summary, no dumps):
  Secrets (secrets-scanner): <N findings, X confirmed>
  SAST (sast-orchestrator): <N findings after triage>
  SCA (cve-triage): <N reachable, EPSS-weighted>
  IaC/container/k8s (if applicable): <N findings>

Findings (severity-sorted, blockers first):

## [BLOCKER] <short title>
  Location: <file:line[–line]>
  Classification: CWE-<N> | OWASP A0<x> | CVSS v3.1 <score> (<vector>)
  Pattern: <name, e.g. "pickle.loads on user-body">
  Impact: <what can the attacker do?>
  Reproduction: <steps or curl example; no version-specific exploit>
  Fix: <concrete patch direction, ideally with code alternative>
  Compensating: <existing controls limiting impact, where applicable>
  Handoff: <if specialist needed: threat-modeler, sast-orchestrator, etc.>

## [HIGH] ...
## [MEDIUM] ...
## [LOW] ...

Open questions for submitter:
  - <intent/context question>
  - <verification request the reviewer can't perform alone>

Non-findings explicitly:
  - <pattern that stood out but is not a finding, with reason — saves the
    next reviewer the same time>

Verification-loop:
  Verdict: <pass | revise | rewrite>
  Security verdict: <no red flags | red flag — solvable | red flag — blocking>
```

Guidance for the report itself:

- Findings are actionable or they're noise. Every finding has a location and a fix direction.
- Reproduction must work within the agreed scope; no public 0-day chains for production targets — see `verification-loop` Layer 2.
- "Non-findings explicit" prevents the next reviewer spending the same time. Two lines per item is enough.
- No long theoretical XSS lecture; link to OWASP cheat sheets and move on.

The report goes to the PR author or service owner, not to "stakeholders in general". Write for them.

## References

- OWASP Top 10 2021 — [https://owasp.org/Top10/](https://owasp.org/Top10/). Primary categories; every finding maps to an A0x.
- OWASP API Security Top 10 — [https://owasp.org/API-Security/editions/2023/en/0x11-t10/](https://owasp.org/API-Security/editions/2023/en/0x11-t10/). For API-scope reviews alongside or instead of Top 10.
- OWASP ASVS v4 — [https://owasp.org/www-project-application-security-verification-standard/](https://owasp.org/www-project-application-security-verification-standard/). Use as a requirement checklist on deep-mode reviews.
- OWASP Code Review Guide v2 — [https://owasp.org/www-project-code-review-guide/](https://owasp.org/www-project-code-review-guide/). Methodology basis for this workflow.
- CWE Top 25 — [https://cwe.mitre.org/top25/](https://cwe.mitre.org/top25/). For CWE classification of findings.
- NIST SP 800-53r5 — [https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final). Control families (AC, SI, SC) for finding mapping in compliance contexts.
- FIRST CVSS v3.1 — [https://www.first.org/cvss/v3-1/specification-document](https://www.first.org/cvss/v3-1/specification-document) and calculator [https://www.first.org/cvss/calculator/3.1](https://www.first.org/cvss/calculator/3.1).

## Categories

- core
- appsec
