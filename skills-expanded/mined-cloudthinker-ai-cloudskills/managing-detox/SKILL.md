---
name: managing-detox
description: |
  Use when working with Detox — detox React Native testing management and
  analysis. Covers test configuration review, device and simulator management,
  build configuration analysis, test result parsing, artifact collection, and
  test runner integration. Use when managing Detox test suites, investigating
  mobile test failures, or reviewing React Native E2E testing configurations.
connection_type: detox
preload: false
---

# Detox React Native Testing Management Skill

Manage and analyze Detox end-to-end tests for React Native applications.

## Core Helper Functions

```bash
#!/bin/bash

# Parse Detox configuration
detox_config() {
    if [ -f ".detoxrc.js" ]; then
        node -e "const c = require('./.detoxrc.js'); console.log(JSON.stringify(c, null, 2))" 2>/dev/null
    elif [ -f "detox.config.js" ]; then
        node -e "const c = require('./detox.config.js'); console.log(JSON.stringify(c, null, 2))" 2>/dev/null
    else
        node -e "const pkg = require('./package.json'); console.log(JSON.stringify(pkg.detox || {}, null, 2))" 2>/dev/null
    fi
}
```

## MANDATORY: Discovery-First Pattern

**Always discover Detox configuration and device targets before querying specifics.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Detox Configuration ==="
detox_config | jq '{
    configurations: (.configurations | keys),
    devices: (.devices | keys),
    apps: (.apps | keys),
    testRunner: .testRunner
}' 2>/dev/null

echo ""
echo "=== Detox Version ==="
npx detox --version 2>/dev/null

echo ""
echo "=== Test Files ==="
TEST_DIR=$(detox_config | jq -r '.testRunner.args.testPathPattern // "e2e"' 2>/dev/null || echo "e2e")
find "$TEST_DIR" -name "*.test.ts" -o -name "*.test.js" -o -name "*.spec.ts" -o -name "*.spec.js" 2>/dev/null | head -15

echo ""
echo "=== Available Simulators ==="
xcrun simctl list devices available 2>/dev/null | grep -E "(iPhone|iPad)" | head -10
echo ""
echo "=== Available Emulators ==="
emulator -list-avds 2>/dev/null | head -5
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Build Configurations ==="
detox_config | jq -r '.apps | to_entries[] | "\(.key)\ttype=\(.value.type)\tbuild=\(.value.build // "none" | .[0:60])"' 2>/dev/null | column -t

echo ""
echo "=== Device Configurations ==="
detox_config | jq -r '.devices | to_entries[] | "\(.key)\ttype=\(.value.type)\tdevice=\(.value.device.type // .value.device.avdName // "unknown")"' 2>/dev/null | column -t

echo ""
echo "=== Test Results ==="
ARTIFACTS_DIR="${DETOX_ARTIFACTS_DIR:-artifacts}"
if [ -d "$ARTIFACTS_DIR" ]; then
    LATEST=$(ls -td "$ARTIFACTS_DIR"/*/ 2>/dev/null | head -1)
    if [ -n "$LATEST" ]; then
        echo "Latest artifacts: $LATEST"
        find "$LATEST" -name "*.log" -o -name "*.png" -o -name "*.mp4" 2>/dev/null | wc -l | xargs echo "Artifact files:"
        find "$LATEST" -name "*.log" 2>/dev/null | while read f; do
            echo "--- $(basename $f) (tail) ---"
            tail -5 "$f"
        done | head -20
    fi
fi
```

## Output Rules
- **TOKEN EFFICIENCY**: Target 50 lines per output
- Summarize build/device configs rather than full Detox config
- Reference artifact paths, never embed screenshots or videos

## Anti-Hallucination Rules
- NEVER guess device types or simulator names — discover via system tools
- NEVER fabricate test results — parse actual artifacts and reports
- NEVER assume platform availability — check for Xcode/Android SDK

## Safety Rules
- NEVER build or run tests without user confirmation — builds take significant time
- NEVER delete artifacts without explicit user approval
- NEVER modify Detox configuration without user consent

## Output Format

Present results as a structured report:
```
Managing Detox Report
═════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

