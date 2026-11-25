---
name: fix-issue
description: Implement a GitHub issue through a verifier-first, self-correcting loop in an isolated worktree. Produces ship-ready code. Usage: /fix-issue <github-issue-number>
user_invocable: true
argument-hint: "<issue-number>"
allowed-tools:
  - Bash(gh issue view:*)
  - Bash(git remote get-url:*)
  - Bash(git branch:*)
  - Bash(git status:*)
  - Bash(ls:*)
---

## Live Context (loaded at invocation)

- **Issue**: !`gh issue view "$ARGUMENTS" --json number,title,body,labels,comments 2>/dev/null`
- **Repo remote**: !`git remote get-url origin 2>/dev/null`
- **Current branch**: !`git branch --show-current 2>/dev/null`
- **Working tree**: !`git status --short 2>/dev/null`
- **Project type**: !`ls Cargo.toml build.sbt package.json go.mod pyproject.toml 2>/dev/null || true`

---

# Fix Issue — Verifier-First Loop

**Guiding principle:** *A loop does not satisfy your goal — it satisfies the gate you wrote.*
A loop will cheerfully ship work that passes a weak gate and misses the intent (Goodhart's Law).
So the gate is designed **first**, **from** the acceptance criteria, and the failing tests are
written **before** any implementation. The objective verify pipeline — not a review agent's
opinion — is the source of truth for "done."

**The gate is a floor, not a specification.** Design the change (Phase 2.5) *before* designing its
gate, and implement that design in full — not just the slice the tests happen to pin down. This
ordering is deliberate and it is what separates this loop from incremental red-green TDD: an agent
told to write a test and then the minimal code to pass it makes locally-minimal decisions, locks
them in, and leaves anything untested unimplemented. Design → gate → implement keeps the upfront
architecture step that produces the better design, and still gets tests written before code.

Work through the phases **in order**. After every Verify failure or Review blocker, enter the
**Fix Phase** and return to Phase 5. The durable **run-log** is updated at the end of every
phase and every fix cycle, so the loop survives context compaction and stays auditable.
**Hard cap: 3 fix cycles.** If you exhaust them, emit the Remaining Blockers Report and stop —
never ship code that doesn't pass the gate.

## Model & Token Policy

Subagents inherit the session model unless pinned — on an expensive top-level model that
multiplies review cost ×4 per issue. **Always pass an explicit `model` to every Agent call**
per the table in each phase (broad exploration: Phase 2 → haiku; implementation: Phase 4 →
sonnet; review: Phase 6 → opus/sonnet; simplify: Phase 7 → haiku). Two phases are **never
delegated at all** — the design (Phase 2.5) and the gate (Phase 3) are the top-level model's
judgment, and they are what everything downstream is measured against. The objective verify pipeline
and the adversarial review — not the main loop's model horsepower — are what guarantee
correctness, so cheaper agents are safe wherever their output is re-verified. That is also why
the top-level model you *start* on matters most for cost: prefer the cheapest model that can
still run Phases 3 and 5 well (design the gate, diagnose failures), escalate only for
design-heavy issues, and lean on Phase-4 delegation to keep implementation drafting off the
top-level model.

Token discipline throughout the loop:
- **Filter command output at the source**: `| grep -E "test result:|error" | tail`, `grep -c`,
  never dump full `cargo test`/`clippy` output or whole files into context.
- **Long builds/tests run in the background** with a filtered result file; poll the summary.
- **Agents read the diff themselves**: pass the worktree path and `git -C <worktree> diff`
  instructions in the prompt — never paste the diff into the agent prompt.
- Targeted reads over full-file reads (`Read` with offset/limit, `sed -n 'A,Bp'`).

---

## Phase 0 — Understand & Init Run-Log

Parse the issue from the Live Context above. Derive:

1. **Change required** — one sentence, no more scope than stated
2. **Acceptance criteria** — enumerated; if the issue doesn't state them, derive from the description
3. **Out of scope** — adjacent issues you spotted but will NOT touch

Then **initialize the run-log** at `<scratchpad>/fix-issue-<N>.md` (template at the end of this
file), recording the issue summary and acceptance criteria. `<scratchpad>` is the session
scratchpad directory. Update this file at the end of every phase and every fix cycle — it is the
loop's durable spine.

If the issue is ambiguous on any acceptance criterion, ask one targeted question before
continuing.

**Model fit check (safety net).** The top-level model is fixed for this run — it cannot be
changed mid-loop. Judge the issue against the `/triage-issue` rubric (design-first → Fable;
mechanical/verbatim-spec → Sonnet; else → Opus). If this issue has an **open design decision**
(no clear approach, competing trade-offs, a new abstraction whose shape is a judgment call) and
you are NOT on Fable, say so in one line and let the user restart on Fable before you invest in a
worktree. Otherwise note the fit and proceed. (Run `/triage-issue <N>` *before* `/fix-issue` to
get this recommendation up front.)

---

## Phase 1 — Isolate (Worktree Setup)

**The user's checkout is never touched — not its files, not its branch.** All work happens in a
dedicated worktree, cut from the **remote base ref**, never from whatever the current checkout
happens to have checked out:

```bash
git fetch origin
git worktree add .claude/worktrees/issue-<N> -b <type>/issue-<N> origin/<base>
```

- **`origin/<base>` is mandatory, not decoration.** Omitting it branches from the current
  checkout's HEAD — so if the user left that on some unrelated feature branch, the fix silently
  inherits it and the PR carries someone else's commits. Branching from the remote ref makes the
  new branch independent of local state. `<base>` is the repo's default branch unless a
  base-branch rule says otherwise (see `/ship-issues` Phase 1b; a caller may pass one in).
- **Never `git switch` / `git checkout` / `git reset` in the main checkout.** It stays on whatever
  branch the user left it on. There is no reason to touch it: you branch from `origin/<base>` and
  work via `git -C <worktree>`. A local base branch being stale is irrelevant — you never read it.
- Choose the branch prefix from the issue labels per convention (`feat/`, `fix/`, `refactor/`,
  `test/`); default to `fix/`. Follow the repo's branch-naming rule if it has one (e.g. rift's
  `CLAUDE.local.md` mandates `<type>/rift-<issue>-<slug>`).
