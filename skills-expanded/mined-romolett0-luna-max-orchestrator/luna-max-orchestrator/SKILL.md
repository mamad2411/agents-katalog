---
name: luna-max-orchestrator
description: Orchestrate complex coding tasks with GPT-5.6 Sol as the controller and GPT-5.6 Luna at Max reasoning as isolated workers in separate top-level chats, never as native subagents. Use when the user asks for Luna Max workers, the Sol + Luna pattern, multi-chat delegation, model-tier-aware parallel implementation, or strict worker isolation.
---

# Luna Max Orchestrator

Run this skill from a main chat using `gpt-5.6-sol`. Plan, decompose, delegate,
monitor, verify, and synthesize. Do not implement delegated code yourself. Do
not use native subagents for Luna.

Treat “Luna Max” as shorthand for `gpt-5.6-luna` with reasoning effort
`max`.

## Check compatibility first

Confirm that the current host exposes all of the following before delegating:

- Agent-callable controls for creating and operating top-level chats. The
  official Codex App Server primitives are `thread/start`, `turn/start`,
  `thread/list`, and `thread/read`; custom hosts may expose equivalent wrappers.
- A way to select `gpt-5.6-luna` and reasoning effort `max` for that chat.
- A way to send follow-up instructions, such as `turn/start` or `turn/steer`.

Installing this skill does not expose App Server RPCs as agent tools. Require a
host integration that makes these controls callable by the orchestrator.

Confirm the main chat uses `gpt-5.6-sol` when the host exposes current-model
metadata. If it does not, tell the user to select Sol and return `BLOCKED`. If
the model cannot be inspected, state the Sol assumption in the final synthesis.

If any capability is unavailable, return `BLOCKED` with the missing capability.
Do not silently fall back to `spawn_agent`, `multi_agent_v2`, or another native
subagent mechanism.

## Enforce the operating rules

1. Use Luna Max only through new top-level chats.
2. Delegate only strictly bounded tasks with exclusive file ownership and
   verifiable success criteria.
3. Start every Luna chat with isolated context. Put every necessary fact in its
   handoff prompt.
4. Keep architecture, ambiguous decisions, final integration, and acceptance
   with Sol.
5. Parallelize independent packages whose files and dependencies do not
   overlap. Run dependent or overlapping packages sequentially.
6. Verify every result rigorously before accepting it.

## Organize chats by project and topic

Treat the Codex project as the top-level container. Name every Luna chat
exactly:

```text
[TOPIC] | [short description]
```

Examples:

- `Frontend | Fix form validation`
- `Backend | Add rate limiting`
- `Auth | Implement refresh token flow`
- `Utils | Optimize date helpers`

Assign the chat to the relevant project when the host allows it. Maintain a
logical map internally or in a state file when useful:

```text
Project
└── Topic
    ├── TASK-001 → Chat ID
    ├── TASK-002 → Chat ID
    └── ...
```

## Use the mandatory handoff protocol

Start every Luna chat with the following block. Keep the task identifier plus
all seven control sections. Replace every bracketed placeholder with concrete,
task-specific information.

```markdown
---
**TASK ID**: [unique ID, for example TASK-001]

**ROLE**:
You are Luna Max, a strictly bounded execution worker. Do not expand scope, make
architectural decisions, create files outside scope, or spawn other agents.

**EXACT OBJECTIVE AND EXPECTED FINAL STATE**:
[State precisely what must be true at the end.]

**IN-SCOPE (exhaustive list)**:
- Exact files and paths you may read or modify
- Allowed commands
- Allowed tools

**OUT-OF-SCOPE (forbidden to touch)**:
- Every other file or configuration
- Unlisted public interfaces and tests
- Unrequested documentation
- Any other unlisted work

**VERIFICATION CRITERIA AND MANDATORY EVIDENCE**:
- [Exact command that must pass, for example `npm test -- path/to/file`]
- Expected final diff or snapshot
- Output that proves completion

**STOP CONDITIONS AND ESCALATION**:
Stop immediately and return `BLOCKED` with a clear explanation if you encounter:
- Ambiguous requirements
- An undeclared dependency
- A necessary file outside scope
- Tests failing for reasons unrelated to the task
- Any decision that is not purely mechanical

Wait for instructions from Sol after returning `BLOCKED`.

**BRANCHING CONTEXT**:
- Project: [for example ProjectAlpha]
- Topic/Branch: [for example Frontend]
- Parent chat, if any: [name or ID]
- Relationship: this is an isolated worker of the [Topic] branch

At the end, always return:

TASK ID | STATUS: PASS or BLOCKED
Summary
Changed files (list)
Verification summary
Raw evidence (command output or diff)
Failure class (if BLOCKED)
---
```

## Follow the orchestration workflow

1. Analyze the user's task and split it into one or more bounded packages.
2. Define exclusive file ownership, dependencies, and verification for each
   package.
3. Create one new top-level Luna Max chat per independent package using the full
   handoff protocol.
4. Launch non-overlapping packages in parallel. Launch dependent packages only
   after their prerequisites pass.
5. Monitor each chat with the host's list, read, and message controls.
6. Inspect the returned status, diff, and command output. Re-run relevant checks
   from Sol's environment when possible.
7. Accept and integrate a `PASS` only when the evidence satisfies every stated
   criterion.
8. Resolve a `BLOCKED` result at the architecture level, then send a revised
   bounded handoff or create a replacement chat.
9. Finish with one synthesis covering accepted changes, verification, remaining
   risks, and any follow-up work.

Optionally ask a worker to create a persistent goal when that facility is
available, but do not make it a prerequisite.
