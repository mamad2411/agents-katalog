---
name: guardrail-validation
description: >
  Use this when running mechanical PASS/FAIL guardrail checks at any phase
  exit, when guardrail-validator emits a verdict, or when authoring/diagnosing
  a G-numbered gate. Covers G01-G110: supply-chain (G32-G34),
  benchmark-regression (G65), marker-ownership (G95-G103), dependency-vetting,
  language-adapter convention gates, and the six perf-confidence gates
  G104, G105, G106, G107, G109, G110 (alloc-budget, soak-MMD, soak-drift,
  complexity, profile-no-surprise, perf-exception pairing). Multi-tenancy
  checks inverted to check ABSENCE.
  Triggers: guardrail, validator, PASS, FAIL, G01, G110, supply-chain, marker-ownership, perf-confidence, alloc-budget, soak, complexity, phase-exit.
version: 1.3.1
last-evolved-in-run: v0.6.0-rc.0-sanitization-restore
status: stable
tags: [guardrail, validator, phase-gate, language-pluggable, multi-tenant-saas]
cross_language_ok: true
---

<!-- This skill is intentionally cross-language: the catalog references both Go-pack and Python-pack guardrails by name, and the perf-confidence band detail names tooling that exists in both packs. The leakage scripts honor `cross_language_ok: true` and skip strict scanning. -->


# guardrail-validation (v1.3.0)

## Scope

Catalogs the G-numbered guardrail gates the pipeline runs at phase exits, organized by package ownership. Pack column = which manifest owns the gate. **shared** = language-neutral (lives in shared-core); **go** / **python** = language-specific (lives in the named language adapter manifest). Aspirational entries are forward-declared design intent — script not yet authored — and live in the manifest's `aspirational_guardrails` field.

## When to activate

- `guardrail-validator` agent at every phase exit.
- Any phase lead before claiming phase-green.
- CI-mode full-run invokes every gate end-to-end.

## Catalog

| Band | IDs | Pack | Domain |
|------|-----|------|--------|
| Universal | G01–G07 | shared | Decision-log validity, target-dir discipline, `run_id` stamping, `active-packages.json` validation (G05), `pipeline_version` drift (G06) |
| Intake | G20–G24, G69, G116 | shared | TPRD completeness, non-goals, clarification cap, §Skills-Manifest validation (G23), §Guardrails-Manifest validation (G24), creds hygiene (G69), retired-doc drift (G116) |
| Design (Go) | G30–G38 | go | API-stub compile, dep vetting, `govulncheck`, `osv-scanner`, license allowlist, semver verdict, Go convention match |
| Design (Python) | G30-py–G38-py | python | API-stub import-check, dep vetting (pip-audit + safety), license allowlist, semver verdict, Python convention match (PEP 8/257/484+, pyproject.toml) |
| Impl (Go) | G40–G48 | go | No `TODO` in src, build/vet/fmt/staticcheck, godoc on exported, ctx-first, no `init()` |
| Impl (Python) | G40-py–G48-py | python | No `TODO` / `NotImplementedError` left in src, build (`python -m build`), `mypy --strict`, `ruff format --check`, docstrings on exported, no top-level side effects |
| Testing (Go) | G60–G65 | go | `go test -race`, coverage ≥90%, goleak, flake check (`-count=3`), benchmark delta gate, `Example_*` presence |
| Testing (Python) | G60-py–G65-py | python | `pytest`, `pytest --cov` ≥90%, asyncio-task-leak harness, flake check (pytest-repeat `--count=3`), pytest-benchmark delta gate, doctest presence |
| Feedback | G80, G85, G86 | shared | Evolution-report, learning-notifications written, quality regression ≥5% cap. G82 (golden regression) retired — replaced by four compensating baselines + G86 (see CLAUDE.md Rule 28). |
| Feedback (aspirational) | G81, G83, G84 | shared (aspirational) | Baselines-not-lowered (G81), per-run decision-log entry caps (G83), output-shape hash compensating baseline (G84). All forward-declared per CLAUDE.md rule 28. |
| Meta | G90, G93 | shared | Skill-index ↔ filesystem strict equality (G90), CLAUDE.md rule contiguity (G93). |
| Markers (Go) | G95–G103 | go | MANUAL byte-preservation, constraint-bench-proof, marker-delete consent, do-not-regenerate hash, stable-since semver, deprecated-in horizon, no-forged-traces-to. Backed by Go AST-hash backend (`scripts/ast-hash/go-backend.go`). |
| Markers (Python) | G95-py–G103-py | python | Same marker-protocol contracts realized over Python AST (`scripts/ast-hash/python-backend.py`). |
| Perf-Confidence (Go) | G104, G107, G109 | go | Alloc-budget (G104), complexity-mismatch (G107), profile-no-surprise (G109). Authored. |
| Perf-Confidence (Python) | G104-py, G107-py, G109-py | python | Same axes via Python tooling (pytest-benchmark JSON peak_memory_b, parametrize-N scaling, py-spy CPU profile). Authored. |
| Perf-Confidence (shared) | G105, G106 | shared | Soak-MMD (G105), soak-drift (G106). Single language-neutral scripts; dispatch via active-packages.json:target_language and read perf-budget.md / state.jsonl regardless of pack. |
| Perf-Confidence (aspirational) | G110, G110-py | go / python (aspirational) | Perf-exception marker pairing. Defer until first [perf-exception:] marker ships; shareable as single shared-core script when authored. |

**Catalog–manifest drift rule**: when adding a new G* script, update both this catalog AND the owning package manifest (`.claude/package-manifests/<pack>.json:guardrails` for live, `:aspirational_guardrails` for forward-declared). `scripts/validate-packages.sh` enforces filesystem ↔ manifest consistency.

## Perf-Confidence band detail (G104–G107, G109, G110, applies to both Go and Python pack realizations)

These six gates collectively enforce CLAUDE.md rule 32 (Performance-Confidence Regime) and rule 33 (Verdict Taxonomy PASS / FAIL / INCOMPLETE). G104, G107, G109 are language-specific (separate Go and Python scripts because bench-output and profile formats differ irreducibly). G105, G106 are single shared-core scripts (state-file schema is language-neutral; signal names manifest-driven). G110 is shareable but deferred until first marker ships.

