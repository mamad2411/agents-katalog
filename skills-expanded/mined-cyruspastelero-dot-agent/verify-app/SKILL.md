---
name: verify-app
description: Verify an app feature by feature: honest coverage matrix, layer-by-layer tests, fix what breaks, enforce with hooks. Use when asked to "verify the app", "test everything properly" or check what is actually tested.
---

# Verify App — honest verification loop with enforcement

You are running a verification campaign, not a test run. The output is threefold: **bugs found and fixed** (each with a regression test), an **honest coverage matrix** (what is verified, how, and what is not), and **machine enforcement** that keeps the matrix true after you're gone. Born from a session where two bugs shipped past a fully green suite and were caught only by hand — never let "the suite is green" masquerade as "the feature works."

## Phase 0 — Recon (before any test)

1. Read the repo's CLAUDE.md / README / handoff docs. Identify: build command, test command, test framework, existing suites.
2. **If the app is a port/migration, find the spec** (the source app). Parity-diffing a screen against its source implementation is verification method zero — it finds entire missing sub-features that no test would think to check.
   Also audit the spec's **design-token/theme file once, up front, with the user**: for each token ask "is this still on-brand?" — an off-brand token in the spec (a stray cold blue in a warm palette) gets baked into every ported screen and then verified as "correct" by parity forever after. Ten minutes on the palette beats rediscovering the same wrong color screen by screen; the `audit-app-design` skill has the full design-pass method when more than tokens are in doubt.
3. Inventory QA affordances: env-var hooks, deep links, seeded/test accounts, debug flags. If none exist, adding them (DEBUG-gated) is usually the first high-leverage commit. The proven trio for UI automation: a **reset-state** flag (wipe data + first-run flags), a **skip-first-run** flag (start flows on the main screen), and a **force-capability-off** flag per flaky environmental capability (see gotchas) — together they make every flow test self-seeding and deterministic.
4. Confirm the baseline: run the full existing suite before changing anything. Never build on a red or unknown baseline.

## Phase 1 — The coverage matrix (exhaustive inventory FIRST)

Create `docs/verification-coverage.md` **in the app repo** (same repo as the code — enforcement needs same-commit updates).

**Enumerate before you test.** The original escape happened because a sub-feature (one exercise type inside a quiz) was never listed, so no one noticed it was never exercised. Build the complete inventory mechanically, not from memory:
- Walk the **navigation graph** (router files, `navigationDestination`s, deep links, tabs, sheets, modals) — every reachable screen is a row.
- Walk the **feature folders** and enumerate every view file; every view that renders something is a row or part of one.
- Walk the **build targets** — every companion and extension target the project ships is its own surface with its own matrix section: watch app, home/lock-screen widgets, complications, share/action extensions, App Intents/Siri, keyboard extensions. If the target exists, it gets rows; a surface is never "verified" because the host app is. (Widgets are the classic miss: they render app data through their own provider code path, and that path shipping wrong numbers looks exactly like the app working.)
- Expand **enums and modes into their own rows**: every exercise type, every quiz mode, every section kind, every settings row, every empty/error/loading state. "Test section ✅" is not a status — "test section: choice ✅ / tone ✅ / matching ✅ / writing ◐ / fill-blank ✅" is.
- **Polymorphic list rows get one row per variant, including the tap destination.** A list whose rows carry a type that changes where tapping navigates (word → dictionary, quote → quote screen, grammar topic → ???) is N features, not one. "Item list renders ✅" proved nothing about "tapping a grammar item lands somewhere real" — that exact gap shipped a per-type dead end past a green suite (collections escape, 2026-08-23).
- For ports: cross-check the enumeration against the source app's screens/components so nothing the spec has is missing from the list.
- Every row starts at ❌. Rows are never deleted, only re-statused.

**Definition of done = 100% of rows dispositioned:** every row is either ✅ (named automated test), or a justified ◐/manual item with a one-line reason ("needs physical mic") that the user has seen and accepted. 🔍 and unexplained ❌ are debt, and the skill's loop keeps working until none remain. Report progress as a fraction (e.g. "41/58 rows ✅, 9 manual-justified, 8 remaining").

Structure of the doc:

- A **"READ FIRST, future agents"** section: what the doc is, the rules below, the project's verification toolbox with exact commands, and hard-won automation gotchas as you collect them.
- Status legend: ✅ **Automated** (a named test fails if this breaks) / 🔍 **Visual** (screenshot once, no protection) / ◐ **Partial** (state what's covered and what isn't) / ❌ **Unverified** (compiled, nothing more).
- Sections: core logic, services/backends, screens & flows. One row per feature, status + how + what's missing.
- A **blind-spots section**: what your automation can NOT prove (e.g. "quiz tests answer randomly — flows complete, but correct answers aren't asserted correct").

