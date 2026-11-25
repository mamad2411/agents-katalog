---
name: vibeview-agent
description: Build, run, drive and test a mobile or TV app on live cloud devices with VibeView - iOS, Android, Apple TV, Android TV and Roku. Use when asked to verify a change on a device, run the app on a simulator or emulator, build it in the cloud (including iOS without a Mac), check a React Native, Expo, Flutter or native app or a Roku channel, or create and run tests for it.
---

# VibeView agent control

VibeView runs your app on cloud iOS, Android, Apple TV, Android TV and Roku
devices (simulators and emulators). From the `vibeview` CLI, or its MCP server,
you can build the app in the cloud, start a session, drive the UI, read logs,
and run saved tests, so you can check that a change actually works, not just
that it compiles. Requires the `vibeview` CLI installed and signed in
(`vibeview login`, or `VIBEVIEW_API_TOKEN` set); `vibeview whoami` tells you
which account and organization you are using.

## 1. Get the app onto a device

Pick the first row that fits, then start a session (section 2).

| Situation | Do this |
|-----------|---------|
| The newest build on VibeView already contains your change, or it is a React Native/Expo debug build and you changed only JS or assets | Nothing to build. A debug build loads your JS from local Metro and hot-reloads it. Find the app with `vibeview list-apps` (MCP: `list_apps`) and its builds with `vibeview list-builds <app>` (MCP: `list_builds`). |
| You have a build file that contains your change (simulator `.app` zipped, `.apk`, Roku channel `.zip`) | `vibeview upload-app <file>` (MCP: `upload_app`). |
| A native change in a React Native/Expo app, or any code change in a Flutter, Capacitor, Kotlin Multiplatform or native app, and this machine can build it (Xcode for iOS/Apple TV) | `vibeview dev --build`. It runs the `development` profile's command from `vibeview.json` here, uploads the result, then starts the session. `vibeview build` builds and uploads without a session. |
| The same kind of change, but no Mac or no toolchain here | Cloud build: `vibeview build --cloud` (section 1.1). This is the iOS path from Linux or Windows. |
| Roku channel | Not cloud-built. Required: a `platforms.roku.build.profiles.development` entry in `vibeview.json` (`command` packages the zip, `artifact` is its path). Without it `vibeview dev --platform roku` refuses to start. With it, `vibeview dev --platform roku --build --detach --json` packages and uploads the channel itself, and `dev-reload` reinstalls it after an edit (section 3). |

Build rules — a build that breaks these installs and then crashes or is
refused:

- **iOS and Apple TV**: a **simulator** build (`-sdk iphonesimulator` or
  `-sdk appletvsimulator`, `CODE_SIGN_IDENTITY=-`) with the `arm64` slice,
  never a device `.ipa` or archive. `CODE_SIGN_IDENTITY=-` signs it to run
  locally (no certificate needed); an unsigned build
  (`CODE_SIGNING_ALLOWED=NO`) can't use the Keychain, so `expo-secure-store`
  fails.
- **Android and Android TV**: an `.apk` (an `.aab` can't be installed) that
  keeps the `x86_64` slice (and `x86` for Android TV) if the app has native
  code. Standard `./gradlew assembleDebug` output has it.

Upload warnings and the build page say when a build can't run (wrong
architecture, a device build), so read them. Details:
https://vibeview.io/docs/preparing-your-build.

**Debug or standalone.** A React Native or Expo *debug* build loads its JS
from Metro on this machine: that's the dev loop with hot reload, and it needs
Metro running. Every other build (a release or `preview` build,
a Flutter, Capacitor, Kotlin Multiplatform or native app) runs **standalone**:
start it with `vibeview dev --standalone` (MCP: `dev_start` with
`standalone: true`). Code changes don't hot-reload there; rebuild instead.
`list-builds` shows each build's kind (`debug`, `release`, `unknown`).

### 1.1 Cloud builds

`vibeview build --cloud` uploads the project source and runs a build
profile's command on a clean cloud builder. The result lands in the app's
build history, ready to run. The upload is every git-tracked file plus every
untracked file `.gitignore` doesn't exclude, so a stray local `.env` goes
too. `node_modules`, `ios/Pods` and `.git` never do. Add paths to a
`.vvignore` file (same syntax as `.gitignore`) to keep more out.
Builds are billed by the minute: ask the developer before starting one.
There is no MCP tool for builds: an agent with only MCP asks the developer to
run `vibeview build --cloud`, then finds the result with `list_builds`.

```bash
vibeview build --cloud --json                      # defaultPlatform, development profile
vibeview build --cloud --platform ios --json
vibeview build --cloud --platform ios --profile preview --json   # runs without Metro
```

Build only the platform you will run. `--platform all` builds, and bills,
every configured platform.

