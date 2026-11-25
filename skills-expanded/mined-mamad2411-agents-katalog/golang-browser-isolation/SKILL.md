---
name: golang-browser-isolation
description: >
  Integrate browser isolation / remote browser patterns with Go backends: URL
  rewriting, session brokers, policy (allow/deny destinations), token handoff,
  and security telemetry. Owned/authorized enterprise isolation—not malware hosting.
---

# Golang Browser Isolation

## Research grounding

Runbook for **remote browser isolation (RBI)** control planes and **Go** services
that broker sessions, enforce URL policy, and emit isolation telemetry.
Skill id: `golang-browser-isolation`.

## Scope And Authorization

- **In scope:** owned isolation platforms, enterprise labs, authorized vendor integrations.
- **Out of scope:** using isolation to hide attacks, bypassing user consent/monitoring laws, unauthorized interception.
- Prefer stage policy dry-runs; production policy changes under change control.
- Redact full URLs with secrets/tokens from logs.
- Pair with `code-quality-standards` and web security headers skills as needed.

## When To Use

- Go gateway decides when to **render untrusted links in isolated browser** vs native.
- Building session broker APIs (create isolation session, stream, tear down).
- Policy: categories, DLP download block, clipboard controls.
- Measuring isolation coverage for high-risk browsing (email links, support tools).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Content safety / moderation models | `golang-content-safety` |
| CDN edge config only | `golang-cdn-config` |
| CASB SaaS control | `golang-casb-notes` |
| Classic XSS fixes in app | `xss-cross-site-scripting` |
| Code quality | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Broker API | Go service: authn user → policy check → vendor/session create → return short-lived embed token |
| Policy | Allow/deny domains, file download, print, clipboard, max session TTL |
| Threat model | Malicious page contained in remote browser; host endpoints stay clean |
| Telemetry | Session start/end, policy deny, download blocked, error rates |
| Pitfalls | Token leakage in Referer, immortal sessions, isolating trusted admin SSO badly |

### Decision table

| Context | Action |
| --- | --- |
| User clicks link from untrusted email | Force isolation |
| Admin console same-site | Native browser |
| Unknown URL category | Isolate + warn |
| Policy deny list | Block without session |
| Download of exe/macro | Block in isolation profile |

## Workflow

### 1. Confirm scope and success criteria

1. User populations, browsers, vendors (or self-hosted), compliance needs.
2. Success: policy denies work; sessions expire; host AV has zero drive-by from isolated path in drill.
3. Privacy: what session content is recorded?

### 2. Inventory

1. Entry points: secure email gateway, web proxy, chat unfurl, Go BFF.
2. IdP groups for isolation-required users.
3. Existing PAC/proxy rules conflicting with RBI.

### 3. Baseline

1. Coverage % of risky clicks isolated; FP tickets (broken sites).
2. Token/session TTLs currently configured.

### 4. Implement Go broker patterns

```go
type IsolateRequest struct {
    UserID string
    URL    string
}

func (s *Broker) Start(ctx context.Context, req IsolateRequest) (sessionURL string, err error) {
    u, err := url.Parse(req.URL)
    if err != nil || !s.policy.Allowed(u) {
        return "", errPolicy
    }
    sess, err := s.vendor.Create(ctx, VendorOpts{
        User: req.UserID,
        URL:  u.String(),
        TTL:  30 * time.Minute,
        Profile: s.policy.Profile(u), // clipboard/download flags
    })
    if err != nil {
        return "", err
    }
    s.metrics.Sessions.Inc()
    s.audit.Log(ctx, "isolate_start", req.UserID, u.Host) // host only if policy
    return sess.ConnectURL, nil
}
```

1. Bind session tokens to user + device; short TTL; HTTPS only.
2. Strip sensitive query params before audit if not required.
3. Health checks against vendor API with timeouts/circuit breakers.

### 5. Verify with evidence

```text
go test ./internal/isolate/... -race
go test ./internal/isolate -run TestPolicyDeny

# Stage: create session, confirm expiry, confirm deny list
curl -sS -X POST https://broker.stage/v1/sessions \
  -H "Authorization: Bearer $USER_TOKEN" \
  -d '{"url":"https://example.invalid/malware-test"}'
```

1. Confirm download of blocked MIME fails inside profile.
2. Confirm token reuse after logout fails.

### 6. Observe and harden

1. Alerts: vendor error rate, session spawn spike, policy deny spike.
2. FP process: temporary allow domain with owner+expiry.
3. Review CSP/embed requirements if isolation UI is iframed.

### 7. Hand off

1. Support runbook for “site broken under isolation.”
2. Link content-safety and CASB notes as needed.
3. Apply `code-quality-standards`.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Tokens | User-bound, short TTL | Long-lived shareable session URLs |
| Logs | Host + reason codes | Full URL with OAuth codes |
| Policy | Risk-based force isolate | Isolate everything including IdP |
| Failures | Fail closed for high-risk entry | Silent native fallback for email links |
| Reviews | FP with expiry | Permanent global allow |

## Output Checklist

- [ ] Populations, entry points, vendor/auth recorded
- [ ] Policy matrix for isolate/block/native
- [ ] Go broker with TTL and policy checks
- [ ] Stage tests: deny, expire, download block
- [ ] Audit without secret leakage
- [ ] Metrics/alerts for vendor and denials
- [ ] FP process documented
- [ ] Exceptions with owner + expiry
- [ ] `code-quality-standards` applied
- [ ] Residual risk noted

## Rules

- Authorized enterprise isolation only.
- Do not use isolation as cover for offensive operations against third parties.
- Prefer least recording consistent with policy.
- Focus on broker/policy in Go; deep malware analysis is out of scope.
- Never paste live session URLs with auth tokens into tickets.
