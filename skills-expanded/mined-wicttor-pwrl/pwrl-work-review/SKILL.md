---
name: pwrl-work-review
description: Review, simplify, and consolidate code after execution
argument-hint: "[Executed tasks from pwrl-work-execute, design specs (optional)]"
---

# pwrl-work-review — Code Simplification & System Review

## Interaction Method

- Use platform's `ask_user_question`, `ask_user`, `ask_user_input`, `vscode/askQuestions` or any available extension/tool for user interaction for all decisions
- Ask one question at a time
- Use multiple-choice questions when possible
- If input is empty, ask: "Should the implementation be reviewed? Confirm scope match, test coverage, and code quality."
- Provide clear recovery suggestions when errors occur

**Purpose:** Review code after execution to consolidate duplication, extract shared helpers, run system-wide consistency checks, compare UI implementations to design specs (when applicable), and determine readiness for shipping.

## Input

Accepts execution results from `pwrl-work-execute`:

```yaml
mode: serial
taskCount: 5
tasksCompleted: 5
results:
  - unit-id: S1
    taskFile: docs/tasks/for-review/...
    status: for-review
    testsPassed: true
    files: [src/utils.ts, src/api.ts]
```

Optional: design spec references for UI work (e.g., Figma links, `docs/design/` files).

## Output: Review Summary

```yaml
duplicationFound: true
duplicationsConsolidated: 3
helpersExtracted: 2
helperNames: [isValidEmail, parseUserInput]
LOCReduced: 120
systemChecks:
  eventTriggering: pass
  mockCoverage: warning
  idempotency: pass
  alternateEntryPoints: pass
designSpecDeltas: 0
refactoringScope: controlled
readyForShipping: true
recommendations:
  - "Add 2 integration tests for mock coverage"
```

---

## Workflow

### 1. Identify Modified Files

After every 2-3 related tasks:

1. Collect files affected by the completed tasks:
   - From each task's `files` field in execution results
   - From `git diff` against base branch: `git diff --name-only <base>...HEAD`
2. Build a consolidated list of files modified by these tasks
3. Focus review ONLY on these files (scope control)

### 2. Detect Duplication

Scan modified files for code duplication:

**Approach:**

1. For each modified file, look for:
   - Identical code blocks (same logic, same structure)
   - Similar patterns with different variable names
   - Copy-paste code (identical comments, same ordering)

2. Cross-file duplication:
   - Compare files modified by different tasks
   - If two tasks modified different files with similar logic → candidate

3. For each candidate, show:
   - Location (file:lines)
   - Code snippet (before)
   - Proposed consolidation (after)
   - LOC reduction estimate

**Example:**

```
Found duplication between src/user.ts:45 and src/signup.ts:72:
  Both validate email with same regex: /^[^@]+@[^@]+\.[^@]+$/
  Proposed: Extract isValidEmail() to src/validation.ts
  LOC reduction: 12 lines
```

**Decision:**

- Ask user: "Extract helper? (yes/no/skip)"
- If yes: proceed to Step 3 (Helper Extraction)
- If no or skip: log as noted for future refactoring

### 3. Extract Helpers

For confirmed candidates, extract shared logic:

**When to extract:**

- Code appears 2+ times across modified files
- Extraction improves readability (function name self-documents)
- Extraction improves testability

**When NOT to extract (YAGNI):**

- Code appears only once
- Extract adds indirection without benefit
- Extract would create complex API (too many parameters)

**Extraction process:**

1. Design helper:
   - Name: clear verb/noun describing what it does
   - Parameters: minimal set needed
   - Return value: typed and documented

2. Create helper file (or add to existing shared module):
   - If no shared module exists: create one (e.g., `src/utils.ts`, `src/validation.ts`)
   - If shared module exists: add helper to it

3. Write tests for helper (test-first):
   - Test normal case
   - Test edge cases (empty, null, boundary)
   - Test error handling

4. Replace call sites:
   - Replace duplicate code blocks with helper call
   - Update all references

5. Run tests:
   - Verify all tests still pass
   - Log: "Extracted [helperName] → [file], replaced [N] call sites, -[M] LOC"

### 4. Run System Checks

After simplifying, verify system consistency:

**Check 1: Event/Observer/Callback Triggering**

- Are events emitted correctly? (e.g., `user.created` after signup)
- Are listeners registered and invoked?
- ✅ **Pass if:** Tests cover real event flow (not just mock assertions)
- ⚠️ **Warn if:** All event tests use mocks (real listener not tested)

