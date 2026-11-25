# Jarela Integrations

Use this skill when the user wants to add, configure, debug, or extend an
integration in Jarela.

## Choose The Integration Path

1. Native/built-in integration: use the existing manifest and typed tools.
2. External LLM provider: add a `.cjs` provider plugin under the configured
   providers directory.
3. External tool: add a `.cjs` tool under the configured tools directory.
4. MCP server: configure a stdio or HTTP MCP server.
5. Built-in code integration: add an in-tree package/tool/provider when the
   integration should ship with Jarela.

Call `describe_extension_surfaces` when unsure which path fits.

## Setup Flow For Users

1. Call `list_integrations` to see configured and available integrations.
2. Call `get_integration_setup(id)` for the chosen integration.
3. Walk the user through prerequisites and credential fields.
4. Use `propose_config_change` for setup actions that require approval.
5. Never put API keys, OAuth tokens, client secrets, passwords, or private keys
   in proposal payloads or chat text.
6. After approval, run the relevant test/probe tool or integration test endpoint
   if available.

## Adding A Built-In Integration

- Add or update the manifest under `lib/integrations/`.
- Add typed tools under `lib/tools/` or a package under `packages/` and register
  with `registerLangChainPackage`.
- Add the side-effect import in `lib/tools/builtins.ts` when adding a new built-in
  tool module.
- Gate network/external-resource tools behind credentials or capability checks.
- Add tests for the manifest, credential probe path, and at least one happy-path
  tool invocation or mocked adapter call.
- Document the setup path in user-facing docs when the integration needs manual
  external configuration.

## Debug Checklist

- Is the credential row present and configured?
- Does `list_tools` show the expected tool name?
- Is the tool category disabled?
- Is the MCP server enabled and connected?
- Does the integration probe fail with auth, network/proxy, missing scope, or
  provider-specific validation?
- Are multiple credentials configured, and does the agent/tool have the intended
  credential override?

## Preferred Agent Behavior

- Prefer typed Jarela tools over shell CLIs like `gh`, `jira`, or `aws` when a
  typed integration is configured.
- Be explicit about whether an action is local setup, vendor setup, OAuth
  consent, or a Jarela approval.
- Validate after saving credentials or changing integration configuration.
