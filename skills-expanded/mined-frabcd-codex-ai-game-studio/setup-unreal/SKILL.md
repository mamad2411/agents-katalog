---
name: setup-unreal
description: Inspect an Unreal Engine project and propose one compatible local Unreal MCP adapter with exact pins, high-risk permissions, health checks, and rollback. Use for Unreal editor automation setup; require digest confirmation before any plugin or server change.
---

# Set up Unreal Engine

Run the core doctor. Inspect the `.uproject`, engine association, source versus Blueprint project, installed editor/toolchain, OS/architecture, GPU-backed screenshot capability, disk needs, current plugins, and existing Unreal MCP host.

Default to Apache-2.0 `IvanMurzak/Unreal-MCP` at the immutable descriptor commit. `GenOrca/unreal-mcp` is the selectable alternative. Explain that editor control can execute console commands, reflection calls, Python, and project writes; it is high-trust local automation and must not ship enabled in a production game.

Create `pack plan unreal --project <root> --output <plan.json>`. Select the alternative only with `--provider GenOrca/unreal-mcp`. Configure a local server executable only by absolute path plus verified SHA-256. Present exact actions, large/plugin downloads, licenses, permissions and RCE-class risks, backups, expiry, rollback operations, and digest. Wait for the user to repeat the displayed digest verbatim. Apply only with `pack apply --project <root> --plan <plan.json> --confirmed-digest <digest>`. Verify with `pack doctor`, plugin load evidence, and a read-only ping; do not open or mutate the editor merely to prove setup.

Only one Unreal MCP may be active. Adapter replacement and rollback each require their own confirmed plans.
