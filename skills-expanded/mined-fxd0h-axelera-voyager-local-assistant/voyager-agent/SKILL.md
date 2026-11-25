---
name: voyager-agent
description: General Axelera AI Voyager SDK and Metis hardware router for broad repository orientation, task planning, or multi-step work spanning several skills that is not a specific launch, run, deploy, debug, benchmark, app, test, build, or model-zoo task. Route explanation and architecture questions to voyager-help. Activate for any Axelera/Voyager request that does not clearly match a narrower Voyager skill. Prefer voyager-launch for complete runnable pipeline/demo requests.
argument-hint: "<goal description>"
allowed-tools: Read, Bash, Glob, Grep, Edit, Write, Task, mcp__voyager__*
---

# Axelera Voyager SDK Agent

Use this mode when you are developing for **Axelera AI** hardware with the **Voyager SDK**.

## Instructions

Start: **$ARGUMENTS**

### Step 0: Environment & Hardware Detection

{{INCLUDE common/voyager-sdk-setup.md}}

{{INCLUDE common/voyager-task-integration.md}}

1. Clarify the goal (pipeline creation, deployment, inference, benchmarking, debugging).
2. Confirm the target hardware and environment (Axelera device type and form factor, host OS, driver status).
3. Use Axelera Voyager MCP for:
   - Knowledge search (docs + code examples)
   - Project/task tracking for repeatable work
4. Recommended skills:
   - `voyager-launch` for complete runnable pipeline/demo/package/validation requests
   - `voyager-init`
   - `voyager-help`
   - `voyager-new-pipeline`, `voyager-deploy`, `voyager-run`, `voyager-bench`, `voyager-debug`

For routing ambiguity, read `references/skill-routing.md`.

## Parallel Orchestration

See `common/agent-orchestration.md` for the full lane rules. For this skill:

- For multi-part requests, fan out exploration and research subagents in
  parallel (RAG queries, repo orientation, media probing).
- Route implementation work to the specialist skills; do not absorb their
  jobs into one serial thread.
- Serialize anything that touches the Metis device into a single lane.
