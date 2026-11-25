---
name: shieldz-payments
description: Accept crypto payments or sell a digital product for crypto without an account. Use when someone wants a payment link, a tip jar or donation page, to sell a file, license key or secret text, or to get paid in USDC, USDT, Bitcoin or Zcash to their own wallet.
---

# Shieldz payments

[Shieldz](https://shieldz.cash) is a non-custodial crypto payment gateway. Payments go straight to the wallet address the user gives; Shieldz never holds funds or keys. $0 platform fee. USDC and USDT on Base, Arbitrum, Optimism, Polygon and Ethereum, plus Bitcoin and Zcash.

## Connect

Remote MCP endpoint (Streamable HTTP, no auth for keyless tools): `https://shieldz.cash/mcp`

Or locally: `npx -y @shieldz/mcp`

## Keyless tools (no account, no API key)

- `create_payment_link`: one-time payment link with a shareable URL, button and QR. Needs `address` and `amount_usd`; `chain` defaults to `base`, `asset` to `USDC`.
- `create_tip_jar`: reusable pay-what-you-want page.
- `create_unlock`: sell a digital product. The buyer pays and the file link, license key or secret text is revealed automatically. Needs `address`, `price_usd`, `payload` and `aup_accepted`.
- `get_account_status`: look up a link or tip jar by its `manage_token`.

## Rules

- Ask the user for their own receiving wallet address and repeat it back before creating anything.
- Never ask for a private key or seed phrase.
- Give the user the `manage_token` from the response and tell them to keep it; it is how they check payments later.
- Pass the user's `email` only if they offer it; it lets them claim a full dashboard later.

Docs: https://shieldz.cash/agents
