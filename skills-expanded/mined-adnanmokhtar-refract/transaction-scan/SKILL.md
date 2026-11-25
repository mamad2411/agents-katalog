---
name: transaction-scan
description: Find transactions that hurt the database — external I/O held inside one, multi-step writes without one or on the wrong handle, inconsistent lock order, SERIALIZABLE or optimistic locks with no retry, queue claims without SKIP LOCKED, long transactions, write skew, lost updates on non-abuse fields, hot rows and savepoints in loops.
kind: skill
pack: database
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: transaction-scan

## Premise

A transaction is a promise with a cost. It promises that a group of writes lands together and that concurrent work sees a consistent state. It costs row locks, a pooled connection and a pinned xmin horizon for as long as it stays open. The defects in this class are the two sides of that bargain. Some code breaks the promise: writes that are not in the transaction they appear to be in, an isolation level that allows the anomaly the code assumes away, a retry that never happens. Other code overpays: a payment call made while the order row is locked, a 10,000-row loop in one transaction, every request writing the same counter row, a savepoint per item. None of these shows up in a unit test with one user. They show up under concurrency, as `40P01`, `idle in transaction`, pool exhaustion, or a total that is short by the lost updates.

**Every finding cites the transaction's opener `<file:line>` (or the write that lacks one) + the statement or call that breaks the rule + the entry point that reaches it + the proof (or the settling test) + the fix in the project's own transaction API.** A grep hit is never a finding by itself. "No transaction defects" is never printed without the class-coverage block (§ Output).

**Detect statically, prove by execution, measure impact last.** The proofs are concurrency and fault oracles: an interleaving that breaks an invariant, a deadlock count, an injected failure that leaves partial state, an `idle in transaction` session during a stubbed slow call. A candidate read in code with no harness is **Unconfirmed** and carries the test that would settle it. A race read from code with no primitive between check and act stays a candidate even when one run of the probe does not reproduce it, because the window can be microseconds.

## The rule

A candidate is a finding when all four hold:

1. **The transaction boundary is where the code assumes it is not.** Something runs inside it that should not (I/O, a data-sized loop, a savepoint per item), or a write the code treats as atomic runs outside it (no transaction, the wrong handle, a raw statement on another pooled connection).
2. **The interleaving or load that breaks it really occurs.** Two workers, two requests, a retry, a webhook redelivery, a burst. A path with one writer per key by construction fails here.
3. **A production entry point reaches it.** Route, consumer, cron, webhook. Seeds, tests and one-off scripts fail here, unless they run in production.
4. **No control already closes it.** A single atomic statement, a unique or exclusion constraint, `FOR UPDATE` taken in the same transaction, a version guard with a retry, an outbox row, an after-commit hook.

## Boundaries

**With `logic-race-scan` (security pack, when installed), in both directions:**

- **There:** a check-then-act, read-modify-write or find-or-create on a value someone gains from — money, credit, balance, stock, quota, seats, votes, trials, coupons and every single-use code or token. Missing idempotency on side-effect endpoints. The per-role authorization matrix. Grep 8b counts these hits (value vocabulary) and this skill never reports them. Its coverage line says `→ logic-race-scan (k)`, and the audit dedupes by `<file:line>` and credits security. **Without the security pack**, this skill reports them under §7 / §8, tagged `security-class (owner pack not installed)`.
- **Here:** the transaction mechanics behind every fix that skill proposes. A fix that raises the isolation level needs §4's retry. A fix that locks two rows needs §3's lock order. A fix that wraps check and act in one transaction must not hold an outbound call inside it (§1). A worker claim is §5. Here also goes every isolation anomaly on a field nobody gains from: a view counter, a denormalized aggregate two workers recompute, a status two consumers write, a JSON settings blob two editors merge.
- **Both fit:** credit security when its pack is installed, and list the row here as `owner: security`.

**Elsewhere:**

- Pool size, a session-level advisory lock or session `SET` behind a transaction-mode pooler, and the database-side backstops (`statement_timeout`, `idle_in_transaction_session_timeout`, `lock_timeout`) → `connection-config-scan` (this pack). §1 and §6 cite its §6 when the backstop is missing.
- A query or write per loop element → `n-plus-one-scan` (this pack). The transaction around the loop is §6 or §10 here.
- Transactions inside migrations (DDL, `CONCURRENTLY` in a transactional migration, a backfill in a DDL transaction) → `migration-safety` (this pack). A constraint that would replace an app-level check, and gapless numbering → `schema-integrity-scan` §3, §6 and §11.
- Tenant context set at session scope → `@tenant-isolation-reviewer` (security pack, when installed).
- Where a service opens and closes its transaction (the design) is backend's `transaction-boundary` pattern when the backend pack is installed. Cross-service atomicity, idempotency and leader locks belong to the distributed-systems patterns `idempotency` and `distributed-lock` when that pack is installed. Without them, the fix lines below are the contract.

## Adapt to the codebase

Read the engine and its version (compose image, Terraform, `SELECT version()`), and read the ORM and its version from the lockfile. Default isolation differs by engine, and APIs changed in the last major of MikroORM, TypeORM and Prisma. Print the lanes you ran in the output header. The statement counters and query loggers used by the proofs are the last column of `database/skills/n-plus-one-scan/SKILL.md` § "Adapt to the codebase — the shared ORM lane table".

**Engine defaults** (Hermitage matrix, CC BY 4.0; Jepsen MySQL 8.0.34, 2023-12-19; PostgreSQL 18 docs):
- **Postgres** defaults to READ COMMITTED. It allows lost update and write skew there. REPEATABLE READ is snapshot isolation: a lost update aborts with `40001`, and write skew is still allowed. SERIALIZABLE (SSI) prevents both, and any statement can fail with `40001`.
- **MySQL / InnoDB** defaults to REPEATABLE READ. A plain `SELECT` reads a snapshot, while DML and locking reads see the latest committed row. Jepsen measured lost updates and write skew at that default. Deadlocks surface as `1213`, lock waits as `1205`.
- **SQLite** runs one writer at a time, with no isolation within one connection.

