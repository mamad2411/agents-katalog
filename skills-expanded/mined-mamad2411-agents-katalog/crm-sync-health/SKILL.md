---
name: crm-sync-health
risk_tier: bounded-write
description: >
  Daily health check on the CRM sync pipeline in Supabase that finds stuck runs, budget-exceeded errors, dead-lettered sources and stale sources, then applies two bounded bookkeeping repairs: it sweeps orphaned `running` rows and releases a dead-lettered queue task once a day unless it died of a budget overrun. Use when the user asks whether the CRM sync is healthy, whether a source is stuck or stale, what happened to the pipeline overnight, or invokes /crm-sync-health. Also the skill the scheduled daily run invokes. One line on a healthy day. Every repair is reported with its row counts, so the signal stays readable.
---

# CRM sync health

A standalone check. It assumes no memory of prior runs, because a scheduled firing has none. Everything needed to interpret the result is in this file or in the config.

**Find, repair the bookkeeping, report everything.** The check may make exactly two writes, both listed in Step 4, both reversible, both reported with counts. Anything else stays a human's call: no code change, no deploy, no secret or config change, no direct call to `sync-all`, no schema change, no `enabled` flip. If the real fix is outside that list, name it and stop.

Why repair at all: on 2026-09-15 `sams` blew its 300s budget three runs in a row, hit `max_attempts`, and the queue quietly stopped claiming it. Nothing resets a dead-lettered task on its own, so the source stayed dark for 21 days while the daily check reported the same stale number every morning. A check that sees the same corpse every day and only describes it is not doing the job.

Why repairs don't muddy the signal: every repair is printed with the source, the count and the date span, and a repair never turns a red line green in the same report. The report says what it found first, then what it did.

Read `${CLAUDE_PLUGIN_ROOT}/references/briefing-config.md` for the `crmHealth` block, and `${CLAUDE_PLUGIN_ROOT}/references/source-discipline.md` for the three-state rule: a database you could not reach is `unavailable`, never a clean pipeline.

---

## Step 1: Read the config

The `crmHealth` block in `briefings.config.json` carries the target and the baseline:

| Key | What it is |
|---|---|
| `crmHealth.projectId` | Supabase project id |
| `crmHealth.schema` | Schema holding `sync_log` and `sync_tasks` |
| `crmHealth.pipelineSources` | The source names that belong to the ticking pipeline |
| `crmHealth.stuckMinutes` | How long a `running` row may sit before it counts as stuck |
| `crmHealth.staleHours` | How long without an `ok` before a source counts as stale |
| `crmHealth.knownIssues` | Named open issues, so they report as still open rather than as news |
| `crmHealth.baseline` | The last verified result of the checks, with its date |

If the block is absent, say so and stop. Never guess a project id, and never run against a database the config does not name.

## Step 2: Run the four checks

One query via the Supabase MCP `execute_sql`. Substitute the config's schema, source list and thresholds. The left join on the source list matters: a source with no `ok` row at all must still show up as stale.

```sql
with src as (select unnest(array['sams','aiscrapesafe','stripe','clarify_pull','clarify_events_pull','clarify_mirror',
  'stigviewer_partner_pull','sams_events_pull','posthog_events_pull','product_pql',
  'customer_direct_advance','attio_pull','attio_users_mirror','attio_mirror']) s)
select 'c1 stuck' chk, source, count(*)::text n, min(started_at)::text oldest, max(started_at)::text newest
  from crm.sync_log where status='running' and finished_at is null and started_at < now()-interval '20 minutes' group by source
union all
select 'c2 budget', source, count(*)::text, min(started_at)::text, max(started_at)::text
  from crm.sync_log where status='error' and error_detail like '[elapsed %' and started_at > now()-interval '24 hours' group by source
union all
select 'c3 stale', s, coalesce(round(extract(epoch from now()-max(l.finished_at))/3600,1)::text,'never'), max(l.finished_at)::text, null
  from src left join crm.sync_log l on l.source=s and l.status='ok' group by s
  having max(l.finished_at) is null or max(l.finished_at) < now()-interval '10 hours'
union all
select 'c4 deadletter', source, consecutive_failures||'/'||max_attempts, last_finished_at::text, left(last_error,200)
  from crm.sync_tasks where enabled and consecutive_failures >= max_attempts
order by 1,2;
```

## Step 3: Read each check against the baseline

### Check 1: stuck runs

Expected: nothing. A row means **the wall-clock budget guard did not fire**, which is a different failure from a slow source. A slow source eventually logs `error`; an orphan sits at `running` forever, because a serverless isolate killed by the platform runs no JavaScript and can't report its own death.

Report per-source counts and the date span. Cross-check against check 3: orphans piling up while every source still has a recent `ok` is a bookkeeping failure, not an outage, and gets described that way.

