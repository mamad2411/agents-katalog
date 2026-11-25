---
name: swarms-marketplace-api
description: Comprehensive reference for the Swarms Marketplace APIs. Use when creating/editing/querying agents or prompts, tokenizing agents (single or batch), claiming fees, or integrating with swarms.world. Covers CRUD for agents and prompts, token launch, batch token launch, schemas, examples, and error handling.
---

# Swarms Marketplace API – Skill Reference

Use this skill when working with the **Swarms Marketplace**: agents, prompts, tokenization (single and batch), and fee claims. All endpoints are under the marketplace base URL; authentication uses an API key or Supabase session.

**Full documentation (for deeper detail):**
- **Overview & endpoint index:** https://docs.swarms.ai/docs/marketplace/api-overview
- **Agents API:** https://docs.swarms.ai/docs/marketplace/agents-api
- **Prompts API:** https://docs.swarms.ai/docs/marketplace/prompts-api
- **Token Launch (single):** https://docs.swarms.ai/docs/marketplace/token-launch-api
- **Token Launch Batch:** https://docs.swarms.ai/docs/marketplace/token-launch-batch-api
- **Tokenization details (costs, bonding curve):** https://docs.swarms.ai/docs/marketplace/tokenization_details
- **Claim Fees API:** https://docs.swarms.ai/docs/marketplace/claim-fees-api
- **Marketplace examples:** https://docs.swarms.ai/docs/marketplace/examples
- **API Reference (auth, limits):** https://docs.swarms.ai/api-reference

---

## Base URLs & authentication

| Service           | Base URL              |
|-------------------|------------------------|
| Marketplace API   | `https://swarms.world` |
| Swarms API        | `https://api.swarms.world` |

**Authentication:** Send API key in the header: `Authorization: Bearer YOUR_API_KEY`.  
Get keys at: https://swarms.world/platform/api-keys

---

## 0. Publish anything – `POST /api/v1/publish/product`

One route for every product type. Send `type` plus the fields the per-type route takes; the response is that route's response (`success`, `id`, `listing_url`, …).

```json
{ "type": "prompt", "name": "Release notes writer", "description": "Turns a changelog into release notes.", "prompt": "You write release notes…" }
```

`type` is `agent` (fields of `/api/add-agent`), `prompt` (`/api/add-prompt`), `tool` (`/api/add-tool`: `name`, `description`, `tool` required) or `bundle` (`/api/v1/publish/bundle`). An unknown `type` is a 400 listing the valid values.

---

## 1. Agents API (CRUD)

### Create agent – `POST /api/add-agent`

**Required:** `name` (min 2 chars), `description`, `useCases` (array, at least one).  
**Optional:** `agent` (code, min 5 chars if set), `language`, `requirements`, `tags`, `is_free` (default `true`), `price_usd` (if paid), `category`, `status`, `tokenized_on`, `ticker`/`creator_wallet`/`private_key` (if tokenized), `image_url`/`file_path`/`image_base64`, `links`, `seller_wallet_address`, `x402_url`, `mcp_url`.

**Schema (input):**

| Parameter                | Type    | Required | Description |
|--------------------------|---------|----------|-------------|
| name                     | string  | Yes      | Display name, min 2 characters |
| agent                    | string  | No       | Agent code; min 5 chars if provided |
| description              | string  | Yes      | Description of the agent |
| language                 | string  | No       | e.g. "python", "javascript" |
| requirements             | array   | No       | `[{ "package": string, "installation": string }]` |
| useCases                 | array   | Yes      | `[{ "title": string, "description": string }]` |
| tags                     | string  | No       | Comma-separated |
| is_free                  | boolean | No       | Default `true` |
| price_usd                | number  | If paid  | Required when `is_free` is false; > 0 |
| category                 | string  | No       | e.g. "data-science" |
| status                   | string  | No       | `pending` \| `approved` \| `rejected`; default `pending` |
| tokenized_on             | boolean | No       | Enable Solana tokenization |
| ticker                   | string  | If token | Required when `tokenized_on` is true; uppercase alphanumeric, max 10 |
| creator_wallet           | string  | If token | Creator wallet public key |
| private_key              | string  | If token | JSON array of 64 bytes, base64, or base58 |
| image_url / file_path / image_base64 | string | No | Image (one of these) |
| links                    | array   | No       | Strings or `{ "name": string, "url": string }` |
| seller_wallet_address    | string  | No       | Seller wallet |
| x402_url / mcp_url       | string  | No       | Valid URL or empty string |

**Success (200):**

```json
{
  "success": true,
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "listing_url": "https://swarms.world/agent/550e8400-e29b-41d4-a716-446655440000",
  "tokenized": false,
  "token_address": null,
  "pool_address": null
}
```

**Example – create agent (cURL):**

```bash
curl -X POST https://swarms.world/api/add-agent \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Data Analysis Agent",
    "agent": "from swarms import Agent\n\nclass DataAnalysisAgent(Agent):\n    def analyze(self, data):\n        pass",
    "description": "An AI agent for analyzing datasets",
    "language": "python",
    "requirements": [{"package": "pandas", "installation": "pip install pandas"}],
    "useCases": [{"title": "Financial Analysis", "description": "Analyze financial data"}],
    "tags": "data,analysis,python",
    "is_free": false,
    "price_usd": 19.99,
    "category": "data-science"
  }'
```

