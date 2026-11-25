---
name: blast-radius
description: "Project-grounded blast-radius tracing for code changes, PRs, diffs, files, symbols, or bugfixes, especially in Helpdesk-style repos. Use before editing, committing, merging, or reviewing when downstream callers, tests, routes, SQL, configs, schema, auth/tenant boundaries, external integrations, sibling bugs, or review-derived trap replays could be affected."
---

# Blast Radius

A change is a stone dropped in a pond. The skill traces every ripple — and stops the next whack-a-mole bug
before it lands in production.

## Scope and Strength

This skill combines a generic blast-radius workflow with Helpdesk-specific production bug patterns.
Use the generic workflow in any repo. Apply Helpdesk-specific rules when the repo has matching
conventions: real-DB-only tests, tenant isolation, route mounting rules, schema authority files, and
the named patterns in `references/bug-patterns.md`.

Do not soften a finding because a rule feels project-specific. If a local convention does not apply,
mark that check `NOT APPLICABLE` with evidence.

## The Rule

**You cannot ship a change you have not traced.** If you can't list what it touches, list the assumptions
each touchpoint makes about it, and prove each assumption still holds — you don't know whether the change
is safe. You're guessing.

This skill produces mode-aware artifacts so the user can both *read* the analysis and *act* on it:

1. **Report** — full structured Markdown, saved to `docs/blast-radius/<change-name>.md` (or
   `$CLAUDE_JOB_DIR` if no docs dir convention applies)
2. **Risk-ranked checklist** — CRITICAL/HIGH/MEDIUM/LOW touchpoints with file:line, why each could
   break, and the verification step
3. **Inline diff annotations** — for diff-bearing modes, annotate the diff with downstream effects per hunk

| Mode | Report | Checklist | Inline annotations |
|---|---|---|---|
| **Plan** | YES | YES | NO unless a diff exists |
| **Pre-commit** | YES | YES | YES |
| **Review** | YES | YES | YES |
| **Post-fix** | YES | YES | NO unless reviewing the fix diff |
| **Lite speed** | Compact report is allowed inline | YES | YES only if a diff exists |

If an artifact is not applicable, say why in `## Trace Boundaries`. Do not skip the verdict,
finding counts, verification plan, or any mandatory check.

## Artifact write safety

Before creating files, check the active route/worktree rules. In guarded repos, write artifacts only
where editing is allowed. If artifact writes are blocked, emit the report/checklist inline or write to
an approved job scratch directory such as `$CLAUDE_JOB_DIR`, and state that repo artifact writes were
skipped. Do not turn a blocked artifact write into a weaker analysis.

## Speed modes — pick by diff size

The full trace can take 10+ minutes on a real codebase. Don't apply that to a one-line change.
Auto-select the speed mode from the change set size:

| Mode | When to pick | What changes |
|---|---|---|
| **Lite** | ≤ 5 files changed, no migration, no auth/middleware change, no rename | Run mandatory core patterns 1, 2, 3, 13 plus any conditional mandatory patterns that apply. Direct callers (1 hop). Compact report/checklist. Target: 2–3 min. |
| **Standard** | 6–20 files, OR any DB change, OR any new route | Full Step 1–7 below. 2-hop fan-out with smart stops. All applicable patterns. All applicable output artifacts. Target: 5–10 min. |
| **Deep** | >20 files, OR auth/tenant/middleware change, OR cross-system integration change, OR explicit `--deep` from user | Full sweep + cross-repo trace (admin, partners) + all mandatory patterns from `bug-patterns.md`. Target: 10–20 min. |

When the user explicitly names a mode ("lite blast-radius on this", "deep trace") use that. Otherwise
classify by counting files in the change set: `git diff --stat <base>...HEAD | tail -1` gives a quick
count.

State the chosen mode at the top of the report so the user knows what was traced.

## When this skill runs

Four entry modes. Detect mode from context — don't ask if it's obvious from the request.

| Mode | Trigger | Input |
|---|---|---|
| **Plan** | "I want to change X" / written plan / proposed migration | A description, a plan doc, or a target symbol/file |
| **Pre-commit** | Uncommitted diff in working tree | `git diff` against HEAD |
| **Review** | Branch, PR, file, or caller targeted for review | `git diff <base>...HEAD`, a PR number, a file path, or a symbol name |
| **Post-fix** | Just landed a bugfix | The fix commit + the original bug description |

Post-fix mode is different from the others: it ALSO does a **sibling-bug hunt** — finds other code with
the same shape as the bug that was just fixed.