| Lane | Open · the handle every statement must use (§2) | After-commit hook (§1 fix) | Isolation · retry signal (§4) | Row lock · skip locked (§3, §5) | Savepoint source (§10) |
|---|---|---|---|---|---|
| **MikroORM** 6 / 7 | `em.transactional(cb)`: the callback gets a fork, and injected EMs follow the context. `@Transactional()` defaults to `REQUIRED` in 7 (`REQUIRES_NEW` in 6). Escape: raw `em.getConnection().execute(sql, params, method)` **without** `em.getTransactionContext()` as the fourth argument runs on another pooled connection | `afterTransactionCommit` subscriber event | `{ isolationLevel: IsolationLevel.SERIALIZABLE }`; `@Property({ version: true })` → `OptimisticLockError` | `lockMode: LockMode.PESSIMISTIC_WRITE` (the enum, never a number); `PESSIMISTIC_PARTIAL_WRITE` = `for update skip locked` | a nested `em.transactional` defaults to `NESTED`, which is a savepoint (7.2 docs). `flush()` wraps its changes in one transaction |
| **TypeORM** 0.3 / 1.x | `dataSource.transaction(async (manager) => …)`; `queryRunner.startTransaction()` (must `release()`). Escape: injected repositories or `dataSource.manager` inside the callback | none: run after the awaited call | `dataSource.transaction('SERIALIZABLE', cb)`. `@VersionColumn` is **not** checked by `save()`: compare-and-set by hand | `.setLock('pessimistic_write')` + `.setOnLocked('skip_locked')` | confirm in the query log |
| **Prisma** 6 / 7 | interactive `$transaction(async (tx) => …, { maxWait, timeout, isolationLevel })`: defaults 2,000 / 5,000 ms. Escape: `prisma.` inside the callback. Batch `$transaction([…])` | code after the awaited `$transaction` | `isolationLevel: 'Serializable'`; write conflicts `P2034` (research catalog; confirm per version) | tagged `$queryRaw` with `FOR UPDATE SKIP LOCKED` | confirm in the query log. Prisma 8 (RC): no transaction timeout, and a nested `db.transaction` does not nest |
| **Sequelize** 6 | `sequelize.transaction(async (t) => …)`: every call needs `{ transaction: t }` unless `Sequelize.useCLS(ns)` | `t.afterCommit(fn)` | `isolationLevel` option | `lock: t.LOCK.UPDATE` | `findOrCreate` runs with savepoints |
| **Drizzle / Knex / pg** | `db.transaction(async (tx) => …)`, `knex.transaction(async (trx) => …)`, `client.query('BEGIN')` on a checked-out client. Escape: `db.` / `knex(` / `pool.query` inside | after the awaited call | `isolationLevel` option / `SET TRANSACTION ISOLATION LEVEL` | Knex `.forUpdate().skipLocked()`; raw `FOR UPDATE SKIP LOCKED` | Drizzle nested `tx.transaction()` is a savepoint |
| **Django** | `transaction.atomic()`; `ATOMIC_REQUESTS = True` wraps every view | `transaction.on_commit(fn)` | `OPTIONS` isolation; catch the driver's `40001` | `select_for_update(skip_locked=True)` inside `atomic()` | nested `atomic()`, and `get_or_create` inside one |
| **SQLAlchemy** 2 | `with Session.begin():` per unit of work | `after_commit` session event | `execution_options(isolation_level=…)`; `version_id_col` → `StaleDataError` | `with_for_update(skip_locked=True)` | `session.begin_nested()` |
| **Rails** | `Model.transaction do … end` | `after_commit` callbacks; read the version's job enqueue-after-commit setting, which changed across 7.2–8.2 | `transaction(isolation: :serializable)`; `lock_version` → `StaleObjectError` | `lock("FOR UPDATE SKIP LOCKED")`, `with_lock` | `transaction(requires_new: true)` |
| **Laravel** | `DB::transaction(fn, $attempts)`: the second argument retries on deadlock | `DB::afterCommit()`, `->afterCommit()` on jobs and events | `$attempts`, or catch the driver code | `lockForUpdate()`, `->lock('for update skip locked')` | a nested `DB::transaction` |
| **Spring / JPA** | `@Transactional` (proxy: self-invocation and private methods bypass it; checked exceptions do not roll back), `TransactionTemplate` | `@TransactionalEventListener(phase = AFTER_COMMIT)` | `@Transactional(isolation = …)`; `@Version` → `ObjectOptimisticLockingFailureException` | `@Lock(PESSIMISTIC_WRITE)`; native `FOR UPDATE SKIP LOCKED` | `Propagation.NESTED` |
| **Go** (`database/sql`, GORM) | `db.BeginTx(ctx, opts)` + `defer tx.Rollback()`; `db.Transaction(func(tx *gorm.DB) error {…})`. Escape: `db.` inside | after `Commit()` | `sql.TxOptions{Isolation: sql.LevelSerializable}` | `FOR UPDATE SKIP LOCKED`; GORM `clause.Locking{Strength: "UPDATE", Options: "SKIP LOCKED"}` | a nested GORM `tx.Transaction` |
| **EF Core** | `await db.Database.BeginTransactionAsync(…)`; `SaveChanges` is one transaction by itself | after `CommitAsync` | the level argument; concurrency tokens → `DbUpdateConcurrencyException` | raw `FOR UPDATE SKIP LOCKED` | `SaveChanges` inside a user transaction creates a savepoint per call |
| **MongoDB** | `session.withTransaction(fn)`; 60 s lifetime by default | after the callback | retry on the `TransientTransactionError` label | the atomic update with a predicate | — |

A project usually wraps its ORM's opener in a **transaction port** (`tx.run(…)`, `unitOfWork.execute(…)`, `withTransaction(…)`). Grep 0b finds the wrapper. Read it once and record which ORM semantics it inherits: context propagation (MikroORM, CLS libraries) or an explicit handle (Prisma, TypeORM, Knex), then extend `TXW` with its call shape.

## Pre-flight greps

Run as **one** script from the repo root (shell state does not survive between tool calls). Grep **N** feeds detector **§N**; grep 0 is context. Every `rg` names its path (`.`): given no path, `rg` reads stdin whenever stdin is a pipe, and under an agent's shell that is a silent zero-hit run. Variables are written `${NAME}`: under zsh, `$NAME[…]` is an array subscript. Any `rg` error on stderr (exit 2) is a failed grep, never zero hits. `-A40` windows overreach past a short transaction: `WIN` cuts a window at the closing brace of the block the opener line opens and tags every line `[tx opened :N]`; a `BEGIN`, `BeginTx` or decorator opener keeps its 40 lines, so check those hits sit inside the transaction. Per-run files live in `$T` (`mktemp -d`), never at a fixed path.

