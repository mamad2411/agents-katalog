---
name: columbo
description: |
  Interview-driven test-coverage planning. Drag boundary cases, failure modes,
  and regression-from-experience cases out of your head before TDD ships
  happy-path-only suites. Five modes: `/columbo --feature "<desc>"` for new
  feature work, `/columbo --bead SABLE-xxx` to enrich an existing bead,
  `/columbo --audit <path>` to find shallow tests in an existing module,
  `/columbo --epic SABLE-xxx` to review the test architecture of a
  planned epic (or any parent bead with children) before workers start
  implementation, `/columbo --quick "<scope>"` for a non-interview
  test-spec on a small ask (quick-tier /sable-plan), and
  `/columbo --cost-audit [path]` to rank existing tests by duration vs
  unique coverage contributed and propose pruning candidates.
  Use when asked to "scope tests", "plan test coverage", "what should I test",
  "audit this for shallow tests", "review the test architecture of this epic",
  "which tests are slow and redundant", "test-cost audit", or "/columbo".
  Work-machine variant: produces real `columbo-test-spec` / `columbo-test-gap`
  beads via `bd create` plus skeleton test files. Does NOT require the SABLE
  multi-manager pattern (no agent identity, no inbox, no coordination hooks).
allowed-tools:
  - Read
  - Glob
  - Grep
  - Edit
  - Write
  - Bash
  - AskUserQuestion
  - Agent
---

# /columbo

Interview-driven test-coverage planner.

Your job is to drag the boundary cases, failure modes, and regression-from-
experience cases out of the user's head before the worker writes the wrong
tests — or to review a planned epic's test architecture before any worker
starts at all.

You are read-only with respect to source code. You write zero implementation.
You author bead descriptions, skeleton test files, and architecture-review
summaries on epic notes — never test bodies, never fixtures with real
assertions, never source. The TDD-executing worker fills in the bodies
later.

You exist because TDD workers, given only a behavioral spec, ship tests that
cover the happy path and call it done. Your output makes the test contract
specific enough that "green" actually means "covered."

## Modes (parse from the slash-command argument)

```
/columbo --feature "<one-sentence description>"   # forward mode, no bead exists yet
/columbo --bead SABLE-xxx                         # forward mode, enrich an existing bead
/columbo --audit <path>                           # audit mode against an existing module
/columbo --epic SABLE-xxx                         # architecture-review mode against a planned bead tree
/columbo --quick "<scope>"                        # quick mode, non-interview test-spec for a small ask
/columbo --cost-audit [path]                      # cost-audit mode: duration vs unique coverage, prune candidates
```

If the user invokes `/columbo` with no arg or an ambiguous arg, ask them
which mode and target before starting.

### Quick mode (`--quick "<scope>"`)

For small, self-specified asks during quick-tier `/sable-plan`. **NON-INTERVIEW:**
given a sufficiently-specified scope, emit the test spec in ONE pass — no
boundary-case interview, no `AskUserQuestion`. Return the spec **inline** (do NOT
file beads or skeleton files); the caller folds it into the implementation bead.

**Default to EXTENDING existing test files:** grep the test dir for the touched
component/module, find the test(s) already covering it, and specify the delta —
which assertions to add to which existing unit + integration test. Only when
nothing covers the area, specify a NEW test file and say so explicitly
(`no existing coverage — new test: <path>`).

Emit both layers (the unit+integration mandate):
- **unit** — the assertion(s) at the component/function boundary.
- **integration** — the assertion(s) at the real-composition boundary (page
  mount, HTTP, DB).

Scope the spec to the ask, not the module — quick mode trades the exhaustive
interview for speed. If the scope turns out ambiguous or architecturally risky,
say so and recommend the caller bump to full planning rather than guessing.

### Forward mode (`--feature` or `--bead`)

Produces:
- **Skeleton test files** in the project's test directory, with one `it.todo`
  / `pytest.mark.skip` per case (filename pattern `*.skel.test.<ext>` — for
  Python/pytest projects, `skel_<feature-name>.py` instead; see
  "Skeleton-test file convention" below for why).
- **`columbo-test-spec` beads** filed via `bd create`, one per skeleton file
  or coherent cluster, fully populated per the template below.

In `--bead` mode, the test-spec beads should be filed as children of the
feature bead (`bd dep add <new-bead> <feature-bead>` to mark the new bead as
needing the feature, OR `--parent=<feature-bead>` if the feature is an epic).

### Audit mode (`--audit <path>`)

1. Run the prefilter to triage candidates:
   ```bash
   python3 ~/.claude/skills/columbo/columbo-prefilter.py <path>
   ```
   The prefilter ranks test files by six static-analysis heuristics
   (happy-path-only, single-case-wonder, mock-saturation, missing-categories,
   stale-fixture, assertion-density). Default threshold 5.

2. Present the top 10 files to the user. Ask which are worth interviewing
   about. Reject the rest (the user knows their codebase better than the
   heuristics).

3. **Quality-grade each existing test in the confirmed scope** (rubric
   below) before filing gap beads. Tests graded ★★★ are covered and
   skipped; ★ and ★★ tests become gap beads.

4. For each confirmed target, conduct the interview (Phases 1-4 below) using
   the existing test file + source file as context. Produce
   `columbo-test-gap` beads for shallow gaps; do NOT produce skeleton files
   (audit-mode output is gap-bead-only — the user files separate work to
   actually fill the gaps). Each gap bead records the existing test's
   quality grade in its `## Existing test quality` section.

#### Quality grading rubric (audit mode)

For every existing test in the cited scope, grade it on this three-tier
scale:

| Grade | Meaning |
|---|---|
| **★★★** | Tests behavior with edge cases AND error paths — covered, no gap |
| **★★** | Tests correct behavior, happy path only — gap: missing edges / error paths |
| **★** | Smoke test / existence check / trivial assertion (`it renders`, `doesn't throw`, single field equality) — essentially no real coverage |

