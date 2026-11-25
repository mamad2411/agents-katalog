---
name: coordination-scan
description: "Locks, leases, leaders, clocks: release, TTL, renewal, advisory locks, wall-clock time, DST — read-only."
kind: skill
pack: distributed-systems
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: coordination-scan

## Premise

A distributed lock is a lease with a deadline, not a mutex. The holder can pause — a GC pause, a long await, a stalled event loop, `SIGSTOP` — past the TTL while another process takes the key; a `DEL` written as "release" then deletes the *new* holder's lock; a `SET … NX` with no TTL turns one crashed holder into a job that never runs again; an `extend()` whose result nobody reads lets two holders act at once. Clocks fail the same way: a duration measured on the wall clock goes negative when NTP steps it, an expiry written on one host's clock and compared on the database's moves a takeover early, and a "newest wins" on timestamps from two hosts loses the later write. None of these show up in a test that runs on one host with one clock and no pauses. This skill finds them in lock helpers, leader keys, lease arithmetic, time comparisons and schedule zones, and proves each with its oracle against a real store in a container. Read-only: it never edits code and never touches a store or cluster that is not a scratch container.

It owns `/ds-audit`'s Locks and leaders (§1–§6) and Clocks (§7–§11) rows. `@resilience-reviewer` (this pack) judges its rows, with `@system-architect` on leader rows (§6).

**Every finding cites the lock, lease or time comparison `<file:line>` + the event it breaks under (a holder paused past its TTL, a crashed holder, a pre-held lock, a lost leadership, a clock step, skew between two clocks, a DST transition) + the [`broker-semantics.md`](../../../../snippets/broker-semantics.md) row its verdict rests on (LO1–LO10, RD4, SD1–SD7, TM1–TM4), read at the installed version + the oracle that showed it, or the test that would settle it + the fix in the project's own primitive** (its lock helper, its atomic release script, its leader wrapper, its clock abstraction). A grep hit is a candidate. "Locks look fine" is never printed; the output is the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/distributed.md`](../../../../snippets/precedents/distributed.md) § 19–24, § 31 and § 35. The oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Distributed, V310–V319.

## The rule

A candidate is a finding when all four hold — the protocol's gates as `precedents/distributed.md` § Reading the seven gates applies them to coordination.

1. **Part A holds: this is a lock, a lease, a leader or a time decision.** A `SET … NX` used as a cache fill, a throttle window, a single-use token or a dedupe marker is not a lock (its owner is in § Boundaries). A `Date.now()` subtraction that is only logged or exported as a metric is not a timeout. The age of a *stored* instant (`now > deliveredAt + 14 days`) is calendar logic and must be wall-clock; CK-1 is a duration whose start was captured **in the same process**.
2. **Part B holds at the installed version.** The lock library, the Redis or Valkey server (for `DELEX`, Redis ≥ 8.4) and the scheduler versions are read (F1, gate 3); the default the verdict rests on is a named row — redis-py `lock()` never expires (LO3), Redisson's `leaseTime` turns the watchdog off (LO4, `[K?]`), redsync's `Unlock()` reports `ErrLockAlreadyExpired` (LO6), client-go does not fence (LO8), Redis expiry runs on the wall clock (RD4). A managed store whose setting is not in the repo is `UNREAD (<service>)`.
3. **Nothing already controls it**, across files. The project's lock helper (`F2b`: an atomic Lua compare-and-delete, a compare-and-extend), a per-event `if (!(await lock.extend())) stop` lower in the file, a transaction-scoped lock that is its own fence (precedent 20), a fencing token checked at the write, an idempotent effect under an efficiency-only lock (precedent 19), or a UTC process (precedent 35) is a control. **Read the whole file and its callees**: in the real-repo run two dropped `extend()` results were refuted only by a check 20–35 lines below them.
4. **The oracle fired, or the fact is two-ended.** A container oracle (tier C: a real Redis or Postgres, small real TTLs, `SIGSTOP` or a latch for the pause, a fake clock only for clock steps and skew) shows the overlap, the lost lock or the wrong fire count; or the static fact cites both ends (tier S: the TTL constant and the work's bound — its outbound timeouts × attempts — or both clocks of a CK-2 pair). Without one, the row is `[report-flagged]` / Unconfirmed with the settling test written out.

## Boundaries

One class, one owner. A neighbour that sees the same `file:line` lists it as corroboration.
- **A lock or limiter held per replica, and a correctness lease with no fencing token** → performance `request-path-scan` § 18 (V38), when that pack is installed. §4 here supplies the clearing grep (4d) and the lease arithmetic and owns the *mechanics* (renewal, its result, the TTL vs the work); without the performance pack the fencing half is reported here tagged `fencing (owner pack not installed)`.
- **A cron that runs on every replica** (once-per-fleet), scheduler registrations its grep misses, and migrations at boot → performance `request-path-scan` § 20 (V40, precedent 24). **A schedule overlapping itself on one process** (npm `cron`, node-cron, `@Scheduled(fixedRate)`, Laravel without `withoutOverlapping`) → backend `job-lifecycle-scan` § 4 (V352), and **a schedule's own zone on one process** (an implicit zone, a fire time in a DST zone's transition hour) → its § 6, when the backend pack is installed. §11 here owns the **coordinated** half — a once-per-period guarantee that rests on time (replicas in different zones, a lock or dedupe key built from the local date, a lease shorter than the repeated hour) — and the process-TZ read both use; without the backend pack §11 also reports the single-schedule rows, tagged `schedule zone (owner pack not installed)`. **A k8s CronJob manifest's own fields** (`timeZone`, `concurrencyPolicy`, `startingDeadlineSeconds`) → infrastructure `k8s-wiring-scan` §5 (V277) when the infrastructure pack is installed; 11c only lists them there, and `job-lifecycle-scan` §6 keeps only the question of which local time the job means. Without the infrastructure pack, 11c rows print tagged `CronJob manifest (owner pack infrastructure not installed)`.
- **A queue job outliving its broker lock or visibility** (BullMQ `lockDuration`, SQS visibility, JetStream `AckWait`) → `messaging-scan` (this pack) § 6. Locks the application takes itself stay here.
- **The outbox relay's leader lease** (an `extend()` dropped in the relay loop) and **a gap-blind cursor** → `dual-write-scan` (this pack) § 3 and § 6, deduped by `file:line`; §4 and §8 here list them as corroboration with the clock half.
- **A transaction-mode pooler** (the setting itself) → database `connection-config-scan` § 3, when the database pack is installed. §5 here owns the advisory-lock **call** through it; dedupe by the lock call's `file:line`.
- **Caches:** a stampede with no single-flight → performance `caching-scan` § 2 (whether a coalescing lock exists); invalidation ordering, delete-before-commit and cross-service invalidation by events → § 4; cache-aside vs write-through order → § 7. The coalescing lock's own mechanics (§1–§4) stay here.
- **Check-then-act on money, a single-use token, or a limit held in one process** → security `logic-race-scan` § 5, § 6, § 8. **Token time checks** (`exp` units, `ignoreExpiration`, leeway) → the security pack's `@auth-reviewer` (TM4); §8 keeps only a skew note. **Client last-write-wins** on a device → mobile `offline-sync-scan` § 4. **An in-process mutex held across I/O** → performance `request-path-scan` § 10.

## Adapt to the codebase — the lock lanes

Read every lock, scheduler and time-id library **with its version** (F1). The Node lane is inline below; Python, Java/Kotlin, Go and .NET greps are in [`stacks.md`](stacks.md), loaded only when F1c printed that stack. Facts are rows of `broker-semantics.md` (tagged and dated there); a `[K?]` row makes its verdict Unconfirmed until the settling test runs.

