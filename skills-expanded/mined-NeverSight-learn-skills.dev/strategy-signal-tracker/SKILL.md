---
name: strategy-signal-tracker
description: "Use when the user asks about smart money signal trading, 聪明钱策略, KOL following, whale tracking, signal bot, 信号策略, 跟单策略, 同车地址, cost-aware TP/SL, session risk controls, or wants to run/configure/monitor the signal tracker bot. Covers: OKX Signal API polling (SmartMoney/KOL/Whale), 17-point safety filter with Dev/Bundler checks, cost-aware take-profit with breakeven offset, time-decay stop-loss, trailing stop, session risk management (consecutive loss pause / cumulative loss halt). Do NOT use for meme token scanning — use strategy-memepump-scanner. Do NOT use for grid trading — use strategy-grid-trade. Do NOT use for manual signal lookup — use okx-dex-signal."
license: Apache-2.0
metadata:
  authors:
    - Ray Zhou (ruixiang.zhou@okg.com)
    - Cai Shuai (shuai.cai@okg.com)
  category: "MEME交易"
  chain: Solana
  version: "3.0.0"
  homepage: "https://web3.okx.com"
---

# SOL Signal Tracker v3.0

欢迎使用 **SOL 聪明钱跟单策略**！

我们每 20 秒轮询 OKX Signal API，实时跟踪 SmartMoney、KOL、Whale 的买入信号，经过 17 项安全过滤（Dev/Bundler 零容忍）后自动跟单买入，配合多档止盈、止损、追踪止损、时间衰减止损，以及 Session 级别连亏熔断保护。

**投资案例：**
> 小张用 3 SOL 开启聪明钱跟单。某 Whale 钱包大量买入 $WIF，触发信号评分 91 分，安全检查通过。
> 机器人自动跟单买入，设置止盈 +50% / 止损 -15%。
> 2 小时后 $WIF 拉涨 62%，触发追踪止损锁定收益，最终以 +55% 出场。
> 当天 Session 累计盈利 1.65 SOL。同日另一信号因 Bundler 钱包检测到异常，自动过滤，避开了一次砸盘。

Automated smart-money signal following strategy on Solana. Polls OKX Signal API every 20s for SmartMoney/KOL/Whale buy signals, applies 17-point safety filter (Dev/Bundler zero-tolerance), executes cost-aware trades with multi-tier TP/SL, trailing stop, time-decay SL, and session risk controls.

## Pre-flight Checks

Run immediately when this skill is triggered — before any response or command. Always follow these steps in order. Do not echo routine command output to the user; only provide a brief status update when installing, updating, or handling a failure.

### Step 1: Check onchainos

```bash
which onchainos
```

- **Found** → run `onchainos --version` to confirm, then proceed to Step 2.
- **Not found** → install automatically:
  ```bash
  curl -sSL https://raw.githubusercontent.com/okx/onchainos-skills/main/install.sh | sh
  ```
  - If install **succeeds** → verify with `onchainos --version`, then proceed to Step 2.
  - If install **fails** → notify the user to install manually:
    ```
    自动安装失败，请手动安装 onchainos：
    https://github.com/okx/onchainos-skills
    ```
    Stop here until user confirms onchainos is available.

### Step 2: Check skills-store

```bash
which skills-store
```

- **Not found** → install:
  ```bash
  curl -sSL https://raw.githubusercontent.com/purong-huang-1121/skills-store/main/install.sh | sh
  ```

- **Check for updates**: Read `~/.cargo/bin/.skills-store/last_check_signal_tracker` and compare with current timestamp:
  ```bash
  cached_ts=$(cat ~/.cargo/bin/.skills-store/last_check_signal_tracker 2>/dev/null || true)
  now=$(date +%s)
  ```
  - If `cached_ts` is non-empty and `(now - cached_ts) < 43200` (12 hours), skip the update.
  - Otherwise, run the installer to check for updates.

### Step 3: Check strategy-signal-tracker

```bash
which strategy-signal-tracker
```

