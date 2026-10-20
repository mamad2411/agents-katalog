---
name: feature-flag-incident-disable
description: >
  Disable feature flags during incidents on owned systems: identify blast-radius
  flags, execute kill/disable with authority, verify traffic shift, and document
  timeline. Use when SEV response needs flag off, incident feature rollback, or
  flag-driven mitigation—complements feature-flag-kill-switch design and
  feature-flag-patterns.
---

# Feature Flag Incident Disable

## Scope And Authorization

- **In scope:** Flag systems and services your org operates during authorized incident response.
- **Out of scope:** Disabling features on customer tenants without authority; reckless global toggles without comms.
- Prefer flags designed as kill switches; not every flag is safe to flip under load.
- Record who authorized the change (IC/commander).
- Pair with `feature-flag-kill-switch` (design) and `feature-flag-patterns` (lifecycle).

## When To Use

- Active incident where a recent feature is implicated.
- Need faster mitigation than deploy rollback.
- Partial disable (percentage → 0%, segment off) before global off.
- Coordinating multi-service flags during SEV.
- Post-incident: ensure flags stay off until fix.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Designing kill-switch flags | `feature-flag-kill-switch` |
| General flag platform patterns | `feature-flag-patterns` |
| Error budget freezes | `error-budget-policy-design` |
| DB migration rollback | `database-migration-safety` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Authority | IC approves production flag changes |
| Scope | Prefer smallest segment that stops bleeding |
| Verify | Metrics + synthetic checks after flip |
| Comms | Status channel notes flag name + time |
| Sticky | Users may be bucketing sticky—plan for that |
| Follow-up | Code remove or keep off with ticket |

## Workflow

### 1. Confirm incident context

1. SEV level, commander, hypotheses linking a flag/feature.
2. Success: symptom relieved or ruled out; timeline logged.

### 2. Identify candidate flags

```bash
# Search recent deploys / flag names in code
rg -n "flag|FEATURE_|launchdarkly|openfeature" -i app | head
```

1. List flags changed in last deploy window.
2. Mark which are **safe kill switches** vs require data migration caution.

### 3. Pre-change checks

1. Default when flag service is down (fail open/closed)—know behavior.
2. Dependencies: does disable break critical path?
3. Snapshot current flag JSON/config for rollback of the toggle itself.

### 4. Execute disable

| Step | Action |
| --- | --- |
| 1 | Announce intent in incident channel |
| 2 | Set percentage to 0 or targeting to none |
| 3 | Global off if needed |
| 4 | Timestamp + actor in incident log |
| 5 | Watch SLIs 5–15 minutes |

1. Prefer progressive: 100% → 10% → 0% if unsure of dependency.
2. Multi-region: confirm all environments/projects updated.
3. If flag evaluated only at session start, note propagation delay.

### 5. Verify mitigation

1. Error rate, latency, queue depth return toward baseline.
2. Synthetic journey for critical path passes with flag off.
3. If no change: re-enable carefully or leave off and pursue other hypotheses—don’t thrash.

### 6. Stabilize

1. Prevent auto-schedulers / percentage ramps from turning it back on.
2. Lock flag changes to incident roles if platform supports.
3. Create fix ticket; keep flag off in production until verified.

### 7. Hand off / postmortem inputs

1. Timeline entries: detect → flag off → impact.
2. Was kill switch adequate? Gaps → `feature-flag-kill-switch` work.
3. Cleanup: remove flag post-fix per patterns skill.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Authority | IC-approved | Random engineer flips 20 flags |
| Scope | Targeted kill switch | Disable unrelated platform flags |
| Verify | Metrics + synthetic | “Should be fine” |
| Lock | Prevent re-enable | Nightly job re-enables 50% |
| Docs | Timeline with flag key | No record of what changed |

## Output Checklist

- [ ] Candidate flags listed with safety notes
- [ ] Authorization recorded
- [ ] Disable executed and timestamped
- [ ] SLI/synthetic verification captured
- [ ] Re-enable prevention set
- [ ] Fix ticket filed
- [ ] Postmortem notes updated
- [ ] Residual risk noted

## Rules

- Incident process first; don’t experiment wildly.
- Know fail-open/closed semantics before flipping.
- Communicate every production flag change.
- Design-time kill switches → `feature-flag-kill-switch`.
- Never leave temporary “off” undocumented for months.