| ID | Severity | Phase | Owner | Check |
|----|---|---|---|---|
| G104 / G104-py | BLOCKER | Impl (M3.5) | profile-auditor (per-pack) | For every bench with a declared `allocs_per_op` (Go) or `heap_bytes_per_call` (Python) in `design/perf-budget.md`, measured ≤ budget. Python uses widened threshold (×1.10 hot, ×1.20 cold) to absorb refcount/GC noise. |
| G105 (shared) | BLOCKER (INCOMPLETE-gated) | Testing (T-SOAK) | drift-detector | For every soak-enabled symbol, final `elapsed_s` in `state.jsonl` ≥ `mmd_seconds`. Verdict < MMD = INCOMPLETE (rule 33) — never auto-passes to PASS. Single language-neutral script. |
| G106 (shared) | BLOCKER | Testing (T-SOAK) | drift-detector | For every declared drift signal, OLS regression over the post-warmup soak timeline. FAIL when slope > 0 AND p < 0.05 AND R² > 0.5 (all three; widens false-positive resistance). Pure-stdlib (no scipy dep). |
| G107 / G107-py | BLOCKER | Testing (T5) | complexity-devil (per-pack) | Scaling sweep at N ∈ {10, 100, 1k, 10k}. Log-log slope fit; compared against declared big-O tolerance window (O(1)→[-0.3,0.5], O(n)→[0.6,1.4], O(n²)→[1.5,2.5], etc.). |
| G109 / G109-py | BLOCKER | Impl (M3.5) | profile-auditor (per-pack) | Top-10 CPU samples ≥ 0.80 coverage over declared hot-path functions. Go: `go tool pprof -top` parsing, runtime.* / syscall.* excluded. Python: py-spy/scalene parsing, asyncio.* / _socket.* / _asyncio.* runtime symbols excluded. <5 user-code samples → INCOMPLETE. |
| G110 (aspirational) | BLOCKER | Impl (M7 + M9) | marker-hygiene-devil | Every `[perf-exception: ... bench/X]` marker in source has a matching entry in `design/perf-exceptions.md` with the same bench name. Orphan markers or orphan entries = FAIL. Authored when first marker ships. |

## Verdict Taxonomy (rule 33)

Any gate that cannot render a decision — profiler unavailable, too few samples, MMD wallclock cap hit before soak completion, flaky benchmark with variance > 20% at `-count=10` — returns **INCOMPLETE**, not PASS. Phase lead surfaces INCOMPLETE verdicts at the applicable HITL gate (H7 for M3.5 gates, H9 for T5 / T-SOAK gates). H9 enumerates INCOMPLETE soak verdicts; user must explicitly extend the run, accept with written waiver, or reject. INCOMPLETE never auto-merges at H10.

## Script mapping

`scripts/guardrails/<id>.sh` (or `.go` / `.py` for compiled / Python-native helpers). Each emits `PASS` / `FAIL:<reason>` / `INCOMPLETE:<reason>` exit codes (0 / 1 / 2 respectively).

## Cross-references

- shared-core `decision-logging` — every guardrail PASS/FAIL emits a decision-log event
- shared-core `review-fix-protocol` — failed BLOCKER guardrails feed the deterministic-first gate before reviewer fleet runs
- `sdk-marker-protocol` — Markers band (G95-G103) enforces the marker grammar
- `sdk-semver-governance` — G31 / `stable-since` semver compatibility check
- CLAUDE.md rule 32 (Performance-Confidence Regime) — rationale for the perf-confidence band
- CLAUDE.md rule 33 (Verdict Taxonomy) — PASS / FAIL / INCOMPLETE semantics
- CLAUDE.md rule 28 (Compensating Baselines) — why G82 retired in favor of G86 + four baselines

---

## Two scopes in this catalog

The G01–G110 catalog above describes guardrails the pipeline runs **on the SDK itself** (`motadatagosdk`, `motadatapysdk`) — language-adapter toolchain, marker protocol, perf-confidence regime, dependency vetting.

The GR-001–GR-024 section below describes guardrails the pipeline runs **on SDK consumers** — the multi-tenant SaaS platform services that depend on the SDK. These check that consumer services respect the platform's multi-tenant invariants: TenantID propagation, schema-per-tenant isolation, JetStream-only inter-service comm, MsgPack wire format, no FK constraints, no SQL JOINs across entities, optimistic locking, soft-delete-only, security headers, and so on. The SDK is built **for** this platform — its consumers must remain compatible.

The two sets are complementary, not overlapping. Both are run by `guardrail-validator` at appropriate phase exits.

---



# Guardrail Validation

Defines the 13 automated quality checks that the guardrail-validator agent runs against all detailed design and implementation outputs. Each check has deterministic PASS/FAIL criteria, a severity level, and an auto-fix suggestion.

## When to Activate
- When the guardrail-validator agent runs its validation pass
- When the detailed-design-lead reviews guardrail compliance
- When any design agent wants to self-check before submitting output
- When adding a new guardrail check to the validation suite
- When interpreting guardrail report results
- Used by: guardrail-validator, detailed-design-lead

## Guardrail Checks

### GR-001: Go Naming Conventions

**What to look for:** Package-qualified name stuttering and incorrect acronym casing in struct, interface, method, and field names.

**PASS criteria:**
- No stuttering: `order.Service` (not `order.OrderService`)
- Correct acronyms: `TenantID`, `HTTPURL`, `APIURL`, `JSONRPC`
- Interfaces named without `I` prefix: `Repository` (not `IRepository`)

**FAIL criteria:**
- Stuttering detected: `order.OrderRepository`, `user.UserService`
- Wrong casing: `TenantId`, `HttpUrl`, `ApiUrl`, `JsonRpc`
- `I`-prefixed interface: `INotifier`, `IEventPublisher`

**Severity:** WARNING

**Auto-fix suggestion:** Rename the type to remove the package name prefix. For acronyms, use all-caps for the entire acronym (`ID`, `URL`, `HTTP`, `API`, `JSON`, `SQL`).

**Script:** `scripts/guardrails/check_naming.sh`

```bash
#!/usr/bin/env bash
# Detect stuttering: type names that repeat the package name
find "$1" -name "*.go" -print0 | while IFS= read -r -d '' f; do
  pkg=$(basename "$(dirname "$f")")
  grep -Pn "type ${pkg^}\w+ (struct|interface)" "$f" && echo "FAIL: $f stuttering"
done
# Detect wrong acronym casing
grep -rPn '(Tenant|Http|Url|Api|Json|Sql)(Id|Url|Api|Rpc)' \
  "$1" --include="*.go"
```

---

### GR-002: TenantID Presence in Domain Structs

**What to look for:** Every struct in `domain/model/` that represents a persistent entity must include a `TenantID` field of type `uuid.UUID`. Even with schema-per-tenant isolation, TenantID is required in Go structs for schema routing (AcquireForTenant), NATS subject construction, logging, and tracing.

**PASS criteria:**
- Struct has `TenantID uuid.UUID` field
- Field is not a pointer (tenant context is always required)

**FAIL criteria:**
- Struct represents a persistent entity but has no `TenantID` field
- TenantID is a `string` instead of `uuid.UUID`

**Severity:** BLOCKER

**Auto-fix suggestion:** Add `TenantID uuid.UUID` as the second field (after `ID`) in the struct definition.

**Script:** `scripts/guardrails/check_tenant_id.sh`

```bash
#!/usr/bin/env bash
# Find domain model structs missing TenantID
for f in $(find "$1" -path "*/domain/model/*.go" -name "*.go"); do
  if grep -q 'type .* struct' "$f" && ! grep -q 'TenantID' "$f"; then
    echo "FAIL: $f missing TenantID in domain struct"
  fi
done
```

---

### GR-003: context.Context as First Parameter

**What to look for:** Every exported method and function that performs I/O or crosses a boundary must accept `context.Context` as its first parameter.

**PASS criteria:**
- `func (s *Service) Create(ctx context.Context, ...) error`
- `func NewHandler(ctx context.Context, ...) *Handler` (for constructors that do I/O)

