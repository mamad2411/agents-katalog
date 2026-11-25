---
name: game-dev-roblox
description: >-
  Set up and build a Roblox Studio game with any coding agent: Luau code in files synced by Rojo,
  the toolchain pinned with Rokit (Rojo, Selene, StyLua, Lune), headless tests for the rules, and
  Studio's built-in MCP server wired to Claude Code, Codex, Cursor, Gemini CLI or VS Code so the
  agent can playtest, read the output and take screenshots. Use WHENEVER the work is "Roblox",
  "Roblox Studio", "Luau", "Rojo", "Rokit", "obby", "tycoon", "simulator", "RemoteEvent",
  "DataStore", "leaderstats", "Studio MCP", "connect Claude/Codex/Cursor to Roblox Studio",
  "playtest my Roblox game", "VFX", "particles", "ability effects", "เกม Roblox", or before writing Luau for a Roblox place.
---

# Roblox Studio

Studio is the editor and the only place a Roblox game runs and publishes. It updates itself, so
there is no engine version to pin: the toolchain is pinned instead, in `rokit.toml`. The code lives
in files under git; Rojo syncs it into Studio.

`scripts/roblox_setup.py` (stdlib) does the file work: `doctor`, `mcp`, `scaffold`. It never
installs, downloads or signs in.

## 1. What is there (always first)

```bash
python scripts/roblox_setup.py doctor --root <game folder>
```

Each `NEEDS` row is the person's step. Pass them on as written:

- **Studio:** free, Windows and macOS only: create.roblox.com → Start creating; install, sign in,
  open it once. Linux has no Studio: say so and stop the Studio steps.
- **Rokit:** github.com/rojo-rbx/rokit → Installation. Never pipe an install script into a shell
  for the person.

## 2. The project

A `default.project.json` already there is an existing Rojo project: record it, change nothing. A
place kept only in Studio (no files) can stay that way. The agent then works through MCP alone, and
there is nothing for git, the linter or the tests to read.

For a new project, show the files, then write them on a yes:

```bash
python scripts/roblox_setup.py scaffold --root <game folder> --dry-run
python scripts/roblox_setup.py scaffold --root <game folder> --title "<game name>"
```

| Path | Becomes in Studio | Holds |
|---|---|---|
| `src/shared/` | ReplicatedStorage.Shared | classes and factories both sides use (`Wallet`, `Pickup`, `PickupFactory`); **no `game` in them** |
| `src/server/` | ServerScriptService.Server (Script) | the one server Script and server classes (`PickupSpawner`): score, currency, saves |
| `src/client/` | StarterPlayerScripts.Client (LocalScript) | input and what the player sees |
| `tests/run.luau` | — (runs under Lune) | the shared classes' tests |
| `rokit.toml` | — | Rojo 7.7.1, Selene 0.32.0, StyLua 2.6.0, Lune 0.11.1 |

Then, each on a yes: `rokit install` (downloads the four tools from GitHub). The person runs
`rojo serve` and connects Studio → Plugins → Rojo → Connect.

## 3. Wire the agent to Studio

Studio has its own MCP server (create.roblox.com/docs/studio/mcp). In Studio, the person turns it
on: **Assistant → `…` → Manage MCP Servers → Enable Studio as MCP server**. Studio's Quick connect
can wire Claude Code, Claude Desktop, Codex CLI, Gemini CLI, Cursor, VS Code and Antigravity by
itself. For a project-level file instead (the writer is shared with every engine:
[`../engine-mcp/SKILL.md`](../engine-mcp/SKILL.md); the Studio tool list is in
[`../engine-mcp/references/roblox.md`](../engine-mcp/references/roblox.md)):

```bash
python scripts/roblox_setup.py mcp --root <game folder>          # Claude Code (the default): shows the change
python scripts/roblox_setup.py mcp --root <game folder> --write  # on a yes
python scripts/roblox_setup.py mcp --client cursor --root <game folder>   # another agent: codex, cursor, gemini, vscode
```

