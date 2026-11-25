---
name: revit-setup
description: Install, check, repair, update or uninstall revit-mcp-next (the Revit MCP server and Revit add-in) on a Windows PC for Codex or Claude Code. Use for first-time setup on a new PC, "MCP unavailable" or revit tools missing, the revit server failing to start, NO_REVIT_RUNNING although Revit is open, the add-in not loading, ADDIN_OUTDATED, ADDIN_NEWER_THAN_BROKER, AUTH_MISMATCH, BRIDGE_ACCESS_DENIED, running the doctor, collecting a support bundle, and run_csharp questions.
---

# Setting up revit-mcp-next

revit-mcp-next has two parts: a Revit add-in (Revit 2024 and/or 2027) and an MCP server (`revit`) that Codex or Claude Code starts. Both live in one folder, the **home**: `%USERPROFILE%\.revit-mcp-next`, or the folder in the `REVIT_MCP_NEXT_HOME` environment variable.

For using Revit once the tools work, follow the `revit` skill.

## Safety rules for setup

- Installing, repairing and uninstalling change the user's machine: files in the home, the Codex config (`~\.codex\config.toml`), the Claude Code user config, `~\.codex\AGENTS.md`, and the Revit add-in manifests in `%APPDATA%\Autodesk\Revit\Addins\<year>\`. Explain what will change and get the user's OK first. Run `-DryRun` first and show the user its output.
- Run the installer from a normal Windows PowerShell window, not from inside the Codex desktop app or another AI app. If you cannot, give the user the exact command to run.
- Never start, stop or kill Revit yourself, and never use screen automation on Revit. Ask the user to close or start Revit.
- Never edit `<home>\config\settings.json` to enable code execution (`run_csharp`). Only the user does that.
- Never install into `%LOCALAPPDATA%`, `%APPDATA%`, `%TEMP%` or a `WindowsApps` folder: the installer refuses these.

## Folder layout (home)

```
<home>\runtime\node.exe                 Node runtime used by the MCP server
<home>\broker\revit-mcp.mjs             the MCP server (what Codex/Claude start)
<home>\broker\revit-mcp-cli.mjs         command line: doctor, clients, support
<home>\addin\<year>\...                 add-in loader and payload per Revit year
<home>\config\settings.json             settings (edited only by the user)
<home>\config\auth.env                  shared token for server and add-in
<home>\instances\                       one file per running Revit with the add-in
<home>\logs\                            broker-*.jsonl, addin-<year>-*.jsonl, loader-<year>.log, install-*.log
%APPDATA%\Autodesk\Revit\Addins\<year>\RevitMcpNext.addin   manifest, points at the loader
```

The doctor command used below (PowerShell):

```powershell
& "$env:USERPROFILE\.revit-mcp-next\runtime\node.exe" "$env:USERPROFILE\.revit-mcp-next\broker\revit-mcp-cli.mjs" doctor
```

If the home is elsewhere, replace `$env:USERPROFILE\.revit-mcp-next` with it. `doctor --quick` skips the slow checks. Each problem line comes with what to do; follow it.

## Fresh install on a new PC

Requirements: Windows 10 or 11; Revit 2024 and/or 2027 installed and licensed; Codex (CLI or desktop) and/or Claude Code installed; the same Windows user runs Revit and the AI app, neither elevated (not "Run as administrator").

