# AGENTS.md

Instructions for coding agents working in this repository. Humans should start with [README.md](README.md). The tracker contract is [protocol.md](protocol.md).

## What this is

Omascreentime (`postman.omascreentime`) is a third-party Omarchy plugin:
a **service** that supervises a Rust tracker, and a **bar-widget** whose
KeyboardPanel overlay shows today's donut, app list, week strip, and
patterns. The overlay is read-only. All focus accounting lives in
`omascreentime-track`.

Do not turn this into a standalone app, an Electron UI, or a first-party
`omarchy.*` plugin.

## Hard constraints

- **Never track focus from QML/JS.** No `ToplevelManager` accrual, no
  `/proc` walks, no Python resolver from the overlay. All of that is Rust.
- **Never write history outside the state dir.** `$XDG_STATE_HOME/omascreentime`
  or `~/.local/state/omascreentime` (`0700` / `0600`).
- **Never edit `/usr/share/omarchy/`.**
- **Do not change the plugin id** (`postman.omascreentime`) unless the user
  explicitly asks.
- **Do not commit** `DESIGN.md`, `PLAN.md`, live history, sockets, `.env`,
  or `target/`.
- **`omarchy plugin add` does not compile.** After clone,
  `mise install && ./scripts/build.sh` must produce
  `target/release/omascreentime-track`.

## Layout

```
manifest.json           id, kinds: ["service","bar-widget"], settings schema
service/Service.qml     ensure the daemon is running
bar/BarWidget.qml       chip + KeyboardPanel host
bar/Model.js            chip text / tooltip / parse
overlay/Overlay.qml     session, Process children, hover, keyboard
overlay/OverlayModel.js donut layout, hit-test, parse, palette
overlay/DonutCanvas.qml filled wedges + goal ring
overlay/AppList.qml     sibling list
overlay/Hero.qml        title + PATTERNS
overlay/WeekStrip.qml   last 7 days
overlay/Patterns.qml    insights
overlay/StatusBar.qml   tracking / idle / error
overlay/Format.js       durations
src/main.rs             proto | ensure | daemon | status | view | stop
src/tracker.rs          buckets, midnight, live view
src/daemon.rs           Hyprland IPC + socket + snapshot
src/hypr.rs             activewindow + event stream
src/resolve.rs          terminal pty foreground process
src/session.rs          loginctl idle / lock
src/apps.rs             fmt, canonical, insights
src/store.rs            atomic history
src/paths.rs            dirs, flock
src/protocol.rs         NDJSON events
tests/                  CLI
scripts/build.sh
scripts/test.sh
scripts/dev-install.sh
```

## Build and verify

```sh
mise install
./scripts/test.sh
./scripts/build.sh
./scripts/dev-install.sh
```

After QML edits on a **symlink** install, force a reload with
`omarchy-shell shell rescanPlugins` — inotify does not follow the plugin
symlink.

## Protocol invariants

Full schema: [protocol.md](protocol.md).

- One JSON object per stdout line. `v` must be `1`. Unknown `type` → ignore.
- stderr is human logs only.
- `view` apps lists every app ≥5s. Overlay groups the donut to 6 slices
  (tail → Other). The list must show the full `apps` array.
- Midnight: credit the open bucket to the day it started.
- Pause on no window, lock, screensaver, session idle. Honor `inhibitingIdle`.

## Overlay invariants

1. **Shared hover.** One `hoverId` plus `hoverTick`. Donut and list both
   read live state. Do **not** clear hover on canvas `onExited`.
2. **Slice ↔ list.** Hovering a slice selects the same id as the list row.
   `hitTestSlices` must match `layoutSlices` geometry.
3. **Do not put a role named `color` on a QML ListModel.** Use `fill`.
4. **`g` / `G` scroll the Flickable.** Arrows scroll too. `j` / `k` move
   the highlighted app. Panel width is 360, height fits content (cap 480).

## Tracker invariants

- Terminals resolve through `/proc` (pty foreground pgrp), not the
  compositor class. Detect terminals by class **or** Hyprland `terminal*`
  tag. Runtimes and launchers unwrap to the real command (comm rename,
  script basename, or best child). Stop at the first non-wrapper so
  jobs under that app are not stolen. Re-resolve every 5s while a
  terminal stays focused. Do not special-case a single app name.
- Browsers fold to a canonical id (`zen-bin` → `zen`, `brave-origin` → `brave`).
- Snapshot writes are atomic. Crash loss is bounded by the 30s commit.

## Out of scope unless asked

- Rewriting the tracker in another language.
- Packaging a prebuilt binary for every arch.
- Changing marketplace id, license, or install/remove docs without
  updating README and `manifest.json` together.
