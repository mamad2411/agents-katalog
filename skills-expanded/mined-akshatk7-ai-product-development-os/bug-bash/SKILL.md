---
name: bug-bash
description: >
  Run a structured bug bash against a test plan, designs, and live product.
  Use when the user mentions bug bash, test plan execution, QA session,
  or wants to systematically test a feature before launch.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Bug Bash Execution

Structured test plan execution framework for pre-launch quality assurance.

## Phases

### Phase 1: Orient
1. Read the test plan (Google Sheet, markdown, or linked doc)
2. Read the project's CONTEXT.md, designs.md, and any product-brief.md
3. Identify the feature surface area — what pages/flows are being tested

### Phase 2: Learn the Designs
1. If Figma links exist, get design context for each relevant screen
2. Document expected behavior per screen/flow
3. Note any edge cases or conditional states from the designs

### Phase 3: Execute Test Plan
1. Walk through each test case in the plan
2. For each test case: navigate to the feature, verify expected behavior, capture screenshots
3. Record PASS/FAIL per test case with evidence (screenshot links)

### Phase 4: File Bugs
1. For each failed test case, document: steps to reproduce, expected vs actual, screenshot, severity
2. File bugs in the team's tracker (Jira, Linear, GitHub Issues)
3. Tag with the bug bash label/epic

### Phase 5: Report
1. Generate a summary: total test cases, pass rate, critical bugs found
2. Categorize bugs by severity (P0/P1/P2)
3. Share the report in the project's updates.md