- Record the worktree path, branch name, and the base commit it was cut from in the run-log.
- **All** subsequent file edits, builds, tests, and git commands run with the worktree as the
  working directory. Prefer `git -C .claude/worktrees/issue-<N> ...` and run `cargo`/`sbt`/`npm`
  with that directory as the working directory — avoid bare `cd` (it can trigger a permission
  prompt).
- **If `worktree add` fails, STOP — do not fall back to the current working tree.** Falling back
  writes the change into the user's checkout, which is the one outcome this phase exists to
  prevent; a "degraded isolation" note does not make that acceptable. Diagnose the specific cause
  and fix it:
  - *branch already exists* → reuse the existing worktree if it is this issue's (check
    `git worktree list`), else pick the next free name or delete the stale branch;
  - *worktree path already exists* → `git worktree remove <path>` if it is a leftover from a
    merged run, else use a fresh path;
  - *not a git repo* → report that and stop; there is nothing to isolate and nothing to PR.
- After the PR merges, clean up: `git worktree remove .claude/worktrees/issue-<N>`.

---

## Phase 2 — Locate

Before writing code, find the exact targets. Choose by scope:

- **Targeted lookup** (you know the symbol/file): inline `git grep -n "<symbol>"` — cheap,
  keep it in the main loop.
- **Broad exploration** (unfamiliar subsystem, many candidate files, naming conventions
  unknown): delegate to an **`Explore` agent with `model: haiku`** and ask for a structured
  map (files → roles → key symbols). This keeps file dumps out of the expensive main context;
  you need the conclusions, not the excerpts.

Identify and record in the run-log:
- Files to modify (be specific; list them)
- Existing utilities/functions to reuse — do not introduce abstractions when something already exists
- Test file(s) to add or extend

If a file is not in that list, do not touch it.

---

## Phase 2.5 — Design (before the gate, before the code)

**Decide the shape of the change here, in one pass, while nothing is committed to yet.** This
phase exists because the alternative is deciding it implicitly — one assertion at a time, inside
Phase 3 — and decisions made that way are locally minimal, never revisited, and silently cap what
Phase 4 builds. Design is also the cheapest thing in this loop to redo: it is prose in the
run-log, not a diff.

Record in the run-log, before writing a single test:

0. **Design of record (only when the repo has the design-sync practice** — `scripts/design-check.py`
   exists or CLAUDE.md/AGENTS.md declares `design-check: <path>`; otherwise skip this item).
   Run `python3 <design-check> --diff <worktree>` and read every decision (`D-n`) and section it
   lists under CODE → DESIGN, plus `docs/decisions/DECISIONS.md` entries for the area. Write in
   the run-log: `design: D-…, RFC-… §… read; premise ok` — or, if the issue's premise
   contradicts a decision, **stop here** and settle it with the user (fix the issue text, or
   amend the decision in this PR). Issues have been wrong at the intent level with every fact in
   them true; the register is what a premise is checked against, not the issue's prose. If the
   design leaves the choice open, decide it below and treat the outcome as a decision to
   *record* (`/design-sync record`) — a `D-n` with a callout, a code citation and a test pin, in
   this PR.
