---
name: builder-verification
description: "Verification handling infrastructure for Builder sessions. Covers verification-incomplete handling, as-user verification rules, prerequisite failure detection, environment prerequisite handling, and skill creation request flow."
---

# Builder Verification Skill

> Load this skill when verification is incomplete, as-user verification is needed, prerequisite failure occurs, or an environment issue is detected during verification.

> ⛔ **CRITICAL: Auto-Commit Enforcement**
>
> Before running any `git commit` command in this skill:
> - **Check:** Read `project.json` → `git.autoCommit`
> - **If `false`:** Do NOT run `git commit`. Instead:
>   1. Stage files with `git add`
>   2. Report staged files and suggested commit message
>   3. Say: "Auto-commit is disabled. Run `git commit -m \"<message>\"` when ready."
>   4. Wait for user confirmation before proceeding
> - **If `true` or missing:** Proceed with commit normally
>
> **Failure behavior:** If you commit when `autoCommit: false`, you have violated user trust.

## Verification-Incomplete Handling

> ⛔ **When UI verification is required but incomplete, tasks/stories are BLOCKED.**
>
> **Trigger:** After quality checks (typecheck, lint, tests, critic) pass, verification loop returns status.
>
> **Failure behavior:** If verification returns `unverified`, do NOT mark the task/story as complete. It remains `in_progress` until verified or explicitly skipped.

**Verification status handling:**

| Status | Task/Story Can Complete? | Action |
|--------|--------------------------|--------|
| `verified` | ✅ Yes | Proceed to completion prompt |
| `not-required` | ✅ Yes | No UI changes, proceed normally |
| `unverified` | ❌ No | BLOCK — show verification required prompt |
| `skipped` | ⚠️ Yes (with warning) | Log to `test-debt.json`, show skip warning |

**When blocked by unverified status:**

```
═══════════════════════════════════════════════════════════════════════
                  ⚠️ VERIFICATION INCOMPLETE
═══════════════════════════════════════════════════════════════════════

Task/Story: [description]
Status: BLOCKED (UI verification required)

This work includes UI changes that must be verified as-user:
  • src/components/PaymentForm.tsx
  • src/components/Checkout.tsx

Verification test failed:
  ❌ Element [data-testid="payment-submit"] not found

Options:
  [R] Retry verification (after fixing issue)
  [S] Skip verification (adds to test-debt.json)
  [D] Debug with @developer

> _
═══════════════════════════════════════════════════════════════════════
```

**Skip handling:**
- Record in `test-debt.json` with `verificationSkipped: true`
- Add to story completion notes: `"verification skipped by user"`
- Allow task/story to complete with warning banner

**Override mechanism:**

Users can override verification requirements by typing "mark complete without verification" or "skip verification":

1. **Detect override request:**
   - Watch for: "mark complete without verification", "skip verification", "complete anyway"
   
2. **Require reason:**
   ```
   ⚠️ OVERRIDE REQUESTED
   
   This bypasses mandatory verification for UI changes.
   Reason required: _
   ```

3. **Log override with reason:**
   - Record in `test-debt.json`:
     ```json
     {
       "overrides": [{
         "file": "src/components/NewFeature.tsx",
         "reason": "Component behind disabled feature flag",
         "overrideAt": "2026-03-03T10:30:00Z",
         "story": "US-003"
       }]
     }
     ```
   - Add to story completion notes: `"verification overridden: [reason]"`

4. **Show confirmation with recommendation:**
   ```
   ⚠️ Story US-003 completing WITHOUT verification.
   
   Reason: Component behind disabled feature flag
   Files: src/components/NewFeature.tsx
   
   Recommendation: Verify manually when feature flag is enabled.
   ```

**State updates when blocked:**
- Task/story remains `in_progress` (NOT completed)
- `chunk.json` → `verification.status: "unverified"`
- User must resolve before committing

See `test-ui-verification` skill for full verification flow.

## Never Use curl/wget for As-User Verification