```bash
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/target/**' -g '!**/.venv/**' -g '!**/.next/**'
   -g '!**/generated/**' -g '!**/temp/**' -g '!*.{md,mdx,json,lock,snap,map,svg,txt,csv}' -g '!**/*.min.*' -g '!**/docs/**' -g '!/ai/**'
   -g '!**/{test,tests,spec,e2e,__tests__,__mocks__,mocks,__snapshots__,fixtures,__fixtures__,testdata,seeds,seeders,factories}/**'
   -g '!**/*{.,_,-}{test,spec,e2e-spec,mock,stories,test-data}.*' -g '!**/test_*.py' -g '!**/conftest.py'
   -g '!**/migrations/**' -g '!**/db/migrate/**' -g '!**/{locales,locale,i18n,translations}/**')
NC=(rg -v --pcre2 '^[^:]+[:-]\d+[:-]\s*(//|/\*|\*(\s|/|$)|#(?!\{)|<!--|--\s)')   # drops comment-only hit and context lines
TXO='\$transaction\(|\.transactional\(|@Transactional\b|\b(dataSource|manager|entityManager|em|orm|sequelize|knex|db|database|conn|connection|client|prisma|tx|trx)\.transaction\(|\b(start|begin)Transaction\(|\bwithTransaction\(|\.query\(\s*["\x27\x60]BEGIN\b|\btransaction\.atomic\b|\bATOMIC_REQUESTS\b|\bbegin_nested\(|\bsession\.begin\(|\btransaction(\(\s*\w+:[^)]*\))?\s+do\b|DB::(transaction|beginTransaction)\(|\.Transaction\(\s*func\b|\.BeginTx?\(|\bBeginTransaction(Async)?\(|\bTransactionTemplate\b|\bRepo\.transact(ion)?\('
TXW='\b(this\.)?(tx|txn|trx|uow|unitOfWork|transaction(Port|Service|Manager|Runner)?)\.(run|execute|transaction|transactional|wrap|perform|inTransaction|withTransaction)\('   # extend with 0b
IO='\bfetch\(|\baxios(\.\w+)?\(|\bgot(\.\w+)?\(|\bky\.\w+\(|\bhttpService\.\w+\(|\bthis\.http\.\w+\(|\bHttp::\w+|\bGuzzle|\b(requests|httpx|aiohttp)\.\w+\(|\burlopen\(|Net::HTTP|HTTParty|Faraday|RestClient|\b(restTemplate|webClient|restClient|httpClient)\.\w+\(|\bhttp\.(Get|Post|Do)\(|\bclient\.Do\(|\b(Get|Post|Put|Send)Async\(|\b\w*[qQ]ueue\.add(Bulk)?\(|\.(publish|sendMessage|produce|enqueue|perform_later|perform_async|delay|apply_async)\(|\b(producer|kafkaTemplate|rabbitTemplate|jmsTemplate|sqs|sns|pubsub)\.\w+\(|Mail::\w+|\b(mailer|mailService|transporter|mailSender)\.\w+\(|\bsend_?[mM]ail\(|\.deliver_now\b|\bstripe\.\w+\.|Stripe::|\b(openai|anthropic)\.\w+|\.(messages|completions)\.create\(|\bs3\.\w+\(|\bPutObjectCommand\b|\bsetTimeout\(|\btime\.sleep\(|\bThread\.sleep\('
OUT='\b(this\.|self\.|@)?\w*(client|Client|gateway|Gateway|provider|Provider|Api|psp|Psp|mailer|Mailer|sms|Sms|notifier|Notifier|webhook|Webhook|publisher|Publisher|producer|Producer|storage|Storage|bucket|Bucket|llm|Llm|sender|Sender|dispatcher|Dispatcher)s?\.(?!(query|release|connect|end|execute|transaction|begin|commit|rollback)\b)\w+\(|\b(this\.|self\.|@)?\w*(carrier|Carrier|courier|Courier|payment|Payment|notification|Notification)\.(?!(query|release|connect|end|execute|transaction|begin|commit|rollback|find\w*|get\w*By\w*|count\w*|exists\w*|save\w*|persist\w*|insert\w*|upsert\w*|delete\w*|remove\w*|load\w*|lock\w*)\b)\w+\('   # domain nouns name repositories too: singular receivers only, repository verbs dropped
LOOP='\bfor\s*\(|\bfor\s+await\b|\.forEach\(|\bwhile\s*\(|\.map\(\s*async\b|^\s*for\s+\w+(\s*,\s*\w+)*\s+in\s|\.(each|find_each|find_in_batches)\s+do\b|\bforeach\s*\(|\bfor\s+[\w, _]+:=\s*range\b|\bEnum\.(map|each)\('
C='balance|credits?|stock|quantity|qty|points|uses|use_?count|used_?count|usage_?count|redemptions?|remaining|seats|quota|inventory|available|votes?|price|amount|total|wallet|refund|payout|fee|cents'   # value fields → logic-race-scan
T="$(mktemp -d "${TMPDIR:-/tmp}/txscan.XXXXXX")"   # per-run files: two runs never share one
cat > "$T/win.py" <<'PY'
# Cut each `rg -n -A40 --null` window at the closing brace of a block the opener line opens (`tx.run(async () => {`);
# a BEGIN / BeginTx / decorator opener keeps its 40 lines. Each line is tagged with the opener's line number.
import re, sys
op = None
for raw in sys.stdin.buffer:
    s = raw.decode('utf-8', 'replace').rstrip('\n')
    if s == '--': op = None; continue
    f, _, rest = s.partition('\0'); m = re.match(r'(\d+)([:-])(.*)', rest)
    if not m: continue
    n, k, t = m.groups()
    if k == ':': op = [f, n, 0, t.count('{') > t.count('}')]   # cut only when the opener line opens the block (a callback)
    if not op or op[0] != f: continue
    op[2] += t.count('{') - t.count('}')
    print('%s%s%s%s%s  [tx opened :%s]' % (f, k, n, k, t, op[1]))
    if op[3] and op[2] <= 0: op = None
PY
WIN=(python3 -I -B "$T/win.py")
for t in js ts py go java kotlin ruby php cs elixir; do printf '%s=%s ' "$t" "$(rg --files -t "$t" "${X[@]}" . | wc -l | tr -d ' ')"; done; echo   # 0 = lane absent

# 0. Context. 0a every opener (the population §1, §2, §4, §6 and §10 read); 0b the project's wrappers around them.
rg -n --pcre2 "${TXO}|${TXW}" "${X[@]}" . | "${NC[@]}"
rg -l0 --pcre2 "${TXO}" "${X[@]}" . | xargs -0 -r rg -n --pcre2 '\(\s*\w+\s*:\s*\(\s*\w+\s*:\s*(EntityManager|SqlEntityManager|QueryRunner|PrismaClient|Prisma\.TransactionClient|Knex\.Transaction|Transaction|\w*Tx\w*)\b[^)]*\)\s*=>|^\s*(export\s+)?(async\s+)?function\s+\w*([Tt]ransaction|[Aa]tomic|[Uu]nitOfWork|Tx)\w*\s*[<(]|^\s*(public\s+|private\s+|protected\s+)?(async\s+)?(run|execute|perform|inTransaction|withTransaction)\s*(<[^>]*>)?\s*\((?:[^()]|\([^()]*\))*\)\s*(:\s*[^{]+)?\{|^\s*def\s+\w*(transaction|atomic|unit_of_work)\w*\s*\(|^\s*func\s+(\([^)]*\)\s*)?\w*(Tx|Transaction)\w*\s*\('
# 1. Inside an opener's block (40 lines at most, cut at its closing brace; each line names the opener): 1a direct I/O;
#    1b a call on an outbound-named dependency (follow it one hop).
rg -n -A40 --null --pcre2 "${TXO}|${TXW}" "${X[@]}" . | "${WIN[@]}" | rg --pcre2 "^[^:]+[-:]\d+[-:].*(${IO})" | "${NC[@]}"
rg -n -A40 --null --pcre2 "${TXO}|${TXW}" "${X[@]}" . | "${WIN[@]}" | rg --pcre2 "^[^:]+[-:]\d+[-:].*(${OUT})" | "${NC[@]}"
# 2. Writes outside the transaction they sit in: 2a the outer client inside a handle-passing callback; 2b MikroORM raw execute
#    inside one (is the transaction context passed?); 2c a callback taking no handle from a helper that passes one; 2d Sequelize
#    calls without { transaction }; 2e Django catching a database error inside atomic().
rg -n -A30 --pcre2 '\$transaction\(\s*async\s*\(\s*\w+|\.transaction\(\s*(["\x27]\w[\w ]*["\x27]\s*,\s*)?(async\s*)?\(?\s*\w+\s*\)?\s*=>|\.Transaction\(func\(\w+ \*gorm\.DB\)' "${X[@]}" . | rg --pcre2 '^[^:]+-\d+-.*(\b(this\.)?prisma\.\w+\.\w+\(|\bthis\.\w+(Repository|Repo)\.\w+\(|\b(dataSource|AppDataSource)\.(manager|getRepository)\b|\bgetRepository\(|\b(knex|db)(\(\s*["\x27]|\.(select|insert|update|delete|query|execute)\()|\bdb\.(Create|Save|Updates?|Delete|First|Find|Exec|Raw|Model|Where)\()' | "${NC[@]}"
rg -n -A30 --pcre2 "\.transactional\(|${TXW}" "${X[@]}" . | rg --pcre2 '^[^:]+-\d+-.*getConnection\([^)]*\)\s*\.execute\b' | "${NC[@]}"
rg -n --pcre2 '\b(withTransaction|transaction)\(\s*async\s*\(\s*\)\s*=>' "${X[@]}" . | "${NC[@]}"
rg -n -A30 --pcre2 'sequelize\.transaction\(\s*async' "${X[@]}" . | rg --pcre2 '^[^:]+-\d+-.*\.(create|update|destroy|findOne|findAll|save|increment|bulkCreate|upsert)\((?![^)\n]*\btransaction\b)'
rg -n -U --pcre2 'with\s+transaction\.atomic\(\)[^\n]*:\n(?:[ \t]+[^\n]*\n){0,25}?[ \t]+except\s+(IntegrityError|DatabaseError)\b' -t py "${X[@]}" .
# 3. Lock acquisitions (3a) and the files taking two or more (3b): the input to the lock-order table.
LOCK='\bfor\s+(no\s+key\s+)?update\b|\bfor\s+share\b|forUpdate\(|lockForUpdate|select_for_update|with_for_update|\bwith_lock\b|\.lock!|LockMode\.PESSIMISTIC\w*|setLock\(|\block:\s*(\w+\.)?LOCK\.|clause\.Locking|@Lock\(|LockModeType\.PESSIMISTIC|pg_advisory_(xact_)?lock\(|\bGET_LOCK\(|\bLOCK\s+TABLE'
rg -n -i --pcre2 "${LOCK}" "${X[@]}" . | "${NC[@]}"
rg -n -i --pcre2 "${LOCK}" "${X[@]}" . | "${NC[@]}" | cut -d: -f1 | uniq -c | awk '$1 > 1'
# 4. Isolation levels and optimistic versions (4a); files setting an isolation level with no retry vocabulary (4b).
ISO='\bisolation_?[lL]evel\b|ISOLATION\s+LEVEL|\bisolation:\s*:\w+|IsolationLevel\.\w+|Isolation\.(SERIALIZABLE|REPEATABLE_READ)|\bLevel(Serializable|RepeatableRead|Snapshot)\b|["\x27](Serializable|SERIALIZABLE|RepeatableRead|REPEATABLE[ _]READ)["\x27]'
VER='\bversion\s*:\s*true\b|@Version(Column)?\b|\block_version\b|\bversion_id_col\b|\boptimisticLock\b'
RETRY='\b40001\b|\b40P01\b|\b1213\b|serialization_failure|SerializationFailure|could not serialize|deadlock_detected|DeadlockDetected|P2034|OptimisticLock(Error|Exception)|StaleObjectError|StaleDataError|ObjectOptimisticLockingFailure|CannotAcquireLock|PessimisticLockingFailure|DeadlockLoser|TransientTransactionError|ConcurrencyConflict\w*|@Retryable|\bretr(y|ies)\w*\b|\battempts\b'
rg -n --pcre2 "${ISO}|${VER}" "${X[@]}" . | "${NC[@]}"
rg -l0 --pcre2 "${ISO}" "${X[@]}" . | xargs -0 -r rg --files-without-match --pcre2 "${RETRY}"   # not -L: in rg that is --follow
# 5. Status-filtered reads in worker, relay, poller and scheduler files (5a), against the skip-locked evidence (5b).
rg --files "${X[@]}" . | rg -i '(worker|processor|consumer|relay|poller|cron|schedul|dispatch|outbox|queue|jobs?)[^/]*$' | tr '\n' '\0' | xargs -0 -r rg -n -i --pcre2 '\b(status|state)\b["\x27]?\s*(:|=|==|===|=>|\bin\b)\s*[\[(]?\s*["\x27:]?(pending|queued|ready|new|scheduled|waiting|retry|unprocessed|unsent)\b|\b(processed_?at|sent_?at|published_?at|claimed_?at|locked_?at|dispatched_?at)\b\s*(:\s*null|IS\s+NULL|__isnull|=\s*None|\.is_\(None\))' | "${NC[@]}"
rg -n -i --pcre2 'skip\s+locked|skipLocked|skip_locked|PESSIMISTIC_PARTIAL_WRITE|setOnLocked\(|SKIP_LOCKED' "${X[@]}" . | "${NC[@]}"
# 6. Loops within 40 lines of an opener (6a; also feeds §3 and §10); request-wide transactions (6b); unmanaged begins (6c).
rg -n -A40 --null --pcre2 "${TXO}|${TXW}" "${X[@]}" . | "${WIN[@]}" | rg --pcre2 "^[^:]+-\d+-.*(${LOOP})" | "${NC[@]}"
rg -n --pcre2 'ATOMIC_REQUESTS\s*[:=]\s*True|around_action\s+:\w*transaction|useGlobalInterceptors\([^)]*Transaction|APP_INTERCEPTOR[^\n]*Transaction|\bTransactionInterceptor\b' -t py -t ruby -t ts -t js -t java -t kotlin "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 'open-in-view|open_in_view|ATOMIC_REQUESTS' -g '*.{yml,yaml,properties,env,toml}' "${X[@]}" .   # 6b config half
rg -n --pcre2 '=\s*await\s+[\w.]+\.transaction\(\s*\)|\b(start|begin)Transaction\(\s*\)|DB::beginTransaction\(|\.Begin(Tx)?\(|BeginTransaction(Async)?\(|query\(\s*["\x27\x60]BEGIN\b' "${X[@]}" . | "${NC[@]}"
# 7. Write-skew shapes: a range-overlap predicate, a single "default"/"primary" flag, an at-least-one count on roles or members.
rg -n --pcre2 '\b(start|from|begin|starts|valid_from|check_in)\w*\s*(<=?|>=?|\$lte?|\$gte?|__lte?|__gte?|lte?:|gte?:)[^\n]{0,80}\b(end|to|until|ends|valid_to|check_out)\w*\b|\bis_?(default|primary|main|current)\b\s*(:|=|==)\s*(true|True|1)\b|\bisDefault\b\s*:\s*true|\bisPrimary\b\s*:\s*true|\b(count|countBy|exists|existsBy)\w*\([^)]*\b(admin|owner|role|on_?call|member)s?\b' "${X[@]}" . | "${NC[@]}"
# 8. A read-modify-write within 6 lines of a persist, on either side. 8a non-value fields (this skill); 8b value fields (→ logic-race-scan).
RMW='(?:(\.|->)\s*\w+\s*([-+]=|\+\+|--)|\b(?<f>\w+)["\x27]?\s*(:|=>|=)\s*\$?\w+(\.|->)\k<f>\s*[-+]\s*[\w.(]|\bset(?<s>[A-Z]\w*)\s*\([^)]*get\k<s>\(\)\s*[-+]|\.\.\.\s*\w+(\.\w+)?\.(settings|preferences|prefs|metadata|meta|config|options|attributes|extra|flags)\b)'
rg -n -U --pcre2 "(?J)${RMW}[^\n]*\n(?:[^\n]*\n){0,6}?[^\n]*\b(save|flush|persist\w*|update|upsert|commit|Save|Updates?|save!)\s*\(|\b(update\w*|upsert|save|persist\w*|Updates?|Save)\s*\([^\n]*\n(?:[^\n]*\n){0,4}?[^\n]*${RMW}" "${X[@]}" . | rg --pcre2 "^[^:]+:\d+:.*${RMW}" | "${NC[@]}" > "$T/rmw.txt"; rg -v -i --pcre2 "${C}" "$T/rmw.txt"
rg -c -i --pcre2 "${C}" "$T/rmw.txt"   # 8b: a count only — these rows are logic-race-scan's
# 9. Atomic increments, every one a hot-row candidate (9a); per-request "last seen" writes in auth / middleware code (9b).
rg -n --pcre2 '(?i)\bset\s+"?(\w+)"?\s*=\s*(?:"?\w+"?\.)?"?\1"?\s*[-+]|\b(increment|decrement)\s*\(|\$inc\b|\bF\(\s*["\x27]\w+["\x27]\s*\)\s*[-+]|gorm\.Expr\(\s*["\x27]\w+\s*[-+]|\braw\(\s*["\x27\x60]\w+\s*[-+]\s*\?' "${X[@]}" . | "${NC[@]}"
rg --files "${X[@]}" . | rg -i '(middleware|guard|interceptor|strateg|filter|hook|auth|session|principal)[^/]*$' | tr '\n' '\0' | xargs -0 -r rg -n -i --pcre2 '\blast_?(seen|active|activity|used|login|access(ed)?|request|ping)_?at\b|\blast(Seen|Active|Activity|Used|Login|Access|Request|Ping)(At)?\b' | "${NC[@]}"
# 10. Explicit savepoints and nested propagation (10a); an opener or savepoint-wrapping helper within 12 lines after a loop (10b).
rg -n --pcre2 '\bbegin_nested\(|requires_new:\s*true|Propagation\.NESTED|propagation:\s*\w*\.?NESTED|\bSAVEPOINT\s+\w|\bsavepoint\s*=\s*True|createSavepoint|\.savepoint\(' "${X[@]}" . | "${NC[@]}"
rg -n -A12 --pcre2 "${LOOP}" "${X[@]}" . | rg --pcre2 "^[^:]+-\d+-.*(${TXO}|${TXW}|\b(get_or_create|update_or_create|create_or_find_by|findOrCreate)\b|SaveChanges(Async)?\()" | "${NC[@]}"
```

Two blind spots are structural. Work around them; do not trust a quiet grep:
- **A port hides the I/O.** `this.carrier.book(…)` inside `tx.run` says nothing about HTTP. Grep 1b catches outbound-sounding names, and only reading catches the rest: for every opener on a write path, follow each call in the block one hop to its implementation. A call into a repository that inserts a job or outbox row in the same database is the correct pattern (precedent 6), not I/O.
- **The handle is semantic, not syntactic.** MikroORM and CLS-based transaction libraries put injected repositories inside the transaction; Prisma, TypeORM, Knex, Drizzle and GORM do not. Grep 2a assumes the second model. Read the wrapper (0b) once to know which one the project uses.

**Measured** (2026-10-15) on a real NestJS + React monorepo (MikroORM 6.6, 516 openers through one transaction port), before → after: 0b 1 → 4 (the port's `run<T>(work: () => Promise<T>)` was missed because its parameter is a function type); 1a 10 → 9 and 1b 14 → 0 (12 hits sat after the transaction's closing brace — a send after commit — and 11 were `this.couriers.create(…)`-style repository ports named after a domain noun); 6a 135 → 114; 9a 3 → 9 (`set "next_code" = "order_code_counters"."next_code" + 1`, a per-tenant hot counter, is now seen); 8b's rows go to a per-run file, so two runs no longer overwrite one shared `${TMPDIR}/tx-rmw.txt`. No fixture line was lost (a `BEGIN`-opened relay and a Go `BeginTx` keep their full windows).

Earlier measurement (2026-10-02). On the same kind of monorepo (about 5,500 TS files after exclusions), the script runs in about 8 s. Grep 0a returns 431 openers, almost all through the project's transaction port; 0b finds that port. 1a: 5 hits → 0 findings. All five were `jobs.enqueue` into a DB-backed export-jobs table, and one hop showed an ORM insert (the outbox precedent). 1b: 13 → 0; the sends ran after the awaited transaction returned. 2a–2e: 0. 3a: 58 lock sites, 18 files with two or more. 4a: 3, 4b: 0 (optimistic conflicts are translated centrally to a 409 that clients retry). 5a: 24, 5b: 2 (the outbox relay is single-consumer behind a leader lock: precedent 9). 6a: 91 lines in 41 files, mostly loops over request-bounded collections. 7a: 26. 8a: 3 → 0 (each under `PESSIMISTIC_WRITE` in the same transaction); 8b: 15 handed to `logic-race-scan`. 9a: 1, a per-tenant numbering row incremented inside order creation (Unconfirmed: needs the per-tenant create rate). 10a: 0; 10b: 4 → 0 (each loop closed before the opener). On `benchmarks/fixtures/node-api`, 0a returns 3 and 2c returns 1. That hit is a `withTransaction(async () => …)` in the order service, whose callback ignores the client it is passed, so both writes run on other pooled connections outside the transaction: a real §2 defect the fixture does not seed. On `vuln-fullstack`, 8b returns the coupon `redemptions + 1` inside `$transaction([…])`, which is `logic-race-scan`'s (VFS-LOGIC-02). `half-built-crm` (SQLite, a connection per call) and `web-dashboard` return 0 on every grep.

## The 3,000-hit path

1. **Intersect.** Keep openers in files that import the data layer or a transaction port; drop frontend and script trees with **one** read showing no production entry point imports them.
2. **Group** by (enclosing function, opener): `rg --json … | jq -r 'select(.type=="match") | "\(.data.path.text):\(.data.line_number)"'`. One decision covers the use cases that share a wrapper, a lock set and a callee.
3. **Rank** by entry point: payment, checkout, order, stock and webhook writes first, then consumers and crons, then admin.
4. **Read the top 30 groups fully**, following each call in the block one hop.
5. **Prefer the runtime bulk oracle at scale.** Run the e2e suite once with the lane's query logger tagging `BEGIN` … `COMMIT`. Flag any transaction open longer than 1 s, any outbound HTTP span whose parent chain holds an open DB transaction span (OpenTelemetry traces show it directly), and any transaction issuing more than 20 `SAVEPOINT`s.
6. **Ledger the rest** as `Live, unreviewed (k groups / n hits)` with the command that continues them. Never `checked`.

## Scans for

Severity assumes a production entry point. Raise to **critical** only on production evidence (an incident, `pg_stat_database.deadlocks` growth, an APM trace), never from code alone.

| § | Class | Ids | Default |
|---|---|---|---|
| 1 | External I/O inside a transaction | DB-23, DB-24 | high on a write path that holds row locks; medium otherwise |
| 2 | Multi-write use case without an effective transaction (none, wrong handle, raw statement outside it) | DB-22 | high |
| 3 | Inconsistent lock order (deadlock) | DB-25 · CWE-833 | medium; high on payment and order paths |
| 4 | SERIALIZABLE, REPEATABLE READ or optimistic locking with no retry | DB-26 · CWE-755 | medium |
| 5 | Queue or outbox claim without `SKIP LOCKED` | DB-27 · CWE-362 | high on payments and jobs; medium otherwise |
| 6 | Long transaction: a data-sized loop, a request-wide transaction, an unmanaged begin | DB-24 · CWE-400 | medium; high on a hot table |
| 7 | Write skew on an integrity invariant | DB-21 · CWE-362 | high |
| 8 | Lost update on a non-value field | DB-20 · CWE-362 | medium |
| 9 | Hot-row contention (one row written by every request) | read-layer R12 | medium |
| 10 | Subtransactions (savepoints) in a loop on a hot path | DB-28 | medium |

### 1. External I/O inside a transaction

```
BAD:   await dataSource.transaction(async (m) => { await m.save(order); await psp.capture(order); })   // row lock held for the PSP's latency
       with transaction.atomic(): order.save(); send_receipt.delay(order.id)                           # worker can run before commit
GOOD:  await dataSource.transaction(async (m) => { await m.save(order); await m.save(Outbox.of('capture', order)); });
       transaction.on_commit(lambda: send_receipt.delay(order.id))
```
**Read the code:** Does the call sit between the opener and its commit, including inside a helper the block calls? Which rows are locked by then: an `UPDATE` or a `FOR UPDATE` earlier in the block? What is the callee's timeout, and does it retry? If the transaction rolls back after the call, has the side effect already happened (an email sent, a card charged, a job enqueued that reads "not found")? **Finding when** an outbound call, a queue publish to an external broker, or a sleep runs inside an open transaction on a production path. **Proof:** stub the call with a 2 s delay; during it, `pg_stat_activity` shows the session `idle in transaction`, or `em.isInTransaction()` / the ORM equivalent is true, and a concurrent update of the same row waits. It fails before the fix. Also fault injection: fail the commit after the call; the side effect must not have fired (`snippets/proof-oracles.md` § "Fault injection", V8).

### 2. Multi-write use case without an effective transaction

```
BAD:   withTransaction(async () => { await queries.updateOrder(id, patch); await queries.insertAudit(...); })  // both use pool.query: outside
       await prisma.$transaction(async (tx) => { await tx.order.update(…); await prisma.stock.update(…); }) // second write escapes
       em.getConnection().execute(sql, params, 'all')        // inside em.transactional: another pooled connection
GOOD:  withTransaction(async (client) => { await queries.updateOrder(client, id, patch); await queries.insertAudit(client, …); })
       every call through `tx`; MikroORM raw: execute(sql, params, 'all', em.getTransactionContext())
```
**Read the code:** List the writes of the use case. Do they all travel through the transaction's handle or context? A statement on the outer client runs on another connection; it is not rolled back, and with a small pool it can wait on the transaction's own lock (a self-deadlock). With no opener at all: is the multi-write one ORM unit of work (`flush`, `SaveChanges`, a Prisma nested write, a single `save` of an aggregate), which is atomic by itself? Spring: is `@Transactional` on a private or self-invoked method, which the proxy never sees? Django: is a database error caught **inside** `atomic()` (grep 2e), leaving the transaction broken? An **outbox row** written outside the caller's transaction (a second connection, a repository not taken from the transaction's handle) is distributed-systems `dual-write-scan` §1's "outbox misused" when that pack is installed: list it here as corroboration, deduped by `file:line`; without it, report it here. **Finding when** two or more writes that must land together can land apart. **Proof:** fault injection (`snippets/proof-oracles.md` § "Fault injection", V7). Throw after the first write: no partial row may remain. For the wrong-handle variant, throw at the end of the callback: the escaped write persisted.

### 3. Inconsistent lock order

```
BAD:   transfer: lock(from) → lock(to)         refund: lock(to) → lock(from)          // opposite orders deadlock
       for (const id of req.ids) await repo.lockAndUpdate(id)                         // caller's order
GOOD:  SELECT id FROM accounts WHERE id = ANY($1) ORDER BY id FOR UPDATE;  -- one order, then update
```
**Read the code:** Build a table of path → ordered list of the rows and tables it locks or updates (3a, 3b, 6a). Any two paths that touch the same pair in opposite orders are candidates. So is a loop over request-ordered ids. On MySQL, an FK check takes a shared lock on the parent: a parent-counter update after child inserts deadlocks with a concurrent child insert. **Finding when** two production paths can interleave on the same rows in opposite orders. **Proof:** 100 iterations of the two paths concurrently; at least one `40P01` / `1213` before the fix, zero after (V9).

### 4. SERIALIZABLE, REPEATABLE READ or optimistic locking with no retry

```
BAD:   await prisma.$transaction(fn, { isolationLevel: 'Serializable' })   // 40001 surfaces as a 500
       retry(() => tx.update(...))                                         // retries one statement, not the transaction
GOOD:  for (let i = 0; i < 3; i++) { try { return await prisma.$transaction(fn, opts) } catch (e) { if (!isSerialization(e)) throw e; await backoff(i) } }
       // side effects after the loop, never inside fn
```
**Read the code:** Where is the level set (4a), and what catches `40001` / `40P01` / `1213` / the ORM's optimistic error? Does the retry re-run the **whole** transaction closure, bounded, with backoff? Do side effects inside the closure fire again on each attempt? A conflict translated to a 409 that the client contract retries is a correct design (precedent 4). **Finding when** an abort the engine will raise under contention reaches the caller as a 500, or a retry repeats a side effect. **Proof:** force the conflict (the write-skew barrier at SERIALIZABLE, or a stubbed driver error carrying SQLSTATE `40001` on the first attempt); the operation completes exactly once, side effects once (V10).

### 5. Queue or outbox claim without `SKIP LOCKED`

```
BAD:   const job = await repo.findOne({ status: 'ready' }); await repo.update(job.id, { status: 'running' })   // two workers, one job
       SELECT * FROM jobs WHERE status = 'ready' LIMIT 10 FOR UPDATE     -- workers queue behind each other
GOOD:  UPDATE jobs SET status = 'running', claimed_at = now()
       WHERE id IN (SELECT id FROM jobs WHERE status = 'ready' ORDER BY id LIMIT 10 FOR UPDATE SKIP LOCKED) RETURNING *
```
**Read the code:** Is a **database table** used as a queue (5a), and how many consumers run it (replicas × worker concurrency, from `connection-config-scan` grep 2b)? A broker-backed queue (BullMQ, Sidekiq, Celery, SQS) claims for you and is `N/A`. A single consumer behind a leader lock is precedent 9; record the lock's TTL, because a leader that outlives its TTL makes delivery at-least-once, so consumers must be idempotent. **Finding when** two or more consumers claim with a bare read-then-update, or serialize on `FOR UPDATE` without `SKIP LOCKED`. **Proof:** N workers on M jobs; each job processed exactly once (a unique `job_runs(job_id)` or a processed-count assertion), and no worker blocks longer than the budget (`snippets/proof-oracles.md` § "Invariant under concurrency").

### 6. Long transaction

```
BAD:   await em.transactional(async (em) => { for (const row of await em.find(Order, {})) { … await em.flush() } })   // data-sized
       ATOMIC_REQUESTS = True  ·  a global transaction interceptor  ·  const trx = await knex.transaction()  // no rollback path
GOOD:  batches of 500, each its own transaction, with a resume key; a transaction scoped to the write-set of one use case
```
**Read the code:** Does the loop in the window (6a) iterate a request-bounded set (a cart's lines) or a data-sized one (all orders, an import file)? Does a request-wide transaction (6b) wrap reads, rendering or outbound calls? Does every unmanaged begin (6c) reach `commit` or `rollback` on every path, including `finally` / `defer`? Is a database-side backstop set (`idle_in_transaction_session_timeout`, `transaction_timeout`: `connection-config-scan` §6)? **Finding when** a production transaction's duration grows with data or waits on something outside the database. **Proof:** lock budget (`snippets/proof-oracles.md` § "Lock budget"). While the batch runs, an update to a row it touched first must complete within the budget, and sampled `now() - xact_start` stays under it.

### 7. Write skew on an integrity invariant

```
BAD:   if (await shifts.count({ day, onCall: true }) > 1) await shifts.update(mine, { onCall: false })  // two do it at once: nobody on call
       if (!await bookings.overlaps(room, from, to)) await bookings.insert(...)                         // double booking at RC and RR
GOOD:  EXCLUDE USING gist (room WITH =, tstzrange(starts, ends) WITH &&)   -- or Postgres 18 WITHOUT OVERLAPS
       lock the parent row (the room, the day) FOR UPDATE first; or SERIALIZABLE + §4's retry
```
**Read the code:** Name the invariant across rows ("at least one admin", "no overlap", "one default per tenant") and find where it is enforced. Is it a constraint, a lock on a shared parent, or a read in application code? At the project's isolation level, can two transactions both pass the read? If one actor gains value by breaking it, it is security's (§ Boundaries). **Finding when** the invariant is checked by a read and enforced by nothing atomic. **Proof:** barrier test. Both transactions read, wait on a latch, then write, and the invariant must hold afterwards (V6). For SQL-level proof, a Postgres `isolationtester` spec.

### 8. Lost update on a non-value field

```
BAD:   row.retryCount += 1; await em.flush()                        // two workers: one increment lost
       prefs = { ...user.settings, theme }; await users.update(id, { settings: prefs })   // concurrent editors drop each other's keys
       obj.status = "done"; obj.save()                              # Django: rewrites every column read earlier
GOOD:  UPDATE t SET retry_count = retry_count + 1 WHERE id = $1
       jsonb_set / a merge in SQL; save(update_fields=["status"]); a version column with a compare-and-set
```
**Read the code:** Is the value read, changed in memory and written back (8a)? Is the row locked (`FOR UPDATE` in the same transaction) or version-guarded? Does the write send the whole row or JSON blob, overwriting concurrent changes to other fields? Is last-writer-wins the intended semantics (precedent 7)? **Finding when** two production writers can interleave and the second silently erases the first. **Proof:** invariant under concurrency (V5): N concurrent increments leave start + N, and two concurrent editors' keys both survive.

### 9. Hot-row contention

```
BAD:   UPDATE stats SET orders_today = orders_today + 1 WHERE id = 1      -- every checkout queues on one row lock
       UPDATE users SET last_seen_at = now() WHERE id = $1               -- a write per read request, inside the request's transaction
GOOD:  sharded counters (N rows, summed on read); aggregate asynchronously from an event table; take the counter lock last
       and commit at once; throttle "last seen" to one write per user per minute, outside the request transaction
```
**Read the code:** Which key does the increment (9a) or per-request write (9b) target: a global row, a tenant row, or a per-user row? How many concurrent transactions reach it at peak? How long does each hold the lock after taking it (a sequence taken early in a long create transaction serializes the whole create)? Gapless numbering legally needs a locked counter row (`schema-integrity-scan` §11); then the finding is only how long the lock is held. **Finding when** concurrent requests serialize on one row on a hot path. **Proof:** K concurrent requests on one key. Sample `pg_stat_activity` for `wait_event_type = 'Lock'` (`transactionid` / `tuple`) and record throughput against K, labelled measured. After the fix, waits drop to near zero and throughput scales with K.

### 10. Subtransactions in a loop on a hot path

```
BAD:   for item in items: with transaction.atomic(): Thing.objects.get_or_create(...)     # one SAVEPOINT per item
       items.each { |i| Model.transaction(requires_new: true) { … } }
GOOD:  one INSERT … ON CONFLICT DO NOTHING for the batch; or no nested block, catching the conflict once outside the loop
```
**Read the code:** Does the loop (10b) open a nested transaction, or call a helper that does (`get_or_create` inside `atomic`, `create_or_find_by`, `findOrCreate`, EF `SaveChanges` in a user transaction, a nested MikroORM `em.transactional`)? How large is N on a hot path? Is a long-running transaction usually open at the same time (a report, a vacuum)? Postgres caches 64 open subtransaction ids per backend; past that, lookups go to `pg_subtrans` on disk (PG 18 docs). GitLab (2021-09-29) found that a single `SAVEPOINT`, combined with a long-running transaction, stalled replicas on `SubtransControlLock` (renamed `SubtransSLRU` in PG 13). **Finding when** a production loop issues a savepoint per element at volume (precedent 5). **Proof:** count `SAVEPOINT` statements per transaction with the lane's statement counter at N = 2 and N = 20; the count must be constant after the fix (`snippets/proof-oracles.md` § "Query-count scaling"). The optional live probe is replica `SubtransSLRU` waits under a concurrent long transaction.

## Live lane (read-only; when a database is reachable)

Open the session read-only and bounded (`BEGIN READ ONLY; SET LOCAL statement_timeout = '5s';`). These are the rows `/db-audit` folds into its L4 check.

```sql
-- §1, §6: the longest open transactions and what they wait on
SELECT pid, application_name, state, now() - xact_start AS xact_age, wait_event_type, wait_event, left(query, 80)
  FROM pg_stat_activity WHERE xact_start IS NOT NULL ORDER BY xact_age DESC LIMIT 20;
-- §3: deadlocks since the stats reset, then who blocks whom right now
SELECT datname, deadlocks, stats_reset FROM pg_stat_database WHERE datname = current_database();
SELECT pid, pg_blocking_pids(pid) AS blocked_by, wait_event_type, wait_event, left(query, 80)
  FROM pg_stat_activity WHERE cardinality(pg_blocking_pids(pid)) > 0;
-- §9: single-row updates by call count (needs pg_stat_statements)
SELECT calls, rows, round(mean_exec_time::numeric, 2) AS mean_ms, left(query, 100) FROM pg_stat_statements
 WHERE query ILIKE 'update%' AND rows <= calls ORDER BY calls DESC LIMIT 20;
-- §10: subtransaction pressure (run on the replicas too)
SELECT wait_event, count(*) FROM pg_stat_activity WHERE wait_event ILIKE 'Subtrans%' GROUP BY 1;
```
MySQL: `SELECT trx_id, trx_started, trx_state, left(trx_query, 80) FROM information_schema.INNODB_TRX ORDER BY trx_started LIMIT 20;`, `SELECT * FROM sys.innodb_lock_waits;`, and `SHOW ENGINE INNODB STATUS\G` (it keeps only the latest deadlock; `innodb_print_all_deadlocks = ON` logs every one). Postgres `log_lock_waits` is off by default through PG 18. Without it, lock waits leave no trace in the logs.

## Output

```
transaction-scan — lanes: typeorm 1.1 (package.json), django 6.1 (pyproject.toml); prisma, mikro-orm, rails, jpa, gorm absent
Engine: postgres 18 (compose) — READ COMMITTED default · wrapper: none · backstops: idle_in_transaction_session_timeout unset

Findings: 2 · Unconfirmed: 1

1. src/payments/checkout.service.ts:58                        [report-with-fix]   high
   §1 I/O inside a transaction — `await this.psp.capture(order)` inside dataSource.transaction opened at :41,
   after `setLock('pessimistic_write')` on the order at :44. Reached by POST /checkout.
   Proof: test/checkout.tx.e2e-spec.ts — stubbed capture 2 s → session idle in transaction 2.0 s, a concurrent
   order update waited 1.9 s (measured; fails). Fix: save the order + an outbox row in the transaction; capture
   in the outbox consumer after commit.

2. reports/views.py:88                                        [report-with-fix]   high
   §2 no effective transaction — `invoice.save()` then `InvoiceLine.objects.bulk_create(lines)` with no atomic();
   a failure between them leaves an invoice with no lines. Reached by the nightly billing cron.
   Proof: fault injection after the first save → orphan invoice row (fails). Fix: wrap both in transaction.atomic().

3. src/stats/counters.repo.ts:21                              [report-flagged]    medium
   §9 hot row — `UPDATE daily_stats SET orders = orders + 1 WHERE day = $1` on every checkout, inside the order
   transaction. Unproven link: no peak checkout rate. Settling probe: 50 concurrent checkouts, lock waits on
   `transactionid` sampled from pg_stat_activity. Fix: aggregate from the orders table, or sharded counter rows.

Verification: 14 candidates → 2 findings · 1 unconfirmed · 4 hardening · 0 pre-existing · 7 refuted

Class coverage:
  §1  I/O inside a transaction     checked (6 hits → 1 finding; 5 were outbox inserts, one hop each)
  §2  no effective transaction     checked (3 hits → 1 finding)
  §3  lock order                   checked (11 lock sites in 4 files → 0 findings; lock-order table built)
  §4  isolation without retry      N/A (no isolation level set; no version columns)
  §5  queue claim                  N/A (jobs run on a broker; no table polled as a queue)
  §6  long transaction             checked (9 loops in windows → 0 findings; all request-bounded)
  §7  write skew                   checked (4 hits → 0 findings; 1 → logic-race-scan)
  §8  lost update (non-value)      checked (2 hits → 0 findings; 6 value-field hits → logic-race-scan)
  §9  hot rows                     checked (1 hit → 1 unconfirmed)
  §10 savepoints in loops          checked (0 hits)
```

`[report-with-fix]`: the boundary is traced from the entry point, the oracle failed first, and the fix is a local change in the project's transaction API. `[report-flagged]`: one link is unproven (no harness, no traffic figure, a wrapper's semantics not read), and the row names it and the settling probe. The coverage block lists **all ten** classes on every run: `checked (k hits → m findings)` only when the grep ran on a present lane; `N/A (<reason>)` only when the surface is absent; `blocked (<reason>)` when the grep failed or the code could not be read. A partial review reads `Live, unreviewed (k groups / n hits)`.

## False positives / precedents

The verifier reads `snippets/precedents/data.md` § "Transactions and concurrency" (precedents 1–11) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:

- **A single atomic statement needs no transaction** (precedent 1). `UPDATE … SET n = n + 1 WHERE …` is the fix for §8, not a race.
- **An outbox, job or audit row inserted in the same database inside the transaction** is the correct pattern for a side effect (precedent 6). Follow the call one hop before reporting §1.
- **A transaction is not a lock.** Two statements in a READ COMMITTED transaction race exactly like no transaction. Only a conditional update, `FOR UPDATE`, a version guard, a constraint or SERIALIZABLE with a retry closes it.
- **The unit of work is already a transaction.** MikroORM `flush()`, EF `SaveChanges`, a Prisma nested write and a Rails autosave are atomic by themselves, so §2 needs two units of work.
- **Savepoints in moderation** (precedent 5), **single consumers** (precedent 9), **advisory locks with a documented scope** (precedent 10), **last-writer-wins by design** (precedent 7).
- **A loop over a request-bounded set** inside a transaction (a cart's lines, a form's rows) is not §6.

## When to run

- On any diff that adds or changes a transaction block or decorator, an isolation or lock keyword, a job or outbox claim, an outbound call in a service that writes, or a counter update: the `/db-audit` dispatch signal.
- On every whole-repo `/db-audit`, reporting all ten classes.
- After an incident with `40P01` / `1213`, `idle in transaction` sessions, pool exhaustion during a third-party outage, double-processed jobs, or totals that drift.

## Halt conditions

- Do not report a high row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/data.md`](../../../../snippets/precedents/data.md). Under `/db-audit` that happens in its verification phase. Run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on any finding without the opener (or the unprotected write) `<file:line>`, the breaking statement or call, the entry point, and the fix in the project's transaction API.
- Do not run a concurrency or fault probe against production, or against a database the operator has not named. Probes run on a local, CI or restored copy.
- Do not propose a bigger pool, a longer timeout, an in-process mutex, or "wrap it in a transaction" at the default isolation level as a fix for a race.
- Do not report a value-field race (money, stock, quota, single-use) when the security pack is installed. Count it in 8b and credit `logic-race-scan`.
- Do not print "no transaction defects" without the class-coverage block. A class whose grep did not run is `blocked`, never `checked`.

## Related

- `/db-audit` dispatches this skill and folds its coverage block and live rows into the class ledger. `/db-fix` closes the findings: the failing-first oracle, the root-cause fix (move the call after commit or into an outbox, thread the handle, order the locks, wrap the retry), a re-run of this detector on the patched lines, and the sibling search.
- `logic-race-scan` (security pack, when installed) owns races on value fields and the authorization matrix (§ Boundaries). Without it, §7 and §8 cover them, tagged.
- `connection-config-scan` (this pack) owns pool sizing, pooler compatibility and the database-side timeouts that backstop §1 and §6. `n-plus-one-scan`, `migration-safety` and `schema-integrity-scan` (this pack) own the neighbouring classes.
- `database/ai-patterns/transaction-isolation.md` holds the isolation, locking and retry method this skill's fixes apply. Backend's `transaction-boundary` pattern (when the backend pack is installed) holds the service-scope design, and the distributed-systems `idempotency` and `distributed-lock` patterns (when installed) hold cross-service atomicity.
- `snippets/proof-oracles.md` § "Invariant under concurrency", § "Fault injection" and § "Lock budget" hold the test shapes per stack.
