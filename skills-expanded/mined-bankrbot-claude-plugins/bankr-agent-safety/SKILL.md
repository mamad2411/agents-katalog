---
name: Bankr Agent - Safety & Access Control
description: This skill should be used when the user asks about "API key security", "read-only key", "IP whitelist", "rate limits", "dedicated wallet", "agent wallet", "key rotation", "access control", or any safety, security, or access control topic related to Bankr.
version: 1.0.0
---

# Safety & Access Control

Comprehensive safety guidance for using the Bankr API and CLI.

## API Key Types

Bankr uses a single key format (`bk_...`) with capability flags:

| Flag | Controls | Default |
|------|----------|---------|
| `agentApiEnabled` | `/agent/*` endpoints | false |
| `llmGatewayEnabled` | LLM Gateway at `llm.bankr.bot` | false |
| `readOnly` | Restricts agent to read-only tools | false |

Manage flags at [bankr.bot/api](https://bankr.bot/api).

## Read-Only API Keys

When `readOnly: true`, all write tools are filtered from the agent session:

**Allowed:** Balances, prices, analytics, portfolio, research
**Blocked:** Swaps, transfers, NFT purchases, staking, orders, token launches, leverage, Polymarket bets, claims

The `/agent/sign` and `/agent/submit` endpoints return 403 for read-only keys.

## IP Whitelisting

Set `allowedIps` on your API key to restrict usage to specific IPs. Requests from non-whitelisted IPs are rejected with 403.

- Empty array = all IPs allowed (default)
- Non-empty array = only listed IPs can use the key

## Dedicated Agent Wallet

When building autonomous agents, create a **separate Bankr account** rather than using your personal wallet:

- **Limited exposure** — compromised key only exposes agent wallet funds
- **Clear accounting** — agent transactions isolated from personal activity
- **Independent controls** — apply stricter access controls without affecting personal use
- **Easy revocation** — disable agent account without disrupting primary wallet

### Recommended Funding

| Chain | Gas Buffer | Trading Capital |
|-------|-----------|-----------------|
| Base | 0.01-0.05 ETH | As needed |
| Polygon | 5-10 MATIC | As needed |
| Ethereum | 0.05-0.1 ETH | As needed |
| Solana | 0.1-0.5 SOL | As needed |

## Rate Limits

| Tier | Daily Limit |
|------|-------------|
| Standard | 100 messages/day |
| Bankr Club | 1,000 messages/day |
| Custom | Set per API key |

Reset window is 24 hours from first message (rolling), not midnight.

## Key Management

- Store keys in environment variables (`BANKR_API_KEY`, `BANKR_LLM_KEY`), never in source code
- Add `~/.bankr/` and `.env` to `.gitignore`
- Rotate keys periodically at [bankr.bot/api](https://bankr.bot/api)
- Revoke immediately if compromised
- Use separate keys for Agent API vs LLM Gateway if needed

## Transaction Safety

- **Test first** — small amounts on Base/Polygon before scaling
- **Verify recipients** — double-check addresses before transfers
- **Gas buffer** — keep enough native tokens for gas
- **Immediate execution** — `/agent/submit` executes with no confirmation prompt
- **Understand calldata** — verify trusted source for arbitrary transactions

## Pre-Deployment Checklist

- Use a dedicated agent wallet, not your personal account
- Fund with limited amounts appropriate to purpose
- Set read-only if agent only queries data
- Configure IP whitelisting for server-side agents
- Store keys in environment variables
- Test with small amounts first
- Implement error handling for rate limits (429) and access control (403)
