---
name: dev-cancel
description: Cleanly stop an active engineering layer flow (dev-autopilot, dev-deep-interview, dev-plan) and report what was completed. Use when the user says "cancel", "stop", "abort", "cancelomc", or wants to exit a multi-phase dev workflow.
---

# Dev Cancel

Derived from oh-my-claudecode (MIT, Yeachan Heo). Adapted for the EvoNexus Engineering Layer — simplified, runtime-free version.

## Use When
- User says "cancel", "stop", "abort", "cancelomc", "stopomc"
- Multi-phase workflow (dev-autopilot, dev-deep-interview, dev-plan, dev-ralplan) is active and the user wants to exit
- Context indicates a long-running dev orchestration that needs a clean stop

## Do Not Use When
- No engineering layer flow is active — just respond conversationally
- The user is canceling a single tool call (Claude Code already handles that)
- The user wants to pause/resume → use the workflow's own pause mechanism instead

## Goal
Stop the active flow cleanly and give the user a structured summary of:
1. **What was completed** before cancel
2. **What was in progress** at cancel time
3. **What was not started**
4. **Where the artifacts live** (spec, plan, code) so the user can resume manually
5. **Recommended next step**

## Workflow

### 1. Detect Active Flow
Look at recent context for signals:
- `dev-autopilot` was invoked → multi-phase pipeline active
- `dev-deep-interview` was invoked → interview loop active
- `dev-plan` was invoked → planning session active
- A `@compass-planner`, `@bolt-executor`, etc. agent was running

### 2. Stop the Flow
- Do NOT call any further agents
- Do NOT continue any in-progress phase
- Do NOT delete artifacts (specs, plans, partial code) — preserve for user inspection

### 3. Generate Cancel Report
Output this structure:

```markdown
## Engineering Layer Cancel Report

**Flow stopped:** {dev-autopilot | dev-deep-interview | dev-plan | other}
**Stopped at phase:** {phase name}
**Reason:** {user request / error / explicit abort}

### Completed
- [phase 1: spec written → workspace/projects/specs/...]
- [phase 2: plan approved → workspace/projects/plans/...]

### In Progress (at cancel time)
- [phase X: implementing Y in file Z]

### Not Started
- [remaining phases]

### Artifacts Preserved
- Spec: `workspace/projects/specs/[C]autopilot-spec-{name}.md`
- Plan: `workspace/projects/plans/[C]autopilot-plan-{name}.md`
- Code changes: see `git status`

### Recommended Next Step
- "Resume manually": pick up from {phase} using {agent} directly
- "Re-run from scratch": delete artifacts and re-invoke `dev-autopilot`
- "Investigate first": review the artifacts before deciding

### Open Questions
[any unresolved decisions the flow was waiting on]
```

## Rules
- **Always preserve artifacts.** Never delete spec/plan files on cancel — the user may want to resume.
- **Never cascade cancels into business layer.** Cancel only stops engineering flows; Clawdia/Flux/etc. routines keep running.
- **Be explicit about what's incomplete.** Don't claim partial work as done.
- **Suggest the cheapest resume path** — usually picking up from where the flow stopped, not restarting.

## Failure Modes To Avoid
- **Silent cancel**: stopping without a report. Always emit the structured summary.
- **Cleanup overreach**: deleting artifacts the user might want.
- **Continuing one more phase**: "let me just finish this last bit". No — stop means stop.
- **Vague status**: "I stopped the workflow." → useless. Always include phase, completed work, and next step.
