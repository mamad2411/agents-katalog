---
name: daily-alpha-scanner
description: "One-click daily alpha scanner that runs a full 5-step on-chain research pipeline using OKX OnchainOS: (1) Hot Token Discovery with narrative categorization (AI, Meme, DeFi, Infra), (2) Smart Money / KOL / Whale buy-signal tracking with sold-ratio scoring, (3) Meme Coin launchpad scanning (pump.fun, fourmeme) with dev reputation and bundle/sniper detection, (4) Batch security audit (honeypot, mintable, fake LP, wash trading), (5) Consolidated briefing with composite scoring (0-100) and BUY / WATCH / AVOID verdicts. Supports Solana, Base, Ethereum, BSC, Arbitrum. Use when the user wants a daily market scan, alpha discovery, token recommendations, or asks 'what to buy today'. Trigger keywords: daily scan, alpha scanner, today's alpha, what to buy, market scan, daily briefing, 每日扫描, 今日推荐, 扫链, 今天买什么, 市场扫描, 链上日报, 每日研报."
license: MIT
compatibility: "Requires onchainos CLI v3.1+ and OKX Web3 API key (OKX_API_KEY, OKX_SECRET_KEY, OKX_PASSPHRASE). Internet access required for on-chain data queries."
metadata:
  author: zhuyansen
  version: "1.0.0"
  homepage: "https://github.com/zhuyansen/daily-alpha-scanner"
---

# Daily Alpha Scanner

A systematic 5-step pipeline that scans on-chain data across multiple chains and produces a consolidated briefing with purchase recommendations.

## Pipeline

```
Step 1: Hot Tokens    →  Step 2: Smart Money   →  Step 3: Meme Scan
     ↓                        ↓                        ↓
Step 4: Security Audit (batch scan all candidates)
     ↓
Step 5: Consolidated Briefing + Purchase Recommendations
```

## Prerequisites

Verify before starting:
```bash
which onchainos && onchainos --version
```
If missing: `curl -sSL https://raw.githubusercontent.com/okx/onchainos-skills/main/install.sh | sh`

