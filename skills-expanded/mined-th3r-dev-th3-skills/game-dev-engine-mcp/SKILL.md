---
name: game-dev-engine-mcp
description: >-
  Wire a coding agent (Claude Code, Codex, Cursor, Gemini CLI, VS Code) to a game engine's MCP
  server so it can read the scene, edit, run the game, send input, read the logs and take a
  screenshot: Roblox Studio (built in), Unity (official Unity MCP, or MCP for Unity), Unreal (the
  official Unreal MCP plugin on 5.8+, or EngineWire), Godot (Godlink), Blender (Blender Lab or MCP
  for Blender), web games (Chrome DevTools MCP, Playwright MCP), and Bevy. Official server first,
  every package pinned, one config writer for every client. Use WHENEVER the work is "MCP",
  "connect Claude/Codex/Cursor to Unity/Unreal/Godot/Blender/Roblox", "Unity MCP", "Unreal MCP",
  "Godot MCP", "Blender MCP", "Studio MCP", "Playwright MCP", "Chrome DevTools MCP", "let the agent
  playtest", "agent can't see the game", "screenshot the game from the agent", "mcp.json",
  "เชื่อม MCP กับเอนจิน", or before adding any engine's server to an agent's config.
---

# Engine MCP

One method for every engine: pick the server, the person turns on the editor side, the script
writes the client entry, then the agent proves the loop by running the game and looking at it.

`scripts/engine_mcp.py` (stdlib) does the config work: `list`, `doctor`, `config`. It never installs,
downloads or signs in.

## 1. Pick the server

**Official first.** A community server only when there is no official one, or it lacks a step of the
loop (play, logs, screenshot) that the work needs.

| Engine | `--engine` | Default server | Official | Read |
|---|---|---|---|---|
| Roblox | `roblox` | Studio MCP, built in | yes | [`references/roblox.md`](references/roblox.md) |
| Unity 6+ | `unity` | Unity MCP (`com.unity.ai.assistant`, open beta, needs the AI tools plan) | yes | [`references/unity.md`](references/unity.md) |
| Unity, no AI plan or < 6 | — | MCP for Unity (CoplayDev, MIT): its own Configure button | no | [`references/unity.md`](references/unity.md) |
| Unreal 5.8+ | `unreal` | Unreal MCP plugin, HTTP `127.0.0.1:8000` | yes (experimental) | [`references/unreal.md`](references/unreal.md) |
| Unreal 5.0-5.7 | — | EngineWire (ChiR24, MIT), capability token | no | [`references/unreal.md`](references/unreal.md) |
| Godot 4.4+ | `godot` | Godlink (tomyud1, MIT): editor addon | no (none exists) | [`references/godot.md`](references/godot.md) |
| Blender | `blender` | MCP for Blender (MIT); Blender Lab's own server on 5.1+ | Lab: yes | [`references/blender.md`](references/blender.md) |
| Web (HTML5, Phaser, three.js) | `web` / `playwright` | Chrome DevTools MCP; Playwright MCP | yes | [`references/web.md`](references/web.md) |
| Bevy | `bevy` | `bevy_brp_mcp` + the game's `bevy_remote` feature | no | below |

```bash
python scripts/engine_mcp.py list
```

Other engines, checked 2026-11-18. Each is small and community-made; read its README and pin a
release before use:

| Engine | Server | State |
|---|---|---|
| Bevy | [natepiano/bevy_brp](https://github.com/natepiano/bevy_brp) | MIT/Apache, active; crate version follows the Bevy version; `bevy_brp_extras` adds screenshot and input |
| Defold | [Fulviuus/defold-mcp](https://github.com/Fulviuus/defold-mcp) | MIT, 18 stars, thin upkeep |
| GameMaker | [yearningss/gamemaker-mcp](https://github.com/yearningss/gamemaker-mcp) | MIT, active, low use |
| Cocos Creator | [FunplayAI/funplay-cocos-mcp](https://github.com/FunplayAI/funplay-cocos-mcp) | MIT, active |
| O3DE | [nickschuetz/o3de-mcp](https://github.com/nickschuetz/o3de-mcp) | licence unclear: do not use until it states one |

## 2. Editor side (the person's step)

`list` prints it per engine; the reference has the full path. Installs, add-ons, sign-ins and
accepting a connection prompt are the person's yes, never the agent's.

## 3. Wire the agent

```bash
python scripts/engine_mcp.py config --engine <id> --client claude --root <game folder>          # shows it
python scripts/engine_mcp.py config --engine <id> --client claude --root <game folder> --write  # on a yes
```

| `--client` | Writes | Shape |
|---|---|---|
| `claude` | `.mcp.json` | `command`/`args`/`env`, or `type: http` + `url`; also prints the `claude mcp add` line |
| `cursor` | `.cursor/mcp.json` | `command`, or `url` |
| `gemini` | `.gemini/settings.json` | `command`, or `httpUrl` |
| `vscode` | `.vscode/mcp.json` | `servers`, `type: stdio` or `type: http` |
| `codex` | nothing | prints the `~/.codex/config.toml` block; the global file is the person's |

Other servers in the file are kept. A file that is not valid JSON is refused, not repaired. Every
npx/uvx package is pinned (`--selftest` fails on an unpinned one). A config holding a path under
the home folder (Unity's relay) is flagged: keep it out of git or use the client's user scope.
Restart the agent after a write.

## 4. Prove the loop

```bash
python scripts/engine_mcp.py doctor --engine <id> --root <game folder>
```

`doctor` checks the command is on disk, or the HTTP port is listening. Then, in the agent:

1. List the tools (`tools/list`, or the client's MCP panel). **Use the names the server returns.**
   Servers rename tools between releases; the references only list names that were checked.
2. Run the loop once: start or play → input → logs → screenshot → stop.
3. Report what the logs and the capture show. A step the server cannot do, or that could not run,
   is **NOT ASSESSED**, never a pass.

| Step | Roblox | Unity (MCP for Unity) | Unreal | Godot | Blender | Web |
|---|---|---|---|---|---|---|
| Play | `start_stop_play` | `manage_editor` play | toolset via `call_tool` | run tool | `execute_blender_code` | dev server + `navigate_page` |
| Input | `user_keyboard_input` | — | Input toolset | input tool | — | `press_key`, `click_at` |
| Logs | `get_console_output` | `read_console` | Console toolset | log tool | code result (UNVERIFIED) | `list_console_messages` |
| Look | `screen_capture` | `manage_camera` screenshot | Scene Capture toolset | screenshot tool | `look` / `get_screenshot_of_window_as_image` | `take_screenshot` |

The reference for each engine has the exact names and what is unverified.

## Rules

- **Code execution is the person's account.** `execute_luau`, `execute_code`, `execute_blender_code`,
  `evaluate_script`, Python in Unreal: each runs with the editor's or browser's rights. Test
  project, under git, saved first.
- **Loopback only.** Keep HTTP servers on `127.0.0.1`. Never turn on "allow remote" or bind
  `0.0.0.0`. A capability token (EngineWire) is a password: env var, never a committed file.
- **Telemetry off** where the server has a switch (`DISABLE_TELEMETRY`, `--no-usage-statistics`).
- **Pinned, never `@latest`.** To move a version, read its release notes, change the pin in
  `engine_mcp.py` and in the reference, and run `--selftest`.
- **No `curl | sh`** installers on the person's behalf.
- **Ask first:** saving or publishing the project, inserting store assets, generating paid assets.
- **The engine's docs over this file.** Everything here was checked on 2026-11-18; each reference
  names its sources. Recheck before trusting a version or a tool name.

Related: [`../roblox/SKILL.md`](../roblox/SKILL.md) (Rojo, the scaffold, Roblox code rules),
[`../modeling/SKILL.md`](../modeling/SKILL.md) (Blender from a headless script; MCP is for looking
at and poking a live Blender).

## Credits

The Roblox part started from [roblox-suite's `roblox-mcp`](https://github.com/nonlooped/roblox-suite/blob/fc1c3dd26fef67ee4d7b6e20b1299b44fc6101ae/roblox-mcp/SKILL.md)
(MIT, © 2026 nonlooped) and was rechecked against Roblox's MCP page.
