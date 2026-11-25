---
name: setup-godot
description: Inspect a Godot project and propose one compatible local Godot MCP adapter with exact pins, permissions, health checks, and rollback. Use for Godot editor automation setup or adapter replacement; never install or activate a server before digest confirmation.
---

# Set up Godot

Run the core doctor and inspect `project.godot`, Godot version/path, OS/architecture, Node requirements, existing Godot MCP servers, credentials by variable name only, and current worktree state.

Default to MIT-licensed `Coding-Solo/godot-mcp` at the immutable descriptor commit. Offer Apache-2.0 `IvanMurzak/Godot-MCP` only after a verified comparison. Never activate both for the Godot host.

Create a proposal with `pack plan godot --project <root> --output <plan.json>`. Select the alternative only with `--provider IvanMurzak/Godot-MCP`. A preinstalled server may be selected only with an absolute path and matching `--server-sha256`. Show exact actions, expected downloads, license and commercial implications, permissions, backups, expiry, rollback operations, and digest. Wait for confirmation, then use `pack apply ... --confirmed-digest <digest>`. Finish with `pack doctor` and a non-mutating Godot connection/version check.

Use `--replace` only when the proposal names the current adapter and explains the substitution. Any rollback requires its own proposal and confirmation.
