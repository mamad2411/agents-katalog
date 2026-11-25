---
name: improve-tests
description: "Cut a test suite to the tests that catch real bugs and its run time to the minimum: measure first, delete or demote low-value tests, fix slow setup, and prove every cut keeps the checks that matter."
argument-hint: "[path or area of the test suite]"
disable-model-invocation: true
license: MIT
---

# Improve Tests

Measure a test suite, find the tests that cost time and catch nothing, find the setup that wastes time, and cut both. The goal is the shortest run that still catches the bugs this project actually makes. Starts from a measured baseline and an assessment: if the suite is already lean, say so and stop.

Test files are the target, so editing and deleting them is expected. Production code changes only where a test needs a seam (Step 7), and only as the approved plan names it. If a cheap test is impossible because module boundaries are wrong across several modules, that is architecture work: say so, and tell the user to run `/improve-architecture` in Claude linked installs or Cursor, `/supermatt:improve-architecture` from the Claude plugin, `$improve-architecture` in Codex, or `/skill:improve-architecture` in OMP.

## Principles

Every step applies these. Findings cite them by name.

- **Name the break.** A test earns its place by the break it catches: a realistic change to production code that turns it red. A test with no nameable break costs time and catches nothing. Test as little as reaches the confidence the project needs, and spend tests where the project goes wrong: complicated conditionals, money, security, code with a bug history.
- **Our data, not their library.** Where our code hands work to a library (PDF, email, image, chart, spreadsheet, HTTP client, ORM, framework router), the library owns the rendering and has its own tests. Our claim is the data we hand it. Build that data in a plain function or object (the document model, the template variables, the request payload) and assert on it in a fast test. Keep one smoke test per adapter that the real library accepts our data: the call does not raise, and the output is valid (a PDF starts with `%PDF`). A test that renders a full PDF to check an invoice total pays for the renderer to test the library.
- **Cheapest level.** Every claim sits at the cheapest level that still keeps its failure mode. In-memory logic goes in unit tests. A high-level test (request, system, browser, e2e) keeps only what nothing lower can catch: wiring, configuration, one happy path per critical user flow. When a high-level test and a lower one check the same claim, the high-level check goes.
- **Observable behavior.** A test asserts outputs and state at a public boundary, so it survives a refactor that keeps behavior. A test that fails on such a refactor is a false alarm, and false alarms train people to ignore red. Mock only what others can observe (an email sent, a third-party API, a message queue). Use the real version of what only this app touches (its own database), or a fast fake.
- **Evidence over coverage.** Line coverage shows a line ran, not that anything checked it: deleting tests while keeping line coverage can still lose bug detection. Rank the evidence that a claim stays covered: a mutation run (no mutant loses its only killer), then a read of the other test's assertion, then line coverage. A test that has never failed is not proof of no value: it can be the only guard of a rare break.

## Guardrails

1. **The default verdict is Lean.** A suite with a few slow tests is not a problem. Do not invent cuts.
2. **Never remove the only guard of a claim we own.** Every deletion names where its claim stays covered, or why the claim is not ours (library behavior, trivial code).
3. **Keep list.** These stay unless the user says otherwise: regression tests tied to a bug or incident, contract tests at a service boundary, tests of error text or formats that consumers rely on, property and invariant tests, tests on money, auth, and permission paths.
4. **Speed never buys a weaker claim.** A lever that makes a test fast by removing what it proves (stubbing the database in a test whose claim is the query) is a deletion. Treat it as one, with the evidence a deletion needs.
5. **No new dependencies without asking.** Before proposing a specific profiler or mutation tool the project does not have, load and follow the `dependency-vetting` skill through the host's skill mechanism. Obtain separate user approval before adding the vetted tool.

## Process

### Step 1: Baseline

1. Find every suite: read the manifests and CI config (`package.json` scripts, `Gemfile`, `pyproject.toml`, `go.mod`, `.github/workflows/`). A project often has more than one (unit and browser, backend and frontend). The CI command is the one that counts.
2. Check that the working tree is clean and the suite is green. If it is red, or flakes on this run, stop and report: a cut on a red suite cannot be verified.
3. Run each suite with per-test and per-file timing. Read `SPEED-LEVERS.md` for the timing command per runner and for splitting boot, import, and setup time from test time. If the project has coverage set up, record it in the same run. Time every run on a quiet machine: no other test suite running, counting your own subagents and other sessions. Record the load average just before the run. A suite that fills every core raises the load by itself, so quiet means nothing else is running, not a load threshold. When another suite is running, name it and ask the user once whether to wait.
4. Record the baseline per suite: command, wall time, test count, file count, the share of time in boot, import, and setup, and the 20 slowest files and 20 slowest tests with their times.

Scope: if the user named a path or area, scope to it. Otherwise take the whole suite, with the slowest files first: in most suites a few files hold most of the time.

Done when: every suite has a baseline row taken from a real run.

### Step 2: Map the claims

Dispatch independent subagents, one per area of the test tree (by directory or by test level), in one message. Each one reads its area's test files in full, edits nothing, and returns rows, not file contents. Each one also runs Step 3 on its own area, so brief it with Step 3's move list and the path to this skill's `RED-FLAGS.md`. If independent subagents are unavailable, use sequential fresh sessions where possible; otherwise perform the areas yourself and report the independence gap. One row per test file in scope:

- **Level**: unit, integration (database, file system), request or controller, system or browser, e2e.
- **Exercises**: the production code it runs.
- **Claims**: each distinct observable behavior it checks, one line each.
- **Real libraries**: renderers, mailers, HTTP clients, browsers it drives for real.
- **Doubles**: what it mocks or stubs.
- **Time**: from the baseline.
- **Moves**: per claim, the break it catches, its move from Step 3, and the evidence. A claim whose cover sits in another area is marked for you to check.

Done when: every test file in scope has a row, and any file skipped is listed with its reason.

### Step 3: Diagnose

The Step 2 subagents run this step inside their areas. `RED-FLAGS.md` names each defect, and the name carries the move. For each claim, name the break, then take the first move that applies:

1. **Delete**: no nameable break, or the same claim is checked elsewhere at the same or a cheaper level.
2. **Demote**: the claim is real but sits above its cheapest level. It gets written at the cheaper level, and the high-level check goes. What only the high level can catch stays.
3. **Merge**: near-duplicates with the same arrange and act become one parameterized test.
4. **Rewrite**: the claim is real, but the test is fragile or over-mocked.
5. **Fix flake**: the test is nondeterministic.
6. **Keep**.

For a claim marked covered elsewhere, read the other test's assertion: running the same code is not checking the same thing. The subagents check cover inside their own area. You check the claims they marked as covered in another area. If the project already has a mutation tool set up (Stryker, mutant, mutmut, PIT, go-mutesting), run it yourself, scoped to the modules whose tests you propose to delete, and record which mutants lose their only killer.

Then read the timing profile against `SPEED-LEVERS.md`. A lever is a finding only when the profile shows the time it would recover.

Done when: every claim in the map has a move, and every Delete and Demote names its evidence.

### Step 4: Assess

Each finding carries its payoff: seconds saved from the baseline timings, or, for a fast test with no break, the maintenance cost it removes (it fails on refactors, it pins an implementation). A finding with neither is a style preference. Drop it.

| Verdict | Meaning | Action |
|---|---|---|
| **Lean** | Tests catch real breaks at sensible levels, and the time goes to tests that earn it | Tell the user, show the baseline. **Stop.** |
| **Localized** | A few files or one lever hold most of the waste | Present only those candidates. |
| **Systemic** | Waste spreads across the suite: a whole level duplicates another, one setup pattern runs everywhere | Present ranked candidates. Recommend the top 3-5 batches for this session. |

**Idempotency rule:** on an unchanged suite already assessed and trimmed, do not re-propose completed or rejected cuts without new evidence.

**User override:** if the user names a specific cut on a Lean suite, scope strictly to it.

### Step 5: Present candidates

Group findings into batches the user accepts or rejects whole: one lever, or one flag across one area. Rank by seconds saved, then by maintenance cost removed. For each batch:

- **Change**: files touched, tests removed, added, or rewritten.
- **Flag or lever**: its name from the reference files.
- **Saves**: estimated seconds, from the baseline timings.
- **Stays covered by**: where each removed claim lives after the change.
- **Risk**: what confidence the change could cost.

Ask through the host's native multi-select capability when exposed, following its live schema. Use one option per batch, with the label naming the batch and the description carrying the saving and risk; preserve the highest-saving-first order and split across calls at the tool's live limit. If native multi-select is unavailable, show the same choices in chat and wait for the user's selections.

### Step 6: Plan

Use the host's native plan mode when exposed. Otherwise draft the same plan in chat. Per accepted batch, the plan lists the files to edit or delete, the replacement tests a demotion writes first, any production seam, and the command that verifies the batch. Order the batches:

1. Levers that change no test (configuration, environment, parallelism).
2. Demotions and rewrites, replacements first.
3. Deletions, so each lands on a suite where its replacements already pass.
4. Tiers and CI splits (`SPEED-LEVERS.md`, Tiers and CI), last, so a tier holds only tests that survived the cuts.

Present the plan through the host's native approval mechanism when exposed. Otherwise present it in chat. Require explicit user approval before Step 7 edits files.

### Step 7: Apply

Per batch:

1. Write replacement tests first (demotions and rewrites) and run them: they pass. Where a replacement needs a seam that is missing, extract the part that builds the data out of the code that calls the library, so the library call becomes a thin adapter with no decisions in it.
2. Apply the edits and deletions.
3. Run the full suite: green. Where the runner supports it, run it in random order too: shared setup and turned-off isolation can hide order dependence.
4. Time it against the baseline on a quiet machine (Step 1). Revert a lever that saves nothing measurable.
5. Commit the batch on its own.

When a batch goes red, revert it and diagnose from the reverted state, then retry a smaller batch.

### Step 8: Verify and report

1. Run each suite with the baseline command and timing, back to back with the base commit under the same load. Numbers taken under different loads do not compare.
2. If coverage was recorded in Step 1, compare the changed areas. A line that lost its only test either belongs to library behavior or trivial code (say which), or its test comes back.
3. Report:
   - per suite: wall time, test count, and file count, before and after
   - per batch: what changed, the measured saving, where the removed claims live now
   - what stayed and why: keep-list tests, rejected batches
4. Re-run the Step 4 assessment on the changed areas and report the evidence-based verdict. If previously accepted waste remains, explain why; do not automatically start another round.
