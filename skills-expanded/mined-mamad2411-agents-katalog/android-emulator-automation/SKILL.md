---
name: "android-emulator-automation"
description: "Use semantic ADB and UIAutomator workflows to inspect, launch, and interact with Android apps from agents."
metadata:
  version: "0.1.0"
  category: "quality-release"
  tags: ["android", "adb", "uiautomator", "emulator", "automation"]
  triggers:
    include: ["android emulator automation", "adb semantic ui automation", "uiautomator dump and tap", "launch android app and inspect screen", "android agent tap text on emulator"]
    exclude: ["play store release only", "room dao only", "gradle scan only"]
  owners: ["@android-agent-skills/maintainers"]
  test_targets: ["examples/orbittasks-compose", "benchmarks/triggers.jsonl"]
---
# Android Emulator Automation

## When To Use
- Use this skill when the request is about: android emulator automation, adb semantic ui automation, uiautomator dump and tap.
- Primary outcome: Use semantic ADB and UIAutomator workflows to inspect, launch, and interact with Android apps from agents.
- Reach for this skill when an agent needs to launch an APK, inspect the current screen, or perform a deterministic interaction without writing Espresso or Compose UI tests.
- Handoff skills when the scope expands:
- `android-testing-ui`
- `android-permissions-activity-results`

## Workflow
1. Verify the Android SDK, `adb`, the target device or emulator, and boot completion before attempting interaction.
2. Install or launch the target app with explicit package awareness so the request stays tied to the right artifact.
3. Dump the current UI hierarchy and prefer semantic selectors such as text, content description, or resource ID over raw coordinates.
4. Perform the smallest interaction that proves the workflow and re-dump the screen when state changes matter.
5. Hand off long-lived regression coverage to UI tests once the automation path is understood.

## Guardrails
- Prefer semantic selectors to pixel coordinates; only fall back to coordinates when the UI tree is missing the required metadata.
- Treat automation as an inspection and smoke tool, not a replacement for deterministic UI tests.
- Verify device state, package name, and boot completion before issuing input commands.
- Keep the scripts safe for CI by avoiding destructive shell commands or device-wide settings changes.

## Anti-Patterns
- Hard-coding coordinates when text or resource IDs are available.
- Running emulator commands before the device is boot-complete.
- Treating flaky one-off automation as proof of a stable UI workflow.
- Mixing app install, interaction, and log scraping into one opaque script with no intermediate output.

## Examples
### Happy path
- Scenario: Build the Compose fixture, install it on an emulator, and dump the current OrbitTasks screen.
- Command: `bash skills/android-emulator-automation/scripts/run_examples.sh`

### Edge case
- Scenario: Launch a preinstalled app and target a single semantic control without relying on screen coordinates.
- Command: `python3 skills/android-emulator-automation/scripts/navigator.py --find-text "Blocked" --tap`

### Failure recovery
- Scenario: Confirm the device is discoverable and UIAutomator can dump the hierarchy before chasing a selector bug.
- Command: `python3 skills/android-emulator-automation/scripts/device_health.py --json`

## Done Checklist
- The target package, device serial, and current screen are explicit.
- Semantic selectors were preferred over coordinates.
- The automation path is reproducible in local development and CI.
- The request hands off to UI testing when the workflow needs regression coverage.

## Official References
- [https://developer.android.com/studio/run/emulator](https://developer.android.com/studio/run/emulator)
- [https://developer.android.com/tools/adb](https://developer.android.com/tools/adb)
- [https://developer.android.com/training/testing/other-components/ui-automator](https://developer.android.com/training/testing/other-components/ui-automator)
- [https://developer.android.com/studio/test/command-line](https://developer.android.com/studio/test/command-line)
