---
name: int-asaas
description: "Asaas payment platform integration via API v3. Manage payments (Pix, boleto, credit card), customers, subscriptions, transfers, balance, and marketplace subaccounts. Use when users ask about payment collection, billing automation, Pix, boleto, subscriptions, or financial transfers via Asaas. Integração Asaas: cobranças, clientes, assinaturas, Pix, boleto."
---

# Asaas Payment Skill

Integration with Asaas billing platform via REST API v3.

## When to use

- Create or query payment charges (Pix, boleto, credit card)
- Manage customers in Asaas
- Create or cancel recurring subscriptions
- Check account balance or initiate Pix transfers
- Generate Pix QR codes or boleto digitable lines
- Create marketplace subaccounts for split payments
- List webhook events for payment confirmations

## Setup

Requires environment variables:

```bash
export ASAAS_API_KEY="your_api_key_here"
export ASAAS_SANDBOX="true"   # set to "false" for production
```

### How to obtain the API key

1. Log in to https://www.asaas.com (or https://sandbox.asaas.com for testing)
2. Go to Account Settings → Integrations → API Key
3. Copy the key — it starts with `$aact_` in production

**Auth header used in all requests:**
```
access_token: ${ASAAS_API_KEY}
```

---

## Base URL

| Environment | URL |
|-------------|-----|
| Production | `https://api.asaas.com/v3` |
| Sandbox | `https://sandbox.asaas.com/api/v3` |

Select based on `ASAAS_SANDBOX` env var. **Default is sandbox (safe).**

---

## Enums

### billingType
| Value | Description |
|-------|-------------|
| `BOLETO` | Bank slip |
| `CREDIT_CARD` | Credit card |
| `PIX` | Pix instant payment |
| `UNDEFINED` | Any method (customer chooses) |

### Payment status
| Value | Description |
|-------|-------------|
| `PENDING` | Awaiting payment |
| `RECEIVED` | Payment received |
| `CONFIRMED` | Payment confirmed |
| `OVERDUE` | Past due date |
| `REFUNDED` | Refunded |
| `RECEIVED_IN_CASH` | Received in cash |
| `REFUND_REQUESTED` | Refund requested |
| `CHARGEBACK_REQUESTED` | Chargeback requested |
| `AWAITING_CHARGEBACK_REVERSAL` | Awaiting chargeback reversal |
| `DUNNING_REQUESTED` | Dunning in progress |
| `DUNNING_RECEIVED` | Dunning received |
| `AWAITING_RISK_ANALYSIS` | Under risk analysis |

### Subscription cycle
`WEEKLY` | `BIWEEKLY` | `MONTHLY` | `QUARTERLY` | `SEMIANNUALLY` | `YEARLY`

### Subscription status
`ACTIVE` | `INACTIVE` | `EXPIRED`

### Pix key type
`CPF` | `CNPJ` | `EMAIL` | `PHONE` | `EVP`

### Company type (subaccounts)
`MEI` | `LIMITED` | `INDIVIDUAL` | `ASSOCIATION`

---

## Format Rules

| Field | Format | Example |
|-------|--------|---------|
| CPF | 11 digits, no dashes | `12345678901` |
| CNPJ | 14 digits, no dashes | `12345678000199` |
| CEP | 8 digits, no dashes | `30140071` |
| Dates | ISO `YYYY-MM-DD` | `2026-04-10` |
| Amounts | BRL float | `99.90` |
| IDs | Prefixed strings | `cus_xxx`, `pay_xxx`, `sub_xxx` |

---

## Payments

### Create payment

```bash
curl -s -X POST \
  "${BASE_URL}/payments" \
  -H "access_token: ${ASAAS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "customer": "cus_000000000001",
    "billingType": "PIX",
    "value": 150.00,
    "dueDate": "2026-04-20",
    "description": "Monthly service fee"
  }'
```

**Body fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `customer` | string | yes | Customer ID (`cus_xxx`) |
| `billingType` | string | yes | `BOLETO`, `CREDIT_CARD`, `PIX`, `UNDEFINED` |
| `value` | number | yes | Amount in BRL (must be > 0) |
| `dueDate` | string | yes | Due date `YYYY-MM-DD` |
| `description` | string | no | Payment description |

### Get payment

```bash
curl -s -X GET \
  "${BASE_URL}/payments/pay_000000000001" \
  -H "access_token: ${ASAAS_API_KEY}"
```

### List payments

```bash
curl -s -X GET \
  "${BASE_URL}/payments?customer=cus_000000000001&status=PENDING&limit=10&offset=0" \
  -H "access_token: ${ASAAS_API_KEY}"
```

**Query params:**
| Param | Type | Description |
|-------|------|-------------|
| `customer` | string | Filter by customer ID |
| `status` | string | Filter by payment status |
| `limit` | number | Results per page (default 10) |
| `offset` | number | Pagination offset |

### Get Pix QR code

```bash
curl -s -X GET \
  "${BASE_URL}/payments/pay_000000000001/pixQrCode" \
  -H "access_token: ${ASAAS_API_KEY}"
```

Returns `payload` (copy-paste Pix string) and `encodedImage` (base64 PNG).

### Get boleto

