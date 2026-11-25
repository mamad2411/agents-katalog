---
name: opsphere-onboarding
description: Get started with Opsphere in Antigravity; discover tools, account and workspace without changing configuration.
---

# Opsphere in Antigravity

Use live MCP discovery, then `ops_my_usage` and `ops_accounts_list` to identify the active workspace and plan. Personal Workspace availability does not mean it is currently selected. Do not expose internal IDs unless diagnosing a mismatch.

If disconnected, read the installed `connect-another-client` skill and its reference. Never copy tokens from another app. Installing a skill does not install or authorize MCP. Complete OAuth in Antigravity after `agy plugin install`. Let Antigravity use its stable CIMD client_id. Do not configure client_id, callback, tokens or secrets.

MCP discovery lists definitions, not permission to execute them. When
`ops_my_usage` reports `catalog.mode: stable`, the visible count stays the same
across workspaces: no refresh or reconnection is needed for a workspace change.
Use workspace availability and `ops_list_integrations` for live configuration;
report unknown status as unknown. Never switch workspace to bypass a denial.

Ask what the user wants to do. For integration setup use `configure-integration`; for provider/account notes use `set-work-context`. For an operational investigation choose the installed incident, endpoint, CI or postmortem skill. A listed tool may still require credentials; respect its live eligibility and errors.

For QA work, use `qa-test-investigation` for a suspected defect and
`qa-release-readiness` for a promotion decision. When `qa_catalog_get` is
available, discover suites through the active workspace SCM integration without
guessing repository names or requiring a manifest. Ask before persisting an
ambiguous source with `qa_source_confirm`; never execute discovered commands.
`READY_WITH_UNCONFIRMED_POLICY` is not an unconditional release approval.

Keep the active workspace unless the user explicitly requests a change. Start with read-only diagnostics; ask before state-changing operations. Do not manually pass or invent a `context_id` for normal operations.

The package supports local Antigravity IDE and CLI. Do not copy OAuth files from another client.