**FAIL criteria:**
- `func (s *Service) Create(entity Entity, ctx context.Context) error`
- `func (s *Service) Create(entity Entity) error` (no context at all)

**Severity:** BLOCKER

**Auto-fix suggestion:** Move `ctx context.Context` to be the first parameter. If context is missing entirely, add it.

**Script:** `scripts/guardrails/check_context_param.sh`

```bash
#!/usr/bin/env bash
# Find exported methods where context.Context is not the first parameter
grep -rPn 'func \(\w+ \*?\w+\) [A-Z]\w+\([^)]*\)' "$1" \
  --include="*.go" | grep -v 'ctx context.Context' | grep -v '_test.go'
```

---

### GR-004: Schema-Per-Tenant Isolation Verification

**What to look for:** Tenant-scoped services must use `AcquireForTenant` + `SET search_path` for tenant routing. One shared `pgxpool.Pool` per app-database is correct. No `tenant_id` columns. No FK constraints. All SQL uses `:schema` prefix. Verify repositories use `AcquireForTenant` pattern.

**PASS criteria:**
- Repository constructors accept shared `*pgxpool.Pool` (one per app-database)
- Repository methods call `AcquireForTenant(ctx, pool, tenantSchema)` before queries
- `SET search_path` used to scope connection to tenant schema
- Migration files use `:schema` placeholder for all DDL
- No `tenant_id` columns in any table
- No `FOREIGN KEY` constraints in any migration

**FAIL criteria:**
- Migration files contain `tenant_id` columns (schema IS the tenant)
- Migration files contain `FOREIGN KEY` constraints (forbidden platform-wide)
- Migration files missing `:schema` prefix on table names
- Repository code uses `pool.Query()` directly without `AcquireForTenant`
- `SERIAL`/`BIGSERIAL` used instead of UUID
- `TIMESTAMP` used instead of `TIMESTAMPTZ`

**Severity:** BLOCKER

**Auto-fix suggestion:** Use `AcquireForTenant(ctx, pool, tenantSchema)` pattern. Remove `tenant_id` columns. Remove FK constraints. Add `:schema` prefix to all DDL. Replace SERIAL with UUID, TIMESTAMP with TIMESTAMPTZ.

**Script:** `scripts/guardrails/tenant-isolation-check.sh`

---

### GR-004a: No Foreign Key Constraints

**What to look for:** Any `FOREIGN KEY`, `REFERENCES ... ON DELETE`, `REFERENCES ... ON UPDATE` in SQL files.

**PASS criteria:** Zero FK constraint declarations in all SQL files.

**FAIL criteria:** Any FK constraint found.

**Severity:** BLOCKER

**Auto-fix suggestion:** Remove FK constraint. Use plain UUID column with `-- app-managed ref, no FK` comment. Add explicit index on the reference column.

**Script:** `scripts/guardrails/querybuilder-validation-check.sh`

---

### GR-004b: No SQL JOINs Across Entities

**What to look for:** `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`, `CROSS JOIN`, `FULL JOIN` in repository Go files.

**PASS criteria:** Zero SQL JOINs in repository adapter code.

**FAIL criteria:** Any SQL JOIN found in repository code.

**Severity:** BLOCKER

**Auto-fix suggestion:** Remove SQL JOIN. Use cross-join worker pool pattern: run primary query first, collect reference IDs, resolve via `EntityResolver.FetchByIDs()` in parallel.

**Script:** `scripts/guardrails/querybuilder-validation-check.sh`

---

### GR-004c: QueryStruct DSL Enforcement

**What to look for:** List/aggregate queries must use `querybuilder.Compile()` with `EnforcePagination()`, not raw SQL strings.

**PASS criteria:**
- `EnforcePagination()` called before every `Compile()`
- List/Analytics methods use compiled SQL from QueryStruct
- No raw `SELECT ... FROM ... WHERE` strings in repository List methods

**FAIL criteria:**
- `Compile()` called without `EnforcePagination()`
- Raw SQL strings for dynamic list queries

**Severity:** WARNING (BLOCKER for list endpoints)

**Auto-fix suggestion:** Replace raw SQL with `querybuilder.Compile(qs, tenantSchema)` pattern.

**Script:** `scripts/guardrails/querybuilder-validation-check.sh`

---

### GR-004d: MsgPack Columnar Encoding

**What to look for:** List/Analytics repository methods must return `[]byte` (MsgPack via `EncodeColumnar`), not Go structs or JSON. All NATS payloads must use MsgPack encoding exclusively.

**PASS criteria:**
- `encoding.EncodeColumnar()` used in List/Analytics return path
- Content-Type `application/x-msgpack` set on HTTP/NATS responses
- No `json.Marshal` on query result sets
- All NATS message bodies use `msgpack.Marshal`/`msgpack.Unmarshal`

**FAIL criteria:**
- `json.Marshal` on query result rows
- List/Analytics returning Go structs instead of `[]byte`
- `json.Marshal`/`json.Unmarshal` used for NATS message payloads

**Severity:** BLOCKER

**Auto-fix suggestion:** Replace `json.Marshal(rows)` with `encoding.EncodeColumnar(rows, columns, pagination)`. Replace `json.Marshal`/`json.Unmarshal` in NATS adapter code with `msgpack.Marshal`/`msgpack.Unmarshal`.

**Script:** `scripts/guardrails/querybuilder-validation-check.sh`

---

### GR-004e: Optimistic Locking on Updates

**What to look for:** Every UPDATE on a domain entity must include `AND version = $N` in WHERE clause and `version = version + 1` in SET clause.

**PASS criteria:**
- UPDATE includes version check in WHERE
- `RowsAffected() == 0` checked after update
- Version incremented in SET clause

**FAIL criteria:**
- UPDATE without version check
- No `RowsAffected()` check after update

**Severity:** BLOCKER

**Auto-fix suggestion:** Add `AND version = $N` to WHERE, `version = version + 1` to SET, check `RowsAffected()`.

**Script:** `scripts/guardrails/querybuilder-validation-check.sh`

---

### GR-004f: Soft Delete Only

**What to look for:** `DELETE FROM` in repository code. All deletes must be soft: `UPDATE ... SET is_deleted = true, deleted_at = now()`.

**PASS criteria:** Zero `DELETE FROM` in repository adapter code.

**FAIL criteria:** Any `DELETE FROM` found.

**Severity:** BLOCKER

**Auto-fix suggestion:** Replace `DELETE FROM` with `UPDATE ... SET is_deleted = true, deleted_at = now()`.

**Script:** `scripts/guardrails/querybuilder-validation-check.sh`

---

### GR-004g: pg_duckdb Analytics Routing

**What to look for:** Analytics/aggregation methods must set `force_duckdb_execution = true` on acquired connection before running GROUP BY queries.

**PASS criteria:**
- `SET force_duckdb_execution = true` on acquired connection in Analytics methods
- Routing based on `compiled.IsAnalytics` (from QueryStruct GROUP BY presence)

**FAIL criteria:**
- Analytics method missing `force_duckdb_execution` SET
- GROUP BY queries running without DuckDB routing

**Severity:** WARNING

