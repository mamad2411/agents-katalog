---
name: imlazy-router
description: Classify the task into Quick/Standard/Heavy/Vault/Learn tier and route to the right workflow. Adaptively consults heuristics.log to refine borderline classifications.
---

# imlazy-router

## Output contract

Output `tier=<quick|std|heavy|vault|learn>` and the name of the next skill to invoke.

If genuinely ambiguous between two adjacent tiers, ask ONE clarifying multiple-choice question and stop. Never multi-turn.

If the message has no actionable verb (e.g., the user said "i am lazy" with no ask), output `tier=none` and respond conversationally without loading any skills.

## Classification heuristics

| Signal | Tier |
|--------|------|
| Single-line content fix (typo, spelling, value, version bump) | quick |
| Single-file edit ≤30 lines, no new dependency added | quick |
| Factual question, code explanation, lookup | quick |
| Run a command (test, build, format, lint) without modifying code | quick |
| Single rename or import cleanup, no behavior change | quick |
| 1-3 file feature or bugfix with clear requirements | standard |
| Refactor of a single function or component | standard |
| Schema or config migration involving 2-3 files | standard |
| Single-concern enhancement (caching, validation, error handling, tracing) | standard |
| "create vault", "save knowledge", "vault init", "vault search" | vault |
| New subsystem (auth, billing, replay, notifications, collaboration) | heavy |
| User explicitly says "design", "plan", "architecture", or "let's build" | heavy |
| Multi-component feature with unclear integration points | heavy |
| Cross-cutting migration (e.g., REST to GraphQL across the whole API) | heavy |
| Router misclassification feedback from Skill(imlazy-learn) | learn |

## Disambiguation

When the signal is between Quick and Standard: ask "Will this need a new test, or is it a content/config edit only?"

When the signal is between Standard and Heavy: ask "Are the requirements clear, or do we need to design this together first?"

Wait for ONE answer. Default to the lighter tier if the answer is still ambiguous.

## Adaptive lookup

Before classifying, read up to the last 20 lines of `~/.claude/imlazy/heuristics.log` if it exists.

If a recent misclassification (≤30 days) matches this task's signal pattern, shift the borderline classification toward the tier that turned out correct in similar past cases.

If the file does not exist or is empty, classify purely from the heuristics table above.

## Routing

| Tier | Next action |
|------|-------------|
| quick | None — proceed inline; use the Quick-tier completion gate from `imlazy-bootstrap`, no further skills loaded |
| std | Invoke `Skill(imlazy-planning)` in light mode → then `Skill(imlazy-tdd)` → then `Skill(imlazy-code-review)` |
| heavy | Invoke `Skill(imlazy-brainstorm)` first → on spec approval, invoke `Skill(imlazy-planning)` in full mode |
| vault | Invoke `Skill(imlazy-vault)` with task description |
| learn | Invoke `Skill(imlazy-learn)` to log misclassification |

## Escalation rule

If verification fails after Quick-tier work, escalate to Standard: invoke `Skill(imlazy-tdd)` and `Skill(imlazy-planning)` (light mode) and log the misclassification via `Skill(imlazy-learn)` with predicted=quick, actual=standard.
