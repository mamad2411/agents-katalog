---
name: macos13-computer-use
description: Use the locally installed macOS 13 Computer Use backend for desktop-app inspection and control on this machine, including sessions with an alternative CODEX_HOME.
---

Use the configured **`computer-use` MCP server** for desktop work on macOS 13.
It launches the custom signed native backend directly from the Codex host,
where the existing Accessibility and Screen Recording permissions are usable.
Discover its current tools and follow their input schemas; native MCP inputs
can differ from the `sky` JavaScript facade.

The canonical backend remains under
`~/.codex/computer-use-macos13/Codex Computer Use for macOS 13.app` in every
Codex home. Keep this path and signed bundle stable during plugin maintenance.
The source checkouts are `codex-computer-use-ventura` for the bridge and
`open-codex-ventura` for the native backend.

New Unified Computer Use workers connect to this backend through a private
local broker. On this installation the direct MCP wrapper starts the broker
under the Codex host and checks its existing desktop permissions. If Unified
reports denied access or has retained its previous worker settings, use the
direct native MCP tools. Browser tools keep their normal browser runtime.

When a desktop operation requires checking native access, `doctor` with
`prompt: false` reports permissions without requesting settings changes.
Treat missing native access as a real limit; this skill does not authorize
changing privacy grants, re-signing the app, or launching the official
macOS-14.4-dependent Sky service on Ventura.
