---
name: setup-engine
description: "Configure the project's game engine and version. Pins the engine in AGENTS.md, detects knowledge gaps, and populates engine reference docs via web search when the version is beyond the LLM's training data."
---

> Port provenance: adapted from the pinned upstream source at `984023ddac0d5e27624f2baacde6105e45de375f` under MIT; see the repository parity ledger for the exact path and blob.

# Plan a compatible engine setup

This is a setup workflow and may be invoked only explicitly. It never installs,
enables, launches, or reconfigures anything during its inspection and proposal
phases.

1. Run the read-only checks defined by `$ai-game-studio:toolchain-doctor`.
2. Detect existing Unity, Godot, Unreal, browser, and project evidence before
   asking the user to choose an engine.
3. Compare viable engines by project fit, platform export, team language,
   maturity, performance, accessibility, license, install size, and existing
   investment. Verify current terms before relying on them.
4. Recommend one engine and one adapter. Do not activate more than one MCP server
   for the same host application.
5. Produce one transaction containing `plan_id`, environment evidence, exact
   actions, pinned sources, command arguments, downloads, licenses, permissions,
   conflicts, backups, health checks, uninstall and rollback operations, expiry,
   and digest.
6. Show every file that would be materialized, including root and path-scoped
   `AGENTS.md`, selected `.codex/agents/*.toml`, `.ai-game-studio/project.json`,
   and `.ai-game-studio/lock.json`.
7. Wait for explicit confirmation of the exact digest. Applying the transaction
   is a separate operation. Changed evidence, an expired plan, or a digest
   mismatch requires a new plan.

If the preferred route is unavailable on the detected OS, architecture, GPU, or
application version, first attempt a verified native adaptation. Otherwise show
a concise alternative comparison and ask the user to confirm the substitution.

## Codex portability

Use the search, file-editing, shell, user-input, and subagent capabilities available in the active Codex surface. Use PowerShell syntax on Windows and POSIX syntax on macOS/Linux; do not require a Unix compatibility layer on Windows. Inherit the active model and permission mode, and do not weaken approval or sandbox boundaries.
