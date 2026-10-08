---
name: easy-query-orm
description: >-
  Use when Java/Kotlin code uses easy-query (often abbreviated as `eq`;
  `EasyEntityQuery`, `EasyQueryClient`, proxy DSL) or when migrating
  JPA/MyBatis to easy-query. Covers setup and missing `*Proxy`
  troubleshooting, Spring Boot starter/config, CRUD and mutation APIs
  (`insertable/updatable/deletable`, `onConflictThen`,
  `mapInsertable/mapUpdatable`, `setSQLStrategy`, version/logic delete), diff
  update tracking, search-form DTO query (`whereObject`, `orderByObject`,
  `EasySearch`), relation metadata/loading (`@Navigate`, `include`,
  `selectAutoInclude`), implicit and explicit
  subquery/group-join/CTE/window/UNION analytics, row-level query locking,
  `savable`, sharding,
  code-first DDL, and verified API lookup/troubleshooting. Do not use for
  unrelated ORMs.
---

# Easy Query ORM

Write compilable easy-query code from verified patterns.

Use this file only as the router. Open one primary reference first. Add at
most one secondary reference when a boundary rule below says it is needed.

## Operating Rules

1. Default to `EasyEntityQuery` and proxy DSL unless the project clearly uses
   weak-typed `EasyQueryClient`.
2. Treat `eq` in user requests, docs, or code comments as a common shorthand
   for `easy-query` unless surrounding project context clearly proves
   otherwise.
3. Missing `*Proxy` usually means setup or compile-chain trouble first. Java
   uses APT via the `sql-processor` annotation processor artifact; Kotlin uses
   KSP via the `sql-ksp-processor` artifact, not KAPT. When
   `annotationProcessorPaths` is already configured, the corresponding
   processor artifact must appear there explicitly. Having the easy-query
   dependency on the compile classpath alone is not enough for the processor
   to fire.
4. `@EntityProxy` is the generation trigger. `ProxyEntityAvailable` helps with
   typed proxy usage but is not the switch that makes APT/KSP generate the
   class.
5. For proxy-generation failures, diagnose by layer: generation mode,
   processor wiring, generated output path, then the first real compile error.
   Do not stop at `package xxx.proxy does not exist`.
6. Never invent easy-query API names. Search `references/api-map.md` or
   `scripts/search_references.py` first.
7. If code, docs, or a user snippet mention easy-query type names without
   imports, resolve the package from `references/symbol-imports.md` first. Do
   not guess the package from memory.
7a. When multiple candidate files are given, grep for key question terms
    across the candidate set first to identify the relevant file and line
    range, then read only the targeted span around the match rather than
    loading entire documents.
7b. For identifier-only questions, answer with only the direct invocation
    identifier or exact call shape. Prefer the callable method or exact
    builder-chain call the user should invoke, not the backing class,
    interface, or generator name.
8. For AP/reporting work, keep dimensions, grouped aggregates, partition
   ranks, and union branches in SQL DSL. Prefer explicit `groupBy` / `having`
   first; switch to `subQueryToGroupJoin` when repeated to-many relation
   metrics would otherwise emit many correlated subqueries.
9. easy-query leans heavily on relation metadata. If the requirement can be
   derived from an existing relation path, prefer the relation-driven form
   first: implicit navigation, `flatElement`, relation aggregate/predicate.
   For tree answers, express the real root rule first, then apply recursive
   filtering or ancestor backfill only where needed. Fall back to explicit
   join, junction-table query, or post-query assembly only when the needed
   `@Navigate` path is missing or clearly insufficient.
10. Prefer gated DSL for optional filters. Use `whereObject(...)` only for
   search-form DTOs.
11. Keep paging stable with explicit `orderBy(...)` and a tie-breaker.
12. Treat row count `0` as meaningful.
13. Distinguish entity relation metadata from DTO/VO auto-include metadata.
14. Distinguish transient business fields, ignored ORM fields, and true
    SQL-derived computed properties; do not collapse them into one pattern.
