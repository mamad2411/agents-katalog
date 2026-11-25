---
name: advertiser
description: |
  Advertiser data query and management tool. Query ad performance data, create and manage campaigns via Open API Key.
  Triggers: 'ad data', 'ad performance', 'advertiser', 'campaign', 'ad status', 'create ad', 'pause ad'.
metadata:
  author: ads3
  version: "1.0.2"
---

# Advertiser Skill

## Overview

Manage ad campaigns and query performance data via Open API Key.

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

## API: Get Campaign List

Get campaign list with performance data.

### Method: GET

**URL**:
```
/advertiser/campaigns
```

**Query Parameters**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| current | number | No | Page number, default 1 |
| pageSize | number | No | Items per page, default 10 |

### Example Request

```bash
curl -X GET 'https://app.ads3.ai/api/v2/advertiser/campaigns?current=1&pageSize=10' \
  -H 'open-api-key: YOUR_API_KEY'
```

### Response Example

```json
{
  "data": [
    {
      "id": "6789abc123def456",
      "name": "Campaign 2026 Q1",
      "campaignStatus": "onGoing",
      "impressions": 150000,
      "clicks": 3500,
      "conversions": 280,
      "billingType": "CPC",
      "bidding": {
        "billingType": "CPC",
        "costPer": 0.15
      },
      "budget": {
        "strategy": "daily",
        "amount": 100,
        "startTime": 1712188800000,
        "endTime": 1714780800000
      },
      "cost": 525.50,
      "ctr": 2.33,
      "cr": 8.0,
      "creator": {
        "nickName": "John",
        "balance": 1500.00
      }
    }
  ],
  "total": 15,
  "current": 1,
  "success": true
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| data[].id | string | Campaign ID |
| data[].name | string | Campaign name |
| data[].campaignStatus | string | Status: onGoing/paused/ended/auditing/reject |
| data[].impressions | number | Total impressions |
| data[].clicks | number | Total clicks |
| data[].conversions | number | Total conversions |
| data[].billingType | string | Billing type: CPA/CPC/CPM |
| data[].cost | number | Total spend (USDT) |
| data[].ctr | number | Click-through rate (%) |
| data[].cr | number | Conversion rate (%) |
| data[].creator.balance | number | Account balance (USDT) |

---

## API: Get Campaign Summary

Get daily performance summary for a campaign.

### Method: GET

**URL**:
```
/advertiser/campaign/summary/:campaignId
```

**Path Parameters**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaignId | string | Yes | Campaign ID |

**Query Parameters**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| current | number | No | Page number, default 1 |
| pageSize | number | No | Items per page, default 10 |

### Example Request

```bash
curl -X GET 'https://app.ads3.ai/api/v2/advertiser/campaign/summary/6789abc123def456?current=1&pageSize=30' \
  -H 'open-api-key: YOUR_API_KEY'
```

### Response Example

```json
{
  "data": [
    {
      "onDate": "2026-04-08",
      "impressions": 5200,
      "clicks": 125,
      "conversions": 10,
      "cost": 18.75,
      "ctr": 2.40,
      "cr": 8.0
    },
    {
      "onDate": "2026-04-07",
      "impressions": 4800,
      "clicks": 110,
      "conversions": 9,
      "cost": 16.50,
      "ctr": 2.29,
      "cr": 8.18
    }
  ],
  "total": 30,
  "current": 1,
  "success": true
}
```

---

## API: Get Campaign Detail

Get single campaign details.

### Method: GET

**URL**:
```
/ad/campaign/:campaignId
```

**Path Parameters**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaignId | string | Yes | Campaign ID |

### Example Request

```bash
curl -X GET 'https://app.ads3.ai/api/v2/ad/campaign/6789abc123def456' \
  -H 'open-api-key: YOUR_API_KEY'
