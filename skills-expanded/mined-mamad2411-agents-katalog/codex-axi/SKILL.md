---
name: codex-axi
description: Delegate engineering work to Codex tasks or deterministic workers and inspect or steer their state.
---

# codex-axi

Use `codex-axi` to control Codex work in the current workspace.

- `codex-axi task list`
- `codex-axi worker start --message "<task>"`
- `codex-axi delegate --message "<task>"`

Workers are ordinary Codex threads managed by codex-axi. They are not native Codex subagents.
