---
name: diagnose-bugs
description: MUST USE for systematic bug diagnosis — hypothesis loop, bisect, boundary isolation, observability-first. Complements debug skill when root cause non-obvious or intermittent.
---

# Diagnose Bugs

Diagnosis finds **mechanism** before fix. Complement `debug` (full reproduce-fix-verify loop) with structured hypothesis ranking, signal-first investigation, and sibling-pattern search — especially intermittent and prod-only bugs.

## When This Skill Applies

- Intermittent failures (<100% repro)
- Works locally, fails prod only
- "Sometimes slow" without stack trace
- Heisenbugs around timing/concurrency
- After `debug` Phase 2 stuck isolating

## Severity Model

| Level | Signal | Action |
|-------|--------|--------|
| **D0** | Data corruption / payment wrong intermittent | Stop feature; preserve evidence |
| **D1** | Prod-only no repro yet | Instrument first |
| **D2** | Repro local, cause unclear | Hypothesis loop |
| **D3** | Cosmetic | Low priority |

Cross-ref: `debug` for standard loop; `observability` for traces; `sql-write` for DB symptoms.

## Phase 0 — Symptom Charter

One page:

```markdown
Symptom: [user-visible]
Expected:
Actual:
First seen:
Frequency: X% / N users
Environments:
Already tried:
```

No fixes in charter.

## Phase 1 — Signals Before Code (2025–2026)

Check dashboards/logs/traces for incident window:

```promql
sum(rate(http_requests_total{status=~"5.."}[5m])) by (route)
```

| Signal shape | Hypothesis direction |
|--------------|---------------------|
| Cliff at deploy time | regression diff |
| Gradual rise | leak, queue backlog |
| Spike then flat | timeout threshold crossed |
| Periodic | cron, certificate expiry |

Cross-ref: `monitoring-check` if blind.

## Phase 2 — Hypothesis List (Ranked)

| # | Hypothesis | Predict if true | Cheap test | Result |
|---|------------|-----------------|------------|--------|
| 1 | Pool exhausted | active conns = max | metric query | |
| 2 | Cache stale | hard refresh fixes | curl headers | |

Max 5 active; kill fast with disproof.

## Phase 3 — Boundary Isolation

Walk path — test each hop independently:

```bash
curl -v https://edge/health
curl -v http://localhost:8080/health   # bypass edge
psql -c 'SELECT 1'
```

Binary search: disable feature flag, half traffic, half code path (`git bisect` if deploy-correlated).

## Phase 4 — Intermittent Toolkit

- Add **correlation id** logging at boundaries if missing
- Increase sampling on errors (OTel tail sampling)
- Record env: thread id, request id, lock holder
- Stress test with parallel requests — reproduce races

For races: look for check-then-act, shared mutable singleton, async without lock.

## Phase 5 — Sibling Search

When mechanism found:

```bash
rg -n "same_bug_pattern" --glob '*.py'
```

Fix class of bugs — report in output.

## Phase 6 — Handoff to Fix

Deliver to `debug` Phase 4 with:

- Proven root cause mechanism
- Minimal repro or metric signature
- Suggested regression test type

## Output Template

```markdown
## Bug Diagnosis: [title]

**Status:** solved / inconclusive / needs instrumentation
**Severity:** D0–D3

### Symptom charter
...

### Evidence timeline
- ...

### Hypotheses tested
| # | Result |

### Root cause mechanism
...

### Recommended fix direction
(not full impl unless asked)

### Siblings
- ...

### Observability gaps
- ...
```

## Anti-Patterns

- **Random config tweaks** without hypothesis
- **Production printf** without sampling — cost + PII risk
- **Stopping at proximate cause** ("DB timeout") without why timeout
- **Single trace** generalization
- **Skipping bisect** when deploy-correlated

## Cross-References

| Skill | Use when |
|-------|----------|
| `debug` | Full fix cycle |
| `diagnose-bugs` | You are here — deeper isolation |
| `incident-response` | Sev1 process |
| `ci-fix` | CI-only env diff |

## Cursor Kit Templates

- `monitoring` — dashboard links in runbook

## Extended Reference — Operational Drill

Run this drill when the skill triggers in production (not only doc review):

1. **Capture evidence first** — commands, screenshots, log lines with timestamps; do not change prod before snapshot.
2. **Classify severity** using this skill's table; if between two levels, choose the higher until disproved.
3. **Apply the smallest fix** that addresses root cause; avoid drive-by refactors in the same change.
4. **Verify with the same command** that failed before; add automated guard (CI rule, test, alert).
5. **Record in output template** and link follow-up skills from Cross-References.

## Extended Reference — Runnable Sanity Pack

```bash
# Repository context (adapt paths)
git status -sb
git log -3 --oneline
# Replace SVC with your service name
test -f docker-compose.yml && docker compose ps
test -f package.json && npm run -s test 2>&1 | tail -5
```

## Extended Reference — Stakeholder Comms

| Severity | Who to inform | Channel | SLA |
|----------|---------------|---------|-----|
| Blocker | On-call / founder | incident chat | <15m |
| High | Team lead | ticket comment | same day |
| Medium | PR reviewer | PR description | this sprint |
| Low | backlog | deferred list | next review |

## Extended Reference — Definition of Done

- [ ] Output template filled completely
- [ ] Severity assigned per finding with fix snippet
- [ ] Cross-skill follow-ups checked or N/A with reason
- [ ] No secrets pasted into notes or tickets
- [ ] Re-run key verification command after fix

## Extended Reference — 2025–2026 Practice Notes

- Prefer **automation in CI** over manual checklist repetition for this domain.
- Pair **metrics/alerts** with any production change recommended here (`observability` where applicable).
- Document **rollback** in the same PR/issue as the forward fix.
- Keep playbooks **versioned in git** — when process changes, update this SKILL in the same PR.

## Extended Reference — Common Questions

**Q: How long should this review take?**  
A: Time-box discovery (15–30m), then fix loop. If stuck without new evidence, switch to `diagnose-bugs` or `research`.

**Q: Can we waive a blocker?**  
A: Only with written accept + expiry date + compensating control; never silent waive.

**Q: What if tools are missing locally?**  
A: Run what you can; document gaps in "Commands run" with install note — do not skip severity classification.

## Extended Reference — Finding ID Convention

Use stable IDs in reports: `[SKILL]-001`, increment per session. Refer to IDs in PR comments for traceability.

## Extended Reference — Pair Review

For S0/A0/T0 class issues, second person validates reproduction steps before merge when team size allows.

