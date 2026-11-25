---
name: setup
description: >-
  Use when the user asks to set up, install, connect or update Omniverse MCP, when a tool says it cannot reach the
  Kit app or that the extension is older than the server, or when Isaac Sim or another Kit app should be driven from
  here for the first time. Installs the Kit extension of this plugin's release, has the user point Kit at it and turn
  it on, and checks the connection with get_sim_state.
allowed-tools: mcp__plugin_omniverse-mcp_omniverse__get_sim_state
---

# Set up Omniverse MCP

The plugin's MCP server talks to a Kit app (Isaac Sim, USD Composer) through the Kit extension `ovmcp.bridge`, which
must come from the same release. This skill installs that extension, has the user turn it on in Kit, and checks the
two can talk. Kit's settings are the user's: say what to click, never edit Kit's config files.

## Steps

1. **Check first.** Call `get_sim_state`.
   - It answers without a `note` line: the setup is done. Say so, with the up axis, units and prim count it
     reports, and stop.
   - It answers with a `note`: Kit runs another release's extension, after an update of the plugin or from an older
     copy (a clone of the repo). Go on with step 2.
   - It fails, refused or timed out: run `uvx omniverse-mcp==0.5.1 extension path`, which changes nothing. When it
     says "is not installed there yet", this is a first setup: go on with step 2. Without that line the extension is
     installed: have the user start Kit if it isn't running, then check again; still refused, go on with step 3.
   - It fails otherwise: its message says why; step 4 lists each message and what to do.
   - There is no such tool: the plugin's server didn't start. `/mcp` shows its error. Without `uv` the user installs
     it (https://docs.astral.sh/uv/getting-started/installation/) and restarts Claude Code; a version not found means
     this release isn't on PyPI yet.
2. **Install the extension** of this plugin's release, with the user's yes:

   ```
   uvx omniverse-mcp==0.5.1 extension install
   ```

   It copies `ovmcp.bridge` into the user's data folder, in place of an older one, and prints the folder Kit needs.
   On Windows, "Could not install ... quit it" means a Kit app has the extension loaded: ask the user to quit it,
   then run the command again. When it printed "in place of <version>", the folder is already on Kit's search path:
   skip step 3, and have the user restart Kit. Otherwise do step 3.
3. **Point Kit at the folder, once,** by the user's hand, in the Kit app:
   - **Window > Extensions**, the menu (☰) at the top right, **Settings**;
   - under **Extension Search Paths**, unless it is listed already, the green **+**, then the folder the command
     printed;
   - search for `ovmcp`, under **THIRD PARTY**: turn **Omniverse MCP Bridge** on, and **Autoload**;
   - the extension starts at once: go on with step 4. Kit saves the search path and Autoload when it exits, so the
     user quits it once with **File > Exit** before the next session.

   A headless or scripted Kit takes `--ext-folder <the folder> --enable ovmcp.bridge` on its command line instead.
   A user who had the extension from a clone of the repo (`isaacsim.mcp.bridge` or the clone's `extension/` folder)
   turns that one off and removes its search path, so Kit loads one copy. One who installed **Omniverse MCP Bridge**
   from Kit's community registry (under **THIRD PARTY**, marked *Community - Unverified*) uninstalls it in the
   Extensions window: the plugin keeps the extension of its own release.
4. **Check again** with `get_sim_state`: it answers without a `note`. The Kit console shows
   `[ext: ovmcp.bridge-0.5.1] startup` once the extension runs. Every failure starts "Kit app connection failed";
   what follows says which:
   - "Missing or wrong bridge token": Kit runs as another user or on another machine;
     [Kit on another machine](https://github.com/serionist/omniverse-mcp/blob/main/docs/SETUP.md#kit-on-another-machine)
     says how to set one by hand.
   - "older than this MCP server" or "speaks bridge protocol": Kit loads another release's extension. Did step 2
     run? Then Kit loads another copy: do step 3, its last paragraph too.
   - It answers, with a `note` still: Kit loads another copy too; do step 3, its last paragraph too.
   - Anything else (refused, timed out): Kit isn't running, the extension is off, or it listens on another port than
     the server (`OMNIVERSE_MCP_PORT`, 8211 by default).
5. **Keep the outputs out of git.** The server writes captures and long answers to `mcp_output/` in the project.
   When the project is a git repository and `.gitignore` doesn't name it, offer to add the line `mcp_output/`.

## Done means

- `get_sim_state` answers from the user's Kit app, without a `note`.
- The user knows the extension autoloads, and that after updating the plugin this skill updates the extension.

## Never

- Edit Kit's `user.config.json` or other settings files: Kit rewrites them when it exits.
- Install the extension, or change `.gitignore`, without the user's yes.
- Set `OMNI_KIT_ACCEPT_EULA` or accept NVIDIA's licence for the user.
