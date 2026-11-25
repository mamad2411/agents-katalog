---
name: connection-config-scan
description: Audit how the app connects to its database — a client per request, pool size × processes × replicas against max_connections or the pooler, transaction-pooler incompatibilities, serverless storms, missing statement, idle-in-transaction, lock and acquire timeouts, reads-after-write on a replica, leaked connections, and session settings that weaken integrity.
kind: skill
pack: database
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: connection-config-scan

## Premise

Database connections are a hard, finite, server-side resource. Each Postgres connection is a process, and the server refuses the next one past `max_connections` (`53300 too many clients`, MySQL `1040`). The application sees almost none of this in code. The pool size is in a config file, the multiplier is in a Kubernetes HPA, a KEDA `ScaledObject`, a gunicorn flag or a `WORKER_CONCURRENCY` env var, and the ceiling is in a parameter group or a managed-database tier table. So connection defects are **arithmetic across files**, plus a few settings whose absence is the defect: no statement timeout, no idle-in-transaction timeout, no acquire timeout, a session feature behind a transaction pooler, a correctness read sent to a lagging replica.

**Every finding cites the setting `<file:line>` (or the file where it is missing) + every other term the claim depends on, each with its own `<file:line>` or its documented default + the arithmetic or the probe + the fix.** A pool size alone is never a finding. "Connections look fine" is never printed without the class-coverage block (§ Output) and the budget table (§2).

