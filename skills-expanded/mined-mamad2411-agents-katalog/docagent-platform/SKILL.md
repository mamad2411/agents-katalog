---
name: docagent-platform
description: Routes DocuAgent work by user intent — product UI (NestJS /execution/* + MSAL) vs Agents OpenAPI (/agents/v1). Use when choosing which skill applies, auth (X-API-Key for ConfigAgent only), polling async jobs, or staying endpoint-first. For Results tabs, filters, and NestJS vs SDU paths, use docagent-results.
---

# DocuAgent platform router

## Two stacks

| Stack | Surface | Base (UAT) | Primary auth |
|-------|---------|------------|--------------|
| **Product** | Next.js web app (`doc-agent/frontend`) | `NEXT_PUBLIC_DEV_API` → e.g. `https://api.uat.doc-agent.lfxdigital.app/v1` | MSAL Bearer JWT, service key login, or team SA + `X-Actor-Email` |
| **Agents OpenAPI** | SDU FastAPI ([Swagger](https://api.uat.t4s.lfxdigital.app/agents/v1/docs)) | `https://api.uat.t4s.lfxdigital.app/agents/v1` | `X-API-Key` on `/config_integration/*`; other groups per deployment |

NestJS **orchestrates** SDU for document runs. The UI triggers and polls **`/execution/*`**, not Agents `check_execution_status`.

OpenAPI wire prefixes: **`Air8`** → `/air8_integration/`, **`ConfigAgent`** → `/config_integration/`, **`LFSearch`** → `/search_integration/`, **`NER`** → `/ner_integration/`.

**Product UX map:** `doc-agent/setup/docs/guides/USERFLOW.md`

---

## Product auth (`axiosInstance.ts`)

Priority on outbound requests:

1. **Team mode:** `Authorization: Bearer <SA key>` + `X-Actor-Email: <email>`  
   **Exceptions** (must use user MSAL JWT even in team mode): `/admin/*`, `/teams/:id/sa-key`
2. **User mode:** `Authorization: Bearer <MSAL ID token>` (401 → refresh once)
3. **Service key login:** same Bearer header shape (pasted on `/login`)
4. **Public routes** (no bearer): URLs containing `/public/`, `/share/`, `/changelog`

Local dev: frontend defaults to `http://localhost:3001/v1`; config routes may split to `NEXT_PUBLIC_CONFIG_API` (port 3101) when localhost.

**Config Agent** (separate from Results): direct `NEXT_PUBLIC_EXTERNAL_AGENT_ENDPOINT` + API key, or gateway `/agents/v1/config_integration/*`.

---

## Agents API onboarding

- Do **not** require `DOCAGENT_AGENTS_API_BASE_URL` from end users. Examples use **`https://api.uat.t4s.lfxdigital.app/agents/v1`**.
- Discover contract: `GET /openapi.json` or [Swagger UI](https://api.uat.t4s.lfxdigital.app/agents/v1/docs).
- **`DOCAGENT_AGENTS_API_KEY`**: only `/config_integration/*`.

### Preflight

```bash
curl -sS "https://api.uat.t4s.lfxdigital.app/agents/v1/health"
```

---

## Decision tree (pick domain skill)

0. **Results page / recent runs / browse extractions / queue** → `docagent-results`  
   - Human: `/results` tabs (`?tab=documents|batches|orders|queue`)  
   - Automation: NestJS `/execution/sdu-*` + Bearer  
   - Agent with only `execution_id`: SDU `check_execution_status` (not what UI uses)
1. **Extract / validate documents** (UI: POST `/execution/sdu-extraction-executions`; SDU: `validate_and_extract_docs`) → `docagent-extraction`
2. **Content checks** (UI: `/execution/sdu-check-content-executions`; SDU: `check_doc_content`) → `docagent-content-check`
3. **Export Excel / blob** → `docagent-export-results` + Results row `POST …/sdu-export-data-executions`
4. **Config chat, uploads, shipment mapping, embeddings, global config jobs** → `docagent-config-agent`. Multipart → `docagent-file-prep`
5. **Poll `execution_id` on raw SDU** (no JWT) → `docagent-results` (SDU section)
6. **Company research** → POST from OpenAPI; poll via `docagent-results`
7. **Supplier/buyer/factory/product search** → `docagent-search`
8. **NER trace / suggest / pipelines** → `docagent-ner`
9. **Health / memory only** → `docagent-admin-kpis`

---

## Async polling (match product behavior)

| Job type | UI poll interval | Endpoint | Stop when |
|----------|------------------|----------|-----------|
| Document extraction | **2s** | `GET /execution/sdu-extraction-executions/{id}` | `output` present or **422** |
| Batch | **2s** | `GET …/batch/{id}` | batch complete |
| Content check | **2s** | `GET /execution/sdu-check-content-executions/{id}` | `output` present |
| Results queue tab | **15s** | `GET …/queue-status` | dashboard |
| Agent SDU fallback | 2–5s backoff | `GET …/check_execution_status?execution_id=` | terminal status |

Config jobs: poll `GET /config_integration/config-job/{job_id}`. Embeddings: poll `…-embeddings-status/{job_id}`. NER: poll `…/status/{task_id}`.

Backoff: start 1–2s, cap ~10–15s; stop on failed or reasonable wall-clock budget.

---

## Request discipline

- Prefer explicit JSON bodies from `openapi.json` schemas.
- Multipart: use `-F`; read OpenAPI `multipart/form-data` schema — do not guess field names.
- On **422**, read `detail` and fix the body.

---

## Safety

- **DELETE** on `/search_integration/*/{search_id}` removes backing-store data — confirm with user first.
- Do not log API keys or full document payloads in chat transcripts.

---

## Endpoint coverage map (Agents OpenAPI)

| Group | Skill(s) |
|-------|----------|
| Health `/`, `/health`, `/memory` | `docagent-admin-kpis` |
| DocuAgent document processing | `docagent-extraction`, `docagent-content-check`, `docagent-export-results`, `docagent-results` |
| `ConfigAgent` | `docagent-config-agent`, `docagent-export-results`, `docagent-file-prep` |
| `LFSearch` | `docagent-search`, `docagent-results` |
| `NER` | `docagent-ner` |

**Product Results** (not in Agents Swagger): NestJS `/execution/*` — see `docagent-results`.
