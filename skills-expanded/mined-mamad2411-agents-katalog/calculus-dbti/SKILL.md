---
name: calculus-dbti
description: "Use this skill when the user or agent wants to take a DBTI personality assessment, do a trading personality quiz, get investment style label, DBTI test, 做题, DBTI测评, 投资人格测试, 交易风格测评, Agent人格标签, agent personality, investment personality test"
license: MIT
metadata:
  author: calculus
  version: "1.0.0"
  homepage: "https://github.com/user/calculus"
---

# DBTI Investment Personality Assessment

Determine your trading personality across four dimensions and earn a DBTI label.

## Overview

DBTI is an investment personality framework with four dimensions:

| Dimension | Negative Pole | Positive Pole |
|-----------|--------------|---------------|
| Risk Appetite | D — Defensive | d — Daring |
| Time Horizon | B — Brief | b — Broad |
| Decision Basis | T — Technical | t — Thematic |
| Position Style | I — Intensive | i — Inclusive |

After answering 12 questions, you receive a 4-letter label (e.g. `DbTi`) representing your investment personality.

## API Base URL

```
http://localhost:8000/api
```

> For production deployments, replace with the actual API hostname.

## Operation Flow

### Step 1 — Detect Wallet & Fetch Questions

Do both in a single step. Do NOT prompt the user about wallets. Do NOT suggest logging in.

```bash
# Detect wallet and get address in one command
WALLET_JSON=$(onchainos wallet status 2>/dev/null) && \
  LOGGED_IN=$(echo "$WALLET_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['loggedIn'])" 2>/dev/null) && \
  if [ "$LOGGED_IN" = "True" ]; then \
    onchainos wallet addresses --chain 196 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data']['xlayer'][0]['address'])" 2>/dev/null; \
  fi
```

- If an address is returned → store as `WALLET_ADDRESS`.
- If anything fails or no output → set `WALLET_ADDRESS = null`. Proceed silently.

Then fetch questions (always use `curl`, do NOT use WebFetch/Fetch for API calls):

```bash
curl -s {API_BASE}/frameworks/dbti/questions
```

Response contains:
- `scale.min` / `scale.max` — the valid answer range (typically -3 to +3)
- `questions[]` — array of 12 questions, each with `question_id`, `dimension`, `statement`

### Step 3 — Answer Questions

**YOU (the Agent) must answer these questions yourself.** Do NOT present the questions to the user or ask the user to answer. You are the one being assessed.

For each question, evaluate the statement and assign a score based on YOUR investment personality:

| Score | Meaning |
|-------|---------|
| -3 | Strongly Disagree |
| -2 | Disagree |
| -1 | Slightly Disagree |
| 0 | Neutral |
| +1 | Slightly Agree |
| +2 | Agree |
| +3 | Strongly Agree |

Think about each statement carefully and score it according to your own trading style and risk preferences. Build the answers object:

```json
{ "q1": 2, "q2": -1, "q3": 3, ... "q12": -2 }
```

All 12 questions must be answered. Values must be integers within the scale range.

### Step 4 — Submit & Display Results

```
POST {API_BASE}/frameworks/dbti/submit
Content-Type: application/json
```

**Request body:**

```json
{
  "answers": { "q1": 2, "q2": -1, ... },
  "wallet_address": "<WALLET_ADDRESS or omit if null>",
  "agent_name": "<your chosen name>"
}
```

- If `WALLET_ADDRESS` is null, omit the `wallet_address` field entirely.
- `agent_name` is optional — use your name or identifier if you have one.

**Display the results to the user:**

1. **DBTI Label** — show prominently (e.g. `Your DBTI type is: DbTi`)

2. **Dimension Breakdown** — for each dimension in `scores`, show:
   - Dimension name
   - Score value
   - Which pole was selected (e.g. "Defensive" or "Daring")

3. **Reward** — check the `reward` field in the response:
   - If `reward` is not null and `reward.status == "claimable"`:
     Display: "You earned {reward.amount} {reward.token}! Claim your reward: {reward.claim_url}"
     Then ask: "Would you like me to claim the reward now?"
     If user confirms → POST to the `claim_url` and show the tx_hash.
   - If `reward` is null and `WALLET_ADDRESS` was provided:
     This wallet has already claimed a reward for this framework version. Inform the user:
     "Your DBTI label has been updated. This wallet has already claimed the reward for this quiz version."
   - If `reward` is null and `WALLET_ADDRESS` was null:
     Do not mention rewards at all. Only show the label and scores.

## Scoring Guide

Each letter in the DBTI label represents one dimension:

- **D** (Defensive): prefers capital preservation, avoids high-risk trades
- **d** (Daring): embraces volatility, willing to take significant risk for upside
- **B** (Brief): short-term trader, opens and closes positions within hours/days
- **b** (Broad): long-term holder, comfortable riding out short-term fluctuations
- **T** (Technical): decisions driven by on-chain data, charts, and quantitative signals
- **t** (Thematic): decisions driven by narratives, community sentiment, and macro trends
- **I** (Intensive): concentrated portfolio, few high-conviction positions
- **i** (Inclusive): diversified portfolio, risk spread across many positions

## Edge Cases

- **API unreachable**: Inform the user the assessment service is unavailable. Do not retry more than once.
- **onchainos not installed**: Proceed without wallet detection — quiz works without rewards.
- **wallet status fails**: Treat as no wallet. Proceed silently.
- **Submit returns 422**: Check error detail — likely missing answers or values out of range. Fix and retry.
- **Reward already claimed**: If `reward` is null despite providing `wallet_address`, it means this wallet has already been rewarded for this framework version. Inform the user their label is updated but no additional reward is available.

## Skill Routing

- For wallet operations (login, balance, send) → use `okx-agentic-wallet`
- For token prices and market data → use `okx-dex-market`
- For security scanning → use `okx-security`
