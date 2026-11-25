---
name: altium-mcp
description: Uses the altium-mcp Model Context Protocol server to read and edit PCB/schematic data from Altium Designer via a DelphiScript bridge on Windows. Apply when the user enables the altium-mcp MCP server, mentions Altium Designer, X2.EXE, PCB layers/rules/nets, schematic components, designators, schematic edits, workspace projects, or MCP tools get_server_status, altium_ping, get_schematic_data, edit_schematic, get_pcb_*, get_all_designators, get_component_pins.
---

# Altium MCP

## Portable use

- **MCP `instructions`**: Compliant clients load server guidance automatically when the MCP session starts (no skill file required for that part).
- **Cursor Agent Skills**: Copy this folder to the client machine (see `INSTALL.md` here), or run `altium-mcp-install-skill` after installing the package.

## Scope

This skill documents the **published** altium-mcp server: Node orchestration plus DelphiScript bundled as `altium-scripts/` in the package (copied at runtime into the workspace `AltiumScript/` directory).

## Architecture (short)

1. **MCP server (Node)** registers tools and, on each live call, acquires a workspace file lock, syncs bundled scripts into `AltiumScript/`, writes `request.json`, and spawns **X2.EXE** with `-RScriptingSystem:RunScript(ProjectName="<workspace>\\AltiumScript\\Altium_API.PrjScr"|ProcName="Altium_API>Run")`.
2. **DelphiScript** (`Altium_API.pas` in the bundle) reads `request.json`, runs the command, writes `response.json` (`success`, `result`, `error`).
3. **Workspace root**: env `ALTIUM_MCP_WORKSPACE`, else `workspaceRoot` in `~/.altium-mcp/config.json` (Windows: `%USERPROFILE%\.altium-mcp\config.json`), else `~/.altium-mcp/workspace`.
4. **Altium EXE**: env `ALTIUM_MCP_ALTIUM_EXE`, else `altiumExePath` in that config file, else newest `AD*\X2.EXE` under `C:\Program Files\Altium`.

## Where tool documentation lives

- **`src/toolDefinitions.ts`** — Canonical long descriptions (Purpose, When to use, Parameters, Returns, Prerequisites, Errors). Edit here first.
- **`src/index.ts`** — Registers tools with those descriptions and MCP `ToolAnnotations` (read-only hints for most tools).
- **MCP `instructions`** — `src/mcpInstructions.ts`: short workflow + table; clients receive this at initialize.
- **This file** — Human/agent skill; keep in sync when adding or renaming tools.

## Agent workflow

1. **get_server_status** — Confirm `altiumExeFound`, `scriptProjectFound`, paths. Stop and fix setup if false.
2. **configure_altium_exe** — Only if exe path is wrong or missing; path must exist on disk.
3. **altium_ping** — Expect JSON with `pong` / protocol version inside `result` from the bridge.
4. **Data tools** — Follow document focus rules below.

## Tool reference (summary)

| Tool | Parameters | Returns (typical) | Altium need |
|------|------------|-------------------|-------------|
| get_server_status | — | Paths, exe flags, env | Triggers script sync |
| configure_altium_exe | `path` | `{ ok, altiumExePath }` | File must exist |
| altium_ping | — | `pong` in result | AD install |
| get_workspace_projects | — | Projects + logical docs + focused index | AD open |
| get_schematic_data | optional `schematic_full_path`, `project_full_path`, `schematic_sheet_file_name` | `{ components[], drawing_objects[] }` (mils + parameters + primitives) | Project(s) open |
| edit_schematic | `action` + same sheet targeting as get_schematic_data + mode fields | `{ action, sheet, details }` or Delphi `ERROR:` | Project(s) open |
| get_pcb_layers | — | Layer metadata | **Focused PCB** |
| get_pcb_rules | — | Rule list | **Focused PCB** |
| get_all_nets | — | Net names | **Focused PCB** |
| get_pcb_layer_stackup | — | Stackup JSON | **Focused PCB** |
| get_all_designators | — | string[] designators | **Focused PCB** |
| get_component_pins | `designators: string[]` | Pin data | **Focused PCB** |
| file_mode_capabilities | — | Capability flags | None (Node) |

## Document focus (Altium UI)

| Situation | Requirement |
|-----------|-------------|
| `get_workspace_projects`, `altium_ping`, `get_schematic_data`, `edit_schematic` | No PCB focus; schematic uses paths or focused project |
| `get_pcb_layers`, `get_pcb_rules`, `get_all_nets`, `get_pcb_layer_stackup`, `get_all_designators`, `get_component_pins` | **Active/focused PCB** in the **focused project** |

Tell the user to open and focus the correct `.PcbDoc` when PCB tools return empty or errors.

## MCP tools ↔ bridge commands

