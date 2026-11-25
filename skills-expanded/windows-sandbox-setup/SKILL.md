---
name: windows-sandbox-setup
description: Get Windows Sandbox ready for sandbox-mcp CLI or MCP workflows. Use when sbx or a sandbox tool says "Windows Sandbox isn't ready", when a sandbox is already running and blocks a new one, or before first use.
---

# Set up Windows Sandbox

Windows Sandbox runs only on **Windows 11 24H2 or later, Pro, Enterprise or Education**. Home and Server editions can't run it, and neither can macOS or Linux hosts. The agent must run on that Windows PC itself.

If shell access is available, use the `sbx` CLI; the optional MCP adapter uses the same engine and is not required.

## Check the PC

Run the read-only check. It never enables features, elevates or restarts anything.

```powershell
sbx doctor
```

If `sbx` isn't on PATH, use the portable ZIP's `.\sbx.cmd` (no Node.js install required). With Node.js and npm,
you can also run the one-off check without installing the plugin:

```powershell
npx --yes --package=github:shanselman/sandbox-mcp sbx doctor
```

To install the portable package with its bundled Node.js and verified download, follow [the agent setup guide](https://raw.githubusercontent.com/shanselman/sandbox-mcp/main/docs/agent-setup.md). It asks before admin changes or a restart.

Exit code 0 means ready. Exit code 1 lists each problem with its `Fix:` line; add `--json` for structured output.
`sbx start` and `sbx run` report the same readiness checks as `sandbox_start` and the one-shot MCP tools.

## Fix what it reports

Pass the fixes to the user, in order. They usually need an administrator and a restart, so don't run them yourself or try to work around them.

- **Sandbox feature off:** in an administrator PowerShell, run `Enable-WindowsOptionalFeature -Online -FeatureName Containers-DisposableClientVM -All`, then restart Windows.
- **`wsb` tool missing:** open Windows Sandbox from the Start menu once, then close it. It updates itself from the Microsoft Store, which adds `wsb`.
- **Virtualization off:** turn on Intel VT-x or AMD-V in UEFI/BIOS. Inside a VM, the host must enable nested virtualization.
- **Node.js too old:** `winget install OpenJS.NodeJS.LTS --source winget`, then restart the agent so it sees the new PATH.
- **Home or Server edition:** there is no fix short of a different Windows edition. Tell the user and stop.

## Confirm it works

With shell access, run `sbx run C:\Windows\System32\charmap.exe --network off`. Otherwise, call
`sandbox_run` with `app: "C:\\Windows\\System32\\charmap.exe"` and `network: "off"`. It should report PASS in under a minute.

## If you chose MCP and its tools don't appear

This only affects the optional MCP interface; the CLI remains usable. The plugin starts the server with
`cmd /d /c npx --yes github:shanselman/sandbox-mcp#<version>`, which needs Node.js 20 or later on PATH and
network access for the first download. Run that command in a terminal to see the error; a working server logs
`ready` to stderr and then waits on stdin. Press Ctrl+C to stop it.

## If a sandbox is already running

Windows allows one sandbox at a time. Check with `sbx status` or `sandbox_status`. Stop only a guest you own,
with `sbx stop` or `sandbox_stop`. If you don't own it, it may hold someone's work, so ask its owner or the user
rather than interrupting it. Only with their approval, use the force option.

## Settings

Set these in the shell environment for `sbx`, or in the MCP server environment when using that adapter:

| Variable | Default | Purpose |
|---|---|---|
| `SANDBOX_MCP_HOME` | `%LOCALAPPDATA%\sandbox-mcp` | Where runs, screenshots and reports are kept |
| `SANDBOX_MCP_ALLOWED_ROOTS` | any folder | `;`-separated host folders that may be copied in |
| `SANDBOX_MCP_IDLE_MINUTES` | `30` | Guest shuts down after this long idle; `0` disables |
| `SANDBOX_MCP_KEEP_ON_EXIT` | unset | `1` leaves the sandbox running when the client disconnects |
