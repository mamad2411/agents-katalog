---
name: maestro-mobile-testing
description: "Maestro mobile E2E testing patterns for React Native/Expo apps: YAML test flows, testID selectors, adaptive auth state, optimistic update verification, GraalJS scripting, cross-platform stability, CI/CD integration, Maestro Cloud, and MCP server integration. Use when: write Maestro test, flaky mobile test, test my app, automate mobile testing, mobile E2E, debug test failure, Maestro setup."
license: MIT
metadata:
  version: 1.0.0
  category: toolchain
  author: tovimx
  tags: [react-native, expo, testing, maestro, e2e, mobile, ios, android, ci-cd, mcp]
---

# Maestro Mobile E2E Testing

## Overview

Maestro is a declarative YAML-based mobile E2E testing framework. It provides automatic waiting, built-in retry logic, and fast execution without boilerplate. It's more stable than Detox or Appium for React Native apps.

### Key Features

- **Declarative YAML** — no imperative test code, just steps
- **Automatic waiting** — no manual `sleep()` or flaky waits
- **Built-in retry** — reduces test flakiness
- **Fast execution** — runs quickly without setup overhead
- **Maestro Studio** — interactive test builder (`maestro studio`)
- **Sub-flows** — reusable YAML sequences for DRY tests
- **JavaScript scripting** — GraalJS runtime for HTTP calls and data manipulation
- **Maestro Cloud** — real device testing in CI without local simulators

## Quick Start

### Install

```bash
curl -Ls "https://get.maestro.mobile.dev" | bash
brew install openjdk@17
export JAVA_HOME=/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home
```

### Minimal test

```yaml
appId: com.myapp
---
- launchApp
- tapOn:
    id: "my-button"
- assertVisible: "Expected Text"
```

### Run

```bash
maestro test .maestro/smoke-test.yaml
maestro test --debug .maestro/smoke-test.yaml  # step through
maestro studio                                  # interactive builder
```

## Pattern Index

