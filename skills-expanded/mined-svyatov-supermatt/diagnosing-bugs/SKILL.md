---
name: diagnosing-bugs
description: Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug this", or reports something broken/throwing/failing/slow.
metadata:
  credits-skill: ce-debug
  credits-author: Every
  credits-url: "https://github.com/EveryInc/compound-engineering-plugin/tree/main/skills/ce-debug"
license: MIT
---

# Diagnosing Bugs

A discipline for hard bugs. Skip phases only when explicitly justified.

When exploring the codebase, read the glossary (`docs/agents/domain.md` gives the layout; by default `GLOSSARY.md` at the root, if it exists) to get a clear mental model of the relevant modules, and check ADRs in the area you're touching.

**Start from prior attempts.** If the user says they have been trying, ask what they tried before you start, so you skip their dead ends. If they link an issue, read the whole thread, latest comments first: they often carry newer repro steps or a different suspect. Run `git log --oneline -10 -- <file>` on the files you read to see what changed recently.

## Redact

This skill has you show commands, outputs and captured artifacts. **Redact every secret first**: write `<REDACTED>` in its place. Build loops against env vars, so the credential stays in the environment rather than in what you show. Captured artifacts carry auth headers: quote only the lines that carry the signal.

If the redacted output is not enough to diagnose the bug, say so and ask the user.

## Phase 1: Build a feedback loop

**This is the skill.** Everything else is mechanical. If you have a **tight** pass/fail signal for the bug (one that goes red on _this_ bug), you will find the cause; bisection, hypothesis-testing, and instrumentation all just consume it. If you don't have one, no amount of staring at code will save you.

Spend disproportionate effort here. **Be aggressive. Be creative. Refuse to give up.**

Before writing a feedback-loop test, use a seam named in the spec or issue or explicitly confirmed by the user. Obtain confirmation for a newly discovered seam first, including when the test is only a temporary reproduction. While approval is pending, use a non-test reproduction such as a direct CLI or HTTP call. The Phase 5 gate applies here too.

### Ways to construct one, in roughly this order

1. **Failing test** at whatever seam reaches the bug: unit, integration, e2e.
2. **Curl / HTTP script** against a running dev server.
3. **CLI invocation** with a fixture input, diffing stdout against a known-good snapshot.
4. **Headless browser script** (Playwright / Puppeteer) that drives the UI and asserts on DOM/console/network.
5. **Replay a captured trace.** Save a real network request / payload / event log to disk; replay it through the code path in isolation.
6. **Throwaway harness.** Spin up a minimal subset of the system (one service, mocked deps) that exercises the bug code path with a single function call.
7. **Property / fuzz loop.** If the bug is "sometimes wrong output", run 1000 random inputs and look for the failure mode.
8. **Bisection harness.** If the bug appeared between two known states (commit, dataset, version), automate "boot at state X, check, repeat" so you can `git bisect run` it.
9. **Differential loop.** Run the same input through old-version vs new-version (or two configs) and diff outputs.
10. **HITL shell script.** Last resort. If a human must click, drive _them_ with [`scripts/hitl-loop.template.sh`](scripts/hitl-loop.template.sh) (bundled with this skill) so the loop is still structured: copy it, edit the steps, and ask the user to run it in their own terminal (in Claude Code, `! sh <path>` puts the output in the session). It reads from a TTY, so do not run it yourself. The printed `--- Captured ---` block feeds back to you.

Build the right feedback loop, and the bug is 90% fixed.

### Tighten the loop

Treat the loop as a product. Once you have _a_ loop, **tighten** it:

- Can I make it faster? (Cache setup, skip unrelated init, narrow the test scope.)
- Can I make the signal sharper? (Assert on the specific symptom, not "didn't crash".)
- Can I make it more deterministic? (Pin time, seed RNG, isolate filesystem, freeze network.)

A 30-second flaky loop is barely better than no loop; a 2-second deterministic one is tight, a debugging superpower.

### Non-deterministic bugs

The goal is not a clean repro but a **higher reproduction rate**. Loop the trigger 100×, parallelise, add stress, narrow timing windows, inject sleeps. A 50%-flake bug is debuggable; 1% is not, so keep raising the rate until it's debuggable.

### When you genuinely cannot build a loop

Stop and say so explicitly. List what you tried. Ask the user for: (a) access to whatever environment reproduces it, (b) a redacted captured artifact (HAR file, log dump, core dump, screen recording with timestamps), or (c) permission to add temporary production instrumentation. Do **not** proceed to hypothesise without a loop.

### Completion criterion: a tight loop that goes red

Phase 1 is done when the loop is **tight** and **red-capable**: you can name **one command** (a script path, a test invocation, a curl) that you have **already run at least once** (show the invocation and its output, redacted), and that is:

- [ ] **Red-capable**: it drives the actual bug code path and asserts the **user's exact symptom**, so it can go red on this bug and green once fixed. Not "runs without erroring"; it must be able to _catch this specific bug_.
- [ ] **Deterministic**: same verdict every run (flaky bugs: a pinned, high reproduction rate, per above).
- [ ] **Fast**: seconds, not minutes.
- [ ] **Agent-runnable**: you can run it unattended; a human in the loop only via `scripts/hitl-loop.template.sh`.

