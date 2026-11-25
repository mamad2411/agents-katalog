---
name: t2a-memory
description: Use to install T2A Memory, remember a fact in local memory, and resolve the emitted T2A handoff without LLM API keys.
---

# T2A Memory

## Instructions

Use this skill when the user asks you to install T2A Memory, remember a fact, or use user-level memory.

1. Run `{{T2A_MEMORY_BIN}} remember --memory-home {{MEMORY_HOME}} --tool-home {{TOOL_HOME}} "<fact>"`.
2. Read the emitted `t2a.handoff`.
3. Use the generic `t2a` skill if it is available to resolve the capsule.
4. Fallback workflow: read `task.json`, `prompt.md`, `input.json`, and `output.schema.json`; write only `output.json`.
5. Before commit, run core T2A validation and T2A Memory validation:
   - `{{T2A_BIN}} validate "<task-dir>"`
   - `{{T2A_MEMORY_BIN}} validate --memory-home {{MEMORY_HOME}} --tool-home {{TOOL_HOME}} "<task-dir>"`
6. If both validations pass, run `{{T2A_MEMORY_BIN}} commit --memory-home {{MEMORY_HOME}} --tool-home {{TOOL_HOME}} "<task-dir>"`.
7. After commit, verify with `{{T2A_MEMORY_BIN}} status --memory-home {{MEMORY_HOME}}` and `{{T2A_MEMORY_BIN}} read --memory-home {{MEMORY_HOME}}`.
8. Do not rerun `{{T2A_MEMORY_BIN}} validate` on the same already committed task as the normal close-out check.

## Guidelines

- Do not edit `memory.json` or `MEMORY.md` directly.
- Do not use network access during memory handoff or consolidation.
- Do not call LLM APIs or install LLM SDKs for this workflow.
- Do not ask for `model`, `base_url`, `api_key`, provider settings, or vector database configuration.
- Do not run `git commit` unless the user separately asks for a git commit.
- `t2a-memory commit` commits to local memory files only. It is not `git commit`.

## Examples

- "Install T2A Memory for yourself and remember that T2A tools should not embed LLM API keys."
- "Remember this preference in T2A Memory."
- "Use T2A Memory to store this durable local-memory fact."
