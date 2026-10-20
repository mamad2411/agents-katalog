---
name: feature-flags-architect
description: >
  Feature flag strategy, lifecycle, and operations for production systems. Use
  when designing a flag taxonomy, planning a gradual rollout, building kill
  switches for risky changes, auditing flag debt in a codebase, defining flag
  governance (who can flip what, when, and how), running progressive delivery
  experiments, or recovering from a bad release via flag-based rollback. Covers
  the four flag types (release, ops, experiment, permission), rollout
  ramp patterns, blast-radius math, kill-switch runbooks, and the flag-debt
  cleanup loop that prevents flag rot.
license: MIT + Commons Clause
metadata:
  version: 1.0.0
  author: borghei
  category: engineering
  domain: engineering
  updated: 2026-05-27
  tags: [feature-flags, progressive-delivery, rollouts, kill-switches, release-engineering, experimentation, flag-governance]
---

# Feature Flags Architect

End-to-end feature flag design, rollout, and lifecycle management. Covers flag taxonomy (release vs ops vs experiment vs permission), gradual rollout patterns with blast-radius math, kill-switch runbooks, governance (who can flip what), and the flag-debt cleanup loop that keeps a codebase from drowning in stale flags.

This skill is provider-agnostic: the patterns work whether you run LaunchDarkly, Statsig, Unleash, Flagsmith, ConfigCat, GrowthBook, OpenFeature, or a homegrown system backed by Redis/DynamoDB/Postgres.

---

## When to use this skill

| Situation | Skill applies |
|-----------|---------------|
| Designing a flag system from scratch | Yes — start with the **flag taxonomy** section |
| Planning a risky release (DB migration, payment provider swap, framework upgrade) | Yes — use the **rollout ramp** + **kill switch** sections |
| Auditing a codebase that has hundreds of flags and growing | Yes — use the **flag debt cleanup** section + `scripts/flag_audit.py` |
| Setting up an A/B test or hold-out experiment | Partially — covers the flag side; pair with `engineering/experiment-design` for statistics |
| Building a kill switch for a third-party dependency outage | Yes — use the **kill switch runbook** generator |
| Defining who in the org can flip production flags | Yes — use the **governance** section |
| Building entitlements / paid-tier gating | Use this for the flag mechanics; use `business-growth/paywall-upgrade-cro` for the UX |

---

## Flag taxonomy — the four types

Every flag belongs to exactly one of these four types. The type determines the lifecycle, who can flip it, and whether it should auto-expire. Mixing types in one flag is a root cause of flag debt.

| Type | Purpose | Lifetime | Who flips | Auto-expire? |
|------|---------|----------|-----------|--------------|
| **Release** | Decouple deploy from release. Ship code dark, ramp to users. | Days to weeks | Engineer who owns the feature | Yes — remove after 100% rollout + 1 release |
| **Ops** | Kill switches, circuit breakers, throttles. Turn off risky behavior fast. | Permanent or long-lived | Oncall / SRE / platform team | No — but review quarterly |
| **Experiment** | A/B test, multi-arm bandit, hold-out group. Measure causal impact. | Weeks to months (test duration) | Product / data / growth | Yes — remove after winner is shipped |
| **Permission** | Entitle users to features based on plan, role, beta-list. | Permanent | Product / billing | No — but consolidate into entitlement system |

**Decision rule when adding a flag:** name the type. If you can't, the flag shouldn't exist yet — clarify intent first.

See [references/flag-types-and-patterns.md](references/flag-types-and-patterns.md) for code patterns per type, including server-side vs client-side trade-offs, evaluation-context schema, and naming conventions.

---

## Rollout strategy — the ramp

A flag without a rollout plan is just a config toggle. The rollout plan is the difference between "we shipped a feature" and "we shipped a feature without paging anyone."

### Standard ramp pattern

| Step | % | Hold | Watch | Exit criteria |
|------|---|------|-------|---------------|
| Dogfood | Internal users only | 1-3 days | Error rate, manual feedback | Zero blocker bugs |
| Canary | 1% of users | 24 hours | Error rate vs baseline, p99 latency, business KPI | No regression > 2 stdev |
| Early adopters | 5% | 24-48 hours | Same metrics | Same |
| Quarter | 25% | 24-48 hours | Same + cost / capacity | Same |
| Majority | 50% | 24-48 hours | Same | Same |
| Full | 100% | 1 week observation | Same | Plan flag removal |
| Cleanup | Remove flag | n/a | n/a | PR merged, control plane entry deleted |

This is the **safe default**. Move faster if blast radius is low; slower for irreversible / high-cost / hard-to-monitor changes.

### Blast radius math

Before flipping, compute:

```
blast_radius = (users_affected_per_pct × pct_enabled) × (avg_session_count × time_to_detect_minutes / 60)
```

