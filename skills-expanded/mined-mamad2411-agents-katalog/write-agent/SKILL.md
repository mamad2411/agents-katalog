---
name: write-agent
description: Use when creating, designing, or fixing an omp subagent (task agent) — triggers include "write an agent", "make me an agent", "create a subagent", agent `.md` definitions, and agents that misbehave when spawned via task.
---

# write-agent

Turn a job into an omp task agent: grill the design, write the definition, smoke the spawn. Three steps, in order. Each ends on a completion criterion; do not advance early.

## 1. Grill

Map the agent as a **design tree** and interview the user per the grilling-via-ask rule. Ask the frontier in rounds; a question blocked by an open sibling waits for the next round. Facts you can look up (existing agents, tool names, model selectors) are yours — check `~/.omp/agent/agents/`, `.omp/agents/`, and installed plugins first; the *decisions* are the user's.

Frontier branches, in rough order:

- **Job**: one sentence, one responsibility. An agent with two jobs is two agents.
- **Surface**: tools it may use. Read-only research (read/grep/glob/find/web_search) vs. mutation (edit/write/bash). Wrong side = untrustworthy output or a sandboxed agent that can't finish.
- **Autonomy**: does it run unattended (`blocking: false`, async) or must the parent wait (`blocking: true`)? Can it spawn children (`spawns`)?
- **Model**: effort level and selector (`@smol`, `@slow`, role alias, or concrete model). Cheap effort for mechanical work; high effort for reasoning-bound jobs.
- **Output**: free text, or a schema the parent parses? Structured consumers (workpools, orchestration) want `output`.
- **Triggers**: when should the parent dispatch this agent instead of another? These words become its `description`.
- **Home**: where the file lives — project `.omp/agents/` (repo-shared), user `~/.omp/agent/agents/` (personal), or shipped in a plugin's `agents/` dir (distributed with base@heynemann).

Completion: frontier empty **and** the user confirms the design. Read back the tree before writing anything.

## 2. Write

Read [`agent-format.md`](agent-format.md), then write one `.md` file named `<agent-name>.md` in the home the user picked. `name` + `description` + body (the system prompt) are required; add optional frontmatter fields only where the grill gave you a decision.

**Description is a trigger pointer**: front-load the leading words, list the branches that should dispatch this agent, cut what the body already says. Same rules as a skill description.

**The body is the whole world**: subagents start blank — no conversation history, no user context. The dispatch `task` text arrives at first turn; the parent's `context` string precedes it. Write the body so an agent that has never seen this conversation can succeed: state the job, the contract (what it receives, what it returns), the constraints, and the completion criteria. Borrow the dispatch convention that keeps this readable: `# Target`, `# Change`, `# Acceptance`.

**Positive phrasing**: prompt the behavior you want; a prohibition earns its place only as a hard guardrail, paired with the positive target.

**RFC 2119**: MUST/SHOULD/OPTIONAL with the same weight as the harness uses — MUST for correctness-critical behavior, never for style.

Completion: file written, frontmatter parses (name + description non-empty), body self-contained. Re-read the file once before advancing.

## 3. Smoke

Dispatch proves it: spawn the agent with a trivial task exercising its main path (read-only agent → one real lookup; structured agent → one schema-valid return). Fix what the smoke exposes — a spawn error, a schema miss, a rambling return — then smoke again.

Completion: the dispatch returned and its shape matches the design from step 1.

Report to the user: file path, the trigger `description` verbatim, and the smoke result.