| `--client` | Writes | Notes |
|---|---|---|
| `claude` | `.mcp.json` | also prints the `claude mcp add` one-liner |
| `cursor` | `.cursor/mcp.json` | |
| `gemini` | `.gemini/settings.json` | |
| `vscode` | `.vscode/mcp.json` | `servers`, `type: stdio` |
| `codex` | nothing | prints the `~/.codex/config.toml` block; the global file is the person's to edit |

Other servers in the file are kept. A file that is not valid JSON is refused, not repaired.
Restart the agent. Studio shows a green dot with the count of connected clients, and
`list_roblox_studios` returns the open place: every tool call names that `studio_id`.

## 4. Build, check, playtest

| Check | Command | Needs |
|---|---|---|
| Place file | `rojo build -o build/game.rbxl` | Rokit tools |
| Lint | `selene src` | Rokit tools |
| Format | `stylua --check src tests` | Rokit tools |
| Rules | `lune run tests/run`: `FAIL <name>: …` lines, then `Tests: N passed, M failed` | Rokit tools |
| Playtest | MCP: `start_stop_play` → `character_navigation` / `user_keyboard_input` → `get_console_output` + `screen_capture` → `start_stop_play` | Studio open, MCP on |

A playtest's result is what the output and the capture show. One that could not run is NOT
ASSESSED, never a pass.

**An agent that playtests PRs** (a `playtester` role in an agent team): scenarios written from each
issue's "Done when", server-authority probes, PASS/FAIL with screenshots, a bug issue per failure.
Read [`references/agentic-playtest.md`](references/agentic-playtest.md).

## Rules for Roblox code

