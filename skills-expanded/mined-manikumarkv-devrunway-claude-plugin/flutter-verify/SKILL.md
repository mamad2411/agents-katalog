---
name: flutter-verify
description: Produce the manual verification checklist for a Flutter change — scoped to what the change actually touches, each item marked emulator-ok or device-required, with the exact simctl/adb command where one exists. Use before opening a PR, before a release build, or any time the question is "what do I have to check by hand, and what needs a real phone". Usage — /flutter-verify [what changed]
argument-hint: "[what changed, or a path to a diff]"
arguments:
  - name: change
    description: "Description of the change (e.g. 'paginated the program list'), or a path to a diff file. If omitted, the uncommitted/branch diff is used."
user-invocable: true
effort: medium
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(git diff *)
  - Bash(git status *)
  - Bash(flutter devices *)
  - Bash(adb devices *)
  - Bash(xcrun simctl list *)
---

# /flutter-verify — what to check by hand, and where

An emulator is honest about some questions and confidently wrong about others. It will
happily render your layout at 200% text and tell you the truth; it will also render a
60fps scroll on a desktop CPU and tell you a lie you will not discover until a user on a
three-year-old mid-range Android does.

The value of this command is not the checklist. It is knowing which half of the checklist
the emulator is allowed to answer.

---

## Step 1 — Establish what changed

In order:

1. If `$ARGUMENTS[0]` is a path to an existing file, Read it and treat it as the diff.
2. Else if `$ARGUMENTS[0]` is non-empty, treat it as the description of the change.
3. Else, get the diff yourself:

```bash
git diff --stat
git diff develop...HEAD --name-only 2>/dev/null || git diff main...HEAD --name-only
```

If both the description and the diff are available, use both — the description says what
was intended, the file list says what was touched. Where they disagree, trust the files.

If you have neither, ask one question and stop until it is answered:

> What changed? One line is enough — e.g. "paginated the program list".

Do not guess. A guessed scope produces a checklist for someone else's change.

---

## Step 2 — Classify the change

Match the change against the kinds below. A change usually matches two or three. Emit
**only** the matched sections, plus §L (both platforms) which is always emitted.

| Signal in the description or the diff | Kind | Section |
|---|---|---|
| Widget, layout, padding, theme, colours, text styles, a new screen | UI / layout | §A |
| List, grid, pagination, infinite scroll, pull-to-refresh, feed | List / scroll | §B |
| Form, text field, validation, submit button, picker | Form | §C |
| Route, `go_router`, deep link, tab, back handling | Navigation / links | §D |
| Model class, `fromJson`, Drift/Isar/Hive schema, migration, cached shape | Model / local schema | §E |
| Login, logout, token, refresh, session, biometric unlock | Auth / session | §F |
| Dio client, repository, endpoint, retry, timeout, cache headers | Networked | §G |
| `permission_handler`, camera, location, notifications prompt, photos | Permissions | §H |
| FCM, APNs, notification payload, notification tap handling | Push | §I |
| IAP, StoreKit, Play Billing, subscription, paywall | Purchases | §J |
| Method channel, Pigeon, plugin, native code, background task, WorkManager | Platform / background | §K |

**Scoping is a hard rule, not a preference.** If the change is "paginate the program
list", emit §B, §G and §L — and possibly §A if the row widget changed. Do **not** emit
biometric items, purchase items, or permission items because they are generally good
practice. An unscoped checklist is ignored wholesale, which is worse than a short one.

---

## Step 3 — Tag every item

Every item carries exactly one tag. Use this table to decide; it is the whole point of the
command.

| The emulator is honest about | The emulator is confidently wrong about |
|---|---|
| Layout across screen sizes | **Any performance number, ever** |
| Dark mode | Real biometrics and keystore policy |
| Text scale up to 200% | Real push tokens and terminated-state delivery |
| RTL | Purchases |
| The four states (loading / empty / error / loaded) | Camera, NFC, BLE, real sensors |
| Deep link routing | Doze and OEM battery killers |
| Process death and state restoration | Cellular ↔ wifi transitions, real flaky signal |
| Data migrations on upgrade | App Links / Universal Links domain verification |
| Permission denial paths | Real TalkBack / VoiceOver gestures |
| The semantics tree | Thermal throttling, real memory pressure |

