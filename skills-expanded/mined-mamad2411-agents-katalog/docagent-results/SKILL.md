---
name: docagent-results
description: Check DocuAgent extraction, batch, and content-check results. Use when the user says "check results", "see my extraction", "recent runs", "is it done", "find order X", or "results page". Agents must run API calls when they have execution_id; never refuse with "I can't pull results from this workspace".
---

# Check results (DocuAgent)

**Source of truth for product UX:** `doc-agent/frontend` — especially `/results`, `app/services/results/`, `app/utils/axiosInstance.ts`. Canonical product map: `doc-agent/setup/docs/guides/USERFLOW.md`.

## Two stacks (do not conflate)

| Stack | Who uses it | Base (UAT) | Auth |
|-------|-------------|------------|------|
| **Product / NestJS execution API** | Web app, automation with JWT | `NEXT_PUBLIC_DEV_API` → e.g. `https://api.uat.doc-agent.lfxdigital.app/v1` | MSAL Bearer JWT, **service key** (login paste), or **team SA** + `X-Actor-Email` |
| **Agents / SDU OpenAPI** | Config Agent, integrators, **agents with only `execution_id`** | `https://api.uat.t4s.lfxdigital.app/agents/v1` | `X-API-Key` on `/config_integration/*` only; **`check_execution_status` has no auth** |

The **Results UI never calls** `/agents/v1/air8_integration/*`. It lists and polls **`/execution/*`** on the NestJS gateway.

`DOCAGENT_AGENTS_API_KEY` is **Config Agent only** — not for listing Results rows.

---

## Agent playbook (required)

When the user asks to **check results**, **recent runs**, **see an extraction**, or **is it done**:

1. **Do not** open with "I can't pull your results from here" or blame the skills repo.
2. **Pick path by what you have** (see decision table below) — run the call, interpret JSON, summarize.
3. **If they gave `execution_id`** (or it appears in chat/logs) and you have **no Bearer JWT**: poll SDU immediately (no Azure login, no API key):

```bash
curl -sS "https://api.uat.t4s.lfxdigital.app/agents/v1/air8_integration/check_execution_status?execution_id=<execution_id>"
```

This is an **agent shortcut**. The **product UI** polls `GET {DEV_API}/execution/sdu-extraction-executions/{id}` every **2s** until `output` exists (or **422** = failed).

4. **If they want recent runs / browse by order** and can supply **Bearer JWT** (or team SA + actor email): use NestJS list API (matches the Results page).
5. **If they gave `order_id` but no `execution_id` and no JWT**: ask for **one execution id** from the Results row or trigger email, **or** guide them to `/results` in the browser. Do not stop after auth lecture.
6. **DNS errors** on `api.uat.doc-agent.lfxdigital.app`: note the limit; **still use** `api.uat.t4s.lfxdigital.app` for `check_execution_status` when you have `execution_id`.

### Anti-patterns

| Bad | Do instead |
|-----|------------|
| "This workspace only has skills + API key" | Poll SDU if you have `execution_id`; list NestJS if you have Bearer |
| "Results require Azure AD, not that key" | Keys are unrelated; SDU status GET needs neither key nor JWT |
| "Send me execution id for the curl command" | **Run** the request and interpret the response |
| Tell user UI uses `check_execution_status` | UI uses NestJS GET-by-id; SDU poll is agent fallback |
| Default to Swagger when id is in chat | Poll first; UI second |

---

## Results in the web app (`/results`)

**Post-login default:** MSAL landing on `/` redirects to **`/results`** unless `returnUrl` / trial deep link applies.

### Tabs (URL `?tab=`)

| `?tab=` | UI label | Content |
|---------|----------|---------|
| `documents` (default) | **Extractions** | Single-document runs |
| `batches` | **Batches** | Multi-file batch jobs |
| `orders` | **Checks** | Content-check runs |
| `queue` | **Queue** | Live queue dashboard |

Valid keys: `documents | batches | orders | queue`. Invalid tab → normalized to `documents`.

**Note:** There is **no Exports tab** on `/results`. Excel export is a **row action** (`POST …/sdu-export-data-executions`).

### Extractions tab — browse recent runs

- Default: **page size 50**, sort **`createdOn` desc**
- Filters debounce **500ms**; list + **count** API share the same criteria (pagination totals match)
- **Deep links:** `/results?tab=documents&fieldConfigId=<id>&executionId=<id>` (used after guided trial)

| Filter | API param | Notes |
|--------|-----------|--------|
| Order ID | `orderId` | |
| Execution ID | `executionId` | Partial, case-insensitive |
| Field config | `fieldConfigId` | Exact |
| Status | `status` | `completed`, `failed`, `pending`, `queued`, `processing` |
| Date range | `fromDate`, `toDate` | UI maps `created_on_from` / `created_on_to` |
| Sort | `sortBy`, `sortOrder` | `createdOn` or `lastUpdatedOn` |

**Status display:** if `status === "pending"` and `queuedAt` is set, UI shows **QUEUED**.