Required env vars: `OKX_API_KEY`, `OKX_SECRET_KEY`, `OKX_PASSPHRASE` (Web3 API key from https://web3.okx.com/onchainos/dev-portal)

## Execution

### User Parameters

Ask the user before starting (or use defaults):

| Parameter | Default | Options |
|-----------|---------|---------|
| Chains | Solana + Base | Solana (501), Ethereum (1), Base (8453), BSC (56), Arbitrum (42161) |
| Focus | All narratives | AI, Meme, DeFi, Infra, BTC-eco, Political |
| Risk tolerance | Medium | Conservative, Medium, Aggressive |
| Output | Terminal | Terminal, Markdown file |

If the user just says "扫一下" or "daily scan" without parameters, use defaults (Solana + Base, all narratives, medium risk).

---

## Step 1: Hot Token Discovery

**Goal**: Find trending tokens across target chains, categorize by narrative.

### 1.1 Fetch Trending Tokens

Run in parallel for each target chain:

```bash
# Trending by OKX trending score (hot-tokens ranking)
onchainos token hot-tokens --chain <chainId> --limit 20

# Volume-based trending (complementary view)
onchainos token trending --chains <chainIds> --sort-by 5 --time-frame 4 --limit 30
```

### 1.2 Extract & Categorize

From the results, extract for each token:
- `tokenSymbol`, `tokenContractAddress`, `chainIndex`
- `price`, `change` (24h %), `volume`, `marketCap`, `liquidity`
- `holders`, `top10HoldPercent`, `bundleHoldPercent`, `devHoldPercent`
- `riskLevelControl` (1=low, 2=medium, 3=high)

Categorize by narrative based on token name, symbol, and tags:
- **AI/Agent**: tokens related to AI, agents, virtual, autonomous
- **Meme**: animal names, cultural references, ironic/funny names
- **DeFi**: DEX tokens, lending, yield, staking
- **Infra**: L1/L2, bridges, oracles, tooling
- **BTC-eco**: BTC wrappers, ordinals, BTC-related
- **Political**: political figures, events
- **Stablecoin/Yield**: USD-pegged, yield-bearing stablecoins

### 1.3 Filter Criteria

Remove tokens that are obvious noise:
- Top10 concentration > 80% (extreme whale control)
- Market cap < $5K (dust)
- Volume/MCap ratio > 100x (likely bot wash trading)
- Zero holders or zero liquidity

Keep a shortlist of **top 15-20 interesting tokens** for further analysis.

---

## Step 2: Smart Money Signal Scan

**Goal**: Identify what smart money, KOLs, and whales are actively buying.

### 2.1 Aggregated Buy Signals

Run in parallel for each target chain:

```bash
# Smart money buy signals
onchainos signal list --chain <chainId> --wallet-type 1 --limit 10

# KOL buy signals
onchainos signal list --chain <chainId> --wallet-type 2 --limit 10

# Whale buy signals
onchainos signal list --chain <chainId> --wallet-type 3 --limit 10
```

### 2.2 Extract Signal Data

For each signal entry:
- `token.symbol`, `token.tokenAddress`, `token.marketCapUsd`
- `triggerWalletCount` (number of smart money addresses buying)
- `amountUsd` (total buy amount)
- `soldRatioPercent` (how much they've already sold — key metric!)
- `token.top10HolderPercent`, `token.holders`

### 2.3 Signal Quality Scoring

Rate each signal:
- **Strong**: 5+ wallets buying, soldRatio < 30%, marketCap > $100K
- **Medium**: 3+ wallets buying, soldRatio < 60%
- **Weak**: 1-2 wallets, soldRatio > 70% (already exiting)
- **Exit signal**: soldRatio > 90% (smart money dumping)

### 2.4 Cross-reference with Hot Tokens

Flag tokens that appear in BOTH Step 1 (trending) AND Step 2 (smart money buying) — these have the strongest alpha signal.

---

## Step 3: Meme Coin Scan

**Goal**: Scan launchpads for new launches worth tracking.

### 3.1 New Token Scan

```bash
# Latest meme launches on Solana
onchainos memepump tokens --chain 501

# Latest meme launches on BSC (if in target chains)
onchainos memepump tokens --chain 56
```

### 3.2 Extract Key Metrics

For each new meme token:
- `symbol`, `tokenAddress`, `bondingPercent` (bonding curve progress)
- `market.marketCapUsd`, `market.buyTxCount1h`, `market.sellTxCount1h`
- `tags.snipersPercent`, `tags.bundlersPercent`
- `tags.top10HoldingsPercent`, `tags.devHoldingsPercent`, `tags.freshWalletsPercent`
- `tags.totalHolders`
- `social.x` (has Twitter?), `social.website`, `social.telegram`
- `creatorAddress` (for dev reputation lookup)

### 3.3 Developer Reputation Check

For promising tokens (survived bonding, has social presence):

```bash
onchainos memepump token-dev-info --address <tokenAddress> --chain <chainId>
```

Key fields:
- `devCreateTokenCount` — how many tokens this dev has created
- `devRugPullTokenCount` — how many rugged
- `devLaunchedTokenCount` — how many survived past bonding curve

### 3.4 Bundle/Sniper Detection

```bash
onchainos memepump token-bundle-info --address <tokenAddress> --chain <chainId>
```

### 3.5 Meme Scoring

Filter out garbage:
- Sniper % > 50% → likely bot-controlled → skip
- Top10 holdings > 60% → extreme concentration → skip
- 0 holders or < 3 holders → too early → skip
- No social presence at all → skip
- Dev has > 5 rug pulls → skip

Keep tokens that have:
- Survived bonding curve (migrated)
- Sniper < 20%, bundle < 10%
- Has at least Twitter presence
- Dev rug pull rate < 20%
- Growing holder count

---

## Step 4: Security Audit

**Goal**: Batch security scan all candidate tokens from Steps 1-3.

### 4.1 Collect Candidates

Merge the shortlisted tokens from Steps 1, 2, and 3 (deduplicate by address). Max 10 tokens for batch scan.

### 4.2 Batch Token Security Scan

```bash
onchainos security token-scan --tokens "<chainId1>:<addr1>,<chainId2>:<addr2>,..."
```

Up to 10 tokens per batch. Key fields to check:
- `riskLevel`: LOW / MEDIUM / HIGH
- `isHoneypot`: true = INSTANT REJECT
- `isMintable`: true = can create infinite tokens
- `isDumping`: true = active sell pressure
- `isFakeLiquidity`: true = liquidity is fake
- `isLiquidityRemoval`: true = LP being pulled
- `isCounterfeit`: true = fake/copycat token
- `isWash`: true = wash trading detected

### 4.3 Advanced Risk Analysis

For tokens that pass the security scan, run advanced info:

```bash
onchainos token advanced-info --address <address> --chain <chainId>
```

Key fields:
- `devCreateTokenCount` — serial deployer?
- `devRugPullTokenCount` — rug history
- `lpBurnedPercent` — LP lock safety (higher = safer)
- `sniperHoldingPercent` — sniper concentration
- `bundleHoldingPercent` — bundle bot concentration
- `suspiciousHoldingPercent` — flagged wallets
- `tokenTags` — look for: `communityRecognized`, `smartMoneyBuy`, `dsPaid`, `CTO`

### 4.4 Risk Classification

| Risk Level | Criteria | Action |
|------------|----------|--------|
| SAFE | LOW risk, no flags, LP burned > 90%, dev clean | Can consider |
| CAUTION | LOW risk but some flags (high dev token count, moderate concentration) | Small position only |
| DANGER | Any honeypot/mintable/fake liquidity flag | REJECT |
| CRITICAL | Multiple red flags, dev rug history, active dumping | REJECT + warn |

---

## Step 5: Consolidated Briefing

**Goal**: Synthesize all data into a single actionable report.

### 5.1 Report Structure

Use the template at `templates/daily-briefing.md` to generate the output.

### 5.2 Scoring Model

Each candidate token gets a composite score (0-100):

| Factor | Weight | Data Source |
|--------|--------|-------------|
| Narrative strength | 15% | Step 1 categorization + current market meta |
| On-chain momentum | 20% | Price change, volume, tx count, holder growth |
| Smart money conviction | 25% | Signal count, wallet count, sold ratio |
| Security score | 25% | Security scan + advanced info |
| Liquidity depth | 15% | Liquidity USD, liquidity/mcap ratio |

### 5.3 Purchase Recommendation Tiers

Based on composite score and risk tolerance:

**BUY (Score > 70, Security = SAFE)**
- Strong narrative + smart money backing + clean security
- Suggested position: 2-5% of portfolio

**WATCH (Score 50-70, Security = SAFE/CAUTION)**
- Promising but needs more confirmation
- Set price alerts, monitor daily

**AVOID (Score < 50 or Security = DANGER/CRITICAL)**
- Too risky or no clear edge
- Explain specific red flags

### 5.4 Output Format

Generate the briefing with:
1. Executive summary (3-5 bullets)
2. Hot tokens by narrative table
3. Smart money signal table
4. Meme scan highlights
5. Security audit results
6. Final recommendation table with risk rating
7. Disclaimer

### 5.5 Save Report

```bash
# Save to reports directory
mkdir -p reports
# Filename: daily-alpha-YYYY-MM-DD.md
```

---

## Error Handling

- If `onchainos` returns error 50125 (region restriction): inform user to check API key region or use VPN
- If any step returns empty data: skip that step, note it in the report, continue with available data
- If security scan returns empty for a token: mark as "UNSCANNED" in the report, do NOT recommend
- Always run all 5 steps even if some data is partial — the report should indicate data completeness

## Quick Mode

If the user says "快速扫描" / "quick scan", run abbreviated version:
1. `hot-tokens` top 10 only (single chain)
2. `signal list` smart money only (single chain)
3. Skip meme scan
4. Security scan top 5 candidates only
5. Abbreviated 1-page briefing

## Chain Reference

| Chain | ID | Meme Support |
|-------|----|-------------|
| Solana | 501 | pumpfun, believe, launchlab, moonshot, etc. |
| BSC | 56 | fourmeme, flap |
| Base | 8453 | clanker, bankr |
| Ethereum | 1 | Limited |
| TRON | 195 | sunpump |
