---
name: job-lifecycle-scan
description: "Jobs and schedules: model in the payload, deleted record, payload drift, self-overlap, misfire, schedule zone, lost failure — read-only."
kind: skill
pack: backend
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: job-lifecycle-scan

## Premise

A background job makes a contract with three things a request never meets: **time**, **deploys** and **its own result**. Each breaks without a failing test. A Celery task handed an ORM instance under `pickle` runs on the enqueue-time copy and `save()`s it over newer data. A record deleted before the worker picks the job up turns into N retries and a dead-letter row instead of one discard. A rolling deploy hands old payloads to new code: a renamed field reads `undefined`, an amount becomes `NaN`. A `@Cron` that sometimes runs longer than its period runs **twice at once on one process** — npm `cron` and node-cron overlap by default, and `@nestjs/schedule` does not change that. A month-end charge scheduled in-process at 02:00 is simply skipped when no process is up at 02:00, and a zone-less `30 2 * * *` in a DST zone fires at 03:00 one day a year and twice on another. A FastAPI `BackgroundTasks` raises after the 200 was sent, and a scheduled method that throws leaves one log line. This skill finds those shapes and proves each with **cross-commit replay, the scheduler's own fire-time iterator plus a concurrency counter, and a failing run that must leave a record**. Read-only: it never edits code.

Backend owns **one service's job contract** (eval § 4.1, § 4.2): what the payload carries, whether it survives a deleted row and a deploy, whether a schedule overlaps **itself on one process**, misses a fire time or fires in the wrong zone, and whether a failure is recorded. Job idempotency, retries, locks and commit-then-publish are distributed-systems'; enqueue inside a transaction is database's; once-per-fleet is performance's (§ Boundaries). It owns `/backend-audit`'s job rows (`job-lifecycle-scan §1–§7`); `@api-reviewer` (this pack) judges them in refute mode.

**Every finding cites the producer, processor or schedule entry `<file:line>` + the inventory row it depends on (the scheduler or queue library and its version, the base processor or scheduler wrapper, the process TZ) + what happens (the run count, the fire times, the stale value, the missing record) against what the job promises + the oracle that showed it, or the run that would settle it + the fix in the project's own wrapper.** A grep hit is a candidate. "Jobs look fine" is never printed; the output is the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/backend.md`](../../../../snippets/precedents/backend.md). The oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Backend: V351 (job payload replay), V352 (fire times and overlap), V353 (job failure recorded) and V357 (the version pair rule).

## The rule

A candidate is a finding when all four hold — `precedents/backend.md` § Reading the seven gates for backend, applied to jobs.

1. **Part A holds: this job runs in production.** The processor is registered by a module a deployed process type loads, the schedule entry is enabled (`disabled`, an env flag, a `ScheduleModule` imported only by a worker that is deployed), the producer is on a live path. A script, a test harness or a one-off CLI is not a job (gate 1).
2. **Part B holds at the installed version.** The queue and scheduler versions come from the lockfile (F1); without one they are `UNREAD` and every row resting on a default is Unconfirmed (V357). The defaults in § Adapt were read from installed source or run; a `[K]` default is Unconfirmed until V352/V353 runs on the installed version.
3. **Nothing already controls it**, across files: a base processor or scheduler wrapper (P5 — one row with N sites), a lease or claim taken first in the handler (a Redis `SET … NX`, `pg_try_advisory_xact_lock`, a unique `INSERT … ON CONFLICT DO NOTHING`), an in-process running flag, a `version` field with a dispatcher for every version, a drain-before-deploy runbook that is enforced (B-R7), a catch-up query (`due ≤ now and not yet posted`), a failed listener that writes a dead-letter or a status row.
4. **The oracle fired, or the fact is two-ended.** V351–V353 on the real queue and the library's own scheduler (tier U) shows the stale write, the double run, the lost fire time or the missing record, or the static fact cites both ends (tier S: the default at the installed version, and the handler that outlives its period or must run). Without one, the row is `[report-flagged]` / Unconfirmed with the settling run written out.

## Boundaries

One class, one owner. A neighbour that sees the same `file:line` lists it as corroboration (`precedents/backend.md` § Owned elsewhere). Each routed row prints `→ <pack> <skill> §n (k)` and is never graded here; without the owner's pack the hits are listed tagged `<class> (owner pack <x> not installed)`, never at the owner's severity.
- **A redelivered or stalled job repeating its effect, poison messages and the dead-letter path, a lock or visibility shorter than the run** → distributed-systems `messaging-scan` §2/§3/§6 (V292, V293), when the distributed-systems pack is installed; without it performance `request-path-scan` §24 is the fallback. `removeOnFail: true` (7b) is its §3 row.
- **Retrying a validation error (BJ-09) and a retry that repeats an earlier step of the same job (BJ-10)** → distributed-systems `retry-deadline-scan` §1 and §6 (V304, V308). **The lock or lease guarding a schedule** — its release, TTL and renewal — → `coordination-scan` §1–§4; **a coordinated schedule's DST day** (a fleet lock shorter than the repeated hour, a lock key built from the local date) → `coordination-scan` §11 (V319). §6 here owns one schedule's own zone and prints `→ distributed-systems coordination-scan §11 (k)` for the zone rows whose handler takes a fleet lock.
- **Commit, then publish with nothing durable between** → distributed-systems `dual-write-scan` §1; **Temporal and durable-workflow versioning** → `workflow-scan` §2; **an event schema shared across services** → `event-contract-scan`. §3 here owns one service's job payload.
- **Enqueue inside an open transaction** (the worker reads "not found", a rollback leaves a phantom job — BJ-01) and **model callbacks that enqueue before commit** (BS-04) → database `transaction-scan` §1 (V8), when the database pack is installed (`precedents/backend.md` § B-R6).
- **A schedule every replica runs** → performance `request-path-scan` §20 (V40); **durable work held in process memory** (`BackgroundTasks`, `@Async`, a `void` promise lost on restart) → its §22 (V42). One cron that overlaps itself **and** runs on every replica is two findings: §4 here and perf §20.
- **A k8s CronJob manifest** (`timeZone`, `concurrencyPolicy`, `startingDeadlineSeconds`) → infrastructure `k8s-wiring-scan` §5 (V277), when the infrastructure pack is installed. **Migrate-on-boot** (BJ-12) → devops `deploy-safety-scan` §1.
- **A fire-and-forget promise nobody observes** → code-quality `error-handling-scan` §4; **DST arithmetic in code** → `correctness-smell-scan` §6. **A cron or worker with no counter** → observability `metric-hygiene-scan` §2; a failure record nothing alerts on → `alert-audit`. §7 here owns whether a failure leaves **any** record; both rows stand.
- **Pickle as a deserialization hole** → security `sast-scan`. §1 here owns the stale write.
- **Data-orchestrator DAGs** (Airflow, Dagster, Prefect, dbt Cloud jobs) → data-engineering `orchestration-scan`, when installed. This skill reads the application's own schedulers and queues.

## Adapt to the codebase — the lanes

Read every queue and scheduler library **with its version** (F1), the process TZ (F2) and the inventory (grep 0) first. `[V]` rows were run or read from installed source (§ Sources); `[K]` are vendor docs not run here.

