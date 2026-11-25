---
name: setup
description: Install the Browser Bridge extension into Chrome or Brave
user_invocable: true
---

# Browser Bridge — Setup

This is a delegating stub. The full install + setup flow lives at one canonical URL so it stays in sync across direct paste-from-the-web installs and `/claude-browser-bridge:setup` invocations from inside an existing Claude session.

## What to do

1. Fetch the canonical install document:

   ```bash
   curl -fsS https://browser-bridge.softwaresoftware.dev/install.txt
   ```

2. Follow every phase in order. That document is the operator script for end-to-end setup: rules, marketplace bootstrap, plugin + daemon install, loading the extension (the one manual step), an end-to-end verification with `list_tabs`, and hand-off.

3. If `install.txt` is unreachable (network down, the static site is being redeployed, etc.), fall back to the steps below — the same flow, condensed. install.txt is the source of truth when reachable.

## Why this is a stub

The install flow exists in one place — `install.txt` at the URL above — so that:

- A user on a fresh machine pastes the URL into Claude Code and gets the same flow
- A user already inside a Claude session can run `/claude-browser-bridge:setup` and get the same flow
- The flow updates in one place; no drift between two copies

When operating from this skill, you ARE the install agent install.txt addresses in second person. Read it, then act.

## Fallback (only if install.txt is unreachable)

The plugin is already installed if you're running this skill, so skip the marketplace/install phases and go straight to the extension load:

1. **Resolve the extension path** and confirm it exists. The extension ships with this plugin at `${CLAUDE_PLUGIN_ROOT}/extension/`. Confirm `${CLAUDE_PLUGIN_ROOT}/extension/manifest.json` is present, and print the path — the user pastes it into the browser's file picker.

2. **Detect the browser** (`which brave-browser brave google-chrome chromium-browser microsoft-edge`) or ask which they use.

3. **Print browser-specific steps:**
   - Brave: open `brave://extensions` → enable Developer mode (top-right) → Load unpacked → select the path → the "Browser Bridge" card shows a green **ON** badge when connected.
   - Chrome: same, at `chrome://extensions`.
   - Edge: same, at `edge://extensions` (Developer mode toggle is bottom-left).

4. **Verify end to end.** The daemon auto-starts on the first browser tool call (a PreToolUse hook), so don't start it by hand — just call `list_tabs`. If it returns tabs, the bridge works. If you get "Browser extension not connected", the extension isn't loaded or the browser is closed — send the user back to step 3 and confirm the ON badge. For daemon trouble, check `daemon_status` for `claude-browser-bridge`.

5. **Make the daemon persistent.** The lazy hook has no boot-persistence or crash-restart. Hand the daemon to the OS service manager via `daemon_install_autostart` with `daemon_name: claude-browser-bridge`, `command: node`, `args: ["dist/daemon.cjs"]`, and `cwd` set to the plugin root (the directory holding `dist/daemon.cjs` — `${CLAUDE_PLUGIN_ROOT}`). It writes and loads a systemd unit (Linux), launchd plist (macOS), or Scheduled Task (Windows). No per-OS pidfile wiring is needed — the daemon writes its own pidfile (`~/.claude/daemons/claude-browser-bridge.pid`) on startup, so the bundled hook defers to the managed daemon instead of spawning a duplicate, identically across platforms. Confirm `daemon_status` shows `running: true`, then call `list_tabs` once more (it also fires the hook, proving it defers to the managed daemon instead of double-spawning).

6. **Hand off.** Tell the user the bridge is live and they can now ask for browser tasks in plain language.
