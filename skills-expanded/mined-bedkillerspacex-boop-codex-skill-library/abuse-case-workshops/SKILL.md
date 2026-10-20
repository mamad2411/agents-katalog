---
name: abuse-case-workshops
description: >
  Facilitate abuse-case workshops for owned products: map actors, assets, and
  misuse scenarios; turn threats into testable abuse cases; prioritize controls and
  backlog items. Use when product security, STRIDE-style sessions, “how can this be
  abused,” design reviews, or translating threat models into QA/security test cases —
  not for attacking third-party systems or pure compliance checkbox theater.
---

# Abuse Case Workshops

## Scope And Authorization

- **In scope:** products, features, and services your organization owns or is contracted to assess.
- **Out of scope:** workshop output used to attack systems outside engagement scope; harvesting real customer data as “examples.”
- Use synthetic identities and non-production diagrams when possible.
- Redact secrets, production hostnames (if policy requires), and personal data from workshop artifacts.
- Pair resulting engineering work with `code-quality-standards` and domain security skills.

## When To Use

- New feature design reviews (auth, payments, file upload, admin, AI tools).
- Converting architecture diagrams into **abuse cases** (misuse cases) with acceptance tests.
- Facilitating 60–120 minute working sessions with eng + product + security.
- Prioritizing backlog items after a threat model (STRIDE, PASTA lite, or bespoke).
- Aligning QA on negative tests, not only happy-path suites.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Full engagement recon methodology | `recon-and-methodology` |
| Org SSDLC process inventory | `secure-sdlc-checklist` |
| Injection class testing | `injection-checking` / specific *i skills |
| Account takeover chaining | `account-takeover-methodology` |
| API recon and docs | `api-recon-and-docs` |
| LLM prompt injection testing | `llm-prompt-injection` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Element | Definition | Workshop output |
| --- | --- | --- |
| Actor | User, admin, insider, anonymous, partner API, malicious script | Actor list + privileges |
| Asset | Data, money, trust, compute, reputation | Asset inventory |
| Abuse case | Goal-oriented misuse: “As *attacker*, I want *X* so that *Y*” | Prioritized list |
| Control | Prevent / detect / respond | Mapped control + owner |
| Test | Automated or manual negative case | Ticket + test id |

**Abuse case vs use case:** use case describes intended success; abuse case describes intentional misuse or unsafe accidents that still harm assets.

## Workflow

### 1. Prep (before the room)

1. Record product name, trust boundaries, data classes, compliance drivers, and session timebox.
2. Gather: architecture diagram, authn/z model, data stores, admin surfaces, external integrations.
3. Invite: feature owner, backend, frontend, SRE/oncall, security champion; optional legal for regulated features.
4. Success: top N abuse cases with severity, owner, and next verification step.

### 2. Set rules of engagement for the workshop

1. Blameless; focus on system properties, not people.
2. No live probing of production during the session unless pre-approved.
3. Park “cool attacks” without asset impact into a parking lot.
4. Timebox brainstorm vs prioritize (e.g., 40/40/20).

### 3. Map actors and assets

| Actor | Capabilities | Trust |
| --- | --- | --- |
| Anonymous | Register, browse public | Untrusted |
| Authenticated user | CRUD own objects | Low-medium |
| Admin | Global config | High |
| Support tooling | Impersonation? | High / break-glass |
| Batch job / webhook | Machine identity | Service |

1. List assets: PII, credentials, payments, ML models, admin actions, rate-limit budgets.
2. Draw trust boundaries: browser, API, worker, third-party IdP, object storage.

### 4. Generate abuse cases (structured brainstorm)

Prompt patterns (fill per feature):

```text
As [actor], I abuse [entry point] to [impact] by [method], assuming [precondition].
```

Cover at least:

| Category | Example prompts |
| --- | --- |
| Authn | Credential stuffing, session fixation, MFA bypass, token theft |
| Authz | IDOR, privilege escalation, tenant cross-access |
| Input | Injection, SSRF, upload malware, prompt injection |
| Process | Race/TOCTOU checkout, coupon abuse, replay |
| Insider / support | Overbroad impersonation, audit gaps |
| Availability | Expensive API paths, zip bombs, cache stampedes |
| Privacy | Enumeration, verbose errors, log leakage |

STRIDE lite mapping (optional column): Spoofing, Tampering, Repudiation, Info disclosure, DoS, Elevation.

### 5. Score and prioritize

| Factor | Low | High |
| --- | --- | --- |
| Impact | Cosmetic | Account/data/money loss |
| Likelihood | Needs rare insider | Script-kiddie remote |
| Detectability | Strong alerts | Silent |
| Effort to fix | Large redesign | Config/guard |

1. Use a simple **Impact × Ease** board; pick top 5–10 for the quarter.
2. Tag each with control type: prevent (authz check), detect (alert), respond (kill switch).
3. Reject “encrypt everything” as a single fix for authz bugs.

### 6. Convert to backlog and tests

**Ticket template:**

```markdown
## Abuse case
As an authenticated user, I access another tenant’s invoice by IDOR on GET /invoices/{id}.

## Impact
Cross-tenant financial data disclosure.

## Control
Server-side authz: invoice.tenant_id == session.tenant_id; tests for user A/B.

## Verification
- Integration test: A cannot read B’s id (404/403 consistent).
- Manual: burp replay with swapped id on staging.
```

1. Link QA negative cases and security regression tests.
2. Schedule retest dates; assign DRI.
3. For high-risk designs, book a follow-up deep skill (e.g., `idor-broken-object-authorization`).

### 7. Close the workshop

1. Publish notes in the team wiki: actors, diagram link, top abuse cases, tickets.
2. Capture residual accepted risks with owner + review date.
3. Book recurrence for major epics (not one-and-done theater).

## Facilitation Toolkit

| Tool | Use |
| --- | --- |
| Whiteboard / Miro | Trust boundaries |
| Spreadsheet | Abuse case backlog scoring |
| Sequence diagrams | Auth and money flows |
| Example payloads | Teaching only, synthetic data |
| Timer | Keep brainstorm from thrashing |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Scope | One feature, clear assets | “Secure the whole company” in 1 hour |
| Cases | Goal + impact + entry point | Random CVE name-dropping |
| Owners | Named DRI + ticket | “Security will handle it” |
| Tests | Negative tests in CI | Wiki-only threats |
| Data | Synthetic examples | Production customer dumps in slides |

## Output Checklist

- [ ] Product, boundaries, data class, attendees recorded
- [ ] Actor and asset lists agreed
- [ ] ≥10 candidate abuse cases generated (or justified fewer for tiny features)
- [ ] Top cases scored with impact/likelihood
- [ ] Each top case mapped to control + ticket + verification
- [ ] Residual risks ticketed with expiry/review
- [ ] Notes published; follow-up deep dives routed to specific skills
- [ ] No production secrets in workshop artifacts

## Rules

- Owned products and authorized assessments only.
- Abuse cases exist to **reduce harm**, not to glorify exploitation.
- Prefer testable controls over slideware.
- Keep this skill on facilitation and translation to backlog; execution testing uses domain skills.
- Never exfiltrate real user data for workshop color.