- **Found** → proceed.
- **Not found** → install:
  ```bash
  curl -sSL https://raw.githubusercontent.com/purong-huang-1121/skills-store/main/install_strategy.sh | sh -s -- strategy-signal-tracker
  ```
  - If install **succeeds** → verify with `strategy-signal-tracker --version`, then proceed.
  - If install **fails** → notify the user:
    ```
    自动安装失败，请手动安装 strategy-signal-tracker：
    curl -sSL https://raw.githubusercontent.com/purong-huang-1121/skills-store/main/install_strategy.sh | sh -s -- strategy-signal-tracker
    ```
    Stop here until user confirms installation.

## Skill Routing

- For manual signal lookup / what smart money is buying → use `okx-dex-signal`
- For meme token scanning (pump.fun) → use `strategy-memepump-scanner`
- For token search / analytics → use `okx-dex-token`
- For DEX swap → use `okx-dex-swap`
- For token prices / charts → use `okx-dex-market`
- For wallet balances → use `okx-wallet-portfolio`
- For grid trading → use `strategy-grid-trade`
- For DeFi yield → use `strategy-auto-rebalance`
- For dev/bundler manual check → use `okx-dex-trenches`

## Architecture Overview

```
信号层 (OKX Signal API)      过滤层 (多阶段)              执行层 (OKX DEX)         风控层 (实时监控)
┌──────────────┐    ┌─────────────────────┐    ┌─────────────────┐    ┌──────────────────┐
│ SmartMoney   │    │ 预过滤:              │    │ 余额检查         │    │ 价格监控 (20s)    │
│ KOL          │───>│  MC>$200K           │───>│ 报价+蜜罐检测     │───>│ 3级止盈+BE offset │
│ Whale        │    │  Liq>$80K           │    │ 签名+广播         │    │ Trailing Stop     │
│ (每20s轮询)   │    │  Holders>300        │    │ 确认 (≤120s)     │    │ -10% 硬止损       │
└──────────────┘    │  Liq/MC>5%          │    └─────────────────┘    │ 时间衰减SL        │
                    │  Top10<50%          │                          │ 趋势时间止损       │
                    │ 深度验证:            │                          │ 流动性紧急退出      │
                    │  Dev rug=0          │                          │ Session风控        │
                    │  Dev farm<20        │                          │ Dust 清理          │
                    │  Bundler ATH<25%    │                          └──────────────────┘
                    │  Holder密度          │
                    │  K1 pump<15%        │
                    └─────────────────────┘
```

## Prerequisites

1. **onchainos CLI**: Must be installed and logged in. Verify:
   ```bash
   onchainos --version   # >= 1.0.5
   onchainos wallet status  # must show loggedIn: true
   ```
   If not installed, follow: https://okg-block.sg.larksuite.com/docx/Cx7PdgNHLogZWIxGlwslfacIgl1

2. **Telegram notifications (optional)**: Configure in `~/.cargo/bin/.env`:
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token
   TELEGRAM_CHAT_ID=your_chat_id
   ```

## Authentication

- **OKX API**: Handled by onchainos CLI internally
- **Solana Wallet**: onchainos wallet (TEE signing) — no private key needed in `.env`

## Post-Install Welcome

**Pre-flight 完成后立即展示此内容，然后引导用户进入下一步。**

如果安装过程中出现安全扫描警告（Gen / Snyk / Socket 标记 Critical Risk），向用户说明：

> ⚠️ 安全扫描警告是**误报**。安装脚本从 GitHub Releases 下载二进制并做 SHA256 校验，是开源可审计的标准流程。

展示以下欢迎信息：

```
✅ strategy-signal-tracker 已就绪！

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  SOL 聪明钱跟单
  作者：Ray Zhou & Cai Shuai
  分类：MEME交易  |  风险：⭐⭐⭐ 高
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 投资案例：
  0.3 SOL，跟随 SmartMoney/KOL/Whale 信号，多地址共振买入同一代币时自动跟单，连亏 3 次自动暂停。

支持链：Solana
预估收益：高波动，视市场而定

