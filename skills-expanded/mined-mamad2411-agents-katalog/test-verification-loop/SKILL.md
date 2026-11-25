---
name: test-verification-loop
description: "3-pass stability verification and automated fix loops. Use when running stability checks, handling test retries, or managing the fix loop algorithm. Triggers on: stability check, 3 passes, fix loop, test retries, verification loop."
---

# Test Verification Loop

> Load this skill when: running 3-pass stability verification, implementing fix loops, or managing test retry logic.

## 3-Pass Stability Verification

> 🔄 **A single passing test run is not enough. Require 3 consecutive passes to declare verified.**
>
> **Trigger:** After a verification test passes for the first time (or after any fix is applied).
>
> **Why:** Transient issues, timing problems, and flaky behavior are only caught with multiple passes.

### Configuration

In `project.json` → `agents.verification`:

```json
{
  "agents": {
    "verification": {
      "requiredPasses": 3,
      "runBroaderTestsAfterFix": true
    }
  }
}
```

### Stability Verification Flow

```
Verification test PASSES
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ INCREMENT PASS COUNTER                                               │
│                                                                     │
│ State: { passCount: 1, requiredPasses: 3 }                           │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ CHECK: passCount >= requiredPasses?                                  │
│                                                                     │
│ ├─── NO ──► Run test again, increment counter, loop                 │
│ │                                                                   │
│ └─── YES ──► ✅ VERIFIED — declare feature stable                   │
└─────────────────────────────────────────────────────────────────────┘
```

### Pass Counter Reset Rules

| Event | Pass Counter Action |
|-------|---------------------|
| Test passes | Increment by 1 |
| Test fails | Reset to 0, enter fix loop |
| Fix applied by @developer | Reset to 0 (require fresh 3 passes) |
| Environment recovery completed | Reset to 0 (require fresh 3 passes) |
| Manual intervention | Reset to 0 (require fresh 3 passes) |

### State Tracking

Track stability verification state in `chunk.json` → `verification.loop`:

```json
{
  "verification": {
    "loop": {
      "stabilityCheck": {
        "testPath": "tests/ui-verify/profile-dropdown.spec.ts",
        "feature": "Add Settings option to profile dropdown",
        "requiredPasses": 3,
        "currentPasses": 2,
        "lastPassAt": "2026-03-03T10:45:00Z",
        "resetReason": null
      }
    }
  }
}
```

### Stability Progress Display

```
═══════════════════════════════════════════════════════════════════════
              🔄 STABILITY VERIFICATION IN PROGRESS
═══════════════════════════════════════════════════════════════════════

Feature: Add "Settings" option to profile dropdown
Test: tests/ui-verify/profile-dropdown.spec.ts

Stability check: 2/3 passes ██████████████░░░░░░░ 67%

Pass 1: ✅ 10:42:15 (2.3s)
Pass 2: ✅ 10:42:18 (2.1s)
Pass 3: ⏳ Running...
═══════════════════════════════════════════════════════════════════════
```

### Stability Failure (Mid-Stability Fail)

```
═══════════════════════════════════════════════════════════════════════
              ❌ STABILITY CHECK FAILED
═══════════════════════════════════════════════════════════════════════

Feature: Add "Settings" option to profile dropdown
Test: tests/ui-verify/profile-dropdown.spec.ts

Progress: 2/3 passes, then FAILED on pass 3

Error: Timeout waiting for '[data-testid="settings-option"]'

This indicates a flaky test or intermittent issue.
Pass counter reset to 0. Entering fix loop...

───────────────────────────────────────────────────────────────────────
Analyzing failure pattern...
Classification: FEATURE (element timeout in feature assertion section)
═══════════════════════════════════════════════════════════════════════
```

### After Fix — Fresh Passes Required

```
═══════════════════════════════════════════════════════════════════════
              🔄 FIX APPLIED — RESTARTING STABILITY CHECK
═══════════════════════════════════════════════════════════════════════

Fix: Updated selector timing in ProfileDropdown component
Applied by: @developer

Stability check reset: 0/3 passes (fresh verification required)
Running pass 1...
═══════════════════════════════════════════════════════════════════════
```

