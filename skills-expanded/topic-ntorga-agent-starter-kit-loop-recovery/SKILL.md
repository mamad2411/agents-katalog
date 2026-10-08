---
name: loop-recovery
description: Structured recovery and escalation when an agent hits a retry loop.
usedBy: [all]
version: 0.0.3
lastUpdated: 2026-09-12
---

## Purpose

When an agent has repeated the same failing action three times, it needs a concrete recovery procedure — not just the instruction to "reassess." This skill defines the recovery steps, the escalation path when the second approach also fails, and the detection patterns that catch loops before they waste effort.

## Procedure

1. **Stop and report.** State what was attempted and what failed. Do not retry.

2. **Check for oscillation.** Before diagnosing, review the last several actions. If the agent has been alternating between two states — modifying file A, then file B, then file A again, or toggling between two error messages — the loop is structural, not incidental. Skip straight to step 5 on second detection.

3. **Check for drift.** If recent actions touched files unrelated to the stated goal, the agent is flailing. Acknowledge the drift, discard the unrelated changes, and refocus on the original objective before diagnosing.

4. **Diagnose.** Identify why the approach is not working. The answer must be a root cause, not a symptom — "the API rejects the payload because field X is required" is a diagnosis; "it returns 400" is a symptom.

5. **Pivot.** Propose a fundamentally different approach. Trivial variations (different whitespace, reordered arguments, minor rewording) do not count as a different approach. If no alternative exists, skip to step 7.

6. **Execute the pivot.** Attempt the new approach. If it succeeds, resume normal work. If it fails twice with the same result, proceed to step 7.

7. **Abandon and hand off.** Return a handoff explaining:
   - The original approach and why it failed.
   - The alternative approach and why it also failed (or why no alternative existed).
   - What is needed to unblock (different tooling, human intervention, missing information).

## Guardrails

- Never attempt a third approach. Two failed approaches show the problem needs human judgment or context the agent lacks.
- Never retry with debug commands, additional logging, or exploratory reads unless the new information would change the approach — not merely confirm the same failure.
- Never continue after detecting oscillation twice. An A→B→A→B cycle means the two approaches are undoing each other — a third attempt will repeat the pattern.
- Never treat drift (touching unrelated files) as progress. If the last action modified files outside the task scope, revert it before proceeding.
