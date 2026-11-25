---
name: side-effect-parity-scan
description: "V1→V2 side-effect parity: observers, traits, dual-run duplicates, hidden consumers, crons, triggers — read-only."
kind: skill
pack: migration
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: side-effect-parity-scan

## Premise

The effects a port loses are the ones no controller shows. In V1 a Laravel observer (a Rails callback, a Django signal) sends the "your order has shipped" e-mail from `updated`, a `LogsActivity` trait writes an audit row for every balance change, a MySQL trigger keeps `orders.line_count`, a view feeds the finance workbook through its own login, and `routes/console.php` expires credit every night. A controller-by-controller port ports none of them, and V2 still compiles, passes its tests and answers every route. Two effects also appear that V1 never had: an e-mail sent twice in the dual-run window, because V2's subscriber fires on rows the V1 → V2 sync inserts, and a job enqueued inside a transaction that V1 dispatched `afterCommit`.

This skill owns the V1≠V2 delta for MG-SE-1, MG-SE-2, MG-HC-1, MG-JB-1 and DM-10 (SE §1–§5). Mechanisms that exist in one codebase (in-transaction I/O, the outbox, a schedule's own zone) stay with their owners; this skill answers "does V2 produce the effect multiset V1 produced, once, at the same moment".

**Every finding cites the V1 emitter (observer, trait, listener, trigger, schedule, view) `file:line`, the (entity, verb) or job key, the written V2 counterpart search, and the oracle (V371–V373).** Keyword hits are not effects: the lanes and greps match **call shapes**, because `webhook` and `audit` as bare words were most of the tokens on four fixtures (eval § 3.6).

## The rule

A candidate becomes a finding only when all four hold:

1. **V1 emits it on a live path.** The observer is registered (`#[ObservedBy]`, `::observe`), the trait is on the model, the listener is in `$listen`, the schedule entry is not commented out, the trigger is created by a migration that ran.
2. **The V2 multiset differs.** For the same (entity, verb): an effect kind missing (SE-1), an extra or earlier one (SE-2), a consumer's object gone or renamed (HC-1), a schedule or consumer missing (JB-1), DB-side logic with no code or DDL counterpart (DM-10).
3. **The counterpart search is written out** — V2 subscribers and `@OnEvent` listeners in **any** module, outbox inserts, DB triggers and functions in V2 migrations, k8s `CronJob`s and BullMQ repeats, a gateway or another service ([precedents § 1, § 28](../../../../snippets/precedents/migration.md)) — and every place reads empty.
4. **No record makes it intentional** (ADR plus `pair-map` row with a reason, § 3, § 26), and the V1 effect is not dead (§ 2).

## Boundaries

- **The in-transaction mechanism** (external I/O inside a transaction, publish-then-commit, the outbox and its relay) → database `transaction-scan` §1 and distributed-systems `dual-write-scan` §1–§2, when those packs are installed. SE §2 reports only that V1 waited for commit and V2 does not, or that V2 repeats an effect V1 already sent; without the owner packs it reports the delta and names the missing mechanism review in the row.
- **A schedule's own semantics in one codebase** (self-overlap, misfire, zone, DST) → backend `job-lifecycle-scan` §4–§6, when the backend pack is installed. SE §4 compares V1's entry to V2's.
- **FK actions and constraints in one codebase** → database `schema-integrity-scan` §2. SE §5 reports a V1 rule V2 lost. Lost unique / NOT NULL constraints and soft delete → `data-cutover-orchestrate` (§5–§9) and `surface-parity-scan` §5 (scope).
- **Shadow traffic that reaches real downstreams** → `cutover-routing-scan` §3; SE §2 covers the dual-run window, not the mirror.

## Lanes

`paired-inventory` supplies I-SIDE (`<table>.<event>`, a route key or `event:<ident>`, with the effect `kinds`), I-SCHED (job keys, cron, zone, overlap) and I-SCHEMA (FK `on_delete`, `derived:<table>.<column>` for a trigger-maintained column, `view:<name>`; a V1 table with no V2 row collapses to one `table:` row). The greps below add grants, export headers, the columns an activity trait logs, replication guards and commit timing, which no lane keys, and re-read triggers and FK actions from the DDL when the V2 snapshot is partial.

| Stack | Effects with no call site (§1) | Commit timing, dual run (§2) | Hidden consumers (§3) | Jobs (§4) | DB-side logic (§5) | Tag |
|---|---|---|---|---|---|---|
| **Laravel (V1)** | observers, `$dispatchesEvents`, `booted()` closures, `LogsActivity` / `Searchable` / `Notifiable`, `EventServiceProvider::$listen`, queued mail | `->afterCommit()`, `ShouldDispatchAfterCommit`, `DB::afterCommit` | `CREATE VIEW` + `GRANT` in migrations, `fputcsv` headers, `Storage::disk('sftp')` | `routes/console.php` `Schedule::`, Kernel `schedule()`, `ShouldQueue` jobs and listeners | `DB::unprepared('CREATE TRIGGER …')`, `storedAs` / `virtualAs`, `cascadeOnDelete()` | [V] port-pair |
| **NestJS + MikroORM (V2)** | `EventSubscriber` `after*` hooks, `@OnEvent`, queue `add('<name>')`, activity / audit services | the transaction runner's `onCommit` hook, outbox rows, a replication guard on subscribers | migrations `create view` / `grant`, export header literals, SFTP / S3 puts | `@Cron` / `@Interval`, BullMQ `repeat` / `upsertJobScheduler`, `@Processor`, k8s `CronJob` | `deleteRule` / `onDelete` on relations, snapshot `deleteRule`, `formula`, migrations `create trigger` | [V] port-pair |
| **Rails** | callbacks (`after_commit`, `after_save`), concerns, `ActiveSupport::Notifications` | `after_commit` vs `after_save` | DB views, `whenever` exports | `whenever`, `sidekiq-cron` | `dependent: :destroy` vs DB `ON DELETE` | [K?] |
| **Django** | signals (`post_save`), `save()` overrides | `transaction.on_commit` | views via `RunSQL` | Celery beat | `on_delete=CASCADE` (emulated in Python) | [K?] |
| **Spring / JPA** | `@EntityListeners`, `@TransactionalEventListener` | `TransactionPhase.AFTER_COMMIT` | views, report SQL | `@Scheduled`, Quartz | `CascadeType.REMOVE` vs DDL | [K?] |
| **Express / Go** | explicit calls only | hand-written | report SQL | `node-cron`, `robfig/cron` | DDL | [K?] |

## Tool lane and ledger

Static only. The proof is a **journal**: both sides' SMTP at Mailpit, outbound HTTP at WireMock, a recording queue consumer, and an `EXCEPT` diff of audit and activity tables, per (entity, verb) (`proof-oracles.md` § Harnesses (migration), V371). Capturing V1 in its own test suite with `Mail::fake()` / `Http::fake()` is unmeasured [K?]. Without a bootable V1, SE rows are static-fact candidates and V371 is Unconfirmed with the request written out. The engine ledger comes first; in solo mode an `I-SCHED` record with an old extractor hash makes §4 `blocked`.

## Pre-flight

Run as one script (bash 3.2-safe). Inputs and the inside-V2 rule are those of `surface-parity-scan` § Pre-flight. This exclusion array keeps `migrations/` **on purpose**: views, grants, triggers and FK actions live there. V1 greps run through `v1g` by V1 stack (`surface-parity-scan` § Pre-flight). The V1-ONLY job lookup skips a job whose `target_live` is `no` or `ambiguous` (dead in V1, precedent § 48) and drops comment lines, so a `// Ported from …` note is never the counterpart.

```bash
PI="${PI:-.claude/skills/paired-inventory/scripts/pair-inventory.py}"; V2="${V2:-.}"; V1="${V1:-}"; MIG="${MIG:-$V2/ai/migration}"
abs() { (cd "$(dirname "$1")" 2>/dev/null && printf '%s/%s\n' "$(pwd)" "$(basename "$1")") || printf '%s\n' "$1"; }
PI=$(abs "$PI"); MIG=$(abs "$MIG"); [ -n "$V1" ] && V1=$(abs "$V1"); cd "$V2" || exit 2   # grep from inside V2: rg globs also match the root path given
OUT="$(mktemp -d "${TMPDIR:-/tmp}/side-effect-parity.XXXXXX")"; export GIT_OPTIONAL_LOCKS=0; mkdir "$OUT/no-v1"; : > "$OUT/stamp"
ck() { [ "$2" -lt 2 ] || echo "$1 BLOCKED (rg exit $2) — the class is blocked, never 0 hits"; }
if [ -n "$V1" ]; then SIDE=(--v1="$V1" ${LIVE:+--live-v1}); else SIDE=(--v1-inventory="$MIG/v1-inventory"); echo "solo: V1 greps search an empty dir (blocked, no V1 tree)"; fi
python3 -I "$PI" "${SIDE[@]}" --v2=. --lanes=I-SIDE,I-SCHED,I-SCHEMA --pair-map="$MIG/pair-map.tsv" --ledger="$MIG/ledger.md" --out="$OUT/run" > "$OUT/candidates.tsv" 2> "$OUT/ledger.txt"; echo "pair-inventory exit $? — 0 ran clean · 1 candidates (not a failure) · 2/3/4 BLOCKED: read $OUT/ledger.txt (its last line prints the reason) before any row"
S1=$(ls -d "$OUT"/run/run.*/v1 2>/dev/null | head -1); V1ROOTS=("${S1:-${V1:-$OUT/no-v1}}"); V2ROOTS=(.)
case "/${V1ROOTS[0]}/" in */fixtures/*|*/test/*|*/tests/*|*/spec/*|*/e2e/*|*/docs/*|*/lang/*|*/vendor/*) echo "BLOCKED: the V1 root path holds an excluded segment, so every V1 grep reads 0 files — copy V1 out or use the snapshot";; esac
X=(-g '!**/{node_modules,vendor,dist,build,coverage,storage,bootstrap/cache}/**' -g '!**/{test,tests,spec,__tests__,__mocks__,fixtures,e2e}/**'
   -g '!**/*.{spec,test,e2e-spec,test-data,fixture,fixtures,d,stories}.*' -g '!**/{lang,locales,i18n,docs}/**' -g '!**/database/{seeders,factories}/**' -g '!**/*.{md,lock,map,snap}')
V1STACK=none; [ -f "${V1ROOTS[0]}/composer.json" ] && V1STACK=laravel; [ -d "${V1ROOTS[0]}/supabase/migrations" ] && V1STACK=supabase; echo "V1 stack: $V1STACK (V1 greps read its files: PHP for laravel, SQL + edge functions for supabase, else N/A — never 0 files silently)"
v1g() { local id="$1" php="$2" sb="$3"; shift 3; case "$V1STACK" in laravel) rg -n --pcre2 "$@" "$php" -g '*.php' "${X[@]}" "${V1ROOTS[@]}"; ck "$id" $?;; supabase) if [ "$sb" = - ]; then echo "$id N/A (V1 stack supabase: no grep for this shape; the lane rows carry it)"; else rg -n -i --pcre2 "$sb" -g '*.{sql,ts,toml}' -g '!**/{node_modules,tests,__tests__}/**' -g '!**/*.{test,spec}.ts' "${V1ROOTS[0]}/supabase"; ck "$id" $?; fi;; *) echo "$id N/A (V1 stack $V1STACK: this grep reads Laravel PHP or Supabase SQL; a Rails, Django or Spring V1 prints N/A)";; esac; }
awk -F'\t' '$1=="CANDIDATE" && ($4 !~ /^(col|table|unique):/ || $5=="on_delete")' "$OUT/candidates.tsv" | cut -f2-9
# 1. Effects with no call site in V1 (observers, model events, traits, listeners) and every emitter call on both sides — call shapes, not words.
v1g SE1a '#\[ObservedBy\(|::observe\(|\$dispatchesEvents\b|static::(?:creat|updat|sav|delet|restor)(?:ed|ing)\(|^\s*use\s+[^;]*\b(?:LogsActivity|Searchable|Notifiable|Auditable|HasAuditTrail)\b|protected\s+\$listen\b' '\bcreate\s+(?:or\s+replace\s+)?(?:constraint\s+)?trigger\s+\w+'
v1g SE1b '\bMail::\w+\(|\bNotification::send\w*\(|->notify(?:Now)?\(|(?<![\w>:])event\(|\b\w+::dispatch(?:Sync|AfterResponse)?\(|(?<![\w>:])dispatch\(|\bactivity\(\)|\bHttp::(?:post|put|patch|delete)\(|->(?:searchable|unsearchable)\(\)' '\bnet\.http_(?:post|get|request)\s*\(|\bpg_notify\s*\(|\bpgmq\.send|\binsert\s+into\s+[\w."]*(?:notif|audit|activit|outbox|queue|histor)\w*|functions\.invoke\(|\.from\(\s*[\x27"]\w*(?:notif|audit|activit|outbox|queue)\w*[\x27"]\s*\)\s*\.(?:insert|upsert)\('
rg -n --pcre2 '\.(?:add|addBulk)\(\s*[\x27"`][\w:.-]+[\x27"`]|@OnEvent\(|\.emit(?:Async)?\(\s*[\x27"`]|\b\w*[Mm]ail\w*\.(?:send\w*|add)\(|\b\w*(?:[Aa]ctivity|[Aa]udit)\w*\.(?:log|record|write)\(|\b\w*[Ww]ebhook\w*\.(?:send|post|dispatch)\(|\basync\s+after(?:Create|Update|Delete|Upsert|Flush)\s*\(|@(?:AfterInsert|AfterUpdate|AfterRemove|AfterCreate|AfterDelete)\(' -g '*.{ts,js}' "${X[@]}" "${V2ROOTS[@]}"; ck SE1c $?
# 1e. The entities each V2 subscriber covers — the line a missing-verb finding cites (read its after* hooks against V1's verbs).
rg -n -U --pcre2 'getSubscribedEntities\([^)]*\)[^{\n]*\{\s*\Kreturn\s*\[[^\]\n]*\]' -g '*.{ts,js}' "${X[@]}" "${V2ROOTS[@]}"; ck SE1e $?
# 1d. Columns a V1 activity trait logs (`logOnly([...])`) and every V2 write to them: each write site must log as V1 did.
LC=$(rg -o --no-filename --pcre2 'logOnly\(\[[^\]]*\]' -g '*.php' "${X[@]}" "${V1ROOTS[@]}" | grep -o "'[a-z_]*'" | tr -d "'" | sort -u | awk -F_ '{s=$1; for(i=2;i<=NF;i++) s=s toupper(substr($i,1,1)) substr($i,2); printf "%s%s|%s", (n++?"|":""), $0, s}'); echo "V1 activity-logged columns: ${LC:-none (SE1d N/A)}"
rg -n --pcre2 '\.(?:'"${LC:-__none__}"')\s*(?:[-+*/]?=)(?!=)' -g '*.{ts,js}' "${X[@]}" "${V2ROOTS[@]}"; ck SE1d $?
# 2a. Dual-run duplicates: a V1→V2 sync exists (first line), and these emitting subscribers never check for a replicated write.
rg --files -g '**/{sync,cdc,replication,dual-write}/**' -g '!**/node_modules/**' "${V2ROOTS[@]}"; ck SE2a-sync $?
rg -l0 --pcre2 '\basync\s+after(?:Create|Update|Delete|Upsert)\s*\(|@OnEvent\(|@(?:AfterInsert|AfterUpdate)\(' -g '*.{ts,js}' "${X[@]}" "${V2ROOTS[@]}" | xargs -0 -r rg -l --pcre2 '\.(?:add|send\w*|emit|publish|log)\(' | tr '\n' '\0' | xargs -0 -r rg --files-without-match --pcre2 'replicat|isReplicatedWrite|v1-sync|getFilterParams|\bsource\s*===?'; ck SE2a ${PIPESTATUS[0]}
# 2b. Effects enqueued inside a transaction body; V1's commit-deferred dispatches (afterCommit and friends) on the next line.
rg -n -U --pcre2 '(?:\btransactional|\$transaction|\btx\.run|\.transaction)\(\s*async[^\n]*\n(?:(?!\s*\}\s*\)\s*;)[^\n]*\n){0,40}?[^\n]*?\K\b(?:this\.)?\w*(?:[Qq]ueue|[Mm]ail\w*|[Bb]us|[Ee]mitter|[Pp]roducer)\w*\.(?:add|send\w*|publish|emit)\(' -g '*.{ts,js}' "${X[@]}" "${V2ROOTS[@]}"; ck SE2b $?
v1g SE2c '(?:->afterCommit\(\))|\$afterCommit\s*=\s*true|\bShouldDispatchAfterCommit\b|\bShouldHandleEventsAfterCommit\b|DB::afterCommit\(|[\x27"]after_commit[\x27"]\s*=>\s*true' '\bdeferrable\s+initially\s+deferred\b|\bcreate\s+constraint\s+trigger\b'
# 3. Hidden consumers: views, grants to non-app logins, export headers and drop targets — both sides, migrations included.
rg -n -i --pcre2 'create\s+(?:or\s+replace\s+)?(?:materialized\s+)?view\s+\w+|\bgrant\s+select\b|\bfputcsv\(\s*\$\w+\s*,\s*\[|Storage::disk\(\s*\x27(?:sftp|ftp|s3)\x27' -g '*.{php,sql}' "${X[@]}" "${V1ROOTS[@]}"; ck SE3a $?
rg -n -i --pcre2 'create\s+(?:or\s+replace\s+)?(?:materialized\s+)?view\s+\w+|\bgrant\s+select\b|[\x27"`]\w+(?:,\w+){2,}[\x27"`]|\b\w*sftp\w*\.(?:put|upload)\w*\(|\bputObject\(' -g '*.{ts,js,sql,py}' "${X[@]}" "${V2ROOTS[@]}"; ck SE3b $?
# 4. Jobs: every schedule and consumer on both sides (I-SCHED pairs them); for each V1-ONLY job, the V2 lines naming its target.
v1g SE4a '\bSchedule::(?:command|job|call)\(|\$schedule->(?:command|job|call)\(|\bimplements\s+[^{]*\bShouldQueue\b' '\bcron\.(?:schedule|alter_job|unschedule)\s*\('
rg -n --pcre2 '@(?:Cron|Interval|Timeout)\(|\brepeat\s*:\s*\{|\bupsertJobScheduler\(|^\s*kind:\s*CronJob\b|^\s*schedule:\s*["\x27]|@Processor\(' -g '*.{ts,js,yaml,yml}' "${X[@]}" "${V2ROOTS[@]}"; ck SE4b $?
awk -F'\t' '$3=="V1-ONLY" && $4 ~ /^job:/{print $6}' "$OUT/candidates.tsv" | while read -r A; do T=$(printf '%s' "$A" | sed -E 's/.*target=([^;]*).*/\1/'); L=$(printf '%s' "$A" | sed -nE 's/.*target_live=([^;]*).*/\1/p'); case "$L" in no|ambiguous) printf '%s → dead in V1 (target_live=%s): its run errors every time — not a port gap; settle with cron.job_run_details\n' "$T" "$L"; continue;; esac; W=$(printf '%s' "$T" | sed -E 's/^[a-z]+://; s/([a-z])([A-Z])/\1 \2/g' | tr ' :_-' '\n\n\n\n' | awk 'length>4' | head -2 | paste -sd'|' -); [ -n "$W" ] || { printf '%s → target not named (read the job command on the V1 row)\n' "$T"; continue; }; H=$(rg -n -i --pcre2 "$W" -g '*.{ts,js,yaml,yml}' "${X[@]}" "${V2ROOTS[@]}" 2>/dev/null | grep -v -E '^[^:]+:[0-9]+:[[:space:]]*(//|\*|/\*|#)' | head -3 | tr '\n' ' '); printf '%s → %s\n' "$T" "${H:-no V2 code line names it (comments, tests and e2e specs excluded); read the paired-by-name I-SCHED rows}"; done
# 5. DB-side logic: triggers, procedures, generated columns, FK actions in V1; what V2 declares in entities, snapshots and migrations.
rg -n -i --pcre2 'create\s+trigger\b|create\s+(?:procedure|function)\b|DB::unprepared\(|->(?:storedAs|virtualAs)\(|->(?:cascadeOnDelete|nullOnDelete|cascadeOnUpdate)\(\)|->onDelete\(\s*\x27(?:cascade|set null)\x27' -g '*.{php,sql}' "${X[@]}" "${V1ROOTS[@]}"; ck SE5a $?
rg -n -i --pcre2 '\b(?:deleteRule|updateRule|onDelete|onUpdate)\s*:\s*[\x27"]|"(?:deleteRule|updateRule)"\s*:\s*"|create\s+trigger\b|create\s+(?:or\s+replace\s+)?function\b|\bformula\s*:|\bgenerated\s+always\b' -g '*.{ts,js,sql,json}' -g '!**/package*.json' "${X[@]}" "${V2ROOTS[@]}"; ck SE5b $?
for R in "$V1" .; do [ -n "$R" ] && find "$R" -newer "$OUT/stamp" -type f -not -path '*/node_modules/*' | head -3; done; echo "write check done (empty = nothing written)"
```

Build the effect table before judging: one row per (entity, verb) with V1's kinds (I-SIDE plus SE1a/SE1b, following each observer method to its body) and V2's kinds (SE1c, following each subscriber to the queue or service it calls, one hop).

## Measured

Measured 2026-10-18 on this repo's fixtures, and 2026-10-19 on one real Supabase → Nest port (read-only).

- **A real Supabase → Nest port** (2026-10-19). Before: SE1a/SE1b/SE2c/SE4a read `*.php` (0 V1 lines) and the I-SIDE lane had 4 V2 rows. After: SE1a 472 · SE1b 85 · SE2c 10 · SE4a 43; I-SIDE V2 rows 175, I-SCHED V2 rows 60; the 4 dead V1 jobs print `dead in V1` instead of a lookup. `port-pair`: the same lines, minus two `// Ported from …` comment hits in the V1-target lookup.

