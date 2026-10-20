---
name: test-flow
description: "Unified test flow — skip gate, activity resolution, quality check pipeline, completion prompt, and Tier 2 skill loading. The single canonical entry point for all story/task completion quality checks. Use when a story or task completes. Triggers on: story complete, task complete, quality checks, run tests, verification pipeline."
---

# Test Flow — Unified Quality Check Pipeline

> **Single entry point.** Builder calls test-flow unconditionally after every story/task completion.
> test-flow owns the full decision tree: skip gate, activity resolution, quality checks, fix loop, and completion prompt.
>
> Both ad-hoc mode and PRD mode reference this skill — neither defines inline quality checks.

---

## Section 1: Skip Gate

> **First step.** Before running any quality checks, determine if the pipeline can be skipped entirely.
> Builder calls test-flow unconditionally; test-flow decides whether to actually run.

The verification pipeline can be skipped when **ALL** changed files match one of:

| Skip Criterion | File Patterns |
|----------------|---------------|
| Docs-only changes | `*.md` files only |
| Config-only changes | `project.json`, `*.config.*`, `.env*` |
| Test-only changes | `*.test.ts`, `*.spec.ts`, `__tests__/**` |
| CI/build config changes | `.github/**`, `Dockerfile`, `docker-compose*` |
| Lockfile-only changes | `pnpm-lock.yaml`, `package-lock.json`, `yarn.lock` |
| User explicit skip | User says "skip verification" |

**Skip gate algorithm:**

```
function shouldSkip(changedFiles, userRequest):
  if userRequest contains "skip verification":
    return { skip: true, reason: "user-explicit" }

  skipPatterns = [
    "*.md",
    "project.json", "*.config.*", ".env*",
    "*.test.ts", "*.spec.ts", "__tests__/**",
    ".github/**", "Dockerfile", "docker-compose*",
    "pnpm-lock.yaml", "package-lock.json", "yarn.lock"
  ]

  for file in changedFiles:
    if not anyMatch(file, skipPatterns):
      return { skip: false }

  return { skip: true, reason: "all-files-match-skip-patterns" }
```

**When skipped:**
- Log: `Skip gate: pipeline skipped — [reason]`
- Proceed directly to Completion Prompt (Section 5)
- Do NOT run typecheck, lint, tests, critics, or Playwright

**When NOT skipped:**
- Proceed to Section 2: Activity Resolution

---

## Section 2: Activity Resolution

> Determines which tests, critics, and verification steps to run based on what changed.
> No prompts, no user selection — fully automatic.

### How It Works

```
Task complete
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 1: Collect Changed Files                                       │
│                                                                     │
│ • git diff --name-only HEAD~1 (or vs base branch)                  │
│ • Include staged + unstaged changes                                 │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 2: Resolve Activities                                          │
│                                                                     │
│ Read: ~/.config/opencode/data/test-activity-rules.json             │
│ Read: <project>/docs/test-debt.json (hotspots)                     │
│                                                                     │
│ For each changed file:                                              │
│   • Match against filePatterns → collect activities                 │
│                                                                     │
│ For diff content:                                                   │
│   • Match against codePatterns → collect additional activities      │
│                                                                     │
│ Check cross-cutting rules:                                          │
│   • Multiple directories touched? → add oddball-critic              │
│   • Shared module touched? → add dx-critic                          │
│                                                                     │
│ Check hotspots:                                                     │
│   • File in test-debt.json? → add its critics, force E2E           │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 3: Display Activities (Informational Only)                     │
│                                                                     │
│ Show what's running — NO confirmation prompt                        │
│ Execution proceeds immediately after display                        │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 4: Execute Activities                                          │
│                                                                     │
│ 1. Baseline: typecheck, lint (always)                               │
│ 2. Unit tests: resolved testers for file types                      │
│ 3. Critics: resolved critics in parallel                            │
│ 4. E2E / Playwright: always included (see Section 3)                │
│ 5. Quality: aesthetic-critic, tailwind-critic if resolved           │
└─────────────────────────────────────────────────────────────────────┘
```

### Activity Resolution Algorithm

**Pre-resolution step:** Read `project.json` → `context.testing` if present. This file contains project-specific testing conventions that may affect test execution (e.g., app kill patterns before test runs, specific test target configuration, base test class requirements). Pass this context to any test-writing agents during activity execution.