```bash
curl -s -X GET \
  "${BASE_URL}/payments/pay_000000000001/identificationField" \
  -H "access_token: ${ASAAS_API_KEY}"
```

Returns `identificationField` (digitable line) and barcode.

### Get installments

```bash
curl -s -X GET \
  "${BASE_URL}/payments/pay_000000000001/installments" \
  -H "access_token: ${ASAAS_API_KEY}"
```

---

## Customers

### Create customer

```bash
curl -s -X POST \
  "${BASE_URL}/customers" \
  -H "access_token: ${ASAAS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João da Silva",
    "cpfCnpj": "12345678901",
    "email": "joao@email.com",
    "phone": "31999990000"
  }'
```

**Body fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | yes | Customer name |
| `cpfCnpj` | string | yes | CPF (11 digits) or CNPJ (14 digits), numbers only |
| `email` | string | no | Valid email address |
| `phone` | string | no | Phone number |

### List customers

```bash
curl -s -X GET \
  "${BASE_URL}/customers?name=João&limit=20" \
  -H "access_token: ${ASAAS_API_KEY}"
```

**Query params:** `name`, `cpfCnpj`, `limit`

---

## Subscriptions

### Create subscription

```bash
curl -s -X POST \
  "${BASE_URL}/subscriptions" \
  -H "access_token: ${ASAAS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "customer": "cus_000000000001",
    "billingType": "BOLETO",
    "value": 99.90,
    "cycle": "MONTHLY",
    "nextDueDate": "2026-05-01",
    "description": "Pro plan"
  }'
```

**Body fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `customer` | string | yes | Customer ID |
| `billingType` | string | yes | `BOLETO`, `CREDIT_CARD`, `PIX` |
| `value` | number | yes | Amount per cycle (must be > 0) |
| `cycle` | string | yes | Billing cycle |
| `nextDueDate` | string | yes | First due date `YYYY-MM-DD` |
| `description` | string | no | Subscription description |

### List subscriptions

```bash
curl -s -X GET \
  "${BASE_URL}/subscriptions?customer=cus_000000000001&status=ACTIVE&limit=10" \
  -H "access_token: ${ASAAS_API_KEY}"
```

### Cancel subscription

```bash
curl -s -X DELETE \
  "${BASE_URL}/subscriptions/sub_000000000001" \
  -H "access_token: ${ASAAS_API_KEY}"
```

---

## Financial

### Get balance

```bash
curl -s -X GET \
  "${BASE_URL}/finance/balance" \
  -H "access_token: ${ASAAS_API_KEY}"
```

### Create transfer (Pix out / TED)

```bash
curl -s -X POST \
  "${BASE_URL}/transfers" \
  -H "access_token: ${ASAAS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "value": 250.00,
    "pixAddressKey": "joao@email.com",
    "pixAddressKeyType": "EMAIL",
    "description": "Supplier payment"
  }'
```

**Body fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `value` | number | yes | Amount in BRL (must be > 0) |
| `pixAddressKey` | string | no | Pix key value |
| `pixAddressKeyType` | string | no | `CPF`, `CNPJ`, `EMAIL`, `PHONE`, `EVP` |
| `description` | string | no | Transfer description |

---

## Marketplace (Split Payments)

### Create subaccount

```bash
curl -s -X POST \
  "${BASE_URL}/accounts" \
  -H "access_token: ${ASAAS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Parceiro Comercial LTDA",
    "email": "parceiro@empresa.com",
    "cpfCnpj": "12345678000199",
    "companyType": "LIMITED",
    "phone": "31999990000",
    "postalCode": "30140071",
    "address": "Rua das Flores",
    "addressNumber": "100",
    "province": "Centro"
  }'
```

**Required fields:** `name`, `email`, `cpfCnpj`

---

## Utilities

### Get webhook events

```bash
curl -s -X GET \
  "${BASE_URL}/webhook/events?event=PAYMENT_CONFIRMED&limit=10&offset=0" \
  -H "access_token: ${ASAAS_API_KEY}"
```

**Common event types:** `PAYMENT_CONFIRMED`, `PAYMENT_RECEIVED`, `PAYMENT_OVERDUE`, `TRANSFER_CREATED`, `SUBSCRIPTION_CREATED`

---

## Auth Model

- **Type:** API Key
- **Header name:** `access_token` (note: lowercase, not `Authorization`)
- **Header value:** raw API key, no `Bearer` prefix
- **Key format:** `$aact_YTU5YTE0M...` (production) or similar pattern in sandbox

## Rate Limits

- Asaas enforces rate limits per API key
- Default limit: ~120 requests/minute (see official docs for current values)
- Back off on HTTP 429; retry after the `Retry-After` header value
- Full rate limit details: https://docs.asaas.com

## Notes

- This skill is based on the MCP implementation at `workspace/projects/mcp-dev-brasil/packages/payments/asaas/src/index.ts` (mcp-dev-brasil project), which includes Zod validation for CPF/CNPJ, email, CEP, and date formats
- **Always start with `ASAAS_SANDBOX=true`** — sandbox is isolated from production funds
- For credit card payments, tokenization requires additional fields not covered here — see https://docs.asaas.com
- Webhook configuration (registering your endpoint URL) must be done in the Asaas dashboard, not via API