1. **Data & state model** — the types this change introduces or alters. Make invalid states
   unrepresentable; prefer a newtype/`opaque type` over a bare primitive; prefer an `enum`/ADT
   over a boolean pair. Name each type and its invariant.
2. **Error model** — every way this can fail, and which channel carries it (typed error vs defect,
   `thiserror` vs `anyhow`, `IO[E, A]` vs `Task`). Name the failure modes explicitly; the ones you
   do not name here are the ones that get swallowed in Phase 4.
3. **Contracts** — for each new or changed public function: inputs, output, preconditions,
   what it guarantees. One line each.
4. **Boundaries** — which module each piece lands in, and why that one. Reuse the Phase 2
   `reuse:` list; if you are adding an abstraction, say what existing thing was insufficient.
5. **Edge cases** — enumerate them: empty/zero/boundary inputs, concurrent access, partial
   failure, ordering. This list is an input to Phase 3, and it is normally *longer* than the
   issue's acceptance criteria. Criteria say what a person asked for; this says what the code
   must survive.

Rules for this phase:

- **Stays in the main loop.** You may spawn an `architect` agent (`model: sonnet`) to lay out
  *options* on a genuinely open design question, but the decision and the written design are
  yours — this is the judgment the top-level model is being paid for.
- **Design the issue, not a platform.** Scope is still exactly what Phase 0 recorded. An upfront
  design step is not an invitation to generalize; it is how you avoid re-deciding the same thing
  five times at assertion granularity.
- **If the design surfaces an open question the issue does not settle** — competing approaches
  with real trade-offs, a new abstraction whose shape is a judgment call — stop and ask it now,
  per the Phase 0 model-fit check. Answering it after the tests are written costs a rewrite of
  the gate too.
- **Keep it short.** Five headings, a few lines each. A design longer than the diff it describes
  is a smell.

---

## Phase 3 — Gate Spec (Verifier-First)

**This is the core of the loop. Design the verifier before the implementation.**

The gate is derived from **two** sources, not one: the Phase 0 **acceptance criteria** and the
Phase 2.5 **edge cases**. Criteria alone produce a thin one-test-per-bullet gate that tracks what
was asked for and misses what the code has to survive.

For **each** acceptance criterion *and* each Phase 2.5 edge case, define a concrete,
machine-checkable check:
- a **named test** to write (preferred), or
- a command whose output objectively proves it.

Record the criterion/edge-case → check map in the run-log. This is the contract the implementation
must satisfy — a floor, not a ceiling (Phase 4 implements the whole design, not just this).

**Then write the tests first** — before any production code:
- Unit tests: `#[cfg(test)] mod tests` in the same file (Rust) or `object XSpec extends ZIOSpecDefault` (Scala)
- Integration tests: `tests/` directory when end-to-end behaviour must be verified
- Cover the happy path, the Phase 2.5 failure modes, and the Phase 2.5 edge cases

**No tautological tests.** A test states its expected value **literally**. It must never compute
the expectation by calling the code under test, by re-implementing that code's algorithm in the
test body, or by round-tripping through the thing being verified (`assert_eq!(parse(s),
parse(s))`, `expected = format(x)` then asserting `format(x) == expected`). Such a test passes
against any implementation, including a wrong one, and writing it before the code does **not**
prevent it — it is the failure mode that survives test-first discipline. Round-trip properties are
legitimate only as a *supplement* to literal-value tests, never as the sole check for a criterion.

Run the new tests and confirm they **fail for the right reason** (red). Record the **verbatim
failure output** in the run-log — the assertion message, expected-vs-actual, or the compile error
— not the word "red". A test that passes before you've implemented anything is not exercising the
criterion; and a red you did not read is only evidence that you ran the suite, not that the test
discriminates. If the red is a bare compile error because the API does not exist yet, that is
normal — note it as such, and re-confirm the assertion actually discriminates once it compiles.

**You own the gate.** The tests are designed and written here, in the main loop — this is the
quality-critical judgment and is never delegated. Whoever writes the *implementation* (you, or a
delegated agent in Phase 4), the gate tests must not be weakened, deleted, or edited downstream
to make code pass. If an implementer thinks a test is wrong, it reports back and the main loop
adjudicates.

