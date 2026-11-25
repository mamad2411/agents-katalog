---
name: project-convergence
description: Use when a project starts from zero or is already drifting because vibe coding, scope drift, unclear agent progress, weak handoff, or missing coordination artifacts make it hard to know what the next agent should do. Trigger on requests involving delivery-plan.md, AGENTS.md, CLAUDE.md, OpenSpec planning, project convergence, agent handoff, agent coordination, or lossless multi-agent collaboration.
---

# Project Convergence

## Overview

Turn a drifting project into a convergent multi-agent workflow. Projects expand faster than they converge when no shared control surface exists.

Use this skill to establish four linked artifacts:
- `delivery-plan.md` as the single progress and handoff surface
- OpenSpec changes as the executable units of work
- `AGENTS.md` as the shared operating contract
- `CLAUDE.md` as the bootstrap instruction to read `AGENTS.md`

## Use This Skill

Use when:
- A new project has no shared planning surface.
- Different agents or humans need lossless handoff.
- The project keeps growing but nobody can state current phase, blocker, or next verifiable output.
- The user asks for `delivery-plan.md`, `AGENTS.md`, `CLAUDE.md`, OpenSpec setup, scope control, or "what should the next agent do".
- A repo already has some planning files, but they are stale, conflicting, or not linked to execution.

Do not use when:
- The task is a one-off code change with no handoff or project-shaping risk.
- The repo already has a working convergence system that clearly maps stage status, next change, and agent rules.

## Required Workflow

### 1. Detect convergence failure

- Check whether the repo lacks any of these signals:
  - current phase
  - active blockers
  - next verifiable output
  - next OpenSpec change
  - explicit cross-agent operating rules
- If those signals are missing, assume the project is not convergent yet.

### 2. Create or repair `delivery-plan.md`

Make `delivery-plan.md` the entry point for project state, not roadmap copy and not launch copy.

- State the current phase in one line.
- List stage goals, blockers, next verifiable output, and the next OpenSpec change to pick up.
- Include milestone status and traceability pointers (`Decision Log`, `Source Links`).
- Keep it short enough that a new agent can scan it first and act second.
- Read [references/delivery-plan-guidelines.md](./references/delivery-plan-guidelines.md) before drafting or repairing it.

### 3. Translate stage work into granular OpenSpec changes

- At phase kickoff, you MUST create the full proposal set for that phase before execution starts.
- If proposal coverage for the active phase is incomplete, treat the project as non-convergent state.
- Break stage work into small proposals that each produce one verifiable result.
- Prefer many small changes over one vague umbrella change.
- Map each proposal to a milestone and one verifiable output.
- Link each plan item to exactly one next actionable OpenSpec change.
- Keep CLI details out of this skill body.

**REQUIRED SUB-SKILL:** Use `openspec` for CLI commands, delta syntax, validation, and archive flow.

Read [references/openspec-breakdown-guidelines.md](./references/openspec-breakdown-guidelines.md) for the breakdown rules this skill expects.

### 4. Maintain `AGENTS.md` and `CLAUDE.md`

- Put durable operating rules in `AGENTS.md`:
  - required artifacts
  - handoff expectations
  - planning discipline
  - update rules
  - project-specific constraints
- Put only a bootstrap instruction in `CLAUDE.md`:
  - tell the agent to read `AGENTS.md` first
  - avoid duplicating the full operating contract
- Read [references/agent-context-files.md](./references/agent-context-files.md) before writing either file.

### 5. Re-sync after every milestone, blocker, or handoff

- Update `delivery-plan.md` when phase, blocker, or next output changes.
- Update OpenSpec when the next executable unit changes.
- Update `AGENTS.md` when operating rules change.
- Keep `CLAUDE.md` stable unless the bootstrap instruction becomes wrong.
- Read [references/handoff-and-feedback-loop.md](./references/handoff-and-feedback-loop.md) for the expected loop.

## Artifact Contract

### `delivery-plan.md`