```
function resolveActivities(changedFiles, diffContent, project):
  # Load rules
  rules = read("~/.config/opencode/data/test-activity-rules.json")
  hotspots = read("<project>/docs/test-debt.json") or { hotspots: {} }

  activities = {
    baseline: ["typecheck", "lint"],
    unit: Set(),
    critics: Set(),
    quality: Set(),
    reasoning: []
  }

  for file in changedFiles:
    for pattern, rule in rules.filePatterns:
      if globMatch(file, pattern):
        # Collect critics
        activities.critics.addAll(rule.critics or [])
        activities.reasoning.push(file + " → " + (rule.reason or pattern))

        # Determine unit tester
        if rule.unit === true:
          activities.unit.add(inferUnitTester(file))
        else if rule.unit is string:
          activities.unit.add(rule.unit)

        # Quality critics
        if rule.quality === true:
          activities.quality.addAll(["aesthetic-critic"])
        else if rule.quality is array:
          activities.quality.addAll(rule.quality)

  # Match code patterns in diff
  for pattern, rule in rules.codePatterns:
    if regexMatch(diffContent, pattern):
      activities.critics.addAll(rule.critics or [])
      activities.reasoning.push("Code pattern: " + pattern)

  # Cross-cutting rules
  directories = countDistinctDirectories(changedFiles)
  if directories >= rules.crossCuttingRules.multipleDirectories.threshold:
    activities.critics.addAll(rules.crossCuttingRules.multipleDirectories.add.critics)

  sharedPaths = rules.crossCuttingRules.sharedModuleTouch.paths
  if anyMatch(changedFiles, sharedPaths):
    activities.critics.addAll(rules.crossCuttingRules.sharedModuleTouch.add.critics)

  # Hotspot escalation
  for file in changedFiles:
    if file in hotspots.hotspots:
      h = hotspots.hotspots[file]
      activities.critics.addAll(h.addedCritics or [])
      activities.reasoning.push(file + " → hotspot: " + h.reason)

  return activities

function inferUnitTester(file):
  if file.endsWith(".tsx") or file.endsWith(".jsx"):
    return "react-tester"
  if file.endsWith(".go"):
    return "go-tester"
  return "jest-tester"
```

### Skip Playwright for These File Types

These file types never trigger Playwright:

- `*.d.ts` — Type definitions
- `*.test.ts`, `*.spec.ts`, `__tests__/**` — Test files
- `*.md`, `README*`, `docs/**` — Documentation
- `.eslintrc*`, `.prettierrc*`, `tsconfig*.json` — Dev config
- `.gitignore`, `.github/**` — Git/CI config
- `*.lock`, `package-lock.json` — Lockfiles

### Informational Activity Display

After resolution, display what's running — **no confirmation, execution proceeds immediately:**

```
═══════════════════════════════════════════════════════════════════════
                      TEST ACTIVITIES FOR THIS CHANGE
═══════════════════════════════════════════════════════════════════════

Changed files:
  • src/components/PaymentForm.tsx
  • src/api/payments/charge.ts

Running:
  ✓ Baseline: typecheck, lint
  ✓ Unit tests: @react-tester, @jest-tester
  ✓ Critics: @frontend-critic, @backend-critic-ts, @security-critic
  ✓ E2E: IMMEDIATE (payment code detected)
  ✓ Quality: @aesthetic-critic

═══════════════════════════════════════════════════════════════════════
```

**Note:** This display is informational. User is NOT asked to confirm or modify.

### Test Execution Mode (CRITICAL)

> ⚠️ **ALWAYS run tests in CI/non-watch mode to prevent orphaned processes.**

| Runner | Watch Mode (DO NOT USE) | CI Mode (USE THIS) |
|--------|------------------------|-------------------|
| **Vitest** | `vitest` (default) | `vitest run` |
| **Jest** | `jest --watch` | `jest` (default) |
| **Playwright** | N/A | Default is single-run |
| **Go test** | N/A | Default is single-run |

**Enforcement:**

1. **Check if project uses Vitest** — look for `vitest` in `package.json` dependencies
2. **If Vitest detected**, verify the test script includes `run`:
   - ✅ `"test": "vitest run"`
   - ❌ `"test": "vitest"` (will watch)
3. **If the script is wrong or uncertain**, run with explicit flags:
   ```bash
   CI=true npx vitest run
   ```
