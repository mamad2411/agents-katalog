---
name: n-plus-one-scan
description: Find per-element database round trips — a relation or query touched inside a loop, parallel single-row reads, a resolver per parent with no batch loader, row-by-row writes, per-row counts, joins that multiply rows — across the ORM lanes, each proved by a query-count scaling test.
kind: skill
pack: database
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: n-plus-one-scan

## Premise

An N+1 is one database round trip per element where one statement (or one per relation) would do. Every query in it is fast, so no slow-query log shows it; the cost is N × the round trip, and N grows with the data — page size, a tenant's rows, the size of an upload. CWE files it under **CWE-1050** (resource-consuming call inside a loop) and **CWE-1073** (a method that issues an excessive number of data accesses instead of using the database's set operations). It is the class detection most often gets wrong in both directions: a loop over three currencies is reported, and a lazy relation read by a serializer two files away is missed.

This skill moved from the performance pack: a database round trip belongs to the pack that owns the database. The name is unchanged, so references by name still resolve.

**Every finding cites the per-element call `<file:line>` + the loop, resolver or map it sits in + the entry point that reaches it + the query-count proof (or the test that would settle it) + the fix in the project's ORM.** A grep hit is never a finding by itself. "No N+1 found" is never printed without the class-coverage block (§ Output).

**Detect statically, prove by execution, measure impact last.** The proof is a **query-count scaling test**: the same entry point issues the same number of statements at 2 parents and at 20. Impact (p95, RPS) is the performance pack's ranking step, not a precondition. A candidate read in code with no harness to run the test is **Unconfirmed**, carrying the test that would settle it. It is never dropped as "speculative", and never promoted to Finding on reading alone, because a cost claim needs the oracle to fire ([`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 2, gate 6).

## The rule

A per-element call is a finding when all four hold:

1. **It is a round trip.** Follow the callee to the ORM or driver. An identity-map hit, a request-scoped batch loader, Prisma's same-tick `findUnique` batching, a cache read, or a chunked `IN (…)` statement is not one.
2. **N grows.** The loop's collection comes from a query, the request or an upload. A domain constant (three currencies, a fixed list of queues) does not grow: that is Hardening. A per-parent child set capped by an enforced business rule (an order's lines) grows slowly: still a finding, one severity step lower (§ Scans for). A cap nothing enforces is no cap.
3. **A production entry point reaches it.** Route, resolver, consumer, cron, export. Seeds, tests, migrations and one-off scripts fail here.
4. **Nothing upstream already loaded it.** `populate` / `include` / `select_related` / `with()` / `JOIN FETCH` on the query that built the list, or a lazy-load-raise mode the tests prove is on.

## Boundaries

- Outbound HTTP, cache or queue calls per element (network N+1) → `request-path-scan` § 3, when the performance pack is installed. Without it, the row is Refuted here as `not a DB round trip` with that route named.
- Sequential awaits of **independent** calls (not per element) → `request-path-scan` § 1 (performance pack, when installed); the fix skill is backend's `parallelize-independent-ops`.
- N requests from the browser → frontend `@data-flow-auditor` class 3, when the frontend pack is installed.
- A list with no `LIMIT`, deep OFFSET, over-fetch, `IN` lists with no chunking → `query-shape-scan` (this pack). The index the batched query needs → `index-coverage-scan` (this pack).
- A read-modify-write inside the loop (lost update) → `transaction-scan` (this pack); money, stock, quota or single-use → `logic-race-scan` (security pack, when installed). External I/O inside a transaction that wraps the loop → `transaction-scan` § 1.
- A per-row authorization check that loads the owner per row **is** an N+1 and is reported here; whether the check is correct is security's.

## Adapt to the codebase — the shared ORM lane table

Read the ORM **and its version** from the lockfile or manifest (`package-lock.json` / `pnpm-lock.yaml`, `poetry.lock`, `Gemfile.lock`, `composer.lock`, `go.mod`, `pom.xml`, `*.csproj`), never from memory: load strategies, batching defaults and APIs changed in the last two majors of MikroORM, TypeORM, Prisma and Django. Print the lanes you ran in the output header. The other database detectors reference this table.

