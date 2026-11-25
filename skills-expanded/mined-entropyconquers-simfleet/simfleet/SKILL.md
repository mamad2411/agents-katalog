---
name: simfleet
description: >
  Operate a simfleet device fleet: slimmed iOS simulators and Android emulators, parallel React Native
  worktree lanes with leased Metro ports, the native build cache, and per-agent device claims. Use this
  skill whenever a project has `.sim-fleet/project.json` and an agent needs to boot or slim a simulator
  or emulator, run one or more worktrees on devices, allocate or inspect Metro ports, launch an
  environment/build variant, tap/type/inspect a device, claim a device for its session, or diagnose
  simulator RAM — even when the request only says "run this branch", "open the simulator", or "fix a
  Metro port collision".
---

# simfleet

simfleet is one control plane for every simulator, emulator, Metro server, and lane on this Mac. The
browser dashboard and this CLI operate the same state. Never start a second dashboard, an unmanaged
Metro, or a device outside the fleet.

## Setup

```bash
bun add -g simfleet            # or: bunx simfleet <command>
simfleet version
simfleet serve                 # dashboard + API on http://127.0.0.1:8790, menu-bar icon
```

Host tools: `brew install mobai-app/tap/simslim baguette watchman` (iOS) and
`brew tap kdbhalala/avdslim https://github.com/kdbhalala/avdslim.git && brew install avdslim scrcpy`
plus the Android SDK (Android). Commands run from any checkout or worktree of a project with
`.sim-fleet/project.json`; simfleet resolves the main checkout. Set `SIM_FLEET_URL` only when the server
runs at another origin.

```bash
simfleet status                # host RAM, worktrees, lanes, Metros, simulators, emulators, agents
simfleet ports                 # environment port ranges and live leases
simfleet sim list | emu list | lane list | agents
```

Read [`references/api.md`](references/api.md) when the CLI lacks an operation or another program needs
the HTTP/WebSocket contract.

## Rules

- **Devices are always slim unless the user explicitly asks for stock.** Boot with
  `simfleet sim boot <udid>` / `simfleet emu boot <avd>`; both apply and verify the slim profile. Do not
  boot fleet devices with `xcrun simctl boot`, Xcode, Android Studio, or another tool's boot command.
  The server auto-slims strays (Android live; iOS only in its first minutes, because SimSlim reboots).
  Use `--stock`, `sim restore`, or `emu restore` only on explicit request, and `slim` afterwards.
- **Claim what you hold.** Every CLI call from a Claude Code or Codex session is attributed to the
  device it touches. Run `simfleet claim <udid-or-avd> "what you are doing"` before a long task and
  `simfleet release <udid-or-avd>` when done. Never drive a device another live session has claimed
  (check `simfleet agents`).
- **Lanes own ports.** A debug lane leases its Metro port from the environment's range; release lanes
  embed JS and have no Metro. Never pick ports by hand, hash branch names into ports, or kill an
  unknown Node/Metro process — inspect `ports`/`status` and stop the owning lane.
- **Bundle identifiers are stable native identities**, never worktree identities. Environments
  (development/staging/preprod/production) select runtime JS config and never force a native build.
- **JS-first.** For ordinary React Native changes: start a lane, wait for Metro, launch. Build natively
  only when native inputs changed, and only through `native plan` / `native ensure` (fingerprinted,
  single-flight, shared across agents) — never `expo run:ios`, CocoaPods, or Xcode directly.
- Work in existing worktrees. Create one only when asked, via `simfleet worktree create`.
- Stop only lanes you started.

## Run a worktree on a device

```bash
simfleet status && simfleet ports                          # 1. inspect ownership first
simfleet sim boot <udid>                                   # 2. or: simfleet emu boot <avd>
simfleet claim <udid> "testing checkout on feature-x"      # 3.
simfleet native plan <abs-worktree> debug <udid>           # 4. iOS: expect a cache hit for JS-only work
simfleet native ensure <abs-worktree> <udid> debug
simfleet lane start <abs-worktree> <udid-or-avd> [environment] [debug|release]   # 5.
simfleet lane launch <lane-id>                             # 6. waits for Metro health
simfleet lane open-url <lane-id> <path-or-url>             #    uses the mode's scheme
```

Lane creation fails rather than stealing a worktree, device, or occupied port. If launch reports Metro
not ready, read `simfleet lane log <lane-id>` and fix the actual Metro error while keeping the lease.

Parallel agents each own exactly one worktree, device, and lane; `native ensure` may be called
concurrently (one build, everyone reuses it).

## Drive a device

Inspect semantically before using coordinates, then verify with another `ui` call.

```bash
simfleet sim ui <udid> [x y]                       # accessibility tree / hit test (points)
simfleet sim tap|double-tap <udid> <x> <y>
simfleet sim swipe <udid> <x1> <y1> <x2> <y2>
simfleet sim type <udid> "text" ; simfleet sim key <udid> Enter
simfleet sim button <udid> home ; simfleet sim rotate <udid> landscape-left
simfleet sim open-url <udid> 'myapp://path'

simfleet emu ui <avd> [x y]                        # UIAutomator tree (device pixels)
simfleet emu tap|swipe|type|key|button|open-url|dev-menu <avd> ...
simfleet emu screenshot <avd> /abs/out.png
```

Android devices are addressed by AVD name (the `emulator-5554` serial only exists while running).
Android lanes are debug-only; `lane launch` sets up `adb reverse` and opens the dev client, which must
already be installed.

## Stop

```bash
simfleet lane stop <lane-id>
simfleet release <udid-or-avd>
simfleet sim shutdown <udid> | simfleet emu shutdown <avd>     # only devices you booted
```

## Report

State the lane ID, worktree/branch, device, environment/mode, bundle ID, Metro port and health (or
embedded delivery), whether the device is slim, and whether the native artifact was reused or rebuilt.
Metro health or a successful launch is not proof a feature works; include UI evidence of the feature
itself.