Production rules (from CLAUDE.md) that govern everything you write from here:
- No comments unless the WHY is non-obvious (a hidden constraint, surprising invariant, workaround)
- No `.unwrap()` / `panic!` / `todo!` in production code paths (Rust)
- No error swallowing — failures must propagate or be explicitly handled
- No over-engineering — solve the stated problem, not hypothetical future requirements

---

## Phase 4 — Implement

Implement the **Phase 2.5 design in full**, and turn the Phase 3 tests green.

**The gate is the floor, not the ceiling.** Do not write the minimal code that satisfies the
tests: the tests are a sample of the design, and code shaped to pass exactly that sample leaves
every unsampled behaviour — an unhandled error variant, an edge case whose test was harder to
write, an invariant the type system was supposed to carry — quietly unimplemented, with a green
pipeline reporting success. Every element of the Phase 2.5 design ships: the types and their
invariants, every named failure mode routed to its channel, every contract honoured.

**Scope is still the issue, not the gate.** "Implement the design fully" is not licence to
broaden: the design was itself scoped to Phase 0's change-required in Phase 2.5, and nothing
outside it gets built here. If implementing the design reveals it was wrong, fix the design in
the run-log and say so — do not silently diverge from it.

**Delegated implementation (default for mechanical work; quality-neutral by construction).**
The loop's quality guarantee is the gate (Phase 3, main-loop-owned) plus adversarial review
(Phase 6, opus/sonnet) — not the drafting model. So making the red tests green may be delegated
to a **`general-purpose` (or your `developer`) agent on `model: sonnet`** with no effect on what
ships, *provided the guardrails below hold*. Decide per issue:

- **Delegate** when the work is mechanical against a well-formed gate **and a written Phase 2.5
  design**: clear target list, the approach is settled, changes are localized. The design is what
  makes delegation safe here — it is the part a cheaper model would get wrong, and it is already
  decided.
- **Keep in the main loop** when the issue is design-heavy, cross-cutting, or the approach is
  still unsettled — there the main loop's judgment is the value, and delegation would risk it.
  (Record which mode you chose in the run-log.)

The delegation brief must be self-contained — the agent has none of this conversation's context:
- the worktree path (all edits happen there; never touch files outside the Phase 2 target list);
- the run-log's Change-required, Acceptance-criteria, Targets (files to modify, utilities to
  reuse — so it doesn't reinvent existing abstractions), **and the full Phase 2.5 Design section**
  (types, error model, contracts, boundaries, edge cases) — verbatim, since the design is what it
  is implementing;
- that it implements **the design**, not the minimum that passes the tests: every named failure
  mode and edge case is handled even where no test pins it down;
- that the **gate tests already exist and are immutable** — it writes production code to make
  them pass and must NOT weaken, delete, or edit any test (if one looks wrong, report back);
- the production rules (no `unwrap`/`panic!`/`todo!`, errors propagate, comments only for a
  non-obvious why, no over-engineering);
- ask it to return the list of files changed + a one-paragraph summary, NOT a full diff.

**After the agent returns, the main loop reads the diff itself** (`git -C <worktree> diff`) before
Phase 5 — mandatory, not optional: the main loop must understand the implementation to triage
review findings and write surgical fixes. The Fix Phase always stays in the main loop and is
never re-delegated (fixes are context-dependent). Phases 5–8 are unchanged: the same objective
pipeline and the same opus/sonnet review gate the delegated code exactly as they gate your own.

---

## Phase 5 — Verify (objective gate = source of truth)

Auto-detect project type and run the **full** pipeline, with the worktree as the working
directory. Do not skip steps.

**Rust** (`Cargo.toml` present):
```bash
cargo fmt                        # auto-fix; never block on fmt alone
cargo clippy -- -D warnings      # must produce zero warnings
cargo test                       # all tests pass, including the Phase 3 gate tests
cargo deny check                 # run only if deny.toml exists
```

**Scala** (`build.sbt` present):
```bash
sbt compile
sbt scalafmtCheckAll
sbt test
```

**Node / TypeScript** (`package.json` present):
```bash
npm run lint 2>/dev/null || npx tsc --noEmit
npm test
```

The Phase 3 gate tests must now be green. Record the result in the run-log.

Run every step with **filtered output** (e.g. `cargo clippy ... 2>&1 | grep -cE "^(error|warning)"`,
`cargo test ... 2>&1 | grep -E "test result:|FAILED"`); only on failure re-run the failing step
with enough context to diagnose. Full pipeline output belongs in a file, not in context.

