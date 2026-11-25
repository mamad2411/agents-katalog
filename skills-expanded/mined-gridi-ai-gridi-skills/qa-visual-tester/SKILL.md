---
name: qa-visual-tester
description: >
  A skill that creates QA test sheets based on user requirements and performs visual verification
  like manual QA by directly viewing real browser screens using Microsoft Playwright MCP.
  Verification results are recorded by creating individual directories per QA issue, with screenshots included.
  Use this skill when QA testing, visual verification, manual test automation, QA sheet creation, or screen verification is requested.
---

## 🌐 Language

> All output documents and user-facing messages must be written in the language specified
> by `crew-config.json → preferences.language`. If not set, default to English.

# QA Visual Tester

Creates QA sheets based on user requirements, verifies screens using Playwright MCP, and records results per issue.

## Workflow Overview

```
1. Gather Requirements ──────────── Confirm QA target/scope from the user
        │
        ▼
2. Create QA Sheet ──────────────── Generate test item markdown document
        │
        ▼
3. Execute Tests (Playwright MCP) ── Perform visual verification on real screens
        │
        ▼
4. Record Results ───────────────── Issue directory + screenshots + report per issue
        │
        ▼
5. Final QA Report ──────────────── Write overall summary report
```

## 1. Gather Requirements

Confirm the following with the user:

- **Target URL**: URL of the web application to test
- **QA Scope**: List of features/pages to test
- **Expected Behavior**: Description of normal behavior for each feature (documents, verbal, stories, etc.)
- **Browser Size**: Desktop (1280x720) / Mobile (390x844) / Both (default: Desktop)

```
Example input:
- "Run QA on login/sign-up at http://localhost:3000"
- "Create a QA sheet based on docs/user-stories/account.md and run tests"
- "Run full QA on the deployed staging environment: https://staging.example.com"
```

If requirements are ambiguous, always ask for clarification. If the QA scope is broad, categorize by page/feature.

## 2. Create QA Sheet

### Output Directory Structure

```
{project-root}/qa-results/{date}-{target-name}/
├── qa-sheet.md              ← QA sheet (test item list)
├── qa-report.md             ← Final QA report (written after execution)
└── issues/                  ← Per-issue directories
    ├── ISSUE-001-{slug}/
    │   ├── report.md
    │   └── screenshot-*.png
    └── ISSUE-002-{slug}/
        ├── report.md
        └── screenshot-*.png
```

### QA Sheet Format

qa-sheet.md template: [references/qa-sheet-template.md](references/qa-sheet-template.md)

The QA sheet uses the Given-When-Then format for each test item. Item IDs follow the `QA-{feature-code}-{sequence}` format.

## 3. Execute Tests (Playwright MCP)

### Core Principle

> **Use Playwright MCP tools only.** Do not write Playwright test code (.spec.ts).
> Like automating manual QA, use MCP tools to directly control the browser and visually inspect the screen.

### Playwright MCP Tool Execution Sequence

Execute the following pattern for each test item:

```
1. browser_navigate  → Navigate to target page
2. browser_snapshot  → Understand current page structure (accessibility snapshot)
3. browser_click / browser_fill_form / browser_press_key → Reproduce user actions
4. browser_snapshot  → Verify action result structure
5. browser_take_screenshot → Capture result screen (evidence preservation)
6. Compare with expected result → PASS / FAIL determination
```

### Key MCP Tool Usage

**Page Navigation and Structure Understanding:**
- `browser_navigate` : Navigate to URL
- `browser_snapshot` : Returns the accessibility tree of the current page (including element ref numbers)
- `browser_take_screenshot` : Capture current screen as PNG

**Reproducing User Actions:**
- `browser_click` : Click element by ref number
- `browser_fill_form` : Enter text in form fields
- `browser_type` : Keyboard typing
- `browser_press_key` : Enter specific keys (Enter, Tab, Escape, etc.)
- `browser_select_option` : Select dropdown options
- `browser_hover` : Mouse hover

**Verification Aids:**
- `browser_evaluate` : Execute JavaScript (DOM inspection, value checking, etc.)
- `browser_wait_for` : Wait for specific conditions
- `browser_console_messages` : Check console logs/errors
- `browser_network_requests` : Check network requests

### Verification Criteria

| Verdict | Criteria |
|---------|----------|
| **PASS** | Expected result matches actual result |
| **FAIL** | Expected result does not match actual result |
| **BLOCKED** | Test cannot be performed due to unmet preconditions |
| **SKIP** | Test target is not yet implemented |

An issue directory must be created for every FAIL verdict.

### Screenshot Saving Rules

- PASS items: No separate saving required (save to qa-results root if needed)
- FAIL items: Must be saved in the corresponding issue directory
- Filename format: `screenshot-{sequence}-{description}.png`

## 4. Issue Recording

Create an individual issue directory for each item with a FAIL verdict.

### Issue Directory Structure

```
issues/ISSUE-001-login-error-message-missing/
├── report.md          ← Issue detail report
├── screenshot-01-before-action.png
├── screenshot-02-after-action.png
└── screenshot-03-expected-vs-actual.png
```

Issue report.md template: [references/issue-report-template.md](references/issue-report-template.md)

## 5. Final QA Report

After all test items are executed, summarize the overall results in qa-report.md.

```markdown
# QA Report

**Test Date**: {timestamp}
**Target URL**: {url}
**Test Environment**: {browser, screen size}

## Results Summary

| Item | Count |
|------|-------|
| Total Tests | {total} |
| PASS | {pass} |
| FAIL | {fail} |
| BLOCKED | {blocked} |
| SKIP | {skip} |

## Detailed Test Results

| ID | Test Item | Result | Notes |
|----|-----------|--------|-------|
| QA-AUTH-001 | Normal login | PASS | - |
| QA-AUTH-002 | Wrong password error | FAIL | See ISSUE-001 |

## Discovered Issues

| Issue ID | Severity | Title | Related TC |
|----------|----------|-------|------------|
| ISSUE-001 | High | Login error message not displayed | QA-AUTH-002 |

## Issue Directories

- `issues/ISSUE-001-login-error-message-missing/`
```

## Completion Checklist

- [ ] 1. User requirements confirmed
- [ ] 2. QA sheet (qa-sheet.md) created
- [ ] 3. All test items executed via Playwright MCP
- [ ] 4. Issue directories + screenshots created for FAIL items
- [ ] 5. Final QA report (qa-report.md) written

## References

- QA Sheet Template: [references/qa-sheet-template.md](references/qa-sheet-template.md)
- Issue Report Template: [references/issue-report-template.md](references/issue-report-template.md)