| Lane | Per-element shape (the finding) | Fix primitive | Lazy-load-raise / bulk runtime oracle | Query counter for the proof test |
|---|---|---|---|---|
| **MikroORM** 6 / 7 | Always an explicit call: `await x.rel.load()` / `.init()` / `.loadItems()` / `.loadCount()` / `.matching()`, `ref.load()`, `wrap(x).init()`, `em.findOne` / `em.find` / `em.count` per element. An unloaded `Collection` throws on `getItems()` and serializes as `[]` (6.6.16 source), so it never lazy-loads silently. | `populate: ['rel']` on the list query; `em.populate(list, ['rel'])`; `dataloader: DataloaderType.ALL` (default `NONE`) batches `Reference.load()` / `Collection.load()`. `loadStrategy` default: `joined` in 6, `balanced` in 7 (to-one joined, to-many select-in) | per-request `debug: ['query']` log over the e2e suite | `loggerFactory` that counts the `query` namespace |
| **TypeORM** 0.3 / 1.x | lazy relation typed `Promise<T>` awaited per element; `findOne*` / `findBy` per element; `eager: true` loads on every `find*` and is ignored by the QueryBuilder | `relations`, `leftJoinAndSelect`, `relationLoadStrategy: 'query'` for wide joins | `logging: ['query']` | custom `Logger.logQuery` counter |
| **Prisma** 6 / 7 | `findUnique` / `findFirst` / `findMany` awaited per element in sequence; `findMany` per element (never batched) | nested `include` / `select`; `findMany({ where: { fk: { in: ids } } })`. `relationLoadStrategy: 'join'` is still Preview in 7.x | `log: [{ emit: 'event', level: 'query' }]` | `$on('query')` counter (not `$extends`, which counts operations, not SQL) |
| **Sequelize** 6 | association getter `await x.getItems()`, `findByPk` per element | `include`; `separate: true` on a to-many | `logging` callback | `logging: () => n++` |
| **Drizzle** 0.45 | `db.select()…where(eq(…))`, `db.query.t.findFirst` per element | `inArray(t.id, ids)`; relational `with` (one SQL statement, so not N+1, but cap the children) | `logger` | `logger: { logQuery: () => n++ }` |
| **Knex / pg / mysql2** | `pool.query(…)`, `knex(t).where(…)` per element; a repository helper wrapping one | `whereIn`; `= ANY($1)` with an array | `knex.on('query')` | the same, or wrap `pool.query` |
| **Mongoose** 9 | `findById`, per-document `populate` per element | `populate` on the list query; `$in` | `mongoose.set('debug', fn)` | debug-function counter |
| **Django** 5.2–6.1 / DRF | FK or reverse access per element in a view, a template `{% for %}` or a serializer (`SerializerMethodField`, nested `many=True`, `source='a.b'`) over a queryset nobody optimised — DRF does not optimise querysets; `.count()` / `.exists()` per row | `select_related` (FK, 1:1), `prefetch_related` / `Prefetch` (M2M, reverse FK), `annotate(Count(…))`; Django 6.1 `qs.fetch_mode(models.FETCH_PEERS)` | Django 6.1 `FETCH_RAISE`; django-zeal (nplusone is abandoned) | `CaptureQueriesContext`; pytest-django `django_assert_num_queries` (savepoints count) |
| **SQLAlchemy** 2.x | a `relationship()` on its default `lazy="select"` touched per element | `selectinload` (collections), `joinedload` (to-one; a joined collection needs `.unique()`) | `raiseload('*')` / `lazy="raise"` (not applied during flush) | `before_cursor_execute` event counter |
| **Rails** 7.2–8.1 | association read in `.each`, a view partial or a serializer; `.count` per row; a finder per element | `includes` / `preload` / `eager_load`; `counter_cache` | `strict_loading_by_default` + `action_on_strict_loading_violation = :raise`; Prosopite (Bullet misses finder-in-loop) | `assert_queries_count` (7.2+); n_plus_one_control `perform_constant_number_of_queries` |
| **Laravel** 12 / 13 | `$m->rel` in `foreach` / Blade `@foreach`; `->rel()->count()` per row | `with()`, `load()`, `loadMissing()`, `withCount()` | `Model::preventLazyLoading()` (fires only for results of more than one row); `automaticallyEagerLoadRelationships()` hides N+1 from detectors | `$this->expectsDatabaseQueryCount(n)`; `DB::getQueryLog()` |
| **Hibernate / JPA / Spring Data** (Hibernate 6.6 / 7, Boot 4) | lazy collection touched per element or by Jackson; `@ManyToOne` / `@OneToOne` are **EAGER by default**, so a JPQL list fans out into secondary selects; Spring Boot's `open-in-view` (on by default) runs lazy loads during serialization | `JOIN FETCH`, `@EntityGraph`, `@BatchSize` / `hibernate.default_batch_fetch_size`, DTO projections, `FetchType.LAZY` | `hibernate.generate_statistics` (`getCollectionFetchCount()` > 0); `spring.jpa.open-in-view=false` | hypersistence-utils `SQLStatementCountValidator.assertSelectCount(n)`; `getPrepareStatementCount()` |
| **GORM** v1.31 | `db.First` / `Find` / `Take` per element in a `range` loop | `Preload` (1 + k queries, which is fine), `Joins` (to-one only), `Where("id IN ?", ids)` | logger at Info | `db.Callback().Query().After("gorm:query").Register(…)`; go-sqlmock expectations |
| **EF Core** 10 | `FindAsync` / `FirstOrDefaultAsync` in `foreach`; lazy-loading proxies | `Include` / `ThenInclude`; `AsSplitQuery` | `ConfigureWarnings(w => w.Throw(RelationalEventId.MultipleCollectionIncludeWarning))` | `DbCommandInterceptor` counter |
| **Ecto** 3.14 | `Repo.get` / `Repo.preload` inside `Enum.map` (no lazy loading, so always explicit) | `Repo.preload(list, :assoc)`; `preload:` in the query | — | a handler on the repo's `:query` telemetry event |
| **GraphQL / tRPC** (Nest `@ResolveField`, Apollo, Pothos, Strawberry / Graphene, graphql-ruby, gqlgen, Spring `@SchemaMapping`) | a field resolver per parent that calls a repository | a **request-scoped** DataLoader (never a module singleton, which leaks rows across requests); graphql-batch; Spring `@BatchMapping` | — | statements per operation. A tRPC procedure is an endpoint: §2 applies inside it |

NestJS on Express or Fastify issues the same queries either way. The adapter changes how a request-scoped loader is wired, not the count.

## Pre-flight greps

Run as **one** script from the repo root (shell state does not survive between tool calls). Grep **N** feeds detector **§N**; grep 0 is context. Every `rg` names its path (`.`): `rg` given no path reads stdin whenever stdin is a pipe, and under an agent's shell that is a silent zero-hit run. A lane line that prints `No files were searched` means the lane is absent and becomes an `N/A` reason. Any `rg` error on stderr (exit 2) is a failed grep, never zero hits.

