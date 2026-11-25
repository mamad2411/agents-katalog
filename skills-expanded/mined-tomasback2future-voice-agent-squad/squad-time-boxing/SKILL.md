---
name: squad-time-boxing
description: Exploratory work has a 2-hour cap. At 2h, stop and write up what you know — hypotheses tried, ruled-out causes, evidence collected, what is still unknown. Then escalate, parallelize, or block. Long unsuccessful sessions are a signal, not a setback.
allowed-tools:
  - Bash
disable-model-invocation: false
---

# Time-boxing exploratory work

Some items have unclear scope: bug repros, perf investigations, "figure out why X is slow." These can become black holes. The time-box is the circuit breaker.

## When to use this skill

Invoke this skill any time you are working on an investigation, a debug, or a "figure out" item — anything where the path to "done" is not yet visible. Set a mental timer at the start of the work; check in against it at the 1h and 2h marks.

## The rule

**Default exploration cap: 2 hours of focused work** before you escalate or change approach.

If you are 2h in and still do not understand the problem:

1. **Stop.** Do not push through to "almost there." If you were actually almost there, you would be done.
2. **Write up what you know** as `## Investigation log` in the item:
   - Hypothesis space tried (one bullet per hypothesis)
   - Ruled-out causes (and what evidence ruled them out)
   - Evidence collected (logs, perf numbers, repro conditions)
   - What is still unknown
3. **Choose one of three exits:**
   - (a) Escalate to the user with the writeup and a specific question.
   - (b) Spawn a parallel agent on the most promising remaining hypothesis.
   - (c) Set `status: blocked` if you have hit an external dependency.

Do **not** quietly extend the cap to 4h, then 6h, telling yourself "I am close." That is the failure mode this skill exists to prevent.

## Why this matters

Long unsuccessful sessions correlate strongly with going down the wrong path. By hour 4, you have invested enough sunk cost that you are no longer evaluating alternatives — you are defending the path you took. The 2-hour cap forces a re-evaluation before sunk cost dominates.

The writeup itself is also valuable independent of the exit choice. Even if you eventually return to the same hypothesis, the writeup gives the next session (or the parallel agent) a structured starting point instead of a blank slate. Investigations that produced a good writeup are net-positive even when they did not produce a fix.

## Items where investigation IS the item

For items whose scope is "investigate why X" or "figure out the root cause of Y," the time-box is the item's `estimate` field. If the estimate was 2h and you blow past it, the item was sized wrong — re-estimate honestly and tell the user. Do not silently extend.

## How to apply

1. At the start of an investigation, note the time. Set an explicit 2h cap.
2. At the 1h mark, do a quick check: am I narrowing the hypothesis space, or am I bouncing between unrelated guesses? If bouncing, re-plan.
3. At the 2h mark, regardless of how you feel about progress, stop and write up.
4. Choose the exit (escalate / parallelize / block) and execute.
5. If you continue after the writeup, set a fresh cap (typically 1h more) and check again.

## Anti-patterns to avoid

- Telling yourself at 2h: "I am close, just 30 more minutes." That is sunk-cost talking.
- Not writing the investigation log because "I know what I tried." You do, until tomorrow when you do not.
- Treating the cap as a hard deadline that fails the session. The cap is a circuit breaker, not a failure threshold; a 2h investigation that ends in a clean writeup is a successful 2h.
- Spawning a parallel agent as the default exit without first asking whether escalation would be cheaper.