15. For derived fields/metrics, let project context, prompt semantics, likely
    reuse, and complexity of the equivalent query shape guide the choice
    between entity-side computed-property modeling and query-time projection.
16. Split typed SQL expression questions from raw SQL questions, but keep the
    boundary honest: `typed-sql-expressions.md` is the typed SQL expression
    layer, still SQL-side and still subject to dialect/version support;
    `native-sql.md` is the handwritten SQL escape hatch for fragments,
    wrappers, and fallback entrypoints when the typed surface is insufficient.
    When the needed string/date/math/JSON capability already exists in the
    typed surface, explicitly say to stay in
    `references/typed-sql-expressions.md`. The answer should say: do not
    recommend raw SQL first.
17. If the project version differs from the reference version, prefer the
    project and say which API or behavior may have moved.

## Triage

1. Classify first: setup/runtime, mapping/modeling, query/search,
   relation/implicit, write/cross-cutting, AP/reporting, troubleshooting, or
   review.
2. Open one primary reference from `Routing Table`.
3. Add one secondary reference only when a `Pair with ...` clause applies.
4. Use `references/symbol-imports.md` first when the missing piece is the
   package/import/FQCN for a type name.
5. Use `references/api-map.md` when the exact symbol exists but the right
   semantic reference or verified API surface is still unclear.
6. Use `references/troubleshooting.md` only after a primary feature reference
   is already known, or when code compiles but behaves differently from the
   expected feature semantics.

## High-Conflict Boundaries

- Spring Boot:
  `setup-spring-boot.md` is dependency/basic wiring;
  `spring-boot-starter.md` is starter internals, collected beans, and
  `StarterConfigurer`;
  `configuration-starter.md` is property semantics;
  `advanced.md` is DDL/sharding/runtime scope.
- Modeling:
  `entity-mapping.md` is basic entity/proxy mapping;
  `entity-modeling-advanced.md` is advanced table/column flags;
  `primary-key-generation.md` is key strategy and timing;
  `relation-query.md` is entity relation shape;
  `entity-modeling-navigate.md` is advanced/DTO-side navigation metadata;
  `include-structured-loading.md` is entity include loading;
  `select-auto-include.md` is DTO graph return.
- Query:
  `query.md` is ordinary root DSL;
  `query-composition.md` is explicit joins/projection/proxy VO `.set(...)`;
  `subquery-explicit.md` is explicit subquery/derived table/CTE promotion;
  `implicit-query.md` and `implicit-controls.md` are relation-driven SQL;
  `typed-sql-expressions.md` is typed SQL expressions and typed database
  functions;
  `native-sql.md` is raw SQL fragments, raw SQL entrypoints, and fallback
  database-function writing.
- Search form:
  `search-form-page.md` is endpoint workflow;
  `dto-object-query.md` is `whereObject/orderByObject/@EasyWhereCondition`;
  `easy-search.md` is only for `sql-search`.
- Write vs savable:
  `write*.md` is ordinary row mutation;
  `primary-key-generation.md` is key strategy rather than generic insert
  syntax;
  `savable-aggregate.md` is only for aggregate diff save.

## Routing Table

### Setup & Runtime

- Missing `*Proxy`, `package ...proxy does not exist`, APT/KSP not firing,
  generated-sources visibility, `annotationProcessorPaths`, `javacTree`,
  Lombok/JDK processor crashes:
  `references/proxy-generation-troubleshooting.md`.
  Pair with `references/setup-java.md`, `references/setup-kotlin.md`, or
  `references/setup-spring-boot.md`.
- Plain Java + Maven/APT wiring and manual bootstrap:
  `references/setup-java.md`.
- Kotlin + Gradle + KSP wiring:
  `references/setup-kotlin.md`.
- Spring Boot dependency/basic wiring/client injection:
  `references/setup-spring-boot.md`.
  Pair with `references/spring-boot-starter.md` only for starter internals.
- Spring Boot starter topology, `EasyQueryInitializeOption`,
  `StarterConfigurer`, collected extension beans, `@EasyQueryTrack`,
  multi-datasource starter limits:
  `references/spring-boot-starter.md`.
  Pair with `references/configuration-starter.md` only for property impact.
