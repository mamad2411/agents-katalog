---
name: senior-code-review
description: Use when asked to review a diff, branch or pull request, or before merging a change of medium risk or higher, including agent-generated code. Not for explaining code or answering questions about how it works.
---

# Code Review

**Core rule:** judge the change by evidence in the diff and its checks, not by the author's confidence — yours included.

## Inputs

Establish before reading the code:

- the goal or acceptance criteria;
- the change set: `git diff <base>...HEAD` plus uncommitted work (`senior risk --base <base>` lists the files and the risk signals);
- verification results that actually ran;
- risk level and the contracts the change touches.

If the goal is unknown, infer it cautiously from the task or commit messages and say that you did.

## Independence

For medium risk and above, when the host can start a subagent, give a fresh reviewer only the goal, the diff and the verification results — not the session history. A reviewer who watched the change being written inherits its blind spots. Without a subagent, review the diff as if someone else wrote it, after re-reading the goal.

One fresh review per change is enough. After fixing its findings, prove each fix yourself (a test or command that failed before and passes now) instead of starting another reviewer; a second review is for a fix that changed the design, not for one that closed a finding.

## Review axes

**Correctness** — Does the code do what was asked? Are error paths, boundaries, nullability, ordering and state transitions right?

**Regression risk** — Which existing behavior changed implicitly? Are public and internal contracts preserved? Do tests cover the behavior rather than the implementation?

**Security and data integrity** — when relevant: authentication/authorization, input validation and injection, secrets in code or logs, unsafe file/network operations, data loss, migrations, privilege boundaries. For each input the caller controls, ask what it can reach: fields copied into stored records (can a user set their own role, owner or price?), ids and paths used for lookups, amounts and limits.

**Complexity** — new dependencies, single-use abstractions, broad rewrites for local changes, mechanisms the project already has.

**Operability** — for runtime changes: failure behavior, logs, rollback, observability.

## Try to break it

Reading a diff tends to confirm it. For medium risk and above, switch to attacking it once you understand it.

For each behavior the change adds or alters, name the input, state or timing most likely to make it wrong: empty, boundary and malformed values, a second caller of the same code, a retry or a rerun, two requests at once, existing data written by the old version, another OS, timezone or locale, a guard the diff removed. Then check it — run it, write a quick test, or trace it through the code — instead of judging it plausible.

Keep a one-line record of each attack and its result. An attack that held is evidence too. Effort follows risk: a few attacks for a medium change, more for auth, money, data or concurrency. Skip this for low-risk diffs.

## Findings

Order by impact. Each actionable finding has:

- severity (blocker, important, minor);
- location (`file:line`) and the evidence;
- why it matters — a concrete input or scenario that breaks;
- the smallest credible fix, or a question.

Do not manufacture findings to look thorough. A clean review is a valid outcome; when you attacked the change, list the attacks that held, so the reader can see what "clean" covers.

## Red flags

| If you notice yourself thinking… | Do this instead |
|---|---|
| "The tests pass, so the logic is right" | Check what the tests actually assert |
| "I can't think of how this breaks" | Try the inputs and timings above before concluding it holds |
| "This looks like a style issue" about a behavior change | Classify by consequence, not by appearance |
| "I wrote this, I know it's fine" | Review it as a stranger's diff, or hand it to a fresh reviewer |
| "I'll list every nit to be thorough" | Keep minor findings brief and separate from blockers |

## Exit

Finish with exactly one verdict:

- **approve** — evidence supports merging;
- **approve with notes** — no blocker; non-blocking follow-ups listed;
- **changes required** — at least one concrete blocker;
- **not enough evidence** — required context or verification is unavailable; say what is missing.

When receiving review feedback on your own work, verify each point against the code before changing anything; push back with evidence when a suggestion is wrong.
