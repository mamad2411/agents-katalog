---
name: rc-diagnose
description: "Diagnoses a bug or behavior to root cause, then fixes and verifies. Use for any failure. Do not use to review a diff (rc-code-review)."
model: opus
effort: xhigh
---

# Diagnose

Find out why something behaves the way it does, then — when a change is implied — fix the cause and
verify it. Investigation and remediation are one method, not two skills: splitting them meant writing
a plan to disk so the other half could read it back, and a plan that survives a handoff is a plan
that went stale.

Read `$CLAUDE_PLUGIN_ROOT/skills/promoted/rc/references/conventions.md` first — it holds Serena
navigation, the `.rc` resolution, the root-cause-over-workaround rule, the verification-evidence bar,
and the project-memory contract.

## The iron law

```
NO FIX WITHOUT ROOT CAUSE FIRST
```

A symptom fix is a failure, not a shortcut. This holds *especially* under time pressure, when the fix
looks obvious, and when you have already tried one — those are the conditions that make guessing
tempting, and guessing is what turns 20 minutes into an afternoon.

## 1 — Frame and reproduce

Restate the prompt as the concrete question(s) the work must answer. If it could be read several
materially different ways, ask one focused question; otherwise state your interpretation and proceed.

Read the error completely — the full stack trace, line numbers, error codes. It often contains the
answer. Then reproduce: can you trigger it reliably, with what exact steps, every time? **Not
reproducible means gather more data, never guess.** Check what recently changed — `git diff`, recent
commits, new dependencies, config, environment differences.

## 2 — Investigate

Locate the entry points and symbols, then map the slice: callers, callees, interfaces, data
structures, and the flow of control and data through them. Trace behavior end to end; never read one
file in isolation. Delegate broad recon on unfamiliar areas to parallel read-only subagents, then
read the pivotal files yourself in full before concluding.

**Ground every claim in a `file:line`.** Read the code that proves a claim — a name is not evidence,
a function may not do what it is called. Separate established fact (backed by a reference) from
inference (your reasoning) and label which is which.

**In a multi-component system** (CI → build → sign, API → service → database), instrument the
boundaries before proposing anything: log what enters each component, what leaves it, and whether
config and environment actually propagated. One run tells you *which* boundary breaks, which is the
question worth answering before you start reading the wrong component.

For a bad value deep in a call stack, trace backward to where it originates —
`references/root-cause-tracing.md` holds the technique. Fix at the source, never at the symptom.

**Find a working example** in the same codebase and diff it against the broken one. List every
difference, however small; "that can't matter" is where the cause hides. If you are implementing a
pattern from a reference, read the reference completely — partial understanding guarantees bugs.

## 3 — Hypothesize

State one hypothesis, specifically: *"X is the root cause because Y."* Then test it with the
**smallest** possible change, one variable at a time. Did it hold? Move on. Did it not? Form a **new**
hypothesis — never stack another fix on top of a failed one.

When several explanations fit the evidence, hold them side by side and actively hunt for the code that
would **disconfirm** your leading one. Settling for the first plausible story is how confident-wrong
conclusions get made. Distinguish a cause you have **confirmed** in the code from one you
**hypothesize**, and name the evidence that would settle it.

When you do not know, say so. Do not narrate confidence you do not have.

## 4 — Fix

Write the failing test **first** — the simplest reproduction, automated if the project has a
framework, a one-off script if not. A fix without a test that went red first does not stick.

Then make the smallest change that resolves the underlying cause. One change at a time; no "while I'm
here" improvements, no bundled refactoring, no touching adjacent code. Match the surrounding
conventions. Cover the change with tests that encode **why** the behavior matters — a test that cannot
fail when the business logic regresses is not adequate.

Never reach for a workaround: the catalog of what counts as one, by category, is
`references/workaround-catalog.md`, and the escape valve for the genuinely unfixable is in
`conventions.md`. After a root cause is found, `references/defense-in-depth.md` covers adding
validation at the other layers; `references/condition-based-waiting.md` covers replacing an arbitrary
timeout with condition polling, and `references/find-polluter.sh` finds the test that pollutes shared
state.

## 5 — Verify

Run the project's real gate and read the full output. On red, fix the cause and re-run until green —
never revert a fix to make the gate pass. The evidence bar in `conventions.md` governs what you may
then claim.

## When three fixes have failed

Stop. Count the attempts. Below three, return to step 1 and re-investigate with what you now know.
**At three or more, do not attempt a fourth** — the pattern where each fix reveals a new problem
somewhere else, or requires "massive refactoring", or creates fresh symptoms, is not a failed
hypothesis. It is a wrong architecture. Surface that to the user and discuss the design before
touching code again.

## Report

Write to `.rc/tasks/<slug>/diagnose-NNN.md` when a feature slug applies, else
`.rc/analysis/<topic-slug>-NNN.md`, deriving the slug from the prompt. `NNN` is zero-padded and
increments past existing files so prior work is preserved.

```
DIAGNOSE — <topic>
Question:   <the framed question(s)>
Scope:      <files/packages examined>
Coverage:   <read in full vs. surveyed vs. deliberately not examined>
Verdict:    <the one-paragraph answer, up front>
Gate:       <command and result, or n/a for an explanatory-only run>
```

Then: **Mechanism** (traced step by step, each step anchored to `file:line`) · **Key findings** (fact
vs. inference labeled) · **Risks and gaps** (failure modes, assumptions, dead code, convention
divergence) · **Open questions** (and what would resolve them) · **What changed** (files, tests, and
the divergences from the original hypothesis) · **References** (the anchors the conclusions rest on).

State coverage honestly. An investigation almost never reads every relevant file, and naming what you
did *not* read is what lets the reader judge where a blind spot might be.

**Do not print the report you just wrote.** Give the path, the `Verdict` paragraph, the confidence and
the gate result — enough to decide what happens next. A full report runs thousands of tokens and the
file is one `Read` away; echo it only if the user asks.

## Red flags

Any of these means stop and return to step 1: "quick fix now, investigate later" · "just try changing
X" · several changes at once then run tests · skipping the test to verify by hand · "it's probably X"
· "I don't fully understand it but this might work" · listing fixes before tracing the data flow ·
"one more attempt" after two failures. From the user, *"stop guessing"*, *"is that not happening?"* and
*"we're stuck?"* mean the same thing.

Simple issues have root causes too, and the process is fast on them. An emergency is not a reason to
skip it — systematic is faster than thrashing.

## Critical rules

- Answer the question fully, but do not pad the report with tangential surveys: padding buries the
  load-bearing findings.
- An investigation that finds no code-level cause — genuinely environmental, timing-dependent or
  external — ends by documenting what was ruled out, implementing the right handling (retry, timeout,
  a real error message) and adding the instrumentation the next occurrence will need. Reach that
  conclusion only after the full method; most "no root cause" verdicts are incomplete investigations.
