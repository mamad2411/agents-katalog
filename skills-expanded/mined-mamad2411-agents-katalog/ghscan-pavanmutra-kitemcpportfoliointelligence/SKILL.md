# India News Tracker

Track and analyze Indian stock market news, corporate announcements, SEBI circulars, bulk/block deals, and earnings calendars. Auto-fetches headlines from MoneyControl, Economic Times, LiveMint, BSE/NSE filings.

## What This Skill Does

- Fetches latest Indian market news from multiple sources
- Categorizes news by impact (1-10 scale)
- Identifies portfolio-relevant alerts
- Filters for actionable opportunities
- No API key required - uses free web sources

## When to Use This Skill

- "Indian market news today", "latest stock news India"
- "BSE NSE announcements today", "quarterly results India"
- "SEBI circular latest", "RBI policy update"
- "bulk deals block deals today India"
- Daily market news briefing for NSE/BSE

## Data Sources (All Free)

1. **MoneyControl** - Primary source for Indian markets
   - URL: https://www.moneycontrol.com/stocks/marketstats/

2. **Economic Times** - Business news
   - URL: https://economictimes.indiatimes.com/markets

3. **LiveMint** - Financial news
   - URL: https://www.livemint.com/markets

4. **BSE/NSE Corporate Filings** - Official announcements
   - URL: https://www.bseindia.com/corporates/
   - URL: https://www.nseindia.com/corporates/

5. **Screener.in** - Corporate actions calendar
   - URL: https://www.screener.in/

## Analysis Framework

### News Categories

| Category | Description | Priority |
|----------|-------------|----------|
| **EARNINGS** | Quarterly results, guidance | HIGH |
| **CORPORATE_ACTION** | Dividend, bonus, split, buyback | HIGH |
| **M&A** | Mergers, acquisitions, stake sales | HIGH |
| **REGULATORY** | SEBI circular, RBI policy | CRITICAL |
| **BULK_DEAL** | Institutional block/bulk deals | MEDIUM |
| **NEW_ORDERS** | Major contract wins | MEDIUM |
| **SECTOR_NEWS** | Policy affecting sectors | HIGH |
| **MANAGEMENT** | Leadership changes | LOW |

### Impact Scoring (1-10)

| Score | Level | Description | Example |
|-------|-------|-------------|---------|
| 9-10 | **CRITICAL** | Market-wide impact | RBI rate decision, SEBI major circular |
| 7-8 | **HIGH** | Sector or large-cap | Reliance results, banking policy |
| 5-6 | **MEDIUM** | Single stock significant | Mid-cap order win, bonus |
| 3-4 | **LOW** | FYI only | Analyst target change |
| 1-2 | **NOISE** | Skip | Rumor, unverified |

### Price-In Check

```
1. When did news break?
   - Pre-market today → NOT priced in
   - During yesterday → PARTIALLY priced
   - > 24 hours → FULLY priced (skip)

2. What's price reaction?
   - > 2% move = reacting
   - Volume > 2x = institutional interest
   
3. Continuation opportunity?
   - Beat + small move = upside
   - M&A + gap to target = arbitrage
   - Corporate action + ex-date > 7 days = window open
```

## Workflow

### Step 1: Fetch News (Max 5 searches)
```
1. "India stock market news today site:moneycontrol.com"
2. "India market today site:economictimes.indiatimes.com"
3. "NSE BSE announcements today bulk deals"
4. "SEBI circular 2026" OR "RBI policy update 2026"
5. "India quarterly results today"
```

### Step 2: Filter & Score
```
- Only past 24 hours (unless corporate action)
- Score each by impact (1-10)
- Deduplicate across sources
- Keep top 10 by impact
```

### Step 3: Categorize
```
- Type: EARNINGS, CORPORATE_ACTION, M&A, REGULATORY, BULK_DEAL, etc.
- Sentiment: BULLISH, BEARISH, NEUTRAL
- Affects Portfolio? YES/NO
```

