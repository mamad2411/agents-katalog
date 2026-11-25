---
name: diagnosing
description: "Call on a hard bug or a performance regression — BEFORE the first code edit. Trigger words (RU+EN): не воспроизводится, иногда падает, флак, «почему-то», регрессия, стало медленно, «было же зелёное» / not reproducible, intermittently fails, flaky, «somehow», regression, got slow, «it was green before». First builds a TIGHT feedback loop that reddens on EXACTLY this bug; fixing by hypothesis without a red loop is not allowed. Boundary: this catches the cause of one bug; systematic coverage is test-generation."
---

# Diagnosing bugs

Complements the Iron Law ("no fixes without a root cause") with HOW to find that cause.

## Phase 1 — build a feedback loop. THIS IS THE SKILL

Everything else is mechanics. Have a **tight** pass/fail pair that reddens EXACTLY on this bug and
you will find the cause: bisection, hypothesis testing, instrumentation merely consume it. No loop —
no amount of staring at the code will save you. Invest here disproportionately. **Be persistent,
inventive, do not give up.**

### What to build it with (roughly in this order)

1. **A failing test** at the right seam (unit/integration/e2e).
2. **curl / an HTTP script** against a live dev server.
3. **A CLI call** on a fixture, diff stdout against a reference.
4. **A headless browser** (Playwright) — drives the UI, asserts DOM/console/network.
5. **A trace replay** — save a real request/payload/log and run it through the code in isolation.
6. **A throwaway harness** — a minimal slice of the system (one service, mocks) through one function.
7. **Property / fuzz** — "sometimes wrong" → 1000 random inputs, hunt the failure mode.
8. **Bisection** — the bug appeared between two states → automate `git bisect run`.
9. **find-polluter** — a test is green alone but red in the suite (or vice versa) → a neighboring
   test dirties shared state (FS / global / DB). Run the suspects one by one in suite order, stop at
   the first that reproduces — that is the polluter. Separate from `git bisect` (that hunts the
   guilty COMMIT, this one the guilty TEST in the suite).
10. **Differential** — the same input through old vs new version (or two configs), diff.
11. **HITL script** — a last resort: if a human clicker is needed, guide them with a script, the
    output back into the loop.

Built the right loop — the bug is 90% beaten.

### Tighten the loop (treat it as a product)

- **Faster** — cache the setup, skip extra init, narrow the scope.
- **Sharper signal** — assert exactly the symptom, not "did not crash".
- **More deterministic** — pin the time, seed the RNG, isolate the FS, freeze the network; wait for
  readiness by **polling a condition** (a loop until ready with a timeout), not `sleep N`: an
  arbitrary sleep = flake and wasted time. (In the stress mode for a non-deterministic bug, below, a
  sleep is inserted ON PURPOSE — that is different.)

A 30-second flaky loop is barely better than none; a 2-second deterministic one is a superpower.

### A non-deterministic bug

The goal is not a clean repro but a **higher reproduction rate**. Run the trigger 100×, parallelize,
add stress, narrow the timings, insert sleeps. A 50% flake is debuggable, a 1% one is not: raise the
rate.

### Can't build a loop — STOP, say so

List what you tried. Ask for: access to the reproduction environment, a captured artifact (HAR, log
dump, core, a screen recording with timing) or permission to instrument temporarily. **Do NOT
hypothesize without a loop.**

### Phase 1 completion criterion

You can name **ONE command** (a path to a script, a test call, a curl) that you have **already run
at least once** (paste the call and its output), and it is:
- [ ] **red on THIS bug** — exercises the real code path and asserts the EXACT user symptom, reddens
  on the bug and greens after the fix. Not "runs without error" — catches this bug specifically.

### Run classification: infra ≠ bug

Each run of the loop is EXACTLY one category (see [[complexity-budget]]):
- **fail** — the bug reproduced, the evidence is valid (what you want).
- **pass** — no symptom (baseline/after the fix).
- **infra** — the run broke by itself (environment, dependency, network, a crashed service) — this
  is NOT "no bug", the run simply has nothing to measure.
- **not_run** — there is no terminal result.

**Do NOT count infra/not_run as "the bug did not reproduce".** Counting it that way = chasing a
phantom or closing a live bug as vanished. First fix the infra / get the artifact, bring the run to
fail|pass, then hypothesize. A non-deterministic bug is a series of fail/pass, not infra.

## Next (after the loop)

Root cause → minimal fix → green loop → regression test (must redden on the old code) →
verification by a fresh run. See [[task-cycle]] and [[receiving-review]].

In multi-component systems — instrument EVERY boundary (what came in / what went out / did the env
vars pass through), see in one run WHERE it breaks, then dig into that layer.

### A dispute with a measurable consequence is settled by MEASURING, not by argument

A fork of "which is better" that has a measurable consequence is closed by a script in one run, not
by trading arguments. A measured case: review found that a node's new geometry breaks the edge
routing; instead of a dispute — a script counting crossings on four live processes, three variants
(15 · 16 · 21 crossings). The decision took one run.

The best outcome of such a measurement — it becomes a test: then a regression "nudged it to look
nice" is caught mechanically, not by the memory of the disputants. A measurement that did not become
a test will have to be repeated.

### A fix counter → architecture (not "fix #4")

3+ failed fixes in a row on one symptom are NOT the next hypothesis but a signal of a WRONG
architecture: each fix exposes new coupling, because the consequence is fixed, not the form. STOP,
escalate to the owner with a map of what each fix exposed — not "fix #4". Count fixes explicitly.

### Defense-in-depth — ONLY for the irreversible

For IRREVERSIBLE operations (data loss, money, destructive FS/git) validate at EVERY layer after the
root fix (entry / business logic / env-guard / log), so the bug becomes structurally impossible. For
ordinary logic — **one** guard in the shared function (that is both the cheapest and the root place,
as the minimal fix above demands); multiple layers are justified only by the cost of
irreversibility. Reconciling with the minimal fix: as many layers as the cost of error is worth.

## When NOT to apply

- **The cause is already known.** The feedback loop is a search tool. You know what is broken — fix
  it; building a loop for discipline's sake means paying for an answer already obtained.
- **An infrastructure failure, not the code.** A runner fell, disk ran out, a token rotted — the
  loop will redden honestly and lead away from the real cause. The run class is determined first.
- **An edit with no observable failure** — a new feature, cleanup, a document. There is nothing to
  diagnose: no failure the loop could catch.
- **The failure reproduces on one run and is fixed by one line.** A tight loop here costs more than
  the fix itself, and the feedback is already there.
