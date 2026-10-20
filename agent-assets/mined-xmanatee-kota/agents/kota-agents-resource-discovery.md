# Resource Discovery Module

This module owns KOTA's agentic resource discovery surface.

- Discover from existing runtime/module metadata, setup status, tool definitions,
  skill-ops skill summaries, MCP config metadata, knowledge provider results,
  and recall hits.
- Do not maintain a hand-authored capability catalog here.
- Discovery is advisory and read-only. It may point to tools, setup flows, or
  modules, but it must not execute tools, satisfy setup, connect MCP servers,
  or probe external packages.
- Keep the CLI, HTTP routes, and agent tool backed by the same provider and
  typed result shape.
- Redact or omit secret-bearing setup and connector values. Surface metadata,
  readiness, and access paths instead of raw credentials or private payloads.
