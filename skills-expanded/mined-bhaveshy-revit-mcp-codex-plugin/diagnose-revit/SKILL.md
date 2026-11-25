---
name: diagnose-revit
description: Diagnose Windows 11 Revit MCP Next connection, launcher, add-in, queue, preview-token, or client failures. Use when Revit tools are missing, revit.status fails, requests time out, the bridge is unavailable, or preview/apply reports stale state.
---

# Diagnose Revit MCP Next

Start with `revit.status`. Inspect its structured diagnostics before retrying:

Require native Windows 11 with Revit 2024. Treat macOS, Linux, WSL, remote
containers, and cross-machine bridge layouts as unsupported.

- active document fingerprint and generation
- bridge/add-in versions and protocol compatibility
- queue depth and ExternalEvent state
- preview-token counts and recovery hints

Use the installed support CLI only for diagnosis:

```powershell
cmd /c "%LOCALAPPDATA%\RevitMcpNext\revitctl.cmd" doctor --pretty
```

If the install checkout is available, also run:

```powershell
npm run doctor:windows
npm run doctor:clients -- -Client codex
```

Interpret common failures:

- `BRIDGE_UNAVAILABLE`: open Revit 2024 and a project; confirm the add-in loaded.
- `PROTOCOL_VERSION_MISMATCH`: rebuild/reinstall the broker and add-in together.
- `REVIT_EXTERNAL_EVENT_TIMEOUT`: close ordinary Revit dialogs, bring Revit
  forward, wait for idle, and retry once.
- generation/document mismatch: refresh bounded reads and rebuild the preview.
- missing/expired/used preview: preview again; never reuse or fabricate tokens.
- `LAUNCHER_NOT_FOUND`: verify the existing Revit MCP Next installation and
  set `REVIT_MCP_NEXT_LAUNCHER` or `REVIT_MCP_NEXT_INSTALL_ROOT` when it uses a
  non-default location. Do not install or rebuild it automatically.

Do not expose auth files in logs or support output. Do not blindly retry a
mutation after timeout or unknown commit state; stabilize the bridge and verify
with read-only tools first.