```bash
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/.next/**' -g '!**/target/**'
   -g '!**/.venv/**' -g '!**/*.min.*' -g '!**/*.{md,lock,map,svg,json,snap,sql,yml,yaml}')
# Never a production request path: tests, mocks, fixtures, seeds, migrations, generated ORM clients, MikroORM temp/, i18n, docs, ai/.
T=(-g '!**/{test,tests,__tests__,spec,e2e,__mocks__,mocks,fixtures,__fixtures__,testdata,seeds,seeders,migrations,migrate,locales,i18n,generated,__generated__,.prisma,temp}/**'
   -g '!**/*.{spec,test,e2e-spec,mock,stories,test-data,doc}.*' -g '!**/{*_test,*_spec,test_*,conftest}.*' -g '!ai/**' -g '!docs/**')
# A loop header, any stack; capture 1 = its indentation (possessive, so it cannot shrink and swallow the file).
L='^([ \t]*+)(?:(?:async\s+)?(?:for|foreach|while)\b|@foreach\b|[^\n]*?(?:\.(?:forEach|map|flatMap|reduce|each\w*|find_each|filter_map|collect|Select|ForEach)\s*(?:\(\s*async\b|\(\s*\w+\s*->|\{\s*(?:\|\w|\w+\s*->)|\s+do\s*\||\(\s*(?:function|fn)\b)|\bEnum\.\w+\([^\n]*\bfn\b))[^\n]*\n'
# The body: up to 30 lines indented deeper than the header (atomic, so blank lines cannot backtrack exponentially);
# comment lines are skipped; \K makes rg print only the hit line. One line is reported per loop — read the whole loop.
B='(?>\1[ \t]+[^\n]*\n|\1\{[ \t]*\n|[ \t]*\n){0,30}?\1[ \t]++(?!//|#|\*|/\*)[^\n]*?\K'
# An awaited call chain; a receiver that is a queue, cache, Redis or object store is never the database (NR).
NR='(?!(?:this\.)?(?:\w*(?:[Rr]edis|[Cc]ache|[Qq]ueue)s?|media|fileStores?|storage|bucket|s3|objectStore|blobs?)\b)'
A='\bawait\s+'"$NR"'(?:[\w$]+(?:\([^()\n]*\))?[!?]?\.)*'
DB='\b(?:db|DB|tx|Tx|repo|conn|pool|store)\b(?:\.\w+(?:\([^()\n]*\))?)*\.'
JR='\b\w*(?:[Rr]epository|Repo|Dao|DAO|entityManager|jdbcTemplate|session)\.'
RA="$A"'(?:find\w*|get\w*By\w*|fetch[A-Z]\w*|load\w*|init|populate|matching|query\w*|execute\w*|raw|getOne\w*|getMany\w*|getRaw\w*|\$queryRaw\w*|(?:Find|First\w*|Single\w*|ToList|ToArray|Load)Async)\b\s*[(<]'
WA="$A"'(?:save\w*|persistAndFlush|flush|insert\w*|update\w*|upsert\w*|create\w*|delete\w*|remove(?!Objects?\b)\w*|destroy|increment|decrement|native(?:Insert|Update|Delete)|(?:SaveChanges|Add\w*|Update\w*|Remove\w*)Async)\b\s*[(<]'
CA="$A"'(?:count\w*|exists?\w*|aggregate\w*|loadCount|getCount|(?:Count|LongCount|Any|All|Sum|Max|Min|Average)Async)\b\s*[(<]'
RO='\.objects\.(?:get|filter|exclude|first|last|all|raw|in_bulk|values\w*)\(|\bsession\.(?:get|query|execute|scalars?|scalar_one\w*)\(|\.refresh_from_db\(|\b[A-Z][a-z]\w*(?:\.|::)(?:find\w*|where\w*|first\w*|take|pluck|query)\b|->(?:load|loadMissing|fresh)\(|'"$DB"'(?:First|Find|Take|Last|Where|Preload|Raw|Get|Select|Query\w*)\(|'"$JR"'(?:find\w*|get\w*|load|query\w*|createQuery|select\w*)\(|\bRepo\.(?:get\w*|one|all|preload)\b'
WO='\.(?:save|delete)\(\)|\.objects\.(?:create|get_or_create|update_or_create)\(|\.(?:filter|exclude)\([^\n]*\)\.(?:update|delete)\(|\bsession\.(?:flush|commit)\(|\.(?:save!?|update!?|update_columns?|create!?|destroy!?|touch)\b|->(?:save|update|delete|increment|decrement|push)\(|::create\(|'"$DB"'(?:Create|Save|Updates?|UpdateColumns?|Delete|Exec\w*)\(|'"$JR"'(?:save\w*|persist|merge|delete\w*|flush|update)\(|\bRepo\.(?:insert|update|delete)\w*'
CO='\.(?:count|exists)\(\)|\.aggregate\(|\.(?:count|exists\?|sum|average|maximum|minimum)\b(?![(\w])|->\w+\(\)->(?:count|exists|sum|avg|max|min)\(|'"$DB"'Count\(|'"$JR"'(?:count\w*|exists\w*)\(|\bRepo\.aggregate\b'
J=(-t js -t ts -t cs); O=(-T js -T ts -T cs)

# 0. Context, not a detector: files that import the data layer (0a, the triage intersect) and the loading config that
#    decides §1 / §7 verdicts (0b: eager flags, lazy-raise modes, batch loaders, load strategies).
DL=$(rg -l --pcre2 '@mikro-orm/|\btypeorm\b|@prisma/client|\bsequelize\b|drizzle-orm|\bknex\b|\bmongoose\b|from\s+["\x27](?:pg|mysql2(?:/promise)?)["\x27]|\bdjango\.db\b|\bsqlalchemy\b|ActiveRecord::|Illuminate\\Database|jakarta\.persistence|gorm\.io/gorm|Microsoft\.EntityFrameworkCore|\bEcto\.' "${X[@]}" "${T[@]}" .); printf '%s\n' "$DL" | wc -l
rg -n -U --pcre2 '@(?:ManyToOne|OneToMany|ManyToMany|OneToOne|Property|Embedded)\((?:[^@;]){0,240}?\beager:\s*true|@(?:ManyToOne|OneToMany|ManyToMany|OneToOne)\([^\n]*\n\s*\w+[!?]?\s*:\s*Promise<|\blazy\s*=\s*["\x27](?:select|dynamic)["\x27]|FetchType\.EAGER|open-in-view|strict_loading\w*|preventLazyLoading|shouldBeStrict|automaticallyEagerLoadRelationships|raiseload|FETCH_(?:RAISE|PEERS)|\bdataloader\s*:|\bloadStrategy\s*:|relationLoadStrategy|default_batch_fetch_size|@BatchSize' "${X[@]}" "${T[@]}" .

# 1. A relation touched through the loop element. 1a JS/TS explicit loads and awaited lazy props; 1b Python two-hop;
#    1c Ruby; 1d PHP / Blade; 1e Java / Kotlin lazy collections; 1f C# lazy proxies; 1g templates; 1h serializers.
rg -n -U --pcre2 '^([ \t]*+)(?:for\s*(?:await\s*)?\(\s*(?:const|let|var)\s+((?!\w*(?:[Qq]ueue|[Rr]edis|[Cc]ache|[Cc]lient)s?\b)\w+)\s+of\b|[^\n]*\.(?:forEach|map|flatMap)\(\s*async\s*\(?\s*((?!\w*(?:[Qq]ueue|[Rr]edis|[Cc]ache|[Cc]lient)s?\b)\w+))[^\n]*\n(?>\1[ \t]+[^\n]*\n|[ \t]*\n){0,30}?\1[ \t]++(?!//|#|\*|/\*)[^\n]*?\K(?:\bawait\s+(?:\2|\3)\.\w+(?:\.\w+\([^()\n]*\))?\s*(?:[;,)\]]|$)|\b(?:\2|\3)\.\w+\.(?:load|init|loadItems|loadCount|matching)\(|\bawait\s+(?:\2|\3)\.get[A-Z]\w*\(|\bwrap\(\s*(?:\2|\3)\b)' -t js -t ts "${X[@]}" "${T[@]}" .
rg -n -U --pcre2 '^([ \t]*+)(?:async\s+)?for\s+(\w+)\b[^\n]*\bin\b[^\n]*:[ \t]*(?:#[^\n]*)?\n(?>\1[ \t]+[^\n]*\n|[ \t]*\n){0,30}?\1[ \t]++(?!//|#|\*|/\*)[^\n]*?\K\b\2\.(?!(?:id|pk)\b)\w+\.(?!(?:isoformat|strftime|lower|upper|strip|split|replace|format|startswith|endswith|append|extend|add|items|keys|values|get|copy|date|time|year|month|day|hour|minute|total_seconds|quantize|hex|encode|decode)\b)\w+' -t py "${X[@]}" "${T[@]}" .
rg -n -U --pcre2 '^([ \t]*+)[^\n]*\.(?:each|each_with_index|each_with_object|map|flat_map|filter_map|select|reject|sum|group_by|sort_by|find_each|collect)\b[^\n]*?\|\s*(\w+)[^\n]*\n(?>\1[ \t]+[^\n]*\n|[ \t]*\n){0,30}?\1[ \t]++(?!//|#|\*|/\*)[^\n]*?\K\b\2\.\w+\.(?!(?:to_s|to_i|to_f|strftime|iso8601|downcase|upcase|present\?|blank\?|nil\?|round|each|map)\b)\w+' -t ruby "${X[@]}" "${T[@]}" .
rg -n -U --pcre2 '^([ \t]*+)@?foreach\s*\([^\n]*?\bas\s+(?:\$\w+\s*=>\s*)?\$(\w+)[^\n]*\n(?:[^\n]*\n){0,30}?[^\n]*?\K\$\2->\w+(?:\(\))?->\w+' -t php "${X[@]}" "${T[@]}" .
rg -n -U --pcre2 '^([ \t]*+)for\s*\(\s*(?:final\s+)?(?:[\w<>?,.\[\] ]+\s+)?(\w+)\s*(?::|\bin\b)[^\n]*\n(?>\1[ \t]+[^\n]*\n|[ \t]*\n){0,30}?\1[ \t]++(?!//|#|\*|/\*)[^\n]*?\K\b\2\.(?:get[A-Z]\w*\(\)|[a-z]\w*)\.(?:size|stream|forEach|iterator|isEmpty|contains|count|first|sumOf)\b' -t java -t kotlin "${X[@]}" "${T[@]}" .
rg -n -U --pcre2 '^([ \t]*+)foreach\s*\(\s*(?:var|[\w<>?,.]+)\s+(\w+)\s+in\b[^\n]*\n(?>\1[ \t]+[^\n]*\n|\1\{[ \t]*\n|[ \t]*\n){0,30}?\1[ \t]++(?!//|#|\*|/\*)[^\n]*?\K(?:\b\2\.[A-Z]\w*\.(?:Count|Any|Where|Select|Sum|First\w*|ToList)\b|\.Entry\(\s*\2\s*\)\.(?:Collection|Reference)\()' -t cs "${X[@]}" "${T[@]}" .
rg -n -U --pcre2 '(?:\{%-?\s*for\s+(\w+)\s+in\b|<%-?[^%\n]*\.each\s+do\s*\|(\w+)\|)[^\n]*\n(?:[^\n]*\n){0,40}?[^\n]*?\K(?:\{\{-?\s*\1\.\w+\.\w+|<%=[^%\n]*\b\2\.\w+\.\w+)' -g '*.{html,htm,jinja,jinja2,j2,twig,erb}' "${X[@]}" "${T[@]}" .
rg -n --pcre2 'SerializerMethodField|\bsource\s*=\s*["\x27]\w+\.\w+|\b\w+Serializer\([^)\n]*many\s*=\s*True' -t py "${X[@]}" "${T[@]}" .

# 2. An explicit read (repository / ORM / driver) inside a loop body: 2a await-style stacks, 2b the rest.
rg -n -U --pcre2 "$L$B(?:$RA)" "${J[@]}" "${X[@]}" "${T[@]}" .
rg -n -U --pcre2 "$L$B(?:$RO)" "${O[@]}" "${X[@]}" "${T[@]}" .
#    2c. No-ESLint fallback for helper-hidden queries: any `await` in a loop body, only in files that import the data layer
#    ($DL). One line per loop; follow each callee to the driver (2a keys on data-verb names and misses `this.summary(o)`).
printf '%s\n' "$DL" | tr '\n' '\0' | xargs -0 -r rg -n -U --pcre2 "$L$B"'\bawait\b' "${J[@]}"

# 3. Per-element reads fanned out in parallel: Promise.all(xs.map(…)), asyncio.gather(*…), Task.WhenAll(xs.Select(…)).
rg -n -U --pcre2 '^([ \t]*+)[^\n]*?(?:Promise\.(?:all|allSettled)|\bp(?:Map|All)\b|asyncio\.gather|Task\.WhenAll)\s*\((?:[^\n]*?(?:\.(?:map|flatMap|Select)\(|\bfor\b)|[ \t]*\n[ \t]*[\w$.()]+\.(?:map|flatMap|Select)\()(?:[^\n]*?\K|[^\n]*\n(?>\1[ \t]+[^\n]*\n|[ \t]*\n){0,20}?\1[ \t]++(?!//|#|\*|/\*)[^\n]*?\K)(?:\b(?:em|prisma|db|knex|pool|client|tx|trx|manager|queryRunner|session|\w*[Rr]epo\w*|\w*[Ss]ervice|this\.\w+)(?:\.\w+(?:\([^()\n]*\))?)*\.(?:find\w*|findOne\w*|get\w*|load\w*|count\w*|query\w*|execute\w*|exists?\w*|aggregate)\s*[(<]|\b\w+\.objects\.|\bsession\.(?:get|execute|scalars?)\(|(?:Find|First\w*|Single\w*|Count|Any)Async\()' "${X[@]}" "${T[@]}" .

#    3b. The same fan-out with any callee (a use case's `.execute(id)`, a port method, a free function), in the app roots
#    that hold $DL files (apps/api, src, …: a use case calls a port and never imports the ORM itself).
DR=($(printf '%s\n' "$DL" | sed -E 's#^\./##; s#^((apps|packages|services|libs|modules)/[^/]+|[^/]+)/.*#\1#' | sort -u))
[ ${#DR[@]} -gt 0 ] && rg -n -U --pcre2 '^[ \t]*+[^\n]*?(?:Promise\.(?:all|allSettled)|\bp(?:Map|All)\b)\s*\((?:[^\n]*?\K\.(?:map|flatMap)\(|[ \t]*\n\K[ \t]*[^\n]*?\.(?:map|flatMap)\()' -t js -t ts "${X[@]}" "${T[@]}" "${DR[@]}"

# 4. GraphQL files (4a) that define field resolvers (4b) and carry no batch loader (4c): read every per-parent resolver.
rg -l0 --pcre2 '@nestjs/graphql|type-graphql|\bgraphql\b|strawberry|graphene|GraphQL::|gqlgen|@pothos|\bnexus\b' "${X[@]}" "${T[@]}" . | xargs -0 -r rg -l0 --pcre2 '@ResolveField\(|@FieldResolver\(|@SchemaMapping\b|\bdef resolve_\w+\(|@strawberry\.field|^\s*field\s+:\w+|func \(r \*\w+Resolver\) \w+\(ctx context\.Context, obj \*|\bresolve\s*:\s*(?:async\s*)?\(\s*(?:parent|root|obj|source)\b|^\s*\w+\s*:\s*(?:async\s*)?\(\s*(?:parent|root|obj|source)\s*[,)]' | xargs -0 -r rg --files-without-match --pcre2 '\b(?:DataLoader|[Dd]ataloader|BatchLoader|batch_load\w*|load_many|BatchMapping|dataloaden|GraphQL::Batch|loaders?\.)'

# 5. A write per element: save / persist-and-flush / insert / update / upsert / delete.
rg -n -U --pcre2 "$L$B(?:$WA)" "${J[@]}" "${X[@]}" "${T[@]}" .
rg -n -U --pcre2 "$L$B(?:$WO)" "${O[@]}" "${X[@]}" "${T[@]}" .

# 6. A count / exists / aggregate per element.
rg -n -U --pcre2 "$L$B(?:$CA)" "${J[@]}" "${X[@]}" "${T[@]}" .
rg -n -U --pcre2 "$L$B(?:$CO)" "${O[@]}" "${X[@]}" "${T[@]}" .

# 7. Two or more collections joined into one statement (7a), and QueryBuilder files with ≥ 2 join-selects (7b).
rg -n --pcre2 'populate:\s*\[[^\]\n]*,[^\]\n]*\]|populate:\s*\[\s*["\x27](?:\*|\$infer)|relations:\s*(?:\[[^\]\n]*,|\{[^}\n]*,)|include:\s*\{[^}\n]*:\s*(?:true|\{)[^}\n]*,[^}\n]*:\s*(?:true|\{)|\.Include\([^)\n]*\)(?:\s*\.ThenInclude\([^)\n]*\))*\s*\.Include\(|(?i:join\s+fetch)[^\n]*(?i:join\s+fetch)|\beager_load\(|\bjoinedload\([^\n]*joinedload\(' "${X[@]}" "${T[@]}" .
rg -c --pcre2 '\.(?:leftJoinAndSelect|innerJoinAndSelect|joinAndSelect)\(' "${X[@]}" "${T[@]}" . | rg ':(?:[2-9]|\d\d+)$'
```

