---
name: ui-crawler-max
description: >-
  Autonomous UI crawler for iOS simulator apps — rapid, element-precise data collection.
  Use whenever the user says "crawl my app", "auto-test the UI", "click/tap through every
  screen", "monkey test", "explore the app and find errors/crashes", "collect screenshots
  of all screens", "smoke test the whole app", or asks for any app QA sweep, crash hunt,
  or screen inventory. It taps every reachable button/cell/switch via XCUITest,
  screenshots and journals every screen, detects crashes AS THEY HAPPEN with repro steps,
  streams console errors, and fans out cheap parallel Haiku subagents to label the haul.
  Data collection only — route fixes to swiftui-max/swift-language afterwards. Trigger
  even for a vague "is anything in my app broken?" — a crawl answers it empirically.
---

# UI Crawler Max

Crawl an iOS app in the simulator like a tireless QA intern: tap everything reachable,
record everything seen, never judge. This skill **collects data**; siblings analyze it
(`swiftui-max` for UI fixes, `swift-language` for crashes/concurrency, `apple-hig-ux`
for design verdicts). Environment: Xcode 26.6, iOS 26.5 simulators (`iPhone 17 Pro`
present), `xcodegen` installed. No `idb`, no `cliclick` needed — the crawler runs
*inside* the app process via XCUITest, so every tap is element-precise (`element.tap()`),
never screen-coordinate guessing.

## Architecture (4 moving parts)

1. **`scripts/UICrawlerTests.swift`** — a complete, compile-verified XCUITest that greedy-DFS
   explores the app: screen signature = FNV-1a hash of visible element identifiers+labels+
   frames (rounded to 10pt buckets); global visited-set of `(screen, element)` keys; taps
   unvisited buttons/cells/switches/segmented controls (tab-bar/nav/back buttons are
   `.button` descendants, covered); `swipeUp` up to 3× per screen to reveal more; back-nav
   ladder: nav back button → Done/Close/Cancel/Dismiss → edge swipe → relaunch.
2. **`scripts/crawl.sh`** — boots the sim, starts a console **error log stream before the
   run**, invokes `xcodebuild test`, harvests `.ips` crash reports afterwards, prints the
   artifact tree.
3. **Journal + screenshots** — JSON-lines journal per step, PNG + accessibility-hierarchy
   dump per *new* screen. After every single tap the crawler asserts
   `app.state == .runningForeground`; on crash it writes a repro record (last 10 steps),
   relaunches, marks the crashing element visited (**never tapped twice**), and continues.
4. **Haiku labeling fan-out** — after the run, parallel `model: haiku` subagents label
   batches of ~10 screens using `scripts/haiku-analysis-prompt.md`. Fast, factual, no fixes.

## Prerequisite: a UI-testing target

XCUITest needs a `bundle.ui-testing` target. Check: `xcodebuild -list -project App.xcodeproj`
— if no `*UITests` target exists and the project uses xcodegen, add one and regenerate:

```yaml
# project.yml (minimal app + UI test bundle)
name: MyApp
options: { bundleIdPrefix: com.example }
targets:
  MyApp:
    type: application
    platform: iOS
    deploymentTarget: "17.0"
    sources: [MyApp]
  MyAppUITests:
    type: bundle.ui-testing
    platform: iOS
    sources: [MyAppUITests]          # put UICrawlerTests.swift in this folder
    dependencies:
      - target: MyApp                # sets TEST_TARGET_NAME → XCUIApplication() targets MyApp
schemes:
  MyApp:
    build: { targets: { MyApp: all } }
    test:  { targets: [MyAppUITests] }
```

Then: `mkdir -p MyAppUITests && cp <skill>/scripts/UICrawlerTests.swift MyAppUITests/ && xcodegen generate`.
For non-xcodegen projects, add the target in Xcode (File → New → Target → UI Testing Bundle)
or route to `apple-dev-conductor` for project surgery. The template is warning-free in both
Swift 5 and Swift 6 language modes.

## Run workflow

```bash
SKILL=<path-to-this-skill>
bash "$SKILL/scripts/crawl.sh" ~/Projects/MyApp MyApp "iPhone 17 Pro"
```

Knobs (env vars on `crawl.sh`):

| Var | Default | Meaning |
|---|---|---|
| `CRAWL_MAX_STEPS` | 150 | hard step budget |
| `CRAWL_MAX_MINUTES` | 5 | hard time budget |
| `CRAWL_DENYLIST` | see Safety | comma-separated destructive labels, substring match |
| `CRAWL_ARTIFACTS` | `<proj>/crawl-artifacts/<ts>` | output dir |
| `UITEST_TARGET` | `<SCHEME>UITests` | UI test bundle name |
| `APP_NAME` | scheme name | process name for log predicate + crash matching |

**Env into the test runner — the #1 footgun.** Vars reach the runner only via xcodebuild's
*environment* with the `TEST_RUNNER_` prefix (stripped on delivery; verified in
`man xcodebuild`):

```bash
# WRONG — sets a build setting; the test process never sees it
xcodebuild test -scheme MyApp CRAWL_MAX_STEPS=300

# RIGHT — environment variable with TEST_RUNNER_ prefix
env TEST_RUNNER_CRAWL_MAX_STEPS=300 xcodebuild test -scheme MyApp ...
```

