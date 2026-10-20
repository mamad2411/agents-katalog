# MCP Registry Module

This module owns operator-facing import from MCP Registry-compatible metadata
into KOTA external MCP server configuration.

- Keep this as a config import surface, not a runtime capability registry.
- Decode registry metadata at the boundary, then emit the same strict
  `mcpServers` config shape the core MCP manager already consumes.
- Do not execute, install, or probe registry packages during import.
- Private MCP tunnel support stays an adapter here: validate configured
  provider profiles and target allowlists, then project them to existing
  MCP config/setup surfaces. Do not add a general proxy or a second MCP
  capability catalog.
- The emitted `mcpServers` entry for a tunnel profile is the allowlisted
  private MCP target. Tunnel-client launch metadata belongs in setup and
  diagnostics, not in a stdio MCP server config.
- Tunnel runtime credentials are setup/secrets concerns. Diagnostics may name
  secret references and readiness states, but never print raw credential
  values.
- Keep registry field support and diagnostics in focused source tests rather
  than durable prose catalogs.
