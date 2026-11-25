---
name: pynecore-ide
license: MIT
description: Work inside a project set up by PyneIDE, the VS Code extension for PyneCore. Use whenever a project contains a `.pyneide/` folder or `pyneide.*` keys in `.vscode/settings.json`, when the user mentions PyneIDE, "run it in the IDE", the chart, Edit Inputs, debugging a Pyne script bar by bar, Next Bar / Run to Bar / Choose Bar on Chart, the PyneIDE Run output panel, the managed Python environment, Manage Plugins, or asks why the terminal cannot find `pyne`. Covers the IDE-managed environment and how an agent shell reaches it, which generated files matter and which are disposable, the editor commands for running, debugging, profiling, inputs, data and charts, and how to report what was verified in the IDE versus the CLI.
---

# PyneIDE project workflow

PyneIDE initializes a project with a workdir, a managed Python environment and editor
settings, and runs Pyne scripts on a chart with a bar-by-bar debugger. An agent usually has no
UI tools, so this skill tells you how to reach the IDE's environment from a shell, which
commands to name when the user works in the editor, what the IDE writes into the project, and
how to report evidence honestly. Nothing outside the project folder is consulted.

## 1. The project structure PyneIDE requires

PyneIDE works on a PyneCore workdir and expects this layout (the project folder itself when it
holds the `.pyne` marker, otherwise a `workdir/` child):

```
.pyne                 # marker: workdir_version = "1.0"
scripts/  scripts/lib/
data/                 # <name>.ohlcv + <name>.toml pairs
config/               # .gitignore (*), api.toml, plugins/<plugin>.toml, symbol_map.toml
output/  output/logs/
cache/
```

```bash
python3 <skill>/scripts/ide_env.py             # verify the structure, list scripts/data/config
python3 <skill>/scripts/ide_env.py --create    # add whatever is missing, never overwrite
python3 <skill>/scripts/ide_env.py --json
```

Exit code 1 means a required folder or the marker is missing; `--create` makes the folder a
valid workdir for both the IDE and the CLI. A missing `data/<name>.toml` next to an `.ohlcv`
file or an unconverted CSV is reported too. The script reads only the project folder.

## 2. The environment and how to reach it

| Setup | Interpreter | `pyne` | Notes |
|-------|-------------|--------|-------|
| Managed (default) | `<workspace>/.pyneide/venv/bin/python` (Python 3.14) | `<workspace>/.pyneide/venv/bin/pyne` | Created with `uv`; PyneCore + `debugpy`; `.pyneide/.gitignore` is `*`; PyneCore auto-updates daily unless pinned |
| User venv | `pyneide.venvPath` (dir) | `<venv>/bin/pyne` | Takes precedence over `pythonPath`; you install PyneCore and `debugpy` |
| User interpreter | `pyneide.pythonPath` | next to it | Same |

Rules:

- The IDE's **integrated terminal** has the project's `pyne`, `python` and `pip` on PATH. The
  agent's shell does not. Always call `<venv>/bin/pyne --workdir <workdir> run <script> <data>`
  by absolute path (set `PYNE_NO_LOGO=1`), or `<venv>/bin/python` for tooling.
- Do not `pip install` into the managed environment. Plugins go through
  **PyneIDE: Manage Plugins** (the IDE keeps the pinned Core version); a different PyneCore
  release is selected with the `pyneide.pynecore.version` setting (minimum 6.11.1) followed by
  **Setup Environment**. A broken environment is rebuilt with **Remove Environment** then
  **Setup Environment**; **Show Environment Log** has the failure.
- Never commit `.pyneide/`; it is per machine. Workdir outputs (`output/`, `cache/`,
  `data/*.ohlcv`, `config/plugins/` with keys) belong in `.gitignore` too.
- `.pyneide/env.json` records `python`, `pynecore`, `debugpy` versions and `selection` (`""` =
  managed, else the user path). It is informational; do not edit it.