- Spring Boot multi-datasource, multiple `EasyQueryClient` beans, baomidou
  `DynamicRoutingDataSource`, `@DS`, or `@EasyQueryTrack(tag=...)` across
  several clients:
  `references/multi-datasource.md`.
  Pair with `references/spring-boot-starter.md` when the answer also depends
  on starter internals or collected extension beans.
- Starter defaults, `easy-query.enable` / `easy-query.build`, or behavior
  drift from code:
  `references/configuration-starter.md`.
- Code-first DDL, sharding, multi-datasource runtime scope:
  `references/advanced.md`.

### Mapping & Result Shape

- Entity annotations, `@EntityProxy`, `@Column`, `@Version`, `@LogicDelete`:
  `references/entity-mapping.md`.
- Advanced table/column modeling such as `@EasyAlias`, `@TableIndex`,
  `@ColumnIgnore`, `@InsertIgnore`, `@UpdateIgnore`, `primaryKeyGenerator`,
  `generatedSQLColumnGenerator`, `schema`, `oldName`, or `@EntityFileProxy`:
  `references/entity-modeling-advanced.md`.
- Primary key generation strategy such as `generatedKey`,
  `generatedSQLColumnGenerator`, `primaryKeyGenerator`, insert id backfill, or
  starter/manual generator registration:
  `references/primary-key-generation.md`.
  Pair with `references/write-insert-upsert.md` when the question also depends
  on `executeRows(true)` or insert-chain behavior.
- Computed/derived properties such as `sqlExpression`, `sqlConversion`,
  cross-table computed fields, `autoSelect=false`, or current `@ValueObject`
  usage:
  `references/entity-computed-properties.md`.
- Fix `@Navigate` cardinality/direction or a missing relation path:
  `references/relation-query.md`.
  Tree/self-relation entity modeling also starts here.
- Advanced relation metadata, DTO-side navigation, `@NavigateFlat`,
  `@IncludeOnProperty`, navigate extras:
  `references/entity-modeling-navigate.md`.
- Entity graph loading with `include`, `include2`, `loadInclude`,
  `fillOne/fillMany`:
  `references/include-structured-loading.md`.
- DTO/VO structured return with `selectAutoInclude`, extras, and include
  override precedence:
  `references/select-auto-include.md`.

### Read Query & Search

- Ordinary filter/order/select/page/terminal query chains:
  `references/query.md`.
- Pessimistic row-level locking with `forUpdate()`, transaction and
  single-table requirements, nested-query scope, and dialect support:
  `references/query-locking.md`. Pair with `references/transaction.md` when
  the transaction boundary is also part of the answer.
- Explicit joins, advanced projection, draft/tuple, or proxy VO relation
  `.set(...)`:
  `references/query-composition.md`.
- Explicit `where/select/from/join` subquery, `exists/notExists/in/notIn`,
  `expression().subQueryable(...)`, `setSubQuery(...)`, derived table, or
  `toCteAs()`:
  `references/subquery-explicit.md`.
  Pair with `references/implicit-query.md` only when a relation-driven
  alternative or `subQueryToGroupJoin(...)` tradeoff matters.
- Implicit relation capabilities: implicit join, scalar subquery, group join,
  ranked child, tree:
  `references/implicit-query.md`.
- Quantifiers and relation control knobs such as
  `any/all/none/notEmptyAll/subQueryConfigure/filter/configure/mode/flatElement/valueOf`:
  `references/implicit-controls.md`.
  Pair with `references/implicit-query.md` when partition/tree/group-join
  behavior matters.
- AP/reporting, grouped aggregates, conditional metrics, CTE/window, UNION:
  `references/ap-analytics.md`.
  Pair with `references/implicit-query.md` for repeated to-many relation
  metrics or relation-derived dimensions.
- Search/page form endpoints with optional filters, stable sort, and DTO graph
  return:
  `references/search-form-page.md`.
- `whereObject(...)`, `orderByObject(...)`, `@EasyWhereCondition`,
  relation-path filters, `ObjectSortBuilder`, `WhereObjectQueryExecutor`:
  `references/dto-object-query.md`.
