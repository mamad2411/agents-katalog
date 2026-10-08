---
name: access0x1-rail
description: >-
  Operate the Access0x1 payments rail from an AI agent via the @access0x1/mcp
  server. Use when an assistant needs to discover which chains the rail runs on,
  read a chain's router/USDC/feed addresses, look up a merchant, check whether a
  customer's payment has landed before releasing a service, build a hosted
  checkout link, or make a budget-scoped agent payment. Teaches the discover →
  look up → verify → act loop and when to trust vs. conservatively degrade.
---

# Operating the Access0x1 rail

The `@access0x1/mcp` server is your toolbox for the Access0x1 payments rail. Its
one rule shapes everything: **never assume a chain address from memory.** Every
router, USDC, and price-feed address is read from the rail's manifest at runtime,
so the addresses you act on are always the ones the rail actually published — not
a stale value from training data or a copy-paste.

## The loop

Work in this order. Each step narrows what you act on and gives you the proof to
act honestly.

1. **Discover chains — `list_chains`.** Start here. It returns every chain the
   rail is deployed on with its id, name, router address, and whether the manifest
   asserts the contracts are source-verified. Never name a chain or an address the
   list did not give you.
2. **Read the chain's facts — `chain_facts(chainId)`.** Get the router, settlement
   USDC, native/USD and USDC/USD feeds, an explorer base, and an RPC — all from the
   manifest. A field the manifest does not carry comes back `null`; treat `null` as
   "the rail does not publish this," never as a cue to fill it in yourself.
3. **Look up the merchant — `merchant_lookup(merchantId | ownerAddress)`.**
   Resolve who you are dealing with and their indexed running totals.
4. **Verify indexed state before you act — `verify_payment(merchantId, minUsd?,
   maxAgeSeconds?)`.** This is the gate before releasing a paid service. It answers
   "has a qualifying payment landed?" from the index and returns a typed verdict
   plus the reasoning behind it.
5. **Act.** Either hand the buyer a `checkout_link(merchantId, amountUsd?)`, or —
   for autonomous spend — call `agent_pay_request(merchantId, usdAmount,
   resourceUrl)`, which forwards to the rail's own budgeted pay route.

## When to trust, and when to degrade

Every indexed read (`merchant_lookup`, `merchant_payments`, `network_leaderboard`,
`verify_payment`) carries two honesty signals. Read them before you rely on a
number:

- **`asOfBlock`** — the indexer's synced block height. Always label a count "as of
  block N." A number without a block is a number you cannot stand behind.
- **`indexingHealthy` / `hasIndexingErrors`** — whether the index is trustworthy
  right now.

`verify_payment` already bakes the conservative rule in, so follow its verdict:

- **Release the service only when `verified` is `true` AND `indexingHealthy` is
  `true`.** Both must hold.
- **Withhold on any degradation.** A failed read, `hasIndexingErrors`, a missing
  `asOfBlock`, or a merchant with no indexed history all resolve to `verified:
  false`. The `reasoning` array tells you exactly which one — surface it to the
  user instead of guessing.
- **Absent data is never goodwill.** The tool defaults to "not verified," so an
  indexer that is behind or erroring can never read as a cleared payment.

## Dormant capabilities are not failures

Some tools depend on optional configuration:

- The indexed-history tools need `ACCESS0X1_SUBGRAPH_URL`. Without it they return
  `status: "dormant"` — the capability is absent, not broken. Proceed as though
  you have no indexed opinion rather than treating it as an error.
- `checkout_link` and `agent_pay_request` need `ACCESS0X1_WEB_BASE_URL` and report
  dormant the same way when it is unset.

A `dormant` result means "this deployment did not turn this on." An `isError`
result means "this capability is configured but this specific call could not
complete" — those are different, and you should tell the user which one happened.

## Keys and money

This server holds no wallet and no keys. `agent_pay_request` only shapes and
forwards a request to the rail's `/api/agent/pay` route, which owns the signer, the
spend meter, the URL allowlist, and the caller-auth gate. You are asking the rail
to spend within its own budget — you are not spending directly. Treat a payment as
a real side effect: confirm the amount and the merchant with the user first.

## A worked example: a booking assistant

A booking assistant confirming a reservation that was paid on-chain:

1. `list_chains` → confirm the rail covers the chain the customer paid on.
2. `merchant_lookup({ merchantId: "49" })` → confirm the merchant exists and read
   their totals.
3. `verify_payment({ merchantId: "49", minUsd: 25, maxAgeSeconds: 3600 })` → did a
   payment of at least $25 land within the last hour, on a healthy index?
   - `verified: true`, `indexingHealthy: true` → confirm the booking, cite the
     block: "Payment confirmed as of block N."
   - anything else → do not confirm; read back the `reasoning` line that failed and
     ask the customer to wait for the index to catch up or to complete payment.
4. To collect a new charge instead, `checkout_link({ merchantId: "49", amountUsd:
   25 })` and hand the buyer the link.