Two traps worth stating explicitly, because both fail *silently*:

- **Performance.** An Android emulator runs on your desktop CPU and is routinely faster
  than a real mid-range phone; the iOS simulator uses your Mac's CPU and GPU. A frame
  chart from either is not evidence. There is no emulator flag that fixes this. Never
  write `emulator-ok` on a performance item, no matter how the change is described.
- **Keystore.** The emulator keystore is software-backed. A hardware-bound key policy —
  `setUserAuthenticationRequired`, StrongBox, `.biometryCurrentSet` — will appear to work
  perfectly on the emulator and then behave differently on a real secure element.
  Anything biometric is device-only, including the parts that "obviously" work.

---

## Step 4 — Emit the checklist

Output this shape. Nothing before it except one line naming the scope. No preamble, no
summary of the change back to the user — they know what they changed.

```markdown
## Verification — <short name of the change>
Scope: <matched kinds, comma separated>

### Emulator / simulator
- [ ] **emulator-ok** — <thing to do and what you are looking for>
      `<exact command, if one exists>`

### Physical device required
- [ ] **device-required** — <thing to do>  ·  _why: <the one-line reason it can't be faked>_

### Before you call it done
- [ ] <the promote-to-test item, if anything here was checked by hand twice>
```

Every `device-required` item carries its reason. Without the reason the item gets skipped
under deadline; with it, the developer can make an informed call.

Where a command differs by platform, give both lines — Android then iOS. Substitute the
real package name / bundle id from `android/app/build.gradle` and `ios/Runner.xcodeproj`
if you can read them; otherwise leave `<pkg>` and `<bundle-id>` as placeholders and say so
once at the bottom.

---

## Section catalogue

Pull items from the matched sections only. Trim anything that plainly does not apply —
these are the candidates, not a quota.

### §A — UI / layout

- **emulator-ok** — Smallest supported screen: no overflow stripes, nothing clipped.
- **emulator-ok** — Largest / tablet: the layout uses the width rather than stretching one column.
- **emulator-ok** — Dark mode. `adb shell cmd uimode night yes` · `xcrun simctl ui booted appearance dark`
- **emulator-ok** — 200% text: nothing truncated, no overlap, buttons still tappable.
  `adb shell settings put system font_scale 2.0` · `xcrun simctl ui booted content_size accessibility-extra-large`
- **emulator-ok** — RTL: padding mirrors, icons that indicate direction flip.
  `adb shell settings put global debug.force_rtl 1` (or run with an RTL locale)
- **emulator-ok** — Keyboard open: the focused field is not covered; the screen scrolls.
- **emulator-ok** — Safe areas: notch, dynamic island, gesture bar, status bar overlap.
- **emulator-ok** — Semantics tree has labels on the new elements (Widget Inspector → semantics, or `debugDumpSemanticsTree()`).
- **device-required** — Screen-reader walk of the new screen with real gestures. _why: TalkBack and VoiceOver gesture handling, focus order and announcement timing are not reproduced by the simulator's accessibility inspector._

### §B — List / scroll

- **emulator-ok** — All four states render: loading, empty, error, loaded.
- **emulator-ok** — Page 2 loads when you reach the end of page 1; scroll position does not jump when items append.
- **emulator-ok** — Page boundary: no duplicated and no skipped item between pages.
- **emulator-ok** — Pull-to-refresh resets to page 1 without duplicating rows or stacking pages.
- **emulator-ok** — Error mid-pagination: kill the network at page 3, confirm the error is inline (not a full-screen wipe of loaded pages) and retry refetches only the failed page.
  `adb shell svc wifi disable && adb shell svc data disable` (restore with `enable`)
- **emulator-ok** — Empty result on page 1 shows the empty state, not an infinite spinner.
- **emulator-ok** — Rapid scroll to the bottom does not fire duplicate page requests (watch the log).
  `adb logcat --pid=$(adb shell pidof -s <pkg>)`
- **emulator-ok** — Background and return mid-list with `always_finish_activities` on: the list restores or resets cleanly, no crash, no blank screen.
  `adb shell settings put global always_finish_activities 1`
- **device-required** — Scroll smoothness and jank in profile mode on the oldest supported hardware. _why: the emulator runs on the desktop CPU and will show a smooth scroll that a real mid-range device cannot produce._
  `flutter run --profile` then DevTools → Performance