**Auto-fix suggestion:** Add `conn.Exec(ctx, "SET force_duckdb_execution = true")` before analytics query execution.

**Script:** `scripts/guardrails/querybuilder-validation-check.sh`

---

### GR-005: Godoc Comments on Public Types

**What to look for:** Every exported type (`type Foo struct`, `type Bar interface`), function, and method must have a godoc comment starting with the type/function name.

**PASS criteria:**
- `// EntityService handles entity lifecycle operations.`
- Comment starts with the exported name

**FAIL criteria:**
- Exported type with no preceding comment
- Comment does not start with the type name (e.g., `// Handles entities`)

**Severity:** WARNING

**Auto-fix suggestion:** Add `// <TypeName> <brief description>.` immediately above the type declaration.

**Script:** `scripts/guardrails/check_godoc.sh`

```bash
#!/usr/bin/env bash
# Find exported types without godoc comments
grep -rPnB1 '^type [A-Z]\w+ (struct|interface)' "$1" \
  --include="*.go" | grep -v '^--$' | \
  awk '/^[^\/].*type [A-Z]/{print "FAIL: " $0 " missing godoc"}'
```

---

### GR-006: Error Wrapping with %w

**What to look for:** All `fmt.Errorf` calls must use `%w` to wrap the original error, preserving the error chain for `errors.Is()` and `errors.As()`.

**PASS criteria:**
- `return fmt.Errorf("creating entity: %w", err)`
- Wrapping verb is `%w`, not `%v` or `%s`

**FAIL criteria:**
- `return fmt.Errorf("creating entity: %v", err)` (loses error chain)
- `return fmt.Errorf("creating entity: %s", err.Error())` (loses error chain)
- `return errors.New("creating entity: " + err.Error())` (loses error chain)

**Severity:** BLOCKER

**Auto-fix suggestion:** Replace `%v` or `%s` with `%w` in the `fmt.Errorf` format string. Replace string concatenation with `fmt.Errorf("...: %w", err)`.

**Script:** `scripts/guardrails/check_error_wrapping.sh`

```bash
#!/usr/bin/env bash
# Find fmt.Errorf calls using %v or %s instead of %w for error wrapping
grep -rPn 'fmt\.Errorf\([^)]*(%v|%s)[^)]*,\s*err' "$1" --include="*.go"
# Find error string concatenation
grep -rPn 'errors\.New\([^)]*\+\s*err' "$1" --include="*.go"
```

---

### GR-007: No init() Functions

**What to look for:** The `func init()` pattern in any Go file. Per CLAUDE.md rule #4, all initialization must be explicit.

**PASS criteria:**
- No `func init()` declarations in any `.go` file
- Initialization done in constructors or `main()`

**FAIL criteria:**
- Any `func init() { ... }` declaration

**Severity:** BLOCKER

**Auto-fix suggestion:** Move the init() body into a named function and call it explicitly from `main()` or a constructor. For validator registration, use a `NewValidator()` constructor.

**Script:** `scripts/guardrails/check_no_init.sh`

```bash
#!/usr/bin/env bash
# Find init() function declarations
grep -rPn '^func init\(\)' "$1" --include="*.go" && exit 1 || exit 0
```

---

### GR-008: No Global Mutable State

**What to look for:** Package-level `var` declarations that hold mutable state (database connections, caches, configuration). Immutable package-level constants and read-only singletons (like a compiled regex) are acceptable.

**PASS criteria:**
- Dependencies injected via struct fields
- Package-level `var` only for compile-time interface checks or sentinel errors

**FAIL criteria:**
- `var db *pgxpool.Pool` at package level
- `var cache = make(map[string]interface{})` at package level
- `var cfg Config` modified after initialization

**Severity:** BLOCKER

**Auto-fix suggestion:** Move the variable into a struct field and inject it via constructor. Use the composition root (`cmd/main.go`) to wire dependencies.

**Script:** `scripts/guardrails/check_global_state.sh`

```bash
#!/usr/bin/env bash
# Find package-level var declarations that are likely mutable state
# Excludes: interface checks (var _ Interface = ...), errors (var Err...)
grep -rPn '^var\s+(?!_\s|Err)\w+\s+\*?(pgxpool|sql|nats|http\.Client|map\[)' \
  "$1" --include="*.go"
```

---

### GR-009: Migration File Completeness

**What to look for:** Every `.up.sql` migration file must have a corresponding `.down.sql` file with the same numeric prefix.

**PASS criteria:**
- `000001_create_entities.up.sql` has matching `000001_create_entities.down.sql`
- Down migration reverses the up migration (DROP TABLE, DROP INDEX, etc.)

**FAIL criteria:**
- `.up.sql` file exists without a matching `.down.sql`
- `.down.sql` is empty or contains only comments

**Severity:** BLOCKER

**Auto-fix suggestion:** Create the missing `.down.sql` file with the inverse operations (DROP TABLE for CREATE TABLE, DROP INDEX for CREATE INDEX).

**Script:** `scripts/guardrails/check_migrations.sh`

```bash
#!/usr/bin/env bash
# Find .up.sql files without matching .down.sql
for up in $(find "$1" -name "*.up.sql"); do
  down="${up%.up.sql}.down.sql"
  if [ ! -f "$down" ]; then
    echo "FAIL: Missing down migration for $up"
  elif [ ! -s "$down" ]; then
    echo "FAIL: Empty down migration $down"
  fi
done
```

---

### GR-010: Dependency Cycle Detection

**What to look for:** Import cycles between service packages. Service A must not import Service B if Service B imports Service A. Shared types belong in a common package.

**PASS criteria:**
- No circular import paths between service packages
- Shared types in `internal/shared/` or `pkg/` packages

**FAIL criteria:**
- Service A imports Service B's internal types, and Service B imports Service A
- Domain package imports application or adapter packages

**Severity:** BLOCKER

**Auto-fix suggestion:** Extract shared types into a `pkg/shared/` or `internal/shared/` package that both services can import. Use interfaces at service boundaries instead of concrete types.

**Script:** `scripts/guardrails/check_cycles.sh`

```bash
#!/usr/bin/env bash
# Build a dependency graph from import statements and detect cycles
for f in $(find "$1" -name "*.go" -path "*/internal/*"); do
  pkg=$(dirname "$f" | sed 's|.*/internal/||')
  imports=$(grep -Po '"[^"]*internal/\K[^"]+' "$f" 2>/dev/null)
  for imp in $imports; do
    echo "$pkg $imp"
  done
done | sort -u | tsort 2>&1 | grep -i "cycle" && exit 1 || exit 0
```

### GR-012: No Core NATS Usage (JetStream Only)

**What to look for:** Any usage of core NATS APIs (`nc.Publish`, `nc.Subscribe`, `nc.QueueSubscribe`, `nc.Request`, `nc.RequestWithContext`, `nc.RequestMsg`, `msg.Respond`) or JetStream subscribe without queue group (`js.Subscribe`). All inter-service communication MUST use JetStream APIs exclusively: `js.Publish`/`js.PublishMsg` for publishing, `js.QueueSubscribe` for subscribing, and the core NATS request-reply pattern for request-reply.

