---
name: test-prerequisite-detection
description: "Prerequisite and environment failure detection and classification. Use when analyzing test failures to determine if they are prerequisite issues, environment problems, or actual feature failures. Triggers on: prerequisite failure, environment issue, failure classification, blocker detection, test-debt."
---

# Test Prerequisite Detection

> Load this skill when: classifying test failures, detecting prerequisite blockers, handling environment issues, or managing test-debt.json.

## Prerequisite Failure Detection

> 🎯 **Distinguish prerequisite failures from feature failures.**
>
> When a test fails, analyze WHERE it failed to determine the appropriate fix action.
> A login failure blocking a menu test is a different problem than a missing menu item.

### Failure Classification Algorithm

```
Test failure occurs
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 1: Parse test file for markers                                  │
│                                                                     │
│ Extract from JSDoc header:                                          │
│   • @prerequisites — Steps that must succeed before feature test    │
│   • @feature-assertions — The actual feature under test             │
│                                                                     │
│ If markers missing, use heuristic detection (Step 1b)               │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 2: Analyze failure location                                     │
│                                                                     │
│ Parse Playwright error output:                                       │
│   • Extract line number of failure                                   │
│   • Extract selector or assertion that failed                        │
│   • Compare against @prerequisites vs @feature-assertions            │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 3: Classify failure                                             │
│                                                                     │
│ ├─── Failure in prerequisite step ──► PREREQUISITE FAILURE          │
│ │    (e.g., login failed, page didn't load)                         │
│ │                                                                   │
│ ├─── Failure in feature assertion ──► FEATURE FAILURE               │
│ │    (e.g., button not found, wrong text)                           │
│ │                                                                   │
│ ├─── Test syntax error or import ──► TEST_INVALID                   │
│ │    (e.g., SyntaxError, Module not found)                          │
│ │                                                                   │
│ └─── Environment/infrastructure ──► ENVIRONMENT                     │
│      (e.g., port conflict, process conflict)                        │
└─────────────────────────────────────────────────────────────────────┘
```

### Heuristic Detection (Fallback)

When test files lack `@prerequisites`/`@feature-assertions` markers:

| Failure Pattern | Classification | Confidence |
|-----------------|----------------|------------|
| Login/auth error before feature test | Prerequisite | High |
| `page.goto()` fails with 404/500 | Prerequisite | High |
| `page.goto()` times out | Prerequisite | High |
| Navigation click fails before reaching feature | Prerequisite | Medium |
| Timeout waiting for element in feature component | Feature | High |
| Assertion failed on feature behavior | Feature | High |
| Element not found for feature under test | Feature | High |
| `SyntaxError` in test file | Test Invalid | High |
| `Cannot find module` / `Module not found` | Test Invalid | High |
| Test-specific variable `is not defined` | Test Invalid | High |

**Detection regex patterns:**

```javascript
const PREREQUISITE_PATTERNS = [
  /Error: page\.goto.*(?:404|500|timeout)/i,
  /Error: .*login.*(?:failed|timeout)/i,
  /Error: .*auth.*(?:failed|unauthorized)/i,
  /Timeout.*waiting for.*navigation/i,
  /net::ERR_CONNECTION_REFUSED/i,
  /ECONNREFUSED/i,
];

const TEST_INVALID_PATTERNS = [
  /SyntaxError:/,
  /Cannot find module/,
  /Module not found/,
  /is not defined/,
  /Unexpected token/,
];

const ENVIRONMENT_PATTERNS = [
  /EADDRINUSE/,
  /already running/i,
  /single instance/i,
  /port.*in use/i,
  /EACCES|EPERM|EBUSY/,
];
```

### Failure Classification Output

```typescript
interface FailureClassification {
  type: "PREREQUISITE" | "FEATURE" | "TEST_INVALID" | "ENVIRONMENT";
  component: string;
  error: string;
  failedAt: string;
  confidence: "high" | "medium" | "low";
  existingTest?: string;
  suggestedFix?: {
    agent: "@developer" | "@ui-tester-playwright";
    description: string;
  };
}
```

### Prerequisite Failure Report Format

