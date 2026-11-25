---
name: keepworking
description: >
  Use this skill when the user wants persistent progress instead of a shallow
  answer: "keep working", "continue until verified", "debug until the cause is
  clear", "repair and re-run", "parallelize these checks", "do not stop at
  analysis", or any task that needs goal locking, tiered routing, evidence,
  repair, and re-verification before closure.
---

# keepworking

Use this skill to keep non-trivial work moving until there is evidence.

## Core Goal

Move from request to verified closure:

```text
goal -> plan -> execute -> verify -> repair -> re-verify -> close
```

## Routing

Before doing work, classify the next useful step.

| Tier | Use for | Default behavior |
| --- | --- | --- |
| `simple` | search, classification, summaries, status checks | read-only, low-risk discovery |
| `medium` | bounded implementation, repair, deterministic checks | scoped edits and verification |
| `complex` | architecture, deep debugging, multi-stage workflows | staged checkpoints and explicit risks |

Escalate when the current tier can no longer close the task safely:

- `simple -> medium` when edits or deterministic checks are needed
- `medium -> complex` when the cause is still unclear after one verification cycle
- `complex -> simple` when cheap discovery can reduce ambiguity first

## Workflow

1. Restate the current goal in one line.
2. Separate discoverable facts from preferences.
3. Pick the smallest useful next slice.
4. Define the action unit: action, object, scope, owner, completion criteria, and verifier.
5. Check whether an existing skill, playbook, or stop rule applies.
6. Execute or inspect that slice.
7. Verify with evidence.
8. If verification fails, record the failure cause, change the next attempt, repair, and re-run the same or stronger check.
9. Close only when the evidence satisfies the action unit's completion criteria and unresolved risks are explicit.

## Evidence

Prefer evidence that another person or tool can inspect:

- file paths
- command output
- test or build output
- logs
- browser or UI checks
- screenshots
- structured manifests
- audit events

Do not treat a chat response as completion.

## Action Units

Do not close a large goal just because one step produced output. Close the current action unit first.

An action unit names:

- action: inspect, edit, create, run, compare, verify, repair, publish, etc.
- object: exact file, artifact, issue, dataset, thread, deployment, or decision
- scope: what is included and what is outside this slice
- owner: main chat, local tool, sub-agent, external app, or user
- completion criteria: observable conditions required for done
- verifier: command, test, build, log, render, diff, source check, review pass, or user confirmation

If the verifier is unavailable, say what could not be verified and use `partial`, `blocked`, or `failed` instead of `done`.

## Reuse And Stop Rules

Before non-trivial execution, check whether a relevant skill, playbook, or stop rule already applies.

Repeated wins can become playbooks or skill candidates when their preconditions, verifier, and escalation trigger are clear.

Repeated failures should become stop rules:

```text
Failure Cause:
Method To Avoid:
Changed Next Attempt:
Verifier To Re-run:
```

Do not retry the same failed method against the same input unless the failure cause has changed.

## Parallel Work

Use parallel branches only when the branches are independent.

```text
route -> fan-out -> collect evidence -> fan-in synthesis -> verify -> close
```

The main chat remains the owner of final synthesis and closure.

## Output

Use this report shape:

```text
Current Goal:
Tier:
Action Unit:
Completion Criteria:
Work Done:
Evidence:
Verification:
Learned Pattern:
Stop Rule:
Unresolved Risks:
Next Action:
Close Decision:
```

If work continues, make the next deep-dive target visible.