```

### Response Example

```json
{
  "id": "6789abc123def456",
  "name": "Campaign 2026 Q1",
  "campaignStatus": "onGoing",
  "budget": {
    "strategy": "daily",
    "amount": 100,
    "startTime": 1712188800000,
    "endTime": 1714780800000
  },
  "targeting": {
    "includedRegions": ["South-eastern Asia"],
    "platform": "All"
  },
  "bidding": {
    "billingType": "CPC",
    "costPer": 0.15,
    "assetId": "xxx",
    "assetName": "USDT"
  },
  "ads": [
    {
      "id": "ad_001",
      "adFormat": "image",
      "text": "Join our community!",
      "brandName": "TonAI",
      "buttonText": "Learn More",
      "destination": {
        "actionType": "visit.website",
        "destinationConfig": {
          "url": "https://example.com"
        }
      }
    }
  ]
}
```

---

## API: Create Campaign

Create a new campaign.

### Method: POST

**URL**:
```
/ad/campaign
```

**Request Body**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Campaign name |
| targeting | object | Yes | Targeting settings |
| targeting.includedRegions | string[] | No | Included regions |
| targeting.excludedRegions | string[] | No | Excluded regions |
| targeting.includedLanguages | string[] | No | Included languages |
| targeting.excludedLanguages | string[] | No | Excluded languages |
| targeting.platform | string | No | Platform: All/Android/iOS |
| targeting.telegramPremium | boolean | No | TG Premium users only |
| targeting.isHighValueUser | boolean | No | High value users only |
| targeting.userLinkedTonWallet | boolean | No | TON wallet connected users only |
| budget | object | Yes | Budget settings |
| budget.strategy | string | Yes | Strategy: daily |
| budget.amount | number | Yes | Daily budget (USDT) |
| budget.total | number | No | Total budget (USDT) |
| budget.startTime | number | Yes | Start timestamp (ms) |
| budget.endTime | number | Yes | End timestamp (ms) |
| bidding | object | Yes | Bidding settings |
| bidding.billingType | string | Yes | Billing type: CPA/CPC/CPM/oCPC/oCPM |
| bidding.costPer | number | Yes | Cost per event (USDT) |
| bidding.assetId | string | Yes | Asset ID |
| bidding.assetName | string | Yes | Asset name (USDT) |
| ads | array | Yes | Ad creatives list |
| ads[].adFormat | string | Yes | Format: image/video |
| ads[].image | string | No | Ad image URL |
| ads[].popupImage | string | No | Popup image URL |
| ads[].icon | string | No | Icon URL |
| ads[].text | string | Yes | Ad copy |
| ads[].brandName | string | No | Brand name |
| ads[].buttonText | string | No | Button text |
| ads[].destination.actionType | string | Yes | Action type: visit.website/join.telegram |
| ads[].destination.destinationConfig.url | string | Yes | Destination URL |
| marketplaces | string[] | No | Marketplace IDs to target |
| apiConfigId | string | No | API verification config ID |

### Example Request

```bash
curl -X POST 'https://app.ads3.ai/api/v2/ad/campaign' \
  -H 'open-api-key: YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Spring Campaign 2026",
    "targeting": {
      "includedRegions": ["South-eastern Asia", "Eastern Asia"],
      "platform": "All"
    },
    "budget": {
      "strategy": "daily",
      "amount": 50,
      "total": 1000,
      "startTime": 1712188800000,
      "endTime": 1714780800000
    },
    "bidding": {
      "billingType": "CPC",
      "costPer": 0.1,
      "assetId": "asset_usdt_id",
      "assetName": "USDT"
    },
    "ads": [{
      "adFormat": "image",
      "popupImage": "https://cdn.example.com/ad.png",
      "icon": "https://cdn.example.com/icon.png",
      "text": "Join the revolution!",
      "brandName": "MyBrand",
      "buttonText": "Get Started",
      "destination": {
        "actionType": "visit.website",
        "destinationConfig": {
          "url": "https://myapp.com"
        }
      }
    }]
  }'
```

---

## API: Update Campaign

Update campaign configuration.

### Method: PATCH

**URL**:
```
/ad/campaign/:campaignId
```

### Example Request

```bash
curl -X PATCH 'https://app.ads3.ai/api/v2/ad/campaign/6789abc123def456' \
  -H 'open-api-key: YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Updated Campaign Name",
    "budget": {
      "strategy": "daily",
      "amount": 80,
      "startTime": 1712188800000,
      "endTime": 1714780800000
    }
  }'
```

---

## API: Pause Campaign

Pause a campaign.

### Method: PATCH

**URL**:
```
/ad/campaign/:campaignId/pause
```

### Example Request

```bash
curl -X PATCH 'https://app.ads3.ai/api/v2/ad/campaign/6789abc123def456/pause' \
  -H 'open-api-key: YOUR_API_KEY'
```

---

## API: Resume Campaign

Resume a paused campaign.

### Method: PATCH

**URL**:
```
/ad/campaign/:campaignId/resume
```

### Example Request

```bash
curl -X PATCH 'https://app.ads3.ai/api/v2/ad/campaign/6789abc123def456/resume' \
  -H 'open-api-key: YOUR_API_KEY'
```

---

## API: End Campaign

End a campaign permanently.

### Method: POST

**URL**:
```
/ad/campaign/end
```

**Request Body**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaignId | string | Yes | Campaign ID |

### Example Request

```bash
curl -X POST 'https://app.ads3.ai/api/v2/ad/campaign/end' \
  -H 'open-api-key: YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{"campaignId": "6789abc123def456"}'
