---
name: demo-pipeline
description: "Record automated demos for mobile and web apps. Converts natural language demo scripts into Maestro flows (mobile) or webreel configs (web), executes them to capture screenshots and video, and generates a QA report. Use when: record demo, demo recording, record app demo, grab demo, automated demo."
license: MIT
metadata:
  version: 1.0.0
  category: toolchain
  tags: [demo, recording, testing, screenshots, video, maestro, webreel, expo, react-native]
---

# Demo Pipeline

Record polished app demos from a natural language script. Works with Expo mobile (Maestro) and web apps (webreel/Playwright).

**Pipeline:** DISCOVER → DETECT → STATE SETUP → PARSE → EXECUTE → COMPILE

## Quick Start

User says: "record demo — show the login, navigate to rewards, highlight featured items, end on profile"

You:
1. Discover all screens, states, and flows via static analysis
2. Detect the project type and running state
3. Set up demo state injection (if demo_mode is enabled)
4. Generate a unified YAML script from the description
5. Present YAML for user approval
6. Execute with the right tool (Maestro or webreel)
7. Collect screenshots, video, and generate report

## Phase 0: DISCOVER — Flow & State Analysis

Analyze the codebase to map all screens, states, flows, and native dependencies.

### Step 1: Discover screens

Read the file-based routing structure:
```bash
find src/app -name "*.tsx" -not -name "_layout.tsx" -not -name "+not-found.tsx" | sort
```

For each screen file, extract the route path from its filesystem location.

### Step 2: Identify states per screen

For each screen file, search for UI conditionals that reveal possible states:

```bash
grep -n "loading\|isLogged\|isEmpty\|error\|balance.*>\|\.length.*==.*0" src/app/**/*.tsx
```

Common patterns to look for:
- `{loading ? <Skeleton/> : ...}` → `loading` state
- `{isLoggedIn && ...}` or `{user ? ... : ...}` → `guest` vs `logged-in`
- `{items.length === 0 ? <EmptyState/> : ...}` → `empty` state
- `{balance > 0 ? ... : ...}` → `empty-balance` vs `has-balance`
- `{error ? <Error/> : ...}` → `error` state

### Step 3: Map navigation flows

Search for navigation calls to build a flow graph:

```bash
grep -rn "router\.push\|router\.replace\|href=" src/app/ src/components/
```

Group into named flows (e.g., "Full reward claim": home → rewards → [id] → scan → confirmation).

### Step 4: Identify native dependencies

Search for native module usage per screen:

```bash
grep -rn "expo-camera\|CameraView\|useMobileWallet\|SeedVault\|Linking\|expo-local-authentication" src/
```

Mark each screen's native dependencies. These will be flagged as `native: real | mock` in the YAML.

### Step 5: Present flow map

Generate a flow map in YAML format (see [templates/flow-map.yaml](templates/flow-map.yaml)) and present to user:

> "I discovered N screens with M possible states and K flows. Here's the map:
> [flow map YAML]
> Which flows do you want in the demo?"

Then proceed to Phase 1.

## Phase 1: DETECT — Project Type & State

Before anything, determine what kind of project this is and whether it's running.

### Step 1: Identify project type

Check in order (stop at first match):

1. **Read `app.json`** — if it has an `"expo"` key → **Expo project**
   - Check if `app.json` has `"web"` in platforms → Expo universal
   - Extract `expo.slug` or `expo.name` for app ID
   - Default app ID: from `expo.ios.bundleIdentifier` or `expo.android.package`

2. **Glob for `next.config.*`** — if found → **Next.js web project**

3. **Read `package.json` scripts** — if has `"dev"` or `"start"` → **Generic web project**

4. **If none match** → ask user

### Step 2: Check running state

**For mobile (Expo):**
```bash
# Android
adb devices 2>/dev/null | grep -v "List"
# iOS (macOS only)
xcrun simctl list booted 2>/dev/null
```

If no device/emulator → tell user: "No running device detected. Start your emulator/device and the Expo dev server, then try again."

**For web:**
```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:8081 2>/dev/null
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 2>/dev/null
curl -s -o /dev/null -w "%{http_code}" http://localhost:5173 2>/dev/null
```

If no server → tell user: "No dev server detected. Start your dev server and try again."

### Step 3: Announce detection

Tell the user what you detected, e.g.:
> "Detected: **Expo mobile** project (`com.example.myapp`) with Android emulator running. I'll use **Maestro** for recording."

Then proceed to Phase 2.

## Phase 1.5: STATE SETUP — Demo State Injection

**Only runs when the unified YAML has `demo_mode: true`.** Skip this phase entirely for regular demos without state emulation.

### Step 1: Check if demo mode is needed

If any step in the YAML has a `state:` block or `native: mock`, demo mode is required.

### Step 2: Inject state via adb

