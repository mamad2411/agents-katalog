---
name: outsmart-prediction-markets
description: "Trade prediction markets on Jupiter and browse Polymarket odds. Use when: user asks about prediction markets, betting on events, Polymarket, Jupiter markets, binary outcomes, probability, odds, forecasting, futarchy. NOT for: sports betting (off-chain), regular token trading, LP farming."
homepage: https://github.com/outsmartchad/outsmart-cli
metadata: { "openclaw": { "requires": { "bins": ["curl"] }, "install": [{ "id": "node", "kind": "node", "package": "outsmart", "bins": ["outsmart"], "label": "Install outsmart CLI (npm)" }] } }
---

# Prediction Markets

Bet on real-world outcomes. AI agents have a genuine edge here — better at probabilistic reasoning, synthesizing info, and spotting cognitive biases in pricing.

## When to Use

- "What are the odds of X happening?"
- "Bet on Bitcoin reaching $200k"
- "Browse prediction markets"
- "What's trending on Polymarket?"

## When NOT to Use

- Sports betting on off-chain platforms
- Regular token trading — use dex-trading
- LP farming — different skill

## Polymarket (Browse Odds)

Public API, no auth needed. World's largest prediction market.

### Search Markets

```bash
curl -s "https://gamma-api.polymarket.com/public-search?q=bitcoin&limit_per_type=5&events_status=active" | python3 -m json.tool
```

### Trending Events

```bash
curl -s "https://gamma-api.polymarket.com/events?active=true&closed=false&order=volume24hr&ascending=false&limit=10" | python3 -m json.tool
```

### Event Details

```bash
curl -s "https://gamma-api.polymarket.com/events/slug/EVENT_SLUG" | python3 -m json.tool
```

### Orderbook

```bash
curl -s "https://clob.polymarket.com/book?token_id=CLOB_TOKEN_ID" | python3 -m json.tool
```

## Jupiter Prediction (Trade on Solana)

Native Solana. Binary YES/NO contracts priced $0-$1. Price = implied probability. Winners get $1.

### Browse Events

```bash
curl -s "https://api.jup.ag/prediction/v1/events?includeMarkets=true&limit=10" \
  -H "x-api-key: $JUPITER_API_KEY" | python3 -m json.tool
```

### Search

```bash
curl -s "https://api.jup.ag/prediction/v1/events/search?query=bitcoin&limit=10" \
  -H "x-api-key: $JUPITER_API_KEY" | python3 -m json.tool
```

## The Only Rule: Edge

Only bet when your estimated probability significantly differs from market price.

```
Edge = Your_Probability - Market_Price
```

| Edge | Action |
|------|--------|
| > 15% | Strong bet, 3-5% of portfolio |
| 10-15% | Standard bet, 1-2% |
| 5-10% | Marginal, small or skip |
| < 5% | No edge. Market is probably right. |

### Example

"Will SOL reach $300 by March?" — market says 25%. You estimate 45%. Edge = 20%.

Buy 100 YES at $0.25 = $26.32. If right: $100. If wrong: -$26.32. EV: +$18.68.

## Where AI Has Edge

| Category | Edge | Notes |
|----------|------|-------|
| Crypto events | High | ETF approvals, protocol launches, price targets |
| Technology | High | AI milestones, product launches |
| Economics | Medium-High | Fed decisions, inflation |
| Politics | Medium | Deep liquidity, smart money, edge is rarer |
| Sports | Low | Avoid unless specialized data |

## Portfolio Rules

- Max 10% total in open prediction positions
- Max 3-5% per individual bet
- Track accuracy: record every bet, estimate, and outcome
- Adjust: what categories are you best at? Double down there.
