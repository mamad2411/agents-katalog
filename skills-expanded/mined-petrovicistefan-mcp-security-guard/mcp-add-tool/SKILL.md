---
name: mcp-add-tool
description: Adds a tool or CLI command to shipped mcp-security-guard (SDK server, confirms, tests, README, changelog). Use when extending audits, Team MCP tools, or analysis surfaces.
---

# Add a tool (mcp-security-guard)

1. Implement logic under `src/` (prefer pure modules + existing finding/`Severity` types, OWASP tags via `owasp.ts`).
2. Wire MCP tool in the server entry (`src/index.ts` / related) with honest description and strict input schema.
3. Dangerous actions: require the same confirm pattern as peers (`confirm_launch`, `confirm_network`, `write`, `i_own_this_server`, …).
4. Team-related: user-facing MCP tools may status/request/report with confirmation; **no** admin approve/revoke/policy-push as tools.
5. Cloud/Team egress: extend `cloud.ts` / `team.ts` contracts only with hash/name/version-class fields; update PRIVACY.md.
6. Tests: vitest. Bench/corpus if detection rules change.
7. Docs: README tools table, CHANGELOG, plugin skill/command if user-facing.

`npm run build && npm test` before claiming done.