```
═══════════════════════════════════════════════════════════════════════
              ⚠️ PREREQUISITE FAILURE DETECTED
═══════════════════════════════════════════════════════════════════════

Feature under test: Add "Settings" option to profile dropdown
Status: NOT TESTED (blocked by prerequisite)

Prerequisite that failed:
  ❌ Login: "Timeout waiting for '[data-testid="login-submit"]'"
  
  This appears to be an auth/login issue, not a problem with your feature.
  Your menu option change was NOT tested.

Classification confidence: HIGH
Existing test found: tests/e2e/auth.spec.ts

Screenshot: ai-tmp/verification/screenshots/login-failure.png

Entering automated fix loop...
═══════════════════════════════════════════════════════════════════════
```

---

## Environment Prerequisite Detection

> 🔧 **Environment prerequisites are infrastructure issues that cannot be fixed by code changes.**

### Environment vs Application Prerequisites

| Type | Examples | Fix Method |
|------|----------|------------|
| **Application** | Login bug, missing element, API error | Code change via @developer |
| **Environment** | Process conflict, port in use, native app bootstrap | Skill-based recovery |

### Environment Prerequisite Categories

| Category | Detection Patterns | Example Skills |
|----------|-------------------|----------------|
| **Process management** | `EADDRINUSE`, `already running`, `single instance` | `ui-test-electron` |
| **Port/service availability** | `ECONNREFUSED`, `port in use`, connection timeout | `start-dev-server` |
| **Native app bootstrap** | Platform-specific launch errors | `ui-test-electron`, `tauri-testing` |
| **External services** | HTTP 503, 429, `service unavailable` | N/A (wait or mock) |
| **File system** | `EACCES`, `EBUSY`, `EPERM` | Manual intervention |

### Environment Detection Patterns

```javascript
const ENVIRONMENT_PATTERNS = {
  processConflict: [
    /EADDRINUSE/,
    /already running/i,
    /single instance/i,
    /another instance/i,
    /lock file exists/i,
  ],
  zombieProcess: [
    /multiple.*Electron.*processes/i,
    /orphaned.*process/i,
    /zombie.*process/i,
    /stale.*process/i,
  ],
  portConflict: [
    /port.*in use/i,
    /ECONNREFUSED/,
    /connection refused/i,
    /net::ERR_CONNECTION_REFUSED/,
  ],
  nativeAppBootstrap: [
    /electron.*failed/i,
    /app launch.*failed/i,
    /cannot connect to.*app/i,
    /BrowserContext.*launch/,
  ],
  externalService: [
    /503 Service Unavailable/,
    /429 Too Many Requests/,
    /rate limit/i,
    /service unavailable/i,
  ],
  fileSystem: [
    /EACCES/,
    /EPERM/,
    /EBUSY/,
    /permission denied/i,
    /file is locked/i,
  ],
};
```

### Electron Zombie Process Pre-Check

> ⚠️ **Run this check BEFORE launching Electron E2E tests.**

**Detection:**

```bash
ZOMBIE_COUNT=$(pgrep -f "Electron" | wc -l | tr -d ' ')

if [ "$ZOMBIE_COUNT" -gt "0" ]; then
  echo "⚠️ Found $ZOMBIE_COUNT Electron-related processes"
  pgrep -af "Electron" 2>/dev/null || true
fi
```

**Prompt:**

```
═══════════════════════════════════════════════════════════════════════
              ⚠️ ZOMBIE ELECTRON PROCESSES DETECTED
═══════════════════════════════════════════════════════════════════════

Found 3 Electron-related processes that may interfere with tests:

  PID 12345: Electron Helper (Renderer)
  PID 12346: Electron Helper (GPU)
  PID 12347: YourApp

[K] Kill all and continue
[S] Skip cleanup (may cause test failures)
[C] Cancel tests

═══════════════════════════════════════════════════════════════════════
```

### Environment Fix Flow