**PASS criteria:**
- No calls to `nc.Publish(`, `nc.Subscribe(`, `nc.QueueSubscribe(`, `nc.Request(`, `nc.RequestWithContext(`, `nc.RequestMsg(`, or `msg.Respond(`
- No `js.Subscribe(` without queue group (all subscribes use `js.QueueSubscribe`)
- All publish calls use `js.Publish()` or `js.PublishMsg()`
- All request-reply uses the core NATS request-reply pattern (publish to subject with msg.Reply (core NATS auto-set) header, subscribe to reply subject via JetStream)

**FAIL criteria:**
- Any core NATS publish: `nc.Publish(`
- Any core NATS subscribe: `nc.Subscribe(`, `nc.QueueSubscribe(`
- Any core NATS request-reply: `nc.Request(`, `nc.RequestWithContext(`, `nc.RequestMsg(`
- Any core NATS respond: `msg.Respond(`
- Any JetStream subscribe without queue group: `js.Subscribe(` (must use `js.QueueSubscribe`)

**Severity:** BLOCKER

**Auto-fix suggestion:** Replace `nc.Publish()` with `js.PublishMsg()`. Replace `nc.Subscribe()`/`nc.QueueSubscribe()` with `js.QueueSubscribe()`. Replace `nc.Request()`/`nc.RequestWithContext()`/`nc.RequestMsg()` with `core NATS request-reply.Request()`. Replace `msg.Respond()` with `js.PublishMsg()` to the reply subject. Replace `js.Subscribe()` with `js.QueueSubscribe()` and add a queue group name.

**Script:** `scripts/guardrails/no-core-nats.sh`

```bash
#!/usr/bin/env bash
# GR-012: Detect forbidden core NATS API usage in Go source files
# All inter-service communication must use JetStream APIs exclusively.
set -euo pipefail

DIR="${1:-src/}"
FAIL=0

# Forbidden core NATS patterns (bypass JetStream persistence, ack, and dedup)
CORE_PATTERNS=(
  'nc\.Publish\('
  'nc\.Subscribe\('
  'nc\.QueueSubscribe\('
  'nc\.Request\('
  'nc\.RequestWithContext\('
  'nc\.RequestMsg\('
  'msg\.Respond\('
)

for pattern in "${CORE_PATTERNS[@]}"; do
  while IFS= read -r match; do
    if [ -n "$match" ]; then
      echo "FAIL: $match — core NATS API usage detected (use JetStream equivalent)"
      FAIL=1
    fi
  done < <(grep -rPn "$pattern" "$DIR" --include="*.go" 2>/dev/null || true)
done

# Detect js.Subscribe without queue group (must use js.QueueSubscribe)
while IFS= read -r match; do
  if [ -n "$match" ]; then
    echo "FAIL: $match — js.Subscribe without queue group (use js.QueueSubscribe)"
    FAIL=1
  fi
done < <(grep -rPn 'js\.Subscribe\(' "$DIR" --include="*.go" 2>/dev/null | \
  grep -v 'QueueSubscribe' || true)

if [ "$FAIL" -eq 0 ]; then
  echo "PASS: No core NATS API usage found"
  exit 0
else
  exit 1
fi
```

---

### GR-013: Stream-Per-Service Validation

**What to look for:** Every microservice in `src/services/` must bootstrap its own JetStream stream at startup by calling `EnsureStream`. The stream name must follow the UPPER_SNAKE_CASE convention derived from the service name. Stream subjects must include both domain event subjects (`tenant.*.{service}.>`) and reply subjects (``). All `QueueSubscribe` calls must specify a non-empty queue group name.

**PASS criteria:**
- Every service directory in `src/services/` has at least one `.go` file containing an `EnsureStream` call
- Stream name in the config matches UPPER_SNAKE_CASE of the service directory name (e.g., `identity` -> `IDENTITY`, `api-gateway` -> `API_GATEWAY`)
- Stream subjects include `tenant.*.{service}.>` pattern for domain events
- Stream subjects include `` pattern for request-reply
- All `QueueSubscribe` calls have a non-empty queue group argument (second parameter is not `""`)

**FAIL criteria:**
- Service directory exists in `src/services/` but has no `EnsureStream` call
- Stream name does not match the expected UPPER_SNAKE_CASE convention
- Missing `tenant.*.{service}.>` subject in stream config
- Missing `` subject in stream config
- Any `QueueSubscribe` call with an empty string `""` as queue group

**Severity:** BLOCKER

**Auto-fix suggestion:** Add `EnsureStream()` call in the service's `main()` or initialization function using `ServiceStreamConfig` with the correct service name, subjects, and retention policy. For empty queue groups, assign the conventional name `{service}-{handler-name}`.

**Script:** `scripts/guardrails/stream-per-service.sh`

```bash
#!/usr/bin/env bash
# GR-013: Validate that every service bootstraps its own JetStream stream
# and all QueueSubscribe calls use non-empty queue groups.
set -euo pipefail

DIR="${1:-src/services/}"
FAIL=0

# Check each service directory for EnsureStream call
if [ -d "$DIR" ]; then
  for svc_dir in "$DIR"/*/; do
    [ -d "$svc_dir" ] || continue
    svc_name=$(basename "$svc_dir")

    # Check for EnsureStream call
    if ! grep -rq 'EnsureStream' "$svc_dir" --include="*.go" 2>/dev/null; then
      echo "FAIL: $svc_dir — service '$svc_name' has no EnsureStream call (must bootstrap its JetStream stream at startup)"
      FAIL=1
      continue
    fi

    # Derive expected stream name (UPPER_SNAKE_CASE)
    expected_stream=$(echo "$svc_name" | tr '[:lower:]-' '[:upper:]_')

    # Check stream name matches convention
    if ! grep -rPq "(\"$expected_stream\"|toStreamName|StreamName.*$expected_stream)" "$svc_dir" --include="*.go" 2>/dev/null; then
      # Also accept dynamic derivation via toStreamName or ServiceStreamConfig with service name
      if ! grep -rPq "ServiceName:\s*\"$svc_name\"" "$svc_dir" --include="*.go" 2>/dev/null; then
        echo "FAIL: $svc_dir — stream name should be '$expected_stream' (UPPER_SNAKE_CASE of '$svc_name')"
        FAIL=1
      fi
    fi

    # Check for tenant domain subject pattern
    if ! grep -rPq "tenant\.\*\.$svc_name\.>" "$svc_dir" --include="*.go" 2>/dev/null; then
      # Accept if using ServiceStreamConfig (EnsureStream auto-generates subjects)
      if ! grep -rPq "ServiceName:\s*\"$svc_name\"" "$svc_dir" --include="*.go" 2>/dev/null; then
        echo "FAIL: $svc_dir — missing tenant.*.${svc_name}.> subject in stream config"
        FAIL=1
      fi
    fi

    # Check for reply subject pattern
    if ! grep -rPq "$svc_name\._reply\.>" "$svc_dir" --include="*.go" 2>/dev/null; then
      # Accept if using ServiceStreamConfig (EnsureStream auto-generates subjects)
      if ! grep -rPq "ServiceName:\s*\"$svc_name\"" "$svc_dir" --include="*.go" 2>/dev/null; then
        echo "FAIL: $svc_dir — missing ${svc_name}._reply.> subject in stream config"
        FAIL=1
      fi
    fi
  done
fi

# Check for empty queue group in QueueSubscribe calls across all source
SCAN_DIR="${2:-src/}"
while IFS= read -r match; do
  if [ -n "$match" ]; then
    echo "FAIL: $match — QueueSubscribe with empty queue group (must specify a non-empty queue group name)"
    FAIL=1
  fi
done < <(grep -rPn 'QueueSubscribe\([^,]+,\s*""' "$SCAN_DIR" --include="*.go" 2>/dev/null || true)

if [ "$FAIL" -eq 0 ]; then
  echo "PASS: All services have stream bootstrap and valid queue groups"
  exit 0
else
  exit 1
fi
```

