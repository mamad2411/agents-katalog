---
name: notis-mcp
description: Use when an agent accesses Notis through the hosted generic MCP server and needs the discovery, validation, execution, connection, and skill-backed guide workflow.
mcp_resource: true
mcp_tool_patterns: []
---

# Notis MCP

Use this guide when the current agent is connected to the hosted Notis MCP and
does not have shell or Notis CLI access.

## Core workflow

1. Call `notis_list_toolkits` when you need to understand which integrations
   are connected or connectable.
2. Call `notis_search_tools` with a concrete description of the complete task.
   Use returned target tool names exactly.
3. When a result includes `required_resource_uri`, read that MCP Resource
   before constructing the target call. If the client cannot read MCP
   Resources, call `notis_fetch` with the same URI.
4. Call `notis_describe_tools` when the search result is ambiguous or when you
   need the current complete JSON Schema.
5. Call `notis_validate_calls` before execution.
6. Use `notis_execute_read` only for target tools classified with the `read`
   lane. Use `notis_execute_write` only for target tools classified with the
   `write` lane.
7. Give every write call its own stable `idempotency_key`. Reuse that exact key
   only when retrying the same intended mutation.

Notis classifies effects server-side. Never infer that a target tool is
read-only from its name.

## Skill-backed operating guides

Notis publishes complex operating contracts as `notis://docs/*` MCP Resources.
The content is generated directly from the canonical Notis skills, so the
resource changes whenever its owning skill changes.

The most important guides are:

- `notis://docs/notis-query` for structured native-database queries and
  generated database upserts
- `notis://docs/notis-automation` for reminder and automation mutations
- `notis://docs/notis-apps` for explicit Store app installation
- `notis://docs/notis-cli` when comparing the generic MCP workflow with the
  local CLI workflow

Prefer the URI returned with the selected tool instead of guessing which guide
applies.

## Connections

If the required cloud toolkit is not connected, call
`notis_connect_toolkit`. Return the authorization URL to the user and wait for
them to finish the provider flow before retrying discovery.

Local desktop MCP servers, credentials, shell tools, and desktop controls
cannot be configured through hosted MCP. The complete Your Computer bundle,
including Local MCP, is available on every plan, including Free; configure it
through Notis Desktop before using it from a local-capable agent surface.

## Safety boundaries

- Validate every mutation before executing it.
- Do not invent target tool names or arguments.
- Do not place secrets in search queries or tool arguments unless the target
  tool explicitly requires the secret.
- Treat returned cursors and identifiers as opaque.
- Respect the server-returned execution lane and cloud-support status.
- Local app source/build/deployment commands, local files, local shell,
  debugging overrides, and credential retrieval are intentionally unavailable
  through hosted MCP. Native Store and app-management tools follow the
  server-returned surface and PostHog visibility policy.
- Skill administration is available on every plan, including Free. Individual
  curated skills can still declare additional paid entitlements; when one does,
  its install or execution returns the canonical upgrade-required result.