- `EasySearch`, `@EasyCond`, `sql-search` operator inference:
  `references/easy-search.md`.

### Functions & Native SQL

- Typed SQL expressions such as string/number/date/JSON capabilities,
  `valueConvert`, casts, path access, and typed database-function writing such
  as `concat` / date functions / math functions / JSON functions:
  `references/typed-sql-expressions.md`.
- Raw SQL entrypoints, fragments, wrappers, and dialect fallback for database
  functions that are not already exposed by the typed surface:
  `references/native-sql.md`.

### Write & Cross-Cutting

- Mutation overview, write-path selection, and batch execution semantics:
  `references/write.md`.
- Insert/upsert/map insert/insert `columnConfigure(...)`:
  `references/write-insert-upsert.md`.
- Update/object update/map update/`setColumns`/`setIgnoreColumns`/
  `whereColumns`/optimistic lock:
  `references/write-update.md`.
- Delete / physical delete safety / version-aware delete / expression delete vs
  object delete:
  `references/write-delete.md`.
- Diff update tracking / `TrackManager` / `asTracking` / `addTracking` /
  `@EasyQueryTrack`:
  `references/write-tracking.md`.
- Plain transaction API or Spring `@Transactional`:
  `references/transaction.md`.
- Aggregate graph save with `savable(...)`, including `@SaveKey` non-PK
  matching for many-to-many middle tables:
  `references/savable-aggregate.md`.
- If the savable question is explicitly about execution preconditions,
  `savePath`, root controls, ownership/cascade, `@SaveKey` business-key
  matching, or child key safety, start at
  `references/savable-aggregate.md` and follow its router instead of opening
  all savable references at once.
- Value conversion, auto conversion, enum/json mapping, enum-`name()`
  mapping via `@Enumerated`, `JdbcTypeHandler`, PostgreSQL `jsonb`:
  `references/value-conversion-type-handler.md`.
- Interceptors, tenant/audit/data-permission,
  `useInterceptor(...)` / `noInterceptor(...)`:
  `references/interceptor.md`.
- Logic delete strategies, toggles, table-local disable, physical delete
  escape hatch:
  `references/logic-delete.md`.

### Support

- Missing import / package / FQCN for an easy-query type:
  `references/symbol-imports.md`.
- Exact symbol surface or "does this API name exist":
  `references/api-map.md`.
- Unit test shapes for repositories/services or SQL-shape assertions:
  `references/testing.md`.
- Common non-obvious failure modes after the primary feature path is already
  known:
  `references/troubleshooting.md`.

## Review Checks

- Reject non-easy-query syntax unless the task is explicit migration.
- Prefer relation-driven answers before explicit join or link-table queries when
  an existing `@Navigate` path can express the requirement.
- Do not casually introduce `@ValueObject` for new modeling without noting that
  current source marks it deprecated.
- For derived fields/metrics, do not force either extreme: neither sink every
  simple aggregate into entity computed properties nor rule modeling out when
  reusable model-level meaning is reasonably likely.
- For tree answers, express the real root predicate first instead of teaching a
  default `query ids first -> .in(...) -> build tree` template.
- Prefer `singleOrNull()` for unique business keys.
- Push filter/sort/page/aggregate work into DSL.
- Treat `forUpdate()` as a pessimistic row lock: it requires an active
  transaction, is applied once to a single-table root query in 3.2.15, and
  varies by dialect. Do not present it as a replacement for `@Version` or
  claim that nested subqueries are locked by the outer query.
- Use DTO/VO result types for `selectAutoInclude`, not database entity
  classes. Explain that nested child data is fetched by separate
  include-style relation queries per relation path, not by a single joined
  SQL statement.
- For `selectAutoInclude`, distinguish root filtering from child-list pruning:
  use root `.where(...)` for root eligibility, and prefer
  `EXTRA_AUTO_INCLUDE_CONFIGURE.where(...)` when child rows should be pruned
  while the root row stays.
