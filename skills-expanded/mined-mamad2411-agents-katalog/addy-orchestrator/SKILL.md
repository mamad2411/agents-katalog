---
name: addy-orchestrator
description: "Orchestrates end-to-end software development using the addyosmani/agent-skills framework. Guides the user through define → plan → build → verify → review → ship phases, spawns subagents for each step, tracks state persistently, and never loses focus on workflow completion. Use when the user says \"let's build X\", \"help me implement X\", \"walk me through X\", or wants structured multi-phase dev guidance. Also triggers when a task is clearly non-trivial and would benefit from phased execution."
---

# Addy Orchestrator

**Skills path:** `~/.claude/plugins/cache/addy-agent-skills/agent-skills/1.0.0/skills/`

## Core Principle

This skill never loses focus. At every step, show the user exactly where they are, what just finished, and what's next. Always read the state file first. Always write the state file after. Never move to the next phase without explicit user confirmation.

---

## Phase 0: Intake

Before doing anything, check for an existing session state file:

```
<project-dir>/.addy-session.md
```

If it exists, read it and resume from the last completed phase. Tell the user:
> "Resuming: you're on phase N/M — [phase name]. Ready to continue?"

If no state file, interview the user with exactly these questions:
1. What are you building or fixing? (one sentence)
2. Does a spec already exist, or are we starting from scratch?
3. Greenfield or existing codebase?
4. What does "done" look like?

Then determine the phase sequence (see table below) and confirm it with the user before proceeding.

---

## Phase Sequences

| Scenario | Sequence |
|----------|----------|
| Vague idea | idea-refine → spec-driven-development → planning-and-task-breakdown → incremental-implementation → test-driven-development → code-review-and-quality → git-workflow-and-versioning |
| Clear spec, no plan | planning-and-task-breakdown → incremental-implementation → test-driven-development → code-review-and-quality → git-workflow-and-versioning |
| Bug fix | debugging-and-error-recovery → test-driven-development → code-review-and-quality |
| UI feature | spec-driven-development → frontend-ui-engineering → browser-testing-with-devtools → code-review-and-quality |
| API design | spec-driven-development → api-and-interface-design → test-driven-development → code-review-and-quality |
| Security / perf | security-and-hardening / performance-optimization (standalone) |
| Shipping | shipping-and-launch |

---

## State File Format

Write `.addy-session.md` in the project directory after every phase:

```markdown
# Addy Session

task: <one-line description>
started: <date>
sequence: [phase1, phase2, phase3, ...]
current_phase: <index starting at 0>
status: in_progress | complete

## Completed Phases
### phase-name
- Summary: ...
- Artifacts: ...
- Decisions: ...

## Accumulated Context
<running context block — grows with each phase>
```

---

## Phase Execution Loop

Repeat this loop for every phase until all are done:

### 1. Announce the phase

Always show a status header:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Phase N/M: [PHASE-NAME]
Done: ✓ phase1  ✓ phase2
Next: phase4, phase5
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 2. Spawn the subagent

```
You are executing the [SKILL_NAME] phase of a structured development workflow.

Read and follow the skill at:
~/.claude/plugins/cache/addy-agent-skills/agent-skills/1.0.0/skills/[SKILL_NAME]/SKILL.md

== Accumulated context ==
[paste context block from state file]

== Your task ==
[specific instruction for this phase]

When done, output:
PHASE SUMMARY: <2-3 sentences>
ARTIFACTS: <list of files created/modified>
DECISIONS: <any choices made that affect later phases>
BLOCKERS: <anything requiring human input before next phase>
```

### 3. Process the result

- Extract PHASE SUMMARY / ARTIFACTS / DECISIONS / BLOCKERS from subagent output
- Update the state file
- If BLOCKERS is non-empty: **stop and resolve with the user before continuing**
- Show the user the phase result, then ask: *"Ready to move to [next phase], or do you want to adjust anything first?"*
- Do not auto-advance — always wait for explicit go-ahead

### 4. Never abandon the loop

If the user goes on a tangent, acknowledge it, then redirect:
> "Got it. Let me note that for phase N. To keep the workflow on track — want to continue with [current phase] or address this first?"

---

## Completion

When all phases are done:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ All phases complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Present:
- What was built/fixed (1 paragraph)
- Files changed or created
- Decisions made along the way
- Suggested next steps (deploy, monitor, doc)

Mark `.addy-session.md` status as `complete`.

