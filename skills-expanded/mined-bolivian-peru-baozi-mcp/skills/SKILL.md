# Baozi Prediction Markets - SKILL.md

AI agent skill for Solana prediction markets.
76 MCP tools. Safe-by-default. Agent builds, user signs. Zero private keys.

## Quick Start

```bash
npm i -g @baozi.bet/mcp-server
npx @baozi.bet/mcp-server
```

## Identity

| Key | Value |
|-----|-------|
| Name | Baozi |
| Program | `FWyTPzm5cfJwRKzfkscxozatSxF6Qu78JQovQUwKPruJ` |
| Network | Solana Mainnet |
| Version | 5.0.0 |

## Links

| Resource | URL |
|----------|-----|
| Website | https://baozi.bet |
| npm | https://www.npmjs.com/package/@baozi.bet/mcp-server |
| GitHub | https://github.com/bolivian-peru/baozi-mcp |
| MCP Docs | https://baozi.bet/mcp |
| SKILL.md | https://baozi.bet/mcp/skill |
| Telegram | https://t.me/baozibet |
| Twitter | https://x.com/baozibet |
| Email | baozi@agentmail.to |
| Solscan | https://solscan.io/account/FWyTPzm5cfJwRKzfkscxozatSxF6Qu78JQovQUwKPruJ |

## Security Model

```
Agent → MCP Server → Unsigned Tx → User Signs → Solana
       (no keys)     (build only)   (wallet)    (on-chain)
```

**RULE: Agent NEVER touches private keys.**

## URLs (MEMORIZE)

| URL | Purpose |
|-----|---------|
| https://baozi.bet | Homepage / Official markets |
| https://baozi.bet/labs | Community markets |
| https://baozi.bet/labs/create | Create Lab market |
| https://baozi.bet/private | Private tables |
| https://baozi.bet/private/create | Create Private |
| https://baozi.bet/my-bets | User portfolio |
| https://baozi.bet/leaderboard | Rankings |
| https://baozi.bet/affiliate | Referral earnings |
| https://baozi.bet/arena | Agent Arena (competitive leaderboard) |
| https://baozi.bet/mandates | Delegated mandates |
| https://baozi.bet/agents/proof | Resolution proofs |
| https://baozi.bet/mcp | MCP documentation |
| https://baozi.bet/mcp/skill | This SKILL.md |

## Fees

| Layer | Platform | Creation | Max Creator |
|-------|----------|----------|-------------|
| Official | 2.5% | 0.01 SOL | — |
| Lab | 3.0% | 0.01 SOL | 2.0% |
| Private | 2.0% | 0.01 SOL | 1.0% |

Fees apply to **GROSS WINNINGS** (stake + profit).

**Fee Split:** `platform_fee = affiliate (1%) + creator (up to 2%) + protocol`
**Constraint:** `creator_fee + affiliate_fee ≤ platform_fee`

## Market Types

**BOOLEAN**: Yes/No outcome
- "Will BTC hit $100k?"
- Pari-mutuel (odds shift with bets)

**RACE**: Multiple outcomes (2-10)
- "Who wins the election?"
- Winner takes all

## ⚠️ MARKET CREATION RULES (CRITICAL)

### THE GOLDEN RULE
Bettors must have **NO information advantage** while betting is open.

### TYPE A - Event-based
Examples: Game result, announcement, award

**RULE: Close 24 HOURS before event**
- ✓ "Super Bowl Feb 8 6:30pm" → close Feb 7 6:30pm
- ✗ Close same day = INFO ADVANTAGE

### TYPE B - Measurement period
Examples: Weekly chart, monthly stats

**RULE: Close BEFORE period starts**
- ✓ "Netflix Top 10 Jan 6-12" → close Jan 5
- ✗ Close during/after = INFO ADVANTAGE

### VALIDATION CHECKLIST
- □ Objective outcome? If NO → REJECT
- □ Data source specified? If NO → REJECT
- □ Info advantage possible? If YES → REJECT
- □ Future event/period? If NO → REJECT

### APPROVED DATA SOURCES

| Category | Primary | Backup |
|----------|---------|--------|
| Crypto | CoinGecko | CoinMarketCap |
| Sports | Official league | ESPN |
| Charts | Netflix/Billboard | FlixPatrol |
| Economic | BLS.gov / Fed | FRED |

## Most Used Tools

### 1. list_markets
```json
{"name":"list_markets","arguments":{"layer":"Lab","status":"Active"}}
```

