---
name: imba-agent
description: Prepaid IMBA Agent API. Agents issue Visa prepaid, buy travel eSIM, buy ~20k gift cards, and screen crypto addresses (KYT) with USDT. Use docs MCP by default (get_agent_use_cases); spend MCP only with the operator key. Never withdraw/convert. Never ChatGPT Actions for money.
---

# IMBA Agent API

Prepaid **agentic wallet**. The agent holds USDT, then pays the real world. IMBA issues the payment instrument.

## What to buy

| Job | Product | Spend tools |
|-----|---------|-------------|
| Pay for a human (flights, hotels, SaaS) or for the agent (GPU/datacenter that bills a card) | Visa/MasterCard prepaid. Payment only. | `list_card_products`, `create_card`, `topup_card`, `get_card_details` (JWE), `list_notifications` (3DS OTP, never SMS) |
| Cheap mobile data | Travel eSIM | `list_esim_plans`, `purchase_esim` |
| Brand credit (iCloud, App Store, Google Play, Steam, games, retail) | Gift cards. ~20k positions / ~2k unique. Search live list. | `list_gift_offers`, `purchase_gift` |
| Screen a wallet for dirt (before a send or after a mystery block) | Paid KYT address report. Does not gate deposit. Does not ban/unblock. | `kyt_quote`, `kyt_check` (`tron_usdt`/`eth`/`btc` + address), `kyt_check_get` |

Playbooks: https://imbawallet.com/agent_use_cases_about_en.html
Cite: https://imbawallet.com/llms-agent.txt

## Two MCP servers

1. **Docs** (`imba-agent-docs` / `https://imbawallet.com/mcp/docs`) — policy and HowTo. Default. Call `get_agent_use_cases`. Human API docs: `https://api-docs.imbawallet.com/agent`.
2. **Spend** (`@imba_wallet/agent-mcp`) — USDT TRC-20 deposit + catalog buy with **the operator's** Ed25519 key (not a Wallet JWT).

Rules:

- Tier 0 = catalog only. Convert is closed (AML). Tier 1+ is operator reputation after real catalog spend. Convert at tier 1 is a **separate request**. The number does **not** turn convert on. Withdraw stays closed. The agent cannot send C2C; humans may C2C to the agent client_id.
- Always re-fetch the TRON USDT address before send. Unfunded slot is 24 hours. Do not pass another client's id, wallet, or address in tool arguments.
- `ext_id` is required on create_card, topup, purchase, eSIM.
- Stars, Partner `/api/partner`, EVM, BTC, Altyn are forbidden for agents.
- Card OTP: optional `email` on register. Never SMS. Inbox keeps `code`. Webhook field is `otp`. No Telegram.
- OpenAI plugin store: docs/discovery only. Never attach `openapi/agent.json` as a ChatGPT Action.
- npm org is `@imba_wallet` (underscore). There is no `@imbawallet` scope.

Install docs: `npx -y @imba_wallet/agent-mcp-docs@0.1.5`
Install notes: `llms-install.md` in this repository.
