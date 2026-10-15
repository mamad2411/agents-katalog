---
name: agentforge-debug
description: >
  Triages a stuck or failing AgentForge pipeline run. Walks the user from
  symptom → state inspection → root-cause classification → fix path. Trigger
  when the user reports an AgentForge run that is "stuck", "failing",
  "looping", "blowing its budget", "not picking up at the gate", "schema
  invalid", "won't dispatch", "node not picking it up", or asks "why is
  pipeline X not finishing?". Do NOT trigger for general AgentForge design
  questions (use `agentforge-workflow`) or for debugging unrelated AI
  pipelines.
license: MIT
metadata:
  author: mandarnilange
  version: "0.2.0"
---

# AgentForge Pipeline Debug

You are helping a user triage an AgentForge pipeline run that is not
behaving. Run state lives in the SQLite/Postgres state store; every agent
step, gate decision, and node heartbeat is recorded there. The dashboard
visualises the same data. This skill walks from the symptom the user
reports to a concrete fix path.

The bias is **read first, change last**. Never propose mutations (re-run,
abort, force-approve gate) until you have read the current run state and
classified the root cause.

## When to use this skill

Trigger on any of:
- "Pipeline X is stuck / not finishing / hung"
- "My run is looping / hitting max iterations / failing schema validation"
- "Gate is not picking up / no one can approve"
- "Agent blew its budget / cost ceiling hit"
- "Node not picking up the job / scheduler isn't dispatching"
- "Dashboard says paused but nothing is happening"
- "Why is pipeline `<id>` failing?"

Do **not** trigger for:
- Workflow design questions (use `agentforge-workflow`).
- General LLM-app debugging unrelated to AgentForge.

## Reference material

Read on demand:

- `references/symptom-tree.md` — symptom → likely cause → first command to run
- `references/state-model.md` — pipeline / agent run / gate status enums and
  what each transition means
- `references/fix-paths.md` — concrete recipes for each root cause
  (re-run agent, edit prompt, swap node, raise budget, force gate, etc.)

The authoritative status enums live at:
- `packages/core/src/domain/models/pipeline-run.model.ts` — `PipelineRunStatus`
- `packages/core/src/domain/models/agent-run.model.ts` — `AgentRunRecordStatus`, `AgentRunExitReason`
- `packages/core/src/domain/models/gate.model.ts` — `GateStatus`

Read the status enum from the source if you need the exact list — do not
rely on memory.

## The flow

### 1. Capture the symptom precisely

Restate what you heard in one or two lines. Resist jumping to fixes.

Ask only what you need:
- The pipeline run ID (or pipeline name + project name).
- What the user expected to happen.
- What they observe (dashboard state, error message, last log line).
- When it started — was it working before? What changed?

Skip questions whose answers you can infer from the dashboard / state.

### 2. Read the run state

Run these in order. Stop reading the moment you have enough to classify:

```bash
# High-level run state — status, current phase, last update
agentforge get pipeline <run-id>

# Per-agent run records — which one is stuck/failed
agentforge get pipeline <run-id> --agents          # if available; otherwise:
# Inspect via dashboard at http://localhost:3001/runs/<run-id>

# Logs for the suspect agent run
agentforge logs <run-id> --agent <agent-name>

# Node pool health — relevant if the symptom is "not dispatching"
agentforge get nodes
```

If the user does not have CLI access (e.g. on a worker host), point them at
the dashboard pages: `/runs/<id>`, `/runs/<id>/agents/<agent-name>`,
`/nodes`.

### 3. Classify the root cause

Use `references/symptom-tree.md`. The classifications:

| Class | One-line tell |
|---|---|
| **Gate hung** | `pipeline_run.status = paused_at_gate`, no recent gate decision |
| **Agent failed (LLM error)** | `agent_run.status = failed`, `error` field non-empty, `exitReason = error` |
| **Agent failed (schema invalid)** | `failed` with `error` mentioning Zod or `validate` step |
| **Agent failed (script step)** | `failed` with last step type `script` and non-zero `exitCode` |
| **Loop spinning** | Agent `running` with high `retryCount` or `loop.iteration ≈ maxIterations` |
| **Budget hit** | `failed` with `exitReason = budget-tokens` or `budget-cost` |
| **Timeout** | `failed` with `exitReason = timeout` |
| **Stuck dispatching** | `agent_run.status = pending`/`scheduled` for long, no node claim |
| **Node down** | `nodes` table shows the targeted node `offline` or stale heartbeat |
| **Node affinity miss** | `pending` forever; no node satisfies `nodeAffinity.required` |
| **Cancelled** | `pipeline_run.status = cancelled` — was someone else's `agentforge cancel <run-id>`? |

Tell the user the class in one sentence and cite the evidence ("agent
`developer` is `failed` with `exitReason: budget-cost`, run cost was
$0.62 vs the $0.60 ceiling").

### 4. Propose the fix path

Use `references/fix-paths.md` for the matched class. Present **the smallest
reversible action first**, then escalating options.

For example, on a schema-invalid failure:
1. Inspect the agent's last LLM output via dashboard or logs.
2. If the LLM hallucinated a missing field, propose tightening
   `prompts/<agent>.system.md` — but **do not edit the file yet**. State
   the proposed change in chat first.
3. If the schema itself is wrong, point at the schema file and propose
   the minimum change. Again, do not edit yet.
4. Re-run only the failed agent: `agentforge run --continue <run-id>` —
   only after the user authorises.

Do not skip to "abort and re-start the pipeline" unless the run is
unrecoverable.

### 5. Confirm before mutating state OR editing files

Two categories of confirmation:

**State mutation** — approving a gate, cancelling a run, re-running an
agent, force-clearing a stuck claim. State your understanding, the
proposed action, and the expected outcome. Wait.

**File edits** — modifying a prompt, a schema, an agent / pipeline /
node YAML, or anything else under `.agentforge/`. **Default to creating
a new file alongside the existing one** if your fix involves a substantive
rewrite (e.g. a redesigned prompt). For surgical changes (one-line tweak),
ask explicit confirmation per file.

Use `AskUserQuestion` (Claude Code) or the host agent's interactive-prompt
tool when available. Otherwise, propose in chat and wait for a yes/no:

> *"Proposed change to `prompts/analyst.system.md`: add 'You MUST include
> a `summary` field in your output JSON.' as a new sentence at the end of
> the 'Output contract' section. Apply this edit? (y/n)"*

One question per file. Read-only investigation (running `agentforge get
...` commands, reading logs, inspecting the dashboard) does **not** need
confirmation.

**Never silently overwrite** a prompt, schema, or agent file. The user's
prior version may be the "right" version; your proposed edit is a
hypothesis until they accept it.

## Hard rules

- **Read before write.** Always inspect run state before proposing a fix.
- **Never tell the user to delete the SQLite file** or `TRUNCATE pipeline_runs`
  to "clear stuck state". That is data loss. Use the proper CLI.
- **Never bypass a gate** without explicit user authorisation. Gates are the
  audit trail.
- **Do not propose `--no-verify` or skip-validation flags** to bypass
  schema failures. Fix the schema or the prompt.
- **Do not assume the dashboard is wrong.** When the dashboard and CLI
  disagree, the state store is the source of truth — read it directly.
- **Propose one fix at a time.** Avoid stacked changes that make it
  impossible to know which one solved the problem.
- **Confirm every file edit explicitly.** Use `AskUserQuestion` or the
  host agent's interactive-prompt tool. Default to creating a new file
  alongside the existing one for substantive rewrites; one-line tweaks
  may edit in place after explicit confirmation. Never overwrite
  silently.

## What success looks like

- The user knows exactly which agent / phase / gate is the failure point.
- The user knows the root-cause class with cited evidence.
- The user has a concrete next action (CLI command, file edit, gate
  decision) and an idea of what will tell them whether it worked.
- No state has been mutated without their explicit go-ahead.
