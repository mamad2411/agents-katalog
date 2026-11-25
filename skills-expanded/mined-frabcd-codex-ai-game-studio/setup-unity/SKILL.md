---
name: setup-unity
description: Inspect a Unity project and propose one compatible local Unity MCP adapter with exact pins, permissions, health checks, and rollback. Use for Unity editor automation setup or adapter replacement; never install or activate a server before digest confirmation.
---

# Set up Unity

Use the core doctor first. Confirm `ProjectSettings/ProjectVersion.txt`, Unity/Hub availability, OS/architecture, Python or Node requirements, existing Unity MCP servers, disk/network needs, and uncommitted files.

Default to `CoplayDev/unity-mcp` at the descriptor's immutable commit and MIT license. Choose `IvanMurzak/Unity-MCP` only when checked-in descriptor or doctor evidence shows that it satisfies a stated project requirement the default cannot; present that evidence. Otherwise use the default. Exactly one Unity MCP may be selected.

Run `pack plan unity --project <root> --output <plan.json>`. Select the alternative only with `--provider IvanMurzak/Unity-MCP`. If a verified local server executable already exists, add `--server-executable <absolute-path> --server-sha256 <sha256>`; never accept a relative or hash-mismatched executable. Present downloads, licenses, permissions, actions, backups, expiry, rollback, and digest. Wait for the user to repeat the displayed digest verbatim. Apply with `pack apply --project <root> --plan <plan.json> --confirmed-digest <digest>` and finish with `pack doctor` plus a read-only Unity version/connection health check.

If another Unity host selection is active, use `--replace` only after comparing capability, quality, cost, performance, security, and limitations. Rollback is always a separately confirmed transaction.

Do not invoke this skill for version-only or other metadata-only questions. Read only the requested project metadata and do not create an adapter plan.