**Row actions** (when `output` exists): view/edit output, export Excel, share (completed only), view payload, retry, delete.

**List does not auto-poll** — in-progress rows stay stale until refresh or user switches filters. Use **Queue** tab for live queue state.

### Above tabs

`GET /execution/sdu-extraction-executions/me/job-uptime?days=14` — refreshes every **60s** (SWR).

### Queue tab

`GET /execution/sdu-extraction-executions/queue-status` every **15s** (pauses when tab hidden).

---

## NestJS execution API (what the UI calls)

**Auth** (same as `axiosInstance.ts`):

1. **Team mode:** `Authorization: Bearer <service-account-key>` + `X-Actor-Email: <user email>`  
   Skip team SA for `/admin/*` and cross-team `/teams/:id/sa-key` — use user JWT.
2. **User mode:** `Authorization: Bearer <MSAL ID token>` (or service key from `/login`)
3. **Public (no bearer):** `GET …/execution/public/sdu-extraction-executions/share/{token}`

| Environment | Base |
|-------------|------|
| UAT | `https://api.uat.doc-agent.lfxdigital.app/v1` |
| Local frontend default | `http://localhost:3001/v1` |

### List recent extractions

```http
GET {base}/execution/sdu-extraction-executions?page=0&size=50&sortBy=createdOn&sortOrder=desc
Authorization: Bearer <token>
```

Optional filters: `orderId`, `executionId`, `fieldConfigId`, `status`, `fromDate`, `toDate`.

Count (matches filters):

```http
GET {base}/execution/sdu-extraction-executions/records/count?...
```

### One extraction (UI polling target)

```http
GET {base}/execution/sdu-extraction-executions/{id}
Authorization: Bearer <token>
```

- Poll every **2s** while running until `output` is present
- **422** → treat as failed (UI stops polling)
- Response includes `status`, `requestBody`, `output`, `queuedAt`, `fileSasUri`, `isShared`

### Content checks

```http
GET {base}/execution/sdu-check-content-executions?page=0&size=5
GET {base}/execution/sdu-check-content-executions/{id}
GET {base}/execution/sdu-check-content-executions/records/count
```

### Batches

```http
GET {base}/execution/sdu-extraction-executions/batch?page&size
GET {base}/execution/sdu-extraction-executions/batch/{batchId}
```

### Other Results endpoints

| Action | Method | Path |
|--------|--------|------|
| Retry one | POST | `/execution/sdu-extraction-executions/{id}/retry` |
| Retry all pending | POST | `/execution/sdu-extraction-executions/retry-all-pending` |
| Edit output | PATCH | `/execution/sdu-extraction-executions/{id}/edited-output` |
| Discard edits | PATCH | `/execution/sdu-extraction-executions/{id}/edited-output/discard` |
| Delete | DELETE | `/execution/sdu-extraction-executions/{id}` |
| Export Excel | POST | `/execution/sdu-export-data-executions` body `{ execution_id }` |
| Queue status | GET | `/execution/sdu-extraction-executions/queue-status` |
| My job uptime | GET | `/execution/sdu-extraction-executions/me/job-uptime?days=14` |

---

## SDU status poll (Agents API) — agent shortcut only

**Not used by the Results UI.** Use when you have `execution_id` but no JWT.

```bash
curl -sS "https://api.uat.t4s.lfxdigital.app/agents/v1/air8_integration/check_execution_status?execution_id=<execution_id>"
```

- **404 / 500 "No execution found"** → wrong id or environment
- **Still running** → backoff 2–5s, poll again
- **Completed** → summarize returned fields; for full `output` / preview, use NestJS GET-by-id or Results UI

NestJS persists the MongoDB record the UI shows; SDU poll reads the pipeline directly.

---

## Share links

1. Enable: `POST /execution/sdu-extraction-executions/{id}/share` → `{ shareToken, shareUrl, expiresAt? }`
2. Public read: `GET /execution/public/sdu-extraction-executions/share/{token}` (no auth)
3. App route: `/share/{token}` — prefers `editedOutput` over `output`

Do not invent share URLs; use `shareUrl` from the API.

---

## Output shape (what users see in modal)

Per document in `output`: Order ID, Nation, Doc Type, Doc ID, Result, Reason, extracted fields, `human_validate_status`, timestamps. List rows also expose `fieldConfigId`, `createdOn`, `lastUpdatedOn`, `createdBy`, `requestBody` (order_id, file_name, nation, doc types).

---

## Quick decision

| User wants… | Action |
|-------------|--------|
| Browse recent runs in product | `/results` → Extractions tab (or Bearer list GET above) |
| Status of known run, agent has id only | SDU `check_execution_status` |
| Full output + list by order | NestJS `/execution/sdu-extraction-executions` + Bearer |
| Live queue / capacity | `/results?tab=queue` or `queue-status` GET |
| Public read-only link | `/share/{token}` or public share GET |
| Config / threads / global config jobs | `docagent-config-agent` + `X-API-Key` |