Use `scripts/rollout_simulator.py` to model this for your traffic profile. Output: estimated affected users at each ramp step, ETA to detect a regression, and a recommended ramp schedule.

See [references/rollout-and-kill-switch-playbook.md](references/rollout-and-kill-switch-playbook.md) for ramp templates by change type:

- Pure UI / cosmetic — `aggressive` ramp (1% → 100% in 24h)
- New feature, additive — `standard` ramp (1 week)
- Backend migration with dual-write — `cautious` ramp (2-3 weeks)
- Schema change, irreversible writes — `conservative` ramp (4-6 weeks with cohort isolation)
- Third-party dependency swap — `phased` ramp by user-segment, never by random %

---

## Kill switches — the ops flag pattern

Kill switches are the cheapest insurance you can buy. Every external dependency, every risky code path, every feature that could go wrong should have one.

### When to add a kill switch

- New third-party SDK / API integration (e.g., new payment gateway)
- New caching layer (Redis, CDN, edge compute)
- Any code path that could explode the database (background job, sync write to slow downstream)
- AI / ML inference calls (LLM, embeddings, recommendations) — high cost, variable latency
- Any auth flow change

### Kill switch design

A good kill switch:

1. **Defaults to ON** (feature enabled). Flipping the switch turns the feature **off**, falling back to the previous behavior.
2. **Fails open or closed deliberately.** Document which, and why. Most safety kill switches fail open (allow traffic through, but skip the new feature). Some (auth, billing) must fail closed.
3. **Has a runbook attached.** Anyone on oncall can flip it without paging the owner.
4. **Is independent of the release flag.** A release flag controls rollout; a kill switch controls outage response. Don't reuse one for both.
5. **Has alerting wired in.** When flipped, the on-call rotation is paged so the team knows something failed.

Use `scripts/kill_switch_runbook.py` to generate a runbook template for a kill switch (flag name, expected behavior on/off, who to page, rollback steps, post-incident actions).

---

## Flag governance — who can flip what

The governance model is independent of the tool. Map these roles into whichever flag system you use.

| Role | Can flip | Cannot flip | Requires approval |
|------|----------|-------------|-------------------|
| Engineer (feature owner) | Release flags they own, in non-prod | Production release flags > 5%, any ops/permission flag | Yes for prod ramp steps > 5% |
| Engineer (any) | Nothing in prod | Anything in prod without approval | Yes for any prod flip |
| Oncall / SRE | Any ops flag, kill switches | Permission flags, experiments | No — but must log + post-incident review |
| Product / Growth | Experiment flags, permission flags (paid tiers) | Release, ops | Yes for experiment changes mid-flight |
| Anyone | Read-only access, evaluation history | Any flip in prod | n/a |

### Audit log requirements

Every flag flip in prod logs:
- Who flipped it (human or system, with identity)
- When (ISO 8601 timestamp, UTC)
- From what value to what value
- Justification (free-text, required for non-emergency flips)
- Related ticket / incident (required for ops flips)

Retention: 1 year minimum for release/experiment, 7 years for permission flags (legal/billing).

---

## Flag debt — the cleanup loop

Stale flags rot. They:

- Add code paths that aren't tested
- Confuse future readers ("is this still active?")
- Hide dead code from coverage tools
- Increase the chance of mis-flipping a permanent flag
- Multiply the matrix of states that QA has to verify

Every flag added without a removal plan becomes flag debt.

### The cleanup loop

Run quarterly (more often if you ship fast):

1. **Inventory** — run `scripts/flag_audit.py --path .` against your codebase. Output: every flag reference, age, type, last-flipped date, percent enabled.
2. **Classify** — for each flag: is it (a) still ramping, (b) at 100%, (c) at 0% for > 30 days, (d) unreferenced in code.
3. **Decide**:
   - Still ramping → keep, check the rollout is progressing
   - At 100% for > 1 release → schedule removal (flag is now permanent control flow — delete it)
   - At 0% > 30 days → either flip on or remove (decision the owner has been avoiding)
   - Unreferenced in code → delete from control plane immediately
4. **Execute** — open PRs to remove flag code paths. Use the audit output as the PR description.
5. **Measure** — track flag count over time. Healthy systems have stable or shrinking flag count; debt growth is a red flag (pun intended).

See [references/flag-debt-and-cleanup.md](references/flag-debt-and-cleanup.md) for the full cleanup runbook including how to remove flags safely, dead-code detection patterns, and PR templates.

---

## End-to-end workflows

### Workflow: Add a new release flag