A finding is a grep hit **plus** a read of the enclosing function **plus** the callee followed to the database **plus** the hops back to an entry point. Three blind spots are structural, so work around them rather than trust a quiet grep:

- **A helper hides the query.** Greps 2a and 3 key on data-verb callee names (`find*`, `get*By*`, `load*`, `execute*`, `query*`). A loop calling `this.summary(order)`, which queries two calls deeper, is missed by them; 2c (any `await` in a loop body of a `$DL` file) and 3b (any `Promise.all(xs.map(…))` in the app roots holding `$DL`) list those loops, and each callee is followed to the driver. A use case that calls a port in a loop sits outside `$DL`: 3b covers its fan-out, and ESLint's `no-await-in-loop` (below) its sequential loop.
- **Indentation scopes the body.** A one-line body (`for (…) await x.save();`) or minified code is missed. On JS / TS, ESLint's `no-await-in-loop` is the cross-check: `npx --no eslint --rule '{"no-await-in-loop":"error"}' -f json <roots>` with the project's own config, keeping only that `ruleId`. Measured on ESLint 10.10.0 (2026-10-02): it reports an `await` in a `for` body, **not** in a `forEach(async …)` or `.map(async …)` callback. Greps 1a and 2a cover those.
- **Serialization is a loop nobody wrote.** A DTO getter, `toJSON`, a Jackson-serialized lazy collection, a Rails serializer or a DRF nested serializer touches a relation per row, with no `for` in sight. Grep 1h lists the DRF cases. For the rest, read the response mapper of every list endpoint.

