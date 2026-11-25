---
name: exploratory-testgen
description: Use this skill whenever the user asks for exploratory functional testing, browser-based discovery, UI flow validation, fast health checks before automation, or a test plan proposal for a frontend. This skill performs non-invasive discovery, proposes a plan for approval, executes approved exploratory flows with Playwright (Chrome preferred, Chromium fallback), captures flow evidence screenshots, and writes a final report in docs/testing. Trigger it for rapid product health checks before formal automation.
allowed-tools: Bash(playwright-cli:*)
---

# ExploratoryTestGen

Purpose: run project-agnostic exploratory functional testing with evidence, without changing source code or infrastructure.

## Code Modification Guardrail

- Never modify application code under test (frontend or backend source code).
- In on-the-fly mode, do not edit project code files; only generate runtime evidence artifacts.
- In test-code mode, only create or modify Playwright testing code and related testing artifacts.
- Allowed edits in test-code mode are limited to Playwright test files, test fixtures/page objects, Playwright config, and testing evidence docs.
- Do not modify product implementation files (for example: app source, backend source, infrastructure, database scripts, or business logic modules).

Execution reference (bundled in this skill): [references/exploratory-plan.md](references/exploratory-plan.md)

## Activation Checklist

Before execution, confirm:
- Project root to assess.
- Target URL (local, staging, or controlled production).
- Standard frontend port and readiness endpoint for preflight (for example, 3000 and `/`).
- Optional frontend start command to use only if preflight fails.
- Non-sensitive test credentials or profiles.
- User restrictions (what to include or exclude).
- Output path for the report (default: docs/testing).
- Browser policy: launch with Playwright using an external Chrome window first (maximizable), then fallback to external Chromium if Chrome is not available.

## Operating Principles

- Be project-agnostic.
- Base all findings on observable evidence.
- Never perform destructive or code-changing actions.
- Do not use embedded browser tooling from the editor for execution; use Playwright CLI in a separate browser window.
- Do not execute tests until the user approves the proposed plan.
- Always end with a final report in docs/testing.
- Keep execution reproducible in Playwright steps, even if discovery starts from interactive commands.
- Keep all screenshots inside the report output directory. Do not write screenshots outside the chosen output path.
- For user-facing updates, use direct and concrete language focused on functional impact and UX clarity.
- Avoid unnecessary implementation details in user-facing feedback (for example, browser engine details) unless explicitly requested.

## Required Workflow

### Phase 1: Functional Discovery (no tests yet)

Goal: build a minimal functional map to avoid blind testing.

Actions:
- Inspect frontend entry point and navigation structure.
- Identify main modules or screens.
- Detect access rules: roles, permission barriers, authentication states.
- Identify critical dependencies: API calls, client storage, notifications, network behavior.
- Assess locator stability coverage: data-testid, aria attributes, labels, ids.

Output:
- Preliminary functional map with high-impact risk areas.

### Phase 2: Test Plan for Approval

Goal: produce a clear execution plan before opening browser testing loops.

Plan must include:
- Functional scope.
- Ordered flows.
- Positive and negative cases per flow.
- Observable pass/fail criteria.
- Evidence to collect (screenshots, messages, state transitions, HTTP errors).
- Known risks (fragile locators, responsive menus, asynchronous flows).
- Report artifact naming rule using flow + timestamp (for example: exploratory-login-20260729-153010.md).

Rule:
- Stop and request explicit user approval before execution.

### Phase 3: Exploratory Execution

Goal: execute all approved flows and validate real behavior.

Preflight before opening the browser:
- Validate if the target frontend is already reachable at the expected URL/port.
- If reachable, do not run any start command and proceed directly to exploration.
- If unreachable, attempt to start the frontend only when a user-approved start command is available.
- Re-check readiness after startup attempt; if still unreachable, stop and report blocker with evidence.

Execution guidelines:
- Use Playwright CLI to launch browser contexts in an external window. Browser policy is: external Chrome preferred, external Chromium fallback.
- Prioritize realistic user interactions.
- Validate visible UI state transitions.
- Record functional errors and degradations.
- Retry actions only with evidence of sync or viewport issues.
- Document expected vs observed state mismatches.

Screenshot evidence policy:
- Capture screenshots with flexible density by flow complexity.
- For simple flows, capture at least start and final state.
- For complex flows, add transition and error-state captures when relevant.
- Store screenshots only under output path, using this structure:
	- Report file: <output-path>/exploratory-<flow-or-scope>-<timestamp>.md
	- Screenshots: <output-path>/screenshots/<flow-id>/<step-or-state>.png
- Render screenshots inline in the report body using Markdown images with relative paths, so evidence is visible without navigating to links.
- Optional textual links can be added, but never as the only evidence format.

### Phase 4: Findings and Non-invasive Recommendations

Goal: convert observations into actionable guidance without touching code.

Allowed:
- Suggest stable selectors.
- Suggest accessibility improvements that increase automability.
- Suggest functional observability improvements.

Forbidden:
- Editing files.
- Implementing selectors.
- Creating pull requests.
- Running destructive commands.

### Phase 5: Final Report

Goal: produce a trackable artifact in docs/testing.

Artifact requirements:
- Report file must use flow + timestamp naming.
- Report and screenshots must be in the same output root.
- Every executed flow must have at least one inline screenshot evidence block.

Required report structure:
1. Executive summary.
2. Approved context and scope.
3. Environment and assumptions.
4. Executed flows.
5. Flow-by-flow result (OK, Partial, Blocked).
6. Key evidence.
7. Flow evidence gallery (with relative screenshot links per flow).
8. Prioritized findings (High, Medium, Low).
9. Non-invasive recommendations.
10. Residual risks and next steps.

## Functional Coverage Model

Try to cover:
- Access and session.
- Primary navigation.
- Main create/edit business workflow.
- List/detail workflow.
- Relevant state transitions.
- User feedback and notifications.
- Expected error paths (auth, permissions, validations, conflicts, timeout).
- Basic responsive behavior and minimum functional accessibility.

## Completion Criteria

Execution is complete only when:
- User approved a plan.
- All approved flows were executed.
- Evidence and results are documented.
- Non-invasive recommendations are provided.
- Report was generated in docs/testing (or configured output path).
- Screenshot files exist inside the report output directory and are embedded inline in the report.
- No screenshot link points outside the report output directory.

## Task References

| Task | Reference |
|---|---|
| Inspect element attributes and generate stable locators | [references/element-attributes.md](references/element-attributes.md) |
| Exploration runbook and command sequence | [references/exploration.md](references/exploration.md) |
| Locator stability assessment and anti-patterns | [references/locators.md](references/locators.md) |
| Named browser sessions for isolated exploration | [references/session-management.md](references/session-management.md) |
| Test credentials and storage state management | [references/storage-state.md](references/storage-state.md) |