1. **Name it** following the convention `<team>.<feature>.<rollout-step>` (e.g., `growth.signup_v2.enabled`).
2. **Type it** as `release` in the control plane.
3. **Set defaults** — off in prod, on in dev/staging.
4. **Add to code** behind a single-purpose evaluation function. Don't sprinkle `if flag` everywhere.
5. **Add a removal ticket** to the team backlog with target date = expected ramp end + 1 sprint.
6. **Deploy** the code, dark.
7. **Run the ramp** per [rollout-and-kill-switch-playbook](references/rollout-and-kill-switch-playbook.md) using `scripts/rollout_simulator.py` to compute blast radius.
8. **Monitor** key metrics at each step.
9. **At 100% + 1 release**, remove the flag, code paths, and tests for the old path.

### Workflow: Build a kill switch for a new dependency

1. **Identify the failure mode** — what happens if the dependency is slow, down, returns bad data?
2. **Pick fail-open vs fail-closed** — document the choice.
3. **Add the kill switch flag** as type `ops`, defaults to feature-on.
4. **Wrap the dependency call** in a single function gated by the flag.
5. **Add the fallback path** — what happens when the flag is off. Test it.
6. **Generate the runbook** with `scripts/kill_switch_runbook.py --flag <name> --feature <name>`.
7. **Page oncall** — register the runbook in your incident response wiki.
8. **Test it in staging** — flip the flag, verify fallback works.
9. **Add alerting** — when the flag is flipped to off in prod, page the team.

### Workflow: Audit flag debt before a code-freeze / migration

1. **Run** `scripts/flag_audit.py --path . --format json > flags.json`.
2. **Triage** — read the output, classify each flag (still ramping / 100% / 0% / unreferenced).
3. **Identify zero-risk removals** — unreferenced flags + flags at 100% for > 90 days.
4. **Open cleanup PRs** in batches of 5-10 flags. Each PR removes the flag, the gated branch, and the now-dead alternate branch.
5. **Re-run audit** post-cleanup to confirm flag count dropped.
6. **Track flag count** as a team metric. Cap it (e.g., "no team owns more than 20 active flags").

### Workflow: Recover from a bad release using flag-based rollback

1. **Identify the regression** — error rate spike, customer report, alert.
2. **Find the flag** — every prod-impacting change should be behind a flag. If it isn't, that's a separate process bug to fix later.
3. **Flip the flag off** — via control plane, not a code deploy.
4. **Confirm recovery** — error rate returns to baseline within minutes.
5. **Log the flip** in the incident channel with timestamp + who flipped.
6. **Post-incident**: root-cause the regression, fix the code, retest, re-ramp with smaller initial step (e.g., 0.1% instead of 1%).

---

## Anti-patterns

- **Nested flags.** `if flag_a and flag_b and not flag_c`. Refactor: collapse into one decision function with a clear input contract.
- **Flag-as-config.** A flag that has been at the same value for > 6 months and isn't a kill switch isn't a flag — it's config. Move it to your config system.
- **Permission flags as release flags.** Don't mix: a paid-tier gate has different lifecycle requirements than a feature rollout.
- **No removal plan.** Every flag PR should include a removal ticket. If the team can't agree on a removal trigger, the flag probably shouldn't ship.
- **Flipping flags in code deploys.** Defeats the purpose. Flag flips happen via the control plane, instantly, with audit log.
- **Random sampling for irreversible operations.** If a flag controls a one-way write (delete user, charge card, send email), don't use percentage rollout — use explicit cohorts you can verify.
- **One giant flag for "the new system".** Decompose: `db_v2.dual_write`, `db_v2.read_from_v2`, `db_v2.delete_v1`. Each can ramp and roll back independently.

---

## Tooling outputs

| Script | Input | Output |
|--------|-------|--------|
| `scripts/flag_audit.py` | Codebase path, optional flag-system export JSON | List of flag references, age, classification, recommended action. JSON or markdown. |
| `scripts/rollout_simulator.py` | Total user count, target metric, ramp profile name | Per-step blast radius, time-to-detect estimate, recommended ramp schedule |
| `scripts/kill_switch_runbook.py` | Flag name, feature description, dependency name, oncall rotation | Markdown runbook with default state, flip procedure, validation, escalation |

All scripts: standard library only, argparse CLI, both JSON and human-readable output. Run `--help` on any for full usage.

---

## References

- [flag-types-and-patterns.md](references/flag-types-and-patterns.md) — taxonomy, code patterns per type, evaluation context, naming conventions, server-vs-client trade-offs
- [rollout-and-kill-switch-playbook.md](references/rollout-and-kill-switch-playbook.md) — ramp templates by change type, blast-radius math, kill-switch design, monitoring/alerting hookup
- [flag-debt-and-cleanup.md](references/flag-debt-and-cleanup.md) — cleanup loop, dead-code detection, safe removal patterns, governance for flag count

---

## Related skills

- `engineering/observability-designer` — wire the metrics needed to make ramp decisions
- `engineering/incident-commander` — flag-based rollback during incidents
- `engineering/chaos-engineering` — verify kill switches actually work under fault injection
- `product-team/experiment-design` (if available) — statistical design of A/B tests behind flags