- **Profiles** live in `vibeview.json` under
  `platforms.<platform>.build.profiles.<name>`, each with a `command` and an
  `artifact` (a project-relative path; `*` is allowed in the file name).
  Three names are conventional. `development` is the default and what
  `vibeview dev` runs (a debug build for React Native/Expo). `preview` is
  the same build in Release with the JS inside, so it runs standalone.
  `production` is a signed store build that VibeView devices can't run.
  Other names work too.
- **Run it from the project root.** The command runs in a clean
  environment, so it must install dependencies itself (`npm ci`,
  `yarn install --immutable` for Yarn 2+, `yarn install --frozen-lockfile`
  for Yarn 1 with `"packageManager": "yarn@1.x"` in package.json (without
  it, `npx --yes yarn@1 install --frozen-lockfile`: the builders' default
  Yarn is 2+), `pnpm install --frozen-lockfile` or `bun install`, plus
  `pod install` for a bare iOS build).
- **Under `--json` nothing prompts.** A missing profile is an `error` event
  with `code: "config_required"` whose message names the key to add (e.g.
  `platforms.ios.build.profiles.preview {command, artifact}`): add it to
  `vibeview.json` and rerun. A project with no app yet gets one created from
  the build, and its `appId` is written to `vibeview.json`. Never link a
  project to a sample app (`is_sample: true` in `list-apps --output json`):
  every account starts with sample apps (Atlas; older accounts also TV
  Catalog and JetStream), and none of them is the developer's app. Show
  the developer any `vibeview.json` change you make.
- **Expo**: a managed project (no `ios/` or `android/` folder) builds with
  `npx expo prebuild --platform <p>` followed by `xcodebuild` or Gradle in the
  same command. Never use `npx expo run:ios` / `run:android` as a cloud build
  command: they need a local device and fail. Metro for the dev loop is
  `npx expo start`. Ready-made commands per framework:
  https://vibeview.io/docs/cloud-builds#frameworks.
- **Xcode and Node** can be chosen per run with `--xcode <version>` (iOS,
  Apple TV) and `--node <major>`; a version that isn't available is refused
  before anything is charged and the error lists the choices.

