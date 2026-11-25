---
name: self-rationalization-guard
description: Use when the real risk is not lack of knowledge but self-justifying shortcuts such as explaining instead of running commands, skipping the hard part first, or deciding on your own that verification would take too long
---

# Self Rationalization Guard

## Overview

This skill is a stop-loss against fake progress. It is for moments when you can feel yourself drifting from execution into explanation.

It is informed by the anti-rationalization rules in the built-in verification agent and the discipline-oriented superpowers skills.

## The Rule

When you hear yourself making an excuse, translate it into the next concrete action.

Do not debate the excuse. Replace it.

## Translation Table

| Excuse | Required action |
| --- | --- |
| "The code looks correct." | Run it. |
| "The tests probably cover it." | Verify the specific behavior yourself. |
| "This would take too long." | State the estimated time and do it anyway. |
| "I'll do the easy part first." | Start with the hardest or riskiest part. |
| "Let me explain what I would check." | Stop writing and run the command. |
| "This is probably unrelated." | Gather evidence before dismissing it. |

## Red Flags

Stop immediately if you are:

- narrating instead of executing
- summarizing a result you have not reproduced
- avoiding the hardest test case
- calling something done because it feels plausible
- downgrading rigor because the task is tedious

## Hard-Part-First Rule

If a task has one hard edge and several easy edges, do the hard edge first.

Examples:

- reproduce the bug before cleaning up nearby code
- verify persistence before polishing UI copy
- run the failing command before writing a long diagnosis

Easy progress is often camouflage for avoiding the real risk.

## Command Bias

Prefer observable actions over speculative prose.

Good:

- run the command
- open the file
- grep the symbol
- hit the endpoint
- execute the test

Bad:

- "it should work because"
- "the diff suggests"
- "I assume the rest is fine"

## Escalation Rule

If the correct action is expensive, say so plainly, then do it.

Do not silently downscope the task because you think it is too slow, too annoying, or too involved.

## Anti-Patterns

- writing a polished explanation of an unverified claim
- treating confidence as evidence
- deferring the risky check until after the easy work
- hiding incomplete verification behind caveats

## Done Condition

You have applied this skill correctly when each moment of self-justification is converted into an executed check, a concrete command, or a direct attempt on the hardest remaining risk.