> ⛔ **CRITICAL: Never use `curl`, `wget`, or HTTP client libraries to verify as-user behavior.**
>
> **Trigger:** Verifying any change that affects browser/UI behavior (CORS, cookies, headers, API responses consumed by browsers).
>
> **Failure behavior:** Using curl for as-user verification produces false positives. CORS, CSP, cookie policies, and many security features are enforced by browsers ONLY — curl bypasses all of them.

| Tool | What It Tests | What It Misses |
|------|---------------|----------------|
| `curl` | Server responds with 200 | CORS blocks, cookie policies, CSP, browser fetch behavior |
| `wget` | File downloads successfully | Same as curl |
| HTTP libraries | API returns correct data | Same as curl |
| **Playwright** | Full browser/app behavior | Nothing — this is the correct tool |

**Especially for CORS:** A `curl -I` request will succeed even when browsers are blocked. CORS is enforced by browsers, not servers. The server sends headers, but only browsers actually block requests when headers are missing or wrong.

**Always delegate as-user verification to Playwright via the `test-ui-verification` skill.**

### What Requires As-User Verification

| Change Type | Why Playwright Required |
|-------------|---------------------|
| CORS configuration | Browsers enforce CORS, curl doesn't |
| Cookie settings (SameSite, Secure, HttpOnly) | Browsers enforce cookie policies |
| CSP headers | Browsers enforce Content-Security-Policy |
| Authentication flows | Redirects, cookies, session handling |
| API responses consumed by UI | Browser fetch behavior differs from curl |
| Any `**/cors*`, `**/headers*`, `**/security*` file | Security features are browser-enforced |

## Prerequisite Failure Detection

> 🎯 **When verification fails, classify the failure as PREREQUISITE vs FEATURE.**
>
> **Trigger:** Verification test fails — analyze WHERE it failed.
>
> **Why:** A login failure blocking a menu test is a different problem than a missing menu item. The fix strategy differs.

**Failure classification:**

| Classification | Meaning | Fix Strategy |
|----------------|---------|--------------|
| `PREREQUISITE` | Test failed before reaching the feature | Fix the prerequisite first |
| `FEATURE` | Test failed on the feature assertion | Fix the feature |
| `TEST_INVALID` | Test file has syntax/import error | @ui-tester-playwright fixes test |
| `ENVIRONMENT` | Infrastructure issue (see below) | Skill-based recovery |

**Detection method:**

1. Parse test file for `@prerequisites` and `@feature-assertions` markers
2. Analyze failure location against markers
3. If markers missing, use heuristic detection (see `test-prerequisite-detection` skill)

**Prerequisite failure handling:**

```
Verification test fails
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ CLASSIFY FAILURE                                                     │
│                                                                     │
│ ├─── PREREQUISITE ──► Find existing test, confirm issue, fix       │
│ │                                                                   │
│ ├─── FEATURE ──► Normal fix loop with @developer                   │
│ │                                                                   │
│ ├─── TEST_INVALID ──► @ui-tester-playwright fixes test file              │
│ │                                                                   │
│ └─── ENVIRONMENT ──► Skill-based recovery (see below)              │
└─────────────────────────────────────────────────────────────────────┘
```

**When prerequisite failure detected:**

1. Search for existing test covering the prerequisite (e.g., `tests/e2e/auth.spec.ts`)
2. Run that test to confirm the issue
3. If confirmed, delegate fix to @developer
4. After fix, re-run prerequisite test
5. If prerequisite passes, retry original feature verification

See `test-prerequisite-detection` skill for full algorithm.

## Environment Prerequisite Handling

> 🔧 **Environment failures require skill-based recovery, not code changes.**
>
> **Trigger:** Failure matches environment patterns (port conflict, process conflict, etc.)
>
> **Why:** These issues can't be fixed by @developer — they need infrastructure recovery.

**Environment categories:**

| Category | Example Errors | Recovery |
|----------|----------------|----------|
| Process conflict | `EADDRINUSE`, `already running` | Kill process, restart |
| Port conflict | `ECONNREFUSED`, `port in use` | Check/start dev server |
| Native app | `Electron launch failed` | Load platform-specific skill |
| External service | `503 Service Unavailable` | Wait or use mock |