- Pyne analysis: the IDE ships its own pyright variant plus a Pyne checker; in a Pyne
  workspace it replaces Pylance (**Use PyneIDE for Python Analysis**). Red squiggles from
  plain Pylance on `close[1]` are false positives; the project's `pyrightconfig.json` silences
  them.

## 3. What the IDE writes into the project

| File | Agent action |
|------|--------------|
| `.pyne`, `scripts/`, `data/`, `output/`, `config/`, `cache/` | The PyneCore workdir; work here as in any PyneCore project |
| `scripts/demo.py`, `data/demo.ohlcv` + `.toml` | Demo; reuse for smoke tests or delete |
| `scripts/<name>.toml` | Inputs and settings written by the first run and by **Edit Inputs…**; commit it |
| `.vscode/settings.json` | `pyneide.workdir`, interpreter, `files.exclude`; edit freely |
| `pyrightconfig.json` | Type-checker relaxations for `Series`; keep |
| `.vscode/pyne.code-snippets` | Editor snippets; informational |
| `.pyneide/` | Environment; never commit or modify |
| `AGENTS.md`, `CLAUDE.md`, `AGENT_RULES.md`, `.agents/`, `.claude/`, `.cursor/` | Per-project agent boilerplate the IDE generates. These global `pynecore-*` skills replace it; it is not needed, and it can be deleted or ignored in git (`pyneide.showAgentFiles` controls its visibility; Initialize Pyne Project re-creates it). Its "Pine source ownership" rule and the IDE's Compile / Run / Debug commands for scripts in the charting platform's language go through the PyneSys cloud compiler; such sources are converted locally instead, see the `pynecore-pine2pyne` skill (`../pynecore-pine2pyne/SKILL.md`); only the user asking for the cloud compiler by name opens that path, after one line on what is uploaded |

Details and file contents: `references/project-files.md`.

## 4. The editor workflow (what to tell the user, what to check)

Command Palette titles are prefixed `PyneIDE:`; the full list with ids and settings is in
`references/commands-and-settings.md`.

| Goal | Command / place |
|------|-----------------|
| New project | **Initialize Pyne Project** (keeps existing files) |
| New script | **New Script…** in the **Pyne** activity-bar view (Scripts / Data / Output tree) |
| Choose data for a script | **Select Data…** (data picker, also **Download new data…**) |
| Run | **Run Pyne code** (editor toolbar button or Pyne tree); the chart opens and `output/<script>.csv`, `_strat.csv`, `_trade.csv` are written |
| Debug | **Debug Pyne code**: breakpoints in the source; the **Pyne** scope shows the bar's OHLCV and time; Watch accepts `close[1]`; **Next Bar**, **Run to Bar…**, **Pause Run at Next Bar**, **Resume Run**; **Choose Bar on Chart…** pauses on a picked bar |
| Profile | **Profile Pyne code** (flame button): per-line share column, hot lines flagged, summary lens; `output/<script>_profile.json`; **Show/Hide Profile**; Python 3.13+ |
| Inputs | **Edit Inputs…**: a form from the `input.*()` declarations; Save writes `scripts/<script>.toml` and re-runs; Reset to defaults |
| Chart | **Open Chart**: plots, drawings, trade markers; **Performance**, **Trades**, **Stats** tabs for strategies; Layers popup, measure, go-to-date, fullscreen, CSV export |
| Data | **Download Data…**, **Open Symbol Browser**, per-file **Update (continue)**, **Truncate & Re-download…**, **Download Other Timeframe…**, **Open as Table**, **Preview Chart** |
| Multi-timeframe data | **Show Data Requirements** (what `request.security()` needs), **Edit Symbol Map** (`config/symbol_map.toml`) |
| Logs | Output panel **PyneIDE Run** (`log.*` lines, runtime errors; revealed on first log line by default); Problems panel (checker diagnostics, failing line of a runtime error) |
| Environment | **Setup Environment**, **Remove Environment**, **Reveal Environment Folder**, **Show Environment Log**, **Manage Plugins** |
| Stop | **Stop Run** |

