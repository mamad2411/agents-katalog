---
name: setup-blender
description: Inspect Blender and a game project, then propose the pinned local Blender MCP adapter with permissions, addon steps, health checks, and rollback. Use for Blender-assisted 3D generation or animation; never install the addon or server before digest confirmation.
---

# Set up Blender

Run the core doctor and inspect Blender/Python versions, OS/architecture, `uv` availability, existing Blender MCP configuration, project asset paths, GPU backend, disk/network needs, and uncommitted work.

The supported adapter is MIT-licensed `ahujasid/blender-mcp` at the immutable descriptor commit. Explain that the Blender addon accepts local socket commands and the server can execute Python in Blender, so it requires high trust and localhost-only networking.

Use `pack plan blender --project <root> --output <plan.json>`. If using an already installed server executable, require its absolute path and matching SHA-256. Present the addon/server downloads, license, Python pin, filesystem/network/process permissions, backups, expiry, rollback operations, and digest. Wait for verbatim confirmation before apply. Finish with `pack doctor`; ask before launching Blender, installing an addon, or running a scene-changing health check.

Keep one Blender MCP host active. Preserve original `.blend` and source assets and use separate before/after files for generated or enhanced results.