**Detect statically, prove by execution, measure impact last.** §2 is proved by arithmetic whose every term is cited. It is a static-fact class, so the full trace passes the proof gate ([`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 2, gate 6). A load test at the maximum replica count turns it from arithmetic into a measurement. The timeout classes are proved by making the timeout fire. A term the run cannot read is `UNKNOWN`, never guessed. The row becomes `[report-flagged]`, naming the missing input and the command that reads it.

## The rule

A candidate is a finding when all four hold:

1. **The setting is the one production runs.** Read the value through its actual path: env var → config module → driver option. Read it in the deploy overlay that ships, not `.env.example`. A default applies only when nothing sets the value, and then it is cited as the installed version's default.
2. **The load that breaks it really occurs.** Maximum replicas, not current replicas. The peak worker concurrency. A burst of serverless invocations. A slow query or a stalled downstream.
3. **No control absorbs it.** A transaction-mode pooler in front, a role-level timeout, a proxy (RDS Proxy, a Neon or Supabase pooler), a sticky-primary window after writes.
4. **The failure is real.** Connection refusal, requests hanging on acquire, a runaway query pinning a connection and its locks, a stale read that a write or an authorization decision depends on, a pool drained by an error path.

## Boundaries

- **What happens inside a connection's transaction** (I/O held open, long transactions, savepoint storms) → `transaction-scan` (this pack). This skill owns the **database-side backstops** that bound those defects (§5, §6), and `transaction-scan` §1 and §6 cite them.
- **A session-level advisory lock or session `SET` behind a transaction pooler** is §3 here. When the setting carries tenant or role context, the cross-tenant consequence goes to `@tenant-isolation-reviewer` (security pack, when installed), deduped by `<file:line>`. Without the security pack it is reported here, tagged `security-class (owner pack not installed)`.
- **SQLite `PRAGMA foreign_keys` off per connection, and MySQL `sql_mode` without strict mode** → `schema-integrity-scan` §1 and §6 (this pack). This skill reads them only as session settings and never reports them.
- **An HTTP agent, Redis client or SDK client built per call** → `request-path-scan` (performance pack, when installed). This skill owns database clients and pools only.
- **Per-workload tuning of the numbers** (the pool size that saturates this database's cores) belongs to `@database-optimizer`, and capacity planning across services to `@capacity-planner` (distributed-systems pack, when installed). This skill proves the invariant they tune inside: Σ pools ≤ the ceiling.
- **Backups, failover and replica promotion** → `dr-audit` (infrastructure pack, when installed). Lag *monitoring* is a §8 Hardening row here.

## Adapt to the codebase

Read the driver, ORM and pooler **with versions** from the lockfile and deploy files, because defaults moved: Prisma 6 → 7 changed who owns the pool and its acquire timeout, and PgBouncer gained protocol-level prepared statements in 1.21. Read the engine and version first with the context block in `snippets/refute-before-report.md` § "2. The gates" (G1–G3). Print the lanes you ran in the output header.

| Lane | Pool max knob · default when unset | Acquire timeout · default | Statement / lock timeout knob | Lifetime, validation | Replica routing |
|---|---|---|---|---|---|
| **node-postgres** (`pg.Pool`; Prisma 7 / TypeORM / MikroORM ride on it) | `max` · 10 | `connectionTimeoutMillis` · **0 = waits forever** | client config `statement_timeout`, `lock_timeout`, `idle_in_transaction_session_timeout` (startup parameters) | `idleTimeoutMillis`; no max lifetime: recycle at the proxy | — |
| **Prisma** 6 / 7 | v6: URL `connection_limit` · CPUs × 2 + 1. v7: the driver adapter's pool (`pg`: 10) | v6 `pool_timeout` · 10 s. v7 `pg` · 0 (upgrade finding) | role level (`ALTER ROLE … SET`); v7 via the `pg` pool config | — | `@prisma/extension-read-replicas` (`$primary()` forces the writer) |
| **MikroORM** 6 (Knex) / 7 (Kysely) | `pool: { min, max }` · the driver's default for the installed version | 6: Knex `acquireConnectionTimeout` (Knex default 60 s) | `driverOptions` connection startup parameters | `pool.idleTimeoutMillis` | `replicas: [...]`; `preferReadReplicas` defaults to **true**: every read outside a transaction goes to a random replica, and `{ connectionType: 'write' }` forces the primary (7.2 docs) |
| **TypeORM** | `poolSize` / `extra.max` · `pg` default 10 | `extra.connectionTimeoutMillis` | `extra.statement_timeout`; role level | — | `replication: { master, slaves }`: read which queries the installed version sends to a slave |
| **Sequelize** 6 | `pool.max` · 5 | `pool.acquire` · 30 s | `dialectOptions` / role level | `pool.idle` · 10 s | `replication: { read, write }` |
| **Knex** 3 | `pool.max` · 10 (min 2; the docs recommend `min: 0`) | `acquireConnectionTimeout` · 60 s | role level | — | — |
| **SQLAlchemy** 2 | `pool_size` 5 + `max_overflow` 10 | `pool_timeout` · 30 s | `connect_args` `options='-c statement_timeout=…'`; role level | `pool_pre_ping` off, `pool_recycle` −1; `NullPool` behind an external pooler; `engine.dispose(close=False)` after a fork | session `bind` per read |
| **Django** | one connection per thread; `CONN_MAX_AGE` · 0 = a new connection per request; psycopg pool `OPTIONS: {"pool": …}` (5.1+, needs `CONN_MAX_AGE = 0`) | pool `timeout` | `OPTIONS: {"options": "-c statement_timeout=…"}`; role level | `CONN_HEALTH_CHECKS` | a router's `db_for_read` |
| **Rails** | `pool:` in `database.yml` · `RAILS_MAX_THREADS` (template 3) vs Puma `threads` | `checkout_timeout` | `variables: { statement_timeout: … }` | `idle_timeout`, `reaping_frequency` | `connects_to`, `connected_to(role: :reading)`, automatic role switching with a delay |
| **Laravel** | one connection per PHP-FPM child: `pm.max_children` × pods | — | role level | — | `read` / `write` hosts + `'sticky' => true` |
| **Spring / HikariCP** | `maximumPoolSize` · 10 (`minimumIdle` = max) | `connectionTimeout` · 30 s | role level; `options=-c statement_timeout=…` in the JDBC URL | `maxLifetime` 30 min, `keepaliveTime` 2 min; `leakDetectionThreshold` · 0 (off); `spring.jpa.open-in-view` · **true** | `AbstractRoutingDataSource` + `@Transactional(readOnly = true)` |
| **Go** `database/sql` / GORM | `SetMaxOpenConns` · **0 = unlimited**; `SetMaxIdleConns` · 2 | `context.WithTimeout` per call | role level + `ctx` deadlines | `SetConnMaxLifetime` · 0 (forever) | GORM `dbresolver` |
| **.NET** (Npgsql / ADO.NET) | `Maximum Pool Size` in the connection string (pooling is per connection string) | `Timeout` | `Command Timeout`; role level | `Connection Idle Lifetime` | — |
| **PgBouncer** | `default_pool_size` · 20 per (db, user); `max_client_conn` · 100 | `query_wait_timeout` · 120 s | — | `server_idle_timeout`; `idle_transaction_timeout` · **0** | — |
| **MySQL server** | `max_connections` | — | `max_execution_time` (read-only `SELECT` only); `innodb_lock_wait_timeout` · 50 s | `wait_timeout` · 28,800 s: a pool lifetime must sit below it | — |

Defaults in this table come from the research catalog dated 2026-10-02 and the MikroORM 7.2 docs fetched that day. Confirm a default against the installed version before an arithmetic row rests on it, and label it `DEFAULT` in the budget table.

## Pre-flight greps

Run as **one** script from the repo root (shell state does not survive between tool calls). Grep **N** feeds detector **§N**. Every `rg` names its path (`.`): given no path, `rg` reads stdin whenever stdin is a pipe, and under an agent's shell that is a silent zero-hit run. `X` drops non-production code. `XC` keeps the config, env, manifest and Dockerfile layer (hidden files included), where most of this class lives. Variables are written `${NAME}`, because zsh reads `$NAME[…]` as a subscript. Any `rg` error on stderr is a failed grep, never zero hits.

```bash
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/target/**' -g '!**/.venv/**' -g '!**/.next/**'
   -g '!**/generated/**' -g '!**/temp/**' -g '!*.{md,mdx,json,lock,snap,map,svg,txt,csv}' -g '!**/*.min.*' -g '!**/docs/**' -g '!/ai/**'
   -g '!**/{test,tests,spec,e2e,__tests__,__mocks__,mocks,__snapshots__,fixtures,__fixtures__,testdata,seeds,seeders,factories}/**'
   -g '!**/*{.,_,-}{test,spec,e2e-spec,mock,stories,test-data}.*' -g '!**/test_*.py' -g '!**/conftest.py'
   -g '!**/migrations/**' -g '!**/db/migrate/**' -g '!**/{locales,locale,i18n,translations}/**')
XC=(--hidden -g '!.git/**' -g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/.venv/**' -g '!**/.next/**'
    -g '!*.{md,mdx,lock,snap,map,svg,csv}' -g '!**/{package-lock,composer,npm-shrinkwrap}.json' -g '!**/pnpm-lock.yaml' -g '!**/docs/**' -g '!/ai/**'
    -g '!**/{test,tests,spec,e2e,__tests__,__mocks__,mocks,__snapshots__,fixtures,__fixtures__,testdata}/**' -g '!**/*{.,_,-}{test,spec,e2e-spec,mock}.*'
    -g '!**/{locales,locale,i18n,translations}/**' -g '!**/migrations/**' -g '!**/db/migrate/**')
NC=(rg -v --pcre2 '^[^:]+[:-]\d+[:-]\s*(//|/\*|\*(\s|/|$)|#(?!\{)|<!--|--\s)')   # drops comment-only lines
DL='@mikro-orm|typeorm|@prisma/|\bsequelize\b|drizzle-orm|\bknex\b|mongoose|from\s+["\x27](pg|mysql2|postgres|mariadb)["\x27]|require\(["\x27](pg|mysql2)["\x27]\)|django\.db|sqlalchemy|ActiveRecord|Illuminate\\Database|jakarta\.persistence|gorm\.io|database/sql|Microsoft\.EntityFrameworkCore|Npgsql|Ecto\.'
for t in js ts py go java kotlin ruby php cs elixir; do printf '%s=%s ' "$t" "$(rg --files -t "$t" "${X[@]}" . | wc -l | tr -d ' ')"; done; echo   # 0 = lane absent

# 1. 1a a database client or pool built inside a block (indented: per call, per request, per tenant); 1b request-pinned connections.
rg -n --pcre2 '^\s+.*(\bnew\s+(PrismaClient|Pool|Client|Sequelize|DataSource|MongoClient|Knex)\s*\(|\bknex\(\s*\{|\b(mysql2?|mariadb)\.create(Pool|Connection)\(|\bMikroORM\.init\(|\bcreate_(async_)?engine\(|\b(psycopg2?|asyncpg|pymysql|MySQLdb|sqlite3)\.(connect|create_pool)\(|\b(sql|gorm|pgxpool|pgx)\.(Open|Connect|ConnectConfig|NewWithConfig)\(|\bPG\.connect\(|\bMysql2::Client\.new\(|\bnew\s+PDO\(|\bDriverManager\.getConnection\(|\bestablish_connection\b)' "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 'open-in-view|\bCONN_MAX_AGE\b|\bCONN_HEALTH_CHECKS\b' "${XC[@]}" .
# 2. The budget's terms. 2a pool knobs (config + code); 2b pool objects in data-layer files; 2c deploy multipliers (replicas,
#    HPA / KEDA maxima, workers, threads, Jobs); 2d concurrency in code; 2e the server ceiling and pooler budget; 2f every file
#    that hands a database URL to a process (each is a connecting process class).
rg -n --pcre2 '\bconnection_limit=\d+|\bpool_?[sS]ize\b|\bpoolSize\b|\bmax_?[pP]ool_?[sS]ize\b|\bmaximumPoolSize\b|\bmax_overflow\b|\bconnectionLimit\b|SetMaxOpenConns\(|\bMax(imum)? Pool Size\b|\b[A-Z_]*POOL_(MAX|SIZE|MIN)\b|\bDB_POOL\w*|\bpool\s*:\s*\d+|\b(max_size|min_size)\b' "${XC[@]}" . | "${NC[@]}"
rg -l0 --pcre2 "${DL}" "${X[@]}" . | xargs -0 -r rg -n --pcre2 '\bpool\s*[:=]\s*\{|\bmax\s*:\s*\d+\s*[,}]' | "${NC[@]}"
MUL='^\s*(replicas|minReplicas|maxReplicas|minReplicaCount|maxReplicaCount|desired_count|desiredCount|max_capacity|maxCapacity|replica_count|parallelism|reservedConcurrency|provisionedConcurrency|maxInstances|max_instances|instances|exec_mode|workers|threads|concurrency|worker_concurrency|scale|maxSurge)\s*[:=]|--(workers|concurrency|threads|scale)[ =]+\S|^\s*(workers|threads)\s+\S|\bpm\.max_children\b|\bkind:\s*(HorizontalPodAutoscaler|ScaledObject|Deployment|StatefulSet|CronJob|Job)\b|\b[A-Z]+_(CONCURRENCY|WORKERS|THREADS)\b'
rg -n --pcre2 "${MUL}" -g '*.{yml,yaml,toml,tf,hcl,ini,conf,cfg,properties}' -g 'Procfile*' -g 'Dockerfile*' -g '.env*' -g 'ecosystem.config.*' -g '*gunicorn*.py' -g 'puma.rb' "${XC[@]}" . | "${NC[@]}"
rg -n --pcre2 '\b[A-Z]+_(CONCURRENCY|WORKERS|THREADS)\b|\bconcurrency\s*:\s*[\w.]+|\bcluster\.fork\(|\bworker_concurrency\b|\bWEB_CONCURRENCY\b' "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '\bmax_connections\b|\bsuperuser_reserved_connections\b|\breserved_connections\b|\bmax_wal_senders\b|\bdefault_pool_size\b|\bmax_client_conn\b|\bmax_db_connections\b|\breserve_pool_size\b|\bmax_user_connections\b' "${XC[@]}" .   # no NC: a manifest comment often states the managed ceiling — cite it as `stated`
rg -l --pcre2 '\b(DATABASE_URL|DB_HOST|DB_URL|POSTGRES_(HOST|URL|DSN)|PGHOST|MYSQL_(HOST|URL|DSN)|SPRING_DATASOURCE_URL|ConnectionStrings__\w+|DATA_SOURCE_(NAME|URI)|\w*DB_DSN)\b|\bdatasourceSecret\s*:|postgres[-_]exporter|mysqld?[-_]exporter|pgbouncer[-_]exporter' -g '*.{yml,yaml,toml,tf,hcl,ini,conf,env,sh}' -g 'Dockerfile*' -g 'Procfile*' -g '.env*' "${XC[@]}" .   # exporters and sidecars connect too
# 3. 3a a pooler and its mode; 3b session-scoped features in code; 3c a direct URL kept for migrations.
rg -n -i --pcre2 '\bpool_mode\b|\bpgbouncer\b|[:@]6543\b|pooler\.supabase|-pooler\.|\bodyssey\b|\bpgcat\b|\bsupavisor\b|rds[-_ ]?proxy|aws_db_proxy|\bmax_prepared_statements\b|\bproxysql\b' "${XC[@]}" . | "${NC[@]}"
rg -n --pcre2 '["\x27\x60]\s*SET\s+(?!LOCAL\b|TRANSACTION\b|CONSTRAINTS\b)(SESSION\s+)?\w+\s*(=|TO\b)|set_config\([^)]*,\s*(false|FALSE)\s*\)|["\x27\x60]\s*LISTEN\s+\w|pg_(try_)?advisory_lock\(|\bWITH\s+HOLD\b|CREATE\s+TEMP(ORARY)?\s+TABLE\b(?![^;\n]*ON\s+COMMIT\s+DROP)|["\x27\x60]\s*PREPARE\s+\w+|\bDISABLE_SERVER_SIDE_CURSORS\b|\bprepare\s*:\s*false\b|\bstatement_cache_size\b|\bprepareThreshold\b' "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '\bdirectUrl\b|\bDIRECT_(DATABASE_)?URL\b|\bMIGRAT\w*_DATABASE_URL\b' "${XC[@]}" . | "${NC[@]}"
# 4. Serverless: function manifests and handler entry points (each one a pool per instance).
rg --files "${XC[@]}" . | rg '(^|/)(serverless\.ya?ml|vercel\.json|netlify\.toml|template\.ya?ml|samconfig\.toml|wrangler\.toml)$'
rg -n --pcre2 '\bexports\.handler\b|\bexport\s+(const|async\s+function)\s+handler\b|\bdef\s+lambda_handler\b|@vercel/functions|from\s+["\x27]aws-lambda["\x27]|@netlify/functions|\battachDatabasePool\(|\bruntime\s*=\s*["\x27]edge["\x27]' "${X[@]}" . | "${NC[@]}"
# 5. Statement timeout evidence (5a: config and code; 5b: role-level SET anywhere, migrations included).
NDB=(rg -v -i --pcre2 '^[^:]*(redis|valkey|cache|queue|bull|kafka|s3|storage|object-store|smtp|mail)[^/:]*:|\b(redis|valkey|ioredis|S3_|s3Client|SMTP_|HTTP_|bull)\w*')   # drop cache, queue, object-store and HTTP clients
rg -n -i --pcre2 'statement_?timeout|query_?timeout|\bmax_execution_time\b|\bsocketTimeout\b|\bcommand_?timeout\b|\bQueryTimeout\b|\bquery\.timeout\b|\bdefault-timeout\b|options=-c\b' "${XC[@]}" . | "${NC[@]}" | "${NDB[@]}"
rg -n -i --pcre2 '\bALTER\s+(ROLE|USER|DATABASE)\s+\S+\s+SET\s+(statement_timeout|lock_timeout|idle_in_transaction_session_timeout|transaction_timeout)\b' --hidden -g '!**/node_modules/**' -g '!*.md' .
# 6. Idle-in-transaction, transaction and lock timeouts for application sessions; pooler and ORM transaction timeouts.
rg -n -i --pcre2 'idle_?in_?transaction_?session_?timeout|(?<!session_)transaction_?timeout|lock_?timeout|\binnodb_lock_wait_timeout\b|\block_wait_timeout\b|\bidle_transaction_timeout\b|\btransactionLifetimeLimitSeconds\b|\bmaxWait\b' "${XC[@]}" . | "${NC[@]}"
# 7. Acquire timeout, lifetime, idle and validation settings.
rg -n --pcre2 '\bconnectionTimeoutMillis\b|\bacquireConnectionTimeout\b|\bacquireTimeoutMillis\b|\bacquire\s*:\s*\d|\bconnectionTimeout\b|\bpool_timeout\b|\bpool_pre_ping\b|\bpool_recycle\b|\bmaxLifetime\b|\bmax_lifetime\b|\bidleTimeoutMillis\b|\bSetConnMaxLifetime\b|\bSetConnMaxIdleTime\b|\bSetMaxIdleConns\b|\bvalidationQuery\b|\btestOnBorrow\b|\breapIntervalMillis\b|\bcheckout_timeout\b|\bwait_timeout\b|Connection (Idle )?Lifetime|\bconnect_?[tT]imeout\b|\bkeepAlive\b|\bkeepalives\b' "${XC[@]}" . | "${NC[@]}" | "${NDB[@]}"
# 8. 8a replica routing config; 8b reads sent to a replica explicitly; 8c lag awareness.
rg -n --pcre2 '\breplicas\s*:\s*\[|\bpreferReadReplicas\b|\breadReplicas\b|\bread_?replica\w*|\bREPLICA_\w*URL\b|\b\w*READ(ER)?_\w*URL\b|\breplication\s*:\s*\{|\bslaves\s*:|connected_to\(role:\s*:reading|\bconnects_to\b|\bdatabase_selector\b|\bdb_for_read\b|\bDATABASE_ROUTERS\b|\bdbresolver\b|\bAbstractRoutingDataSource\b|\breader_?[eE]ndpoint\b|\$replica\(|\bwithReplicas\b|["\x27]sticky["\x27]\s*=>' "${XC[@]}" . | "${NC[@]}"
rg -n --pcre2 '\bconnectionType\s*:\s*["\x27]read|getConnection\(\s*["\x27]read|connected_to\(role:\s*:reading|\.using\(\s*["\x27](replica|read)\w*|\$replica\(|Clauses\(dbresolver\.Read\)|@Transactional\(\s*readOnly\s*=\s*true' "${X[@]}" . | "${NC[@]}"
rg -n -i --pcre2 '\bReplicaLag\b|\breplay_lag\b|pg_last_xact_replay_timestamp|\breplay_lsn\b|Seconds_Behind_(Master|Source)|\breplication_?lag\b|\breplica_?lag\b|\bmax_replication_lag\b' "${XC[@]}" . | "${NC[@]}"
# 9. Checkouts that can leak: 9a JS/TS data-layer files that check out a client or query runner and never release; 9b Go rows
#    without a deferred Close; 9c Python connections or cursors assigned outside `with`; 9d JDBC resources outside try-with-resources.
rg -l0 --pcre2 "${DL}" -t js -t ts "${X[@]}" . | xargs -0 -r rg -l0 --pcre2 '\bawait\s+\w+\.connect\(\s*\)|\bcreateQueryRunner\(' | xargs -0 -r rg --files-without-match --pcre2 '\.release\(\s*\)'
rg -n -U --pcre2 'rows,\s*err\s*:?=\s*\w+\.Query(Context)?\([^\n]*\n(?:(?![^\n]*defer\s+rows\.Close)[^\n]*\n){0,8}?\s*for\s+rows\.Next\(\)' -t go "${X[@]}" .
rg -n --pcre2 '^\s*\w+\s*=\s*([\w.]+\.)?(connect|cursor|raw_connection)\(\s*\)\s*$' -t py "${X[@]}" .
rg -n --pcre2 '^\s*(Connection|Statement|PreparedStatement|ResultSet)\s+\w+\s*=\s*[\w.]+\.(getConnection|createStatement|prepareStatement|executeQuery)\(' -t java -t kotlin "${X[@]}" .
```

`rg --files-without-match` is spelled out: in ripgrep, `-L` means `--follow`. Two blind spots are structural:
- **A setting can live outside the repo.** A managed database's parameter group, a Helm value supplied at deploy time, a platform default. A quiet 5a, 6a or 2e means "not configured in the repo", never "not configured". With a reachable database, the live lane settles it. Without one, the row is Unconfirmed and carries the `SHOW` to run.
- **Documents state terms too.** A runbook, a README budget or a codebase profile may record the replica count or the tier's connection limit that no manifest carries. Read them (`rg -n -i 'max_connections|connection budget|replicas' -g '*.md' .`), cite them as `stated in <file:line>`, and weigh them below a manifest. A stated figure can disagree with the provider's own table.

**Measured** (2026-10-15) on a real NestJS + React monorepo (MikroORM 6.6, Kubernetes with an HPA, a KEDA worker, a migrate Job and a managed-database Prometheus exporter), before → after: 2e 0 → 5 (the trial patch states `max_connections=100` in a YAML comment that the comment filter used to drop; the comment lines now print, cited as `stated`); 2f 9 → 11 files (the postgres-exporter Helm values, whose DSN comes from a secret, are a connecting process class the budget had missed; so are pods still terminating during a rollout, now a template row); 5a 8 → 6 and 7a 5 → 3 (a Redis `commandTimeout` / `connectTimeout` and an S3 `connectionTimeout` are not database settings). On the fixtures only a Redis `commandTimeout` line left (`slow-marketplace`), and `infra-ops` gained two stated ceilings.

Earlier measurement (2026-10-02). On the same kind of monorepo with Kubernetes manifests (an API HPA, a KEDA-scaled worker, a migrate Job), the script runs in about 10 s:
- 1a: 15, all one-off scripts, CLIs and the migrate Job's inline `MikroORM.init`. These are not per-request (precedent), but each is a connecting process class in the §2 budget.
- 2a: 16; 2b: 2 (the CLI config's `pool: { min: 1, max: 2 }`); 2c: 45; 2d: 15; 2e: 0; 2f: 8.
- 3a: 0, so 3b's 2 `SET session_replication_role` lines in a dump routine are N/A.
- 5a: 6 and 6a: 4. Statement and lock timeouts are wired through env vars. `idle_in_transaction_session_timeout` and `transaction_timeout` appear nowhere: §6 Unconfirmed, with `SHOW idle_in_transaction_session_timeout;` as the app role as the settling probe.
- 7a: 4. 8a: 4: replicas are configured with `preferReadReplicas: false`, so reads default to the primary. 8b: 3: explicit read-connection uses in an infra port, to read. 9a–9d: 0.
- The repo's own budget reads 5 × 10 API + 5 × 4 worker = 70 against 97 usable. Its provider runbook lists the database tier at 47 connections, and the code default `DB_POOL_MAX = 20` applies to any process that leaves the env var unset. So the ceiling term is ambiguous: Unconfirmed until `SHOW max_connections` runs on the instance.

On `benchmarks/fixtures/node-api`, 2a returns `poolSize: 20` (NAPI-CAP-01's anchor) and no manifest states a replica count, so §2 is `[report-flagged]` with the replica term missing. 5a returns `statementTimeoutMs: 0` (NAPI-CAP-02's anchor), and that value is never passed to the `Pool`. On `vuln-fullstack`, 2c returns `replicas: 3` and no pool knob exists. The term is the query engine's default (CPUs × 2 + 1, verified for 6.x; the manifest asks for `^5.9`), and the pod's CPU count is unstated: `UNKNOWN`. On `half-built-crm`, 1a returns `sqlite3.connect` per call: an in-process engine, N/A.

## Scans for

| § | Class | Ids | Default |
|---|---|---|---|
| 1 | A database client or pool per request, per call or per tenant; a connection pinned for the whole request | DB-45 · CWE-400 | high in serverless or at high request rates, else medium |
| 2 | Connection budget: Σ (pool × processes × max replicas) + other clients over the ceiling or the pooler | DB-45 · CWE-770 | high over the ceiling at max replicas; medium within 10 % of it |
| 3 | Transaction-mode pooler with session features | DB-47 | high when it breaks exclusion or context; medium for prepared-statement errors |
| 4 | Serverless functions opening raw connections | DB-45 · CWE-770 | high |
| 5 | No statement timeout for application sessions | DB-46 · CWE-400 | medium; high on a small request-facing pool |
| 6 | No idle-in-transaction, transaction or lock timeout for application sessions | DB-46 · CWE-400 | medium |
| 7 | No acquire timeout, max lifetime or validation | DB-46 · CWE-400 | high with unbounded concurrency, else medium |
| 8 | Read-after-write or a correctness read routed to a replica | DB-29 | medium; high for auth, permission and balance reads |
| 9 | A connection, cursor or query runner not released on every path | CWE-772 | high (the pool drains on the error path) |

### 1. A client or pool per request

```
BAD:   async handler(req) { const prisma = new PrismaClient(); … }            // a pool per request
       def view(request): engine = create_engine(URL)                         # a pool per call
       tenantPools[tenantId] ??= new Pool(cfg)   // unbounded tenants × pool size
       spring.jpa.open-in-view left at its default (true): a connection for the whole request, rendering included
GOOD:  one module-scope (or DI-singleton) pool per process; per-tenant pools bounded by an LRU with a cap counted in §2
```
**Read the code:** Is the indented constructor (1a) inside a function called per request, job or tenant, or inside a provider or constructor that runs once? Each process holding its own pool is §2's arithmetic, not §1. In .NET, `new NpgsqlConnection` per call is correct (the driver pools by connection string). One-off CLIs and migration runners are precedent, but count them in §2. **Finding when** a production request or job builds a client or pool, or holds a connection for longer than its database work. **Proof:** `SELECT count(*), state FROM pg_stat_activity WHERE application_name = '<app>' GROUP BY state` stays flat while the request count rises, and connect spans are absent from steady-state traces. Socket count: `snippets/proof-oracles.md` § "Socket and handle count". It fails before the fix.

### 2. The connection budget

Build this table for every run that finds a database. Cite every term. Use **maximum** replicas, add the rolling-deploy surge, and write `UNKNOWN` instead of guessing.

```
connecting process class       pool max (cited)       procs/pod (cited)       max pods (cited)            subtotal
api                            DB_POOL_MAX=5 :63      1 (Node, no cluster)    HPA maxReplicas 10 :12        50
worker                         5 :86                  1                       KEDA maxReplicaCount 4 :57    20
migrate Job                    2 (CLI config :28)     1                       parallelism 1                  2
surge (maxSurge 25 %)          5                      1                       3 extra api pods              15
terminating pods (rollout)     5                      1                       old pods inside terminationGracePeriodSeconds, still holding a pool   ≤ 15
exporters, sidecars (2f)       the exporter's own pool, usually 1–3   1                1 per release                   3
cron, BI, consoles, replicas   stated budget or UNKNOWN                                                     ≥ 3
Σ clients                                                                                                    90
usable = max_connections − superuser_reserved_connections − replication slots − provider reserve = UNKNOWN (SHOW it)
```

Read inside each process too. Puma `threads` above the Rails `pool:` makes threads wait for a connection. A worker's `WORKER_CONCURRENCY` × the connections each job holds above the pool size does the same. Go's default `SetMaxOpenConns(0)` has no cap at all. Each prefork worker (gunicorn, uvicorn `--workers`, PM2 cluster, Celery prefork, PHP-FPM children) holds its own pool, and threads share one. Behind a transaction-mode pooler there are **two** budgets. Clients: Σ app pools ≤ `max_client_conn`. Server: `default_pool_size` × (db, user) pairs + `reserve_pool_size` ≤ usable connections. Each read replica has its own ceiling. Managed providers often cap connections per plan, which can sit below the engine's `max_connections`, so read the provider's tier table. **Finding when** Σ at maximum scale exceeds a cited ceiling, or the inner arithmetic makes requests wait on their own process's pool. **Proof:** the table, with every term cited. Then scale to max replicas under load in a disposable environment: no `53300` / `1040`, and acquire waits stay bounded.

### 3. Transaction-mode pooler with session features

```
BAD:   pool_mode = transaction  +  `SET app.tenant_id = …` / LISTEN / pg_advisory_lock() / CREATE TEMP TABLE / WITH HOLD cursor
       PgBouncer < 1.21 (or max_prepared_statements = 0) with a driver that names prepared statements
       Django `.iterator()` server-side cursors without DISABLE_SERVER_SIDE_CURSORS; migrations run through the pooler port
GOOD:  SET LOCAL / set_config(…, true) inside the transaction; pg_advisory_xact_lock; ON COMMIT DROP temp tables; a direct
       connection (session mode, or DIRECT_URL / directUrl) for LISTEN, migrations and session work
```
**Read the code:** Is there a pooler (3a), and which mode, at which version? Behind transaction mode, every 3b hit is a candidate. Does a session `SET` carry tenant or role context (→ security, § Boundaries)? Does a session advisory lock guard a critical section, so that it now excludes nothing? **Finding when** a session-scoped feature runs through a transaction-mode pooler. **Proof:** run the feature twice through the pooler so it lands on different backends. Client 1 sets the value and commits; client 2 reads `current_setting(…, true)`: non-empty is the leak. For locks, client B takes the "held" key and succeeds. For prepared statements, look for `prepared statement … does not exist` / `already exists` under concurrency.

### 4. Serverless functions opening raw connections

```
BAD:   export const handler = async () => { const c = new Client(DB_URL); await c.connect(); … }   // one per invocation
GOOD:  a pool at module scope with max 1 per instance, behind RDS Proxy / a pgbouncer / the provider's pooled endpoint;
       Vercel Fluid's attachDatabasePool(pool); Prisma: a small connection_limit per instance or the pooled URL
```
**Read the code:** Which functions (4a) reach the database, through which host (a pooler or proxy, or the native port)? What is the concurrency limit (reserved, provisioned or platform maximum)? That limit is the §2 multiplier. **Finding when** concurrent invocations × pool per instance can exceed the ceiling with no proxy in between. **Proof:** an invocation burst at the concurrency limit in a disposable environment; the database connection count stays within the proxy's pool.

### 5. No statement timeout

```
BAD:   statementTimeoutMs: 0 in config, never passed to the pool      ·   no ALTER ROLE app SET statement_timeout
GOOD:  ALTER ROLE app SET statement_timeout = '15s';  (a separate role with a larger limit for reports, ETL and migrations)
       or the driver's startup parameter on every pooled connection
```
**Read the code:** Follow the value from env to config to driver option (5a). A setting that is read but never handed to the driver does nothing. Look for a role-level `SET` (5b) and for a managed parameter group. The Postgres docs advise against a global `statement_timeout` in `postgresql.conf` (precedent 36). Do reporting and migration roles get their own limits? **Finding when** an application session can run a statement with no upper bound. **Proof:** through the app's own pool, with the timeout set via the production path, `SELECT pg_sleep(<timeout + 1 s>)` is cancelled with `57014`; it fails before (`snippets/proof-oracles.md` § "Timeout firing", V22).

### 6. No idle-in-transaction, transaction or lock timeout

```
BAD:   no idle_in_transaction_session_timeout anywhere; PgBouncer idle_transaction_timeout = 0; Prisma 8 (RC) has no transaction timeout
GOOD:  ALTER ROLE app SET idle_in_transaction_session_timeout = '30s';  lock_timeout per role; transaction_timeout (PG 17+)
```
**Read the code:** Which of the backstops (6a) apply to application sessions? What bounds a transaction that `transaction-scan` §1 or §6 would hold open? `idle_session_timeout` is the wrong tool behind a pooler, because the pooler does not expect the server to close its connections. **Finding when** an application session can sit idle in a transaction, or wait on a lock, without bound. **Proof:** open a transaction through the app's pool and idle past the timeout; the server ends the session. Hold a row lock in one session; the app's update fails with `55P03` within `lock_timeout`.

### 7. No acquire timeout, lifetime or validation

```
BAD:   new Pool({ max: 10 })                         // connectionTimeoutMillis 0: a saturated pool hangs every request
       sql.Open(...) with no SetConnMaxLifetime        // a connection reused across a failover or past the LB idle limit
GOOD:  an acquire timeout below the request budget; a max lifetime below the server's and the load balancer's idle limits;
       pre-ping or validation where the lane offers it
```
**Read the code:** For each pool (2a, 2b), which of acquire timeout, lifetime and validation are set (7a), and which defaults apply at the installed version (lane table)? **Finding when** a saturated pool makes requests wait without bound, or connections can outlive the server's or proxy's idle cutoff. **Proof:** hold every pool connection, and the next request fails within the acquire timeout instead of hanging. Then idle the pool past the server's `wait_timeout`, and the next query succeeds.

### 8. Read-after-write or a correctness read on a replica

```
BAD:   MikroORM replicas with preferReadReplicas left at true: `await em.flush(); return em.findOne(Order, id)` reads a replica
       a permission, balance or uniqueness check routed to the reader endpoint
GOOD:  `{ connectionType: 'write' }` for reads that follow a write or decide one; a sticky-primary window after writes;
       an LSN / GTID wait; analytics and lists on the replica
```
**Read the code:** Are replicas configured (8a), and what does the default route do with a plain read? For each handler that writes and then reads the same entity outside a transaction, and for each authorization, balance or uniqueness check, which connection serves the read? The same holds **across processes**: a job, consumer or webhook handler triggered by a write (enqueued after the commit) that reads the row on the replica can run before replay reaches it and see "not found" or the old value. Is lag monitored (8c)? Absence of monitoring is Hardening. **Finding when** a read that must see the latest write can be served by an asynchronous replica. **Proof:** in a test environment, pause replay on the replica (`SELECT pg_wal_replay_pause();`), write then read through the app, and the read must come from the primary. Resume with `pg_wal_replay_resume()`.

### 9. A connection, cursor or query runner not released

```
BAD:   const client = await pool.connect(); await client.query(sql); client.release();    // a throw skips release
       rows, err := db.Query(q)  … for rows.Next() { … }                                    // no defer rows.Close()
GOOD:  try { … } finally { client.release() }  ·  pool.query() for one-shot statements  ·  defer rows.Close()  ·  with engine.connect() as c:
```
**Read the code:** Does every path, including `throw`, early `return` and a client disconnect, release the checkout (9a–9d)? A framework-managed session (Django, Rails, Spring `@Transactional`) releases for you. **Finding when** an error path can keep a connection checked out. **Proof:** force the error path 2 × pool-size times, then a normal request still succeeds within the acquire timeout, and the pool's in-use count returns to its baseline (node-postgres `pool.totalCount` / `idleCount`, Go `DB.Stats().InUse`, HikariCP `leakDetectionThreshold`).

## Live lane (read-only; when a database is reachable)

These rows feed `/db-audit`'s L4 check. Connect **as the application role**, because role-level settings differ from the superuser's.

```sql
SHOW max_connections; SHOW superuser_reserved_connections; SHOW max_wal_senders;
SELECT count(*) AS other_clients FROM pg_stat_activity WHERE usename <> current_user;
SHOW statement_timeout; SHOW lock_timeout; SHOW idle_in_transaction_session_timeout;   -- transaction_timeout too on PG 17+
SELECT rolname, rolconfig FROM pg_roles WHERE rolconfig IS NOT NULL;                  -- ALTER ROLE … SET values
SELECT application_name, state, count(*) FROM pg_stat_activity GROUP BY 1, 2 ORDER BY 3 DESC;
SELECT now() - pg_last_xact_replay_timestamp() AS replica_lag;                       -- on each replica
```
MySQL: `SHOW VARIABLES WHERE Variable_name IN ('max_connections', 'wait_timeout', 'max_execution_time', 'innodb_lock_wait_timeout');` and `SELECT USER, COUNT(*) FROM information_schema.PROCESSLIST GROUP BY USER;`. PgBouncer admin console: `SHOW CONFIG;`, `SHOW POOLS;`.

## Output

```
connection-config-scan — lanes: node-postgres via MikroORM 6.6, kubernetes (HPA, KEDA), pgbouncer absent
Engine: postgres 16 (managed; tier table: 47 connections) · replicas: 1 reader, preferReadReplicas left at its default (true)

Findings: 1 · Unconfirmed: 2

1. deploy/k8s/hpa.yaml:12                                    [report-flagged]    high
   §2 connection budget — api 5 × 10 + worker 5 × 4 + migrate 2 + surge 15 = 87 against max_connections
   UNKNOWN: the README states 97 usable, the provider tier table states 47. Settling probe: SHOW max_connections
   as the app role. Fix: lower DB_POOL_MAX or maxReplicas until Σ ≤ usable − 10 %, or put a transaction-mode pooler in front.

2. src/orders/confirm-order.service.ts:52                    [report-with-fix]   medium
   §8 read-after-write on a replica — `await em.flush()` then `em.findOne(Order, id)` outside a transaction;
   `replicas` is set at src/orm.config.ts:22 with preferReadReplicas at its default, so the response reads the
   replica. Reached by POST /orders/:id/confirm. Proof: replay paused on the test replica → the response shows the
   pre-confirm status (fails). Fix: `{ connectionType: 'write' }` on that read, or read inside the transaction.

3. src/db/pool.ts:31                                         [report-flagged]    medium
   §6 no idle-in-transaction timeout — statement and lock timeouts are wired; idle_in_transaction_session_timeout
   and transaction_timeout are set nowhere in the repo. Settling probe: SHOW idle_in_transaction_session_timeout as
   the app role. Fix: ALTER ROLE app SET idle_in_transaction_session_timeout = '30s'.

Verification: 11 candidates → 1 finding · 2 unconfirmed · 3 hardening · 0 pre-existing · 5 refuted

Class coverage:
  §1  client per request          checked (15 hits → 0 findings; all CLIs and the migrate Job, counted in §2)
  §2  connection budget           checked (budget table built; 1 term UNKNOWN → 1 unconfirmed)
  §3  pooler session features     N/A (no pooler in any manifest or URL)
  §4  serverless                  N/A (no function manifest or handler)
  §5  statement timeout           checked (6 hits → 0 findings)
  §6  idle / transaction / lock   checked (4 hits → 1 unconfirmed)
  §7  acquire / lifetime          checked (4 hits → 0 findings)
  §8  replica reads               checked (4 config + 3 code hits → 1 finding; lag unmonitored → hardening)
  §9  unreleased connections      checked (0 hits)
```

`[report-with-fix]`: every term is cited, the oracle or the arithmetic proves it, and the fix is a config or code change. `[report-flagged]`: one term is `UNKNOWN`, or the fix is an operational decision (a pooler, a tier change). The row names the missing input and the probe. The coverage block lists **all nine** classes on every run: `checked (k hits → m findings)`, `N/A (<reason>)` or `blocked (<reason>)`. A partial review reads `Live, unreviewed (k files / n hits)`.

## False positives / precedents

The verifier reads `snippets/precedents/data.md` § "Connections, poolers, replicas and timeouts" (precedents 33–37), `snippets/precedents/performance.md` § "Capacity and volume" (precedent 37: a bigger pool is not a fix), and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:

- **A large app-side pool behind a transaction-mode pooler is fine.** The server-side pool is the real limit. Budget the pooler's numbers instead.
- **`connection_limit = 1` or `NullPool` per serverless instance behind an external pooler** is the intended configuration.
- **One-off CLIs, seeds and migration runners** that open their own ORM are not §1. They are §2 budget terms while they run.
- **Protocol-level prepared statements behind PgBouncer ≥ 1.21** with `max_prepared_statements > 0` (precedent 33). **`SET LOCAL` inside a transaction** (precedent 34). **Analytics on a replica** (precedent 35). **ETL and migration roles with larger timeouts** (precedent 36).
- **SQLite is in-process.** It has no client-server pool, so §1, §2, §4 and §7 are N/A. Its session pragmas are `schema-integrity-scan`'s.

## When to run

- On any diff touching DB client or pool config, an env file, compose, Kubernetes, Helm, Terraform, a process manager or pooler config, a replica route, or a code path that checks out a connection: the `/db-audit` dispatch signal.
- On every whole-repo `/db-audit`, reporting all nine classes and the budget table.
- Before raising replica counts or autoscaler maxima, adding a worker fleet or a serverless function against a shared database, or moving to a managed tier.
- After `too many clients`, acquire timeouts, `prepared statement … does not exist`, a runaway query, or a stale read report.

## Halt conditions

- Do not report a high row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/data.md`](../../../../snippets/precedents/data.md). Under `/db-audit` that happens in its verification phase. Run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on any §2 row without the budget table, with every term cited or marked `UNKNOWN`. Never fill a term from memory or from "typical" values.
- Do not propose raising `max_connections` or the pool size as the fix for exhaustion without the arithmetic. The fixes are fewer or smaller pools, a pooler, or a shorter hold time.
- Do not run a probe that sets server-wide parameters, kills sessions or pauses replay outside a disposable environment the operator named. The live lane is read-only.
- Do not print "connections look fine" without the class-coverage block. A class whose grep did not run is `blocked`, never `checked`.

## Related

- `/db-audit` dispatches this skill, prints its budget table in the bound-verification block and folds its coverage into the class ledger. `/db-fix` closes the findings: arithmetic-derived pool sizes, role-level timeouts, pooler-safe session handling and primary-pinned reads, then re-runs this detector.
- `transaction-scan` (this pack) owns what runs inside a connection's transaction, and `schema-integrity-scan` (this pack) owns the integrity pragmas and SQL modes.
- `database/ai-patterns/connection-pooling.md` and `database/ai-patterns/read-replicas.md` hold the sizing, pooler-mode and routing method this skill's fixes apply. `@database-optimizer` tunes the per-workload numbers.
- `@tenant-isolation-reviewer` (security pack, when installed) owns tenant context behind a pooler. `@capacity-planner` (distributed-systems pack, when installed) consumes the budget table. `request-path-scan` (performance pack, when installed) owns non-database clients built per call.
- `snippets/proof-oracles.md` § "Timeout firing" and § "Socket and handle count" hold the test shapes per stack.
