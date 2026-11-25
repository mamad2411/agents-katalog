<!--
  SKILL.md — SDET operating manual.
  Runtime: Claude Code + ACP (swappable coding CLI). Content stays LCD —
  no assumptions about a specific framework unless injected via a stack overlay.
  Injection points are marked: `STACK: ...`
-->

# Skill: SDET

## Invocation

```
/sdet <task reference — suite to extend, failing test, or feature needing coverage/evals>
```

Or picked up from a Signal Protocol entry / PR assigned to sdet. Related wired
skills: `test-master`, `tdd`, `playwright-expert` (only if wired here).

---

## Step 1 — Read the existing suites

- Read the test directory, its README, runner config and fixtures.
- Note the isolation mechanism, the stubs, the naming pattern.
- Note what is unmeasured (no coverage, no evals, no contract tests) and say so.

<!-- STACK: stack-specific test runner + single-test command injected here -->

---

## Step 2 — Find the gap or the failure

- New work: which behaviour, shared shape, or external boundary has no test?
- Failure: reproduce it; run it in isolation, then in suite order, then repeated.
- Classify: product bug, test bug, or flaky (ordering, time, shared state, network).
- Product bug → stop; report to the owning dev with verbatim output.

---

## Step 3 — Write the smallest change

- Extend the existing suite and fixtures; no second runner, no new framework.
- Isolation: refuse non-test databases/dirs; reset state before each test.
- Tripwire: real model/network calls disabled globally; one opt-in live test behind an env var.
- Contract tests pin the key sets of hand-synced shapes.
- Eval harness: human-labelled golden set including hard cases, repeat runs, flip rate, pinned model id and prompt version recorded per result.
- One failure reason per test. Few meaningful tests over broad shallow coverage.

---

## Step 4 — Run everything you wrote

- Run the new tests, then the full suite, more than once if flakiness is in play.
- Report failing output verbatim. A failing suite is the finding; never "some failures".
- Live eval runs: opt-in only, cost shown first.

---

## Step 5 — Hand off (async)

```markdown
## SDET — <Task>

### Changed
- <test / fixture / harness> — <one line why>

### How to run
- `<command>`

### Results
- <verbatim output, pass and fail>

### Docs updated
- <README / test docs touched, or "none needed">

### Open
- <product bugs for owning dev, unmeasured areas>
```

Release decision stays with qa-engineer. Do not merge your own work.
