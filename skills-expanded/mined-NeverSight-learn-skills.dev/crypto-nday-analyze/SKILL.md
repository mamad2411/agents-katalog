---
name: crypto-nday-analyze
description: "Execute Solana customizable N-day (7-365 days) technical analysis, outputting regression channel chart, key indicators, and scenario playbook. Use when user requests SOL analysis, Solana price analysis, SOL technical indicators, trend analysis, or asks for SOL N-day report. Triggers include \"SOL 14天分析\", \"SOL 30天分析\", \"crypto-nday-analyze 30\", \"Solana N day analysis\", \"分析 SOL\", \"SOL 技術分析\"."
---

# crypto-nday-analyze

**N-day technical analysis for cryptocurrencies with linear regression channel charts**

Execute customizable N-day (7-365 days) technical analysis for any cryptocurrency, outputting a comprehensive Markdown report, regression channel chart, and key indicator playbook.

## Installation

```bash
# Install the skill
npx skills add https://github.com/nandemo-agent/crypto-nday-analyze

# Install dependencies
cd ~/.agents/skills/crypto-nday-analyze
npm install
pip3 install -r requirements.txt
```

Or use directly via npx:

```bash
npx @nandemo-agent/crypto-nday-analyze SOL 30
```

## When to Use This Skill

Use when the user requests:

1. **Crypto technical analysis** - "分析 SOL", "給我 BTC 30 天報表"
2. **Price trend analysis** - "SOL 最近走勢如何"
3. **N-day reports** - "幫我產生 SOL 14 天分析", "30 day analysis for ETH"
4. **Trading signals** - "SOL 現在該買還是賣", "給我技術指標"
5. **Regression channel** - "畫一下通道圖", "show me the trend channel"

### Trigger Phrases

- "幫我產生 SOL 30 天報表"
- "分析 BTC 技術指標"
- "ETH 7 天分析"
- "crypto-nday-analyze SOL 30"
- "Give me a 30-day analysis for Solana"
- "畫 SOL 通道圖"
- "SOL technical indicators"

## Usage

### Basic Command

```bash
crypto-nday-analyze <SYMBOL> <DAYS>
```

**Parameters:**
- `SYMBOL` - Cryptocurrency symbol (SOL, BTC, ETH, ADA, etc.)
- `DAYS` - Number of days to analyze (7-365)

### Common Examples

```bash
# Solana 30-day analysis (most common)
crypto-nday-analyze SOL 30

# Bitcoin 14-day analysis
crypto-nday-analyze BTC 14

# Ethereum 90-day analysis
crypto-nday-analyze ETH 90

# Quick 7-day check
crypto-nday-analyze SOL 7
```

### Advanced Options

```bash
crypto-nday-analyze <SYMBOL> <DAYS> [OPTIONS]

Options:
  -o, --output <path>      Output directory (default: current directory)
  -f, --format <type>      Output format: md, json (default: md)
  --chart-only             Generate chart only (no report)
  --no-chart               Skip chart generation (report only)
  -e, --exchange <name>    Data source: binance, coingecko (default: binance)
  --json                   Output JSON to stdout
  -h, --help               Show help
```

### Advanced Examples

```bash
# Save to specific directory
crypto-nday-analyze SOL 30 --output ~/reports

# JSON output for programmatic use
crypto-nday-analyze BTC 30 --format json

# Chart only (no report)
crypto-nday-analyze SOL 30 --chart-only

# JSON to stdout (for piping)
crypto-nday-analyze ETH 30 --json | jq '.signal.signal'

# Use CoinGecko instead of Binance
crypto-nday-analyze SOL 30 --exchange coingecko
```

## Output Files

For a command like `crypto-nday-analyze SOL 30`:

1. **Report:** `SOL_30D_TA_Report.md` - Comprehensive technical analysis
2. **Chart:** `SOL_30D_chart.png` - Linear regression channel visualization

### Report Contents

- 📊 Executive Summary
  - Regression channel metrics (slope, bands, position)
  - Current price and trend direction
  
- 🎯 Support & Resistance Levels
  - R1, R2, R3 (resistance)
  - S1, S2, S3 (support)
  
- 🔍 Technical Indicators (29+ indicators)
  - **Trend:** EMA, MACD, ADX, Ichimoku, Parabolic SAR
  - **Momentum:** RSI, Stochastic, KDJ
  - **Volatility:** Bollinger Bands, ATR
  - **Volume:** OBV, VWAP
  
- ⚠️ Key Alerts
  - Divergence detection (RSI, MACD)
  - Overbought/oversold signals
  
- 🎭 Three Scenario Playbook
  - Scenario A: Breakout (bullish)
  - Scenario B: Breakdown (bearish)
  - Scenario C: Consolidation (neutral)
  
- 🏁 Conclusion & Recommendations
  - Overall signal (BULLISH/BEARISH/NEUTRAL)
  - Confidence score
  - Short/medium-term strategy

