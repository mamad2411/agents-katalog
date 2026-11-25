---
name: flutter-screenshots
description: Capture screenshots of every screen and every state of a Flutter app on an iOS simulator and/or Android device, driven by a local mock backend, and deliver them as an organized zip with a README index. Use when the user asks for screenshots of all screens/states, a visual inventory or screen map of a Flutter app, store listing or QA screen captures, or "сделать картинки всех экранов" / "صور لكل الشاشات".
---

# Flutter screenshots of all screens and states

Produces `build/screenshots/<platform>/screens/<group>/*.png` + `README.md` + a zip, for iOS
(simulator) and Android (emulator or USB device). The app runs its real UI code; only the
backend is replaced by a local mock, so every state (empty, error, loading, each status
value, flags) can be produced on demand and reproducibly.

How it works:

- `scripts/mock_server.py` serves JSON fixtures per scenario and, when the app asks, captures
  the device screen (`simctl io screenshot` / `adb exec-out screencap`).
- `templates/shots.dart` is an in-app driver: it rebuilds the app per scenario, navigates,
  taps, types, scrolls long screens and requests shots.
- `scripts/run.sh` orchestrates everything and cleans up after itself.

`SKILL_DIR` below means the directory containing this file.

## 1. Survey the app (read code before writing anything)

Build a written inventory before touching files:

- **Entry & bootstrap** — `main*.dart`, flavors (`--flavor`, `lib/main_<flavor>.dart`), DI setup
  (GetIt / Get.put / Provider roots), what the root widget creates (providers, blocs).
- **Navigation** — `onGenerateRoute` / `routes:` map / GoRouter / auto_route. List every route and
  every screen pushed directly with `MaterialPageRoute(builder: ...)` (grep `Navigator.push`,
  `showDialog`, `showModalBottomSheet`). Note required route arguments.
- **State drivers** — for each screen, what decides what it shows: API fields (status enums,
  flags, empty lists), local storage (auth token, onboarding flag), loading/error states.
  Grep for `if (`, `switch`, `status ==`, `isEmpty`, `Status.error`.
- **API layer** — base URL constant/getter, every endpoint path, the envelope shape, and the
  models' `fromJson` (field names and *types*: an `int` field fed a string crashes parsing).
- **Side effects at startup** — permission prompts (ATT, notifications, location), analytics
  SDK activation, version/force-update checks, splash redirects.
- **Dead code** — screens not reachable from any route; list them and skip unless asked.

Write the inventory as a table *screen × state → what data produces it*. That table is the
scenario list. Show it to the user when the app is large, and ask which mode/role variants
matter (e.g. user roles, feature flags, A/B variants).

## 2. Point the app at the mock

Find where the base URL is built and add a compile-time override (harmless in production —
the define is empty unless passed):

```dart
static String get baseUrl {
  const mock = String.fromEnvironment('MOCK_API');
  if (mock.isNotEmpty) return '$mock/api/v1/';   // keep the app's path prefix
  ...
}
```

Cover *every* HTTP client (multiple Dio instances, `http` package, absolute URLs built from a
separate `domain` getter). Third-party hosts (maps, address suggestions, payment pages) are
left alone unless a screen needs them; mention in the README when a screen shows a third-party
error because of that. Ask before committing this change; otherwise revert it at the end.

## 3. Mock data — `tool/screenshots/mock/`

```
tool/screenshots/mock/
  routes.json          [{"method": "GET", "path": "/api/v1/orders/current", "fixture": "order.json"},
                        {"path": "re:^/api/v1/documents/\\d+$", "fixture": "docs.json"},
                        {"method": "DELETE", "path": "re:^/api/v1/cards/\\d+$", "body": {"ok": true}}]
  fixtures/*.json      one response body per file — built from the models' fromJson
  files/               PDFs / HTML / images, served at http://127.0.0.1:8787/files/<name>
```

- Write fixtures from the model code, with realistic local-language data (names, amounts,
  dates relative to today). Match field types exactly.
- Default fixtures = the "happy" logged-in state. Variants either live in separate fixture
  files (`order_active.json`) or are patched per scenario.
- Unmatched requests return `200 {}` and are listed in `raw/unmocked.txt` after a run — use that
  list to add missing routes.
- Scenario patch (sent from the driver with `scenario(name, patch)`; everything resets first):
  - `set: {"order.json": {"data": {"status": 5}}}` deep-merge (null sets null)
  - `replace: {"cards.json": {...}}` · `use: {"order.json": "order_active.json"}`
  - `fail: ["orders/current"]` → 500 · `status: {"users/me": 401}` · `slow: ["orders"]` → hangs 60 s
    (loading state)

## 4. Driver — `tool/screenshots/`

1. Copy `SKILL_DIR/templates/shots.dart` to `tool/screenshots/shots.dart` unchanged.
2. Create `tool/screenshots/shots_main.dart` from `SKILL_DIR/templates/shots_main.dart`:
   - Replicate the app's real `main()` init, **minus** permission prompts, analytics
     activation and crash reporting (system alerts would cover the screenshots, and the run
     must not send real analytics).
   - Root: `runApp(ShotsRoot(builder: (_) => <same providers + MaterialApp as the app>))`.
     Providers/blocs must be *inside* the builder so each `open()` starts from fresh state.
   - `MaterialApp`: use the app's `onGenerateRoute`, set `Shots.navigatorKey` to the app's
     navigator key (or pass `Shots.navigatorKey`), and an **inert initial route** — never the
     real splash (it redirects asynchronously and lands on top of the scripted screen).
   - GoRouter / Navigator 2.0 apps: set `Shots.navigate = (r, a) async => router.go(r, extra: a);`.
   - A `session()` helper that writes/clears the auth token and first-run flags in storage.