For each step that has a `state:` block, inject the mock data before executing that step's actions.

**Injection mechanism:**
```bash
# Write mock state to AsyncStorage via adb
adb shell "run-as <APP_ID> sh -c 'cat > /data/data/<APP_ID>/files/demo-state.json'" <<< '{"wallet":"0x123","balance":5000}'
```

Alternative — use deep links to navigate to specific states:
```bash
adb shell am start -a android.intent.action.VIEW \
  -d "<SCHEME>://demo?screen=<SCREEN>&state=<STATE_JSON_ENCODED>"
```

### Step 3: Handle native mocks

For steps with `native: mock`:
- Inject the mock result into AsyncStorage before the step executes
- The app's demo bootstrap reads this and skips the native module, showing the result directly

For steps with `native: real` (or no `native` field):
- No injection — let the real native flow execute

### Step 4: Cleanup after recording

After all steps complete:
```bash
adb shell "run-as <APP_ID> sh -c 'rm -f /data/data/<APP_ID>/files/demo-state.json'"
```

### Important: App-side requirement

The project needs a demo bootstrap file. If it doesn't exist, tell the user:

> "Demo mode requires a bootstrap file. I'll create `src/demo/bootstrap.ts` — a dev-only file that reads mock state from AsyncStorage. This file has zero impact on production builds since it's gated behind `__DEV__`."

See [state-injection.md](state-injection.md) for the full bootstrap implementation.

## Phase 2: PARSE — Natural Language → Unified YAML

Convert the user's natural language demo description into a structured YAML script.

### Step 1: Analyze the description

Extract:
- **Screens/sections** to show (each becomes a step)
- **Interactions** (taps, scrolls, typing)
- **Key elements** to highlight (get screenshot actions)
- **Flow order** (navigation sequence)

### Step 2: Identify testIDs or selectors

**For mobile (Expo/React Native):**
- Search codebase for testID props: `grep -r 'testID=' src/`
- Match testIDs to screens/elements in the description
- If no testID exists, use text-based selection

**For web:**
- Search for `id=`, `data-testid=`, or distinctive text
- Use CSS selectors

### Step 3: Generate unified YAML

```yaml
target: <expo-mobile|web|expo-universal>
app_id: <detected app ID>        # mobile only
base_url: <detected URL>         # web only

demo_mode: false               # true to enable state injection
env:                           # environment variables (optional)
  DEMO_MODE: "true"

steps:
  - name: "<Screen Name>"
    state:                       # optional — mock state to inject
      key: value
    native: real                 # optional — real | mock (default: real)
    actions:
      - <action>: <value>
      - screenshot: "<NN-name>"

output:
  screenshots: ./screenshots/
  video: ./videos/demo.mp4
  video_mode: device-only      # device-only | full
  report: ./docs/demo-report.md
```

**Supported actions** (see [reference.md](reference.md) for full details):

| Action | Example |
|--------|---------|
| `tap` | `tap: "tab-rewards"` or `tap: "Button Text"` |
| `type` | `type: { target: "search-input", text: "Espresso" }` |
| `scroll` | `scroll: down` |
| `swipe` | `swipe: left` |
| `wait` | `wait: 2s` |
| `wait_for` | `wait_for: "loading-done"` |
| `screenshot` | `screenshot: "03-rewards"` |
| `navigate` | `navigate: "http://localhost:3000/dashboard"` |
| `key` | `key: "Enter"` |

Auto-number screenshots with `NN-` prefix (01, 02, 03...).

### Step 4: Present for approval

Show the generated YAML to the user. Ask:
> "Here's the demo script I generated. Review it and let me know if you'd like to change anything, or approve to proceed with recording."

**HARD GATE: Do NOT proceed to Phase 3 until the user explicitly approves the YAML.**

## Phase 3: EXECUTE — Run the Recording

Translate approved unified YAML → tool-specific format → execute.

### Mobile Path: Maestro

**Step 1: Generate Maestro flow**

Action mapping:

| Unified | Maestro |
|---------|---------|
| `tap: "id"` | `- tapOn:\n    id: "id"` |
| `tap: "Text"` | `- tapOn: "Text"` |
| `type: { target, text }` | `- tapOn:\n    id: "target"\n- inputText: "text"` |
| `scroll: down` | `- scroll` |
| `swipe: left` | `- swipe:\n    direction: LEFT\n    duration: 400` |
| `wait: 2s` | (no-op — Maestro auto-waits; used for pacing only) |
| `wait_for: "id"` | `- extendedWaitUntil:\n    visible:\n      id: "id"\n    timeout: 10000` |
| `screenshot: "name"` | `- takeScreenshot: "name"` |

**Step 2:** Save to `./maestro/demo-recording.yaml`

**Step 3:** Execute:
```bash
maestro record maestro/demo-recording.yaml --output videos/demo.mp4
```

