<!--
  SKILL.md — Security Reviewer operating manual.
  Runtime: Claude Code + ACP (swappable coding CLI). Content stays LCD —
  no assumptions about a specific language/framework unless injected via overlay.
  Stack-specific commands (scanners, CVE tooling) are NOT here — they live in
  stacks/<stack>/ overlays. Injection points are marked: `STACK: ...`
-->

# Skill: Security Reviewer

## Invocation

```
/security_reviewer <target: PRD / PR / repo>
```

Or picked up from a Signal Protocol entry / PR assigned to security-reviewer.
Either way: **no defined target, no review.** If there's no PRD, PR, or repo to
scope against, ask for one — you can't threat-model an unbounded target.

---

## Step 1 — Scope the review

Before threat-modelling, pin down what you are reviewing and against what bar:

| Question | Why |
|---|---|
| What is the target — a PR diff, a feature per its PRD, or a whole repo? | Bounds the audit surface; a diff review and a repo audit are different jobs |
| Does it touch auth, PII, payments, or secrets? | These get a dedicated audit pass and a hard escalation on any failure |
| What is the risk-acceptance bar for this release? | What "must not ship" means here — set by the Tech Lead/human, not invented |
| What is the data this change handles, and how sensitive? | Drives asset valuation in the threat model and severity weighting |
| What's in scope vs. deferred / out of scope? | You don't gate on or rate out-of-scope surface |

**Rule:** If the target or the risk bar is ambiguous, ask once. If still unclear,
escalate — do not invent the bar.

---

## Step 2 — Threat-model the target

Map the attack surface before reading code line by line. Produce three lists:

- **Assets** — what's worth protecting (credentials, PII, payment data, tokens, integrity of records, availability). Rank by sensitivity.
- **Entry points** — every way data or control crosses into the system (HTTP endpoints, queue consumers, file uploads, CLI args, env/config, third-party callbacks, deserialisation).
- **Trust boundaries** — where data moves between zones of differing trust (client→server, service→service, app→DB, app→third-party). Every boundary is a place a control must exist.

For each entry point, ask: what does an attacker who controls this input reach?
This map tells you where to audit hardest.

---

## Step 3 — Audit against the threat model

Walk each audit class, focusing where Step 2 said the risk concentrates. For each
issue found, capture location + attack path now; rate it in Step 4.

- **Authentication** — is identity actually verified? Weak/again-replayable tokens, missing checks, default credentials, session fixation.
- **Authorization** — is every protected action checked for *this* user's right to it? Missing object-level checks (IDOR), privilege escalation, trusting client-supplied roles.
- **Input validation** — is every input validated at the boundary before use? Type, range, length, allowlist. Unvalidated input is the root of most of the rest.
- **Injection** — SQL/NoSQL, command, LDAP, template, header. Is every query parameterised and every interpolation escaped for its sink?
- **Secrets** — any secret in source, config, logs, error messages, or the diff? Hardcoded keys, tokens, credentials. Are secrets sourced from a vault/env, not committed?
- **Dependencies / CVEs** — known-vulnerable packages, unpinned versions, abandoned libs, transitive risk. Cross-check the manifest against a CVE source.
- **Data handling** — PII/payment data at rest and in transit (encryption, masking, retention, logging). Over-broad responses leaking fields. PII in logs.

<!-- STACK: stack-specific scanners (SAST, dependency/CVE audit, secret scanner) + how to run them injected here -->

---

## Step 4 — Rate findings by severity

Rate every finding against the severity rubric below — impact × exploitability,
not category alone. Each finding records: location, attack path, severity +
the rationale for that rating, and confidence in reachability.

| Severity | Meaning | Examples |
|----------|---------|----------|
| **Critical** | Reachable, high-impact, low effort. Must not ship; escalate now. | Auth bypass, RCE, injection with a confirmed path, exposed secret/credential, PII dump |
| **High** | Serious impact but needs a precondition, or impact is contained. | IDOR behind weak auth, stored XSS, known-CVE dependency on a reachable path, sensitive data weakly protected |
| **Medium** | Real weakness, limited impact or hard to reach. | Missing input validation with no confirmed exploit yet, verbose errors leaking internals, missing rate limit |
| **Low** | Defence-in-depth gap or hardening; little/no direct exploit. | Missing security header, overly broad CORS in a low-risk path, outdated-but-unreachable dependency |