3. Script: group shots by area (`group('03_home')`), one `scenario()` + `open()` +
   `shot()`/`shotLong()` per state, with a `desc:` used in the README. Use mode/role prefixes
   when the user wants variants separated (`group('05_admin', prefix: 'admin_')`).

Driver API (all in `shots.dart`):

| Call | Purpose |
|---|---|
| `scenario(name, patch)` | reset mock + apply patch |
| `open(route, args:, settle:)` | fresh app tree, replace stack with route |
| `push(widget)` / `openWidget(widget)` | screens without named routes |
| `shot(name, desc:)` / `shotLong(name)` | capture; `shotLong` scrolls the main scrollable and captures `_scrollN` until the end |
| `tap('Text')` / `tapAt(offset)` / `back()` | interaction (`tap` scrolls the target into view) |
| `type('9991234567', index: 0)` | types through the field's input formatters (masks) and `onChanged` |
| `dumpTexts(tag)` | logs visible texts — use it to discover labels on unknown screens |
| `ctx` / `nav` | BuildContext / NavigatorState, e.g. `ctx.read<MyBloc>().add(...)` to reach a state directly |
| `want(group)` | honor `--only` |

For dialogs and bottom sheets: open the screen, then `tap()` the trigger or dispatch the
bloc/provider event via `ctx`, then `shot()`.

## 5. Run

From the project root:

```bash
SKILL_DIR/scripts/run.sh --platform ios [--flavor dev] [--only main,auth]
SKILL_DIR/scripts/run.sh --platform android [--device SERIAL] [--flavor dev]
```

Runs take minutes (build + one shot every few seconds): launch them in the background and
wait for completion. `run.sh`:

- picks the FVM SDK when `.fvmrc` / `.fvm` exists, the first booted simulator / first adb device;
- iOS: temporarily rewrites hard-coded `FLUTTER_TARGET` in `project.pbxproj` (flavor configs
  silently override `-t` otherwise) and restores it on exit; sets a 9:41 status bar;
- Android: `adb reverse tcp:8787` so the device reaches the host at 127.0.0.1, SystemUI demo
  mode for a clean status bar (restored on exit). Requires cleartext HTTP to 127.0.0.1 in
  debug (`usesCleartextTraffic` or a debug network-security-config) — check the manifest;
- starts the mock, runs the driver, waits for `SHOTS: DONE`, prints driver log lines,
  `tap: not found` misses, failed shots and unmocked endpoints, then packages.

Logs: `build/screenshots/<platform>/logs/`. Output: `build/screenshots/<platform>/screens/` and
`screenshots_<platform>_<date>.zip`.

## 6. Review every shot, iterate

Do not deliver unreviewed images. Make contact sheets and look at them:

```bash
python3 SKILL_DIR/scripts/sheet.py /tmp/sheet_main.png build/screenshots/ios/raw/03_*.png
```

Check each state actually rendered: wrong screen (redirect), blank page (data parse error →
compare fixture types with `fromJson`), missing dialog, `tap: not found`, duplicate frames.
Fix fixtures/script and rerun only the affected groups with `--only`. Rename or drop shots
whose state did not render rather than shipping misleading names.

Real app bugs found along the way (overflow stripes, missing assets, crashes on a field) go
into `tool/screenshots/NOTES.md` — it is appended to the README. Report them to the user; do
not fix app code unless asked.

## 7. Deliver and clean up

- Hand over the zip path, counts per group, what is *not* covered and why, and the bugs found.
- Revert temporary app changes (base-URL override if not approved, any patched file). `run.sh`
  restores `project.pbxproj` itself. Ask whether to keep `tool/screenshots/` in the repo —
  keeping it makes the next run a one-liner.

## Pitfalls (each cost a rerun before)

- **Navigator reparenting**: rebuilding the tree with a new key does not reset routes — a
  `GlobalKey<NavigatorState>` moves the old navigator state into the new tree. `open()`
  therefore always navigates explicitly after the rebuild.
- **Splash / version checks** started in the first frame navigate later and cover the scripted
  screen. Use an inert initial route; make the mock's version endpoint accept the build's
  version (debug builds may report a different version than release).
- **HTTP to the mock** must send `Content-Length` (the driver does) — chunked bodies are not read.
- **Debug-only overflow stripes** are real layout bugs; report them, don't hide them.
- **Native views** (WebView, PDF, maps) appear in shots because capture is done by the OS, not
  by Flutter — give them reachable URLs via `mock/files/`.
- **Static/singleton state** (GetX `Get.put`, static flags in helpers) survives `open()`;
  reset it in `session()` or the scenario when a screen depends on it.
- **Locked / sleeping device**: a backgrounded app renders no frames. `run.sh` wakes the
  device, keeps it on (`svc power stayon true`, restored on exit) and waits for the user to
  unlock a PIN/pattern lock screen — ask the user to unlock and keep it on the app.
- **Real devices** reinstall the debug build, replacing an installed build with the same
  application id — tell the user before running on their phone.
- **OEM status bars** (ColorOS, MIUI, One UI) may ignore SystemUI demo mode; the real clock and
  icons then appear in shots. Emulators and Pixel devices honor it.
- **Soft keyboard**: `shot()` hides it by default; pass `keyboard: true` to capture it.
