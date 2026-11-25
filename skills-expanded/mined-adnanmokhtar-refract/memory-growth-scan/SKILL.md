---
name: memory-growth-scan
description: "Find server memory that grows with traffic: unbounded maps and memoisers keyed by request data, listeners and intervals never removed, request state on singletons, unreleased streams, buffers that grow while a consumer lags, units of work never cleared, heap limits against container limits. Proved by heap growth or handle count."
kind: skill
pack: performance
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: memory-growth-scan

## Premise

Memory that grows with traffic is a slow outage. The process is killed for running out of memory, the orchestrator restarts it, the dashboard shows a sawtooth, and the restart hides the cause until traffic doubles and the sawtooth's period falls under an hour. Every shape in this skill is visible in the code before any snapshot exists: a module-level `Map` that a handler writes and nothing deletes, a listener added per connection to an emitter that lives for the process, a stream relay that never waits for `drain`. This skill is the static front end of `memory-leak-hunt` (this pack). It finds the candidates and proves each one with a deterministic count; `memory-leak-hunt` attributes what a test cannot isolate, over a soak.

**Every finding cites the growing object at `<file:line>` + its lifetime (why it outlives the request) + the request-derived key or payload that makes it grow + the missing bound (max, TTL, removal on teardown, a scope that ends, a cap on a buffer that waits for a slower consumer) + the proof or the probe that would settle it + the fix in the project's stack.** A grep hit is never a finding by itself, and "no memory growth found" is never printed without the class-coverage block (§ Output).

**The key decides, not the container.** A module-level map keyed by currency codes is a cache with a fixed size. The same map keyed by user id, session id, URL, IP or upload id grows with traffic and is the finding unless something removes entries. Existence is proved by an invariant that does not move between runs: the container's size, the listener count, the open-handle count, or the post-GC heap across batches of **distinct** inputs ([`proof-oracles.md`](../../../../snippets/proof-oracles.md) § "Heap growth" and § "Socket and handle count"). Time-to-OOM is an estimate (`bytes per entry × new keys per hour` against the headroom from §9), labelled `ESTIMATED`; it ranks a finding and never proves one.

## The growth rule

A candidate is a finding when all three hold:

1. **It outlives the request.** It sits at module or package scope, in a static field, on a framework singleton, on a long-lived emitter or client, or in a closure stored by one of those.
2. **A production path adds to it per distinct input.** A route, consumer, job or connection handler writes an entry, registers a callback, starts a timer or buffers bytes, keyed or sized by data it does not control.
3. **Nothing bounds it.** There is no `max` or TTL, no removal on the matching teardown (`close`, `end`, `finally`, `unsubscribe`, `clearInterval`), no scope that ends (a request-scoped provider, an ORM `fork()`), and no cap on what waits for a slower consumer.

What lives as long as the process, per framework:

| Framework | Process-lifetime (rule 1 holds) | Ends with the request |
|---|---|---|
| **NestJS** (Express or Fastify adapter) | Fields of a default-scope provider, controller or gateway: "a single instance … shared across the entire application", its lifetime "tied directly to the application lifecycle" (NestJS docs, *Injection scopes*) | `Scope.REQUEST` providers, and anything that depends on one ("the `REQUEST` scope bubbles up the injection chain") |
| **Express / Fastify / Node** | Module scope, `app.locals`, Fastify decorators, a client or emitter created at boot | `req`, `res` and `reply` and their listeners, `AsyncLocalStorage` stores |
| **Spring** | Singleton beans (the default scope) and `static` fields | `@RequestScope` beans, `ThreadLocal` values **only** when removed before the pooled thread is reused |
| **Django / FastAPI / Flask** | Module globals and class attributes, per worker process (each gunicorn or uvicorn worker holds its own copy) | The request object, view locals, `contextvars` |
| **Rails / Sidekiq** | Constants, class variables (`@@x`), class-level instance variables | Controller instances, `ActiveSupport::CurrentAttributes` (reset per request) |
| **Laravel** | Under PHP-FPM nothing: each request starts fresh. Under Octane, queue workers and other daemons, static properties and singletons persist: "adding data to a statically maintained array will result in a memory leak" (Laravel 12 docs, *Octane*, Managing Memory Leaks) | The request, under FPM everything |
| **Go** | Package-level variables, goroutines that never return | Handler locals, `r.Context()` values |
| **ASP.NET Core** | Singletons, `static` fields | Scoped services |

## Boundaries

