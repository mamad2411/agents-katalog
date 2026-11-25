---
name: fable-mode
description: Use PROACTIVELY the moment a task has many layers — multiple dependent steps, unknowns that could change the approach, debugging where the first theory might be wrong, or anything that needs verification before handoff. Also use when a task keeps failing or stalling, or when the founder says "slow down and do this right", "think this through first", or "use the five gates". Loads the five-gate task loop so the session applies the full working discipline.
---

# Fable Mode — the five-gate task loop, as a callable skill

This is the invokable form of the method documented in [`docs/03-the-five-gates.md`](../../docs/03-the-five-gates.md) — read that for the full essay; this file is the execution checklist. It changes how you run the *current* task; it produces no files of its own.

A hard task is anything where the first idea might be wrong. For a one-file edit or a simple lookup, skip the gates and just do the work.

## Run the gates in order — a gate must pass before the next opens

**Gate 1 — Scope.** Write done in 1–2 sentences + the check that proves it. Load standing rules (MEMORY.md, RULES.md). Name the 1–3 load-bearing unknowns. Ambiguity that changes the build → one question at the biggest gap; otherwise state your default and proceed.

**Gate 2 — Evidence.** Open the real file/API/page before designing against it; training memory is only a hypothesis generator. Recalled workspace memory is dated evidence — recency-gate it. Cheapest probe of the biggest unknown first. One item end-to-end before scaling to N.

**Gate 3 — Adversarial.** Try to kill your answer — and *test* the killing case, don't imagine it. Steelman the existing thing before changing it. Re-decide after every tool result. Two failed attempts at the same fix = wrong diagnosis: stop patching, test the assumption underneath. "Already solid" is a legitimate finding.

**Gate 4 — Verify.** "It ran" ≠ verified. Verify at the layer of the claim with evidence you didn't generate (live page, screenshot, diff, count). Sample the tails. A suspiciously clean result = broken verification until explained.

**Gate 5 — Report.** Lead with the answer. Separate verified from assumed, out loud, with specifics. Report observations, not intentions. Never state as fact what you haven't verified this session.

## When stalled, name your gate

Stalling or surprised by a result? Say which gate you're at and re-run it. The smell list (three attempts at one fix, "should work", building on unopened data, a too-clean sweep) is in the doc — any one smell means stop and step back a gate.

## Stacking

This skill sequences the task; it doesn't replace task-specific tools. Content that ships still passes both `content-gate/` gates; research-backed claims still go through `deep-research`; the session still closes with `session-close`. Fable mode decides *when* to reach for them.

## Escalation rule

If a task keeps failing under this discipline, that's the signal to bring the founder a calibrated blocker report (or try a stronger model) — not to loosen the process. Keep the discipline either way.
