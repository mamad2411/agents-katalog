---
name: n8n-mcp-tools-expert
description: Expert guide for using n8n-mcp MCP tools effectively. Use when searching for nodes, validating configurations, accessing templates, managing workflows, or using any n8n-mcp tool. Provides tool selection guidance, parameter formats, and common patterns.
---
# n8n MCP Tools Expert

Master guide for using n8n-mcp MCP server tools to build, validate, and manage n8n workflows.

## Tool Categories

1. **Node discovery** → `SEARCH_GUIDE.md`
2. **Configuration validation** → `VALIDATION_GUIDE.md`
3. **Workflow management** → `WORKFLOW_GUIDE.md`
4. **Template library** → `search_templates`, `get_template`, `n8n_deploy_template`
5. **Data tables** → `n8n_manage_datatable`
6. **Documentation and guides** → `tools_documentation`, `ai_agents_guide`, Code node guides

## Fast Path

1. Search: `search_nodes({query: "keyword"})`
2. Inspect: `get_node({nodeType: "nodes-base.name"})`
3. Validate: `validate_node({nodeType, config, profile: "runtime"})`
4. Create or edit workflow.
5. Validate workflow.
6. Iterate with `n8n_update_partial_workflow`.
7. Activate only after validation passes.

## Most Used Tools

| Tool | Use When |
|---|---|
| `search_nodes` | Find nodes by keyword |
| `get_node` | Understand operations/properties; default `detail="standard"` |
| `validate_node` | Check one node config; use `profile="runtime"` |
| `n8n_create_workflow` | Create an initial workflow |
| `n8n_update_partial_workflow` | Iteratively edit workflows; preferred for changes |
| `validate_workflow` / `n8n_validate_workflow` | Check complete workflows |
| `n8n_deploy_template` | Deploy a template to an n8n instance |
| `n8n_manage_datatable` | CRUD for n8n data tables and rows |
| `n8n_autofix_workflow` | Auto-fix validation errors |

## Critical nodeType Formats

Use short prefixes for search/inspect/validation tools:

```javascript
"nodes-base.slack"
"nodes-base.httpRequest"
"nodes-langchain.agent"
```

Use full prefixes inside workflow JSON/tools:

```javascript
"n8n-nodes-base.slack"
"n8n-nodes-base.httpRequest"
"@n8n/n8n-nodes-langchain.agent"
```

`search_nodes` returns both `nodeType` and `workflowNodeType`; use the correct one for the target tool.

## Safety and Efficiency Rules

- Use `get_node` with default/standard detail for most cases; `detail="full"` is a last resort.
- Always set validation profiles explicitly; prefer `profile="runtime"` before deployment.
- Use smart connection parameters such as `branch` and `case` instead of manual `sourceIndex` when available.
- Include an `intent` on workflow updates so tool responses are more useful.
- Expect auto-sanitization on workflow updates; it can fix common node structure issues but not broken connections or paradoxical states.
- Build workflows iteratively rather than one large update.
- Validate after every meaningful change and before activation.

## Tool Availability

Always available without n8n API credentials:

- `search_nodes`, `get_node`
- `validate_node`, `validate_workflow`
- `search_templates`, `get_template`
- `tools_documentation`, `ai_agents_guide`

Requires `N8N_API_URL` and `N8N_API_KEY`:

- workflow create/update/list/get/delete/test/executions/version tools
- `n8n_validate_workflow` by ID
- `n8n_deploy_template`
- `n8n_autofix_workflow`
- `n8n_manage_datatable`

If API tools are unavailable, use templates and validation-only workflows.

## Detailed References

- `SEARCH_GUIDE.md` — node discovery, detail levels, docs mode, property search, versions.
- `VALIDATION_GUIDE.md` — validation profiles, validation structure, auto-sanitization, error handling.
- `WORKFLOW_GUIDE.md` — create/update workflow operations, smart parameters, AI connections, activation, versions.
- `references/tool-patterns.md` — common mistakes, detailed examples, templates, data table management, self-help tools, unified tool reference, performance, and best practices.

## Summary

Most successful n8n-mcp work follows this loop: search → inspect → validate node → create workflow → validate workflow → partial update → validate again → activate. Keep payloads small, use the correct nodeType format, and use references only when the task needs details.

**Related Skills:** n8n Expression Syntax, n8n Workflow Patterns, n8n Validation Expert, n8n Node Configuration, n8n Code JavaScript, and n8n Code Python.
