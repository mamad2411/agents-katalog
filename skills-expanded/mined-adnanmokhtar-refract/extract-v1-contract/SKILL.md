---
name: extract-v1-contract
description: "Extract a V1 feature's behaviour contract — inputs, outputs, effects, rules, invariants, known bugs — every claim a pinned v1 file:line plus excerpt, prefilled from paired-inventory lane rows."
kind: skill
pack: migration
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# extract-v1-contract

Read V1's *actual* behaviour into `ai/migration/contracts/<feature>.md` so V2 can be re-derived from a written spec, not transposed from V1's source. This is the single highest-leverage step in any port — every regression-after-cutover begins with "we missed this in V1."

## Premise

Find V1's real behaviour, no hand-waves. Every claim in the contract is a citation: `<v1-path:line>` + a one-line excerpt of the actual source line, pinned to a specific V1 commit SHA. Paraphrases like "validates input" or "returns the user" are halted — the contract is the source line plus its observable consequence. Inputs, outputs, side effects, business rules, invariants, and known V1 bugs are read out of V1's code + tests + git log + telemetry, not inferred from product docs. The contract is what V1 *does*, not what V1 *should* do.

## Halt conditions

- Halt on any contract claim missing `<v1-path:line>` + one-line source excerpt.
- Halt on a contract written against an unpinned V1 (no `v1_commit_pinned` in the ledger row), or read from the live V1 checkout instead of the pinned snapshot.
- Halt on a claim copied from a lane row without opening its `file:line` in the snapshot. The row is a lead; the excerpt must still match.
- Halt on tier expansion (Standard → Heavy) without an explicit user-recorded justification on the ledger row.
- Halt on "feature too small to need a contract" — small features per tier rules; no contract per tier rules; never silent-skip.

This skill is the procedural arm of `migration-discipline.md` + `feature-port.md` Phase 1.

## Tier-aware contract scope

The contract's required scope scales with the ledger row's `tier:` field (set by audit). **Canonical default:** `trivial` until the parity audit sets `tier:` on the ledger (`migration-discipline.md`); `validate-migration-artifacts.sh` defaults missing ledger `tier` to `trivial`. Do not assume `heavy` when `tier` is absent — read the ledger row after audit.

- **Heavy tier**: full 9-section contract (Inputs / Outputs / Side effects / Business rules / Invariants / Performance characteristics / Caller assumptions / Edge cases V1 handles / Known V1 bugs). All sections populated; every claim cited `<path:line>` with one-line excerpt.
- **Standard tier**: 3 sections only — § 1 Inputs, § 2 Outputs (per code path), § 9 Known V1 bugs. Skip § 3–§ 8 as separate sections; fold any load-bearing item flagged by audit into the relevant section. Citation discipline still applies.
- **Trivial tier**: no contract required. The audit's classification + 1-paragraph "what changed" + 1-paragraph "why no contract" is the artifact.

Refuse to expand a contract beyond its tier without an explicit user request to upgrade the tier (which the user records on the ledger row + justifies in the audit).

## When to use

- A new ledger row enters state `In-progress` (called by `/port-feature` automatically).
- Re-extracting an existing contract because parity tests revealed behaviour the contract didn't capture.
- Auditing whether a previously-written contract is complete (call this on the V1 side; diff against existing contract).

## When NOT to use (refuse + explain)

- V1 doesn't exist (greenfield). There is no contract to extract — write the contract from product / API spec.
- The "feature" is not a feature — it's a cross-cutting concern (e.g., logging middleware, error envelope). These migrate as infrastructure, not as features. Use `legacy-modernizer` strategy instead.
- The feature is too large to contract in one document (>500 lines) — split into sub-features first; one ledger row each.
- V1 is being actively modified during extraction. Pin V1's commit before extracting; extraction is meaningless against a moving target.

## Prerequisites

- `.claude/_extracted-codebase.md § Migration` is populated (V1 root + V2 root + ledger path detected).
- A specific feature is identified (entry point: route URL, function name, class, file path).
- Read access to: V1 source, V1's tests, git log, bug tracker (or its equivalent — issue list, PRs, internal docs), production telemetry (latency / error / log samples) for the feature if available.

## Procedure

### 0. Read V1 at the pin, and prefill from the lane rows

