---
name: cryptorefills-buy
description: "Buy gift cards, top up phones, and get travel eSIMs with Bitcoin, Lightning, Ethereum, Solana, USDC, USDT, or 15+ other cryptos on Base, Polygon, Arbitrum, Tron, and more. No account or CLI install — MCP-native. 10,500+ brands, 180+ countries."
compatibility: "Requires MCP client connected to https://api.cryptorefills.com/mcp/http. Header: User-Agent: Cryptorefills-MCP/1.0. Crypto wallet for payment. No account or API key needed."
metadata:
  author: cryptorefills
  version: "1.2.0"
  homepage: "https://www.cryptorefills.com"
  repository: "https://github.com/cryptorefills/agents"
---

# Cryptorefills Buy — MCP Purchase Workflow

Full purchase lifecycle: search, price, validate, order, pay, track delivery. Supports all crypto payment methods, fixed and range-based products, multi-product carts, and interactive guided purchasing.

**For browse-only**, follow the instructions in **cryptorefills-catalog**.
**For autonomous agent purchases with USDC on Base** (no account), follow **cryptorefills-x402** instead.

When the user needs autonomous wallet-based purchasing without human payment interaction, switch to the cryptorefills-x402 skill instructions.

## When to Activate

- User wants to buy a gift card, top up a phone, or get an eSIM with crypto
- User mentions paying with Bitcoin, Lightning, Ethereum, Solana, USDC, USDT, Litecoin, Dogecoin, TON, SUI, or other cryptocurrency
- User wants to place an order or complete a purchase on Cryptorefills
- User needs help checking order status or tracking delivery
- Keywords: "buy gift card with crypto", "pay with bitcoin", "pay with ethereum", "pay with solana", "purchase esim", "top up phone with USDC", "buy with USDT", "pay with litecoin", "pay with dogecoin"

## Requirements

- MCP client connected to `https://api.cryptorefills.com/mcp/http`
- Required header: `User-Agent: Cryptorefills-MCP/1.0`
- Crypto wallet for payment
- No Cryptorefills account or API key needed

To configure the MCP connection in Claude Code:
```json
{
  "mcpServers": {
    "cryptorefills": {
      "url": "https://api.cryptorefills.com/mcp/http",
      "headers": { "User-Agent": "Cryptorefills-MCP/1.0" }
    }
  }
}
```

## Spending Safeguards

**Always confirm before purchasing.** Present product name, denomination, price, and payment method — wait for explicit user approval before calling `createOrder`.

- **Set a per-session spending limit** (default: $100 max per session, $50 max per transaction — increase only if the user explicitly requests it) and track cumulative spend across orders
- **Verify the quoted price** from `getProductPrice` before proceeding to `createOrder`
- Digital goods are **non-refundable** once delivered
- Gift card codes are **cash-like** — store securely, never share publicly or write to files
- Keep codes in memory until the user redeems them
- Log every purchase: order ID, product, amount, payment method
- Use a dedicated wallet with limited balance for agent-initiated purchases
- Terms: https://www.cryptorefills.com/terms/

## Core Workflow

```
searchProducts → getProductPrice → validateOrder → createOrder → getOrderStatus
         │                                              │
         └── or use purchaseElicitation ────────────────┘
```

Two paths to purchase:

1. **Manual flow** — Search → price → validate → create → track (full control)
2. **Guided flow** — `purchaseElicitation` walks through the purchase interactively (recommended for conversational agents)

## Step-by-Step: Manual Flow

### 1. Search / Discover

Use `searchProducts` or `listBrands` to find products.

```
searchProducts(country_code="US", q="Netflix")
```

**Note**: The search parameter is `q` (not `query`), and language is `lang` (not `language`).

Country codes must be **uppercase** Alpha-2 ISO (`US`, `IT`, `BR`). Note: the x402 skill uses lowercase — different endpoint.

### 2. Get Price

**Fixed-denomination products** (`is_dynamic: false`): Price is already in the `listProductsForCountry` response (`coin_amount` field). No extra call needed.

**Range-based products** (`is_dynamic: true`): Use `getProductPrice` to get the price for a specific amount within the range.

```
getProductPrice(brand_name="Amazon.com", country_code="US", face_value=75, coin="USDC")
```

`face_value` is a number (`75`), not a string. Returns `coin_amount` with the exact crypto price.

### 3. Validate Order

Use `validateOrder` before creating. Both `validateOrder` and `createOrder` use a `body` wrapper with `payment` and `deliveries`.

```
validateOrder(body={
  payment: {type: "via", payment_via: "USER_WALLET", coin: "BTC", network: "Mainnet"},
  deliveries: [{
    denomination: "25 USD",
    brand_name: "Steam",
    beneficiary_account: "user@example.com",
    country_code: "US"
  }]
})
```