### Check 2: budget-exceeded

The `[elapsed ` prefix is written only by the guard, so anything here is real. Pull the full row and **quote `error_detail` verbatim**:

```sql
select id, source, started_at, error_detail from crm.sync_log
where error_detail like '[elapsed %' and started_at > now()-interval '24 hours' order by started_at desc limit 5;
```

A summary of an error is an opinion. The verbatim string is the evidence.

An `[elapsed ...]` row whose message is an upstream HTTP 5xx (PostHog `500`, `503 Queries are a little too busy`) is a vendor blip, not a pipeline fault. If the same source has an `ok` after it, say "upstream 5xx, recovered on the next run" and move on.

### Check 3: stale sources

The pipeline ticks every four hours and cron drifts up to ninety minutes, so anything under `staleHours` isn't reported.

A source in `knownIssues` reports as **still open**, not as news. **A known-stale source that has dropped back under the threshold has recovered on its own. Say so plainly.** That's the good-news case and it's easy to lose in a report shaped around problems.

Any other source here is new and leads the report. If it also appears in check 4, check 4 is the cause; say so in one line.

### Check 4: dead-lettered tasks

`crm.claim_sync_tasks` skips any task where `consecutive_failures >= max_attempts`, and nothing ever resets it. A row here means the queue has stopped running that source entirely. This is the failure that hides best: no new errors, no new orphans, just silence and a growing stale number.

## Step 4: Repair (two writes, nothing else)

Run these only after the checks have been read and recorded for the report.

**Repair A: sweep orphans.** Rows still `running` after 2 hours are dead: the lease is 900s and the largest budget is 300s. Close them as errors with a note that is *not* `[elapsed ...]`, so check 2 never mistakes a sweep for a guard firing.

```sql
with swept as (
  update crm.sync_log set status='error', finished_at=started_at,
    error_detail='Orphaned run: source never returned, so finish() was never called and the row stayed status=running. Swept <YYYY-MM-DD> by the CRM sync health check (rows running > 2h).'
  where status='running' and finished_at is null and started_at < now()-interval '2 hours'
  returning source, started_at)
select source, count(*), min(started_at), max(started_at) from swept group by source;
```

Rows between `stuckMinutes` and 2 hours are left alone; they may still be in flight. Report them as stuck.

**Repair B: release a dead-lettered task, at most once a day, and never for a budget overrun.** Only when the task has not finished anything in the last 20 hours, and only when `last_error` is not a budget overrun (`exceeded its ... budget`). The 20-hour guard stops a loop. The overrun exclusion matters more: a source that runs out its budget also eats the run's wall clock, and the platform kills the isolate before the sources behind it finish. On 2026-10-06 releasing `sams` cost a whole tick: it overran again, one other phase-1 source completed, and `clarify_pull` was orphaned. An overrun needs a human, so it escalates instead.

```sql
update crm.sync_tasks set consecutive_failures=0, attempts=0, next_due_at=now(), updated_at=now()
where enabled and consecutive_failures >= max_attempts and last_finished_at < now()-interval '20 hours'
  and coalesce(last_error,'') not like '%exceeded its%budget%'
returning source, last_error;
```

The next scheduled `sync-all` tick picks the task up. Don't invoke `sync-all` yourself.

A dead-lettered task left in place leads the report. Quote `last_error` verbatim and say why it stayed: "budget overrun; needs a human" or "dead-lettered again after release; needs a human". For an overrun, name the options: give the source its own `deferred` invocation (like `attio_mirror`), make it faster, or raise `budget_ms` in `crm.sync_tasks` and `SOURCE_BUDGET_MS` in `sync-all/index.ts` together. A bigger budget alone doesn't help when the run's wall clock is the real ceiling. Then stop.

If either write fails, say which and why, verbatim. Don't retry.

## Step 5: Report

**Healthy (checks 1, 2 and 4 clean, check 3 only known issues, no repairs):** one line. `pipeline healthy.` or `pipeline healthy, <issue> still stale at Nh.`

**Anything else:** lead with the source name and check number. Quote `error_detail` verbatim where there is one. Say plainly whether it's a known issue or something new. Then a short **Repaired** block: what was swept (per source, count, date span), what was released, and when the next tick will show whether the release held. A repair is never reported as a fix to the underlying cause; it's bookkeeping.

**Database unreachable:** say the pipeline state is unknown, and that no repairs ran. Never report an unreachable database as healthy.

---

## Boundaries

- Two writes, both above, both reported with counts. No other write of any kind.
- No code change, deploy, secret, config, schema or `enabled` change. No direct `sync-all` call.
- Never runs against a project the config does not name.
- Never paraphrases an `error_detail`.
- Never reports an unreachable source as a clean one.
- Ruled-out causes belong in the project's engineering notes, not here.
