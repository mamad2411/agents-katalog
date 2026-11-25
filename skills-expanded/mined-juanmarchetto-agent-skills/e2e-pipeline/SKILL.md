---
name: e2e-pipeline
description: "Generate and run E2E tests for mobile and web apps. Discovers screens, states, and flows via static analysis, generates Maestro test flows with assertions, executes them, and reports pass/fail results. Use when: run e2e, test flows, e2e tests, generate tests, automated testing."
license: MIT
metadata:
  version: 1.0.0
  category: toolchain
  tags: [e2e, testing, maestro, expo, react-native, assertions, quality]
---

# E2E Pipeline

Generate and run comprehensive E2E tests from static analysis of your codebase. Discovers all screens, states, and flows, generates Maestro test flows with real assertions, and reports results.

## How This Differs From demo-pipeline

demo-pipeline produces **marketing assets** (video recordings, screenshots, animated demos). e2e-pipeline produces **test results** (pass/fail verdicts, regression detection, coverage reports). Same discovery phase, completely different output: demo-pipeline asks "does it look good?" while e2e-pipeline asks "does it work correctly?"

## Workflow

**Pipeline:** DISCOVER > DETECT > GENERATE > EXECUTE > REPORT

### Phase 0: DISCOVER — Flow & State Analysis

Analyze the codebase to map all screens, states, flows, and native dependencies.

**Step 1: Discover screens**
Read the file-based routing structure:
```bash
find src/app -name "*.tsx" -not -name "_layout.tsx" -not -name "+not-found.tsx" | sort
```

**Step 2: Identify states per screen**
Search for UI conditionals:
```bash
grep -n "loading\|isLogged\|isEmpty\|error\|balance.*>\|\.length.*==.*0" src/app/**/*.tsx
```

**Step 3: Map navigation flows**
```bash
grep -rn "router\.push\|router\.replace\|href=" src/app/ src/components/
```

**Step 4: Identify native dependencies**
```bash
grep -rn "expo-camera\|CameraView\|useMobileWallet\|SeedVault" src/
```

**Step 5: Present flow map**
Present the discovered map and ask:
> "I discovered N screens with M states and K flows. Which flows do you want to test? (default: all)"

### Phase 1: DETECT — Project Type & State

Detect project type (Expo/React Native/web) and check running state (device/emulator/server).

### Phase 2: GENERATE — Create Test Flows

For each selected flow, generate a Maestro test YAML with assertions.

**Assertion Reference:**

| Assertion | Maestro equivalent | Use when |
|-----------|-------------------|----------|
| `assert_visible: "Text"` | `- assertVisible: "Text"` | Verify element appears on screen |
| `assert_visible: { id: "elem" }` | `- assertVisible: { id: "elem" }` | Verify element by testID |
| `assert_not_visible: "Text"` | `- assertNotVisible: "Text"` | Verify element is gone |
| `assert_contains: { id: "elem", text: "val" }` | `- assertVisible: { id: "elem", text: "val" }` | Verify element has specific text |
| `assert_enabled: { id: "elem" }` | `- assertVisible: { id: "elem", enabled: true }` | Verify element is interactive |
| `assert_count: { text: "Item", count: 5 }` | `- assertVisible: "Item"` + repeat logic | Verify expected number of elements |
| `assert_text_contains: { id: "elem", text: "partial" }` | `- assertVisible: { id: "elem", containsText: "partial" }` | Verify partial text match |
| `screenshot_on_fail: true` | Maestro auto-captures | Capture state on failure |

**Test YAML format:**
```yaml
flow: "<Flow Name>"
steps:
  - name: "<Step Name>"
    actions:
      - tap: "Element"
      - assert_visible: "Expected Result"
      - screenshot_on_fail: true
```

**Present for approval:**
> "I generated N test flows covering M screens. Review and approve, or select which to run."

**HARD GATE: Do NOT execute until user approves.**

### Phase 3: EXECUTE — Run Tests

**Step 1:** Generate Maestro test files in `./maestro/tests/`:
```bash
mkdir -p maestro/tests
```

**Step 2:** Run all tests:
```bash
maestro test maestro/tests/
```

Or run individually:
```bash
maestro test maestro/tests/flow-name.yaml
```

**Step 3:** Capture failure screenshots:
```bash
mkdir -p screenshots/failures
cp ~/.maestro/tests/*/screenshots/* screenshots/failures/ 2>/dev/null || true
```

### Phase 4: REPORT — Results

Generate `./docs/test-report.md` and present summary.

## Example Output

```
E2E Test Results — 2026-03-16
Passed: 8/10 flows
Failed: 2 (see below)

FAILED checkout-flow:
  assert_visible "Order Confirmed" timed out after 10s
  Screenshot: failures/checkout-timeout.png
  Likely cause: payment API not responding

FAILED search-flow:
  assert_count items expected 5, got 0
  Screenshot: failures/search-empty.png
  Likely cause: API server not running or search index empty

Passed flows:
  login-flow .............. OK (3.2s)
  signup-flow ............. OK (4.1s)
  profile-edit-flow ....... OK (2.8s)
  settings-flow ........... OK (1.9s)
  navigation-flow ......... OK (2.1s)
  logout-flow ............. OK (1.5s)
  onboarding-flow ......... OK (5.3s)
  home-scroll-flow ........ OK (2.0s)

Coverage: 10 flows, 47 assertions, 32 screens
Report saved: ./docs/test-report.md
```

## Error Handling
- If Maestro is not installed: provide install command (`curl -Ls "https://get.maestro.mobile.dev" | bash`)
- If no emulator/device detected: prompt user to start one and provide platform-specific instructions
- If app is not running: attempt to start it, or ask user to launch manually
- If test times out: capture screenshot, report which assertion failed, suggest increasing timeout
- If all tests fail: likely environment issue — check device connection, app state, and API availability
- If flow discovery finds 0 screens: ask user to specify the source directory

## Structure

```
e2e-pipeline/
├── SKILL.md           # This file
├── reference.md       # Complete action and assertion reference
└── templates/
    ├── maestro-test.yaml   # Maestro test template
    └── test-report.md      # Report template
```
