---
name: cesto-toolkit
description: >
  Complete toolkit for the Cesto platform — covers all APIs, basket creation, portfolio simulation, and market data.
  Use this skill whenever the user wants to interact with Cesto in any way: create a basket post, view basket data,
  analyze token performance, simulate a portfolio, check basket analytics, or publish to Cesto Labs.
  Trigger for any mention of "Cesto", "Cesto Labs", "basket", "basket idea", "post a basket", "community basket",
  "create basket post", "share my allocation", "publish basket", "Cesto API", "basket performance",
  "basket analytics", "simulate portfolio", "token analysis", or "basket detail".
---

# Cesto Toolkit

Complete API toolkit for the [Cesto](https://app.cesto.co) platform. Covers basket creation (Cesto Labs),
portfolio simulation, market data, and analytics.

**Backend URL:** `https://backend.cesto.co`
**Frontend URL:** `https://app.cesto.co`

---

## IMPORTANT: Execution Order and Presentation Rules

### Strict execution order

When this skill is loaded, follow this EXACT order. Do NOT skip steps or reorder.

1. **Authentication FIRST** — Before calling ANY API (public or authenticated), complete the auth check. No API calls until auth is confirmed.
2. **Then proceed** with whatever the user requested — fetching data, creating baskets, simulating portfolios, etc.

### Presentation rules

Follow these rules for ALL output during this skill:

- **NEVER show raw curl commands or their output** to the user. Run them silently via Bash and process the results yourself.
- **NEVER show access tokens, refresh tokens, JWT strings, or session IDs** in your text output. These are sensitive — keep them internal.
- **NEVER show raw JSON responses** from API calls. Parse them and present clean, formatted results.
- **Suppress Bash tool output** when it contains tokens or technical data. Use `2>/dev/null` and pipe through processing scripts to extract only what you need.
- **Show only clean, human-readable messages** to the user. Examples:
  - Auth: "Checking authentication..." → "Logged in! Wallet: 7xKX...v8Ej" (or "Opening browser to log in...")
  - Data: Show clean formatted tables, not raw JSON
  - Post creation: Show the post title, allocation table, and link — not the raw API response
- **Keep it conversational and seamless.** The user should feel like they're talking to an assistant, not watching terminal output.

---

## Authentication

Authentication uses a magic-link flow. The CLI checks for stored tokens and handles
login automatically. No manual JWT pasting required.

### Auth file location

`~/.cesto/auth.json`

```json
{
  "accessToken": "eyJ...",
  "refreshToken": "eyJ...",
  "accessTokenExpiresAt": "2026-03-19T14:00:00Z",
  "refreshTokenExpiresAt": "2026-03-26T13:00:00Z",
  "walletAddress": "7xKXq9..."
}
```

### Auth check (MUST be the very first step)

1. Check if `~/.cesto/auth.json` exists
   - If not → trigger login flow
2. Read the file and check token expiry:
   - `accessToken` valid → use it in `Authorization: Bearer <accessToken>` header. Show: "Authenticated! Wallet: XXXX...XXXX"
   - `accessToken` expired, `refreshToken` valid → call `POST /auth/refresh` silently to get new tokens → update `auth.json` → show: "Session refreshed! Wallet: XXXX...XXXX"
   - Both expired → trigger login flow

### Silent token refresh

```
POST https://backend.cesto.co/auth/refresh
Content-Type: application/json

{ "refreshToken": "<refreshToken from auth.json>" }

Response:
{ "accessToken": "eyJ...(new)", "refreshToken": "eyJ...(new)" }
```

Update `auth.json` with new tokens and recalculated expiry timestamps. Decode the JWT `exp` claim to get the expiry:

```
payload = JSON.parse(base64decode(token.split('.')[1]))
expiresAt = new Date(payload.exp * 1000).toISOString()
```

Do this silently. Do NOT show the refresh API call or response to the user.

### Login flow (when no valid tokens exist)

1. Call `POST https://backend.cesto.co/auth/cli/session` silently → get `{ sessionId, expiresIn }`
2. Build magic link: `https://app.cesto.co/cli-auth?session=<sessionId>`
3. Open browser automatically:
   - Mac: `open <url>`
   - Linux: `xdg-open <url>`
   - Windows: `start <url>`
   - If open fails → just show the link
4. Show ONLY this to the user:
   ```
   Opening browser to log in...
   If the browser didn't open, visit this URL:
   https://app.cesto.co/cli-auth?session=<sessionId>

   Waiting for authentication...
   ```
5. Poll `GET https://backend.cesto.co/auth/cli/session/<sessionId>/status` every 3 seconds silently
   - `"pending"` → wait and poll again (show nothing)
   - `"authenticated"` → save tokens to `~/.cesto/auth.json` silently
   - `"unknown"` or empty or unexpected response → **keep polling** (do NOT bail out)
   - Only stop on **confirmed HTTP 404** (session truly expired/not found) → show: "Login timed out. Please try again."
   - Max 100 attempts (5 minutes)
6. Create `~/.cesto/` folder if needed (Mac/Linux: `chmod 700`)
7. Write `auth.json` silently (Mac/Linux: `chmod 600`). Do NOT show the file contents.
8. Show ONLY: "Logged in successfully! Wallet: XXXX...XXXX"

### How to run auth commands silently

When running curl commands for auth, extract values using scripts and suppress all output:

```bash
# Example: Create session silently, extract sessionId
SESSION_ID=$(curl -s -X POST https://backend.cesto.co/auth/cli/session \
  -H "Content-Type: application/json" | python3 -c "import sys,json; print(json.load(sys.stdin)['sessionId'])")
```

### CRITICAL: Resilient polling logic

The polling script MUST be resilient to unexpected responses. Use `'unknown'` as the default
status (never `'error'`), and only bail out on a **confirmed HTTP 404**. Any other unexpected
response should be treated as "keep waiting."

```bash
# Resilient polling script
for i in $(seq 1 100); do
  RESULT=$(curl -s "https://backend.cesto.co/auth/cli/session/${SESSION_ID}/status")
  STATUS=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('status','unknown'))" 2>/dev/null)

  if [ "$STATUS" = "authenticated" ]; then
    echo "$RESULT"
    exit 0
  elif [ "$STATUS" = "pending" ]; then
    sleep 3
  elif [ "$STATUS" = "unknown" ] || [ -z "$STATUS" ]; then
    # Unexpected response — check if it's a real 404 before bailing
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "https://backend.cesto.co/auth/cli/session/${SESSION_ID}/status")
    if [ "$HTTP_CODE" = "404" ]; then
      echo "SESSION_EXPIRED"
      exit 1
    fi
    # Not a 404 — keep waiting (could be a transient error)
    sleep 3
  else
    sleep 3
  fi
done
echo "TIMEOUT"
exit 1
```

**Why this matters:** If the default status is set to `'error'` and used as a bail-out condition,
the script exits on the first unexpected response (e.g., a JSON response without a `status` field)
before the user has time to authenticate in the browser. Using `'unknown'` as the default and only
bailing on confirmed 404 ensures the script waits the full 5 minutes.

Never show these commands' raw output. Only show the clean messages listed above.

### Error handling for auth

| Status | Meaning | Action |
|---|---|---|
| 401 on any API call | Access token expired/invalid | Try silent refresh. If refresh also fails, trigger login flow. |

---

## Available Endpoints

| # | Endpoint | Method | Auth | Description |
|---|----------|--------|------|-------------|
| 1 | `/tokens` | GET | No | List all supported tokens |
| 2 | `/products` | GET | No | List all baskets |
| 3 | `/products/{slug}` | GET | No | Basket detail with strategy and performance |
| 4 | `/products/{id}/analyze` | GET | No | Per-token market data for a basket |
| 5 | `/products/{id}/graph` | GET | No | Historical time series (portfolio vs S&P 500) |
| 6 | `/products/analytics` | GET | No | Cross-basket analytics summary |
| 7 | `/cesto-labs/posts` | POST | Yes | Create a Cesto Labs basket post |
| 8 | `/agent/simulate-graph` | POST | Yes | Simulate portfolio historical performance |

**Notes:**
- `slug` is the URL-friendly name (e.g., `war-mode`). Use for the detail endpoint.
- `id` is the UUID (e.g., `adb0abe3-5ce0-40b0-80a4-e7a39f21807a`). Use for analyze, graph, and analytics.
- Both `slug` and `id` are returned by `GET /products`.
- `minimumInvestment` is in smallest unit (divide by 1,000,000 for USDC).
- Some fields like `tokenPerformance7d` and `tokenPerformance30d` may be `null`.
- Prediction market baskets (`category: "prediction"`) do not have graph or performance data.

For complete response structures of endpoints 2–6, see [references/api-reference.md](references/api-reference.md).

---

## 1. Token Registry

**GET** `/tokens`

Fetches all supported tokens on the Cesto platform. **Only call AFTER authentication is confirmed.**

**Response:** Array of token objects.

```json
[
  {
    "mint": "So11111111111111111111111111111111111111112",
    "symbol": "SOL",
    "name": "Solana",
    "logoUrl": "https://raw.githubusercontent.com/solana-labs/token-list/main/assets/mainnet/So11111111111111111111111111111111111111112/logo.png"
  }
]
```

| Field | Type | Description |
|---|---|---|
| `mint` | string | Solana mint address (unique identifier) |
| `symbol` | string | Token ticker (e.g. "SOL", "BONK") |
| `name` | string | Full token name (e.g. "Solana", "Bonk") |
| `logoUrl` | string | URL to the token's logo image |

**Important:** Only tokens returned by this API are supported by the Cesto platform. Fetch this list silently and use it internally to validate baskets. Do NOT dump the raw token list to the user.

---

## 7. Create Cesto Labs Basket Post

**POST** `/cesto-labs/posts`

Creates a basket post on Cesto Labs (community section). Requires authentication.

**Headers:**

| Header | Value |
|---|---|
| `Authorization` | `Bearer <accessToken>` |
| `Content-Type` | `application/json` |

### Request Payload

**Top-level fields:**

| Field | Type | Required | Rules |
|---|---|---|---|
| `title` | string | Yes | 1–100 characters |
| `description` | string | Yes | 1–1000 characters |
| `aiGenerateThumbnail` | boolean | Yes | Always set to `true`. Never include `thumbnailUrl`. |
| `allocations` | array | Yes | At least 1 allocation. All `percentage` values must sum to exactly 100. |

**Allocation object fields:**

| Field | Type | Required | Rules |
|---|---|---|---|
| `mint` | string | Yes | Must match a `mint` from the `/tokens` API |
| `symbol` | string | Yes | Must match a `symbol` from the `/tokens` API |
| `name` | string | Yes | Must match a `name` from the `/tokens` API |
| `percentage` | number | Yes | 1–100, max 2 decimal places |
| `logoUrl` | string | No | From the `/tokens` API |
| `description` | string | No | Max 200 characters |

### Example Payload

```json
{
  "title": "Low Risk DeFi Powerhouse",
  "description": "A conservative DeFi basket focused on established Solana protocols.",
  "aiGenerateThumbnail": true,
  "allocations": [
    {
      "mint": "So11111111111111111111111111111111111111112",
      "symbol": "SOL",
      "name": "Solana",
      "percentage": 40,
      "logoUrl": "https://raw.githubusercontent.com/solana-labs/token-list/main/assets/mainnet/So11111111111111111111111111111111111111112/logo.png",
      "description": "Foundation layer — most liquid and battle-tested"
    }
  ]
}
```

### Response

| Field | Description |
|---|---|
| `slug` | URL-friendly identifier for the post |
| `title` | The post title |
| `allocations` | The token allocations as submitted |

**Post URL format:** `https://app.cesto.co/cesto-labs/<slug>`

After creating a post, show the user:
- Post title
- A clean allocation table (token, percentage, rationale)
- The post link
- Note about admin approval if applicable

---

## 8. Simulate Portfolio Graph

**POST** `/agent/simulate-graph`

Simulates historical performance of a custom token allocation and compares it against the S&P 500 benchmark. Both start at 1000. Requires authentication.

**Headers:**

| Header | Value |
|---|---|
| `Authorization` | `Bearer <accessToken>` |
| `Content-Type` | `application/json` |

### Request Payload

| Field | Type | Required | Description |
|---|---|---|---|
| `allocations` | array | Yes | Token allocations (min 1 item) |
| `allocations[].token` | string | Yes | Token symbol (e.g. "SOL", "USDC") |
| `allocations[].mint` | string | Yes | Solana mint address |
| `allocations[].weight` | number | Yes | Allocation weight/percentage |
| `name` | string | Yes | Portfolio name |

### Example Payload

```json
{
  "allocations": [
    { "token": "SOL", "mint": "So11111111111111111111111111111111111111112", "weight": 50 },
    { "token": "USDC", "mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v", "weight": 50 }
  ],
  "name": "My Portfolio"
}
```

### Response

| Field | Type | Description |
|---|---|---|
| `workflowId` | string | Always `"agent-simulation"` |
| `name` | string | Portfolio name from request |
| `timeSeries` | array | Daily historical simulation data |
| `allocations` | array | Token allocations from request |

**`timeSeries[]` item:**

| Field | Type | Description |
|---|---|---|
| `timestamp` | string (ISO 8601) | Date |
| `portfolioValue` | number | Simulated portfolio value (starts at 1000) |
| `sp500Value` | number | S&P 500 benchmark value (starts at 1000) |
| `isLiquidated` | boolean | Whether portfolio was liquidated |

---

## Error Handling

| Status | Meaning | Action |
|---|---|---|
| 400 | Validation failed | Surface the API error message to the user |
| 401 | Access token expired/invalid | Try silent refresh, then retry. If refresh fails, trigger login flow. |
| 403 | Forbidden / No valid API key or JWT | User lacks permission or auth missing |
| 404 | Not found | Double-check the slug or ID |

Always surface the API error message — it's descriptive and helps the user understand what went wrong.
