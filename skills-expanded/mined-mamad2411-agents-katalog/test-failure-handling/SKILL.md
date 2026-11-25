---
name: test-failure-handling
description: "Failure logging, manual fallback options, and verification-failures.json management. Use when handling test failures, logging failures, or managing manual fallback options. Triggers on: test failure, failure logging, manual fix, skip verification, verification-failures.json."
---

# Test Failure Handling

> Load this skill when: logging verification failures, handling manual fallback options, or managing verification-failures.json.

## Failure Logging (verification-failures.json)

> 📝 **Log all verification failures for debugging and pattern analysis.**
>
> **Trigger:** Fix loop stopped (any stop condition), or manual skip/abandon.

### File Location

```
<project>/ai-tmp/verification-failures.json
```

### Structure

```json
{
  "schemaVersion": 1,
  "failures": [
    {
      "id": "2026-03-03T10:30:00Z-profile-dropdown-settings",
      "feature": "Add Settings option to profile dropdown",
      "testFile": "tests/ui-verify/profile-dropdown-settings.spec.ts",
      "prd": "print-templates",
      "story": "US-005",
      "startedAt": "2026-03-03T10:30:00Z",
      "stoppedAt": "2026-03-03T10:45:00Z",
      "stopReason": "max_attempts_reached",
      "totalIterations": 4,
      "failedComponent": {
        "name": "auth-login",
        "type": "prerequisite",
        "testFile": "tests/e2e/auth.spec.ts"
      },
      "attempts": [
        {
          "attemptNumber": 1,
          "error": "Timeout waiting for '[data-testid=\"login-submit\"]'",
          "fixAgent": "@developer",
          "fixDescription": "Fixed missing data-testid on login button",
          "result": "fail",
          "duration": "45s",
          "screenshot": "ai-tmp/verification/screenshots/auth-attempt-1.png"
        },
        {
          "attemptNumber": 2,
          "error": "Timeout waiting for '[data-testid=\"login-submit\"]'",
          "fixAgent": "@developer",
          "fixDescription": "Added explicit wait for login form",
          "result": "fail",
          "duration": "60s",
          "screenshot": "ai-tmp/verification/screenshots/auth-attempt-2.png"
        },
        {
          "attemptNumber": 3,
          "error": "Timeout waiting for '[data-testid=\"login-submit\"]'",
          "fixAgent": "@developer",
          "fixDescription": "Updated selector to use role",
          "result": "fail",
          "duration": "55s",
          "screenshot": "ai-tmp/verification/screenshots/auth-attempt-3.png"
        }
      ],
      "resolution": "manual",
      "resolutionDetails": "User chose [M] to fix manually"
    }
  ],
  "stats": {
    "totalFailures": 5,
    "autoFixed": 3,
    "manuallyFixed": 1,
    "skipped": 1,
    "abandoned": 0,
    "autoFixRate": 0.6,
    "lastUpdated": "2026-03-03T10:45:00Z"
  }
}
```

### Stop Reason Values

| Value | Description |
|-------|-------------|
| `max_attempts_reached` | Component had 3 failed fix attempts |
| `same_error_twice` | Exact same error occurred twice in a row |
| `max_iterations` | Total loop iterations exceeded 10 |
| `environment_no_skill` | Environment issue with no matching skill |
| `external_service_unavailable` | External service failure (503, 429) |
| `user_skip` | User selected [S] Skip |
| `user_abandon` | User selected [A] Abandon |

### Resolution Values

| Value | Description |
|-------|-------------|
| `auto_fixed` | Automated fix loop successfully resolved |
| `manual` | User fixed manually and retried |
| `skipped` | User skipped verification |
| `abandoned` | User abandoned the feature |
| `pending` | Not yet resolved |

### Writing to Failure Log

When a failure occurs:

1. Read existing `ai-tmp/verification-failures.json` (or create if missing)
2. Append new failure entry to `failures` array
3. Update `stats` counters
4. Write file atomically

```bash
mkdir -p ai-tmp
```

---

## Manual Fallback Options

> 🛑 **When automated fix fails, provide clear manual options.**
>
> **Trigger:** Fix loop stopped (any stop condition).

