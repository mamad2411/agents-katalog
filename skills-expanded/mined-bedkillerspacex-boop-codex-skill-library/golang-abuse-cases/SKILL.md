---
name: golang-abuse-cases
description: >
  Abuse-case / threat-driven design for Go services: enumerate misuse, fraud,
  automation abuse, and authZ failure modes; map controls, tests, and rate limits.
  Use during design/review of owned systems — authorized threat modeling only,
  not instructions to commit fraud against third parties.
---

# Golang Abuse Cases

## Scope And Authorization

- **In scope:** Threat modeling and hardening of applications you build or are
  authorized to assess.
- **Out of scope:** Planning real-world fraud, harassment, or attacks on third parties.
- Abuse cases complement **use cases** — intentional misuse by hostile or negligent actors.
- Pair with `golang-abac-design`, `rate-limit-bypass-testing` (authorized), `code-quality-standards`.
- Privacy/safety-sensitive products need legal/policy review of mitigations.

## When To Use

- Design docs for new Go APIs (payments, signup, messaging, uploads).
- Security design review before launch.
- Turning pen-test findings into regression abuse tests.
- Prioritizing guardrails (rate limits, authZ, audits).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| ABAC implementation | `golang-abac-design` |
| Auth middleware | `gin-middleware-auth` |
| Injection labs | injection skills / `ghauri-sqli-lab` |
| Load testing product | performance skills |
| Implementation quality | `code-quality-standards` |

## Concepts

| Term | Meaning |
| --- | --- |
| Use case | Intended actor goal |
| Abuse case | Hostile/ unintended goal using the system |
| Actor | External attacker, malicious insider, buggy client, scraper |
| Impact | Fraud loss, data leak, spam, resource exhaustion |
| Control | Mitigation in product/engineering |
| Residual risk | Accepted with owner |

### Template

```text
Abuse case ID: AC-…
Actor: …
Goal: …
Method (high level): …
Preconditions: …
Impact: …
Controls: …
Detection: …
Tests: …
Owner: …
```

Do not write step-by-step weaponization for crimes; keep methods at engineering depth
sufficient to design controls.

## Workflow

### 1. Frame the system

1. List trust boundaries (internet client, worker, admin, webhooks).
2. List sensitive assets (PII, funds, invite tokens, rate-limited resources).
3. List trust assumptions (email verified ⇒ human; webhook signature valid).
4. Success: catalog of top abuse cases with controls and tests linked to code.

### 2. Brainstorm abuse cases by category

| Category | Examples (product-dependent) |
| --- | --- |
| Authn | Credential stuffing, session fixation, token replay |
| Authz | IDOR, privilege escalation, tenant escape |
| Fraud | Promo abuse, referral loops, chargebacks |
| Automation | Scraping, invincible bots, fake accounts |
| Content | Spam, CSAM reporting paths (policy), injection in content |
| Resources | Large upload, expensive API zip bombs, fan-out bombs |
| Business logic | Race double-spend, coupon reuse, state skip |
| Supply | Malicious dependency — separate supply-chain review |

### 3. Prioritize

| Factor | Score impact |
| --- | --- |
| Financial loss | High |
| User safety / privacy | High |
| Reputation | Medium-High |
| Ease of automation | Raises likelihood |
| Detectability | Low detect → prioritize prevention |

Use simple MoSCoW or risk matrix; fix P0 before launch.

### 4. Map controls in Go architecture

| Control type | Go-oriented examples |
| --- | --- |
| Authn | hardened middleware, MFA step-up |
| Authz | ABAC/PDP deny default |
| Quotas | token bucket middleware per principal |
| Idempotency | keys on payment intents |
| Validation | strict decode, size limits, `http.MaxBytesReader` |
| Async | queue with backpressure |
| Audit | slog security events |
| Kill switch | feature flag disable endpoint |

```go
// Example: upload size limit
r.Body = http.MaxBytesReader(w, r.Body, 8<<20)

// Example: per-user rate limit key
key := "rl:msg:" + userID
if !limiter.Allow(key) {
    http.Error(w, "rate_limited", http.StatusTooManyRequests)
    return
}
```

### 5. Detection

- Metrics: spike in 401/403/429, signup velocity, payment declines.
- Logs: authz deny reasons, idempotency conflicts.
- Alerts: threshold breaches to on-call / fraud ops.
- Avoid logging secrets while detecting abuse.

### 6. Abuse-oriented tests

```go
func TestIDOR_CannotReadOtherTenant(t *testing.T) { /* ... */ }
func TestCoupon_SingleUse(t *testing.T) { /* concurrent double redeem */ }
func TestUpload_RejectsOversize(t *testing.T) { /* ... */ }
```

Use `go test -race` for racey financial paths. Table-driven negative tests.

### 7. Document in design review

Include abuse case table in RFC:

| ID | Abuse | Control | Test | Residual |
| --- | --- | --- | --- | --- |
| AC-01 | Cross-tenant read | ABAC tenant check | TestIDOR… | Low |
| AC-02 | SMS pump | Rate limit + captcha | … | Med cost |

### 8. Iterate post-launch

- Feed incident reviews into new abuse cases.
- Revisit when adding endpoints or raising limits.
- Retire obsolete cases when features die.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Depth | Control-ready descriptions | Crime howto manuals |
| Coverage | Authz + business logic | Only OWASP Top 10 bingo |
| Tests | Automated negatives | “We’ll monitor” only |
| Defaults | Deny / limit | Open relay for growth hacks |
| Ownership | Named control owner | Nobody owns fraud edges |

## Output Checklist

- [ ] Assets and trust boundaries listed
- [ ] Abuse case catalog prioritized
- [ ] Controls mapped to components
- [ ] Detection signals defined
- [ ] Negative/abuse tests implemented for P0
- [ ] Rate limits/size limits on expensive paths
- [ ] Authz deny-by-default verified
- [ ] Residual risks accepted with owners
- [ ] RFC/security review section updated
- [ ] `code-quality-standards` applied to mitigations

## Rules

- Authorized defensive design only — no operational crime guidance.
- Prefer prevent + detect over “trust the client.”
- Business logic abuse is as important as injection classes.
- Automate regression tests for abuse cases you claim closed.
- Hand deep framework auth to ABAC/middleware skills for implementation detail.
