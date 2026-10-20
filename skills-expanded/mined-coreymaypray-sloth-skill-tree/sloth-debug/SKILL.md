---
name: sloth-debug
description: "Use when a Maycrest build hits any bug, test failure, or unexpected behavior on the Expo/Supabase/Vercel stack — before proposing any fix."
---

# Sloth Debug — Root-Cause-First 🦥

## Overview

Random fixes waste time and breed new bugs. Quick patches hide the real problem and resurface
in front of the client. At Maycrest we find the cause before we touch the code.

**Core principle:** Find the root cause before attempting any fix. A symptom fix is a failure.

**Violating the letter of this process is violating the spirit of debugging.**

## The Iron Law

```
NO FIX WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose a fix. No exceptions on a client build.

## When to Use

Any technical issue: test failures, production bugs, unexpected behavior, performance problems,
build/deploy failures, integration breakage.

**Especially when:** under deadline pressure, "just one quick fix" looks obvious, you've already
tried multiple fixes, the last fix didn't hold, or you don't fully understand the issue.

**Don't skip because:** the bug "looks simple" (simple bugs have root causes too), you're rushing
(rushing guarantees rework), or Corey wants it fixed NOW (systematic is faster than thrashing).

## The Four Phases

Complete each phase before the next.

### Phase 1: Root Cause Investigation

**Before ANY fix:**

1. **Read errors carefully** — full stack traces, line numbers, file paths, codes. They often
   contain the exact answer. Don't skim past warnings.
2. **Reproduce consistently** — exact steps, every time? Not reproducible → gather data, don't guess.
3. **Check recent changes** — `git diff`, recent commits, new deps, config/env differences.
4. **Gather evidence across boundaries** — for multi-component systems (Expo client → Supabase
   RLS → Postgres, or Next.js route → API → Vercel edge), log what data *enters* and *exits* each
   boundary, verify env/config propagation, check state at each layer. Run once to see WHERE it
   breaks, then investigate that component.
5. **Trace data flow backward** — when the error is deep in the stack, work backward from the
   bad value: where did it originate? What called this with the bad value? Keep walking up the
   call chain until you reach the source. Fix at the source, not where it surfaced.

### Phase 2: Pattern Analysis

1. **Find working examples** — similar code in the same codebase that works.
2. **Compare against references** — reading a pattern? Read the reference implementation
   completely, every line. No skimming.
3. **Identify differences** — list every difference between working and broken, however small.
   Don't assume "that can't matter."
4. **Understand dependencies** — what config, env, components, and assumptions does this need?

### Phase 3: Hypothesis and Testing

1. **Form one hypothesis** — "I think X is the root cause because Y." Specific, written down.
2. **Test minimally** — smallest possible change, one variable at a time.
3. **Verify before continuing** — worked → Phase 4. Didn't → form a NEW hypothesis, don't stack fixes.
4. **When you don't know** — say "I don't understand X." Don't pretend. Research or ask Corey.

### Phase 4: Implementation

1. **Create a failing test first** — simplest reproduction, automated if possible. Required
   before fixing. Use [sloth-tdd](../sloth-tdd/SKILL.md) to write it properly.
2. **Implement a single fix** — address the root cause, ONE change, no "while I'm here" extras.
3. **Verify the fix** — test passes, no other tests broken, issue actually resolved.
4. **If the fix doesn't work** — STOP. Count attempts. < 3 → return to Phase 1 with new info.
   **≥ 3 → question the architecture (below).** Never attempt fix #4 without that discussion.
5. **If 3+ fixes failed: question the architecture.** Each fix exposing new coupling in a
   different place, or requiring "massive refactoring," means the pattern is wrong — not the
   hypothesis. Ask: is this pattern sound, or are we continuing through inertia? Discuss with
   Corey before any more fixes.

## Red Flags — STOP and Return to Phase 1

- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- Proposing solutions before tracing data flow
- **"One more fix attempt" (after 2+ failures)** → question the architecture instead

## Signals from Corey That You're Doing It Wrong

- "Is that not happening?" → you assumed without verifying
- "Will it show us…?" → you should have added evidence gathering
- "Stop guessing" → you're proposing fixes without understanding
- "Ultrathink this" → question fundamentals, not symptoms
- "We're stuck?" (frustrated) → your approach isn't working

**When you see these:** STOP. Return to Phase 1.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple, skip the process" | Simple issues have root causes too. The process is fast for them. |
| "Client emergency, no time" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this first, then investigate" | The first fix sets the pattern. Do it right from the start. |
| "I'll write the test after the fix works" | Untested fixes don't stick. The test first proves it. |
| "Multiple fixes at once saves time" | Can't isolate what worked. Breeds new bugs. |
| "Reference is long, I'll adapt the pattern" | Partial understanding guarantees bugs. Read it completely. |
| "One more fix attempt" (after 2+) | 3+ failures = architecture problem. Question the pattern. |

## Example: AOS Sober Living booking app

**Symptom:** bookings silently vanish for some clients; the Expo UI shows success.

**Phase 1** — reproduce: only fails for clients created before a recent migration. `git diff`
shows a new `org_id` column added to `bookings`. Boundary logging: the Expo insert succeeds, but
the Supabase response returns zero rows. **Trace backward:** the RLS policy filters on
`org_id = auth.jwt() ->> 'org_id'`; legacy clients have a null `org_id`, so the policy silently
rejects the row. Root cause = null `org_id` on legacy rows, not the insert code.

**Phase 4** — failing test asserts a legacy-client booking persists. Single fix: backfill
`org_id` for legacy rows (the source), not loosening RLS (the symptom). Test passes, RLS intact.

## Integration with the Maycrest roster

- Write the Phase 4 failing test with [sloth-tdd](../sloth-tdd/SKILL.md).
- Confirm the fix with [sloth-verify](../sloth-verify/SKILL.md) before claiming it's resolved.
- Deep Supabase/RLS or Vercel-edge breakage? Pull in the relevant `maycrest-automate` specialist.
- Hand the certified fix to `maycrest-ops:reality-checker` for the production-readiness verdict.

---
*Adapted from the MIT-licensed [obra/superpowers](https://github.com/obra/superpowers) project (© 2025 Jesse Vincent). See [NOTICE](../../NOTICE).*