### Step 4: Verify Prices
```
kite_get_ltp() for any stock-specific news
kite_get_quotes() for volume check
```

### Step 5: Generate Report

```markdown
# India Daily News Briefing

## Date: DD MMM YYYY

### CRITICAL News (Score 9-10)
- [Headline] - Impact: CRITICAL - Symbol: XXX
- [Headline] - Impact: CRITICAL - Symbol: XXX

### HIGH Impact News (Score 7-8)
- [Headline] - Impact: HIGH - Symbol: XXX
- ...

### Portfolio Alerts
- [Holding] - [News] - Action: [HOLD/ADD/REDUCE/SELL]

### Market Mood
- Overall: [BULLISH/BEARISH/NEUTRAL]
- FII/DII: [Today's flows]
- Nifty: [Level and trend]

### Action Items
- [Action 1]
- [Action 2]
- [Action 3]
```

## Output Schema

```json
{
  "date": "YYYY-MM-DD",
  "scan_time": "HH:MM IST",
  "critical_news": [
    {
      "headline": "string",
      "source": "string",
      "news_date": "YYYY-MM-DD",
      "impact": 9,
      "type": "REGULATORY",
      "symbol": "string",
      "sentiment": "BEARISH",
      "priced_in": false,
      "action": "ESCAPE impacted sectors"
    }
  ],
  "high_impact_news": [],
  "portfolio_alerts": [
    {
      "symbol": "RELIANCE",
      "headline": "Q3 results beat",
      "impact": 7,
      "action": "HOLD"
    }
  ],
  "market_mood": {
    "overall_sentiment": "BULLISH",
    "fii_dii_flow": "FII +1200 Cr, DII +800 Cr",
    "nifty_level": 22500,
    "nifty_trend": "ABOVE 50DMA"
  },
  "action_items": [
    "Verify Nifty support at 22400",
    "Check SEBI circular impact on NBFCs"
  ]
}
```

## Save Location
Save to: `reports/YYYY-MM-DD/news_opportunities.json`

## Integration

### Use With
- **india-market-breadth** - Confirm with breadth
- **fii-dii-flow-tracker** - Institutional flow confirmation
- **weekly-fno-trade-planner** - Weekly direction
- **portfolio-scanner** - Alert on holdings

### Input From
- MoneyControl (web)
- Economic Times (web)
- LiveMint (web)
- BSE/NSE filings (web)

## India-Specific Considerations

### Trading Hours (IST)
- Pre-market: 09:00-09:15
- Regular: 09:15-15:30
- Post-market: 15:30-16:00
- News after 15:30 = next day opportunity

### Key Events to Watch
- **RBI Policy** - Bi-monthly (6/year)
- **Union Budget** - February 1
- **Quarterly Results** - Apr, Jul, Oct, Jan
- **FII Data** - Daily around 16:00
- **Block/ Bulk Deals** - End of day

### Sector Rotation Triggers
- **Budget** - Infrastructure, defense, agriculture
- **RBI Policy** - Banks, NBFCs, realty
- **Monsoon** - Agri, FMCG, rural consumption

## Error Handling

| Error | Recovery |
|-------|----------|
| Web search fails | Retry 5x with 5s delay |
| All sources down | Use previous day + mark STALE |
| KiteMCP fails | Skip price verify, note in output |

## Quick Reference

```
News Impact: 9-10 = CRITICAL, 7-8 = HIGH, 5-6 = MEDIUM
Types: EARNINGS, CORPORATE_ACTION, M&A, REGULATORY, BULK_DEAL
Filter: Only 24h old unless corporate action
Min Market Cap: ₹500 Cr
```

## Skill Metadata

- **Type**: News Analysis / Market Intelligence
- **API Required**: No (free sources)
- **Execution Time**: 3-5 minutes
- **Update Frequency**: Daily (before market open)
- **Confidence Level**: Medium-High (verify with prices)