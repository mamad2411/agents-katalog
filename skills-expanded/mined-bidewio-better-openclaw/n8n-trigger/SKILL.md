---
name: n8n-trigger
description: "Trigger automation workflows, manage webhooks, and orchestrate multi-step tasks via the n8n instance at {{N8N_HOST}}:{{N8N_PORT}}."
metadata:
  openclaw:
    emoji: "⚡"
---

# n8n Trigger Skill

n8n workflow automation is available at `http://{{N8N_HOST}}:{{N8N_PORT}}` within the Docker network.

## Triggering a Webhook

Fire a webhook to start a pre-configured workflow:

```bash
# POST with JSON payload
curl -X POST "http://{{N8N_HOST}}:{{N8N_PORT}}/webhook/openclaw-trigger" \
  -H "Content-Type: application/json" \
  -d '{
    "event": "file_processed",
    "file": "/data/output/result.csv",
    "timestamp": "2025-01-15T10:30:00Z"
  }'

# GET webhook with query parameters
curl "http://{{N8N_HOST}}:{{N8N_PORT}}/webhook/openclaw-status?task_id=abc123"
```

## Triggering a Test Webhook

During workflow development, use the test webhook endpoint:

```bash
curl -X POST "http://{{N8N_HOST}}:{{N8N_PORT}}/webhook-test/openclaw-trigger" \
  -H "Content-Type: application/json" \
  -d '{"test": true, "message": "Hello from OpenClaw"}'
```

## Listing Workflows

Retrieve all workflows via the n8n REST API:

```bash
curl -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "http://{{N8N_HOST}}:{{N8N_PORT}}/api/v1/workflows"
```

## Activating / Deactivating a Workflow

```bash
# Activate workflow by ID
curl -X PATCH "http://{{N8N_HOST}}:{{N8N_PORT}}/api/v1/workflows/1" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"active": true}'

# Deactivate
curl -X PATCH "http://{{N8N_HOST}}:{{N8N_PORT}}/api/v1/workflows/1" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"active": false}'
```

## Getting Workflow Executions

Check the status and output of past workflow runs:

```bash
curl -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "http://{{N8N_HOST}}:{{N8N_PORT}}/api/v1/executions?workflowId=1&limit=10"
```

## Creating a Workflow via API

```bash
curl -X POST "http://{{N8N_HOST}}:{{N8N_PORT}}/api/v1/workflows" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "OpenClaw Data Pipeline",
    "active": false,
    "nodes": [
      {
        "parameters": { "httpMethod": "POST", "path": "openclaw-pipeline" },
        "name": "Webhook",
        "type": "n8n-nodes-base.webhook",
        "typeVersion": 1,
        "position": [250, 300]
      }
    ],
    "connections": {}
  }'
```

## Webhook Naming Conventions

- `openclaw-trigger` — general purpose task trigger
- `openclaw-pipeline` — data processing pipeline entry
- `openclaw-notify` — notification dispatch
- `openclaw-schedule` — scheduled task callbacks

## Tips for AI Agents

- Prefer webhook triggers over polling for real-time task orchestration.
- Always validate that the target workflow is **active** before sending webhook requests; inactive workflows will silently drop events.
- Include a `timestamp` and unique `event_id` in every webhook payload for traceability.
- Use the n8n API (`/api/v1/`) for programmatic workflow management; use webhooks (`/webhook/`) for event-driven triggers.
- Check n8n health at `http://{{N8N_HOST}}:{{N8N_PORT}}/healthz`.
- Store the `$N8N_API_KEY` in the `.env` file, never hard-code it.
