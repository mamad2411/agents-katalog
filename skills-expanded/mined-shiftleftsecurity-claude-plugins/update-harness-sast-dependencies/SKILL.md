---
name: update-harness-sast-dependencies
description: Install or update Harness SAST and SCA engine dependencies (analyzers and dependency tooling). Use when the user asks to update the security tools, install missing dependencies, or check for updates.
---

# Update Harness SAST and SCA dependencies

Use this when the user wants to **install** analysis dependencies (first-time, ~400MB) or **update** them to the latest version.

## What happens

- Nothing installed yet: downloads and installs dependencies, then reports success.
- Installed but an update exists: installs the update and reports success.
- Already up to date: reports the current version.

## Claude Code plugin

If the user is using the **Harness SAST and SCA** plugin with Claude Code, run the bundled update script and show the output:

```bash
node "${CLAUDE_PLUGIN_ROOT}/handlers/update-handler.js"
```

If **`CLAUDE_PLUGIN_ROOT`** is not set, use the plugin directory the user actually loaded with **`claude --plugin-dir`**, for example:

```bash
node "/path/to/plugin/handlers/update-handler.js"
```

Some installs use a default under **`$HOME/.claude/plugins/`**; only use that if it matches how the user installed the plugin.

## Devin

### Devin CLI

Use the **Devin** release artifact (`release/curness-devin-plugin/`), not the Claude plugin. Add its path to **`plugin_dirs`** in `~/.config/devin/config.json` (or **`/config`** in Devin), then run the update handler:

```bash
node "/path/to/curness-devin-plugin/handlers/update-handler.js"
```

This installs analysis dependencies (if missing) and merges hooks into **`~/.config/devin/config.json`** with absolute handler paths. Run **`install-harness-sast-devin-hooks.js`** from the same directory if you only need the hook merge. Start a **new** `devin` session after the first install so hooks and MCP load.

### Devin Desktop (Devin Local)

If the user runs **Devin Local** in Devin Desktop with the Curness VSIX, hooks are registered automatically into the same **`~/.config/devin/config.json`**. Run **`node "/path/to/curness-devin-plugin/handlers/update-handler.js"`** only when they also use **`plugin_dirs`** for cloud skills/MCP, or to install/update analysis dependencies. **Cascade** (default agent) uses Windsurf-style hooks only — see the Windsurf / Cascade paths in the main README.

## Cursor plugin

If the user loaded the **Harness SAST and SCA** Cursor plugin with **`agent --plugin-dir`**, run:

```bash
node "/path/to/curness-cursor-plugin/handlers/update-handler.js"
```

Use the same **`<plugin>`** directory they passed to **`--plugin-dir`** (repo **`cursor-plugin/`** or **`release/curness-cursor-plugin/`**). IDE installs may live under **`~/.cursor/plugins/local/harness-sast-and-sca/`** instead.

## Cursor extension / VS Code only

If the user has only the **Harness SAST and SCA** extension (no Claude or Cursor plugin), point them at the extension or project **`install.sh`** instead of **`update-handler.js`**.

## If the command fails

Suggest starting a new session so install hooks can run, or running **`install.sh`** from the Harness SAST and SCA project if they are setting up from source.