### Option: [M] Fix Manually

When user selects [M]:

1. **Display full context:**
   ```
   MANUAL FIX MODE
   
   Feature: Add "Settings" option to profile dropdown
   Blocked by: auth-login (prerequisite)
   
   Last error:
     Timeout waiting for '[data-testid="login-submit"]'
   
   Relevant files:
     - src/components/LoginForm.tsx
     - tests/e2e/auth.spec.ts
   
   Screenshots:
     - ai-tmp/verification/screenshots/auth-attempt-3.png
   
   Type "retry" when you've fixed the issue.
   Type "skip" to skip verification.
   Type "abandon" to abandon this feature.
   ```

2. **Wait for user input**

3. **On "retry":**
   - Reset fix loop state (clear component attempts)
   - Restart verification from the beginning
   - Enter 3-pass stability check on success

4. **Update failure log:** `"resolution": "manual"`

### Option: [S] Skip Verification

When user selects [S]:

1. **Require skip reason:**
   ```
   Skip reason (required):
   > _
   ```

2. **Log the skip:**
   ```json
   {
     "resolution": "skipped",
     "resolutionDetails": "User skip: [reason provided]"
   }
   ```

3. **Mark feature as unverified:**
   - PRD story continues but is flagged
   - Adds entry to `test-debt.json`

4. **Display warning:**
   ```
   ⚠️ FEATURE MARKED UNVERIFIED
   
   Feature: Add "Settings" option to profile dropdown
   Skip reason: [user's reason]
   
   This is logged in test-debt.json for follow-up.
   Continuing to next story...
   ```

### Option: [A] Abandon

When user selects [A]:

1. **Confirm abandonment:**
   ```
   ⚠️ ABANDON FEATURE?
   
   This will revert all changes made for this story.
    The chunk will be marked as "abandoned" in session.json.
    
    Type "confirm" to proceed or "cancel" to go back.
    > _
    ```

2. **On confirm:**
   - Revert story changes (git checkout)
   - Update chunk status to `abandoned` in `session.json`
   - Log to verification-failures.json: `"resolution": "abandoned"`

3. **Display result:**
   ```
   ❌ FEATURE ABANDONED
   
   Story: US-005 - Add "Settings" option to profile dropdown
   Changes have been reverted.
   
   Moving to next story...
   ```

---

## Story Blocking (PRD Mode)

```
❌ STORY BLOCKED: Unit tests failing after 3 fix attempts

Story: US-003 - Add print preview modal

Failing tests:
  • PrintPreview.test.tsx: Expected modal to be visible
  • usePreview.test.ts: Hook returned undefined

Options:
  1. Review and fix manually, then type "retry"
  2. Type "skip unit-test" to bypass (adds to test-debt.json)
  3. Abort PRD

> _
```

When a user skips a test, record it in `test-debt.json` so future changes to that file get escalated testing (hotspot behavior).

---

## External Service Handling

External service failures (503, 429) **cannot be automatically fixed**:

```
═══════════════════════════════════════════════════════════════════════
              ⚠️ EXTERNAL SERVICE UNAVAILABLE
═══════════════════════════════════════════════════════════════════════

The test failed due to an external service issue:
  Service: api.stripe.com
  Error: 503 Service Unavailable

This cannot be automatically fixed. Options:
  [W] Wait and retry in 5 minutes
  [M] Use mock/stub for this service (creates fixture)
  [S] Skip verification
═══════════════════════════════════════════════════════════════════════
```

---

## Environment Failure Report

```
═══════════════════════════════════════════════════════════════════════
              🔧 ENVIRONMENT PREREQUISITE DETECTED
═══════════════════════════════════════════════════════════════════════

Feature under test: Add "Settings" option to profile dropdown
Status: BLOCKED (environment issue)

Environment issue:
  ❌ Electron: "Error: another instance is already running"
  
  Category: Process conflict
  This is an infrastructure issue, not a code problem.

Matching skill found: ui-test-electron
Action: Loading skill and attempting recovery...
═══════════════════════════════════════════════════════════════════════
```
