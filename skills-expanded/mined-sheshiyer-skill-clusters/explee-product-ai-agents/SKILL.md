---
name: explee-product-ai-agents
description: "Run Explee pre-built and custom AI agents, then poll run status and return structured outputs. USE WHEN a task matches the Craft workspace workflow for explee-product-ai-agents."
cluster: explee-master
version: 1.0.0
origin: "craft-agent workspace"
---

# Explee Product Skill — AI Agents

Use this skill for extraction, reasoning, and automation tasks powered by Explee Agents.

## Authentication

Use API key auth:
- Header: `X-API-Key: <api_key>`
- Base URL: `https://api.explee.com`

```bash
export EXPLEE_API_KEY='<your_api_key>'
```

## Primary Endpoints

- `GET /public/api/v1/agents`
- `POST /public/api/v1/agents/{agent_id}/runs`
- `POST /public/api/v1/agents/runs`
- `GET /public/api/v1/agents/runs/{run_id}`

## Execution Pattern

1. List available agents and inspect input schema.
2. Choose pre-built agent if available; otherwise run custom agent.
3. Submit run with minimal valid input.
4. Poll until completion, then return normalized result.

## Request Templates

### List Agents

```bash
curl 'https://api.explee.com/public/api/v1/agents' \
  -H 'Accept: application/json' \
  -H "X-API-Key: ${EXPLEE_API_KEY}"
```

### Run Pre-built Agent

```bash
curl 'https://api.explee.com/public/api/v1/agents/<agent_id>/runs' \
  -X POST \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H "X-API-Key: ${EXPLEE_API_KEY}" \
  --data '{"input":{}}'
```

### Poll Agent Run

```bash
curl "https://api.explee.com/public/api/v1/agents/runs/${RUN_ID}" \
  -H 'Accept: application/json' \
  -H "X-API-Key: ${EXPLEE_API_KEY}"
```

## Guardrails

- Validate payload against returned `input_schema` before run.
- For custom agents, keep system prompts concise and deterministic.
- Always report run status lifecycle (`pending` → `completed`/`failed`).
