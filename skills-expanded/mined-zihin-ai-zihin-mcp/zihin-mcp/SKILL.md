---
name: zihin-mcp
description: Use this guide when starting work with the Zihin MCP server to discover account permissions, current schemas and the appropriate task-specific guide.
---

# Work with Zihin MCP

Start with `whoami` to confirm the account and role. Available tools reflect the key's
permissions. Discover identifiers with list tools; do not invent UUIDs or model names.

Before writing structured data, read `zihin://schemas/{type}` and the selected tool's
input schema. Entity schemas describe full records; supply only fields accepted by the
tool. Use `validate_schema_data` where supported, then inspect the result and warnings.
Treat `success: false` as a failed operation. A successful write can still return warnings
that must be addressed before publication.

Choose the relevant guide:
- Agent creation: `zihin://skills/criar-agente`.
- API and MCP tools: `zihin://skills/tools-de-agente`.
- Automation and channels: `zihin://skills/triggers-e-canais`.
- Troubleshooting: `zihin://skills/diagnostico`.
- Budgets, policies and human intervention: `zihin://skills/governanca-e-operacao`.

`chat_with_agent` and `test_trigger` execute real work and can consume credits or produce
external effects. Match these actions to the user's request. Keep credentials in tenant
secrets and configuration, never in prompts or skill text.
