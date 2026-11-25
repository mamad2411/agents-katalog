---
name: pwrl-review-analyze
description: "Analyze code for quality, security, tests, documentation, and integration issues."
argument-hint: "[prepare artifact from pwrl-review-prepare]"
---

# pwrl-review-analyze — Comprehensive Code Analysis

**Purpose:** Phase 3 of review workflow. Performs deep analysis of code changes across multiple dimensions: quality, security, test coverage, documentation, and integration. Identifies issues and compiles findings for the report phase.

## Interaction Method

- Run tools automatically (linter, security scanner, test runner, type checker).
- Show progress and findings in real-time.
- Prompt user only for manual review of high-complexity or ambiguous items.
- Parse tool output to extract issues with severity levels.

## Input: Prepare Artifact

Expects artifact from `pwrl-review-prepare` with:

```yaml
prepare_id: YYYY-MM-DD-UNN-prepare
files_modified: [file list]
review_scope:
  code_quality: true
  security: true
  test_coverage: true
  documentation: true
tools_configured: [linter, test_framework, type_checker]
```

## Output: Analyze Artifact

Emit analyze artifact. See [artifact-schemas.md](../pwrl-review/references/artifact-schemas.md) for the complete schema.

## Ready for Report
- **Status:** ready
- **Next Skill:** pwrl-review-report
- **Artifacts Passed:** This analyze artifact + findings
```

Artifact passed to `pwrl-review-report`.

## Workflow

### Step 1: Verify Prepare Artifact

1. Check that input artifact has:
   - Valid `prepare_id`
   - `files_modified` list populated
   - `tools_configured` items listed
   - `ready_for_analysis: true`

2. **If verification fails:**
   - Return error: "Prepare artifact invalid. Return to pwrl-review-prepare."

### Step 2: Code Quality Analysis

**Run configured linter/style checker:**

1. **Execute linter** on all modified source files
2. **Parse output:**
   - Categorize by rule (complexity, style, logic)
   - Extract file:line for each issue
   - Determine severity (error/warning)
   - Map to severity levels:
     - **CRITICAL:** Logic errors, null pointer dereferences
     - **MAJOR:** High complexity (>10 nesting), performance issues
     - **MINOR:** Style, naming, missing constants

3. **Report findings:**
   - Top 5-10 issues by severity
   - Trend (improved/same/degraded vs. baseline)
   - Code quality score if available

**Special checks:**

- Unused imports: MINOR
- Unused variables/functions: MAJOR (if public API)
- Too many parameters (>5): MINOR
- Duplicate code blocks (>50 LOC): MAJOR
- Complex conditionals (>4 branches): MAJOR

### Step 3: Security Analysis

**Run security scanner or manual checks:**

1. **Automated security scan** (if tool configured):
   - Detect SQL injection, XSS, XXE, CSRF risks
   - Check for hardcoded secrets
   - Validate input sanitization
   - Verify auth/authorization logic

2. **Manual high-risk patterns:**
   - New database queries (check SQL injection)
   - New API endpoints (check auth, validation)
   - New external API calls (check rate limits, error handling)
   - Changed authentication logic (check correctness)

3. **Severity mapping:**
   - **CRITICAL:** SQL injection, hardcoded secrets, missing auth
   - **MAJOR:** Incomplete validation, weak error handling
   - **MINOR:** Inconsistent security patterns

### Step 4: Test Coverage Analysis

**If test files modified or code quality checks enabled:**

1. **Run test suite** on modified code
   - Count passed/failed tests
   - Extract coverage metrics
   - Identify uncovered lines/branches

2. **Compare to baseline:**
   - Coverage before: X%
   - Coverage after: Y%
   - If Y < X: MAJOR issue
   - If Y < required (e.g., 80%): MAJOR issue
   - If Y >= required: ✓ pass

3. **Test quality checks:**
   - Assertions per test (should be 1-3)
   - Mocking strategy (appropriate?)
   - Edge case coverage (positive, negative, boundary)
   - Test names descriptive?

4. **Severity mapping:**
   - **CRITICAL:** No tests for critical path
   - **MAJOR:** Coverage < required threshold
   - **MINOR:** Weak test assertions, poor names

### Step 5: Documentation Analysis

**If docs modified or code modified:**

1. **Check README/documentation updates:**
   - Does README mention new APIs/features?
   - Deprecations documented?
   - Examples provided for complex changes?

2. **Check inline documentation:**
   - Functions have JSDoc/docstrings?
   - Types annotated?
   - Comments explain "why" not just "what"?

3. **Check configuration:**
   - Config schema documented?
   - Environment variables documented?

4. **Severity mapping:**
   - **MAJOR:** No docs for new public API
   - **MINOR:** Missing comments, poor examples

### Step 6: Integration Checks

**Verify code integrates with system:**

1. **Build verification:**
   - Run build command on modified code
   - Check for compilation errors
   - Verify no import errors
   - **Status:** ✓ pass or ✗ fail with error

2. **Test verification:**
   - Run full test suite (not just modified tests)
   - Check for test failures
   - **Status:** ✓ pass or ✗ fail with list of failures

3. **Regression detection:**
   - Compare test results to baseline
   - New test failures?
   - Performance regressions? (if benchmarks exist)
   - **Status:** ✓ none or ✗ regressions detected

4. **Import verification:**
   - Check all imports resolvable
   - No circular dependencies?
   - All dependencies defined in package.json?

**Severity mapping:**

- **CRITICAL:** Build fails, core tests fail
- **MAJOR:** New test failures, regressions
- **MINOR:** Warnings, performance degradation

### Step 7: Compile Findings

**Organize all findings by category:**

1. **Group by dimension:**
   - Code Quality: [list of issues]
   - Security: [list of issues]
   - Tests: [list of issues]
   - Documentation: [list of issues]
   - Integration: [list of issues]

2. **Sort by severity within each:**
   - CRITICAL issues first
   - MAJOR issues second
   - MINOR issues last

3. **Count totals:**
   - Total issues
   - By severity
   - By category

### Step 8: Generate Recommendation

**Determine approval status:**

| Condition                       | Recommendation      |
| ------------------------------- | ------------------- |
| 0 CRITICAL, 0 MAJOR, any MINOR  | **approved**        |
| 0 CRITICAL, ≤3 MAJOR, any MINOR | **request-changes** |
| ≥1 CRITICAL or >3 MAJOR or fail | **rejected**        |
| Integration fails (build/tests) | **rejected**        |

### Step 9: Generate Analyze Artifact

Emit complete artifact with all findings, recommendation, and next steps.

## Error Handling & Testing

See [error-and-testing.md](../pwrl-review/references/error-and-testing.md) for comprehensive error recovery strategies, prevention tactics, and test coverage expectations for this phase.

**Edge Cases:**

- ✅ Build fails (CRITICAL, recommended: rejected)
- ✅ High complexity (MAJOR)
- ✅ Unused imports (MINOR)
- ✅ Security scanner unavailable (skipped)
- ✅ Multiple CRITICAL issues (recommended: rejected)

**Output Validation Tests:**

- ✅ Artifact structure complete
- ✅ Findings organized by category/severity
- ✅ Recommendation logic correct
- ✅ Counts accurate
