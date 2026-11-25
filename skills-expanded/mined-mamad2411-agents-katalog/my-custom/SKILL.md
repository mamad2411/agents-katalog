---
name: my-custom-skill
description: Example custom agent skill — a template to get started.
---

# My Custom Skill

This is a template for creating a custom agent skill.

## How Skills Work

There are **two valid skill patterns** in the current architecture:

### Pattern A: Prompt-Only (Recommended)

No `script` field in frontmatter. This SKILL.md is injected into the LLM's context
when `activate_skill` is called. The LLM then uses built-in atomic tools
(bash, codegen, workspace_read/write, glob, grep) to accomplish the task.

This is the **primary extension mechanism** — like Claude Code's slash commands.

### Pattern B: Subprocess Script

Add `script: scripts/my-script.py` to frontmatter. The script is executed as a
subprocess with `--args-json` and must communicate via stdout (JSON) and file I/O
in the agent workspace (`AGENT_WORK_DIR`). Scripts **cannot** access the LLM or
environment router — use this only for deterministic computation.

## Behavioral Guidelines (Edit for Your Skill)

When this skill is activated:

1. Use `codegen` to query the environment for relevant information.
2. Use `workspace_read` / `workspace_write` to persist state.
3. Use `bash` to run any computation or data processing.
4. Call `done` with a summary when finished.

## Example: A "Daily Journal" Skill

When activated, the agent should:
1. `codegen` with instruction: "What happened recently? Summarize recent events."
2. `workspace_read` path `journal.jsonl` to load previous entries.
3. `workspace_write` path `journal.jsonl` to append today's entry.
4. `done` with summary of what was journaled.