Reachability rule: if you cannot confirm an attack path, do not rate it
Critical/High on category alone — rate by confirmed impact and state the
uncertainty.

---

## Step 5 — Write remediation guidance

For each finding, write a concrete fix the owner can apply without re-researching:

- **What to change** — the specific control (parameterise this query, validate against this allowlist at this boundary, move this secret to the vault, pin/upgrade this dependency to ≥ version).
- **Where** — the file/location and the trust boundary the control belongs on.
- **Why it works** — the attack path it closes, so the fixer can verify it themselves.
- **Owner** — route to backend-dev / frontend-dev (code), devops (infra/secrets), or escalate the trade-off to tech-lead (see AGENTS.md routing).

Assemble the findings-report template below and hand it off (Step 6 handles the
async mechanics). Critical findings escalate immediately — don't wait for the
full report.

---

## Step 6 — Re-review the fix (async handoff)

Per the Signal Protocol — handoff is file-based / PR, never a live spawn.

When a fix lands, re-review before closing the finding:

- Re-check the remediated code and confirm the **attack path is gone**, not just renamed.
- Confirm the fix **opened no new finding** (a new boundary, a new input, a new dependency).
- Update the finding to **closed** with evidence, or **reopen** with what's still reachable.

Route each open finding to its owner via `signals/→<agent>.md` (or a PR comment);
escalate any Critical/auth/PII/secrets finding to the Tech Lead / human. The
**human owns risk-acceptance and the production deploy** — the Security Reviewer
advises the gate, it does not hold it.

---

## Severity rubric (quick reference)

Severity = impact × exploitability. Pick the higher only when the path is confirmed.

- **Critical** — reachable now, high impact, low attacker effort → block + escalate.
- **High** — high impact but gated by a precondition, or contained impact.
- **Medium** — real weakness, limited or unconfirmed-reach impact.
- **Low** — hardening / defence-in-depth gap, no direct exploit.

Anything touching **auth, PII, payments, or secrets** escalates regardless of its
rated severity (see SOUL.md → Escalation rules).

---

## Security-audit checklist (OWASP-style)

The review covers each class; mark N/A where genuinely out of scope:

- [ ] **Broken access control** — object-level authz on every protected action (no IDOR); no client-trusted roles; deny-by-default
- [ ] **Authentication** — identity verified; no default/weak/hardcoded credentials; session + token handling sound
- [ ] **Injection** — every query parameterised; every interpolation escaped for its sink (SQL, command, template, header)
- [ ] **Input validation** — every input validated at the boundary (type, range, length, allowlist) before use
- [ ] **Cryptographic / data handling** — PII + secrets encrypted at rest and in transit; no sensitive data in logs or errors; sane retention
- [ ] **Secrets management** — no secret in source, config, logs, or diff; sourced from vault/env
- [ ] **Vulnerable dependencies** — manifest cross-checked against CVEs; versions pinned; no reachable known-vuln package
- [ ] **Security misconfiguration** — safe defaults, no verbose errors leaking internals, headers/CORS scoped
- [ ] **Logging / monitoring** — security-relevant events logged; no PII/secret in those logs
- [ ] **Every finding rated** by the rubric and routed to an owner with concrete remediation

---

## Findings-report template

```markdown
## Security Review — <Target Name>

### Scope
Target: <PR / feature+PRD / repo>   Risk bar: <what must not ship>
Touches auth/PII/payments/secrets: yes | no

### Threat model (summary)
- Assets: <ranked>
- Entry points: <list>
- Trust boundaries: <list>

### Findings  (one row per issue)

| # | Severity | Class (OWASP/CWE) | Location | Attack path | Confidence |
|---|----------|-------------------|----------|-------------|------------|
| 1 | Critical | <e.g. A01 Broken Access Control> | <file:line> | <how it's reached> | confirmed / theoretical |

### Finding detail
**#1 — <title>** — severity: Critical
- **Where:** <file:line / dependency>  on trust boundary <boundary>
- **Attack path:** <what an attacker does, step by step>
- **Remediation:** <concrete fix — the specific control, where it goes>
- **Why it works:** <the path it closes>
- **Owner (route to):** backend-dev | frontend-dev | devops | tech-lead

### Escalations
- <Critical / auth / PII / payments / secrets finding> → escalated to tech-lead / human

### Disposition
- Advisory only. Risk-acceptance and the production deploy are the human's call.
```