```
ENVIRONMENT prerequisite detected
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 1: Categorize the environment issue                            │
│                                                                     │
│ Match error against ENVIRONMENT_PATTERNS                            │
│ → processConflict, portConflict, nativeAppBootstrap, etc.           │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 2: Search for matching skill                                    │
│                                                                     │
│ Skill naming convention: {category}-testing                         │
│                                                                     │
│ ├─── SKILL FOUND ──► Load skill, run recovery procedure             │
│ └─── NO SKILL ──► Offer skill creation request                      │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 3: Execute skill recovery                                       │
│                                                                     │
│ 1. Load skill via skill tool                                         │
│ 2. Execute skill's environment recovery steps                       │
│ 3. Retry the original test                                          │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Blocker Tracking (test-debt.json)

> 🚧 **Track prerequisite blockers that affect multiple features.**

### File Location

```
<project>/ai-tmp/test-debt.json
```

### Structure

```json
{
  "schemaVersion": 1,
  "prerequisiteBlockers": [
    {
      "id": "auth-login-timeout",
      "prerequisite": "login",
      "type": "application",
      "error": "Timeout waiting for '[data-testid=\"login-submit\"]'",
      "firstSeen": "2026-03-03T10:30:00Z",
      "lastSeen": "2026-03-03T11:15:00Z",
      "affectedFeatures": [
        {
          "story": "US-005",
          "feature": "Add Settings menu option",
          "testFile": "tests/ui-verify/profile-dropdown-settings.spec.ts",
          "blockedAt": "2026-03-03T10:30:00Z"
        }
      ],
      "status": "open",
      "fixAttempts": 3,
      "lastFixAttempt": "2026-03-03T10:45:00Z"
    }
  ],
  "skippedVerifications": [...],
  "stats": {
    "totalBlockers": 1,
    "openBlockers": 1,
    "resolvedBlockers": 0,
    "totalSkipped": 1,
    "lastUpdated": "2026-03-03T14:00:00Z"
  }
}
```

### Blocker Status Values

| Status | Description |
|--------|-------------|
| `open` | Blocker is active |
| `resolved` | Blocker has been fixed |
| `wont_fix` | Marked as won't fix |

### Known Blocker Detection

When the same prerequisite fails for a different feature:

```
⚠️ KNOWN BLOCKER DETECTED

This feature is blocked by a known issue:
  Blocker: auth-login-timeout
  First seen: 2026-03-03T10:30:00Z
  Other affected features: 1

Options:
  [B] Mark as verification blocked (tracks for bulk re-verify)
  [M] Attempt manual fix
  [S] Skip verification
```

---

## Bulk Re-verification

> 🔄 **Re-verify all features blocked by a resolved prerequisite.**

### Triggering Bulk Re-verification

**User input patterns:**
- "auth is fixed"
- "login is working now"
- "verify-blocked auth-login-timeout"
- "re-verify blocked features"

### Bulk Verification Flow

```
User confirms bulk re-verification
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 1: Verify blocker is fixed                                      │
│                                                                     │
│ Run prerequisite test first                                          │
│ ├─── PASS ──► Blocker is fixed, proceed                              │
│ └─── FAIL ──► Blocker still exists, abort                           │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 2: Verify each affected feature                                 │
│                                                                     │
│ For each feature in affectedFeatures:                                │
│   1. Run verification test                                           │
│   2. Apply 3-pass stability check                                    │
│   3. Record result                                                   │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 3: Update blocker status                                        │
│                                                                     │
│ If all features pass: set status to "resolved"                       │
│ If some fail: keep blocker open for failed features                  │
└─────────────────────────────────────────────────────────────────────┘
```

### Bulk Verification Complete

```
═══════════════════════════════════════════════════════════════════════
              ✅ BULK RE-VERIFICATION COMPLETE
═══════════════════════════════════════════════════════════════════════

Blocker: auth-login-timeout
Status: RESOLVED

Results:
  ✅ US-005: Add Settings menu option — VERIFIED (3/3 passes)
  ✅ US-007: Add Logout confirmation — VERIFIED (3/3 passes)
  ❌ US-012: Add Profile edit link — FAILED (new issue)

Blocker resolved for 2/3 features.

Updated:
  • test-debt.json — blocker marked resolved
  • session.json / chunk.json — verificationBlocked cleared for US-005, US-007
═══════════════════════════════════════════════════════════════════════
```
