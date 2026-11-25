---
name: stackbone-coder
description: >-
  Use this skill to GENERATE a new Stackbone piece from a clean idea through a guided interview:
  first decide what to build — a deep agent, a durable workflow, or a workflow-agent (a workflow
  that calls an agent) — then scaffold it with the stackbone CLI and interview the user surface by
  surface. For an agent you ask for its tools and its system prompt; for a workflow you ask for the
  input data and the output data (the inputSchema / outputSchema); then you walk the capability
  checklist ONE AT A TIME — do we need a database? human-in-the-loop? RAG? storage? an LLM call?
  a connector? prompts? config? secrets? a schedule? to call another agent? — and wire in only the
  surfaces the user actually needs. This skill DRIVES the interview and the scaffolding; it delegates
  the real code to the `stackbone` skill (SDK authoring) and the commands to the `stackbone-cli` skill.
  Trigger on requests like: build a new agent, scaffold a workflow, create a workflow that calls an
  agent, "I want to make an agent that …", "I need a pipeline that takes X and returns Y", start a
  new workspace piece, generate an agent with tools, kick off a new Stackbone project.
  For writing the SDK code itself use the `stackbone` skill; for the CLI surface use `stackbone-cli`;
  for triaging a failing run use `stackbone-debug`.
license: MIT
metadata:
  author: stackbone
  version: '1.2.0'
  organization: Stackbone
  date: July 2026
---

# Stackbone coder — generate a piece by interview

This skill turns _"I want to build X"_ into a scaffolded, wired-up Stackbone piece. It is an **interview + scaffolding orchestrator**: it picks the right shape, runs `stackbone` CLI to lay down the files, then asks the user exactly what each surface needs and wires in only those. It does **not** replace the other skills — it calls them:

- **`stackbone`** skill → the SDK code (tools, workflow steps, the ambient `stackbone` client, every capability deep-dive).
- **`stackbone-cli`** skill → the commands (`init`, `add`, `dev`, `login`, `publish`).
- **`stackbone-debug`** skill → triage when a run misbehaves.

## Golden rules

- **One question at a time.** Never dump the whole interview at once. Ask, get the answer, move on. Use a structured question tool (e.g. `AskUserQuestion`) when you have one.
- **Default to the minimal piece.** Only add a capability the user says yes to. A tool-only agent or a single-step workflow is a perfectly good answer.
- **Never ask for injected env.** `DATABASE_URL`, `OPENROUTER_API_KEY`, `HMAC_SECRET`, `WORKFLOW_REDIS_URL`, etc. are platform-managed — the runtime injects them. Don't ask for connection strings or keys.
- **You orchestrate; the other skills implement.** When it's time to write code, follow the `stackbone` skill. When it's time to run a command, follow the `stackbone-cli` skill.

## The flow (5 steps)

### 1. Pick the piece type

Ask **one** question first — what are we building?

| Type               | What it is                                                                                                               | Pick it when                                                                        |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------- |
| **agent**          | A [deepagents](https://github.com/langchain-ai/deepagentsjs) agent: model + system prompt + tools, holds a conversation. | A human (or another agent) **talks to it** and it reasons/acts with tools.          |
| **workflow**       | Durable, replayable code: `input → steps → output`, no conversation.                                                     | A background job, ETL, a scheduled task, multi-step orchestration with checkpoints. |
| **workflow-agent** | A durable workflow that **calls a deep agent** in one of its steps (`callDeepAgent`).                                    | You need both: deterministic orchestration **and** a reasoning agent in the loop.   |

Then detect the workspace: if the cwd already has `package.json` + `deep-agents/` (or `workflows/`), you'll **`add`** to it; otherwise you'll **`init`** a new one.

### 2. Scaffold with the CLI

Drive `stackbone` (see the **stackbone-cli** skill for the full surface):

- **New workspace:** `stackbone init <name> --with <agent|workflow|workflow-agent>`
- **Existing workspace:** `stackbone add <deep-agent|workflow|workflow-agent> <name>`
- `workflow-agent` and `add workflow --calls <agent>` wire the workflow→agent step for you.

> **Network:** every `add` kind is fully **offline** (the pieces are members of the already-linked workspace). Only `init` needs a signed-in session (`stackbone login`) — it links the workspace to the org.

### 3. Type-specific interview

Open the matching reference and run its interview:

| Building…        | Read & run                                                                                          |
| ---------------- | --------------------------------------------------------------------------------------------------- |
| an agent         | [references/agent.md](references/agent.md) — its **tools** and its **system prompt**                |
| a workflow       | [references/workflow.md](references/workflow.md) — its **input** and **output** data → the schemas  |
| a workflow-agent | [references/workflow-agent.md](references/workflow-agent.md) — both, plus the workflow→agent wiring |

### 4. Capability checklist — one at a time

Open [references/capabilities.md](references/capabilities.md) and walk **every** capability with the user, one question each: _do we need a database? storage? an LLM call? RAG? human-in-the-loop? a connector? prompts? config? secrets? a schedule? to call another agent?_ For each **yes**, the reference tells you the surface, where it's reachable from (tool vs. workflow step), what to add (a `schema.ts`, a line in an optional `agent.yaml`, a `config.schema.ts`…), and which `stackbone`-skill deep-dive to follow for the code.

### 5. Wire & verify

Write the code with the **stackbone** skill, then boot the emulator with `stackbone dev` (see **stackbone-cli**) and exercise the piece — chat the agent, `start` the workflow, check a `run` — before you call it done.

## Reference files

| File                                                         | What it holds                                                                                                                            |
| ------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------- |
| [references/agent.md](references/agent.md)                   | The agent interview: role, system prompt, the tools (name / description / inputs / behaviour), model choice.                             |
| [references/workflow.md](references/workflow.md)             | The workflow interview: trigger, input data, output data, the steps; how answers map to `inputSchema` / `outputSchema` and `'use step'`. |
| [references/workflow-agent.md](references/workflow-agent.md) | The combined interview + the workflow step that calls the agent via `callDeepAgent`.                                                     |
| [references/capabilities.md](references/capabilities.md)     | The full capability checklist — every surface, when it applies, what it adds, and the deep-dive pointer.                                 |