The user can supply input in several forms: a **PR number** (`#856`), a **file path** ("trace
`apps/api/src/services/foo.js`"), a **specific function/caller** ("blast radius of
`orderRouteService.getRoute`"), a **diff** (current working tree, or a branch), or just a **plain
description**. See Step 1 for how to handle each.

## Step 1 — Identify the change set

Don't trace what you haven't named. Make the change set explicit before fanning out.

The skill accepts several input forms — match the user's input to the right one and proceed:

| Input form | How the user phrases it | What to do |
|---|---|---|
| **PR number** | "blast radius on PR 856", "trace #1234" | `gh pr diff <num>` for the diff; `gh pr view <num> --json title,body,headRefName,baseRefName` for context |
| **Diff (uncommitted)** | "what's the blast radius of my current changes", "check my diff" | `git diff` (working tree) and `git diff --staged` |
| **Branch / commit range** | "trace this branch", "review changes since main" | `git diff <base>...HEAD`, then `git log --oneline <base>..HEAD` |
| **Specific file** | "trace apps/api/src/services/foo.js", "what depends on this file" | Treat the whole file as the change set; `cortex_outline` the file, then trace each exported symbol |
| **Specific symbol / caller** | "blast radius of `orderRouteService.getRoute`", "what calls this function" | Start from the symbol — `cortex_find_references` and trace each call site |
| **Written plan / description** | "I want to add a `deleted_at` column to products" | Extract proposed changes from prose; if vague, STOP and ask for concrete changes |
| **Post-fix sweep** | "I just fixed X, find similar bugs" | The fix commit + the original bug description; pattern-hunt for siblings (see Step 5) |

For PR mode specifically:

```bash
gh pr diff <num>                                          # the full diff
gh pr view <num> --json title,body,headRefName,baseRefName,files  # metadata + file list
gh pr view <num> --json reviewDecision,statusCheckRollup  # current review state (useful context)
```

Also capture the live PR review-thread state at the start of the trace and again immediately before
the final verdict. GitHub GraphQL `reviewThreads.nodes[].isResolved` is the source of truth for
unresolved conversations; REST comments can look open after a thread is resolved, and local proof can
look complete while new review threads are open. Use the PR review-thread query in
`references/trace-recipes.md`.

Build a **review feedback trap bank** before the trace. Search current PR threads, earlier
blast-radius/prove-it artifacts for the touched domain, and recent resolved Cursor/Copilot/human
comments when available. Extract the invariant class behind each valid finding, not just the literal
line comment. If the current change touches that invariant class, replay it in Step 5.5 with proof or
mark it `NOT APPLICABLE` with source evidence.

When a valid PR conversation appears after a PR was already claimed locally proven, classify it as a
`Local Proof Miss` if a focused local test, canary, schema check, import-cycle check, or browser/API/DB
workflow should reasonably have caught it. The closeout is not only fixing the line: add the local
regression/proof that catches the invariant and update the responsible skill/runbook with the new trap
class or command recipe. If the skill/runbook cannot be updated because a gate blocks it, record the
blocker in the report and keep the merge/readiness verdict blocked unless Ben explicitly accepts the
exception.

If `headRefOid` changes after you started tracing, rerun the trace against the new head. Do not carry
forward a verdict from an older SHA.

For symbol / caller mode, the change set is the symbol's call graph rather than a diff:
- Start: the symbol itself
- Fan out: all references, all importers, all tests, all routes that hit it
- Live DB verification still applies if the symbol touches DB

For file mode, treat every exported symbol as a change set item, plus any internal DB queries. A
"trace the whole file" request is usually "what would change if I rewrote this file".

Write the resolved change set to the report's `## Change Set` section. List both the *input form*
the user gave and the *resolved items* you fanned out from. This is the working list everything
else flows from.

## Step 2 — Classify the change type (adaptive depth)

The trace depth and pattern depend on what kind of change it is. Don't trace a util function the same
way you trace a schema migration. Read **`references/change-types.md`** for the full taxonomy, but the
core categories are:

- **Database schema** (migration, column add/remove/rename/type) → trace all reads/writes of affected
  columns. ALWAYS verify the live schema against what the code assumes.
- **API route** (path, method, request/response shape, status codes) → trace all clients
- **Service method signature** → trace all direct callers + mocks + re-exports
- **Validation / business logic** → trace SIBLING code paths doing similar validation (this is the
  whack-a-mole killer)
- **DB-backed guard / idempotency / duplicate prevention** → build a falsification matrix for identity
  sources, active vs cancelled rows, all writers to the same table, and concurrent attempts
- **Async / queue / worker / scheduled job** → prove atomic claim, duplicate scheduler/worker behavior,
  stale running recovery, retry policy, post-commit bookkeeping failures, and idempotent side effects
- **Cross-layer DTO / projection / print payload / notification shape** → build a field-level matrix from
  producer field names through route/service/DB/worker/read-model/UI consumers; aliases must match runtime source
- **Order / invoice / inventory / pricing / label-printing** → treat field mismatches, retries, unavailable
  downstream services, and UI rehydration as data-integrity risks, not UX polish
- **Synchronous route converted to async/queued work** → enumerate every validation, confirmation, and
  recoverable error returned by the old synchronous path. Prove each still happens before enqueue, or prove
  the product deliberately accepts background failure instead of staff choice.
- **Irreversible side effect plus bookkeeping/projection** → identify the commit point, then prove failures
  after that point cannot mark the committed operation as uncommitted, failed, or safely retryable.
- **Helper return variants / truthy result handling** → enumerate every return variant. Prove dedupe, locks,
  notifications, and retry suppression happen only for real success, not for unavailable/cancelled/skipped results.
- **SQL type / range cast / parser boundary** → prove casts cannot throw or de-index the hot path. Guard
  malformed, out-of-range, empty, and wrong-type values before casting, and verify predicates still use the intended indexes.
- **Mode flag / reason-set / conditional branch** → every new flag, branch, reason string, or structured code
  path needs on/off and sibling-reason coverage, including idempotent repeat behavior and parameter ordering.
- **Proof lane / live-proof registry / verification command** → prove the selected lane is the right one,
  cannot be stolen by generic file matches, and fails non-zero when the runtime condition it claims to verify is absent.
- **Evidence artifact / PR readiness artifact** → verify artifacts are current-head, portable, and internally
  consistent; stale "pending" checklists, "create PR" leftovers inside an opened PR, or machine-specific command
  prefixes are findings.
- **Audit/log/redaction shape** → prove optional audit fields use stable explicit values instead of literal
  `undefined`/omitted JSON drift where traceability depends on them, and prove secrets are redacted in both
  structured objects and serialized text forms such as quoted JSON headers (`"x-api-key":"secret"`).
- **Parser / numeric extraction shape** → regex-based parsers must reject partial matches, punctuation-only
  values, multiple decimals, `NaN`, and infinite values before returning business objects or amounts.
- **Config / env var / feature flag** → trace all readers + deployment configs + docs
- **Auth / permission / multi-tenancy** → trace ALL routes that share the boundary
- **Type / interface** → trace all usages + JSON schemas + external consumers
- **Refactor (rename / move)** → trace static imports AND dynamic require/import-string usages
- **Test** → trace what it covers + similar tests that should have caught this

A change can be multiple types. Run each applicable trace.

**Depth heuristic** — 2 hops with smart stops:
- Stop at module public boundaries (an exported interface that's stable)
- Stop at unrelated domain boundaries (don't follow `fs.readFile` into the Node stdlib)
- Always continue across cross-cutting concerns (auth, tenant, transactions, queues) even if "2 hops"
- For database changes, always trace until you hit every SQL string referencing the affected column

## Step 3 — Fan out the trace

**Pattern-library first**: for each item in the change set, walk **`references/bug-patterns.md`**
and run the recipes for the patterns that apply. The applicability heuristic (at the bottom of
that file) tells you which patterns to scan based on the change type. This is faster and more
accurate than deriving recipes from scratch — these are the specific bug shapes this codebase
actually has.

Core patterns are MANDATORY for every change regardless of type. If a pattern truly does not apply,
record it as `NOT APPLICABLE` with evidence rather than silently skipping it:

- **Pattern 1 (tenant-scope leak)** — for every function in the radius that touches the DB
  directly or transitively, confirm tenant scoping. Don't restrict Pattern 1 to "tenant-related
  changes" — tenant leaks happen most often in functions nobody thought were tenant-related.
- **Pattern 2 (mock policy)** — every test in the radius using `jest.mock(...config/database)`,
  `jest.mock('pg')`, or an in-memory DB fake is HIGH risk regardless of whether the mocked
  symbols exist. Per CLAUDE.md the project's standing rule is real-DB-only.
- **Pattern 3 (schema drift)** — for every DB-touching file, SQL string, migration/schema edit, or test
  asserting DB shape in the radius, compare referenced columns against live DB or mark live verification
  blocked. Do not trust code, migrations, or types as runtime truth.
- **Pattern 13 (deleted secret files)** — every diff or PR must be scanned for deletions of
  `.env`, `credentials.*`, `*.pem`, secret JSON files. Even when removed from the working tree
  they remain in git history and every credential they contained must be rotated. This is
  CRITICAL, not LOW — leaked secrets are an immediate incident.

For DB-backed validation, identity matching, idempotency, duplicate guards, soft-delete filters,
changed `WHERE` predicates, async/worker changes, cross-layer DTO/projection changes, or
order/invoice/inventory/pricing/label-printing changes, the PR-adversarial patterns are also mandatory:

- **Pattern 15 (identity fallback mismatch)** — when a guard can match by ID, name, email, SKU, invoice
  number, PO id, or any fallback identity, test old-row/new-row combinations where one side has the ID
  and the other only has an alias/name. A guard that works for `supplier_rex_id` but misses historical
  `supplier_name` rows is still incomplete.
- **Pattern 16 (predicate/index drift)** — compare every changed SQL predicate against live indexes.
  Wrapping an indexed column in a new function (`LOWER(col)` → `LOWER(TRIM(col))`) can turn a guard or
  lookup into a scan. Repeated drift across sibling lookups is a finding, not a footnote.
- **Pattern 17 (schema authority disagreement)** — live DB is the source of runtime truth, but committed
  migrations, canonical schema files, and docs are contract truth. If they disagree, record the drift and
  classify the risk; do not let "live DB passed" erase a broken committed schema contract.
- **Pattern 18 (open PR review threads)** — in PR mode, unresolved GitHub review threads are findings.
  If reviewers already found a counterexample, blast-radius must ingest it or explicitly report it as
  unresolved.
- **Pattern 19 (async claim/retry integrity)** — queue, worker, scheduler, and background job changes must
  prove atomic row/job claim, duplicate scheduler behavior, stale running recovery, retry limits, and
  post-commit bookkeeping failure semantics. Missing proof on a state-mutating async path is HIGH risk.
- **Pattern 20 (field-level runtime contract)** — every cross-layer payload/projection must map actual
  runtime field names and aliases from producer to consumer. This is exact-spelling work: compare frontend
  payload builders/tests, route inputs, service mappers, DB JSON, worker inputs, read models, print payloads,
  notifications, and UI consumers for every quantity, ID, status, and intent field. Run a field-spelling
  collision scan: list producer keys and mapper/consumer keys side-by-side, then search for near-miss aliases
  with the same words in different order or shape (`quantityReceived` vs `receivedQuantity`, `productId` vs
  `retailExpressProductId`, snake_case vs camelCase). If the mapper does not read the exact key produced by
  the real caller, or the only proof uses a mock/fixture shape, classify it HIGH. A mock, fixture, or
  hard-coded response that bypasses the changed producer is HIGH risk unless a separate real-boundary proof
  covers the same fields.
- **Pattern 21 (operator retry/reopen path)** — UI workflows around invoices, receiving, labels, printing,
  or other staff operations must prove close/reopen/refresh rehydration plus unavailable/cancelled/retry
  behavior. Transient frontend-only state is HIGH risk when the backend is the lock source.
- **Pattern 22 (sync-confirmation preservation before async enqueue)** — when an endpoint queues work before
  the old synchronous service call, enumerate old confirmation/error outcomes from the skipped call path
  and prove recoverable staff choices still return before `202 Accepted`. Turning a recoverable confirmation
  into a later background failure is HIGH risk.
- **Pattern 23 (commit-boundary bookkeeping split)** — for stock, money, invoice, pricing, sync, or other
  irreversible side effects, identify the first committed write/API call and inspect the try/catch boundary.
  Bookkeeping, projection, notification, or status-update failures after commit must not record the whole
  operation as failed/uncommitted or safely retryable. Missing proof is HIGH risk.
- **Pattern 24 (return-variant success semantics)** — for printing, notifications, sync helpers, quick actions,
  and integrations, enumerate return variants such as success, unavailable, skipped, cancelled, no-op, and
  error. Truthy objects are not success. Dedupe keys, locks, retry suppression, and success notifications
  must be gated by the success discriminant only.
- **Pattern 25 (conditional branch / reason-set coverage)** — every added mode flag, behavior branch, error code,
  status, reason string, or structured result path must have positive and negative proof. Reason filters must cover
  all sibling reasons that the business process expects to recover, not only the first literal string found. SQL
  branch tests must prove placeholder ordering and idempotent repeat behavior.
- **Pattern 26 (type/range cast safety)** — any SQL or parser cast from JSON/text/external payload data must prove
  empty, malformed, and out-of-range values cannot throw the whole query/job. Any cast on an indexed column must
  prove the predicate stays indexable or record a performance finding.
- **Pattern 27 (proof-lane integrity)** — live-proof registries, command selectors, CI mirrors, and route/file
  matchers must prove they select the domain-specific lane for mixed diffs and fail non-zero when their asserted
  runtime resource, table, route, worker, browser state, or downstream artifact is missing. A command that exits 0
  for an empty result set is false proof.
- **Pattern 28 (artifact truth and portability)** — verification, review, blast-radius, and PR-readiness artifacts
  must describe the current state of the PR and use portable commands. Machine-local PATH/NODE_PATH prefixes,
  stale "pending" sections, stale "create PR" tasks inside an already-open PR, contradictory gate status, or
  evidence from the wrong head/base are findings.
- **Pattern 29 (runtime-to-proof parity)** — verifier, replay, backtest, report, and live-proof code must use the
  same helpers or prove equivalent predicates, inputs, and truth conditions as production runtime code.
- **Pattern 30 (integration fault and idempotency matrix)** — external clients must prove fallback criteria,
  timeout/cancellation behavior, idempotent retry boundaries, sanitized errors, and duplicate-side-effect prevention.
- **Pattern 31 (boundary, identifier, and omitted-field invariants)** — tenant, supplier, owner, affected-row,
  identifier-shape, default-change, and omitted-field/upsert behavior must be locked from real source and tests.
- **Pattern 32 (observability and redaction contract)** — log/error changes must prove adversarial message, stack,
  non-object, cookie/token/header, and live-identifier redaction while preserving useful diagnostic shape.
- **Pattern 33 (public seam, UI, and accessibility contract)** — export/startup seams, API client keys, UI lock
  rehydration, nested-route specificity, and custom listbox/combobox keyboard/focus behavior must be proven.
- **Pattern 34 (test-integrity false confidence)** — schema-coupled DB mocks, source-string-only assertions,
  leaked test env, brittle count assertions, and non-isolated module-load tests are findings in the radius.

After the pattern sweep, use the recipes in **`references/trace-recipes.md`** for the general
fan-out (cortex_find_references, importers, route registry, etc.). Then produce the Pattern-Library
Sweep table in the report (one row per pattern with hit/miss verdict + evidence).
The recipes give the exact `cortex_find_references`, `grep`, `psql`, and `git log` invocations per
change type. Key principles:

- **Cortex-first** — `cortex_find_references` and `cortex_find_importers` before `grep`. They understand
  symbol scope and avoid false positives. Use `cortex_find_text` for string-level matches (SQL column
  names, env vars, config keys).
- **grep for strings** — column names, env vars, route paths, feature flag keys, and dynamic-require
  strings will be missed by symbol-level tools. Use `grep -rn` for these.
- **git log for history** — `git log -p -S "<symbol>"` shows who added/changed this and why, often
  surfaces assumptions baked into the original change.
- **Route registry sweep** — for auth/tenant changes, walk `apps/api/src/routes/` and group routes by
  the middleware chain they mount under.

For every touchpoint discovered, capture:
- file:line
- The assumption it makes about the changed thing ("expects `result.customer_id` to be non-null", "expects
  column `sku` to be string and unique per tenant")
- Whether that assumption still holds after the change
- Whether there's a test that would have caught a violation

## Step 4 — Verify against the live database (REQUIRED)

This step is non-negotiable for any change that touches data. The dev DB is the source of truth, not
the migration files, not the model, not the type. Mocks lie; live schema doesn't.

If `psql` is blocked, use the graceful-degradation recipe in `references/trace-recipes.md`. Do not
silently fall back to migration files. The verdict is **NEEDS REVIEW (live verification blocked)** at
minimum — never **SAFE TO PROCEED** without live schema confirmation.

For every DB-touching call in the blast radius:

1. Pull live schema for affected tables: columns, types, nullability, defaults, constraints, indexes.
2. Diff live schema against code assumptions, including cross-table type traps and join behavior.
3. Reconcile schema authorities: live DB, committed migrations, canonical bootstrap/schema files,
   code assumptions, tests, and docs. Drift is at least MEDIUM; HIGH if it can cause data loss,
   duplicate writes, runtime crashes, or reviewer-visible ambiguity.
4. Run a realistic live sample query, not just a count.
5. Check every changed predicate, lookup, join, `ON CONFLICT`, and uniqueness guard against live
   indexes/constraints.
6. Reject mocked DB tests in the radius as HIGH risk.

Write findings to the report's `## Live Schema Verification` section. Include the actual `\d` output
or column listing, code assumption, PASS/FAIL, and the exact commands from `references/trace-recipes.md`.

## Step 5 — Sibling-bug hunt (ALWAYS for validation/business-logic changes; MANDATORY post-fix)

This is the whack-a-mole killer. **Run it always when**:
- The change is in post-fix mode (you just fixed a bug)
- The change touches **validation logic** (a `WHERE` clause, status check, permission check, type
  cast, mapping table, parameter validation, schema validation)
- The change touches **business logic** (a calculation, a state transition, an enum mapping)
- The change adds or modifies a **null/undefined guard** (the same shape may exist elsewhere)
- The change involves a **rename** of a literal value (status, role, enum, config key) — see
  pattern 8 in `bug-patterns.md`

For other kinds of changes, the sweep is opportunistic — run it when the pattern is repeatable.

Sibling sweeping IS NOT optional for the change classes above. The most common production
regression in this codebase is "fixed validation in one place, missed the bulk variant / worker /
sync job." If you find the change shape, you MUST search for siblings.

1. Characterize the bug as a *pattern*, not an instance. Example:
   - Instance: "ProductEditService.updateProduct didn't include tenant_id"
   - Pattern: "UPDATE/DELETE on tenant-partitioned tables without `WHERE tenant_id = $1`"

2. Search for the pattern. Examples:
   - Tenant leak → `grep -rn "UPDATE products" apps/api/src/` then check each for `WHERE.*tenant_id`
   - Missing await → `grep -rn "asyncFn(" apps/api/src/` then check return value usage
   - Bad type cast → `grep -rn "::int" apps/api/src/` near join columns

3. Each match: read the surrounding code. Same bug? Different bug? Safe by construction (e.g. a route
   that already filters tenants upstream)? Capture all three categories in the report.

## Step 5.5 — Adversarial PR review sweep

This step exists because a trace can be locally true and still miss the counterexample a reviewer will
find five minutes later. Run it whenever the input is a PR, a rerun after previous findings, or a change
touches validation/business logic, identity matching, duplicate/idempotency guards, soft-delete filters,
or DB-backed write prevention.

Review-derived traps are first-class inputs. Replay valid current or prior Cursor/Copilot/human findings
that match the touched invariant class before inventing new edge cases. A review comment that was "fixed
once" is not closed for a new change until the current diff proves the same class cannot recur.

1. **Build a falsification matrix**. Turn the fix into a grid of ways it can be wrong. Include only axes
   that apply, but do not skip an axis just because the happy path passed:
   - identity source present vs absent (`supplier_rex_id`, name, SKU, email, PO id, external id)
   - old row has ID vs only fallback identity; new request has ID vs only fallback identity
   - alias/name/case/whitespace mismatch
   - active vs cancelled/soft-deleted/historical row
   - one row vs many rows; newest vs oldest; received vs pending state
   - single route vs existing/bulk/mixed/pending/worker writer to the same table
   - concurrent attempts, lock winner vs lock waiter
   - queued vs running vs stale running vs succeeded vs failed vs retryable state
   - pre-commit business confirmation vs background failure for recoverable staff choices
   - post-commit side effect succeeds but projection/bookkeeping/notification fails
   - printer/integration unavailable vs cancelled vs success vs retry after recovery
   - UI close/reopen/refresh while backend state remains active
   - producer field name vs consumer alias for every quantity, ID, status, and intent field
   - near-miss field spellings with the same words in different order or case, including quantity/received, ID, status, and intent variants
   - non-zero quantity and zero/falsy quantity through the real producer and mapper, not a mocked response
   - old synchronous validation/confirmation/error code vs new async enqueue response
   - recoverable staff choice before enqueue vs background failure after enqueue
   - irreversible commit succeeds but bookkeeping/projection/status/notification update fails
   - helper returns success vs unavailable vs cancelled vs skipped vs error, and which variants write dedupe/lock/retry state
   - new mode flag or reason string on vs off, plus sibling reasons that should recover the same way
   - malformed, empty, out-of-range, and wrong-type external IDs before any SQL/parser cast
   - domain-specific proof lane selected vs generic route/glue-file lane selected for mixed diffs
   - proof command asserted resource present vs absent, including empty result sets that must fail
   - verification artifact current PR/head/base vs stale pending/remaining checklist or machine-local command
   - review-derived traps: action timestamp source, UUID vs integer identity, undefined/JSON hashing,
     decline/dedupe semantics, local ID vs external ID aliases, helper unavailable/cancelled/skipped
     return variants, close/reopen rehydration, post-commit bookkeeping, and stale proof artifacts
   - runtime verifier/replay/backtest/live-proof predicate vs production helper predicate
   - external request method idempotent vs non-idempotent under timeout or transient retry
   - omitted field vs explicit null/zero/false on retry/upsert paths
   - tenant/supplier/domain identifier present vs missing vs wrong identifier family
   - log/error value as Error vs string/object, message vs stack, bearer/access/refresh/cookie/header token shape
   - custom control mouse path vs keyboard path, generic route child vs deepest/specific route child
   - source-string/mock/count-only proof vs real seam/live/runtime behavior proof
   - old behavior preserved vs intentionally changed

2. **Write the matrix into the report**. Each cell must be `PROVED`, `FAILED`, `NOT APPLICABLE`, or
   `UNTESTED`. Any `FAILED` cell is a finding. Any important `UNTESTED` cell caps the verdict at
   NEEDS REVIEW; if it is on a write path, async side effect, identity boundary, tenant/auth boundary,
   operator confirmation path, or data-integrity guard, cap at DO NOT MERGE.

3. **Simulate review comments before reviewers do**. Ask: "What would Copilot or a strict reviewer object
   to in this diff?" Explicitly scan for false positives, false negatives, performance regression,
   missing DB backstop, stale schema contracts, unsafe casts, proof-lane collisions, non-failing
   proof commands, stale/non-portable evidence artifacts, and tests that prove only the happy-path shape.

4. **Close previous findings mechanically on reruns**. If this is a rerun after an earlier blast-radius
   report, create a `## Finding Closure Ledger`:
   - previous finding ID / severity
   - exact fix
   - exact proof command/query
   - residual risk
   - reviewer-style counterexample tried

   Do not write "now covered" unless the counterexample that created the finding has a direct proof.

5. **Ingest live review threads**. In PR mode, query GitHub review threads at the end and summarize every
   unresolved thread by file:line, author, and risk theme. If an unresolved thread names a plausible bug,
   include it as a finding even if your local trace did not discover it independently.

## Step 6 — Risk-rank and write the outputs

Score each touchpoint:
- **CRITICAL** — deleted secret files, credential exposure in git history, confirmed live secret leak,
  or any finding that requires immediate incident handling.
- **HIGH** — production data loss, tenant leak, auth bypass, cross-system sync break, mocked test
  hiding the issue, schema drift between code and live DB, unresolved PR thread naming a plausible data
  integrity bug, or important falsification-matrix failure
- **MEDIUM** — caller compiles but behavior differs (silently wrong totals, missing field in response,
  default param drift), missing test coverage, sibling code with the same bug, predicate/index drift, or
  schema-authority disagreement that is not immediately production-breaking
- **LOW** — internal helper that needs updating, comment/docs stale, low-traffic path

Assign every finding a stable ID before writing the verdict:
- `BR-CRIT-001`, `BR-HIGH-001`, `BR-MED-001`, `BR-LOW-001`
- Reuse the same ID on reruns when the finding is the same underlying risk.
- Include the ID in the report tables, checklist, inline annotations, and closure ledger.
- Do not mark an ID closed without direct proof and a reviewer-style counterexample.

Then produce:
1. **Report** — see template in `references/output-templates.md`. Saves to `docs/blast-radius/`.
2. **Checklist** — risk-ordered, one line per touchpoint, with the verification command/test to run.
3. **Inline annotations** — for review mode, emit a `blast-radius-inline.md` keyed to diff hunks the
   user can paste into the PR or read alongside the diff.
4. **Diagnostic Gate Summary** — a normalized block inside the report with the
   gate verdict, consensus status, diagnose status recommendation, blocking
   finding IDs, disagreement ledger, and exact next handoff. This does not make
   blast-radius a fixer; it makes its findings consumable by `$diagnose`,
   `$diagnostic-cohort`, and `/goal` handoffs.

For PR mode or reruns, the report must also include:
- `## PR Review State` — head SHA, check status summary, unresolved-thread count, and the final
  GraphQL query timestamp
- `## Adversarial Matrix` — the falsification matrix from Step 5.5
- `## Review Feedback Trap Replay` — valid current/prior review findings, invariant class, applicability,
  local regression/proof, and residual risk
- `## Finding Closure Ledger` — required when any previous report or review thread had HIGH/MEDIUM
  findings

### Verdict guardrail (CRITICAL — read this every run)

Verdict is driven by **findings**, not by patterns checked. The most common failure mode of this
skill is "all mandatory patterns 1/2/13 returned PASS → verdict SAFE TO PROCEED" even when the
report contains a real HIGH finding from elsewhere. That is a false-confidence failure and it has
shipped real bugs in past runs.

Before writing the verdict, derive it mechanically. Prefer `scripts/derive_verdict.py` when available:

```bash
scripts/derive_verdict.py \
  --critical <n> --high <n> --medium <n> \
  --live-schema <verified|blocked|not_applicable> \
  --unresolved-threads <n> \
  --prior-unclosed <none|medium|high|critical> \
  --untested-important <none|review|do_not_merge> \
  --mandatory-patterns <passed|failed>
```

If the script is unavailable, apply the same precedence rules by hand and say the script was not run.

**Hard rules**:

- If ANY finding is **HIGH** or **CRITICAL** → verdict is **DO NOT MERGE**, full stop.
- If ANY finding is **MEDIUM** (and no HIGH) → verdict is **NEEDS REVIEW**, full stop.
- If live schema verification was BLOCKED → verdict is at minimum **NEEDS REVIEW** (you cannot
  certify what you did not verify).
- If PR mode has ANY unresolved GitHub review thread → verdict is **DO NOT MERGE / REVIEW THREADS
  OPEN**, full stop. The report may still distinguish "thread likely false positive" from "real bug",
  but the PR is not clean.
- If a prior HIGH/MEDIUM finding is not closed in the Finding Closure Ledger with a direct proof and a
  reviewer-style counterexample → verdict cannot improve beyond that prior severity.
- If a valid review-derived trap applies to the current diff but has no local regression, live proof, or
  documented `NOT APPLICABLE` evidence → verdict is at best **NEEDS REVIEW**. If the trap covers data
  writes, async work, business state, identity, money, inventory, or user-visible workflow state, verdict
  is **DO NOT MERGE**.
- If an important adversarial-matrix cell is `UNTESTED` → verdict is at best **NEEDS REVIEW**; if the
  untested cell covers a write path, async side effect, identity boundary, tenant/auth boundary, operator
  confirmation path, or data-integrity guard, verdict is **DO NOT MERGE**.
- If proof is `PARTIALLY PROVED`, mock-only, stale, wrong-head, or missing a required lifecycle leg,
  verdict is **DO NOT MERGE** for PR/ship decisions. Full proof is the only passing state.
- **SAFE TO PROCEED** is reserved for: every finding is LOW, every mandatory pattern PASSED, and
  live schema verification ran successfully, PR threads are resolved when in PR mode, and the
  adversarial matrix has no important UNTESTED/FAILED cells. No exceptions.

Before writing the verdict, do this micro-check:
1. Scan your own report. Count HIGH, MEDIUM, LOW findings.
2. Apply the mapping above mechanically. The verdict is the worst-case classification, not the
   average and not the "feel."
3. If the most severe finding is HIGH but you're tempted to write SAFE TO PROCEED because "the
   patterns all passed" — STOP. The patterns are a coverage tool. They tell you what you looked
   at, not what's safe.

**Pattern-coverage trap**: passing every named pattern does NOT mean the change is safe. The
pattern library is finite. Real bugs exist outside it (migration bootstrap regressions, build
script edits, infra config changes, etc.). Always weight the actual findings, never the
patterns-checked checklist.

## Step 7 — Recommend the verification plan

Don't just list risks. List the *commands the user should run* to prove the change is safe:
- The specific Jest tests to run (or to add)
- The specific E2E paths to exercise
- The specific psql queries to run against dev to confirm schema/data
- The specific sibling files to grep before merging
- The falsification-matrix cells that still need proof
- The final GitHub GraphQL review-thread query for PR mode

This is the part the user does after reading the report. Make it copy-pasteable.

## Stopping rules

This skill can run forever if you don't draw a line. Stop tracing when:
- You hit a stable public interface (e.g. Express router boundary, exported package API)
- You've gone 2 hops and the next hop is in an unrelated domain
- You're trawling the same file you've already analyzed (no new info)
- You've covered every SQL string for the affected columns (DB changes are exhaustive, not depth-limited)
- The user explicitly says "narrow to X"

For PR mode, do not stop before the final review-thread query. For DB-backed validation/identity/duplicate
guards, do not stop before the adversarial matrix is written and each important cell is classified.

When you stop, say *why* in the report's `## Trace Boundaries` section. Honesty about what wasn't
traced is more valuable than a false claim of completeness.

## What this skill is NOT

- Not a fixer. Surfacing what could break is the deliverable. Fixing is the user's call.
- Not `scope-check`. That checks whether the diff matches the task. Blast-radius checks downstream effects.
- Not `patch-or-fix`. That checks whether the fix is root-cause. Blast-radius checks whether the fix is
  complete (no sibling bugs, no missed callers).
- Not a replacement for tests. A green blast-radius report does not mean the code is correct — it means
  you've enumerated the surface area and verified the assumptions you knew to check.

## Output paths

- Report: `docs/blast-radius/<YYYY-MM-DD>-<change-slug>.md`
- Checklist: `docs/blast-radius/<YYYY-MM-DD>-<change-slug>-checklist.md`, and repeated in the
  report's `## Checklist` section
- Inline annotations: `docs/blast-radius/<YYYY-MM-DD>-<change-slug>-inline.md`

If `docs/blast-radius/` doesn't exist, create it. If the project has a different convention (e.g.
`evidence/`), use that instead. If route/worktree rules block artifact writes, emit the outputs
inline or use `$CLAUDE_JOB_DIR` if that path is allowed, and record the write limitation in
`## Trace Boundaries`.