4. **CI environment variable** — set `CI=true` as a safety net:
   ```bash
   CI=true npm test
   ```

---

## Section 3: Quality Check Pipeline

> ⛔ **After EVERY task/story completes, run resolved activities automatically. No prompts, no skipping.**
>
> This applies to BOTH ad-hoc mode AND PRD mode.

### Activity Execution Order

After @developer completes a task, run resolved activities in this order:

| Step | Activity | Source | Fix Loop |
|------|----------|--------|----------|
| 1 | **Typecheck** | Always (baseline) | Yes, max 3 attempts |
| 2 | **Lint** | Always (baseline) | Yes, max 3 attempts |
| 3 | **Unit Tests** | Resolved testers | Yes, max 3 attempts |
| 3.5 | **Rebuild/Relaunch** | `electron-build-deploy` skill (if `buildDeploy` configured), `postChangeWorkflow` steps, or auto-inferred from `apps[]` | Yes, max 3 attempts |
| 4 | **Critics** | Resolved from patterns | Report findings, @developer fixes |
| 5 | **E2E / Playwright** | PRD: gated by `testVerifySettings` (default on). Ad-hoc: opt-in only (user request or explicit `testVerifySettings` opt-in) | Yes, configurable attempts (see Retry Strategy) |
| 6 | **Quality** | Resolved quality critics | Report findings |

### Pipeline Flow