**Read [`references/luau.md`](references/luau.md) before writing Luau.** It holds the house style
(Roblox's style guide as the base), the typed **class + factory** pattern every module follows,
what the Luau VM rewards, and a review checklist, with each rule's source.


- **The server decides.** Currency, items, score, damage and cooldowns change on the server. A
  client message is a request: check its type, range and rate, and whether the player could do
  that now.
- **Classes and factories.** Each kind of thing is a typed class; one factory per family makes
  them from a frozen table of definitions, so a new kind is one row. Rules classes in `src/shared/`
  never touch `game`, so Lune tests them; world code (Parts, connections) is a server class with
  `destroy()`.
- **Files are the source.** With Rojo connected, edit `src/`, not Studio's script editor: the next
  sync overwrites a Studio edit. Use MCP `multi_edit` only for a place with no files.
- **Saves.** DataStore calls in `pcall` with retries; save on leave and in `game:BindToClose`.
- **Scripts.** Roblox recommends a `Script` with `RunContext = Client` over a `LocalScript`
  (create.roblox.com/docs/scripting/scripts). A ModuleScript runs once per side, and the two sides
  never share a copy. No circular requires.
- **Ask first:** `save_place` (writes a new place version), publishing, anything paid, and any
  asset upload.
- **API from the docs.** Read `create.roblox.com/docs/reference/engine/classes/<Class>.md` (or MCP
  `http_get`) before using an API you have not checked; Roblox changes weekly. To find the page,
  start from the indexes `create.roblox.com/docs/llms.txt` and
  `create.roblox.com/docs/reference/engine/llms.txt`.
- **Effects.** Particles, beams, trails, highlights, ability visuals: read
  [`../roblox-vfx/SKILL.md`](../roblox-vfx/SKILL.md).
- **Design:** for a young audience, run `design-lens`'s black-hat audit on anything paid.

## Deeper reference: roblox-suite

[roblox-suite](https://github.com/nonlooped/roblox-suite/tree/fc1c3dd26fef67ee4d7b6e20b1299b44fc6101ae)
(MIT) has one specialist skill per area. Pinned to commit `fc1c3dd`, `last_reviewed` 2026-06-17.

| Topic | Suite skill |
|---|---|
| Core (services, RunContext) | [`roblox-core`](https://github.com/nonlooped/roblox-suite/blob/fc1c3dd26fef67ee4d7b6e20b1299b44fc6101ae/roblox-core/SKILL.md) |
| Networking (remotes, server authority, exploits) | [`roblox-networking`](https://github.com/nonlooped/roblox-suite/blob/fc1c3dd26fef67ee4d7b6e20b1299b44fc6101ae/roblox-networking/SKILL.md) |
| DataStores (safe saves, versioning, quotas) | [`roblox-datastores`](https://github.com/nonlooped/roblox-suite/blob/fc1c3dd26fef67ee4d7b6e20b1299b44fc6101ae/roblox-datastores/SKILL.md) |
| UI | [`roblox-user-interfaces`](https://github.com/nonlooped/roblox-suite/blob/fc1c3dd26fef67ee4d7b6e20b1299b44fc6101ae/roblox-user-interfaces/SKILL.md) |
| Animation (Animator, IK, TweenService, markers) | [`roblox-animation`](https://github.com/nonlooped/roblox-suite/blob/fc1c3dd26fef67ee4d7b6e20b1299b44fc6101ae/roblox-animation/SKILL.md) |
| Audio (audio graph vs Sound) | [`roblox-audio`](https://github.com/nonlooped/roblox-suite/blob/fc1c3dd26fef67ee4d7b6e20b1299b44fc6101ae/roblox-audio/SKILL.md) |
| Monetization (passes, products, subscriptions, PolicyService) | [`roblox-gamepasses`](https://github.com/nonlooped/roblox-suite/blob/fc1c3dd26fef67ee4d7b6e20b1299b44fc6101ae/roblox-gamepasses/SKILL.md) |
| Open Cloud | [`roblox-open-cloud`](https://github.com/nonlooped/roblox-suite/blob/fc1c3dd26fef67ee4d7b6e20b1299b44fc6101ae/roblox-open-cloud/SKILL.md) |
| Teleport | [`roblox-teleport`](https://github.com/nonlooped/roblox-suite/blob/fc1c3dd26fef67ee4d7b6e20b1299b44fc6101ae/roblox-teleport/SKILL.md) |
| Rojo | [`roblox-rojo`](https://github.com/nonlooped/roblox-suite/blob/fc1c3dd26fef67ee4d7b6e20b1299b44fc6101ae/roblox-rojo/SKILL.md) |
| Studio MCP | [`roblox-mcp`](https://github.com/nonlooped/roblox-suite/blob/fc1c3dd26fef67ee4d7b6e20b1299b44fc6101ae/roblox-mcp/SKILL.md) |
| Physics (constraints, network ownership) | [`roblox-physics`](https://github.com/nonlooped/roblox-suite/blob/fc1c3dd26fef67ee4d7b6e20b1299b44fc6101ae/roblox-physics/SKILL.md) |
| NPCs (PathfindingService) | [`roblox-npcs`](https://github.com/nonlooped/roblox-suite/blob/fc1c3dd26fef67ee4d7b6e20b1299b44fc6101ae/roblox-npcs/SKILL.md) |
| Testing (Developer Console, MicroProfiler) | [`roblox-testing`](https://github.com/nonlooped/roblox-suite/blob/fc1c3dd26fef67ee4d7b6e20b1299b44fc6101ae/roblox-testing/SKILL.md) |

Read the matching file before writing code in that area. This skill's house rules win where they
disagree (class + factory from `references/luau.md`, Lune tests instead of TestEZ, `.luau` files,
the Rojo layout from the scaffold); the engine docs win over both. The suite's `.lua` scripts are
examples to adapt, never files to drop into `src/`. VFX is not in the table: it goes to
[`../roblox-vfx/SKILL.md`](../roblox-vfx/SKILL.md).

## Full template

[th3 Game Studio](https://github.com/th3r-dev/th3-game-studio) has the same scaffold behind
`/setup-engine roblox`, plus a `roblox-specialist` agent, `test-run.sh roblox`, and the whole
studio flow (brief, stories, reviews, release).
