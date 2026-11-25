---
name: debug
description: "Use when hitting a bug, a test or CI failure, unexpected behavior, or when about to claim something is fixed and the root cause is not yet proven with evidence."
---

# Debug

> **Output language:** answer and write artifacts in the user's own language (match their messages, not the repo's history).

## Overview

Fuses systematic root-cause debugging with **verification-before-completion**.

**Core principle: evidence before fixes; evidence before "fixed" claims.**

**Announce:** "Using debug to …"

## When to Use

- Any bug, flaky test, build/CI failure, unexpected behavior, performance mystery
- Especially under time pressure ("just one quick fix")
- Before claiming "done" / "passing" / "fixed"

**When NOT to use:** pure greenfield feature with no failure (use **grill** / **write-spec** / **write-plan** / **tdd**).

## The Iron Law

```
1. NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.
2. NO "FIXED" / "PASSING" / "DONE" CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE IN THIS TURN.
```

**Violating the letter is violating the spirit.**

## Workflow (phases — do in order)

### Phase 1 — Investigate (no fix yet)

1. Read the full error / stack / logs (don't skim)
2. Reproduce consistently — if you can't, gather data, don't guess
3. Check recent changes (`git diff`, commits, config, env)
4. Multi-component systems: instrument **boundaries** (in → out) to see *where* it breaks
5. Trace bad values backward to the source; plan to fix at source

Create todos for these steps; **do not edit production logic** until Phase 1 has a stated root cause.

### Phase 2 — Pattern

- Find a working similar path in-repo
- Diff working vs broken; list every difference
- Note dependencies / assumptions

### Phase 3 — Hypothesis

- One hypothesis: "X is root cause because Y"
- Design the **smallest** test/probe that would falsify it
- If wrong → new hypothesis (don't stack random changes)

### Phase 4 — Fix via TDD

1. **tdd** + **test-design**: write a failing regression that locks the bug
2. Watch RED for the right reason
3. Minimal fix → GREEN
4. **Verify** (below) before any success language

### Phase 5 — Verify before claims (mandatory)

Before saying fixed/passing/done/complete:

1. IDENTIFY the command that proves the claim
2. RUN it fresh (full command)
3. READ exit code and failures
4. ONLY THEN claim, **with the evidence**

| Claim | Requires |
|-------|----------|
| Tests pass | Test run output, 0 failures |
| Bug fixed | Original symptom re-tested + regression green |
| Build OK | Build exit 0 |
| Requirements met | Checklist against plan/spec |

Red-green proof for the regression: fail without fix → pass with fix (mentally or actually revert-check when feasible).

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "Obvious one-liner" | Still need cause + regression test. |
| "Should work now" | RUN verification. |
| "I'm confident / tired" | Confidence ≠ evidence. |
| "Logged something, good enough" | Boundary evidence must show *where*. |
| "Fix first, understand later" | That's how you get two bugs. |

## Red Flags — STOP

- Proposing a fix before stating root cause
- "Should", "probably", "seems" success wording
- Commit/PR of a fix without fresh test/symptom proof
- Shotgun changes across unrelated files
- Skipping the failing regression test

## Checklist

- [ ] Root cause stated with evidence
- [ ] Failing regression (tdd) observed RED then GREEN
- [ ] Fresh verification command run this turn
- [ ] Claim includes that evidence
- [ ] No unrelated drive-by edits

## Hand-off

**Transition gate** — before the fix ships, ask the user (one AskUserQuestion; never auto-advance):

```
A) Recommended: Proceed → review (then commit-and-push)
B) Review first — run **review** on the fix (`references/code.md`; upstream = the failing repro), then return to this gate
C) Adjust — back into debug for the un-locked edge, then return to this gate
D) Something else (I will type it)
```

- Structure was the cause → **solid**
- Ship the fix → **review** + **commit-and-push**
