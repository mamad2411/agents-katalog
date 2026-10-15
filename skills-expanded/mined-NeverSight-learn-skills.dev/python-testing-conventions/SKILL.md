---
name: python-testing-conventions
description: "Use when writing or restructuring Python tests — deciding how much duplication a test should carry before it stops being readable, what a fixture should cover and at what scope, when to parametrize instead of writing another test, whether a dependency should be doubled or run for real, and what belongs in a fast default suite versus a slower marked tier. Also for pytest specifics: fixtures, conftest placement, parametrize ids, markers, and keeping a suite from writing into the real home directory. Gives the default answer per question rather than an evaluation, so choices stay consistent across projects instead of drifting session to session, and each entry says whether it overrides a model's own instinct or just confirms it."
metadata:
  family: python
---

# Python testing defaults

Personal, agent-maintained Python projects. Split out of `python-conventions` on 2026-08-31, which
keeps the design and style defaults; this skill owns the test suite. Nothing here is tool config —
pytest's own configuration lives with the repo's quality tooling, not here.

**Each entry says whether it's overriding your own default instinct or just confirming one.** A
capable model already parametrizes value matrices and reaches for `tmp_path` unprompted. This skill
exists for the places a model left alone drifts — inlining the same arrange block into every test
rather than promoting it to a fixture, and reaching for a mock where the suite could own the real
thing.

## Testing conventions

- Snippet: [`references/snippets/testing.py`](references/snippets/testing.py)
- Fixtures first, always. Any setup a test needs — a tmp tree, a fake `HOME`, a stubbed `c.run`, a
  constructed object, a monkeypatched env — is a `pytest` fixture (in `conftest.py` once two files
  want it), not lines hand-rolled at the top of each test body. Two reasons, and the second is the
  bigger one: it removes the mechanical duplication, and it **surfaces when the suite is doing the
  same thing three different ways** — three hand-rolled versions of "make a fake repo" hide in three
  test bodies indefinitely; three fixtures named `fake_repo`, `tmp_repo`, and `repo_dir` sit next to
  each other in `conftest.py` and get merged. Reach for the built-ins (`tmp_path`, `monkeypatch`,
  `capsys`, `caplog`) before writing a helper that reimplements one. A helper _function_ is the
  fallback only for setup that needs per-call arguments a fixture can't take — and even then, a
  fixture returning a factory (`make_repo(name)`) usually fits.
- Fixture scope: narrowest that stays correct. For the module-singleton pattern in
  `python-conventions` — construct the expensive object at module/session scope, but reset its
  _mutable_ state via a function-scoped fixture. A `monkeypatch` inside a broad-scoped fixture stays
  live for the whole scope, not just one test — a real, silent cross-test leak source.
- DAMP vs. DRY — a different axis from `python-conventions`' production-code DRY decision, not a
  re-derivation of it: setup mechanics (fixtures/helpers, the _how_) stay DRY; the scenario a test
  verifies (the _what_) stays explicit and readable top-to-bottom in that test. `parametrize` is the
  sanctioned everyday tool for a real input→expected matrix, and is _more_ explicit than N
  copy-pasted bodies, because the varying values are isolated from the fixed logic — attach `ids`
  once values stop being self-explanatory. The line: **if adding a case means adding a value,
  parametrize; if it means changing the test's logic (a branch, a different setup, a different
  assertion), write a new test.** What's actually warned against is collapsing genuinely different
  scenarios into one branching mega-test, or hiding the scenario inside a helper whose name doesn't
  say what it asserts.
- Model default: **mostly confirms, overrides in one direction.** A model parametrizes value
  matrices unprompted, and that's right. What it does _not_ reliably do is promote setup to fixtures
  — left alone it inlines the same three-line arrange block into every test it writes, which is the
  "same thing three ways" failure above. The other narrow override: `python-conventions`' modularity
  abstraction instinct can leak into folding scenarios that differ in _logic_ into one
  parametrized-with-branches test, or into a `check_*` helper that owns the assertion.
- Never run a code-mutating command as part of a test's exercised behavior unless the test's actual
  subject is that mutation. A fix/format/autocorrect command run before the assertion silently masks
  the exact defect a check-only equivalent would have caught. Confirmed live 2026-08-23 in
  `scaffoldapy`: an e2e test ran `inv quality.precommit` (fixes formatting, _then_ checks) against a
  freshly generated repo — real CI runs the check-only `inv quality.check` with no such gate, so a
  dprint markdown-wrapping bug in the generated `README.md`/`SKILL.md` passed this test while
  failing every generated repo's actual first CI run. Prefer the check-only/dry-run form of a
  command in a test unless the mutation itself is under test.
- Model default: **overrides.** A model reaches for the "full" fix-then-check invocation of a
  quality/build tool by habit (it's the everyday command, and "make sure everything's clean" reads
  as the safe choice) — this entry blocks that instinct in tests specifically, where it silently
  narrows what the test can catch.

### Don't double anything the suite can run for real

- Default: **no mock, fake or stub for a dependency the suite can own the whole lifetime of** —
  in-process, or as a subprocess it starts and stops. A SQLite file, a temp directory, a local
  queue, your own entrypoint under a subprocess: run the real thing. A third-party HTTP API is the
  other side of the line, and a hand-written stand-in for one is correct rather than a compromise.
- The deciding question is that lifetime test, not a list of technologies — a list goes stale and
  invites arguing about membership, while "can this suite start it and stop it" answers a new case
  on its own.
- Why: it is the premise `db-defaults` already selects on. Every default there is chosen partly for
  "pytest-local testability with no docker/cloud", and doubling the database throws away the thing
  the dependency was picked for. You get to run the real thing _because_ the choice was made to let
  you.
- **Real is not the same as sandboxed, and running real services makes the difference matter more.**
  The `tmp_path` rule above is the sharp version: a test that reaches `Path.home()` writes into the
  real one. A real service under test needs its own temporary state as much as a fake would.
- **Where a framework singleton makes an in-process arrangement dishonest, the answer is a
  subprocess fixture, not a mock.** Starting the real entrypoint against its own temporary state
  reproduces the deployment shape instead of pretending the coupling is absent. Give it a bounded
  readiness wait that fails with the child's output — an unbounded condition that can never become
  true hangs rather than failing.
- Model default: **overrides.** Left alone a model reaches for an in-memory fake the moment a test
  would otherwise open a file or a socket; patching is the shape most training data shows, and
  "tests shouldn't touch the disk" reads as the disciplined choice. It is the wrong instinct
  wherever the suite could simply own the real thing.

## Full rationale

See [`references/rationale.md`](references/rationale.md) — the sources consulted, the DAMP-vs-DRY
debate as it actually stands, and the fixture-scope reasoning behind the defaults above.

## Starter snippet

[`references/snippets/testing.py`](references/snippets/testing.py) is a runnable sketch of the
fixture and parametrize shapes described here.

## Editing this skill

This file is _copied_ into `~/.agents/skills/python-testing-conventions` at install time, never
symlinked. Edit the source in the [`agent-skills`](https://github.com/TheodoreAD/agent-skills) repo,
push, then re-run the install
(`npx skills add TheodoreAD/agent-skills --global --skill python-testing-conventions`) to refresh
every project's copy. Editing the deployed copy in place is local drift and reaches no other
machine.
