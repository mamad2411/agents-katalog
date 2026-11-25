---
name: simulators
description: Run, see, drive and verify an app on this machine's own simulators. iOS Simulators run on the macOS VM that macbox runs here (`mac-sim`) and Android emulators on this machine itself (`android-sim`), both local and free; web runs in T3 Code's browser. Use it whenever work needs the app running - "open the simulator", "run it on iPhone / Android", "check it on iOS / Android", screenshots, tapping through a flow, recording an animation, checking 60 fps, widgets, Live Activities, the Dynamic Island - for any Expo / React Native app, including new ones. After every change to what a screen shows or how it moves, use it to see the change running, record it and measure it.
---

# Simulators on this machine

Every simulator runs here, next to you, so they cost nothing and you see the screen exactly. There is one command per platform, and both have the same shape:

| Platform | Command | What you get |
|---|---|---|
| iOS | `mac-sim` | A pool of iOS Simulators on macbox's macOS VM (`ssh macbox`). Slim ones by default; `--full` for widgets, Live Activities, the Dynamic Island and push; `--sharp` for real-iPhone pixels; `--small` for a small phone. |
| Android | `android-sim` | A pool of Android emulators (720x1600, the layout width of a Pixel 9), if this machine has the Android part set up (`android-sim status`). |
| Web | `npx expo start --web` or the project's own dev server | In T3 Code, look at it in T3's browser: `preview_open` with `target: {kind: "environment-port", port}`. |

When the task says "the app" without a platform, iOS is the primary target and Android second. An app that ships on both isn't done until both have been checked. For a build on a real phone (an `.ipa`, TestFlight, an `.apk`), use the `phone-builds` skill.

## Commands

Run them from inside the app's checkout. Each checkout gets its own simulator and keeps it until `down`, so agents in different checkouts never wait for each other.

| | iOS | Android |
|---|---|---|
| Claim and boot | `mac-sim up [--full\|--sharp\|--small]` | `android-sim up` |
| Build, install, open (Metro runs here; JS edits arrive by Fast Refresh) | `mac-sim run` | `android-sim run` |
| Release build: what users get, no Metro | `MODE=release mac-sim run` | `MODE=release android-sim run` |
| Expo Go instead of a build | `MODE=go mac-sim run` | install Expo Go (see `references/android.md`) |
| The screen as a tree, with refs like `@e12` | `mac-sim snapshot` | `android-sim snapshot` |
| Tap, type, scroll, swipe, back, open... (any agent-device command) | `mac-sim ad press @e12` | `android-sim ad press @e12` |
| Lossless screenshot, copied here | `mac-sim shot /tmp/x.png` | `android-sim shot /tmp/x.png` |
| Record the screen (seconds), copied here | `mac-sim record /tmp/a.mp4 5` | `android-sim record /tmp/a.mp4 5` |
| Open a link or deep link | `mac-sim open <url>` | `android-sim ad open <url>` |
| The ids for T3 Code's `device_open` | `mac-sim t3` | `android-sim serial` (hostId `local`) |
| Every simulator and who uses it | `mac-sim status` | `android-sim status` |
| Build, Metro and device output | `mac-sim logs` | `android-sim logs` |
| Done: free it | `mac-sim down` | `android-sim down` |

Measure a recording with `sim-fps /tmp/a.mp4` (below). The first build of a project takes 2 to 15 minutes; later builds are incremental. Run `run` again after native changes (a new native dependency, config plugins, `app.json`). Details per platform: [references/ios.md](references/ios.md) and [references/android.md](references/android.md).

## In T3 Code: show it to the user

- After `up` or `run`, call `device_open` so the user watches every tap live in the Device panel. For iOS, `mac-sim t3` prints the `hostId` and `deviceId` to pass (the hostId is macbox's SSH device host in T3's settings). For Android, use `hostId: "local"` with `deviceId` from `android-sim serial`. Both commands print this reminder when they run inside T3 Code. `device_list` shows every device if you're unsure.
- Keep driving with `mac-sim ad ...` / `android-sim ad ...`. On iOS, don't also use the `agent-device` command that `device_open` returns: two sessions on one simulator refuse each other (`DEVICE_IN_USE`). On Android both work.
- `device_screenshot` is fine for a quick look. For anything you judge, use `shot`, which is lossless at the simulator's own pixels.
- The panel's stream costs CPU. Call `device_close` (without `shutdown`) when the user no longer needs to watch, and `down` when the task is done.

## Verify every change: the simulator loop

A screen doesn't exist until you've seen it running. Code review, a passing build and "it should work" prove nothing about what the user sees or how it moves. After **every** change to a screen, an interaction or an animation, run this loop before you move on, and again before you call the work done:

1. **Run it.** `run` (or let Fast Refresh deliver a JS edit), then reach the screen.
2. **Screenshot it and actually look.** Open the PNG; don't trust your memory of the code. Check alignment, spacing rhythm, truncation with long content, the safe areas and the Dynamic Island, dark and light mode, Dynamic Type at XL, and the empty, loading and error states.
3. **Record the whole flow, not just the hero moment.** Start the recording, drive the flow inside it, then measure:
   ```bash
   mac-sim record /tmp/flow.mp4 10 &    # or: android-sim record /tmp/flow.mp4 10 &
   mac-sim ad press @e4; mac-sim ad swipe ...   # drive the flow within those seconds
   wait
   sim-fps /tmp/flow.mp4
   ```
   Exercise all of it: every transition, push and pop, and tab switch. Try every back path (the iOS edge swipe, Android's back), and after a one-way door (sign-in, onboarding done, purchase) a back that must *not* re-enter the old state. Present, drag, dismiss and cancel mid-drag every modal and sheet. Bring the keyboard up and down. Hit every press state, then add rapid taps and scroll flings at the ends of lists.
4. **Measure, don't eyeball.** `sim-fps` must report **60 fps in every stretch of motion, 0 dropped frames**. Then look at the frames themselves ([references/verify.md](references/verify.md) shows how), hunting for:
   - one-frame flashes: white or unstyled first paint, a wrong-theme or wrong-color frame mid-transition;
   - layout jumps, double-render pops, and springs that clip or overshoot into content;
   - a keyboard jump-cut, and elements that reflow after they appear.

   One bad frame means the flow isn't done.
5. **Fix, re-run, re-verify.** Make a few fixes at a time, never a big batch, because regressions hide in batches. Stop at "I can't find a flaw", not at "looks fine".
6. **Before you report it done**, re-run the loop on a **Release build** (`MODE=release ... run`): debug builds and Expo Go add jank of their own and hide the real kind. Then go through the checklist in [references/verify.md](references/verify.md).

Report what you verified: the screenshots and recordings you took, and what `sim-fps` printed.

### Where 60 fps is real here

The iOS Simulator draws on the host's GPU through the VM's virtual GPU, so the host's GPU sets the ceiling:

- **Measure motion on a 1x iOS simulator** (`slim-1`, `slim-2`, `full`). Example, measured on an Intel Arrow Lake iGPU (Core Ultra 200S) on 2026-10-28: 1x simulators reached about 92 to 96 frames/s in a heavy Liquid Glass benchmark, well above 60.
- **`sharp` and `small` are 3x.** They have 9 times the pixels, so heavy scenes can fall below 60 because of the host's GPU, not your app (about 50 frames/s on that same iGPU). Use them for still screenshots, not for frame-rate verdicts.
- **Other simulators animating at the same time share the GPU.** If `sim-fps` shows drops, check `mac-sim status` / `android-sim status` and record again. Record with nobody watching the Device panel too, when you can.
- **A stretch `sim-fps` calls "still or frozen"** may be the screen standing still, or the app freezing. Look at the frames on both sides of it.

## Rules

- **Close it when the task is done: `mac-sim down` / `android-sim down`.** The pools are shared with other agents and the user. Idle iOS simulators shut down after 20 minutes without a `mac-sim` command or a viewer; a forgotten Android emulator stops after 6 hours.
- **Snapshots are the truth.** Refs (`@eN`) change with the screen; take a new snapshot before each tap.
- Use your checkout's simulator only. Don't erase or reset pool simulators, and don't restart CoreSimulatorService (it shuts down every simulator on the Mac). Don't run Simulator.app or `npx expo run:ios` on the Mac: Simulator.app opens a window per simulator and doubles the GPU work. An Android emulator the user opened from the Device panel is theirs; use it only when they ask.
- **The `full` iOS simulator is also the user's own.** Don't change its settings or erase it; `mac-sim down` leaves it running.
- If the Mac doesn't answer (`mac-sim` says the VM is down), run `macbox status`; `macbox up` starts it in about 2 minutes. If it won't start, tell the user.

## References

| File | Read it for |
|---|---|
| [references/ios.md](references/ios.md) | The iOS pool and its kinds, how `mac-sim run` builds, Expo Go, monorepos, the idle shutdown, failures, files |
| [references/android.md](references/android.md) | The Android pool, setting it up, builds, Metro ports, Expo Go, failures, files |
| [references/verify.md](references/verify.md) | The done checklist, frame-by-frame inspection, `perf`, the device matrix |