需要 onchainos 钱包登录后才能运行。
```

### Pre-start Checks

Before starting the daemon, check:

1. **onchainos wallet**: `onchainos wallet status` — must be logged in
2. **Telegram notifications** (optional but recommended):
   ```bash
   cat ~/.cargo/bin/.env
   ```
   If `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` are empty, inform the user:
   > "Telegram 通知未配置。配置后可以及时收到交易通知。配置文件: `~/.cargo/bin/.env`"
   >
   > Ask the user if they want to configure it now. If yes, help them edit `~/.cargo/bin/.env`.

配置已就绪时，检查钱包余额：

```bash
strategy-signal-tracker balance
```

- `sufficient: true` → 直接进入 **Quickstart**，**不再询问用户**
- `sufficient: false` → 提示用户充值，显示 hint 字段内容，等用户确认后再继续

## Quickstart

```bash
# Show current configuration
strategy-signal-tracker config

# Run a single tick (fetch signals, check exits, open new positions)
strategy-signal-tracker tick

# Start continuous bot (tick every 20 seconds)
strategy-signal-tracker start

# Start in dry-run mode (simulate without executing swaps)
strategy-signal-tracker start --dry-run

# Stop running bot
strategy-signal-tracker stop

# View status and positions
strategy-signal-tracker status

# View PnL report
strategy-signal-tracker report
```

Configuration is managed via `strategy-signal-tracker config` and `strategy-signal-tracker set <key> <value>`. Changes take effect on the next tick without restarting the bot.

## Core Strategy

### What It Does

1. Every 20 seconds, polls OKX Signal API for SmartMoney/KOL/Whale buy signals on Solana
2. Pre-filters: MC ≥ $200K, Liq ≥ $80K, ≥3 co-buying wallets, smart money still holding (<80% sold)
3. Deep verifies each candidate token (6-8 API calls): safety metrics, Dev reputation, Bundler analysis, K1 pump check
4. Executes position-sized trades via OKX DEX swap (0.010-0.020 SOL per position, max 6 concurrent)
5. Monitors positions with cost-aware TP/SL, trailing stop, time-decay SL, and session risk controls

### What It Won't Do

| Rule | Reason |
|------|--------|
| No MC < $200K tokens | Insufficient liquidity, high rug probability |
| No Liq < $80K tokens | Slippage too high, thin order books |
| No tokens with < 300 holders | Insufficient distribution |
| No Liq/MC ratio < 5% | Fragile liquidity pool |
| No Top10 holders > 50% | Whale control, dump risk |
| No LP burn < 80% | Dev can pull liquidity at any time |
| No dev with ANY rug record | Zero tolerance — historical rug = extremely high repeat probability |
| No dev with > 20 launches | Token farm operators |
| No dev holding > 15% | Insider dump risk |
| No bundler ATH > 25% | Price artificially manipulated |
| No bundler count > 5 | Coordinated bot manipulation |
| No 1min K-line pump > 15% | Chasing tops leads to bags |
| No low-MC tokens from non-pump/bonk platforms | MC < $2M only from pump.fun or bonk.fun |
| No soldRatio > 80% signals | Smart money already exiting |
| No trading after 3 consecutive losses | 10min pause to cool down |
| No trading after 0.05 SOL cumulative loss | 30min pause |
| No trading after 0.10 SOL cumulative loss | Session terminated — protect capital |

---

## Safety Filter System (17 Checks)

### Layer 1: Server-Side Pre-filter (API Parameters, Zero Extra Cost)

| # | Filter | Threshold | Source |
|---|--------|-----------|--------|
| 1 | Market Cap | ≥ $200K | signal/list `minMarketCapUsd` |
| 2 | Liquidity | ≥ $80K | signal/list `minLiquidityUsd` |
| 3 | Co-buying wallets | ≥ 3 | signal/list `minAddressCount` |
| 4 | Smart money holding | soldRatioPercent < 80% | signal/list response |

### Layer 2: Client-Side Deep Verification (6-8 API Calls per Token)

| # | Filter | Threshold | Source |
|---|--------|-----------|--------|
| 5 | Holders | ≥ 300 | price_info |
| 6 | Liq/MC Ratio | ≥ 5% | price_info |
| 7 | Top10 Holder % | ≤ 50% | price_info |
| 8 | Holder Density | ≥ 300 per $1M MC | price_info |
| 9 | LP Burn | ≥ 80% | price_info |
| 10 | 1min K-line Pump | ≤ 15% | candles(1m) |
| 11 | Dev Rug Count | = 0 (ZERO tolerance) | memepump/tokenDevInfo |
| 12 | Dev Launches | ≤ 20 | memepump/tokenDevInfo |
| 13 | Dev Holding % | ≤ 15% | memepump/tokenDevInfo |
| 14 | Bundler ATH % | ≤ 25% | memepump/tokenBundleInfo |
| 15 | Bundler Count | ≤ 5 | memepump/tokenBundleInfo |
| 16 | SOL Balance | ≥ buy_sol + 0.05 GAS_RESERVE | all_balances |
| 17 | Honeypot Check | isHoneyPot=false, taxRate ≤ 5 | quote |

---

## Position Management

### Position Sizing (Tiered by Signal Strength)

| Tier | Condition | Position Size |
|------|-----------|---------------|
| **high** | ≥ 8 co-buying wallets | 0.020 SOL |
| **mid** | ≥ 5 co-buying wallets | 0.015 SOL |
| **low** | ≥ 3 co-buying wallets | 0.010 SOL |

| Param | Value |
|-------|-------|
| Max Positions | 6 |
| Slippage | 1% |
| Max Price Impact | 5% |

### Cost Model (Breakeven Calculation)

```
breakeven_pct = (FIXED_COST_SOL / position_sol) × 100 + COST_PER_LEG_PCT × 2