- **`port-pair`, paired** (`--live-v1`). Engine (the build whose candidate rows carry a `lane` column): I-SIDE V1-ONLY `order.updated` (mail) and `wallet.updated` (activity); I-SCHED V1-ONLY `wallets:expire-credits` and `ReleaseStaleReservations`; I-SCHEMA V1-ONLY `derived:order.line_count how=trigger` and `view:finance_invoice_totals`, and `fk:ticket_message(ticket_id) on_delete cascade → no action` CHANGED (the snapshot, not the entity decorator, is what V2's database has). Grep lines: SE1a 5 · SE1b 6 · SE1c 11 · SE1d 3 (every balance and credit-limit write) · SE1e 3 subscribers · SE2a-sync 4 · SE2a 2 · SE2b 1 · SE2c 1 · SE3a 8 · SE3b 5 · SE4a 9 · SE4b 9 · SE5a 6 · SE5b 18 (every snapshot FK rule, the `no action` one among them); the job-target lines point at the two ported service methods (ported, never scheduled). **The observer-only seed** (shipped e-mail) and **the trait-only seed** (wallet balance audit) are both V1-ONLY I-SIDE rows with SE1a lines (`#[ObservedBy]`, `use LogsActivity`) and no `afterUpdate` in SE1c for those entities; SE1e prints the two subscribers' `return [Order]` / `return [Wallet]` lines the findings cite, and SE1d lists the three V2 writes the missing hook leaves unaudited. The decoys (ticket SMS moved to a notifications-module subscriber with a replication guard, the invoice audit row from a V2 trigger, the weekly report CronJob, the nightly invoice `@Cron`) each match their V1 row on reading.
- **Solo** (re-recorded inventory with `I-SCHED` faulted): I-SIDE rows as above tagged `solo`; I-SCHED `blocked (extractor changed since record; re-record)`, so §4 prints `blocked`; the V1 greps read an empty directory, so triggers and views (not in any recorded lane) are Unconfirmed-solo; the recorded `fk:ticket_message(ticket_id) on_delete=cascade` row against SE5b is the one SE guarantee row that can become a Finding.
- **V2-only fixtures** (no V1): `ds-defects` SE1c 19 · SE2a-sync 8 · SE4b 41 (an event-heavy fixture: these are the inventory, not noise); `backend-defects` SE1c 5 · SE4b 12; `slow-marketplace` SE1c 4 · SE3b 2 · SE5b 2; `obs-defects`, `quality-mix` ≤ 2.

## The 3,000-row path

1. **Table, not lines.** Collapse SE1a–SE1c into the (entity, verb) → kinds table; one V1 trait or observer missing in V2 is **one finding with N verbs** (`LogsActivity` covers created, updated and deleted; precedents § 27).
2. **Read in this order:** effects on money and stock writes, customer-facing e-mail and SMS, audit rows, then jobs, then consumers, then the rest.
3. **Group subscribers** by module before searching: an effect "missing" from the orders module is often in a notifications or integrations module (the counterpart rule, § 1).
4. **Close a group with one checked reason** (`12 V1 listeners on framework-internal events: none emits an external effect`). Effects on write routes are never bulk-closed by name.
5. **Ledger the rest** as `Live, unreviewed (k groups / n lines)`.

## Scans for

| § | Class | Finding when (after the counterpart search) | Default severity | Solo | Oracle |
|---|---|---|---|---|---|
| 1 | MG-SE-1 side effect dropped | the V1 (entity, verb) kinds ⊄ V2's | high for customer-facing, money or audit effects; medium for cache or search refresh | Unconfirmed-solo | V371 |
| 2 | MG-SE-2 duplicated or reordered | V2 repeats an effect V1 already sent in the dual-run window, or fires before commit where V1 waited | high (a customer gets it twice; a job acts on a rolled-back row) | Unconfirmed-solo | V371 |
| 3 | MG-HC-1 hidden consumer broken | a V1 view, grant, export or drop that a non-app consumer reads has no V2 twin, or its name or columns changed | high | Unconfirmed-solo | V372 |
| 4 | MG-JB-1 job or consumer not ported | a V1 schedule or queue consumer has no V2 entry with the same expression, zone and overlap rule | high when it moves money or stock or releases a hold; medium for reports | Unconfirmed-solo (blocked when the I-SCHED record is stale) | V373 |
| 5 | DM-10 DB-side logic not reproduced | a V1 trigger, procedure, generated column or FK action has no V2 DDL or code path | high | **Finding** for a lost FK action; triggers Unconfirmed-solo | V371 |

### 1. Side effect dropped (MG-SE-1)

```
BAD:   V1  OrderObserver::updated → Mail::to(…)->queue(new OrderShippedMail)  (attached by #[ObservedBy]; no controller calls it)
       V2  OrderSubscriber handles afterCreate only; nothing enqueues 'order-shipped'
       V1  Wallet uses LogsActivity ->logOnly(['balance_minor', …])          V2  WalletActivitySubscriber ports afterCreate and afterDelete — no afterUpdate
GOOD:  V2  afterUpdate on the status change enqueues 'order-shipped'  ·  afterUpdate logs the wallet change, as the trait did
```
**Read both ends.** Which verbs does each V1 observer, trait and listener cover (a trait logs every dirty event its options allow; SE1d lists every V2 write to a column it logs)? For each, which V2 subscriber, `@OnEvent` listener, service call or DB trigger produces the same kind — in **any** module, read one hop into the queue name or service? Is the V2 effect conditional on the same change (status → shipped)? Does the V2 subscriber for that entity (SE1e) have the hook for every verb V1 covered? **Finding when** a (entity, verb) kind V1 emits on a live path is produced nowhere in V2. **Proof:** V371 — the effect journal per (entity, verb) on create, update, delete and restore.

### 2. Duplicated or reordered (MG-SE-2)

```
BAD:   V2  OrderSubscriber.afterCreate mails 'order-placed' — also for rows the V1 → V2 sync inserts while V1 still mails them
       V1  ProcessInvoiceIssued::dispatch($invoice)->afterCommit()       V2  await this.queue.add('invoice-issued', …) inside tx.run
GOOD:  V2  if (isReplicatedWrite(args)) return;  ·  onCommit(() => this.queue.add('invoice-issued', …))
```
**Read both ends.** Is there a dual-run window (SE2a-sync: a sync, CDC or replication path writing V1 rows into V2)? During it, which side owns the customer-facing effect, and does every V2 subscriber that emits check for a replicated write (SE2a lists those that never do; an internal audit row is a data question, an e-mail or webhook is the finding)? For commit timing: did V1 defer the dispatch (SE2c), and does V2's transaction runner offer an `onCommit` hook the call ignores? **Finding when** an effect V1 sent once is sent twice, or runs on a rolled-back or not-yet-visible row. **Proof:** V371 in dual-run mode (the customer journal shows 2), and with a fault after the enqueue.

### 3. Hidden consumer broken (MG-HC-1)

```
BAD:   V1  CREATE VIEW finance_invoice_totals … ; GRANT SELECT … TO reports_ro      V2  only finance_wallet_movements is recreated and granted
       V1  fputcsv($out, ['sku', 'qty_available', 'updated_at'])                     V2  'sku,available,updatedAt'
GOOD:  V2  the view and its grant in a migration  ·  V1's header kept (or a dated retirement signed by the consumer's owner)
```
**Read both ends.** Who reads it — a login other than the app's (grants), a partner importer (SFTP, S3), a BI workbook, another repository's query? Does the consumer read by name (a CSV header, a view column)? After which cutover step does the V1 object freeze? **Finding when** a non-app consumer of a V1 object finds it missing, renamed or reshaped in V2 with no dated retirement. **Proof:** V372 — the consumer inventory: every non-app login, view, export and drop maps to a V2 twin or a signed retirement.

### 4. Job or consumer not ported (MG-JB-1)

```
BAD:   V1  Schedule::command('wallets:expire-credits')->dailyAt('00:15')->timezone('Asia/Riyadh')->onOneServer();
       V2  PromoCreditService.expireAll() ported and injected into Schedules — no @Cron, repeat or CronJob calls it
GOOD:  V2  @Cron('0 15 0 * * *', { name: 'wallets-expire-credits', timeZone: 'Asia/Riyadh' })   (single-runner as V1's onOneServer)
```
**Read both ends.** For each V1 entry: expression, zone, overlap guard (`withoutOverlapping`), one-server rule. For each V2 candidate: `@Cron` (on a single-replica scheduler?), BullMQ repeat, a k8s `CronJob` (zone set? `concurrencyPolicy`?). The job-target lines show a ported method nothing schedules. A cron moved to a CronJob with the same zone and an ADR is the control; a stricter overlap guard on V2 is Hardening. **Finding when** a V1 entry has no V2 entry, or runs at another expression or zone. **Proof:** V373 — schedule equality plus one dry run on a snapshot.

### 5. DB-side logic not reproduced (DM-10)

```
BAD:   V1  CREATE TRIGGER order_lines_after_insert … UPDATE orders SET line_count = line_count + 1   V2  lineCount column, default 0, nothing maintains it
       V1  $table->foreignId('ticket_id')->constrained('tickets')->cascadeOnDelete();               V2  snapshot "deleteRule": "no action" for ticket_messages (whatever the entity decorator says)
GOOD:  V2  a formula, trigger or code path for line_count  ·  deleteRule 'cascade' in the entity **and** a migration that creates it
```
**Read both ends.** Which V1 columns change with no PHP code touching them (a trigger, a generated column, a cascade)? What does V2 declare in the entity, the migration and the schema snapshot — and do they agree? The migration (and the snapshot it was generated from) is what the database has; an entity decorator nobody generated a migration for changes nothing. Is the V2 behaviour stricter (no action: a delete now fails) or looser (orphans)? **Finding when** a row V1's database changed by itself is not changed on V2, or a delete that cascaded in V1 fails or orphans in V2. **Proof:** V371 — the row-delta journal on insert and delete.

## Output

```
side-effect-parity-scan — paired · laravel 11.31.0 → nest 11.0.6 + mikro-orm 6 + bullmq · sync: scripts/sync (3), deploy/cdc (1)

Findings: 2 · Unconfirmed: 5

1. v2/apps/api/src/orders/order-events.subscriber.ts:15           [report-flagged]   high
   §1 order.updated mail dropped — V1 OrderMailObserver::updated (v1/app/Observers/OrderMailObserver.php:21), attached by
   #[ObservedBy] (Order.php:16). V2: no afterUpdate in any subscriber; no 'order-shipped' enqueue anywhere.
   Unproven link: no journal run. Settling probe: V371 update path, status → shipped, Mailpit shows 1 on V1, 0 on V2.
2. v2/apps/api/src/migrations/.snapshot-api.json:212             [report-with-fix]  high
   §5 FK action lost — V1 ticket_messages.ticket_id cascadeOnDelete (…_create_tickets_tables.php:29); the V2 schema
   says "no action" although the entity decorator says cascade (no migration carries it). Proof: V371 delete of a
   ticket with messages: V1 deletes both, V2 fails on the FK.

Verification: 14 candidates → 2 findings · 5 unconfirmed · 1 hardening · 0 pre-existing · 6 refuted

Class coverage:
  §1  effect dropped         checked (I-SIDE 2 V1-ONLY, SE1a 5 → 2; ticket SMS moved to notifications subscriber)
  §2  duplicated / early     checked (SE2a 2, SE2b 1 → 2)
  §3  hidden consumer        checked (SE3a 4 objects → 2)
  §4  job not ported         checked (I-SCHED 2 V1-ONLY → 2; weekly report = k8s CronJob, ADR-0013)
  §5  DB-side logic          checked (SE5a 3 rules + 1 trigger → 2)
```

`[report-with-fix]`: both ends cited, the search written out, the journal (or the two-ended static fact for a lost FK action) fired, and the fix local. `[report-flagged]`: one link unproven; the row names the probe. Every run prints all five §s as `checked (k candidates → m)`, `N/A (<reason>)`, `blocked (<reason>)` or `Unconfirmed-solo (k)`.

## Precedents

The verifier reads [`precedents/migration.md`](../../../../snippets/precedents/migration.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4: § 1 the counterpart search, § 2 dead V1, § 3 intentional breaks, § 21 solo, § 24 stale records, § 26 pair-map reasons, § 27 one wiring row, § 28 counterparts outside the app (a trigger, a CronJob), § 32 observer and trait effects. Oracles: [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Migration, V371–V373.

## When to run

- On every whole-repo `/compare-v1`, printing all five §s.
- On a diff that ports a model, a service that writes, a subscriber, a job or schedule, a migration, an export, or a sync script; before a write flip.

## Halt conditions

- Do not report a high row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md). Under `/compare-v1` that is `@parity-auditor` in refute mode plus `@verifier` on every HIGH. Run standalone, apply the protocol as a separate second pass, tag rows `self-verified`, and keep the rest Unconfirmed, Hardening or Refuted. Never drop them.
- **Solo mode never prints GO.** Only a lost FK action (§5) can become a Finding from the recorded I-SCHEMA row plus the V2 search; every other row is `Unconfirmed-solo` with "re-run with `--v1=<path>`" (precedents § 21), and a stale or re-hashed lane is `blocked` (§ 24).
- Do not call an effect missing before searching every V2 module, the V2 migrations, deploy files and `pair-map.tsv`; write the search into the row.
- Do not count keyword hits as effects; follow each call to its queue, mailer or table.
- Do not mark a behaviour row `[report-with-fix]` without the journal (V371) or the consumer and schedule inventories (V372, V373).
- Do not print "effects are at parity" without the class-coverage block; a blocked lane or grep is `blocked`, never `checked`.

## Related

- `paired-inventory` (I-SIDE, I-SCHED, I-SCHEMA), `surface-parity-scan`, `semantics-parity-scan`, `cutover-routing-scan` §3 (shadow isolation), `data-cutover-orchestrate` (this pack); `/compare-v1`, `@parity-auditor`, `/find-and-fix --from-audit`.
- Database `transaction-scan` §1 and `schema-integrity-scan` §2; distributed-systems `dual-write-scan` §1–§2; backend `job-lifecycle-scan` §4–§6 — each when its pack is installed.
