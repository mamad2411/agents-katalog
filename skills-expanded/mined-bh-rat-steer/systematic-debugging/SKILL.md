---
name: systematic-debugging
description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes
license: MIT
metadata:
  version: 0.1.0
---

# Systematic Debugging

Random fixes waste time and create new bugs. Quick patches mask
underlying issues.

**Core principle:** ALWAYS find root cause before attempting fixes.
Symptom fixes are failure.

This skill bundles its own steer runtime at `scripts/steer.py`; the
commands below invoke it with `python3` and need nothing installed.
Paths are relative to this skill's directory: when your working
directory is elsewhere (it usually is), use the skill's full path
(`python3 <path-to-this-skill>/scripts/steer.py ...`).

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

In this skill the law is machine-enforced: the flow below keeps the fix
step locked until the investigation artifacts actually exist. You cannot
propose fixes in Phase 1 because the flow will not let you get there.

## When to Use

Use for ANY technical issue: test failures, bugs in production,
unexpected behavior, performance problems, build failures, integration
issues.

**Use this ESPECIALLY when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work
- You don't fully understand the issue

**Don't skip when:**
- Issue seems simple (simple bugs have root causes too)
- You're in a hurry (rushing guarantees rework)
- Manager wants it fixed NOW (systematic is faster than thrashing)

## Process

The four phases are an enforced flow; steps verify themselves against
artifacts in `out/debug/`, and you cannot skip ahead.

1. Announce: "Working through the systematic-debugging flow."
2. Run `python3 scripts/steer.py flow status` (in the workspace) to see the current phase.
3. Do what the directive says, guided by the phase notes below.
4. Run `python3 scripts/steer.py flow next` and repeat until all steps report complete.

Do NOT claim the bug is fixed while `python3 scripts/steer.py flow status` shows incomplete
steps. The flow is defined in `flow.toml`.

### Phase 1: Root Cause Investigation (step: investigate)

BEFORE attempting ANY fix:

1. **Read error messages carefully.** They often contain the exact
   solution. Read stack traces completely; note line numbers, file
   paths, error codes.
2. **Reproduce consistently.** Can you trigger it reliably? What are the
   exact steps? If not reproducible, gather more data; don't guess.
3. **Check recent changes.** Git diff, recent commits, new dependencies,
   config changes (git diff, git log).
4. **Gather evidence in multi-component systems.** For each component
   boundary, log what enters and what exits, and verify config
   propagation. Run once to see WHERE it breaks, then investigate that
   component. When the error is deep in a call stack, first read
   `references/root-cause-tracing.md`.

Everything you find goes in `out/debug/evidence.md`; the flow checks it
exists before Phase 2 unlocks.

### Phase 2: Pattern Analysis (step: analyze)

1. **Find working examples.** Locate similar working code in the same
   codebase.
2. **Compare against references.** If implementing a pattern, read the
   reference implementation COMPLETELY. Don't skim; read every line.
3. **Identify differences.** List every difference between working and
   broken, however small. Don't assume "that can't matter." The list
   goes in `out/debug/comparison.md`.
4. **Understand dependencies.** What components, settings, and
   assumptions does the working version rely on?

### Phase 3: Hypothesis and Testing (step: hypothesize)

1. **Form a single hypothesis.** Write `out/debug/hypothesis.md`:
   "I think X is the root cause because Y." Be specific.
2. **Test minimally.** The SMALLEST possible change that tests the
   hypothesis. One variable at a time.
3. **Verify before continuing.** Confirmed? Move on. Wrong? Form a NEW
   hypothesis; do NOT stack more fixes on top.
4. **When you don't know, say so.** "I don't understand X" beats
   pretending. Research or ask for help.

### Phase 4: Implementation (steps: failing-test, fix)

1. **Create a failing test case first.** Simplest possible reproduction,
   automated if a test framework exists. Record the command and its
   failing output in `out/debug/failing-test.md`; the fix step stays
   locked until it exists. The test-driven-development skill, if
   installed, covers writing proper failing tests.
