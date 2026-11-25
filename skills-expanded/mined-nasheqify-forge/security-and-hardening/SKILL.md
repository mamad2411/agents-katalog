---
name: security-and-hardening
description: >
  Security-first development discipline. Treat external input
  as hostile, secrets as sacrosanct, authorization checks as
  required. Methodology layer for the security / code-security
  agent personas.
  Triggers when handling external input, secrets, or authorization, or during pre-production hardening; NOT a substitute for the offensive security agent (pentest) or static code-security review.
status: active
invocation:
  primary: workflow-step
  secondary: [user-facing]
disable-model-invocation: false
uses: []
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.
Without Buddy (plugin): if this session holds no Buddy boot entry, run `python3 <root>/scripts/forge_setup.py offer-check` once, as its own call (`<root>`: two levels above this skill's folder); if it prints a line, pass that offer to the user in one sentence, then continue with this skill.


# Skill: security-and-hardening

## Source

agent-skills at `eb07f19` (MIT License, © 2025 Addy Osmani); Forge's register of adopted methods.

## Purpose

**Security-first development discipline.** Treat external
inputs as hostile, secrets as sacrosanct, authorization
checks as required. Security is not a phase — it is a
constraint on every line of code that touches user data,
auth, or external systems.

This skill is a **methodology layer** — structured patterns
+ required thresholds that a persona (`security` agent for
pentest, `code-security` agent for static reviews) applies
concretely. Skill without persona = cheatsheet, persona
without skill = ad-hoc.

## When to use

- Build / solve with user input, auth, external APIs, file
  uploads, webhooks.
- Storage or transmission of sensitive data (PII, payment,
  credentials).
- Before a production deploy as a security review template
  (see `shipping_and_launch`).
- Before a Code Review Board L2 as preparation for the
  security sub-agent persona.

### Do not call for

- Throwaway prototypes / playground code without a
  persistence decision.
- Pure UI components without a data flow
  (frontend_ui_engineering is the right methodology).
- Pentest execution itself — that's the `security` agent
  (offensive).
- Static code review for security findings — that's the
  `code-security` agent.

## Standalone

Why an own skill and not a mode of `code_review_board` or
`agents/code-security`? Three disciplines, three personas:

- **`code_review_board`** = review run on a concrete code
  diff, multi-persona, findings output. Operates on an
  existing diff. Needs methodology as an anchor, but is
  itself not a methodology container.
- **`agents/code-security`** = reviewer persona in the
  Code Board, checks the diff for security findings.
  Applier, not methodology owner.
- **`agents/security`** = offensive pentest persona,
  executes recon / exploit. Result owner, not the
  discipline maintenance owner.
- **`security_and_hardening` (this skill)** = the ongoing
  methodology collection — boundary system, OWASP
  patterns, auth flows, audit triage. Loaded by personas;
  lives independent of single diffs / reviews.

Deleting + integrating into `code_review_board` as a mode
would tie the discipline to diff reviews — but security
methodology applies during building, before any boundary
code, in spec authoring (auth-flow design), not just at the
review step. Standalone: methodology container for **all**
phases, consumed by 3 personas.

## Three-tier boundary system

### Always do (no skip)

- **Validate all external input** at system boundaries (API
  routes, form handlers, CLI args).
- **Parameterize all database queries** — never concatenate
  user input into SQL / Cypher.
- **Encode output** against XSS (use the framework's auto
  escaping, don't bypass it).
- **HTTPS** for all external communication.
- **Hash passwords** with algorithm-specific thresholds
  (see `owasp.md` §Password-hashing thresholds — never plaintext,
  never MD5 / SHA-1 / SHA-2).
- **Set security headers** (CSP, HSTS, X-Frame-Options,
  X-Content-Type-Options).
- **httpOnly + secure + sameSite cookies** for sessions.
- **`npm audit` / `pip-audit` / dependency scan** before
  every release.

### Ask first (user-approval required)

- New auth flows or changes to existing auth logic.
- Storage of new sensitive data categories (PII, payment).
- New external service integration.
- CORS config change.
- Adding a file-upload handler.
- Rate-limiting / throttling change.
- Extending permissions / roles.

### Never do

- **Never commit secrets** (API keys, passwords, tokens).
- **Never log sensitive data** (passwords, tokens, full
  credit card numbers).
- **Never trust client-side validation as a security
  boundary**.
- **Never disable security headers for convenience**.
- **Never `eval()` / `innerHTML` / `exec()`** with
  user-provided data.
- **Never store sessions in client-accessible storage**
  (localStorage for auth tokens).
- **Never expose stack traces / internal error details** to
  end users.

## OWASP Top 10 prevention

When writing or reviewing code that touches queries or commands, authentication or password storage, rendered user
content, access control, security configuration or sensitive data: read and follow
`skills/security_and_hardening/owasp.md` (injection, authentication with the password-hashing thresholds, XSS,
access control, misconfiguration, sensitive data exposure, the rest in short form).

## Input validation and rate limiting

When code accepts external input or file uploads, or exposes an endpoint: read and follow
`skills/security_and_hardening/boundaries.md` (schema validation at boundaries, file-upload safety, rate
limiting).

## Dependencies, secrets and untrusted output

When triaging a dependency-audit result, when code or configuration handles a secret, and when external error, log
or tool output is analysed or shown: read and follow `skills/security_and_hardening/secrets-and-supply-chain.md`
(dependency-audit decision tree, secrets management, untrusted-error-output discipline).

## Security review

When reviewing a change for security and before calling security-relevant work done: read and follow
`skills/security_and_hardening/review.md` (security review checklist, red flags, common rationalizations,
anti-patterns).

## Contract

### INPUT

- **Required:** code / spec with a user-facing boundary,
  auth flow, or external service integration.
- **Optional:** threat-model hint (which attacker class,
  which trust boundaries).
- **Context:** repo `CLAUDE.md` privacy-HARD constraint,
  `.gitignore` (secrets), `.env.example` (secret template),
  existing `agents/security.md` +
  `agents/code-security.md` as persona bind.

### OUTPUT

**DELIVERS:**
- Structured security review (boundary system + OWASP
  checklist + audit findings + dependency decision).
- Concrete pattern recommendations (validation schema,
  auth flow, header config, rate-limit values).
- Pre-production checklist as a Markdown block.

**DOES NOT DELIVER:**
- **No pentest run** — that's `agents/security.md`
  (offensive persona, autonomously runs recon / exploit /
  etc). Skill = methodology, agent = applier.
- **No static code review run on a concrete diff** — that's
  `agents/code-security.md` (reviewer in the Code Review
  Board). The BAD / GOOD pattern examples in this skill
  body are **methodology illustrations**
  (what's-right-discipline), not diff-scan heuristics. The
  code-security agent reads these patterns as anchors but
  scans the concrete diff itself.
- **No secret scanning** — that's hook mechanics
  (pre-commit + scanning tooling), not skill.
- **No production incident response** — that's
  `root_cause_fix` (phase A analysis) plus the security
  agent (forensics).

**ENABLES:**
- Build workflow verify phase: the security sub-agent
  persona in Code Review Board L2 uses this skill as the
  methodology anchor.
- Shipping-and-launch: pre-production security review step
  references this checklist.
- Council decisions on auth architecture: trade-off
  analysis references these patterns.

### DONE

- Three-tier boundary checked (always-do all met,
  ask-first explicitly user-confirmed, never-do violations
  none).
- OWASP Top 10 sweep performed (at least A1 injection +
  A2 auth + A4 access control + A6 sensitive data — the
  others context-dependent).
- Input validation at every boundary via a schema (Zod /
  Pydantic / etc).
- Dependency audit run + decision tree applied.
- Security review checklist ticked or explicitly
  documented as N/A.

### FAIL

- **Retry:** an audit tool isn't installable / runnable →
  try an alternative tool (`pip-audit` instead of
  `safety`).
- **Escalate:** architecture conflict between spec and
  security pattern (e.g. spec says "token in
  localStorage", pattern says "never") → council or
  spec_amendment_verification.
- **Abort:** not foreseen — security findings are
  surfaced, never silently skipped.

## Boundary

- **No pentest run** → `agents/security.md` (offensive
  persona).
- **No static review run on a code diff** →
  `agents/code-security.md` (reviewer persona in
  code_review_board).
- **No compliance audit** (GDPR, SOC2, HIPAA) — outside
  skill scope, dedicated tooling.
- **No crypto implementation** (writing your own
  algorithms) → NEVER, use a library.
- **No bug fix** → `root_cause_fix` (a security bug is a
  bug; runs through the 5-step lifecycle).

## References

| Topic | SoT |
|-------|-----|
| Offensive pentest persona | `agents/security.md` |
| Static code-security reviewer | `agents/code-security.md` |
| Pre-production security review | `skills/shipping_and_launch/SKILL.md` |
| Untrusted error output | `skills/root_cause_fix/diagnosis.md` §Triage checklist |
| Required checklist | see `review.md` §Security review checklist (no separate references/ file) |
| Privacy constraint | user profile `[INVARIANT] Privacy HARD` |
