---
name: agent_team_ops
description: >
  Stand up and operate a live multi-agent team for large, parallelizable work.
  Use after a launch packet exists, when several sessions must run in parallel
  with separate contexts, a shared tool stack, remote drive, and conflict-safe
  fan-in. Each member runs its own evidence-first loop; the main session owns
  acceptance.
---

# agent_team_ops

Agent Team Ops is the live-team operating skill. It is not the launch-packet
step and not a single execution loop.

```text
teamwork_preview -> agent_team_ops -> keepworking (per member)
```

## Use When

- a locked launch packet already splits into independent branches
- parallel sessions with separate contexts beat one long context
- the operator wants to drive and approve work remotely
- a shared, token-efficient tool stack should back every member
- merges are likely to collide and need a conflict contract

Skip this skill when one loop can finish the task. Standing up a team has
real overhead.

## Operating Loop

```text
environment -> charter -> stand up -> assign -> remote drive -> parallel run -> conflict-safe fan-in -> evidence close
```

### 1. Environment

Confirm the team substrate is ready before assigning work:

- a session multiplexer (e.g. TMUX) or equivalent parallel-session mechanism
- the shared tool stack (strategy/verify, structure/execute, quality/method,
  token optimization) — see `docs/ko/tooling-setup.md`
- isolated branches or worktrees so members never edit the same file in parallel

Record the tool-stack state. An unverified tool is not part of the run.

### 2. Charter

Write a team charter that every member can read without hidden chat context:

- one-sentence team objective and current mode (plan / execute / review)
- per-member role, in-scope paths, and out-of-scope paths
- the shared task list with dependency order
- the conflict rule: one owner per file or per worktree
- the evidence each member must return

### 3. Stand Up

Start one session per member. Give each member only its slice of the charter
plus the shared task list. Members do not improvise scope.

### 4. Assign

Map launch-packet branches to members. Each member receives the full prompt
text, not just a file path. Dependencies are explicit: a dependent member does
not start until its upstream evidence lands.

### 5. Remote Drive

If remote control is enabled, the operator can issue instructions and approve
tool calls from a phone. Keep a hard approval gate for any destructive or
outward-facing action regardless of channel. Use completion notifications to
detect when a member is blocked or done — not to skip verification.

### 6. Parallel Run

Each member runs its own evidence-first loop (goal -> plan -> execute ->
verify -> repair -> re-verify -> close). The main session stays free to
coordinate, unblock, and re-route, in a coordinator ("bot") posture.

### 7. Conflict-Safe Fan-In

A member's branch is not complete until it returns:

- member id and branch / worktree
- status and result summary
- evidence path (changed files, test/build output, logs)
- unresolved risks

Before merge, run a conflict check: no two members own the same file; shared
contracts (schemas, interfaces) changed by only one member; dependent work
re-verified against upstream results.

### 8. Evidence Close

The main session verifies the integrated result and closes. Member completion
is never final acceptance.

## Triple-Crown Division Of Labor

Map tools to roles so the stack reads as one pipeline, not five gadgets:

| Role | Question it answers | Stack slot |
| --- | --- | --- |
| Strategy / verify | what and why | strategy + verification tool |
| Structure / execute | in what order | project / spec execution tool |
| Quality / method | how to do it well | skill / methodology tool |
| Token optimization | how to stay in budget | output-compression proxy |

Members inherit the same pipeline so output is comparable at fan-in.

## Anti-Patterns

| Anti-pattern | Why |
| --- | --- |
| Standing up a team for a one-loop task | Overhead with no parallel benefit. |
| Two members owning the same file | Race conditions and merge noise. |
| Remote approval that skips the gate | A phone tap is still a destructive action. |
| Treating a completion ping as acceptance | Completion needs verified evidence. |
| Members improvising scope | Charter drift breaks comparable fan-in. |
| Unverified tools in the stack | "Installed" claims must be checked. |

## Output Contract

At stand up:

```text
Objective:
Mode:
Members + Roles:
Tool-Stack State:
Shared Task List:
Conflict Rule:
Approval Gate:
```

At close:

```text
Members Returned:
Evidence Paths:
Conflict Check:
Verification Gate:
Unresolved Risks:
Close Decision:
```
