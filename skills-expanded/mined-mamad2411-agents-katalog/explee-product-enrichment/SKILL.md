---
name: explee-product-enrichment
description: "Use Explee enrichment APIs to find emails for contacts in single or batch mode and track async task status. USE WHEN a task matches the Craft workspace workflow for explee-product-enrichment."
cluster: explee-master
version: 1.0.0
origin: "craft-agent workspace"
---

# Explee Product Skill — Enrichment

Use this skill for outreach data completion and email finding workflows.

## Authentication

Use API key auth:
- Header: `X-API-Key: <api_key>`
- Base URL: `https://api.explee.com`

```bash
export EXPLEE_API_KEY='<your_api_key>'
```

## Primary Endpoints

- `POST /public/api/v1/enrich/email`
- `POST /public/api/v1/enrich/email/batch`
- `GET /public/api/v1/enrich/email/batch/{task_id}`
- `GET /public/api/v1/tasks`

## Execution Pattern

1. Use single enrichment for quick checks.
2. Use batch for scale (up to documented limits).
3. Poll task endpoint until `completed` or `failed`.
4. Return final structured results and failure reasons.

## Request Templates

### Single Email Enrichment

```bash
curl 'https://api.explee.com/public/api/v1/enrich/email' \
  -X POST \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H "X-API-Key: ${EXPLEE_API_KEY}" \
  --data '{"first_name":"Ada","last_name":"Lovelace","domain":"example.com","mode":"basic"}'
```

### Batch Enrichment Submit

```bash
curl 'https://api.explee.com/public/api/v1/enrich/email/batch' \
  -X POST \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H "X-API-Key: ${EXPLEE_API_KEY}" \
  --data '{"contacts":[{"first_name":"Ada","last_name":"Lovelace","domain":"example.com"}]}'
```

### Batch Result Poll

```bash
curl "https://api.explee.com/public/api/v1/enrich/email/batch/${TASK_ID}" \
  -H 'Accept: application/json' \
  -H "X-API-Key: ${EXPLEE_API_KEY}"
```

## Guardrails

- Confirm mode (`basic` vs `premium`) due to credit differences.
- Never expose raw API key in final output.
- For low match rates, suggest improving names/domain quality.