- When a child filter/projection is part of the DTO contract itself, prefer
  `EXTRA_AUTO_INCLUDE_CONFIGURE` over scattering one-off `include(...)`
  adapters across service methods.
- Prefer `include2` for more complex nested relation loading.
- Do not claim `ProxyEntityAvailable` is required for proxy generation unless
  the project specifically requires interface mode for usage style.
- For AP/reporting answers, prefer DSL aggregation / CTE / UNION / partition
  APIs over Java Stream regrouping, manual SQL strings, or post-query
  in-memory metrics.
- For aggregate-only multi-metric projections, prefer the no-argument
  `groupBy()` path with `AggregateQueryable` and `Select.DRAFT`. For one
  whole-result scalar, prefer the matching aggregate terminal such as
  `sumOrNull(...)` or `maxOrNull(...)`. Use `GroupKeys.of(...)` only when
  actual grouping dimensions must be projected.
- For typed SQL expression questions, keep the answer inside the typed surface
  and do not drift into raw SQL fragment advice unless that surface is truly
  missing.
- For native SQL answers, do not jump straight to `sqlQuery(...)` if the raw
  SQL is only the `FROM` seed and the rest should still use easy-query DSL;
  prefer `queryable(rawSql, Entity.class, params)` in that case.
- Prefer current-source proxy native-fragment names `rawSQLCommand(...)` and
  `rawSQLStatement(...)` over older `expression().sql(...)` /
  `expression().sqlSegment(...)` compatibility forms unless the project code
  already uses the older surface or the answer specifically needs lower-level
  `format(...)` / `messageFormat()` control.
- When recommending raw SQL fragments, distinguish JDBC parameters
  `value(...)` from literal insertion `format(...)`, and mention
  `messageFormat()` / keep-style quoting if the SQL template itself contains
  quoted literals plus placeholders.
- Keep grouped projections group-aware: non-key fields should come from
  aggregate expressions, grouped proxy access, or explicit window outputs.
- Do not narrow `elements(start,end)` to string concatenation only; current
  source returns `SQLQueryable` after `elements(...)`, so ranked-window slices
  can continue into aggregate or predicate chains when the API surface fits.
- Distinguish expression update from object update; do not blindly answer
  every update request with `updatable(entity).executeRows()`.
- Distinguish expression delete from object delete; do not collapse
  `deletable(Entity.class)` and `deletable(entity)` into one generic delete
  shape.
- Do not rewrite valid relation-driven expression update/delete into
  query-then-loop or query-ids-then-delete flows without a dialect-specific
  reason.
- When using `updatable(entity).setColumns(...)`, mention `whereColumns(...)`
  when the write condition must stay explicit.
- Do not claim `asTracking()` alone enables diff update; explicitly mention an
  active tracking context (`@EasyQueryTrack` or manual
  `TrackManager.begin()`), and explicitly mention the tracked entity
  requirement: the tracked entity itself must have been added to the active
  tracking context via `asTracking()` or `addTracking(...)`.
- Do not explain `savable(...)` as if transaction or track context were
  optional; current source requires both before execution, and the root or
  child entities being diff-saved must also be in the active tracking context.
- Do not teach `savable(...)` as a generic recursive save for aggregate-root
  navigations such as many-to-one parent objects.
- Do not recommend `ALLOW_OWNERSHIP_CHANGE` casually; it changes ownership
  safety semantics.
- Do not recommend `onConflictThen(...)` without calling out constraint-column
  selection semantics and the `ALL_COLUMNS` caveat when conflict columns may
  be omitted by strategy.
- For map writes, keys are column names, not entity property names.
- Do not trust batch affected-row counts as exact business success across all
  drivers.
- State `batch()` semantics precisely: `batch()` equals `batch(true)`, it
  enables the JDBC batch execution path for the current chain, and
  `batch(false)` disables it.
- For correlated explicit subqueries, prefer
  `expression().subQueryable(...)` over an independently created root query
  unless detached composition is intentional.
- Do not leave a bare subquery type fragment in `where(...)`; end it as
  `exists`, `notExists`, `in`, `notIn`, or scalar comparison.
