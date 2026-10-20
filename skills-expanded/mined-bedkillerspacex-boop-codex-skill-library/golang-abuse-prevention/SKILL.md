---
name: golang-abuse-prevention
description: >
  Design and implement abuse-prevention controls in Go services: rate limits,
  account/device throttles, progressive friction, and anti-automation signals.
  Use for owned APIs, signup/login, and high-cost endpoints under authorization.
---

# Golang Abuse Prevention

## Research grounding

Operational runbook for **abuse prevention in Go** services: limiting automated
and human abuse (credential stuffing, scrape floods, invite spam, expensive
API abuse) without blocking legitimate traffic. Skill id: `golang-abuse-prevention`.

## Scope And Authorization

- **In scope:** systems you own, labs/CTFs, or engagements with written authorization.
- **Out of scope:** building tooling to evade third-party abuse controls, fraud
  against external services, or unauthorized load generation.
- Prefer non-production validation; use change windows for production rate-limit
  and challenge rollouts.
- Redact secrets, tokens, personal data, device IDs, and customer identifiers
  from notes and tickets.
- Pair code/config changes with `code-quality-standards`.

## When To Use

- Adding or tuning rate limits, quotas, CAPTCHA/challenge gates, or bot signals
  on Go HTTP/gRPC handlers.
- Signup, login, password-reset, OTP, invite, upload, search, or payment
  endpoints show abuse or cost spikes.
- You need Go-specific patterns: middleware, `golang.org/x/time/rate`, Redis
  token buckets, context deadlines, structured deny responses.
- Focus tokens: **golang, abuse, prevention**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Pure token-bucket math / store design | `rate-limit-token-bucket-design` or `rate-limit-bypass-testing` (authorized) |
| CAPTCHA/bot challenge research only | `captcha-bypass-research` (authorized control research) |
| API auth / JWT validation | `api-auth-and-jwt-abuse` or `golang-api-gateway-auth` |
| AuthZ matrix / RBAC | `golang-access-control` |
| Alert noise reduction | `golang-alert-fatigue` / `golang-alerting` |
| Implementation quality baseline | `code-quality-standards` |
| Secrets rotation program | `secrets-management-hygiene` |

## Domain Focus (Go abuse controls)

| Area | Guidance |
| --- | --- |
| Limit keys | IP (/32 or /64 carefully), user ID, API key, device fingerprint, route+method |
| Algorithms | Token bucket, sliding window, fixed window+jitter, leaky bucket for queues |
| Go libs | `golang.org/x/time/rate`, Redis (INCR+PTTL or Lua), `ulule/limiter`, custom middleware |
| Response | 429 + `Retry-After`; stable error body; no oracle that reveals valid users |
| Progressive friction | Soft delay → CAPTCHA/WebAuthn step-up → hard block with ticket path |
| Costly ops | Separate budgets for SMS, email, AI inference, export, bulk search |
| Signals | Velocity, ASN/geo mismatch, UA entropy, TLS JA3 (edge), failed-auth ratio |
| Fail mode | Prefer fail-closed for auth and money paths; document fail-open with alerts |
| Pitfalls | Global mutex bottlenecks, NAT false positives, missing key expiry, logging PII |

## Workflow

### 1. Confirm scope and success criteria

1. Record owner, service, environment, authorization, and blast radius (which
   clients or regions can be throttled).
2. Define measurable success: e.g. max N req/s per user on `/login`, SMS
   spend under budget, false-positive rate under X% on golden traffic.
3. Identify break-glass (allowlist for health checks, partner IPs, load tests)
   with owner + expiry.

### 2. Inventory abuse surface

1. Map public and authenticated routes; mark high-cost and unauthenticated.
2. List existing limits (edge WAF, API gateway, app middleware, DB connection caps).
3. Collect abuse signals: 4xx/5xx rates, SMS/email volume, unique IPs per account.
4. Note multi-tenant isolation: tenant A load must not starve tenant B if shared limits.

### 3. Baseline

1. Capture RPS, p95 latency, 429 counts, and cost metrics **before** changes.
2. Replay or load-test representative good traffic; record false-positive candidates.
3. Version configs (limit tables, Redis key prefixes) and note data sensitivity.

### 4. Implement Go controls

1. Put limits **closest to the expensive work** but after cheap auth where the
   key is the user/API key (avoids pure-IP limits starving NAT users when identity is known).
2. Use context-aware handlers; never block the process with unbounded work.

