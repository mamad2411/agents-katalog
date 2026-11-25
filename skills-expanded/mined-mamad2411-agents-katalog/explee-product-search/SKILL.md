---
name: explee-product-search
description: "Use Explee Search APIs to find companies and people with natural-language targeting and optional AI scoring. USE WHEN a task matches the Craft workspace workflow for explee-product-search."
cluster: explee-master
version: 1.0.0
origin: "craft-agent workspace"
---

# Explee Product Skill — Search

Use this skill for lead generation, ICP targeting, account research, and people discovery.

## Authentication

Use API key auth (not cookies):
- Header: `X-API-Key: <api_key>`
- Base URL: `https://api.explee.com`

Recommended shell setup:

```bash
export EXPLEE_API_KEY='<your_api_key>'
```

## Primary Endpoints

- `POST /public/api/v1/search/companies`
- `POST /public/api/v1/search/companies-by-domains`
- `POST /public/api/v1/search/people`
- `POST /public/api/v1/search/people-by-domains`
- `POST /public/api/v1/search/nl-to-filters`

## Execution Pattern

1. Start from user goal (ICP, territory, titles, domains).
2. If input is vague, call `nl-to-filters` first.
3. Run one search endpoint with a limited result set.
4. Return concise rows + next-step recommendation.

## Request Templates

### NL to Filters

```bash
curl 'https://api.explee.com/public/api/v1/search/nl-to-filters' \
  -X POST \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H "X-API-Key: ${EXPLEE_API_KEY}" \
  --data '{"definition":"B2B fintech in Europe hiring SDRs"}'
```

### Search Companies

```bash
curl 'https://api.explee.com/public/api/v1/search/companies' \
  -X POST \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H "X-API-Key: ${EXPLEE_API_KEY}" \
  --data '{"definition":"AI SaaS companies in India"}'
```

### Search People

```bash
curl 'https://api.explee.com/public/api/v1/search/people' \
  -X POST \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H "X-API-Key: ${EXPLEE_API_KEY}" \
  --data '{"job_titles":["Head of Marketing"],"company_filters":{"definition":"B2B SaaS"}}'
```

## Guardrails

- Do not run huge searches by default; start narrow.
- Call out credit impact before expensive runs.
- Summarize method, endpoint, and status in outputs.
