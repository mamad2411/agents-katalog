---
name: dev-ralph
description: Persistence loop — keep working on a task until it's resolved or until a circuit breaker stops you. Different from /loop (which is time-based) — ralph is iteration-based with state.
---

# Dev Ralph

Derived from oh-my-claudecode (MIT, Yeachan Heo). Adapted for the EvoNexus Engineering Layer.

Persistence loop. Keep iterating on a task until it's resolved, with a circuit breaker for safety. **Different from `/loop`** (which runs a prompt every N minutes) — ralph runs the same agent repeatedly until a goal is met.

## Use When
- Task has a clear completion signal but unclear iteration count
- "Fix until tests pass" type work
- Auto-correcting loops where each iteration uses the previous result

## Do Not Use When
- Time-based polling → use `/loop` (built-in)
- Single-shot work
- No clear completion signal (you'll loop forever)

## Iron Rules
1. **Completion signal must be defined upfront** — "tests pass" or "build green" or "verifier APPROVES"
2. **Circuit breaker:** stop after 5 iterations OR after 3 identical failures
3. **State persisted between iterations** — what's been tried, what failed, why
4. **Never silently spin** — emit progress every iteration

## Workflow

```
Iteration 1:
  - Run agent (e.g., @bolt-executor) with task
  - Check completion signal
  - If met: STOP, success
  - If not: record what was tried, what failed
  - Increment iteration counter

Iteration 2:
  - Run agent with task + accumulated state
  - Check completion signal
  - ...

Iteration 5 (max):
  - Stop and report: "Reached max iterations without completion"
  - Hand off to @apex-architect with full state dump

OR

3-identical-failure breaker:
  - If iteration N produces the same error fingerprint as N-1 and N-2
  - Stop immediately
  - The issue is no longer "fix the bug" — it's "question the approach"
```

## Output

Per iteration, emit:
```
[ralph iteration {N}/{max}]
  Goal: {completion signal}
  Tried: {what this iteration did}
  Result: {success | failure: {reason}}
  State: {what's been tried so far}
```

Final report saved to `workspace/development/debug/[C]ralph-{topic}-{date}.md`.

## Pairs With
- `@bolt-executor` (most common driver)
- `@hawk-debugger` (for bug-fix loops)
- `@oath-verifier` (provides the completion signal)
- `@apex-architect` (escalation when circuit breaker trips)

## Cancellation
Interrupted by `dev-cancel` — preserves state for resume.
