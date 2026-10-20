---
description: Kick off a brand new app from an idea — runs the full Atelier pipeline from PRD to shippable v1.
argument-hint: [one-line idea or leave blank to be interviewed]
allowed-tools: Read, Write, Edit, Bash, Agent, TodoWrite
---

You are kicking off a new app build with the **Atelier** team.

User idea: $ARGUMENTS

## Your plan

1. Invoke the **orchestrator** sub-agent with the "New app from idea" workflow.
2. Orchestrator will:
   - Interview the user via `product-manager` (AskUserQuestion)
   - Produce PRD + features.json
   - Delegate to `solution-architect` and `ui-ux-designer` (parallel)
   - Spin up `database-engineer`, `backend-dev`, and the relevant frontend specialist(s) in parallel
   - Gate with `test-engineer`, `code-reviewer`, `security-auditor`, `qa-verifier`
   - Ship via `devops-engineer`
   - Persist state via `progress-keeper` at every milestone

3. Track progress in a top-level TodoList.
4. Stop and escalate to the user whenever an open question lacks a clear default.

Call the orchestrator now. Do not do the work yourself.