Debugging notes: the Pyne debugger steps the source you wrote; with `pyneide.debug.justMyCode`
off you land in PyneCore internals where `Persistent`/`Series` live in a `__state__` list
(`from pynecore.core.instance_state import explain_state; explain_state(main, __state__)`
renders it). For strategy validation look at Trades and Stats, not the chart image.

## 5. Agent route: verify with the CLI, report precisely

Without UI tools, every runtime check goes through the CLI with the IDE's environment:

```bash
PYNE_NO_LOGO=1 <workspace>/.pyneide/venv/bin/pyne --workdir <workdir> run <script> <data>
PYNE_NO_LOGO=1 <workspace>/.pyneide/venv/bin/pyne --workdir <workdir> run <script> <data> --profile
```

The CLI and the IDE share the runtime, the workdir, the `.toml` files and the output files, so a
CLI run reproduces what the IDE would show except the rendering. Then report:

- what ran (script, data file, range, settings) and the numbers from `output/<script>_strat.csv`;
- what was checked in the editor, if anything (which panel, which bar); otherwise say the chart
  and live behaviour are unverified and name the IDE command the user can run to confirm;
- which environment executed it (managed `.pyneide/venv` or a user venv) and the PyneCore version.

Never claim a chart looked right or a breakpoint paused somewhere you did not observe.

## 6. Common requests

| Request | Answer / action |
|---------|-----------------|
| "`pyne` not found" | The agent shell lacks the project PATH; use the absolute `.pyneide/venv/bin/pyne` or `uv run pyne`; the IDE's integrated terminal has it |
| "Update PyneCore" | Managed env updates itself daily; to pin or change: `pyneide.pynecore.version` in `.vscode/settings.json`, then **Setup Environment** |
| "Install a data/broker plugin" | **Manage Plugins** (status bar menu); user-managed envs get a `pip install` line to run |
| "Run it in the IDE" | Open the script, press **Run Pyne code**, pick data with **Select Data…**; results in the chart and `output/` |
| "Change a parameter without editing code" | **Edit Inputs…** (writes `scripts/<script>.toml`), or edit that `.toml` directly |
| "Step through bar 1234" | Set a breakpoint, **Debug Pyne code**, **Run to Bar…** 1234 (or **Choose Bar on Chart…**), then **Next Bar** |
| "Where is my strategy's performance?" | Chart → Performance / Trades / Stats, or `output/<script>_strat.csv` and `_trade.csv` |
| "The chart shows nothing for my plot" | Plot calls must be unconditional in `main()`; check the Problems panel and **PyneIDE Run** for a runtime error |
| "Get rid of the generated agent files" | Delete `AGENTS.md`, `CLAUDE.md`, `AGENT_RULES.md`, `.agents/`, `.claude/`, `.cursor/` or add them to `.gitignore`; these skills do not use them |
| "Re-initialize the project" | **Initialize Pyne Project** again; user files are kept, the boilerplate above is re-created |

## 7. Bundled files

| File | Use |
|------|-----|
| `scripts/ide_env.py` | Verify or create the workdir structure PyneIDE requires; lists scripts, data pairs, config, output (stdlib; reads only the project folder) |
| `references/commands-and-settings.md` | Every PyneIDE command (title + id) and setting with defaults |
| `references/project-files.md` | What each generated file contains, what to edit, `.gitignore` recommendations, snippet prefixes |

Writing the scripts themselves is the `pynecore-strategy` skill; the `pyne` CLI (every command,
option and environment variable) is the `pynecore-cli` skill; data provider and notifier
plugins are the `pynecore-plugin` skill; the PyneCore documentation is bundled in the
`pynecore-docs` skill.
