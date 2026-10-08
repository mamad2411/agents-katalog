---
name: gstack-qa-only
description: Read-only QA report for an OPC desktop flow, CLI command, local URL, staging URL, or documented user journey. Does not modify code.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# gstack-qa-only

Use this skill to test behavior and report bugs without changing files.

## Workflow

1. Define the target flow, environment, and success criteria.
2. Run the app, command, or URL using the existing project workflow.
3. Exercise the primary path and at least two edge paths.
4. Capture objective evidence: command output, logs, screenshots if available, request/response details, or UI text.
5. Separate product bugs from setup failures.

## OPC Checks

When testing OPC desktop, prefer:

- `npm --prefix desktop test`
- `./script/build_and_run.sh --verify`
- provider bridge health and `/models` behavior when relevant
- installed app behavior when the issue concerns `/Applications/OPC.app`

## Output

Return a QA report:

- Environment
- Tested flow
- Pass/fail summary
- Bugs with reproduction steps
- Evidence
- Suggested regression coverage

Do not edit code in this workflow.