| Lane | Defaults that decide verdicts | Controls and decoys |
|---|---|---|
| **`@nestjs/schedule`** 6.1.3 and 12.0.2 (on npm `cron` 4.4.0, pinned exactly) | `@Cron` is `CronJob.from({ ...options })`: `waitForCompletion` is off unless the decorator passes it, so a run longer than the period overlaps the next; `@Interval` is `setInterval(target)` with no option at all; every scheduled method is wrapped in a `try/catch` that only logs (`Logger('Scheduler').error`); no `timeZone` → process TZ [V source, both tarballs read 2026-10-14]. A real repo with no lockfile reads `UNREAD` (gate 3) | `@Cron(expr, { waitForCompletion: true, timeZone })`; a lease or running flag first in the handler; a failure counter or run row in the handler's `catch` |
| **npm `cron`** 4.4.0 | overlaps by default (1 s schedule, 2.5 s work → 3 concurrent); `waitForCompletion: true` serialises; no `timeZone` → process TZ; `30 2 * * *` in America/New_York fires 03:00 on spring-forward day; a tick delayed past `threshold` (250 ms) is skipped with a console warning [V ran lab B; `threshold` read from source]. In-process, nothing persists: a fire time with no process up never runs | positional `waitForCompletion` (10th argument) — read it |
| **node-cron** 4.6.0 | `noOverlap` defaults to false (2 concurrent in the same test); `timezone` option [V ran] | `{ noOverlap: true, timezone }` |
| **BullMQ** 6.3.15 / `@nestjs/bullmq` | `attempts` 0 → one try; the failed set is kept unless `removeOnFail`; Job Schedulers (`upsertJobScheduler`, `repeat`) can overlap a long run when worker concurrency > 1 [V source; overlap K] | a `failed` listener that dead-letters or settles a status row; a base processor that declares it (P5) |
| **Celery** 5.6.3 · **APScheduler** 3.11.3 | Celery: `task_serializer='json'` (pickle is opt-in), `enable_utc=True`, `timezone=None` → beat in UTC; beat sends on schedule whatever the last run did [K]. APScheduler: `max_instances=1` (safe, B-R1), `coalesce=True`, `misfire_grace_time=1` s — a run more than 1 s late is skipped [V source] | `misfire_grace_time` / `job_defaults`; a task lock |
| **Rails Active Job** 8.1 · **Sidekiq** 7+ | GlobalID arguments raise `ActiveJob::DeserializationError` when the record is gone; no retry unless `retry_on` [V guide 8.1.4]; Sidekiq rejects non-JSON arguments (7+) [V secondary] | `discard_on ActiveJob::DeserializationError` in `ApplicationJob` covers every job |
| **Laravel** 12.x | scheduled tasks overlap by default; `withoutOverlapping()` lock expires after 24 h; DST: a task "may run twice or not at all"; `SerializesModels` re-fetches by id; jobs try once by default [V docs] | `->withoutOverlapping()->timezone(…)`; `$deleteWhenMissingModels = true`; a `failed()` method |
| **Spring** (Boot 3.2+) · **Quartz** | with `spring.threads.virtual.enabled=true` every execution gets its own virtual thread, so `fixedRate` overlaps itself (spring-framework #31900, #33408) [V issues]; `@Scheduled(cron)` without `zone` → JVM zone [K]; `@Async void` exceptions reach only the `AsyncUncaughtExceptionHandler` (logged) [K]. Quartz: overlap unless `@DisallowConcurrentExecution`; no misfire instruction → the smart policy fires once now [K] | `fixedDelay`; ShedLock; `zone = "…"`; `withMisfireHandlingInstruction…` |
| **robfig/cron** v3 · **FastAPI** 0.143 | robfig overlaps unless `SkipIfStillRunning`/`DelayIfStillRunning`; zone via `CRON_TZ=` or `WithLocation` [K]. FastAPI `BackgroundTasks` that raise leave the response a 200 [V ran] | a durable queue for work that must happen (perf §22) |

## Tool lane and ledger

Each tool prints `ran` / `blocked (<why>)` / `NOT-RUN (<why>)` in the output header.

| Tool | Command | Covers | Limits |
|---|---|---|---|
| **Fire-time iterator + concurrency counter** (V352) | the library's own iterator over a year in the business zone (`cron`'s `sendAt`/`CronTime.getNextDateFrom`, APScheduler `get_next_fire_time`, Quartz `getFireTimeAfter`, robfig `Next`); the handler's schedule overridden to every 1 s with a 2.5 s body for 6 s, entry/exit counted; fake timers for downtime | §4–§6 | the handler must be callable from a harness (an exposed `runOnce` or the provider resolved from the real module); `NOT-RUN` otherwise, never PASS |
| **Cross-commit replay** (V351) | `git worktree add $SCRATCH/prev <base>`; enqueue with the old producer, run the new processor on the real queue in a container, then the reverse; for §1–§2 enqueue, update or delete the row, then run | §1–§3 | an eager or in-process queue proves nothing |
| **Failure record** (V353) | make the processor or scheduled method throw on the real queue; assert a failed-jobs row, a dead-letter entry, a status row set `failed` or a counter an alert reads | §7 | — |
| Larastan `checkJobSerializesModels` | `vendor/bin/phpstan analyse` with the rule enabled | §1–§3 Laravel lane (dispatch arguments vs the job constructor) | opt-in [K docs] |

## Pre-flight greps

Run as **one** script from the repo root (shell state does not survive between tool calls; bash 3.2-safe). Grep **N** feeds detector **§N**; F1, F2 and grep 0 are the gates every § reads first. Every `rg` names its path — `.` or `"${ROOTS[@]}"`: given no path, `rg` reads stdin under an agent's shell and reports a silent zero. Include globs come **first**, exclusions last; with an explicit root, globs match relative to it, so exclusions start with `**/`. Any `rg` exit 2 is a failed grep, never zero hits. A block question ("this `@Cron` has no `waitForCompletion`") is a bounded `-U` lookahead over the call's balanced parentheses or a file-level `--files-without-match`, never `-A<n> | rg -v` (rg-context-negation).