**Rules (put these verbatim in the doc):**
1. Never mark ✅ without naming the test.
2. 🔍 is a snapshot in time — any later change to that screen invalidates it.
3. Update the feature's row in the same commit as the change.
4. When a bug escapes to the user, record the escape in the row — it's evidence the old status was too optimistic.
5. Be precise about what a test proves (see blind-spots).
6. For ports: parity-diff against the spec before trusting any ◐/❌ row.
7. **Parity is not correctness.** The spec app has its own bugs; a faithful port reproduces them and the parity diff then *confirms* the broken behavior as "matching spec". When a flow dead-ends or misbehaves identically in the spec app, that's a finding to flag to the user (fix-or-inherit is their call), never silent verification. Keep a "spec-app dead ends" list in the matrix.

## Phase 2 — Work the matrix to 100%, in layers of increasing cost

The matrix is the worklist: iterate over its ❌/🔍/◐ rows (highest-risk first — money paths, data-loss paths, anything users touch daily) and upgrade each with the cheapest layer that honestly proves it. Keep looping — self-paced, background runs — until the Definition of done holds.

1. **Unit** — for logic buried in views/services, extract a pure seam first (a static function, a protocol + default-parameter injection, a `decode(data:)` split from the bundle load), then test the seam. Prefer many small extraction commits.
2. **Integration with real backends, locally** — Firebase emulator suite, testcontainers, local DB. Wrap in a runner script that starts the backend, injects a flag/env into the app under test, runs the gated suite, tears down. Gate the suite on that env so normal runs skip it. This layer catches API-semantics bugs unit tests can't (e.g. `setData(merge:)` vs `updateData` dotted-path behavior).
3. **Deep-link + screenshot visual passes** — cheap; records only 🔍. Also sweep Dynamic-Type/large-font and smallest-supported-device once. Three rules: confirm the intended fixture state actually exists before shooting (a prior test run may have wiped or replaced the seed data — an "empty state" sweep that was meant to be a "seeded" sweep records the wrong rows); actually LOOK at every shot — the pass has zero value if the images are captured but unreviewed; and review each shot for **design coherence, not just layout** — check every prominent color against the app's palette/token file, and flag any hue that fights the brand's temperature or appears nowhere else in the design. No test asserts colors, and for ports parity actively blesses the wrong ones — the collections Quiz button shipped the spec's cold-blue `secondary` into a warm green brand, parity-correct and user-flagged by hand (2026-08-23). An off-brand-but-faithful screen is a finding for the user (restyle-or-inherit is their call), recorded in the matrix like any other. Reviewed shots also catch real layout bugs (content pinned under floating chrome, mis-fired overlays).
4. **UI/E2E automation** — the only thing that makes a *screen* ✅. Drive real flows end to end (sign-out→sign-in, complete a lesson, run a session). Make tests self-seeding (create the data they need) and state-tolerant (a prior failed run may leave the app mid-flow). **Seed through the production write path** (the same store/API call the app uses), not hand-built minimal fixtures: a hand-made seed contains only the data shapes you thought of, while the production path creates the shapes users actually get — the collections escape survived precisely because tests seeded easy word items instead of calling the lesson-save path that also creates English-titled grammar items. Gate anything that costs money or external quota (live agents, paid APIs) behind an explicit env var; it must skip, not fail, without it. **Run on a dedicated device/instance — see "Isolated test devices" below.**
5. **Leave honest ❌** for what genuinely needs a human/device (mic quality, haptics, store sign-in providers) — listed, not forgotten.