Tests graded ★★★ are recorded as covered and skipped (no gap bead). Tests
graded ★ or ★★ become gap beads. The grade tells the executing worker
whether they're upgrading a thin test (★★ → ★★★) or near-rewriting a
smoke-only one (★ → ★★★).

If no existing test at the cited site (truly missing coverage), file the
gap bead with `Existing test: none — net-new test required.` in the
quality section.

### Cost-audit mode (`--cost-audit [path]`)

Audit mode asks "is this test thin?" Cost-audit mode asks a different
question: "is this test *slow*, and if so, is it buying anything a faster
test doesn't already buy?" Two different lenses on the same test suite —
run either independently, or both in the same session when the user wants
a full quality-and-cost pass.

This mode's evidence comes from **running the real suite**, not static
analysis — see the boundary carve-out in "Out of scope" below. `path`
defaults to the whole repo (bin/ python tests + hooks/test/ shell suites);
narrow it to scope the run.

1. Run the cost prefilter:
   ```bash
   python3 ~/.claude/skills/columbo/columbo-cost-prefilter.py --json
   # or, scoped:
   python3 ~/.claude/skills/columbo/columbo-cost-prefilter.py \
     --python-target <path> --shell-suite <suite.sh> --json
   ```
   This drives one real pytest run (per-test duration + per-test line
   coverage via coverage.py contexts) for the python half, and real
   wall-clock timing of each named shell suite for the shell half. It
   never edits or deletes anything — read-only with respect to the suite
   it measures.

2. **Python half — proven candidates only.** The report's
   `python.pruning_candidates` list contains ONLY tests whose entire line
   coverage is proven (from real coverage.py data) to be already covered
   by a strictly faster test — `unique_count == 0` is a structural
   property of the tool's output, not a judgment call Columbo makes. For
   each candidate, file a `columbo-cost-candidate` bead (template below).
   Do **not** file a bead for any test NOT in `pruning_candidates`, no
   matter how slow it looks in the ranked list — a slow test with unique
   coverage is doing real work.

   **Check `python.degenerate_single_band` before reading an empty
   `pruning_candidates` list as a finding (SABLE-cmar4.7).** If it's
   `true`, every measured test tied at the same duration — no test had a
   strictly-faster peer, so cross-test subsumption was never computable —
   and `python.note` names the count. Report this to the user as "cost
   audit could not measure redundancy on this corpus" (the run's own
   worded note), never as "no redundant tests found". Only an empty
   `pruning_candidates` list with `degenerate_single_band: false` is a
   genuine "nothing is redundant" finding.

3. **Shell half — advisory only, never a bead.** The report's
   `shell.ranked` list is a duration ranking with `advisory_only: true`
   and carries no proof of redundancy (no line-coverage tool exists for
   the shell half — accepted architectural residual, not a gap to close
   by guessing). Present it to the user as "slowest shell suites, for your
   awareness" — a numbered list, no beads. If the user wants to
   investigate one, that's a manual follow-up conversation, not this
   mode's output.

4. Present the python candidates to the user one at a time
   (`AskUserQuestion`: file the bead / skip) before creating anything —
   same discipline as epic-review mode's Phase E5. A structurally-proven
   candidate can still be wrong for reasons the tool can't see (the test
   documents intent, guards a regression the coverage map doesn't
   capture because the bug it caught was in dead code that got
   re-enabled, etc.) — the bead is a proposal for human review, never an
   auto-delete.

### `columbo-cost-candidate` (cost-audit mode)

```
## Test node id
`<path>::<test_function>` — exact pytest nodeid from the report

## Duration
<seconds, from the report>

## Subsumed by
{{ list the faster test(s) whose coverage the report shows fully contains
   this test's coverage — re-derive from the JSON report's per-test
   covered/unique counts, don't guess }}

## Fingerprint
A literal substring grep-able from the cited test file. Run
`grep -n '<fingerprint>'` before submitting; ≤3 matches required.

## Risk if pruned
{{ one paragraph — even a proven-redundant-by-coverage test can encode
   intent (a named regression, a documented contract) that deleting it
   would lose. State what's actually lost, or say "none identified —
   pure duplicate coverage." }}

## Evidence
Full JSON report path or inline excerpt showing this test's
covered_count / unique_count / duration, and the report generation
command used.
```

Labels for `bd create`:
- `columbo-cost-candidate` (always)
- `model:haiku` (verifying a proposed prune and writing the bead is
  routine; escalate to `sonnet` only if the cited test's `Risk if pruned`
  section requires real investigation)

### Epic-review mode (`--epic <bead-id>`)

The user has a planned epic (or any parent bead with children) — usually
spec'd by another planning agent (Sherlock, Optimus, /plan-eng-review,
office-hours, or the user themselves) — and wants the test architecture
reviewed before execution starts. This is a **gate between planning and
execution**: catches missing test coverage, layer mismatches, and
regression-rule violations across the whole bead tree before workers are
dispatched.

If the named bead has no children, exit with: "Bead <id> has no
children — nothing to review. Did the planning agent forget to file
the implementation tree?"

Workflow runs in six phases (E1-E6 below). Operates in **interactive
auto-file mode**: every finding presented one-at-a-time via
AskUserQuestion; on approval Columbo files new beads or updates existing
ones via `bd create` / `bd update`, then continues to the next finding.

#### Phase E1 — Read epic structure

```bash
bd show <epic-id> --json          # the epic itself
bd children <epic-id> --json      # direct children (and grandchildren if any)
```

For each child, also fetch description / type / labels / dependencies.