```bash
ROOTS=(.)   # server and worker code; in a monorepo name the apps: ROOTS=(apps/api apps/worker). Manifests always search .
BASE="${BASE:-}"   # §3 diff lane: BASE=<base-branch> runs it; empty → N/A (the 3w whole-repo lane always runs)
SCAN="${SCAN:-$(mktemp -d "${TMPDIR:-/tmp}/jl.XXXXXX")}"; mkdir -p "$SCAN"
CODE=(-g '*.{ts,mts,cts,js,mjs,cjs,py,java,kt,cs,go,php,rb}')
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/{dist,build,out,target,coverage,.next,.venv,venv,generated,__generated__}/**'
   -g '!**/{test,tests,__tests__,spec,specs,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata}/**'
   -g '!**/*.{spec,test,e2e-spec,stories}.*' -g '!**/test_*.py' -g '!**/*_test.go' -g '!**/*.d.ts' -g '!**/*.min.*'
   -g '!**/{migrations,migration,db/migrate,seeders,seeds}/**' -g '!**/{locales,locale,i18n,translations}/**' -g '!**/{docs,ai,.claude}/**')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(?://|/\*|\*(?:\s|/|$)|#(?!\[))')   # drops comment-only lines
# F1 queue, scheduler and workflow libraries — ranges from manifests; exact versions from the lockfile (gate 3; V357)
rg -n --no-heading --pcre2 '"(bullmq|bull|bee-queue|@nestjs/bullmq|@nestjs/bull|@nestjs/schedule|cron|node-cron|node-schedule|toad-scheduler|agenda|bree|pg-boss|graphile-worker|@temporalio/\w+)"\s*:\s*"[^"]+"' -g '**/package.json' -g '!**/node_modules/**' .
rg -n --no-heading --pcre2 '"node_modules/(?:bullmq|bull|@nestjs/schedule|cron|node-cron|agenda|pg-boss)":\s*\{|^\s*["\x27]?/?(?:bullmq|bull|@nestjs/bullmq|@nestjs/schedule|cron|node-cron|agenda|pg-boss)@\d[\w.-]*' -g '**/{package-lock.json,pnpm-lock.yaml,yarn.lock}' -g '!**/node_modules/**' .   # exact: pnpm 9 keys are indented and single-quoted; package-lock prints the key line, read its version below it
rg -n --no-heading -i --pcre2 '^\s*["\x27]?(celery|apscheduler|rq|dramatiq|huey|arq|django-q2?|django-celery-beat|fastapi|temporalio)\b\s*[=<>~!^]|gem\s+["\x27](?:sidekiq|sidekiq-cron|good_job|solid_queue|resque|delayed_job|whenever|rails)["\x27]|"laravel/(?:framework|horizon)"\s*:|github\.com/(?:robfig/cron/v3|go-co-op/gocron\S*|hibiken/asynq|riverqueue/river)\s+v|go\.temporal\.io/sdk\s+v|spring-boot-starter-quartz|<artifactId>quartz</artifactId>|<PackageReference Include="(?:Hangfire|Quartz)[\w.]*"' -g '**/{pyproject.toml,requirements*.txt,Pipfile,Gemfile,composer.json,go.mod,pom.xml,build.gradle*,*.csproj}' -g '!**/node_modules/**' .
# F2 the zone a zone-less schedule runs in (process TZ, framework zone settings) and the Spring virtual-thread switch (§4, §6)
rg -n --no-heading --pcre2 '^\s*ENV\s+TZ[\s=]|^\s*-?\s*TZ\s*[:=]|name:\s*["\x27]?TZ["\x27]?\s*$|-Duser\.timezone=|process\.env\.TZ\s*=|^\s*TIME_ZONE\s*=|^\s*(?:CELERY_)?(?:timezone|TIMEZONE|CELERY_TIMEZONE)\s*=|\benable_utc\s*=|\bconf\.timezone\s*=|["\x27]timezone["\x27]\s*=>|\bschedule_timezone\b|spring\.threads\.virtual\.enabled|^\s*virtual:\s*$' -g '**/{Dockerfile*,*.dockerfile,*.yaml,*.yml,.env*,*.env,*.properties,settings*.py,celery*.py,celeryconfig.py,config/app.php}' "${X[@]}" .
# 0 THE INVENTORY — schedule entries, processors, producers, guards. Every § reads it first (P5: a base processor or scheduler wrapper is one row)
SCHED='@(?:Cron|Interval|Timeout)\s*\(|\bnew\s+CronJob\s*\(|\bCronJob\.from\s*\(|\b\w+\.schedule\s*\(\s*["\x27\x60][\d*/,?LW# -]+["\x27\x60]|\bscheduleJob\s*\(|\.add_job\s*\(|@\w+\.scheduled_job\s*\(|\bbeat_schedule\b|\bCELERYBEAT_SCHEDULE\b|\bSchedule::(?:command|job|call|exec)\s*\(|\$schedule->(?:command|job|call|exec)\s*\(|@Scheduled\s*\(|\.AddFunc\s*\(|\.AddJob\s*\(|\bRecurringJob\.AddOrUpdate\b|\bupsertJobScheduler\s*\(|\brepeat\s*:\s*\{'
PROC='@Processor\s*\(|\bextends\s+WorkerHost\b|\bnew\s+Worker\s*\(|@(?:shared_task|job)\b|@\w+\.(?:task|actor)\b|<\s*(?:ApplicationJob|ActiveJob::Base)\b|include\s+Sidekiq::(?:Job|Worker)\b|implements\s+ShouldQueue\b|implements\s+(?:org\.quartz\.)?Job\b|extends\s+QuartzJobBean\b|\basynq\.NewServeMux\b'
PROD='\b\w*(?:[Qq]ueue|[Pp]roducer|[Jj]obs|dlq)\w*\s*\.\s*(?:add|addBulk|enqueue\w*)\s*\(|\.(?:delay|apply_async|send_task|enqueue_call)\s*\(|\.perform_(?:later|async|in|at)\b|\b[A-Z]\w+::dispatch(?:Sync|AfterResponse)?\s*\(|\bdispatch\s*\(\s*new\s+\w+|BackgroundJob\.(?:Enqueue|Schedule)\b|\bclient\.Enqueue\s*\('
GUARD='\b(?:withLeaderLock|underLease|withLock|acquireLock|tryLock|tryAcquire|[Rr]edlock|pg_try_advisory(?:_xact)?_lock|pg_advisory(?:_xact)?_lock|SchedulerLock|withoutOverlapping|onOneServer|DisallowConcurrentExecution|SkipIfStillRunning|DelayIfStillRunning)\b|\bSKIP\s+LOCKED\b|(?i:\bon\s+conflict\b[^\n]*\bdo\s+nothing\b)|["\x27]NX["\x27]|\bthis\.(?:is)?(?:[Rr]unning|[Bb]usy|[Ii]nFlight|[Ll]ocked)\b|\bself\.(?:is_)?(?:running|busy|locked)\b'
rg -l --null --pcre2 "$SCHED" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" > "$SCAN/sched"
rg -l --null --pcre2 "$PROC" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" > "$SCAN/proc"
rg -l --null --pcre2 "$PROD" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" > "$SCAN/prod"
xargs -0 -r rg -l --pcre2 "$GUARD" < "$SCAN/sched" | sort > "$SCAN/guarded"
n() { tr -cd '\0' < "$1" | wc -c | tr -d ' '; }
echo "0 schedule files: $(n "$SCAN/sched") (guarded: $(wc -l < "$SCAN/guarded" | tr -d ' ')) · processor files: $(n "$SCAN/proc") · producer files: $(n "$SCAN/prod")"
echo "0 schedule entries: $(xargs -0 -r rg -c --no-heading --pcre2 "$SCHED" < "$SCAN/sched" | awk -F: '{s+=$NF} END {print s+0}') · processors: $(xargs -0 -r rg -c --no-heading --pcre2 "$PROC" < "$SCAN/proc" | awk -F: '{s+=$NF} END {print s+0}') · producer calls: $(xargs -0 -r rg -c --no-heading --pcre2 "$PROD" < "$SCAN/prod" | awk -F: '{s+=$NF} END {print s+0}')"
rg -n --no-heading --pcre2 'class\s+\w+\s+extends\s+(?!WorkerHost\b)\w*(?:WorkerHost|Processor|Job|Worker)\b|\bfunction\s+\w*(?:[Ll]ease|[Ll]eader|[Ll]ock)\w*\s*\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | head -20   # base processors and lock helpers (P5)
# 1 the payload carries a model: pickle (1a); an identifier, not an id or a literal, handed to a producer (1b, read whether it is an entity); Quartz JobDataMap (1c)
rg -n --no-heading --pcre2 '\btask_serializer\s*=\s*["\x27]pickle|\baccept_content\s*=[^\n]*pickle|CELERY_(?:TASK_)?SERIALIZER\s*=\s*["\x27]pickle|\bserializer\s*=\s*["\x27]pickle' -g '*.py' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
xargs -0 -r rg -n --no-heading --pcre2 '(?:\.(?:delay|perform_later|perform_async)\s*\(|\.apply_async\s*\(\s*[\[(]|\b\w*(?:[Qq]ueue|[Pp]roducer|[Jj]obs)\w*\s*\.\s*(?:add|enqueue\w*)\s*\(\s*(?:["\x27\x60][^"\x27\x60]+["\x27\x60]|[\w.]+)\s*,|\bdispatch\s*\(\s*new\s+\w+\s*\(|::dispatch\s*\()\s*(?:this\.|self\.|@)?(?![\w.]*(?:_id|_ids|_pk|Id|Ids|ID|Key|_key|uuid|Uuid|\.id|\.pk|\.uuid|\.key)\b)(?!(?:true|false|null|None|nil|undefined)\b)[a-z_][\w.]*\s*[,)\]]' < "$SCAN/prod" | "${NC[@]}"
rg -n --no-heading --pcre2 '\bJobDataMap\b[^\n]*\.put\s*\(|\.usingJobData\s*\(\s*["\x27]\w+["\x27]\s*,\s*(?!["\x27\d])[a-z]\w*\s*\)' -g '*.{java,kt}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 2 a record deleted between enqueue and perform: Rails jobs and the base class without discard_on (2a); Laravel SerializesModels without $deleteWhenMissingModels (2b);
#   throw-on-missing loads inside processor files (2c — a not-found branch, a discard or a typed non-retryable error clears the row on read)
echo "2a rails jobs: $(rg -l --pcre2 '<\s*(?:ApplicationJob|ActiveJob::Base)\b' -g '*.rb' "${X[@]}" "${ROOTS[@]}" | wc -l | tr -d ' ') · with discard_on/retry_on DeserializationError: $(rg -l --pcre2 '(?:discard_on|retry_on|rescue_from)\s*\(?\s*ActiveJob::DeserializationError' -g '*.rb' "${X[@]}" "${ROOTS[@]}" | wc -l | tr -d ' ') (a hit in application_job.rb covers every job)"
rg -l --null --pcre2 '\bSerializesModels\b' -g '*.php' "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg --files-without-match --pcre2 '\$deleteWhenMissingModels\s*=\s*true|#\[DeleteWhenMissingModels\]' | sed 's/^/2b SerializesModels, no deleteWhenMissingModels: /'
xargs -0 -r rg -n --no-heading --pcre2 '\.(?:findOneOrFail|findOrFail|findOneByOrFail|findUniqueOrThrow|findFirstOrThrow|firstOrFail|getReferenceById|orElseThrow)\s*\(|::findOrFail\s*\(|\.objects\.get\s*\(|\b\w+\.find\s*\(\s*\w*_?id\b|\.(?:one|scalar_one)\s*\(\s*\)' < "$SCAN/proc" | "${NC[@]}"
# 3 payload or signature drift across deploys — 3w whole repo: job.data reads no literal producer payload of the same queue sets; Celery tasks whose required
#   positional args outnumber what a .delay / apply_async / send_task caller passes. Candidates — V351 settles them. Then the diff lane: changed signatures and job.data reads
if command -v python3 >/dev/null 2>&1; then python3 -I - "$SCAN/proc" "$SCAN/prod" <<'PY'
import re, sys
def L(p): return [f for f in open(p, 'rb').read().decode('utf-8', 'replace').split('\0') if f]
def R(f):
    try: return open(f, encoding='utf-8', errors='replace').read()
    except OSError: return ''
def N(s, i): return s.count('\n', 0, i) + 1
def A(s, i):   # top-level arguments of the call whose '(' ends at i
    d, q, out, cur, j = 0, None, [], i, i
    while j < len(s):
        c = s[j]
        if q:
            if c == '\\': j += 1
            elif c == q: q = None
        elif c in '"\'`': q = c
        elif c in '([{': d += 1
        elif c in ')]}':
            if d == 0: return out + [s[cur:j]]
            d -= 1
        elif c == ',' and d == 0: out.append(s[cur:j]); cur = j + 1
        j += 1
    return out
proc, prod = L(sys.argv[1]), L(sys.argv[2]); JS = ('.ts', '.mts', '.cts', '.js', '.mjs', '.cjs')
reads, sets, opened = {}, {}, set()
for f in proc:
    s = R(f) if f.endswith(JS) else ''
    qs = {a or b for a, b in re.findall(r'@Processor\(\s*["\'`]([^"\'`]+)|\bnew\s+Worker\s*(?:<[^>]*>)?\(\s*["\'`]([^"\'`]+)', s)}
    if len(qs) != 1: continue
    q = qs.pop()
    for m in re.finditer(r'\bjob\.data\??\.(\w+)(?!\s*(?:\?\?|\|\|))', s): reads.setdefault(q, []).append((f, N(s, m.start()), m.group(1)))
    for m in re.finditer(r'\{([^{}]*)\}\s*=\s*job\.data\b', s):
        for k in m.group(1).split(','):
            k = re.match(r'\s*(\w+)\s*(:[^=]*)?$', k)
            if k: reads.setdefault(q, []).append((f, N(s, m.start()), k.group(1)))
for f in prod:
    s = R(f) if f.endswith(JS) else ''
    v = {m.group(2): m.group(1) for m in re.finditer(r'@InjectQueue\(\s*["\'`]([^"\'`]+)["\'`]\s*\)\s*(?:(?:private|public|protected|readonly)\s+)*(\w+)', s)}
    v.update({m.group(1): m.group(2) for m in re.finditer(r'\b(?:const|let|var)\s+(\w+)\s*=\s*new\s+Queue\s*(?:<[^>]*>)?\(\s*["\'`]([^"\'`]+)', s)})
    for m in re.finditer(r'\b(\w+)\s*\.\s*(add|addBulk)\s*\(', s):
        q = v.get(m.group(1))
        if not q: continue
        a = A(s, m.end()); p = a[1].strip() if len(a) > 1 else ''
        items = A(p[1:-1] + ')', 0) if m.group(2) == 'add' and p.startswith('{') and p.endswith('}') else None
        keys = [re.match(r'\s*["\']?(\w+)["\']?\s*(?::|$)', x) for x in items or [] if x.strip()]
        if items is None or not all(keys): opened.add(q); continue
        sets.setdefault(q, []).append((f, N(s, m.start()), {k.group(1) for k in keys}))
