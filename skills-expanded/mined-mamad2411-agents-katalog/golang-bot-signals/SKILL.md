---
name: golang-bot-signals
description: >
  Implement bot-risk signal collection and scoring in Go: request heuristics,
  device/TLS fingerprints (where lawful), velocity, reputation fusion, thresholds,
  shadow mode, and false-positive handling. Use only on owned/authorized systems.
---

# Golang Bot Signals

## Research grounding

Runbook for **bot signal scoring** in **Go** services—feature extraction, score
fusion, calibration, and step-up triggers—distinct from managed allowlists.
Skill id: `golang-bot-signals`.

## Scope And Authorization

- **In scope:** owned apps, labs, authorized anti-abuse features with privacy review.
- **Out of scope:** building tools to bypass third-party bot defense, harvesting fingerprints for stalking, unauthorized tracking.
- Prefer privacy-preserving aggregates; document lawful basis for device signals.
- Redact raw fingerprints and PII from logs/tickets.
- Pair with `code-quality-standards` and accessibility requirements for challenges.

## When To Use

- Scoring **unknown** traffic after managed bots are identified (`golang-bot-managed`).
- Implementing multi-signal fusion (IP reputation, velocity, header consistency, JS/challenge results).
- Calibrating thresholds, shadow mode, and FP/FN review queues.
- Emitting score distributions for security board packs.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Known-good bot registry / partner keys | `golang-bot-managed` |
| CAPTCHA vendor ops / authorized research | `captcha-bypass-research` |
| Pure rate limits | rate-limit skills |
| Full ATO methodology | `account-takeover-methodology` |
| Code quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Signals | IP/ASN reputation, path velocity, header entropy, TLS JA3/JA4 (if policy allows), cookie integrity, challenge outcome |
| Scoring | Weighted sum or rules engine; clamp; never single brittle signal for hard deny |
| Actions | allow / soft challenge / hard challenge / deny / tarpit |
| Calibration | Shadow mode ≥ 1 week; measure FP on real users & partners |
| Pitfalls | Blocking datacenter ASN wholesale, UA banlists, no FP appeal path, high-cardinality logs |

### Signal → weight sketch

| Signal | Example weight | Notes |
| --- | --- | --- |
| Known bad IP list hit | +0.5 | Short TTL; false positive risk |
| Extreme velocity same IP+route | +0.3 | Sliding window in Redis |
| Missing expected browser headers on HTML routes | +0.2 | Don’t apply to pure API |
| Failed interactive challenge | +0.4 | After challenge presented |
| Managed bot identity | −1.0 | Short-circuit allow |
| Passed recent challenge | −0.3 | Trust window |

## Workflow

### 1. Confirm scope and success criteria

1. Legal/privacy sign-off for fingerprints; list routes in scope.
2. Success metrics: abuse reduction, FP rate < target, p99 latency budget for scorer.
3. Define max action without human review (e.g. soft challenge only).

### 2. Inventory signals available

1. Edge logs, CDN bot score, app middleware, challenge provider callbacks.
2. Gaps: no shared velocity store, no IP intel feed, no shadow pipeline.
3. Map each signal to retention and PII class.

### 3. Baseline

1. Record current block/challenge rates and support FP tickets.
2. Sample labeled good (login success, checkout) vs known abuse (if available).
3. Fix seed thresholds from shadow recommendations, not gut feel alone.

### 4. Implement scorer in Go

```go
type Features struct {
    IPRep       float64
    Velocity    float64
    HeaderScore float64
    Challenge   float64
    ManagedBot  bool
}

func Score(f Features) (float64, string) {
    if f.ManagedBot {
        return 0, "allow_managed"
    }
    s := 0.5*f.IPRep + 0.3*f.Velocity + 0.2*f.HeaderScore + 0.4*f.Challenge
    switch {
    case s >= 0.85:
        return s, "deny"
    case s >= 0.55:
        return s, "challenge"
    default:
        return s, "allow"
    }
}
```

1. Use context timeouts on Redis/IP intel; document fail-open/closed per route sensitivity.
2. Metrics: `bot_score_bucket`, `bot_action_total{action}`, latency histogram.
3. Log **reason codes**, not full fingerprints.

### 5. Verify with evidence

```text
go test ./internal/botsignal/... -count=1
go test ./internal/botsignal/... -race

# Shadow mode: compute score, never enforce
# Compare would-block vs actual user success rate

# Load fixture vectors
go test ./internal/botsignal -run TestScoreFixtures -v
```

1. Unit tests for managed short-circuit, velocity spikes, missing intel.
2. Stage A/B: 5% enforce challenge; watch conversion and support volume.
3. Confirm a11y path: alternative challenge or allowlist for assistive tech policy.

### 6. Observe and harden

1. Alert on score distribution shift, intel feed stale, Redis errors.
2. Weekly FP review sample; adjust weights with ticketed change.
3. Expire temporary denylists; re-test after CDN or client changes.

### 7. Hand off

1. Document action matrix and appeal process.
2. Link `golang-bot-managed`, captcha, rate-limit skills.
3. Apply `code-quality-standards`.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Fusion | Multi-signal + shadow calibration | Single UA blocklist |
| Privacy | Hashed/ truncated features, short retention | Raw device graphs forever |
| Actions | Graduated challenge | Instant permanent ban on first hint |
| Failures | Explicit fail mode per route | Silent open on intel timeout for banking |
| Logs | Reason codes | Full JA3 + cookie dump |

## Output Checklist

- [ ] Privacy/authorization for signals recorded
- [ ] Feature list with weights and retention
- [ ] Go scorer + tests including managed short-circuit
- [ ] Shadow mode results before hard enforce
- [ ] FP process and a11y impact documented
- [ ] Metrics/alerts for distribution and feed health
- [ ] Fail-open/closed matrix by route class
- [ ] Exceptions with owner + expiry
- [ ] `code-quality-standards` applied
- [ ] Residual risk noted

## Rules

- Authorized anti-abuse only; no evasion tooling for third parties.
- Prefer multi-signal decisions; document every hard-deny rule.
- Do not log secrets or raw PII fingerprints.
- Focus on `golang-bot-signals`; managed identity → `golang-bot-managed`.
- Evidence (fixtures, shadow stats) over intuition.