**Waiting and reading the result.** With `--json`, stdout is NDJSON. You
get `build_created` (the cloud build `id`), `status` (`queued`, then
`running`), `build_log` and `warning` events. While a build is queued, the
`queued` status event carries `queue` (`reason`: `builders_busy`,
`org_limit`, `builders_offline` or `starting`; `position` in line, 1 when
none is ahead; `limit`, the plan's builds at once), and a `queue` event
(`id`, `queue`) follows whenever that changes. `vibeview builds logs <id>
--follow --json` emits the same `status` and `queue` events. Each build ends with one
`build_finished` event. It carries `status`, `error_summary`,
`app_public_id`, `app_build_id` (the uploaded build it produced) and
`launch_warning`. A non-null `launch_warning` means the build won't launch
(for example an iOS 27 SDK build without the scene life cycle): fix that
before running it. Exit code 0 means every build succeeded. On failure, read
the log before changing anything:

```bash
vibeview builds list --json              # recent cloud builds, with status
vibeview builds logs <id>                # a build's log
vibeview builds logs <id> --follow       # stream until done; exit 1 if it failed
```

With `--no-wait` it prints the ids and exits; follow up with
`builds logs <id> --follow`. A build can succeed and still be unable to run
on VibeView devices (for example a device build); its result says why.

**Running it.** Pass `app_build_id` from `build_finished` (or an id from
`list-builds`):

```bash
vibeview dev --platform ios --build <app_build_id> --detach --json               # development (debug) build, with Metro
vibeview dev --platform ios --standalone --build <app_build_id> --detach --json  # preview or any other non-debug build
```

Pass the `--platform` the build was made for. Without it `dev` uses
`defaultPlatform`, and a build of another platform's app is refused.

MCP: `dev_start` with `build_id` (plus `standalone: true` for a non-debug
build). Plain `vibeview dev` with no `--build` already picks the app's newest
debug build, cloud-built ones included.

A signed store build is made with `--production` and sent to the stores with
`vibeview submit`; that is a release task for the developer, not part of
verifying a change.

## 2. Start a session

1. For a React Native/Expo dev session, start Metro in the project
   (`yarn start`, `npx expo start` or equivalent) and leave it running. Not
   needed with `--standalone` or on Roku.
2. Start a dev session in the background and get structured output. No
   `vibeview.json` yet in this project (first run here)? Pass `--platform`
   (`ios`, `android`, `tvos`, `androidtv` or `roku`) and `--app` explicitly —
   non-interactive runs never prompt, so both must be given up front (`--app`
   is the `app_id` from `upload-app` or `list-apps`):
   ```bash
   vibeview dev --platform ios --app <app_id> --detach --json
   ```
   Once `vibeview.json` exists (this run or an earlier one), a bare
   `vibeview dev --detach --json` reruns the same platform/app. A
   `{"event":"error","code":"config_required",...}` line names exactly what's
   still missing (usually `--platform` or `--app`) — pass it and retry. In an
   account whose only apps are samples, a bare `vibeview dev --json` with a
   build command in `vibeview.json` builds and uploads the app itself (this
   can take minutes; under `--detach` it logs to `.vibeview/dev-detach.log`),
   and without one it ends with `code: "no_apps"`: build or upload the app
   first. Add
   `--model "<name>"` for an exact device model (`vibeview list-devices
   --models`) or `--device-category tablet` for a tablet.
3. Parse the `session_ready` line from stdout:
   ```json
   {"event":"session_ready","session_id":"...","url":"...","pid":1234,"build":{...}}
   ```
   Use `session_id` as `--session <id>` on every verb below. The event
   fires once the session accepts commands (device up, app installed) —
   no need to poll `dev-status` first. If every device is busy, it waits in
   the queue first (`queued` events) rather than failing. `build` says which
   build was installed (`build.build`), why (`build.reason`: it prefers a
   debug build of the project's own app version over a newer one of another
   version), and the newest debug build of each other version
   (`build.other_debug_builds`). If the app shows a red error screen right
   after start ("React Native version mismatch", or "undefined is not a
   function" in a native module), the build may be from other native code —
   rerun with `--build <id>` of one of those.
4. **Immediately tell the developer the session `url`** — "watch or take
   over at any time: `<url>`". The page is a live, fully interactive view
   of the device; the developer watching along is a feature, not a risk.
   (For a session you attached to with `--session` instead of starting,
   the page is `https://vibeview.io/sandbox/<session_id>`.)

Running `dev` writes two things into the project root: a `.vibeview/`
directory (live session state, plus `local.json` with this developer's own
flag overrides such as `--metro-port` — local machine state, never commit)
and a `vibeview.json` (the platform/app/build setup, which teammates DO
want). Flags never rewrite a value `vibeview.json` already has; they are
saved to `.vibeview/local.json` instead, and the CLI prints what it saved.
The CLI keeps `.vibeview/` out of git itself with a `.vibeview/.gitignore`
(everything except `test-spec.json`); don't add lines to the project's own
`.gitignore` for it. Leave `vibeview.json`
tracked, but tell the developer you created it rather than letting it
appear unexplained in their `git status`.

## 3. Verifying

- **Always run `ui-tree` first** — every ref (`@e5`) the UI exposes comes
  from here. Never guess a ref.
  ```bash
  vibeview ui-tree --session <id>
  ```
  An empty or near-empty first tree usually means the app is still booting
  (splash screen, fetching remote config) — NOT a broken session. Take a
  screenshot to confirm, `wait`, and fetch the tree again before concluding
  anything is wrong.
- Act on the screen using refs from the tree:
  ```bash
  vibeview tap @e5 --session <id>
  vibeview type "hello@example.com" --session <id>
  vibeview scroll down --session <id>
  vibeview press back --session <id>
  ```
- **Read the observation in every response before deciding the next
  action.** Every mutating verb returns one of: screen unchanged, a
  `+`/`~`/`-` diff with fresh `@e` refs, a full tree, or an "unavailable"
  warning. Refs go stale the moment the screen changes — a stale ref is
  refused. **The refusal does NOT include the current screen**: because the
  action never ran, the observation comes back as "screen unchanged" with no
  tree, so run `ui-tree` again to get live refs before retrying. Never reuse
  a ref from a previous observation.
- **Take a screenshot whenever you changed how something LOOKS.** The UI
  tree proves an element exists, has the right text, and occupies the right
  rect — it says nothing about colour, contrast, or whether something is
  hidden behind another view, so a screen can pass every check the tree can
  express and still be visibly broken (text the same colour as its
  background, a view drawn on top of another). Tree for structure and refs;
  screenshot for appearance.

  **Actually look at the image** — confirming the file was written proves
  nothing about how it renders.
  ```bash
  vibeview screenshot --out ./check.png --session <id>   # then open it
  ```
  Over MCP, `screenshot` only writes the file and returns its path unless
  you pass `inline: true`, which returns the image itself (under 1 MB — a
  JPEG when the PNG is large — at the same size, so its pixels are still tap
  coordinates). If you cannot
  open files on the machine running the server, `inline: true` is the only
  way you will ever see the screen. It costs a lot of context, so use it
  when appearance matters — not to confirm a tap landed, which the
  response's observation already tells you.
- **When something breaks — a crash, a frozen screen, an unexpectedly empty
  tree — read the app logs before guessing.** `logs` returns the app's own
  output from the device: JS console lines, native errors, and crash
  messages (not full system logs, and not Metro's terminal — native crashes
  never appear there). The response ends with a `cursor`; pass it back as
  `--since` to see only lines that arrived after your last read, which is
  the natural loop for "did my action log what I expected".
  ```bash
  vibeview logs --session <id>                 # recent lines (default 100)
  vibeview logs --since 42 --session <id>      # only lines after cursor 42
  ```
- **Off-screen elements**: use `scroll-to <text>` rather than repeating
  `scroll down`. It scrolls until an element whose label, value, or
  accessibility id contains that text is visible, and stops early when the
  content stops changing (end of list). Omit `--direction` for vertical
  lists (it auto-detects); pass it explicitly for horizontal strips.
  ```bash
  vibeview scroll-to "Delete account" --session <id>
  ```
  A `scroll-to` that never finds its text, or a `type` whose field does not
  end up holding the text, prints `error` and exits 1 — check the reason
  line and the screen before retrying.
- **Precise two-point gestures** (sliders, drag-and-drop reorder, map
  panning) need `drag` — `swipe`/`scroll` are direction-only and can't
  express them. Each end is independently a ref or `x,y`:
  ```bash
  vibeview drag @e5 @e9 --session <id>
  vibeview drag 100,400 300,400 --session <id>
  vibeview drag @e5 300,400 --press-ms 500 --session <id>
  ```
  Use `--press-ms 500` or more for long-press-to-reorder lists, and
  `--velocity 150` for slow, precise slider adjustments.
- **System alerts** (permission prompts and similar) sit above the app
  and block it. Call `alert get` first to read the message and the exact
  button labels, then act on one:
  ```bash
  vibeview alert get --session <id>
  vibeview alert accept --button "Allow" --session <id>
  ```
  On Apple TV this also covers the "Open in …?" prompt a deep link raises;
  the button is answered with the remote.
- Use `set-location --lat 51.5074 --lon -0.1278` to place the device before
  a location-based flow (maps, store finders, region-gated screens); the app
  reads it like a GPS fix. Not on TV.
- Use `set-language <tag>` (`de`, `ja`, `pt-BR`, … or `default`) to restart the
  app in another language — for checking translations or localized
  screenshots. Only the app changes; old refs are stale after it. iPhone, iPad,
  Apple TV and Android 13+; not Roku or embed sessions.
- Use `set-status-bar clean` before App Store screenshots: 9:41, a full
  battery and full Wi-Fi and cellular signal, kept for the rest of the session
  (`set-status-bar default` puts the real one back). iOS phones and tablets
  only.
- Use `open-url` to jump straight to a deep link instead of navigating by
  hand:
  ```bash
  vibeview open-url "myapp://settings" --session <id>
  ```
- **TV apps**: start the session with `--platform tvos` (Apple TV) or
  `--platform androidtv` (Android TV). Navigate with the d-pad via `press`
  (`dpad_up`/`dpad_down`/`dpad_left`/`dpad_right`/`dpad_center`), or move
  focus directly with `tap-focused` (moves focus AND activates) / `focus`
  (moves focus only, no activation).
- **Foldables**: any model `vibeview list-devices --models` (MCP:
  `list_device_models`) marks form factor `foldable` — the iPhone Duo,
  Android foldables such as the Pixel 9 Pro Fold. Start on one by its exact
  model name from that list, e.g.
  `vibeview dev --detach --json --model "iPhone Duo"` or
  `vibeview dev --platform android --detach --json --model "Pixel 9 Pro Fold"`
  (MCP: `dev_start` with `model`). It starts closed, on the cover screen. Fold with a preset
  or an exact hinge angle, and rotate:
  ```bash
  vibeview set-posture open --session <id>        # closed | partial | open
  vibeview set-posture --angle 75 --session <id>  # 0 (shut) to 180 (flat)
  vibeview rotate --session <id>                  # Duo: quarter turn clockwise
  vibeview rotate --degrees 270 --session <id>    # Duo: quarter turn back (180: half)
  ```
  Each response says where the device ended up — posture, angle and which
  screen is lit (`cover` or `inner`; the device decides — on the Duo a small
  angle can keep the inner screen lit on the way down), or the new
  orientation. The posture names come from each device's own angle ranges,
  so trust the reported `posture` over the angle you asked for: the Duo
  reads 0 as `closed` and 170 up as `open`; in between it depends on how the
  hinge got there (moved in one go it switches at about 85 degrees, moved in
  small steps it keeps the screen it had); an Android foldable uses its own
  ranges (the Pixel 9 Pro Fold: 0-30 `closed`, 31-149 `partial`, 150 up
  `open`) and its inner screen whenever it is not closed. An Android foldable rotates like a phone. Folding
  switches screens of different sizes and rotating turns the picture, so run
  `ui-tree` afterwards — old refs are stale. On other phones and tablets
  `rotate` toggles portrait/landscape (only 90 is accepted); TV devices don't
  rotate.
- **Roku channels**: start the session with
  `vibeview dev --platform roku --detach --json` (or `dev_start` with platform
  `roku` over MCP); after an edit run `vibeview dev-reload` (MCP:
  `dev_reload`) to re-package, upload and restart the channel in the same
  session — about five seconds. `vibeview dev --roku-debug` is for a person
  debugging in VS Code, not for you: use plain `dev --platform roku --detach`
  plus `dev-reload` (which refuses a debug session). Use `dev-reload` after
  your edits rather than `--watch`: `--watch` reloads on every save, which
  suits a person, not an agent that edits several files. The remote's
  names are `press up/down/left/right/select/back`
  (`dpad_*` also works), plus `enter`, `backspace` and the media keys `play/rewind/forward/replay/info`; `home` is refused (the session stays in your channel); `relaunch-app` restarts the channel with its launch parameters; `clear-text` is unavailable. `type` lands in a focused
  on-screen keyboard; the typed text shows up in the tree as the text box's
  child label, which is what the response verifies against. `logs` returns
  the channel's console output (its `print` lines, why it exited, and the
  error plus backtrace after a runtime error); `open-url` is unavailable. A
  Back on the channel's root
  screen exits it; the session relaunches it within seconds, so a fresh
  first screen after `press back` is not a crash.

## 4. When only a human can act — stop and hand off

Some screens need things you must never guess or invent: **login
credentials, 2FA/OTP codes, CAPTCHAs, destructive confirmations
("Delete account?"), anything payment- or real-account-shaped.** When you
hit one:

1. **Stop driving.** Do not type guessed credentials, do not tap through a
   destructive confirmation to "see what happens".
2. **Ask the developer, naming exactly what you need and where**: "I'm at
   the login screen — please sign in at `<session url>` and tell me when
   you're done." The session page is fully interactive; the developer can
   drive the device directly while you wait.
3. **On resume, run `ui-tree` FIRST** — the human just changed the screen,
   so every ref you held is stale — and **verify the blocker is actually
   gone from the tree** (e.g. the login form is absent) instead of trusting
   the confirmation alone. If it's still there, say what you still see and
   ask again.

### When VibeView itself gets in your way

If VibeView — not the user's app — gets in your way (an error you can't
explain, a missing capability, confusing output), offer to tell the VibeView
team. Show the user what you will send and send it only with their OK:

    vibeview feedback bug "dev_start says build not found for a build I just uploaded" \
      --details "upload-app returned build 123; dev --build 123 failed" --session <id>

