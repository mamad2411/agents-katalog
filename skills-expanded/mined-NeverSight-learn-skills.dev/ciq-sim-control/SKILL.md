---
name: ciq-sim-control
description: Drive the Garmin Connect IQ simulator for any Monkey C project — set device state (battery, charging, DND, notifications, color-shift, sleep, units, time), switch weather and AOD/display mode, run reusable scenario configs, build a screenshot gallery, and capture store screenshots. Use whenever asked to launch/run the simulator, reproduce a device condition, test how code renders under some state, screenshot a watch face/app, or run simulator test automation. File-first and deterministic; AI only orchestrates.
---

# Connect IQ simulator control

> **Uses the `ciqkit` command** from the garmin-connectiq-devkit toolkit. If `ciqkit`
> isn't on PATH: clone https://github.com/bayville/garmin-connectiq-devkit and run
> `./install.sh` once (or invoke the repo's `scripts/simctl.sh` directly). Run commands
> from your Monkey C project dir, or set `CIQKIT_PROJECT=/path/to/project`.

Prefer `ciqkit sim` over clicking menus.

**Mental model:** device state lives in `simulator.ini`, read only at sim startup — so it
gets set by *stop → patch → relaunch* (deterministic, no UI). Only **weather** and
**display-mode/AOD** have no file; those use UI automation (needs macOS Accessibility) and
print `[UI]`.

## Cheat sheet

```sh
ciqkit sim launch | reload                 # run in fresh sim | repush to running sim
ciqkit sim set battery=15 charging=on dnd=on notify=3   # batch state (one relaunch)
ciqkit sim battery 8 off | dnd on | notify 5 | time 24 | units statute | colorshift red
ciqkit sim display aod       # [UI] high|aod|off
ciqkit sim weather --avail on --cond Rain --temp 9      # [UI]
ciqkit sim shot [path]       # face-only PNG; then READ it
ciqkit sim scenario <name> | list | gallery all         # reusable configs + matrix
ciqkit test [device]         # unit tests
```

`set` keys: `battery charging days dnd notify alarms sleep time units colorshift training wifi ble`.
Run `ciqkit sim help` for the full list; **batch related keys into one `set`** (each `set`
relaunches once, ~8–10 s).

## Configs & verifying

- Named configs live in the toolkit's `scenarios/default.scenarios` + a project-local
  `scenarios.local` (`name: battery=25 charging=on` or
  `name: ui:weather --avail on --cond Snow --temp -4`).
- Verify a change: `ciqkit sim reload` → set the state → `shot` and READ the PNG. Prefer a
  unit test (`ciqkit test`) for logic; use screenshots to confirm the visual.

## Depth on demand (in the toolkit repo / on GitHub)

- Why file-first, full key table, evidence: [SIMULATOR_CONTROL.md](https://github.com/bayville/garmin-connectiq-devkit/blob/main/docs/SIMULATOR_CONTROL.md)
- Test strategy / coverage mapping: [TESTING.md](https://github.com/bayville/garmin-connectiq-devkit/blob/main/docs/TESTING.md)
- Screenshots / store frames: [SCREENSHOTS.md](https://github.com/bayville/garmin-connectiq-devkit/blob/main/docs/SCREENSHOTS.md)

## Rules

- Changing `simctl` behavior REQUIRES updating this skill + docs in the same change and
  re-verifying on a real simulator ([CONTRIBUTING.md](https://github.com/bayville/garmin-connectiq-devkit/blob/main/CONTRIBUTING.md)).
- Errors: "not running" → `ciqkit sim launch`; `[UI]`/`shot` fails → grant Accessibility,
  close any open modal; file-based change not showing → it needs the relaunch that
  `set`/`scenario` already do.