### Update agent – `POST /api/edit-agent`

Same body as create, **plus required** `id` (agent UUID).

**Example:**

```bash
curl -X POST https://swarms.world/api/edit-agent \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"id": "550e8400-e29b-41d4-a716-446655440000", "name": "Advanced Data Agent", "description": "Updated description", "price_usd": 24.99}'
```

### Query agents – `POST /api/query-agents`

**Auth:** Optional.  
**Body:** `search`, `category`, `priceFilter` ("all" | "free" | "paid"), `userFilter`, `sortBy` ("newest" | "oldest" | "popular" | "rating"), `limit` (1–100, default 6), `offset` (default 0).

**Example:**

```bash
curl -X POST https://swarms.world/api/query-agents \
  -H "Content-Type: application/json" \
  -d '{"search": "data analysis", "category": "data-science", "sortBy": "newest", "limit": 10, "offset": 0}'
```

**Response:** Array of agent objects (id, name, agent, description, language, requirements, use_cases, tags, is_free, price_usd, category, status, image_url, user_id, created_at, updated_at, etc.).

---

## 2. Prompts API (CRUD)

### Create prompt – `POST /api/add-prompt`

**Required:** `name` (min 2 chars), `prompt` (min 5 chars), `useCases` (at least one), `tags` (min 2 chars).  
**Optional:** `description`, `is_free`, `price_usd`, `category`, `status`, `tokenized_on`, `ticker`/`creator_wallet`/`private_key` (if tokenized), `image_url`/`file_path`/`image_base64`, `links`, `seller_wallet_address`.

**Schema (input):** Same pattern as agents for pricing, tokenization, and images; content field is `prompt` instead of `agent`.

**Success (200):**

```json
{
  "success": true,
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "listing_url": "https://swarms.world/prompt/550e8400-e29b-41d4-a716-446655440000",
  "tokenized": false,
  "token_address": null,
  "pool_address": null
}
```

**Example – create prompt:**

```bash
curl -X POST https://swarms.world/api/add-prompt \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Technical Blog Writer",
    "prompt": "You are an expert technical writer. Topic: {topic}",
    "description": "Prompt for technical blog posts",
    "useCases": [{"title": "Tutorial Creation", "description": "Step-by-step tutorials"}],
    "tags": "writing,technical,blog",
    "is_free": false,
    "price_usd": 4.99,
    "category": "content"
  }'
```

### Update prompt – `POST /api/edit-prompt`

Same as create plus **required** `id` (prompt UUID).

### Query prompts – `POST /api/query-prompts`

**Body:** `search`, `category`, `priceFilter`, `userFilter`, `sortBy`, `limit` (1–100), `offset`.  
**Response:** Array of prompt objects.

**Using a marketplace prompt with an agent:** Set `marketplace_prompt_id` in agent config (e.g. Swarms API completions); the system fetches the prompt from the marketplace. See https://docs.swarms.ai/docs/marketplace/prompts-api#using-marketplace-prompts-with-agents.

---

## 3. Token Launch (single) – create agent + token in one call

**Endpoint:** `POST https://swarms.world/api/token/launch`  
**Content-Type:** `application/json` or `multipart/form-data` (for image file).

**Body (JSON):**

| Parameter    | Type   | Required | Description |
|-------------|--------|----------|-------------|
| name        | string | Yes      | Min 2 characters |
| description | string | Yes      | Non-empty |
| ticker      | string | Yes      | 1–10 chars, letters/numbers only; uppercased |
| private_key | string | Yes      | JSON array, base64, or base58 (64 bytes) |
| image       | string/file | No  | URL, base64, or multipart file |

Creates a minimal agent listing and mints a token on Solana. **Cost ~0.04 SOL** (from wallet tied to `private_key`).

**Success (200):**

```json
{
  "success": true,
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "listing_url": "https://swarms.world/agent/550e8400-e29b-41d4-a716-446655440000",
  "tokenized": true,
  "token_address": "7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU",
  "pool_address": "9yZ...configKey"
}
```

**Example (JSON):**

```bash
curl -X POST https://swarms.world/api/token/launch \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Token Agent",
    "description": "Agent launched and tokenized via API.",
    "ticker": "MAG",
    "private_key": "[1,2,3,...]"
  }'
```

**Multipart (image):** Use `-F "image=@/path/to/icon.png"` with other fields as form fields.

---

## 4. Token Launch Batch – multiple tokens in one request

**Endpoint:** `POST https://swarms.world/api/token/launch/batch`  
**Content-Type:** `application/json` only (no multipart).  
**Batch size:** 1–50 tokens per request. Tokens are processed in parallel.

**Body:**

| Parameter    | Type  | Required | Description |
|-------------|-------|----------|-------------|
| private_key | string| Conditional | Default key for all tokens; required if any token has no own `private_key` |
| tokens      | array | Yes     | 1–50 token items (see below) |

