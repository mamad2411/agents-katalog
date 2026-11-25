---
name: cli-for-agents
description: "Design/review CLIs for agent-friendliness: non-interactive flags, layered help, idempotency, dry-run, actionable errors. Trigger: 'agent CLI', 'automation-friendly CLI', 'headless CLI design'."
when_to_use: "Activate when building or reviewing a CLI that agents will drive. Do NOT use for general coding or web UI work."
argument-hint: "[CLI name or command to design/review]"
disable-model-invocation: true
license: Apache-2.0
compatibility:
  - opencode-native
  - claude-standalone
  - cursor-native
  - codex
metadata:
  author: controlkeel
  version: "1.1"
  category: development
  ck_mcp_tools: [ck_validate, ck_finding]
---

# CLI for Agents

CLIs that agents can drive reliably. Most human-oriented CLIs block agents with interactive prompts, missing examples, and ambiguous errors.

## Do NOT use when
- Building web UIs or non-CLI tools
- The CLI already follows these patterns and needs no review

## Checklist

Design or review against these rules. Record violations as `ck_finding` (rule `cli.agent_unfriendly`).

- **Non-interactive first**: Every input as a flag. Interactive is fallback, not default.
- **Layered help**: `--help` per subcommand, not full manual dump.
- **Examples on every `--help`**: Real copy-pasteable invocations.
- **stdin/pipelines**: Accept stdin where sensible, support chaining.
- **Actionable errors**: Missing flag → correct example invocation, not a hang.
- **Idempotency**: Same command twice = safe (no-op or "already done").
- **Destructive actions**: `--dry-run` to preview, `--yes`/`--force` to skip confirmations.
- **Predictable structure**: `resource verb` pattern consistent across all subcommands.
- **Machine-readable output**: IDs, URLs, durations on success — not just "done".

## Output

- CLI design with flags, examples, error messages
- Or: review findings for existing CLI
- `ck_finding` records for agent-unfriendly patterns
