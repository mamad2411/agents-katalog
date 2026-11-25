---
name: n8n-workflow-tester
description: Test, score, and inspect n8n workflows via MCP. Safe by design — no credential access, no destructive auto-repair. Use when testing workflows, debugging executions, searching nodes, or building workflows incrementally.
triggers:
  - test workflow
  - workflow score
  - execution trace
  - debug n8n
  - search n8n nodes
  - suggest nodes
  - workflow suite
  - n8n execution
  - validate node
  - workflow tester
---

# n8n Workflow Tester — MCP Skill

Safe MCP server for testing, scoring, and inspecting n8n workflows. Deliberately excludes credential management and autonomous auto-repair to minimize risk surface.

## When to Use

- Testing a workflow with specific payloads
- Debugging failed executions (trace per-node data flow)
- Searching for the right n8n node type for a task
- Building workflows incrementally (add node, connect, test)
- Validating node types exist before adding them
- Running full test suites against workflow configs
- Checking execution history and status

## Tool Selection Guide

### Testing (validate workflow behavior)

| Tool | When | Example |
|------|------|---------|
| `test_workflow` | Run a single payload against a workflow | `configPath: "workflows/api-pipeline.json", payloadName: "happy-path"` |
| `evaluate_workflow_result` | Run + get scored result with issues | Same params — returns score breakdown |
| `run_workflow_suite` | Run ALL payloads in a config | `configPath: "workflows/telegram-bot.json"` |

### Workflow Operations (build and modify)

| Tool | When | Example |
|------|------|---------|
| `create_workflow` | Create new workflow from JSON | `workflow: { name: "Test", nodes: [...], connections: {...} }` |
| `update_workflow` | Replace entire workflow JSON | `workflowId: "abc123", workflow: { ... }` |
| `delete_workflow` | Remove a workflow | `workflowId: "abc123"` |
| `add_node_to_workflow` | Append a single node | `workflowId: "abc123", node: { type: "n8n-nodes-base.httpRequest", ... }` |
| `connect_nodes` | Wire two nodes together | `workflowId: "abc123", source: "HTTP Request", target: "Set"` |

### Introspection (debug and inspect)

| Tool | When | Example |
|------|------|---------|
| `get_workflow_summary` | Quick overview of a workflow | `workflowId: "zs8ZpR4wpOlvbAeC"` |
| `list_executions` | See recent runs, filter by status | `workflowId: "abc", status: "error", limit: 5` |
| `get_execution` | Full execution details | `executionId: "12345"` |
| `get_execution_trace` | Lightweight per-node trace | `executionId: "12345"` — best for debugging data flow |

### Catalog (find and validate nodes)

| Tool | When | Example |
|------|------|---------|
| `search_nodes` | Find nodes by name | `query: "telegram"` |
| `list_node_types` | List ALL available node types | No params |
| `list_triggers` | List only trigger nodes | No params |
| `get_node_type` | Full schema for a node type | `nodeType: "n8n-nodes-base.httpRequest"` |
| `validate_node_type` | Check if a node type exists + suggest alternatives | `nodeType: "n8n-nodes-base.telegramApi"` |
| `suggest_nodes_for_task` | Natural language node suggestions | `task: "send a message to Telegram with an image"` |
| `get_catalog_stats` | Catalog overview (counts) | No params |

## Scoring Model

Tests use a two-tier scoring system:

- **Tier 1 (70% weight)**: Infrastructure — HTTP success, no timeout, non-empty output. Must be 100 to pass.
- **Tier 3 (30% weight)**: Quality — custom field validation, length constraints, data checks.
- **Pass condition**: Tier 1 = 100 AND final score >= quality threshold.

## Workflow Config Format

Test configs are JSON files in `workflows/`:

```json
{
  "workflowId": "zs8ZpR4wpOlvbAeC",
  "description": "SynthVault content engine",
  "payloads": {
    "happy-path": {
      "body": { "day": 1 },
      "checks": [
        { "field": "caption", "operator": "exists" },
        { "field": "hashtags", "operator": "minLength", "value": 3 }
      ]
    },
    "edge-case-day-57": {
      "body": { "day": 57 },
      "checks": [
        { "field": "source", "operator": "equals", "value": "gemini" }
      ]
    }
  }
}
```

## Common Workflows

### Debug a failing execution
1. `list_executions` with `status: "error"` to find the failing run
2. `get_execution_trace` to see per-node data flow
3. Identify the broken node from the trace
4. Fix and `update_workflow` or `add_node_to_workflow`
5. `test_workflow` to verify the fix

### Build a workflow incrementally
1. `suggest_nodes_for_task` to find the right nodes
2. `validate_node_type` to confirm they exist
3. `create_workflow` with initial structure
4. `add_node_to_workflow` + `connect_nodes` to extend
5. `run_workflow_suite` to test all scenarios

### Validate before deploying
1. Write a config JSON with payloads and checks
2. `run_workflow_suite` to test all payloads
3. Review scores — Tier 1 must be 100, overall above threshold
4. Fix any issues and re-test

## Safety Boundaries

**Included**: workflow CRUD, node management, execution inspection, catalog search.

**Excluded by design**: credential management, secrets lifecycle, destructive restore, autonomous repair loops.

## Prerequisites

- n8n instance running and accessible
- `N8N_BASE_URL` and `N8N_API_KEY` configured
- MCP server running (`node dist/index.js`)