**V1 is read from a snapshot of the pinned SHA, never from the live checkout** (D27). A V1 branch that moves during extraction makes every `v1-path:line` in the contract point at a line that is no longer the one cited.

```bash
PIN="<v1_commit_pinned from the ledger row>"; RUN="$(mktemp -d "${TMPDIR:-/tmp}/v1-contract.XXXXXX")"; : > "$RUN/stamp"
export GIT_OPTIONAL_LOCKS=0; mkdir "$RUN/v1"
git -C "<v1-root>" archive "$PIN" | tar -x -C "$RUN/v1"                       # write-free; read every V1 file from "$RUN/v1" (a V1 in a subdirectory of its repo: archive "$PIN:<subdir>")
PI=.claude/skills/paired-inventory/scripts/pair-inventory.py
python3 -I "$PI" --v1="<v1-root>" --pin="$PIN" --v2=. --pair-map=ai/migration/pair-map.tsv --out="$RUN/pi" > "$RUN/candidates.tsv" 2> "$RUN/ledger.txt"; echo "pair-inventory exit $?"
# the feature's V1 rows: every lane file, filtered to the files and route keys of this feature
cat "$RUN"/pi/v1/*.tsv 2>/dev/null | awk -F'\t' -v pat="<feature's V1 paths or route prefix, as a regex>" '$1 !~ /^#/ && ($4 ~ pat || $2 ~ pat)' > "$RUN/feature-rows.tsv"; wc -l < "$RUN/feature-rows.tsv"
find "<v1-root>" -newer "$RUN/stamp" -type f -not -path '*/.git/*' | head -3               # must print nothing
```

Without a V1 tree (solo mode), the rows come from `ai/migration/v1-inventory/<lane>.tsv`, checked fresh first (`paired-inventory` § Modes: `sha` = the pin, extractor hash = the installed module). The contract can be prefilled from those rows, but every claim the procedure below would read in V1 code is marked `UNREAD (no V1 tree)`. It is never paraphrased from the row.

Every lane row is `lane · key · attrs · file:line · excerpt`. It **seeds** a contract line, already cited:

| Lane | Contract section it seeds |
|---|---|
| I-ROUTES, I-RULES (incl. `GLOBAL trim_strings` / `empty_to_null`), I-CONF | § Inputs (method + path, every field rule, defaults for omitted fields) |
| I-ERR | § Outputs — one error path per status / `code` row |
| I-AUTHZ, I-SCOPE | § Inputs (who may call) and § Invariants (tenant and owner scope, soft delete) |
| I-SIDE, I-SCHED | § Side effects (the emitter multiset per entity verb; the schedule with its zone and overlap rule) |
| I-ENUM, I-SCHEMA | § Outputs (value sets) and § Invariants (unique, FK, NOT NULL, derived columns, views) |
| I-MONEY | § Business rules (the rounding mode and its order on each money path) |

A prefilled line is a **lead, not a claim**. Open the cited `file:line` in the snapshot, confirm the excerpt, then write the observable consequence the procedure below establishes. A row whose excerpt no longer matches is a stale record: re-record it, do not cite it. The rows are only what the lanes can see. Steps 1–8 still read the entry point down, because conditionals, error paths that throw no mapped exception, and consumer assumptions have no lane. The prefill is what the reader must not miss, not the whole contract. A lane that printed `blocked` in `ledger.txt` seeds nothing, and its sections are read by hand.

### 1. Identify the entry point + boundary

Pick **one** entry point (e.g., a route handler, a CLI command, a job consumer). Trace outward until you reach:

- I/O boundaries (DB, external HTTP, queue, cache, file).
- Auth / authz checks.
- Output construction (response builder, log emit, queue publish).

Everything *between* the entry and the boundary is in scope. Things called from outside this scope but used internally (e.g., `getUser`) are dependencies, not part of this feature's contract — record them in the dependencies section.

### 2. Trace the happy path — read every line

```text
For each file in the call graph (entry → boundaries):
  1. Read the entire file. Don't skim — read.
  2. Note every conditional, including ones with no comment.
  3. Note every error path (try/except, error returns, .catch).
  4. Note every side effect (write, emit, publish, invalidate, log).
  5. Note every type / shape of input + output.
  6. Note every dependency call: which function, what args, what return shape.
  7. Note any time / random / external-state dependence.
```

### 3. Trace error paths — read every catch / error return