```
Task/Story complete
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ RESOLVE ACTIVITIES (automatic, no prompt)                           │
│ Read test-activity-rules.json, match patterns, check hotspots       │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ DISPLAY ACTIVITIES (informational only, no confirmation)            │
│ Show what's running and why                                         │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────┐
│ 1. Typecheck        │
└─────────────────────┘
    │
    ├─── PASS ──► Continue
    └─── FAIL ──► Fix loop (max 3) ──► Still failing? STOP
    │
    ▼
┌─────────────────────┐
│ 2. Lint             │
└─────────────────────┘
    │
    ├─── PASS ──► Continue
    └─── FAIL ──► Fix loop (max 3) ──► Still failing? STOP
    │
    ▼
┌─────────────────────┐
│ 3. Unit tests       │
│ (resolved testers)  │
└─────────────────────┘
    │
    ├─── PASS ──► Continue
    └─── FAIL ──► Fix loop (max 3) ──► Still failing? STOP
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 3.5. Rebuild/Relaunch                                               │
│                                                                     │
│ If apps.desktop.buildDeploy exists in project.json:                 │
│                                                                     │
│   1. Read buildDeploy.triggerPaths (array of glob patterns)          │
│   2. Match changedFiles against triggerPaths:                        │
│                                                                     │
│      function shouldRebuild(changedFiles, triggerPaths):             │
│        for file in changedFiles:                                     │
│          for pattern in triggerPaths:                                 │
│            if globMatch(file, pattern):                               │
│              return { rebuild: true, trigger: file, pattern }        │
│        return { rebuild: false }                                     │
│                                                                     │
│   3a. If NO match → Skip build-deploy with message:                 │
│       "⏭️ Build-deploy skipped: no changed files match              │
│        triggerPaths (changed: [N] files, patterns: [M])"            │
│       → Proceed to Step 4 (critics)                                 │
│                                                                     │
│   3b. If ANY match → Load `electron-build-deploy` skill:            │
│       "🔨 Build-deploy triggered: {file} matched {pattern}"         │
│       → Skill handles: build → kill → copy → relaunch              │
│       → Do NOT proceed to Playwright until skill reports success    │
│       → On failure: treat as test-flow failure (fix loop, max 3)   │
│                                                                     │
│ Else if postChangeWorkflow exists → evaluate step conditions first, │
│   then execute matching non-Playwright steps                        │
│   (condition: "files-changed-in:..." checked against changedFiles)  │
│                                                                     │
│ Else check apps[] in project.json:                                   │
│   • No apps[] or web-only → Skip (HMR handles it)                  │
│   • Desktop + bundled/hybrid → Build + relaunch Electron            │
│   • Desktop + remote → Ensure Electron running (no rebuild)         │
│                                                                     │
│ CRITICAL: Desktop → always Playwright-Electron, never browser       │
│ CRITICAL: webContent "remote" → NEVER frontend build for UI changes │
└─────────────────────────────────────────────────────────────────────┘
    │
    ├─── PASS (or skipped) ──► Continue
    └─── FAIL ──► Fix loop (max 3) ──► Still failing? STOP
    │
    ▼
┌─────────────────────┐
│ 4. Critics          │
│ (resolved critics)  │
└─────────────────────┘
    │
    ├─── No issues ──► Continue
    └─── Issues found ──► @developer fixes ──► Re-run critic
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 5. E2E / Playwright                                                  │
│                                                                     │
│ **testVerifySettings gate (checked FIRST):**                         │
│                                                                     │
│ PRD mode:                                                            │
│   - Check testVerifySettings.prdUIVerify_Analysis (default: true)    │
│     If false → skip Playwright analysis/verification with:           │
│     "⏭️ Skipping Playwright analysis: testVerifySettings             │
│      .prdUIVerify_Analysis is false"                                 │
│   - Check testVerifySettings.prdUIVerify_StoryTest (default: true)   │
│     If false → skip UI test writing with:                            │
│     "⏭️ Skipping UI test writing: testVerifySettings                 │
│      .prdUIVerify_StoryTest is false"                                │
│   - If BOTH are false → skip entire Step 5                           │
│                                                                     │
│ Ad-hoc mode:                                                         │
│   - Default: Playwright is OPT-IN (does NOT run automatically)       │
│   - Runs ONLY when:                                                  │
│     a) User explicitly requests it ("verify in browser",             │
│        "run playwright", "run e2e", selects [E])                     │
│     b) testVerifySettings.adHocUIVerify_StoryTest is explicitly      │
│        set to true in project.json (project opts in)                 │
│   - If neither condition met → skip with:                            │
│     "➖ Playwright: not requested (opt-in for ad-hoc mode)"          │
│                                                                     │
│ **After passing the settings gate:**                                 │
│                                                                     │
│ Playwright verification runs (gated by testVerifySettings only).      │
│                                                                     │
│ Pipeline resolution:                                                 │
│   1. If apps.desktop.buildDeploy configured:                         │
│     → Build-deploy already handled in Step 3.5 (triggerPaths gate)  │
│     → If Step 3.5 succeeded → proceed to Playwright                │
│     → If Step 3.5 was skipped (no trigger match) → proceed         │
│     → If Step 3.5 failed → pipeline already stopped                │
│   2. Else check for postChangeWorkflow override                      │
│   3. Else auto-infer from apps[] configuration:                      │
│     • Desktop + bundled → build → relaunch → playwright-electron    │
│     • Desktop + remote → ensure Electron → playwright-electron      │
│     • Desktop + hybrid → build → relaunch → playwright-electron     │
│     • Web → playwright (dev server + HMR)                           │
│     • No apps[] → playwright with dev server                        │
│                                                                     │
│ Scoping:                                                             │
│   - Run scoped Playwright tests (changed files + 1-hop consumers)   │
│   - Use authentication config for login flows                        │
│                                                                     │
│ On failure: retry with fix attempts (see Retry Strategy below)       │
│                                                                     │
│ CRITICAL: Desktop apps ALWAYS use playwright-electron,              │
│ NEVER browser-based verification                                     │
└─────────────────────────────────────────────────────────────────────┘
    │
    ├─── PASS (or deferred/skip) ──► Continue
    └─── FAIL ──► Fix loop ──► Still failing? See Retry Strategy
    │
    ▼
┌─────────────────────┐
│ 6. Quality critics  │
│ (if resolved)       │
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│ ✅ TASK VERIFIED    │
│                     │
│ Proceed to          │
│ Completion Prompt   │
└─────────────────────┘
```

### Retry Strategy

Playwright failures use a hard cap of **20 attempts per issue**. Both PRD mode and ad-hoc mode behave identically:

| Mode | Max Attempts | On Exhaustion |
|------|-------------|---------------|
| **PRD mode** | 20 attempts with fix attempts between each | STOP and report to user (see below) |
| **Ad-hoc mode** | 20 attempts with fix attempts between each | STOP and report to user (see below) |

Each attempt is logged with what was tried. On exhaustion (20 failed attempts for the same issue), STOP and report:

```
⛔ PLAYWRIGHT FIX LOOP EXHAUSTED

Attempted 20 fixes for the following issue without success:
  [issue description]

Files affected: [list]
Last error: [error summary]
```

