---
name: zihin-tools-de-agente
description: Use this guide when adding external API or MCP capabilities to a Zihin agent, configuring authentication, validating tools or restricting their availability.
---

# Configure agent tools

Read `zihin://schemas/api_config` before building an API tool. Validate the payload with
`validate_schema_data`, create the schema and confirm the tool resolves in `list_agent_tools`.

- `editor_schema.api.endpoints[].name` must match `tool_definition.name`.
- Path parameters use `${parameter_name}` and must be declared in the input schema.
- Store credentials with tenant secret tools and reference them using `secret_ref`.
  Use the authentication shape in the current schema; do not put secrets in descriptions.
- Describe the operation and return value clearly. Prefer one operation per API schema.
- Set the API timeout through `editor_schema.api.timeout_ms`. For external MCP tools,
  use `config.call_timeout_ms`; connection timeout and call timeout are different settings.

Register external MCP endpoints with `create_mcp_server`. Use `test_mcp_server` to check
connectivity and authentication. After changing available tools, call `invalidate_mcp_cache`
and inspect `list_agent_tools` again.

To restrict tools for one agent, use a behavior CSP with `rules.must_not_tools`. Use the
exact resolved tool name, including the server prefix for an external MCP tool. Review
warnings for names outside the current surface. `update_csp` replaces the rules object,
so include the fields that must remain. Verify the effective configuration afterward.

Perform a real agent test only when authorized by the task: it can consume credits and
perform the external operation. A successful validation is not a substitute for checking
authentication, permissions and the external system's result.
