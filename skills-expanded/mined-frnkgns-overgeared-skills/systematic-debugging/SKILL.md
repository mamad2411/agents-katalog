---
name: systematic-debugging
description: Find the root cause of a defect with a disciplined loop-to-evidence-to-hypothesis-to-fix workflow. Use when something is broken, behavior is unexpected, a build or test suddenly fails, a regression is reported, data reaches the wrong process/session/component, the user asks "why is this happening?", a symptom appears only intermittently, or several attempted fixes have already failed.
---
# Systematic Debugging

## Rule

Evidence before edits. Do not start with random code changes, and do not repeatedly patch symptoms.

## Phase 1 — Build a feedback loop

This phase is the skill. Everything after it consumes its output. Without a loop that goes red on this specific defect, bisection, hypothesis testing, and instrumentation are all guesswork dressed as method.

Construct the loop, roughly in this order:

1. A failing test at whatever seam reaches the defect.
2. A curl or HTTP script against a running dev server.
3. A CLI invocation with a fixed input, diffed against known-good output.
4. A headless browser script that drives the UI and asserts on the DOM, console, or network.
5. A replayed captured artifact: a real request, payload, or event log saved to disk and run through the path in isolation.
6. A throwaway harness exercising a minimal subset with one entry point.
7. A property or fuzz loop when the symptom is intermittent and wrong, running many inputs to expose the failure mode.
8. A bisection harness when the defect appeared between two known states.

Then tighten it. A loop is a product, not a means:

- Faster: cache setup, skip unrelated initialization, narrow scope.
- Sharper: assert the reported symptom, not merely that nothing crashed.
- More deterministic: pin time, seed randomness, isolate the filesystem, freeze the network.

A thirty-second flaky loop is barely better than none. A two-second deterministic one is a debugging instrument.

### Completion criterion

Phase 1 is done only when one command exists that has already been run at least once, with its output shown, and that is:

- **Red-capable**: drives the real defective path and asserts the reported symptom, so it can go red on this defect and green once fixed.
- **Deterministic**: the same verdict every run.
- **Fast**: seconds, not minutes.
- **Agent-runnable**: runnable unattended.

If you catch yourself forming a theory before this command exists, stop. Reading code to build a theory is the exact failure this phase prevents.

### Intermittent defects

The goal is a higher reproduction rate, not a clean reproduction. Run the trigger many times, add load, narrow timing windows, inject sleeps. A half-reproducing defect is debuggable; a one-percent defect is not.

### When no loop is possible

Stop and say so explicitly. List what was tried. Ask for access to a reproducing environment, a redacted captured artifact, or permission to add temporary instrumentation. Do not proceed to hypothesising without a loop.

## Phase 2 — Reproduce and minimise

Record before you reproduce:

- Expected behavior, in the user's terms.
- Actual behavior, including the exact error text or wrong output.
- Reproduction steps, as a sequence someone else could follow.
- Affected environment: project, branch, runtime and dependency versions.
- Evidence already available: logs, screenshots, captured payloads, failing command output.

Then run the loop and watch it go red. Confirm it produces the reported failure rather than a nearby one; the wrong defect means the wrong fix.

Then shrink the reproduction to the smallest case that still goes red. Cut inputs, callers, configuration, data, and steps one at a time, re-running after each cut, keeping only what is load-bearing. Removing any remaining element must turn the loop green.

Minimising shrinks the hypothesis space in Phase 3 and becomes the regression test in Phase 5.

## Trace the whole path

Trace execution and data across the real path, not just the reported location: entry point, boundaries, callers, persistence, asynchronous hops, and process or session ownership. Read the code that runs instead of assuming it does.

For a UI defect with data that arrives but does not render, walk every layer between them: response shape, then the mapping from response to view model, then component state, then filters, then pagination, then template conditions, then what is actually rendered. A defect at one layer commonly looks like a defect at another.

## Phase 3 — Hypothesise

Generate three to five ranked hypotheses before testing any. A single hypothesis anchors on the first plausible idea.

Each must be falsifiable and state its prediction:

> If X is the cause, then changing Y will make the defect disappear, or changing Z will make it worse.

A hypothesis with no testable prediction is a hunch; sharpen it or discard it.

Show the ranked list before testing. The user often knows which candidates are already ruled out. Do not block on their reply; proceed with your ranking.

## Phase 4 — Instrument

Every probe targets one specific prediction. Change one variable at a time.

Prefer a debugger or REPL when the environment supports one; a single breakpoint beats ten logs. Otherwise add targeted logs at the boundaries that distinguish hypotheses. Never log everything and search.

Tag every temporary log with a unique prefix such as `[DEBUG-a4f2]` so cleanup becomes one search. Untagged logs survive.

For performance regressions, logging is usually the wrong instrument. Establish a baseline measurement first, then narrow by measurement.

## Phase 5 — Fix and regression test

Write the regression test before the fix, but only where a correct seam exists.

A correct seam exercises the real defect pattern as it occurs at the call site. When the only available seam is too shallow to reproduce the chain that caused the defect, a test there gives false confidence.

**When no correct seam exists, that absence is itself the finding.** Record it: the structure is preventing this class of defect from being locked down.

Where a correct seam exists:

1. Turn the minimised reproduction into a failing test at that seam.
2. Confirm the failure is the intended one. If it was forced by mutating code or a fixture, diff against a pristine copy to prove the mutation landed.
3. Apply the fix.
4. Watch it pass.
5. Re-run the Phase 1 loop against the original, unminimised scenario.

## Phase 6 — Clean up

Before reporting done:

- The original reproduction no longer reproduces.
- The regression test passes, or the missing seam is documented.
- All tagged instrumentation is gone.
- Throwaway harnesses are deleted or moved to an explicitly marked debug location.

## Redundancy check

Before planning a fix, check whether the behavior already exists. Search by the domain concept rather than the wording of the request, and report where you looked. An existing implementation turns this into a different task entirely.

## Capture the outcome

A confirmed root cause is durable knowledge. Record it through `knowledge-vault` in the established locations: the cause and its correction belong in `issues/bugs/`, and a rejected approach someone would otherwise retry belongs in `attempts/`. Record the failed attempts too, not only the one that worked; the discarded path is what stops the next session repeating it.

## Rules

- Do not weaken, delete, or bypass a failing check to make the symptom disappear.
- Do not assume the newest change is the cause; confirm with Git history or evidence.
- Distinguish root cause from secondary effects such as stale cache, wrong session, or duplicated state.
- If several fixes have failed, stop patching and return to evidence gathering. Repeating an identical approach requires new evidence, a changed condition, or a stated difference.
- A passing build is build evidence only. It does not prove the reported defect is fixed.
- Implement only when implementation is requested or authorized; stay read-only for review-only tasks.
- Keep the preserved evidence (commands run, files inspected, hypotheses tested) for the final report.

## Reporting

State the root cause, the evidence that proves it, the fix applied, and the verification that was actually run. Distinguish confirmed causes from remaining uncertainties. Never claim the issue is resolved without rerunning the reproduction. When runtime access was unavailable, say "implemented; runtime verification pending" with the exact remaining steps rather than claiming success.
