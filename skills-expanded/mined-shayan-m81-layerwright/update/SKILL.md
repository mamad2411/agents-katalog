---
name: update
description: Update Layerwright on this computer when a newer version is out - the Figma plugin, the /layer commands and the MCP server they run. Use for /layer:update, when the user asks to update Layerwright, or when a request from the Figma window asks for it.
---

# Update Layerwright

1. `layerwright_update()`: the version this session runs, the newest one on npm, and the command.
2. Up to date → say so in one line and stop. npm couldn't be reached → say so; the user can try again later.
3. A newer one is out → one line: "Layerwright <current> → <latest>". Ask before running it (AskUserQuestion when you have it: Update now / Not now), unless this came from the Update button in the Figma window: pressing it was their OK.
4. Run the command it gives in the terminal: `npx -y layerwright@latest update` (any folder; the first run downloads the new version, so it can take a minute). Show the user its ✓ / ✗ lines. No terminal in this client → give them the command to run themselves.
5. Tell them what's left, as its "Next" lines say: in Claude Code, type `/reload-plugins` in each open session (this one too), or start a new one; in the desktop app or Codex, a new session; in Figma, close and reopen the Layerwright plugin. The newer version takes over the shared Figma connection by itself.
6. From the Figma window → `figma_reply({ id, status: "done", message })` with one line: the version now and what's left. A ✗ line → `status: "failed"` with it.
