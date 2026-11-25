---
name: cursor-check-agent-compatibility
description: "Run the full repository compatibility pass: scanner score, startup path, validation loop, and docs reliability."
---

## Runtime selection

Before runtime-dependent work, read [execution selection](references/runtime/selection.md). In a verified T3 host follow [the T3 contract](references/runtime/t3.md) and its method reference; the inline section below is the native Codex branch, not literal T3 dispatch. Outside T3, native Codex follows that inline branch unchanged. If the host is ambiguous or a required capability is unavailable, report the gap; a permission refusal never authorizes switching branches.

## Native Codex branch

# Check agent compatibility in Codex

Run a bounded, evidence-based compatibility review of an explicitly supplied local plugin directory.

## Workflow

1. Run `python3 scripts/cursor_plugin_scanner_adapters.py compatibility <plugin-root> --local-scan`.
2. Preserve the four separate results: deterministic structural scan, startup-contract review, validation-contract review, and documentation reliability review.
3. Report `local_codex_compatibility_score` as the local static Codex score. Never label it as the upstream Agent Compatibility Score; `agent_compatibility_score` remains unavailable unless the upstream scanner was separately reviewed and executed.
4. Treat `runtime_executed: false` and `components_executed: false` as material limits. Verify actual startup and validation behavior separately when the user requests runtime proof and the repository provides safe commands.
5. Prioritize fixes from observed issues. Do not penalize the target for unavailable external tooling.

The local scanner never executes plugin components, hooks, MCP servers, startup commands, or tests. It performs no network access, credential reads, or external writes.