No `[S] Save as-is`, no `[D] Discard`, no `[F] Try more` — just stop and inform the user.

See `test-verification-loop` skill for the detailed fix loop algorithm.

### Ops-Only Task Verification

When `taskType` is `ops-with-runtime-impact` (classified during analysis):
- Standard pipeline (typecheck → build → test) is **skipped** (no source files changed)
- In **PRD mode**: Playwright verification runs directly against the affected runtime behavior after ops commands complete
- In **ad-hoc mode**: Playwright is opt-in — runs only if user explicitly requests verification

When `taskType` is `ops-only`:
- Entire pipeline is skipped — mark complete after ops commands succeed

### Verification Contract Integration

When the current chunk's `chunk.json` contains a `verification.contract`, use it to guide verification:

> ⛔ **Staleness check (MANDATORY):** Before using the contract, verify it belongs to the current chunk.
> Compare `verification.contract.generatedAt` against the chunk's `startedAt` time.
> If the contract predates the current chunk (or `verification.contract` is `null`), treat it as **no contract** and fall through to the default activity resolution (Section 2).
> This prevents stale contracts from previous tasks causing verification skips.

| Contract Criterion | Test Activity | Execution |
|--------------------|---------------|-----------|
| `activity: "typecheck"` | Baseline typecheck | `npm run typecheck` |
| `activity: "lint"` | Baseline lint | `npm run lint` |
| `activity: "unit-test"` | Unit test generation + run | @tester → `npm test` |
| `activity: "e2e"` | E2E test generation + run | @ui-tester-playwright |
| `activity: "critic"` | Code review | @critic |

**Recording verification results** (in `chunk.json` → `verification`):

```json
{
  "verification": {
    "status": "pass",
    "results": [
      { "activity": "typecheck", "status": "pass" },
      { "activity": "lint", "status": "pass" },
      { "activity": "unit-test", "status": "pass", "attempts": 1 },
      { "activity": "e2e", "status": "pass", "attempts": 1 }
    ],
    "completedAt": "2026-02-28T10:15:00Z"
  }
}
```

**Contract types:**

| Contract Type | Verification Behavior |
|---------------|----------------------|
| `verifiable` | Run all criteria, all must pass |
| `advisory` | Skip automated verification, log for review |
| `skip` | Run only typecheck + lint |

---

## Section 4: Failure Reporting

After max failed attempts:

```
═══════════════════════════════════════════════════════════════════════
                      ❌ VERIFICATION FAILED
═══════════════════════════════════════════════════════════════════════

Checks failed after [N] fix attempts:

  ❌ Typecheck: 2 errors in SubmitButton.tsx
     - Property 'loading' does not exist on type 'Props'
     - Cannot find module './spinner.css'

Options:
  1. Review and fix manually, then type "verify" again
  2. Type "skip [activity]" to bypass this check (if allowed)
  3. Type "abort" to discard all changes

> _
═══════════════════════════════════════════════════════════════════════
```

### Bypass Restrictions

| Activity | Can Skip? | Rationale |
|----------|-----------|-----------|
| `typecheck` | ❌ Never | Broken types = broken code |
| `lint` | ✅ Yes | Style issues don't break runtime |
| `unit-test` | ✅ Yes | User accepts risk |
| `critic` | ✅ Yes | Suggestions, not blockers |
| `ui-tester-playwright` | ⚠️ Depends | See E2E bypass rules |

**E2E bypass rules:**
- Activities triggered by `immediate` signals → Cannot skip
- Activities triggered by `deferred` signals → Can skip with warning
- Activities in `testing.neverSkip[]` → Cannot skip

---

## Section 5: Completion Prompt

After all checks pass:

```
═══════════════════════════════════════════════════════════════════════
                          TASK COMPLETE
═══════════════════════════════════════════════════════════════════════

✅ [Task description]

Quality checks:
  ✅ Typecheck: passed
  ✅ Lint: passed
  ✅ Unit tests: [N] generated, all passing
  ✅ Critic: no issues

Changed files: [count] ([file list])

Options:
  [C] Commit this change
  [N] Next task (add more work)

> _
═══════════════════════════════════════════════════════════════════════
```

#### Build & Deploy Section (Conditional)

When `apps.desktop.buildDeploy` is configured, include a **Build & Deploy** section in the completion report after "Quality checks":