Examples:
  high (0.020): 0.001/0.020×100 + 1.0×2 = 5.0% + 2.0% = 7.0%
  mid  (0.015): 0.001/0.015×100 + 1.0×2 = 6.7% + 2.0% = 8.7%
  low  (0.010): 0.001/0.010×100 + 1.0×2 = 10.0% + 2.0% = 12.0%
```

| Cost Param | Value | Description |
|------------|-------|-------------|
| `FIXED_COST_SOL` | 0.001 | priority_fee × 2 + rent |
| `COST_PER_LEG_PCT` | 1.0% | gas + slippage + DEX fee per leg |

---

## Exit System (7-Layer Priority Chain)

### Take Profit (Cost-Aware, Net Targets + Breakeven Offset)

| Tier | Net Target | Sell % | Trigger (low tier) | Trigger (high tier) |
|------|-----------|--------|-------------------|---------------------|
| TP1 | +5% net | 30% | 5% + 12% = **17%** raw | 5% + 7% = **12%** raw |
| TP2 | +15% net | 40% | 15% + 12% = **27%** raw | 15% + 7% = **22%** raw |
| TP3 | +30% net | 100% | 30% + 12% = **42%** raw | 30% + 7% = **37%** raw |

### Trailing Stop

| Param | Value | Description |
|-------|-------|-------------|
| Activate | +12% after TP1 | Start tracking peak price |
| Distance | 10% | Exit when price drops 10% from peak |

### Stop Loss (Hardcoded + Time-Decay)

**Hard SL:** -10% from entry (SL_MULTIPLIER = 0.90)

**Time-Decay SL** (tightens over time, only when no TP triggered):

| Hold Time | SL Level | Description |
|-----------|----------|-------------|
| 15min+ | -10% | Same as initial |
| 30min+ | -8% | Tighten |
| 60min+ | -5% | Further tighten |

### Emergency & Time Stops

| Condition | Action |
|-----------|--------|
| Liquidity < $5K | Full exit (RUG_LIQ emergency) |
| Position < $0.10 | Dust cleanup |
| 15min K-line reversal (after 30min hold) | Full exit (trend stop) |
| Hold time ≥ 4 hours | Hard time stop — full exit |

---

## Session Risk Controls (v3.0)

| Trigger | Threshold | Action |
|---------|-----------|--------|
| Consecutive losses | ≥ 3 | Pause 10 minutes |
| Cumulative loss | ≥ 0.05 SOL | Pause 30 minutes |
| Cumulative loss | ≥ 0.10 SOL | **Session terminated** — no more trades |
| Profitable trade | Any win | Reset consecutive loss counter |

---

## OKX API Endpoints Used

### Signal API (HMAC-signed)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v6/dex/market/signal/list` | POST | SmartMoney/KOL/Whale buy signals |
| `/api/v6/dex/market/signal/supported/chain` | GET | Supported chains |