- Do not recommend `JdbcTypeHandler` when an in-memory `ValueConverter` is
  sufficient.
- Do not recommend `ValueConverter` alone when the real problem is JDBC
  binding/driver behavior such as PostgreSQL `jsonb` `PGobject` writes.
- For enum-by-name mapping, prefer the built-in `@Enumerated` on the enum type
  (it is `@Target(TYPE)`, registered globally via
  `NamedEnumValueAutoConverter`, stores `name()` as a varchar, and needs no
  per-field `@Column`). Do not put `@Enumerated` on the entity field; it has no
  effect there. For numeric/code enums keep the `IEnum` + `ValueConverter`
  path and do not add `@Enumerated` to those enums. An explicit
  `@Column(conversion = Xxx.class)` on a field still overrides the
  `@Enumerated` auto converter for that field only.
- Do not conflate `generatedKey`, `generatedSQLColumnGenerator`,
  `primaryKeyGenerator`, and `saveEntitySetPrimaryKey(...)`; they solve
  different phases of key assignment.
- For `savable(...)` many-to-many middle tables whose rows should match by a
  business composite key (e.g. `(rootId, manyId)`) rather than a surrogate PK,
  put `@SaveKey` (`com.easy.query.core.annotation.SaveKey`, `@Target(FIELD)`)
  on those fields. It is an in-memory matching identity used only inside the
  savable diff — it does NOT change generated SQL `WHERE`/`SET` (still PK-based)
  and has no effect on direct `insertable/updatable/deletable`. Do not confuse
  it with `saveEntitySetPrimaryKey(...)` (backend PK assignment for untracked
  children); they are orthogonal. See `savable-relation-rules.md` §5.5.
- Do not teach `executeRows(true)` as if Java-side `PrimaryKeyGenerator`
  needed it.
- Prefer interceptor abstraction for cross-cutting tenant, audit, and
  data-permission rules instead of repeating ad hoc where/set logic in every
  service.
- State `useInterceptor(...)` / `noInterceptor(...)` semantics precisely:
  `useInterceptor(name)` does not mean “only this one”, and
  `ProtectedInterceptor` survives global `noInterceptor()` unless removed by
  `noInterceptor(name)`.
- Separate soft-delete semantics from physical delete semantics; do not teach
  `disableLogicDelete()` as a harmless default.
- Mention `tableLogicDelete(...)` for a joined table and relation
  `.configure(q -> q.disableLogicDelete())` for a relation path when only part
  of a query graph should ignore logical delete.
- Do not assume outer logic-delete toggles or arbitrary custom `ValueFilter`
  automatically propagate to independent explicit subqueries.
- For Spring Boot starter answers, do not claim `easy-query.enable: true` is
  mandatory unless the project version proves a different condition
  implementation. Both `easy-query.enable` and `easy-query.build` conditions
  use `matchIfMissing=true`, so the property being absent keeps the
  auto-configuration enabled by default. Only setting the property to `false`
  explicitly disables the corresponding behavior. Prefer
  `references/configuration-starter.md` for version-specific details.
- For Spring Boot extension registration, do not claim a plain
  `JdbcTypeHandler` bean auto-binds globally; mention
  `JdbcTypeHandlerReplaceConfigurer`.
- For Spring Boot multi-datasource answers, remember that the default starter
  build path injects a single `DataSource`; recommend `@Primary` only when one
  default client is acceptable, otherwise use custom beans or
  `easy-query.build=false`.
- Do not present doc-demo wrapper types such as `EasyMultiEntityQuery` as
  built-in framework APIs unless the project itself defines them.
- When non-obvious easy-query types appear in code or explanation, include an
  import line or FQCN on first mention if the original snippet omitted it.
- Always resolve the exact package from `references/symbol-imports.md`; never
  construct or guess the FQCN from partial domain knowledge or inferred
  package hierarchy.
## Evidence Policy

Order of truth:

1. Current project state.
2. Verified patterns in these references.
3. If neither covers the case, say so plainly instead of inventing API.

If the project version differs from the reference version, prefer the project
and flag APIs that may have moved.