For each error path:
- What input triggers it?
- What's the observable behaviour (HTTP status, exception class, error code string, log line, side effect attempted/skipped)?
- Does the error path leave the system in a clean state, or partially mutated?
- Is the error path tested? Find the test (if any).

### 4. Read tests — what V1's authors thought it does

Read every test file that touches V1's feature. Note:

- Behaviours the tests cover (these are the AUTHORS' contract).
- Behaviours the tests do NOT cover but the code clearly handles (these are the SILENT contract — the most common source of regressions).
- Behaviours the tests cover that aren't in the code anymore (dead tests = past contract).

### 5. Read git log — why is V1 shaped this way

```bash
git log --follow -p <v1-entry-point>      # entry point's history
git log --follow -p <v1-supporting-files> # each file in the call graph
```

Pay attention to:

- Recent bug fixes — these reveal hidden invariants (the conditional that "looks weird" is the patch for an old bug).
- "Quick fix" / "hotfix" commits — disproportionately load-bearing in production.
- PR discussion / review comments (if accessible) — reveal contract decisions never in the code.

### 6. Read bug tracker / issue list

Search for the feature name + adjacent terms. Capture:

- Bugs reported against V1 that are still open (these are V1's *known* bugs — decide explicitly: preserve in V2 (parity) OR fix in V2 (contract break + ADR)).
- Bugs reported and fixed (these often left a check or branch in the code that's not obvious — find the commit).
- Feature requests against V1 that landed (these are evolution of V1's contract).

### 7. Inspect production telemetry (if available)

- **Latency p50/p95/p99** — V2's contract includes "no worse than V1". Capture the V1 baseline.
- **Error rate** — what's V1's normal error rate? V2's must not exceed it.
- **Throughput** — V1's QPS / RPS / req-rate. V2 must handle the same.
- **Log samples** — sample 100 production logs of this feature. What inputs is V1 actually receiving (vs what the unit tests use)? Anonymise before saving.
- **DB cost per call** — how many queries, what query plans, what row counts. Captures perf-uplift candidates.

### 8. Inspect adjacent code that *consumes* V1

Run `git grep` for V1's exported symbols / endpoints. For each consumer:

- What return shape does the consumer expect? (E.g., does the caller `if (user)` or does it `if (user != null)` — both should still work in V2; if the consumer uses `Object.keys(user)` then V2's column projection must keep all keys.)
- Does the consumer rely on side-effect ordering?
- Does the consumer rely on V1 throwing vs returning null? (One of the most common silent breaks.)

The contract section "Caller assumptions" lists every observable the consumers depend on, with `<file>:<line>` citations.

### 9. Synthesise the contract

Write `ai/migration/contracts/<feature>.md` with this structure:

```markdown
# Contract: <feature>

> V1 entry point: `<v1-path:line>`
> V1 commit pinned: `<sha>`
> Author: <name> | Reviewed: <name> | Date: <iso>

## Inputs

- `<param-name>`: <type> — <constraints>; default `<default>` if any; validated by `<validator-path:line>` if any.
  - Edge cases V1 handles: empty string, null, oversize (>N bytes), malformed (e.g., trailing whitespace), Unicode normalisation, etc.
- ...

## Outputs (per code path)

### Happy path
- Shape: `<TS / Pydantic / dataclass / JSON shape>`
- Field-by-field semantics: `<name>` is `<source>` — e.g., `total = sum(line.amount) + tax` where `tax = orderTotal * taxRate(jurisdiction)`.

### Error path: <name> (e.g., `MissingUser`)
- Trigger: `<input condition>`
- Observable: HTTP `<code>`, body `<shape>`, log line `<structured fields>`, metric `<name>` incremented.
- Side effects executed before the error: `<list>` (e.g., "audit log written before failing — system depends on this").
- Side effects skipped: `<list>`.

(Repeat for every error path.)

## Side effects (every code path)

- DB writes: table `<t>`, columns `<c>`, condition `<when>`, idempotency key `<if any>`.
- External HTTP: endpoint `<url>`, method `<m>`, when `<condition>`, retry policy `<r>`, timeout `<t>`.
- Queue publishes: queue `<q>`, message shape `<s>`, ordering required `<y/n>`.
- Cache: reads from `<key pattern>`, writes to `<key pattern>` with TTL `<t>`, invalidates on `<event>`.
- File I/O: `<path>`, mode, atomicity required.
- Logs systems depend on: structured field `<name>`, consumed by `<system>` (e.g., billing dashboard reads `event=order_created`).
- Metrics: counter `<name>`, histogram `<name>`, when emitted.

## Business rules

For each named rule found in code (give it a name even if V1 doesn't):

- **Rule-001: orders.discount.minimum_order_value** — discount applies only if `order.total >= 50`. Source: `<path:line>`. Test: `<path:line>` (or "no direct test"). Origin: `<git commit / issue>`.
- ...

## Invariants

- **Ordering**: e.g., audit log written BEFORE the DB commit (so audit captures intent even on commit failure). Source: `<path:line>`.
- **Idempotency**: e.g., POST /orders with same `Idempotency-Key` returns same response without re-executing side effects. Source: `<path:line>`. Storage: `<table>`.
- **Atomicity**: e.g., user-create + welcome-email-enqueue are in one DB transaction; either both happen or neither.
- **Retry semantics**: e.g., on HTTP 503 from external X, retry up to 3 times with exponential backoff; on 4xx, no retry; on network error, retry once.
- **Concurrency**: ordering or exclusion guarantees under concurrent calls (e.g., row-level lock on user; advisory lock on report-generation per user).

## Performance characteristics (V1 baseline)

- Latency: p50 `<ms>`, p95 `<ms>`, p99 `<ms>` (source: `<dashboard / log / measurement>`).
- DB queries per call: `<count>` (`<list>`).
- External HTTP calls per call: `<count>`.
- Memory per call: `<estimate>`.
- Throughput cap: `<qps>` if known.

## Caller assumptions (consumers of V1)

- `<consumer-path:line>` expects V1 to: `<observable>`. Breaking this is a contract change.
- ...

## Edge cases V1 handles (catalogued, with citations)

- Empty input: `<observable>` (source: `<path:line>`).
- Null input: `<observable>` (source: `<path:line>`).
- Concurrent calls with same key: `<observable>` (source: `<path:line>`).
- Network error from dependency X: `<observable>` (source: `<path:line>`).
- Dependency timeout: `<observable>` (source: `<path:line>`).
- Oversized input: `<observable>` (source: `<path:line>`).
- Malformed input (per validator): `<observable>` (source: `<path:line>`).

## Known V1 bugs

For each, decide: **preserve** (parity) or **fix** (contract break, separate ADR).

- **Bug-001**: <description>. <issue link>. Decision: **preserve** — V2 reproduces this behaviour. Caller depends on the buggy behaviour (`<path:line>`). Fixing requires ADR + caller migration.
- **Bug-002**: <description>. <issue link>. Decision: **fix** — pre-arranged ADR `<ADR-NNN>`; ships in a separate PR after V2 cutover.

## Open questions (for migration owner)

- ...
```

### 10. Review the contract

A second reviewer reads V1 alongside the contract. Their job: find anything the contract missed. Common misses:

- A debug-only log line that production parses for billing.
- A test fixture that hides the only callsite that exercises a rare branch.
- An old hotfix branch with no comment and no test that now reads as "obviously dead".

### 11. Register the pin in the ledger

The pin is chosen **before** step 0, not after the read: the ledger row's `v1_commit_pinned`, or, for a first extraction, `git -C <v1-root> rev-parse HEAD` recorded on the row first. Every citation in the contract resolves against that SHA's snapshot. Update `ai/migration/ledger.md` for this feature: `state: In-progress`, `v1_commit_pinned: <sha>`, `contract: ai/migration/contracts/<feature>.md`. When a later V1 commit changes a cited file, the contract is re-extracted at the new pin; it is never patched line by line against the live tree.

After this point, V1 must NOT be modified for this feature. V1 is the parity oracle.

## Output format

The contract file at `ai/migration/contracts/<feature>.md` is the artifact, scoped to the ledger row's tier:
- Heavy tier → full 9-section contract per the structure above.
- Standard tier → 3-section contract (Inputs / Outputs per code path / Known V1 bugs) with the same citation discipline.
- Trivial tier → no contract file written; the audit doc carries the rationale.

Linting checks (run via `scripts/validate-migration-artifacts.sh`):

- Every `<path:line>` citation resolves (file exists, line exists, content roughly matches).
- Every error path has: trigger + observable + side-effect notes.
- Every external dependency has: shape + retry/timeout/idempotency notes.
- The ledger row references this contract.
- The V1 commit pinned in the ledger row resolves.

## Output expectations — citation discipline

Every claim in the contract is a citation, not a paraphrase. Two requirements:

1. **`<path:line>` resolves** — file exists at the pinned V1 commit, line exists, and the cited line is within ±3 of the claim's subject. The validator's `check_audit_provenance` + path-resolver checks each reference.
2. **One-line excerpt of the cited line** — quote the actual source line beside the citation so a reviewer (and the validator's `check_audit_body_consistency` / citation-spoof detector) can verify the line's content matches the claim. Without an excerpt, an audit can echo "looks identical at `<path:line>`" while the line at that location says something else — the **Trusted Summary** anti-pattern. Excerpts make spoofing visible.

Example:

```markdown
- Rule-003: discount minimum $50.
  Source: `Reports/views.py:217` — `if order.total < 50: return None`
```

NOT:

```markdown
- Rule-003: discount minimum $50. Source: Reports/views.py:217  ← unverifiable
```

## Project anchors (read before extracting)

Before you start, read `ai/migration/_v2-anchors.md` (schema at `templates/packs/migration/_v2-anchors-schema.md`). It declares the project's:

- `project_kind` (frontend / backend / API / mixed) — drives which axes the contract covers (e.g., frontend adds form fields, UI affordances, query-param surface, per-button permission gates, reactive lifecycle).
- `v1_root` and `v2_root` — your `<v1-path:line>` citations resolve relative to `v1_root`.
- Gold-standard files — exemplar V2 implementations the port should match in shape. Concrete file names are project-specific and live in `_extracted-idioms.md § Gold standards` (e.g., the project's canonical CRUD-page leaf component; the project's base-service / repository-base / controller-base class).
- Shared component map — components / hooks / utilities V2 reuses. The contract's "consumer assumptions" must reflect these. Names are project-specific (read from `_extracted-idioms.md § Shared inventory`).
- Layering rules — the project's actual layer chain as extracted (e.g., components → composables / hooks → services → core for frontend; controller → service → repository for backend; handler → use-case → domain for hexagonal). The contract's side-effect ownership maps to whichever layer chain the project uses.

Without anchors, contracts drift from V2 reality. The validator's `check_v2_structure` + `check_composable_reuse` + `check_service_shape` halts at audit time on contracts that ignore anchors.

## Verify (postconditions)

Contract: [`templates/snippets/postcondition-check.md`](../../../../snippets/postcondition-check.md). **Preconditions are not verification** — this skill guards its entry and must also check its exit. Every entry under `## Failure modes` that this skill's own write could cause becomes a check here, observed rather than assumed, reported when it passes as well as when it fails, and `NOT RUN` with a reason where no signal is available. A failure mode the skill documented and never checked is a risk it accepted on the caller's behalf without saying so.

## Failure modes

- **"This feature is too small to need a contract."** — small features are where regressions hide because nobody bothered. The contract is cheap; write it.
- **"V1 is incomprehensible."** — incomprehensible V1 is exactly when the contract is most valuable. Allocate more time; pair with V1's last author if reachable.
- **"The contract grew too big."** — feature is too large; split. Each split feature gets its own contract + ledger row.
- **"V1 has no tests."** — record-replay is your test data. Capture production traffic samples (anonymised) into `tests/parity/<feature>/replay/`.
- **"V1 has bugs we don't know about."** — that's fine; the contract is "what V1 *does*", not "what V1 *should* do". Bugs live in the **Known V1 bugs** section. The contract evolves when parity tests find new ones.
- **"The contract is wrong about V1 (parity tests failing in unexpected ways)."** — revise the contract; re-pin V1 if V1 has moved; investigate. The contract being wrong is itself a discovery.

## Related

- `migration-discipline.md` — the rule this skill enforces.
- `feature-port.md` — Phase 1 of the per-feature lifecycle.
- `parity-test-generate.md` — consumes this contract to build parity tests.
- `perf-uplift-survey.md` — consumes the **Performance characteristics** + **Side effects** sections.
- `migration-architect.md` (agent) — uses this contract to plan V2.
- `parity-auditor.md` (agent) — verifies the contract is complete before cutover.
- `paired-inventory` (skill) — the lane rows step 0 prefills from; `/migration-scan --record-v1-inventory` records them for solo runs.