Key fields:
- `payment.type` — always `"via"` for crypto payments
- `payment.payment_via` — from `getPaymentViasWithCurrencies` (e.g., `"USER_WALLET"`)
- `payment.coin` — cryptocurrency (e.g., `"BTC"`, `"USDC"`)
- `payment.network` — use the exact string from `getPaymentViasWithCurrencies`. Common values:

| Coin | `network` value |
|------|----------------|
| BTC | `Mainnet` |
| ETH | `ETH Mainnet` |
| USDC | `Base`, `Polygon (Matic)`, `Solana`, `Arbitrum` |
| USDT | `Polygon (Matic)`, `Tron` |
| SOL | `Solana` |
- `deliveries[].denomination` — for fixed products: exact string from `listProductsForCountry` (e.g., `"25 USD"`). For range products: the literal string `"range"` (plus `product_value` with the desired amount)
- `deliveries[].brand_name` — exact brand name from `listBrands`
- `deliveries[].beneficiary_account` — email for gift cards/eSIMs, E.164 phone for mobile recharge
- `deliveries[].country_code` — uppercase Alpha-2

Catches errors early: invalid phone, out-of-range amount, unavailable product, minimum order amount.

### 4. Create Order

Same `body` schema as `validateOrder`, plus `user.email` is required.

```
createOrder(body={
  user: {email: "buyer@example.com"},
  payment: {type: "via", payment_via: "USER_WALLET", coin: "BTC", network: "Mainnet"},
  deliveries: [{
    denomination: "25 USD",
    brand_name: "Steam",
    beneficiary_account: "user@example.com",
    country_code: "US"
  }]
})
```

Returns: `order_id`, `wallet_address`, `coin_amount`, `qr_url`, `qr_text` (payment URI), `payment_state`, `order_state`.

**Presenting payment to the user**: In text-only environments, present the `qr_text` payment URI (e.g., `bitcoin:3EFu...?amount=0.00038`) — wallets can parse it directly. In rich environments, link to or render the `qr_url` image.

**Multi-product orders**: Include up to 10 items in the `deliveries` array. Each can be a different brand/country/delivery type.

### 5. Track Order

Poll `getOrderStatus` with the order ID.

- **Poll interval**: Every 30 seconds
- **Payment states**: `WalletCreated` → `PaymentRequested` → `PaymentReceived` (or `Expired`)
- **Order states**: `WaitingForPayment` → `Done` (success) / `Expired` / `Canceled` / `WaitingForManualAction`
- **Payment windows**: Lightning invoices expire in ~15 minutes. On-chain payments expire in ~60–180 minutes depending on method.

Stop polling when order reaches a terminal state.

### 6. Deliver

When order state is `Done`:
- **Gift cards**: Code/PIN in `deliverable.pin_code`. If it starts with `http`/`https`, it's a URL to visit. Plain text is a manual redemption code.
- **Mobile top-ups**: Applied automatically to the phone number. No code to deliver.
- **eSIMs**: QR code and activation instructions in order details.

## Worked Examples (3 Product Types)

### Example A: Gift Card — Steam $25 US (BTC)

```
1. searchProducts(country_code="US", q="Steam")
   → finds brand "Steam", category "games"

2. listProductsForCountry(country_code="US", brand_name="Steam", coin="BTC")
   → products: [{product_id: "a300c244-...", denomination: "25 USD", coin_amount: "0.00038", is_dynamic: false}]

3. validateOrder(body={
     payment: {type: "via", payment_via: "USER_WALLET", coin: "BTC", network: "Mainnet"},
     deliveries: [{denomination: "25 USD", brand_name: "Steam", beneficiary_account: "gamer@email.com", country_code: "US"}]
   })
   → coin_amount: "0.00038", problems: [] (valid)

4. createOrder(body={
     user: {email: "buyer@email.com"},
     payment: {type: "via", payment_via: "USER_WALLET", coin: "BTC", network: "Mainnet"},
     deliveries: [{denomination: "25 USD", brand_name: "Steam", beneficiary_account: "gamer@email.com", country_code: "US"}]
   })
   → order_id: "e054...", wallet_address: "3EFu...", coin_amount: "0.00038", qr_text: "bitcoin:3EFu...?amount=0.00038"

5. getOrderStatus(order_id="e054...")
   → payment_state: "PaymentRequested", order_state: "WaitingForPayment"
```

### Example A2: Range Gift Card — Amazon.com $50 US (USDC on Base)

```
1. searchProducts(country_code="US", q="Amazon")
   → finds brand "Amazon.com", is_dynamic: true, range $5–$500

2. getProductPrice(brand_name="Amazon.com", country_code="US", face_value=50, coin="USDC")
   → coin_amount: "51.08", product_id: "5549e92e-..."

3. validateOrder(body={
     payment: {type: "via", payment_via: "USER_WALLET", coin: "USDC", network: "Base"},
     deliveries: [{denomination: "range", brand_name: "Amazon.com", beneficiary_account: "user@email.com", country_code: "US", product_value: "50"}]
   })
   → coin_amount: "51.08", problems: [] (valid)
   → Note: denomination is "range" (literal string), product_value is "50" (desired amount)

4. createOrder(body={
     user: {email: "buyer@email.com"},
     payment: {type: "via", payment_via: "USER_WALLET", coin: "USDC", network: "Base"},
     deliveries: [{denomination: "range", brand_name: "Amazon.com", beneficiary_account: "user@email.com", country_code: "US", product_value: "50"}]
   })
   → order_id, wallet_address (USDC on Base), coin_amount: "51.08"
```

