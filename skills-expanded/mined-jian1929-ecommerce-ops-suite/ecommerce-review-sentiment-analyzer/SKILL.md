---
name: ecommerce_review_sentiment_analyzer
description: Analyze customer review sentiment for e-commerce products. Extract insights from positive/negative reviews, identify improvement opportunities, and track sentiment trends over time.
version: 1.0.0
---

# E-Commerce Review Sentiment Analyzer

Automatically analyze customer reviews to extract actionable insights for product improvement and customer satisfaction.

## When to Use

Use this skill when the user wants to:
- Understand what customers love/hate about their products
- Identify product improvement opportunities from reviews
- Track customer sentiment over time
- Compare sentiment between products or time periods
- Generate review summaries for product pages

## Supported Platforms

- Amazon, Shopify, Walmart, eBay, Etsy, Google Reviews, Trustpilot

## Workflow

### Step 1: Gather Reviews
Ask the user for:
1. Product URL or ASIN/SKU
2. Number of reviews to analyze (recommended: 20-100 for quality insights)
3. Time period (last 30/60/90 days, or all-time)

### Step 2: Extraction
For each review, capture:
- Star rating (1-5)
- Review text
- Date posted
- Verified purchase badge (if available)
- Helpful votes (if available)

### Step 3: Sentiment Analysis

**Positive Signals (4-5 stars):**
- What features do customers praise?
- What use cases work well?
- What keeps customers coming back?

**Negative Signals (1-2 stars):**
- What complaints appear most?
- What are the common defects mentioned?
- What expectations weren't met?

**Neutral Feedback (3 stars):**
- Mixed feelings to investigate
- Potential improvements noted

### Step 4: Theme Extraction
Group reviews by theme:
- Quality/Durability
- Value for Money
- Ease of Use
- Customer Service
- Shipping/Packaging
- Design/Aesthetics
- Performance

### Step 5: Output Format

```markdown
## Review Sentiment Analysis Report

### Overview
| Metric | Value |
|--------|-------|
| Total Reviews Analyzed | N |
| Average Rating | X.X/5 |
| Positive (4-5★) | XX% |
| Neutral (3★) | XX% |
| Negative (1-2★) | XX% |

### Top 5 Positive Themes
1. [Theme]: [Count] mentions - "Representative quote"
2. ...

### Top 5 Negative Themes
1. [Theme]: [Count] mentions - "Representative quote"
2. ...

### Sentiment by Category
| Category | Positive | Neutral | Negative |
|----------|----------|---------|----------|
| Quality | 75% | 15% | 10% |
| Value | 60% | 25% | 15% |
| ...

### Key Insights
1. **Strength**: [What customers love most]
2. **Opportunity**: [Biggest improvement area]
3. **Risk**: [Critical issue to address immediately]

### Recommendations
1. [Specific action with expected impact]
2. [Product improvement suggestion]
3. [Customer communication strategy]

### Review Response Templates
**For Positive Reviews:**
> Thank you for your wonderful review! We're thrilled you enjoyed [specific feature]. Your support means the world to us.

**For Negative Reviews:**
> We're sorry to hear about your experience with [issue]. We'd love to make this right. Please contact us at [support email].
```

## Best Practices

1. **Sample Size**: Minimum 20 reviews for valid insights, 100+ for statistical significance
2. **Time Weighting**: Recent reviews are more relevant than older ones
3. **Verified Badge**: Weight verified purchase reviews higher
4. **Handle Extremes**: Ignore obvious fake reviews (all caps, no detail, etc.)
5. **Quantify**: Always estimate percentage of reviews mentioning each theme

## Limitations

- Review text quality varies (short reviews = less insight)
- Some platforms restrict review scraping
- Sentiment analysis has ~85% accuracy, validate with manual spot-check
- International reviews may require translation

## Quick Start

1. **Provide product URL** or list of review URLs
2. **Select time period** (last 30/60/90 days recommended)
3. **Receive actionable report** with specific improvement suggestions

## Example Prompts

- "Analyze reviews for my Amazon product ASIN B08N5WRWNW"
- "What do customers complain about most in our Shopify reviews?"
- "Compare sentiment between our two best-selling products"
- "Track review sentiment trends for Q1 2024"
- "Generate review highlights for our product page"