### Stability Verified

```
═══════════════════════════════════════════════════════════════════════
              ✅ FEATURE VERIFIED (STABLE)
═══════════════════════════════════════════════════════════════════════

Feature: Add "Settings" option to profile dropdown
Test: tests/ui-verify/profile-dropdown.spec.ts

Stability check: 3/3 passes ████████████████████ 100%

Pass 1: ✅ 10:42:15 (2.3s)
Pass 2: ✅ 10:42:18 (2.1s)
Pass 3: ✅ 10:42:21 (2.2s)

Feature is stable and verified.
═══════════════════════════════════════════════════════════════════════
```

---

## Automated Fix Loop

> 🔄 **When verification tests fail, automatically classify and fix the issue.**
>
> **Trigger:** Verification test fails (during initial run or stability check).

### Configuration

```json
{
  "agents": {
    "verification": {
      "autoFixLoop": true,
      "fixAttemptTimeoutMinutes": 5,
      "runBroaderTestsAfterFix": true
    }
  }
}
```

### Fix Loop Algorithm

```
Verification test FAILS
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 1: CLASSIFY FAILURE                                             │
│                                                                     │
│ Use failure classification (load test-prerequisite-detection)       │
│                                                                     │
│ Result: PREREQUISITE | FEATURE | ENVIRONMENT | TEST_INVALID         │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 2: CHECK STOP CONDITIONS                                        │
│                                                                     │
│ STOP if ANY of these are true:                                       │
│ • Component has 3 failed fix attempts                               │
│ • Same exact error occurred twice in a row (no progress)            │
│ • Total loop iterations > 10 (runaway prevention)                   │
│                                                                     │
│ ├─── STOP TRIGGERED ──► Log failure, offer manual options           │
│ │                                                                   │
│ └─── CONTINUE ──► Proceed to fix                                    │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 3: FIND EXISTING TEST (for prerequisites)                       │
│                                                                     │
│ Search for existing test matching the failed component:              │
│ 1. Check tests/e2e/ for files matching component name               │
│ 2. Check test manifests/indexes if they exist                       │
│ 3. If no dedicated test exists, use error context to guide fix      │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 4: DELEGATE FIX                                                 │
│                                                                     │
│ Based on classification:                                             │
│ • PREREQUISITE (code issue) ──► @developer                          │
│ • FEATURE (code issue) ──► @developer                               │
│ • ENVIRONMENT ──► Load skill-based recovery                         │
│ • TEST_INVALID ──► @ui-tester-playwright for test fix                     │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 5: VERIFY FIX                                                   │
│                                                                     │
│ After fix is applied:                                                │
│ 1. Re-run the component's test (if separate from verification test) │
│ 2. If pass → Retry original verification test                       │
│ 3. If fail → Record attempt, check stop conditions, loop            │
│                                                                     │
│ On verification test pass → Enter 3-pass stability check            │
└─────────────────────────────────────────────────────────────────────┘
```

### State Tracking

State is tracked in `chunk.json` → `verification.loop`:

```json
{
  "verification": {
    "loop": {
      "originalFeature": "tests/ui-verify/profile-dropdown-settings.spec.ts",
      "startedAt": "2026-03-03T10:30:00Z",
      "totalIterations": 3,
      "lastError": null,
      "lastErrorCount": 0,
      "components": {
        "auth-login": {
          "type": "prerequisite",
          "testFile": "tests/e2e/auth.spec.ts",
          "attempts": [
            {
              "attemptNumber": 1,
              "error": "Timeout waiting for '[data-testid=\"login-submit\"]'",
              "fixAgent": "@developer",
              "fixDescription": "Fixed missing data-testid on login button",
              "result": "pass",
              "duration": "45s"
            }
          ],
          "status": "fixed"
        }
      }
    }
  }
}
```

### Stop Conditions