`crawl.sh` does this for you — prefer it over hand-rolled xcodebuild. It also starts
`xcrun simctl spawn <udid> log stream --level error --style compact --predicate
'processImagePath CONTAINS[c] "<AppName>"' > "$ART/console-errors.log" &` **before**
`xcodebuild test` (a stream started after misses launch-time errors), kills it after, and
copies new `.ips` files from `~/Library/Logs/DiagnosticReports` created since run start.

The crawler exports `CRAWL_MODE=1` into the app's launch environment — the app may check
it to load fixture data or skip onboarding.

## Output artifact contract

```
crawl-artifacts/<timestamp>/
├── journal.jsonl            # per step: {step, screenSignature, action, elementLabel,
│                            #   elementType, timestamp, result}
│                            # actions: newScreen|tap|scroll|back|skipDenied|dismissAlert|
│                            #   leftApp|crashDetected|relaunch|done
├── screens/<sig>.png        # first screenshot of each unique screen
├── screens/<sig>.txt        # accessibility hierarchy (app.debugDescription)
├── crash-<step>.json        # {crashDetected, step, lastAction, timestamp, repro:[last 10 steps]}
├── crashes/*.ips            # symbolicatable OS crash reports
├── console-errors.log       # error-level unified log for the app process
├── xcodebuild.log           # full build/test output
└── crawl.xcresult           # standard result bundle (attachments, timings)
```

The final `done` journal line summarizes: `steps=N screens=M crashes=K`.

## Post-run flow (main agent — do this yourself, in order)

1. **Read the cheap signals first**: `console-errors.log`, every `crash-*.json`, and
   `journal.jsonl` (grep for `crashDetected`, `skipDenied`, `relaunch`, `leftApp`).
   Symbolicate `.ips` crashes only if a crash was detected.
2. **Fan out Haiku labelers**: split `screens/` into batches of ~10; for each batch launch
   an Agent with `model: haiku` **in parallel (one message, multiple tool calls)** using
   the filled template from `scripts/haiku-analysis-prompt.md`. Each returns strict JSON
   `{screens:[{signature, name_guess, purpose, elements_count, issues:[{type, evidence}]}]}`.
3. **Merge** all batch outputs + crash records + console-error counts into
   `<artifacts>/report.json`, then write the human summary: screens found, coverage
   (steps used / budget), crash count with repro steps, issue tally by type, and the
   3–5 most suspicious screens (embed their PNG paths so the user can look).
4. **Route fixes — do not fix here**: crash stacks & concurrency (`_dispatch_assert_queue_fail`,
   Swift runtime traps) → **swift-language**; layout/dead-end/unlabeled-button/UI bugs →
   **swiftui-max**; design-quality judgments → **apple-hig-ux**. Hand each the artifact
   paths and the relevant `report.json` slice — the evidence is the deliverable.

## Safety (non-negotiable)

- **Never crawl an app signed into a real account or talking to production APIs.** A
  crawler taps *everything*: it will send messages, delete data, and buy things. Simulator
  + test account/fixtures (`CRAWL_MODE=1`) only. If the user asks to crawl a device build
  or a production-logged-in app, refuse and set up a fixture configuration first.
- **Deny-list of destructive labels** (case-insensitive substring match, checked before
  every tap; matches are journaled as `skipDenied`, never tapped). Defaults:
  `delete, remove, erase, reset, pay, purchase, buy, subscribe, checkout, sign out,
  log out, logout, send, report, block`. Extend per app via `CRAWL_DENYLIST` — e.g. an
  email app should add `archive, reply`; keep the defaults, append to them.
- Permission alerts (photos/notifications/location) are auto-accepted by an
  `addUIInterruptionMonitor` handler and journaled as `dismissAlert` — review those lines
  to know which protected resources the crawl granted.
- Budgets are hard stops (`CRAWL_MAX_STEPS`/`CRAWL_MAX_MINUTES`); the crawl always exits
  with a `done` journal line even mid-exploration.
- **Artifacts can capture personal data.** System alerts (e.g. Apple Account verification)
  surface over the app mid-crawl and land in screenshots with real emails/names from the
  host's simulator state. Review `screens/` before sharing artifacts, and prefer a
  freshly-erased simulator (`xcrun simctl erase <udid>`) for runs whose output leaves the
  machine. On *system* alerts prefer dismissive buttons ("Not Now", "Cancel") — affirmative
  choices can bounce the crawl into the iOS Settings app.

## Troubleshooting

- **Monitor never fires / test hangs on an alert**: interruption monitors only trigger on
  the *next* interaction; the crawler's constant tapping handles this. A hang usually
  means a non-alert modal — check the last `screens/<sig>.png`.
- **Signature churn (same screen counted many times)**: timestamps/carousels change labels
  every second. Raise frame bucketing or exclude `.staticText` from the signature loop in
  `UICrawlerTests.swift`.
- **`xcodebuild: error: Scheme not shared`**: share the scheme (or add the `schemes:` block
  to project.yml above).
- **Build fails before tests**: that's a build problem, not a crawl problem — use the
  `xcode-build-fixer` skill first.
