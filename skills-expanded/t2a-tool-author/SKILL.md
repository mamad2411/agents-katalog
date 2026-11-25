---
name: t2a-tool-author
description: Use when modifying a CLI, API, SDK, CI job, workflow, or MCP server that has embedded LLM calls, model/provider config, or a bounded reasoning checkpoint and needs T2A authoring guidance.
---

# T2A Tool Author

## Instructions

Use this skill when changing a tool to support T2A.

1. Find one bounded reasoning checkpoint.
2. Replace one embedded model call with a local T2A handoff.
3. Keep the rest of the tool unchanged.
4. Create a capsule with `task.json`, `prompt.md`, bounded input, and `output.schema.json`.
5. Return a T2A Handoff Result with `type: "t2a.handoff"`.
6. Accept host-agent-written `output.json`.
7. Run T2A protocol validation and tool-owned domain validation before commit/resume.
8. Add a demo fixture or template task and run `t2a validate`.

Before commit/resume, check:

- protocol validation passed
- `validation.json` matches the current task
- domain validation passed
- only then mutate state

Before editing, inspect the tool and propose:

- the checkpoint to migrate
- files to change
- files to add
- validation command
- risks / assumptions

Wait for approval unless the user explicitly asked you to proceed.

## Guidelines

- Do not add OpenAI, Anthropic, Gemini, Ollama, LangChain, or other LLM SDKs.
- Do not add new `model`, `provider`, `base_url`, `api_key`, or provider config for the migrated T2A path.
- Do not remove unrelated existing provider configuration unless it belongs to the checkpoint being migrated and the user approves.
- Do not build an agent framework, scheduler, daemon, queue, or MCP bridge.
- Do not refactor the whole tool.
- Do not skip `output.schema.json`.
- Do not let the host agent directly mutate tool state.
- Do not trust `output.json` without validation.
- Do not auto-resume before validation.
- A first migration demo fixture may be generated and test-only.

## Examples

- Replace a summarization provider call with a capsule and `output.schema.json`.
- Replace issue triage model config with a local `t2a.handoff`.
- Replace risk classification model calls with host-agent reasoning and tool-owned ID validation.