---

## Guardrail Report Format

The guardrail-validator agent produces a report in this exact format:

```yaml
guardrail_report:
  run_id: "<from-run-manifest>"
  timestamp: "<ISO-8601>"
  agent: "guardrail-validator"
  summary:
    total_checks: 13
    passed: 11
    failed: 2
    blockers: 1
    warnings: 1
  checks:
    - id: GR-001
      name: "Go Naming Conventions"
      severity: WARNING
      status: PASS
      findings: []
    - id: GR-002
      name: "TenantID Presence"
      severity: BLOCKER
      status: FAIL
      findings:
        - file: "docs/detailed-design/components/notification-service/domain/model/preference.go"
          line: 12
          description: "Struct NotificationPreference missing TenantID field"
          auto_fix: "Add TenantID uuid.UUID as second field"
    # ... remaining checks
  verdict: BLOCK | CONDITIONAL | PASS
  verdict_rule: >
    BLOCK if any BLOCKER check has status FAIL.
    CONDITIONAL if only WARNING checks have status FAIL.
    PASS if all checks have status PASS.
```

## Script-to-Check Mapping

| Check | Script Path | Run Command |
|-------|-------------|-------------|
| GR-001 | `scripts/guardrails/check_naming.sh` | `bash scripts/guardrails/check_naming.sh docs/detailed-design/` |
| GR-002 | `scripts/guardrails/check_tenant_id.sh` | `bash scripts/guardrails/check_tenant_id.sh docs/detailed-design/` |
| GR-003 | `scripts/guardrails/check_context_param.sh` | `bash scripts/guardrails/check_context_param.sh docs/detailed-design/` |
| GR-004 | `scripts/guardrails/check_tenant_isolation.sh` | `bash scripts/guardrails/check_tenant_isolation.sh docs/detailed-design/` |
| GR-005 | `scripts/guardrails/check_godoc.sh` | `bash scripts/guardrails/check_godoc.sh docs/detailed-design/` |
| GR-006 | `scripts/guardrails/check_error_wrapping.sh` | `bash scripts/guardrails/check_error_wrapping.sh docs/detailed-design/` |
| GR-007 | `scripts/guardrails/check_no_init.sh` | `bash scripts/guardrails/check_no_init.sh docs/detailed-design/` |
| GR-008 | `scripts/guardrails/check_global_state.sh` | `bash scripts/guardrails/check_global_state.sh docs/detailed-design/` |
| GR-009 | `scripts/guardrails/check_migrations.sh` | `bash scripts/guardrails/check_migrations.sh docs/detailed-design/` |
| GR-010 | `scripts/guardrails/check_cycles.sh` | `bash scripts/guardrails/check_cycles.sh docs/detailed-design/` |
| GR-012 | `scripts/guardrails/no-core-nats.sh` | `bash scripts/guardrails/no-core-nats.sh src/` |
| GR-013 | `scripts/guardrails/stream-per-service.sh` | `bash scripts/guardrails/stream-per-service.sh src/services/` |
| GR-021 | `scripts/guardrails/msgpack-nats-check.sh` | `bash scripts/guardrails/msgpack-nats-check.sh src/` |
| GR-014 | `scripts/guardrails/frontend/frontend-existence-check.sh` | `bash scripts/guardrails/frontend/frontend-existence-check.sh` |
| GR-015 | `scripts/guardrails/frontend/api-contract-alignment-check.sh` | `bash scripts/guardrails/frontend/api-contract-alignment-check.sh` |
| GR-016 | `scripts/guardrails/frontend/frontend-null-safety-check.sh` | `bash scripts/guardrails/frontend/frontend-null-safety-check.sh` |
| GR-017 | `scripts/guardrails/frontend/api-envelope-check.sh` | `bash scripts/guardrails/frontend/api-envelope-check.sh` |

| GR-022 | `scripts/guardrails/security-headers-gate.sh` | `bash scripts/guardrails/security-headers-gate.sh src/gateway/` |
| GR-023 | `scripts/guardrails/pg-image-check.sh` | `bash scripts/guardrails/pg-image-check.sh src/tests/` |
| GR-024 | `scripts/guardrails/time-sleep-ban.sh` | `bash scripts/guardrails/time-sleep-ban.sh src/` |

All scripts accept a directory path as the first argument and exit with code 0 (PASS) or 1 (FAIL). Output is one finding per line in the format: `FAIL: <file>:<line> <description>`.

---

### GR-022: Security Headers Gate

**What to look for:** The API Gateway MUST include security headers middleware (X-Content-Type-Options, X-Frame-Options, CSP, HSTS, Referrer-Policy). Missing security headers was P0 defect DEF-001 in the testing phase.

**PASS criteria:**
- At least one `.go` file in `src/gateway/` contains `X-Content-Type-Options`
- SecurityHeaders middleware exists and sets all required headers

**FAIL criteria:**
- Zero matches for `X-Content-Type-Options` in `src/gateway/` Go files

**Severity:** BLOCKER

**Auto-fix suggestion:** Create `src/gateway/internal/adapters/http/security_middleware.go` with SecurityHeaders middleware. Wire it in `router.go` (ADD-ONLY).

**Script:** `scripts/guardrails/security-headers-gate.sh`

```bash
#!/usr/bin/env bash
# GR-022: Verify API Gateway includes security headers
set -euo pipefail
DIR="${1:-src/gateway/}"
if grep -rn 'X-Content-Type-Options' "$DIR" --include="*.go" >/dev/null 2>&1; then
  echo "PASS: Security headers found in gateway code"
  exit 0
else
  echo "FAIL: No X-Content-Type-Options header found in $DIR — security headers middleware is missing (DEF-001)"
  exit 1
fi
```

---

### GR-023: PostgreSQL Image Gate

**What to look for:** Test containers MUST use `duckdb/duckdb:latest` for PostgreSQL. The pg_duckdb extension is not available on standard `postgres:XX` images. This was BLOCKER TS-001 in the testing phase.

**PASS criteria:**
- Zero matches for `postgres:` (without `duckdb`) in test Go files

**FAIL criteria:**
- Any test file references a `postgres:` image that is not `duckdb/duckdb:latest`

**Severity:** BLOCKER

**Auto-fix suggestion:** Replace `postgres:16`, `postgres:18`, or any `postgres:XX` image string with `duckdb/duckdb:latest`.

**Script:** `scripts/guardrails/pg-image-check.sh`

