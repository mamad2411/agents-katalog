---
name: slicewise
description: A disciplined loop for implementing, fixing, refactoring, or unblocking a single feature or slice in an existing codebase. Reads the relevant docs/specs first and reports drift before coding, splits work into small file-disjoint commit units, and for each unit runs a build/test gate then dispatches two independent reviewers in parallel and reconciles their findings before handing off a commit you run yourself (it never auto-commits). Use when the user says things like "implement this feature", "add this API", "fix this bug", "refactor this", "finish this slice", or "this PR/merge is stuck". Not for one-line typo fixes (answer directly), and not for the initial mass-scaffold of an entire API layer (use a fan-out authoring harness instead).
---

# slicewise

The everyday discipline for building **one slice at a time** in an existing codebase. You write the
code yourself, but every commit unit is objectively verified — a full test gate plus two independent
reviewers reconciled against each other — and the human, not the agent, decides what lands.

한국어 안내는 [README.ko.md](https://github.com/pjw81226/slicewise/blob/main/README.ko.md)를 참고하세요.

## Principles (non-negotiable)

1. **No auto-commit.** You never run `git commit`. You hand the user exact, file-disjoint `git`
   blocks and they run them, on a **fresh branch** for the current issue. (Only commit yourself if the
   user explicitly says "commit it" / "do it".)
2. **Always dual review.** Every commit unit is reviewed by **two independent reviewers in parallel**,
   then reconciled. No risk-based gating — the small unit that "looks trivial" is where the subtle bug
   hides. If only one reviewer is available, run it and **warn** that this invariant is relaxed.
3. **Tests are the ground truth.** A build/compile floor for every unit; the full suite green before
   anything lands. Risky changes get **real integration tests, not mocks or fakes**.
4. **No scope creep.** Only the current issue. Anything outside the plan — extra features, new
   dependencies, edits to unrelated files — you **ask first**.

## Checklist (make each a todo)

1. Read first, report drift.
2. Plan file-disjoint commit units.
3. Implement → test gate (per unit).
4. Dual review → reconcile (per unit, always).
5. Re-verify → commit handoff.
6. Doc sync + drift sweep.
7. PR / merge unblocking (only if you hit it).
- (cross-cutting) Log reusable troubleshooting the moment you hit it.

## Configuration

Read `.slicewise.yml` (or `.json`) at the repo root if present; otherwise **auto-detect** the
toolchain from the ecosystem. See `docs/configuration.md` for the schema and the detect table. The
keys you care about: `build`, `test`, `integration`, `lint`, `docs` (globs to read in Phase 1),
`reviewers` (the roster for Phase 4), `troubleshooting_log`, `commit_convention`. When a key is
absent, detect it (package.json→npm, Cargo.toml→cargo, go.mod→go test, pom.xml/build.gradle→mvn/gradle,
pyproject.toml→pytest, Makefile→make) and **state what you detected** so the user can correct you.

## Phase 1 — Read first, report drift (before any code)

- Read the configured `docs` globs (default: `docs/**`, `**/*.md`, plus any OpenAPI/schema/ADR files),
  the related code, and any design notes for this slice. Understand the contract before touching it.
- **Drift detection is a first-class deliverable.** If two docs disagree, or a doc contradicts the
  code (a spec that no longer matches the schema, a data model that drifted from the migration), you
  **report it and get a decision before writing code.** Silently "fixing" it the wrong way is the
  classic trap.
- State scope in one line: what you will build, and what is explicitly out of scope.

## Phase 2 — Plan file-disjoint commit units

- Split the work into small units whose file sets **do not overlap** (e.g. infra/port · domain logic ·
  docs). If one file is touched by two units, merge them into one unit.
- For genuinely hard logic (auth/social login, pairing, IoT, RAG, aggregation, external integrations),
  lay down the skeleton with `// TODO(impl)` markers and fill it in deliberately — don't fake it.

## Phase 3 — Implement → test gate (per unit)

- Write it yourself, matching the surrounding style. Cross-context references go by ID; external
  systems go through a port/adapter, not a direct call.
- Run the **build/compile floor** (`build` command). It must pass — that's the floor, not the goal.
- For **risky changes**, add real integration tests, not mocks: raw SQL / complex queries, JSONB or
  document mapping, concurrency and locking, migrations, money, auth/authorization, anything with a
  data-loss or ownership-boundary failure mode. Assert hard — exercise boundary values, ownership
  checks, time/ordering — so a false green can't sneak through.
- Before the unit is final, run the **full `test` suite** and confirm it is green (failures = 0).

## Phase 4 — Dual review → reconcile (per unit, always)

**Dispatch the reviewer roster in parallel, in one message.** All reviewers are **read-only** (they
report; they never edit). The zero-config default roster is the bundled `code-reviewer` agent run
**twice with different lenses**:
- **Lens A** — correctness, security, concurrency / data-safety.
- **Lens B** — simplicity / DRY, project conventions, test adequacy.

For cross-model diversity, set `reviewers: ["codex", "code-reviewer"]` in config to use one Codex
reviewer (via the `codex` plugin, if installed) plus one Claude reviewer. If a configured reviewer
isn't available, degrade to single and **warn** that the always-dual-review invariant is relaxed.

Shared prompt template (same for every reviewer, only the lens differs):
- **Target:** the `git diff` of the working tree + the list of changed/new file paths + a couple of
  reference files showing the pattern to match.
- **Design context:** state the decisions that are already settled, so reviewers check *consistency,
  bugs, and security within that design* instead of re-litigating the architecture.
- **Output contract:** prioritized findings — 🔴 must-fix / 🟡 should-fix / 🟢 nit — each with
  `file:line` and a concrete fix. Explicit instruction: *"If it's sound, say it's sound. Do not
  fabricate issues."*
- **Scrutiny points:** data loss, JSONB/serialization mapping, IDOR / authorization, concurrency
  TOCTOU, migration safety, test adequacy, doc↔code consistency.

**Reconcile (this step is the whole point).** Compare the two reports; don't just concatenate them.
See `docs/reconcile-rubric.md` for the full decision table. In short:
- 🔴 → **verify it's real, then apply, then prove the fix with a new test.** If the two reviewers
  disagree, resolve by evidence, not by vote.
- Over-engineering / speculative asks → **reject with a stated reason** (name the rejection as
  explicitly as the adoption). "Deterministic key, so a per-segment HEAD check is unnecessary — rejected."
- Every adopted fix is reflected in code **and** proven by a test that would fail without it.

## Phase 5 — Re-verify → commit handoff

- After applying reconciled fixes, run the `test` suite again — green.
- **Do not commit.** Present numbered, **file-disjoint** blocks:
  ```
  git add <exact paths for this unit>
  git commit -m "<conventional subject>" -m "<body>"
  ```
  Add a trailer (sign-off, issue ref, co-author) only if the project already uses one. The user runs
  the blocks. If they say "do it", then you run them.

## Phase 6 — Doc sync + drift sweep

- If behavior or a contract changed, update the docs it touched (endpoint schemas, error cases,
  status, ER diagrams, counts/summaries).
- **Sweep the mirrors:** when you change one field/column, `grep` for its old name across every doc
  and generated artifact (overview docs, exported schema JSON, SVG diagrams) so no straggler survives.
  Mark generated artifacts (SVGs, etc.) for regeneration. Historical changelog lines are history —
  leave them.

## Phase 7 — PR / merge unblocking (only if you hit it)

- Classify the blocker: `gh pr view <n> --json mergeable,mergeStateStatus,reviewDecision` →
  CONFLICTING (conflicts) / UNSTABLE or BLOCKED (checks) / review.
- For conflicts: merge `origin/<base>` in, resolve **only** the conflicts (union / consistency),
  confirm zero markers, and get the **whole merge tree green** before handing off the push.
- For count/summary conflicts, recompute from the underlying groups and reconcile to the true number.

## Cross-cutting — Troubleshooting log

When you hit a real troubleshooting trap (build, test, runtime, or a design pitfall), append it to the
configured `troubleshooting_log` (default `TROUBLESHOOTING.md`). **Create it if missing; append to the
bottom if it exists — never a fresh file each time.** Format each entry as: a one-line title (date +
feature/branch), then **Cause / Resulting problem / Fix / Alternatives considered**. Record only
reusable traps, not one-off typos — this is an accumulating asset so the next person doesn't hit the
same wall.

## Tooling notes

- Reviewers see uncommitted work via `git diff` (assume a clean baseline before the unit).
- Codex unavailable → single Claude reviewer + a stated note that the full-review invariant is broken.
- `build`/`test`/`lint` and `gh` run via Bash. Prefer the repo's own scripts over ad-hoc commands.
- If a decision won't show up in a later code scan (a design fork, a rejection rationale, a schema
  switch), write it down where the project keeps such notes so it isn't lost.