| # | Pattern | Reference |
|---|---------|-----------|
| 1 | Selector Strategy: testID vs Text | [core-patterns.md](references/core-patterns.md#1-selector-strategy-testid-vs-text) |
| 2 | Auth Pre-Flight Pattern | [core-patterns.md](references/core-patterns.md#2-auth-pre-flight-pattern) |
| 3 | Adaptive Tests (Both Auth States) | [core-patterns.md](references/core-patterns.md#3-adaptive-tests-handle-both-auth-states) |
| 4 | Testing Optimistic Updates | [core-patterns.md](references/core-patterns.md#4-testing-optimistic-updates) |
| 5 | Dismissing Native Alerts | [core-patterns.md](references/core-patterns.md#5-dismissing-native-alerts) |
| 6 | Sub-Flows for Reusability | [core-patterns.md](references/core-patterns.md#6-sub-flows-for-reusability) |
| 7 | Deep Links (Expo) | [core-patterns.md](references/core-patterns.md#7-deep-links-expo) |
| 8 | Platform-Specific Logic | [core-patterns.md](references/core-patterns.md#8-platform-specific-logic) |
| 9 | Environment Variables | [core-patterns.md](references/core-patterns.md#9-environment-variables) |
| 10 | Selector State Properties | [core-patterns.md](references/core-patterns.md#10-selector-state-properties) |
| 11 | Relative Position Selectors | [core-patterns.md](references/core-patterns.md#11-relative-position-selectors) |
| - | OTP/Magic-Link Auth Testing | [auth-testing.md](references/auth-testing.md) |
| - | CI/CD & Maestro Cloud | [ci-cd.md](references/ci-cd.md) |
| - | Critical Gotchas & Platform Differences | [gotchas.md](references/gotchas.md) |
| - | MCP Server Integration | [mcp-integration.md](references/mcp-integration.md) |

## Test File Template

```yaml
# {Feature} {Action} Test
#
# Tests: {what this validates}
# Prerequisites:
# - Simulator/emulator running with app installed
# - Backend or mock server running (if API-dependent)

appId: com.myapp
env:
  TEST_EMAIL: maestro-{feature}@example.com
  EMAIL_SERVICE_URL: http://localhost:8025
---
# ==========================================
# STEP 1: LAUNCH + AUTH PRE-FLIGHT
# ==========================================

- launchApp

- swipe:
    direction: DOWN
    duration: 100

- extendedWaitUntil:
    visible:
      id: "auth-loaded"
    timeout: 15000

- takeScreenshot: 01-initial-state

# ==========================================
# STEP 2: {ACTION}
# ==========================================

- tapOn:
    id: "target-element"

# ==========================================
# STEP 3: VERIFY
# ==========================================

- extendedWaitUntil:
    visible:
      id: "expected-result"
    timeout: 5000

- takeScreenshot: 02-final-state
```

## Example Output

Running a Maestro test produces output like this:

```
$ maestro test .maestro/smoke-test.yaml

 ║
 ║  > Flow: .maestro/smoke-test.yaml
 ║
 ║    ✅  Launch app "com.myapp"
 ║    ✅  Swipe from center to bottom
 ║    ✅  Wait until "auth-loaded" is visible (timeout: 15s)
 ║    ✅  Take screenshot "01-initial-state"
 ║    ✅  Tap on "tab-home"
 ║    ✅  Wait until "dashboard-header" is visible (timeout: 5s)
 ║    ✅  Tap on "action-button"
 ║    ✅  Wait until "undo-button" is visible (timeout: 3s)
 ║    ✅  Take screenshot "02-final-state"
 ║
 ║    Duration: 8.2s
 ║    Status: ✅ PASSED
```

Screenshots are saved to `~/.maestro/tests/{timestamp}/`.

## Folder Structure

```
.maestro/
├── README.md                    # Quick reference + testID inventory
├── config.yaml                  # Shared configuration
├── flows/                       # Reusable sub-flows
│   ├── auth-and-return.yaml
│   ├── complete-action.yaml
│   └── verify-result.yaml
├── scripts/                     # GraalJS helpers
│   ├── fetch-otp.js
│   └── split-otp.js
├── smoke-test.yaml              # Guest navigation
├── auth-signin.yaml             # OTP sign-in flow
├── feature-screenshots.yaml     # Screenshot capture flows
└── feature-action.yaml          # Feature-specific tests

scripts/
├── mock-api-server.ts           # Lightweight mock for E2E
└── run-e2e.sh                   # Orchestration script
```

### Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Main test | `{feature}-{action}.yaml` | `checkout-purchase.yaml` |
| Sub-flow | `{action}-{context}.yaml` | `auth-and-return-to-dashboard.yaml` |
| Script | `{verb}-{noun}.js` | `fetch-otp.js` |

## Troubleshooting

### Device Not Found

```
Error: No devices found
```

**Cause:** No simulator/emulator running, or Maestro can't detect it.

**Fix:**
- iOS: Open Xcode > Window > Devices and Simulators > boot a simulator, or run `xcrun simctl boot "iPhone 16"`
- Android: Start emulator with `emulator -avd <name>` or open Android Studio > Device Manager
- Verify with `maestro devices` (should list at least one device)

### Element Not Found

```
Error: Element not found: id "my-button"
```

**Cause:** The element hasn't rendered yet, the testID is wrong, or a native alert is blocking it.

**Fix:**
1. Run `maestro hierarchy` to see all elements on screen — check if your element exists
2. Use `maestro studio` to interactively explore the element tree
3. Add `extendedWaitUntil` before the interaction (the element may need time to render)
4. Check if a native alert or permission dialog is blocking — add `tapOn: text: "OK" optional: true` before your step
5. Verify the testID is actually set in your React Native component (`testID="my-button"`)

### Flaky Tests

**Symptoms:** Test passes sometimes, fails other times.

**Common causes and fixes:**
- **Race conditions**: Add auth pre-flight pattern (Pattern 2) — don't interact before auth resolves
- **Animations**: Use `extendedWaitUntil` instead of fixed `sleep` calls
- **Network dependency**: Start a mock API server instead of relying on real backends
- **iOS cold boot crash**: Add the post-launch swipe (see [gotchas.md](references/gotchas.md))
- **Optional elements**: Don't use `optional: true` unless the action is genuinely optional

### Checklist for New Tests

```
[ ] Unique test email (maestro-{feature}@example.com)
[ ] Selector strategy chosen (testID for i18n, text for single-language)
[ ] Auth pre-flight pattern used (auth-loaded)
[ ] Post-launch swipe added (iOS crash prevention)
[ ] Both auth states handled (adaptive flows)
[ ] Native alerts dismissed after mutations
[ ] Short timeouts for optimistic updates (3-5s)
[ ] Sub-flows created for reusable sequences
[ ] Descriptive screenshots at key points
[ ] Header comment with prerequisites
[ ] Mock API server started if backend-dependent
[ ] Tags added for CI filtering (ci, smoke, wip)
```

## Debugging

```bash
maestro test --debug .maestro/test.yaml   # Step through interactively
maestro record .maestro/test.yaml          # Record as video
maestro studio                             # Interactive UI builder
maestro hierarchy                          # View element tree
```

## Resources

- [Maestro Documentation](https://docs.maestro.dev/)
- [Maestro Selectors Reference](https://docs.maestro.dev/api-reference/selectors)
- [Maestro Cloud](https://cloud.maestro.dev/)
- [Maestro MCP Server](https://docs.maestro.dev/getting-started/maestro-mcp)
- [Maestro GitHub](https://github.com/mobile-dev-inc/Maestro)
- [GraalJS HTTP Requests](https://docs.maestro.dev/advanced/javascript/make-http-s-requests)
- [Conditions & Adaptive Flows](https://docs.maestro.dev/advanced/conditions)
- [GitHub Actions Integration](https://docs.maestro.dev/cloud/ci-integration/github-actions)
