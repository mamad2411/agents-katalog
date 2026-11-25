---
name: qa-mobile
description: Author, execute, diagnose and maintain mobile QA for Android, iOS and hybrid apps through the team's available device or simulator tools. Load through qa for mobile scope; mobile web alone uses qa-web.
---

# Mobile execution specialist

Continue the `/qa` workflow. The existing `core.md`, `test-automation.md`,
`code-review.md` and `ticket-state.md` own shared contracts; this skill adds
mobile mechanics. The orchestrator or an assigned general worker authors tests;
the execution-only test-runner runs selected tests and preserves evidence.

## Prepare the target

1. Read the feature contract and identify native Android/iOS, React Native,
   Flutter, embedded WebView, or browser-only scope. Inventory the existing
   automation language, framework, build command and CI device strategy before
   adding tools. Read only the chosen recipe: [Maestro](references/maestro.md),
   [Appium/hybrid](references/appium.md), or [native tests](references/native.md).
2. Inspect capabilities, not just config: SDK/driver/client versions, installed
   device images, attached serials/UDIDs, selected Xcode, signing/provisioning,
   build ABI, OS/minimum target and free resources. Missing iOS runtime does not
   invalidate useful Android work. Preserve exact blocker and unexecuted scope.
3. Pin app package/bundle, APK/IPA/app hash, source revision when available,
   build variant, API/backend configuration, device identity, OS/build, locale,
   orientation and permission state. Check endpoints in the actual installed
   build or observed traffic before mutating a connected backend. An app called
   “staging” is insufficient. A simulator `.app` and physical-device IPA have
   different architectures/signing requirements.
4. Prefer a task-owned simulator/emulator when available. Never default to the
   first connected device. On shared physical hardware, scope app-data reset,
   uninstall, permissions and media changes to approved test data. Do not reset
   the whole device or iOS keychain. Check whether reinstall clears data; do not
   assume it does. Keep fresh-install, upgrade and retained-data cases separate.

## Author a useful slice

Map criterion → mobile risk → setup → action → independent observable outcome.
Select relevant cases, not a mandatory matrix for every small ticket:

- Input partitions and boundaries; keyboard/IME interactions; scrolling and
  obscured controls; back navigation and cancellation; business state after
  failed, interrupted or duplicate submissions.
- Permission first ask, allow, deny and later revocation when the feature uses
  it. Explicitly configure prompts; blanket auto-grants erase denial coverage.
- Background/foreground, process termination/relaunch and activity recreation
  where state matters. These are different transitions; relaunch with a reset
  does not test persistence. Add deep-link, rotation, interrupted network or
  upgrade cases only when they expose a scoped risk.
- Isolated app state, synthetic accounts/data and backend cleanup. A local app
  reset does not delete server fixtures. Pair permitted actors for access risks;
  route selected security/performance work to those overlays.

Inspect the installed accessibility hierarchy/Inspector or native test tree.
Prove that the locator uniquely identifies the intended control and that its
action reaches the expected state. Use accessible semantics/resource IDs/test
identifiers actually observed; source IDs supplement the runtime proof. Control
locale for text assertions. Re-query after navigation/context changes; avoid
stale element handles. A Flutter key is not automatically an accessibility ID.

Wait for observable readiness, transitions and business completion using the
runner's assertions, idling resources or explicit bounded waits. Animation idle
alone does not prove an asynchronous save completed. Do not replace unresolved
synchronization with sleeps, automatic full-test retries or weakened assertions.

## Execute and diagnose

Run the selected tests on the pinned serial/UDID. Record command, exit code,
test count, runner/app/image identity and artifact paths. Capture initial
permission/state setup and cleanup results. Real driver, real installed app and
observable assertions are required for device-executed claims; YAML parsing,
mock-driver calls and source inspection are separate evidence categories.

On failure preserve first output, screenshot, hierarchy, runner/server logs and
scoped device logs. Determine whether app crashed/ANR'd, OS/permission dialog
blocked interaction, locator was absent/ambiguous, WebView context changed,
fixture/backend was wrong, or a business assertion failed. Use timestamp/process
correlation; unrelated device log errors are not product defects. Follow the
shared single diagnostic-rerun limit and state the hypothesis before rerunning.

## Maintain and hand off

After a fix, keep the detecting assertions and test hash unchanged when comparing
builds. Record any necessary test repair separately with its original failure.
Centralize repeated navigation only when repetition exists; keep criterion
assertions readable. Revalidate locators and timings against changed builds.
Retain device coverage gaps and device-only risks such as camera, push delivery,
power, radio/BLE and OS vendor differences; emulation cannot establish them.

Stop only owned processes, remove task-created device/app/backend fixtures and
verify cleanup. Keep redacted screenshots/logs with the handoff. Report mobile
results by OS/device/build and distinguish native execution, manual observation,
source-only checks and not-run adaptations. The disposable reference target is
documented in `tools/specialists/mobile/README.md`; it is optional, not a product
test runner requirement.