cmp_ = skip = 0
for q in sorted(reads):
    if q in opened or q not in sets: skip += 1; continue
    cmp_ += 1; have = set().union(*[k for _, _, k in sets[q]])
    for f, n, k in reads[q]:
        if k not in have: print(f"3w {f}:{n} job.data.{k} — no producer of '{q}' sets it (" + "; ".join(f"{pf}:{pn} sets {', '.join(sorted(pk))}" for pf, pn, pk in sets[q]) + ")")
tasks = {}
for f in proc:
    s = R(f) if f.endswith('.py') else ''
    for m in re.finditer(r'^[ \t]*@(?:shared_task|\w+\.task)\b(\((?:[^()]|\([^()]*\))*\))?[^\n]*\n(?:[ \t]*@[^\n]*\n)*[ \t]*(?:async\s+)?def\s+(\w+)\s*\(', s, re.M):
        req, ps = [], A(s, m.end())
        for i, p in enumerate(x.strip() for x in ps):
            if p.startswith('*'): break
            if not p or p == '/' or (i == 0 and re.search(r'\bbind\s*=\s*True', m.group(1) or '')) or re.search(r'(?<![=<>!])=(?!=)', p): continue
            req.append(re.match(r'\w+', p).group(0))
        tasks[m.group(2)] = (f, N(s, m.start(2)), req)
calls = 0
for f in prod:
    s = R(f) if f.endswith('.py') else ''
    for m in re.finditer(r'\b(\w+)\.(delay|apply_async)\s*\(|\bsend_task\s*\(\s*["\'](?:[\w.]*\.)?(\w+)["\']\s*,?', s):
        name = m.group(1) or m.group(3); t = tasks.get(name)
        if not t: continue
        a = [x.strip() for x in A(s, m.end()) if x.strip()]; kw = {x.split('=', 1)[0].strip(): x.split('=', 1)[1].strip() for x in a if re.match(r'\w+\s*=(?!=)', x)}
        if m.group(2) == 'delay': pos, ks = [x for x in a if not re.match(r'\w+\s*=(?!=)', x)], set(kw)
        else:
            lit = kw.get('args', a[0] if a and not re.match(r'\w+\s*=(?!=)', a[0]) else '()')
            if not re.match(r'^[\[(].*[\])]$', lit, re.S): continue
            pos = [x for x in A(lit[1:-1] + ')', 0) if x.strip()]
            ks = set(re.findall(r'["\'](\w+)["\']\s*:', kw.get('kwargs', '')))
        if any(x.startswith('*') for x in pos): continue
        calls += 1; miss = [r for r in t[2][len(pos):] if r not in ks]
        if miss: print(f"3w {t[0]}:{t[1]} {name}() requires {len(t[2])} ({', '.join(t[2])}) — {f}:{N(s, m.start())} passes {len(pos)}: missing {', '.join(miss)}")
print(f"3w whole-repo lane: {cmp_} queues compared (job.data reads vs literal producer payloads), {skip} skipped (no literal producer in ROOTS, or a spread / non-literal / addBulk payload: read) · {len(tasks)} tasks, {calls} callers checked")
PY
else echo "3w NOT-RUN (python3 absent): read each processor's job.data reads against its producers"; fi
if [ -n "$BASE" ]; then
  git diff --name-only "$BASE"...HEAD -- "${ROOTS[@]}" | sed 's|^\./||' | sort -u > "$SCAN/changed"
  cat "$SCAN/proc" "$SCAN/prod" | tr '\0' '\n' | sed 's|^\./||' | sort -u > "$SCAN/jobfiles"
  comm -12 "$SCAN/changed" "$SCAN/jobfiles" | while IFS= read -r f; do
    git diff -U0 "$BASE"...HEAD -- "$f" | rg -n --no-heading --pcre2 '^[-+](?![-+])[^\n]*(?:\bdef\s+\w+\s*\(|\bperform\s*\(|\bhandle\s*\(|\bjob\.data\b|\b(?:interface|type)\s+\w*(?:Job|Payload|Data|Message)\w*\b|\bpublic\s+function\s+__construct\s*\(|\bdata\s+class\b|\brecord\s+\w+\s*\(|\bversion\s*[:=])' | sed "s|^|3 $f |"
  done
