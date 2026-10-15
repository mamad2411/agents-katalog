---
name: general-ticket-orchestration
description: 'Core orchestration mechanics for dispatching agents, handling responses, managing state, and coordinating workflows. Load for any multi-agent task — planning, implementation, or general coordination.'
metadata: v20260325.1
---


# Orchestration

Dispatch agents, parse responses, manage state, escalate failures. This file covers universal mechanics. See reference files for workflow-specific patterns.

## Role-Based Dispatch

Map roles to whatever agent types your project provides. If only one agent type exists, it fills all roles.

| Role       | Purpose                          | Typical Agent Types              |
| ---------- | -------------------------------- | -------------------------------- |
| Researcher | Explore codebase, gather context | planner, developer, general      |
| Writer     | Create plans, documents          | planner, developer               |
| Executor   | Implement code changes           | executor, developer              |
| Critic     | Review artifacts for gaps        | planner, developer               |
| Verifier   | Run tests, check results         | validator, developer, general    |

Pick the best available agent for each role. One agent can fill multiple roles across dispatches.

## Model Tier Selection

| Tier     | Use For                                                          |
| -------- | ---------------------------------------------------------------- |
| Highest  | Complex implementation, critical reviews, plan writing, deputies |
| Standard | Normal implementation, research, documentation                   |
| Light    | Summarization, simple verification, parsing                      |

## Dispatch Patterns

**Parallel:** Independent tasks dispatched together. Example: multiple research agents exploring different areas.

**Sequential:** Each task depends on the prior result. Example: research, then compile, then write.

**Default to sequential when unsure.** A failed parallel batch costs more than a slower sequential chain.

## Status Classification

| Status  | Meaning                       | Action                                     |
| ------- | ----------------------------- | ------------------------------------------ |
| SUCCESS | Task fully completed          | Log, move to next task                     |
| PARTIAL | Some work done, more remains  | Log partial, dispatch agent for remainder  |
| BLOCKED | Needs external input          | Stop immediately, escalate                 |
| FAILED  | Task failed                   | Stop immediately, escalate                 |

## Context Passing

Keep prompts lean. Agents read their own procedure files.

**Include:** ticket path, file paths, brief summaries of prior discoveries, critical constraints.

**Omit:** full documents, detailed instructions, architecture explanations already on disk.

## Ticket Folder Convention

```
tickets/
  ticket-00001-short-description/
    description.md
    research/
    compiled-research.md
    plan.md
    implementation/
      phase-N.md
    review-gate.md
    logs/
      summary.md
      phase-N.md
```

Auto-increment ticket numbers. Format: `ticket-NNNNN`.

## Orchestrator Boundaries

**Does:**
- Select and dispatch agents by role
- Generate all ticket documents via `render.js` before dispatching
- Pass generated file paths to subagents in dispatch prompts
- Parse responses, decide next action
- Maintain its own logs (summary, phase logs) after every dispatch
- Escalate blockers immediately

**Does NOT:**
- Write or modify code (delegates to Executor)
- Run commands — build, test, lint (delegates to Verifier)
- Conduct codebase research (delegates to Researcher)
- Edit files that subagents are responsible for filling in
- Retry BLOCKED or FAILED work
- Make architectural decisions

## Error Escalation

- BLOCKED or FAILED: stop immediately, escalate to project lead
- No retries on implementation failures
- Verification fix loops: max 2 attempts, then escalate
- Always include: what was attempted, what went wrong, what is needed

## Document Generation

The orchestrator creates ALL ticket documents. Subagents never create files from scratch — they fill in `[bracketed placeholders]` in files the orchestrator has already generated.

**Workflow:** Generate doc → dispatch subagent with file path → subagent edits the file → orchestrator validates.

```
node scripts/render.js <type> --ticket <ticket-path> [--key value ...]
node scripts/render.js list --verbose    # show all templates and args
```

`<ticket-path>` is the path to the ticket folder (e.g., `tickets/active/my-ticket` or just `active/my-ticket` — leading `tickets/` is stripped automatically).

The script outputs only the absolute file path of the generated file — pass this path to the subagent in its dispatch prompt. Templates live in `templates/` for human reference.

Subagents will not edit files unless explicitly told to. Always include the file path and an edit instruction in the dispatch prompt:

> Read the file at `/abs/path/to/research/api-layer.md`. It has `[bracketed placeholders]`. Use the Edit tool to replace ALL placeholders with your findings. Do not return findings in your response — write them into the file.

## Workflow Selection

| Situation                        | Reference                        |
| -------------------------------- | -------------------------------- |
| General task or ad-hoc work      | `references/general.md`          |
| Planning a ticket from scratch   | `references/planning.md`         |
| Executing an existing plan       | `references/implementation.md`   |

## References

- `references/general.md` — General task orchestration patterns
- `references/planning.md` — Research pipeline, plan writing, critique flow
- `references/implementation.md` — Phase execution, executor dispatch, pivots