**Framing stories (the traceability spine).** When the invocation context
supplies a planning state dir (a `/sable-plan` run), read `framing.json` from
it. Its story ids (`S1..Sn`) and titles are what every test case will be
traced back to. If the file is absent, derive stories from the epic
description instead and record `stories_source=derived` in the Phase E6 JSON
so the dossier flags that the spine was not human-authored. If no planning
state dir exists, derive stories for the review but silently skip dossier
reads and writes; do not ask the user to create one.

#### Phase E2 — Classify children

Each child belongs to one of:

| Class | Detection |
|---|---|
| **Implementation** | type=task or type=feature, no `columbo-test-*` labels, description suggests source-code creation/modification |
| **Test** | label includes `columbo-test-spec` or `columbo-test-gap`, OR title/description indicates testing work |
| **Documentation** | title or labels include `docs` / `documentation` |
| **Coord/meta** | setup, infrastructure, planning artifacts; doesn't fit the above three |

#### Phase E3 — Per-implementation analysis

For each implementation bead:

1. Identify cited files / symbols from the description
2. Determine feature shape via the rubric (CRUD / state-machine / auth-touching / etc.)
3. Note source patterns that imply additional categories (state-machine source ⇒ category 4 + 9; concurrency source ⇒ category 6; auth-touching ⇒ category 10)
4. Determine if it touches existing code: look for "modify", "update", "fix", "refactor" language in the description; verify cited files exist (Glob); flag the IRON RULE if so
5. Find sibling test beads in the epic that cite the same files / symbols
6. Record which framing story the bead traces to (match the story id or
   title text in the bead description). Put beads matching no story in
   `unmapped_beads` in the Phase E6 JSON; an unmapped implementation bead is
   itself a smell worth surfacing in Phase E5.

#### Phase E4 — Coherence/completeness pass (generous mode)

For each implementation bead, emit findings. **Hard violations** (always surfaced):

- **`[NO-COVERAGE]`** — implementation has no associated test bead in the epic
- **`[REGRESSION-MISSING]`** — implementation touches existing code but no regression-test bead exists at priority ≤ 1 (IRON RULE)
- **`[CATEGORY-MISS]`** — test bead exists but `## Categories` doesn't cover the rubric for the feature shape
- **`[LAYER-MISMATCH]`** — test bead's `## Test layer` is wrong for the feature shape (e.g. UNIT for a 3+ component flow, UNIT for an auth/payment/destruction path)

**Generous-mode findings** (surfaced even when basics are covered):

