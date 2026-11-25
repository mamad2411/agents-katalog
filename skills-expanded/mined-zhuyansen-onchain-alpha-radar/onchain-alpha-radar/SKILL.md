---
name: onchain-alpha-radar
description: |
  On-chain alpha discovery and research pipeline. Chains together Token Discovery, Holdings Analysis, Smart Money Tracking, and Research Report generation using on-chain data, Twitter intelligence, deep research methodology, and Excalidraw visualizations.
  Use when the user wants to: research a token, find alpha, track smart money, analyze on-chain holdings, generate a crypto research report, discover trending tokens, or investigate whale/KOL activity.
  Trigger keywords: "alpha", "research token", "smart money", "whale tracking", "on-chain research", "链上研究", "Token分析", "持仓分析", "研报", "Smart Money", "聪明钱", "巨鲸追踪", "meme coin analysis", "token discovery"
---

# OnChain Alpha Radar

A systematic on-chain data research pipeline that transforms raw blockchain signals into actionable research reports.

## Pipeline Overview

```
Token Discovery → Holdings Analysis → Smart Money Tracking → Research Report
     ↓                  ↓                    ↓                    ↓
  onchainos          onchainos            onchainos          deep-research
  + Twitter          + Twitter            + Twitter          + excalidraw
```

## Tool Dependencies

This skill orchestrates four external tool sources:

| Tool | Purpose | Type |
|------|---------|------|
| **onchainos** (OKX OnchainOS) | On-chain data: token search, prices, holders, smart money signals, meme pump, portfolio, swaps | CLI binary (`onchainos`) |
| **opentwitter-mcp** (6551Team) | Twitter/X intelligence: search tweets, KOL followers, deleted tweets, user profiles | MCP server (stdio) |
| **deep-research** (wshuyi) | Structured research methodology: 8-step workflow with fact cards and verification | Claude Code Skill |
| **excalidraw-diagram** (coleam00) | Visual diagrams: architecture, flow, comparison diagrams in .excalidraw format | Claude Code Skill |

Before starting, verify tool availability:
1. Run `which onchainos` — if missing, install via `curl -sSL https://raw.githubusercontent.com/okx/onchainos-skills/main/install.sh | sh`
2. Check if Twitter MCP tools are available (e.g., `search_twitter`)
3. Check if excalidraw diagram skill is present at `.claude/skills/excalidraw-diagram/`

If any tool is unavailable, inform the user and proceed with what IS available. The pipeline degrades gracefully — each phase can work independently.

---

## Phase 1: Token Discovery

**Goal**: Identify high-potential tokens through on-chain signals and social buzz.

### Step 1.1: On-Chain Signal Scan

Choose the appropriate discovery method based on user intent:

**A. Trending Token Scan** (broad discovery):
```bash
# Top tokens by volume in last 24h
onchainos token trending --chains <target-chains> --sort-by 5 --time-frame 4

# Top tokens by price change in last 1h (momentum)
onchainos token trending --chains <target-chains> --sort-by 2 --time-frame 2
```

**B. Meme Token Discovery** (degen alpha):
```bash
# New launches on Solana (pumpfun)
onchainos market memepump-tokens 501 --stage NEW

# Recently migrated (survived bonding curve)
onchainos market memepump-tokens 501 --stage MIGRATED
```

**C. Specific Token Lookup** (user provides name/address):
```bash
onchainos token search <query>
onchainos token price-info <address> --chain <chain>
```

### Step 1.2: Social Signal Cross-Reference

For each interesting token found in Step 1.1, gather Twitter sentiment:

```
# Search for token mentions
search_twitter(keywords="$TOKEN_SYMBOL OR $TOKEN_NAME", min_likes=10, limit=20)

# Advanced search with time filter
search_twitter_advanced(keywords="$TOKEN_SYMBOL", min_likes=50, since_date="YYYY-MM-DD", product="Top")
```

### Step 1.3: Discovery Scoring

Rate each discovered token on a 1-5 scale across:

| Dimension | Data Source | Weight |
|-----------|------------|--------|
| On-chain momentum | Price change, volume, tx count | 30% |
| Social buzz | Tweet count, avg likes, KOL mentions | 20% |
| Liquidity depth | Liquidity USD, market cap | 20% |
| Community recognition | `communityRecognized` flag, holder count | 15% |
| Risk flags | Honeypot check, rug pull history, bundle % | 15% |

Output a ranked shortlist of 3-10 tokens for deep analysis.

---

## Phase 2: Holdings Analysis