```go
// Example: per-key token bucket via x/time/rate (single instance; use Redis for multi-replica)
type LimiterStore struct {
	mu    sync.Mutex
	m     map[string]*rate.Limiter
	r     rate.Limit
	burst int
}

func (s *LimiterStore) Allow(key string) bool {
	s.mu.Lock()
	defer s.mu.Unlock()
	lim, ok := s.m[key]
	if !ok {
		lim = rate.NewLimiter(s.r, s.burst)
		s.m[key] = lim
	}
	return lim.Allow()
}
```

3. Multi-replica: prefer Redis Lua or atomic INCR with TTL; document clock skew.
4. Separate **abuse** limits from **fair-use quotas** (quota = product plan; abuse = safety).
5. Return consistent 429 JSON/gRPC `ResourceExhausted`; set `Retry-After` when known.
6. For signup/login: progressive delay + optional challenge; never leak “user exists”.
7. Keep secrets and HMAC keys for device tokens in KMS/Vault; rotate with dual-read.

### 5. Verify with evidence

```bash
# Unit/integration
go test ./internal/abuse/... -count=1
go test ./... -race -count=1

# Static / vuln
go vet ./...
staticcheck ./...
govulncheck ./...

# Local load against owned staging (authorized only)
# hey -n 1000 -c 50 -H "Authorization: Bearer $TOKEN" https://staging.example/api/v1/login
```

1. Prove: under limit → 200; over limit → 429 with Retry-After; allowlisted → 200.
2. Prove multi-key isolation (user A exhaustion does not block user B).
3. Chaos: Redis down → documented fail mode (closed or open) and alert fires.
4. Redact IPs/tokens from logs attached to tickets.

### 6. Observe and harden

1. Metrics: `abuse_limit_hits_total{route,key_type}`, `abuse_challenge_served_total`,
   false-positive samples, SMS/email spend.
2. Alert on sudden 429 spikes **and** on limit path errors (Redis failures).
3. Review NAT/corporate egress false positives; prefer user-key after auth.
4. Revisit limits after product launches; exceptions with owner + expiry only.

### 7. Hand off

1. Update runbooks: how to raise a limit, allowlist, and investigate blocks.
2. Apply `code-quality-standards` to middleware and store code.
3. Link related skills: rate-limit design, captcha research, API gateway auth.
4. Schedule post-deploy review of false positives within 7 days.

## Go patterns (topic-specific)

| Pattern | Prefer | Avoid |
| --- | --- | --- |
| Keying | user/API key after auth; IP as secondary | Only global process limit |
| Store | Redis with TTL + Lua; or edge gateway | In-memory only on N>1 replicas |
| Middleware | `http.Handler` chain; early return 429 | Doing limit after DB write |
| Concurrency | lock per key or sharded maps; -race tests | One giant mutex for all keys |
| gRPC | interceptor + `codes.ResourceExhausted` | Silent drop without status |
| Cost APIs | separate budget counter + kill switch | Same RPS as cheap GETs |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Authorization | Owned staging load tests | Hammering third-party login |
| Topic fidelity | Limits, friction, cost budgets in Go | Only generic `go test` checklist |
| Deny UX | 429 + Retry-After + support path | Infinite spinner / empty 500 |
| Identity | Post-auth user-scoped limits | Throttling whole /8 office IP forever |
| Fail mode | Documented + alerted | Silent open under Redis outage |
| Secrets | Short-lived challenge secrets | Hardcoded HMAC in repo |

## Output Checklist

- [ ] Scope, owner, environment, authorization recorded
- [ ] Abuse routes and cost centers inventoried
- [ ] Baseline RPS/cost/429 metrics captured
- [ ] Go middleware/store limits implemented with correct keying
- [ ] Progressive friction / challenge path documented if used
- [ ] Multi-replica store behavior verified
- [ ] Fail-open/closed mode documented and alerted
- [ ] Tests (`go test`, preferably `-race`) and load evidence attached (redacted)
- [ ] Metrics and runbook updated
- [ ] Exceptions have owner + expiry; residual risk noted
- [ ] `code-quality-standards` applied if code shipped

## Rules

- Authorized use only; evidence over guesses.
- Do not design evasion of third-party abuse systems.
- Prefer reversible limit changes and explicit owners.
- Do not weaken limits “temporarily” without ticket + expiry.
- Keep focus on `golang-abuse-prevention` (Go abuse controls); route pure
  rate-limit theory, CAPTCHA research, and JWT auth to neighbor skills.
- Never paste live secrets, tokens, or full device graphs into skill notes.