If you catch yourself reading code to build a theory before this command exists, **stop: jumping straight to a hypothesis is the exact failure this skill prevents.** No red-capable command, no Phase 2.

## Phase 2: Reproduce + minimise

Run the loop. Watch it go red as the bug appears.

Confirm:

- [ ] The loop produces the failure mode the **user** described, not a different failure that happens to be nearby. Wrong bug = wrong fix.
- [ ] The failure is reproducible across multiple runs (or, for non-deterministic bugs, reproducible at a high enough rate to debug against).
- [ ] You have captured the exact symptom (error message, wrong output, slow timing) so later phases can verify the fix actually addresses it.

### Rule out the environment

Confirm the environment is the one you think it is: the right branch, dependencies installed and current, the expected runtime version active, required env vars set, no stale build output (`dist/`, `.next/`, binaries from another branch).

**A dirty tree is a suspect.** When `git status` shows uncommitted work that could reach the failing code, test it before you suspect committed code:

1. Preserve the reproduction harness and its fixtures outside the worktree, with the same symptom assertion runnable against this checkout after stashing. If that is not possible, compare in a disposable worktree with only the harness changes applied instead and skip steps 2-4; require the same assertion to execute there too. Do not remove or overwrite main-worktree changes to construct the comparison.
2. `git stash push -u -m "diagnosing-bugs: without WIP"`. If it prints `No local changes to save`, nothing was stashed: skip to Minimise.
3. Re-run the preserved loop against the stashed checkout. Confirm the identical symptom assertion is present and actually executes. A missing test, fixture, dependency, or skipped assertion is an inconclusive comparison, not green.
4. Restore that exact entry, whatever the result (including a failed or inconclusive run): `git stash pop --index stash@{n}`, where `n` is the index of the `diagnosing-bugs: without WIP` entry in `git stash list`. On a conflict, show the user the output and the stash ref; leave the resolution to them.

The identical assertion goes green without the WIP: the uncommitted changes cause the difference; locate the responsible edit without attributing agent-created harness changes to the user. Loop stays red: the WIP is ruled out. An inconclusive comparison rules out nothing.

### Minimise

Once it's red, shrink the repro to the **smallest scenario that still goes red**. Cut inputs, callers, config, data, and steps **one at a time**, re-running the loop after each cut, and keep only what's load-bearing for the failure.

Why bother: a minimal repro shrinks the hypothesis space in Phase 3 (fewer moving parts left to suspect) and becomes the clean regression test in Phase 5.

Done when **every remaining element is load-bearing**: removing any one of them makes the loop go green.

Do not proceed until you have reproduced **and** minimised.

## Phase 3: Hypothesise

First, **audit your assumptions**: list the beliefs your picture of the bug depends on (this function returns what its name says, the config loads before this runs, the caller passes a non-null value) and mark each _verified_ (you read it, ran it, or checked state) or _assumed_. Many wrong hypotheses are right ones tested against a wrong assumption.

Then match the symptom against the known **bug classes** in [BUG-CLASSES.md](BUG-CLASSES.md) (timezone, encoding, cache staleness, concurrency and others). A match is a cheap first hypothesis.

Find a **working sibling**: similar code in the same codebase that works. List every difference between it and the broken path, however small. Each difference is a candidate hypothesis.

Generate **3-5 ranked hypotheses** before testing any of them. Single-hypothesis generation anchors on the first plausible idea.

Each hypothesis must be **falsifiable**: state the prediction it makes.

> Format: "If <X> is the cause, then <changing Y> will make the bug disappear / <changing Z> will make it worse."

If you cannot state the prediction, the hypothesis is a vibe: discard or sharpen it. A good prediction names something you have not looked at yet: another code path, another input, another observable. "`user` will be null when I log it" only restates "`user` is null", so it cannot catch a wrong hypothesis.

**Show the ranked list to the user before testing.** They often have domain knowledge that re-ranks instantly ("we just deployed a change to #3"), or know hypotheses they've already ruled out. Cheap checkpoint, big time saver. Don't block on it; proceed with your ranking if the user is AFK.

## Phase 4: Instrument

Each probe must map to a specific prediction from Phase 3. **Change one variable at a time.**

Tool preference:

1. **Debugger / REPL inspection** if the env supports it. One breakpoint beats ten logs.
2. **Targeted logs** at the boundaries that distinguish hypotheses.
3. **Stack capture** when you do not know who passes the bad value: log a stack trace (`new Error().stack`, `traceback.print_stack()`) just before the failing operation. In tests, write it to stderr; the test logger can swallow it.
4. Never "log everything and grep".

**Tag every debug log** with a unique prefix, e.g. `[DEBUG-a4f2]`. Cleanup at the end becomes a single grep. Untagged logs survive; tagged logs die.

