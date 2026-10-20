---
name: golang-bot-managed
description: >
  Design and operate managed bot-control planes in Go: allow/deny lists, managed
  bot registries (search, monitoring, partners), mTLS/API-key identity for known
  good bots, rate tiers, and step-up when confidence is low. Authorized/owned only.
---

# Golang Bot Managed

## Research grounding

Runbook for **managed bot control** implemented in **Go** edge/API services:
distinguishing known-good automated clients from abusive automation, with
allowlists, signed bot identity, and operational SLAs. Skill id: `golang-bot-managed`.

## Scope And Authorization

- **In scope:** owned APIs, labs, authorized bot-management features you operate.
- **Out of scope:** evading third-party bot defenses, credential stuffing, CAPTCHA fraud.
- Validate in stage with synthetic bots before production threshold changes.
- Redact bot secrets, partner keys, and end-user identifiers from tickets.
- Pair code with `code-quality-standards`; accessibility when step-up challenges fire.

## When To Use

- You run a Go gateway that must **preferentially allow** search crawlers, uptime monitors, payment webhooks, and partner bots.
- Building a **managed bot registry** (token, mTLS, verified User-Agent + reverse DNS) with rate tiers.
- Separating “known good automation” from anonymous high-risk traffic.
- On-call needs clear allowlist change process and kill switches.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Raw signal scoring / ML features | `golang-bot-signals` |
| CAPTCHA / challenge research | `captcha-bypass-research` (authorized) |
| Rate-limit design only | `rate-limit-bypass-testing` / rate-limit skills |
| Abuse / ATO chaining methodology | `account-takeover-methodology` |
| Implementation quality | `code-quality-standards` |
| General WAF policy | CDN/WAF catalog skills |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Identity | API keys in headers, mTLS client certs, JWT service tokens, IP+rDNS for crawlers |
| Registry | Config or DB: bot_id, owner, rate_tier, scopes, expiry, contact |
| Decisions | allow_managed → rate_tier_A; unknown → score path (`golang-bot-signals`); deny → 403/429 |
| Ops | Change ticket for allowlist, dual-control for production keys, expiry automation |
| Pitfalls | UA-only allowlists, immortal partner keys, blocking a11y tools, no audit of who added bots |

### Managed bot decision table

| Client class | Identity proof | Default action | Rate |
| --- | --- | --- | --- |
| Search crawler | rDNS + documented ranges | Allow GET only | Tier crawl |
| Uptime probe | Shared secret / mTLS | Allow health paths | Tier probe |
| Partner API | Scoped API key / JWT | Allow scoped routes | Contract RPS |
| Unknown | None | Defer to signals | Strict |
| Abusive | Prior block | Deny + log | Zero |

## Workflow

### 1. Confirm scope and success criteria

1. List protected routes, bot classes required for business, false-positive budget.
2. Success: known bots pass SLAs; unknown abuse reduced; every allowlist entry has owner+expiry.
3. Define break-glass to bypass bot control for incident response (audited).

### 2. Inventory current control

1. Existing middleware, CDN bot scores, partner keys in secrets manager.
2. Logs: can you distinguish managed vs unknown today?
3. Shadow mode metrics if flipping from open to managed.

### 3. Baseline

1. Capture 7d traffic mix: managed share, 429/403 rates, partner error budgets.
2. Hash current allowlist config; note keys without rotation.
3. Record a11y and official crawler requirements.

### 4. Implement managed control plane (Go)

```go
type ManagedBot struct {
    ID        string
    Owner     string
    Tier      string   // crawl|probe|partner
    Scopes    []string // path prefixes or methods
    ExpiresAt time.Time
}

func (m *Manager) Classify(r *http.Request) Decision {
    if b, ok := m.byClientCert(r.TLS); ok && time.Now().Before(b.ExpiresAt) {
        return Decision{Class: "managed", Bot: b, Action: Allow}
    }
    if b, ok := m.byAPIKey(r.Header.Get("X-Bot-Key")); ok {
        return Decision{Class: "managed", Bot: b, Action: Allow}
    }
    // Fall through to signal scorer — do not UA-string alone for security decisions.
    return Decision{Class: "unknown", Action: Score}
}
```

1. Store keys in Vault/KMS; never commit.
2. Enforce scope checks (path/method) after identity.
3. Emit metrics: `bot_managed_requests_total{bot_id,tier,action}` (bot_id cardinality bounded).

### 5. Verify with evidence

```text
go test ./internal/botmgr/... -count=1
go test ./internal/botmgr/... -race

# Synthetic managed client
curl -sS -o /dev/null -w '%{http_code}\n' \
  -H "X-Bot-Key: $STAGE_BOT_KEY" https://api.stage.example/v1/health

# Unknown client should not get partner tier
curl -sS -o /dev/null -w '%{http_code}\n' https://api.stage.example/v1/health

# Config expiry audit
go run ./cmd/bot-registry-audit -fail-on-expired -fail-on-no-owner
```

1. Prove partner still within RPS; prove revoked key → 401/403.
2. Confirm crawler allow path does not open write endpoints.

### 6. Observe and harden

1. Alerts: spike in managed 401s (key rotation mishap), sudden new bot_id, registry audit failures.
2. Fail mode: if registry unavailable, document fail-open (public) vs fail-closed (sensitive APIs).
3. Quarterly key rotation + rDNS revalidation for crawlers.

### 7. Hand off

1. Runbook: add/remove bot, rotate key, emergency deny.
2. Cross-link `golang-bot-signals`, rate-limit, captcha skills.
3. Apply `code-quality-standards`.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Allowlist | Key/mTLS + scopes + expiry | `User-Agent: Googlebot` only |
| Keys | Vault, rotated, dual-control | Long-lived key in repo |
| Metrics | Bounded bot_id set | Label per client IP |
| Failures | Documented fail mode | Silent open when Redis down |
| a11y | Challenges don’t trap AT users | CAPTCHA wall for all unknowns |

## Output Checklist

- [ ] Scope, routes, bot classes, authorization recorded
- [ ] Registry schema with owner + expiry
- [ ] Go classifier with scoped allow and signal fallback
- [ ] Stage proof: managed OK, revoked denied, unknown scored
- [ ] Metrics + alerts for auth failures and audit
- [ ] Fail-open/closed decision documented
- [ ] a11y / legitimate crawler impact reviewed
- [ ] Exceptions ticketed with expiry
- [ ] `code-quality-standards` applied
- [ ] Residual risk noted

## Rules

- Authorized bot management only; do not help evade others’ defenses.
- Prefer cryptographic or secret identity over forgeable headers alone.
- Every production allowlist entry needs owner and expiry.
- Focus on `golang-bot-managed`; deep scoring → `golang-bot-signals`.
- Never paste live bot API keys into chat or commits.