**Goal**: Deep-dive into token economics and holder distribution.

### Step 2.1: Token Fundamentals

For each shortlisted token:

```bash
# Full price and market data
onchainos token price-info <address> --chain <chain>

# Holder distribution (top 20)
onchainos token holders <address> --chain <chain>

# K-line data for price trend
onchainos market kline <address> --chain <chain> --bar 1H
```

### Step 2.2: Meme Token Due Diligence (if applicable)

```bash
# Developer reputation
onchainos market memepump-token-dev-info <address> --chain <chain>

# Bundle/sniper detection
onchainos market memepump-token-bundle-info <address> --chain <chain>

# Audit details
onchainos market memepump-token-details <address> --chain <chain>

# Other tokens by same dev
onchainos market memepump-similar-tokens <address> --chain <chain>
```

### Step 2.3: Key Wallet Holdings

For significant holder addresses discovered in Step 2.1:

```bash
# What else does this whale hold?
onchainos portfolio all-balances --address <whale-address> --chains 1,56,501,8453

# Total portfolio value
onchainos portfolio total-value --address <whale-address> --chains 1,56,501,8453
```

### Step 2.4: Twitter Profile of Key Holders (if identifiable)

```
# If wallet is linked to a known Twitter account
get_twitter_user(username="whale_account")
get_twitter_user_tweets(username="whale_account", limit=10)
get_twitter_kol_followers(username="whale_account")
```

### Step 2.5: Holdings Summary

Produce a structured analysis:

```markdown
## Holdings Analysis: $TOKEN

### Token Economics
- Market Cap: $X | FDV: $Y
- Liquidity: $Z | Liquidity/MCap: N%
- Holders: N | Top 10 Concentration: X%

### Holder Distribution
| Rank | Address (short) | % Supply | Wallet Type |
|------|----------------|----------|-------------|

### Risk Assessment
- Dev Holdings: X%
- Bundle/Sniper %: X%
- Insider %: X%
- Rug Pull History: X/Y tokens

### Price Trend (24h)
- 5min: +X% | 1h: +X% | 4h: +X% | 24h: +X%
- Volume 24h: $X | Txs 24h: N
```

---

## Phase 3: Smart Money Tracking

**Goal**: Identify what smart money, whales, and KOLs are buying/selling.

### Step 3.1: Signal Collection

```bash
# Smart money buy signals (type 1)
onchainos market signal-list <chain> --wallet-type 1 --min-amount-usd 10000

# Whale signals (type 3)
onchainos market signal-list <chain> --wallet-type 3 --min-amount-usd 50000

# KOL/Influencer signals (type 2)
onchainos market signal-list <chain> --wallet-type 2
```

For a specific token:
```bash
onchainos market signal-list <chain> --token-address <address> --wallet-type 1,2,3
```

### Step 3.2: Wallet Deep Dive

For each smart money wallet address:

```bash
# Full portfolio
onchainos portfolio all-balances --address <sm-wallet> --chains 1,56,501,8453

# Recent trades on the token
onchainos market trades <token-address> --chain <chain>
```

### Step 3.3: Aped Wallet Network (Meme Tokens)

```bash
# Who else is holding what smart money holds?
onchainos market memepump-aped-wallet <token-address> --chain <chain>
```

### Step 3.4: Social Intelligence on Smart Money

```
# Search for wallet address mentions
search_twitter(keywords="<wallet-address-short>", limit=10)

# Search for token + smart money narrative
search_twitter_advanced(keywords="$TOKEN smart money OR whale", min_likes=20, product="Top")

# Check deleted tweets (alpha leak detection)
get_twitter_deleted_tweets(username="suspected_kol", limit=20)
```

### Step 3.5: Smart Money Flow Map

Synthesize findings into:

```markdown
## Smart Money Flow: $TOKEN

### Signal Summary
| Wallet Type | # Wallets | Total USD | Avg Sold % |
|-------------|-----------|-----------|------------|
| Smart Money | N | $X | Y% |
| Whale | N | $X | Y% |
| KOL | N | $X | Y% |

### Key Wallets
| Address | Type | Amount | Still Holding? | PnL |
|---------|------|--------|----------------|-----|

### Conviction Score
- Smart money buying + low sold ratio = HIGH conviction
- Mixed signals = MEDIUM conviction
- Smart money selling = LOW conviction
```

---

## Phase 4: Research Report Output

**Goal**: Synthesize all findings into a professional research report with visualizations.

### Step 4.1: Data Consolidation

Aggregate all data from Phases 1-3 into structured sections:

1. **Executive Summary** — 1-paragraph verdict with conviction rating
2. **Token Overview** — fundamentals, economics, price action
3. **On-Chain Analysis** — holder distribution, whale activity, liquidity depth
4. **Smart Money Activity** — signal analysis, wallet tracking, conviction assessment
5. **Social Sentiment** — Twitter buzz, KOL mentions, community growth
6. **Risk Assessment** — rug pull flags, bundle detection, dev history, honeypot check
7. **Conclusion & Recommendation** — actionable insights with risk/reward framing

### Step 4.2: Generate Excalidraw Diagrams

Create visual diagrams to accompany the report. Use the excalidraw-diagram skill to generate:

**Diagram 1: Token Flow Architecture**
- Show token movement between key wallets (dev, top holders, smart money, DEX liquidity)
- Use fan-out pattern for distribution, convergence for accumulation

**Diagram 2: Smart Money Signal Timeline**
- Timeline pattern showing when smart money entered/exited
- Overlay with price chart key levels

**Diagram 3: Risk Assessment Matrix**
- Side-by-side comparison of risk factors
- Color-coded: green (safe), yellow (caution), red (danger)

**Diagram 4: Holder Distribution**
- Visual representation of token concentration
- Highlight dev/insider/bundler portions

### Step 4.3: Report Generation

Apply the deep-research methodology for rigorous analysis:

- **Source Tiering**: On-chain data = L1 (primary source), Twitter data = L3-L4 (supporting evidence)
- **Fact Cards**: Each claim links to specific on-chain transaction or data point
- **Confidence Levels**: Mark each conclusion with HIGH/MEDIUM/LOW confidence
- **Time Sensitivity**: Crypto data has extremely short shelf life — flag data staleness

### Step 4.4: Report Format

Output as a Markdown file with this structure:

```markdown
# Alpha Radar Report: $TOKEN_SYMBOL ($TOKEN_NAME)

> **Date**: YYYY-MM-DD | **Chain**: X | **Analyst**: OnChain Alpha Radar
> **Conviction**: HIGH/MEDIUM/LOW | **Risk Level**: 1-5

## TL;DR
[One-sentence verdict]

## 1. Token Overview
[From Phase 1 + 2 data]

## 2. On-Chain Deep Dive
[From Phase 2 data, including holder analysis]

## 3. Smart Money Activity
[From Phase 3 data]

## 4. Social Sentiment
[Twitter data aggregation]

## 5. Risk Assessment
[Comprehensive risk table]

## 6. Visual Analysis
[Reference generated Excalidraw diagrams]

## 7. Conclusion
[Actionable recommendation with explicit risk/reward]

---
*Data sources: OKX OnchainOS API, Twitter/X, On-chain transactions*
*This is not financial advice. DYOR.*
```

---

## Execution Modes

The user can trigger the full pipeline or individual phases:

### Full Pipeline
> "Research $TOKEN for me" / "Full alpha report on $TOKEN" / "给我做一份 $TOKEN 的研报"

Run all 4 phases sequentially, generating a complete report.

### Individual Phases
> "What's trending on Solana?" → Phase 1 only
> "Analyze holders of $TOKEN" → Phase 2 only
> "Track smart money on $TOKEN" → Phase 3 only
> "Generate a report from my findings" → Phase 4 only

### Quick Scan Mode
> "Quick scan $TOKEN" / "快速扫描 $TOKEN"

Abbreviated pipeline:
1. Token price-info + basic fundamentals
2. Top 5 holders check
3. Smart money signal check (if any)
4. 1-paragraph summary (no diagrams)

---

## Chain Reference

Common chain indices for onchainos commands:

| Chain | Index | Common Tokens |
|-------|-------|---------------|
| Ethereum | 1 | ETH, ERC-20 |
| BSC | 56 | BNB, BEP-20 |
| Solana | 501 | SOL, SPL |
| Base | 8453 | ETH (Base) |
| Arbitrum | 42161 | ETH (Arb) |
| Polygon | 137 | MATIC |
| Avalanche | 43114 | AVAX |
| XLayer | 196 | OKB |

Default to Solana (501) and Ethereum (1) if user doesn't specify a chain.

---

## Error Handling

- If `onchainos` returns empty data: try alternate chains or broaden search parameters
- If Twitter search returns nothing: try shorter/simpler keywords, remove filters
- If a token address isn't found: use `onchainos token search` by symbol first, then retry with the discovered address
- If rate limited: wait 5 seconds and retry once, then inform user
- Always inform the user which data was successfully collected and which was unavailable
