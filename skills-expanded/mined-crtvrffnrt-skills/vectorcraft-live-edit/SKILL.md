---
name: vectorcraft-live-edit
description: Edit the currently open VectorCraft document through its live MCP connection, including Azure architecture diagrams using the user's local Azure SVG icon library.
---

# VectorCraft live editing

Work in the user's active VectorCraft desktop document. Inspect live state before editing; never assume object IDs, selection, or content from a previous turn. Preserve unrelated artwork and user changes.

## Local context

- Skill directory: the directory containing this file. Resolve bundled scripts relative to it, regardless of the current working directory.
- Desktop app: Flatpak `ai.storyteller.vectorcraft`, running as Linux user `user` (UID 1000).
- Live MCP backend: `127.0.0.1:7979`.
- CLI: `vectorcraft-cli` on PATH; this machine uses `/usr/local/bin/vectorcraft-cli`. Never execute it from `/tmp` or install a symlink pointing there.
- Bundled helper: `scripts/vectorcraft.py TOOL 'JSON_ARGUMENTS'`. It launches the installed CLI in explicit remote mode, initializes MCP, calls one tool, and prints JSON. It exits nonzero on protocol/tool errors or a 60-second timeout. A timed-out mutation may already have applied: inspect state before retrying.
- Last edited document: `/home/user/Downloads/default-1.vectorcraft`, 1920 × 1080. This is context, not a permanent target: confirm the live `path` and title each time.
- Original Azure icons: `/home/user/Documents/Azure_Public_Service_Icons/Icons`. Use these SVG assets rather than drawing substitute icons.

## Persistent installation and reboot checks

Before connecting, run `command -v vectorcraft-cli` and `vectorcraft-cli --help`. Resolve symlinks if needed: the executable must live outside temporary storage. If it is missing, fails to start, or points into `/tmp`, install a copy from the installed Flatpak release. On this machine, query Flatpak as desktop user `user`:

```bash
release_dir=$(runuser -u user -- flatpak info --show-location ai.storyteller.vectorcraft)
test -n "$release_dir" && test -x "$release_dir/files/bin/vectorcraft-cli"
# Run only after the checks above succeed; writing /usr/local/bin requires root.
install -m 0755 "$release_dir/files/bin/vectorcraft-cli" /usr/local/bin/vectorcraft-cli
vectorcraft-cli --help
```

When already running as the desktop user, omit `runuser -u user --`. For a user-only installation, use `$HOME/.local/bin/vectorcraft-cli` and ensure `$HOME/.local/bin` is on that user's persistent shell PATH. Never hardcode a Flatpak deployment hash or use `/proc` as the installed executable. Copy the binary rather than linking to temporary storage. If the app is not installed, install the official VectorCraft release first; do not download an arbitrary binary. Refresh the copied CLI after updating the desktop app if connection/schema compatibility changes.

Keep this skill and its bundled helper in persistent storage. Examples below use paths relative to the skill directory; invoke the helper by absolute path when working elsewhere. Python 3 is required; the helper uses only its standard library.

After a reboot, the CLI remains installed, but the app/control server may not be running. Check the listener and follow the connection recovery section before calling tools. Do not create a background service or restart the desktop app without considering unsaved work.

## Connect and discover

Start with:

```bash
python3 scripts/vectorcraft.py inspect_document '{"depth":1}'
python3 scripts/vectorcraft.py inspect_ui '{}'
```

`inspect_document` reports the active path, revision, dirty state, artboards, selection, object IDs, and layer tree. Drill into specific IDs or use `command_run` with `document.find` / `document.node` instead of repeatedly dumping the full document.

The MCP stdio command is:

```bash
vectorcraft-cli mcp --connect 127.0.0.1:7979
```

Always use `--connect`: omitting it can silently fall back to a separate headless document. Use MCP `tools/list` for current schemas. Discover schemas from the live server; do not depend on a cached catalogue in temporary storage.

For command discovery:

```bash
python3 scripts/vectorcraft.py command_list '{"filter":"object.scale"}'
python3 scripts/vectorcraft.py command_run '{"id":"document.node","params":{"id":123,"summary":true}}'
```

Do not guess command names or parameters. A command can return a tool error without terminating the helper.

## If the connection is unavailable

Check `pgrep -x vectorcraft` and `ss -ltnp`. VectorCraft's random loopback single-instance launch port is not its control server. The control server requires `--control 7979` at startup; it cannot be assumed to attach retroactively to an existing window.

If the CLI is missing, use the persistent installation section above. Discover the current Flatpak deployment rather than relying on a running process or an old process ID.

