---
name: explee-master-orchestrator
description: "Route user intent to the correct Explee product workflow (Search, Enrichment, AI Agents, AutoGTM) using API key auth first with cookie fallback. USE WHEN a task matches the Craft workspace workflow for explee-master-orchestrator."
cluster: explee-master
version: 1.0.0
origin: "craft-agent workspace"
---

# Explee Master Orchestrator

Use this as the single entry skill for Explee tasks. It decides which product workflow to run and which credential mode to use.

## Child Skills (routing targets)

- `explee-product-search`
- `explee-product-enrichment`
- `explee-product-ai-agents`
- `explee-product-autogtm`
- `explee-api-cookie-access` (auth fallback guidance)

## Routing Rules by Intent

### Route to Search when user asks to:
- Find companies / accounts / prospects
- Find people by role/title/domain
- Convert natural-language ICP to filters

Primary endpoints:
- `POST /public/api/v1/search/nl-to-filters`
- `POST /public/api/v1/search/companies`
- `POST /public/api/v1/search/people`

### Route to Enrichment when user asks to:
- Find/verify work emails
- Run single or batch email enrichment
- Track enrichment task status

Primary endpoints:
- `POST /public/api/v1/enrich/email`
- `POST /public/api/v1/enrich/email/batch`
- `GET /public/api/v1/enrich/email/batch/{task_id}`

### Route to AI Agents when user asks to:
- Run Explee pre-built agent workflows
- Run custom agents with prompts/schemas
- Poll agent runs for completion

Primary endpoints:
- `GET /public/api/v1/agents`
- `POST /public/api/v1/agents/{agent_id}/runs`
- `POST /public/api/v1/agents/runs`
- `GET /public/api/v1/agents/runs/{run_id}`

### Route to AutoGTM when user asks to:
- Build end-to-end GTM pipeline
- Turn ICP into prioritized outreach list
- Chain search + enrichment + ranking

Pipeline pattern:
1. `nl-to-filters`
2. companies/people search
3. email enrichment
4. prioritization output

## Credential Strategy (IMPORTANT)

Use both stored credential types with this preference order:

1. **Primary:** Cookie auth
   - `Cookie: <cookie_string>`
   - Use this first when both credentials are available.

2. **Fallback:** API key header
   - `X-API-Key: <api_key>`
   - Use when cookie is unavailable or rejected.

3. **If auth fails:**
   - On 401/403 with cookie, retry once with API key (if available).
   - If both fail, ask user to refresh credentials.

## Request Templates

### Template A — Cookie first

```bash
curl 'https://api.explee.com/<endpoint>' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H "Cookie: ${EXPLEE_COOKIE}"
```

### Template B — API key fallback

```bash
curl 'https://api.explee.com/<endpoint>' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H "X-API-Key: ${EXPLEE_API_KEY}"
```

## Standard Operating Flow

1. Classify intent into one route (Search / Enrichment / Agents / AutoGTM).
2. Confirm objective and expected output format.
3. Execute with cookie auth first.
4. If needed, retry with API key fallback.
5. Return concise execution summary:
   - selected route
   - endpoint(s)
   - auth mode used
   - status code(s)
   - result summary and next action

## Guardrails

- Never print full API key or full cookie string in user-visible output.
- Call out estimated credit impact before large/batch operations.
- For mutating or high-cost actions, confirm scope first.
- Keep initial runs small (pilot batch) before scaling.