`kind` is `bug`, `friction` (worked, but confusing, slow or awkward) or `idea`.
Never include passwords, tokens, test data values or personal data. Over MCP
the same tool is `send_feedback`.

## 5. Tests

A test is a list of plain-language steps; a step starting with "Verify" is a
check. Write one when the developer asks for a repeatable check, not to
verify a one-off change (driving the session does that).

- **AI runs are beta and use usage credit.** The first run of a new test is
  driven by the AI agent; once it passes, later runs replay the saved path
  and use AI only where the screen changed. Ask before starting AI runs.
- **Never put real credentials in steps.** Use `{{key}}` placeholders whose
  values the developer stores as test data in the dashboard.
- **A run on a new device needs a build that runs without Metro.** A React
  Native debug build without its JS inside stops at its error screen there.
  Run such tests against a `preview` (or other release) build. Without
  `--build`, a run prefers a build that runs on its own, and falls back to a
  debug build with a warning. A run on a session you hold (`run_test` with
  `session_id`) uses that session's app, Metro included.

From a shell:

```bash
vibeview create-test "Sign in" --app <app_id> \
  --steps '["Tap Sign in", "Type {{email}} into Email", "Verify the home screen shows"]' --output json
vibeview run-test <test-id> --output json            # new device, waits for the result
vibeview run-test <test-id> --build <id> --mode replay
vibeview list-suites                                 # groups (the CLI calls them suites)
vibeview run-suite <suite-id> --output json
```

