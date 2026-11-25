---
name: qa-test-case-generation
description: Use when generating manual QA test cases from requirements, BRDs, user stories, acceptance criteria, spreadsheets, live mockup/prototype URLs, uploaded mockups, screenshots, wireframes, or existing test case templates; especially when coverage, deduplication, traceability, validations, permissions, workflows, or edge cases matter.
---

# QA Test Case Generation

## Overview

Act as a senior manual QA engineer. Analyze requirements and optional mockups/templates, then produce professional, complete, practical, non-duplicated test cases that are ready for Excel, Google Sheets, or a test management tool.

The output must be traceable to requirements, mockup elements, business rules, or logical QA risks. Do not invent unrealistic requirements; document assumptions and clarifications when information is missing.

## Resources

Use these files as needed:

- `assets/default-test-case-template.md` - default table format when no user template is provided.
- `references/qa-coverage-checklist.md` - broad QA coverage checklist.
- `references/boundary-edge-case-checklist.md` - validation, boundary, and edge-case prompts.
- `references/deduplication-rules.md` - rules for removing repeated or overlapping cases.
- `references/live-mockup-url-review.md` - detailed checklist for inspecting live mockup or prototype URLs.
- `examples/sample-output.md` - compact example of final output style.

## Workflow

### Step 1: Intake Analysis

Identify every provided input before generating test cases:

- Required requirement source: requirements document, spreadsheet, BRD, user story, feature description, acceptance criteria, API spec, or ticket.
- Optional live mockup/prototype URL.
- Optional uploaded mockups, screenshots, wireframes, prototypes, or UI references.
- Optional existing test case template.
- Optional existing test cases for reuse or duplicate removal.
- Optional user roles, permissions, business rules, API documentation, and acceptance criteria.
- Any explicit output constraints such as Excel-ready table, CSV, Markdown, test management format, language, module scope, or ID prefix.

Summarize the module or feature under test in 3-6 bullets. If the requirements are in a spreadsheet, review all relevant sheets, column headers, hidden context, notes, and status fields when accessible.

### Step 2: Requirement Review

Extract and organize:

- Features, modules, screens, fields, actions, buttons, menus, links, uploads, downloads, exports, and attachments.
- Workflows, alternate flows, approvals, rejections, cancellations, edits, deletes, view-only flows, and status transitions.
- Business rules, validations, calculations, dependencies, prerequisites, permissions, roles, and access restrictions.
- Required and optional fields, accepted formats, default values, uniqueness rules, min/max lengths, numeric ranges, date rules, and file constraints.
- Search, filter, sort, pagination, reset/clear, save/submit/cancel, refresh/reopen behavior, persistence, duplicate records, notifications, and messages.
- UI and non-functional expectations that affect manual QA, including labels, formatting, usability, layout, data display, and error handling.

Track unclear or missing details immediately under `Clarifications Needed`; do not hide ambiguity inside test cases.

### Step 3: Mockup and Prototype Review

When uploaded mockups, screenshots, or wireframes are provided, compare them against the requirements and record:

- Missing UI elements from requirements.
- Extra UI elements not described in requirements.
- Inconsistent labels, field names, statuses, menu names, icons, or button text.
- Missing buttons, links, actions, filters, table columns, upload/download controls, or confirmation dialogs.
- Required vs optional field mismatches.
- Layout, usability, accessibility, readability, grouping, ordering, and formatting concerns.

When a live mockup/prototype URL is provided, open the URL and inspect the live UI as a QA engineer. Load `references/live-mockup-url-review.md` and use it to:

- Navigate available pages, tabs, menus, buttons, modals, forms, tables, filters, action menus, and links.
- Record every visible screen/page and every visible UI element, including fields, buttons, dropdowns, checkboxes, radio buttons, tables, filters, search inputs, date pickers, upload fields, status labels, icons, actions, links, pagination, sorting controls, and navigation elements.
- Observe available states such as empty, loading, disabled, read-only, error, success, draft, approval, rejected, and pending states when they are visible or discoverable without unsafe actions.
- Identify possible user flows such as create, view, edit, delete, search, filter, sort, approve, reject, submit, cancel, upload, download, open/view attachment, export, and import.
- Interact carefully: open menus, dropdowns, and modals only as needed to discover behavior; do not submit destructive actions or delete real data unless explicitly allowed and clearly safe in a mock/demo environment.
- If authentication, loading failures, blank pages, broken navigation, inaccessible pages, or unclear prototype behavior blocks review, document the limitation and continue with available requirements or screenshots.

When both requirements and any mockup source are provided, produce a gap analysis with:

- Requirements clearly represented in the mockup.
- Requirements missing from the mockup or not testable in the live UI.
- Extra UI elements or flows in the mockup that are not mentioned in the requirements.
- Conflicts or inconsistencies such as mismatched labels, missing fields, different statuses, wrong field types, missing/unexpected buttons, inconsistent validation, or unclear workflow behavior.
- Questions and clarifications needed from the product owner, BA, designer, or developer.

Generate UI-specific and gap-based test cases for relevant mismatches and list unresolved mismatches under `Missing/Unclear Requirements` or the live mockup gap analysis section.

### Step 4: Template Handling

If the user provides a test case template, follow it exactly:

- Preserve column names, order, ID style, status values, priority/severity labels, wording conventions, and formatting expectations.
- Add only fields that are clearly requested or necessary; if a needed field is absent, place traceability or notes in the closest available column.
- Match the template's granularity. If the template uses one row per test case, do not split steps across rows unless the template does.

If no template is provided, use the default format from `assets/default-test-case-template.md` with these columns:

- Test Case ID
- Module / Feature
- Test Scenario
- Preconditions
- Test Steps
- Test Data
- Expected Result
- Priority
- Severity
- Test Type
- Status
- Notes

### Step 5: Test Case Design

Create cases that are practical for a manual QA engineer to execute. Cover the feature from user intent through data persistence:

- Requirement-based scenarios from written requirements, BRDs, user stories, acceptance criteria, and business rules.
- UI-based scenarios from uploaded mockups, screenshots, wireframes, or live mockup/prototype observation.
- Requirement vs UI gap scenarios where the mockup is missing, adds, or conflicts with expected behavior.
- Positive scenarios and core happy paths.
- Negative scenarios, invalid input, empty input, required field validation, optional field behavior, boundary values, rare user behavior, and error handling.
- Minimum and maximum length, special characters, numeric fields, date fields, date ranges, and past/future restrictions.
- File upload behavior, file size limits, file type validation, preview/view/download/export behavior, and attachment persistence when relevant.
- Dropdowns, multi-selects, search, filters, sorting, pagination, reset/clear behavior, table columns, and data formatting.
- Save, submit, cancel, edit, delete, view-only, confirmation popups, success messages, error messages, API/backend validation, and refresh/reopen persistence.
- Permission-based access, role-based access, status transitions, approval/rejection workflows, dependencies between fields, and dependencies between test cases.
- Empty, loading, disabled, read-only, error, success, draft, approval, rejected, pending, and other visible UI states.
- Accessibility and usability observations that are visible from the UI: labels, required indicators, button clarity, error visibility, color/status clarity, table readability, form layout, navigation clarity, disabled button clarity, and basic keyboard/navigation concerns when observable. Mark unverifiable accessibility items as `Needs validation`.
- Regression risks and data correctness/formatting risks introduced by the requirements or observed UI.

Use professional QA language. Prefer `Verify that...` in scenarios and expected results. Avoid vague wording such as `works correctly`, `properly`, or `as expected` unless followed by a specific verifiable behavior.

### Step 6: Deduplication and Quality Review

Before finalizing, review every case against `references/deduplication-rules.md`:

- Remove duplicates and repeated cases.
- Merge cases that test the same behavior with different wording.
- Keep separate cases when inputs, roles, statuses, validations, or outcomes are meaningfully different.
- Confirm every case has one clear purpose and is traceable to a requirement, mockup element, business rule, or logical QA risk.
- Mark the source for each case as `Requirement`, `Mockup`, `Requirement + Mockup`, or `Inferred QA Risk`. If the active template has no `Source` column, include this source tag in `Notes`.
- Include requirement IDs in the `Source` or `Notes` column when IDs are available.
- Confirm test steps are numbered, executable, and do not depend on hidden knowledge.
- Confirm expected results are specific, observable, and verifiable.
- Prioritize risky and business-critical flows.

### Step 7: Final Output

Return these sections in order:

1. `Requirement Summary`
2. `Live Mockup Observation Summary` when a live mockup/prototype URL is provided
3. `Requirement vs Mockup Gap Analysis` when mockups, screenshots, wireframes, or live URLs are provided
4. `Assumptions`
5. `Clarifications Needed`
6. `Coverage Areas` or `Test Coverage Strategy`
7. `Test Cases Table`
8. `Missing/Unclear Requirements`
9. `Suggested Improvements` or `Missed Risks / Additional QA Suggestions`

If a section has no findings, write `None identified` rather than deleting the section.

For `Live Mockup Observation Summary`, include the URL reviewed, pages/screens observed, main UI elements, main user actions, important UI states, and inaccessible or unclear areas.

For `Requirement vs Mockup Gap Analysis`, include requirements covered by the mockup, requirements missing from the mockup, extra UI elements not in requirements, conflicts/inconsistencies, and questions or clarifications needed.

## Output Rules

- Use clean Markdown by default. Use CSV, TSV, or spreadsheet-oriented formatting when requested.
- Keep IDs unique and stable. Use a simple pattern such as `TC-<MODULE>-001` unless the provided template uses another pattern.
- Put prerequisites in `Preconditions`, not in the first test step.
- Put concrete values in `Test Data` when helpful.
- Set initial `Status` to `Not Run` unless the user or template specifies another value.
- Use priority and severity consistently:
  - Priority: `High`, `Medium`, `Low`
  - Severity: `Critical`, `Major`, `Minor`, `Trivial`
- Use test types such as `Functional`, `Negative`, `Boundary`, `Validation`, `UI`, `Permission`, `Workflow`, `Integration`, `Regression`, `Usability`, and `Data Persistence`.
- If the user requests a compact live-mockup table or the provided template includes a `Source` column, use source values `Requirement`, `Mockup`, `Requirement + Mockup`, or `Inferred QA Risk`.
- Do not skip edge cases just because they are implicit, but label assumptions clearly when the requirement does not state the rule.
- Do not claim full coverage when requirements are incomplete; describe the coverage limits.
