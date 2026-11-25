---
name: request-path-scan
description: Find what slows the request path or breaks on a second replica — sequential awaits, unbounded fan-out, network N+1, blocking or CPU work on the event loop, full buffering, clients built per call, missing timeouts and load shedding, and in-process state, files, schedulers, broadcasts and jobs — each proved by a run-invariant oracle.
kind: skill
pack: performance
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: request-path-scan

## Premise

A request's latency is the sum of what it waits for, and a server's capacity is what one replica can do times the number of replicas. This skill covers the three ways code breaks that arithmetic. **Request-path cost** is waiting in series, fanning out without a cap, calling the network once per element, blocking the event loop, burning CPU on the request thread, buffering whole payloads, or rebuilding clients per call. **Missing overload controls** are an outbound call with no deadline, a server with no timeouts or limits, nothing that sheds load, and a health probe that restarts every pod together. **Horizontal-scale blockers** are state, files, schedules, broadcasts and jobs that work on one replica and break on two. The research behind this pack found no published agent skill that covers the scale family (research catalog, 2026-10-02).

**Every finding cites the code `<file:line>`, the entry point that reaches it, the condition that makes it cost or break (N, payload size, concurrency, replica count, each cited), the proof (or the probe that would settle it), and the fix.** A grep hit is never a finding. "Request path looks fine" is never printed without the class-coverage block (§ Output).

