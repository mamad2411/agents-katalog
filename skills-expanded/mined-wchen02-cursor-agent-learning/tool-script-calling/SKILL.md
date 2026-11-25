---
name: tool-script-calling
description: Practice agent shell commands, hook scripts around shell, and MCP tool calls. Use when learning or demonstrating tools/script calling, safe repo scripts, or beforeShellExecution patterns.
---

# Tool & script calling (learning)

Short workflow for **how the agent runs commands** vs **calls MCP tools**, using this repo’s safe examples.

## Steps

1. **Shell (terminal)** — From repo root, run the demo scripts and interpret output:
   - `./examples/scripts/demo-info.sh` — one-line JSON demo.
   - `./examples/scripts/count-docs-md.sh` — read-only count of `docs/*.md`.
   - If needed: `chmod +x examples/scripts/*.sh` once.

2. **Hooks (optional)** — Mention or configure `beforeShellExecution` / `afterShellExecution`: audit with [`audit.sh`](../../hooks/advanced/audit.sh) or block risky patterns with [`block-risky-shell.sh`](../../hooks/advanced/block-risky-shell.sh). See [QUICK-REFERENCE.md](../../../docs/QUICK-REFERENCE.md) and [tools-and-shell-calling.md](../../../examples/agent-frameworks/tools-and-shell-calling.md).

3. **MCP (optional)** — If **project-docs** MCP is configured, call **`list_example_scripts`** (check tool schema first) to fetch [examples/scripts/README.md](../../../examples/scripts/README.md). That lists scripts **without** executing them on the server. For broader MCP habits use `@mcp-patterns`.

## Reference

- Full pattern write-up: [tools-and-shell-calling.md](../../../examples/agent-frameworks/tools-and-shell-calling.md)