**When environment failure detected:**

1. **Categorize the issue** using error patterns
2. **Search for matching skill:**
   - `electron-testing` for Electron issues
   - `start-dev-server` for port/server issues
   - `docker-testing` for container issues
3. **If skill found:** Load skill, run recovery, retry test
4. **If no skill:** Offer skill creation request (see below)

**Environment failure prompt:**

```
═══════════════════════════════════════════════════════════════════════
              🔧 ENVIRONMENT ISSUE DETECTED
═══════════════════════════════════════════════════════════════════════

Feature under test: Add "Settings" option to profile dropdown
Status: BLOCKED (environment issue)

Issue detected:
  ❌ Electron: "Error: another instance is already running"
  Category: Process conflict

Matching skill found: electron-testing
Loading skill and attempting recovery...
═══════════════════════════════════════════════════════════════════════
```

See `test-prerequisite-detection` skill for full detection patterns.

## Skill Creation Request Flow

> 📝 **When no skill exists for an environment issue, queue a creation request for @toolkit.**
>
> **Trigger:** Environment failure detected but no matching skill found.
>
> **Why:** @toolkit creates skills — Builder just queues the request with context.

**When no skill exists:**

```
═══════════════════════════════════════════════════════════════════════
              ❌ NO MATCHING SKILL FOUND
═══════════════════════════════════════════════════════════════════════

Environment issue requires a skill that doesn't exist yet.

Detected pattern: "Electron single-instance conflict"
Suggested skill: electron-testing

Options:
  [T] Queue skill creation for @toolkit (creates pending-update)
  [M] Fix manually, then type "retry"
  [S] Skip verification
═══════════════════════════════════════════════════════════════════════
```

**When user selects [T]:**

1. **Create pending-update file:**
   ```
   ~/.config/opencode/pending-updates/YYYY-MM-DD-new-skill-{name}.md
   ```

2. **Request file format:**
   ```markdown
   ---
   requestedBy: builder
   date: YYYY-MM-DD
   priority: high
   type: new-skill
   ---
   
   # New Skill Request: {skill-name}
   
   ## Detected Pattern
   
   Environment prerequisite failure during verification test.
   
   **Error:** "{error message}"
   **Context:** {what Builder was trying to do}
   **Project:** {project name}
   
   ## Suggested Skill
   
   **Name:** {skill-name}
   **Purpose:** {brief description}
   
   **Recovery steps needed:**
   1. {step 1}
   2. {step 2}
   3. {step 3}
   
   ## Screenshots
   
   - ai-tmp/verification/screenshots/{screenshot}.png
   
   ## Source Test
   
   - {test file path}
   - Failed at: {failure point}
   ```

3. **Track pending request in `chunk.json` → `verification.loop`:**
   ```json
   {
     "verification": {
       "loop": {
         "pendingSkillRequest": {
           "skillName": "electron-testing",
           "requestedAt": "2026-03-03T10:45:00Z",
           "requestFile": "~/.config/opencode/pending-updates/2026-03-03-new-skill-electron-testing.md"
         }
       }
     }
   }
   ```

4. **Tell user:**
   ```
   ✅ Skill creation request queued.
   
   File: ~/.config/opencode/pending-updates/2026-03-03-new-skill-electron-testing.md
   
   Next steps:
   1. Switch to @toolkit to create the skill
   2. Come back here and type "retry" to use the new skill
   
   Options:
     [M] Fix manually now
     [S] Skip verification
   ```

**On retry — skill hot-reload:**

When user types "retry" after requesting a skill:

1. Check if the requested skill now exists:
   ```bash
   ls ~/.config/opencode/skills/{skill-name}/SKILL.md 2>/dev/null
   ```

2. **If skill exists:**
   - Load the skill via skill tool
   - Execute recovery steps
   - Retry the original verification test
   - Clear `pendingSkillRequest` from state

3. **If skill doesn't exist:**
   - Show same options again
   - Remind user: "Skill not yet created. Switch to @toolkit to create it."
