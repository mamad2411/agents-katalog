---
name: kimi-replay
description: "Re-render a stored event log for a completed plugin-managed Kimi job. Use only when the user explicitly asks to replay a Kimi job."
---

# Kimi Replay

Forward this request to the local kimi-code companion runtime by shell. Do not use MCP for this skill.

## Invocation

- Resolve the plugin root: prefer `$PLUGIN_ROOT` if the host sets it; otherwise use the directory that CONTAINS the `skills/` directory (i.e. two levels up from this `SKILL.md`).
- Sanity check: `<plugin-root>/scripts/companion.sh` must exist — it is the bundled entrypoint that resolves Node and runs the compiled runtime from `<plugin-root>/dist/`.
- Launch the shell command from the user's current workspace directory so `scripts/companion.sh` captures the intended workspace cwd.
- Run: `PLUGIN_ROOT="<plugin-root>" "<plugin-root>/scripts/companion.sh" replay <args>`
- Data directories: standard cache installs verify shared `CLAUDE_PLUGIN_DATA`/`PLUGIN_DATA` against this package's own host-specific directory. On `PLUGIN_DATA_CONFLICT`, surface the error; do not automatically choose a new store or copy data. An explicit absolute `KIMI_PLUGIN_CC_DATA` selects a custom data parent (the runtime appends `kimi-plugin-cc/`). Checkouts retain unambiguous legacy variables and the Codex fallback under `CODEX_HOME` or `HOME`; a launch with no home needs an explicit data root.

## Arguments

Pass through: `<job-id>`

## Handling

- Require a job id and pass it unchanged.
- Return companion stdout verbatim because replay output is the diagnostic artifact.