1. The user downloads the revit-mcp-next release package (zip) and extracts it to a normal folder, for example `C:\Tools\revit-mcp-next`. Do not run anything from inside a download or temp folder.
2. Ask the user to close every Revit window (save their work first).
3. In a normal PowerShell window in the extracted folder, preview the install:
   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File .\installer\install.ps1 -DryRun
   ```
   Show the user the summary: home folder, Revit years found, Codex and Claude registration, AGENTS.md edit, conflicts found.
4. After the user agrees, install (same command without `-DryRun`). Optional switches, only when the user wants them:
   - `-DisableConflictingPlugins`: turns off other Revit plugins that conflict (for example revit-mcp-cowork in Codex). While revit-mcp-cowork stays enabled in Claude Code, its hook auto-approves our destructive tools; tell the user.
   - `-TrustRevitAlwaysLoad`: pre-trusts the add-in so Revit does not ask "Always Load" on first start.
   - `-NoAgentsSnippet`: do not add the Revit rule to `~\.codex\AGENTS.md`.
   - `-RemoveLegacy`: remove old revit-mcp-next installs that the installer reports.
   - `-Json`: machine-readable summary.
5. Restart the AI app so it loads the `revit` server:
   - Codex: start a new thread; for the desktop app, quit and reopen it. Check with `codex mcp list` (shows `revit`) or `codex mcp get revit --json`.
   - Claude Code: restart it, then `/mcp` should show `revit` connected. Check with `claude mcp list`.
6. Ask the user to start Revit and open a model. On the first start Revit may ask whether to load the add-in: the user chooses "Always Load".
7. Run the doctor (command above). All lines should pass.
8. In the chat, call `status {}` (the `revit` skill). It should list the Revit version and the open document.

## Problems and fixes

| Symptom | What to do |
|---|---|
| No `revit` tools in the chat ("MCP unavailable") | Restart the thread or app (step 5). Still missing: run the doctor and follow its lines; check `codex mcp get revit --json` or `claude mcp list`. Not installed: fresh install. |
| The `revit` server fails to start or times out at startup | Run the doctor. Usually `runtime\node.exe` or `broker\revit-mcp.mjs` is missing (re-run the installer) or the config points at an old home (re-run the installer; it rewrites the `revit` entry). |
| `status` says no Revit with the add-in is running, but Revit is open | The add-in did not load. Ask the user: is there an "Always Load" prompt or an add-in error at Revit start? Then check `<home>\logs\loader-<year>.log` and the manifest `%APPDATA%\Autodesk\Revit\Addins\<year>\RevitMcpNext.addin`. Re-run the installer (with `-TrustRevitAlwaysLoad` if the user wants), then the user restarts Revit. |
| ADDIN_OUTDATED | The running add-in is older than the server: the user restarts Revit so it loads the installed add-in. |
| ADDIN_NEWER_THAN_BROKER | Re-run the installer, then start a new chat thread. |
| AUTH_MISMATCH or AUTH_NOT_CONFIGURED | Re-run the installer (it keeps one token in `config\auth.env`), or the user restarts Revit. |
| BRIDGE_ACCESS_DENIED | Revit and the AI app run as different users or one is elevated: run both as the same normal user. |
| ADDIN_PIPE_MISSING or REVIT_EXITED right after start | The user restarts Revit. If it repeats, collect a support bundle (below). |
| Two installs fight (old LocalCache or `%LOCALAPPDATA%\RevitMcpNext` folders) | Re-run the installer with `-RemoveLegacy` after the user agrees. |
| Revit-cowork tools (`say_hello`, `send_code_to_revit`...) appear next to `revit` | They belong to another plugin. Do not use them. Offer `-DisableConflictingPlugins` (Codex) or disabling that plugin in Claude Code. |
| `run_csharp` is not in the tool list | That is the default: C# execution is off. Only the user can enable it (installer switch or their own edit of `settings.json`), then start a new thread. Never enable it yourself. |

## Support bundle

```powershell
& "$env:USERPROFILE\.revit-mcp-next\runtime\node.exe" "$env:USERPROFILE\.revit-mcp-next\broker\revit-mcp-cli.mjs" support
```
It gathers the logs and checks needed for a bug report and prints where it saved them. Ask the user before sending it to anyone; it can contain model and file names.

## Update to a new release

1. The user closes Revit.
2. Extract the new package and run `installer\install.ps1` from it (with `-DryRun` first). It replaces the server and add-in in the same home and keeps settings and the token.
3. Restart the AI app (new thread) and Revit. Run the doctor.

## Uninstall

The user closes Revit, then in the package folder:
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\installer\uninstall.ps1 -DryRun
```
Show the summary, and after the user agrees run it without `-DryRun`. It removes the `revit` entries, the skills plugin and the AGENTS.md block from the Codex and Claude configs (re-enabling a plugin the installer disabled), the Revit manifests and trust entries it added, and the runtime, server and add-in files; `config` and `logs` stay. `-Purge` deletes the whole home instead. Then restart the AI app.
