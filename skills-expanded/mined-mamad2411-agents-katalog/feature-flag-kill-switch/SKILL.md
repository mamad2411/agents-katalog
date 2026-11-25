---
name: feature-flag-kill-switch
description: >
  Design kill-switch feature flags for owned releases: default-safe off paths,
  independent of deploy, fast global disable, no dangerous side effects, and
  test coverage for off mode. Use when building release kill switches, circuit
  breakers via flags, or ensuring a feature can be disabled in seconds.
---

# Feature Flag Kill Switch

## Scope And Authorization

- **In scope:** Features and flag platforms for systems you own.
- **Out of scope:** Using flags to disrupt systems outside your control.
- A kill switch must leave the system in a **supported** degraded mode—not a hard crash.
- Control who can flip production kill switches (RBAC on flag tool).
- Pair with `feature-flag-incident-disable` for runtime use and `feature-flag-patterns` for lifecycle.

## When To Use

- Shipping risky features (new checkout path, new recommender, new protocol).
- Need mitigation faster than CI/CD rollback.
- Regulatory or safety features requiring instant disable.
- Multi-service features needing coordinated off switch.
- Reviewing whether an existing flag is a true kill switch or only a cosmetic toggle.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Incident execution steps | `feature-flag-incident-disable` |
| Flag taxonomy, cleanup, targeting | `feature-flag-patterns` |
| Envoy outlier ejection | `envoy-outlier-detection` |
| Error budget freezes | `error-budget-policy-design` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Default | Safe without flag service? Prefer fail to old path |
| Independence | Off path doesn’t need new code deploy |
| Speed | Global off propagates within agreed SLO (e.g. <1–2 min) |
| Side effects | Off doesn’t corrupt data mid-write |
| Testing | CI tests both on and off |
| Naming | `killswitch_*` or `ks_*` prefix for discoverability |

## Workflow

### 1. Confirm scope and success criteria

1. Feature risk, supported degraded behavior, max disable time.
2. Success: documented off path; game-day disable works; tests cover off.

### 2. Design the off path

| Question | Kill-switch quality |
| --- | --- |
| What happens when off? | Old code path / no-op / queue drop with user message |
| In-flight requests? | Finish or abort safely |
| Writes? | No half-applied dual writes |
| Dependencies? | Off doesn’t call broken new service |

### 3. Implement flag evaluation

```python
# Conceptual — evaluation local with short TTL cache
if flags.is_enabled("killswitch_new_checkout", context):
    return new_checkout(req)
return legacy_checkout(req)
```

1. Evaluate at request boundary for quick effect (not only at process boot).
2. Cache TTL short enough for kill SLO; document staleness.
3. If flag SDK down: choose **fail safe** (usually legacy/off for new risk).

### 4. Platform controls

1. Separate permission: “kill switch operators” vs marketing percentage flags.
2. Audit log every change.
3. Protect from accidental percentage ramps on kill switches (boolean only).
4. Multi-region projects updated atomically or with clear order.

### 5. Test and game day

```bash
pytest -q tests/test_killswitch_new_checkout.py
# Stage game day: enable → load → disable → verify legacy metrics
```

1. Automated tests: off path unit/integration.
2. Game day quarterly for critical switches.
3. Measure propagation delay to 99% of instances.

### 6. Wire observability

1. Metric `flag_killswitch_new_checkout` evaluated true/false rates.
2. Alert when critical kill switch is on longer than expected after incident.
3. Dashboard link from runbook.

### 7. Hand off

1. Runbook section in service manual: when/how to disable.
2. Owner + backup for the flag.
3. Removal plan after feature is stable (don’t keep forever without review).

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Off path | Battle-tested legacy | Off throws 500 |
| Eval | Per request | Boot-only config |
| Fail SDK | Default legacy | Default new risky path |
| Permissions | Restricted toggle | Everyone admin in LD |
| Naming | `killswitch_payments_v2` | `flag_42` |

## Output Checklist

- [ ] Degraded/off behavior defined and supported
- [ ] Per-request evaluation with known cache TTL
- [ ] Fail-safe on SDK outage documented
- [ ] RBAC + audit on flag tool
- [ ] On/off tests in CI
- [ ] Game-day evidence for critical switches
- [ ] Runbook linked
- [ ] Residual risk noted

## Rules

- Kill switch must be safe, fast, and authorized.
- Prefer boolean global switches for emergencies.
- Don’t dual-write without off-path integrity design.
- Incident flipping → `feature-flag-incident-disable`.
- General flag hygiene → `feature-flag-patterns`.
