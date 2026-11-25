---
name: argent-testing
description: Set up or use Argent (Software Mansion) for deep interactive testing of the running iOS Simulator or Android emulator — tap/swipe gestures, recorded E2E flows replayed as smoke tests, visual regression diffing, deep-link testing, and native performance profiling (Hermes, React DevTools, Xcode Instruments, Perfetto). Use when a bug needs live interaction to reproduce, when a flow needs a repeatable regression test, or when investigating jank/memory/hangs. For a quick "does this screen look right after my change" check, use the `preview` skill instead — it's faster and doesn't require any setup.
---

Argent (`@swmansion/argent`) is a third-party agentic toolkit — a CLI plus its own MCP server — that gives an agent live control of the iOS Simulator or Android emulator: tapping, swiping, typing, hardware buttons, recorded-flow replay, screenshot diffing, and native profiling. It goes well beyond this plugin's own `preview` skill, which only screenshots whatever is already on screen.

## When to reach for Argent vs `preview`

- **`preview`** (bundled, no setup): screenshot the current screen, check for device errors, run tsc. Use after almost every UI change — this is the default.
- **Argent** (opt-in, one-time setup per project): the task needs the agent to *drive* the app — reproduce a bug that only appears after a sequence of taps, replay a login flow as a regression check, diff a screen against a visual baseline, or profile why something is janky/leaking memory. Don't reach for this for routine "did my change land correctly" checks.

## One-time setup (per project, not per plugin)

Argent's MCP server is registered in the *app's own* editor/workspace config, not this plugin's — each project that wants it opts in individually. Use yarn, not npm/npx:

```bash
yarn dlx @swmansion/argent@latest init --yes --global --no-telemetry
```

`--yes` skips the interactive wizard (editor selection, auto-approve prompts); `--global` is the CLI's default meaning ("install on PATH for this machine") but **verified: running the wizard via `yarn dlx` did not actually leave a persistent `argent` binary on PATH** in testing — the wizard still correctly wrote `.mcp.json`, `.claude/settings.json` (adds `mcp__argent` to the allow-list), `.vscode/mcp.json`, and copied rules/skills/agents into `.claude/`, but `which argent` came back empty afterward. Until that's root-caused, don't rely on a bare `argent` command being resolvable — invoke everything through `yarn dlx @swmansion/argent@latest <command>` instead (confirmed working every time, just slower per call due to yarn's resolution step). If `.mcp.json`'s `"command": "argent"` entry fails to start, rewrite it to `["yarn", "dlx", "@swmansion/argent@latest", "mcp"]`.

Expo's own docs recommend pairing Argent with the Expo MCP server this plugin already provides — Argent drives the simulator/emulator, the Expo tooling supplies Expo-specific conventions (routes, config, design tokens). They're complementary, not overlapping.

Note: Argent's core CLI is Apache-2.0, but the platform-specific native binaries are proprietary Software Mansion IP with redistribution restrictions — read their license before including it in a build pipeline.

## Using it — verified tool names (v0.25.2)

Confirmed by running `yarn dlx @swmansion/argent@latest tools` — 76 tools total, spanning iOS Simulator, Android emulator, physical devices, and Chromium. The ones you'll reach for most:

- **`list-devices`** — enumerate simulators/emulators/physical devices; get the `udid`/serial every other tool needs.
- **`screenshot --udid <id> --scale 1.0 --out <path>`** — capture the screen. Coordinates for `gesture-*` tools are **normalized 0.0–1.0 fractions of width/height, not pixels** — read them off a screenshot, don't guess pixel positions.
- **`gesture-tap` / `gesture-swipe` / `gesture-scroll` / `keyboard`** — interaction primitives. Verified: a tap call returns `{ tapped: true, timestampMs }` even when nothing observable happens on screen — a successful return does **not** guarantee the tap landed on the intended element. Always re-screenshot after interacting and check the result visually; don't trust the return value alone.
- **`launch-app` / `reinstall-app` / `restart-app`** — app lifecycle by bundle id (iOS) / package name (Android).
- **`screenshot-diff`** — visual regression: compare two PNGs.
- **`native-describe-screen` / `native-full-hierarchy` / `native-find-views`** — accessibility-tree discovery; use before tapping to get real element coordinates instead of guessing.
- **`react-profiler-start/stop` / `native-profiler-start/stop`** — Hermes CPU + React commit capture, and native (Instruments/Perfetto) profiling, respectively.
- **`run-sequence`** — chain multiple interaction steps in one call, for scripted flows.

Run `argent tools describe <name>` (or `yarn dlx @swmansion/argent@latest run <tool> --help`) for a tool's exact flags before calling it — flag names aren't always what you'd guess (e.g. `screenshot` takes `--udid`, not `--device`).

## Boot devices through Argent, not raw platform tools

Use **`boot-device`** to start a simulator/emulator, not `xcrun simctl boot` / `emulator -avd` directly — a device booted outside Argent is missing the accessibility hooks Argent's own tools expect (`describe` on such a device returns a hint: *"This simulator was not booted through argent... boot-device with force=true reboots the simulator with the full accessibility settings"*).

## Never guess tap coordinates from a screenshot — use `describe`

`gesture-tap`/`gesture-swipe` take **normalized 0.0–1.0 fractions of width/height**, and it is easy to mis-eyeball those from a screenshot — a coordinate error is by far the most common cause of a tap silently landing on nothing. **Verified failure mode:** `gesture-tap` returns `{ tapped: true, timestampMs }` — a "success" — even when the tap landed on empty space and nothing happened. The return value does not confirm your coordinates were right.

Always call **`describe`** (cross-platform: iOS ax-service or Android devtools) first, read the target element's `(x, y, width, height)` frame, and tap its center (`x + width/2`, `y + height/2`) — don't estimate from a screenshot. Re-screenshot after every interaction to visually confirm the expected change happened; treat `{tapped: true}` alone as inconclusive.

## Platform-specific verified behavior (v0.25.2, tested against real devices)

- **Android:** fully verified working end-to-end — `boot-device` → `describe` → `gesture-tap` (using `describe`'s coordinates) → `screenshot` correctly confirmed a real app launch (tapping the Phone icon opened the dialer). No extra setup needed beyond a working Android SDK emulator.
- **iOS:** `screenshot` works reliably headless, no GUI required. **`gesture-tap` and other interaction tools require the simulator's GUI application to actually be running** — on a machine missing it (some CI-oriented or trimmed Xcode installs), every interaction call fails with `CoreDevice HID transport is dead: ... reattach required`, even immediately after `boot-device --force`. This is a real environment prerequisite, not a flaky Argent bug — screenshot-only iOS workflows still work fine without it.

  **Naming/path varies by Xcode version** (verified across two): Xcode ≤26 ships it as `Simulator.app` at `Contents/Developer/Applications/Simulator.app`. **Xcode 27 renamed and relocated it to `DeviceHub.app` at `Contents/Applications/DeviceHub.app`** — the old path is gone entirely under 27, not just moved-and-still-findable. Check both before concluding it's missing:
  ```bash
  ls "$(xcode-select -p)/Applications/Simulator.app" 2>/dev/null || ls "$(xcode-select -p)/../Applications/DeviceHub.app" 2>/dev/null
  ```
  Launch whichever exists (`open <path>`) and keep it running before relying on iOS interaction — booting the device via `simctl`/`boot-device` alone, without the GUI app actually open, is what produces the HID transport error.

## If Argent isn't installed

Don't fail silently — tell the user the task would benefit from Argent, give them the `init` command above, and fall back to `preview` plus manual reasoning in the meantime.