**Existence by a run-invariant oracle; cost by noise-aware timing.** A run-invariant check proves the defect exists: the call count at N = 2 and N = 20, the peak in-flight count, event-loop delay against a control, the time ratio at N vs 10N, a timeout that fires, a socket count, or a duplicate-execution count behind two replicas. See [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § "The core rule: existence by invariant, cost by statistics". A p95 or RPS delta only **ranks** a proven finding. A candidate read in code with no harness to run its oracle is **Unconfirmed**, carrying the exact probe. It is never dropped as "speculative", and never promoted to Finding on reading alone ([`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 2, gate 6).

## The rule

A candidate is a finding when all four hold:

1. **A production path runs it.** A route, resolver, consumer, cron or webhook, followed call by call. Boot code, CLIs, seeds, tests and one-off scripts fail here (`precedents/performance.md`, precedent 23).
2. **The condition grows or occurs.** N, payload or concurrency grows with data or the request, or the user controls it. A downstream really can stall. For §16–§24, deployment evidence shows more than one replica or process (grep 0). One replica by design makes the row `latent` (Hardening), not Refuted.
3. **No control on the path stops it.** A limiter, an outer deadline, a shared store, a lock with a fencing token, a dedupe reserve, the proxy, or an edge setting. Read each one; never assume it.
4. **The oracle fires, failing first.** Alternatively, for a static-fact class (a missing timeout, an absent shared store, a config pair whose arithmetic is wrong), every term of the trace is cited.

## Boundaries

- **Database round trips** per element → `n-plus-one-scan`. Unbounded reads → `query-shape-scan`. DB pool, statement and acquire timeouts and the connection budget across replicas → `connection-config-scan`. External I/O inside a transaction and queue claims without `SKIP LOCKED` → `transaction-scan`. Auto schema sync at boot → `schema-integrity-scan` § 8. These are database-pack skills: when that pack is not installed, the row reads `N/A (owner pack database not installed)`.
- **Memory growth** (unbounded maps by size, listeners, timers, unit-of-work growth) → `memory-growth-scan`, and **cache TTL, key dimensions, invalidation and stampede** → `caching-scan` (both this pack). Here, a process-local map or cache is judged only for what breaks across replicas (§17, §18).
- **Retry policy** (eligibility, caps, backoff, retries at several layers) → `retry-deadline-scan` §1–§8; **consumer idempotency, poison/DLQ and lock or visibility vs run time** → `messaging-scan` §2, §3 and §6, which own them (§24 here is their fallback); a lock's own mechanics (owner check, TTL, renewal) → `coordination-scan` §1–§4; breakers and the reserve design → `@resilience-reviewer` (all distributed-systems pack, when installed). This skill detects the missing timeout (§12) and hands over the call table. Without that pack, the GOOD blocks here are the contract and §24 grades. Capacity math across services → `@capacity-planner`.
- **Business invariants** (money, stock, quota, single-use, OTP and login attempt counters) held in one process, and non-idempotent payment endpoints → `logic-race-scan` § "8. Limits, quotas and counters held in one process", § "5. Check-then-act on a balance, stock or limit" and § "4. Missing idempotency on money and side-effect endpoints" (security pack, when installed; dedupe by `<file:line>`). Without the security pack, report it here, tagged `security-class (owner pack not installed)`.
- **ReDoS** → `injection-scan` § "13. ReDoS". **GraphQL depth and cost limits** → `@api-security-reviewer` § "GraphQL (if the API exposes a GraphQL endpoint)". **N requests from the browser** → frontend `client-data-scan` §1 (when the frontend pack is installed; without it, `/bundle-perf` prints row W1 N/A).
- **Super-linear work** (CX-1…CX-5) → algorithms `complexity-scan` §1–§5, which owns the class when the algorithms pack is installed: §11 here then prints its hits as `→ complexity-scan` and does not grade them. Without that pack, 11a/11b run and grade here (the `asymptotic-complexity` row in `ownership.json`). **Fixes:** §1 and §2 → backend `parallelize-independent-ops` (when installed; its independence gate is kept). §11 rewrites → `/design-algorithm --from-audit` (algorithms pack, when installed; `/analyze-complexity` is that pack's whole-repo audit). Everything else → `/perf-fix`.

## Adapt to the codebase

Read the runtime, framework and worker library **with versions** from the manifests and lockfile. The request model decides which classes exist at all: an event-loop stall is a fabrication on a thread-per-request server (precedent 27). Print the lanes you ran in the output header.

| Lane | Request model | The ORM in this lane | What blocks | Bounded-parallel primitive | Shared store for sessions · limits · locks | Scheduler · queue worker |
|---|---|---|---|---|---|---|
| **Node** (Express, Fastify, NestJS on either, Next route handlers) | one event loop per process; × PM2 / `cluster` × replicas | MikroORM, Prisma, TypeORM, Drizzle, Sequelize, Knex: async I/O, never a loop stall (their hydration CPU is) | `*Sync(` fs, crypto, zlib, child_process; sync bcrypt; large `JSON` | `p-limit`, `p-map`, `Promise.all` per fixed chunk | a session `store`, `express-rate-limit` `store`, `@nestjs/throttler` `storage`, `@fastify/rate-limit` `redis` | `@nestjs/schedule` runs in every instance; BullMQ `Worker` `concurrency` (default 1) |
| **Python async** (FastAPI, Starlette, Django ASGI) | event loop; sync `def` endpoints share AnyIO's 40-token thread limiter | Django ORM is sync: in `async def` use its `a…` methods (`aget`, `acount`) or `sync_to_async`; SQLAlchemy needs `AsyncSession` | `requests`, `time.sleep`, `psycopg2`, `boto3`, `open()` (ruff `ASYNC`) | `asyncio.Semaphore` + `gather`, `TaskGroup` | Redis-backed cache and session; slowapi / flask-limiter `storage_uri=redis://` | Celery (prefetch multiplier 4; one beat); APScheduler in its own process |
| **Python sync** (Django / DRF, Flask on gunicorn) | one worker per request; GIL per process | Django ORM, SQLAlchemy | CPU holds the worker (capacity, precedent 27) | `ThreadPoolExecutor(max_workers=…)` | as above | as above |
| **Go** (net/http, gin, chi) | goroutine per request | GORM, sqlx, pgx block only their goroutine | a lock across I/O; a lost request `ctx` | `errgroup.SetLimit`, a semaphore channel | Redis-backed limiter (`rate.NewLimiter` is per process) | `robfig/cron` per process + a lock; asynq worker concurrency |
| **JVM** (Spring MVC, WebFlux, Quarkus) | MVC thread or virtual thread per request; WebFlux event loop | Hibernate / JPA and JDBC block: fine on MVC, a finding on a Netty thread (R2DBC there) | `.block()`; JDBC in reactive code; `synchronized` + I/O with virtual threads on JDK < 24 | a bounded `ThreadPoolExecutor`, `StructuredTaskScope` | Spring Session (Redis / JDBC); Bucket4j with a proxy manager | `@Scheduled` + ShedLock; Quartz JDBC clustered; listener `concurrency` / `prefetch` |
| **.NET** (ASP.NET Core) | thread pool + async | EF Core async API; sync `.ToList()` in an async handler holds a pool thread | `.Result`, `.Wait()`, `GetAwaiter().GetResult()` | `Parallel.ForEachAsync` with `MaxDegreeOfParallelism`, `SemaphoreSlim` | DataProtection `PersistKeysTo…`; a distributed cache; the built-in rate limiter is per instance | `BackgroundService` runs per instance; Hangfire / Quartz clustered |
| **Ruby** (Rails on Puma, Sidekiq) | Puma threads × workers under the GVL | ActiveRecord blocks its thread; pool ≥ threads | CPU in controllers (GVL wait) | `concurrent-ruby` with a fixed pool | Redis `cache_store` and session store; Rack::Attack on a shared cache | solid_queue / good_job recurring (DB-deduped); Sidekiq `concurrency` |
| **PHP** (Laravel on FPM or Octane) | a process per request (FPM); long-lived workers under Octane | Eloquent blocks its process | — | `Http::pool` over a bounded set | `SESSION_DRIVER` / `CACHE_STORE` redis or database | `Schedule::…->onOneServer()`; queue workers, Horizon |

Defaults in this table come from the research catalog dated 2026-10-02. Confirm a default against the installed version before a row rests on it, and label it `DEFAULT`.

**Context before hunting** (once per run). Map the entry points and their call rates, and rank list, search, export, import, webhook and consumer paths first. Read the deployment shape from grep 0 and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 2 (G4): replicas, autoscaler maxima, workers per pod, serverless, and the LB idle timeout. A line from a Helm values file for a logging chart is not the API's replica count. Then list the assumptions nothing enforces: "lists are small", "this runs on one pod", "the job runs once".

## Pre-flight greps

Run as **one** script (shell state does not survive between tool calls). Grep **N** feeds detector **§N**. Every `rg` names its path: given no path, `rg` reads stdin whenever stdin is a pipe, and under an agent's shell that is a silent zero-hit run. Code greps search `"${ROOTS[@]}"`, and config greps (manifests, Dockerfiles, env, IaC) search `.` with `XC`. `X` drops tests, migrations, generated code, catalogs and browser components. Variables are written `${NAME}`, because zsh reads `$NAME[…]` as a subscript. Any `rg` error on stderr is a failed grep, never zero hits.

```bash
ROOTS=(.)   # the server-side code: in a monorepo name the apps (ROOTS=(apps/api services/worker)); config greps always search .
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/target/**' -g '!**/.venv/**' -g '!**/.next/**'
   -g '!**/generated/**' -g '!**/temp/**' -g '!*.{md,mdx,json,lock,snap,map,svg,txt,csv,sql,html,css,scss}' -g '!**/*.min.*' -g '!**/docs/**' -g '!/ai/**'
   -g '!**/{test,tests,spec,e2e,__tests__,__mocks__,mocks,__snapshots__,fixtures,__fixtures__,testdata,seeds,seeders,factories}/**'
   -g '!**/*{.,_,-}{test,spec,e2e-spec,mock,stories}.*' -g '!**/test_*.py' -g '!**/conftest.py' -g '!**/*.{tsx,jsx,vue,svelte}'
   -g '!**/migrations/**' -g '!**/db/migrate/**' -g '!**/{locales,locale,i18n,translations}/**' -g '!**/*lock.y*ml')
XC=(--hidden -g '!.git/**' -g '!.claude/**' -g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/.venv/**' -g '!**/.next/**'
    -g '!*.{md,mdx,lock,snap,map,svg,csv}' -g '!**/{package-lock,composer,npm-shrinkwrap}.json' -g '!**/pnpm-lock.yaml' -g '!**/docs/**' -g '!/ai/**'
    -g '!**/{test,tests,spec,e2e,__tests__,__mocks__,mocks,__snapshots__,fixtures,__fixtures__,testdata}/**' -g '!**/*{.,_,-}{test,spec,e2e-spec,mock}.*' -g '!**/migrations/**' -g '!**/db/migrate/**')
NC=(rg -v --pcre2 '^[^:]+[:-]\d+[:-]\s*(//|/\*|\*(\s|/|$)|#(?!\{)|<!--|--\s)')
FLD='^\S+:\d+:\s*(private|protected|public|readonly|static|export|module\.exports)\b'
B='(?:[^()]|\((?:[^()]|\([^()]*\))*\))*?'
LOOP='(?:for\s*\(|for\s+await\b|for\s+\w+(?:,\s*\w+)*\s+in\s|for\s+_?,?\s*\w+\s*:?=\s*range\b|foreach\s*\(|[^\n]*\.(?:forEach|map|each)\s*(?:\(\s*async\b|\s*do\b))'
for t in js ts py go java kotlin ruby php cs; do printf '%s=%s ' "$t" "$(rg --files -t "$t" "${X[@]}" "${ROOTS[@]}" | wc -l | tr -d ' ')"; done; echo
# 0. Deployment shape (gate 7 for §12–§24): replicas, autoscalers, workers, LB idle timeout, stickiness. Confirm the workload each line belongs to.
rg -n --pcre2 '^\s*(replicas|minReplicas|maxReplicas|minReplicaCount|maxReplicaCount|desiredCount|desired_count|instances|workers|threads)\s*[:=]\s*["\x27]?[\w$]|\bkind:\s*(HorizontalPodAutoscaler|ScaledObject)\b|--(workers|concurrency|scale)[ =]\S|\bexec_mode\s*:\s*["\x27]?cluster|\b(WEB_CONCURRENCY|WORKER_CONCURRENCY)\b|\bidle_timeout\b|\bsessionAffinity:\s*ClientIP|\bip_hash\b|\bsticky\b|\bstickiness\b' -g '*.{yml,yaml,toml,tf,hcl,conf,ini,cfg}' -g 'Procfile*' -g 'Dockerfile*' -g 'ecosystem.config.*' -g '*gunicorn*.py' -g 'puma.rb' -g '.env*' "${XC[@]}" . | "${NC[@]}"
# 1. 1a two consecutive awaits whose second line does not use the first's binding; 1b an await inside a loop body (DB callees go to n-plus-one-scan).
rg -n -U --pcre2 '^[ \t]*(?:(?:const|let|var|final|val)\s+)?(?:\{[^}\n]*\}|\[[^\]\n]*\]|(?<v>[\w$]+))(?:\s*:\s*[^=\n]+)?\s*=\s*await\s+(?!import\()[^\n]+(?=\n(?:[ \t]*\n)?[ \t]*(?:(?:const|let|var|final|val)\s+)?(?:\{[^}\n]*\}|\[[^\]\n]*\]|[\w$]+)(?:\s*:\s*[^=\n]+)?\s*=\s*await\s+(?!import\()(?(<v>)(?![^\n]*\b\k<v>\b)))' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n -U --pcre2 "^[ \\t]*${LOOP}[^\\n]*(?=\\n(?:[^\\n]*\\n){0,12}?[^\\n]*\\bawait\\s)" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 2. 2a fan-out over a mapped list; 2b a goroutine per item; 2c files holding a limiter, hand-rolled too: `.slice(i, i + K)`, `*_AT_ONCE`, a Bulkhead (a 2a hit outside them is uncapped until read).
rg -n --pcre2 'Promise\.(all|allSettled|any|race)\(\s*[\w$.?]+\.map\(|\.forEach\(\s*async\b|asyncio\.gather\(\s*\*|\.create_task\(|Task\.WhenAll\([^)]*\.Select\(|\.parallelStream\(\)|CompletableFuture\.(supplyAsync|runAsync)\(|\bThread\.new\b|Parallel\.ForEach\(' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n -U --pcre2 '^\s*for\b[^\n{]*\{(?=[ \t]*\n(?:[^\n]*\n){0,3}?\s*go\s+(?:func\b|\w+\())' -t go "${X[@]}" "${ROOTS[@]}"
rg -l --pcre2 '\bp-limit\b|\bpLimit\(|\bp-map\b|\bpMap\(|\bSemaphore\(|\.SetLimit\(|\bBottleneck\b|MaxDegreeOfParallelism|\bconcurrency\s*:\s*\d|\.slice\(\s*(\w+)\s*,\s*\1\s*\+\s*\w+\s*\)|\b[A-Z][A-Z0-9_]*_(?:AT_ONCE|CONCURRENCY|PARALLELISM|IN_FLIGHT)\b|\bclass\s+\w*Bulkhead\b|\bnew\s+\w*Bulkhead\(' "${X[@]}" "${ROOTS[@]}"
# 3. An outbound client, cache or SDK call awaited inside a loop body.
rg -n -U --pcre2 "^[ \\t]*${LOOP}[^\\n]*(?=\\n(?:[^\\n]*\\n){0,12}?[^\\n]*(?:\\bawait\\s+(?:fetch|axios(?:\\.\\w+)?|got|ky|undici\\.request|firstValueFrom|lastValueFrom|this\\.http(?:Service)?\\.\\w+|[\\w.]*(?:[cC]lient|[rR]edis|[cC]ache|[sS]torage|[sS]3|[sS]qs|[sS]ns|[sS]tripe|[oO]pen[aA][iI]|[aA]nthropic|[mM]ailer|[qQ]ueue)\\.\\w+)\\s*\\(|\\brequests\\.(?:get|post|put)\\(|\\bhttp\\.(?:Get|Post)\\(|\\bclient\\.Do\\(|\\bHttp::\\w+\\())" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 4. 4a Node sync fs / child_process inside a function (module-top-level lines are boot); 4b blocking calls in Python files with async def; 4c Reactor .block(); 4d .NET sync-over-async.
rg -n --pcre2 '^[ \t]+.*\b(readFileSync|writeFileSync|appendFileSync|existsSync|statSync|lstatSync|readdirSync|mkdirSync|rmSync|unlinkSync|copyFileSync|renameSync|realpathSync|accessSync|openSync|readSync|writeSync|execSync|execFileSync|spawnSync)\(' -t js -t ts "${X[@]}" "${ROOTS[@]}" | rg -v --pcre2 "${FLD}" | "${NC[@]}"
rg -l0 --pcre2 '^\s*async\s+def\s' -t py "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -n --pcre2 '\brequests\.(get|post|put|patch|delete|head|request|Session)\b|\burllib\.request\b|\btime\.sleep\(|\b(psycopg2|pymysql|MySQLdb)\.|\bsqlite3\.connect\(|\bboto3\.(client|resource)\(|\bredis\.(Redis|StrictRedis)\(|\.objects\.(get|filter|all|create|update|count|exists)\(|\bsubprocess\.(run|call|check_output|Popen)\(|\bhttpx\.(get|post|Client)\(|(?<![\w.])open\(' | "${NC[@]}"
rg -n --pcre2 '\.block(First|Last)?\(\)|\.toFuture\(\)\.get\(\)' -t java -t kotlin "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 '\.Result\b|\.Wait\(\)|\.GetAwaiter\(\)\.GetResult\(\)|Task\.WaitAll\(|Thread\.Sleep\(|\basync\s+void\b' -t cs "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 5. CPU work that runs on the request thread: sync crypto and zlib, sync bcrypt, the JSON deep-clone idiom, image decode.
rg -n --pcre2 '\b(pbkdf2Sync|scryptSync|generateKeyPairSync|generatePrimeSync|hkdfSync|randomFillSync|gzipSync|gunzipSync|deflateSync|inflateSync|deflateRawSync|inflateRawSync|unzipSync|brotliCompressSync|brotliDecompressSync|zstdCompressSync|zstdDecompressSync)\(|\bbcrypt(js)?\.(hashSync|compareSync|genSaltSync)\(|JSON\.parse\(\s*JSON\.stringify\(|\bhashlib\.(pbkdf2_hmac|scrypt)\(|\bbcrypt\.(hashpw|checkpw)\(|\bImage\.open\(|\bBCrypt::Password\.create\b' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 6. 6a whole bodies buffered into memory; 6b files that configure response compression (none here and none at the edge = a §6 row).
rg -n --pcre2 '\.toArray\(\)|responseType\s*:\s*["\x27](arraybuffer|blob)|\bawait\s+[\w.]+\.(arrayBuffer|buffer|blob)\(\)|\bfs\.promises\.readFile\(|\.fetchall\(\)|\bmodel_validate\(\s*json\.loads\(|\b(io|ioutil)\.ReadAll\(|\.readAllBytes\(\)|\bres\.(send|json)\(\s*await\s|\.toBuffer\(\)|\bBuffer\.concat\(\s*\w*[Cc]hunks\b' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -l --pcre2 '\bcompression\(|@fastify/compress|\bGZipMiddleware\b|UseResponseCompression|\bgzip\s+on\b|\bencode\s+(gzip|zstd)\b|\bRack::Deflater\b' "${XC[@]}" .
# 7. An outbound client, agent or SDK constructed inside a function (class-field initializers run once per provider and are dropped).
rg -n --pcre2 '^[ \t]+.*(\baxios\.create\(|\bnew\s+(?:https?\.)?Agent\(|\bnew\s+(?:Redis|IORedis|Cluster)\(|\bcreateClient\(|\bnew\s+(?:S3|SQS|SNS|DynamoDB|SES|Kinesis|EventBridge|SecretsManager)Client\(|\bnew\s+(?:Stripe|OpenAI|Anthropic)\(|\bnew\s+HttpClient\(|HttpClient\.new(?:HttpClient|Builder)\(|\bboto3\.(?:client|resource)\(|\bhttpx\.(?:Async)?Client\(|\brequests\.Session\(|\bredis\.(?:Redis|StrictRedis)(?:\.from_url)?\(|\bnew\s+RestTemplate\(|\bWebClient\.(?:create|builder)\(|&http\.Client\{|\bnew\s+(?:Kafka|Queue|Worker|Producer)\()' "${X[@]}" "${ROOTS[@]}" | rg -v --pcre2 "${FLD}" | "${NC[@]}"
# 8. A regex, validator, template, serializer or formatter built inside a function.
rg -n --pcre2 '^[ \t]+.*(\bnew\s+RegExp\(|\bnew\s+Ajv\(|\bajv\.compile\(|\b(?:Handlebars|handlebars|ejs|pug|nunjucks|_)\.compile\(|\bregexp\.MustCompile\(|\bPattern\.compile\(|\bnew\s+ObjectMapper\(|\bnew\s+JsonSerializerOptions\b|\bTypeAdapter\(|\bnew\s+Intl\.(?:NumberFormat|DateTimeFormat|Collator)\()' "${X[@]}" "${ROOTS[@]}" | rg -v --pcre2 "${FLD}" | "${NC[@]}"
# 9. Log arguments formatted eagerly, and console.log on server paths.
rg -n --pcre2 '\blog(?:ger)?\.(?:debug|trace|info)\(\s*f["\x27]|\blog(?:ger)?\.(?:debug|trace)\(\s*String\.format\(|\blog(?:ger)?\.(?:debug|trace)\(\s*"[^"]*"\s*\+|\b(?:logger|log|console)\.(?:debug|trace|log)\([^)]*JSON\.stringify\(|\bconsole\.log\(' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 10. In-process locks (also §18: a process-local lock cannot guard a cross-replica invariant).
rg -n --pcre2 '\bnew\s+(?:Mutex|Semaphore|ReentrantLock|ReentrantReadWriteLock)\b|from\s+["\x27](?:async-mutex|await-lock|async-lock)["\x27]|\.runExclusive\(|\b(?:threading|asyncio)\.(?:Lock|RLock|Semaphore)\(\)|\bsync\.(?:Mutex|RWMutex)\b|\bsynchronized\s*(?:\(|\w)|\block\s*\(\s*\w+\s*\)\s*$|\bMonitor\.Enter\(|\bSemaphoreSlim\(|\bMutex\.new\b' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 11. 11a a linear lookup inside a per-element callback; 11b a linear lookup inside a loop body (ALL_CAPS lists and `title.includes(word)` string tests are skipped).
rg -n --pcre2 '\.(?:filter|map|forEach|some|every|reduce|flatMap|find)\(\s*\(?\s*(\w+)\b[^)]*\)?\s*=>[^\n]*?\b(?!\1\b)(?![A-Z][A-Z0-9_]*\b)[\w$]+(?:\.[\w$]+)*\.(?:includes|indexOf|find|findIndex|some|filter)\(|\.pop\(0\)|\bsum\([^)]*,\s*\[\]\s*\)' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | rg -v --pcre2 '\b[A-Z][A-Z0-9_]*(?:\.\w+)*\.(?:filter|map|forEach|some|every|reduce|flatMap|find)\(|\b\w*(?:[Tt]ext|[Nn]ame|[Tt]itle|[Ll]abel|[Pp]hrase|[Rr]eason|[Mm]essage|[Ss]tr(?:ing)?|[Ll]ower|[Ll]ow|[Rr]aw|[Ss]can|[Pp]ath|[Uu]rl|[Ss]lug|[Ll]ine|[Qq]uery|[Ss]earch|[Hh]aystack)(?:\.toLowerCase\(\)|\.trim\(\))?\.(?:includes|indexOf)\(|\.(?:includes|indexOf)\(\s*[\x27"\x60]'
rg -n -U --pcre2 "^[ \\t]*${LOOP}[^\\n]*(?=\\n(?:[^\\n]*\\n){0,3}?[^\\n]*\\b(?![A-Z][A-Z0-9_]*\\b)[\\w$]+(?:\\.[\\w$]+)*\\.(?:includes|indexOf|contains|index)\\()" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 12. 12a outbound calls with no timeout or signal in the call; 12b a Go handler replacing the request context.
rg -n -U --pcre2 "\\bfetch\\((?!${B}\\b(?:signal|timeout)\\b)|\\baxios(?:\\.(?:get|post|put|patch|delete|head|request|create))?\\((?!${B}\\btimeout\\b)|\\b(?:requests|httpx)\\.(?:get|post|put|patch|delete|head|request)\\((?!${B}\\btimeout\\s*=)|\\btimeout\\s*=\\s*None\\b|\\bhttp\\.(?:Get|Post|Head|PostForm)\\(|\\bhttp\\.DefaultClient\\b|&http\\.Client\\{\\s*\\}|\\bHttpRequest\\.newBuilder\\(|\\bnew\\s+RestTemplate\\(\\s*\\)|InfiniteTimeSpan|\\bNet::HTTP\\.(?:get|start|post)\\(|\\bFaraday\\.new\\((?!${B}timeout)" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 '\bcontext\.(?:Background|TODO)\(\)' -t go "${X[@]}" "${ROOTS[@]}" | rg -v '(^|/)(main\.go|cmd/)' | "${NC[@]}"
# 13. 13a server timeouts, keep-alive and body-limit knobs at every hop (app server; Caddy `keepalive`, ingress-nginx `keep-alive` / `upstream-keepalive-timeout`,
#     HAProxy `timeout http-keep-alive`, Traefik `idleConnTimeout`, Envoy `idle_timeout`); 13b the server bootstraps where they belong; 13c the proxy hops.
rg -n --pcre2 '\b(?:keepAliveTimeout|headersTimeout|requestTimeout|connectionTimeout|bodyLimit|ReadHeaderTimeout|ReadTimeout|WriteTimeout|IdleTimeout|MaxRequestBodySize|client_max_body_size|keepalive_timeout|proxy_read_timeout|--timeout-keep-alive|--keep-alive|keepalive_idle_conns|keepalive_interval|upstream-keepalive-timeout|upstream-keepalive-time|idleConnTimeout|idle_timeout|http-keep-alive)\b|^\s*keepalive\s+\d+\w*\s*$|^\s*["\x27]?keep-alive["\x27]?\s*:\s*["\x27]?\d|^\s*timeout\s+http-keep-alive\b|\bhttp\.ListenAndServe\(|\blimit\s*:\s*["\x27]\d+\s*(?:mb|gb)["\x27]|\bidle_timeout\b' "${XC[@]}" . | "${NC[@]}"
rg -n --pcre2 '\bNestFactory\.create\b|\b[Ff]astify\(\s*\{|\bexpress\(\)|\buvicorn\.run\(|\bhttp\.Server\{|\bcreateServer\(' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 13c. The proxy hops in front of the app: each needs its keep-alive read, or its DEFAULT (precedent 91).
rg -n --pcre2 '^\s*reverse_proxy\b|\bproxy_pass\s+https?://|\bkind:\s*Ingress\b|\bingressClassName\s*:|\bingress-nginx-controller\b|\b(?:traefik|haproxy|envoyproxy)\b[^\n]*\b(?:image|kind|entryPoints)\b' -g '*.{yml,yaml,conf,cfg,toml}' -g 'Caddyfile*' "${XC[@]}" . | "${NC[@]}"
# 14. Unbounded executors and queues, and any admission control or load shedding present.
rg -n --pcre2 'new\s+LinkedBlockingQueue<[^>]*>\(\s*\)|Executors\.new(?:Fixed|Cached)ThreadPool\(|\bqueue\.Queue\(\s*\)|\basyncio\.Queue\(\s*\)|Channel\.CreateUnbounded<|make\(chan\s+[^,)]+,\s*\d{4,}\)|\bnew\s+PQueue\(|\bfastq\(|\basync\.queue\(|\bmaxConnections\b|\blimit_(?:req|conn)\b|under-pressure|ConcurrencyLimiter|AddConcurrencyLimiter|\bmax_concurrency\b|\bloadshed|\bBulkhead\b|\bShedLoad\w*|\bMAX_QUEUE_DEPTH\b|\bRetry-After\b' "${XC[@]}" . | "${NC[@]}"
# 15. 15a probes in manifests; 15b the health handlers they call.
rg -n --pcre2 '\b(?:livenessProbe|readinessProbe|startupProbe)\b' "${XC[@]}" . | "${NC[@]}"
rg -n --pcre2 '@Get\(\s*["\x27](?:health|healthz|live|livez|liveness|ready|readyz|readiness)|["\x27]/(?:health|healthz|live|livez|liveness|ready|readyz|readiness)["\x27]|\bHealthCheckService\b|\bpingCheck\(|HealthIndicator\b|AddHealthChecks\(' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 16. 16a session stores and per-process signing keys in code; 16b stickiness and session drivers in config.
rg -n --pcre2 '\bexpress-session\b|\bcookie-session\b|@fastify/(?:secure-)?session\b|\bnew\s+(?:session\.)?MemoryStore\(|\bSESSION_(?:ENGINE|TYPE|DRIVER)\b|\bsession_store\b|\bAddSession\(|\bAddDistributedMemoryCache\(|\bAddDataProtection\(|\bPersistKeysTo\w*|\b(?:JWT_SECRET|SECRET_KEY|jwtSecret|sessionSecret)\b[^\n]*\b(?:randomBytes|randomUUID|token_hex|token_urlsafe|uuid4?\()' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 '\bsessionAffinity\b|\bip_hash\b|\bsticky\b|\bstickiness\b|\bSESSION_(?:ENGINE|TYPE|DRIVER)\b|spring-session' -g '*.{yml,yaml,conf,tf,hcl,toml,ini,cfg,env,gradle,xml}' -g '.env*' "${XC[@]}" . | "${NC[@]}"
# 17. 17a mutable process state (empty Map/Set at module or provider scope, in-memory caches, embedded SQLite, instance-0 logic); 17b in-memory cache or SQLite drivers in config.
rg -n --pcre2 '^(?:export\s+)?(?:const|let|var)\s+\w+\s*(?::[^=]+)?=\s*new\s+(?:(?:Map|Set)(?:<[^\n]*>)?\(\s*\)|(?:LRUCache|LRU|NodeCache|QuickLRU)\b)|^\s+(?:private|protected|public|static|readonly)\s+(?:readonly\s+|static\s+)?\w+\s*(?::[^=]+)?=\s*new\s+(?:(?:Map|Set)(?:<[^\n]*>)?\(\s*\)|(?:LRUCache|LRU|NodeCache|QuickLRU)\b)|from\s+["\x27](?:lru-cache|node-cache|memory-cache|quick-lru|cache-manager)["\x27]|\bCacheModule\.register(?:Async)?\(|@(?:functools\.)?(?:lru_cache|cache)\b|\bcachetools\.|\bAddMemoryCache\(|\bbetter-sqlite3\b|\bNODE_APP_INSTANCE\b|\bcluster\.is(?:Primary|Master)\b|^(?:let|var)\s+\w*(?:[nN]extId|[cC]ounter|[sS]eq)\w*\s*=\s*\d|^var\s+\w+\s*=\s*(?:map\[|sync\.Map\b)' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 'backends\.locmem|:memory_store\b|\bspring\.cache\.type\b|\bCACHE_(?:STORE|DRIVER)\s*=\s*(?:array|file)|\bbackends\.sqlite3\b|\badapter:\s*sqlite3|DATABASE_URL=["\x27]?(?:file:|sqlite)' -g '*.{py,rb,yml,yaml,properties,env,toml}' -g '.env*' "${XC[@]}" .
# 18. Rate limiters (a library, or a hand-rolled `*Limiter` class), quota counters, dedupe sets and lease locks (read each for a shared store or a fencing token).
rg -n --pcre2 '\bexpress-rate-limit\b|\brateLimit\(|\bRateLimiterMemory\b|\bThrottlerModule\.forRoot(?:Async)?\(|@nestjs/throttler|@fastify/rate-limit|\bnew\s+Bottleneck\(|\bstorage_uri\b|\bflask_limiter\b|\bslowapi\b|\bdjango_ratelimit\b|\bRack::Attack\b|\brate_limit\s+to:|\bBucket4j\b|\bBucket\.builder\(|\bRateLimiter\.create\(|\brate\.NewLimiter\(|\bAddRateLimiter\(|\btollbooth\b|\bprocessing\w*\.(?:add|has)\(|\b[Rr]edlock\b|["\x27]NX["\x27]|\bnx\s*[:=]\s*(?:true|True)\b|\bSET\s+\S+\s+\S+\s+NX\b|\bclass\s+\w*(?:RateLimit\w*|Limiter)\b' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 19. 19a files written to local disk or served from it; 19b per-pod and single-writer volumes.
rg -n --pcre2 '\bmulter\(\s*\{\s*dest\b|\bdiskStorage\(|\bcreateWriteStream\(|\bwriteFile\((?!Sync)|\.save\(\s*os\.path\.join\(|\bFileSystemStorage\b|\bMEDIA_ROOT\b|active_storage\.service\s*=\s*:local|\bstorage\s+:file\b|\bFILESYSTEM_DISK\s*=\s*(?:local|public)|Storage::disk\(\s*["\x27](?:local|public)|\.transferTo\(|\bFiles\.write\(|\bexpress\.static\(|@fastify/static|\bServeStaticModule\b|\bos\.Create\(' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 '\bemptyDir\b|\bReadWriteOnce\b|\bhostPath\b|^\s*-\s*\./[\w./-]*(?:upload|media|storage|files|export|report)\w*:' -g '*.{yml,yaml,tf}' "${XC[@]}" . | "${NC[@]}"
# 20. 20a in-process schedulers, incl. registrations with no decorator at the call site (a NestJS SchedulerRegistry explorer, Hangfire recurring jobs on memory storage); 20b migrations run by a process entrypoint; 20c files holding a lock or leader election,
#     a project helper too (`withLeaderLock`, `lockKey:`); 20d per scheduled method, awaited writes, deletes and sends BEFORE its first lock call (following `this.<method>(` one level) — every replica runs them.
rg -n --pcre2 '\bcron\.schedule\(|\bnew\s+CronJob\(|\bscheduleJob\(|@Cron\(|@Interval\(|@Timeout\(|\bScheduleModule\b|^setInterval\(|\b(?:Background|AsyncIO)Scheduler\(|\bschedule\.every\(|\bbeat_schedule\b|celery[^\n]*(?:\s-B\b|--beat)|\bRufus::Scheduler\b|@Scheduled\(|\bRAMJobStore\b|\bisClustered\b|scheduleAtFixedRate\(|\bcron\.New\(|\bgocron\.|\bPeriodicTimer\b|\bSchedule::|->(?:everyMinute|everyFiveMinutes|hourly|daily|cron)\(|\bSchedulerRegistry\b|\.add(?:CronJob|Interval)\(|\bredbeat\b|\bRecurringJob\.AddOrUpdate\b|\bUse(?:InMemory|Memory)Storage\(' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 '\b(?:prisma\s+migrate\s+deploy|manage\.py\s+migrate|alembic\s+upgrade|db:migrate|sequelize(?:-cli)?\s+db:migrate|migration:run|knex\s+migrate:latest|mikro-orm(?:-esm)?\s+migration:up|goose\s+up|flyway\s+migrate)\b|\bmigrationsRun\s*:\s*true|\bgetMigrator\(\)\.up\(|\bmigrator\.up\(|\bDatabase\.Migrate\(\)|\bMigrateAsync\(\)' -g 'Dockerfile*' -g '*.{sh,yml,yaml,toml,json,ts,js,py,rb,cs,go}' -g 'Procfile*' "${XC[@]}" . | "${NC[@]}"
LK='\bSchedulerLock\b|\bShedLock\b|\bonOneServer\b|pg_try_advisory(?:_xact)?_lock|\bLeaderElect|\bleader[-_ ]?election\b|\bcoordination\.k8s\.io\b|\bwith\w*Lock\b|\bleader[-_]lock\b|\blockKey\s*:|\bLEADER_KEY\b|\b(?:acquire|try)Lock\(|\b[Rr]edlock\b'
rg -l --pcre2 "${LK}" "${XC[@]}" .
rg -l --pcre2 '@(?:Cron|Interval|Timeout|Scheduled)\(' -t ts -t js -t java -t kotlin "${X[@]}" "${ROOTS[@]}" | LK="${LK}" python3 -c '
import os, re, subprocess, sys
LK = os.environ["LK"]; R = lambda f: open(f, errors="replace").read().split("\n")
def body(L, i, d=0, o=False):                    # 0-based start line → (start, end) of its brace-matched body
    for j in range(i, min(len(L), i + 400)):
        for ch in re.sub(r"([\x27\"`]).*?\1", "", L[j]): d += (ch == "{") - (ch == "}"); o = o or ch == "{"
        if o and d <= 0: return i, j
    return i, min(len(L) - 1, i + 60)
lockers = {m[1] or m[2] for f in subprocess.run(["rg", "-l", "--pcre2", LK, *sys.argv[1:]], capture_output=True, text=True).stdout.split() for FL in [R(f)]
           for k, l in enumerate(FL) for m in [re.match(r"\s*export\s+(?:async\s+)?function\s+(\w+)|\s*export\s+const\s+(\w+)\s*=", l)] if m and re.search(LK, "\n".join(FL[k + 1:body(FL, k)[1] + 1]))}
LOCK = re.compile(r"(?:%s)|\b(?:%s)\s*\(" % (LK, "|".join(map(re.escape, sorted(lockers))) or "(?!)"))   # a lock helper, or a function whose body takes one
SIDE = re.compile(r"\bawait\s+[\w.$\[\]]*?\.(?:remove|delete\w*|unlink|purge|destroy|send\w*|publish|emit|enqueue|add|addBulk|put\w*|post|insert\w*|update\w*|upsert\w*|native(?:Delete|Update)|persist\w*|flush|save|create\w*|charge|notify\w*|write\w*|execute)\s*\(")
SIG = r"\(\s*[^)]*\)\s*(?::[^{]*)?\{\s*$"
for f in (l.strip() for l in sys.stdin if l.strip()):
    L = R(f); meth = {m[1]: k for k, l in enumerate(L) for m in [re.match(r"\s*(?:private|protected|public)?\s*(?:async\s+)?(\w+)\s*" + SIG, l)] if m}
    for k in [k for k, l in enumerate(L) if re.search(r"@(?:Cron|Interval|Timeout|Scheduled)\(", l)]:
        m = next((j for j in range(k + 1, min(k + 6, len(L))) if re.search(SIG, L[j])), None)
        if m is None: continue
        hits, st = [], {"lock": None, "seen": set()}
        def walk(a, b, depth):                    # stop at the first lock call; follow this.<method>( one level
            for j in range(a, b + 1):
                if st["lock"]: return
                if j != a and LOCK.search(L[j]): st["lock"] = j + 1; return
                if SIDE.search(L[j]): hits.append(j + 1)
                c = re.search(r"\bthis\.(\w+)\(", L[j])
                if depth and c and c[1] in meth and c[1] not in st["seen"]: st["seen"].add(c[1]); walk(*body(L, meth[c[1]]), depth - 1)
        walk(*body(L, m), 1)
        for h in hits: print("%s:%d  side effect before the lock in %s (lock: %s)" % (f, h, re.search(r"(\w+)\s*\(", L[m])[1], "line %d" % st["lock"] if st["lock"] else "none — every replica runs it; per-replica by design?"))
' "${ROOTS[@]}"
# 21. 21a WebSocket, SSE and subscription fan-out and the adapters that cross replicas; 21b in-memory channel layers in config.
rg -n --pcre2 '@WebSocketGateway\(|\bnew\s+Server\([^)]*\)|\bcreateAdapter\(|@socket\.io/\w+-adapter|\bIoAdapter\b|\bwss\.clients\b|\bInMemoryChannelLayer\b|\bchannels_redis\b|\benableSimpleBroker\(|\bAddSignalR\(|\bnew\s+PubSub\(|\btext/event-stream\b|@Sse\(' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 '\badapter:\s*async\b|\bInMemoryChannelLayer\b' -g '*.{yml,yaml,py}' "${XC[@]}" .
# 22. 22a work started and not awaited (fire-and-forget, in-process background tasks); 22b inline or async-in-process queue drivers.
rg -n --pcre2 '^\s+void\s+[\w.]+\(|\.catch\(\s*\(\s*\w*\s*\)\s*=>\s*(?:\{\s*\}|undefined|null)\s*\)|\bsetTimeout\([^\n]*\b(?:retry|attempt|resend|redeliver)|\bBackgroundTasks\b|\.add_task\(|\basyncio\.create_task\(|\bthreading\.Thread\(|\bexecutor\.submit\(|@Async\b|CompletableFuture\.runAsync\(|\bTask\.Run\(|^\s+go\s+func\(' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 '\bqueue_adapter\s*=\s*:async|\bQUEUE_CONNECTION\s*=\s*sync' -g '*.rb' -g '.env*' "${XC[@]}" .
# 23. Queue workers, their concurrency and prefetch, partitions and the autoscaler signal.
rg -n --pcre2 '\bnew\s+Worker\(|@Processor\(|\bextends\s+WorkerHost\b|\bconcurrency\s*:\s*[\w.]+|\bworker_prefetch_multiplier\b|\bworker_concurrency\b|--concurrency[ =]|\.prefetch\(\s*\d+\s*\)|\bbasic_qos\(|\bprefetch_count\b|\bpartitionsConsumedConcurrently\b|\bMaxNumberOfMessages\b|^\s*:concurrency:|\blagThreshold\b|\bqueueLength\b|\bkind:\s*ScaledObject\b|\bMessageGroupId\b|\btask_routes\b|\bnew\s+Queue\(' "${XC[@]}" . | "${NC[@]}"
# 24. 24a retry, lock, visibility and dead-letter settings in config files and in code that imports a queue library (not an HTTP client's `retry`); 24b consumer files with no dedupe marker anywhere in them.
rg -n --pcre2 '\battempts\s*:\s*\d|\bbackoff\s*:|\blockDuration\b|\bmaxStalledCount\b|\bvisibility_timeout\b|\bVisibilityTimeout\b|\bChangeMessageVisibility\b|\bmax_retries\b|\bautoretry_for\b|\backs_late\b|\bredrive_policy\b|\bdeadLetter\w*|\bdead_letter\w*|x-dead-letter-exchange|DeadLetterPublishingRecoverer|ReportBatchItemFailures|max\.poll\.interval\.ms|\backDeadlineSeconds\b|sidekiq_options[^\n]*retry|\bretryUntil\b' -g '*.{yml,yaml,toml,ini,cfg,properties,tf,hcl,json,py,rb}' -g '.env*' "${XC[@]}" . | "${NC[@]}"
rg -l0 --pcre2 "(?:from\s+|require\(\s*)['\"](?:bullmq|bull|bee-queue|agenda|amqplib|amqp-connection-manager|kafkajs|@aws-sdk/client-sqs|@google-cloud/pubsub|@nestjs/bullmq|@nestjs/bull|@nestjs/microservices)['\"]|\\b(?:Sidekiq|ActiveJob|ShouldQueue|RabbitListener|KafkaListener|SqsListener|JmsListener|WorkerHost|eachMessage|eachBatch)\\b|@Processor\\(|\\bnew\\s+(?:Worker|Queue)\\(|\\b(?:consume|subscribe)\\(\\s*[\x27\x22]" -t js -t ts -t java -t kotlin -t php -t cs -t go "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -Hn --pcre2 '\battempts\s*:\s*\d|\bbackoff\s*:|\blockDuration\b|\bmaxStalledCount\b|\bvisibility_timeout\b|\bVisibilityTimeout\b|\bChangeMessageVisibility\b|\bmax_retries\b|\bautoretry_for\b|\backs_late\b|\bredrive_policy\b|\bdeadLetter\w*|\bdead_letter\w*|x-dead-letter-exchange|DeadLetterPublishingRecoverer|ReportBatchItemFailures|max\.poll\.interval\.ms|\backDeadlineSeconds\b|sidekiq_options[^\n]*retry|\bretryUntil\b' | "${NC[@]}"
rg -l0 --pcre2 '@Processor\(|\bextends\s+WorkerHost\b|\bnew\s+Worker\(|@(?:EventPattern|MessagePattern|RabbitListener|KafkaListener|SqsListener|JmsListener|OnEvent)\(|\b(?:consume|subscribe)\(\s*["\x27]|\beachMessage\b|@(?:shared_task|app\.task)\b|\bdef\s+perform\b|\bSidekiq::(?:Worker|Job)\b|\bShouldQueue\b|\bIConsumer<' "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg --files-without-match --pcre2 '\bidempoten\w*|\bdedup\w*|\bprocessed_(?:messages|events|jobs)\b|\bON\s+CONFLICT\b|\bonConflict\w*\(|\bupsert\w*\(|\binsertOrIgnore\b|\bjobId\s*:|\bShouldBeUnique\b'
```

The greps narrow; reading decides. Three blind spots are structural:
- **Wrappers hide the callee.** `await this.images.fetchCatalogImage(url)` inside a loop is network N+1, but its name is not a client's. Grep 1b lists every per-element await, so follow each callee to the driver: database → `n-plus-one-scan`, network → §3, independent work → §1.
- **Absence is the defect for §12–§16 and §20–§24**: no timeout, no limit, no shared store, no lock, no dedupe. A setting may live outside the repo (an ingress, a gateway, a platform default). Quiet greps mean "not in the repo", never "not configured": the row is Unconfirmed with the setting to read.
- **The ESLint and Ruff lanes are sharper where they run.** `no-await-in-loop` (ESLint core), `n/no-sync` with `allowAtRootLevel` (eslint-plugin-n), `ruff check --select ASYNC,PERF,S113,G004 .`, `golangci-lint run --enable=noctx,bodyclose,contextcheck`, `gosec -include=G112,G114 ./...`, and BlockHound in Reactor tests. A hit there is a candidate under the same read rule.

**Measured** (2026-10-02) on a real NestJS-on-Fastify + MikroORM + Postgres + React monorepo (about 13,000 files) with `ROOTS=(apps/api)`: about 9 s; counts are source / `scripts/` lines.
- Request path: 1a 97 / 13 · 1b 379 / 89 (bulk: § The 3,000-hit path) · 2a 3 (chunks and small domain lists) · 3 21 / 1 · 4 4 / 10 (CA files and a boot `mkdirSync`; one lazy i18n read to check) · 5 2 (deep-clone of small receipts) · 6 0, with 3 files configuring compression · 7 3 / 1 (client factories) · 8 9 / 2 (`Intl.DateTimeFormat` per call) · 9 1 / 104 · 10 0 · 11 57 / 6 (after skipping ALL_CAPS constants; most of the rest are small lists).
- Overload: 12 2 / 2 (a Dockerfile health one-liner, and the shared outbound client whose `init` carries the signal: follow it) · 13 8 (limits and keep-alive set in the bootstrap) · 14 0 · 15 19 probes.
- Scale and queues: 0 27 (mostly logging-chart replicas; the API autoscaler sits in a patch file) · 16 0 (stateless tokens) · 17 8 / 3 (per-process breaker and single-flight maps) · 18 40 (throttler guards, Redis `SET … NX` stores and leader keys) · 19 16 / 1 (a local-disk storage driver among `emptyDir` scratch volumes) · 20 48 `@Cron` / `@Interval` methods, the leader-key files, and migrations run by a Job · 21 5 (a gateway with the Redis adapter) · 22 20 / 7 · 23 16 · 24 50 config lines, and 5 of 7 consumer files with no dedupe marker.
- **Re-measured** (2026-10-15, read-only) on a real NestJS + React monorepo with `ROOTS=(apps/api packages/contracts)`, about 4 s: 2c 0 → 34 limiter files (hand-rolled `.slice(at, at + K)` chunks, `ENQUEUES_AT_ONCE`, a `Bulkhead` class — the old line saw no limiter and left every fan-out "uncapped"); 6a 0 → 3 (`.toBuffer()`, `Buffer.concat(chunks)`); 11a 63 → 42 (callbacks over ALL_CAPS word lists and substring tests on string receivers dropped); 14 0 → 24 (the heavy-read bulkhead, `ShedLoadError`, a queue-depth cap, `Retry-After`); 20c 0 → 45 files (a `withLeaderLock` / `withPeriodLock` helper and its `lockKey:` callers); 20d 4 rows — two retention jobs that delete object-store files before their only lock (the audit's one finding), a per-replica socket re-auth and an unlocked dispatch tick to read; 24a 60 → 24 (HTTP clients' `retry: { attempts }` and two browser files dropped: only queue-importing code and config files are read). 13a still shows only the Node bootstrap: the Caddy → ingress-nginx hops set nothing, so 13c lists the hops and § 91 supplies the defaults to order. On `benchmarks/fixtures/node-api`, 1a returns exactly the seeded sequential awaits. 12a returns the seeded untimed charge and not its sibling refund call, which carries `AbortSignal.timeout`. 17a returns the seeded in-memory limiter map. On `vuln-fullstack`, grep 0 shows `replicas: 3`. 19a lists `diskStorage` uploads and `writeFile` into the uploads directory, served from a per-replica volume. 1b lists the feed import's per-item image fetch. 1a drops the controller's dependent pair (the second await uses the first). 6a lists an image body buffered whole before its size check. `half-built-crm` and `web-dashboard` return no candidate beyond a health route and a `fetchall()` in the database helper. 18 gained a hand-rolled `class …Limiter` alternative (2026-10-21): on `benchmarks/fixtures/*` it adds 1 line, a per-pod login limiter holding its window in a `Map`, which the library-only line never listed.

## The 3,000-hit path

1. **Close path classes with one cited reason.** `scripts/`, `tools/`, `bin/`, probe and load-test folders close as "not request-reachable" only after `rg -n --hidden -g 'Dockerfile*' -g '*.{yml,yaml,toml,json}' -g 'Procfile*' -g '!**/node_modules/**' '<dir>/' .` shows that no image, deployed job or route runs them. Count the class in the coverage line.
2. **Group** by (enclosing function, callee): `rg --json … | jq -r 'select(.type=="match") | "\(.data.path.text):\(.data.line_number)"'`. One decision covers a group with the same callee and the same loop source.
3. **Rank by reachability and rate**: public and list, search, export, import and webhook routes and consumers first. Admin paths carry the largest N (precedent 39).
4. **Read the top 30 groups** with the § questions below.
5. **Prefer a runtime bulk oracle at scale.** Run the e2e suite once with `node --trace-sync-io`, `PYTHONASYNCIODEBUG=1`, BlockHound or an outbound-call counter (nock, MSW, `httptest`) at two fixture sizes. Each stack trace or each count that moves with N is a confirmed site.
6. **Ledger the rest** as `Live, unreviewed (k groups / n hits)` with the command that continues it. Never mark it `checked`.

## Scans for

Severity follows the research catalog's scale. Promote one step for an anonymous or public entry point, or an N the user controls. Demote one step when a cache or proxy provably fronts it, for an admin-only path, or when schema validation caps N. A scale class (§16–§24) on a single replica by design is `latent`: it goes to Hardening. Ids are the performance research catalog's class ids (RT request path, RS resilience, SC scale and queues).

| § | Class | Ids | Default |
|---|---|---|---|
| 1 | Sequential awaits of independent I/O | RT-09 | medium; high when ≥ 300 ms saveable on a hot path |
| 2 | Unbounded fan-out (concurrency ∝ input) | RT-10, RT-05 · CWE-770 | high; critical when N is user-controlled |
| 3 | Network N+1: per-element outbound call where a batch exists | RT-11 · CWE-1050 | high on a list path, else medium |
| 4 | Blocking I/O on the event loop or async runtime | RT-01, RT-02, RT-07, RT-08 · CWE-1322 | critical for a network call in an async handler or reactive loop; else high |
| 5 | CPU-heavy work on the request thread | RT-03 · CWE-1322 | high; critical when the cost scales with user input |
| 6 | Full buffering; payload and serialization cost | RT-14 · CWE-770 | high for uploads and unbounded bodies; else medium |
| 7 | Client, agent or pool built per call; init in a serverless handler | RT-12, RT-17 · CWE-400 | medium; critical for a .NET `HttpClient` per call |
| 8 | Regex, validator, template or serializer built per call | RT-13 | low; medium on a proven-hot path |
| 9 | Eager or synchronous logging in the hot path | RT-13 | low; medium on a proven-hot path |
| 10 | Lock held across I/O, or one hot global lock | RT-06 | high; critical across an untimed network call |
| 11 | Super-linear work on request-sized input | RT-15 · CWE-407 | high when N is user-sized; else low |
| 12 | Outbound call with no timeout, no total deadline or no propagated deadline | RS-01, RS-03 · CWE-1088 | critical on a request path to a remote dependency |
| 13 | Inbound server timeouts and limits (keep-alive vs LB, header read, body size) | RS-02 · CWE-400 | critical internet-facing; medium internal |
| 14 | No admission control, load shedding or bulkhead; synchronized load | RS-04, RS-06 · CWE-770 | high |
| 15 | Health probe that checks a shared dependency | RS-07 | high |
| 16 | Session or auth state in one process; sticky sessions relied on | SC-01 | high; critical on checkout or payment |
| 17 | Process-local state used as truth (L1 cache, embedded SQLite, id counters, "instance 0") | SC-02, SC-10, SC-11 | high; critical for colliding ids; medium for a perf-only L1 |
| 18 | Limiter, quota, dedupe set or lock held per replica; lease with no fencing | SC-03, SC-04 · CWE-799, CWE-362 | high (auth and money limits → security) |
| 19 | Local filesystem for uploads or generated files | SC-05 | high |
| 20 | Once-per-fleet work run per replica: schedulers, startup migrations | SC-06, SC-09 · CWE-837 | critical with side effects; medium when idempotent |
| 21 | Broadcast that reaches one replica (WebSocket, SSE, subscriptions) | SC-07 | high |
| 22 | Durable work held in process memory (fire-and-forget, in-process queues) | SC-08 | critical for payments, emails, webhooks; else medium |
| 23 | Worker concurrency, prefetch, partitions and autoscaling signal vs backlog | SC-12, SC-15, SC-16 | medium; high when it exhausts a pool |
| 24 | Redelivered jobs: no dedupe, lock or visibility shorter than the work, no DLQ | SC-13, SC-14 · CWE-837 | critical with side effects; else high |

### 1. Sequential awaits of independent I/O

```
BAD:   const items = await orders.items(id); const customer = await crm.get(o.customerId); const price = await pricing.quote(o) (Σ latency)
GOOD:  const [items, customer, price] = await Promise.all([orders.items(id), crm.get(o.customerId), pricing.quote(o)]) · asyncio.gather / TaskGroup · errgroup · StructuredTaskScope · Task.WhenAll — over a fixed, small set
```
**Read the code:** Does the second call use the first's result, or need its side effect (precedent 24)? Do the calls share one transaction or one ORM unit of work, so they cannot overlap on one connection? Is the downstream rate-limited or ordered? For 1b, is each iteration independent of the last? **Finding when** two or more independent waits on a reachable path add up. **Proof:** `proof-oracles.md` § "Wall-clock with mocked latency" (V25): each dependency mocked at L, wall time < 2L, which fails at about 3L first. Or § "Max in-flight", where the peak should be ≥ 2.

### 2. Unbounded fan-out

```
BAD:   await Promise.all(cart.items.map(i => shipping.quote(i))) (1,000 items → 1,000 sockets and pool slots) · for _, id := range ids { go fetch(ctx, id) } · asyncio.gather(*(call(x) for x in xs)) · items.forEach(async …)
GOOD:  const limit = pLimit(8); await Promise.all(items.map(i => limit(() => shipping.quote(i)))) · errgroup.SetLimit(8)
```
**Read the code:** Is the list request- or data-sized, or a constant ≤ ~10, or capped by validated `maxItems` (precedent 25)? Does a 2c limiter sit in the path? Does the client already cap concurrency (an agent's `connections`, a pool queue with a timeout)? Does `forEach(async` also drop errors and return early? **Finding when** in-flight calls grow with N, with no cap. **Proof:** § "Max in-flight" (V26). At N = 1,000 the peak stays ≤ the cap, and stays at it for two concurrent requests when the cap protects a downstream.

### 3. Network N+1

```
BAD:   for (const id of ids) { prices.push(await redis.get(`price:${id}`)) } (N round trips; MGET exists) · for item in items: requests.post(f"{SVC}/score", json=item) (the service has /score:batch)
GOOD:  await redis.mget(ids.map(k)) · pipeline · the batch endpoint · a per-request DataLoader in front of the service
```
**Read the code:** Follow the callee to the wire. Database → `n-plus-one-scan`. Is there a batch API, `MGET`, pipeline or bulk endpoint? Is N capped and the call cached? **Finding when** outbound calls grow with N and a batch primitive exists, or the calls hold the request for N × RTT. **Proof:** count outbound calls (nock, MSW `request:start`, an `httptest` handler counter, Redis `MONITOR`) at N = 2 and N = 20: the test asserts equal counts and fails before the fix ([`proof-oracles.md`](../../../../snippets/proof-oracles.md) § "Query-count scaling", applied to calls; V27).

### 4. Blocking I/O on the event loop or async runtime

```
BAD:   async handler(req) { const tpl = fs.readFileSync(path) } · async def view(): requests.get(url) (the loop stalls) · Mono.fromCallable(() -> jdbc.query(…)).block() on a Netty thread · var r = client.GetAsync(u).Result; (ASP.NET)
GOOD:  await fs.promises.readFile (or read once at boot) · httpx.AsyncClient · R2DBC or a bounded elastic scheduler · await
```
**Read the code:** Is the enclosing function on a request path, or boot code (module top level, constructor of a singleton, `onModuleInit`: precedents 23, 66)? Is the runtime event-loop based (lane table)? A thread-per-request server has no loop to stall (precedent 27): there the finding is held worker-seconds, measured differently. In Python, is a sync `def` endpoint running in AnyIO's 40-token pool? **Finding when** a blocking call runs on the loop or a reactive thread per request. **Proof:** § "Event-loop delay" (V28): p99 loop delay under 20 concurrent requests, measured against a benign control, fails first. Use asyncio debug `slow_callback_duration`, BlockHound for Reactor, and `dotnet-counters` ThreadPool queue length > 0 while thread count climbs.

### 5. CPU-heavy work on the request thread

```
BAD:   crypto.pbkdf2Sync(pw, salt, 600_000, 32, 'sha256') · zlib.gunzipSync(req.body) · JSON.parse(JSON.stringify(bigTree)) · hashlib.pbkdf2_hmac(...) in an async view · image resize in a controller · sort of an upload in the handler
GOOD:  crypto.pbkdf2 / scrypt (callback or promisified) · zlib streams · structured data built once · a worker pool (piscina, worker_threads, ProcessPoolExecutor) or a job queue for image and report work
```
**Read the code:** What bounds the input: a validated size, a body limit, the record count? Does the cost grow with the input (zlib, JSON, sort), or is it fixed per call (one hash at fixed rounds)? Is a free-threaded Python build in use (precedent 58)? **Finding when** request-path CPU blocks the loop or holds a GIL or GVL worker for a cost that grows with input or traffic. **Proof:** § "Event-loop delay" at the largest realistic payload, with the cost parameter turned up (V28). For input-size scaling, use the time ratio at N vs 10N (V35). GIL: `py-spy record --gil`.

### 6. Full buffering; payload and serialization cost

```
BAD:   Buffer.from(await res.arrayBuffer()) then a size check · await cursor.toArray() into the response · io.ReadAll(r.Body) · an export route that builds the whole array · model_validate(json.loads(raw)) on large bodies · no compression anywhere
GOOD:  stream with a byte cap (pipeline, StreamingResponse, io.LimitReader) · check Content-Length and count bytes while reading · paginate (query-shape-scan) · model_validate_json · compression at the edge or the app
```
**Read the code:** Who sets the size: a remote server, the user, the table? Is there a cap enforced **before** the bytes are held? Is the response compressed at the CDN or proxy (check `Content-Encoding`)? An unbounded query behind it is `query-shape-scan` § 1; this § owns holding the result in memory. **Finding when** memory or serialization time grows with a payload nobody bounds before it is read. **Proof:** § "Heap growth" as RSS high-water with a payload 10× the typical size (V29), plus response bytes at p95.

### 7. Client, agent or pool built per call

```
BAD:   async quote() { const http = axios.create({ httpsAgent: new https.Agent({ keepAlive: true }) }); … } · new HttpClient() per request (.NET socket exhaustion) · boto3.client('s3') in an endpoint · new Redis() in a service method
GOOD:  one client per process (module scope or a DI singleton) · IHttpClientFactory · SDK clients built at init, outside the handler
```
**Read the code:** Is the constructor inside a function called per request, or in a provider factory or constructor that runs once? A thin wrapper over a shared agent costs an object, not a socket (precedent 29). In serverless, is the client inside `handler` instead of at module scope? Database clients → `connection-config-scan` § 1. **Finding when** each call opens a new connection, TLS handshake or pool. **Proof:** § "Socket and handle count" (V30): sockets opened across 50 calls stay ≤ the pool size, which fails first at 50.

### 8. Built per call: regex, validator, template, serializer

```
BAD:   function check(s) { return new RegExp(PATTERN).test(s) } · ajv.compile(schema) per request · new ObjectMapper() per call · Handlebars.compile(tpl) per render · Pattern.compile in a method · TypeAdapter(Model) in a function body
GOOD:  compile once at module scope or construction; cache by key when the set is bounded
```
**Read the code:** Is the path hot (a profile, a list loop)? Does the platform cache it already: Python `re` (precedent 28), .NET static `Regex` methods? **Finding when** a hot path rebuilds a compiled object per call. **Proof:** allocations per operation (Go `testing.AllocsPerRun`, JMH `-prof gc`, BenchmarkDotNet `[MemoryDiagnoser]`). Otherwise use the timing protocol inside the noise band (V31, § "Noise band rules for timing oracles").

### 9. Eager or synchronous logging in the hot path

```
BAD:   logger.debug(f"order {order!r}") · log.debug("x=" + expensive()) · logger.debug(JSON.stringify(cart)) at INFO level · console.log on a server path (a synchronous write when stdout is a file or pipe)
GOOD:  lazy arguments (logger.debug("order %s", order)) · a structured async logger · guard expensive fields with isDebugEnabled
```
**Read the code:** Is the level enabled in production? Is the argument large or computed? **Finding when** a hot path formats or writes log output that is dropped, or that writes synchronously. **Proof:** allocations per operation at the production log level, or the timing protocol (V31). Low unless a profile proves the path hot.

### 10. Lock held across I/O, or one hot global lock

```
BAD:   mu.Lock(); resp, _ := http.Get(u); mu.Unlock() · await mutex.runExclusive(() => fetch(url)) · synchronized (this) { jdbc… }
GOOD:  copy under the lock, do the I/O outside it · per-key locks or sharding · sync.Map / RWMutex for read-mostly maps
```
**Read the code:** What does the lock guard, and is it contended on a request path? Is the I/O inside it timed? On JDK ≥ 24 `synchronized` no longer pins virtual threads (precedent 53), but it still serializes. A lock that guards a cross-replica invariant is §18. **Finding when** concurrent requests queue on one lock held across network or disk I/O. **Proof:** § "Max in-flight" on the downstream under K concurrent requests. The peak is 1 before the fix. Alternatively, mutex profile delay (`SetMutexProfileFraction` + `pprof …/mutex`, `asprof -e lock`).

### 11. Super-linear work on request-sized input

```
BAD:   orders.filter(o => ids.includes(o.id)) (O(n × m) with request-sized ids) · for x in items: if x in seen_list: … · queue.pop(0) in a loop · sort inside a loop · string += in a loop
GOOD:  const wanted = new Set(ids); orders.filter(o => wanted.has(o.id)) · set / dict · deque · sort once
```
**Owner check first:** when `.claude/skills/complexity-scan/SKILL.md` exists, print each hit as `<file:line> → complexity-scan §1–§5` with the count and stop; the algorithms pack grades it (with its cap resolution from `algo-sites.py`). The rest of this § is the fallback without it. **Read the code:** Are both collections request- or data-sized, or is one a constant (≲ 50)? Is the inner collection already a `Set` or dict (linters cannot see types)? **Finding when** the work grows faster than linearly in a size the user or the data controls. **Proof:** [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § "Time ratio at N vs 10N" (V35): about 10× per decade is linear and about 100× is quadratic. Count operations rather than time where you can.

### 12. Outbound call with no timeout, no total deadline or no propagated deadline

```
BAD:   await fetch(`${PSP}/charges`, { method: 'POST', body }) (undici: no total deadline, 300 s per phase) · axios.create({ baseURL }) (timeout 0) · requests.post(url, json=b) · &http.Client{} · HttpRequest.newBuilder(u) without .timeout · ctx := context.Background() inside a handler (the caller's deadline is lost)
GOOD:  fetch(u, { signal: AbortSignal.timeout(2_000) }) · axios.create({ timeout: 2_000 }) · requests.post(u, timeout=(3, 10)) · http.Client{Timeout: 5 * time.Second} · NewRequestWithContext(r.Context(), …) · inner budgets < the caller's
```
**Read the code:** Follow the client to its factory: a shared client with a default timeout covers the call. Does an outer deadline wrap it (`AbortSignal.timeout`, `context.WithTimeout`, a TimeLimiter)? Is the deadline **total**, body included? undici's body timeout resets on every chunk. Does caller timeout ≥ Σ (callee timeout × attempts) + backoff hold? Retry policy → `@resilience-reviewer` § "2. Retries". DB statement and acquire timeouts → `connection-config-scan` § 5 and § 7. **Finding when** a request-path call to a remote dependency can wait without bound. **Proof:** § "Timeout firing" (V34). A socket that accepts and never answers makes the call fail within the deadline + margin. A slow drip proves the total deadline, and sockets return to baseline.

### 13. Inbound server timeouts and limits

```
BAD:   Node server behind an ALB (idle 60 s) with keepAliveTimeout left at 5 s → intermittent 502s (Node ≤ 26 default) · headersTimeout ≤ keepAliveTimeout · Go http.ListenAndServe / &http.Server{} without ReadHeaderTimeout (gosec G112, G114) · body limit raised to hundreds of MB on JSON routes · no request timeout on long uploads
GOOD:  keepAliveTimeout > the LB idle timeout, headersTimeout above it · ReadHeaderTimeout + IdleTimeout set · per-route body limits
```
**Read the code:** Find the LB idle timeout (grep 0, IaC, provider default) and the app's keep-alive (13a, else the runtime default for the installed version, precedent 71). Does a proxy (nginx, Envoy) terminate keep-alive in between? Then order the whole chain hop by hop (13c, [`precedents/performance.md`](../../../../snippets/precedents/performance.md) § 91): each hop's upstream idle timeout below the next hop's client keep-alive — Caddy's `keepalive` (DEFAULT 2m) in front of ingress-nginx's `keep-alive` (DEFAULT 75 s) is inverted. Which routes need large bodies, and do they stream? **Finding when** the cited pair is inverted, or the server lacks a header-read timeout or a body bound on an internet-facing port. **Proof:** `proof-oracles.md` § "Server limits" (V45): the config arithmetic with both terms cited is a static-fact proof. Then an idle-gap soak through the real LB gives 0 × 502, a slow header client is closed at `ReadHeaderTimeout`, and an oversized body gets 413.

### 14. No admission control, load shedding or bulkhead

```
BAD:   Executors.newFixedThreadPool(n) (unbounded queue) · asyncio.Queue() / queue.Queue() with no maxsize · Channel.CreateUnbounded · one HTTP agent or pool for every downstream (one slow dependency starves the rest) · every tenant's job fired at :00
GOOD:  a bounded queue with a rejection policy · fast 429 / 503 with Retry-After past a concurrency cap (under-pressure, ConcurrencyLimiter, limit_conn at the ingress) · a pool per downstream · jittered schedules and TTLs
```
**Read the code:** Is any admission control present: the ingress, the gateway, serverless concurrency, an app limiter (grep 14)? Does an unbounded buffer sit on the request path? Is one pool shared by unrelated dependencies (`@resilience-reviewer` § "4. Bulkheads" owns the sizing)? Absence of shedding alone is Hardening, unless an anonymous route reaches §5 or §6 work or a 14 hit buffers without a bound. Memory growth of the buffer → `memory-growth-scan`. **Finding when** excess load queues without bound where it should be refused. **Proof (existence):** `proof-oracles.md` § "Admission control" (V46): block the worker, submit cap + K items, and the K excess are rejected fast instead of queued. **Cost:** an open-model run to 2× the knee (`load-test` skill) where goodput plateaus.

### 15. Health probe that checks a shared dependency

```
BAD:   livenessProbe → /health → SELECT 1 + redis.ping() (a database blip restarts every pod at once)
GOOD:  liveness = the process answers · readiness = this pod can serve (warm-up, local deps) · dependency health → metrics, alerts
```
**Read the code:** Which handler does each probe call (15a → 15b), and what does it touch? Is there a degraded mode readiness would remove? Is there a `startupProbe` for slow boots? **Finding when** liveness depends on a shared dependency, or readiness on one with no documented "no degraded mode" decision. **Proof:** `proof-oracles.md` § "Probe independence" (V47): with the dependency stopped (or its client mocked to fail), the liveness endpoint still returns 200. Then, in a disposable cluster, stop the database for 60 s: no pod restarts.

### 16. Session or auth state in one process

```
BAD:   app.use(session({ secret })) (default MemoryStore) · SESSION_DRIVER=file · AddDataProtection() without PersistKeysTo… · JWT secret = randomBytes(32) at boot (each replica signs with its own key) · sessionAffinity: ClientIP to make it work
GOOD:  a Redis or database session store · signed stateless tokens with a shared secret from env or KMS · a persisted key ring
```
**Read the code:** Where does the session, the CSRF or OAuth `state` / PKCE verifier, and the signing key live? Does the deploy rely on stickiness (16b), and only for a WebSocket handshake? **Finding when** a request served by another replica loses the session or fails verification. **Proof:** two replicas behind round-robin (§ Proof — two replicas; V36). Log in, then 10 authenticated calls give 0 × 401. Repeat after `kill -9` of the replica that served the login.

### 17. Process-local state used as truth

```
BAD:   const prices = new Map() written on update and read on every request · CACHES = locmem in production · :memory_store · better-sqlite3 / sqlite3 in a scaled service · let nextId = 0 · if (process.env.NODE_APP_INSTANCE === '0') runJobs()
GOOD:  the shared store is the truth (Redis, the database); an L1 only with a short TTL and pub/sub or versioned invalidation · database sequences, UUIDv7 or ULID · leader election instead of "instance 0"
```
**Read the code:** Is the data written at runtime, or immutable reference data (precedent 30)? Does a write on one replica invalidate the others? Does it hold authorization data? Does "instance 0" mean one host or one process? TTL, size and key → `caching-scan`, growth → `memory-growth-scan`. **Finding when** replicas serve different answers for the same key, or ids collide across pods. **Proof:** two replicas (V37): write via A, read via B within the TTL, and the value is fresh. Ids stay unique across 2 pods, and primary-only work runs exactly once.

### 18. Limiter, quota, dedupe set or lock held per replica

```
BAD:   rateLimit({ windowMs: 60_000, max: 100 }) (memory store: the real limit is replicas × 100) · a partner-API quota counted in a module variable · processing.add(id) as the "already running" guard · redis.set(lock, token, 'PX', ttl, 'NX') around a write with no fencing token checked by the resource
GOOD:  the limiter's Redis or database store · gateway limits · a unique constraint or conditional update as the guard · a fencing token checked at the write, or an efficiency-only lock where a duplicate is harmless
```
**Read the code:** What does the limit protect? Login, OTP, coupon, money, stock and plan quotas go to `logic-race-scan` § 8 (security pack, when installed); without that pack they stay here and print as a Finding tagged `security-class (owner pack not installed)` (§ Boundaries), never dropped. A hand-rolled limiter class holding its window in a process `Map` is the same class as a library limiter on its memory store. A downstream's quota, an expensive route or an efficiency lock stay here. Is the store shared? Does a lease guard correctness (a duplicate effect) or only efficiency? A shared lock's own mechanics — owner-checked release, an atomic TTL, the acquire result read, renewal and its result — are distributed-systems `coordination-scan` §1–§4 when installed; its grep 4d lists fencing tokens and whether the write checks them (the clearing evidence for the fencing half here). **Finding when** the effective limit or exclusion multiplies with replicas. **Proof:** two replicas (V38): limit 10/min, 30 requests give ≤ 10 accepted (plus tolerance). A provider mock sees ≤ its quota. For a lease, SIGSTOP the holder past its TTL: no second accepted write.

### 19. Local filesystem for uploads or generated files

```
BAD:   multer({ storage: diskStorage({ destination: 'uploads/' }) }) then served by express.static · invoices written to ./exports · Django FileSystemStorage for user files · active_storage.service = :local in production · emptyDir or RWO volume for uploads
GOOD:  object storage as the system of record (stream to it); local disk only as scratch consumed within the same request
```
**Read the code:** Is the file read back by a later request or another process? Which volume holds the directory (19b), and is it shared (RWX) or per pod? **Finding when** a file written on one replica must be read on another or survive a reschedule. **Proof:** two replicas (V39): upload via A, then GET 10× round-robin gives 0 × 404. Again after the pod is recreated.

### 20. Once-per-fleet work run per replica

```
BAD:   @Cron('0 * * * *') sendPayoutReminders() in the API (HPA up to 10) · node-cron / APScheduler started at boot · celery worker -B in a scaled Deployment · @Scheduled without ShedLock · CMD prisma migrate deploy && node main.js
GOOD:  one scheduler (a CronJob or cloud scheduler that enqueues, a single-replica Deployment, or a DB lock such as pg_try_advisory_xact_lock, ShedLock or onOneServer) · migrations in a Job, an init container or a release step
```
**Read the code:** Which process loads the scheduler module, and how many replicas run it (grep 0)? Does the tick take a lock (20c), and does anything with a side effect run **before** it (20d — a delete, send or write ahead of the lock runs on every replica, [`precedents/performance.md`](../../../../snippets/precedents/performance.md) § 92)? Is that lock a lease with no fencing while the job has side effects? Is the job idempotent? Is a k8s CronJob missing `concurrencyPolicy: Forbid`? Is a scheduler registered with no decorator at the call site (a `SchedulerRegistry.addCronJob` explorer: the module still loads on every replica)? Does the migration runner lock, at the installed version (precedent 77's table): MikroORM, TypeORM, umzug, Drizzle, Django, Alembic and Doctrine take **no** cross-process lock; Laravel `--isolated` skips and exits 0 while a mutex lives; Rails fails the others; Prisma waits 10 s, then fails; a Job, init container or release step runs once. Migrate-on-boot is owned by devops `deploy-safety-scan` §1 when that pack is installed (20b lines are its corroboration; dedupe by `file:line`). **Finding when** N replicas run a side-effecting job N times, or race a migration. **Proof:** 2–3 replicas (V40) with the schedule overridden to every 10 s: 5 ticks give exactly 5 executions (count rows). Then `kill -9` the holder mid-run, and the next tick runs once. Migrations: 3 simultaneous cold starts on an empty database give 0 crashes.

### 21. Broadcast that reaches one replica

```
BAD:   Socket.IO server with no adapter · wss.clients.forEach(send) · InMemoryChannelLayer · cable adapter: async · enableSimpleBroker · new PubSub() for GraphQL subscriptions · an EventEmitter feeding SSE
GOOD:  @socket.io/redis-adapter (or postgres, cluster) · channels_redis · STOMP broker relay · a Redis or NATS bus · a managed fan-out
```
**Read the code:** Is the event emitted on one replica and expected by clients connected to another? Does long-polling also need sticky sessions? **Finding when** an event emitted on replica A never reaches a client on replica B. **Proof:** two replicas (V41): a client connected to A, the event triggered through B, received within 2 s.

### 22. Durable work held in process memory

```
BAD:   void sendWelcomeEmail(user) in a handler · setTimeout(() => retryWebhook(e), 30_000) · jobs.push(job) on a module array · FastAPI BackgroundTasks for payments · @Async for invoices · go func() { deliver() }() in a handler · QUEUE_CONNECTION=sync
GOOD:  a durable queue (BullMQ, Celery, Sidekiq, SQS) or an outbox row in the same transaction, drained by a worker
```
**Read the code:** Is loss acceptable (telemetry, cache warm-up), or does the work move money, send messages or call partners? Is the promise awaited before the response? Does a durable outbox already back it? **Finding when** work that must happen is lost on deploy, OOM or `kill -9`. **Proof:** V42: enqueue 100, `kill -9` the process after 1 s, restart, and 100 complete (or the loss is an accepted, written decision).

### 23. Worker concurrency, prefetch, partitions and the autoscaling signal

```
BAD:   new Worker(q, fn) (BullMQ concurrency default 1) · RabbitMQ prefetch 0 (unlimited unacked) · Celery long tasks at prefetch multiplier 4 · Kafka partitions 3 with maxReplicas 10 · CPU-based HPA on an I/O-bound consumer · one queue for slow and fast jobs
GOOD:  workers ≈ λ × service time (Little's law) · prefetch 1 + acks_late for long tasks · partitions ≥ consumers · KEDA on lag or queue age · separate queues per job class
```
**Read the code:** What arrival rate λ and service time S are known (metrics, a runbook, a stated budget)? Does concurrency × replicas × connections per job fit the DB pool (→ `connection-config-scan` § 2)? Is ordering per key required? **Finding when** the cited arithmetic shows capacity below λ, unbounded prefetch, or consumers past the partition cap. With λ unknown the row is Unconfirmed, carrying the metric to read. **Proof:** `proof-oracles.md` § "Queue age at a fixed arrival rate" (V43): the arithmetic, every term cited. Then a fixed λ for 10 min (`load-test`): oldest-message age stays flat, and doubling consumers roughly doubles throughput up to the cap.

### 24. Redelivered jobs

```
BAD:   a consumer that charges, emails or calls a partner with no dedupe key (at-least-once delivery → twice) · a BullMQ job doing 45 s of sync work at lockDuration 30 s · SQS visibility below 6 × the Lambda timeout · attempts: 5 with no backoff and no dead-letter queue · a whole batch retried for one bad message
GOOD:  an atomic reserve (a unique insert of the message id in the effect's transaction, or a conditional status update) · lock or visibility sized above the p99 run time, or a heartbeat · bounded retries with backoff · a DLQ with an alarm
```
**Fallback only.** With the distributed-systems pack installed (`.claude/skills/messaging-scan/` exists), print `→ distributed-systems messaging-scan §2/§3/§6 (k)` with the 24a/24b counts and do not grade; V44 probe 1 stays the shared oracle (its V296). Without it, grade here. **Read the code:** Follow each consumer (24b) into its use case. Is the effect guarded by an atomic reserve, or by a read-then-write (not a reserve)? Is the lock or visibility longer than the worst run? Where do poison messages go? Money and stock effects → `logic-race-scan` § 4; reserve design → `@resilience-reviewer` § "5. Idempotency → exactly-once EFFECT"; DLQ replay → `dlq-replay` (distributed-systems pack, when installed). **Finding when** a redelivery or an expired lock can repeat a side effect, or one bad message blocks the rest. **Proof:** `proof-oracles.md` § "Redelivery" (V44): a job sleeping 1.5 × the lock or visibility timeout gives exactly 1 side effect. A good message delivered twice gives 1 effect. 1 poison + 100 good: the good drain and the poison lands in the DLQ after N tries.

## Proof — two replicas

Scale classes (§16–§22, §24) have one decisive oracle: the service run twice behind a round-robin proxy, in a disposable environment, with the alternation shown first, schedules overridden through the path production uses, and effects counted in the database. The harness and its rules are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § "Two replicas behind round-robin"; each § above names its pass condition, and V36–V42 list the variants a fix must pass.

## Output

```
request-path-scan — lanes: node 22 / NestJS 11 on Fastify (package.json); python, go, jvm, .net, ruby, php absent
Deployment: api HPA maxReplicas 10 (deploy/k8s/api-hpa.yaml:9) · worker KEDA (deploy/k8s/worker-scaler.yaml:14) · LB idle 60 s (DEFAULT)

Findings: 1 · Unconfirmed: 1

1. src/payments/psp.client.ts:41                               [report-with-fix]   critical
   §12 no deadline — `fetch(`${PSP}/charges`, { method: 'POST', body })` on POST /orders/:id/pay; no signal, no factory
   default, no outer deadline. Proof: test/payments/psp-timeout.spec.ts — a socket that never answers holds the call
   past 30 s (fails); with AbortSignal.timeout(2_000) it rejects at 2.0 s and the socket closes. Fix: 2 s total deadline
   below the route's 5 s budget; retry policy left to @resilience-reviewer. CWE-1088

2. src/reminders/payout-reminder.job.ts:19                      [report-flagged]    critical
   §20 scheduler on every replica — @Cron('0 * * * *') sends payout e-mails from the API process (maxReplicas 10);
   no lock in the file or in ScheduleModule's setup. Unproven link: no two-replica harness in the repo. Settling probe:
   proof-oracles § Two replicas with CRON_EXPR='*/10 * * * * *', 5 ticks → expect 5 rows in reminder_runs. Fix: move the tick
   to the k8s CronJob that enqueues, or take pg_try_advisory_xact_lock(<job key>) inside the run.

Verification: 23 candidates → 1 finding · 1 unconfirmed · 9 hardening · 0 pre-existing · 12 refuted

Class coverage:
  §1  sequential awaits    checked (12 hits / 9 groups → 0; dependent pairs)  · §2  unbounded fan-out   checked (3 → 0; chunks of 50)
  §3  network N+1          checked (21 → 0; 4 routed to n-plus-one-scan)       · §4  blocking on loop   checked (4 → 0; all boot code)
  §5  CPU on request       checked (2 → 0; a receipt deep-clone under 1 KB)    · §6  full buffering     checked (1 → 0; compression in bootstrap)
  §7  client per call      checked (3 → 0; factories run once per provider)    · §8  built per call     checked (9 → 9 hardening; not proven hot)
  §9  eager logging        checked (1 → 0) · scripts/ closed: not reachable    · §10 lock across I/O    checked (0 hits)
  §11 super-linear work    checked (57 / 34 groups → 0) · Live, unreviewed (12 groups / 19 hits)
  §12 outbound timeout     checked (2 → 1 finding)                             · §13 server timeouts    checked (8 → 0; keep-alive 72 s > LB 60 s)
  §14 admission control    checked (0; ingress limit not in repo → 1 hardening) · §15 health probes    checked (19 → 0; liveness skips the DB)
  §16 sessions             N/A (stateless signed tokens)                       · §17 process-local      checked (8 → 0; per-process breaker maps)
  §18 per-replica limits   checked (40 → 0; throttler on Redis, leases)        · §19 local filesystem   checked (17 → 0; object storage)
  §20 per-replica cron     checked (48 → 1 unconfirmed; 30 take a DB lock; 20d 0 before-lock effects)
  §21 broadcast            checked (5 → 0: Redis adapter)                      · §22 in-process work    checked (20 → 0; outbox-backed)
  §23 worker sizing        checked (16 → 0; KEDA on queue length; λ unknown → 1 hardening) · §24 redelivered jobs checked (5 → 0)
```

`[report-with-fix]`: the path is traced from the entry point, the oracle failed before the fix, and the fix is concrete. `[report-flagged]`: one link is unproven (no harness, a setting outside the repo, a replica count or λ unknown), and the row names it with the settling probe. The coverage block lists **all twenty-four** classes on every run: `checked (k hits → m findings)` only when the grep ran on a present lane, `N/A (<reason>)` only when the repo has no such surface (no queue, no WebSocket, no session), `blocked (<reason>)` when a grep failed or code could not be read. A partial review reads `Live, unreviewed (k groups / n hits)`, never `checked`. Every finding carries the evidence block from [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § "Implementation notes for the test writer". A cost number with no harness label is deleted, not softened.

## False positives / precedents

The verifier reads [`precedents/performance.md`](../../../../snippets/precedents/performance.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:

- **Request path:** boot is not the request path (§ 23, § 66); dependent awaits and ordered downstreams stay sequential (§ 24); fan-out over a constant list or fixed chunks is bounded (§ 25); CPU off the request path, and thread-per-request servers with no loop to stall (§ 26, § 27); Python's regex cache (§ 28); a thin wrapper over a shared agent (§ 29).
- **Overload:** an outer deadline or a client factory sets the timeout, and the library defaults (§ 72); controls at the edge — ingress, gateway, serverless limits, a bounded executor (§ 79); readiness on a per-pod dependency (§ 80); synchronised load needs synchronised triggers (§ 82).
- **Scale and queues:** one replica by design is `latent (one replica)`, Hardening until the shape changes (§ 73); signed stateless sessions (§ 74); a shared store as the control (§ 75); one scheduler (§ 76); migrations that run once or hold a lock (§ 77); broadcast adapters, object storage and an outbox (§ 78); deliberate queue settings (§ 81).
- **Version flips:** JDK ≥ 24 pinning (§ 53), Go ≥ 1.23 timers (§ 54), Go ≥ 1.25 `GOMAXPROCS` (§ 55), and Node's 5 s `keepAliveTimeout` still a finding through Node 26 (§ 71).

## When to run

- On any diff touching a handler, resolver, consumer, outbound client, server bootstrap, scheduler, queue worker, session or limiter config, upload path, or a deploy manifest that changes replicas, probes or timeouts: the `/perf-audit` dispatch signal.
- On every whole-repo `/perf-audit`, reporting all twenty-four classes.
- Before raising replicas or an autoscaler maximum, adding a second worker fleet, or moving a single-box service behind a load balancer: §16–§24 are the "what breaks on replica two" checklist.

## Halt conditions

- Do not report a high or critical row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/performance.md`](../../../../snippets/precedents/performance.md). Under `/perf-audit` that happens in its verification phase. Run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on any finding without the code `<file:line>`, the entry point, the cited condition (N, payload, concurrency, replicas) and the fix. A §12–§24 row without its deployment terms cited, or marked `UNKNOWN`, is not a finding.
- Do not mark `[report-with-fix]` without an oracle that failed first. Without a harness, the row is `[report-flagged]` / Unconfirmed, with the probe written out. Never write a latency, speed-up or count that no tool produced.
- Do not run the two-replica, kill or fault-injection probes against production or a host the operator has not named.
- Do not propose sticky sessions as the fix for a scale class, a bigger pool or more replicas for a request-path class (§1–§11), or a cache in front of a per-element call (§3). The fix removes the cause: a cap, a deadline, a batch call, a shared store, one scheduler, a reserve. §23 alone sizes concurrency, and only from the cited arithmetic.
- Do not print "request path looks fine" without the class-coverage block. A class whose grep did not run is `blocked`, never `checked`. Do not re-derive a class another skill owns (§ Boundaries); cross-link it.

## Related

- `/perf-audit` dispatches this skill and folds its coverage block into the class ledger; `@performance-optimizer` ranks verified findings by measured or `ESTIMATED` impact. `/perf-fix` closes them failing-first and re-runs this detector on the patched line.
- `memory-growth-scan`, `caching-scan` (this pack): growth and cache correctness. `profile-endpoint`, `load-test`, `memory-leak-hunt` (this pack): the harnesses behind the cost numbers.
- `n-plus-one-scan`, `query-shape-scan`, `connection-config-scan`, `transaction-scan` (database pack, when installed): database round trips, reads, pools and transactions.
- `@resilience-reviewer`, `@capacity-planner`, `chaos-test`, `dlq-replay` (distributed-systems pack, when installed): retry policy, breakers, capacity math, fault drills and dead-letter replay.
- `logic-race-scan`, `injection-scan`, `@api-security-reviewer` (security pack, when installed): business invariants in one process, ReDoS and GraphQL cost limits.
- `parallelize-independent-ops` (backend pack, when installed) is the fix skill for §1 and §2. For §11, when the algorithms pack is installed: `complexity-scan` §1–§5 detects and grades, `/analyze-complexity` is the whole-repo audit and `/design-algorithm --from-audit` the fixer; without it §11 grades here and `/perf-fix` fixes.
- `rules/performance-principles.md` holds the MUSTs these classes enforce; [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § "Class variants (performance)" (V25–V47) holds the variant lists a fix must pass.