`create-test` reuses an identical test and refuses a different one with the
same name; pass `--if-exists update` (or `new`, `fail`) to choose, and
`--group <id>` to add it to a group. `run-test` and `run-suite` always start
their own device and stop it afterwards; exit code 0 = passed, 1 = a test
failed, 2 = the run couldn't run. `--mode` is `hybrid` (Smart, the default),
`ai` (AI only) or `replay` (No AI: no AI and no usage credit; a step with no
saved path is reported as not checked). `--platform android` runs an iOS
test's app on Android (same form factor), and `--retry` retries a failure
once.

Over MCP: `create_test`, then `run_test` (or `run_group`), then `get_run`.
`get_run` answers at once, and a run takes minutes. While it says the run
is still in progress, space the calls out (for example, about 30 seconds
apart) rather than calling it back to back. With a shell, prefer
`vibeview run-test`, which waits for the result itself. `run_test` with
`session_id` runs on a session you hold, the device you are driving; without it, it starts and stops its own device. See
section 8.

## 6. Cleanup

**Always** stop the session when done verifying — a running session bills
streaming minutes even when idle:
```bash
vibeview dev-stop
```
If the `dev --detach` process is killed or the computer sleeps, its session
ends on its own within about 90 seconds (unless a browser tab is watching
it) — but don't rely on that; stop it.
A session nobody uses also ends on its own after the organization's idle
timeout (30 minutes by default). Only device actions (tap, type, swipe,
press, …) and app reloads count as use; `ui-tree`, `screenshot`, `logs`,
`find` and `wait` do not, and neither does keeping `dev --detach` running.
A session you did not start with `dev` (one created through the API, the
sandbox, or a collaboration link) is stopped by id:
```bash
vibeview stop <session-id>
```