**Token item:**

| Field        | Type   | Required | Description |
|-------------|--------|----------|-------------|
| name        | string | Yes      | Min 2 characters |
| description | string | Yes      | Non-empty |
| ticker      | string | Yes      | 1–10 chars, letters/numbers only |
| private_key | string | No       | Override top-level key for this token |
| image       | string | No       | URL or base64 (no multipart in batch) |

**Success – all succeeded (200):**

```json
{
  "success": true,
  "total": 2,
  "succeeded": 2,
  "failed": 0,
  "results": [
    {"success": true, "index": 0, "id": "uuid", "listing_url": "https://swarms.world/agent/...", "token_address": "...", "pool_address": "..."},
    {"success": true, "index": 1, "id": "uuid", "listing_url": "...", "token_address": "...", "pool_address": "..."}
  ]
}
```

**Partial success (207):** Some items failed. Same structure; `success: false`, `succeeded` + `failed` counts; failed entries in `results` have `success: false`, `index`, `error`. Optional `failures` array lists only failed items.

**Example – batch launch:**

```bash
curl -X POST https://swarms.world/api/token/launch/batch \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "private_key": "[1,2,3,...]",
    "tokens": [
      {"name": "Agent One", "description": "First.", "ticker": "ONE"},
      {"name": "Agent Two", "description": "Second.", "ticker": "TWO"}
    ]
  }'
```

**Mixed keys:** Set top-level `private_key` and override per token with `private_key` on individual items.

---

## 5. Tokenization details (costs & bonding curve)

- **Creation fee:** **0.04 SOL** per token (~$4 USD equivalent; varies with SOL price). One-time, paid when launching the token.
- **Initial market cap:** 18 SOL equivalent.
- **Graduation market cap:** 400 SOL equivalent; after that the token graduates from the virtual pool and is tradeable on DEXs.
- **Ticker:** 1–10 characters, letters and numbers only; stored uppercase (e.g. `AGENT`, `MYBOT`).

Full details: https://docs.swarms.ai/docs/marketplace/tokenization_details

---

## 6. Error responses & status codes

**Common error body fields:** `error`, `message`, `details`, `status_code`. Optional: `errors` (validation), `existingId` (duplicate), `how_to_get_key` (401), `currentUsage`, `limits`, `resetTime` (429), `token_index` (batch/per-token errors), `required_sol`, `current_balance_sol` (insufficient SOL).

| Code | Meaning |
|------|---------|
| 200  | Success |
| 207  | Multi-Status (batch: partial success; check `results`) |
| 400  | Bad request (validation, invalid key, insufficient SOL, etc.) |
| 401  | Unauthorized (missing/invalid API key) |
| 403  | Forbidden (content validation failed) |
| 404  | Not found |
| 405  | Method not allowed |
| 429  | Too many requests (rate limit) |
| 500  | Internal server error |

**401 example:** Response includes `how_to_get_key`: "https://swarms.world/platform/api-keys".

---

## 7. Rate limits

- **Paid agents / Paid prompts / Free content:** 500 per user per day each; reset at midnight UTC.
- Batch token launch: each token in the batch counts toward the agent creation limit.

429 responses include `currentUsage`, `limits`, and `resetTime`.

---

## 8. Validation & content rules

- **Agents:** Duplicate = same name + same `agent` content for same user → 400 with `existingId`. Content validation can return `trustworthiness`, `contentQuality`.
- **Prompts:** Duplicate = same content for same user → 400 with `existingId`.
- **Tokenization:** When `tokenized_on` is true (or using token launch), `ticker` + `creator_wallet` + `private_key` required for add-agent/add-prompt; for token launch only `private_key` (and name, description, ticker) required.
- **Private key formats:** JSON array of 64 integers, base64, or base58 (e.g. Phantom export).

---

## 9. Quick reference – endpoints

| API        | Endpoint              | Method | Auth  | Purpose |
|------------|-----------------------|--------|-------|---------|
| Account    | /api/me               | GET    | Yes   | Your user id, username, credit balance and listing counts |
| Any        | /api/v1/publish/product | POST | Yes   | Create agent, prompt, tool or bundle (`type` + that type's fields) |
| Agents     | /api/add-agent        | POST   | Yes   | Create agent |
| Agents     | /api/edit-agent       | POST   | Yes   | Update agent |
| Agents     | /api/query-agents     | POST   | No    | Search/filter agents |
| Prompts    | /api/add-prompt       | POST   | Yes   | Create prompt |
| Prompts    | /api/edit-prompt      | POST   | Yes   | Update prompt |
| Prompts    | /api/query-prompts    | POST   | No    | Search/filter prompts |
| Tools      | /api/add-tool         | POST   | Yes   | Create tool |
| Token      | /api/token/launch      | POST   | Yes   | Single agent + token |
| Token      | /api/token/launch/batch | POST | Yes   | Batch agent + token (1–50) |

When in doubt or when you need full request/response schemas, code samples in multiple languages, or edge-case behavior, use the **full documentation URLs** listed at the top of this skill.