**Outcome:**
- All steps pass → **Phase 6 (Review)**
- Any step fails → note every failure → **Fix Phase** → return to Phase 5

---

## Phase 6 — Review (advisory checker layer)

Spawn these agents with the Agent tool, **in parallel** (one message, multiple Agent calls).
Point each agent at the worktree and tell it to run `git -C <worktree> diff` itself — do not
paste the diff into the prompt. **Pin each agent's `model` explicitly** (they otherwise
inherit the session model, multiplying cost):

1. **`pr-review-toolkit:code-reviewer`** — `model: opus` — changed files, CLAUDE.md compliance,
   correctness bugs. Deep-reasoning verification (locking, semantics parity, merge-resolution
   correctness) — the one agent that earns a strong model.
2. **`pr-review-toolkit:silent-failure-hunter`** — `model: sonnet` — catch blocks, fallback
   logic, `unwrap_or`, `getOrElse`, error-swallowing patterns; instruct it to compile-check
   non-default feature sets (`--no-default-features`) when cfg-gated code changed. Skip if the
   diff contains no error handling code. (Not haiku: this agent's findings are historically
   the highest-severity — cfg-scope breaks, masked failures — and need real reasoning.)
3. **`pr-review-toolkit:pr-test-analyzer`** — `model: sonnet` — do the gate tests actually
   cover every acceptance criterion **and every Phase 2.5 edge case and failure mode** (pass it
   both lists)? Are there tautological tests — ones whose expectation is computed by the code
   under test, or that would pass against a wrong implementation? Ask it explicitly; that class
   survives test-first discipline and is invisible to a coverage number.
