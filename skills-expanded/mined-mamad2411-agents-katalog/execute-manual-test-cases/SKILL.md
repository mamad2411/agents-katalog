---
name: execute-manual-test-cases
description: Execute manual QA test cases from a named test case file using project setup, environment, or context files named in the prompt. Use when the user asks to run manual test cases, validate a feature manually, perform UAT/sanity/regression execution from a document, or report pass/fail/blocked results with evidence.
---

# Execute Manual Test Cases

## Required References

Before executing any manual test case, read the exact files named by the user:

1. The manual test case file, such as Markdown, CSV, spreadsheet, document, or plain text.
2. The project context or setup file named in the prompt, such as README, environment notes, QA setup, API docs, user-flow docs, deployment notes, or feature documentation.
3. Any referenced sample data, fixture, account instructions, endpoint docs, or prerequisite files needed to execute the cases safely.

If the prompt does not identify a test case file, ask for one. If the prompt identifies test cases but no setup context, look for project-standard setup docs first. If the target environment, app URL, credentials, or required test data are still unclear, mark affected cases `Blocked` and state the missing requirement instead of inventing it.

## Execution Modes

Select the execution approach from the test case and setup context:

- `ui`: Execute through the browser or available UI automation/browser tools.
- `api`: Execute through documented API requests using safe local or test endpoints.
- `cli`: Execute through project commands or scripts described by the setup context.
- `document-only`: Review expected behavior against available evidence when execution is impossible, and clearly mark cases as not executed.

Use the mode implied by each test case. Do not convert manual cases into automated tests unless the user explicitly asks for automation.

## Workflow

1. Read the manual test case file and identify case IDs, titles, preconditions, test data, steps, expected results, priority, and execution notes.
2. Read the named project setup/context files and identify the target environment, startup commands, URLs, accounts, seed data, feature flags, browser/device requirements, and safety constraints.
3. Prepare execution only within the requested environment. Start local services only when the setup context requires it and the command is safe for the workspace.
4. Execute each test case step by step, following the documented steps rather than optimizing or skipping ahead.
5. Capture actual results, observed behavior, evidence references, logs, screenshots, response excerpts, or command outputs when available.
6. Assign a result for each case: `Pass`, `Fail`, `Blocked`, or `Not Run`.
7. For failures, include concise reproduction detail, expected versus actual behavior, affected step, and likely evidence source.
8. For blocked cases, include the missing environment, data, access, dependency, or clarification needed.
9. Summarize totals, high-risk failures, environment details, and residual risks.

## Boundaries

- Do not claim a manual test passed unless the steps were actually executed and the expected result was observed.
- Do not expose secrets, passwords, tokens, private user data, or sensitive provider responses in the report.
- Do not run destructive, production, migration, payment, email/SMS, or irreversible actions without explicit approval.
- Do not use production systems unless the user explicitly names production and approves the risk.
- Do not alter test cases, requirements, or setup docs unless the user asks for updates.
- Do not silently skip steps. Mark them `Blocked` or `Not Run` with a reason.

## Output

- Test case file and setup/context files inspected.
- Environment or execution target used.
- Per-case result table with ID, title, status, actual result, evidence, and notes.
- Failure details with expected versus actual behavior.
- Blockers, assumptions, skipped cases, and recommended follow-up.