**Check 2: Mock vs. Real Interaction Balance**

- What proportion of tests use mocked dependencies vs. real implementations?
- ✅ **Pass if:** ≥1 integration test per feature covers real interactions
- ⚠️ **Warn if:** All tests use mocks (no integration coverage)

**Check 3: Idempotency & Cleanup Safety**

- Can operations be retried safely?
- Are resources cleaned up after failure? (finally blocks, teardown)
- ✅ **Pass if:** Retry doesn't cause double effects; cleanup always runs
- ⚠️ **Warn if:** Failure leaves partial state or resource leaks

**Check 4: Alternate Entry Points**

- Is behavior consistent across different access methods?
- ✅ **Pass if:** All entry points tested with same behavior expectations
- ⚠️ **Warn if:** Only one entry point tested, or behavior diverges

**Log results:**

```
System Check Results:
  [✓] Event triggering: POST /user fires 'user.created'
  [⚠] Mock coverage: 8/10 tests use mocks → add 2 integration tests
  [✓] Idempotency: DELETE /user safe to retry
  [✓] Alternate entry points: API + CLI tested, consistent behavior
```

### 5. Compare to Design Specs (UI Work Only)

For tasks involving UI/component changes:

**If design specs exist:**

- Read from `docs/design/` or linked Figma file
- Compare: layout, spacing, colors, typography, responsive behavior
- Classify each delta:

| Severity | Meaning                                     | Action           |
| -------- | ------------------------------------------- | ---------------- |
| Minor    | Within 2px, slightly different shade        | Acceptable, note |
| Moderate | Wrong component variant, minor layout shift | Should fix       |
| Critical | Completely wrong layout, broken responsive  | Must fix         |

**If no design specs:**

- Skip this step entirely
- Log: "No design specs found; skipping visual comparison"

### 6. Control Refactoring Scope

**Golden Rule: Only simplify code that was changed by executed tasks.**

**Do:**

- Simplify code you just wrote
- Extract helpers from duplications you introduced
- Fix obvious bugs in modified code
- Improve tests for changed behavior

**Do NOT:**

- Refactor unrelated modules
- Do "while we're here" cleanup
- Change naming/style for consistency in untouched code

**Enforcement:**

- Build list of affected files from task execution results
- If scope check finds a change to an unrelated file:
  - Warn: "File [path] was modified but is not in any task's files list"
  - Ask: "Remove this unrelated change before shipping? (yes/no)"

### 7. Produce Review Summary

```yaml
duplicationFound: true
duplicationsConsolidated: 2
helpersExtracted: 1
helperNames: [isValidEmail]
LOCReduced: 34
systemChecks:
  eventTriggering: pass
  mockCoverage: warning
  idempotency: pass
  alternateEntryPoints: pass
refactoringScope: controlled
readyForShipping: true
recommendations:
  - "Add 2 integration tests with real DB for user module"
```

If `readyForShipping` is true, work is ready for pull request creation.

---

## Optional Deep Review Mode

For complex or high-risk changes, offer deep review:

```
/pwrl-work-review docs/tasks/for-review/ --deep
```

Deep review adds:

- **Performance:** Any obvious regressions? (N+1 queries, memory leaks)
- **Security:** New vulnerabilities? (XSS, injection, auth bypass)
- **Accessibility:** UI changes only (ARIA labels, keyboard nav, contrast)
- **API contracts:** Breaking changes? (new required params, removed fields)
- **DB migrations:** Safe? (backward compatible, rollback plan)

For detailed analysis, use the dedicated `/pwrl-review` skill.

---

## Error Handling

| Scenario                       | Handling                                           |
| ------------------------------ | -------------------------------------------------- |
| No duplications found          | Log "No duplications detected" (normal)            |
| Git diff parsing fails         | Log error, ask user to verify git state, retry     |
| Design spec not found          | Skip design comparison, continue                   |
| Tests fail after consolidation | Revert consolidation, mark as blocked, investigate |
| Unrelated changes in diff      | Warn user, ask to remove or explain                |

---

## Dependencies

- **pwrl-work-execute (S5)** — Consumes executed task results
- **Git** — For diff analysis
- **File system** — For reading/writing modified files
- **Test framework** — For verifying helpers and consolidations

## References

- **S1 Analysis:** `docs/analysis/2026-06-05-pwrl-work-structure-analysis.md`
- **Source Phase 3:** Installed `pwrl-work` skill (Phase 3: Simplify & Review, lines 173-185)
