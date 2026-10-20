# Market Intelligence Skill

Real-time market sentiment and narrative detection for trading edge.

## Signal Sources

### Primary Feeds
- Crypto Fear & Greed Index
- Funding rates (perp markets)
- Exchange inflow/outflow
- Options skew (if available)

### Social Signals
- Twitter/X high-impact accounts
- Reddit sentiment (r/cryptocurrency, r/wallstreetbets)
- News aggregation

## Analysis Framework

### Sentiment Classification
```
Noise → Ignore
FUD → Contrarian opportunity (if technicals strong)
Alpha → Confirm with technicals before acting
```

### Narrative Detection
Track emerging themes:
- ETF approvals/denials
- Regulatory events
- Macro correlations (rates, USD, gold)
- Sector rotation (DeFi, AI, Meme, etc.)

### Multi-Agent Analysis

**GLM5 (Deep Research)**:
- Macro context analysis
- Event impact modeling
- Historical analogs
- Narrative durability assessment

**MiniMax (Quick Scan)**:
- Real-time sentiment pulse
- Trending keywords
- Momentum shift detection

## Signal Confidence Levels

| Source | Weight | Latency |
|--------|--------|---------|
| On-chain | High | 10m |
| Funding rates | High | Real-time |
| Social volume | Medium | 5m |
| News headlines | Medium | 1-30m |
| Rumor/speculation | Low | Variable |

## Alert Triggers

Auto-monitor for:
- Funding rate spikes (>50% annualized)
- Exchange inflow surges (>$100M)
- Volatility expansion (ATR breakout)
- Correlation breakdowns

## Commands

- `/sentiment [asset]` - Current mood
- `/narrative` - Active themes
- `/alerts` - Configure watch triggers
- `/funding` - Perp market heatmap