### Market API (HMAC-signed)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v6/dex/market/price-info` | POST | MC / Liq / Holders / Price / Top10 |
| `/api/v6/dex/market/token/search` | GET | Community recognized status |
| `/api/v6/dex/market/candles` | GET | 1m/15m K-lines for pump check & trend stop |
| `/api/v6/dex/market/price` | POST | Real-time price monitoring |

### Trenches API (HMAC-signed)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v6/dex/market/memepump/tokenDevInfo` | GET | Dev reputation (rug=0, farm<20, hold<15%) |
| `/api/v6/dex/market/memepump/tokenBundleInfo` | GET | Bundler analysis (ATH<25%, count<5) |

### Trade Execution API (HMAC-signed)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v6/dex/balance/all-token-balances-by-address` | GET | SOL balance check |
| `/api/v6/dex/aggregator/quote` | GET | Quote + honeypot detection |
| `/api/v6/dex/aggregator/swap-instruction` | GET | Swap instruction for Solana |
| `/api/v6/dex/pre-transaction/broadcast-transaction` | POST | Broadcast signed tx |
| `/api/v6/dex/post-transaction/orders` | GET | Order confirmation (≤120s) |

---

## Command Index

| # | Command | Auth | Description |
|---|---------|------|-------------|
| 1 | `strategy-signal-tracker tick` | Yes | Execute one tick: fetch signals, check exits, open positions |
| 2 | `strategy-signal-tracker tick --dry-run` | Yes | Simulate without executing swaps |
| 3 | `strategy-signal-tracker start` | Yes | Start foreground bot (tick every 20s) |
| 4 | `strategy-signal-tracker start --dry-run` | Yes | Start in dry-run mode |
| 5 | `strategy-signal-tracker stop` | No | Stop running bot via PID file |
| 6 | `strategy-signal-tracker status` | No | Show positions, session stats, PnL |
| 7 | `strategy-signal-tracker report` | No | Detailed PnL report |
| 8 | `strategy-signal-tracker history` | No | Trade history |
| 9 | `strategy-signal-tracker reset --force` | No | Clear all state |
| 10 | `strategy-signal-tracker analyze` | Yes | Market analysis (current signals) |
| 11 | `strategy-signal-tracker config` | No | Show all parameters |
| 12 | `strategy-signal-tracker set <key> <value>` | No | Set a config parameter |

---

## Configuration

All parameters are viewable with `strategy-signal-tracker config` and modifiable with `strategy-signal-tracker set <key> <value>`. Changes take effect on the next polling cycle (≤20s) without restarting the bot.

### Key Parameters

| Section | Param | Default | Description |
|---------|-------|---------|-------------|
| Polling | `poll_interval_sec` | 20 | Signal polling interval |
| Signal | `signal_labels` | "1,2,3" | 1=SmartMoney, 2=KOL, 3=Whale |
| Signal | `min_wallet_count` | 3 | Minimum co-buying wallets |
| Signal | `max_sell_ratio` | 0.80 | Skip if smart money sold >80% |
| Safety | `min_mcap` | $200,000 | Minimum market cap |
| Safety | `min_liquidity` | $80,000 | Minimum liquidity |
| Safety | `min_holders` | 300 | Minimum holder count |
| Safety | `min_liq_mc_ratio` | 5% | Minimum liq/mc ratio |
| Safety | `max_top10_holder_pct` | 50% | Maximum top10 holder % |
| Safety | `min_lp_burn` | 80% | Minimum LP burn % |
| Dev | `dev_max_rug_ratio` | 0.0 | Zero tolerance for rug history |
| Dev | `dev_max_launched` | 20 | Max dev launched tokens |
| Dev | `dev_max_hold_pct` | 15% | Max dev holding % |
| Bundler | `bundle_max_ath_pct` | 25% | Max bundler ATH % |
| Bundler | `bundle_max_count` | 5 | Max bundler count |
| Position | `max_positions` | 6 | Max concurrent positions |
| Position | `slippage_pct` | 1% | Swap slippage |
| Cost | `fixed_cost_sol` | 0.001 | Fixed cost per trade (SOL) |
| Cost | `cost_per_leg_pct` | 1.0% | Cost per leg (%) |
| TP | TP1/TP2/TP3 | +5%/+15%/+30% net | Net profit targets |
| SL | `sl_multiplier` | 0.90 | Hard stop loss (-10%) |
| Trail | `trail_activate` | 12% | Trailing stop activation |
| Trail | `trail_distance` | 10% | Trailing stop distance |
| Entry | `max_k1_pct_entry` | 15% | Max 1m pump at entry |
| Session | `max_consec_loss` | 3 | Consecutive loss pause trigger |
| Session | `session_loss_limit_sol` | 0.05 | Cumulative loss pause (SOL) |
| Session | `session_stop_sol` | 0.10 | Cumulative loss halt (SOL) |