### Example B: Mobile Top-up — Claro 15 BRL Brazil (USDC on Base)

```
1. searchProducts(country_code="BR", q="Claro")
   → finds brand "Claro Credits", category "mobile_credits"

2. listProductsForCountry(country_code="BR", brand_name="Claro Credits", coin="USDC")
   → products: [{denomination: "15 BRL", delivery_type: "by_phone", is_dynamic: false}]

3. validateOrder(body={
     payment: {type: "via", payment_via: "USER_WALLET", coin: "USDC", network: "Base"},
     deliveries: [{denomination: "15 BRL", brand_name: "Claro Credits", beneficiary_account: "+5511999887766", country_code: "BR"}]
   })
   → Note: beneficiary_account is the E.164 phone number (not email)

4. createOrder(body={
     user: {email: "buyer@email.com"},
     payment: {type: "via", payment_via: "USER_WALLET", coin: "USDC", network: "Base"},
     deliveries: [{denomination: "15 BRL", brand_name: "Claro Credits", beneficiary_account: "+5511999887766", country_code: "BR"}]
   })
   → order_id, wallet_address (USDC on Base), coin_amount
```

### Example C: eSIM — Italy data plan (ETH)

```
1. searchProducts(country_code="IT", q="eSIM")
   → finds brand "eSIM", category "e-sim"

2. listProductsForCountry(country_code="IT", brand_name="eSIM", coin="ETH")
   → products: [{denomination: "1 GB 7 days", delivery_type: "by_email", is_dynamic: false}]

3. validateOrder(body={
     payment: {type: "via", payment_via: "USER_WALLET", coin: "ETH", network: "ETH Mainnet"},
     deliveries: [{denomination: "1 GB 7 days", brand_name: "eSIM", beneficiary_account: "traveler@email.com", country_code: "IT"}]
   })
   → Note: denomination is "1 GB 7 days" (exact string from listProductsForCountry), beneficiary is email

4. createOrder(body={
     user: {email: "buyer@email.com"},
     payment: {type: "via", payment_via: "USER_WALLET", coin: "ETH", network: "ETH Mainnet"},
     deliveries: [{denomination: "1 GB 7 days", brand_name: "eSIM", beneficiary_account: "traveler@email.com", country_code: "IT"}]
   })
   → order_id, wallet_address (ETH), coin_amount, qr_text
```

## Step-by-Step: Guided Elicitation

`purchaseElicitation` is an interactive, stateful tool that guides the agent through the entire purchase. Ideal for conversational UIs.

1. Call `purchaseElicitation` with empty body `{}` (optionally pass `lang` for localized prompts) — receive a `session_token`
2. The server returns a question (e.g., "What country?", "Which brand?", "What denomination?")
3. Pass the user's answer back with the `session_token`
4. Repeat until `status` equals `complete` (order created) or `error`
5. Use `action: "back"` to revert a step if the user changes their mind

The elicitation handles product selection, denomination, delivery info, and payment method selection internally. It's the simplest path from intent to purchase.

## Critical Gotchas

- **Phone numbers**: Must be E.164 format — `+` prefix, country code, number, no spaces or dashes
- **Country codes**: **Uppercase** for MCP tools (`US`, not `us`). The x402 skill uses lowercase
- **Country match**: Product country must match where the recipient will redeem
- **Range amounts**: Must fall within `min_value` and `max_value`. Out-of-bounds amounts are rejected
- **Validate first**: Always call `validateOrder` before `createOrder` to catch errors
- **Payment timeout**: Lightning ~15 min, on-chain ~60–180 min. Create a new order if expired
- **WaitingForManualAction**: Means Cryptorefills support is reviewing — inform the user and wait
- **Cart limit**: Maximum 10 items per `createOrder` call. Split larger orders into multiple calls
- **Currency in pricing**: Prices quoted in fiat; payment in crypto at locked exchange rate

## References

Load references only when you need deeper detail than what's in this skill file.

| File | Load when... | Content |
|------|-------------|---------|
| `references/mcp-tools.md` | You need exact parameter schemas for a specific MCP tool call | All 10 MCP tool signatures with parameters |
| `references/payment-methods.md` | User asks about specific chains, networks, or payment routing | Supported cryptocurrencies, chains, payment flow |
| `references/order-lifecycle.md` | Order enters an unexpected state or you need delivery/polling details | Order and payment state machines, delivery types |
| `references/troubleshooting.md` | A tool call returns an error or order is stuck | Common errors, recovery steps |