```bash
#!/usr/bin/env bash
# GR-023: Verify test containers use duckdb/duckdb:latest, not postgres:XX
set -euo pipefail
DIR="${1:-src/tests/}"
MATCHES=$(grep -rn 'postgres:' "$DIR" --include="*.go" 2>/dev/null | grep -v 'duckdb' | grep -v '_test.go:.*// allowed' || true)
if [ -z "$MATCHES" ]; then
  echo "PASS: No postgres:XX image references found in test code"
  exit 0
else
  echo "$MATCHES" | while IFS= read -r line; do
    echo "FAIL: $line — use duckdb/duckdb:latest instead of postgres:XX (TS-001)"
  done
  exit 1
fi
```

---

### GR-024: time.Sleep Ban in Tests

**What to look for:** `time.Sleep` usage in test files. Tests should use `assert.Eventually` or `require.Eventually` with polling instead of sleeping. This was HIGH finding TS-002 in the testing phase.

**PASS criteria:**
- Zero `time.Sleep` calls in `*_test.go` files

**FAIL criteria:**
- Any `time.Sleep` found in test files

**Severity:** WARNING

**Auto-fix suggestion:** Replace `time.Sleep(duration)` followed by assertion with `require.Eventually(t, func() bool { return <condition> }, timeout, pollInterval)`.

**Script:** `scripts/guardrails/time-sleep-ban.sh`

```bash
#!/usr/bin/env bash
# GR-024: Flag time.Sleep usage in test files
set -euo pipefail
DIR="${1:-src/}"
FAIL=0
while IFS= read -r match; do
  if [ -n "$match" ]; then
    echo "WARNING: $match — use assert.Eventually or require.Eventually instead of time.Sleep (TS-002)"
    FAIL=1
  fi
done < <(grep -rn 'time\.Sleep' "$DIR" --include="*_test.go" 2>/dev/null || true)
if [ "$FAIL" -eq 0 ]; then
  echo "PASS: No time.Sleep found in test files"
  exit 0
else
  exit 1
fi
```

### Rule #15 Frontend Guardrails (BLOCKING)

Added after run `cce7be05` where the implementation-lead skipped all frontend waves, leading to 8 production bugs. These guardrails are BLOCKER severity — the phase CANNOT complete if any fail.

| ID | Name | Severity | What it Catches |
|----|------|----------|-----------------|
| GR-014 | Frontend Existence | BLOCKER | Frontend designs exist but code/tests missing |
| GR-015 | API Contract Alignment | BLOCKER | handleResponse doesn't unwrap envelope, hardcoded URLs, localStorage tokens |
| GR-016 | Frontend Null Safety | BLOCKER | `.length`/`.map()` on undefined without `??` or `?.` guard |
| GR-017 | API Envelope | WARNING | Double-unwrapping `data?.data`, raw `<a href>` for SPA navigation |

### Rule #16 Story-Level Completion Guardrails (BLOCKING)

Added after run `cce7be05` where EP-FND-07 (Account & Branding) had complete design specs for 8 stories but implementation covered only 3. Logo upload, color picker, locale detection, and locale application were entirely missing. No pipeline stage flagged the gap because guardrails checked aggregate metrics (compile, test count) not per-story completeness.

| ID | Name | Severity | What it Catches |
|----|------|----------|-----------------|
| GR-018 | Story Completion | BLOCKER | Stories in plan that are missing backend handlers, frontend components, or tests |
| GR-019 | Design-Impl Traceability | BLOCKER | Story design specs that have no matching implementation artifacts |
| GR-020 | Contract-Handler Coverage | BLOCKER | NATS subjects in contracts/routes with no registered handler (catches "missing" not just "stubbed") |

| ID | Script | Command |
|----|--------|---------|
| GR-018 | `scripts/guardrails/implementation/story-completion-check.sh` | `bash scripts/guardrails/implementation/story-completion-check.sh .` |
| GR-019 | `scripts/guardrails/implementation/design-impl-traceability-check.sh` | `bash scripts/guardrails/implementation/design-impl-traceability-check.sh .` |
| GR-020 | `scripts/guardrails/implementation/contract-handler-coverage-check.sh` | `bash scripts/guardrails/implementation/contract-handler-coverage-check.sh .` |

## Examples

### GOOD

```yaml
guardrail_report:
  run_id: "f47ac10b-58cc-4372-a567-0e02b2c3d479"
  timestamp: "2026-03-09T18:00:00Z"
  agent: "guardrail-validator"
  summary:
    total_checks: 13
    passed: 13
    failed: 0
    blockers: 0
    warnings: 0
  checks:
    - id: GR-001
      name: "Go Naming Conventions"
      severity: WARNING
      status: PASS
      findings: []
    - id: GR-002
      name: "TenantID Presence"
      severity: BLOCKER
      status: PASS
      findings: []
    # ... all 13 checks with status PASS
  verdict: PASS
  verdict_rule: "All checks passed."
```

### BAD

```yaml
guardrail_report:
  checks:
    - id: GR-002
      status: FAIL
  verdict: PASS
```

Why it is wrong: A BLOCKER check (GR-002) has status FAIL, but the verdict is PASS. When any BLOCKER fails, the verdict must be BLOCK. Also, the report is missing run_id, timestamp, summary counts, finding details, and 12 of 13 checks.

### BAD

```yaml
guardrail_report:
  summary:
    total_checks: 5
  checks:
    - id: GR-001
    - id: GR-003
    - id: GR-005
    - id: GR-007
    - id: GR-009
  verdict: PASS
```

Why it is wrong: Only 5 of 13 checks were run. All 13 guardrail checks are mandatory. Skipping checks does not mean they pass.

## Common Mistakes

1. **Running only a subset of checks** -- All 13 guardrail checks must be executed on every validation pass. Skipping checks because "they probably pass" masks regressions. The report must show all 13 checks with explicit PASS/FAIL status.

2. **Classifying GR-002 (TenantID) as WARNING instead of BLOCKER** -- Missing TenantID in a domain struct breaks multi-tenancy at the application layer. This is always a BLOCKER because downstream connection routing, NATS subjects, and logging depend on it.

3. **Ignoring the auto-fix suggestion** -- Each FAIL finding includes an auto-fix suggestion. The guardrail-validator should include these in the report so the owning agent can apply the fix without re-analysis.

4. **Not mapping findings to owning agents** -- Each finding should reference the agent whose output contains the violation, so the detailed-design-lead can route fixes to the correct agent.

5. **Treating an empty .down.sql as a PASS for GR-009** -- A down migration file that exists but contains no SQL statements is functionally equivalent to a missing file. Both are FAIL conditions.

6. **Missing the schema isolation check in GR-004** -- Verifying that repositories use `AcquireForTenant()` with `SET search_path` on each acquired connection from the shared app-database pool. Without this check, tenant data could be written to the wrong schema.

7. **Allowing core NATS API usage (GR-012)** -- Any `nc.Publish`, `nc.Subscribe`, `nc.Request`, or `msg.Respond` call bypasses JetStream persistence, acknowledgment, and deduplication. These are always BLOCKERS because messages can be silently lost when no subscriber is listening, and request-reply creates ephemeral inbox subjects outside JetStream.