4. **Language best-practices / anti-pattern lens** — `general-purpose`, `model: sonnet` — idioms,
   anti-patterns, and code style graded against the repo's **language skill**, NOT correctness
   (that's agent #1). The other three agents catch bugs, swallowed errors, and coverage gaps but
   none enforce language idiom, so this is the pass that keeps the diff *idiomatic*, not just
   correct. The brief MUST tell the agent to invoke the matching skill via the Skill tool **first**,
   then review the `git -C <worktree> diff` against it. Pick the skill by the diff's file types:
   - `.rs` → `/rust-best-practices` (error-handling idioms, ownership/borrowing, newtypes,
     `unwrap`/`clone` overuse, `#[must_use]`, `thiserror` vs `anyhow` at boundaries)
   - `.scala` / `build.sbt` → `/scala3-best-practices` (⁠`opaque type` vs `AnyVal`, `given`/`using`
     vs `implicit`, `enum` vs sealed hierarchies, visibility); **also** `/zio-best-practices` when
     the diff touches `zio.*` (Service Pattern 2.0, typed errors, `Cause`/`Exit`, `Schedule`), and
     `/fp-patterns` for typeclass/ADT/effect-composition design
   - other languages → idiomatic judgment, noting no skill was available
   Same Blocker/Non-blocker classification as the others; **style-only nits are Non-blockers**
   unless they also violate a CLAUDE.md rule. Skip this agent for trivial no-logic diffs (pure
   docs/config, or a one-line mechanical change).

The verify pipeline is the objective gate; review findings are **advisory**. Classify:

| Class | Criteria | Action |
|-------|----------|--------|
| **Blocker** | Confidence ≥ 80 (Important or Critical) from any agent | Must fix |
| **Blocker** | An acceptance criterion has no covering test | Must fix |
| **Blocker** | A Phase 2.5 failure mode or edge case is unimplemented, or a test is tautological | Must fix |
| **Non-blocker** | Confidence < 80 (Suggestion) | Log; apply only if trivially safe |

**Gate check:**
- Zero Blockers → **Phase 7 (Simplify)**
- Any Blocker → **Fix Phase** → return to Phase 5

---

## Fix Phase

Triggered by: Phase 5 failure or Phase 6 Blocker.

1. Append a cycle entry to the run-log: `cycle N — <blockers found> → <fixes applied>`, one line
   per fix (`fixed: <what> in <file>`).
2. Fix **all** open blockers (verify failures + review blockers) in one pass — no partial fix
   followed by re-verify.
3. **No scope expansion**: fix the gate's failures, do not broaden the change.
4. Increment the cycle counter (you started at 0). Return to **Phase 5**.

**If this was the 3rd failed cycle** (counter = 3): stop. Do not enter Phase 7. Emit the
Remaining Blockers Report (end of file) and stop.

---

## Phase 7 — Simplify

Spawn **`pr-review-toolkit:code-simplifier`** — `model: haiku` — pointed at the worktree diff
(it reads the diff itself). Haiku is safe here: its suggestions are triaged by the main loop
and every applied one is re-verified by the full pipeline, so a bad suggestion cannot ship.
Instruct it to return a ranked list (file, location, before → after) and NOT to apply edits.
Apply suggestions that:
- Reduce lines without changing behaviour
- Improve naming clarity
- Remove duplication

After applying, re-run the verify pipeline (Phase 5) to confirm no regression.

---

## Phase 8 — Ship Report

Output this block when the gate passes:

```
## Ship-Ready: Issue #<N> — <title>

### Worktree
- Path: .claude/worktrees/issue-<N>
- Branch: fix/issue-<N>

### What changed
- <bullet — one line per meaningful change>

### Design
- <one line per Phase 2.5 decision that shaped the diff>
- Design: unchanged — <docs/decisions the diff cites>, confirmed | amended — D-n (<one line>) | n/a — <why>
  (mandatory line when the repo has design-sync; copy it into the PR body; `design-check --strict` must pass)

### Acceptance criteria + edge cases → gate
- [x] <criterion 1> — covered by test `<test_name>`
- [x] <edge case 1> — covered by test `<test_name>`

### Verification
| Check               | Result                          |
|---------------------|---------------------------------|
| fmt / scalafmt      | PASS (auto-fixed if needed)     |
| clippy / compile    | PASS — zero warnings            |
| tests               | PASS — N total, M new           |
| code-reviewer       | PASS — no blockers              |
| silent-failures     | PASS / SKIPPED (no error code)  |
| test coverage       | PASS — criteria + edge cases    |

### Fix cycles used: N / 3
### Run-log: <scratchpad>/fix-issue-<N>.md

### Next step
Run /commit-commands:commit-push-pr from the worktree (.claude/worktrees/issue-<N>).
After merge, clean up: git worktree remove .claude/worktrees/issue-<N>
```

---

## Remaining Blockers Report (when 3 cycles exhausted)

```
## Blocked After 3 Fix Cycles — Issue #<N>

### Unresolved issues
1. [source: clippy/test/code-reviewer/...] <description> — <file:line>
2. ...

### Cycle history (from run-log)
- Cycle 1: <summary>
- Cycle 2: <summary>
- Cycle 3: <summary>

### Worktree (left in place for inspection)
- Path: .claude/worktrees/issue-<N>   Branch: fix/issue-<N>

### Recommended next step
Manual investigation required. The blockers above need human judgement
before this change is ship-ready.
```

---

## Run-Log Template

Write this to `<scratchpad>/fix-issue-<N>.md` in Phase 0 and update it every phase / cycle:

```markdown
# Run-Log: Issue #<N> — <title>
worktree: .claude/worktrees/issue-<N>   branch: fix/issue-<N>

## Targets
- files: <list>
- reuse: <existing utilities>

## Design (Phase 2.5 — written before any test)
- types & invariants: <...>
- error model / failure modes: <...>
- contracts: <fn> — <in> → <out>, guarantees <...>
- boundaries: <module> because <...>
- edge cases: <enumerated>

## Acceptance criteria + edge cases → gate
- [ ] <criterion or edge case> → test `<name>` (red output: `<verbatim failure line>`)

## Cycles (budget 3)
- cycle 0: verify=<pass/fail> review=<blockers>  fixes: <...>

## Status: <in-progress | ship-ready | blocked>
```

---

## Hard Constraints

- **Do not create a PR** and **do not push** — the ship report is the handoff; the user runs
  `/commit-commands:commit-push-pr` from the worktree.
- **All work happens in the worktree — always, with no fallback.** Cut it from `origin/<base>`, never
  from the current HEAD. If the worktree cannot be created, stop and say why; never write the change
  into the user's checkout instead.
- **Never move the user's checkout.** No `git switch`/`checkout`/`reset`/`merge` outside the
  worktree — their working directory stays on whatever branch they left it on, with whatever
  uncommitted work is in it. `git fetch` is the only git write the main repo ever needs, and it only
  touches remote refs.
- Update the run-log every phase and every cycle.
- **Do not modify** files outside the Phase 2 list.
- **Do not add features** beyond what the issue states.
- **Stop at 3 cycles** — surface blockers instead of shipping a failing gate.
- **One issue at a time** — note adjacent issues found; do not fix them.