else echo "3 diff lane N/A (run with BASE=<base-branch>; 3w above is the whole-repo lane)"; fi
# 4 a schedule that overlaps itself on one process: Nest @Cron / npm cron without waitForCompletion (4a) and @Interval = setInterval (4b);
#   node-cron without noOverlap (4c); Laravel without withoutOverlapping (4d); Spring fixedRate under virtual threads (4e); Quartz (4f); robfig (4g);
#   APScheduler max_instances raised (4h); BullMQ schedulers (4i, read). Each hit is tagged with the file's guard words (a lock or flag clears it on read)
tag() { while IFS= read -r l; do f=${l%%:*}; f=${f#./}; if grep -qxF "./$f" "$SCAN/guarded" || grep -qxF "$f" "$SCAN/guarded"; then echo "$l   [guard in file: read]"; else echo "$l"; fi; done; }
U='(?:[^()]|\((?:[^()]|\((?:[^()]|\([^()]*\))*\))*\))'; B="$U*"   # one balanced unit; a lookahead (?:(?!word)$U)* proves the call never says <word>
rg -U -n --no-heading --pcre2 "@Cron\s*\((?=(?:(?!waitForCompletion)$U)*\))|\bCronJob\.from\s*\((?=(?:(?!waitForCompletion)$U)*\))|\bnew\s+CronJob\s*\((?=(?:(?!waitForCompletion)$U)*\))" -g '*.{ts,mts,cts,js,mjs,cjs}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | tag | sed 's/^/4a /'
rg -n --no-heading --pcre2 '@Interval\s*\(' -g '*.{ts,mts,cts,js,mjs,cjs}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | tag | sed 's/^/4b /'
rg -U -n --no-heading --pcre2 "\b\w+\.schedule\s*\(\s*[\"'\x60][\d*/,?LW# -]+[\"'\x60](?=(?:(?!noOverlap)$U)*\))" -g '*.{ts,mts,cts,js,mjs,cjs}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | tag | sed 's/^/4c /'
rg -U -n --no-heading --pcre2 '(?:\bSchedule::|\$schedule->)(?:command|job|call|exec)\s*\((?=(?:(?!withoutOverlapping)[^;])*;)' -g '*.php' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | tag | sed 's/^/4d /'
rg -q --pcre2 'spring\.threads\.virtual\.enabled\s*[=:]\s*true|virtual:\s*\n\s*enabled:\s*true' -U -g '**/application*.{properties,yml,yaml}' "${X[@]}" . && rg -n --no-heading --pcre2 '@Scheduled\s*\([^)]*\bfixedRate' -g '*.{java,kt}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | sed 's/^/4e virtual threads on: /'
rg -l --null --pcre2 'implements\s+(?:org\.quartz\.)?Job\b|extends\s+QuartzJobBean\b' -g '*.{java,kt}' "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg --files-without-match --pcre2 '@DisallowConcurrentExecution\b' | sed 's/^/4f quartz job, no @DisallowConcurrentExecution: /'
rg -l --null --pcre2 '\bcron\.New\s*\(' -g '*.go' "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg --files-without-match --pcre2 '\b(?:SkipIfStillRunning|DelayIfStillRunning)\b' | sed 's/^/4g robfig cron, no SkipIfStillRunning: /'
rg -n --no-heading --pcre2 '\bmax_instances\s*[=:]\s*(?:[2-9]|\d{2,})\b' -g '*.py' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | sed 's/^/4h /'
rg -n --no-heading --pcre2 '\bupsertJobScheduler\s*\(|\brepeat\s*:\s*\{' -g '*.{ts,mts,cts,js,mjs,cjs}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | sed 's/^/4i /'
# 5 misfire / catch-up: must-run schedule entries by handler name (5a) or path (5b) — in-process schedulers never catch up (5b and 7g match the file NAME, never a directory); APScheduler entries without
#   misfire_grace_time or coalesce (5c, scheduler-level job_defaults is the control); Quartz triggers vs misfire instructions (5d)
MUST='\w*(?i:bill|invoic|settl|payout|charge|renew|subscri|month|statement|ledger|accru|interest|reconcil|payroll|dunning|rollup|snapshot|close|cutoff|usage)\w*'
rg -U -n --no-heading --pcre2 "@(?:Cron|Scheduled|Interval)\s*\((?=$B\)[^\n]*\n(?:[ \t]*(?:@[^\n]*|//[^\n]*)?\n){0,4}?[ \t]*(?:(?:public|private|protected|async|static|void|def|fun)\s+)*$MUST\s*\()" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | sed 's/^/5a /'
tr '\0' '\n' < "$SCAN/sched" | rg --pcre2 "(?i)(?:^|/)[^/]*(?:bill|invoic|settl|payout|charge|renew|subscri|month|statement|ledger|accru|interest|reconcil|payroll|dunning|rollup|snapshot|cutoff|usage)[^/]*$" | sed 's/^/5b /'
rg -U -n --no-heading --pcre2 "\.add_job\s*\((?=(?:(?!misfire_grace_time|coalesce)$U)*\))|@\w+\.scheduled_job\s*\((?=(?:(?!misfire_grace_time|coalesce)$U)*\))" -g '*.py' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | sed 's/^/5c /'
echo "5c apscheduler job_defaults: $(rg -l --pcre2 '\bjob_defaults\b' -g '*.py' "${X[@]}" "${ROOTS[@]}" | wc -l | tr -d ' ') · 5d quartz triggers: $(rg -c --no-heading --pcre2 '\bnewTrigger\s*\(|\bTriggerBuilder\b' -g '*.{java,kt}' "${X[@]}" "${ROOTS[@]}" | awk -F: '{s+=$NF} END {print s+0}') misfire instructions: $(rg -c --no-heading --pcre2 'withMisfireHandlingInstruction\w*|MISFIRE_INSTRUCTION_\w+' -g '*.{java,kt}' "${X[@]}" "${ROOTS[@]}" | awk -F: '{s+=$NF} END {print s+0}')"
# 6 schedule zone: entries with no zone (6a Nest/npm cron, 6b node-cron, 6c Spring, 6d Laravel, 6e robfig, 6f APScheduler); 6g fire hours in 00:00–03:59
rg -U -n --no-heading --pcre2 "@Cron\s*\((?=(?:(?!timeZone|utcOffset)$U)*\))|\bCronJob\.from\s*\((?=(?:(?!timeZone|utcOffset)$U)*\))" -g '*.{ts,mts,cts,js,mjs,cjs}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | tag | sed 's/^/6a /'
rg -U -n --no-heading --pcre2 "\b\w+\.schedule\s*\(\s*[\"'\x60][\d*/,?LW# -]+[\"'\x60](?=(?:(?!timezone)$U)*\))" -g '*.{ts,mts,cts,js,mjs,cjs}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | sed 's/^/6b /'
rg -n --no-heading --pcre2 '@Scheduled\s*\((?=[^)]*\bcron\s*=)(?![^)]*\bzone\s*=)' -g '*.{java,kt}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | sed 's/^/6c /'
rg -q --pcre2 '\bschedule_timezone\b' -g '**/config/app.php' "${X[@]}" . || rg -U -n --no-heading --pcre2 '(?:\bSchedule::|\$schedule->)(?:command|job|call|exec)\s*\((?=(?:(?!->timezone\s*\()[^;])*;)' -g '*.php' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | sed 's/^/6d /'
rg -l --null --pcre2 '\bcron\.New\s*\(' -g '*.go' "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg --files-without-match --null --pcre2 '\bWithLocation\s*\(' | xargs -0 -r rg -H -n --no-heading --pcre2 '\.AddFunc\s*\(\s*"(?!(?:CRON_)?TZ=)' | sed 's/^/6e /'
rg -U -n --no-heading --pcre2 "\.add_job\s*\([^)]*[\"']cron[\"'](?=(?:(?!timezone)$U)*\))|\bCronTrigger\s*\((?=(?:(?!timezone)$U)*\))" -g '*.py' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | sed 's/^/6f /'
{ rg -n --no-heading --pcre2 "[\"'\x60](?:CRON_)?(?:TZ=\S+\s+)?(?:[\d*/,?LW#-]+\s+){4,5}[\d*/,?LW#A-Za-z-]+[\"'\x60]" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
  rg -n --no-heading --pcre2 '^\s*schedule:\s*["\x27]?(?:[\d*/,?-]+\s+){4}[\d*/,?A-Za-z-]+' -g '*.{yaml,yml}' "${X[@]}" .; } |
  awk '/(timeZone|[^a-z]zone|timezone|TZ=)[^,)]*(UTC|Etc\/UTC|GMT)/ { next }
    { if (!match($0, /[\042\047\140 ](CRON_)?(TZ=[^ ]+ +)?[0-9*\/,?LW#-]+( +[0-9*\/,?LW#A-Za-z-]+){4,5}/)) next
      e=substr($0, RSTART+1, RLENGTH-1); n=split(e, f, / +/); o=(f[1] ~ /TZ=/) ? 1 : 0; h=((n-o)==6 ? f[o+3] : f[o+2]); m=split(h, t, ","); hit=0
      for (i=1;i<=m;i++) { split(t[i], r, "-"); if (r[1] ~ /^0?[0-3]$/) hit=1 }
      if (hit && h !~ /\*/) print "6g hour " h ": " $0 }'
rg -n --no-heading --pcre2 'CronExpression\.EVERY_DAY_AT_(?:MIDNIGHT|1AM|2AM|3AM)\b|CronExpression\.EVERY_(?:WEEK|1ST_DAY_OF_MONTH_AT_MIDNIGHT|QUARTER|6_MONTHS|YEAR)\b|->(?:dailyAt|at|twiceDaily|monthlyOn|weeklyOn)\s*\([^)]*["\x27]0?[0-3]:\d\d["\x27]|\b(?:crontab|add_job|CronTrigger)\s*\([^)]*\bhour\s*=\s*["\x27]?0?[0-3]\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | sed 's/^/6g /'
# 7 job result or failure discarded: BullMQ workers with no failed listener (7a); removeOnFail (7b → messaging-scan §3); Celery ignore_result + a result read (7c);
#   Spring @Async void (7d); FastAPI BackgroundTasks (7e); Laravel jobs with no failed() (7f); schedule files that record no failure (7g); status rows never set failed (7h)
rg -l --null --pcre2 '\bnew\s+Worker\s*\(|@Processor\s*\(' -g '*.{ts,mts,cts,js,mjs,cjs}' "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg --files-without-match --pcre2 '\.on\s*\(\s*["\x27]failed["\x27]|@OnWorkerEvent\s*\(\s*["\x27]failed["\x27]|\bQueueEvents\b' | sed 's/^/7a no failed listener: /'
rg -n --no-heading --pcre2 '\bremoveOnFail\s*:\s*(?:true|0)\b' -g '*.{ts,mts,cts,js,mjs,cjs}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | sed 's/^/7b /'
echo "7c ignore_result=True: $(rg -c --no-heading --pcre2 '\bignore_result\s*=\s*True\b|\btask_ignore_result\s*=\s*True\b' -g '*.py' "${X[@]}" "${ROOTS[@]}" | awk -F: '{s+=$NF} END {print s+0}') · result reads: $(rg -c --no-heading --pcre2 '\bAsyncResult\s*\(|\.get\s*\(\s*timeout\s*=' -g '*.py' "${X[@]}" "${ROOTS[@]}" | awk -F: '{s+=$NF} END {print s+0}')"
rg -U -n --no-heading --pcre2 '@Async\b(?=[^\n]*\n(?:[ \t]*@[^\n]*\n){0,3}[ \t]*(?:public|protected|private)?\s*void\b)' -g '*.{java,kt}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | sed 's/^/7d /'
rg -n --no-heading --pcre2 '\b\w+\.add_task\s*\(' -g '*.py' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | sed 's/^/7e /'
rg -l --null --pcre2 'implements\s+ShouldQueue\b' -g '*.php' "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg --files-without-match --pcre2 'function\s+failed\s*\(' | sed 's/^/7f no failed(): /'
tr '\0' '\n' < "$SCAN/sched" | rg --pcre2 "(?i)(?:^|/)[^/]*(?:bill|invoic|settl|payout|charge|renew|subscri|month|statement|ledger|accru|interest|reconcil|payroll|dunning|rollup|snapshot|cutoff|usage)[^/]*$" | tr '\n' '\0' | xargs -0 -r rg --files-without-match --pcre2 '(?i)record\w*fail|\bfailed\b|failure|\.inc\s*\(|capture(?:Exception|IfExhausted)|status\s*[:=]\s*["\x27]failed|\brun(?:Log|Record|History)\b' | sed 's/^/7g must-run schedule file (5b), no failure record: /'
xargs -0 -r rg -l --null --pcre2 "status\s*[:=]\s*[\"'](?:running|processing|in_progress|started)[\"']|\bstate\s*[:=]\s*[\"'](?:running|processing)[\"']" < "$SCAN/proc" | xargs -0 -r rg --files-without-match --pcre2 "[\"']failed[\"']|\bFAILED\b|\.fail\s*\(" | sed 's/^/7h running status, no failed write: /'
# R routed rows — counted here, graded by their owners (§ Boundaries)
TXO='\.transaction(?:al)?\s*\(|\btransaction\.atomic\b|\bDB::transaction\s*\(|\.transaction\s+do\b|\$transaction\s*\(|@Transactional\b|\bBeginTx\s*\(|\btx\.run\s*\('
echo "R → database transaction-scan §1: $(xargs -0 -r rg -l --pcre2 "$TXO" < "$SCAN/prod" | wc -l | tr -d ' ') files hold a transaction opener and a producer call"
echo "R → distributed-systems messaging-scan §2/§3/§6: $(n "$SCAN/proc") processor files (consumer idempotency, poison, lock vs run time) · §3 removeOnFail: $(rg -c --no-heading --pcre2 '\bremoveOnFail\s*:\s*(?:true|0)\b' -g '*.{ts,js,mjs,cjs}' "${X[@]}" "${ROOTS[@]}" | awk -F: '{s+=$NF} END {print s+0}')"
echo "R → distributed-systems retry-deadline-scan §1/§6: $(rg -c --no-heading --pcre2 '\battempts\s*:|\bautoretry_for\b|\bretry_on\b|\bsidekiq_options\b[^\n]*\bretry\b|\bmax_retries\s*=|\$tries\b|\bbackoff\s*:' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | awk -F: '{s+=$NF} END {print s+0}') retry settings"
echo "R → distributed-systems coordination-scan §1–§4: $(wc -l < "$SCAN/guarded" | tr -d ' ') guarded schedule files (lock mechanics) · §11: the 6a/6g rows tagged [guard in file] above (a coordinated schedule's DST day)"
echo "R → distributed-systems dual-write-scan §1: $(xargs -0 -r rg -l --pcre2 '\bon_commit\s*\(|\bafterTransactionCommit\b|\bafter_(?:create_|update_)?commit\b|->afterCommit\s*\(|@TransactionalEventListener\b' < "$SCAN/prod" | wc -l | tr -d ' ') producer files enqueue after a commit · workflow-scan §2: $(rg -l --pcre2 '@temporalio/workflow|go\.temporal\.io/sdk/workflow|from\s+temporalio\s+import\s+workflow' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | wc -l | tr -d ' ') workflow files"
echo "R → performance request-path-scan §20: $(( $(n "$SCAN/sched") - $(wc -l < "$SCAN/guarded" | tr -d ' ') )) unguarded schedule files (every replica runs them) · §22: $(rg -c --no-heading --pcre2 '\b\w+\.add_task\s*\(|@Async\b|^\s*void\s+this\.\w+\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | awk -F: '{s+=$NF} END {print s+0}') in-process work sites"
echo "R → infrastructure k8s-wiring-scan §5: $(rg -l --pcre2 '^\s*kind:\s*CronJob\b' -g '*.{yaml,yml}' "${X[@]}" . | wc -l | tr -d ' ') CronJob manifests (timeZone, concurrencyPolicy, startingDeadlineSeconds)"
```

Three blind spots are structural; work around them rather than trust a quiet grep. **A guard one call away** — a lease taken by a helper the handler calls (`this.underLease(…)` defined in a base class, a claim in the use case) is not in the file: the `[guard in file]` tag is a hint, and an untagged row is cleared only by reading one hop down. **Options built elsewhere** — a schedule whose options object or expression is a constant (`ROLLUP_CRON`, a shared `CRON_OPTS`) is matched where the decorator is; 6g sees the constant's line, and the zone sits at the decorator. **Schedules registered at runtime** (`schedulerRegistry.addCronJob`, a cron string from the database, `upsertJobScheduler` per tenant) — read the registration and quote it.

### Measured (2026-10-14)

- **Real repo, read-only, full tree** (a NestJS 11 monorepo on Fastify with MikroORM; `ROOTS=(apps/api/src)`, the server code only — an earlier run on `ROOTS=(apps/api)` over an older partial copy also swept the app's maintenance scripts: 21 guarded files, 4a 42, 6a 41, 103 retry settings and 34 unguarded files, against the numbers below; the pnpm lockfile pins BullMQ 6.3.4, `@nestjs/bullmq` 11.0.5, `@nestjs/schedule` 6.1.3 on `cron` 4.4.0 — F1's lockfile line, added after the first run printed ranges only, reads them, so §4's default is no longer `UNREAD`): about 1.8 s, 0 `rg` errors, 166 lines, 0 files written into the tree (re-run at the tree's current HEAD: every count below reproduced). F2: no `TZ` in the image, manifests or code → the process runs in UTC. Grep 0: **55 schedule files, 62 entries** (42 `@Cron`, 19 `@Interval`, 1 `@Timeout`), 18 files with a guard word; **8 processor files** (7 on one tenant base processor); 20 producer files behind one producer wrapper; the P5 listing names the base processor and the lock helpers (`lockKey`, `advisoryLockKey`). **§1 0** — every enqueue passes an object literal of ids; the wrapper forwards `data` (P5). **§2: 2c 0** direct throw-on-missing loads in processors; one read one hop down (the bulk-dispatch line) → a missing order throws the domain not-found error, which the use case settles as `failed` once with no retry → cleared; 6 processors `Live, unreviewed`. **§3 N/A** (whole-repo run). **§4: 4a 43 + 4b 19**; the eval's one-hop read found 60 of 62 entries under a lease or claim, and the 2 unguarded ones are process-local metrics samplers → B-R8 → **0 rows**. **§5: 5a 2, 5b 9 files** → storage billing posts every due-and-unposted charge by its ledger (catches up), the order rollup catches up on every 60 s tick, the usage rollup recomputes yesterday and today (one missed night caught up, two not → Hardening), **the performance-snapshot job closes one period per fire time and nothing backfills a missed one** → `[report-flagged]` low. **§6: 6a 42** zone-less entries, **6g 5** expressions in hours 1–3 + 3 `EVERY_DAY_AT_3AM` → all in a UTC process (`precedents/distributed.md` § 35, B-R9) → 0 rows except one: the snapshot job's doc comment says its three `@Cron`s fire at 03:20/03:40/03:50 "workspace time" (the workspace's own zone, east of UTC), while zone-less in a UTC process they fire at those times UTC, and the period each closes is a process-local (UTC) day, not the workspace's business day the finance periods use → `[report-flagged]` low; 6g also lists a backup CronJob at 02:15 → infrastructure `k8s-wiring-scan` §5 (which refuted it as a backup time with no business meaning). **§7: 7a 0** (every processor declares a `failed` listener that dead-letters and settles its status row), 7b 0, **7g 1 → 0** (a retention prune whose file name says `billing`: it delegates to the shared leader-locked sweep helper, and a missed night is pruned the next), 7h 0. Routed: database §1 8 files (a DB-row export-jobs port enqueued in the same transaction — the outbox shape, database's to clear), messaging-scan 8 processor files, retry-deadline-scan 100 retry settings, coordination-scan 18 guarded files (its own run found the nine GET-then-DEL releases), dual-write-scan 1, performance §20 37 files with no guard word in the file (one hop: 2), infrastructure §5 2 manifests.
- **Fixtures** (`benchmarks/fixtures/*`, 18 roots; none seeds a JL class yet — the `backend-defects` fixture is a later build item): 0 `rg` errors on any root. `obs-defects`: a renewal charge `@Cron('0 2 * * *')` hits 4a, 5a, 5b, 6a, 6g and 7g — §5 holds as a candidate (its doc comment and `findDueToday()` charge what renews today, so a 02:00 with no worker up skips that day's renewals; the repository is not in the fixture, so the catch-up read is Unconfirmed), §4 does not (a daily run does not outlive its period), §6 is a UTC process, §7 holds (a throw leaves a log line; observability's `metric-hygiene-scan` §2 seeds the missing counter on the same line), and its 3 worker replicas are performance §20's; 7a lists the invoice processor, cleared on read (its `catch` increments an error counter and rethrows). `slow-marketplace`: an hourly reminder (§4/§5 not rows; performance §20's seed) and a nightly summary claimed by a unique insert — the fixture's own decoy, tagged `[guard in file]`. `infra-ops`, `quality-mix`: 6g lists Velero and CronJob schedules → infrastructure. Every other root prints only the F lines.
- **Research labs and paired samples**: lab B's `cron.mjs` hits 4a (the default job) and stays quiet on the `waitForCompletion: true` job, hits 4c on node-cron, and 6g lists its two New York DST expressions; lab B's FastAPI script hits 7e. A scratch sample set (Node, Python, Ruby, PHP, Java, Go, k8s) gave every POS line a hit and kept every NEG line quiet except by design: a positional `waitForCompletion` (4a, read), a load inside a `try/except DoesNotExist` (2c, read), and a file-level guard tag.
- **`backend-defects` fixture** (2026-10-14, after the fixture's IR-4 and IR-6). The new whole-repo **3w** lane prints the 2 static drift seeds: BD-JL-3a (`job.data.currency`, which no `settlement` producer sets) and BD-JL-3b (a dunning task needs 2 arguments; `apply_async(args=[inv.pk])` passes 1). It compared 1 queue, skipped 4 (a non-literal payload, or no producer in ROOTS) and checked 6 callers of 5 tasks. A paired sample kept every NEG quiet: a defaulted destructure, `?? default`, kwargs, `apply_async((a, b))`, a spread payload, `*args`. 5b and 7g now match file names only, so the two scheduler-named files no longer print because of the `billing/` directory (BD-DECOY-46). On the other 22 fixtures 3w prints its summary line only.

## The 3,000-hit path

JL is inventory-first: a project has a few dozen schedule entries and processors, and one wrapper decides most rows (P5). When the distributed-systems pack is installed, its `messaging-scan` F2 (`ds-inventory.py`) prints every BullMQ processor and producer with the options it resolves to — read it instead of re-deriving. Then: §4 and §6 grouped by guard helper (one read of `withLeaderLock` clears every entry that calls it first); §5 by must-run entry (a handful, each read whole); §7 by base processor; §1 by producer wrapper and its callers. A group may close with one cited reason when the reason is checked, not assumed. A partial review prints `Live, unreviewed (k groups / n hits)`, never `checked`.

## Scans for

| § | Class (research id) | Default severity | Oracle |
|---|---|---|---|
| 1 | the payload carries a model object (BJ-02) | high when the job writes the copy back or charges from it; medium for a stale read | V351 |
| 2 | record deleted between enqueue and perform (BJ-03, BF-RA-05) | medium; low when one alerting failure is the documented design | V351 |
| 3 | payload or signature drift across deploys (BJ-04) | high when the queue can hold jobs across a deploy (delays, retries, schedulers) | V351 |
| 4 | a schedule overlaps itself on one process (BJ-05, BF-SP-06, BF-LA-04 overlap half) | high with side effects; **blocker** on a money job (the `/backend-audit` floor) | V352 |
| 5 | misfire / catch-up policy unspecified (BJ-06) | medium; high for billing, settlement, payout, month-end | V352 |
| 6 | schedule zone implicit or DST-unsafe — one schedule's own zone (BJ-07, BF-SP-06 zone half) | medium; high for a financial cutoff | V352 |
| 7 | job result or failure discarded (BJ-08, BF-FA-05, BF-SP-07) | medium; high on a money path | V353 |

Every lane row that rests on a library default also carries V357: the oracle ran on the installed version and the finding states it.

### 1. The payload carries a model object

```
BAD:   app.conf.task_serializer = 'pickle'; render_invoice.delay(invoice)        # the worker save()s the enqueue-time copy over newer data
       await this.ordersQueue.add('ship', order)      // a class instance: methods, Decimal and Date do not survive JSON
       jobDataMap.put("order", order)                 // Quartz
GOOD:  render_invoice.delay(invoice.id) and a fresh load in the task · queue.add('ship', { orderId: order.id })
       a documented snapshot (an invoice rendered from enqueue-time values) that never writes back
```
**Read the code:** is the 1b identifier an entity or a value (an id, a DTO of ids, a deliberate snapshot)? Does the task write the object back (`save()`, a merge) or act on a field another writer can change between enqueue and run (a price, a status, an address)? A Rails GlobalID argument is re-fetched (fresh, but §2 applies); Laravel `SerializesModels` re-fetches by id and drops relation constraints [K docs]. **Finding when** the job acts on, or writes back, a value older than the row it names. **Proof:** V351 — enqueue at v1, update the row to v2, run: the output reflects v2 and v2 is not overwritten.

### 2. Record deleted between enqueue and perform

```
BAD:   class ReceiptJob < ApplicationJob; def perform(order) … end   # no discard_on: DeserializationError → retries → dead letter
       use SerializesModels;  (no $deleteWhenMissingModels)  ·  const o = await em.findOneOrFail(Order, { id: job.data.orderId })
GOOD:  discard_on ActiveJob::DeserializationError (in ApplicationJob) · public $deleteWhenMissingModels = true
       const o = await em.findOne(…); if (!o) { log.warn('order gone'); return; }   // or a typed non-retryable error settled once
```
**Read the code:** which loads can find nothing (2c, and one hop down in the use case the processor calls)? Does a missing row end as one discard with a log line, or as N retries and a dead-letter row — and is the thrown class one the processor treats as permanent (a domain not-found error settled `failed`) or one the queue retries (an ORM's own `NotFoundError`)? A job whose missing row must alert fails once by design. **Finding when** a deleted or soft-deleted row turns into retries, a dead letter, or a skipped cleanup branch. **Proof:** V351 — enqueue, delete the row, run: one discard, 0 retries, no dead-letter entry.

### 3. Payload or signature drift across deploys

```
BAD:   - def charge(order_id):            + def charge(order_id, currency):     # old payloads: TypeError: missing argument
       - interface ShipJob { orderId }     + interface ShipJob { orderId; carrierId }   // old jobs: job.data.carrierId undefined
GOOD:  + def charge(order_id, currency="USD") · a `version` field and a dispatcher for every version · drain, then deploy (enforced, B-R7)
```
Two drift shapes are static, so the **3w** lane prints them on every run, whole-repo included: a processor reading a `job.data` field that no literal payload sent to the same queue sets, and a Celery task whose required positional arguments outnumber what a `.delay` / `apply_async` / `send_task` caller passes. A 3w row is a candidate — a producer outside `ROOTS`, a wrapper, a spread or a guarded read (`?? default`) can clear it on read; the summary line counts the queues it could not compare. The diff lane (`BASE`) adds every changed signature and payload type. **Read the code:** can the queue hold a job across the deploy — a delay, a retry with backoff, a scheduler, a dead letter someone replays? Does the new code still read every old payload, and does the **old** code (still running during a rolling deploy) read the new one? Cross-service event schemas are `event-contract-scan`'s; Temporal histories are `workflow-scan` §2's. **Finding when** a payload produced by one side of the deploy fails or misreads on the other. **Proof:** V351 — cross-commit replay in both directions on the real queue.

### 4. A schedule overlaps itself on one process

```
BAD:   @Cron('0 */5 * * * *') async settle() { … }   // @nestjs/schedule: no waitForCompletion → a 7-minute run overlaps the next
       @Interval(2000) async drain() { … }   ·   cron.schedule('* * * * *', job)   ·   Schedule::job(new Settle)->everyMinute()
       @Scheduled(fixedRate = 1000) with spring.threads.virtual.enabled=true   ·   a Quartz Job without @DisallowConcurrentExecution
GOOD:  @Cron(expr, { waitForCompletion: true }) · if (this.running) return; this.running = true; try { … } finally { this.running = false }
       { noOverlap: true } · ->withoutOverlapping() · fixedDelay · cron.SkipIfStillRunning · a lease taken first (its mechanics: coordination-scan)
```
**Read the code:** can a run outlive its period — its data grows, it calls out, it has no deadline (B-R8: an idempotent, read-only, cheap job is not a row)? Does a guard run **first**, in the handler or one hop down, and does it cover the same process (a Redis `NX` lease does; a per-replica claim key does; a flag set after an `await` does not)? A lease whose TTL is shorter than the run is `coordination-scan` §4's. **Finding when** two runs of the same schedule execute concurrently on one process with side effects. **Proof:** V352 — the schedule at every 1 s with a 2.5 s body for 6 s on one process: maximum concurrency 1.

### 5. Misfire and catch-up policy unspecified

```
BAD:   @Cron('0 2 * * *') chargeRenewals() { due = findDueToday() … }   // in-process: no process at 02:00 → today's renewals never charged
       sched.add_job(settle_payouts, 'cron', hour=1)   # APScheduler misfire_grace_time=1 s: a paused scheduler skips the run
       a Quartz trigger with no misfire instruction (smart policy fires once now) · a CronJob with no startingDeadlineSeconds (→ infrastructure)
GOOD:  the run selects "due ≤ now and not yet done" by a ledger or watermark, so the next fire catches up
       misfire_grace_time=3600, coalesce=True · withMisfireHandlingInstruction…() chosen and written down
```
**Read the code:** is the job must-run (money, a period close, a report someone reconciles) or skippable (a cache warm, a sweep the next run repeats)? What happens to a fire time when no process is up — a deploy, a crash loop, a paused scheduler? In-process schedulers (`@nestjs/schedule`, npm `cron`, node-cron, `@Scheduled`) persist nothing: the answer is the job's own query. **Finding when** a must-run job can silently miss a period, or runs a backlog the business did not intend. **Proof:** V352 — stop the scheduler across 1 and N fire times on a fake clock, restart: the executions equal the documented policy.

### 6. Schedule zone implicit or DST-unsafe — one schedule's own zone

```
BAD:   @Cron('0 30 2 * * *')  with ENV TZ=Europe/Berlin   // 02:30 does not exist on spring-forward day and happens twice in October
       @Scheduled(cron = "0 0 0 * * *")   (JVM zone)  ·  Schedule::command('close')->dailyAt('00:30')   (no ->timezone())
       a zone-less cron whose comment says "03:20 on the workspace's clock" in a UTC process
GOOD:  UTC process and UTC schedule with a UTC meaning (B-R9) · { timeZone: 'Europe/Berlin' } at an hour outside the transition window
```
**Read the code:** what zone does the process run in (F2: `ENV TZ`, a manifest `TZ`, `-Duser.timezone`, Celery `timezone`; none → UTC)? What does the job **mean** — a UTC instant, or a local business time (a cutoff, "end of day", "the 1st of the month" in a market's zone)? In a DST zone, does a fire time fall in 00:00–03:59 (6g)? A schedule under a fleet lock or keyed on the local date is coordinated: print it `→ distributed-systems coordination-scan §11 (k)`. **Finding when** a schedule fires at a local time other than the one it means, or 0 or 2 times on a DST day. **Proof:** V352 — the library's own iterator over a year in the business zone: one run per business day at the intended local time.

### 7. Job result or failure discarded

```
BAD:   background_tasks.add_task(issue_refund, id); return {"ok": True}   # the task raises after the 200
       @Async public void sendInvoice(…)   ·   @shared_task(ignore_result=True) + AsyncResult(task_id).get()
       new Worker('payouts', fn) with no failed listener · an export row set 'running' that no error path sets 'failed'
       a scheduled method that throws: @nestjs/schedule logs one line and nothing else
GOOD:  a failed listener that dead-letters and settles the status row · a counter an alert reads · a failed() method · a durable queue
```
**Read the code:** when the job throws, what records it — a failed-jobs row, a dead-letter entry, a status row set `failed`, a counter? Does whoever waits on the result (a user polling an export, a caller reading `AsyncResult`) learn of the failure, or poll a `running` row forever? A base processor that declares the listener clears its subclasses (P5) only when the framework registers inherited listeners — read it. Telemetry-only jobs are not rows. **Finding when** a failing run leaves no record a person or an alert can see. **Proof:** V353 — make the job throw on the real queue: an observable failure record exists.

## Proof

The three oracles of `proof-oracles.md` § Backend, run on the project's **registered** processors and **its** scheduler library at the installed version — an eager queue, an in-process mock of the scheduler or a hand-built worker proves nothing (P4): **cross-commit replay** (V351: a payload from the previous commit consumed by the new code and the reverse; a row updated or deleted between enqueue and run), **the fire-time iterator plus a concurrency counter** (V352: a year of fire times in the business zone; every 1 s with a 2.5 s body for 6 s; downtime across 1 and N fire times on a fake clock) and **the failure record** (V353: the job throws, the record exists). The control: a read-only, idempotent, cheap job still runs on time (B-R8), a UTC schedule with a UTC meaning stays quiet (B-R9), a drained-by-runbook queue is not a §3 row (B-R7). An oracle that did not run is `NOT-RUN`, never PASS.

## Output

```
job-lifecycle-scan — lanes: @nestjs/schedule 6.1.3 on cron 4.4.0, bullmq 6.3.4, @nestjs/bullmq 11.0.5 (pnpm-lock.yaml)
Inventory: 62 schedule entries in 55 files (18 with a guard word) · 8 processor files, 7 on one tenant base processor · 20 producer files, 1 wrapper · process TZ: unset (UTC)
Tools: fire-time iterator NOT-RUN (no harness in this run) · concurrency counter NOT-RUN · cross-commit replay N/A (whole repo) · failure record NOT-RUN

Findings: 0 · Unconfirmed: 2

1. src/reports/period-snapshots.job.ts:45,51,57                                                      [report-flagged]  low
   §5 — each fire closes one period (yesterday, last week, last month) and nothing backfills a missed one: no process at 03:50 UTC
   on the 1st → that month's snapshot is never written. Fix: on each tick, close every period since the last stored snapshot. Settling: V352 downtime row.
2. same file, the three @Cron decorators                                                              [report-flagged]  low
   §6 — the doc comment says 03:20/03:40/03:50 "on the workspace's own clock" (UTC+3); zone-less in a UTC process they fire at
   those times UTC. Fix: { timeZone: '<the workspace zone>' }, or correct the comment. Settling: V352 iterator in the business zone.

Verification: 6 candidates read → 0 findings · 2 unconfirmed · 1 hardening (usage rollup: one missed night caught up, two not) · 3 refuted
  (self-verified: billing and order rollup catch up; a missing order settles once) · grouped: §4 62 entries (60 under a lease or claim one hop down; 2 samplers, B-R8), §6 42 zone-less (UTC, B-R9)

Class coverage:
  §1 model in payload          checked (0)
  §2 deleted record            checked (2c 0; 1 of 8 processor files read one hop down → 0) · Live, unreviewed (6 processors)
  §3 payload drift             checked (3w: every compared queue and task read) · diff lane N/A (whole-repo run)
  §4 self-overlap              checked (62 entries → 0; guards one hop down, 2 samplers B-R8) · → distributed-systems coordination-scan §1–§4 (18 files)
  §5 misfire                   checked (5a 2 · 5b 9 files → 1 unconfirmed, 1 hardening)
  §6 schedule zone             checked (42 zone-less, UTC process → 1 unconfirmed) · → infrastructure k8s-wiring-scan §5 (2)
  §7 failure discarded         checked (7a 0 · 7g 1 → 0, a delegated leader-locked prune · 7h 0) · → distributed-systems messaging-scan §3 (0 removeOnFail)
  routed                       → database transaction-scan §1 (8) · → distributed-systems messaging-scan §2/§6 (8), retry-deadline-scan §1/§6 (100),
                               dual-write-scan §1 (1) · → performance request-path-scan §20 (37 files, 2 after one hop)
```

`[report-with-fix]`: V351–V353 failed on the project's own queue and scheduler at the installed version and the fix is local to the project's wrapper, processor or schedule. `[report-flagged]`: one link is unproven (no harness run, the version `UNREAD`, a guard not traced one hop down); the row names it and the settling run. The coverage block lists **all seven** §s on every run: `checked (k → m)`, `N/A (<reason>)`, `blocked (<grep or tool>)`, `→ <owner> (k)` or `Live, unreviewed (k groups / n hits)`. A missing line is printed by `/backend-audit` as `not run`.

## False positives / precedents

The verifier reads [`precedents/backend.md`](../../../../snippets/precedents/backend.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:
- **B-R1** a library default that is safe on the installed version (APScheduler `max_instances=1`) — report an override, never the library; **B-R7** a signature change behind an enforced drain or a versioned payload; **B-R8** an idempotent, read-only, cheap job that may overlap; **B-R9** a zone-less schedule in a UTC process with a UTC meaning (with [`precedents/distributed.md`](../../../../snippets/precedents/distributed.md) § 35 for what "UTC process" requires).
- **B-R6** enqueue inside a transaction is database's; **B-R13** a library retrying a non-idempotent call is distributed-systems'; **B-R16** a job proven on SQLite or an eager queue proves nothing about production.
- **P4** prove on the queue and scheduler that ship; **P5** one finding at the base processor or scheduler wrapper, N entries.

Shapes this skill must not report: a process-local metrics sampler on `@Interval`; a sweep whose processed rows leave its filter (B-D4's shape for jobs); a lease or claim taken in the first lines of a helper the handler calls; a daily job that cannot outlive 24 h flagged for overlap; a deliberate enqueue-time snapshot that never writes back.

## When to run

- On any diff that touches a processor, a producer or its wrapper, a job payload type, a schedule decorator or registration, the scheduler or queue module, a `TZ` setting, or a queue or scheduler library version — `/backend-audit`'s "a processor or scheduler file" signal. §3 runs only on a diff (`BASE=<base-branch>`).
- On every whole-repo `/backend-audit`, reporting all seven §s; before upgrading the scheduler or queue across a major (V357), switching to virtual threads, or moving a schedule into a DST zone.

## Halt conditions

- **Do not report a high row as confirmed until a separate verifier has refuted it.** That verifier is not the run that found it, gets part A (the registration and the process that loads it), part B (the library and its version), the entry and the settling run — never this run's reasoning — and passes the row through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with `precedents/backend.md`. Under `/backend-audit` that is `@api-reviewer` in refute mode, then `@verifier` mode `refute` on every BLOCKER and HIGH; standalone, apply the protocol as a second pass and tag the rows `self-verified`. List the rest as Unconfirmed, Hardening or Refuted; never drop them.
- **Halt before any § when grep 0 or F2 is unread.** A verdict on a schedule entry without its wrapper, its guard and the process zone is invalid.
- **Halt on any finding missing its anchors:** the entry `file:line`, the library and version, the guard read (or its absence one hop down), what happens against what the job promises, the oracle or settling run, the fix in the project's own wrapper.
- **No `[report-with-fix]` without V351 / V352 / V353 on the project's own queue and scheduler** at the installed version (or a two-ended static fact). A mocked scheduler, an eager queue or a unit test of the handler alone is not one.
- **No proposed fix may hide the class:** never stretch an interval instead of adding a guard, never raise `attempts` to absorb a deleted row, never delete the `catch` that records a failure, never pin a schedule to UTC when the business time is local.
- **Do not grade a class another pack owns** (§ Boundaries); route it with a count. **Do not print "jobs look fine"** without the coverage block; a § whose grep did not run is `blocked`, never `checked`.

## Related

- `/backend-audit` dispatches this skill and folds its coverage block into its job ledger rows; `/backend-fix` closes findings failing-first on the real queue and re-runs this detector.
- `state-transition-scan` (this pack) for transitions a job or webhook fires; `@api-reviewer` judges these rows.
- distributed-systems `messaging-scan` §2/§3/§6, `retry-deadline-scan` §1/§6, `coordination-scan` §1–§4/§11, `dual-write-scan` §1, `workflow-scan` §2 and `event-contract-scan`; database `transaction-scan` §1; performance `request-path-scan` §20/§22/§24; infrastructure `k8s-wiring-scan` §5; code-quality `error-handling-scan` §4 and `correctness-smell-scan` §6; observability `metric-hygiene-scan` §2 — when those packs are installed.

## Sources

Defaults tagged `[V]` were read or run on 2026-10-14: `@nestjs/schedule` 6.1.3 and 12.0.2 (the npm tarballs, read in this build's scratch: `scheduler.orchestrator.js` spreads the decorator options into `CronJob.from` and mounts `@Interval` with `setInterval`; `schedule.explorer.js` wraps each method in a log-only `try/catch`; both pin `cron` 4.4.0), npm `cron` 4.4.0 (overlap, `waitForCompletion`, DST fire times and the process-zone default run in backend research lab B's `cron.mjs`; `threshold` 250 ms read from `dist/job.js`), node-cron 4.6.0, BullMQ 6.3.15, Celery 5.6.3 and APScheduler 3.11.3 (installed source, research notes B § 3 and § 12), FastAPI 0.143.0 (`BackgroundTasks` raising after a 200, lab B). `[V docs]`: Rails guides 8.1.4 (Active Job), Laravel 12.x (queues and scheduling); `[V issues]`: spring-framework #31900 and #33408. `[K]`: Quartz, robfig/cron, Spring `@Async`, the BullMQ scheduler overlap, Celery beat — vendor documentation or secondary sources as read by the research, not run. Real-repo and fixture counts are from read-only runs of the block above on 2026-10-14 (batch-5 eval § 3 and § 5.6). Paraphrased; no text reproduced beyond identifiers.
