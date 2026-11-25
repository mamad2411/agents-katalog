---
description: Diagnose and fix a failing Hatchable deploy or a broken deployed app. Use when a Hatchable deploy is rejected, a deployed app errors, or the user reports their Hatchable app is broken.
---

# Fix a Hatchable deploy

Investigate and fix: $ARGUMENTS

Use the Hatchable MCP tools (the `hatchable` server bundled with this plugin). If the first tool call returns an authentication error, stop and tell the user: run `/mcp`, pick **hatchable**, sign in, then ask again. Do not guess at the cause from memory when the platform can tell you the answer.

Work the problem in this order:

1. Identify the project (`list_projects` / `search_projects` if the user didn't name one).
2. **Rejected deploy:** run `dry_run_deploy` and read every error. Each names the unsupported pattern and its supported replacement. Call `read_skill('debug-a-failing-deploy')` for the canonical triage path.
3. **Deployed but broken:** `view_logs` for runtime errors, `get_deployment` for the last deploy's status, `get_schema` plus `execute_sql` to check data-shape assumptions.
4. Fix with `patch_file` or `write_files`, then `dry_run_deploy`, then `deploy`.
5. Verify against the live URL before declaring it fixed, and summarize the root cause in one line.

Never work around a validator by restructuring to sneak a rejected dependency through; the rejection list is the platform contract, and each error points at the supported way.