**The fix loop:** bug found → fix → regression test that would have caught it → matrix row updated → one conventional-commit per logical change (follow the repo's attribution policy). Report findings faithfully; if something is broken and you didn't fix it, the matrix says so.

**The regression test must live at the layer where the bug lived.** Extracting the fix into a pure helper and unit-testing the helper proves the helper — not that production ever calls it: a green unit test on the seam says nothing about reachability (a fix once shipped "verified" while its lookup silently matched nothing in the real flow, caught only by E2E). If the bug was in wiring, state lifetime, or lookup identity, the regression drives the real flow; add the cheap unit test *in addition*, never *instead*.

## Phase 3 — Machine enforcement (make it a working system)

Prose doesn't survive agent turnover. Install both gates:

**Git pre-commit** (`.githooks/pre-commit`, activate with `git config core.hooksPath .githooks`, document that in CLAUDE.md):
```bash
#!/bin/bash
set -euo pipefail
[ "${SKIP_VERIFY_MATRIX:-0}" = "1" ] && exit 0
staged="$(git diff --cached --name-only)"
touches_code=false
while IFS= read -r f; do case "$f" in {CODE_PATHS}) touches_code=true;; esac; done <<< "$staged"
$touches_code || exit 0
echo "$staged" | grep -qx "docs/verification-coverage.md" && exit 0
echo "✋ Commit touches app/test code without updating docs/verification-coverage.md." >&2
echo "   Update the feature's row and stage it. Non-behavioral change? SKIP_VERIFY_MATRIX=1 git commit" >&2
exit 1
```
Replace `{CODE_PATHS}` with the repo's source/test globs (e.g. `src/*|tests/*` or `App/*|AppTests/*`).

**Claude Code Stop hook** (`.claude/settings.json` → `scripts/check-verification-matrix.sh`): on Stop, if `git status --porcelain -uall` shows code changes without a matrix change, emit `{"decision":"block","reason":"…update the matrix row…"}`; pass through when `stop_hook_active` is true (loop guard). Use `-uall` — untracked directories otherwise collapse and hide files.

**Test the gates before committing them**: a code-only commit must block; code+matrix must pass; the bypass must work; the Stop hook must block, pass, and respect the loop guard. Two subtleties from live use: an UNTRACKED matrix file still counts as "touched" in `git status`, masking the Stop hook's block case — test that case with the file moved aside; and when a later commit's matrix delta already landed in an earlier commit, the pre-commit gate still (correctly) blocks — keep a **session-log section in the matrix** so every commit has a legitimate one-line delta, instead of reaching for the bypass.

Finally: add a **MANDATORY section to the repo's CLAUDE.md** pointing at the matrix and the gates, so every future session loads the requirement automatically.

## Automation gotchas (seed the project's own list with these)

- UI-framework text transforms (uppercased section headers) break exact-label queries — query what *renders*.
- Rows/chips inside buttons register as buttons, not text elements.
- Loading screens flash transient values — never match a result by one element; require a co-present anchor (e.g. score AND its Continue button).
- Cached element references go stale across re-renders — re-query directly before tapping anything that appears during loading.
- On failure, export the test-runner's artifacts (screenshots, UI hierarchy, crash logs) before theorizing; a crash log means the app died, not that the element was missing.
- Never trigger OS permission dialogs in automation — pre-grant via tooling (`simctl privacy …`) or take the UI path that avoids them.
- Background long runs; verify from their logs, not from optimism.
- **Environmental capabilities are flaky, not just absent** — an on-device AI model, network service, or sensor can become available mid-session and silently flip which code path automation exercises. Pin it with a DEBUG `--force-no-<capability>` launch flag. Fallback tests guarded on `!available` stay honest but silently lose coverage whenever the capability is warm — record that in the matrix.
- **"0 tests passed" is a failure, never a pass.** It means the selection filter matched nothing (some frameworks match suite/type names, not file names) or the test host crash-looped (crash logs in the runner artifacts are the tell — a teardown/deinit asserting main-thread isolation off-thread crashes exactly this way). Always compare the count of tests that RAN against the count you expected.
- Never debug through your own output filters: a pipe that greps for "failed" makes a skipped phase indistinguishable from a passing one. Confirm counts from raw logs or the result bundle.
- A stale incremental build can re-run OLD code after an edit — if a failure reproduces previous line numbers/messages, touch the file and confirm a fresh "Compiling" line before trusting the run.
- "Hittable" checks may ignore overlay occlusion — an element under a floating bar reports hittable while the overlay swallows the tap. Scroll and assert by frame geometry, not hittability.

## Isolated test devices — never share a simulator/emulator

Sharing a device causes two real failure modes: you terminate/relaunch the app under the user's fingers, and concurrent runs (another agent, another background xcodebuild) corrupt each other's results. So:

- **Create your own device at session start** and use its UDID for every build/test/launch — never the user's booted device and never a hardcoded shared UDID:
  - iOS: `UDID=$(xcrun simctl create "QA-$(basename "$PWD")-$$" <device-type> <runtime>)`; boot it, run everything against `-destination 'platform=iOS Simulator,id='"$UDID"`. Reuse it across the session; `simctl shutdown` (keep) or `simctl delete` (dispose) when done. Grants (`simctl privacy`), content-size overrides, and app-group seeds all target that UDID.
  - Android: dedicated AVD name + explicit port (`emulator -avd qa-<proj> -port 56xx`); web E2E: fresh browser profile/user-data-dir per agent; backend integration: unique DB/emulator project name or port per agent.
- **Serialize runs per device**: one xcodebuild/test process per UDID at a time — a second concurrent run against the same device produces truncated logs and phantom failures. If you need parallelism, create more devices.
- **Parallel test-writing agents share one repo**: tell each agent the worktree is shared (other agents' dirty files and new tests are expected — leave them alone), forbid agents from committing (you review, run, and commit), and serialize project-file regeneration (xcodegen/codegen rewrites race) — an agent regenerating while another's build is mid-flight corrupts both. Per-agent devices, one shared source tree, commits only from the orchestrator.
- **The user's device is read-only territory**: only touch it when reproducing something they reported there, announce it first, and leave the app in the state you found it.
- Ephemeral device state (permissions, sign-ins, seeded data) does not carry over to a fresh device — self-seeding tests (rule above) make this a non-issue.

## Companion surfaces: Apple Watch, widgets, and other embedded targets

Companion and extension targets are part of the app, not an appendix — each gets its **own matrix section**, enumerated the same way, and none is "verified" because the host app is. When Phase 1's target walk finds a watch app or widget target, these sections are mandatory, not optional.

### Widgets (home screen, lock screen, complications)

- **One row per widget kind AND per supported family** (systemSmall/Medium/…, accessoryCircular/Rectangular/Inline) — families render different code paths and truncate differently.
- **Extract the provider math into a seam shared by ALL providers.** Two widgets that each compute "today's total" independently WILL disagree eventually (a home-screen vs lock-screen count mismatch shipped exactly this way); after extraction the disagreement is impossible by construction, and the seam gets unit tests for the day boundary, totals, list caps, and sort/edge cases (zero-limit, empty store).
- **Refresh policy is testable logic, not plumbing**: assert the next timeline entry never crosses midnight (yesterday's total showing as today is the canonical widget bug) and that the refresh cadence is what you intended.
- **The App Group data path is its own row**: the widget reads a different container via a different process — seed the group store, then verify the provider sees it. Widget *rendering* and the OS actually delivering timeline reloads (`WidgetCenter` triggers) usually stay ◐/manual — say so in the row rather than letting the seam tests masquerade as end-to-end coverage.
- Screenshot each family once for the visual layer (🔍), and re-shoot when the widget view changes.

### Apple Watch

- **Dedicated paired simulators**, same isolation rules as above — never the user's pair:
  ```bash
  PHONE=$(xcrun simctl create "QA-phone-$$" com.apple.CoreSimulator.SimDeviceType.iPhone-16-Pro <ios-runtime>)
  WATCH=$(xcrun simctl create "QA-watch-$$" com.apple.CoreSimulator.SimDeviceType.Apple-Watch-Series-10-46mm <watchos-runtime>)
  xcrun simctl pair "$WATCH" "$PHONE" && xcrun simctl boot "$PHONE" && xcrun simctl boot "$WATCH"
  ```
  Runtimes must be a compatible iOS/watchOS pairing or `pair` fails. Watch sims boot slowly and first launches are slower still — use generous timeouts, and screenshot via `simctl io "$WATCH" screenshot`.
- **Layered like everything else**: shared logic goes in a cross-platform module and gets unit-tested once (cheapest); watch-only logic gets a watch test bundle run with `-destination 'platform=watchOS Simulator,id='"$WATCH"`; watch UI flows get XCUITest on the watch scheme (it works on watchOS — smaller API surface, same rules); complications/widgets get their timeline-provider seam unit-tested (assert entries for a seeded date range) plus a screenshot of each supported family.
- **WatchConnectivity is its own matrix row per message type**, and the flakiest thing you'll test: both sims must be booted and paired, the counterpart app running; `isReachable` flaps on simulators. Test the session handlers through a seam with recorded payloads (deterministic), keep one live phone↔watch round-trip as the integration check, and mark it ◐ if it won't run reliably headless.
- **Honest ❌ list for watch**: real watch-face complication rendering, always-on display, haptics, workout/HealthKit sensor data, battery behavior — device-only; list them, don't fake them.
- **App Store/marketing capture on watch sims** already has a working recipe in the `marketing-screenshots` skill — reuse its device setup rather than reinventing.

## Operating rules

- The user often tests on the same device/simulator you do — say so before terminating their app (and prefer the dedicated device above so it never comes up).
- Deleting/overwriting cloud data during tests: watch for sync-back paths first (a local wipe that mirrors to the backend is data loss).
- Keep a session summary in the tracking docs: tests before/after, bugs found (and which layer caught each), what still needs the user.
