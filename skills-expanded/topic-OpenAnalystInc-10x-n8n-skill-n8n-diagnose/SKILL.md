---
description: "Diagnose workflow issues — check status, executions, errors, suggest fixes"
argument-hint: "<workflow-id-or-slug> [execution-id]"
allowed-tools: "Read, Bash(curl *), Grep, Glob"
---

CONTEXT: Investigate why a workflow is failing or misbehaving. Chains: /n8n-status + /n8n-execution + /n8n-run-log + /n8n-diff + catalog lookup.

REQUIRES: ~/.claude/n8n-config.json

STEPS:
1. READ config — confirm connected
2. IDENTIFY target: IF slug → read projects/<slug>/meta.json for workflow_id | IF numeric → use as workflow_id

### Gather evidence:
3. GET workflow details: `curl -s -H "X-N8N-API-KEY: <key>" "<baseUrl>/api/v1/workflows/<id>"`
4. GET recent executions: `curl -s -H "X-N8N-API-KEY: <key>" "<baseUrl>/api/v1/executions?workflowId=<id>&limit=10"`
5. IF specific execution-id → GET full execution: `curl -s -H "X-N8N-API-KEY: <key>" "<baseUrl>/api/v1/executions/<exec-id>"`
6. READ local run log: .n8n-track/executions.jsonl filtered by workflow_id
7. IF project exists → READ projects/<slug>/history.jsonl for recent changes

### Analyze:
8. CHECK execution statuses — count: success, failed, waiting, running
9. IF failures exist → extract error message + failing node name from execution data
10. LOOKUP failing node type in docs/nodes/node-catalog.json — check params, credential requirements
11. IF credential error → CHECK cred-map.json → verify cred exists in n8n: GET /api/v1/credentials
12. IF param error → COMPARE node params against catalog spec
13. IF connection error → CHECK workflow connections for orphans or wrong output indices

### Diagnose:
14. DETERMINE root cause category: credential | parameter | connection | external-service | rate-limit | timeout
15. SUGGEST specific fix based on category

OUTPUT:
```
Diagnosis: "<workflow-name>" (ID: <id>)

Health: <count> success / <count> failed (last <n> executions)

Issue: <root cause description>
  Failing node: <node-name> (<type>)
  Error: <exact error message>
  Category: <credential|parameter|connection|external|rate-limit|timeout>

Fix:
  <specific action to take>
  Command: <suggested /n8n-* command to run>
```

RULES:
- Always check the most recent failed execution first
- Cross-reference errors against node-catalog.json before diagnosing
- If credential issue → check .env first, then cred-map, then n8n API
- Never guess — if unclear, show raw error + suggest /n8n-update-docs for the node type

$ARGUMENTS
