---
name: birdbets-market
description: Interact with BirdBets — a Base prediction market where users bet MYKCLAWD on whether more than N birds will visit a BirdBuddy feeder on a given day
tags: [trading, defi, prediction-market, base]
version: 1
visibility: public
metadata:
  clawdbot:
    emoji: "🐦"
    homepage: "https://birdbets.mykclawd.xyz/bankr-skill"
---

# BirdBets Market Skill Overview

**BirdBets** is a Base-based prediction market platform focused on bird visit forecasting. The skill enables users to bet on whether bird visits will exceed set thresholds, access real-time odds, preview payouts, and manage MYKCLAWD tokens.

## Key Capabilities

- **Market Betting**: Place YES/NO bets on daily bird visit predictions
- **Odds & Payouts**: View current odds and calculate potential returns
- **Token Management**: Acquire MYKCLAWD on Base for betting
- **Market Stats**: Access BirdBuddy visit data and market summaries

## How Markets Work

"Each market asks whether bird visits will be greater than the threshold. YES wins when `actualVisits > threshold`; NO wins when `actualVisits <= threshold`."

## Before Betting

Users must:
1. Specify their side (YES or NO) and bet amount explicitly
2. Verify the market is active, unresolved, and open
3. Review the threshold, odds, liquidity pools, and projected payouts
4. Confirm sufficient MYKCLAWD balance in their Bankr wallet

## Primary Data Sources

- Context API: `https://birdbets.mykclawd.xyz/api/bankr/context`
- Tomorrow's market: `https://birdbets.mykclawd.xyz/api/markets/snapshot?market=Tomorrow`
- Today's stats: Market snapshot and 7-day visit history endpoints
- Bet preparation: `https://birdbets.mykclawd.xyz/api/base-mcp/prepare/bet?from=<wallet>&side=<YES|NO>&stake=<amount>`

**Always use the bet preparation endpoint to place bets.** It returns pre-encoded `approve` and `betYes`/`betNo` transaction calldata. Never encode contract calls manually — the market ID is a `uint256` integer (not a string) and the contract has separate `betYes` and `betNo` functions, not a single `bet(id, bool, amount)`.

After the bet confirms, reply with the share link from the prepare response (`share.url`) — the same link the web app uses for sharing on X/Twitter — so the user sees the share image for the bet they just placed. See the workflows reference for the full `share` object.

The skill operates in read-only mode if the API key or wallet session lacks write permissions—providing information without executing transactions.

## References

- Workflows: https://mykclawd.xyz/api/skills/birdbets/workflows
- Contracts: https://mykclawd.xyz/api/skills/birdbets/contracts