**Measured** (2026-10-15) on a real NestJS + React monorepo (MikroORM 6.6, 739 `$DL` files), before → after the receiver and scope fixes: 0b 3 → 0 (three `eager: true` options of a Vite glob and React hooks; now only an ORM decorator's), 1a 2 → 0 (loops over BullMQ queues), 5a 50 → 46 (object-store `remove` / `removeObject` calls), 6a 6 → 5 (`redis.exists`); new 2c 242 loops with an `await` (2a sees 56 of them by callee name: the rest call helpers, ports and use cases), new 3b 26 `Promise.all(xs.map(…))` sites in `apps/api` (grep 3 sees 2; 3b found the per-warehouse holds read on every order create). No fixture line was lost; 2c and 3b add the per-element fan-outs `brittle-suite`, `ci-defects`, `quality-mix`, `backend-defects`, `ds-defects` and `slow-marketplace` hide behind helper calls.

Earlier measurement (2026-10-02). On the same monorepo at about 13,000 tracked files, the whole script runs in about 5 s and returns: grep 1, 5 lines (0 true: per-queue job counts over a fixed queue list, Playwright probes); grep 2, 49 (8 in `scripts/` probe directories); grep 3, 1 (full order detail read per id with `Promise.all` in chunks: a real §3 candidate, since chunking bounds the pool, not the N); grep 4, 0; grep 5, 45 (chunked retention deletes, which are precedents, beside per-order `save` calls in bulk commands, which are candidates); grep 6, 29 (27 in Playwright scripts); grep 7, 0. On `benchmarks/fixtures/node-api`, grep 2 returns exactly one line: the seeded N+1. On `vuln-fullstack`, grep 2 returns an image fetch per feed item (outbound HTTP, Refuted here and routed to `request-path-scan`), and grep 5 returns a Prisma `upsert` per feed item inside a request-time import (a real §5 candidate).

## The 3,000-hit path

A large repo can return thousands of lines. Triage in this order, and record every step in the coverage block:

1. **Intersect.** Keep hits in files listed in `$DL` (grep 0a), or in files that import a repository from one. A web app's Playwright probes and a frontend's `fetch` loops drop out here. Dismiss a whole directory (`scripts/`, `tools/`, a probe folder) with **one** read that shows no production entry point imports it, and name it in the coverage block.
2. **Group.** One group = (enclosing function, callee): `rg --json … | jq -r 'select(.type=="match") | "\(.data.path.text):\(.data.line_number)"'`, then bucket by function. One decision covers a group with the same callee and the same loop source.
3. **Rank by reachability.** Rank from the context map: route, resolver, consumer and cron first. Rank list, search, export and report endpoints above detail endpoints, and anything with a known call rate (APM, access logs) first of all.
4. **Read the top 30 groups fully.**
5. **Prefer the runtime bulk oracle at scale.** Turn on the lane's lazy-load-raise mode or a per-request query counter (lane table, fourth column) and run the existing e2e suite once with at least 2 parent rows per fixture. Every detector needs ≥ 2 parents to fire, so a single-row fixture is a false negative. Each raise, or each request whose count moves with N, is a confirmed site.
6. **Ledger the rest.** Report remaining groups as `Live, unreviewed (k groups / n hits)`, with the command that continues them. Never mark them `checked`.

## Scans for

Severity assumes a production entry point and an N that grows with data or the request. Drop one step when N is capped by an enforced business rule ≤ 50. A domain-constant N is Hardening. Raise to **critical** only on production evidence (an APM trace, a pool-exhaustion incident), never from code alone.

| § | Class | CWE | Default |
|---|---|---|---|
| 1 | Relation loaded per element (lazy access, explicit load, serializer, template) | CWE-1073 | high on a list / export path, else medium |
| 2 | Explicit query per element (find-by-id, repository helper) | CWE-1050, CWE-1073 | high on a list / export path, else medium |
| 3 | Per-element reads fanned out in parallel | CWE-1050 | high (it also holds up to N pool connections at once) |
| 4 | Field resolver per parent with no batch loader | CWE-1073 | high |
| 5 | Row-by-row writes | CWE-1050 | medium; high when N is request-sized (imports, bulk actions) |
| 6 | Count / exists / aggregate per element | CWE-1073 | medium; high on a list path |
| 7 | Two or more collections joined in one statement (cartesian rows) | CWE-1049 | medium; high when the parent row is wide or the list is user-facing |

### 1. Relation loaded per element

```
BAD:   for (const o of orders) { await o.items.load(); }                 // MikroORM: N selects
       for o in orders: total += o.customer.discount                     # Django: N selects for customer
       @orders.each { |o| o.customer.name } · foreach ($orders as $o) { $o->customer->name; }   // Rails, Laravel: the same
       for (Order o : orders) { o.getItems().size(); }                   // Hibernate lazy bag, N selects
GOOD:  em.find(Order, where, { populate: ['items'] }) · Order.objects.select_related('customer')
       Order.includes(:customer) · Order::with('customer')->get() · @EntityGraph(attributePaths = "items")
```
**Read the code:** Which relation, and is it to-one or to-many? Was it loaded on the query that built the list (`populate`, `include`, `select_related`, `with`, `JOIN FETCH`, `@EntityGraph`), possibly in a base repository? Does a lazy-raise mode run in tests (grep 0b)? Is the access conditional (a flag, a role, a field the client asked for)? Run the test with it on. For MikroORM, `getItems()` on an unloaded collection throws and `toJSON()` returns `[]`: a missing `populate` there is a **wrong-data** bug, not an N+1. Report it as such, with no query count. **Finding when** the relation is loaded per element and nothing upstream loaded it. **Proof:** the scaling test at 2 and 20 parents (each with ≥ 2 children for a to-many).

### 2. Explicit query per element

```
BAD:   for (const id of ids) { const o = await this.em.findOne(Order, { id }); }
       for (const order of orders) { order.lines = await repo.linesOf(order.id); }
GOOD:  const orders = await this.em.find(Order, { id: { $in: ids } });
       const lines = await repo.linesOfMany(orders.map(o => o.id));  // one IN / = ANY($1), grouped in memory
```
**Read the code:** Follow the callee to the driver. Is it a round trip? An identity-map hit is not: MikroORM `em.findOne(E, pk)` returns an already-managed entity without a query (6.6.16 `EntityManager.findOne` → `tryGetById`), and Hibernate's `find` behaves the same. A cache read the test proves warm is not one either. Does the loop's collection come from a query or the request? Is there an existing batch method (`findByIds`, `whereIn`) the loop could call? MikroORM's default `FlushMode.AUTO` flushes pending changes to that entity type before a `findOne` (6.6.16 `tryFlush`), so a loop that mutates and reads adds a flush per iteration. **Finding when** the call is a round trip per element and N grows. **Proof:** the scaling test.

### 3. Per-element reads fanned out in parallel

```
BAD:   await Promise.all(ids.map((id) => this.em.findOne(Order, { id })));   // N queries, N pool checkouts at once
       await asyncio.gather(*(session.get(Order, i) for i in ids))
GOOD:  await this.em.find(Order, { id: { $in: ids } })   ·   one query, then map by id
```
Parallelism does not remove the N statements. It runs them at once, so a 200-element list takes 200 pool connections and starves every other request. **Precedent:** Prisma batches `findUnique` calls made in the same tick with the same `where` / `include` shape into one query, so `Promise.all(ids.map(id => prisma.x.findUnique({ where: { id } })))` is not a finding. `findMany` is never batched (Prisma docs, *Query optimization*, fetched 2026-10-02). A request-scoped DataLoader is the same precedent. **Read the code:** Is the fan-out bounded (`p-limit`, chunking)? Bounded concurrency still runs N queries: it fixes the pool, not the N+1. **Proof:** the scaling test, plus the pool-wait count under the 20-parent run when the pool is small.

### 4. Field resolver per parent with no batch loader

```
BAD:   @ResolveField() customer(@Parent() o: Order) { return this.customers.findOne(o.customerId); }
GOOD:  @ResolveField() customer(@Parent() o: Order) { return this.loaders.customer.load(o.customerId); }  // request-scoped
```
**Read the code:** Is the loader request-scoped? A module-level loader caches rows across users and tenants, which is a correctness bug and possibly a tenant leak (route it to security when that pack is installed). Does the schema allow lists of this type (`[Order!]!`, connections)? Which nested selections multiply it (orders → items → product)? **Finding when** a resolver on a list-reachable type calls the database per parent. **Proof:** the scaling test on one GraphQL operation that selects the field, at 2 and 20 parents.

### 5. Row-by-row writes

```
BAD:   for (const row of rows) { await this.em.persistAndFlush(toEntity(row)); }      // MikroORM 6; 7: em.persist(x).flush()
       for (const row of rows) { await prisma.product.upsert({ where, create, update }); }
       for r in rows: Model.objects.create(**r)
GOOD:  rows.forEach(r => em.persist(toEntity(r))); await em.flush();   // one unit of work, batched inserts
       prisma.product.createMany({ data, skipDuplicates: true }) · INSERT … ON CONFLICT with a multi-row VALUES
       Model.objects.bulk_create(objs, batch_size=500)
```
`em.persist(x)` in a loop with one `flush()` after it is the **fix**, not the finding: MikroORM, Hibernate, SQLAlchemy and EF Core batch the unit of work at flush. **Read the code:** Is N request-sized (an upload, a bulk action) or job-sized? A job loop that commits one chunk per iteration (`nativeDelete … LIMIT`, `in_batches`, `chunkById`) is the correct shape. Does each row need its own transaction or hooks (callbacks, events) that a bulk API would skip? If so, the bulk fix must reproduce them. **Finding when** each element costs a round trip (or a flush) and N grows. **Proof:** the scaling test, counting INSERT / UPDATE statements and transactions.

### 6. Count / exists / aggregate per element

```
BAD:   for (const p of products) { p.reviewCount = await this.em.count(Review, { product: p }); }
       {% for p in products %}{{ p.reviews.count }}{% endfor %}
GOOD:  one GROUP BY query keyed by parent id · annotate(review_count=Count('reviews')) · withCount('reviews') · counter_cache
```
**Read the code:** Is the number displayed per row on a list? Is a denormalized counter already there (`counter_cache`, a `*_count` column) and simply not used? MikroORM's `Collection.loadCount()` caches the count per collection unless `where` or `refresh` is passed, but it still issues one query per parent. **Proof:** the scaling test.

### 7. Two or more collections joined in one statement

```
BAD:   em.find(Order, {}, { populate: ['items', 'payments'] })   // MikroORM 6 default `joined`: rows = items × payments per order
       .Include(o => o.Items).Include(o => o.Payments)           // EF Core single query
       "select o from Order o join fetch o.items join fetch o.payments"   // Hibernate: two List bags → MultipleBagFetchException
GOOD:  loadStrategy / strategy 'select-in' (MikroORM; `balanced` is the 7.x default) · .AsSplitQuery() · one fetch per collection
```
This is also the guardrail for every §1–§4 fix: eager-loading two to-many relations with a join can return more rows and bytes than the N+1 it replaced. **Read the code:** Which populated relations are to-many? Is the parent row wide (JSON, text, blob)? Does pagination apply? Hibernate applies `setMaxResults` **in memory** over a collection fetch (warning `HHH90003004`; `hibernate.query.fail_on_pagination_over_collection_fetch=true` makes it throw). **Finding when** ≥ 2 to-many relations come back joined in one statement on a list path. **Proof:** `EXPLAIN (ANALYZE)` rows returned vs parent rows, plus the response-size delta before and after split loading.

## Proof — the scaling test

The oracle, its per-stack test shapes and the counters are in [`proof-oracles.md`](../../../../snippets/proof-oracles.md), sections *Counting queries per stack* and *Query-count scaling*; the variant list is its V1. The shape:

1. Seed **2** parents (each with ≥ 2 children for a to-many), call the real entry point through the stack (HTTP, GraphQL operation, consumer handler), and count statements with the lane's counter.
2. Seed 18 more (**20** parents), call again with a page size that holds all 20, and count again. Pagination would otherwise hide the growth.
3. Assert the counts are **equal**. Exact-count asserts are brittle, and max-count asserts miss a small N+1. Count uncached statements: the Rails query cache, Django savepoints and an ORM identity map all distort a naive count.
4. The test **fails before the fix**. A test that passes on the unfixed code proves nothing. Rebuild it until it fails.

**Whole-class variants** (each one a row in the same test, or a sibling test): a top-level relation; a second-level relation (order → items → product); access from a serializer, DTO getter or `toJSON`; a count or exists per row; conditional access with the flag or role turned on; per-row authorization loading the owner; a GraphQL resolver per parent; the CSV / export path and the background job that iterate the same set; a polymorphic, `through` or soft-delete-scoped relation; writes in a loop; page 2 of the same list, which some paginators serve from a different path.

## Output

```
n-plus-one-scan — lanes: mikro-orm 6.6 (package.json), django 6.1 (pyproject.toml); prisma, rails, laravel, jpa, gorm, ef absent
Context: 571 data-layer files · loading config: none set (MikroORM 6 default `joined`, dataloader NONE)

Findings: 2 · Unconfirmed: 1

1. src/orders/list-orders.service.ts:44                         [report-with-fix]   high
   §2 query per element — `await this.em.findOne(Customer, { id: o.customerId })` inside the
   `for (const o of page)` loop at :41. Reached by GET /orders (orders.controller.ts:22), page size ≤ 100.
   Proof: test/orders/list-orders.queries.e2e-spec.ts — 2 orders → 3 statements, 20 orders → 21 (fails).
   Fix: populate: ['customer'] on the em.find at :38; delete the loop query. CWE-1073

2. reports/views.py:61                                           [report-with-fix]   medium
   §6 count per element — `s.orders.count()` per seller row in SellerReportView; reached by
   GET /reports/sellers. Proof: CaptureQueriesContext 2 sellers → 3, 20 sellers → 21.
   Fix: .annotate(order_count=Count('orders')) on the queryset at :52. CWE-1073

3. src/catalog/catalog.resolver.ts:30                            [report-flagged]    high
   §4 resolver per parent — @ResolveField brand() calls this.brands.findOne per product; no loader in the file.
   Unproven link: no GraphQL e2e harness. Settling test: one `products(first: 10) { brand { name } }` operation,
   statements at 2 vs 20 products. Fix: a request-scoped DataLoader keyed by brand id.

Verification: 9 candidates → 2 findings · 1 unconfirmed · 3 hardening · 0 pre-existing · 3 refuted

Class coverage:
  §1  relation per element          checked (5 hits → 0 findings; 2 groups were fixed-size queue lists)
  §2  query per element             checked (49 hits / 31 groups → 1 finding; scripts/ dismissed with one read)
  §3  parallel per element          checked (1 hit → 0 findings: a request-scoped DataLoader sits behind the call)
  §4  resolver per parent           checked (1 file → 1 unconfirmed)
  §5  row-by-row writes             checked (31 hits → 0 findings) · Live, unreviewed (9 groups / 14 hits — continue with grep 5a on src/modules/carriers)
  §6  count per element             checked (29 hits → 1 finding; 27 in a Playwright probe directory)
  §7  multi-collection join         checked (0 hits)
```

`[report-with-fix]`: the call is traced from the entry point to the driver, the scaling test failed, and the fix is a local change in the project's ORM. `[report-flagged]`: one link is unproven (no harness, a callee not read, a load strategy the version leaves ambiguous), and the row names that link and the settling test. The coverage block lists **all seven** classes on every run: `checked (k hits → m findings)` only when the grep ran on a present lane; `N/A (<reason>)` only when the repo has no such surface (no GraphQL, no ORM); `blocked (<reason>)` when the grep failed or the code could not be read. A partial review reads `Live, unreviewed (k groups / n hits)`, never `checked`.

## False positives / precedents

The verifier reads [`precedents/performance.md`](../../../../snippets/precedents/performance.md) (cost classes; *N+1 and query shape* is precedents 15–19) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:

- **SQLite in-process.** Many small queries are cheap without a network hop. N+1 is a client/server cost.
- **A domain-constant N** (three currencies, the enabled payment methods, a fixed queue list) is Hardening. A business cap that nothing enforces is not a cap.
- **Batched by construction.** Prisma's same-tick `findUnique`, a request-scoped DataLoader, GORM `Preload` (1 + k queries), MikroORM's `dataloader` option, a chunked `IN (…)` per iteration, and an identity-map hit.
- **The unit of work batches it.** `persist` in a loop followed by a single `flush` / `commit` / `SaveChanges`.
- **Loops in migrations, seeds, fixtures and one-off CLIs** fail the reachability gate, unless they are the backfill that runs in production.
- **Bulk triage is not a verdict.** "All 49 are in services" is not a reading. A group is dismissed only with the callee followed or the directory shown unreachable.

## When to run

- On any diff that adds or changes a list, search, export or report endpoint, a GraphQL resolver, a serializer or response mapper, a relation mapping, or a loop over query results: the `/db-audit` dispatch signal.
- On every whole-repo `/db-audit`, reporting all seven classes. `/perf-audit` dispatches it when the database pack is installed; without it, the performance pack's ledger lists the N+1 row as `N/A (owner pack database not installed)`.
- When a profile shows "many fast queries" rather than one slow one, or an APM trace shows a repeated statement per request.

## Halt conditions

- Do not report a high row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md). Under `/db-audit` that happens in its verification phase; run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on any finding without the per-element call `<file:line>`, the loop or resolver, the entry point, and the fix in the project's ORM.
- Do not mark a finding `[report-with-fix]` without a scaling test that failed. Without a harness it is `[report-flagged]` / Unconfirmed, with the settling test written out.
- Do not report a grep hit as a finding, and do not dismiss a group without following its callee.
- Do not propose caching the loop, raising the pool size, or parallelizing the N queries as the fix. The fix removes the per-element round trip.
- Do not print "no N+1 found" without the class-coverage block. A class whose grep did not run is `blocked`, never `checked`.
- Do not re-derive a class another skill owns (§ Boundaries). Cross-link it.

## Related

- `/db-audit` dispatches this skill and folds its coverage block into the class ledger. `/db-fix` closes the findings with the failing-first scaling test, the root-cause fix, a re-run of this detector on the patched line, and the sibling search.
- `query-shape-scan` (this pack) owns unbounded lists, OFFSET, over-fetch and `IN` chunking. `index-coverage-scan` (this pack) owns the index the batched query needs. `transaction-scan` (this pack) owns what happens inside a transaction around the loop.
- `@query-optimizer` and `/optimize-query` judge the batched statement's plan after the fix.
- `request-path-scan` § 1 and § 3 and `@performance-optimizer` (performance pack, when installed) own network N+1 and sequential awaits, and rank verified findings by measured or estimated impact. Backend's `parallelize-independent-ops` is the fix skill for independent awaits.
- `@data-flow-auditor` (frontend pack, when installed) owns N requests from the browser.
- `rules/database-principles.md` holds the MUST that related reads are batched or joined; the engineering baseline states the same standard as DATA-12.