| Condition | Description | Action |
|-----------|-------------|--------|
| **3 attempts per component** | Component has failed 3 fix attempts | Stop fixing this component |
| **Same error twice** | Exact same error message twice in a row | Stop (no progress being made) |
| **10 total iterations** | Runaway prevention (entire loop) | Stop entire verification |

### Fix Delegation Format

When delegating to @developer:

```
Fix verification failure: [component name]

Classification: [PREREQUISITE | FEATURE]
Test file: [test file path]
Attempt: [N]/3

Error:
[error message]

Stack trace:
[relevant stack trace]

Previous attempts:
- Attempt 1: [fix description] → [result]
- Attempt 2: [fix description] → [result]

Context:
This is [a prerequisite / the feature under test].
[Additional context about what the test is trying to do]
```

### Fix Loop Progress Display

```
═══════════════════════════════════════════════════════════════════════
              🔧 AUTOMATED FIX LOOP IN PROGRESS
═══════════════════════════════════════════════════════════════════════

Feature: Add "Settings" option to profile dropdown
Status: Fixing prerequisite failure

Component: auth-login (PREREQUISITE)
Attempt: 2/3
Agent: @developer

Error: Timeout waiting for '[data-testid="login-submit"]'

Previous attempt:
  Fix: Added explicit wait for login form
  Result: ❌ Still failing

Current fix in progress...
═══════════════════════════════════════════════════════════════════════
```

### Fix Loop Algorithm (Pseudocode)

```
MAX_ATTEMPTS = 3
attempt = 1
lastFailure = null

while attempt <= MAX_ATTEMPTS:
    Run all verification steps
    
    if ALL pass:
        Continue to next phase
    
    if any step fails:
        currentFailure = identify what failed
        
        if currentFailure == lastFailure:
            # Same failure twice in a row — not making progress
            STOP and report to user
        
        lastFailure = currentFailure
        
        Report: "Attempt {attempt}/{MAX_ATTEMPTS}: {failure description}"
        Report: "Running @developer to fix..."
        
        Run @developer with context block:
            <context>
            version: 1
            project:
              path: {project path}
              stack: {stack}
              commands:
                test: {test command}
            conventions:
              summary: |
                {conventions summary}
              fullPath: {path}/docs/CONVENTIONS.md
            currentWork:
              mode: fix-loop
              attempt: {attempt}
              failure: {what failed}
            </context>
            
            Fix these failures:
            - What failed: {test names, lint errors, type errors}
            - Error messages: {stack traces}
            - Files involved: {file list}
        
        attempt += 1

# If loop exhausts without success:
STOP and report to user
```

### Fix Loop Success

```
═══════════════════════════════════════════════════════════════════════
              ✅ FIX LOOP COMPLETE
═══════════════════════════════════════════════════════════════════════

Feature: Add "Settings" option to profile dropdown
Duration: 3m 45s
Iterations: 4

Components fixed:
  ✅ auth-login (prerequisite) — 1 attempt
  ✅ profile-dropdown-settings (feature) — 2 attempts

Entering stability verification (3 passes required)...
═══════════════════════════════════════════════════════════════════════
```

### Fix Loop Stopped

```
═══════════════════════════════════════════════════════════════════════
              ❌ FIX LOOP STOPPED
═══════════════════════════════════════════════════════════════════════

Feature: Add "Settings" option to profile dropdown
Stop reason: Component reached 3 failed attempts

Component: auth-login (PREREQUISITE)
Attempts: 3/3 (max reached)

Last error:
  Timeout waiting for '[data-testid="login-submit"]'

Attempts log:
  1. Fixed missing data-testid → Still failing
  2. Added explicit wait → Still failing
  3. Updated selector to use role → Still failing

This failure has been logged to verification-failures.json.

Options:
  [M] Fix manually, then type "retry"
  [S] Skip verification (marks feature as unverified)
  [A] Abandon feature (reverts story changes)
═══════════════════════════════════════════════════════════════════════
```
