---
name: deprecation-and-migration
description: Removes or replaces something people depend on without breaking them - usage measurement, sunset, consumer migration, dual-running, safe deletion. Triggers - can we delete this old endpoint, deprecate, sunset this feature, move users off the legacy system, dual write.
---

# Deprecation and Migration

Code is a liability: every line is maintained, patched, tested and explained
forever. Most organizations are competent at building and poor at removing,
which is why systems accumulate parts nobody understands and nobody dares
delete. Deliberate removal is an engineering discipline with a method.

## Before removing anything: measure use

"Nobody uses this" is a hypothesis. Verify it:

- Instrument the code path and wait a **full business cycle** — month-end,
  quarter-end and annual jobs are exactly the traffic you will miss in a week
  of observation.
- Log caller identity, not just call count. You need to know *who* to talk to.
- Search the organization: other repositories, dashboards, scripts, scheduled
  jobs, documentation, support macros.
- Zero calls in a full cycle is evidence. Zero calls in three days is not.

## The sunset sequence

| Phase | Action | Exit condition |
|---|---|---|
| 1. Announce | Publish replacement, migration guide, and a **date**. Tell identified consumers directly | Guide exists and the path is proven by one real migration |
| 2. Discourage | Deprecation warnings in logs, headers, docs, editor annotations | New adoption stops |
| 3. Assist | Migrate the consumers you control; help the rest; codemod if possible | Remaining usage is known and named |
| 4. Degrade | Rate-limit, add latency, brownout (scheduled short outages) | Remaining callers have noticed |
| 5. Disable | Turn it off behind a flag, keep the code | No complaints for the observation window |
| 6. Delete | Remove code, schema, docs, tests, dashboards, alerts | Nothing references it |

Do not skip phase 5. A reversible disable turns "we think it's safe" into
evidence, at the cost of a flag.

**Brownouts** (phase 4) are the most effective tool available: a planned
15-minute outage announced in advance surfaces the silent consumer who ignored
every announcement, while the impact is still small and scheduled.

## Migrating consumers

- **The migration guide must show the before and the after**, in code, for the
  common case. A description of the new API is not a guide.
- Provide a compatibility shim where possible: the old interface, implemented
  on the new one. It buys time and decouples your delivery from theirs.
- Migrate one real consumer yourself before asking others. It is the only way
  to find out the guide is wrong.
- Track progress in one visible place: who is migrated, who is not, blocked by
  what.
- Never extend the deadline silently. Extend it once, publicly, with a reason —
  or hold it. A deadline that slips twice stops functioning.

## Data migration

- Dual-write first, read old, compare — a shadow period with a difference log
  is the only real proof the new path matches.
- Backfill in resumable batches with progress recorded; assume it will be
  interrupted.
- Verify **before** cutting over: row counts, checksums, spot-checks of edge
  records (nulls, oldest rows, unicode, very large values).
- Keep the old data read-only for a defined period after cutover. Deleting it
  is the last step, separate, after a verified backup.
- Irreversible deletion always ships alone.

## The cleanup nobody does

Deletion is not complete until these are gone too: the feature flag, the
dual-write code, the old tests, the monitoring dashboard, the alerts, the
runbook entry, the documentation, the unused dependency, the schema, the
permissions and the scheduled job.

Leftovers are worse than the original: a dashboard for a dead feature misleads
during the next incident, and an orphaned alert pages someone at 3am for
something that no longer exists.

## When not to remove

- It works, is cheap to keep, and removal risk exceeds maintenance cost
- Mid-incident or during a freeze
- You cannot identify the consumers — finish measuring first
- The replacement is not yet proven in production

## Exit checklist

- [ ] Usage measured over a full business cycle, with caller identity
- [ ] Replacement exists and one real consumer has migrated to it
- [ ] Sunset date published, with direct notice to known consumers
- [ ] Deprecation warnings in place; new adoption stopped
- [ ] Disabled reversibly and observed before deletion
- [ ] Data verified (counts, checksums, edge records) before cutover
- [ ] Backup verified before any destructive step
- [ ] Flags, tests, dashboards, alerts, docs, schema and jobs all removed