8. **Not verifying stream bootstrap per service (GR-013)** -- Every service must call `EnsureStream` at startup. Without this, publishes and subscribes fail silently or target the wrong stream. The stream name must match the UPPER_SNAKE_CASE convention, and subjects must include both domain and reply patterns.

9. **Allowing encoding/json in NATS adapter code (GR-021)** -- MsgPack is the sole wire format for all inter-service NATS communication. `encoding/json` in NATS handlers/publishers silently produces JSON payloads that other services cannot deserialize with `msgpack.Unmarshal`. JSON is only permitted for external APIs (OPA, Cognito) and config files. This is always a BLOCKER because mixed JSON/MsgPack payloads cause silent deserialization failures across services.

## GR-011: No Inter-Service HTTP Imports (Communication Guardrail)

**What to look for:** Domain service code (not API Gateway) importing `net/http` for inter-service communication, or any HTTP client usage for calling other internal services.

**PASS criteria:**
- Domain services use NATS adapters (`adapters/inbound/nats/`, `adapters/outbound/nats/`) for inter-service communication
- No `net/http` imports in domain service outbound adapters (except API Gateway)
- No `http.Client` usage for calling internal services
- All inter-service query patterns use NATS request-reply

**FAIL criteria:**
- Domain service outbound adapter imports `net/http` for inter-service calls
- `http.Client` or `http.Get`/`http.Post` used to call another internal service
- `google.golang.org/grpc` imported anywhere (gRPC is not used in this platform)

**Severity:** BLOCKER

**Auto-fix suggestion:** Replace HTTP client calls with NATS request-reply via the `ServiceQuerier` port interface. Replace gRPC stubs with NATS request-reply responders.

```bash
#!/usr/bin/env bash
# Verify no inter-service HTTP imports in domain services
for svc in $(find "$1" -path "*/services/*" -name "*.go" ! -path "*/api-gateway/*"); do
  if grep -Pn 'net/http' "$svc" | grep -v '_test.go' | grep -v 'healthz'; then
    echo "FAIL: $svc imports net/http (only API Gateway may use HTTP for business endpoints)"
  fi
done
# Verify no gRPC imports anywhere
grep -rPn 'google.golang.org/grpc' "$1" --include="*.go" && echo "FAIL: gRPC import detected (use NATS instead)"
```

---

## GR-021: MsgPack-Only NATS Payloads (Communication Guardrail)

**What to look for:** `encoding/json` usage in NATS adapter code. **MsgPack is the SOLE wire format for ALL inter-service NATS communication.** `encoding/json` is FORBIDDEN for NATS payloads. JSON is permitted ONLY for external API integrations (OPA, Cognito), config file parsing, and the API Gateway's HTTP response serialization.

**PASS criteria:**
- Zero `encoding/json` imports in `src/services/*/internal/adapters/nats/` directories
- All NATS handler files use `msgpack.Unmarshal` for request deserialization
- All NATS publisher files use `msgpack.Marshal` for message serialization
- `json.Marshal`/`json.Unmarshal` not used anywhere in NATS adapter code
- `encoding/json` imports in `src/gateway/` for HTTP response serialization are acceptable
- `encoding/json` imports for OPA/Cognito external API integration are acceptable

**FAIL criteria:**
- `encoding/json` imported in any file under `src/services/*/internal/adapters/nats/`
- `json.Marshal` or `json.Unmarshal` called in any NATS handler or publisher
- `json.NewDecoder` or `json.NewEncoder` used for NATS message processing
- NATS message `Data` field populated with JSON-encoded bytes

**Severity:** BLOCKER

**Auto-fix suggestion:** Replace `encoding/json` import with `github.com/vmihailenco/msgpack/v5`. Replace `json.Marshal(v)` with `msgpack.Marshal(v)`. Replace `json.Unmarshal(data, &v)` with `msgpack.Unmarshal(data, &v)`. Ensure struct tags include `msgpack:"field_name"` alongside existing tags.

**Script:** `scripts/guardrails/msgpack-nats-check.sh`

```bash
#!/usr/bin/env bash
# GR-021: Verify MsgPack-only NATS payloads — encoding/json is FORBIDDEN in NATS adapter code
# MsgPack is the sole wire format for all inter-service communication.
# JSON is permitted ONLY for: external APIs (OPA, Cognito), config files, API Gateway HTTP responses.
set -euo pipefail

DIR="${1:-src/}"
FAIL=0

# Check 1: encoding/json in NATS adapter directories (FORBIDDEN)
while IFS= read -r match; do
  if [ -n "$match" ]; then
    echo "FAIL: $match — encoding/json import in NATS adapter (use msgpack instead)"
    FAIL=1
  fi
done < <(grep -rn '"encoding/json"' "$DIR" --include="*.go" 2>/dev/null | \
  grep -E '/adapters/nats/|/adapters/inbound/nats/|/adapters/outbound/nats/' | \
  grep -v '_test.go' || true)

# Check 2: json.Marshal/json.Unmarshal in NATS adapter code (FORBIDDEN)
while IFS= read -r match; do
  if [ -n "$match" ]; then
    echo "FAIL: $match — json.Marshal/Unmarshal in NATS adapter (use msgpack.Marshal/Unmarshal)"
    FAIL=1
  fi
done < <(grep -rPn 'json\.(Marshal|Unmarshal|NewDecoder|NewEncoder)' "$DIR" --include="*.go" 2>/dev/null | \
  grep -E '/adapters/nats/|/adapters/inbound/nats/|/adapters/outbound/nats/' | \
  grep -v '_test.go' || true)

# Check 3: Verify NATS handlers use msgpack (positive check — WARNING if missing)
NATS_HANDLER_COUNT=0
MSGPACK_HANDLER_COUNT=0
while IFS= read -r handler_file; do
  if [ -n "$handler_file" ]; then
    NATS_HANDLER_COUNT=$((NATS_HANDLER_COUNT + 1))
    if grep -q 'msgpack' "$handler_file" 2>/dev/null; then
      MSGPACK_HANDLER_COUNT=$((MSGPACK_HANDLER_COUNT + 1))
    else
      echo "FAIL: $handler_file — NATS handler does not use msgpack for message serialization"
      FAIL=1
    fi
  fi
done < <(find "$DIR" -path "*/adapters/nats/*_handler.go" -o -path "*/adapters/inbound/nats/*_handler.go" 2>/dev/null || true)

# Check 4: Verify NATS publishers use msgpack (positive check — WARNING if missing)
while IFS= read -r publisher_file; do
  if [ -n "$publisher_file" ]; then
    if ! grep -q 'msgpack' "$publisher_file" 2>/dev/null; then
      echo "FAIL: $publisher_file — NATS publisher does not use msgpack for message serialization"
      FAIL=1
    fi
  fi
done < <(find "$DIR" -path "*/adapters/nats/*_publisher.go" -o -path "*/adapters/outbound/nats/*_publisher.go" 2>/dev/null || true)

if [ "$FAIL" -eq 0 ]; then
  echo "PASS: All NATS adapter code uses MsgPack exclusively (no encoding/json)"
  exit 0
else
  exit 1
fi
```
