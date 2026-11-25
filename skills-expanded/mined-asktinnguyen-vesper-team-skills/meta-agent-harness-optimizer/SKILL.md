---
name: meta-agent-harness-optimizer
description: This skill should be used when studying, extending, porting, or operationalizing the canvas-org/meta-agent architecture for continual harness optimization. It applies when building systems that improve agent configs from traces, designing filesystem-backed experience stores, analyzing proposer/evaluator loops, capturing harness prompts and tool surfaces, or adapting these patterns into Vesper or another agent runtime.
---

# Meta-Agent Harness Optimizer

Understand and reuse the `canvas-org/meta-agent` design as a practical blueprint for **continual harness optimization**.

The source system is a Python codebase that:
- runs an agent on benchmark tasks,
- captures traces and verification outcomes,
- stores candidate configs and results on disk,
- prompts a proposer agent to write one better harness config,
- validates and evaluates that config,
- then repeats the loop.

## When to use this skill

Use this skill when the task involves any of the following:
- porting `meta-agent` ideas into Vesper,
- designing a self-improving agent loop,
- understanding how the proposer/evaluator architecture works,
- extracting or preserving the repo's **scripts, tool calls, methods, and prompts**,
- adding a new benchmark backend,
- extending the filesystem experience store,
- or turning meta-agent into a reusable team pattern.

## What to read first

Start with:
- `workflows/execution-workflow.md` for the default execution path

Then choose references based on the task:
- Read `references/architecture.md` to understand the whole system.
- Read `references/scripts.md` to capture executable entrypoints, CLI flows, and operational commands.
- Read `references/toolcalls-and-tools.md` to inspect the runtime tool surfaces, hook events, and tau adapter tool wrapping.
- Read `references/methods.md` to inspect key functions, signatures, and file:line implementation anchors.
- Read `references/prompts.md` to capture the proposer prompt, skill-evolver prompt, and harness-guidance prompt logic.
- Read `references/implementation-guide.md` when building a similar system elsewhere.
- Read `references/conventions.md` to preserve naming, file layout, and configuration contracts.

## Core operating model

Treat `meta-agent` as a loop over **artifacts**, not over hidden runtime state.

The key flow is:
1. Load benchmark definitions.
2. Load a harness config module exposing `build_options(ctx)`.
3. Run tasks and save traces.
4. Aggregate candidate results into a filesystem experience store.
5. Prompt a proposer to inspect failures and write a new config.
6. Validate the config before expensive evaluation.
7. Re-evaluate and keep history.
8. Optionally evaluate on holdout and even improve the proposer skill itself.

Read `references/architecture.md` before making architectural claims.

## What matters most in this repo

The highest-signal reusable patterns are:
- **config-as-strategy** via `build_options(ctx)` modules,
- **filesystem memory** for candidate configs, scores, traces, and summaries,
- **tool adaptation** that exposes benchmark environments through the Claude Agent SDK,
- **prompted outer-loop optimization** where the model edits harness code instead of solving tasks directly,
- **meta-optimization** where the system can rewrite its own proposer guidance.

## Scripts, tool calls, methods, and prompts

This skill is intentionally organized so those four categories stay distinct:

### 1) Scripts
Use `references/scripts.md` for:
- `python -m meta_agent.outer_loop`
- `python -m meta_agent.eval_runner`
- `python -m meta_agent.cli`
- benchmark reproduction commands from README
- the source repo's operational command surface

### 2) Tool calls
Use `references/toolcalls-and-tools.md` for:
- Claude CLI invocation flags in `_run_claude_cli(...)`
- Claude Agent SDK hooks and tool surfaces
- tau adapter tool wrappers such as `talk_to_customer`
- MCP-style adapter patterns built via `@tool(...)` and `create_sdk_mcp_server`

### 3) Methods
Use `references/methods.md` for:
- major functions,
- signatures and purposes,
- file:line references,
- extension seams.

### 4) Prompts
Use `references/prompts.md` for:
- the outer-loop proposer prompt,
- the skill-evolver prompt template,
- the bundled proposer `SKILL.md` instructions,
- baseline prompt appends like `BOOTSTRAP_PROMPT`.

## How to work with this pattern

When adapting the design:
- preserve the `build_options(ctx)` contract unless deliberately replacing the config layer,
- keep traces and scores inspectable on disk,
- prefer one harness change at a time,
- keep holdout evaluation separate from search data,
- separate proposal, validation, and evaluation concerns.

## Recommended workflow by task type

Follow `workflows/execution-workflow.md` as the default operating path.

### If implementing a similar system in Vesper
1. Read `workflows/execution-workflow.md`
2. Read `references/architecture.md`
3. Read `references/prompts.md`
4. Read `references/toolcalls-and-tools.md`
5. Read `references/implementation-guide.md`

### If auditing what the original repo actually does
1. Read `workflows/execution-workflow.md`
2. Read `references/methods.md`
3. Read `references/scripts.md`
4. Read `references/prompts.md`

### If extending the source repo
1. Read `workflows/execution-workflow.md`
2. Read `references/conventions.md`
3. Read `references/methods.md`
4. Read `references/architecture.md`

## Bundled helper scripts

Use these optional local helpers when a local clone is available:
- `scripts/refresh-from-local-clone.sh` — refresh copied extracts from a local `meta-agent` clone into this skill's reference snapshot area.
- `scripts/method-inventory.sh` — generate a quick numbered-method inventory from the local clone for verification.

These scripts are convenience helpers. The authoritative interpretation remains in the reference files.