### §C — Form

- **emulator-ok** — Validation fires on empty and on invalid input; messages are attached to the right field.
- **emulator-ok** — Keyboard actions: next moves focus, done submits, the focused field is never covered.
- **emulator-ok** — Double-tap submit sends one request, not two.
- **emulator-ok** — Server-side error (422/409) surfaces on the field, not as a toast that disappears.
- **emulator-ok** — Background mid-entry and return: entered text is preserved or deliberately cleared, not crashed.
  `adb shell settings put global always_finish_activities 1`
- **device-required** — Password manager / autofill and the real keyboard (swipe typing, autocorrect, IME). _why: the emulator uses the desktop keyboard by default and never exercises the platform autofill service._

### §D — Navigation / links

- **emulator-ok** — Deep link from cold start lands on the target screen with a sane back stack.
  `adb shell am start -a android.intent.action.VIEW -d "<scheme>://programs/42" <pkg>` · `xcrun simctl openurl booted "<scheme>://programs/42"`
- **emulator-ok** — Same link while the app is backgrounded, and while it is already on that screen.
- **emulator-ok** — Deep link while logged out: login, then land on the original target, not the home screen.
- **emulator-ok** — Back from the deep-linked screen goes somewhere reasonable, not out of the app.
  `adb shell input keyevent KEYCODE_BACK`
- **emulator-ok** — Process death on the new route restores or exits cleanly.
  `adb shell settings put global always_finish_activities 1`
- **device-required** — The https link opened from Mail / Messages / a browser, verified against the real domain. _why: App Links and Universal Links depend on the OS fetching `assetlinks.json` / `apple-app-site-association` from the live domain; on an emulator the link falls back to the browser and you learn nothing._

### §E — Model / local schema

The first item is mandatory whenever a model, a stored shape, or a local schema changed.
Do not drop it because the change "looks additive".

- **emulator-ok** — **Upgrade install, not fresh install.** Install the previously released
  build, use the app until it has real data, then install the new build **over** it without
  uninstalling. A fresh install runs zero migrations, so a broken migration passes every
  test on the machine of the person who wrote it and breaks for every existing user.
  ```bash
  # Android — same signing key, -r keeps app data
  adb install -r ./previous/app-release.apk
  #   … create data in the app …
  adb install -r build/app/outputs/flutter-apk/app-release.apk
  ```
  ```bash
  # iOS simulator — install over, never uninstall between the two
  xcrun simctl install booted ./previous/Runner.app
  #   … create data in the app …
  xcrun simctl install booted build/ios/iphonesimulator/Runner.app
  ```
- **emulator-ok** — After the upgrade: old rows read back correctly, new nullable fields have sane defaults, nothing renders as empty or "null".
- **emulator-ok** — Cached JSON written by the old build parses in the new build, or is discarded deliberately rather than throwing on startup.
- **emulator-ok** — Partial / corrupt stored data does not crash the launch path.
- **emulator-ok** — Fresh install still works (run it second, so it does not mask the upgrade case).
- **emulator-ok** — Downgrade or reinstall of the old build does not crash on the new schema, if that is a path you support.

### §F — Auth / session

- **emulator-ok** — Expired access token mid-request refreshes once and the original request completes.
- **emulator-ok** — Refresh failure logs out cleanly and lands on login without a crash loop.
- **emulator-ok** — Logout clears the local stores; relaunch does not show cached user data.
- **emulator-ok** — Two concurrent 401s trigger one refresh, not two.
- **device-required** — Biometric unlock: enrolled, wrong finger/face, no enrolment, biometrics removed after the key was created. _why: the emulator keystore is software-backed, so hardware-bound key policies appear to work and then behave differently on a real secure element._
- **device-required** — Session survives ten minutes backgrounded with the screen off. _why: Doze and OEM battery managers do not exist on the emulator._

### §G — Networked

- **emulator-ok** — Offline at request time shows the error state with a retry that works.
  `adb shell svc wifi disable && adb shell svc data disable`
- **emulator-ok** — Slow network: the loading state is visible and not a frozen screen.
  Launch the AVD with `emulator -avd <name> -netdelay gprs -netspeed edge`, or Network Link Conditioner for the iOS simulator.