2. **Implement a single fix** at the root cause. ONE change at a time.
   No "while I'm here" improvements, no bundled refactoring.
3. **Verify:** the failing test passes, no other tests broke, the issue
   is actually resolved. Then, and only then: `python3 scripts/steer.py flow done fix`.
4. **If the fix didn't work:** STOP. Count your attempts. Under three:
   return to Phase 1 and re-analyze with the new information (delete the
   stale artifacts in `out/debug/` so the flow re-gates). Three or more:
   stop fixing.
5. **If 3+ fixes failed, question the architecture.** Each fix revealing
   a new problem elsewhere, fixes needing "massive refactoring", new
   symptoms after every change: that is not a failed hypothesis, that is
   a wrong architecture. Discuss with your human partner before
   attempting more fixes.

## Red Flags - STOP and Follow Process

If you catch yourself thinking:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "Pattern says X but I'll adapt it differently"
- "Here are the main problems: [lists fixes without investigation]"
- Proposing solutions before tracing data flow
- **"One more fix attempt" (when already tried 2+)**
- **Each fix reveals new problem in different place**

**ALL of these mean: STOP. Return to Phase 1.**
`python3 scripts/steer.py flow status` will tell you exactly which phase you are really in;
capture the rationalization you caught yourself in (see Learning).

## Your Human Partner's Signals You're Doing It Wrong

Watch for these redirections:
- "Is that not happening?" - You assumed without verifying
- "Will it show us...?" - You should have added evidence gathering
- "Stop guessing" - You're proposing fixes without understanding
- "Ultra-think this" - Question fundamentals, not just symptoms
- "We're stuck?" (frustrated) - Your approach isn't working

When you see these: STOP. Return to Phase 1.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process is fast for simple bugs. |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start. |
| "I'll write test after confirming fix works" | Untested fixes don't stick. Test first proves it. |
| "Multiple fixes at once saves time" | Can't isolate what worked. Causes new bugs. |
| "Reference too long, I'll adapt the pattern" | Partial understanding guarantees bugs. Read it completely. |
| "I see the problem, let me fix it" | Seeing symptoms is not understanding root cause. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem. Question pattern, don't fix again. |

## When Process Reveals "No Root Cause"

If systematic investigation shows the issue is truly environmental,
timing-dependent, or external: you've completed the process. Document
what you investigated, implement appropriate handling (retry, timeout,
error message), and add monitoring for future investigation.

**But:** 95% of "no root cause" cases are incomplete investigation.

## Learning

This skill improves with use. As you work:

- A disproven hypothesis, a rationalization you caught yourself in, or a
  technique that cracked the case is a lesson; capture it the moment it
  happens: `python3 scripts/steer.py learn note "<one imperative rule>" --kind correction`
- At the start of a debugging session, run
  `python3 scripts/steer.py learn show`; those lessons came
  from real previous bugs. Confirm the ones that helped
  (`python3 scripts/steer.py learn confirm <id>`), dispute the
  ones that misled.
- Before finishing, record the outcome:
  `python3 scripts/steer.py learn run ok` (or `failed` with
  `--note`).

If a `learnings.md` exists in this skill, read it too; those are
promoted lessons that shipped with the skill.

## References

Supporting techniques, loaded only when that branch is hit:

- Bug deep in a call stack: first read `references/root-cause-tracing.md`
  (backward tracing to the original trigger; includes the bisection
  script `scripts/find-polluter.sh`).
- Adding validation after the root cause is found: read
  `references/defense-in-depth.md`.
- Flaky waits and arbitrary timeouts: read
  `references/condition-based-waiting.md` (worked example in
  `references/condition-based-waiting-example.ts`).

Related skills, if installed: test-driven-development (Phase 4, step 1),
verification-before-completion (verify the fix before claiming success).

## Real-World Impact

From debugging sessions:
- Systematic approach: 15-30 minutes to fix
- Random fixes approach: 2-3 hours of thrashing
- First-time fix rate: 95% vs 40%
- New bugs introduced: near zero vs common
