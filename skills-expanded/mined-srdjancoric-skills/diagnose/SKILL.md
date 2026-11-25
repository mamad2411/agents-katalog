---
name: diagnose
description: Disciplined diagnosis loop for hard bugs and performance regressions. Build a feedback loop → reproduce → minimise → hypothesise → instrument → fix → regression-test. Use when user says "diagnose this" / "debug this", reports a bug, says something is broken/throwing/failing, describes a performance regression, or hands you an issue summary from a previous session.
---

# Diagnose

A discipline for hard bugs. Skip phases only when explicitly justified.

## Input

Can start from a fresh session. Look for a **bug handoff** from a previous session — written by the `handoff` skill at `handoffs/<branch>/<slug>.md` (or a path the user passes). If one exists, read it first and map its sections straight onto this skill:

- **What we've tried & ruled out** → pre-seeds your discarded hypotheses. Do **not** re-test these.
- **Current hypothesis** → seeds Phase 4.
- **Relevant files & locations** → where to start looking.

A good handoff lets you skip rediscovery and jump toward the feedback loop and hypotheses. With no handoff, treat whatever the user gives you as the symptom report — what was tried, what failed, the exact symptom.

When exploring the codebase, use the project's domain glossary to get a clear mental model of the relevant modules, and check ADRs in the area you're touching.

## Phase 1 — Build a feedback loop

**This is the skill.** Everything else is mechanical. If you have a fast, deterministic, agent-runnable pass/fail signal for the bug, you will find the cause — bisection, hypothesis-testing, and instrumentation all just consume that signal. If you don't have one, no amount of staring at code will save you.

Spend disproportionate effort here. **Be aggressive. Be creative. Refuse to give up.**

### Ways to construct one — try them in roughly this order

1. **Failing test** at whatever seam reaches the bug — unit, integration, e2e.
2. **Curl / HTTP script** against a running dev server.
3. **CLI invocation** with a fixture input, diffing stdout against a known-good snapshot.
4. **Headless browser script** (Playwright / Puppeteer) — drives the UI, asserts on DOM/console/network.
5. **Replay a captured trace.** Save a real network request / payload / event log to disk; replay it through the code path in isolation.
6. **Throwaway harness.** Spin up a minimal subset of the system (one service, mocked deps) that exercises the bug code path with a single function call.
7. **Property / fuzz loop.** If the bug is "sometimes wrong output", run 1000 random inputs and look for the failure mode.
8. **Bisection harness.** If the bug appeared between two known states (commit, dataset, version), automate "boot at state X, check, repeat" so you can `git bisect run` it.
9. **Differential loop.** Run the same input through old-version vs new-version (or two configs) and diff outputs.
10. **HITL bash script.** Last resort. If a human must click, write a small throwaway bash script that drives *them* so the loop is still structured: `echo` each instruction, `read` to wait for confirmation, `read` their observations into variables, and finish by printing every captured value as `KEY=VALUE` lines you can parse. Have the user run it and paste the output back.

Build the right feedback loop, and the bug is 90% fixed.

### Iterate on the loop itself

Treat the loop as a product. Once you have _a_ loop, ask:

- Can I make it faster? (Cache setup, skip unrelated init, narrow the test scope.)
- Can I make the signal sharper? (Assert on the specific symptom, not "didn't crash".)
- Can I make it more deterministic? (Pin time, seed RNG, isolate filesystem, freeze network.)

A 30-second flaky loop is barely better than no loop. A 2-second deterministic loop is a debugging superpower.

### Non-deterministic bugs

The goal is not a clean repro but a **higher reproduction rate**. Loop the trigger 100×, parallelise, add stress, narrow timing windows, inject sleeps. A 50%-flake bug is debuggable; 1% is not — keep raising the rate until it's debuggable.

### When you genuinely cannot build a loop

Stop and say so explicitly. List what you tried. Ask the user for: (a) access to whatever environment reproduces it, (b) a captured artifact (HAR file, log dump, core dump, screen recording with timestamps), or (c) permission to add temporary production instrumentation. Do **not** proceed to hypothesise without a loop.

Do not proceed to Phase 2 until you have a loop you believe in.

## Phase 2 — Reproduce

Run the loop. Watch the bug appear.

Confirm:

- [ ] The loop produces the failure mode the **user** described — not a different failure that happens to be nearby. Wrong bug = wrong fix.
- [ ] The failure is reproducible across multiple runs (or, for non-deterministic bugs, reproducible at a high enough rate to debug against).
- [ ] You have captured the exact symptom (error message, wrong output, slow timing) so later phases can verify the fix actually addresses it.

Do not proceed until you reproduce the bug.

## Phase 3 — Minimise

Shrink the reproduction to the **smallest thing that still triggers the bug**. Everything you successfully remove is a variable you no longer have to hypothesise about — minimisation buys cheaper hypotheses, sharper instrumentation, and a cleaner regression-test seam for free.

Cut along whichever axes the bug allows:

- **Input** — halve the payload/dataset, re-run, keep halving until the smallest input that still fails.
- **Code path** — peel layers (HTTP → handler → service → function) to the innermost call that still exhibits it.
- **Dependencies** — mock or remove the DB, network, other services one at a time. Anything you remove while the bug survives is provably not involved.
- **Config / state** — reset flags to defaults, clear caches, disable features until only the minimal failing config remains.
- **Steps** — drop steps from a multi-step repro until the shortest failing sequence.