Must contain:
- project phase
- stage objective
- milestone status
- current blockers
- next verifiable output
- next OpenSpec change
- handoff notes needed without replaying full chat history
- decision log pointers
- source links for key context

Must not become:
- product marketing copy
- a long roadmap with no next action
- a changelog dump with no decision surface

### OpenSpec changes

Must contain:
- fine-grained proposals
- clear tasks
- verifiable output per change
- proposal-to-milestone mapping
- linkage from current plan item to next change

Must not become:
- one giant proposal for a whole phase
- a backlog with no validation target

### `AGENTS.md`

Must contain:
- shared project operating rules
- required artifact update behavior
- handoff expectations
- coordination rules that any agent can follow without prior chat context

Must not become:
- a duplicate of all planning content
- a personal note file for one agent

### `CLAUDE.md`

Must contain:
- a clear instruction to read `AGENTS.md` first
- only minimal bootstrap context if needed

Must not become:
- a second full operating manual that can drift from `AGENTS.md`

## Handoff Checklist

- State current phase.
- State blocker or explicitly say none.
- State the next verifiable output.
- State the next OpenSpec change to pick up.
- State decision delta since the previous handoff.
- Include source links for critical context.
- Confirm whether `delivery-plan.md` was updated.
- Confirm whether `AGENTS.md` changed.
- Keep `CLAUDE.md` pointed at `AGENTS.md`.

## Common Mistakes

| Mistake | Correction |
|---|---|
| Starting implementation before establishing a shared control surface | Create or repair `delivery-plan.md` first. |
| Using `delivery-plan.md` as roadmap copy | Keep it focused on current phase, blockers, next output, and next change. |
| Starting a phase without full proposal coverage | Create the full phase proposal set before execution. |
| Creating one oversized OpenSpec proposal | Split work into small changes with one verifiable result each. |
| Handoff lacks traceability | Add decision delta and source links in handoff payload. |
| Duplicating the full contract in `CLAUDE.md` | Keep the contract in `AGENTS.md`; make `CLAUDE.md` a pointer. |
| Updating code but not handoff artifacts | Re-sync the four artifacts after every milestone, blocker, or handoff. |

## Anti-Patterns

- "We can keep moving fast and document later."
- "One big proposal is easier than many small ones."
- "The next agent can infer status from commit history."
- "We only need chat history, not handoff artifacts."
- "CLAUDE.md and AGENTS.md can both contain the same full rules."

## Example Requests

Chinese example:
> 這個專案從 0 開始一路 vibe coding，現在功能一直長、每個 agent 做到哪裡也不清楚，幫我整理。

Expected response shape:
- Establish `delivery-plan.md` first.
- At phase kickoff, create the full proposal inventory for the active phase before execution.
- Map current phase, blockers, next verifiable output, and next OpenSpec change.
- Define `AGENTS.md` as the operating contract.
- Ensure `CLAUDE.md` tells future agents to read `AGENTS.md`.

Chinese example:
> 我想讓不同家的 agent 可以無縫交接，不要再丟失上下文。

Expected response shape:
- Repair or create the four-artifact workflow.
- Require Decision Log and Source Links for critical handoff context.
- Tighten handoff rules in `AGENTS.md`.
- Keep OpenSpec changes granular enough that the next agent can pick up exactly one change.

Chinese example:
> 幫我更新目前階段進度，讓下一個 agent 一眼知道要接哪個 change。

Expected response shape:
- Update milestone status in `delivery-plan.md`.
- Update next verifiable output and next OpenSpec change.
- Record any decision delta and source links that changed the plan.

## References

- [references/delivery-plan-guidelines.md](./references/delivery-plan-guidelines.md)
- [references/agent-context-files.md](./references/agent-context-files.md)
- [references/openspec-breakdown-guidelines.md](./references/openspec-breakdown-guidelines.md)
- [references/handoff-and-feedback-loop.md](./references/handoff-and-feedback-loop.md)
