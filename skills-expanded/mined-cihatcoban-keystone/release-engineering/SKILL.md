---
name: release-engineering
description: Ships safely - versioning, changelog, reproducible builds, staged rollout, rollback, release-time migrations. Triggers - ship this to production, deploy, how should we roll this out, we need a rollback plan, version bump, canary, broke production after deploy.
---

# Release Engineering

A release is a change to the running world, and the only property that
consistently reduces its risk is the ability to **undo it quickly**. Faster,
smaller, reversible releases are safer than rare, large, carefully scheduled
ones — because the variable that dominates incident cost is time to recovery,
not change frequency.

## Prerequisites (not optional)

| Requirement | Why |
|---|---|
| All quality gates green | The pipeline is the contract, not a suggestion |
| Build is reproducible and versioned | You must know exactly what is running |
| Rollback path tested, not assumed | An untested rollback is a hypothesis |
| Migrations are backward compatible | Old and new code run simultaneously during deploy |
| Telemetry exists for the new behavior | Otherwise you cannot tell if it worked |
| Feature is behind a flag if incomplete | Deploy ≠ release |

**Separate deploy from release.** Deploying code and exposing behavior are two
events. Flags make the second one instant and reversible — which converts most
rollbacks from a redeploy into a toggle.

## Versioning

Semantic versioning, applied honestly:

- **MAJOR** — a consumer must change something
- **MINOR** — new capability, backward compatible
- **PATCH** — fix, backward compatible

Two rules people break: a behavior change that breaks a consumer is MAJOR even
if the signature is identical; and once published, a version is immutable —
fix forward with a new version, never re-tag.

Changelog entries are written for the **consumer**: what changed for them,
what they must do. "Refactored internals" belongs in the commit log, not the
changelog.

## Rollout strategies

| Strategy | Mechanism | Use when |
|---|---|---|
| Rolling | Replace instances gradually | Default for stateless services |
| Blue/green | Two environments, switch traffic | Fast rollback matters more than cost |
| Canary | Small traffic share first, watch metrics, expand | Risky change, enough traffic to measure |
| Progressive by flag | Percentage or cohort of users | User-visible behavior changes |
| Shadow | Run new path, discard output, compare | Replacing critical logic (`deprecation-and-migration`) |

Whatever the mechanism, define **in advance**: what you will watch, for how
long, and the numeric condition that triggers rollback. "Watch the dashboards"
without a threshold means the decision gets made by whoever is most optimistic.

## Migrations at release time

The deploy window has old and new code running together. Therefore:

- Schema changes are **expand → migrate → contract**, one phase per release
  (`data-modeling-and-storage`).
- The new code must work with the old schema, and the old code must survive the
  new one. Test both directions; the rollback path runs old code against a
  migrated database.
- Long backfills run outside the deploy, in batches, resumable.
- A migration that cannot be rolled back is a one-way door — it ships alone,
  with a backup verified immediately beforehand.

## Rollback

Decide the **trigger before the deploy**: error rate above X, p95 above Y ms,
business metric below Z for N minutes. Write it in the release note.

Order of preference: turn the flag off → route traffic back (blue/green) →
redeploy previous version → revert commit and roll forward. Whichever is
fastest and least clever.

Rolling back is not a failure of the release; it is the release process working.
Treat the decision as cheap and reversible so that nobody hesitates at the
moment it matters.

## After the release

- Watch the defined signals for the defined window before declaring success.
- Remove the flag once the feature is permanent — an old flag is an untested
  code path.
- Record what you learned if anything surprised you. Two surprises in the same
  area is a pattern worth fixing in the pipeline.

## Post-release verification

"Watch the signals" becomes a checklist you run, at fixed times, against
production — not against staging and not against a health endpoint alone:

| When | Check | Passes when |
|---|---|---|
| Immediately | The new version is what is serving | Build id or version endpoint matches the release, on every instance or region |
| Immediately | Critical user journeys, run as synthetic requests | Each journey succeeds end to end (sign in, the main write path, the main read path) |
| First 15 minutes | Error rate, latency p95/p99, saturation | Within the rollback threshold, compared with the same window a day or a week earlier |
| First 15 minutes | Logs | No new error signatures; the expected new log lines appear |
| First hour | One business signal (orders, sign-ups, messages sent) | Inside its normal band for the time of day |
| End of the window | Flags, migrations, background jobs | Flag states as planned; migrations done; queues draining |

Write the list into the release plan before deploying, with an owner and the
rollback trigger for each numeric row. If a check cannot be run, the release
is not verified — say so in the release notes instead of declaring success.

## Exit checklist

- [ ] Gates green; build versioned and reproducible
- [ ] Version number matches the nature of the change; changelog written for consumers
- [ ] Migration phase is backward compatible with the currently running version
- [ ] Rollback path tested, with a numeric trigger and an owner
- [ ] Rollout strategy and observation window defined before deploying
- [ ] Telemetry for the new behavior is live and checked after deploy
- [ ] Flag removal scheduled as a task