- **emulator-ok** — Timeout produces the timeout message, not a generic crash.
- **emulator-ok** — 401 / 403 / 500 / malformed body each map to a distinct, human message.
- **emulator-ok** — Backgrounding during an in-flight request and returning does not double-fire or leave the spinner stuck.
- **device-required** — Wifi ↔ cellular handover mid-request, and real weak signal. _why: the emulator's network is your desktop's; it never drops to one bar, never re-homes an IP mid-socket._

### §H — Permissions

- **emulator-ok** — Grant path.
- **emulator-ok** — Deny once: the in-app explanation appears, the app stays usable.
- **emulator-ok** — Permanently denied: the app routes to Settings rather than re-prompting into a wall.
  `adb shell pm revoke <pkg> android.permission.CAMERA` · `xcrun simctl privacy booted revoke camera <bundle-id>`
- **emulator-ok** — Grant in Settings and return to the app: the screen recovers without a restart (this crosses a process-death boundary; run it with `always_finish_activities 1`).
- **device-required** — The hardware behind the permission actually working — camera preview, NFC tag read, BLE scan, real GPS fix. _why: the emulator's fake camera and absent NFC/BLE radios tell you the permission dialog worked, not that the feature does._

### §I — Push

- **emulator-ok** — Payload rendering and tap routing for a notification delivered while the app is foregrounded and backgrounded.
  `xcrun simctl push booted <bundle-id> payload.apns`
- **emulator-ok** — Tapping the notification deep-links to the right screen with a sane back stack.
- **device-required** — Real token registration, and delivery in the terminated state. _why: APNs tokens are not issued to the simulator and terminated-state delivery depends on the real OS delivery path._
- **device-required** — A notification arriving after the device has been idle for 30+ minutes. _why: Doze and OEM battery managers defer or drop delivery in ways the emulator never reproduces._

### §J — Purchases

- **device-required** — The entire flow: paywall, purchase, cancel, restore, receipt validation, and the app's state after each. _why: real StoreKit / Play Billing sandbox behaviour, the account picker, and interrupted purchases only exist on a device with a real store account._
- **device-required** — Interrupted purchase: kill the app mid-transaction and relaunch; the entitlement resolves without a double charge.

### §K — Platform / background

- **emulator-ok** — Every method-channel call has a failure path: unimplemented, exception, null. Force each once.
- **emulator-ok** — The feature on the platform you did *not* develop on.
- **emulator-ok** — Process death during the background work: `adb shell settings put global always_finish_activities 1`
- **device-required** — Background task survives ten minutes with the screen off and the app swiped away. _why: Doze, App Standby buckets and OEM killers (Xiaomi, Huawei, Samsung, OnePlus) terminate background work on real devices and do not exist on the emulator._
- **device-required** — Battery and thermal impact of anything long-running. _why: no emulator has a battery._

### §L — Both platforms, always

Emit these regardless of what changed.

- **emulator-ok** — The change works on both Android and iOS. Whichever one you developed on, check the other before the PR.
- **emulator-ok** — Android system back / predictive back on the affected screens.
- **emulator-ok** — iOS swipe-back from the left edge is not broken by the change.
- **emulator-ok** — Process death: `adb shell settings put global always_finish_activities 1`, use the changed screen, background, return. Reset with `... always_finish_activities 0` when done.
- **emulator-ok** — No new red screens, exceptions or `setState after dispose` in the log while working through the above.
  `adb logcat --pid=$(adb shell pidof -s <pkg>)`

---

## Five virtual devices, not fifteen

Where the checklist says "across sizes", it means these five. More than five is theatre;
fewer misses a real class of bug.

| # | Device | Catches |
|---|---|---|
| 1 | Smallest supported screen | Overflow, clipped buttons, cramped rows |
| 2 | Largest phone or a tablet | Stretched single-column layouts, unused width |
| 3 | Oldest supported OS | Removed APIs, older WebView, permission model differences |
| 4 | Newest OS | New permission prompts, predictive back, edge-to-edge changes |
| 5 | **Hostile mode** — dark + 200% text + RTL + slow network, all at once | Almost everything the other four miss |

Device 5 finds the most bugs per minute. If you only run one, run that one.

