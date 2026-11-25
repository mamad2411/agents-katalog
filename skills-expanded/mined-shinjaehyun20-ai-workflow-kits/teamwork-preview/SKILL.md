---
name: teamwork_preview
description: >
  Build a worker-ready launch packet before multi-agent execution. Use when a
  large task needs goal lock, grill-me review, branch planning, objective
  acceptance criteria, explicit approval, and evidence-first fan-in.
---

# teamwork_preview

Teamwork Preview is a Codex-native launch-packet skill.

It is not the execution engine. It prepares work for execution.

```text
goal lock -> grill-me pass -> teamwork_preview -> keepworking
```

## Use When

- the task is large enough to split into independent branches
- the user mentions team, parallel agents, subagents, or delegated workers
- source evidence, scope, and acceptance criteria must be locked before execution
- a worker prompt must be copied as text, not implied by chat context

Skip this skill for simple fixes. Use the normal evidence-first execution loop directly.

## Workflow

### 1. Goal Lock

Write one sentence that states:

- what must be completed
- what mode applies: plan, execute, or review
- what evidence will prove completion

### 2. Grill-Me Pass

Before writing the launch packet, challenge the request:

- What source is missing?
- What output can be self-certified too easily?
- Which acceptance criteria are subjective?
- Which paths, constraints, or runtime capabilities are unverified?
- What should stop the run before damage or wasted work?

Ask only for information that cannot be discovered locally.

### 3. Launch Packet

Create a draft with this shape:

```markdown
# Teamwork Launch Packet

> Status: Draft - awaiting approval
> Main owner: current session
> Execution mode: local loop | subagent fan-out | external worker

## Objective
[result to deliver]

## Context
[background and known constraints]

## Paths
[repository-relative paths or confirmed external references]

## Scope
### In Scope
- [...]

### Out of Scope
- [...]

## Source Evidence To Inspect
- [...]

## Branch Plan
- Branch A: [...]
- Branch B: [...]
- Main session: fan-in, verification, final acceptance

## Acceptance Criteria
- [ ] [objective, checkable condition]

## Verification
- [ ] [test, lint, render, schema, file existence, or review check]

## Stop Conditions
- [...]

## Return Format
- status
- changed paths
- evidence paths
- unresolved risks
```

### 4. Approval Gate

Do not launch delegated work until the user approves, unless the user explicitly asked for immediate execution and the task is low risk.

Accepted approval phrases include:

- go
- launch
- run it
- proceed
- use this

### 5. Execution

If real subagent capability is available and the branches are independent, delegate with the full launch packet copied into each worker prompt.

If subagent capability is not available, execute the packet through the main session's local bounded loop.

If an external worker is used, require file paths, logs, manifests, or verification output. Do not accept a chat-only success claim.

### 6. Fan-In

A branch is not complete until it returns:

- worker or run id when available
- status
- result summary
- evidence path
- unresolved risks

The main session remains the acceptance owner.

## Anti-Patterns

| Anti-pattern | Why |
| --- | --- |
| Passing only a file path as the prompt | The draft can change after launch. Copy the prompt text. |
| Launching without a goal lock | Workers optimize for different targets. |
| Using subjective acceptance criteria | Workers can self-certify weak output. |
| Delegating shared-file edits in parallel | It creates race conditions and review noise. |
| Treating worker completion as final acceptance | The main session must verify and close. |

## Output Contract

Before launch:

```text
Combination:
Goal:
Grill-Me Findings:
Launch Packet Path:
Approval Needed:
```

After launch:

```text
Run:
Branches:
Evidence Paths:
Fan-In Decision:
Verification Gate:
Unresolved Risks:
Close Decision:
```
