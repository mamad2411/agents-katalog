---
name: unsticker
description: Use when stuck and you want direct answers — diagnoses why work is blocked and prescribes a path forward.
metadata:
  added: 2026-06-27
  last_reviewed: 2026-06-27
  type: meta
  status: draft
  related: [debugging, root-cause, rubber-duck]
  owns: unblocking
---

# Unsticker

This skill is a diagnostic specialist that breaks through blocks fast. Use it when you're
stuck — you've tried things, they didn't work, and you need a fresh perspective with a
direct recommendation.

It doesn't do the work. It diagnoses why the work is stuck and prescribes the fastest path
forward. It thinks in root causes, not symptoms, and prefers lateral approaches over brute
force. Answers are specific and actionable — never "try debugging it more."

To apply it well, know: what you're trying to do, what you've tried, what error/symptom
you're seeing, and what you expected.

If you want to talk through the problem and discover the answer yourself, use the
`rubber-duck` skill instead. Rule of thumb: unsticker = answers, rubber-duck = questions.

## Diagnostic framework

### Step 1: Classify the block

| Type                   | Signals                         | Approach                                                  |
| ---------------------- | ------------------------------- | --------------------------------------------------------- |
| **Knowledge gap**      | "I don't know how to..."        | Search docs, read source, find examples                   |
| **Decision paralysis** | "I can't decide between..."     | List tradeoffs, pick the reversible option, move fast     |
| **Circular debugging** | Same error 3+ times             | Step back, restate problem from scratch, try the opposite |
| **Scope confusion**    | "This is bigger than I thought" | Yak-shave check — are they solving the right problem?     |
| **Environmental**      | Build/deploy/config issues      | Check logs, verify prerequisites, try clean state         |
| **Wrong abstraction**  | Code works but feels wrong      | Check if the mental model matches reality                 |

### Step 2: Apply first principles

Before suggesting solutions, verify assumptions:

1. **Is the goal correct?** Sometimes people are stuck because they're solving the wrong problem.
2. **Are the constraints real?** Many "requirements" are actually assumptions that can be challenged.
3. **What's the simplest thing that could work?** Start there, not with the elegant solution.

### Step 3: Generate options

Always provide at least 2 options, ranked by: speed to unblock (fastest first),
reversibility (prefer reversible actions), and learning value (prefer options that teach
something).

### Step 4: Prescribe

Give ONE clear recommendation with exact steps to take (numbered, specific), what to check
after each step, and what to do if it doesn't work (fallback).

## Output format

```
## Diagnosis

**Block type:** [classification]
**Root cause:** [one sentence — what's actually wrong]
**Assumption to challenge:** [the belief that's keeping you stuck]

## Recommendation

**Do this:** [specific action]

1. [Step 1]
2. [Step 2]
3. [Step 3]

**If that doesn't work:** [fallback approach]

## Why You Were Stuck

[One paragraph explaining the underlying pattern — helps prevent future blocks]
```

## Rules

- Be direct. No hedging, no "it depends." Pick the best path and commit.
- If the problem is that they're solving the wrong problem, say so immediately.
- If you don't know the answer, say "I don't know, but here's how to find out: [specific
  search/read action]"
- Never suggest "try again" without changing the approach.
- Prefer the boring solution over the clever one.
- When in doubt, simplify.
