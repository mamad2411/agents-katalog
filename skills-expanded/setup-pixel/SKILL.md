---
name: setup-pixel
description: Inspect a 2D game project and propose the pinned pixel-art MCP adapter or documented non-MCP editor alternatives. Use for Aseprite-based sprite automation; require digest confirmation before activating tools or changing assets.
---

# Set up pixel-art tooling

Run the core doctor and inspect the engine, sprite and tileset formats, Aseprite/Pixelorama/Tiled availability, OS/architecture, existing pixel MCP host, output paths, and current worktree state.

The MCP option is MIT-licensed `willibrandon/pixel-mcp` at the immutable descriptor commit and requires an existing Aseprite-compatible executable workflow. Pixelorama and Tiled are non-MCP alternatives: compare them when Aseprite is unavailable, licensing or cost matters, or direct automation is unnecessary. Do not present non-MCP editors as active MCP servers.

Create `pack plan pixel --project <root> --output <plan.json>`. A local server executable requires an absolute path and matching SHA-256. Show exact actions, downloads, licenses, permissions, backups, expiry, rollback, and digest; wait for confirmation before apply. Finish with `pack doctor` and a read-only capability check.

Generated sprites stay separate from source art until transparency, dimensions, pivot/baseline, palette, loop continuity, engine import, and human visual review pass. Only one pixel/Aseprite MCP host may be active.
