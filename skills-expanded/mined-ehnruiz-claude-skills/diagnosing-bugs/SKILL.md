---
name: diagnosing-bugs
description: A disciplined loop for hard bugs, flaky tests and performance regressions - build a red-capable feedback loop first, reproduce and minimize, rank falsifiable hypotheses, instrument one variable at a time, then repair and remove the probes. Use when the user says "diagnose", "debug this" or "why is this failing", reports a wrong result, a crash, a timeout, a flaky test or a slowdown, or when a first-glance fix did not hold.
---

# Diagnosing bugs

A discipline for hard bugs. Skip a phase only when you can say why. Credit and license:
`LICENSE.md` in this folder.

**Project copy first.** If the repository has its own `.claude/skills/diagnosing-bugs/SKILL.md`, read it and follow it instead of this file. A skill installed for all your projects outranks a project skill with the same name, so without this step a repository's own version of this skill would never run.

Before exploring, read the project's architecture and known-limitations docs if it has them;
some "bugs" are documented gaps.

## Redact

You will show commands, outputs and captured artifacts. **Redact every secret first**: write
`<REDACTED>` in its place. Build loops against environment variables so tokens, webhook URLs
and cookies stay in the environment, not in what you show. Quote only the lines that carry
the signal.

## Phase 1: Build a feedback loop

**This is the skill.** With a tight pass/fail signal that goes red on *this* bug, you will
find the cause; bisection, hypotheses and instrumentation all just consume it. Without one,
no amount of reading code will save you. Spend disproportionate effort here.

Ways to build one, roughly cheapest first:

1. **A failing unit test** at the public seam closest to the symptom, with hand-built input.
2. **A fixture or integration test**: plant the defect in test data and assert on it.
3. **The real entry point, narrowed**: the CLI, endpoint or job run against one input, with
   everything not under suspicion turned off.
4. **Replay**: capture the input once (a request, a payload, a saved page) and replay it
   offline, so the network or browser leaves the loop.
5. **A throwaway script** that drives the browser, API or queue and asserts on the symptom.
6. **Differential**: the same input through the last known-good commit and HEAD, diffing
   the output. Compare runtime and dependency versions first.
7. **Bisection**: when the bug appeared between two known states, automate "check out, run
   the loop, report" so `git bisect run` drives it.
8. **Loop the trigger** for a flaky test (shuffle with a fixed seed, run 100 times) until
   the reproduction rate is high enough to debug.

**Tighten the loop** once you have one: faster (one test, one input), sharper (assert the
exact symptom, not "did not crash"), deterministic (pin time, seed randomness, freeze the
network).

**If you cannot build one**, stop and say so. List what you tried and ask the user for the
artifact you need: a redacted log, the failing run's link, a captured payload, access to
the environment. Do not move to hypotheses without a loop.

**Phase 1 is done** when you can name one command you have already run at least once (show
it and its exit code, redacted) that goes red on this bug and will go green when it is
fixed, is deterministic, runs in seconds and needs no human.

If you catch yourself reading code to build a theory before that command exists, stop:
that is the exact failure this skill prevents.

## Phase 2: Reproduce and minimize

Run the loop and watch it go red. Confirm it is the failure the user described, not a nearby
one. Then cut inputs, config and steps one at a time, re-running after each cut, until every
remaining element is load-bearing.

## Phase 3: Hypothesize

Write **3 to 5 ranked hypotheses** before testing any. Each must be falsifiable: "if X is the
cause, changing Y makes the bug disappear." Show the list to the user before testing;
continue with your ranking if they are away.

## Phase 4: Instrument

One probe per prediction. **Change one variable at a time.** Prefer a debugger session to
logging; when you log, tag every line with a unique prefix such as `[DEBUG-a4f2]` so cleanup
is one grep. For a slowdown, measure before you bisect: find which stage grew, then time
only that stage.

## Phase 5: Fix behind a regression test

Write the regression test **before** the fix, at a real seam, exercising the actual bug
pattern. If the only seam available is too shallow to catch it, that is a finding; record it.
Watch the test fail. If you forced the red by editing code or a fixture, `diff` it against an
untouched copy to prove the edit landed before you trust the failure. An edit that silently
changed nothing would otherwise pass as a failing test. Then apply the fix, watch it pass, and re-run the
Phase 1 loop on the original scenario. The `regression-proof` skill shows how to prove the test fails without
the fix.

## Phase 6: Clean up

Before declaring done:

- [ ] The original repro no longer reproduces (re-run the Phase 1 loop; show the exit code)
- [ ] The regression test passes, or the missing seam is documented in the PR
- [ ] Every `[DEBUG-...]` line is gone (`grep -rn "DEBUG-"` over the source and tests)
- [ ] Scratch scripts, configs and captured artifacts are deleted
- [ ] The hypothesis that turned out right is in the commit message, so the next person
      debugging learns from it