Fallback (no video): `maestro test maestro/demo-recording.yaml`

Copy screenshots:
```bash
mkdir -p screenshots
cp ~/.maestro/tests/*/screenshots/* screenshots/ 2>/dev/null || true
```

### Video Mode: device-only

When `output.video_mode` is `device-only`, record only the device screen (no terminal/Maestro UI):

```bash
# Start device screen recording in parallel
adb shell screenrecord /sdcard/demo-recording.mp4 &
RECORD_PID=$!

# Run Maestro flow in test-only mode
maestro test maestro/demo-recording.yaml

# Stop recording and extract
kill $RECORD_PID 2>/dev/null
adb shell "kill $(adb shell ps | grep screenrecord | awk '{print $2}')" 2>/dev/null
sleep 1
adb pull /sdcard/demo-recording.mp4 videos/demo.mp4
adb shell rm /sdcard/demo-recording.mp4
```

**Limitation:** `adb screenrecord` max 3 minutes per recording. For longer demos, chain multiple recordings and concatenate:
```bash
ffmpeg -f concat -safe 0 -i segments.txt -c copy videos/demo.mp4
```

When `video_mode` is `full` (default), use `maestro record` as before.

### Web Path: webreel

**Step 1: Generate webreel config**

Action mapping:

| Unified | webreel |
|---------|---------|
| `tap: "id"` | `{ "action": "click", "selector": "#id" }` |
| `tap: "Text"` | `{ "action": "click", "text": "Text" }` |
| `type: { target, text }` | `{ "action": "type", "selector": "#target", "text": "text" }` |
| `scroll: down` | `{ "action": "scroll", "y": 500 }` |
| `wait: 2s` | `{ "action": "pause", "ms": 2000 }` |
| `wait_for: "id"` | `{ "action": "wait", "selector": "#id" }` |
| `screenshot: "name"` | `{ "action": "screenshot", "output": "name.png" }` |
| `navigate: "url"` | `{ "action": "navigate", "url": "url" }` |
| `key: "Enter"` | `{ "action": "key", "key": "Enter" }` |

**Step 2:** Save to `./webreel.config.json`

**Step 3:** Execute: `npx webreel record`

### Web Fallback: Playwright

If webreel not installed:
1. Generate Playwright TypeScript script with `recordVideo` context
2. Execute: `npx tsx scripts/demo-recording.ts`
3. Convert: `ffmpeg -i recordings/demo.webm -c:v libx264 -preset fast videos/demo.mp4`

### Error Handling

If execution fails:
1. Show error output to user
2. Suggest fixes (missing testIDs, wrong selectors, app not running)
3. Let user edit YAML and retry from Phase 3

## Phase 4: COMPILE — Generate Outputs

### Step 1: Organize screenshots

```bash
mkdir -p screenshots
ls -la screenshots/
```

Verify all expected screenshots exist. Report any missing.

### Step 2: Verify video

```bash
ls -la videos/demo.mp4
```

Report file size. If missing, explain (e.g., `maestro test` doesn't record video).

### Step 3: Generate report

Create `./docs/demo-report.md` using the [report template](templates/demo-report.md):
- Project name and type (from Phase 1)
- Tool used
- Date
- Step table with screenshot paths and status
- Output file paths and sizes
- Errors encountered

### Step 4: Present summary

> **Demo recording complete!**
> - Screenshots: `N` captured in `./screenshots/`
> - Video: `./videos/demo.mp4` (X MB)
> - Report: `./docs/demo-report.md`

## Example Output

```
Demo recording complete!
- Screenshots: 5 captured in ./screenshots/
  01-login.png (1290x2796)
  02-home-feed.png (1290x2796)
  03-rewards-list.png (1290x2796)
  04-coupon-detail.png (1290x2796)
  05-profile.png (1290x2796)
- Video: ./videos/demo.mp4 (12.3 MB, 45s)
- Report: ./docs/demo-report.md
```

## Error Handling

- **No device/emulator detected**: "Start your emulator/device and the Expo dev server, then try again"
- **No dev server detected**: "Start your dev server and try again"
- **testID not found**: Suggest text-based selection as fallback, or ask user to add testID to component
- **Video recording failed**: Fall back to `maestro test` (screenshots only, no video) and explain limitation
- **Maestro not installed**: Provide install command: `curl -Ls "https://get.maestro.mobile.dev" | bash`

## Related Skills

- [maestro-mobile-testing](https://github.com/JuanMarchetto/maestro-mobile-testing) — deep patterns for writing Maestro tests
- [webreel](https://github.com/JuanMarchetto/webreel-skill) — scripted web demos with cursor animation

## Context

This skill has companion files:
- `reference.md` — complete action reference with tool mappings
- `templates/maestro-flow.yaml` — Maestro flow template
- `templates/webreel-config.json` — webreel config template
- `templates/demo-report.md` — report template
