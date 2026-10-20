---
name: golang-bff-pattern
description: >
  Design secure Backend-for-Frontend (BFF) layers in Go: aggregation, auth
  cookies, CSRF, least data exposure, and tenancy. Use for owned web/mobile
  frontends under authorization.
---

# Golang BFF Pattern

## Research grounding

Runbook for **Backend-for-Frontend** services in Go—tailored APIs for a specific
UI that aggregate downstream microservices securely. Skill id:
`golang-bff-pattern`.

## Scope And Authorization

- **In scope:** BFFs and frontends you own.
- **Out of scope:** building BFFs to exfiltrate third-party APIs without rights.
- Treat BFF as high-trust (session bearer); harden accordingly.
- Pair with `golang-api-gateway-auth`, `golang-access-control`, `code-quality-standards`.

## When To Use

- Web/mobile needs aggregation shapes not fit for public general APIs.
- Moving tokens from browser localStorage to httpOnly cookies via BFF.
- Per-channel (web vs iOS) API differences.
- Focus tokens: **golang, bff, pattern**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Generic API surface | `golang-api-surface` |
| Gateway plugin auth | `golang-api-gateway-auth` |
| GraphQL-specific | dedicated GraphQL security skill if present |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concern | Guidance |
| --- | --- |
| Audience | One BFF per frontend channel ideally |
| Auth | Server-side session/cookie; confidential OIDC client |
| CSRF | Required for cookie sessions on browser BFFs |
| Aggregation | Parallel downstream calls with `errgroup` + timeouts |
| Data minimization | Return UI-needed fields only |
| AuthZ | Enforce per user; never trust client-provided user id |
| Caching | Careful personalized cache keys |
| Pitfalls | BFF becomes second monolith; token leakage to JS |

## Workflow

### 1. Confirm scope and success criteria

1. Frontend channel, downstreams, authorization.
2. Success: no access tokens in JS; CSRF protected; aggregation latency SLO.
3. Threat model: XSS impact, CSRF, SSRF via open downstream URLs.

### 2. Inventory

1. Existing public API over-fetch/under-fetch pain.
2. Auth flows (SPA vs server-rendered).
3. Downstream auth (mTLS, JWT exchange).

### 3. Baseline

1. Measure chatty client call counts.
2. Token storage location today (localStorage?).

### 4. Implement Go BFF

```go
func (b *BFF) Dashboard(w http.ResponseWriter, r *http.Request) {
	ctx := r.Context()
	sess, err := b.sessions.Get(r)
	if err != nil {
		http.Error(w, "unauthenticated", http.StatusUnauthorized)
		return
	}
	g, ctx := errgroup.WithContext(ctx)
	var profile, orders any
	g.Go(func() error {
		var e error
		profile, e = b.users.Get(ctx, sess.UserID)
		return e
	})
	g.Go(func() error {
		var e error
		orders, e = b.orders.List(ctx, sess.UserID)
		return e
	})
	if err := g.Wait(); err != nil {
		http.Error(w, "upstream", http.StatusBadGateway)
		return
	}
	writeJSON(w, map[string]any{"profile": profile, "orders": orders})
}
```

1. Cookies: `HttpOnly; Secure; SameSite=Lax|Strict`; rotate session IDs on login.
2. CSRF token for state-changing routes.
3. Downstream: attach service credentials + user assertion (token exchange); short timeouts.
4. Do not expose arbitrary proxy (`/proxy?url=`)—SSRF risk.
5. Rate limit per session (`golang-abuse-prevention`).

### 5. Verify with evidence

```bash
go test ./internal/bff/... -count=1
go test ./... -race -count=1
```

1. CSRF missing → 403.
2. Session of user A cannot fetch user B aggregates.
3. Browser storage has no access_token.
4. Latency under parallel fan-out within SLO.

### 6. Observe and harden

1. Metrics per BFF route; upstream error breakdown.
2. Alert on upstream p99 and auth failures.
3. Pentest XSS impact (session cookie theft) → CSP on frontend.

### 7. Hand off

1. Contract between frontend and BFF versioned.
2. Runbook for session store outage.
3. Apply `code-quality-standards`.

## BFF vs public API

| | BFF | Public API |
| --- | --- | --- |
| Client | First-party UI | Many integrators |
| Shape | UI-specific | Stable general |
| Auth | Session cookie common | Tokens/API keys |
| Stability | Faster iterate | Strict versioning |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Tokens | httpOnly session | Access token in localStorage |
| Proxy | Fixed downstreams | Open URL proxy |
| AuthZ | Server-side user from session | Trust body `userId` |
| Topic fidelity | Go BFF security pattern | Generic go test only |

## Output Checklist

- [ ] Channel and threat model defined
- [ ] Session/CSRF design implemented
- [ ] Aggregation with timeouts/errgroup
- [ ] Object authZ tests pass
- [ ] No open proxy
- [ ] Metrics/alerts
- [ ] `code-quality-standards` applied

## Rules

- BFF is trusted; minimize XSS blast radius.
- Focus on `golang-bff-pattern`.
- Authorized apps only.
- Never log session tokens.