| MCP tool | Delphi `command` / notes |
|----------|---------------------------|
| altium_ping | `ping` |
| get_workspace_projects | `list_workspace` |
| get_schematic_data | `get_schematic_data` (+ optional path params) |
| edit_schematic | `schematic_edit` (+ `action`, paths, mode params) |
| get_pcb_layers | `get_pcb_layers` |
| get_pcb_rules | `get_pcb_rules` |
| get_all_nets | `get_all_nets` |
| get_pcb_layer_stackup | `get_pcb_layer_stackup` |
| get_all_designators | `get_all_component_data` (parsed in Node) |
| get_component_pins | `get_component_pins` + `designators` array |
| file_mode_capabilities | Node-only (no Altium) |

## get_schematic_data parameters

- `schematic_full_path`: absolute `.SchDoc` path for an open project (preferred when several projects are open; `/` or `\\` accepted).
- Or `project_full_path` + optional `schematic_sheet_file_name` (file name only).
- Omit both path forms to use focused project (optional sheet filter).
- `include_queries` (optional string array): omit for **legacy** JSON `{ "components": [...], "drawing_objects": [...] }` only. If set, response is **filtered**: `schematic_data_mode`, `include_queries` echo, and only requested buckets (e.g. `sheet` → `sheets[]` with size/grids; `wires`, `buses`, `components`, …). Use `[ "all" ]` for every split bucket. Tokens: `all` | `sheet` | `components` | `wires` | `buses` | `net_labels` | `power_ports` | `text_labels` | `junctions` | `ports` | `off_sheet_connectors` | `sheet_symbols` | `directives` | `figures` | `harness` (empty `[]` placeholder) | `drawing_objects` (combined list like legacy). Invalid-only tokens fall back to legacy mode.

Legacy return: components include library parameters; `drawing_objects` lists wires, buses, net labels, graphics, etc. Sheet title-block document parameters are excluded. Not pins inside components.

## edit_schematic (summary)

Single MCP tool; `action` selects mode: `set_component_transform`, `set_component_parameters`, `place_component`, `add_text`, `add_net_label`, `add_wire`, plus WIRES phase-1: `place_wire` (alias of `add_wire`), `place_net_label` (alias of `add_net_label`), `add_bus` (same CSV as wire), `add_bus_entry` (exactly four numbers in `wire_points_csv`); POWER phase-2: `place_power_port` (requires `power_port_style`), `place_gnd` / `place_vcc` (shortcuts with defaults in the bridge). Requires `schematic_full_path` or `schematic_sheet_file_name` (same resolution idea as get_schematic_data). Does not auto-save in Altium. Verify with `get_schematic_data` after edits.

## Troubleshooting TIMEOUT / script “frozen”

- **Breakpoints in Altium Script**: If you run the MCP bridge scripts with the DelphiScript debugger and execution hits a breakpoint, Altium stops until you Continue. No `response.json` is written, so MCP reports **TIMEOUT**. Fix: remove breakpoints in the script project, use **Run** without debugging, or **Stop Debugging** / Continue so the script finishes.
- **Lock file**: After an abandoned run, if tools fail with lock errors, delete **`.bridge.lock`** in the MCP workspace directory (`get_server_status` shows `workspaceRoot`).
- **edit_schematic** uses a longer MCP wait (240s) than other tools; first Altium launch after idle can still be slow.
- **Bridge errors for the agent**: On `success: false`, Altium writes **`bridge_last_error.txt`** in the workspace; live tools merge that file into the returned `error` string. **Compile-time** script errors never reach the bridge: paste Altium Messages into **`bridge_user_reported_error.txt`** in the same folder, then **`get_server_status`** exposes `bridgeUserReportedError` / `bridgeLastError`.

## Interpreting results

- Tool return shape is MCP text content with JSON (pretty-printed objects).
- Bridge: `{ "success": true, "result": ... }` or `success: false` with `error`.
- Node launch/path errors: `AD_NOT_FOUND`, `SCRIPT_PROJECT_NOT_FOUND`, `ALT_LAUNCH_FAILED`, `TIMEOUT`, `INVALID_BRIDGE_RESPONSE`, `RESPONSE_READ_FAILED`.
- Serialized access: `.bridge.lock` under workspace; long Altium operations can block other tools (~default 120s command timeout, ~60s lock wait).

## Delphi commands not yet MCP-exposed

The bridge script may implement additional commands (e.g. `move_components`, `create_net_class`, `take_view_screenshot`, output job helpers) beyond the MCP tools listed in the tables above.

## Authors (source repository)

When changing tools or bridge behavior: update `src/toolDefinitions.ts`, then `src/mcpInstructions.ts` and this `SKILL.md`. Run `npm run build` (syncs this skill into `.cursor/skills/` when `scripts/sync-cursor-skill.mjs` runs).
