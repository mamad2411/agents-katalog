---
name: blueprint-export
description: Export Blueprints from a running UE5 Editor for analysis. Use when the user wants to export, scan, or snapshot their Blueprints.
allowed-tools: [Read, Write, Bash, Glob, Grep]
---

# Blueprint Export

Export Blueprints from a running UE5 Editor via Python remote execution.

## What the User Needs

1. UE5 Editor running with their project open
2. Python Remote Execution enabled (run `/ue5-blueprints:setup` if not done)
3. Blueprint path(s) to export

## Steps

### 1. Get the Blueprint Path(s)

Ask the user for the Blueprint path(s) they want to export. These look like:
- `/Game/MyProject/Blueprints/BP_PlayerCharacter`
- `/Game/MyProject/UI/WBP_MainMenu`

They can find this by right-clicking any asset in the Content Browser and choosing "Copy Reference".

### 2. Choose Export Type

- **T3D Export** — Raw text export with ALL node data including pin connections. Best for deep analysis and wiring map generation. Larger files.
- **Graph Snapshot** — Structured JSON with node types, variables, functions, positions. Smaller, faster, good for quick audits.
- **Both** — Full pipeline for maximum analysis power.

### 3. Create the Target Config

Write a JSON config file for the export scripts. Use `${CLAUDE_PLUGIN_DATA}` for output:

For T3D export, write to `${CLAUDE_PLUGIN_DATA}/export_targets.json`:
```json
[
  {"path": "/Game/...", "output": "MyBP.t3d"}
]
```

For snapshot, write to `${CLAUDE_PLUGIN_DATA}/snapshot_targets.json`:
```json
[
  {"path": "/Game/...", "output": "MyBP_snapshot.json", "graphs": ["EventGraph", "MyFunction"]}
]
```

Set `"graphs"` to `null` to export ALL graphs in the Blueprint.

### 4. Run the Export

Set the output directory and run:
```bash
UE5BP_OUTPUT_DIR="${CLAUDE_PLUGIN_DATA}" python "${CLAUDE_PLUGIN_ROOT}/scripts/run_in_editor.py" "${CLAUDE_PLUGIN_ROOT}/scripts/bp_export_t3d.py"
```

Or for snapshot:
```bash
UE5BP_OUTPUT_DIR="${CLAUDE_PLUGIN_DATA}" python "${CLAUDE_PLUGIN_ROOT}/scripts/run_in_editor.py" "${CLAUDE_PLUGIN_ROOT}/scripts/bp_snapshot.py"
```

### 5. Confirm Results

Read the output files to verify export succeeded. Report file sizes and node counts to the user.

Suggest next steps:
- `/ue5-blueprints:blueprint-audit` to analyze the exported data
- `/ue5-blueprints:blueprint-check` for a quick paste-and-check
