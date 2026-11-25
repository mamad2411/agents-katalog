---
name: publisher
description: |
  Publisher data query and management tool. Query monetization data, block earnings, platform performance, asset balance, transaction history, and submit withdrawals via Open API Key.
  Triggers: 'publisher', 'block revenue', 'monetization', 'ad placement', 'traffic revenue', 'daily revenue', 'platform', 'withdraw', 'earnings', 'balance'.
metadata:
  author: ads3
  version: "1.0.2"
---

# Publisher Skill

## Overview

Query traffic monetization data, manage ad placements, check earnings balance, and submit withdrawals via Open API Key.

---

## Authentication

### Supported Methods

Two authentication methods are supported (choose one):

| Header | Description |
|--------|-------------|
| open-api-key | **Recommended** - Open API Key generated in dashboard |
| token | JWT Token obtained after login |

### API Base URL

```
https://app.ads3.ai/api/v2
```

---

## API: Get Platform List

Get publisher's platform list with aggregated performance metrics.

### Method: GET

**URL**:
```
/publisher/platforms
```

**Query Parameters**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| current | number | No | Page number, default 1 |
| pageSize | number | No | Items per page, default 10 |

### Example Request

```bash
curl -X GET 'https://app.ads3.ai/api/v2/publisher/platforms?current=1&pageSize=10' \
  -H 'open-api-key: YOUR_API_KEY'
```

### Response Example

```json
{
  "data": [
    {
      "id": "platform_001",
      "name": "My Telegram Bot",
      "platformStatus": "onGoing",
      "botAppUrl": "https://t.me/mybot",
      "website": "https://myapp.com",
      "webAppUrl": "https://myapp.com/webapp",
      "impressions": 500000,
      "clicks": 12500,
      "conversions": 850,
      "earn": 1875.5,
      "marketplaces": ["marketplace_001"],
      "isOwner": true
    }
  ],
  "total": 3,
  "current": 1,
  "pageSize": 10,
  "success": true
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| data[].id | string | Platform ID |
| data[].name | string | Platform name |
| data[].platformStatus | string | Status: onGoing/paused/auditing/fail |
| data[].botAppUrl | string | Telegram Bot URL |
| data[].website | string | Website URL |
| data[].webAppUrl | string | Web App URL |
| data[].impressions | number | Total impressions (all time) |
| data[].clicks | number | Total clicks (all time) |
| data[].conversions | number | Total conversions (all time) |
| data[].earn | number | Total earnings in USDT (all time) |
| data[].marketplaces | string[] | Associated marketplace IDs |
| data[].isOwner | boolean | Whether the current user owns this platform |

---

## API: Get Platform Detail

Get a single platform's configuration.

### Method: GET

**URL**:
```
/publisher/platform/:platformId
```

**Path Parameters**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| platformId | string | Yes | Platform ID |

### Example Request

```bash
curl -X GET 'https://app.ads3.ai/api/v2/publisher/platform/platform_001' \
  -H 'open-api-key: YOUR_API_KEY'
```

### Response Example

```json
{
  "id": "platform_001",
  "name": "My Telegram Bot",
  "platformStatus": "onGoing",
  "botAppUrl": "https://t.me/mybot",
  "website": "https://myapp.com",
  "webAppUrl": "https://myapp.com/webapp"
}
```

---

## API: Get Block List

Get ad placement (block) list for a platform, with aggregated performance metrics.

### Method: GET

**URL**:
```
/publisher/blocks
```

**Query Parameters**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| platformId | string | **Yes** | Platform ID to filter blocks |
| current | number | No | Page number, default 1 |
| pageSize | number | No | Items per page, default 10 |

### Example Request

```bash
curl -X GET 'https://app.ads3.ai/api/v2/publisher/blocks?platformId=platform_001&current=1&pageSize=10' \
  -H 'open-api-key: YOUR_API_KEY'