### Chart Features

- Candlestick price action
- Linear regression channel (±2σ)
- Bollinger Bands overlay
- RSI indicator panel
- Volume bars (color-coded)
- Channel touch markers
- Current price highlight

## Agent Workflow

When a user requests crypto analysis:

### Step 1: Parse Request

Extract:
- **Symbol** - SOL, BTC, ETH, etc.
- **Days** - Default 30 if not specified
- **Output preference** - Chart, report, or both

### Step 2: Execute Analysis

```bash
crypto-nday-analyze <SYMBOL> <DAYS> --output <workspace_path>
```

### Step 3: Present Results

**Structured Response Format:**

```markdown
📊 <SYMBOL> <DAYS>-Day Technical Analysis

**Current Price:** $XX.XX
**Overall Signal:** BULLISH/BEARISH/NEUTRAL (XX% confidence)
**Channel Position:** XX% (near upper/lower/mid)

**Key Findings:**
- Trend: [slope direction]
- RSI: [value] ([overbought/oversold/neutral])
- ADX: [value] ([trend strength])
- Divergence: [any alerts]

**Resistance:** R1: $XX | R2: $XX | R3: $XX
**Support:** S1: $XX | S2: $XX | S3: $XX

**Scenario Playbook:**
- 🟢 Breakout above $XX → Targets: $XX, $XX
- 🔴 Breakdown below $XX → Targets: $XX, $XX
- 🟡 Consolidation $XX-$XX → Mean reversion

📁 Full report: [filename].md
📊 Chart: [filename].png
```

### Step 4: Follow-up Suggestions

Offer:
- "Want me to analyze another timeframe?"
- "Should I check other coins?"
- "Need help interpreting the signals?"

## Supported Cryptocurrencies

**Primary (CoinGecko ID mapped):**
- BTC (Bitcoin)
- ETH (Ethereum)
- SOL (Solana)
- BNB (Binance Coin)
- XRP (Ripple)
- ADA (Cardano)
- DOGE (Dogecoin)
- MATIC (Polygon)
- DOT (Polkadot)
- AVAX (Avalanche)

**Others:** Any symbol available on CoinGecko (will attempt direct lookup)

## Technical Indicators Reference

### Trend Indicators

| Indicator | Signals |
|-----------|---------|
| **EMA 12/26** | Golden/Death cross, trend direction |
| **MACD** | Bullish/bearish crossover, divergence |
| **ADX** | Trend strength (>50 very strong, >25 strong) |
| **Ichimoku** | Cloud position, conversion/base line |
| **Parabolic SAR** | Stop-and-reverse levels |

### Momentum Indicators

| Indicator | Signals |
|-----------|---------|
| **RSI** | Overbought (>70), Oversold (<30), Divergence |
| **Stochastic** | %K/%D crossover, overbought/oversold |
| **KDJ** | J-line extremes, K/D crossover |

### Volatility Indicators

| Indicator | Signals |
|-----------|---------|
| **Bollinger Bands** | Band squeeze/expansion, price position |
| **ATR** | Volatility measurement |

### Volume Indicators

| Indicator | Signals |
|-----------|---------|
| **OBV** | Volume trend confirmation |
| **VWAP** | Price vs volume-weighted average |

## Regression Channel Explained

**What is it?**
- Linear regression line (best-fit trend)
- ±2σ standard deviation bands
- Shows channel boundaries and breakout levels

**Key Metrics:**
- **Slope:** USD/day (trend direction and strength)
- **R²:** Fit quality (0-1, higher = better fit)
- **Position:** % within channel (0% = lower band, 100% = upper band)

**Interpretation:**
- **Near upper band (>70%):** Potential resistance, watch for reversal
- **Near lower band (<30%):** Potential support, watch for bounce
- **Mid-channel (30-70%):** Neutral, awaiting direction
- **Breakout:** Price above upper or below lower band (trend change)

## Error Handling

**Common Issues:**

1. **Symbol not found**
   ```
   ❌ Invalid symbol or no data available
   ```
   → Try common symbols (BTC, ETH, SOL) or check CoinGecko

2. **Days out of range**
   ```
   ❌ Days must be between 7 and 365
   ```
   → Use 7-365 day range

3. **Python dependencies missing**
   ```
   ❌ Failed to start Python analyzer
   ```
   → Run `pip3 install -r requirements.txt`

4. **API rate limit**
   ```
   ❌ Failed to fetch data from CoinGecko
   ```
   → Wait a few minutes, CoinGecko has rate limits

## Best Practices

### For Agents

1. **Always specify days** - Default to 30 if user doesn't say
2. **Mention both files** - Report + chart in response
3. **Highlight key alerts** - Divergence, overbought/oversold
4. **Explain signals** - Don't just say "BULLISH", explain why
5. **Include scenarios** - Give user options (breakout/breakdown/consolidation)
6. **Add disclaimer** - "This is technical analysis, not financial advice"

