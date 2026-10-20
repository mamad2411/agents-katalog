---
name: xyops-automate
description: "Build and manage automation pipelines using xyOps at {{XYOPS_HOST}}:{{XYOPS_PORT}}."
metadata:
  openclaw:
    emoji: "🔧"
---

# xyOps Automation

xyOps is available at `http://{{XYOPS_HOST}}:{{XYOPS_PORT}}` within the Docker network.

## List Pipelines

```bash
curl -X GET "http://{{XYOPS_HOST}}:{{XYOPS_PORT}}/api/v1/pipelines" \
  -H "Authorization: Bearer $XYOPS_API_KEY"
```

## Trigger Pipeline

```bash
curl -X POST "http://{{XYOPS_HOST}}:{{XYOPS_PORT}}/api/v1/pipelines/{id}/run" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $XYOPS_API_KEY" \
  -d '{"inputs": {"key": "value"}}'
```

## Tips for AI Agents

- xyOps supports event-driven and scheduled pipeline execution.
- Chain multiple steps with conditional logic and error handling.
