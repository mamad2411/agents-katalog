---
name: multi-instance-electron-dev
description: Run multiple independent dev instances of the same Electron app on one machine by deriving port, config dir, app name, and deep-link scheme from a numeric suffix on the project folder name.
category: electron
version: 1.0.0
version_origin: extracted
tags: [electron, dev, multi-instance, deep-links]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/lukilabs/craft-agents-oss.git
source_ref: main
source_commit: 61f7d48a5b4fd0a8094f002c9e3aea5f3824dcfb
source_project: craft-agents-oss
source_path: scripts/electron-dev.ts
imported_at: 2026-04-18T00:00:00Z
---

# Multi-instance Electron dev

## When to use
- Testing migrations / upgrades where you need "old version" and "new version" running side-by-side.
- Agent app where you want two independent workspaces without data cross-contamination.
- Deep links (custom URL scheme) need to route to the right instance.

## How it works
1. Clone the repo into folders like `craft-agents-1/`, `craft-agents-2/` (or any name ending `-N`).
2. Dev script parses `basename(ROOT_DIR).match(/-(\d+)$/)`. If matches:
   - `CRAFT_VITE_PORT = ${N}173` (e.g. `1173`, `2173`).
   - `CRAFT_CONFIG_DIR = ~/.craft-agent-${N}` - entirely separate config + credentials + sessions.
   - `CRAFT_APP_NAME = "Craft Agents [${N}]"` - shown in macOS menu bar / dock.
   - `CRAFT_DEEPLINK_SCHEME = "craftagents${N}"` - `craftagents1://`, `craftagents2://`, etc.
3. Electron main reads these env vars and uses them for `app.setName()`, config path, and `app.setAsDefaultProtocolClient(scheme)`.
4. Renderer Vite config binds to `CRAFT_VITE_PORT`; `--strictPort` so it fails rather than silently collides.

## Example
```ts
const folderName = basename(ROOT_DIR);
const match = folderName.match(/-(\d+)$/);
if (match) {
  const n = match[1];
  process.env.CRAFT_INSTANCE_NUMBER = n;
  process.env.CRAFT_VITE_PORT = `${n}173`;
  process.env.CRAFT_APP_NAME = `Craft Agents [${n}]`;
  process.env.CRAFT_CONFIG_DIR = join(process.env.HOME, `.craft-agent-${n}`);
  process.env.CRAFT_DEEPLINK_SCHEME = `craftagents${n}`;
}
```

```ts
// apps/electron/src/main/index.ts
app.setName(process.env.CRAFT_APP_NAME || 'Craft Agents');
const DEEPLINK_SCHEME = process.env.CRAFT_DEEPLINK_SCHEME || 'craftagents';
app.setAsDefaultProtocolClient(DEEPLINK_SCHEME);
```

## Gotchas
- Config dir is the most important isolation - if you share `~/.craft-agent`, two instances will corrupt each other's session files with race writes.
- Deep link schemes MUST be unique or the OS routes all `craftagents://` URLs to whichever instance claimed it first.
- Users won't guess the folder-suffix naming - document it. Or use an explicit `CRAFT_INSTANCE=N` env as an alternative path.
- App name is visible to the user (dock, menu bar); make it scannable at a glance.
- Bun's `basename()` on Windows uses backslash-aware path parsing - not an issue but worth testing.
