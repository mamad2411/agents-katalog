---
name: deep-financial-research
description: Comprehensive financial research using MCP servers (Exa + Financial Datasets). Includes integrated DCF valuation. Use for deep company analysis, due diligence, valuation, competitive landscape, and investment research workflows.
license: Complete terms in LICENSE.txt
---

# Deep Financial Research Skill

Comprehensive financial research skill leveraging connected MCP servers for institutional-grade investment analysis. Includes integrated DCF valuation subskill.

## Connected MCP Servers

| Server | Status | Capabilities |
|--------|--------|--------------|
| **exa** | ✅ Connected | Neural web search, news, sentiment, citation extraction |
| **financial-datasets** | ✅ Connected | Real-time prices, fundamentals, insider trades, analyst estimates |
| **lightpanda** | ⚠️ Optional | Browser automation (requires separate setup) |

## Available Subskills

| Subskill | Trigger | Description |
|----------|---------|-------------|
| **dcf-valuation** | "DCF", "intrinsic value", "fair value", "undervalued" | Discounted cash flow valuation with sensitivity analysis |

## When to Trigger This Skill

### Activate For:
- "Deep dive on [company]" / "Research [ticker]"
- "Due diligence" / "DD on [company]"
- "Investment thesis for..."
- "Competitive landscape of [industry]"
- "Real-time stock price" / "Live market data"
- "Insider trading activity"
- "Analyst estimates and price targets"
- "DCF valuation" / "Intrinsic value" / "Fair value"
- "Is [stock] undervalued/overvalued?"
- "Red flags" / "Risk analysis"
- "Market sentiment on [stock]"

### Don't Trigger For:
- Simple factual questions answerable from knowledge
- Conceptual finance education
- Quick mental math calculations

## Research Workflows

### Workflow 1: Company Deep Dive

**Steps:**
1. Get current price and key metrics via Financial Datasets MCP
2. Search recent news and sentiment via Exa MCP
3. Pull fundamentals (revenue, margins, P/E, debt) via Financial Datasets
4. Check insider trading activity via Financial Datasets
5. Get analyst estimates and price targets
6. Synthesize into investment-ready summary with bull/bear cases

### Workflow 2: Due Diligence

**Steps:**
1. All steps from Company Deep Dive, plus:
2. Search for litigation/regulatory issues: `"[company] lawsuit SEC investigation"`
3. Search for accounting red flags: `"[company] restatement audit resignation"`
4. Research management team backgrounds via Exa
5. Check short interest and institutional ownership
6. Identify key risks and catalysts

### Workflow 3: Competitive Landscape

**Steps:**
1. Map industry via Exa: `"[industry] market share competitive landscape"`
2. Pull fundamentals for all major competitors via Financial Datasets
3. Create comparison table (P/E, growth, margins, ROE)
4. Search for recent M&A or disruptive developments
5. Identify winners/losers and positioning changes

### Workflow 4: DCF Valuation (Subskill)

**Trigger:** User asks for valuation, fair value, intrinsic value, or DCF

**Steps:**
1. Gather 5-year FCF history via Financial Datasets
2. Calculate FCF CAGR and select sustainable growth rate
3. Estimate WACC based on sector and capital structure
4. Project FCF for Years 1-5 with growth decay
5. Calculate terminal value (Gordon Growth, 2.5% terminal rate)
6. Discount to present value → fair value per share
7. Run 3×3 sensitivity analysis (WACC ±1%, terminal growth 2-3%)
8. Validate against reported EV and P/FCF multiples

> 📄 Full DCF workflow: [`subskills/dcf-valuation/SKILL.md`](subskills/dcf-valuation/SKILL.md)

### Workflow 5: Market Sentiment

**Steps:**
1. Search mainstream media via Exa with domain filters
2. Pull analyst estimates and recent revisions via Financial Datasets
3. Check insider sentiment (net buys vs sells)
4. Synthesize bullish vs bearish arguments

## Output Format

### Standard Research Output
```markdown
### [Company/Ticker] - Deep Research Summary

**Current Price:** $X (as of [timestamp])

**Business Overview:**
[1-2 sentence description]

**Key Metrics:**
| Metric | Value | YoY |
|--------|-------|-----|
| Revenue | $X | X% |
| P/E | X.x | - |
| Market Cap | $X | - |

**Recent Developments:**
- [News item 1] — [Source](url)

**Bull Case:** [2-3 key arguments]
**Bear Case:** [2-3 key arguments]
**Key Risks:** [Main risks]
**Confidence:** [High/Medium/Low]
```

### DCF Valuation Output
```markdown
### DCF Valuation: [Company] ([TICKER])

#### Valuation Summary
| Metric | Value |
|--------|-------|
| **Current Price** | $XX.XX |
| **Fair Value** | $XX.XX |
| **Upside/(Downside)** | +XX.X% |
| **Verdict** | Undervalued / Fairly Valued / Overvalued |

#### Key Assumptions
| Input | Value | Source/Notes |
|-------|-------|--------------|
| Current FCF | $X.XXB | Financial Datasets (TTM) |
| FCF Growth Rate (5Y) | X.X% | [CAGR/analyst estimates] |
| Terminal Growth | 2.5% | GDP growth proxy |
| WACC | X.X% | [Sector] adjustment |

#### Sensitivity Analysis
| WACC \ Terminal | 2.0% | 2.5% | 3.0% |
|-----------------|------|------|------|
| [WACC-1%] | $XXX | $XXX | $XXX |
| [Base WACC] | $XXX | $XXX | $XXX |
| [WACC+1%] | $XXX | $XXX | $XXX |

**Conclusion:** [Undervalued/Fairly valued/Overvalued] with [X%] upside/downside.
```

## Example Interactions

**User:** "Do a deep dive on NVDA"
→ Execute Workflow 1 (Company Deep Dive)

**User:** "Research Tesla for investment"
→ Execute Workflow 2 (Due Diligence)

**User:** "What's NVDA worth based on DCF?"
→ Execute Workflow 4 (DCF Valuation subskill)

**User:** "Get real-time NVDA price"
→ Use Financial Datasets MCP for price and stats

**User:** "Analyze the AI chip competitive landscape"
→ Execute Workflow 3 (Competitive Landscape)

**User:** "Do a deep dive on AAPL with DCF valuation"
→ Execute Workflow 1 + Workflow 4 (combined analysis)

## MCP Tool Usage

**Financial Datasets MCP Tools:**
- Real-time and historical stock prices
- Company fundamentals (revenue, margins, P/E, etc.)
- Insider trading data
- Analyst estimates and revisions
- Cash flow statements for DCF

**Exa MCP Tools:**
- Neural web search for news and sentiment
- Domain-filtered searches (bloomberg.com, reuters.com, etc.)
- Citation-rich results with source URLs

## Error Handling

| Issue | Response |
|-------|----------|
| MCP server unavailable | Inform user, use native knowledge with caveats |
| Tool timeout | Retry once, proceed with available data |
| Data discrepancy | Note discrepancy, cite both sources |
| Incomplete data | Clearly state what's missing |

## Caveats

- Financial Datasets provides real-time data during market hours
- Exa search results include timestamps for recency
- DCF valuations are sensitive to input assumptions
- Always cross-validate critical claims across sources
- This skill provides research analysis, not investment advice
- Market data may have brief delays depending on exchange

## Technical Notes

- Both MCP servers are auto-discovered by Qwen Code
- Financial Datasets uses OAuth authentication
- Exa uses API key authentication (configured in MCP settings)
- DCF subskill is triggered by valuation-related keywords
- Tool responses include metadata for source attribution