### 2. get_quote
```json
{"name":"get_quote","arguments":{"market":"PDA","side":"Yes","amount":1.0}}
```

### 3. build_bet_transaction
```json
{"name":"build_bet_transaction","arguments":{
  "market":"PDA",
  "outcome":"yes",
  "amount_sol":1.0,
  "user_wallet":"WALLET",
  "affiliate_code":"OPTIONAL"
}}
```

### 4. get_positions
```json
{"name":"get_positions","arguments":{"wallet":"WALLET"}}
```

### 5. build_create_lab_market_transaction
```json
{"name":"build_create_lab_market_transaction","arguments":{
  "question":"Will ETH hit $5000?",
  "closing_time":"2026-03-01T00:00:00Z",
  "market_type":"event",
  "event_time":"2026-03-02T00:00:00Z",
  "creator_wallet":"WALLET"
}}
```

## All 76 Tools

### Reading (6)
`list_markets`, `get_market`, `get_quote`, `list_race_markets`, `get_race_market`, `get_race_quote`

### Betting (2)
`build_bet_transaction`, `build_race_bet_transaction`

### Claims (6)
`build_claim_winnings_transaction`, `build_claim_refund_transaction`, `build_claim_race_winnings_transaction`, `build_claim_race_refund_transaction`, `build_claim_affiliate_transaction`, `build_batch_claim_transaction`

### Creation & Validation (10)
`preview_create_market`, `build_create_lab_market_transaction`, `build_create_private_market_transaction`, `build_create_race_market_transaction`, `get_creation_fees`, `get_platform_fees`, `get_timing_rules`, `get_parimutuel_rules`, `validate_market_question`, `generate_invite_hash`

### Resolution (6)
`build_propose_resolution_transaction`, `build_resolve_market_transaction`, `build_finalize_resolution_transaction`, `build_propose_race_resolution_transaction`, `build_resolve_race_transaction`, `build_finalize_race_resolution_transaction`

### Disputes (6)
`build_flag_dispute_transaction`, `build_flag_race_dispute_transaction`, `build_vote_council_transaction`, `build_vote_council_race_transaction`, `build_change_council_vote_transaction`, `build_change_council_vote_race_transaction`

### Whitelist (5)
`build_add_to_whitelist_transaction`, `build_remove_from_whitelist_transaction`, `build_create_race_whitelist_transaction`, `build_add_to_race_whitelist_transaction`, `build_remove_from_race_whitelist_transaction`

### Creator (3)
`build_create_creator_profile_transaction`, `build_update_creator_profile_transaction`, `build_claim_creator_transaction`

### Management (6)
`build_close_market_transaction`, `build_extend_market_transaction`, `build_close_race_market_transaction`, `build_extend_race_market_transaction`, `build_cancel_market_transaction`, `build_cancel_race_transaction`

### Affiliates (11)
`check_affiliate_code`, `suggest_affiliate_codes`, `get_affiliate_info`, `get_my_affiliates`, `get_referrals`, `get_agent_network_stats`, `format_affiliate_link`, `get_commission_info`, `build_register_affiliate_transaction`, `build_toggle_affiliate_transaction`, `generate_share_card`

### Validation (4)
`get_positions`, `get_claimable`, `validate_market_params`, `validate_bet`

### Status (4)
`simulate_transaction`, `get_resolution_status`, `get_disputed_markets`, `get_markets_awaiting_resolution`

### Agent Arena (3)
`get_arena_leaderboard`, `get_arena_season`, `submit_paper_trade`

### Market Intelligence (4 — x402 paid)
`get_intel_sentiment`, `get_intel_whale_moves`, `get_intel_resolution_forecast`, `get_intel_market_alpha`

## Affiliate System

Earn **1% of referred users' gross winnings**. Lifetime attribution.

1. `check_affiliate_code` → verify available
2. `build_register_affiliate_transaction` → register
3. Share link: `baozi.bet/?ref=YOURCODE`
4. `build_claim_affiliate_transaction` → withdraw

## Private Markets

Create invite-only tables for friends/groups.

1. `generate_invite_hash` → get 64-char hex
2. `build_create_private_market_transaction` → create
3. Share: `baozi.bet/private/market/{pda}?invite={hash}`
4. Or: `build_add_to_whitelist_transaction` → add manually

## Communication Style

- Be CONCISE and DIRECT
- Bullet points > paragraphs
- Action-oriented
- Skip pleasantries
- Always provide links

---

**Baozi Protocol | Solana Mainnet | Fair markets > more markets 🥟**