A tagged probe that prints nothing was most likely never reached. Before you change how it prints, grep the tag to confirm it sits in the test the loop runs, above the call that fails.

**Perf branch.** For performance regressions, read [Performance comparisons](PERFORMANCE.md) before comparing changes. Establish a measured baseline with a timing harness, profiler, or query plan, then test one causal hypothesis at a time.

**Heisenbug.** If the bug goes away when you add a log or attach a debugger, the probe changed the timing or ordering: that is evidence, and the bug is still there. Suspect races, async ordering, and unflushed I/O. Observe from outside the path instead (in-memory buffer dumped after the failure, sampling profiler, `strace`/`dtrace`). A real fix still holds with the probe put back.

### Completion criterion: a causal chain with no gaps

Phase 4 is done when you can state the chain from trigger to symptom, each step with a `file:line` and an observed value that confirms it. "Somehow X leads to Y" is a gap: go back and probe it. No complete chain, no Phase 5.

## Phase 5: Fix + regression test

Record the current commit with `git rev-parse HEAD` before you change any code: it is the fixed point for the review in Phase 6.

**Fix at the source.** Walk the causal chain back from the symptom to where the bad value or state first appears, and fix it there. A guard where the error shows leaves every other path from the source still broken.

Once the cause is proven, search for other sites that make the same mistake. Check each site's inputs and expected behavior against the failing case. Leave correct uses intact. Report any confirmed instance outside scope with its location and evidence.

Write the regression test **before the fix**, but only if there is a **correct seam** for it.

A correct seam is one where the test exercises the **real bug pattern** as it occurs at the call site. If the only available seam is too shallow (single-caller test when the bug needs multiple callers, unit test that can't replicate the chain that triggered the bug), a regression test there gives false confidence.

**If no correct seam exists, that itself is the finding.** Note it. The codebase architecture is preventing the bug from being locked down. Report it to the user in Phase 6, and tell them to run `/improve-architecture` in Claude linked installs or Cursor, `/supermatt:improve-architecture` from the Claude plugin, `$improve-architecture` in Codex, or `/skill:improve-architecture` in OMP to find where the seam should go.

For each confirmed in-scope instance with a correct seam:

1. A seam is pre-agreed only if the spec or issue names it or the user explicitly confirmed it. Obtain confirmation for a newly discovered seam before writing tests. Then load and follow the `tdd` skill through the host's skill mechanism and turn the minimised repro into its failing test at that seam.
2. Apply the fix, and only the fix. A refactor bundled in hides which change turned the loop green.

After applying all confirmed in-scope fixes, rerun the Phase 1 feedback loop against the original (un-minimised) scenario. Use that result to judge the combined fix.

### When the fix fails

Revert it. State which evidence ruled the hypothesis out, then return to Phase 3 for a new hypothesis with its own prediction. A variant of the same theory ("maybe the other branch") is the same hypothesis.

After **2-3 dead hypotheses or 3 failed fixes**, the diagnosis is what is wrong. Match the pattern and show it to the user before you continue:

| Pattern | Diagnosis | Next move |
| --- | --- | --- |
| Hypotheses point at different subsystems | Design problem, not a local bug | Stop, present the findings, and suggest `/improve-architecture` in Claude linked installs or Cursor, `/supermatt:improve-architecture` from the Claude plugin, `$improve-architecture` in Codex, or `/skill:improve-architecture` in OMP |
| Evidence contradicts itself | Wrong mental model of the code | Re-read the path from its entry point, assuming nothing |
| Works locally, fails in CI/prod | Environment difference | Compare config, dependencies, data, timing |
| Fix works but the prediction was wrong | Symptom fix; the cause is still active | Keep investigating |

## Phase 6: Cleanup

Required before declaring done:

- [ ] Original repro no longer reproduces (re-run the Phase 1 loop)
- [ ] Regression test passes (or the missing seam is reported to the user as an architecture finding)
- [ ] All `[DEBUG-...]` instrumentation removed (`grep` the prefix)
- [ ] Throwaway debug harnesses deleted (or moved to a clearly-marked debug location)
- [ ] The full test suite passes
- [ ] The fix is committed, together with the regression test when a correct seam exists; otherwise the missing seam is reported as above. The commit message states the hypothesis that turned out correct, so the next debugger learns.
- [ ] The fix passes QA, unless an outer flow (such as `implement`) runs QA on this diff itself: write the bug report or captured symptom to a file in the OS temporary directory, then load and follow the `qa` skill through the host's skill mechanism, with the commit you recorded in Phase 5 as the fixed point and that file as the request. A fail is a symptom the fix left behind: take it back to Phase 3.
- [ ] The fix is reviewed, unless an outer flow (such as `implement`) reviews this diff itself: load and follow the `code-review` skill through the host's skill mechanism, with the commit you recorded in Phase 5 as the fixed point and, as the spec, the bug report file (write it now if the QA step was skipped). Fix every verified finding, at every severity, in the same turn, and commit the fixes. When the aggregate carries one, send the aggregate together with the first fix's tool call: a message with no tool call ends the turn and leaves the fixes to the user.