```

---

## Campaign Status Reference

| Status | Description |
|--------|-------------|
| onGoing | Running |
| paused | Paused by user |
| systemPaused | Paused by system (insufficient balance, etc.) |
| ended | Ended |
| auditing | Under review |
| reject | Review rejected |
| pending | Pending |
| readyToStart | Ready to start |
| fail | Creation failed |

---

## Billing Type Reference

| Type | Description |
|------|-------------|
| CPA | Cost Per Action |
| CPC | Cost Per Click |
| CPM | Cost Per Mille (1000 impressions) |
| oCPC | Optimized CPC (smart bidding) |
| oCPM | Optimized CPM (smart bidding) |

---

## Targeting Regions Reference

| Region | Description |
|--------|-------------|
| Africa | Africa |
| Middle East | Middle East |
| South-eastern Asia | Southeast Asia |
| Europe and America | Europe and America |
| CIS | Commonwealth of Independent States |
| Eastern Asia | East Asia |
| Southern Asia | South Asia |
| Central Asia | Central Asia |
| Northern Africa | North Africa |
| Western Europe | Western Europe |
| Eastern Europe | Eastern Europe |
| Northern America | North America |
| Latin America and the Caribbean | Latin America and Caribbean |

---

## Error Handling

| HTTP Code | Description |
|-----------|-------------|
| 401 | Unauthorized - Invalid or expired token |
| 400 | Bad Request - Invalid parameters |
| 404 | Not Found - Campaign not found or no permission |
| 500 | Internal Server Error |

---

## Metrics Calculation

- **CTR (Click-Through Rate)** = clicks / impressions × 100%
- **CVR (Conversion Rate)** = conversions / clicks × 100%
- **CPA (Cost Per Action)** = cost / conversions
- **CPC (Cost Per Click)** = cost / clicks

---

## Security

### Never Display Full Open API Keys

When showing credentials to users:
- **open-api-key**: Show first 8 + last 4 characters: `sk_live_...xyz9`

---

## API: Get Recharge Wallets

Get the user's personal deposit wallet addresses for topping up account balance.

### Method: POST

**URL**:
```
/recharge/user/wallets
```

**Request Body**: None (no body required)

### Example Request

```bash
curl -X POST 'https://app.ads3.ai/api/v2/recharge/user/wallets' \
  -H 'open-api-key: YOUR_API_KEY'
```

### Response Example

```json
{
  "list": [
    {
      "chain": "bnbChain",
      "name": "BNB Chain",
      "walletAddress": "0xAbCd...1234",
      "isValid": true,
      "classify": "evm"
    },
    {
      "chain": "arbitrum",
      "name": "Arbitrum Network",
      "walletAddress": "0xEfGh...5678",
      "isValid": true,
      "classify": "evm"
    },
    {
      "chain": "tron",
      "name": "Tron Network",
      "walletAddress": "",
      "isValid": false,
      "classify": "evm"
    },
    {
      "chain": "ton",
      "name": "Ton Network",
      "walletAddress": "",
      "isValid": false,
      "classify": "ton"
    }
  ]
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| list[].chain | string | Chain identifier (e.g. `bnbChain`, `arbitrum`) |
| list[].name | string | Human-readable chain name |
| list[].walletAddress | string | User's deposit address for this chain (empty if not yet assigned) |
| list[].isValid | boolean | Whether this chain is currently supported for deposits |
| list[].classify | string | Chain type: `evm` or `ton` |

> **Note**: Only show entries where `isValid: true` and `walletAddress` is non-empty. Currently supported chains: **BNB Chain** and **Arbitrum Network**. Tron and TON are coming soon.

---

## Insufficient Balance Handling

Trigger this flow when:
- A campaign's `campaignStatus` is `systemPaused` (system paused due to insufficient balance)
- The `creator.balance` shown in campaign list is too low to sustain daily spend

### Step 1 — Retrieve and Show Deposit Addresses

Call `POST /recharge/user/wallets` and display only the entries where `isValid: true` and `walletAddress` is non-empty:

```
Your account balance is insufficient. To top up, send USDT to your deposit address:

• BNB Chain:       0xAbCd...1234
• Arbitrum Network: 0xEfGh...5678

Token: USDT only
```

> ⚠️ These addresses are shown for reference only. Do NOT ask the user to confirm or initiate the transfer through this agent. Always direct them to complete the deposit via the official dashboard (Step 2).

### Step 2 — Guide to Dashboard Deposit

Always follow Step 1 immediately with:

> To deposit, go to: **https://app.ads3.ai/ads → Account → Deposit**
>
> Select your preferred blockchain, transfer USDT to your deposit address above, and your balance will be updated within approximately 10 minutes.

---

## Agent Behavior

1. **Check Open API Key before calls**: Verify that open-api-key is configured
2. **Prompt for Open API Key if missing**: If Open API Key is not provided, ask user to get one from the dashboard first
3. **Never display full Open API Keys**: Only show first 8 + last 4 characters (e.g., `sk_live_...xyz9`)
4. **Confirm before mutations**: Before creating, pausing, or ending campaigns, show a summary and ask for confirmation
5. **Show cost implications**: When creating campaigns, calculate and display estimated daily/total spend
6. **Format numbers nicely**: Use appropriate decimal places (cost: 2, CTR/CVR: 2, counts: 0)
7. **Provide actionable insights**: After showing data, suggest optimizations if CTR < 1% or CVR < 5%
8. **Handle insufficient balance**: When `campaignStatus` is `systemPaused` or balance is low, call `POST /recharge/user/wallets`, show valid deposit addresses, then guide user to https://app.ads3.ai/ads → Account → Deposit

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
2. Timestamps use milliseconds (ms)
3. Newly created campaigns require review before running
4. Campaigns are paused by system when account balance is insufficient
5. Each user can create up to 5 Open API Keys
6. Open API Keys support expiration time, or can be set to never expire