---

## Execution Pipeline

### 1. Signal Fetch (Every 20s)

```
POST /api/v6/dex/market/signal/list
  ├── chainIndex: "501" (Solana)
  ├── walletType: "1,2,3"
  ├── minAddressCount: "3"
  ├── minMarketCapUsd: "200000"
  ├── minLiquidityUsd: "80000"
  └── Returns: token info, wallet type, co-buy count, sold ratio
```

### 2. Pre-filter (Zero Extra API Calls)

- `soldRatioPercent < 80%` — smart money still holding
- `triggerWalletCount >= 3` — sufficient co-buying confirmation

### 3. Deep Verification (6-8 API Calls per Token)

```
price_info     → MC, Liq, Holders, Top10, LP burn
token_search   → communityRecognized
candles (1m)   → K1 pump check (<15%)
tokenDevInfo   → rug=0, farm<20, dev hold<15%
tokenBundleInfo → ATH<25%, count<5
all_balances   → SOL balance check
quote          → honeypot detection + quote confirmation
```

### 4. Buy Execution

```
swap-instruction(SOL → Token, amount, slippage=1%)
  → sign_transaction(keypair)
    → broadcast(signed_tx)
      → wait_order(order_id, timeout=120s, poll=3s)
        → record position (with breakeven_pct)
```

### 5. Position Monitoring (Every 20s)

```
for each position:
  price_info → current price, liq, mcap

  ├── Liq < $5K          → RUG_LIQ emergency exit
  ├── Dust (< $0.10)     → cleanup
  ├── Time-decay SL      → 60min+: -5%, 30min+: -8%, 15min+: -10%
  ├── Hard SL             → price ≤ entry × 0.90
  ├── TP (cost-aware)     → TP1: +5%+BE sell 30%, TP2: +15%+BE sell 40%, TP3: +30%+BE sell 100%
  ├── Trailing Stop       → TP1 reached + 12% activate, peak -10% exit
  ├── Trend time stop     → 30min+ and 15m K-line reversal
  └── Hard time stop      → hold ≥ 4 hours
```

---

## Common Pitfalls

| Problem | Wrong | Correct |
|---------|-------|---------|
| TP doesn't profit | TP uses raw pct | `tp_threshold = net_pct + breakeven_pct` |
| Breakeven too high | FIXED_COST=0.004, LEG=1.5% | 0.001 + 1.0% (measured) |
| Ignoring costs | TP 8% then sell | NET 5% triggers at 5%+12% = 17% raw |
| SL too loose | -18% stop loss | -10% (+ time-decay to -5%) |
| Dev rug | No dev check | tokenDevInfo zero tolerance |
| Bundler manipulation | No bundler check | tokenBundleInfo ATH<25% |
| Losing streak spiral | Keep trading | 3 consecutive loss pause / 0.10 SOL halt |
| Auth 401 error | Unix timestamp | ISO 8601 ms: `2026-01-01T00:00:00.000Z` |
| Swap signature rejected | base64 encoding | **base58** encoding for Solana |

---

## Cross-Strategy Collision Detection

The signal tracker checks a shared lock file before opening a position to prevent buying tokens that are already held by other running strategies (e.g., memepump scanner, ranking sniper), avoiding duplicate entries across strategies.

## Security Notes

- Wallet signing via onchainos wallet (TEE signing) — private keys never leave the secure enclave
- API credentials handled by onchainos CLI internally
- Fail-closed: any safety check API failure = skip token (assume unsafe)
- State files use direct write (no atomic rename) — crash may corrupt JSON