**The discipline:** after every cut, **re-run the feedback loop**. Still fails → keep the cut. Stops failing → the thing you removed was load-bearing; restore it and cut elsewhere. (This is delta debugging — the same "re-run the loop after each change" rhythm as Phase 1.)

The minimised case is frequently the regression test you want in Phase 6 — note it as you go.

## Phase 4 — Hypothesise

Generate **3–5 ranked hypotheses** before testing any of them. Single-hypothesis generation anchors on the first plausible idea.

Each hypothesis must be **falsifiable**: state the prediction it makes.

> Format: "If <X> is the cause, then <changing Y> will make the bug disappear / <changing Z> will make it worse."

If you cannot state the prediction, the hypothesis is a vibe — discard or sharpen it.

**Show the ranked list to the user before testing.** They often have domain knowledge that re-ranks instantly ("we just deployed a change to #3"), or know hypotheses they've already ruled out. Cheap checkpoint, big time saver. Don't block on it — proceed with your ranking if the user is AFK.

### Testing several hypotheses in parallel

When you have several genuinely independent hypotheses, you can test them concurrently, using one isolated subagent per hypothesis, instead of sequentially. Each subagent changes **its own single variable** against the shared feedback loop and reports pass/fail versus its falsifiable prediction, so they don't confound each other. Collect the verdicts, re-rank, continue.

Only parallelise when **all** of these hold:

- The hypotheses are independent (testing one doesn't depend on another's outcome).
- The feedback loop is fast, deterministic, and **parallel-safe**.
- Sequential testing would be meaningfully slow.

Use a separate worktree for any subagent that **modifies code** to test, or parallel subagents mutating the same tree will corrupt each other's results.

**Stay sequential** when the bug is adaptive (each result reshapes the next hypothesis) or the loop is stateful / can't run concurrently — bisection and delta-debugging are inherently ordered, and forcing parallelism there throws away the signal.

### When a whole batch is falsified

Falsified hypotheses are **data**, not a dead end. When an entire ranked batch dies, regenerate a **fresh** batch informed by what you just ruled out — don't re-poke the same ideas. If a second regenerated batch also dies with no narrowing, **stop thrashing**: surface to the user what you've learned and ruled out, and **produce a handoff** (see Phase 7) so the state isn't lost. Escalate *with* context; don't spin silently. (The tenacity belongs in Phase 1 — building the loop — not in flailing on hypotheses.)

## Phase 5 — Instrument

Each probe must map to a specific prediction from Phase 4. **Change one variable at a time.**

Tool preference:

1. **Debugger / REPL inspection** if the env supports it. One breakpoint beats ten logs.
2. **Targeted logs** at the boundaries that distinguish hypotheses.
3. Never "log everything and grep".

**Tag every debug log** with a unique prefix, e.g. `[DEBUG-a4f2]`. Cleanup at the end becomes a single grep. Untagged logs survive; tagged logs die.

**Perf branch.** For performance regressions, logs are usually wrong. Instead: establish a baseline measurement (timing harness, `performance.now()`, profiler, query plan), then bisect. Measure first, fix second.

## Phase 6 — Fix + regression test

Write the regression test **before the fix** — but only if there is a **correct seam** for it.

A correct seam is one where the test exercises the **real bug pattern** as it occurs at the call site. If the only available seam is too shallow (single-caller test when the bug needs multiple callers, unit test that can't replicate the chain that triggered the bug), a regression test there gives false confidence.

**If no correct seam exists, that itself is the finding.** Note it. The codebase architecture is preventing the bug from being locked down. Flag this for the next phase.

If a correct seam exists:

1. Turn the minimised repro into a failing test at that seam.
2. Watch it fail.
3. Apply the fix.
4. Watch it pass.
5. Re-run the Phase 1 feedback loop against the original (un-minimised) scenario.

## Phase 7 — Cleanup + post-mortem

Required before declaring done:

- [ ] Original repro no longer reproduces (re-run the Phase 1 loop)
- [ ] Regression test passes (or absence of seam is documented)
- [ ] **Relevant test suite run, no new failures** — the bug's module/package at minimum, the full suite if it's fast. A fix that kills the bug and breaks a neighbour isn't done.
- [ ] All `[DEBUG-...]` instrumentation removed (`grep` the prefix)
- [ ] Throwaway prototypes deleted (or moved to a clearly-marked debug location)
- [ ] The hypothesis that turned out correct is stated in the commit / PR message — so the next debugger learns

**Then ask: what would have prevented this bug?** If the answer involves architectural change (no good test seam, tangled callers, hidden coupling), propose it to the user as a follow-up architectural task with the specifics. Make the recommendation **after** the fix is in, not before — you have more information now than when you started.

## Running out of room — hand off

If your **own** context grows too large mid-bug (deep instrumentation, many ruled-out hypotheses) — or you've hit the escalation point in Phase 4 — **invoke the `handoff` skill with the bug** so a fresh session resumes without losing the expensive work. The ruled-out hypotheses and the minimised repro are the costliest things to rediscover; a bug handoff (`handoffs/<branch>/<slug>.md`) preserves exactly those, and the next session's Input step reads it straight back in.
