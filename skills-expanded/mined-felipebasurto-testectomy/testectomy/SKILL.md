---
name: testectomy
description: >-
  One skill for tests. Gates every new or changed test at write time, and on
  request cuts a test suite down to the tests that matter: writes Markdown spec
  files (SPEC.md) with the intent, keeps only tests a reader cannot replace
  (external boundaries, money, security, concurrency, parsers, real
  regressions, public contracts), converts brittle assertions to expect tests,
  deletes tests that re-encode the implementation along with the test-only
  production seams they keep alive, and reports bugs the green suite was
  hiding. Use when writing, changing, reviewing or deleting tests, and when the
  user asks for a test audit, test cleanup, test pruning, spec tests, Markdown
  specs, a subsystem test campaign, or to reduce test time and token cost.
---

# Testectomy

Tests that restate the implementation are a second, worse copy of the logic.
Intent is not: it lives in requirements, not in code, and nothing in the code
can validate it. This skill moves intent into `SPEC.md` files that humans own
and agents read, and keeps executable tests only where reading code cannot
replace running it.

Three layers, cheapest first:

| Layer | What it holds | Who checks it |
|-------|---------------|---------------|
| `SPEC.md` | Rules, examples, non-goals, open questions | Agent reads it before and after every change |
| Types / schemas | Shapes, exhaustiveness, nullability | Compiler |
| Executable tests | Only rules that pass the [keep bar](#keep-bar) | Test runner, scoped to touched rules |

For the spec file format, read [spec-format.md](spec-format.md). For expect-test
tooling per language, read [expect-tests.md](expect-tests.md).

## Modes

| Mode | When | What it does |
|------|------|--------------|
| **Gate** | Any time you write, change or review a test | Rejects low-value tests before they land. Never deletes. |
| **Pass** | The user asks to audit, prune or rebuild tests for a repo or path | The [workflow](#pass-workflow): specs, verdicts, deletions, gaps, report |
| **Campaign** | The user asks to prune one whole subsystem in a large repo | The pass, split into lanes with a ledger and an independent preservation review. Read [CAMPAIGN.md](CAMPAIGN.md) first. |

Pass and campaign delete tests, so they run only when the user asked for them.
The gate applies on its own.

## Gate

Before adding or changing any test, answer these. A missing answer means don't
add it yet:

1. **Which rule does it guard?** Name the observable behavior, invariant or
   contract. If the area has a `SPEC.md`, name the rule ID; a test with no
   `Check: test` rule needs one first, and the rule must meet the
   [keep bar](#keep-bar).
2. **What credible regression makes it fail?**
3. **Why doesn't existing coverage catch that already?** Each contract has one
   owner test at the strongest boundary. Another layer needs its own failure
   mode, such as a transport or lifecycle failure the owner can't reach. Prefer
   a new row in an existing table test over a near-duplicate.
4. **Does it need a production seam** (export, flag, wrapper, injection hook)
   that no production caller needs? Then test at the real boundary instead.

Two requests produce junk by reflex. When asked to remove or move something,
don't add tests asserting it's gone. When a test is flaky, don't add a sleep,
a retry or a longer timeout: find the race and await the real signal.

Fixing a test counts as changing it, so the questions above apply: if it
guards no rule in the area's spec, add the rule (with its source) or flag it as
an open question. Bite-check every new test and every changed assertion; a
change that only replaces how the test waits keeps its assertion, so running it
on the fixed and broken code once is enough.

Then check it against every [junk pattern](#junk-patterns). A match fails the
gate unless the keep bar names the contract it independently guards. A test
that would break under a behavior-preserving refactor asserts implementation:
rewrite it at the owning boundary before it lands.

A bug regression test must fail on the pre-fix code for the intended reason and
pass after the fix. One that never demonstrably failed proves the mock, not the
fix. One regression at the owner boundary covers the bug; don't replay it at
every layer it crosses. When a fix makes an expected-failure test pass, remove
its marker in the same change. Prefer a new row in that test over a new test.

If the user explicitly asks for a test the gate rejects, say once why, and offer
the alternative that guards the same thing (usually a row in an existing
boundary test). If they still want it, write it: it's their repo.

## Ground rules

- **Specs come from intent, never from the code.** Sources: README, docs, issues,
  PR descriptions, commit messages, public API docs, product copy, the user.
  Reading the code to learn *what it does* is fine; copying that into a spec as
  *what it must do* is how tests end up blessing bugs.
- **Where code and intent disagree, never encode the code's behavior.** If the
  intent is unambiguous, the code has a bug: write the rule from intent, add its
  test as an expected failure (`pytest.mark.xfail(strict=True)`, `test.fails`,
  `#[should_panic]`-style, or a skip that names the rule ID), and report it under
  Bugs. During a pass or campaign, don't fix production code unless the user
  asked; when the task itself is the fix, fix it. If the intent is only
  partly clear, split it: the firm part becomes a rule ("never negative"), and
  the unclear part goes under `## Open questions` ("0 or 499?").
- **Unsourced behavior on a public contract isn't deletable.** If only the code
  says what a public API returns, keep the test, mark the rule
  `Source: current behavior (unconfirmed)`, and list it as an open question.
- **Read before you judge.** For every candidate, read the complete test, the
  production owner, its entry point, callers, sibling implementations,
  overlapping tests, CI routing and relevant history. When a test claims
  dependency-backed behavior, read the dependency's source or types.
- **Use git history as evidence.** A test that changed in most commits that
  touched its owner, while the behavior didn't change, depends on the
  implementation. A test that never changed while its owner was rewritten may
  assert nothing. A test added in the same commit that removed or renamed
  something often asserts the past.
- **Judge a test by its assertions, not its name.** A test named "clears the
  window" may assert the window was *not* cleared. Files named after a plan
  phase, PR, audit or fix batch (`Phase7`, `Leftover`, `Fixes`) often hold real
  behavior: judge each test, and CONVERT good ones into their owner suite.
- **Static or slow is not a deletion reason.** A test that looks like
  implementation may still be the only guard of a contract. Prove otherwise
  before removing it.
- **Don't add a framework.** If the repo already uses Cucumber, Gauge, specdown
  or similar, write specs in that format. Otherwise use plain Markdown plus the
  repo's existing test runner.
- **Fewer, stronger tests at public boundaries.** One test per rule, at the
  boundary where callers meet it. It must survive any refactor that keeps the
  behavior.

## Pass workflow

Before starting, tell the user what a pass produces and ask which parts they
want: pruning (always), area specs, and the test policy in `AGENTS.md`. With
pruning only, skip steps 4 and 8, record each rule and its source in the
ledger instead of a spec, and classify against the keep bar directly.

Copy this checklist and track it:

```
- [ ] 1. Baseline
- [ ] 2. Inventory
- [ ] 3. Gather intent
- [ ] 4. Write SPEC.md per area
- [ ] 5. Classify every test
- [ ] 6. Apply: delete, convert, fill gaps
- [ ] 7. Prove kept tests bite
- [ ] 8. Write the test policy into AGENTS.md
- [ ] 9. Validate and report
```

### 1. Baseline

Read the root and scoped `AGENTS.md`/`CLAUDE.md`, the CI config and the
package scripts. Take the test, format and changed-files commands from there,
and obey any rules the repo sets for agents and test runs (how many agents,
which model, how often the full suite may run).

Run the full suite once and record: pass, fail and skip counts, wall time,
flaky tests, test and production line counts. Then check the numbers make
sense:

- **Zero or suspiciously few cases is a failed baseline**, even with exit code
  0. Test scripts can silently match no device, target or file.
- **Split build time from run time.** In compiled languages most of the wall
  time is often compiling test code. Report both, and don't promise faster runs
  from cutting tests that already run in milliseconds.
- **Tests skipped on every run** are a finding of their own: they cost build
  time and prove nothing.
- **A red baseline** is a finding: a failing test may be a real product bug.
  Reproduce it and report it; don't delete your way to green.

Never edit source or tests while a test watcher is running in the checkout.

### 2. Inventory

Find the tests yourself; no fixed pattern works across stacks. Tests can be
in any language, any folder, with any name. Use what the repo already says:

- The test runner's config and the CI job: which targets, packages, globs or
  plans they run.
- Build files that declare test targets (an Xcode test plan, `Cargo.toml`,
  `package.json`, `pyproject.toml`, Gradle, Bazel).
- The runner's own listing, when it has one (`--collect-only`, `--list`,
  `-list-tests`, a dry run). It counts cases more reliably than reading files.
- Then read the tree to confirm. Exclude vendored and generated code.

Write down what you found and how: test locations, number of files, lines and
cases, and the command that lists them. Then choose the areas from the
production code, not from the test layout: an area is one cohesive behavior
(pricing, payments, auth). When most tests sit in one folder, group them by
the production owner they exercise. Several areas can share one `SPEC.md`
with different ID prefixes when they live in the same module. On large repos,
run one area per pass and land each separately, or switch to
[campaign mode](CAMPAIGN.md).

### 3. Gather intent

For each area, collect intent sources *before* opening its tests. Write down
the source of each rule (`README#pricing`, `#412`, `commit a1b2c3`, `user`).
A rule with no source except the current code goes under
`## Open questions`, not `## Rules`. The one exception is a public contract
with an existing test (see Ground rules): that becomes a rule marked
unconfirmed *and* an open question. One sentence of intent may yield several
rules when it has distinct failure modes ("never charge twice": sequential and
concurrent).

When intent is thin, ask the user a short batch of concrete questions
("Should a discount larger than the subtotal give 0 or an error?").
Don't guess. If you can't ask (a subagent, a headless run), take the narrowest
reading, put the question under `## Open questions`, and list it in the report.

### 4. Write SPEC.md per area

Put it next to the code it governs (`src/billing/SPEC.md`), unless the repo
already has a `specs/` convention. When the code is organized by layer
(models, services, views) instead of by feature, use one `specs/<area>.md` per
area at the app root. Follow [spec-format.md](spec-format.md).
Every rule gets an ID (`BILL-3`) and a `Check:` level:

- `type`: the type system or a schema already enforces it.
- `read`: an agent verifies it by reading the diff against the rule.
- `test`: it passes the keep bar and needs an executable test.

Default to `read`. Promote to `test` only through the keep bar.

### 5. Classify every test

Read each test in full, including parameter tables, and give each declaration
exactly one verdict. A table test (`it.each`, `parametrize`) is one declaration
unless its rows need different verdicts.

| Verdict | When | Action |
|---------|------|--------|
| **KEEP** | Guards a `Check: test` rule at its public boundary, even if it needs a rename or a mock swapped for a fake | Put the rule ID in the test name |
| **FIX** | Guards a `test` rule, but an assertion can't fail (a negative that passes when only one of several items is missing, a check the production path never reaches), or it passes only by sleeping, retrying or a raised timeout | Repair the assertion or await the real signal, then bite-check it |
| **CONVERT** | Guards a `test` rule through many hand-written field asserts, mocks or private calls, or duplicates a stronger suite | Rewrite as one expect test at the boundary, or move its unique assertion into the keeper |
| **FOLD** | Its input → output pair illustrates a sourced `read` rule well | Move the example into that rule's table, then delete the test |
| **DELETE** | Matches a [junk pattern](#junk-patterns) and guards no keep-bar rule | Delete |

Every DELETE needs one evidence line: what failure the test could actually
detect, and the stronger proof that remains (or why no contract exists). A
missing line means it isn't ready to delete. Evidence that says no other proof
remains contradicts a DELETE: that test is KEEP or FIX. KEEP evidence names the
regression ("fails if reconcile overwrites member notes"); a label ("mirror
sync") isn't evidence. A rule ID is valid only with a source other than the
code: never invent one to justify a verdict.

Test names carry the rule ID in a form the runner accepts and can filter on:
`"BILL-3: …"` with `-t BILL-3` (Vitest, Jest, Bun), `test_BILL_3_…` with
`-k BILL_3` (pytest), `TestBILL3…` with `-run BILL3` (Go).

When unsure between KEEP and DELETE, keep it and list it in the report with the
reason. Deletion count is not the goal.

A test you haven't read in full yet is UNREAD, never a verdict. An UNREAD row
means the classification isn't finished.

### 6. Apply

- Look for the one change behind several verdicts before editing test by
  test: a table test that absorbs a dozen near-copies, a shared fixture, a
  boundary test that replaces a whole mocked layer.
- Delete DELETE/FOLD tests, then their now-unused fixtures, helpers and mocks.
- Delete the test-only production seams they kept alive: exports, getters,
  reset functions, injection parameters, flags, wrappers, and dead production
  code whose only callers were tests. Don't keep aliases. Prefer a net-negative
  production line count.
- Rewrite CONVERT tests per [expect-tests.md](expect-tests.md). Don't add
  replacement tests that restate the same implementation.
- **Gaps:** every `Check: test` rule with no test gets one: an expect test at
  the boundary, named with the rule ID.
- Update CI routing, test inventories and line-cap baselines that list moved or
  deleted files.
- Keep each area's change coherent: spec, test changes and seam removals land
  together.

### 7. Prove kept tests bite

For every new, fixed or converted test, and a sample of the KEEP ones: break the
behavior the rule describes in production code (flip a condition, drop a
branch), run that test, confirm it fails *for that reason*, then revert.
It has to be an assertion failure: a syntax, import or setup error proves
nothing. A test that stays green guards nothing: fix it or delete it. For an
expected-failure test, the bite check runs the other way: temporarily fix the
bug and confirm the test passes (strict mode then reports XPASS). Then run
`git diff` on production code to make sure every mutation was reverted.

### 8. Write the test policy into AGENTS.md

Add or replace the testing section with this, adjusted to the repo's commands:

```markdown
## Tests and specs

- Each area's intent lives in its `SPEC.md`. Read it before changing that area.
- After a change, check every rule your diff touches. For `Check: read` rules,
  state in your summary that you re-checked them. For `Check: test` rules, run
  only the tests that cite those rule IDs (`<runner filter> BILL-3`).
- A new test needs a `Check: test` rule that meets at least one of: external
  boundary, money/auth/data-loss/security, concurrency/time/ordering, large
  input space (parsers, formatters), a real past regression, or a public
  contract others depend on. Everything else is checked by reading. No tests
  for private helpers, restated constants, or mock call arguments.
- A bug-fix regression test must fail on the code before the fix.
- Removing or moving code needs no test that it's gone.
- No sleeps, retries or raised timeouts in tests. Await the operation or its
  signal, and fake the network so unexpected requests fail.
- Behavior changes start in the spec: update the rule, then the code.
- If code and spec disagree, stop and ask. Don't edit the spec to match the code.
```

### Keep it from growing back

If the stack has a linter that can enforce part of the gate, wire it: rules
against fixed sleeps, retries, raised timeouts and mocks that replace behavior
exist for several ecosystems (for TypeScript, `landmines`). Adopt them in an
existing codebase with a per-file allowance of current violations that may
only shrink, so the count ratchets down instead of blocking the merge.

### 9. Validate and report

1. Run the owner and sibling tests for every changed path with the repo's
   runner, then the full remaining suite, the typecheck and the linter.
2. For a removed test that grepped source or checked a plan, run the script or
   dry-run that owns the real contract.
3. Run the repo's formatter on changed files, then `git diff --check`.
4. Run the changed-files gate the repo's policy requires, and its review step
   if it has one.
5. Read `git diff --numstat`; count production and tooling lines separately
   from tests and test support.

Report in this format:

```markdown
## testectomy: <repo or area>

Before → after: <N> tests / <T>s → <N> tests (<x> expected-failure) / <T>s
Lines: tests <a> → <b>, production <c> → <d> (tests can go up when gaps outnumber deletions)
Baseline: <green/red, flaky tests, typecheck/lint state>
Specs written: <paths> (<n> rules: <x> test, <y> read, <z> type)

Bugs (<n>): <rule ID: intent vs actual behavior>, test marked expected-failure
Kept (<n>): <rule ID → test>, one line each with the keep-bar reason
Fixed (<n>): <test: the assertion that couldn't fail, and the repair>
Converted (<n>): <old tests → new expect test or keeper>
Gaps filled (<n>): <rule ID → new test>
Bite check: <n> mutations, all failed on an assertion and were reverted (git diff clean)
Deleted (<n>): grouped by junk pattern, with counts
Kept on purpose: <tests that looked like junk but guard a contract, and which>
Open questions: <code vs intent disagreements needing a human call>
Production cleanup: <test-only seams and dead code removed>
AGENTS.md: <added / updated test policy, filter command>
Proof run: <commands actually run and their results>
Follow-ups: <next areas, PR state>
```

### Landing

Commit, push or open a PR only when the user asked, using the repo's PR flow.
Land one coherent area per PR. After it lands, refresh from the default branch
and rerun the inventory before starting the next area.

## Keep bar

A rule gets `Check: test` only if at least one of these holds. Write which one
next to the rule.

1. **External boundary**: a provider, API, DB, file format, wire protocol or OS
   behavior that you don't control and that can change underneath the code.
   Use the real implementation everywhere you can, and fake only at the
   boundary: recorded real responses, a network-level interceptor, or a small
   scripted fake that behaves like the provider (times out, errors, succeeds). Asserting what the code did *to* the
   fake is fine when that is the rule ("3 attempts", "never charged twice").
2. **Costly or irreversible failure**: money, auth and permissions, data
   deletion, migrations, storage, security, privacy.
3. **Hard to verify by reading**: concurrency, ordering, time zones and clocks,
   floating point, caching and invalidation, retries. Call order counts when
   the order is observable behavior.
4. **Large input space**: parsers, serializers, formatters, compilers,
   renderers, validators. Use expect tests or property tests.
5. **A regression that actually happened**: link the incident or issue, and keep
   the test if the failure can plausibly come back.
6. **Public contract others depend on**: a library API, CLI output, plugin SDK,
   protocol, config format, defaults, prompt bytes, generated cross-language
   code, package or release contents, an architecture boundary, analytics or
   telemetry event names and parameters that dashboards read. Many wire-format
   snapshots of one contract collapse into one table test.

A source-inspection test (grepping a file) passes only when it's the cheapest
independent guard: it fails when the contract changes (the user-facing key,
byte or path) and survives a rename of identifiers.

Everything else is `read`.

## Junk patterns

Ask what the test depends on. A test worth keeping depends on intended
behavior: it changes only when that behavior changes, and fails only when it
regresses. The gate rejects a new test that matches a pattern below; a pass
deletes an existing one unless the keep bar names the contract it guards.

### It depends on the past

It asserts that removed or moved code stays gone. Bringing it back would be a
decision, not a regression.

- A removed feature, screen, flag, endpoint or dependency is asserted absent.
- A moved module is asserted missing from its old path, or an old name is
  asserted not to resolve.
- A presentation is asserted empty or nil for UI that was removed: delete the
  test with the dead code path.

Agents write these when asked to remove something ("so it can't come back").
Removing code never needs a test proving it's gone.

### It depends on nothing

No change to the code under test can make it fail.

- No assertion at all: coverage probes.
- It tests the platform: a button renders, an event fires, a framework or
  language feature works, getters, setters and constructors behave.
- It asserts what the type system or the compiler already guarantees.
- It mocks the unit under test, then asserts what the mock returns; or mocks
  implement the behavior being asserted; or one identical mock stands in for
  different APIs.
- Self-comparisons and identity copies.
- Negative controls that pass for an unrelated reason: a denial from a
  different guard, a rejection the production path never reaches.
- An opt-in harness (screenshots, galleries, renders behind an env flag) that
  is skipped on every normal run: move it to a script or delete it.

### It depends on the implementation

It changes whenever the code does, even when behavior didn't.

- Expected value produced by the helper, renderer or logic under test.
- Restates constants, enums, exports, config, defaults, fixtures, manifests or
  inventories verbatim.
- Asserts layout and motion numbers (point sizes, paddings, opacities, angles,
  durations) that restate constants, unless the number is a documented
  accessibility minimum.
- Asserts the contents of debug-only seeds, preview data, demo fixtures or
  debug menus that ship to no user.
- Exact source, import or string greps that a rename breaks.
- Tests a private function, predicate, private state, internal call order or
  which helper was invoked, when the boundary test already covers the outcome.
- Asserts that a mock was called with arguments the code under test built,
  when no rule is about that interaction.
- Fixtures that supply what the owner should produce (receipts, callback
  ordering, admission), or persistence asserted against a store the real path
  never writes.
- Capability tests that restate a declared flag instead of exercising what the
  flag promises.
- Exists only to keep a test-only export, global or wrapper alive.
- A large snapshot nobody reviews, updated blindly with `-u`.
- A name or fixture that promises more than the input exercises.

### It duplicates another test

- The same contract asserted again at another layer, or per provider, with no
  new failure mode. Keep the one at the strongest boundary.

### It passes by hiding a flake

These guard real behavior, so the verdict is FIX, not DELETE. A test that only
passes on rerun is a bug in the test or the code.

| Hides the flake by | Fix |
|---|---|
| Waiting a fixed real-time delay (sleep, timer) | Await the operation, or a promise or signal its handler resolves. To move time, control the clock (fake timers) and advance it |
| Polling state until a deadline | Have the code that records the event resolve a signal, and await it. A deadline-bound poll fails under load |
| Retrying on failure | Find the race and await what the test depends on. If it can't be fixed now, record it where the repo tracks flaky tests; don't retry it |
| Raising its timeout | Await the real event, or move slow shared setup to suite-level setup |
| Letting network requests through, or answering them silently | Fake at the network boundary with a handler for every request the test makes, and make any other request fail the test |
| Being disabled or skipped on every run | Fix it and re-enable it, or delete it. A disabled test costs build time and proves nothing |

## Done looks like

- Every test left guards a rule with a named regression, and would fail on that
  regression and only on it.
- No test asserts code that no longer exists.
- No two tests guard the same behavior.
- No test sleeps, retries, raises a timeout or stays disabled to pass.
- No production code exists only for tests.
- Every area has a spec, and `AGENTS.md` tells the next agent how to use it.