For a controlled Flatpak launch, run as `user` with the actual desktop environment (`DISPLAY`, `WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `DBUS_SESSION_BUS_ADDRESS`, and `XAUTHORITY` when present). Read only these named values from an existing desktop process; do not print its entire environment. User runtime is `/run/user/1000`. A representative launch is:

```bash
flatpak run --filesystem=/home/user/Downloads ai.storyteller.vectorcraft --control 7979 /home/user/Downloads/default-1.vectorcraft
```

Execute that in the user's desktop session, not as root with missing display variables. Flatpak hides Documents and Downloads by default. Grant only the folders needed for the task. Inline SVG imports avoid needing to expose the icon library to the app.

Do not kill or restart a window containing unsaved work. A separate controlled window reads the saved file and does not include another window's unsaved changes. Explain that limitation if a new window is necessary. Wait for the control listener, then verify the document path before editing. Do not keep retrying failed mutation calls without checking state.

## Use the local Azure SVGs

Find matches with `rg --files` under the icon root. Known paths relative to `Icons`:

| Service | SVG |
|---|---|
| App Service | `web/10035-icon-service-App-Services.svg` |
| Azure Functions | `compute/10029-icon-service-Function-Apps.svg` |
| Managed Redis | `databases/03675-icon-service-Azure-Managed-Redis.svg` |
| Azure SQL Database | `databases/10130-icon-service-SQL-Database.svg` |
| Private endpoint | `other/02579-icon-service-Private-Endpoints.svg` |
| Virtual network | `networking/10061-icon-service-Virtual-Networks.svg` |
| Azure Monitor | `monitor/00001-icon-service-Monitor.svg` |
| Browser/client | `general/10783-icon-service-Browser.svg` |

Import an SVG through `command_run` → `clipboard.importSvg`, params `{svg: "<svg…>", center: [x,y]}`, then `edit.pasteInPlace`. Pass SVG contents as structured JSON from Python, not shell interpolation. This imports editable vector objects, not a screenshot. Read the returned IDs and inspect their bounds before moving or scaling them.

`object.scale` takes percentages: `{ids:[...], sx:145, sy:145, origin:[960,540], strokes:true}`. Never reuse IDs from past imports. Preserve each icon's aspect ratio and keep its original gradients and colors.

When combining SVGs, give every asset's gradient, clip, and mask IDs unique prefixes and update their references. Nested SVG viewBoxes can place each asset into a target rectangle. Preserve text-containing groups when replacing icon geometry: service labels can be nested inside the same group as the icon. Do not delete those groups just because they contain graphics.

## Editing safely

- Prefer replacing individual icon objects in the live document. Preserve surrounding text, connectors, and user additions.
- Whole-diagram replacement is appropriate only when requested or when the target is known to contain only the diagram being replaced. `select.all` plus `edit.clear` affects user additions too; do not use it for an icon-only change.
- Inspect the latest revision immediately before a broad mutation. If content changes while working, re-read it and adapt.
- For a full replacement, stage and validate import data before removing the old content. Keep a backup of the saved file; a disk backup does not preserve unsaved live edits.
- Use native tools (`draw_path`, `draw_shape`, `text.create`, `set_paint`) for vector edits. Use actual library icons for Azure services.
- If old scripts such as `replace-diagram.py`, `replace-local.py`, or `use-local-icons.py` are encountered, treat them as one-off reconstruction scripts. Do not rerun them for routine edits: they clear artwork and reconstruct an older snapshot.

## Verify and save

Call `render_preview` with `{max_side:1600}`. Its result includes an image content block: decode its base64 data to a local PNG and inspect it with `view_image`. Verify labels, connections, icon proportions, clipping, and legibility. Check the latest document path and dirty state.

Save the current document with `save_file {}` after the requested edit is complete, unless the user requests an unsaved preview. Confirm `isError:false`, the intended output path, and any warnings. Report the change and save result concisely. Do not claim native MCP tool registration merely because the shell helper works.

## Documentation

Consult current schemas and these upstream references when needed:

- https://github.com/storytold/vectorcraft/blob/main/docs/mcp.md
- https://github.com/storytold/vectorcraft/blob/main/docs/control-protocol.md

The existing Azure diagram came from Microsoft's published SVG, then its service icons were replaced with assets from the local library. Its reference architecture is https://learn.microsoft.com/en-us/azure/architecture/databases/architecture/write-through-caching-azure-sql-managed-redis . Do not substitute this architecture when the user requests another diagram.

