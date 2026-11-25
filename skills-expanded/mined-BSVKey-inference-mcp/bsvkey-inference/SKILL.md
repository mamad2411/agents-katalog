---
name: bsvkey-inference
description: Use when an agent needs to pay PER TOKEN for Claude or Grok inference settled in BSV micropayments — buying LLM calls without a subscription, account, or credit card, through the hosted inference.bsvkey.com gateway. Triggers on "pay per token", "BSV inference", "micropayment inference", "buy an LLM call with bitcoin", "metered inference", "pay-as-you-go LLM", "settle inference on-chain", "HTTP 402 inference".
---

# BSV Inference — pay-per-token LLM calls, settled in BSV

An OpenAI-compatible gateway that meters every token and settles in BSV
micropayments. An agent prepays a channel once, then calls `infer` as many times
as it wants — each call metered per token and drawn from the channel balance. No
subscription, no account, no card. Models: Claude (haiku/sonnet/opus) and Grok
(grok-4.3 fast, grok-4.6), with optional live web search.

Install it as an MCP server (see README.md) — this skill assumes those four tools
are available: `list_models`, `open_channel`, `infer`, `channel_balance`, `x402_infer`.

`x402_infer` is an alternative to `infer`: instead of a prepaid channel, it pays for a
single call in BSV via x402, using a funded key (`wif` arg or `BSVKEY_WIF`). No channel setup.

## When to use
- The user/agent wants to buy inference on demand and pay only for what it uses.
- Micropayment / per-token billing is preferred over a monthly plan.
- Settlement in BSV (or an on-chain, account-free payment) is desired.

## How it works (the flow)
1. **`list_models`** — no key needed. Returns live per-1,000-token prices in
   satoshis (they float against the live BSV/USD rate) plus which models are
   available. Use it to pick a model or a policy (`auto` = cheapest capable).
2. **Fund a channel once.** Funding is a real BSV payment a wallet must sign, so
   it's done at the website, not by the agent. Call **`open_channel`** for the
   URL + steps: open `https://inference.bsvkey.com`, fund with a BRC-100 wallet
   (or load a key in-page), and copy the returned key `channelId:channelSecret`.
   Put it in `BSVKEY_API_KEY` (or pass `apiKey` to `infer`).
3. **`infer`** — run inference, paid per token from the channel. Args: `prompt`,
   `model` (default `auto`), optional `system`, `maxTokens`, `webSearch`. Returns
   the completion plus a receipt: `charge` (sats), `routedTo`, `balanceSatsAfter`,
   and `truncated` (true if a long web search was cut at the host time limit but
   still billed).
4. **`channel_balance`** — check remaining balance, spend, and request count.

## Notes for the agent
- Payments are REAL BSV. Treat channel funds like money: fund a small amount, and
  top up the SAME channel when it runs low with `POST /v1/channels/<channelId>/topup`
  (header `X-BSV-Channel-Secret`, body `{addSats}` -> 402 quote, then repeat with
  the signed payment), or open a fresh channel. A top-up raises the channel's
  `fundedSats`, so later receipts carry the new total.
- `auto` routing picks the cheapest capable model; name a model explicitly
  (`claude-sonnet-5`, `grok-4.3`, …) when quality or a specific provider matters.
- `webSearch: true` adds a small per-search fee and lets the model use live web
  data; grok-4.6 web searches can be slow and may be truncated (still billed).
- To point at a self-hosted deployment, set `BSVKEY_BASE_URL`.