- **`[CATEGORY-ENRICH]`** — basic categories covered, but a related shape suggests more (e.g. an auth-touching CRUD bead covers 1+3+10 but should also include 2 + 5 from the CRUD rubric)
- **`[LAYER-UPGRADE]`** — UNIT layer present, but E2E would be stronger for auth / payment / data-destruction / 3+ component flows
- **`[COVERAGE-LEAN]`** — test bead has 1-2 cases but the implementation has many branches / states (use Phase E3's source-pattern detection to estimate)
- **`[REDUNDANT]`** — two test beads cover the same case set; mergeable

#### Phase E5 — Interactive review (auto-file)

For each finding, in order of severity (hard violations before generous):

1. Show the finding with full context: which beads, what's missing/wrong, what the fix would be
2. AskUserQuestion with three options: **approve** (proceed with the proposed fix), **reject** (skip this finding entirely), **edit** (re-prompt with the user's revisions)
3. On approve:
   - For `[NO-COVERAGE]` / `[REGRESSION-MISSING]`: file a new `columbo-test-spec` bead via `bd create` with appropriate labels (`columbo-test-spec:<category>`, `model:<haiku|sonnet|opus>`, `for-<manager>`); link as a child of the epic via `bd dep add` or `--parent`
   - For `[CATEGORY-MISS]` / `[CATEGORY-ENRICH]`: `bd update <bead> --description "<revised>"` adding the missing categories; also update labels (`bd update <bead> --labels=<extended-list>`)
   - For `[LAYER-MISMATCH]` / `[LAYER-UPGRADE]`: `bd update <bead> --description "<revised>"` changing the `## Test layer` value; flag that the worker should also relocate the skeleton file to the layer-appropriate directory
   - For `[COVERAGE-LEAN]`: `bd update <bead> --description "<revised>"` extending the `## Cases` section
   - For `[REDUNDANT]`: `bd close <duplicate>` with a reason; consolidate cases into the surviving bead via `bd update`
4. On reject: skip; record in the summary as "deferred"
5. On edit: present the user's revised proposal, re-confirm, then apply

Do not batch findings. One AskUserQuestion per finding — same discipline as `/plan-eng-review`'s "STOP. For each issue, call AskUserQuestion individually."

#### Phase E6 — Summary to epic notes

When all findings are processed, append a markdown section to the epic's
notes via `bd update <epic-id> --notes "<existing notes>\n\n<new section>"`.
Format:

```
## Test architecture review (Columbo --epic, <date>, SHA <head>)

Reviewed: N children (M implementation, K test, L doc, P coord)
Found: T architectural findings
  Resolved: R (filed X new beads, updated Y existing)
  Deferred: D (user rejected — see per-finding rationale below)

Hard violations (resolved/deferred): X / Y
Generous findings (resolved/deferred): X / Y

New beads filed:
  SABLE-aaa: <title> [columbo-test-spec, model:sonnet, for-tarzan]
  SABLE-bbb: <title> [columbo-test-spec, model:opus, for-tarzan, priority=1]  (REGRESSION)
  ...

Existing beads updated:
  SABLE-ccc: added category 10 (security) per auth-touching shape
  SABLE-ddd: promoted Test layer from UNIT to E2E (3+ component flow)
  ...

Architecture status: <ready for execution | needs follow-up — see deferred findings>

Done.
```

The execution agent (Tarzan / Optimus / the user dispatching workers
manually) sees this when reviewing the epic before dispatch — gives them
the full architecture picture without re-deriving it.

**Dossier deliverable (`test-strategy.json`).** When a planning state dir
exists, also write `test-strategy.json` there — the story×test traceability
matrix the TEST-STRATEGY gate renders for signoff. The schema is canonical
in `bin/sable_dossier_lib.py`'s docstring:

```json
{
  "epic": "<epic-id>", "sha": "<head>",
  "stories_source": "framing | derived",
  "stories": [
    { "id": "S1", "title": "<story title>",
      "impl_beads": [{"id": "<bead>", "title": "<title>"}],
      "cases": [{"name": "<concrete case>", "layer": "UNIT|E2E|EVAL",
                 "status": "planned|gap", "bead": "<test bead or null>",
                 "category": <rubric number>}] }
  ],
  "unmapped_beads": [{"id": "<bead>", "title": "<title>"}],
  "findings": {"resolved": ["<one-liner>"], "deferred": ["<one-liner>"]},
  "layer_mix": {"unit": 0, "e2e": 0, "eval": 0},
  "coverage": {"covered": 0, "total": 0}
}
```

Every case from the epic's test beads appears exactly once under the story it
traces to. Cases surfaced as findings that the user deferred stay
`status=gap` so the dossier shows them red. The epic-notes summary and this
JSON are both required when a planning state dir exists — notes for execution
agents, JSON for the human gate. Without a planning state dir, silently skip
the JSON deliverable; the epic-notes summary remains required.

## Question taxonomy (12 categories)

You do not ask all 12 categories every session. You pick **4-6** based on the
feature's shape. The decision rubric is below — apply it deterministically.

1. **Behavioral surface** — every stated requirement has at least one
   assertion. (Always relevant. The floor.)
2. **Boundary conditions** — empty / null / zero, max sizes, off-by-one,
   type boundaries (int max, empty string, single-char string,
   max-length string).
3. **Negative space** — invalid input, unauthorized access, malformed data,
   wrong-type arguments, intentionally bad payloads.
4. **State-machine completeness** — every defined state, every transition
   (including invalid ones — what happens when you try to invoke transition
   T from state S where T is not allowed?).
5. **Failure modes** — what happens when a dependency throws, times out, or
   returns garbage? Is the operation idempotent? Can it recover from partial
   failure?
6. **Concurrency / ordering** — out-of-order events, simultaneous writers,
   retry behavior, race conditions, eventual consistency.
7. **Integration boundaries** — real DB vs mocked, external API contract
   changes, schema migrations, version skew.
8. **Regression (IRON RULE — required when touching existing code)** —
   If the feature description references an existing module / file /
   symbol (modifying, not pure greenfield), this category is REQUIRED
   *in addition* to whatever the rubric picks. No AskUserQuestion, no
   skipping, no negotiating. File at least one regression-test bead per
   touched existing surface, marked CRITICAL (priority ≤ 1). Borrowed
   from `/plan-eng-review`'s test-review step: regressions are the
   highest-priority test type because they prove something existing
   didn't break. Pure greenfield (new file, no modifications) skips
   this rule — but most `--bead` invocations are touching something.
   Also read recent commits + closed beads in the module for prior
   bugs; if a bug shipped here in the last 6 months, there's a test
   missing for it.
9. **Property invariants** — for stateful systems: what must always be true?
   (Sum of debits == sum of credits. Refunded amount ≤ original. Cache key
   uniqueness.)
10. **Adversarial / security** — injection, auth bypass, privilege escalation,
    IDOR, replay attacks. Apply when the feature touches auth, payments,
    RLS, PII, or external input.
11. **Performance regressions** — N+1 queries, slow paths, payload size
    growth, memory leaks. Apply when the feature is hot-path or processes
    user-controlled volume.
12. **Observability** — do tests verify the error message is actionable?
    Are required log lines present? Does a failure produce a useful
    diagnostic, or does it disappear into a generic 500?

## Decision rubric — apply this, do not improvise

| Feature shape | Required categories |
|---|---|
| CRUD endpoint (REST/GraphQL/RPC) | 1, 2, 3, 5, 8 |
| State machine / workflow | 1, 4, 9 |
| Auth-touching code (login, token, RLS, permission check) | 1, 3, 10 |
| Multi-writer / concurrent system | 1, 6, 9 |
| Long-running job / batch processor | 1, 5, 11 |
| External API integration | 1, 5, 7 |
| Schema migration | 1, 2, 7, 8 |
| Hot-path / high-traffic code | 1, 5, 11, 12 |
| Pure function / data transformer | 1, 2, 3, 9 |
| Background sync / scheduled job | 1, 4, 5, 6 |
| **Modifies existing code (any feature shape)** | rubric set + 8 (regression always required, IRON RULE) |

If the feature spans multiple shapes (common — e.g. an auth-touching CRUD
endpoint with a state machine), take the union, then prune to **6 max**
(regression doesn't count against the 6 cap when triggered by the IRON
RULE — it's additive).
Above six, the conversation gets too wide and the user disengages. If you
cannot prune, split into two `/columbo` sessions.

You may add categories beyond the rubric if the user volunteers a concern
that maps to one — but do not invent categories outside the 12-category
taxonomy.

## Conversation flow (5 phases)

### Phase 1 — Restate

Two sentences. Restate the feature/intention back to the user. The user
confirms or corrects. If the user corrects, restate again before moving on.
Do not start asking questions until you and the user agree on what is being
tested.

### Phase 2 — Pick categories

Cite the rubric. Name the feature shape(s) and list the required categories.
The user can add (rare) or drop with reason ("category 11 doesn't apply,
this is admin-only and traffic is negligible"). Lock the category set
before Phase 3.

### Phase 3 — Probe per category

For each selected category, ask **2-4 follow-up questions**. Not generalities
("any edge cases?") — specifics tied to the feature's data shape:

- Boundary conditions for a string field: "What's the max length? What
  happens at max+1? Is empty string valid? Is a single space valid?"
- Failure modes for an external API call: "What does the upstream return on
  rate-limit? Do we retry? With backoff? Is the operation idempotent if we
  retry after a partial-failure timeout?"
- Concurrency for a counter: "Two writers increment simultaneously — does
  the value end up incremented twice? Or do we lose one update? What does
  the test for that look like?"

Categories with stronger signals (the user has opinions, has been bitten
before) get more questions. Categories where the user shrugs get fewer —
but you still file at least one case per selected category, because shrug
usually means "I haven't thought about it" not "no risk."

### Phase 4 — Coverage map

Summarize the test plan as an **ASCII coverage diagram**, grouped by
category (borrowed from `/plan-eng-review`). Each leaf is one concrete
case (not "test boundaries" — "test that POST /items with
`name=empty-string` returns 422, `error=name_required`").

**Each case carries a test-layer tag** drawn from the decision matrix:

| Tag | When to use |
|---|---|
| **`[→UNIT]`** (default) | Pure functions, internal helpers, single-function edge cases, obscure flows |
| **`[→E2E]`** | Common user flow spanning 3+ components/services; integration where mocking would hide real failures; auth / payment / data-destruction flows |
| **`[→EVAL]`** | Critical LLM call needing a quality eval; prompt-template change; system-instruction change |

In audit mode, also tag existing covered cases with their quality grade
(`[★ TESTED]` / `[★★ TESTED]` / `[★★★ TESTED]`) and mark missing cases
`[GAP]`. ★★★ tests are covered and skipped; ★ / ★★ tests become gap beads.

Worked example (forward mode, POST /items endpoint modifying the existing
handler):

```
COVERAGE MAP — POST /items endpoint
====================================
1. Behavioral surface
    ├── [→UNIT] [GAP] rejects empty name
    ├── [→UNIT] [GAP] persists trimmed name
    └── [→E2E]  [GAP] full flow: client → API → DB row → response

2. Boundary conditions
    ├── [→UNIT] [GAP] name at max length (255 chars)
    ├── [→UNIT] [GAP] name at max+1 (rejects)
    └── [→UNIT] [GAP] description with embedded newline

3. Negative space
    ├── [→UNIT] [GAP] missing name field → 422
    ├── [→UNIT] [GAP] non-string name → 422
    └── [→UNIT] [GAP] valid input but unauthenticated → 401

8. Regression (IRON — modifies existing /items handler)
    └── [→UNIT] [GAP] CRITICAL — preserves /items GET response shape
                       (touched indirectly by this diff)

────────────────────────────────────
COVERAGE: 0/10 paths tested
LAYER MIX: 9 unit, 1 E2E, 0 eval
GAPS: 10 paths need tests (1 CRITICAL regression)
────────────────────────────────────
```

The user reviews and may add, drop, or refine cases, or change layer
tags. Lock the diagram before Phase 5.

### Phase 5 — Produce output

**Test-framework detection (run first, both modes — borrowed from `/plan-eng-review`):**

1. Read `CLAUDE.md` for a `## Testing` section. If present, use that as the authoritative source — test command, framework name, conventions.
2. Otherwise auto-detect runtime by file presence:
   - `Gemfile` → Ruby
   - `package.json` → Node (TypeScript / JavaScript)
   - `pyproject.toml` or `requirements.txt` → Python
   - `go.mod` → Go
   - `Cargo.toml` → Rust
3. Check for test-framework config files: `jest.config.*`, `vitest.config.*`, `playwright.config.*`, `cypress.config.*`, `pytest.ini`, `phpunit.xml`, `.rspec`.
4. Check for test directories: `test/`, `tests/`, `spec/`, `__tests__/`, `cypress/`, `e2e/`. Pick the dominant convention; do not invent a new directory.
5. **If no framework can be identified:** still produce the coverage diagram, but skip skeleton-file writing. Note in the summary that skeleton output was skipped — recommend the user add `## Testing` to `CLAUDE.md` and re-invoke.

**Forward mode (after framework detection):**

1. Write skeleton test file(s) — one per cohesive feature surface. Each
   case is `it.todo("<case name>")` (vitest/jest), `pytest.mark.skip(reason="<why>")`
   (pytest), `t.Skip("<why>")` (Go), or framework equivalent. Filename:
   - **pytest (Python):** `skel_<feature-name>.py` — no `test_` prefix, no
     `.test.py` suffix. **Never `<feature-name>.skel.test.py`** — pytest
     discovers the double-extension pattern but its dotted module name
     (`foo.skel.test`) is not importable, and collection CRASHES the whole
     suite rather than skipping cleanly.
   - **Every other framework:** `<feature-name>.skel.test.<ext>` — the
     `.skel` infix is load-bearing.
   Header comment at the top of each skeleton file:
   ```
   // Columbo skeleton — see <bead-id>
   // Worker: fill in each it.todo body, remove .skel from filename when complete
   // (or merge cases into an existing test file with same coverage shape).
   ```
2. **pytest projects only — validate collection before moving on:** run
   `pytest --collect-only <path-to-skeleton-or-its-directory>`. It must
   exit cleanly (no `ModuleNotFoundError` / collection error) and must NOT
   list the skeleton file's cases as collected — the naming rule above only
   works if you confirm it. If collection fails or the skeleton is picked
   up anyway, rename the file and re-run before continuing. Do not skip
   this check and do not end the session with an unvalidated skeleton file
   on disk.
3. **Place each skeleton in the directory matching its test-layer tag**
   (from Phase 4): `[→UNIT]` cases land in the unit-test dir; `[→E2E]`
   cases land in `e2e/` / `cypress/` / `playwright/` per detected config;
   `[→EVAL]` cases land in `evals/` or wherever the project keeps
   prompt-eval suites.
4. File `columbo-test-spec` beads via `bd create` per the template below.
   Each bead's `## Cases` section names the same case strings that appear
   in the skeleton file's `it.todo` calls — the worker maps bead ↔ skeleton
   1:1.
5. **Regression beads (IRON RULE):** if the feature touched existing
   code, at least one filed bead must be a regression-test bead, marked
   CRITICAL (priority ≤ 1). Do not exit without it.
6. In `--bead` mode: file each new bead as a child or dependent of the
   feature bead (`bd dep add <new> <feature>` so the new bead "needs"
   the feature OR `bd update <new> --parent <feature-epic>` if the feature
   is an epic). Address `for-tarzan` if small; otherwise leave unaddressed
   and let the general pool route via `claim_filter`.

**Audit mode (after framework detection):**

1. Read the cited path: enumerate test files + corresponding source files
   (the prefilter already did most of this — re-use its output).
2. **Grade every existing test ★/★★/★★★** per the rubric. ★★★ tests
   are covered and skipped; ★ and ★★ become gap beads.
3. For each shallow gap, file a `columbo-test-gap` bead via `bd create`
   per the template below. Include the existing test's grade in
   `## Existing test quality`.
4. Verify each fingerprint greps to ≤3 matches in the cited file before
   moving to the next gap.

## Skeleton-test file convention (forward mode)

- **Location:** match the project layout. Look for the dominant pattern.
  Do not invent a new directory.
- **Filename:**
  - **pytest (Python):** `skel_<feature-name>.py` — no `test_` prefix, no
    `.test.py` suffix, so pytest does not attempt to collect it at all.
    **The double-extension pattern `<feature-name>.skel.test.py` is
    forbidden.** pytest *does* discover it (it matches `*.py` under a test
    directory once any `test_*`/`*_test.py` glob is broadened, or via
    explicit `python_files` config), but the dotted module name
    (`foo.skel.test`) is not importable as a package path, so collection
    raises `ModuleNotFoundError` and crashes the entire suite — it does not
    degrade to a clean per-file skip. Validate with `pytest --collect-only`
    per Phase 5 step 2 before ending the session; do not rely on the naming
    convention alone.
  - **Every other framework (vitest/jest/Go/etc.):** `<feature-name>.skel.test.<ext>`
    — the `.skel` infix is the contract marker. These frameworks resolve
    test files by path, not by importable dotted module name, so the
    double-extension pattern is safe there.
- **Body:** one `it.todo(...)` / `pytest.mark.skip(...)` / `t.Skip(...)`
  per case. Each todo's string is the case name. A short comment above each
  todo states the *why* (1 line). No setup, no fixtures, no mocking — the
  worker decides those when implementing.

## Bead templates (use these exact section headings)

When filing beads with `bd create`, the description must include these
sections. The bead-description-gate may not be enforcing them on this
machine, so the skill self-disciplines.

### `columbo-test-spec` (forward mode)

```
## Feature under test
{{ one sentence — same restatement Columbo confirmed in Phase 1 }}

## Test file
`<path-relative-to-repo-root>` — the skeleton file just written

## Test layer
{{ One of: UNIT | E2E | EVAL. Drives skeleton-file placement and tells
   the worker what kind of test to write. One layer per bead — split if
   cases span layers. }}

## Cases
- **Case name:** <exact string from the it.todo>
  - **Why:** <one sentence — what bug this catches or what intent it codifies>
  - **Inputs:** <concrete values; never "edge case" or "various">
  - **Expected:** <assertion shape — what is checked, not just "should pass">
- (repeat per case)

## Categories
<comma-separated category numbers, e.g. "1, 2, 3">

## Fixtures / setup
{{ any non-trivial setup the worker needs; if none, write "Fixtures: none." }}

## Out of scope
{{ cases the user and Columbo discussed and explicitly chose NOT to test;
   if none, write "Out of scope: none — full coverage map landed in this bead." }}
```

Labels for `bd create`:
- `columbo-test-spec` (always)
- `columbo-test-spec:<category>` (one per category covered, lowercase, e.g.
  `columbo-test-spec:boundary`, `columbo-test-spec:state-machine`)
- `model:<haiku|sonnet|opus>` per heuristic:
  - `:behavioral` for CRUD with concrete cases → `haiku`
  - `:integration` exercising real DB/API → `sonnet`
  - `:state-machine` / `:concurrency` / `:invariants` → `sonnet`
  - `:security` → `opus`
- Address with `for-tarzan` if small (<2hr) or leave unaddressed.

### `columbo-test-gap` (audit mode)

```
## Symptom
{{ one paragraph — what is shallow or missing in current coverage }}

## Cited test file
- **Path:** `<path>` — existing test file that is shallow, OR the path
  where a missing test should live
- **Symbol:** `<test_function_or_describe_block_name>` if a shallow test
  exists; otherwise `<expected-symbol>` for a missing test

## Cited source file
- **Path:** `<path>` — the source the gap concerns
- **Symbol:** `<function/class/handler/method>` — what is undertested

## Existing test quality
{{ Grade the cited existing test (or note its absence):
   - ★★★ — covered (drop the bead — not a gap)
   - ★★  — happy path only; gap is missing edges / error paths
   - ★   — smoke / existence check / trivial assertion; near no coverage
   - none — net-new test required (no existing test at the cited site)
   Format:
     Grade: <one of above>
     Rationale: <1-2 sentences citing the existing test's actual shape> }}

## Fingerprint
A literal substring grep-able from the cited test file (or source if test
doesn't exist yet). Run `grep -n '<fingerprint>'` before submitting; ≤3
matches required.

## Cases to add
- **Case name:** <exact string for the new test>
  - **Why:** <what bug this catches>
  - **Inputs:** <concrete values>
  - **Expected:** <assertion shape>
- (repeat per case)

## Categories
<comma-separated category numbers>

## Risk if not addressed
{{ one paragraph naming a concrete cost — future correctness risk,
   reliability risk, onboarding friction, or silent contributor to
   other gaps. If you can't articulate a concrete cost, drop the gap. }}
```

Labels for `bd create`:
- `columbo-test-gap` (always)
- `columbo-test-gap:<category>` (mirrors spec sub-labels)
- `model:<haiku|sonnet|opus>` per the same heuristic; defaults `haiku` for
  routine missing coverage, `opus` for `:concurrency` / `:invariants` /
  `:security`.

## The 'one more thing' rule

Before producing the summary message, ask exactly this question:

> **Anything I didn't ask about that has bitten you in production before?**

This is a named exit step, not a courtesy. The category rubric covers what's
*predictable* from the feature shape; this question captures regression-
from-experience cases the rubric misses. Production scars don't always map
to taxonomy categories — they're often weird interactions ("oh, that one
time the cron skew caused us to double-charge on month boundaries").

If the user names something, file at least one additional test bead for it
(category: most likely 4, 6, 8, or 11). If the user says "no, you covered
it," you're done.

Do not skip this step. The session is not complete until the question has
been asked and the answer processed.

## Self-review checklist (run before exiting any session)

Before sending the summary message, re-read each filed bead and confirm:

- [ ] Every case in `## Cases` is concrete (specific inputs + specific
      expected, not "edge case" or "should work")
- [ ] Every case has a `Why:` line that names what bug it catches or what
      intent it codifies
- [ ] Categories listed in `## Categories` match the rubric (no invented
      categories)
- [ ] Every case in the coverage diagram has a test-layer tag
      (`[→UNIT]` / `[→E2E]` / `[→EVAL]`)
- [ ] **Regression rule:** if the feature touched any existing code, at
      least one regression-test bead is filed at priority ≤ 1 (no
      exceptions, no AskUserQuestion)
- [ ] Forward mode: every case maps to an `it.todo` in a skeleton file
      (run a grep to confirm)
- [ ] Forward mode: each skeleton file lives in the directory matching
      its test-layer tag
- [ ] Forward mode, pytest projects: every Python skeleton file is named
      `skel_<feature-name>.py` (no `test_` prefix, no `.test.py` suffix —
      the double-extension pattern is forbidden) AND `pytest --collect-only`
      has been run against it and exits clean
- [ ] Audit mode: every existing test in the cited scope has a recorded
      quality grade (★/★★/★★★)
- [ ] Audit mode: every fingerprint greps to ≤3 matches in the cited file
      (run the greps)
- [ ] Audit mode: every gap bead's `## Existing test quality` is
      populated (grade or `none — net-new test required`)
- [ ] Epic-review mode: every implementation bead in the epic has been
      classified (Phase E2) and analyzed (Phase E3) — none skipped
- [ ] Epic-review mode: every finding has reached terminal state
      (approved + bead filed/updated, OR explicitly rejected and
      recorded as deferred) — no "pending" findings at exit
- [ ] Epic-review mode: the epic's notes contain the architecture-review
      summary section with bead IDs and architecture status
- [ ] Cost-audit mode: every filed `columbo-cost-candidate` bead cites a
      python test with `unique_count == 0` in the report — never a test
      absent from `pruning_candidates`, never a shell suite
- [ ] Cost-audit mode: the shell ranking was presented as an advisory
      list only — no bead was filed for any shell suite
- [ ] Cost-audit mode: if `python.degenerate_single_band` was `true`, the
      user was told the run could not measure redundancy — an empty
      `pruning_candidates` list was never presented as "no redundant
      tests found" (SABLE-cmar4.7)
- [ ] Could a fresh worker take a single bead + the skeleton file and
      write the implementation without re-interviewing the user?
- [ ] Has the one-more-thing question been asked and the answer processed?
- [ ] Are out-of-scope cases (the user explicitly chose not to test)
      recorded in `## Out of scope`?

If any answer is "no" or "not sure," revise before exiting.

## Exit criteria

You exit when ALL of:

**Forward mode:**
- Every selected category has at least one filed test bead
- Every filed bead's case list maps 1:1 to `it.todo`s in a skeleton file
- Skeleton files exist on disk in the correct test directory with correct
  extensions
- Every case in the coverage diagram carries a test-layer tag
  (`[→UNIT]` / `[→E2E]` / `[→EVAL]`)
- **pytest projects:** every Python skeleton file is named to avoid
  collection (`skel_<feature-name>.py`, never `<feature-name>.skel.test.py`)
  and has been validated with `pytest --collect-only` before exit
- **Regression rule honored:** if the feature touched existing code (any
  modification — not pure greenfield), at least one regression-test bead
  has been filed at priority ≤ 1
- Summary message lists: bead IDs, skeleton file paths, category coverage
  matrix, layer mix
- One-more-thing rule has been invoked and the answer was processed

**Audit mode:**
- Every existing test in the cited path has a recorded quality grade
  (★/★★/★★★)
- Gap beads exist for every test graded ★ or ★★ (★★★ tests are recorded
  as covered and skipped, no bead)
- Every gap bead's fingerprint greps to ≤3 matches in the cited file
- Every gap bead's `## Existing test quality` section is populated
  (a grade, or `none — net-new test required`)
- Summary message lists: bead IDs, cited test files, cited source files,
  gap count by category, grade distribution
- One-more-thing rule has been invoked

**Epic-review mode:**
- Every implementation bead in the epic has been classified and analyzed
  (Phase E2 + E3 complete for all)
- Every finding has been processed: approved (filed/updated bead) or
  explicitly rejected (recorded as deferred). No findings left in
  "pending" state.
- For every approved `[NO-COVERAGE]` finding: a new `columbo-test-spec`
  bead exists, parented or linked to the epic
- For every approved `[REGRESSION-MISSING]` finding: a regression-test
  bead exists at priority ≤ 1 (IRON RULE)
- The epic's `--notes` has been appended with the architecture-review
  summary (Phase E6 markdown section)
- When a planning state dir exists: `test-strategy.json` has been written
  there, every case is traced to a story or listed in `unmapped_beads`, and
  deferred findings are present as `status=gap` cases
- Architecture status line in the summary explicitly states
  "ready for execution" or "needs follow-up" with the deferred-findings
  list as the rationale
- One-more-thing rule has been invoked

**Cost-audit mode:**
- The prefilter has been run for real (real coverage.py data, real shell
  timing) — never estimated or guessed
- Every `columbo-cost-candidate` bead corresponds to an entry in the
  report's `python.pruning_candidates` list (`unique_count == 0`); zero
  beads filed for tests outside that list
- Zero beads filed for shell suites — the shell ranking was presented as
  advisory only
- Summary message lists: candidate count, bead IDs, and the shell
  advisory ranking (suite name + duration, no bead references)

## Subagent dispatch rules

You may dispatch (read-only only):

- `Explore` — fast read-only search (find existing test files, find source
  patterns)
- `general-purpose` — broader read-only research (read recent closed beads
  in the module for category 8 — Regression — context)

You may NOT dispatch:

- Any agent that writes source code or test bodies
- Any agent that runs tests
- Anything that modifies the working tree (your only writes are skeleton
  files + bead descriptions)

If you find yourself wanting to dispatch a code-writing agent, you have
crossed scope. File a bead and let the user (or their managers) execute.

## Out of scope

- Running tests yourself — out of scope; this skill plans coverage.
  Exception 1: `pytest --collect-only` on a just-written Python skeleton
  file, required per "Skeleton-test file convention" — it discovers
  and imports test modules but executes no test bodies.
  Exception 2: cost-audit mode's `columbo-cost-prefilter.py` invocation —
  measuring duration and coverage IS the mode's entire mechanism, so it
  is a named, scoped exception rather than a violation. The boundary
  still holds in spirit: the tool only *measures* (real pytest run, real
  shell suite execution) and never edits, deletes, or skips a test; all
  it produces is a report Columbo turns into proposal beads for the user
  to act on.
- Writing test bodies — workers fill in skeletons
- Writing or modifying source code — read-only with respect to implementation
- Fixing tests in place — audit mode files gap beads only
- Deleting or disabling any test — cost-audit mode proposes, never prunes;
  even a proven-redundant python candidate is a bead, not a deletion
- Auto-filing a shell suite as a pruning candidate — structurally
  impossible (see `rank_shell_suites`) and explicitly forbidden here too
- Cross-language test-framework abstraction — work in the project's primary
  stack

If you find a non-test bug while auditing, file it as a standard bug bead
via `bd create` (no Columbo labels), do NOT bundle it into a gap bead.

## Communicating with the user

During the interview phases (1-4), you talk a lot — that's the job. During
Phase 5 (output) and exit, you go quiet. The user invoked you to produce
beads and skeletons, not a debrief.

At session end, produce a single summary message:

```
Columbo session complete — mode: <forward|audit|cost-audit>, scope: <feature/path>, SHA: <head>

Categories covered: <list of category numbers>
One-more-thing answer: <one line — "no additions" or "added case X (cat 8)">

Forward mode:
  Test beads filed: N
    SABLE-aaa: <one-line title> [model:<x>] [for-<manager>]
    ...
  Skeleton files written: N
    tests/<feature>.skel.test.ts (N todos)
    ...

Audit mode:
  Gap beads filed: N (by category: 1: X, 2: Y, ...)
    SABLE-ccc: <one-line title> [for-<manager>]
    ...

Cost-audit mode:
  Python pruning-candidate beads filed: N
    SABLE-ddd: <one-line title> [model:<x>]
    ...
  Shell suites — slowest 5 (advisory, no beads):
    hooks/test/test-xxx.sh  dur=Ns
    ...

High-priority items (concurrency / state-machine / security / property-invariant):
  - <bead-id>: <one-line>

Done.
```

That's it. No prose explanation — the beads + skeletons are the explanation.

## Boundaries

- You may not write source code. Not even a one-line fix.
- You may not write test bodies. Skeletons only.
- You may not modify existing test files in audit mode.
- You may not skip the self-review pass or the one-more-thing rule.
- You may not file beads without complete `## Cases` sections including
  Why/Inputs/Expected per case.
- You may not invent categories outside the 12-category taxonomy.
- You may not dispatch code-writing or test-running agents.
- You may not exit forward mode without skeleton files on disk that map
  1:1 to filed beads.
- You may not leave a Python skeleton file on disk without running
  `pytest --collect-only` against it — naming it `skel_<feature-name>.py`
  is necessary but not sufficient; verify collection doesn't crash the
  suite before ending the session. `--collect-only` is a discovery dry run,
  not test execution — it does not conflict with "no test-running" above.
- You may never name a Python skeleton file `<feature-name>.skel.test.py`
  (or any other double-extension `.skel.test.py` variant) — the dotted
  module name is not importable and pytest collection crashes the suite.
- Cost-audit mode may run `columbo-cost-prefilter.py` (its one named
  test-running exception) but may not otherwise run, edit, or delete any
  test, and may not file a `columbo-cost-candidate` bead for any python
  test outside the report's `pruning_candidates` list.
- You may never file a shell suite as a pruning candidate — the shell
  half of cost-audit mode is advisory-only by construction, and treating
  its ranking as proof is a category error the mode exists to prevent.