### For Users

1. **Choose appropriate timeframe**
   - 7-14 days: Short-term trading
   - 30 days: Medium-term trends
   - 90+ days: Long-term analysis

2. **Combine with fundamentals** - Technical analysis alone is incomplete

3. **Watch for divergences** - RSI/MACD divergence can signal reversals

4. **Use scenario playbook** - Prepare for multiple outcomes

## Examples in Context

### Example 1: User asks "幫我產生 SOL 30 天報表"

```bash
crypto-nday-analyze SOL 30 --output ~/.openclaw/workspace
```

**Agent response:**
> 📊 SOL 30天技術分析完成
> 
> **當前價格:** $84.95  
> **整體訊號:** NEUTRAL (63.8% 信心度)  
> **通道位置:** 75.4% (偏上軌)
> 
> **關鍵發現:**
> - 趨勢: 下降通道 (-0.63 USD/天)
> - RSI: 30.90 (超賣區邊緣) + 看漲背離 ⚠️
> - ADX: 63.27 (極強趨勢)
> 
> **支撐壓力:**
> - R1: $91.59 | R2: $97.62 | R3: $117.30
> - S1: $78.10 | S2: $77.74 | S3: $64.61
> 
> **情境劇本:**
> - 🟢 突破 $91.59 上軌 → 目標 $97.62, $104.52
> - 🔴 跌破 $78.10 中軌 → 目標 $77.74, $64.61
> - 🟡 區間震盪 $78-$92 → 短線交易
> 
> 📁 完整報告: `SOL_30D_TA_Report.md`  
> 📊 通道圖: `SOL_30D_chart.png`

### Example 2: User asks "BTC 14 day analysis"

```bash
crypto-nday-analyze BTC 14
```

**Agent response:**
> 📊 BTC 14-Day Technical Analysis
> 
> **Current Price:** $XX,XXX  
> **Signal:** BULLISH (72% confidence)  
> **Channel Position:** 45% (mid-channel)
> 
> **Key Findings:**
> - Uptrend: +$XXX/day
> - Golden cross confirmed (EMA 12 > EMA 26)
> - RSI: 58 (neutral, room to grow)
> - Volume confirmation: 125%
> 
> **Next levels to watch:**
> - Breakout: $XX,XXX → $XX,XXX
> - Support: $XX,XXX → $XX,XXX
> 
> 📁 Reports available in current directory

### Example 3: Quick check "SOL 現在該買還是賣"

```bash
crypto-nday-analyze SOL 7 --json
```

Parse JSON and respond:
> 📊 SOL 快速技術分析 (7天)
> 
> **訊號:** BEARISH (68% 信心)  
> **建議:** 觀望或等待更低點
> 
> **原因:**
> - 短期下降趨勢
> - RSI 42 (中性偏弱)
> - 未觸及超賣區,下跌空間仍存在
> 
> 想看完整 30 天分析嗎?

## Security & Privacy

**Data Sources:**
- CoinGecko public API (no authentication required)
- No personal data collected
- No API keys needed

**File Output:**
- Reports saved to specified directory only
- No data sent to external services (except CoinGecko for price data)

**Dependencies:**
- All open-source Python libraries
- Auditable code in `src/` directory

## Troubleshooting

### Chart not generated

**Check:**
1. Python dependencies installed: `pip3 install -r requirements.txt`
2. Matplotlib backend configured: `export MPLBACKEND=Agg`
3. Write permissions in output directory

### Incorrect symbol

**Solutions:**
- Use uppercase (SOL not sol)
- Check CoinGecko for exact symbol
- Try common alternatives (e.g., MATIC vs POL)

### API timeout

**Solutions:**
- Check internet connection
- Reduce days (API loads less data)
- Wait and retry (rate limit)

## Changelog

### v0.1.0 (Initial Release)
- ✅ 29+ technical indicators
- ✅ Linear regression channel
- ✅ Markdown report generation
- ✅ Chart visualization
- ✅ Support/resistance calculation
- ✅ Three scenario playbook
- ✅ Divergence detection
- ✅ CoinGecko integration

## Roadmap

- [ ] Multiple exchange support (Binance, Coinbase)
- [ ] Real-time WebSocket data
- [ ] Custom indicator plugins
- [ ] HTML interactive reports
- [ ] Backtesting framework
- [ ] Alert notifications

## License

MIT

## Credits

**Developed by:** nandemo-agent  
**Data Provider:** CoinGecko  
**Inspired by:** crypto-ta-analyzer skill

---

**Meta:**
- Skill name: `crypto-nday-analyze`
- Category: Trading, Technical Analysis, Cryptocurrency
- Complexity: Medium
- Dependencies: Python 3.8+, Node.js 18+