## 7. Command reference

Every verb accepts `--session <id>` to target a specific session (falls
back to the current project's `vibeview dev --detach` session if omitted)
and `--json` to print the raw response envelope as one JSON line instead of
human-readable text.

| Verb | Args | Purpose |
|------|------|---------|
| `ui-tree` | — | Fetch the ref-annotated UI tree for the current screen. |
| `logs` | `[--tail <n>] [--since <cursor>]` | Read recent app logs from the device (JS console, native errors, crash messages). The response's `cursor` feeds the next call's `--since`. |
| `screenshot` | `[--out <path>]` | Capture a screenshot of the current screen and save it to disk. On a phone or tablet its pixels are tap coordinates: a point read off it can be tapped as is — never rescale. |
| `tap` | `<target>` | Tap an element by ref (e.g. `@e5`), or coordinates (e.g. `100,200`) in the space of the tree's rects and the screenshot's pixels. |
| `long-press` | `<ref>` `[--ms <n>]` | Long-press (touch and hold) an element by its ref. |
| `swipe` | `<direction>` `[--distance <short\|medium\|long>]` | Perform a scrollbar-semantic swipe gesture in one of four directions. |
| `scroll` | `<direction>` | Scroll the current view up, down, left, or right using a gesture preset. |
| `scroll-to` | `<text>` `[--direction <up\|down\|left\|right>] [--max-scrolls <n>] [--element-type <type>]` | Scroll until an element matching the text is visible. Stops at end of list. |
| `drag` | `<from>` `<to>` `[--velocity <n>] [--press-ms <n>] [--hold-ms <n>]` | Drag between two points, each an `@ref` or `x,y`. The only precise two-point gesture. |
| `alert` | `<get\|accept\|dismiss>` `[--button <label>]` | Inspect or respond to a system alert on iOS or Apple TV. |
| `type` | `<text>` | Type text into the currently focused input field. On a phone or tablet a line break presses Enter and submits the field (`$'query\n'`), like `press enter`. |
| `clear-text` | — | Clear the text in the currently focused input field. |
| `press` | `<button>` | Press a device button or perform a system gesture (home, back, d-pad, etc). |
| `open-url` | `<url>` | Open a deep link in the app under test, never a browser. Android: a link the app has no screen for fails. iOS/Apple TV: only the app's own URL scheme (`myapp://...`); a web or system link is refused. |
| `relaunch-app` | — | Close the app and start it again (cold start, data kept) — for "does it persist after a restart" checks. The app log keeps streaming. Not on embed sessions. |
| `set-posture` | `<closed\|partial\|open>` or `--angle <0-180>` | Fold or unfold a foldable device (form factor `foldable`: the iPhone Duo, Android foldables) to a preset or an exact hinge angle — exactly one. Reports posture, angle and lit screen. Errors on a device without a hinge. |
| `rotate` | `[--degrees <90\|180\|270>]` | Rotate the device and report the new orientation. Phones/tablets and Android foldables toggle portrait/landscape (90 only); the iPhone Duo turns a quarter clockwise by default. Not on TV. |
| `shake` | — | Shake the device once, like the dashboard's Shake button, to open an app's shake-triggered menus (a bug-report screen, the React Native developer menu in a debug build). Phones, tablets and foldables; not on TV or embed sessions. |
| `set-language` | `<tag\|default>` | Restart the app in another language (`de`, `pt-BR`, …) or the device's (`default`). Only the app changes. iPhone, iPad, Apple TV, Android 13+; not Roku or embed sessions. |
| `set-status-bar` | `<clean\|default>` | Show the clean screenshot status bar (9:41, full battery and signal) or the device's own. iOS phones and tablets only. |
| `set-location` | `--lat <n> --lon <n>` | Set the device's simulated GPS position (decimal degrees; west and south are negative) for location-based flows. Phones, tablets and foldables; not on TV. |
| `wait` | `[--ms <n>]` | Wait for a specified number of seconds before continuing (default: 2s). |
| `find` | `<text>` `[--below <text>] [--above <text>] [--near <text>]` | Find an element by text with optional spatial constraints. |
| `tap-focused` | `<ref>` | TV: move focus to an element and press SELECT in one step. |
| `focus` | `<ref>` | TV: move focus to an element without activating it. |

Dev-loop lifecycle commands (not registry verbs, but needed for every run):

| Command | Purpose |
|---------|---------|
| `dev --detach --json` | Start a device + Metro-tunnel session in the background, emitting `session_ready`/`warning`/`error` JSON events on stdout. Add `--model "<name>"` to pick an exact device model. |
| `dev --build <id>` | Run that uploaded build instead of the app's newest debug build (combine with `--app`, `--platform`, `--model`, `--detach --json`). Only a debug build (kind `debug` in `list-builds`) is accepted, including a debug build with its JS bundle embedded; a release build is refused (run it with `--standalone`). Not on Roku. |
| `dev --build` | With no id: run the `development` profile's build command on this machine, upload the result, then start the session. Needs the local toolchain (Xcode for iOS); use `build --cloud` otherwise. |
| `dev --standalone` | Run a build as it is, with no Metro and no tunnel: a release or preview build, or any non-React Native app. With `--build <id>` that build; without, the app's newest release build. Not on Roku. |
| `build --cloud` | Build a `vibeview.json` profile on a cloud builder and add the result to the app's builds: `--platform <p>\|all`, `--profile <name>`, `--json` (NDJSON; `build_finished` carries `app_build_id`), `--no-wait`, `--download`, `--xcode`, `--node`. Without `--cloud`, `build` runs the command locally and uploads. |
| `builds list` / `builds logs <id>` | Recent cloud builds and their status; a build's log (`--follow` streams until it ends and exits 1 if it failed). Also `builds download <id>` and `builds cancel <id>`. |
| `upload-app <file>` | Upload a zipped simulator `.app`, an `.apk` or a Roku channel `.zip`; prints the `app_id`. `--note` labels the build, `--output json` for structured output. |
| `list-apps` | List the organization's apps: id, name, platform, bundle id / package; sample apps are marked (`is_sample` in `--output json`). |
| `list-builds <app>` | List an app's uploaded builds, newest first: id, version (build number), platform, kind (`debug`/`release`/`unknown`), upload time, expiry (the **Expires on** date, `expired`, or `—` when it has no **Expires on** date yet: not due, **Keep** on, or the app's newest build), note. `--json` prints an array. |
| `list-devices --models` | List the device models you can start (the names `--model` takes); foldables are marked `foldable`. |
| `dev-status` | Check on the current project's detached dev session. |
| `dev-stop` | End the current project's detached dev session. |
| `vibeview stop <session-id>` | End any session by id — one created through the API, the sandbox, or a collaboration link. |
| `dev-reload` | Roku only: re-package, upload and restart the channel in the detached session (the `r` key of the foreground loop). |
| `vibeview feedback <bug\|friction\|idea> "<summary>"` | Send the VibeView team a report about VibeView itself (not your app), only after the user OKs it: `--details`, `--session` (defaults to the detached session, if any), `--quote` (the user's own words). Works with no session. |
| `create-test` / `run-test` / `list-suites` / `run-suite` | Tests from a shell (section 5). |
| `whoami` | Show the signed-in account and organization. |

The CLI also has store-submission commands (`submit`, `submissions`,
`testflight`) for shipping a signed production build. Leave those to the
developer unless they ask; run `vibeview submit --help` for the current
options.

## 8. If you're calling VibeView over MCP

Everything above is also exposed as MCP tools by `vibeview mcp`, so an agent
with no shell can run the whole loop. Tool names are the CLI verbs with
hyphens replaced by underscores (`ui_tree`, `tap`, `scroll_to`, `long_press`,
`clear_text`, `open_url`, `tap_focused`, ...), each taking its args by name
(`tap {ref: "e5"}` or `tap {target: "100,200"}`, `scroll_to {text: "..."}`,
`drag {from: "@e5", to: "300,400"}`, `alert {action: "get"}`) plus an
optional `session_id`.

These tools exist **only** over MCP, with no registry verb — they cover the
steps the CLI does with plain shell commands:

| MCP tool | Args | Purpose |
|----------|------|---------|
| `upload_app` | `file` (required path), `name` | Upload a build (zipped iOS/tvOS simulator `.app`, Android/Android TV `.apk`, Roku channel `.zip`). The MCP equivalent of `vibeview upload-app`, so getting the app onto a device needs no shell. Returns the `app_id` to pass to `dev_start`. |
| `list_apps` | `platform` | List the org's apps (app id, name, platform, bundle id, `is_sample`). The MCP equivalent of `vibeview list-apps` — use it to find an app someone else uploaded. |
| `dev_start` | `platform` (required: `ios`/`android`/`tvos`/`androidtv`/`roku`), `app`, `metro_port`, `model`, `build_id`, `standalone` | Start a session held open by the MCP server. The MCP equivalent of `vibeview dev --detach`; `model` picks an exact device model (e.g. `"iPhone Duo"`); `build_id` runs that build instead of the newest debug one (see `list_builds`). `standalone: true` runs any build as it is with no Metro — a release or preview build, or a non-React Native app (without `build_id`: the newest release build). An app for another platform is refused before a device is taken. Returns `page_url` — relay it to the developer immediately, same as step 4 of section 2 — the device it got (model, OS, category; posture and lit screen on a foldable), and the build it installed (id, version, upload time) with the app's other debug builds. It chooses the build the way `vibeview dev` does (a debug build of the project's own version over a newer one of another version) and says when it can't read the project's version. A red error screen right after start ("React Native version mismatch", or "undefined is not a function" in a native module) may mean the build was made from other native code: try one of the listed other builds with `build_id`. While every device is busy it waits in the queue, sending progress. |
| `list_device_models` | `device_type` | List the device models you can start (model, OS, platform, category, `foldable` marker, and how many are free/busy). The MCP equivalent of `vibeview list-devices --models`. |
| `list_builds` | `app` (required) | List an app's uploaded builds with their kind (`debug`/`release`/`unknown`). The MCP equivalent of `vibeview list-builds`. |
| `dev_stop` | — | Stop the session `dev_start` started. The MCP equivalent of `vibeview dev-stop`. Says "no dev session was running" when there was none. |
| `stop_session` | `session_id` (required) | Stop any session by id. The MCP equivalent of `vibeview stop <session-id>`. Says so when the session had already ended. |
| `create_test` | `app`, `name`, `steps` (required), `group`, `if_exists` | Create a test from plain-language steps, one per line (a check is a step starting with "Verify"). Returns the test id for `run_test`. An identical existing test is reused and a different one with the same name refused, unless `if_exists` is `update`, `new` or `fail`. |
| `run_test` | `test` (required), `session_id`, `device_model`, `ai_use`, `start_from_current_screen` | Run a saved test. With `session_id` it runs on a session you hold; without it, VibeView always starts a new device, runs the test and stops it (it never uses your `dev_start` session). `ai_use`: `smart` (default), `no_ai` (replay only, no usage credit), `ai_only`; AI runs are beta. Returns a run id for `get_run`. |
| `run_group` | `group` (required), `session_id`, `device_model`, `ai_use`, `start_from_current_screen` | Run every test of a group in order, on `session_id` or, without it, on a new device VibeView starts (never your `dev_start` session). Returns a run id for `get_run`. |
| `get_run` | `run_id` (required) | A run's status and, when a test failed, which step and why. |
| `dev_reload` | — | Roku only: re-package, upload and restart the channel in the held session (or this project's `vibeview dev --detach` session). The MCP equivalent of `vibeview dev-reload`. |

If the held session ends elsewhere (dashboard, idle timeout, failure), the
next tool call answers "session … has ended (…) — call dev_start"; the
server has already let it go, so `dev_start` starts a fresh one.
A tool result that ends with `Session … ends in N s for inactivity` means
the held session is about to time out: act on the device to keep it, or call
`dev_stop` if you are done. A session another VibeView dev connection took
over is reported as taken over; it keeps running there, so don't stop it.

**`dev_start` is stateful — it changes the default session for every later
call.** Once it succeeds, any tool called without an explicit `session_id`
targets that session instead of whatever `vibeview dev --detach` state exists
in the project directory. Only one such session can be held at a time
(`dev_start` fails if one is already running), and it stays live — billing
streaming minutes — until `dev_stop` or the MCP connection ends (the server
stops it when the client quits or closes the connection; if the server is
killed or the computer sleeps, the session ends within about 90 seconds
unless a browser tab is watching it). Always call `dev_stop` when you
finish verifying.
