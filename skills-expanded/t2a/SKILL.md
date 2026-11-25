---
name: t2a
description: Complete T2A Protocol capsules when a tool returns t2a.handoff, points to task.json, needs output.json, or asks for validation.
---

# T2A

## Instructions

Use this skill when a tool returns `type: "t2a.handoff"`, points to `task.json`, asks for `output.json`, or asks you to complete a T2A task.

1. Read `task.json` first.
2. Read `prompt.md` and declared input files.
3. Follow `output.schema.json`.
4. Write structured output to the declared output path.
5. Run validation if it is safe and available.
6. Repair `output.json` until validation passes.
7. Stop after validation unless the user explicitly asks you to resume or continue.

## Guidelines

- Do not call external LLM APIs for T2A.
- Do not ask for `model`, `base_url`, `api_key`, or provider configuration.
- Do not invent IDs, URLs, citations, resource IDs, or references.
- Do not read undeclared files unless the user explicitly authorizes it.
- Missing `output.json` can be normal before you complete a pending handoff.
- Treat T2A core validation and issuing-tool domain validation as separate layers.
- Do not resume side-effecting workflows unless explicitly instructed by the user, task policy, or host runtime.

## Examples

- A CLI prints `T2A handoff required` and returns a task directory.
- A tool returns `{"type":"t2a.handoff","local":{"task_file":".../task.json"}}`.
- The user asks you to complete a T2A capsule and run validation.