```

### Response Example

```json
{
  "data": [
    {
      "id": "block_001",
      "name": "Homepage Banner",
      "description": "Main banner on homepage",
      "blockStatus": "onGoing",
      "impressions": 250000,
      "clicks": 5800,
      "conversions": 420,
      "earn": 870.5,
      "ctr": 2.32,
      "cr": 7.24,
      "billingAllocation": {
        "mode": "dynamic",
        "amount": "70%"
      },
      "cpmBillingAllocation": {
        "mode": "fixed",
        "amount": 0.5
      },
      "billings": [
        { "billingType": "CPC", "minPerCost": 0.05 },
        { "billingType": "CPA", "minPerCost": 0.5 }
      ],
      "marketplaces": ["marketplace_001"],
      "cpcLimit": { "daily": 1000 },
      "isOwner": true
    }
  ],
  "total": 5,
  "current": 1,
  "pageSize": 10,
  "success": true
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| data[].id | string | Block ID |
| data[].name | string | Block name |
| data[].description | string | Block description |
| data[].blockStatus | string | Status: onGoing/paused/auditing |
| data[].impressions | number | Total impressions (all time) |
| data[].clicks | number | Total clicks (all time) |
| data[].conversions | number | Total conversions (all time) |
| data[].earn | number | Total earnings in USDT (all time) |
| data[].ctr | number | Click-through rate (%) |
| data[].cr | number | Conversion rate (%) |
| data[].billingAllocation | object | CPC/CPA revenue share settings |
| data[].billingAllocation.mode | string | `dynamic` (percentage) or `fixed` (USDT per event) |
| data[].billingAllocation.amount | string/number | Percentage (e.g. `"70%"`) or fixed USDT amount |
| data[].cpmBillingAllocation | object | CPM revenue share settings |
| data[].billings | array | Accepted billing types and minimum cost thresholds |
| data[].cpcLimit.daily | number | Daily click cap for CPC ads |
| data[].isOwner | boolean | Whether the current user owns this block |

---

## API: Get Block Daily Summary

Get daily performance breakdown for a specific block.

### Method: GET

**URL**:
```
/publisher/block/summary/:blockId
```

**Path Parameters**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| blockId | string | Yes | Block ID |

**Query Parameters**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| current | number | No | Page number, default 1 |
| pageSize | number | No | Items per page, default 10 |

### Example Request

```bash
curl -X GET 'https://app.ads3.ai/api/v2/publisher/block/summary/block_001?current=1&pageSize=30' \
  -H 'open-api-key: YOUR_API_KEY'
```

### Response Example

```json
{
  "data": [
    {
      "onDate": "2026-04-14",
      "impressions": 8500,
      "clicks": 195,
      "conversions": 14,
      "earn": 29.25,
      "ctr": 2.29,
      "cr": 7.18
    }
  ],
  "total": 30,
  "current": 1,
  "success": true
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| data[].onDate | string | Date (YYYY-MM-DD), sorted descending |
| data[].impressions | number | Valid impressions that day |
| data[].clicks | number | Valid clicks that day |
| data[].conversions | number | Valid conversions that day |
| data[].earn | number | Earnings that day (USDT) |
| data[].ctr | number | Click-through rate (%) |
| data[].cr | number | Conversion rate (%) |

---

## API: Get Publisher Asset Balance

Get the current user's publisher account balance.

### Method: GET

**URL**:
```
/user/asset/publisher
```

### Example Request

```bash
curl -X GET 'https://app.ads3.ai/api/v2/user/asset/publisher' \
  -H 'open-api-key: YOUR_API_KEY'
```

### Response Example

```json
{
  "list": [
    {
      "assetName": "USDT",
      "assetId": "asset_usdt_id",
      "balance": 128.50,
      "logo": "https://cdn.ads3.ai/assets/usdt.png",
      "status": "active"
    }
  ]
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| list[].assetName | string | Asset name (e.g. USDT) |
| list[].assetId | string | Asset ID (required for withdrawal) |
| list[].balance | number | Current available balance (USDT) |
| list[].logo | string | Asset logo URL |
| list[].status | string | Asset status |

---

## API: Get Asset Flow History

Get the user's transaction history (deposits and withdrawals).

### Method: GET

**URL**:
```
/user/asset/advertiser/flow
```

**Query Parameters**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| current | number | No | Page number, default 1 |
| pageSize | number | No | Items per page, default 10 |
| flowType | string | No | Filter: `Deposit` or `Withdraw` (omit for all) |

### Example Request

```bash
curl -X GET 'https://app.ads3.ai/api/v2/user/asset/advertiser/flow?current=1&pageSize=20&flowType=Withdraw' \
  -H 'open-api-key: YOUR_API_KEY'
```

### Response Example

```json
{
  "data": [
    {
      "flowId": "flow_001",
      "title": "Withdraw",
      "flowType": "Withdraw",
      "amount": -50.00,
      "symbol": "USDT",
      "assetName": "USDT",
      "orderStatus": "done",
      "createdAt": "2026-04-14 10:23:00"
    },
    {
      "flowId": "flow_002",
      "title": "Revenue Settlement",
      "flowType": "Income",
      "amount": 29.25,
      "symbol": "USDT",
      "assetName": "USDT",
      "orderStatus": null,
      "createdAt": "2026-04-13 00:00:00"
    }
  ],
  "total": 42,
  "current": 1,
  "pageSize": 20,
  "success": true
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| data[].flowId | string | Flow record ID (use for detail lookup) |
| data[].title | string | Transaction description |
| data[].flowType | string | Type: Deposit / Withdraw / Income etc. |
| data[].amount | number | Amount (positive = in, negative = out) |
| data[].symbol | string | Token symbol (USDT) |
| data[].orderStatus | string | Order status for deposits/withdrawals (null for settlements) |
| data[].createdAt | string | Timestamp (YYYY-MM-DD HH:mm:ss) |

---

## API: Get Withdrawal Config

Get the minimum withdrawal amount, fee, and supported chains.

### Method: POST

**URL**:
```
/withdraw/basic
```

**Request Body**: None

### Example Request

```bash
curl -X POST 'https://app.ads3.ai/api/v2/withdraw/basic' \
  -H 'open-api-key: YOUR_API_KEY'
```

### Response Example

```json
{
  "fee": 1,
  "actualFee": 0,
  "min": 10,
  "list": [
    { "chain": "arbitrum", "name": "Arbitrum Network", "isValid": true },
    { "chain": "BNB Chain", "name": "BNB Chain", "isValid": true },
    { "chain": "tron", "name": "Tron Network", "isValid": true },
    { "chain": "ton", "name": "Ton Network", "isValid": true }
  ]
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| min | number | Minimum withdrawal amount (USDT) |
| actualFee | number | Actual withdrawal fee currently charged (USDT) |
| fee | number | Nominal fee (USDT) |
| list[].chain | string | Chain identifier |
| list[].name | string | Chain display name |
| list[].isValid | boolean | Whether this chain is available |

---

## API: Submit Withdrawal

Submit a withdrawal request to transfer earnings to an external wallet.

### Method: POST

**URL**:
```
/withdraw
```

**Request Body**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| assetId | string | Yes | Asset ID from `/user/asset/publisher` |
| amount | number | Yes | Withdrawal amount (USDT), must be ≥ 10 |
| chain | string | Yes | Target chain: `arbitrum` / `BNB Chain` / `tron` / `ton` |
| walletAddress | string | Yes | Destination wallet address |

### Example Request

```bash
curl -X POST 'https://app.ads3.ai/api/v2/withdraw' \
  -H 'open-api-key: YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "assetId": "asset_usdt_id",
    "amount": 50,
    "chain": "arbitrum",
    "walletAddress": "0xYourWalletAddress"
  }'
```

### Response Example

```json
{
  "success": true
}
```

> **Note**: Withdrawals go through a review process. Monitor status via the asset flow history API.

---

## Platform Status Reference

| Status | Description |
|--------|-------------|
| onGoing | Running, receiving ads |
| paused | Paused by user |
| auditing | Under review |
| fail | Review failed |

---

## Block Status Reference

| Status | Description |
|--------|-------------|
| onGoing | Running, receiving ads |
| paused | Paused by user |
| auditing | Under review |

---

## Billing Allocation Mode

| Mode | Description |
|------|-------------|
| fixed | Fixed USDT amount per event |
| dynamic | Percentage share of ad revenue (e.g. "70%") |

---

## Withdraw Status Reference

| Status | Description |
|--------|-------------|
| pending | Waiting to process |
| processing | In progress |
| done | Completed |
| fail | Failed |
| review | Manual review |
| cancel | Cancelled |
| rejection | Rejected |

---

## Error Handling

| HTTP Code | Description |
|-----------|-------------|
| 401 | Unauthorized - Invalid or expired Open API Key / token |
| 400 | Bad Request - Invalid parameters (e.g. missing platformId, amount ≤ 0, insufficient balance) |
| 404 | Not Found - Platform or Block not found or no permission |
| 500 | Internal Server Error |

---

## Metrics Calculation

- **CTR (Click-Through Rate)** = clicks / impressions × 100%
- **CVR (Conversion Rate)** = conversions / clicks × 100%
- **eCPM (Effective CPM)** = earn / impressions × 1000
- **Daily Average Revenue** = total earn / number of active days

---

## Security

### Never Display Full Open API Keys

When showing credentials to users:
- **open-api-key**: Show first 8 + last 4 characters: `sk_live_...xyz9`

---

## Agent Behavior

1. **Check Open API Key before calls**: Verify that open-api-key is configured
2. **Prompt for Open API Key if missing**: If Open API Key is not provided, ask user to get one from the dashboard first
3. **Never display full Open API Keys**: Only show first 8 + last 4 characters (e.g., `sk_live_...xyz9`)
4. **Get platforms first**: When user asks about blocks, first call `GET /publisher/platforms` to obtain the platformId, then call `GET /publisher/blocks`
5. **Format currency**: Display earnings with 2 decimal places and USDT suffix (e.g., `29.25 USDT`)
6. **Calculate eCPM**: When showing block performance, calculate and display eCPM alongside other metrics
7. **Trend analysis**: When showing daily summary, compare recent days to identify growth or decline trends
8. **Withdrawal flow**: Before submitting withdrawal, call `POST /withdraw/basic` to show the user the minimum amount and fees, then call `GET /user/asset/publisher` to confirm available balance, then confirm with the user before calling `POST /withdraw`
9. **Confirm before withdrawal**: Always show a summary (amount, chain, wallet address, fee) and ask for explicit confirmation before submitting a withdrawal

---

## Typical Query Flow

### Check Performance
1. **List platforms** → `GET /publisher/platforms`
2. **List blocks for a platform** → `GET /publisher/blocks?platformId=<id>`
3. **View daily breakdown for a block** → `GET /publisher/block/summary/<blockId>`

### Withdraw Earnings
1. **Get withdrawal config** → `POST /withdraw/basic` (check min amount and fees)
2. **Check balance** → `GET /user/asset/publisher`
3. **Confirm with user** → show summary of amount, chain, destination wallet
4. **Submit withdrawal** → `POST /withdraw`
5. **Track status** → `GET /user/asset/advertiser/flow?flowType=Withdraw`

---

## How to Get Open API Key

Users can obtain an Open API Key by:

1. Login to https://app.ads3.ai/ads
2. Navigate to **Account** → **Open API Keys** page
3. Click **Create Open API Key** button
4. Enter a key name (e.g., "My Skill Key")
5. Click create and **immediately copy and save** the Open API Key
6. **Note**: Open API Key is only shown once upon creation, please save it securely

### Open API Key Format

```
sk_live_xxxx...xxxx
```

---

## Notes

1. All amounts are in USDT
2. Block Summary data is sorted by date descending (newest first)
3. Newly created platforms and blocks require review before receiving ads
4. Revenue is settled **T+1**: today's earnings are credited to your account the following day
5. Minimum withdrawal: **10 USDT**; current fee: **0 USDT** (free)
6. Each user can create up to 5 Open API Keys
7. Open API Keys support expiration time, or can be set to never expire