| Lane | Acquire / release / renew | Defaults that decide verdicts | Greps |
|---|---|---|---|
| **ioredis / node-redis hand-rolled** | `SET k token PX ttl NX` / Lua compare-and-delete or `DELEX k IFEQ token` / Lua compare-and-`PEXPIRE` | LO1 (plain `DEL` deletes another holder's lock; ≥ 8.4 `DELEX`), RD4 (expiry on the wall clock), RD5 (managed: UNREAD) | 1a, 1b, 2a, 2b, 3a, 4a, 4c, 4e, 11d |
| **node-redlock** (`redlock` 5.0.0-beta.2) | `acquire(res, ttl)` throws / `release()` / `extend(ms)` returns a **new** `Lock`; `using(res, ttl, (signal) => …)` | LO2 (`using` aborts through `signal` only; `retryCount: -1` unbounded) | 4b, F2a |
| **Postgres advisory** (`pg`, Prisma `$queryRaw`, MikroORM `execute`) | `pg_try_advisory_lock` / `pg_advisory_unlock`; `pg_advisory_xact_lock` | LO10 (session locks ignore rollback; through a pool or a transaction pooler they leak or exclude nothing) | 3a, 5a, 5b |
| **Leader keys and elections** (a Redis leader key per job, `@kubernetes/client-node` Lease) | the job's lock helper; a Lease object | LO8 (no fencing; `LeaseDuration > RenewDeadline > 1.2 × RetryPeriod`) | 6a, 4a |
| **Schedulers** (`@nestjs/schedule`, `cron`, node-cron, k8s CronJob) | `@Cron(expr, { timeZone })`, `CronJob.from`, `spec.timeZone` | SD1, SD6 (`.spec.timeZone` stable since 1.27; without it the controller's local zone, notes B S11); the process `TZ` (F3) | 11a–11d |
| **Clocks** | `Date.now()`, `new Date()` vs `performance.now()`, `process.hrtime.bigint()` | TM2 (monotonic APIs), TM3 (Redis, ShedLock, Quartz assume synced clocks) | 7a, 8a–8c, 9a, 9b, 10a |
| Python, Java/Kotlin, Go, .NET | per [`stacks.md`](stacks.md) | LO3–LO7, LO9, TM1, SD3, SD4, SD7 | `stacks.md` |

## Read the code — per lock, lease, leader and time decision

F2a lists every acquisition. For each one, answer these; the § each answer feeds is in brackets.
- **What does the lock protect, and is a duplicate harmful?** A payment, a message, an insert with no unique key (correctness) — or a cache warm, an advisory push, an idempotent rebuild (efficiency, precedent 19)? Write which case it is. [§4; fencing → perf § 18]
- **How is it released?** A library release or one atomic compare-and-delete (precedent 21), a `GET` then a compare in the app then a `DEL` (narrow), or a bare `DEL`? Is there a hand-written `DEL` of the same key elsewhere (a cleanup cron, an admin endpoint)? [§1]
- **Does the key always carry a TTL, set in the same command?** [§2] **Is the acquire result read before the work starts?** [§3]
- **What is the work's worst-case bound** — every I/O inside the critical section with its timeout × attempts, or a loop over an unbounded set — against the TTL? What renews the lease, and does a failed renewal stop the work before the next write? [§4]
- **Which connection holds a session advisory lock**, and does it reach the database through a transaction-mode pooler? [§5] **Does a leader re-check before each effect, or exit on loss?** [§6]
- **For each time comparison:** whose clock wrote each side, and is it a duration measured in one process, an expiry shared by hosts, or an ordering decision across writers? [§7–§10] **Which zone does each schedule fire in** (F3 `TZ`, an explicit `timeZone`), and what makes it fire once across the fleet? [§11]

## Pre-flight greps

Run as **one** script from the repo root (shell state does not survive between tool calls; bash 3.2 has no `mapfile`). Grep **N** feeds detector **§N**; the F lines are the gates and the inventory. Every `rg` names its path — `.` or `"${ROOTS[@]}"`: given no path, `rg` reads stdin under an agent's shell and reports a silent zero. Include globs come **first** in every command, exclusions last (for a path several globs match, the last one wins — the repo's rg-traps lint enforces it). Any `rg` exit 2 is a failed grep, never zero hits. File-level greps use `--files-without-match`, never `rg -L` (that is `--follow`). `$ACQ` is the acquisition signature every lock-file grep starts from.

```bash
ROOTS=(.)
CODE=(-g '*.{ts,mts,cts,js,mjs,cjs}')
X=(-g '!**/node_modules/**' -g '!**/{dist,build,out,coverage,.next,.nuxt,.output,generated,__generated__}/**'
   -g '!**/{test,tests,__tests__,spec,specs,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata}/**'
   -g '!**/*.{spec,test,e2e-spec,fuzz,stories}.*' -g '!**/*.d.ts' -g '!**/*.min.*'
   -g '!**/{migrations,migration,seeders,seeds}/**' -g '!**/{locales,locale,i18n,translations}/**' -g '!**/{docs,ai,.claude}/**')
CFG=(--hidden -g '*.{json,yml,yaml,conf,tf,tfvars,env,properties,toml,ini}' -g '**/Dockerfile*' -g '**/.env*'
     -g '!.git/**' -g '!**/node_modules/**' -g '!**/{package-lock,npm-shrinkwrap,composer}.json' -g '!**/pnpm-lock.yaml' -g '!**/yarn.lock'
     -g '!**/{test,tests,__tests__,e2e,fixtures,__fixtures__,testdata}/**' -g '!**/{docs,ai,.claude}/**')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(?://|/\*|\*(?:\s|/|$)|#)')
ACQ='\.set\([^\n]*(?:["\x27]NX["\x27]|\bNX\s*:\s*true)|\.setnx\(|\bnew\s+Redlock\(|\.(?:acquire|using)\(\s*\[|\bpg_(?:try_)?advisory(?:_xact)?_lock(?:_shared)?\s*\('
# F1a lock, scheduler and time-id libraries with their declared ranges (gate 3); F1b Redis/Valkey/Postgres/pooler images and managed services (DELEX needs Redis ≥ 8.4, LO1; a managed server is UNREAD); F1c the other stacks' lock and scheduler libraries (load stacks.md); F1L the locked versions (pnpm, npm, yarn) — the lockfile wins over the range
rg -n --no-heading --pcre2 '"(?:redlock|redlock-universal|@sesamecare-oss/redlock|ioredis|redis|@redis/client|@nestjs/schedule|cron|node-cron|node-schedule|croner|pg|@kubernetes/client-node|uuid|uuidv7|ulid)"\s*:\s*"[^"]+"' -g '**/package.json' -g '!**/node_modules/**' .
rg -n --no-heading -U --pcre2 '^[ \t]*["\x27]?/?(?:redlock|redlock-universal|@sesamecare-oss/redlock|ioredis|redis|@redis/client|@nestjs/schedule|cron|node-cron|node-schedule|croner|pg|@kubernetes/client-node|uuid|uuidv7|ulid)@\d[\w.-]*|"node_modules/(?:redlock|redlock-universal|@sesamecare-oss/redlock|ioredis|redis|@redis/client|@nestjs/schedule|cron|node-cron|node-schedule|croner|pg|@kubernetes/client-node|uuid|uuidv7|ulid)":\s*\{\s*\n\s*"version":\s*"[^"]+"|^"?(?:redlock|redlock-universal|@sesamecare-oss/redlock|ioredis|redis|@redis/client|@nestjs/schedule|cron|node-cron|node-schedule|croner|pg|@kubernetes/client-node|uuid|uuidv7|ulid)@[^\n]*:\s*\n\s+version:?\s+"?[\d.]+' -g '**/{pnpm-lock.yaml,package-lock.json,yarn.lock}' -g '!**/node_modules/**' .
rg -n --no-heading --pcre2 '\bimage:\s*["\x27]?(?:[\w.-]+/)*(?:redis|valkey|postgres|pgbouncer|bitnami/pgbouncer)[:@\s"\x27]|^\s*FROM\s+(?:[\w.-]+/)*(?:redis|valkey|postgres)\b|\b[\w.-]+\.(?:cache\.amazonaws\.com|ondigitalocean\.com|redis\.cache\.windows\.net)\b|\bport:\s*2506[01]\b' "${CFG[@]}" . | "${NC[@]}"
rg -n --no-heading --pcre2 '\b(?:redisson|shedlock[\w-]*|spring-integration-(?:redis|jdbc)|go-redsync/redsync|bsm/redislock|k8s\.io/client-go|go\.etcd\.io/etcd/client/v3|gocron|DistributedLock[\w.]*|RedLock\.net|Hangfire[\w.]*|Quartz|python-redis-lock|pottery|celery-redbeat|apscheduler)\b|^\s*["\x27]?redis\s*(?:[=<>~!\[]|$)' -g '**/{pom.xml,build.gradle,build.gradle.kts,go.mod,*.csproj,Directory.Packages.props,requirements*.txt,pyproject.toml,Pipfile}' -g '!**/{node_modules,vendor,.venv,venv}/**' .
# F2 the inventory (part A): F2a every lock acquisition; F2b the project's own atomic compare-and-delete or compare-and-extend (the fix §1 names)
rg -n --no-heading --pcre2 "$ACQ" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading --pcre2 '\bDELEX\b|\bIFEQ\b|redis\.call\(\s*["\x27](?:get|GET)["\x27]' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# F3 deployment shape and the process time zone (gate 7): replicas, autoscalers, Jobs/CronJobs, TZ, a JVM zone, a mounted /etc/localtime
rg -n --no-heading --pcre2 '^\s*replicas:\s*\d|\bkind:\s*(?:HorizontalPodAutoscaler|ScaledObject|ScaledJob|CronJob|Job)\b|\b(?:min|max)Replicas:\s*\d|^\s*ENV\s+TZ\b|^\s*-?\s*name:\s*["\x27]?TZ["\x27]?\s*$|\bTZ=|-Duser\.timezone|/etc/localtime' "${CFG[@]}" . | "${NC[@]}"
# 1a a DEL/UNLINK of a lock, leader, mutex or lease key; 1b the narrow variant: GET → compare in the app → DEL of the same key within 4 lines (precedent 21)
rg -n --no-heading --pcre2 '\.(?:del|unlink)\(\s*[^)\n]*(?:(?:\b|_)(?:lock|leader|mutex|lease)|Lock|Leader|Mutex|Lease|LOCK|LEADER|MUTEX|LEASE)' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading -U --pcre2 '\.get\(\s*([\w$.]+)\s*\)[^\n]*\n(?:[^\n]*\n){0,3}?[^\n]*\.(?:del|unlink)\(\s*\1\s*\)' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | rg --pcre2 '\.(?:del|unlink)\('
# 2a SET … NX with no PX/EX/PXAT/EXAT/KEEPTTL anywhere on the line (line-level lookahead: the TTL often precedes NX); 2b SETNX (a TTL, if any, comes in a second round trip)
rg -n --no-heading --pcre2 '^(?![^\n]*(?:["\x27](?:PX|EX|PXAT|EXAT|KEEPTTL|px|ex)["\x27]|\b(?:PX|EX|PXAT|EXAT|KEEPTTL)\s*:))[^\n]*\.set\([^\n]*(?:["\x27]NX["\x27]|\bNX\s*:\s*true)' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading --pcre2 '\.setnx\(|["\x27]SETNX["\x27]' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 3a an acquire whose result is dropped: SET … NX as a bare statement, pg_try_advisory_lock with no binding
rg -n --no-heading --pcre2 '^\s*(?:await\s+)?(?:this\.)?[\w$.]+\.set\([^\n]*(?:["\x27]NX["\x27]|\bNX\s*:\s*true)[^\n]*\)\s*;?\s*$|^\s*(?:await\s+)?[\w$.]+(?:\x60|\(\s*["\x27\x60])\s*SELECT\s+pg_try_advisory(?:_xact)?_lock' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 4a a lease extend() whose result is dropped; 4b redlock using() whose routine never reads its AbortSignal; 4c lock/lease TTL constants (the arithmetic's first term); 4d fencing-token evidence (clears perf §18's half); 4e lock files with no renewal at all (fixed TTL: read the work's bound); 4f when renewal lives in the project's lock helper (a renewing file that exports a `with…Lock`/`…Lease` function, discovered by its definition), every caller file that never calls `.extend(`, with the call and its file's TTL constants
rg -n --no-heading --pcre2 '^\s*(?:await\s+)?(?:[\w$]+\.)*[\w$]*(?:[Ll]ock|[Ll]ease|[Ll]eader|[Mm]utex)[\w$]*\.extend\([^)\n]*\)\s*;?\s*$' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading -U --pcre2 '\.using\(\s*\[[^\]]*\]\s*,\s*[\w$.]+\s*,\s*async\s*\(\s*(\w+)\s*\)\s*=>\s*\{(?:(?!\1\.)[^}])*\}' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | rg --pcre2 '\.using\('
rg -n --no-heading --pcre2 '\b[A-Z_]*(?:LOCK|LEASE|LEADER)[A-Z_]*(?:TTL|_MS|SECONDS|TIMEOUT)\w*\s*=\s*[^;\n]+' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading --pcre2 '\bRFencedLock\b|\blockAndGetToken\b|\bfencing_?[Tt]oken\b|\bfenceToken\b|\bModRevision\b|\bIFEQ\b|\bDELEX\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -l0 --pcre2 '\.set\([^\n]*(?:(?:\b|_)(?:lock|leader|mutex|lease)|Lock|Leader|Mutex|Lease|LOCK|LEADER|MUTEX|LEASE)[^\n]*["\x27]NX["\x27]|\bnew\s+Redlock\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg --files-without-match --pcre2 '\.extend\(|\bp?expire\(|\brenew\w*\(|\bheartbeat\w*\(|\bsignal\.aborted\b'
LH=$(rg -l0 --pcre2 "$ACQ" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -l0 --pcre2 '\.extend\(|\bp?expire\b|\brenew\w*\(' | xargs -0 -r rg -o --no-filename --no-line-number --pcre2 '^\s*export\s+(?:async\s+)?(?:const|function)\s+\K[a-z]\w*(?:Lock|Lease|Leader|Mutex)\w*\b' | sort -u | paste -sd'|' -)
echo "4f lock helpers: ${LH:-none}"; [ -n "$LH" ] && rg -l0 --pcre2 "\b(?:$LH)\(" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg --files-without-match --null --pcre2 '\.extend\(' | xargs -0 -r rg -n --no-heading -U --pcre2 "\b(?:$LH)\((?:[^(){};]|\([^()]*\))*|^[ \t]*(?:export\s+)?(?:(?:private|protected|static|readonly)\s+)*(?:const\s+)?[A-Z][A-Z0-9_]*TTL\w*\s*[:=]\s*[^;\n]+"
# 5a session-scoped advisory locks (xact-scoped ones are precedent 20); 5b a transaction-mode pooler in config
rg -n --no-heading --pcre2 '\bpg_(?:try_)?advisory_lock(?:_shared)?\s*\(' "${CODE[@]}" -g '*.sql' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading --pcre2 '\bpool_mode\s*=\s*transaction\b|[?&]pgbouncer=true\b|:6432\b|\bPOOL_MODE\s*[:=]\s*["\x27]?transaction' "${CFG[@]}" . | "${NC[@]}"
# 6a leader-key and leader-election files (input: does the holder re-check before each effect?)
rg -l --pcre2 '\b[\w$]*(?:[Ll]eader|LEADER)[\w$]*(?:Key|KEY|Lock|LOCK|Lease|LEASE)\b|\bonStartedLeading\b|\bLeaderElect\w*|coordination\.k8s\.io' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}"
# 7a a wall-clock delta in a comparison (both directions, and now > start + limit); a subtraction that is only logged is not listed
rg -n --no-heading --pcre2 'Date\.now\(\)\s*-\s*[\w$.]+(?:\([^()\n]*\))?\s*[<>]=?|[<>]=?\s*Date\.now\(\)\s*-\s*[\w$.]+|\bDate\.now\(\)\s*[<>]=?\s*[\w$.]+(?:\([^()\n]*\))?\s*\+\s*[\w$.]+' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 8a an expiry written from the app clock (`*.test-data.*` builders are fixtures); 8b an expiry compared on the database clock; 8c a time-ordered-id floor computed from a host clock
rg -n --no-heading --pcre2 '(?i)\b(?:expires?_?at|lease_?(?:until|expires?\w*)|valid_?until|locked_?until|lock_?expires?\w*|deadline_?at)\w*["\x27]?\s*[:=]\s*(?:new\s+Date\(\s*)?Date\.now\(\)' "${CODE[@]}" "${X[@]}" -g '!**/*.test-data.*' "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading --pcre2 '(?i)\b(?:expires?_at|lease\w*|locked_until|valid_until)\s*[<>]=?\s*(?:now\(\)|current_timestamp|clock_timestamp\(\))' "${CODE[@]}" -g '*.sql' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading --pcre2 '\b[\w$]*(?:[Uu]uid[Vv]?7|[Uu]lid|ULID|[Ss]nowflake|createFromTime)[\w$]*\(\s*[^)\n]*\b(?:Date\.now\(\)|[\w$]*[Nn]ow[\w$]*)\s*-' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 9a last-write-wins on timestamps, client USING TIMESTAMP; 9b ORDER BY created_at in event, projection and outbox code
rg -n --no-heading --pcre2 '\b[\w$.]+\.(?:updatedAt|updated_at|modifiedAt|lastModified|lastSeenAt|timestamp|ts)\s*[<>]=?\s*[\w$.]+\.(?:updatedAt|updated_at|modifiedAt|lastModified|lastSeenAt|timestamp|ts)\b|\bUSING\s+TIMESTAMP\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading -i --pcre2 '\border\s+by\s+["\w.]*created_?at\b|\borderBy\s*:\s*\{\s*created_?at\b' -g '*{event,Event,projection,Projection,projector,Projector,outbox,Outbox}*' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 10a the wall clock as an id or a key
rg -n --no-heading --pcre2 '\b(?:id|Id|ID|key|Key|seq|jobId|messageId|eventId)\s*[:=]\s*(?:String\(\s*|\x60[^\x60\n]*\$\{\s*|\+\s*)?Date\.now\(\)' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 11a @Cron with no timeZone (gated on F3's TZ); 11b an explicit non-UTC zone on a schedule; 11c CronJob manifests with no timeZone (→ infrastructure k8s-wiring-scan §5); 11d local-time getters inside lock files (a dedupe or lock key built from the local date)
rg -n --no-heading -U --pcre2 '@Cron\((?:(?!\btimeZone\b)[^)])*\)' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | rg --pcre2 '@Cron\('
rg -n --no-heading -U --pcre2 '(?:@Cron\(|\bCronJob(?:\.from)?\(|\bcron\.schedule\(|\bscheduleJob\()[^)]*?\btimeZone\s*:\s*["\x27](?!(?:Etc/)?(?:UTC|GMT|Universal|Zulu)\b)[A-Za-z_]+/[\w/+-]+["\x27]' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | rg --pcre2 '\btimeZone\b'
rg -l0 --pcre2 '^\s*kind:\s*CronJob\b' "${CFG[@]}" . | xargs -0 -r rg --files-without-match --pcre2 '^\s*timeZone:'
rg -l0 --pcre2 "$ACQ" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -H -n --no-heading --pcre2 '\.(?:getDate|getHours|getDay|getMonth|getFullYear|toLocaleDateString|toDateString|toLocaleString)\(\)' | "${NC[@]}"
```

Reading the output:
- **F1 is the version gate.** **F1L** prints the locked version: when it printed one, that is the version, not the range's floor (a package locked at two versions: the importer's entry in `pnpm-lock.yaml`, or `<app>/node_modules/<pkg>` in `package-lock.json`, says which one the app gets). `DELEX` exists only on Redis ≥ 8.4 (LO1): with a managed or older server (F1b), the fix is the Lua compare-and-delete. F1c names the other stacks; load `stacks.md` for each.
- **F2a is the subject list (part A).** Each acquisition is a lock, a throttle, a single-use token or a dedupe marker; only locks continue to §1–§6. **F2b names the project's own atomic release or extend** — the fix every §1 row cites when it exists.
- **F3 is the process map and the clock gate** (gate 7): which image runs the jobs, how many replicas, and whether `TZ` is set. No `TZ` in the image or manifests, or `TZ=UTC`, makes the process UTC (precedent 35).
- **4c and 6a are inputs, not verdicts**: TTL constants for the lease arithmetic, and the files whose leader holders §6 reads. 4e lists lock files with no renewal anywhere — each is a fixed-TTL lease whose work bound must be read. 4f covers the case 4e cannot see: the lock and its `extend` live in the project's helper, so a caller is a lock file only through the helper. It lists each caller file that never calls `.extend(`, with the call and the file's `*TTL*` constants; read each callback's bound against that TTL as 4e's rows are read (a file whose other callback extends hides this one: read every call in a file 4f did not list when §4 is in doubt).

Three blind spots are structural, so work around them instead of trusting a quiet grep:
- **The release and the acquire live in different files.** A helper (`withLock(…)`) acquires, and a caller's `finally` releases: read F2b's helper and every caller of it, not only the matched line.
- **A multi-line call hides the TTL or the result.** 2a and 3a are line-level; a `set(` whose `'PX'` is on the next line, or a result bound two lines later, is read by hand (the first grep of this class false-positived 19 of 19 on a real repo because its lookahead looked only after `NX`).
- **The other half of a CK-2 pair is in SQL or another service.** 8a and 8b are halves; a finding needs both clocks cited, and the comparison may sit in a migration's function, a stored procedure or another repo.

### Measured (2026-10-14)

| Tree | Result |
|---|---|
| Research samples (`locks/`, `clocks/`, `sched/` in TS, Python, Java, Go and C#, bad and good) | 0 rg errors. **Every Node BAD line surfaces in its §**: bare `DEL` (1a), `SET … NX` with no TTL (2a), `setnx` + `expire` (2b), a discarded `pg_try_advisory_lock` (3a), `using()` that never reads `signal` (4b), session `pg_advisory_lock` + `pool_mode = transaction` + `?pgbouncer=true` (5a, 5b), a backoff compared on the wall clock (7a), an app-clock expiry and its SQL `< now()` (8a, 8b), an `updatedAt` LWW (9a), `id = Date.now()` (10a), a CronJob with no `timeZone` (11c). The decoys never appear: `SET … 'PX', 30000, 'NX'`, the Lua release, `using()` that checks `signal.aborted`, `cache.del(blockId)`, a `redis.del` of a session key, `pg_try_advisory_xact_lock`, `performance.now()`, a duration that is only stored. The `stacks.md` lanes hit every Python, Java, Go and C# BAD line and miss every decoy (a checked `tryLock`, `setIfAbsent` with a `Duration`, `SetNX(…, 30*time.Second)`, `sync.Mutex`, `threading.Lock`, `time.monotonic`, `System.nanoTime`, `Stopwatch`, `time.Since(start)`) |
| Seeded tree for shapes the samples lack (6 TS files, 1 SQL, 1 Dockerfile; 4 more for the stack lanes) | The GET → compare → DEL release (1a = 1b), node-redis `{ NX: true }` with no `PX` (2a; `{ PX, NX }` stays quiet), a `SET … NX` statement (3a), a dropped `lock.extend()` (4a; the checked `if (!(await lock.extend()))` and zod's `.extend({` stay quiet), `lease_until < now()` and `pg_advisory_lock` in `.sql` (8b, 5a), both comparison directions and `now > start + ttl` (7a), a UUIDv7 floor at `now − lag` (8c), `ORDER BY created_at` in a projector (9b), `String(Date.now())` and a Kafka key from `Date.now()` (10a), `ENV TZ=Europe/Berlin` (F3), one zone-less `@Cron` (11a — the UTC- and Berlin-zoned ones stay out), a Berlin `timeZone` on a schedule (11b — an `Intl.DateTimeFormat` zone in the same file stays out), a lock key from `toLocaleDateString()` (11d) |
| Real repository (NestJS 11 + Fastify, ioredis 5.11.1 on managed Valkey, `@nestjs/schedule` 6.1.3 on `cron` 4.4.0, `uuidv7` 1.2.1 — the lockfile's versions, printed by F1L since 2026-10-14 (F1a prints the manifest ranges); read-only, about 11,100 files) | **Re-run on the full tree 2026-10-14**: 2.0 s, 0 rg errors. F1 adds `postgres:16` and `redis:7-alpine` from the root compose file and CI services (none in production; the managed ports keep the server `UNREAD`). The schedulers now take one helper: F2a **8** acquisitions (7 `SET … NX` — the helper's, an outbox stamp, single-use, OTP and throttle keys — and 1 `pg_advisory_xact_lock`); F2b the helper's Lua release and extend plus 7 other compare lines in 4 files, and a spec in the repo keeps every scheduled `SET … NX` inside the helper. **§1: 1a 0 = 1b 0** — the nine GET → compare → DEL releases below are gone. §2 0, §3 0. **§4: 4a 2** → 1 Refuted at gate 4 (the per-event checked `extend()`), 1 Hardening (the relay); 4c 31 TTL constants; 4d 0; **4e 0** — renewal now lives in the helper's file, so 4e no longer lists a caller. **4f** (added 2026-10-14 for that case; the whole pre-flight 2.5 s with it): the helpers `withLeaderLock`, `withPeriodLock` and two lease helpers, found by their definitions → **23 calls in 21 caller files** that never call `.extend(`, each with its TTL (5 to 30 minutes; one 36-hour period claim). The daily billing pass is back on the list (30-minute TTL, no renewal) and is **Refuted on read**: each merchant's posting takes `pg_advisory_xact_lock` and reads the ledger under it, and unique indexes on the posted period and the one-time rule back it up, so a second holder past the TTL posts nothing twice. The other 20 files are `Live, unreviewed` (sweeps, polls and rollups: their bounds were not read here). §5 0. §6 39 files (input). §7 6 → 2 server → 0. §8 3 server expiries + 1 web (2 `*.test-data.ts` builders excluded since 2026-10-14), 8b 0, 8c 1 (Hardening). §9 9a 1, 9b 3 (the edit-log read, now in the wallet consumer → refuted). §10 0. §11 no `TZ` → 11a **42** zone-less `@Cron` → 0 rows; 11b 0; 11c 2 → infrastructure k8s-wiring-scan §5; 11d 0. The earlier partial copy measured: 1.7 s, 0 rg errors. F2a **22** acquisitions (21 `SET … NX`, 1 `pg_advisory_xact_lock`); F2b the project's own Lua compare-and-delete and compare-and-extend in its leader-lock helper (and two jobs inlining it). **§1: 1a 9 = 1b 9** — nine cron jobs share one hand-written GET → compare → DEL release: one row, nine sites, low (precedent 21), fix = the helper's release; the frontend `http.del` the eval's first grep also counted no longer matches. **§2: 0** — every `SET … NX` carries `PX`/`EX` before `NX` (the eval's first lookahead hit 19 of 19 of them). §3 0 (every acquire is `if (!acquired) return`). **§4: 4a 3** — 2 Refuted at gate 4 (a per-event `if (!(await lock.extend()))` 20–35 lines lower in the same consumer, plus its claims ledger), 1 Hardening (the outbox relay: its effect is an advisory websocket push, precedent 19; dual-write-scan §3 owns relay leases); 4d 0 fencing tokens; 4e 13 fixed-TTL lock files — the daily billing pass (30-minute TTL, no renewal) is Unconfirmed: a comment claims idempotency by unique indexes (precedent 34), the other 12 were not read here. §5 0 session locks, 5b 0. §6 14 leader files (input). **§7: 6 → 2 server comparisons** (a lookup time budget, a reminder cooldown against a stored instant) → 0 rows; the other 4 are `apps/web`. §8: 8a 3 server expiries (a session, an invite, an in-process token cache) with 8b 0 SQL compares → 0; **8c 1** — the outbox consumers' UUIDv7 floor at `now − 30 s` → Hardening (skew past 30 s delays an event to the hourly rescan, never loses it; dual-write-scan §6 owns). §9: 9a 1 (a display "last seen" max, precedent 31), 9b 3 (two relay reads → dual-write-scan §3; one `order by created_at, id` inside one order's edit log → refuted). §10 0. **§11:** no `TZ` in the image or manifests (UTC) → 11a 41 zone-less `@Cron` → 0 rows (precedent 35); 11b 0; 11c 2 CronJob manifests with no `timeZone` (a backup at 02:15; the managed controller's zone UNREAD) → infrastructure k8s-wiring-scan §5 (the manifest field; which local time the backup means is backend job-lifecycle-scan §6's question); 11d 0. Stack lanes: 0 |
| `benchmarks/fixtures/*` (18 fixtures) | 0 rg errors; quiet except: brittle-suite 7a 2 (a refund window `now > deliveredAt + window`: the age of a stored instant, part A refuted); slow-marketplace 7a 2 (in-process cache freshness, precedent 31), 5a 1 + 5b 2 (a session `pg_try_advisory_lock` on a dedicated unpooled `new Client` — the fixture's own decoy SM-DECOY-13, refuted at §5; the §6 read finds the leader client cached with no reset when its connection drops, guarded per row by an `UPDATE … RETURNING` claim → Hardening), 11a 2 (UTC); obs-defects 11a 1 (UTC); quality-mix 10a 1 (`replay-${Date.now()}` as an admin replay id — read whether it keys a dedupe); vuln-fullstack 8a 1 (a session expiry → security); infra-ops 11c 1 (→ infrastructure k8s-wiring-scan §5). Stack lanes: 0 hits on every fixture |

## The 3,000-hit path

1. **Intersect** with F3: a lock or time comparison in code no production process runs (a script, a seed, `apps/web` for server classes) is dismissed with one read. Name the directory in the coverage block.
2. **Group by root cause**: one lock helper, one copied release idiom, one TTL constant, one clock helper is **one** finding with N sites (precedent 21's narrow release across nine cron jobs was one row).
3. **Rank**: locks around money, stock, messages or inserts with no unique key first; then leaders; then efficiency locks; then clocks.
4. **Read the top 30 groups** with the read-the-code questions; sample 10 sites per group, and the rest inherit the verdict with the group's id.
5. **Run the bulk oracle once** per group: V313 (paused holder) over the top lock, V316 (wall clock stepped) over the top time comparison.
6. **Ledger the rest** as `Live, unreviewed (k groups / n hits — <continuing command>)`. Never mark it `checked`.

## Scans for

Severity assumes a lock or comparison reached by F3. A lock whose holder moves money, stock or credit is **BLOCKER** for §1–§4 when the oracle shows two holders acting; the money effect itself is security's (§ Boundaries).

| § | Classes | Default severity |
|---|---|---|
| 1 | LK-1 release without an owner check (CWE-667); the narrow GET → compare → DEL | high for a bare `DEL` around a side effect; narrow: low, medium when the holder can pause between the read and the delete (precedent 21) |
| 2 | LK-2 no TTL, or a TTL set non-atomically (CWE-667) | high |
| 3 | LK-3 acquire result ignored (CWE-667) | high |
| 4 | LK-4 lease shorter than the work; renewal missing or its result ignored (CWE-667) | high for a correctness lock; medium for efficiency; Hardening for an advisory effect (precedent 19) |
| 5 | LK-6 session advisory lock through a pool or a transaction pooler | high for migrations and singletons; medium otherwise |
| 6 | LK-7 a leader keeps acting after losing leadership | high when the leader writes |
| 7 | CK-1 a wall-clock duration guarding a timeout or a lease | high when it guards a lease or lock; medium for a timeout; not a row for logs and metrics |
| 8 | CK-2 an expiry written on one clock and compared on another | high when it guards exclusivity; Hardening when a lag bounds it and a rescan heals it |
| 9 | CK-3 last-write-wins or ordering on wall-clock timestamps | high (a silent lost update) |
| 10 | CK-4 time as an identifier | medium; high when it keys a dedupe or a reserve |
| 11 | CK-6 DST and local-time schedules (coordinated) | medium; high for billing, settlement and payouts |

### 1. Release without an owner check (LK-1)

```
BAD:   finally { await redis.del(LOCK_KEY) }                                   // after the TTL lapsed this deletes the next holder's lock (LO1)
       const held = await redis.get(K); if (held === token) await redis.del(K)  // narrow: owner-checked, two round trips (precedent 21)
GOOD:  one Lua compare-and-delete (if get == token then del) · DELEX K IFEQ token on Redis ≥ 8.4 · redlock release() · the project's helper (F2b)
```
**Read the code:** Is the key the one set with `NX`, and is its value a per-acquire random token? Can the work outlive the TTL (§4's bound)? For the narrow shape, is there an await, I/O or a CPU-heavy step between the `GET` and the `DEL`, and can the holder pause there? Does F2b show the project already ships an atomic release (then the fix is that helper, and the copies are one group)? Is a `DEL` of the key also reachable from an admin endpoint or a cleanup cron (precedent 21 flips back)? A teardown or test fixture is not a row. **Finding when** a holder whose TTL lapsed can delete a key another holder now owns. **Proof (V310):** TTL 200 ms; A acquires and blocks 400 ms (a latch, or a pause injected between the `GET` and the `DEL` for the narrow shape); B acquires at 250 ms; A releases → B's key is gone before the fix and survives after.

### 2. No TTL, or a TTL set non-atomically (LK-2)

```
BAD:   await redis.set(`lock:payout:${id}`, '1', 'NX')        // no PX: a crashed holder blocks every later run
       await redis.setnx(k, token); await redis.expire(k, 30)  // a crash between them leaves an immortal key
       client.set('lock:r', tok, { NX: true })                // node-redis object form, no PX
GOOD:  redis.set(k, token, 'PX', ttl, 'NX') · client.set(k, tok, { PX: ttl, NX: true }) · SETNX + EXPIRE inside one MULTI
```
**Read the code:** Is the TTL set in the same command (or one `MULTI`)? Is the line really a lock, or a single-use token or a throttle with its own expiry elsewhere (part A)? A multi-line `set(` is read by hand. Python, Java and Go shapes (redis-py `lock()` with no `timeout=`, LO3; Spring `setIfAbsent(k, v)`; Go `SetNX(…, 0)`) are in `stacks.md`. **Finding when** a holder that dies before release leaves the key with no expiry. **Proof (V311):** acquire, `kill -9` the holder, then a second acquirer gets the lock within TTL + ε (it never does before the fix).

### 3. Acquire result ignored (LK-3)

```
BAD:   await redis.set(`lock:x`, tok, 'PX', 1000, 'NX'); await doWork()   // runs whether or not it got the lock
       await prisma.$queryRaw`SELECT pg_try_advisory_lock(${KEY})`        // false is discarded
GOOD:  const ok = await redis.set(…, 'NX'); if (!ok) return · const [{ locked }] = await …; if (!locked) return
```
**Read the code:** Is the result bound and checked before the first effect, maybe two lines later (then it is a decoy)? Is the `SET … NX` a lock, or a "first writer wins" marker whose result is irrelevant (a stamp, a throttle)? Redisson `tryLock`, redsync `Lock()` errors and .NET `TryAcquire*` nulls are in `stacks.md`. **Finding when** the work runs after a failed acquire. **Proof (V312):** pre-hold the lock as another holder, call the job: 0 effects after the fix, ≥ 1 before.

### 4. Lease shorter than the work; renewal missing or its result ignored (LK-4)

```
BAD:   for (;;) { await handleBatch(); await lock.extend(); }            // extend() false: another holder has it, and this one carries on
       redlock.using([k], 5000, async (signal) => { await charge(id) })   // never reads signal.aborted (LO2)
       a 30-minute fixed TTL around a pass over every tenant, with no renewal and no idempotent effect
GOOD:  if (!(await lock.extend())) return  before each write · if (signal.aborted) throw signal.error · TTL ≥ 2 × the work's bound,
       or renewal at ≤ TTL/3 with its result checked · a fencing token checked at the write for a correctness lock (perf § 18, V38)
```
**Read the code:** What is the work's worst-case bound — each I/O in the critical section with its timeout × attempts, or the size of the loop — against the TTL constant (4c; 4f prints it beside each helper call)? `THR-DS-LEASE`: TTL ≥ 2 × the bound, or a renewal at ≤ TTL/3 whose failed result stops the work; a correctness lock also needs a fencing token checked at the write. Is a dropped `extend()` backstopped by a check later in the same file, or by a claims ledger (gate 4 — read the whole file)? Is the protected effect correctness or efficiency (precedent 19: a websocket push, a cache warm, a refresh is advisory — write which)? Is a comment's "idempotent" claim backed by a unique index you read (precedent 34)? Does 4d show a fencing token, and is it **checked at the write** (`WHERE fence < :t`), not merely obtained? A relay's lease is `dual-write-scan` §3's. **Finding when** two holders can act at once and the effect is not idempotent. **Proof (V313):** small real TTLs; pause the holder past the TTL (`SIGSTOP`, a latch, a busy loop) while a second holder takes the key: the first stops before its next write, or the resource rejects the stale write (V38 for the fencing half).

### 5. Session advisory lock through a pool or a transaction pooler (LK-6)

```
BAD:   await pool.query('SELECT pg_advisory_lock($1)', [K]) … await pool.query('SELECT pg_advisory_unlock($1)', [K])   // two connections
       pg_try_advisory_lock behind pool_mode = transaction / ?pgbouncer=true / :6432                                  // excludes nothing
GOOD:  pg_advisory_xact_lock inside the transaction that does the work (precedent 20) · one checked-out client for lock, work and unlock
       · a direct or session-mode connection for migrations and singletons
```
**Read the code:** Which connection takes the lock, and is the same one used for the work and the unlock (a `const c = await pool.connect()` held throughout, or a dedicated `new Client`)? Does that connection's URL reach a transaction-mode pooler (5b, and the deploy's env)? The pooler setting itself is database § 3's. **Finding when** the lock is taken and released on different sessions, or a pooler hands the session to another client. **Proof (V314):** pool max 2; acquire, then unlock under a parallel query so it lands on the other connection: `SELECT count(*) FROM pg_locks WHERE locktype = 'advisory'` is 1 after "unlock" before the fix, 0 after.

### 6. A leader keeps acting after losing leadership (LK-7)

```
BAD:   if (this.leader) return true                       // a cached leader client: a dropped connection frees the lock, this replica keeps acting
       a Redis leader key taken once per tick, then a loop of side effects that never re-checks it · OnStartedLeading ignoring its ctx (Go, stacks.md)
GOOD:  re-check (extend, or read the token) before each effect, or abort through a signal · exit the process on loss · fence the writes
```
**Read the code:** For each 6a file: what does the leader do between acquiring and the next check? Does losing the lease (an expired key, a dropped session, a failed renewal) stop it before the next side effect, or does a cached flag keep it running? Is each effect guarded per row anyway (an `UPDATE … RETURNING` claim, a unique key — then Hardening)? Is the process single-replica by design (precedent 23 clears only the cross-replica half)? Once-per-fleet registration is perf § 20's. **Finding when** two replicas can both act as leader and the effect is not guarded per row. **Proof (V315):** block A's renewals (drop its connection, or a fake clientset); A must stop acting before B starts — count writes tagged by identity, overlap 0.

### 7. A wall-clock duration guarding a timeout or a lease (CK-1)

```
BAD:   if (Date.now() - acquiredAt > LEASE_TTL_MS) takeover()    // an NTP step back makes the lease look fresh; forward, expired
       while (Date.now() - started < timeoutMs) { … }          // a step back never times out
GOOD:  performance.now() / process.hrtime.bigint() for in-process durations (TM2) · the store's own TTL (PX) for a shared lease
```
**Read the code:** Was the start captured in this process (CK-1), or is it a stored instant (calendar logic: not CK-1; shared between hosts: §8)? What does the comparison decide — a lease, a lock, a retry timeout (a row), or a log line, a metric, a single-host budget, a cooldown shown to users (precedent 31, not a row)? **Finding when** a wall-clock step can make a lease or timeout fire early or never. **Proof (V316):** under a fake clock that moves `Date.now()` and leaves the monotonic clock alone (`@sinonjs/fake-timers` `setSystemTime`), step the wall clock back 10 s mid-operation: the timeout still fires at the right monotonic time after the fix.

### 8. An expiry written on one clock and compared on another (CK-2)

```
BAD:   app: expiresAt = new Date(Date.now() + 30_000)       SQL: UPDATE leases SET owner = $1 WHERE lease_until < now()
       a UUIDv7/ULID floor computed as uuidv7At(now - lag) on the consumer host, against ids minted on every writer's clock
GOOD:  compute and compare on one clock (lease_until = now() + interval '30 s' and < now(), both in SQL) · Redis PX · a lag that
       bounds the skew, plus a rescan that heals it
```
**Read the code:** Whose clock wrote the expiry (app host, database, another service), and whose clock compares it? Cite both lines (tier S). How large can the skew be against the margin (ShedLock and Quartz assume synced clocks, TM3)? For a time-ordered-id floor: what lag protects late commits, and does a rescan pick up an event a skewed writer placed below the floor (bounded → Hardening; `dual-write-scan` §6 owns the cursor)? A token expiry is security's (TM4). **Finding when** skew between the two clocks moves a takeover early, overlaps two holders, or skips an event for good. **Proof (V317):** app clock = DB clock + 5 s (fake clock on the app, real database): no early takeover, no overlap, no skipped event.

### 9. Last-write-wins or ordering on wall-clock timestamps (CK-3)

```
BAD:   if (incoming.updatedAt > existing.updatedAt) await save(incoming)   // two services' clocks decide which write survives
       a projector reading SELECT … ORDER BY created_at across event streams · Cassandra USING TIMESTAMP from clients
GOOD:  a version counter (WHERE version = :v) · the stream position or a database sequence · a hybrid logical clock
```
**Read the code:** Who writes each timestamp — one database primary (`DEFAULT now()`), or several hosts or clients? Does the comparison decide which write wins, or only what to display (precedent 31)? Is the `ORDER BY created_at` within one aggregate with an id tie-break (one stream), or across streams? A relay's read order is `dual-write-scan` §3's; a device's offline LWW is mobile's. **Finding when** clock skew lets an earlier write overwrite a later one, or a projection applies events out of order. **Proof (V318):** two writers skewed −2 s / +2 s update one row in real order: the later write wins by version after the fix.

### 10. Time as an identifier (CK-4)

```
BAD:   const evt = { id: String(Date.now()), … } · Kafka key `${Date.now()}` · a dedupe key `replay-${Date.now()}`
GOOD:  UUIDv7 / ULID / a database sequence · a business key for a dedupe
```
**Read the code:** Can two replicas, or two calls in one millisecond, mint the same id? Does the id key a reserve, a dedupe or a partition (then a collision drops or merges work, and the redelivery id class is `messaging-scan` §2's)? **Finding when** two events can share an id that something dedupes or orders on. **Proof:** the static fact (the minting line and the consumer that keys on it); there is no V-slot.

### 11. DST and local-time schedules — coordinated (CK-6)

```
BAD:   ENV TZ=Europe/Berlin + @Cron('0 30 2 * * *') under a 10-minute fleet lock   // 02:30 happens twice in October: the lock has expired, both fire
       a daily lock key built from new Date().toLocaleDateString() on replicas with different TZ
GOOD:  UTC for the process and the schedule · an explicit timeZone at a time outside the transition hour · a dedupe keyed on the UTC fire time
```
**Read the code:** What zone does the process run in (F3: `ENV TZ`, a manifest `env: TZ`, `-Duser.timezone`, a mounted `/etc/localtime`)? With no `TZ` anywhere, or `TZ=UTC`, every schedule without a zone is UTC and is not a row (precedent 35). In a DST zone: which fire times fall in the transition hour (01:00–03:00 local in most zones), and what makes the run happen once — a lock whose TTL is shorter than the repeated hour, a key carrying the local date (11d), replicas configured with different zones? A CronJob without `spec.timeZone` fires in the controller's local zone (notes B S11; SD6) — UNREAD on a managed control plane; the manifest field is infrastructure `k8s-wiring-scan` §5's, and which local time the job means is backend `job-lifecycle-scan` §6's, as is a single process's schedule zone (§ Boundaries). **Finding when** a DST transition makes a coordinated job fire 0 or 2 times. **Proof (V319):** on the transition day, under a fake clock in the job's zone, the fleet fires the documented number of times (once).

## Output

```
coordination-scan coverage — scope=whole repo  stacks=ioredis ^5.4.2, @nestjs/schedule ^6.1.3, uuidv7 ^1.2.1 (apps/api/package.json) · Redis: Valkey (managed) UNREAD
Inventory: 22 acquisitions (21 SET … NX, 1 pg_advisory_xact_lock) · atomic release helper: apps/api/src/outbox/lease.ts:20 · TZ: unset (UTC)

Findings: 0 · Unconfirmed: 2 · Hardening: 2

1. apps/api/src/shared/scheduling/lease.ts:13                                                Refuted
   §1 LK-1 — every scheduled lock goes through one helper whose release is an atomic Lua compare-and-delete (and extend a
   compare-and-pexpire), pinned by a spec; an earlier copy had nine crons doing GET → compare → DEL (precedent 21).
2. apps/api/src/billing/storage-billing-daily.job.ts:66                                      Refuted
   §4 4f — a 30-minute fixed TTL, no renewal, around a pass over every tenant. Read: each tenant's posting takes
   pg_advisory_xact_lock then reads the ledger under it, and a unique index on the posted period backstops a second pass
   (precedent 19: a lock outliving the work is efficiency only once the effect is idempotent in the store).
3. apps/api/src/outbox/relay.worker.ts:116                                                   Hardening
   §4 LK-4 — extend() result dropped in the relay loop; the effect is an advisory websocket push (precedent 19). Owner: dual-write-scan §3.
4. apps/api/src/outbox/outbox-consumer.ts:160                                                Hardening
   §8 CK-2 — a UUIDv7 floor at now − 30 s on the consumer host against ids minted on every writer: skew > 30 s delays an event to the
   hourly rescan, never loses it. Owner: dual-write-scan §6.

Verification: 14 candidates → 0 findings · 2 unconfirmed · 2 hardening · 10 refuted (self-verified)

Class coverage:
  §1  release / owner check     checked (9 → 1 group, unconfirmed)
  §2  TTL                       checked (21 SET … NX → 0)
  §3  acquire result            checked (0)
  §4  lease vs work / renewal   checked (3 dropped extend() → 2 refuted, 1 hardening; 13 fixed-TTL files → 1 unconfirmed, Live, unreviewed (12 files))
  §5  advisory via pool         checked (0 session locks; 1 xact lock, precedent 20)
  §6  leader after loss         Live, unreviewed (14 leader files — read with §4's fixed-TTL group)
  §7  wall-clock durations      checked (2 server comparisons → 0, precedent 31)
  §8  two clocks                checked (3 app-clock expiries, 0 SQL compares → 0; 1 id floor → hardening)
  §9  LWW / ordering            checked (1 + 3 → 0; 2 relay reads → dual-write-scan §3)
  §10 time as id                checked (0)
  §11 DST schedules             checked (TZ unset → UTC, precedent 35; 41 @Cron → 0) · → infrastructure k8s-wiring-scan §5 (2 CronJobs)
  → performance request-path-scan §18 (0 fencing rows) · §20 (0)
```

`[report-with-fix]`: the oracle failed on the unfixed code against a real store, and the fix is local to the project's lock helper, release script, leader wrapper or clock abstraction. `[report-flagged]`: one link is unproven (no container run, a work bound not measured, a comment's claim not read, a managed setting UNREAD); the row names it and the settling test. The coverage block lists **all eleven** §s on every run: `checked (k → m)`, `N/A (<reason>)`, `blocked (<grep or tool>)`, `→ <owner> (k)` or `Live, unreviewed (k groups / n hits)`. A missing line is printed by `/ds-audit` as `not run`.

## False positives / precedents

The verifier reads [`precedents/distributed.md`](../../../../snippets/precedents/distributed.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:
- **§ 19** an efficiency lock needs no fencing — name the advisory case (a push, a cache warm, a refresh); flips back when the protected code sends mail, charges or inserts without a unique key.
- **§ 20** a lock scoped to the writing transaction is its own fence (`pg_advisory_xact_lock`, `FOR UPDATE`); ShedLock, Quartz JDBC and `onOneServer` are once-per-fleet controls, but a run past `lockAtMostFor` is still §4.
- **§ 21** a library release or one atomic compare-and-delete is owner-checked; GET → compare → DEL is the narrow LK-1 (low, medium with a pause between); the fix is the project's own helper.
- **§ 22** client-go Lease election does not fence: a leader acting after loss stays a candidate. **§ 23** a scheduler imported only by a single-replica worker is cleared for the fleet half. **§ 24** migration locks are perf § 77's (MG1–MG14).
- **§ 31** wall-clock timestamps are fine for display, audit and single-store TTLs; they flip back for cross-host ordering and for durations guarding a lease or timeout.
- **§ 34** a comment claiming "idempotent" or "one replica" is a pointer; read the index or the manifest. **§ 35** a schedule with no zone in a UTC process is not CK-6.

Shapes this skill must not report: a `SET … NX` that is a throttle, a stamp or a single-use token; a `del` in a test teardown or an admin force-unlock not reachable in production; a `Date.now()` delta that is logged or exported; the age of a stored instant against a business window; an `ORDER BY created_at, id` within one aggregate; 41 zone-less crons in a UTC process.

## When to run

- On any diff that touches a lock helper, a `SET … NX`, a release, an `extend`, an advisory lock, a leader key or election, a time comparison, a TTL constant, a schedule or the process `TZ` — `/ds-audit`'s "a lock helper, `SET … NX`, leader election, a time comparison, a schedule" signal.
- On every whole-repo `/ds-audit`, reporting all eleven §s; before adding replicas to a process that holds a lock, moving the process to another zone, or upgrading the lock library or the Redis server.

## Halt conditions

- **Do not report a high row as confirmed until a separate verifier has refuted it.** That verifier is not the run that found it, gets part A, part B, the `broker-semantics.md` row, the version lines and the F2 row — never this run's reasoning — and passes the row through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with `precedents/distributed.md`. Under `/ds-audit` that is its verification phase; standalone, apply the protocol as a second pass and tag the rows `self-verified`. List the rest as Unconfirmed, Hardening, Pre-existing or Refuted; never drop them.
- **Halt before any § when F1 is unread.** A verdict resting on a library or server default whose version is unknown is invalid; when no row covers the installed range, the row is Unconfirmed with the release notes to read.
- **Halt on any finding missing its anchors:** the lock or comparison `file:line`, the event, the `broker-semantics.md` row, the protected effect (correctness or efficiency, named), the fix in the project's own primitive.
- **No `[report-with-fix]` without a container oracle that failed** (or a two-ended static fact for §4's arithmetic, §8 and §10). Use small real TTLs for Redis expiry, never fake timers; fake clocks only for clock steps, skew and DST.
- **No proposed fix may trade one failure for another without a written decision:** a longer TTL in place of renewal and an idempotent effect, removing the lock, or `maxStalledCount`-style "never run twice" settings that turn a duplicate into a loss.
- **Never contact a store or cluster outside a scratch container**, and never run `kubectl`, `helm` or a cloud CLI against a default context or profile; V315 runs on a kind cluster with its own kubeconfig or on client-go's fake clientset.
- **Do not grade a class another pack owns** (§ Boundaries); route it with a count. **Do not print "locks look fine"** without the coverage block; a § whose grep did not run is `blocked`, never `checked`.

## Related

- `/ds-audit` dispatches this skill and folds its coverage block into the Locks and leaders and Clocks ledger rows; `/ds-fix` closes findings with the failing-first oracle, the fix at the root primitive (the lock helper, not each caller), a re-run of this detector and the sibling sweep.
- `messaging-scan` § 6 (broker locks vs run time) and `dual-write-scan` § 3, § 6 (relay leases, gap-blind cursors), this pack; `@resilience-reviewer` judges these rows, with `@system-architect` on §6.
- performance `request-path-scan` § 10, § 18, § 20 and `caching-scan` § 2, § 4, § 7; database `connection-config-scan` § 3; backend `job-lifecycle-scan` § 4, § 6; security `logic-race-scan` § 5, § 6, § 8 and `@auth-reviewer`; mobile `offline-sync-scan` § 4 — when those packs are installed.

## Sources

Defaults are rows of `broker-semantics.md` (read 2026-10-14: redis.io *Distributed locks* and `DELEX`, the node-redlock README and npm registry, redis-py `redis/lock.py` 8.1.0, the Redisson locks page, the ShedLock README, go-redsync `mutex.go`, the DistributedLock README, client-go `leaderelection.go`, pkg.go.dev `time`, kubernetes.io *CronJob*). Grep literals are the distributed-systems research notes B §§ 1, 2 and 7 (L1–L7, K1, T1–T7, tested on the research samples 2026-10-14) and the batch-5 eval § 3.2 DS-4 and § 3.8, re-measured here. Paraphrased; no text reproduced beyond identifiers.