**If build-deploy ran successfully:**
```
Build & Deploy:
  ✅ Test app updated
     Build command: {buildCommand}
     Build time: {elapsed}s
     Deploy target: {testApp}
```

**If build-deploy was skipped (no trigger paths matched):**
```
Build & Deploy:
  ⚠️ Build skipped (no changed files matched triggerPaths)
```

**If `buildDeploy` is not configured:** Omit the "Build & Deploy" section entirely.

### Handle Response

| Choice | Action |
|--------|--------|
| **C** | Commit the changes, then execute postChangeActions (see Section 5.5) |
| **N** | Return to task prompt |

### Automatic E2E Execution

> ⛔ **E2E write+run is ONE atomic operation. Writing a test without running it is never a valid stopping point.**

> **`testVerifySettings` gate:**
> - **PRD mode:** E2E runs automatically when `testVerifySettings.prdUIVerify_StoryTest` is `true` (default: `true` if absent)
> - **Ad-hoc mode:** E2E is **opt-in** — runs ONLY when user explicitly requests it OR when `testVerifySettings.adHocUIVerify_StoryTest` is explicitly set to `true` in project.json.
>   - If not explicitly set to `true` → skip with: `➖ Playwright: not requested (opt-in for ad-hoc mode)`
>   - User can request at any time by saying "verify in browser", "run playwright", "run e2e", or selecting `[E]`

**When E2E is triggered** (by settings gate or user request):

1. Delegate to @ui-tester-playwright to write E2E tests
2. **Immediately after writing**, run the tests — no user prompt between write and run
3. If tests pass:
   ```
   ✅ E2E tests written and passing:
      • e2e/[test-name].spec.ts — [N] tests, all passing
   ```
4. If tests fail: enter fix loop (delegate fix to @developer, re-run, max 20 attempts per issue)
5. If tests still fail after 20 attempts:
   ```
   ⛔ PLAYWRIGHT FIX LOOP EXHAUSTED

   Attempted 20 fixes for the following issue without success:
     [issue description]

   Files affected: [list]
   Last error: [error summary]
   ```

> **Why atomic?** A test that hasn't been run is unverified — it could have selector mismatches, timing issues, or assertion errors. The user should never see "test written, want me to run it?" — that's two steps for what is logically one operation.

### Ad-hoc During PRD Completion Prompt

```
═══════════════════════════════════════════════════════════════════════
                          TASK COMPLETE
═══════════════════════════════════════════════════════════════════════

✅ [Task description]

Quality checks:
  ✅ Typecheck: passed
  ✅ Lint: passed
  ✅ Unit tests: [N] generated, all passing
  ✅ Critic: no issues

⚠️  Active PRD: [prd-name] ([current-story])

Options:
  [C] Commit this change
  [N] Next task (add more work)
  [R] Return to PRD work

> _
═══════════════════════════════════════════════════════════════════════
```

---

## Section 5.5: Post-Change Actions (After Commit)

> ⛔ **MANDATORY — corresponds to Story Processing Pipeline Step 4.5 in `builder.md`.**
>
> **Runs AFTER commit, not before.** postChangeActions fire once per commit to propagate changes downstream.
> These are distinct from the quality pipeline (Section 3) which runs before commit.
>
> **Applies to ALL commit paths:** PRD per-story commits (Pipeline Step 4), ad-hoc task commits (Phase 2 → Step 1), and any other auto-commit.
> **Failure behavior:** If Builder commits and moves on without checking postChangeActions, the pipeline contract is violated.

After the user chooses **[C] Commit** and the commit succeeds, check `project.json` → `postChangeActions`:

```
Commit succeeds
    │
    ▼
Read project.json → postChangeActions[]
    │
    ├─── No postChangeActions defined ──► Done (proceed to next story or session end)
    │
    └─── Has postChangeActions ──► Evaluate each action's trigger condition
              │
              ▼
         For each action where trigger matches:
              │
              ├── type: "pending-update" ──► Create docs/pending-updates/ file in target project, auto-commit
              ├── type: "agent"          ──► Invoke the specified agent (@support-article-writer, @tools-writer, etc.)
              ├── type: "command"        ──► Run the shell command
              └── type: "notify"         ──► Display the message to the user
```

### Trigger Evaluation

For each action in `postChangeActions[]`:

| Trigger | How to evaluate |
|---------|-----------------|
| `always` | Always fires |
| `files-changed-in` | Check if any committed files match `pathPatterns` globs |
| `feature-change` | Agent judgment: did this change add/modify a user-facing feature? |
| `user-facing-change` | Agent judgment: did this change affect anything a user would see? |

### Action Execution

**`pending-update`:**
1. Resolve `targetProject` via `relatedProjects` in `project.json`
2. Look up the target project path from `projects.json`
3. Create a pending update file: `<target-project>/docs/pending-updates/YYYY-MM-DD-<source>-sync.md`
4. Auto-commit the file to the target project repo:
   ```bash
   cd <target-project> && git add docs/pending-updates/ && git commit -m "chore: Queue sync update from <source-project>"
   ```

**`agent`:**
1. Invoke the specified agent with the `prompt` template
2. Pass changed files and story context
3. Wait for agent completion before proceeding

**`command`:**
1. Run `command` in the project root
2. If `failureMode` is `warn` (default), log warning on failure but continue
3. If `failureMode` is `block`, stop and report error

**`notify`:**
1. Display `message` template to the user (variable substitution: `{changedFiles}`, `{storyId}`, `{prdId}`)
2. Continue immediately (no user response needed)

### Error Handling

- Post-change actions are **fire-once, best-effort by default**
- A failing action does NOT roll back the commit
- Failed actions are logged but do not block the next story
- Exception: actions with `failureMode: "block"` will stop and report

---

Load these specialized skills on demand — only when you reach that phase of testing:

| Need to... | Load this skill |
|------------|-----------------|
| Run the 3-pass verification loop | `test-verification-loop` |
| Detect/handle prerequisite failures | `test-prerequisite-detection` |
| Execute E2E tests (PRD or ad-hoc) | `ui-test-flow` |
| Run Playwright UI verification | `test-ui-verification` |
| Handle failures, manual fallback | `test-failure-handling` |
| Resolve test base URL | `test-url-resolution` |
| Clean up test users | `test-user-cleanup` |
| Sync test documentation | `test-doc-sync` |

**Example:** To load the verification loop skill:
```
skill(name="test-verification-loop")
```

Load skills incrementally — only when you reach that phase of testing. This reduces token consumption compared to loading the entire test flow upfront.

---

## Section 7: Quality Checks (Optional)

If `project.json → testing.qualityChecks: true`:

After E2E tests pass, run @quality-critic:

```
Run @quality-critic with:
  devServerUrl: http://localhost:{devPort}
  changedFiles: [files changed in this PRD/session]
  mode: comprehensive  // for PRD completion
        // or "quick" for ad-hoc
```

**Quality checks include:**
- Accessibility (axe-core) — WCAG 2.1 AA compliance
- Layout Shift (CLS) — cumulative layout shift detection
- Visual Regression — screenshot comparison with baselines
- Performance — FCP, LCP, TTI metrics

**Handle results:**
- No critical issues → Continue
- Critical issues → Show prompt with [F]ix / [S]kip options

---

## Section 8: Full-Site Visual Audit Flow

Run after substantial UI/content changes:

### Trigger Conditions

- Multiple user-facing pages changed in one batch/PRD
- Changes to navigation, docs/help pages, diagrams
- Explicit request for visual/UX coherence sweep

### Required Checks

For each audited route/state, test both desktop and mobile:

1. **Diagram/flow coherence** — Arrow direction, sequencing, labels
2. **Navigation behavior** — Mobile hamburger, overlay layering
3. **Code-block usability** — Copy button, long line handling
4. **Short-page spacing quality** — Avoid oversized empty gaps

### Findings Output Contract

Return structured report grouped by severity (`critical`, `high`, `medium`, `low`).
Each finding includes page URL, user impact, and fix recommendation.

### Post-Fix Re-Verification

After fixes:
- Re-test each prior finding at the same viewport(s)
- Mark each as resolved or still failing
- Block sign-off if unresolved `critical` issues remain

---

## Escape Hatches (Power Users Only)

These overrides exist but are **never required**:

### Per-Task Force

```
User: "force full"
Builder: "Adding all critics + unit tests..."
```

### Per-Task Skip

```
User: "skip security-critic"
Builder: "Removing @security-critic from this run..."
```

### Project-Level Configuration

```json
{
  "testing": {
    "alwaysInclude": ["security-critic"],
    "neverSkip": ["exploit-critic"]
  }
}
```