```bash
# hostile mode, Android
adb shell cmd uimode night yes
adb shell settings put system font_scale 2.0
adb shell settings put global debug.force_rtl 1
# launch the AVD with: emulator -avd <name> -netdelay gprs -netspeed edge
```

---

## Terminal drivers

Give the exact line, not the name of a menu. Anything reachable from the terminal is
repeatable; anything reachable only from a GUI gets done once.

**Android**

| Command | Does |
|---|---|
| `adb shell settings put global always_finish_activities 1` | **The single highest-value command here.** Destroys each activity as you leave it, reproducing what a real device does under memory pressure. Turns "works until you background it" into a failure you can see locally, in seconds. Reset with `0`. |
| `adb shell am start -a android.intent.action.VIEW -d "<url>" <pkg>` | Fire a deep link |
| `adb shell svc wifi disable` / `adb shell svc data disable` | Go offline mid-flow (`enable` to restore) |
| `adb shell pm clear <pkg>` | Reset to first-launch state |
| `adb shell pm revoke <pkg> <permission>` | Test the denial path |
| `adb logcat --pid=$(adb shell pidof -s <pkg>)` | Only your app's log |
| `adb shell input keyevent KEYCODE_BACK` | Back, scriptably |
| `adb install -r <apk>` | Install **over** the existing build, keeping data |
| `adb shell cmd uimode night yes` | Dark mode |
| `adb shell settings put system font_scale 2.0` | 200% text |

**iOS simulator**

| Command | Does |
|---|---|
| `xcrun simctl openurl booted "<url>"` | Fire a deep link |
| `xcrun simctl push booted <bundle-id> payload.apns` | Deliver a notification payload |
| `xcrun simctl ui booted appearance dark` | Dark mode |
| `xcrun simctl ui booted content_size accessibility-extra-large` | Largest text |
| `xcrun simctl privacy booted revoke <service> <bundle-id>` | Test the denial path |
| `xcrun simctl install booted <path>.app` | Install over the existing build |
| `xcrun simctl io booted recordVideo bug.mov` | Record the repro for the ticket |

---

## The physical-device gate before release

This is a separate, fixed list. It does not vary with the change, and no amount of
emulator work substitutes for it. Emit it when the user says the change is going to a
release build, or asks for the release gate.

- [ ] **device-required** — Profile-mode performance on the oldest supported hardware: startup, the heaviest scroll, the heaviest screen.
- [ ] **device-required** — Biometric unlock, including the biometrics-changed-after-enrolment case.
- [ ] **device-required** — Real push in all three states: foreground, background, terminated.
- [ ] **device-required** — Links opened from outside the app, against the live domain.
- [ ] **device-required** — Ten minutes backgrounded with the screen off, then resume.
- [ ] **device-required** — Screen-reader walk of the primary flow with real gestures.
- [ ] **device-required** — Install over the **previously released** version from the store or TestFlight, with existing data.

---

## Hard rules

- **Never write `emulator-ok` on a performance item.** An Android emulator runs on the
  desktop CPU and is often faster than a real mid-range phone; the iOS simulator uses the
  Mac's GPU. There is no configuration that makes either honest about frame timing,
  startup time, memory pressure or battery. If the user asks for a performance check on an
  emulator, say plainly that the number would be meaningless and give the device item.
- **Anything biometric is device-only**, including the parts that appear to pass. The
  emulator keystore is software-backed, so hardware-bound key policies succeed there and
  differ on a real secure element.
- **Always emit the upgrade-install item (§E) when a model or local schema changed.** A
  fresh install skips every migration, so the bug ships to everyone except the person who
  tested it.
- **Emit only the matched sections.** No biometric items on a list change, no purchase
  items on a form change. If in doubt, leave it out — the checklist is only used if it is
  short enough to finish.
- **Every `device-required` item states its reason** in one line. An unexplained item is a
  skipped item.
- **Give commands, not menu paths.** Where no command exists, say so explicitly rather
  than inventing one.
- **Anything you verify by hand more than twice becomes a widget test.** When the change
  touches something already on a previous checklist, say so and name the test to write:
  a widget test for a state, a golden for a layout, an integration test for a flow.
- Do not run the emulator commands for the user unless they ask. This command produces the
  checklist; they drive the device.