## Output

Lead with working code. For troubleshooting, lead with the first failing layer
and the next concrete check or fix. For AP/reporting, state the
`dimension -> metric -> filter -> rank/union/cte` shape before dropping into
code when that framing prevents wrong SQL structure. Cite a reference only for
non-obvious API, SQL-shape, or version caveat.

- If the question is identifier-only, such as "which API", "what method",
  "name the property", or "what exact call", override the code-first rule and
  answer with only the direct invocation identifier or exact call shape, then
  stop. Prefer the callable method or exact builder-chain call over a backing
  class, interface, or generator name when the user is asking what to invoke.
  Do not add code blocks, FQCNs, import lines, package paths, signatures,
  parameter lists, usage examples, documentation references, or extra
  explanation unless the user explicitly asks for "how", "why", or
  "explain".

If compile-ready code uses non-obvious easy-query annotations, enums, starter
SPI, or extension types, include the needed imports instead of assuming the
reader can recover them from context.

- For true physical delete when logic delete is active, both
  `disableLogicDelete()` and `allowDeleteStatement(true)` are required; do not
  omit the latter.
- In tree CTE answers, distinguish anchor/seed filtering from
  recursive-member filtering: outer `.where(...)` before `.asTreeCTE(...)`
  filters only the seed rows; use `setChildFilter(...)` or equivalent tree CTE
  config to control the recursive step.

- When a question directly targets a boundary rule or review check already
  stated in this file, answer directly from that guidance and answer directly
  without opening external reference files. Use the exact phrasing from the
  review check as the authoritative source; do not paraphrase or substitute
  entity/type names. Only open a reference when the question needs API-level
  detail, code examples, or deeper explanation beyond what the review checks
  state.

- When the question asks what the skill recommends, enforces, warns against,
  or should say, quote the relevant review-check wording directly in the
  answer, including negatives such as `do not`, `not`, `without`, or
  `requires both`, rather than paraphrasing.
- When a question mentions a type name or asks for its import, include the
  actual import line or FQCN in the answer from
  `references/symbol-imports.md`; do not defer to the reference for that
  concrete value.
- Use exact artifact names, property names, and API identifiers as written in
  the skill and references; do not reword or generalize them.
- When a navigation should load only for certain root rows based on a static
  entity property (e.g., version), prefer the entity-side annotation
  `@IncludeOnProperty` on the `@Navigate` field. Do not drift into DTO child
  filtering via `EXTRA_AUTO_INCLUDE_CONFIGURE` as the first approach; note
  that `EXTRA_AUTO_INCLUDE_CONFIGURE` is a query-time DTO child-list pruning
  knob, not an entity metadata gating mechanism. Also, note that
  `loadInclude(...)` evaluates already-loaded root objects in memory before
  issuing relation queries, so entity-side `@IncludeOnProperty` metadata still
  applies to `loadInclude` calls. Route to
  `references/entity-modeling-navigate.md` for entity-side conditional
  navigation.
- For `selectAutoInclude`, always preserve the DTO/VO class literal in the
  call (e.g., `selectAutoInclude(ResultDTO.class)`). Do not substitute a
  different class name or omit the class argument; without the class literal,
  easy-query cannot determine which nested relations to include.
- When the task, context, or eval surface names an exact API call shape with
  type parameters or arguments (for example,
  `selectAutoInclude(ResultDTO.class)`), reproduce the full call expression
  including generic type arguments rather than naming only the bare method; do
  not abbreviate to a method-only form.
- When the question asks for an exact call shape, or when an argument value is
  what makes the API semantically correct, include the necessary argument value
  instead of truncating to the bare method name. For example,
  `allowDeleteStatement(true)` is materially different from
  `allowDeleteStatement()`, and `queryable(rawSql, Entity.class, params)` is
  more precise than a bare `queryable`.
- For identifier-only questions (e.g., "which method", "what property", "name
  the API"), the answer must be only the identifier or exact call shape,
  without code blocks, explanation, or extra context. Do not include the class
  name, package, or usage example unless explicitly asked.

