---
name: explee-product-autogtm
description: "Orchestrate an end-to-end AutoGTM flow: ICP query → account/person discovery → enrichment → prioritized outreach list. USE WHEN a task matches the Craft workspace workflow for explee-product-autogtm."
cluster: explee-master
version: 1.0.0
origin: "craft-agent workspace"
---

# Explee Product Skill — AutoGTM

Use this skill for full-funnel go-to-market automation using Explee APIs.

## Objective

Produce a prioritized outreach-ready list from a natural-language GTM objective.

## Authentication

Use API key auth:
- Header: `X-API-Key: <api_key>`
- Base URL: `https://api.explee.com`

```bash
export EXPLEE_API_KEY='<your_api_key>'
```

## AutoGTM Workflow

1. **Translate ICP to filters**
   - Endpoint: `POST /public/api/v1/search/nl-to-filters`
2. **Find target accounts and decision-makers**
   - Endpoints:
     - `POST /public/api/v1/search/companies`
     - `POST /public/api/v1/search/people`
3. **Enrich contactability**
   - Endpoint: `POST /public/api/v1/enrich/email` or batch variant
4. **Rank for activation**
   - Prioritize by title relevance, company fit score, and enrichment success
5. **Return GTM-ready output**
   - Include: company, person, title, email status, priority tier, reasoning

## Request Template Blocks

### Step 1: ICP to filters

```bash
curl 'https://api.explee.com/public/api/v1/search/nl-to-filters' \
  -X POST \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H "X-API-Key: ${EXPLEE_API_KEY}" \
  --data '{"definition":"US B2B SaaS, 50-500 employees, hiring RevOps"}'
```

### Step 2: People search

```bash
curl 'https://api.explee.com/public/api/v1/search/people' \
  -X POST \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H "X-API-Key: ${EXPLEE_API_KEY}" \
  --data '{"job_titles":["VP Revenue Operations","Head of RevOps"],"company_filters":{"definition":"US B2B SaaS"}}'
```

### Step 3: Single enrichment example

```bash
curl 'https://api.explee.com/public/api/v1/enrich/email' \
  -X POST \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H "X-API-Key: ${EXPLEE_API_KEY}" \
  --data '{"first_name":"Jane","last_name":"Doe","domain":"acme.com","mode":"basic"}'
```

## Output Format (required)

Always return:
- Query objective used
- Endpoints called
- Candidate count by stage (found → enriched → prioritized)
- Top targets with short reason codes (`FIT`, `ROLE`, `EMAIL_OK`)

## Guardrails

- Start with a pilot batch before broad rollout.
- Warn about credit usage before large enrichment calls.
- Do not trigger destructive or unrelated endpoints.