- **Runtime attribution and soak** (a growing retained set with its retaining path, a heap that is flat over hours) → `memory-leak-hunt` (this pack). Hand it any candidate the test cannot isolate.
- **Cache correctness** (TTL, stampede, keys, invalidation) → `caching-scan` (this pack). An in-process cache with **no size bound** is reported once, here (§1); `caching-scan` lists it as "see memory-growth-scan §1".
- **`request-path-scan` (this pack)** owns the request path's one-shot costs: §6 a body, upload, download or result held whole in memory (`io.ReadAll`, `arrayBuffer()` before the size check, `fetchall()`), §13 inbound body-size limits, §7 a client, agent or pool built per call, §8 a regex, validator, template or serializer built per call, §2 a goroutine or task per element, and §14 unbounded work queues as admission control. This skill owns what **accumulates over time**: retained objects, and buffers that grow for as long as a consumer lags (§6). Where both runs name the same `<file:line>`, they dedupe and the row carries both classes. A goroutine that never exits is §3 here.
- **The unbounded query** behind a materialised result → `query-shape-scan` § 1 (database pack, when installed); without it, `request-path-scan` §6 holds the materialised result and names the missing `LIMIT`. **Database connections and cursors not released** → `connection-config-scan` § 9 (database pack, when installed); without it, §5 here covers them by the same handle-count oracle.
- **Overload behaviour** of an unbounded work queue (rejecting work, 429 under pressure) → `request-path-scan` §14, with pool and bulkhead sizing at `@resilience-reviewer` § "4. Bulkheads" (distributed-systems pack, when installed).
- **A process-local map used as shared state** (a session store, state used as the truth, a rate-limit window, a dedupe set, an in-memory lock) is a horizontal-scale defect, not a leak: `request-path-scan` (this pack) §16 for sessions, §17 for state used as the truth (including a process-local cache's coherence across replicas) and §18 for limit windows, dedupe sets and locks. Here such a map is judged only for growth; its cache leg (TTL, keys, invalidation) is `caching-scan`'s.
- **Request data retained where another user can read it** (a singleton field holding the current user) is reported here as §4 and is also a cross-user read: route that to `@tenant-isolation-reviewer` (security pack, when installed; [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 9). Without it, tag the row `security-class (owner pack not installed)`.
- **Browser and device memory** (component listeners, intervals and observers in a SPA; mobile leaks) → the frontend and mobile packs (`device-performance-auditor`). Point `ROOTS` at server code only.

## Adapt to the codebase

Read the runtime, framework and ORM versions from the lockfile, manifest and Dockerfile, not from memory, and print the lanes you ran. The lane table names where growth hides per stack and the primitive the fix uses:

| Lane | Growth shapes the greps key on | Bounded primitive (the fix) | Structural count for the proof |
|---|---|---|---|
| **Node / TS** (NestJS on Express or Fastify, Express, Fastify) | module `Map` / `Set` / array, provider fields, `emitter.on` per connection, `setInterval` per request, `if (!res.ok) throw` before the body is read (undici asks callers to "always either consume or cancel the response body", undici README, *Garbage Collection*), `.pipe()` with no error path (Node docs, `readable.pipe()`: on a source error the destination "is not closed automatically", and each stream must be closed by hand "to prevent memory leaks"), `write()` to a stream whose `false` return is ignored | `lru-cache` with `max` (it refuses to construct without `max`, `maxSize` or `ttl`, and a `ttl`-only cache "will potentially grow unbounded" without `ttlAutopurge`: lru-cache 11 README), `once()` / `AbortSignal`, `stream.pipeline()`, `await res.body?.cancel()` | `map.size`, `emitter.listenerCount(e)`, Jest `--detectOpenHandles`, `process.memoryUsage().heapUsed` after `global.gc()` |
| **MikroORM** 6 / 7 | one `EntityManager` (its identity map) carried across a worker loop; `allowGlobalContext: true` (v7 default `false`, which throws on global-EM use); a fork stored in a field | `em.fork()` per job or batch, `em.clear()` after each flush, `@CreateRequestContext()` | `em.getUnitOfWork().getIdentityMap()` size per batch |
| **TypeORM · Prisma · Drizzle · Sequelize · Knex** | no identity map, so §7 is `N/A`; a result materialised whole is `request-path-scan` §6's | keyset batches in jobs; Knex and TypeORM `.stream()` | heap per batch |
| **Django / DRF · Celery** | module dicts, `@lru_cache(maxsize=None)` / `@cache`, `for x in Model.objects.all()` (the QuerySet keeps every row in its result cache), `DEBUG = True` in a long-running process (`connection.queries` records every statement, Django 5.2 FAQ) | `.iterator(chunk_size=…)`, `@lru_cache(maxsize=N)`, `DEBUG = False`, `worker_max_memory_per_child` only as a backstop | `tracemalloc` snapshot diff, `len(connection.queries)` |
| **FastAPI / Starlette · asyncio · SQLAlchemy 2** | `writer.write()` in a relay with no `await writer.drain()` ("the method should be used along with the `drain()` method", Python 3.14 docs, *Streams*); one `Session` across an import loop (pending and modified objects stay referenced until flush or close) | `await writer.drain()`, a session per batch, `yield_per` | `tracemalloc`, `len(session.new)` |
| **Go** (net/http, Gin, chi; GORM, pgx) | package `map` written by handlers, `go func` with no exit, a buffered channel used as an ever-growing backlog, `resp.Body` not closed (golangci-lint `bodyclose`) | `defer resp.Body.Close()`, `context` cancellation, a bounded channel with a drop or block policy, GORM `FindInBatches` | `runtime.NumGoroutine()`, `goleak.VerifyNone(t)`, `runtime.ReadMemStats` |
| **JVM** (Spring; Hibernate / JPA) | `static` / singleton `HashMap` written per request, `ThreadLocal` with no `remove()` (Error Prone `ThreadLocalUsage`), `Files.lines` outside try-with-resources (`StreamResourceLeak`), one persistence context across a batch | Caffeine with `maximumSize`, `try { … } finally { tl.remove(); }`, `flush()` + `clear()` every N, `StatelessSession` | a structural count through a test hook; JFR `jdk.OldObjectSample` |
| **Rails / ActiveRecord · Sidekiq** | `@@x = {}` and constants written per request, `Model.all.each` in a job | `find_each` / `in_batches`, a bounded `ActiveSupport::Cache::MemoryStore` | `GC.start; ObjectSpace.each_object(Klass).count` |
| **Laravel / Eloquent** (Octane, queue workers) | `static array $x` written per request, `Model::all()` in a job, `DB::enableQueryLog()` in a daemon (every query is appended to the connection's log until `DB::flushQueryLog()`) | `chunkById` / `lazyById`, scoped bindings, no query log outside tests | `memory_get_usage()` across N jobs |
| **.NET** (ASP.NET Core; EF Core) | `static Dictionary` written per request, `AddMemoryCache()` with no `SizeLimit`, a tracked `DbContext` across a batch | `MemoryCacheOptions.SizeLimit`, `ChangeTracker.Clear()`, `AsNoTracking()` | `dotnet-counters` GC heap size, `dotnet-gcdump` diff |

Linters that find candidates (a hit is a candidate, judged by the same read): golangci-lint `bodyclose`, `sqlclosecheck`, `rowserrcheck`, `prealloc`; Ruff `B019` (a cache on a method retains `self`); Error Prone `ThreadLocalUsage`, `StreamResourceLeak`; staticcheck `SA6002` (`sync.Pool` of a non-pointer); PMD `AvoidInstantiatingObjectsInLoops`.

## Context before hunting

On a whole-repo run, build one map first. Every later decision reads it:

1. **Process model.** Which processes run the code (API, workers, consumers, cron), how long each lives, how many run per container (cluster mode, gunicorn workers, Puma workers, Octane workers), and whether a request-per-process model (PHP-FPM, serverless) makes §1–§4 `N/A` there.
2. **Memory budget per process** (grep 9): container limit ÷ processes per container, minus the runtime's own overhead, against the heap cap actually set. This is the headroom time-to-OOM divides into.
3. **What grows with traffic.** Users, tenants, sessions, connections, uploaded files, outbound hosts, distinct URLs, and row ids (products, orders, listings: the set any request can touch is the whole table). A container keyed by one of these is a §1 candidate; one keyed by an enum is not.
4. **Evidence already collected.** OOM kills and restart counts, heap and RSS metrics (`process_resident_memory_bytes`, `nodejs_heap_size_used_bytes`, `go_memstats_heap_inuse_bytes`), a sawtooth that trends up, and recycling settings (`max_requests`, `max_memory_restart`, `worker_max_memory_per_child`), which mask a leak rather than bound it.

## Pre-flight greps

Run as **one** script from the repo root (shell state does not survive between tool calls). Grep **N** feeds detector **§N**. Set `ROOTS` to the server code roots; grep 9 reads deploy and runtime config from `.` on purpose. Every `rg` names its path: `rg` given no path reads stdin whenever stdin is a pipe, which under an agent's shell is a silent zero-hit run. A lane count of 0 is an `N/A` reason; any `rg` error on stderr (exit 2) is a failed grep, never zero hits. The loops need `perl` (present on macOS and Linux).

```bash
ROOTS=(.)        # the SERVER code roots (API, workers, shared server packages) — never the browser app
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/.next/**' -g '!**/target/**' -g '!**/.venv/**'
   -g '!**/*.min.*' -g '!**/*.{md,mdx,lock,map,svg,json,snap,sql,yml,yaml,toml}' -g '!ai/**' -g '!docs/**' -g '!.claude/**'
   -g '!**/{test,tests,__tests__,spec,e2e,__mocks__,mocks,fixtures,__fixtures__,testdata,seeds,seeders,migrations,migrate,locales,i18n,generated,__generated__,.prisma,temp}/**'
   -g '!**/*.{spec,test,e2e-spec,mock,stories}.*' -g '!**/{*_test,*_spec,test_*,conftest}.*')
C='^(?![ \t]*+(?://|/?\*|#(?!\{)|--))[^\n]*?'     # skip comment-only lines
for t in js ts py go java kotlin ruby php cs; do printf '%-7s %s\n' "$t" "$(rg --files -t "$t" "${X[@]}" "${ROOTS[@]}" | wc -l)"; done   # 0 = lane absent

# 1. Process-lifetime containers: 1a module- or class-level Map / Set / array / dict / static collection (JS/TS, Python, Go,
#    JVM, Ruby, PHP, C#), printed with the writes and removals its own file makes; 1b memoisers and caches with no size bound.
rg -n --pcre2 '^(?:export\s+)?(?:const|let|var)\s+(\w+)\s*(?::[^=\n]+)?=\s*(?:new\s+(?:Map|Set)\b|\[\s*\]|\{\s*\}|\[\]\s*as\b)|^\s+(?:(?:private|protected|public|static|readonly)\s+)+(\w+)\s*(?::[^=\n]+)?=\s*(?:new\s+(?:Map|Set)\b|\[\s*\]|\{\s*\})|^(\w+)\s*(?::[^=\n]+)?=\s*(?:\{\s*\}|\[\s*\]|dict\(\)|set\(\)|(?:collections\.)?(?:defaultdict|OrderedDict|deque)\((?![^)\n]*maxlen))\s*$|^var\s+(\w+)\s*=\s*(?:make\(\s*map|map\[[^\]]+\][^{\n]*\{\s*\}|\[\][\w.*]+\{\s*\})|^var\s+(\w+)\s+(?:sync\.Map|map\[)|\bstatic\s+(?:(?:final|readonly)\s+)?[\w.]*(?:Map|Set|List|Dictionary|Collection|Queue)<[^=\n]*\s(\w+)\s*=\s*new\b|^\s+private\s+final\s+(?:Map|Set|List|ConcurrentMap)<[^=\n]*\s(\w+)\s*=\s*new\s+(?:Concurrent)?(?:HashMap|HashSet|ArrayList|LinkedHashMap|SkipListMap)\b|^\s*(@@\w+|[A-Z][A-Z0-9_]*)\s*=\s*(?:\{\}|\[\]|Hash\.new|Concurrent::(?:Map|Hash|Array)\.new)|\bstatic\s+\??(?:array\s+)?\$(\w+)\s*=\s*(?:\[\s*\]|array\(\s*\))' "${X[@]}" "${ROOTS[@]}" |
  while IFS= read -r hit; do f=${hit%%:*}; rest=${hit#*:}; l=${rest%%:*}
    v=$(printf '%s\n' "${rest#*:}" | perl -ne 'if (/^\s*var\s+(\w+)/) { print $1 } elsif (/^([^=]*?)\s*=(?!=)/) { $p = $1; $p =~ s/^(\s*(?:(?:export|const|let|var|private|protected|public|static|readonly|final)\s+)*(?:@@)?\w+)\s*:.*$/$1/; print $1 if $p =~ /((?:@@)?\w+)\s*$/ }')
    [ -n "$v" ] || continue; w=$(rg -c --pcre2 "(?<![\\w@])$v(?:\\.(?:set|add|push|unshift|put|putIfAbsent|computeIfAbsent|merge|Store|LoadOrStore|append|setdefault|update|TryAdd|Add)\\(|\\[[^\\]\\n]+\\]\\s*(?:=(?!=)|<<|\\|\\|=))|\\b$v\\s*=\\s*append\\(" "$f"); d=$(rg -c --pcre2 "(?<![\\w@])$v\\.(?:delete|clear|shift|pop|splice|remove|Delete|LoadAndDelete|popitem|TryRemove|Remove|Clear)\\(|\\bdelete\\s*\\(?\\s*$v\\b|\\b$v\\.(?:size|length|Count)\\b\\s*[<>]=?" "$f"); z=$(rg -c --pcre2 "\\b$v\\s*=\\s*(?:new\\b|\\[\\]|\\{\\}|dict\\(|set\\()" "$f"); d=$(( ${d:-0} + ${z:-1} - 1 ))
    [ "${w:-0}" -gt 0 ] && echo "$f:$l: $v  writes=${w:-0} removes=${d:-0}"; done
rg -n --pcre2 "$C"'(?:@(?:functools\.)?(?:cache\b|lru_cache\(\s*(?:maxsize\s*=\s*)?None\b)|\b(?:_\.)?memoize\((?![^\n]*\b(?:max|maxSize|cache)\b)|\bmoize\((?![^\n]*maxSize)|\bmemoizee?\((?![^\n]*\bmax\b)|\bnew\s+NodeCache\((?![^)\n]*maxKeys)|\bnew\s+LRUCache\s*(?:<[^>\n]*>)?\(\s*\{(?![^}\n]*\b(?:max|maxSize|ttlAutopurge)\b)|\bCaffeine\.newBuilder\(\)(?![^;\n]*(?:maximumSize|maximumWeight))|\bAddMemoryCache\(\s*\)|new\s+MemoryCache\(\s*new\s+MemoryCacheOptions\(\s*\)\s*\))' "${X[@]}" "${ROOTS[@]}"

# 1c. Metric series that grow with request data: in files that import a metrics client, an id, email, raw URL or path used
#     as a label value or name. A registry keeps one series per label set for the process lifetime — an unbounded container.
#     The cardinality defect itself is observability `metric-hygiene-scan`'s when that pack is installed (this lane keeps
#     the memory leg); without it the row is reported here tagged `(owner pack not installed)`.
rg -l0 --pcre2 "from\s+['\"](?:prom-client|@opentelemetry/api|@opentelemetry/sdk-metrics|hot-shots|node-statsd|statsd-client|@willsoto/nestjs-prometheus)['\"]|^\s*(?:from|import)\s+(?:prometheus_client|statsd|datadog)\b|\bio\.micrometer\b|prometheus/client_golang|\bPrometheus\.Metrics\b|\blabelNames\s*:" "${X[@]}" "${ROOTS[@]}" |
  xargs -0 -r rg -Hn --pcre2 "$C"'(?![^\n]*exemplarLabels)(?:\blabelNames\s*:\s*\[[^\]\n]*["\x27](?:\w*_id|\w*Id|user\w*|tenant\w*|email|url|path|ip|session\w*|phone|token|query)["\x27]|\.(?:labels|inc|dec|set|observe|startTimer|record|add)\(\s*(?:[\d.]+\s*,\s*)?\{[^}\n]*\b(?:\w*[Ii]d|tenant\w*|user\w*|url|originalUrl|path|email|ip|phone|query)\s*[:,}]|\b(?:req|request)\.(?:url|originalUrl|path|ip|query)\b)'

# 2. Listeners and subscriptions: files that register inside functions and never remove (2a — not a metric's `.observe(`, nor an
#    awaited or object-argument `.subscribe({…})`, which is a remote call); a raised listener cap (2b).
rg -c --pcre2 "$C"'^\s+(?![^\n]*\bawait\s[^\n]*\.subscribe\()[^\n]*?(?:\.(?:on|addListener|prependListener|addEventListener|watch)\(|\.subscribe\(\s*(?!\{)|\bsignal\(\s*\w+\s*\)\.connect\(|\.connect\(\s*\w+\s*,\s*sender|\bon\(\s*\w+\s*,\s*["\x27])' "${X[@]}" "${ROOTS[@]}" |
  while IFS=: read -r f n; do r=$(rg -c --pcre2 '\.(?:off|removeListener|removeAllListeners|removeEventListener|unsubscribe|disconnect|dispose|unwatch|abort)\(|\bonce\(|\{\s*once:\s*true|\bsignal\s*:|\btakeUntil\(|\bfinalize\(|\bfirst\(\)|\btake\(1\)|\bweak\s*=\s*True' "$f"); [ "${r:-0}" -eq 0 ] && echo "$f  registrations=$n removals=0"; done
rg -n --pcre2 "$C"'\bsetMaxListeners\(\s*(?:0|Infinity|[1-9]\d{2,})\s*\)|\bdefaultMaxListeners\s*=' "${X[@]}" "${ROOTS[@]}"

# 3. Work that outlives its owner: intervals against clears per file (3a); tickers, timers, scheduled executors,
#    threads and goroutines started inside a function (3b).
rg -c --pcre2 "$C"'\bsetInterval\(' "${X[@]}" "${ROOTS[@]}" | while IFS=: read -r f n; do c=$(rg -c '\bclearInterval\(|\.unref\(\)' "$f"); echo "$f  setInterval=$n clearInterval/unref=${c:-0}"; done
rg -n --pcre2 "$C"'^\s+[^\n]*?(?:\btime\.(?:NewTicker|Tick)\(|\bthreading\.Timer\(|\bnew\s+Timer\(|\.schedule(?:AtFixedRate|WithFixedDelay)\(|Executors\.new\w*ThreadPool\(|\bnew\s+Thread\(|\bThread\.new\b|\bgo\s+func\s*\()' "${X[@]}" "${ROOTS[@]}"

# 4. State that outlives the request: request data stored on a long-lived object (4a); request, response, socket or
#    context objects put into a container (4b); ThreadLocal with no remove() in the file (4c).
rg -n --pcre2 "$C"'\bthis\.(?!logger\b)\w+\s*=\s*+(?!null\b|undefined\b|new\b|[^;\n]*=>|[^;\n]*\bfunction\b)[^;\n]*\b(?:req|request|ctx|context|currentUser|user|tenant\w*|session|dto|body|payload)\b(?![\w.]*\s*=>)' -g '*.{ts,js,mjs,cjs}' "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 "$C"'\b\w+\.(?:set|push|add|put|append|setdefault|Store)\((?:[^()\n]*,\s*)?\b(?:req|res|request|response|reply|ctx|socket|ws|conn|connection|stream|emitter)\s*[,)]' "${X[@]}" "${ROOTS[@]}"
rg -l --pcre2 '\bThreadLocal\s*<|\bThreadLocal\.withInitial\(' "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -q '\.remove\(\)' "$f" || echo "$f  ThreadLocal without remove()"; done

# 5. Handles never released: an early exit before the response body is read (5a); `.pipe(` on Node streams with no error
#    path (5b); Go response bodies against Close() per file (5c); files and streams opened outside a closing scope (5d).
rg -n --pcre2 "$C"'\bif\s*\(\s*!\s*(?:res|resp|response|upstream|reply|r)\w*\.ok\s*\)\s*(?:\{\s*)?(?:return|throw)\b(?![^\n]*\.(?:text|json|arrayBuffer|blob|body)\b)' -t js -t ts "${X[@]}" "${ROOTS[@]}"
rg -l --pcre2 "$C"'\.pipe\(\s*(?!\))' -t js -t ts "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -q --pcre2 '\bfrom\s+["\x27](?:node:)?(?:stream|fs|zlib|http|https|net)["\x27]|\brequire\(\s*["\x27](?:node:)?(?:stream|fs|zlib)["\x27]|\bcreate(?:Read|Write)Stream\(|\b(?:Readable|PassThrough|Transform)\b' "$f" && ! rg -q --pcre2 '\bpipeline\(|\.on\(\s*["\x27]error["\x27]|\bfinished\(' "$f" && echo "$f  .pipe() with no pipeline/finished/error handler"; done
rg -c --pcre2 "$C"'\b(?:http\.(?:Get|Post|Head|PostForm)|\w+\.Do)\(' -t go "${X[@]}" "${ROOTS[@]}" | while IFS=: read -r f n; do c=$(rg -c 'Body\.Close\(\)' "$f"); [ "${c:-0}" -eq 0 ] && echo "$f  requests=$n Body.Close=0"; done
rg -n --pcre2 "$C"'(?:^\s*\w+\s*=\s*open\(|\bFiles\.(?:lines|list|walk|newBufferedReader)\((?![^\n]*\btry\s*\()|\bnew\s+File(?:Input|Output)Stream\((?![^\n]*\btry\s*\()|\bfs\.promises\.open\(|\bawait\s+open\(\s*[^)\n]+\)\s*;|\bstream\s*=\s*True\b)' "${X[@]}" "${ROOTS[@]}"

# 6. Buffers that grow while a consumer lags: files that write to a stream and never wait for `drain` or use pipeline (6a);
#    in-process batches, backlogs, pending and retry lists that a timer or a downstream call drains (6b).
rg -l --pcre2 "$C"'\.on\(\s*["\x27]data["\x27]|\b\w+\.write\(' -t js -t ts -t py "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -q --pcre2 '\bfrom\s+["\x27](?:node:)?(?:stream|fs|net|zlib|child_process)["\x27]|\brequire\(\s*["\x27](?:node:)?(?:stream|fs|net|zlib)["\x27]|\bcreate(?:Write|Read)Stream\(|\bnew\s+(?:Writable|PassThrough|Transform)\b|\bStreamWriter\b|\bopen_connection\(|\bstart_server\(|\(\s*reader\s*,\s*writer\s*\)' "$f" && ! rg -q --pcre2 '["\x27]drain["\x27]|\bdrain\(\)|\bpipeline\(|\.pause\(\)|\bfor\s+await\b' "$f" && echo "$f  stream writes with no drain / pipeline / pause"; done
rg -n --pcre2 "$C"'\b(?:this\.)?\w*(?:[Bb]uffer|[Bb]atch|[Bb]acklog|[Pp]ending|[Rr]etr(?:y|ies)|[Oo]utbox|[Ii]nbox|[Ss]pool)\w*\s*\.\s*(?:push|unshift|append|appendleft|add|enqueue|offer|put)\(' "${X[@]}" "${ROOTS[@]}"

# 7. A unit of work, session or query log that lives across a batch: configuration and long-lived forks (7a); job files that
#    write through a unit of work and never clear, fork or close it, nor import a local base or helper that forks per event (7b).
rg -n --pcre2 "$C"'(?:\ballowGlobalContext\s*:\s*true|\bthis\.\w+\s*=\s*(?:this\.)?(?:\w+\.)*em\.fork\(|^\s+(?:(?:private|protected|public|readonly)\s+)+\w+\s*(?::[^=\n]+)?=\s*(?:this\.)?(?:\w+\.)*em\.fork\(|\bDB::enableQueryLog\(|^\s*DEBUG\s*=\s*True\b|\bexpire_on_commit\s*=\s*False)' "${X[@]}" "${ROOTS[@]}"
rg -l --pcre2 "$C"'(?:@Processor\(|extends\s+WorkerHost|@Cron\(|@Interval\(|@Scheduled\(|@shared_task|@app\.task|\bdef\s+handle\(self|\bperform\b|\bextends\s+(?:Command|CommandRunner)\b|@Command\(|\bBackgroundService\b|\bIHostedService\b)' "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -q --pcre2 '\b(?:em|entityManager|session|db\.session|_context|dbContext|context)\.(?:persist|add|merge|save|Add|AddRange)\w*\(' "$f" && ! rg -q --pcre2 '\.(?:clear|fork|expunge_all|close|Clear)\(|ChangeTracker\.Clear|AsNoTracking|@(?:Create|Ensure)RequestContext|RequestContext\.create|yield_per|iterator\(|find_each|chunkById|lazyById' "$f" &&
    ! { rg -o -N --pcre2 "from\s+['\"]\K\.{1,2}/[^'\"]+" "$f" | while IFS= read -r i; do b="$(dirname "$f")/$i"; ls "$b".ts "$b".js "$b"/index.ts 2>/dev/null; done | xargs rg -l --pcre2 '\.fork\(|RequestContext\.create|@(?:Create|Ensure)RequestContext' 2>/dev/null | rg -q .; } &&
    echo "$f  writes through a unit of work in a job with no clear/fork/close"; done

# 8. Per-request allocation churn: deep copies and accumulate-by-copy in a reduce. String building in loops and
#    allocation in loops come from the linters in § Adapt (prealloc, PMD, CodeQL string-concatenation-in-loop).
rg -n --pcre2 "$C"'(?:\bJSON\.parse\(\s*JSON\.stringify\(|\bstructuredClone\(|\b(?:_\.)?cloneDeep\(|\bcopy\.deepcopy\(|\.reduce\(\s*(?:async\s*)?\(\s*(\w+)\s*,[^\n]*?=>\s*\(?\s*(?:\[\s*\.\.\.\1\b|\{\s*\.\.\.\1\b))' "${X[@]}" "${ROOTS[@]}"

# 9. Memory limits against worker counts and container limits — deploy and runtime config, read from `.`, not ROOTS.
rg -n -U --pcre2 '(?:--max-old-space-size(?:-percentage)?=\d+|-Xmx\d+[kKmMgG]|\bMaxRAM(?:Percentage)?=\d|\bGOMEMLIMIT\b|\blimits:\s*\{[^}\n]*\bmemory:\s*[^,}\n]+|\blimits:[ \t]*\n(?:[ \t]+\w+:[^\n]*\n){0,3}?[ \t]+memory:\s*\S+|\bmem_limit\s*:\s*\S+|"memory"\s*:\s*"?\d+|\bmemory_mb\s*=\s*\d+|--memory[= ]\S+|\binstance_size_slug\s*:\s*\S+|\b(?:gunicorn|uvicorn|hypercorn|celery|sidekiq|puma)\b[^\n]*\s(?:-w|--workers|-c|--concurrency)[= ]?\s*\S+|\bWEB_CONCURRENCY\b[^\n]*|^\s*workers\s*[=(]\s*\S+|\bworker_concurrency\s*=|\binstances\s*:\s*["\x27]?(?:\d+|max|-1)\b|\bexec_mode\s*:\s*["\x27]?cluster|\bmax_memory_restart\b|--max-memory-restart\b|\bmax_requests(?:_jitter)?\b|--max-requests\b|\bworker_max_(?:memory|tasks)_per_child\b|\bpm\.max_(?:children|requests)\b|^\s*memory_limit\s*=|:concurrency:)' -g 'Dockerfile*' -g '*.{yml,yaml,toml,ini,conf,cfg,env,tf,hcl,json,sh,rb}' -g 'Procfile*' -g '{gunicorn,celery}*.py' -g 'ecosystem.config.*' -g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/dist/**' -g '!ai/**' -g '!docs/**' -g '!.claude/**' -g '!**/{test,tests,__tests__,spec,e2e,fixtures}/**' -g '!**/*{playwright,jest,vitest,cypress}*' -g '!**/{package-lock,composer.lock,Gemfile.lock}*' .
```

A finding is a grep hit **plus** a read of the owner (where the object is created and how long that scope lives) **plus** the write path back to an entry point **plus** a search for the bound. The greps narrow; they do not decide. Three blind spots are structural:

- **Containers passed around.** Grep 1 counts writes and removals in the declaring file only. A registry exported and written from twenty modules, or a removal done by a sweeper elsewhere, shows `removes=0` here and is decided by reading every importer: `rg -n --pcre2 '\b<name>\b' "${ROOTS[@]}"`.
- **Retention through closures.** A callback stored in a long-lived registry keeps everything it captured: `registry.set(id, () => send(req, payload))` retains the request. Grep 4b sees the direct shape; read every `.set(` / `.on(` whose argument is an inline function for what it captures.
- **A drain that exists is not a bound.** A batch flushed every ten seconds is bounded only while the flush succeeds: a flush that puts the batch back on failure (`unshift`, a retry list) grows for as long as the downstream is down. Read the failure path of every drain, and look for a cap with a drop or block policy.

**Measured** (2026-10-02). On a real NestJS-on-Fastify + MikroORM monorepo of about 13,000 tracked files, with `ROOTS` set to the API app and the shared packages, the script runs in about 7 s: grep 1, 19 containers (7 in `scripts/` tooling; of the 12 shipped, 5 have a removal in the same file, 6 are keyed by a bounded set — status names, languages, schema names — or live on a per-run object, and one, an outbound circuit-breaker map, is decided by reading what its key is); grep 2, 9 files; grep 3, 0 (scheduling goes through the framework's `@Interval` and a queue); grep 4, 0; grep 5, 0 (two `.pipe(` files are RxJS, which 5b drops by requiring a Node stream import); grep 6, 1 (a function-local traversal stack, not a buffer); grep 7, 1; grep 8, 2 small JSON round-trip clones; grep 9, 20 lines, including an API and a worker with `--max-old-space-size=700` under a 1 GiB container limit. On `benchmarks/fixtures/node-api`: grep 1 finds the rate limiter's counter `Map` (`writes=1 removes=1`: cleared by a 60 s interval, so bounded per window), grep 2 the request logger's listener on the per-request response, grep 3 that interval (`unref`'d). On `vuln-fullstack`: grep 5a finds two `if (!res.ok) throw` exits before the body is consumed in the remote-image service, grep 8 one `structuredClone` of a settings object, grep 9 a 768 MiB container limit with no heap cap set. `half-built-crm` returns nothing. **Re-measured** 2026-10-15 on the same monorepo (`ROOTS=(apps/api packages/contracts)`): 2a 12 → 4 files (Prometheus `.observe(` and awaited Shopify `.subscribe({…})` calls dropped; the four left are Redis pub/sub and server `on(` registrations to read); 4a 17 → 1 (`=\s*` let the `new` / arrow exclusions backtrack — a constructor assigning `new X(…)` read as request state; `=\s*+` holds them); 7b 5 → 1 (four outbox consumers fork per event inside a shared ledger-consumer helper they import; a bare `Command\b` marker is now `extends Command` / `@Command(`); 1c 1 (a tracing filter hook — the registry's labels are route templates and enums), and on `obs-defects` it returns the seeded `user_id` label (`labelNames` and the `.inc({ user_id })` call). No fixture carries a stream relay or an in-process batch buffer, so grep 6 was checked on seeded samples (a `data` handler writing to a file stream, an asyncio relay with no `drain()`, an event buffer flushed by an interval): it found all three.

## The 3,000-hit path

1. **Intersect and dismiss.** Keep hits in server code reached by a long-running process. Dismiss a whole directory (`scripts/`, tooling, a one-shot CLI) with **one** read that shows no deployed process imports it, and name it in the coverage block.
2. **Group by (owner, key source).** One decision covers every container on the same singleton keyed by the same input; one covers every listener registered on the same emitter.
3. **Rank by key cardinality × call rate.** Per-request ids, URLs, sessions and connections first; per-tenant keys next; domain enums and config sets last (straight to Hardening).
4. **Read the top 30 groups fully.**
5. **Prefer runtime evidence at scale.** Run the e2e suite (or a replay) under `node --expose-gc` with a heap check between batches of distinct inputs, or under `--detectOpenHandles` / `goleak` / `tracemalloc`, and diff. Anything that grows is anchored back to its `<file:line>`; anything flat closes its group.
6. **Ledger the rest** as `Live, unreviewed (k groups / n hits)` with the command that continues them. Never `checked`.

## Scans for

Severity assumes a long-running production process and a key that grows with traffic. Raise one step when the key is per request or per connection and the estimated time-to-OOM is under a day, or when OOM kills are already observed; lower one step when only an admin or a nightly job reaches it.

| § | Class | CWE | Default |
|---|---|---|---|
| 1 | Unbounded process-lifetime container keyed by request data (map, set, array, memoiser, unbounded in-process cache) | CWE-401, CWE-770 | high; critical when keyed per request with time-to-OOM under a day |
| 2 | Listener, subscription or observer registered per request or connection and never removed | CWE-401 | high |
| 3 | Interval, timer, scheduled task, thread or goroutine that outlives its owner | CWE-401, CWE-772 | high |
| 4 | Request state retained by a long-lived object (singleton field, stored closure, `ThreadLocal` in a pool) | CWE-401, CWE-488 | high; critical when another user can read it |
| 5 | Handles never released (unconsumed response bodies, streams not destroyed on error, files, sockets) | CWE-772, CWE-404 | high |
| 6 | Buffers that grow while a consumer lags (ignored stream backpressure, in-process batches, backlogs and retry lists with no cap) | CWE-770 | high when a remote peer or a downstream outage controls the lag; medium otherwise |
| 7 | Unit of work, session or query log carried across a batch | CWE-401 | high in jobs over growing tables; medium otherwise |
| 8 | Per-request allocation churn on a hot path (deep copies, accumulate-by-copy, invariant data rebuilt per call) | CWE-1050 | low; medium on a profiled-hot path |
| 9 | Memory limits that do not fit (heap cap at or above the container limit, workers × per-worker peak over it, recycling masking growth) | CWE-400 | medium; high when OOM kills are observed |

### 1. Unbounded process-lifetime container

```
BAD:   const snapshots = new Map<string, PriceSnapshot>();                 // module scope
       export function snapshot(id) { snapshots.set(id, load(id)); … }        // a key per product viewed, never deleted
       @lru_cache(maxsize=None) def price_for(sku, currency, customer_id): …  # one entry per customer, forever
       private final Map<String, Quote> quotes = new ConcurrentHashMap<>();  // on a singleton @Service
GOOD:  const snapshots = new LRUCache<string, PriceSnapshot>({ max: 5_000, ttl: 60_000 });
       @lru_cache(maxsize=1024) on a function of bounded arguments · Caffeine.newBuilder().maximumSize(10_000)
```
**Read the code:** What is the key, and how many distinct values does production produce per hour (users, ids, URLs, IPs: unbounded; currencies, feature flags, compiled templates per file: bounded)? Is there a removal on every path that ends the entry's life (logout, close, completion, failure), or a sweeper elsewhere? Does `removes>0` in grep 1 really bound it, or only on the happy path? Is the "cache" a source of truth or derived data (a store holding sessions is §4 here for growth and `request-path-scan` §16 for replicas)? Is a memoiser applied to a method (it retains `self`, Ruff `B019`)? **Finding when** the key set grows with traffic and nothing bounds it. **Proof:** the structural count: drive the entry point with N distinct keys (N = 1,000 then 10,000) and assert `size ≤ max` after the fix; it grows linearly before. Without a test hook, the heap-growth shape in [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § "Heap growth".

### 2. Listener or subscription never removed

```
BAD:   wss.on('connection', (ws) => { priceFeed.on('price', (p) => ws.send(p)); });     // one listener per connection, forever
       process.on('unhandledRejection', handler) inside a request handler · bus.setMaxListeners(0)
GOOD:  const onPrice = (p) => ws.send(p); priceFeed.on('price', onPrice); ws.on('close', () => priceFeed.off('price', onPrice));
       events.once(emitter, 'done', { signal }) · RxJS takeUntil(destroy$) · Django signal.connect(receiver, weak=True) (the default)
       Spring: unregister an ApplicationListener added at runtime · Go: return from the goroutine on ctx.Done()
```
**Read the code:** Which object is the emitter, and how long does it live? A listener on `req`, `res`, a socket or a stream dies with that object and is not a finding. One on a module emitter, a shared client (`redis.on`, `ioredis.subscribe`), `process`, or a singleton accumulates. Is there a matching removal on **every** teardown path, including errors and client aborts? Did someone raise the listener cap (grep 2b)? Node's `MaxListenersExceededWarning` in the logs is the runtime tell. **Finding when** a per-request or per-connection registration targets a longer-lived emitter with no removal. **Proof:** `emitter.listenerCount('price')` returns to its baseline after N connections open and close; before the fix it equals N.

### 3. Work that outlives its owner

```
BAD:   onConnection(ws) { setInterval(() => ws.ping(), 30_000); }                 // the interval keeps ws alive after close
       go func() { for v := range ch { … } }()  // ch is never closed and nothing cancels the goroutine
       executor.scheduleAtFixedRate(task, 0, 1, SECONDS) inside a request method
GOOD:  const t = setInterval(…); ws.on('close', () => clearInterval(t));
       go func() { for { select { case <-ctx.Done(): return; case v := <-ch: … } } }()
       one scheduler at boot (Nest @Interval, Spring @Scheduled, a queue) instead of one per request
```
**Read the code:** Is the timer, thread or goroutine started per request or per connection, or once at boot? What stops it, and is that reached on every exit path? What does its callback capture? On Go ≥ 1.23 an unstopped `time.Ticker` or `time.After` in a loop is collectable (`precedents/performance.md` § 54); a goroutine blocked forever is not. **Finding when** per-request work keeps running, or keeps its captures alive, after its owner ends. **Proof:** active handle or goroutine count back to baseline after N requests: Jest `--detectOpenHandles`, `runtime.NumGoroutine()` / `goleak.VerifyNone(t)`, a thread count from the JVM's `ThreadMXBean`.

### 4. Request state retained by a long-lived object

```
BAD:   @Injectable() export class ReportService { private currentUser; run(req) { this.currentUser = req.user; … } }   // default scope = shared
       pending.set(jobId, () => notify(req, result))                      // the closure retains req until the job settles, or forever
       private static final ThreadLocal<User> CURRENT = new ThreadLocal<>();  // set per request, never removed, pooled thread reused
GOOD:  pass the user as an argument, or use AsyncLocalStorage / nestjs-cls / a Scope.REQUEST provider
       store the id, not the request; delete the entry in finally · try { CURRENT.set(u); … } finally { CURRENT.remove(); }
```
**Read the code:** Is the class a singleton (the framework table in § The growth rule)? Is the field written from request data outside the constructor? Does a stored closure capture `req`, `res`, a socket or a large payload, and when is it deleted? Can a second request read the value the first one wrote (a correctness and security consequence, routed per § Boundaries)? **Finding when** request data is written to a process-lifetime holder and either accumulates or crosses requests. **Proof:** two concurrent requests as different users: the second never observes the first's value; for retention, a `WeakRef` to the request object is cleared after `global.gc()` once the request ends (`WeakReference` on the JVM).

### 5. Handles never released

```
BAD:   const res = await fetch(url); if (!res.ok) throw new HttpError(res.status);   // body never read nor cancelled
       createReadStream(path).pipe(gzip).pipe(res)            // an error in the middle leaves the others open
       resp, err := http.Get(u)  … return                    // no defer resp.Body.Close()
       lines = open(path).readlines() · Files.lines(p).count() outside try-with-resources
GOOD:  if (!res.ok) { await res.body?.cancel(); throw … } · await pipeline(createReadStream(path), gzip, res)
       defer resp.Body.Close() · with open(path) as f: · try (Stream<String> s = Files.lines(p)) { … }
```
**Read the code:** Does every exit, including errors and timeouts, consume, cancel or close the handle? Does the stream chain use `pipeline` (which destroys every stage on error) or `.pipe()` with an error handler on each stage? Is the HTTP client pooled, so that an unread body keeps a pooled socket busy until garbage collection? Database connections and cursors are §9 of `connection-config-scan` when the database pack is installed. **Finding when** an exit path leaves a socket, file descriptor or stream open. **Proof:** [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § "Socket and handle count": N failing requests against a local stub, then sockets opened ≤ the pool size and handles back to baseline, the error path included.

### 6. Buffers that grow while a consumer lags

```
BAD:   source.on('data', (chunk) => socket.write(chunk))          // write() returns false and is ignored: Node buffers every chunk
       writer.write(data) in an asyncio relay with no await writer.drain()
       eventBuffer.push(e) per request; a 10 s interval ships it and, on failure, eventBuffer.unshift(...batch)   // grows while the sink is down
       retryQueue.append(evt) on every failed webhook, drained by a loop that also fails
GOOD:  await pipeline(source, socket) · if (!sink.write(c)) await once(sink, 'drain') · await writer.drain()
       a capped buffer with an explicit policy when full (drop oldest and count it, block the producer, spill to a durable queue)
       failed work moves to a durable retry store (a queue with a DLQ, an outbox row), not a process array
```
Node's `writable.write()` documentation is direct: once `write()` returns `false`, "do not write more chunks until the `'drain'` event is emitted"; otherwise "Node.js will buffer all written chunks until maximum memory usage occurs", and a TCP peer that never reads makes this "a remotely exploitable vulnerability" (Node.js 26 docs, *Stream*). **Read the code:** Who sets the consumer's pace: a remote peer, a downstream service, a disk? Does the producer wait (`drain`, `pipeline`, `for await`, `pause()`), or keep writing? For each batch, backlog or retry list, what bounds it while the drain fails: a cap with a drop or block policy, or nothing? Is the buffered work durable elsewhere, or lost on restart as well (`request-path-scan` §22)? **Finding when** a slower or failing consumer makes a process-lifetime buffer grow without bound. **Proof:** heap or RSS high-water with a slow consumer (V29 in [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § "Class variants (performance)"): pipe a fast source into a sink that reads 1 KiB/s, or fail the flush target for N intervals, and assert the buffered bytes stay at the cap after the fix; they grow with time before it.

### 7. Unit of work, session or query log carried across a batch

```
BAD:   for (const chunk of chunks) { for (const r of chunk) em.persist(build(r)); await em.flush(); }   // one EM, identity map grows
       for row in rows: session.add(Model(**row))         # one Session for the whole import, committed at the end
       DEBUG = True in the worker settings · DB::enableQueryLog() in a queue worker
GOOD:  for (const chunk of chunks) { const em = orm.em.fork(); …; await em.flush(); }   // or em.clear() after each flush
       a session per batch, commit and close · Hibernate flush() + clear() every N · EF ChangeTracker.Clear() / AsNoTracking()
```
**Read the code:** How long does the unit of work live: one request (bounded; `precedents/performance.md` § 33), one batch, or the whole worker? Does the ORM keep an identity map at all (the lane table)? Is MikroORM's `allowGlobalContext` turned on so a worker can use the global EM? Is a fork stored in a field and reused across jobs? **Finding when** a unit of work, session or query log accumulates across batches of a growing set. **Proof:** heap after a forced GC, or the identity-map size, flat across batches 1, 5 and 10; per-batch flush time flat as well.

### 8. Per-request allocation churn on a hot path

```
BAD:   const copy = JSON.parse(JSON.stringify(catalog));      // the whole catalog cloned per request
       ids.reduce((acc, x) => [...acc, x.id], [])            // copies the accumulator every step: quadratic allocation
       const byId = new Map(allProducts.map((p) => [p.id, p])) inside the handler, from data that changes daily
GOOD:  clone only what is mutated, or freeze the shared value · ids.map((x) => x.id)
       build the index once and rebuild on change (an event, a version check), not per request
```
Client, agent and regex construction per call are `request-path-scan`'s (this pack). The quadratic **time** of accumulate-by-copy (`[...acc, x]`, `string +=` in a loop) is algorithms `complexity-scan` §2 when that pack is installed (it grades the row; this § lists it with `→ complexity-scan §2`); this § keeps per-request copies of a large constant and the allocation count. Without the algorithms pack, both halves grade here. **Read the code:** Is the path hot (a profile, call rate from APM)? How large is the copied value? Is the work invariant across requests? Python `re.compile` per call is cached by the module and is not this class (`precedents/performance.md` § 28). **Finding when** a hot path allocates in proportion to a large or growing value on every call and a profile or the allocation count shows it. **Proof:** allocations per operation (Go `testing.AllocsPerRun`, JMH `-prof gc`, BenchmarkDotNet `[MemoryDiagnoser]`; in Node, heap used per 1,000 calls after `global.gc()`) fall after the fix; the time ratio at N vs 10N returns to about 10× for accumulate-by-copy (V35).

### 9. Memory limits that do not fit

```
BAD:   limits: { memory: 1Gi } with NODE_OPTIONS=--max-old-space-size=2048      // the kernel kills the pod before V8 collects
       limits: { memory: 2Gi } with gunicorn --workers 8, each peaking at 400 MiB  // 3.2 GiB of workers in a 2 GiB container
       -Xmx2g in a 2 GiB container (no room for metaspace, threads, buffers)
GOOD:  heap cap below the limit with room for native memory: e.g. --max-old-space-size ≈ 70 % of the limit, measured
       GOMEMLIMIT a little under the container limit · workers × measured peak + overhead ≤ limit
```
Facts the arithmetic needs: the JVM's container support is on by default and its default maximum heap is a quarter of the memory it sees (JDK 21 `java` man page; JDK 25 GC tuning guide, *Ergonomics*). Go has had a soft memory limit (`GOMEMLIMIT`) since 1.19, and its GC guide advises leaving "an additional 5-10% of headroom" below a container limit for memory the runtime does not track. Node's default heap limit depends on the version and the memory it detects: read it, do not assume it, with `node -e "console.log(require('v8').getHeapStatistics().heap_size_limit / 2 ** 20)"` inside the image under the container's limit. Recycling settings are a backstop, not a bound: gunicorn's `max_requests` (default 0, off) exists "to help limit the damage of memory leaks" (gunicorn 26 `config.py`); Celery's `worker_max_memory_per_child` (default no limit) replaces a worker after the task that crossed it; PM2's `max_memory_restart`; Octane restarts a worker after 500 requests by default. **Read the code:** Which process runs in which container, and how many per container? Is the heap cap set, and where (Dockerfile `ENV`, the deployment's `env`, `package.json` scripts that only tests use)? What is the measured peak per process (a dashboard, a load test)? Is a recycling setting hiding a growth that §1–§7 should explain? **Finding when** the configured caps cannot fit inside the limit, or OOM kills are observed with no cap below the limit. **Proof:** the arithmetic in the finding (`processes × (heap cap + native overhead) ≤ limit`, each term cited), then a load test at the expected peak with no OOM kill and the runtime's own memory-pressure GC visible before the limit.

## Output

```
memory-growth-scan — lanes: node 22 (package.json engines), nestjs 11 on fastify, mikro-orm 6.6; go, jvm, python absent
Context: 2 long-running processes (api, worker; 1 per container) · limit 1 GiB, heap cap 700 MiB (deploy/k8s/api-deployment.yaml:58)

Findings: 2 · Unconfirmed: 1

1. src/realtime/price-feed.gateway.ts:41                       [report-with-fix]   high
   §2 listener per connection — handleConnection() calls this.feed.on('price', …) on a singleton emitter; no off() on
   disconnect. Proof: test/realtime/price-feed.listeners.e2e-spec.ts — 200 connect/disconnect cycles, listenerCount
   200 (fails; baseline 1). Fix: keep the handler reference and remove it in handleDisconnect(); CWE-401

2. src/catalog/image-import.service.ts:12                      [report-with-fix]   medium
   §5 body never consumed — `if (!res.ok) throw` before reading or cancelling the body of a pooled undici request;
   reached from the product editor's "add image from URL". Proof: 50 failing fetches against a local stub, then
   connections opened = 50 (fails; pool size 10). Fix: `await res.body?.cancel()` before the throw.

3. src/catalog/snapshot.cache.ts:9                             [report-flagged]    medium
   §1 module Map keyed by productId, written per view, no delete in the file (grep 1: writes=1 removes=0).
   Unproven link: a nightly reset may exist outside the file. Settling probe: rg -n '\bsnapshots\b' src/ ; then the
   size test at 1k/10k distinct ids. Fix: LRUCache({ max: 5_000, ttl: 60_000 }).

Verification: 14 candidates → 2 findings · 1 unconfirmed · 8 hardening · 0 pre-existing · 3 refuted

Class coverage:
  §1  process-lifetime containers   checked (19 hits / 12 shipped → 0 findings, 1 unconfirmed; scripts/ dismissed with one read)
  §2  listeners                     checked (9 files → 1 finding)
  §3  timers / threads / goroutines checked (0 hits; scheduling via @Interval and the queue)
  §4  request state on singletons   checked (0 hits)
  §5  handles                       checked (2 hits → 1 finding)
  §6  buffers behind a slow consumer checked (1 hit → 0 findings: a function-local traversal stack)
  §7  unit of work across a batch   checked (1 hit → 0 findings: the job forks per run)
  §8  allocation churn              checked (2 hits → 0 findings: small values, path not hot)
  §9  memory limits                 checked (20 lines → 0 findings: heap cap 700 MiB under a 1 GiB limit)
```

`[report-with-fix]`: the owner, its lifetime, the growing key or payload and the entry point are cited, the oracle fired, and the fix is local. `[report-flagged]`: one link is unproven (a removal that may live elsewhere, a key cardinality assumed, no harness), and the row names it and the settling probe. Numbers carry their label, **measured** or **ESTIMATED**; a number no tool produced is deleted. The coverage block lists **all nine** classes on every run: `checked (k hits → m findings)` only when the grep ran on a present lane; `N/A (<reason>)` only when the repo has no such surface (no long-running process, no JVM); `blocked (<reason>)` when a grep failed or the code could not be read; `Live, unreviewed (k groups / n hits)` for groups left after triage.

## False positives / precedents

The verifier reads [`precedents/performance.md`](../../../../snippets/precedents/performance.md) § "Memory" (precedents 30–33), § "Measurement validity" (52: compare allocations, not time) and the version-aware entries (54: Go timers; 56: Python cycles with `__del__`), plus [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:

- **A map keyed by a domain-bounded set is a lookup table.** Status names, currencies, compiled templates per file, one entry per configured integration: Hardening. It flips back when the key comes from requests or is a row id: "bounded by the number of products" is bounded by a table that grows, not by the code, so a map keyed by product, order or user id with no `max` and no eviction is a §1 Finding.
- **A bounded cache is bounded.** `max` (and a TTL where staleness matters), a `WeakMap` keyed by objects the request owns, a single-flight map whose entry is deleted when the load settles.
- **Heap that plateaus after warm-up is not a leak.** JIT code, connection pools and caches filling to their bound grow first and then stop; one snapshot or one RSS reading proves nothing (§ 31).
- **Per-request objects die with the request.** A listener on `req`, `res`, a socket or a stream; an interval cleared on `close`; a request-scoped unit of work.
- **Boot-time registrations are one-off.** A `process.on('SIGTERM')`, a Redis `subscribe` in `onModuleInit`, a scheduler started once.
- **PHP under FPM and per-invocation serverless functions** start each request with fresh memory: §1–§4 there are `N/A`, except for module scope reused across warm serverless invocations.
- **A recycling setting is evidence, not exoneration.** `max_requests` or `max_memory_restart` present means someone saw growth: look harder at §1–§7, and report §9 only for the limit arithmetic.

## When to run

- On any diff that adds a module- or class-level collection, a memoiser, an in-process cache, a listener or subscription, a timer, a stream relay, an in-process batch or retry buffer, a batch job, or changes a container memory limit, a heap flag or a worker count: the `/perf-audit` dispatch signal.
- On every whole-repo `/perf-audit`, reporting all nine classes.
- When dashboards show RSS or heap climbing under flat load, OOM kills, or a restart cadence: run this first, then hand the top candidates to `memory-leak-hunt` for a soak.

## Halt conditions

- Do not report a high row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md). Under `/perf-audit` that happens in its verification phase; run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on any finding without the growing object's `<file:line>`, its lifetime, the key or payload that grows it, the entry point, and the fix.
- Do not mark a growth finding `[report-with-fix]` on reading alone: the structural count, handle count or heap-growth oracle must have fired across batches of **distinct** inputs. Otherwise it is `[report-flagged]` / Unconfirmed, with the probe written out.
- Do not propose raising the memory limit, adding a restart, `max_requests` or a periodic process recycle as the fix. They hide the growth; the fix bounds it.
- Do not print "no memory growth found" without the class-coverage block. A class whose grep did not run is `blocked`, never `checked`.
- Do not re-derive a class another skill owns (§ Boundaries); cross-link it.

## Related

- `/perf-audit` dispatches this skill and folds its coverage block into the class ledger; `/perf-fix` closes the findings with a failing-first oracle, the bounded primitive, a re-run of this detector on the patched line, and the sibling search.
- `memory-leak-hunt` (this pack) is the runtime oracle: snapshot diffs, the retaining path and the soak for anything a test cannot isolate. `caching-scan` (this pack) owns cache correctness; `request-path-scan` (this pack) owns payload cost, per-call construction, admission control and process-local shared state; `@caching-architect` designs a replacement cache.
- `query-shape-scan` and `connection-config-scan` (database pack, when installed) own the unbounded query and unreleased connections.
- `@resilience-reviewer` (distributed-systems pack, when installed) owns pool and bulkhead sizing; `@tenant-isolation-reviewer` (security pack, when installed) owns request data that crosses users.
- [`proof-oracles.md`](../../../../snippets/proof-oracles.md) (§ "Heap growth", § "Socket and handle count", V29, V32, V35) and [`precedents/performance.md`](../../../../snippets/precedents/performance.md) are the shared proof and precedent files.

Sources (fetched 2026-10-02): NestJS docs, *Injection scopes*; Laravel 12.x docs, *Octane* (Managing Memory Leaks, Max Request Count) and `Illuminate/Database/Connection.php` (12.x, the query log); Django 5.2 FAQ, *Databases and models* (`connection.queries`); Node.js 26.10 docs, *Stream* (`readable.pipe()`) and *CLI*; undici README (*Garbage Collection*); lru-cache README (v11.5.3); gunicorn 26.2.2 `gunicorn/config.py`; Celery 5.6 configuration guide; PM2 7.0 option schema; Go GC guide (*Memory limit*); JDK 21 `java` man page (`UseContainerSupport`) and JDK 25 GC tuning guide (*Ergonomics*). The class list, shapes and oracles come from the performance research catalog for this pack (2026-10-02: CM-01, CM-06, CM-07, RT-13, RT-19, RT-21). Paraphrased; no text reproduced beyond short quoted phrases.
