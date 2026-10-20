---
name: golang-ab-testing
description: >
  Implement A/B (experiment) testing in Go services: assignment, bucketing,
  consistent hashing, exposure logging, feature-flag interplay, metrics, and
  statistical caution. Use for owned products running experiments — not to
  manipulate users unethically or hide security controls behind flags forever.
---

# Golang A/B Testing

## Scope And Authorization

- **In scope:** Product experimentation on applications you operate, with privacy review
  for user assignment logging.
- **Out of scope:** Dark patterns; running experiments on third-party sites; using A/B
  to silently disable security for a cohort without governance.
- Log exposures carefully (PII minimization); respect consent/opt-out.
- Pair with `feature-flag-patterns`, `observability-metrics-tracing`, `code-quality-standards`.

## When To Use

- Shipping two UX/algorithm variants with measured metrics.
- Gradual cohort rollout beyond boolean flags.
- Ensuring sticky assignment per user/device.
- Designing exposure events for experiment analysis.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Simple on/off flags | `feature-flag-patterns` |
| Metrics backend | `observability-metrics-tracing` |
| AuthZ policy design | `golang-abac-design` |
| Go style | `go-style-conventions` |
| Implementation quality | `code-quality-standards` |

## Concepts

| Term | Meaning |
| --- | --- |
| Experiment | Named test with variants A/B/(n) |
| Assignment | Mapping subject → variant |
| Sticky | Same subject keeps variant |
| Exposure | Event that subject saw variant |
| Guardrail metrics | Error rate, latency must not tank |
| Sample ratio mismatch | Assignment % ≠ expected (bug) |
| Feature flag | Delivery mechanism; experiment is measurement layer |

## Workflow

### 1. Define experiment

| Field | Example |
| --- | --- |
| Key | `checkout_button_color_2026q3` |
| Variants | `control`, `treatment` |
| Split | 50/50 |
| Subject | `user_id` (logged-in) or `anon_id` |
| Primary metric | purchase_rate |
| Guardrails | p99 latency, 5xx rate |
| Duration | start/end |

Privacy: can you log subject ids? Prefer pseudonymous keys.

### 2. Deterministic bucketing in Go

```go
import (
    "hash/fnv"
)

func bucket(experiment, subject string, mod uint32) uint32 {
    h := fnv.New32a()
    _, _ = h.Write([]byte(experiment))
    _, _ = h.Write([]byte{0})
    _, _ = h.Write([]byte(subject))
    return h.Sum32() % mod
}

func Assign(experiment, subject string) string {
    // 0-49 control, 50-99 treatment
    if bucket(experiment, subject, 100) < 50 {
        return "control"
    }
    return "treatment"
}
```

Prefer a shared library (or vendor SDK) for multi-language consistency. Include
experiment salt so rebalances are intentional.

### 3. Assignment service interface

```go
type Assigner interface {
    Variant(ctx context.Context, exp, subject string) (string, error)
}

// Implementation may call remote config (LaunchDarkly, GrowthBook, in-house)
```

Fallback: safe default `control` on assigner failure (document fail-open vs closed).

### 4. Apply in handler

```go
func (h *Handler) Checkout(w http.ResponseWriter, r *http.Request) {
    subj := subjectFrom(r)
    v, err := h.assigner.Variant(r.Context(), "checkout_button_color_2026q3", subj)
    if err != nil {
        v = "control"
    }
    h.exposure.Log(r.Context(), Exposure{
        Experiment: "checkout_button_color_2026q3",
        Variant:    v,
        Subject:    subj, // or hashed
    })
    // render variant
}
```

### 5. Exposure logging

```go
// Emit once per subject per experiment period (dedupe) to avoid bias
type Exposure struct {
    Experiment string
    Variant    string
    Subject    string
    TS         time.Time
}
```

Ship to analytics warehouse; **do not** log every scroll as exposure unless defined.

### 6. Metrics

| Metric type | Examples |
| --- | --- |
| Primary | conversion |
| Secondary | AOV, clicks |
| Guardrail | latency, errors, refunds |
| Health | assignment counts per variant |

Instrument in Go with OTel metrics or your statsd wrapper.

### 7. Stats caution (engineering)

- Don’t stop early without plan (peeking).
- Check sample ratio mismatch (50/50 should be ~equal assignments).
- Segment analysis pre-registered.
- Coordinate with data science for significance — engineers supply clean exposure data.

### 8. Cleanup

- After decision, remove losing branch or convert to permanent flag default.
- Delete dead code paths; experiments are not eternal feature flags.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Assignment | Sticky deterministic | rand every request |
| Failure | Documented default | 500 if flag service down for UX test |
| Exposure | Once per subject | Log every asset → inflated metrics |
| Security | Never A/B away auth | Skip CSRF for “treatment” |
| Cleanup | Remove code after | Nested experiments forever |

## Output Checklist

- [ ] Experiment design doc (metrics, split, subjects)
- [ ] Deterministic sticky assignment
- [ ] Safe fallback on assigner errors
- [ ] Exposure events deduped and privacy-reviewed
- [ ] Primary + guardrail metrics wired
- [ ] Sample ratio monitoring
- [ ] End date and cleanup owner
- [ ] `code-quality-standards` applied

## Rules

- Privacy and ethics on user experimentation.
- Sticky assignment; measure exposures correctly.
- Do not experiment away security controls.
- Clean up after launch decision.
- Flags skill for delivery; this skill for experiment discipline in Go.
