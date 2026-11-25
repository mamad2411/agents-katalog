---
name: ecommerce_competitive_monitor
description: Monitor competitor prices, products, and reviews for e-commerce businesses. Track pricing changes, new product launches, and customer sentiment.
---

# E-Commerce Competitive Monitor

Monitor competitor prices, products, and reviews for e-commerce businesses.

## When to Use

Use this skill when the user wants to:
- Track competitor pricing changes
- Monitor competitor product launches
- Analyze competitor customer reviews
- Set up automated price monitoring alerts
- Research market positioning

## Supported Platforms

- Amazon, Shopify, WooCommerce, Etsy, eBay, Walmart, TikTok Shop

## Workflow

### Step 1: Discovery
Ask the user about their business:
1. What platforms do you sell on?
2. Who are your main competitors? (2-5 competitors)
3. What products/categories do you want to monitor?
4. How often do you want updates? (daily, weekly, real-time)

### Step 2: Setup
For each competitor, gather:
- Store URL or product listing URLs
- Key products to track
- Price ranges they operate in

### Step 3: Research Framework

**Price Monitoring:**
1. Check historical pricing data (if available via web scraping)
2. Identify pricing patterns (sales, promotions, seasonal)
3. Calculate price gaps between competitors
4. Estimate margin impact

**Product Monitoring:**
1. Track new product launches
2. Monitor product descriptions and keyword usage
3. Analyze inventory patterns
4. Identify product gaps in competitor offerings

**Review Analysis:**
1. Gather recent reviews (1-3 months)
2. Categorize feedback themes (positive, negative, feature requests)
3. Calculate satisfaction scores
4. Identify strengths and weaknesses

### Step 4: Output Format

Provide structured findings:

```markdown
## Competitive Intelligence Report

### Price Analysis
| Competitor | Product | Their Price | Your Price | Gap |
|-----------|---------|-------------|------------|-----|
| [Name]    | [SKU]   | $[X]        | $[Y]       | +/-$|

### Key Findings
- [Top 3 pricing insights]
- [Product gap opportunities]
- [Review-based improvements]

### Recommendations
1. [Priority action with specific price/margin impact]
2. [Product opportunity]
3. [Review response strategy]

### Next Steps
- Set up monitoring frequency: [daily/weekly]
- Tools to use: [list]
```

## Best Practices

1. **Be Specific**: Always use actual product names, SKUs, and real prices when available
2. **Cite Sources**: Reference where data was gathered from
3. **Quantify Impact**: Estimate revenue/margin impact of findings
4. **Prioritize**: Highlight the top 3 most actionable insights
5. **Mark Estimates**: Use ⚠️ when data is incomplete or estimated

## Limitations

- Real-time pricing requires API access or scraping (may have limitations)
- Review data limited to publicly available sources
- International platforms may have different data availability
- Always respect robots.txt and platform Terms of Service

## Quick Start

1. **Enter the competitor URL** or product listing
2. **Define your products** to compare against
3. **Set monitoring frequency**: daily/weekly alerts
4. **Receive actionable reports** with specific recommendations

## Example Prompts

- "Monitor Amazon competitor pricing for our laptop products"
- "Track new product launches from our top 5 Shopify competitors"
- "Analyze customer reviews from our main competitor on Etsy"
- "Set up weekly competitive intelligence reports"

## Advanced Use Cases

- **Price Elasticity Analysis**: "What's the optimal price point given competitor pricing?"
- **Product Gap Identification**: "What products do competitors offer that we don't?"
- **Seasonal Trend Analysis**: "How do competitor prices change during holiday seasons?"
- **Review Sentiment Tracking**: "Track competitor review ratings over time"
