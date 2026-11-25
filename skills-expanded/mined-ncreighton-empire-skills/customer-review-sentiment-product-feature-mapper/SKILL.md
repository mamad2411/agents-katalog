---
name: customer-review-sentiment-product-feature-mapper
description: "Extract sentiment from customer reviews across Amazon, Etsy, Shopify, Google and map complaints/praise to product features. Use when the user needs feature prioritization, competitive analysis, or data-driven product roadmap creation from real customer feedback."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": [
          "OPENAI_API_KEY",
          "GOOGLE_SHEETS_API_KEY",
          "SERPAPI_KEY",
          "SLACK_WEBHOOK_URL"
        ],
        "bins": []
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "📊"
    }
  }
---

# Customer Review Sentiment → Product Feature Mapper

## Overview

This skill transforms raw customer reviews into actionable product intelligence by automating the extraction, analysis, and mapping of sentiment to specific product features across all major review platforms.

**What It Does:**
- Scrapes and aggregates reviews from Amazon, Etsy, Shopify, Google Reviews, and Trustpilot
- Performs multi-dimensional sentiment analysis (positive/negative/neutral) at feature level
- Maps complaints and praise to exact product attributes (durability, price, ease-of-use, design, etc.)
- Identifies feature gaps by comparing your product to top competitors
- Quantifies feature demand by aggregating review volume per feature category
- Generates prioritized product roadmap recommendations with exact customer quotes as evidence
- Exports results to Google Sheets, Slack, or PDF reports for team collaboration

**Why It Matters:**
Stop making product decisions based on assumptions. This skill gives you concrete, quantified evidence of what customers actually want. You'll know exactly which features drive satisfaction, which create churn, and where competitors are winning.

**Integrations:**
- Slack (auto-send summaries to product channels)
- Google Sheets (live dashboard updates)
- WordPress (embed sentiment charts in blog posts)
- GitHub (create feature request issues automatically)
- Zapier/Make (trigger workflows on high-priority insights)

---

## Quick Start

Try these prompts immediately:

```
Analyze reviews for [PRODUCT NAME] from Amazon and create a feature priority 
matrix showing which complaints appear most frequently. Include exact quotes 
and sentiment scores.
```

```
Compare customer sentiment for my yoga mat vs the top 3 competitors on Etsy. 
Show me where I'm losing and winning by feature. Map results to a product 
roadmap with quarterly milestones.
```

```
Pull all 1-star and 2-star reviews for my Shopify store from the last 90 days. 
Group complaints by feature category, quantify by volume, and suggest fixes 
with competitive examples. Export to Google Sheets and Slack.
```

```
Generate a "Voice of Customer" report: aggregate all reviews across Amazon, 
Google, and Trustpilot for [PRODUCT]. Show sentiment trends over time. 
Highlight emerging customer needs not yet addressed by competitors.
```

---

## Capabilities

### 1. **Multi-Platform Review Aggregation**
Automatically collects reviews from:
- **Amazon** (product ratings, verified purchase reviews, images)
- **Etsy** (shop and product-level reviews, response tracking)
- **Shopify** (native reviews via Shopify API)
- **Google Reviews** (location/product reviews via Google My Business API)
- **Trustpilot** (company-wide sentiment trends)

*Example:*
```
Collect all reviews for SKU-12345 from Amazon (last 6 months) and Shopify 
(last 90 days). Filter for 1-3 stars only. Include review date, reviewer name, 
rating, and full text.
```

### 2. **AI-Powered Feature Extraction & Sentiment Mapping**
Uses GPT-4 to:
- Identify specific product features mentioned in each review (e.g., "battery life," "noise level," "shipping speed")
- Assign sentiment polarity to each feature mention (positive/negative/neutral with confidence score 0-1)
- Extract actionable pain points and praise points
- Normalize feature language across reviews (e.g., "durability" = "longevity" = "built to last")

*Example output:*
```json
{
  "review_id": "AMZ-98765",
  "rating": 2,
  "text": "Battery dies after 2 hours. Terrible.",
  "features_extracted": [
    {
      "feature": "battery_life",
      "sentiment": "negative",
      "confidence": 0.97,
      "quote": "Battery dies after 2 hours"
    }
  ]
}
```

### 3. **Competitive Feature Benchmarking**
Analyzes competitor products to:
- Extract features they emphasize (from reviews AND product descriptions)
- Compare sentiment scores feature-by-feature (your product vs competitors)
- Identify feature gaps (features competitors have that you don't)
- Quantify competitive advantage (features where you win significantly)

*Example:*
```
Show me a comparison table: My Bluetooth speaker vs JBL Flip 6 vs UE Boom 3. 
Metrics: sound quality sentiment (1-10), durability sentiment, price satisfaction, 
ease of use. Show exact review quotes for each metric.
```

### 4. **Feature Demand Quantification**
Calculates:
- **Mention frequency:** How many reviews mention each feature?
- **Sentiment volume:** Total positive vs negative mentions per feature
- **Trend analysis:** Is demand for a feature increasing/decreasing over time?
- **Correlation:** Which features drive 5-star ratings? Which drive 1-star?

*Example dashboard metric:*
```
Feature: "Fast Charging"
- Mentioned in: 142 reviews (18% of all reviews)
- Sentiment: 78% positive, 12% negative, 10% neutral
- Trend: +23% month-over-month mentions
- 5-star correlation: 0.73 (strong positive)
- Competitor gap: 3 competitors emphasize this; you don't
```

### 5. **Prioritized Product Roadmap Generation**
Creates actionable roadmaps with:
- **Priority score** (0-100) based on demand volume + sentiment strength + competitive gap
- **Customer impact** (estimated satisfaction increase if implemented)
- **Implementation effort** (based on feature complexity heuristics)
- **Exact customer quotes** as proof points
- **Competitor benchmarks** showing how feature is implemented elsewhere
- **Recommended timeline** (immediate fixes, Q1-Q4 planning)

*Example:*
```
Priority: 87/100 | Feature: "Noise Cancellation"
Impact: +15% satisfaction (est.) | Effort: Medium | Timeline: Q2
Mentions: 247 reviews | Sentiment: 82% positive | Gap: Competitor X has this

Top quote: "Love the speaker but can't use in coffee shops—too much ambient noise"
Other quotes: [3 more examples]

Competitor example: Brand Y uses [specific tech]. Review sentiment: 88% positive.
```

### 6. **Automated Reporting & Distribution**
Exports insights to:
- **Google Sheets** (live dashboard; auto-updates daily)
- **Slack** (daily/weekly digests to product channels with priority alerts)
- **PDF reports** (executive summaries with visualizations)
- **CSV/JSON** (raw data for further analysis)
- **GitHub issues** (auto-creates feature requests with customer evidence)

---

## Configuration

### Required Environment Variables

```bash
# OpenAI API for sentiment analysis & feature extraction
OPENAI_API_KEY=sk-...

# Google APIs (Sheets, Reviews)
GOOGLE_SHEETS_API_KEY=...
GOOGLE_REVIEWS_API_KEY=...

# Review platform APIs
AMAZON_API_KEY=...
AMAZON_API_SECRET=...
SHOPIFY_API_KEY=...
SHOPIFY_STORE_URL=https://yourstore.myshopify.com

# Optional: for competitive analysis
SERPAPI_KEY=...  # Web search for competitor reviews

# Optional: for Slack/GitHub distribution
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
GITHUB_TOKEN=...
```

### Configuration Options

```yaml
review_sources:
  amazon:
    enabled: true
    asin: "B0123456789"
    days_back: 180
    min_length: 20  # filter very short reviews
  
  etsy:
    enabled: true
    shop_id: "12345678"
    product_id: "9876543"
  
  shopify:
    enabled: true
    filter_status: "published"
  
  google_reviews:
    enabled: true
    place_id: "ChIJ..."

sentiment_analysis:
  model: "gpt-4"
  temperature: 0.3
  language: "en"
  feature_normalization: true

output:
  google_sheets:
    enabled: true
    sheet_id: "1A2B3C4D5E..."
    overwrite_mode: "append"
  
  slack:
    enabled: true
    channel: "#product-insights"
    frequency: "daily"  # or weekly, monthly
    mention_threshold: 50  # only alert on features w/ 50+ mentions
  
  github:
    enabled: false
    repo: "owner/product-roadmap"
    label: ["feature-request", "customer-feedback"]
```

---

## Example Outputs

### Feature Sentiment Matrix

```
Feature              | Mentions | % Positive | Trend    | Priority
─────────────────────┼──────────┼────────────┼──────────┼─────────
Battery Life         | 312      | 65%        | ↑ +18%   | 94/100
Sound Quality        | 287      | 88%        | ↑ +5%    | 82/100
Price Value          | 256      | 52%        | ↓ -12%   | 76/100
Ease of Use          | 198      | 91%        | → 0%     | 71/100
Design/Aesthetics    | 167      | 84%        | ↑ +7%    | 68/100
Durability           | 145      | 59%        | ↓ -8%    | 64/100
Bluetooth Range      | 98       | 73%        | → 0%     | 52/100
```

### Competitive Comparison (Sentiment by Feature)

```
Feature: "Battery Life"

Your Product (Speaker X):
- Mentions: 312 | Positive: 65% | Avg Rating: 3.7/5
- Key complaint: "Only lasts 6 hours"
- Top quote: "Good sound but dies too fast"

Competitor A (JBL Flip 6):
- Mentions: 456 | Positive: 79% | Avg Rating: 4.4/5
- Key advantage: "20-hour battery"
- Top quote: "Best battery life in this price range"

Competitor B (UE Boom 3):
- Mentions: 389 | Positive: 72% | Avg Rating: 4.1/5
- Key advantage: "15-hour battery"
- Top quote: "Battery lasts longer than expected"

Your Gap: -14 percentage points in positive sentiment
Action: Extend battery life or market existing battery feature better
```

### Priority Roadmap

```
Q2 2024 - URGENT (Priority 80+)
┌─────────────────────────────────────────────┐
│ Battery Life Enhancement                     │
│ Priority: 94/100 | Effort: High | Impact: +18% satisfaction
│ Customer evidence: 312 mentions, 65% positive
│ Quote: "Lasts only 6 hours—worse than competitors"
│ Competitor benchmark: JBL Flip 6 (20h) has 79% positive sentiment
└─────────────────────────────────────────────┘

Q3 2024 - HIGH PRIORITY (Priority 70-79)
┌─────────────────────────────────────────────┐
│ Improve Mid-Range Price Competitiveness     │
│ Priority: 76/100 | Effort: Medium | Impact: +12% satisfaction
│ Evidence: 256 mentions, only 52% positive sentiment
│ Quote: "Great product but expensive for what you get"
└─────────────────────────────────────────────┘

Q4 2024 - MEDIUM PRIORITY (Priority 60-69)
┌─────────────────────────────────────────────┐
│ Upgrade Durability/Materials                │
│ Priority: 64/100 | Effort: High | Impact: +8% satisfaction
│ Evidence: 145 mentions, 59% positive sentiment
│ Quote: "Buttons stopped working after 8 months"
└─────────────────────────────────────────────┘
```

### Voice of Customer Report (Slack Digest)

```
📊 CUSTOMER INSIGHTS DIGEST — Week of Jan 15

🔴 URGENT ALERTS
• Battery Life complaints spiked 45% this week (89 mentions)
  Top quote: "Dies after 6 hours of use. Very disappointed."
  Action: Review power management firmware

🟢 WINS TO CELEBRATE
• Sound Quality consistently praised (88% positive)
  Top quote: "Crystal clear audio—best in its class"

📈 EMERGING TRENDS
• "Waterproof" mentioned in 23 new reviews (↑ 340% YoY)
  Customer need: Not currently a feature for your product
  Competitor: Brand Y now emphasizes waterproofing

🎯 THIS WEEK'S ROADMAP RECOMMENDATION
Prioritize: Battery life fix (94/100)
Quick win: Add waterproof rating to packaging/marketing (low effort)
```

---

## Tips & Best Practices

### 1. **Segment by Customer Segment**
Run separate analyses for:
- New customers (first 2 weeks) vs long-term users (6+ months)
- Different price tiers (if selling multiple variants)
- Geographic regions (different feature preferences by region)
- Use cases (professionals vs hobbyists)

*Example:*
```
Compare sentiment for [PRODUCT] between US (reviews) vs EU (reviews).
Show which features matter most to each region. Are pricing expectations 
different?
```

### 2. **Track Sentiment Trends Over Time**
Set up weekly/monthly tracking to:
- Detect when a feature sentiment suddenly drops (quality regression?)
- Monitor competitor sentiment movement
- Measure impact of product updates on review sentiment

*Action:*
```
Create a Google Sheet showing [PRODUCT] battery life sentiment over 12 months.
Did the recent firmware update improve sentiment? By how much?
```

### 3. **Validate with Mention Frequency Thresholds**
Ignore features mentioned in <10 reviews (noise).
Only prioritize features with 50+ mentions (genuine customer need).

### 4. **Pair Qualitative Quotes with Quantitative Data**
Never rely on sentiment % alone. Always:
- Show actual review quotes (proof)
- Include mention counts (volume = urgency)
- Note trends (is this growing/shrinking demand?)

### 5. **Monthly Competitive Benchmarking**
Update competitor analysis monthly. Features competitors add quickly become table-stakes.

### 6. **Export for Team Distribution**
- Share Google Sheet dashboard with Product/Marketing/Engineering
- Set Slack alerts for priority items (90+/100 priority)
- Create GitHub issues for engineering with customer evidence

---

## Safety & Guardrails

### What This Skill Will NOT Do

**❌ Privacy violations:**
- Does not attempt to re-identify anonymous reviewers
- Does not store personally identifiable information beyond review author name (public data)
- Does not scrape contact information for spam campaigns
- Complies with GDPR/CCPA by handling data as read-only analysis

**❌ Bias and fairness:**
- Cannot guarantee unbiased sentiment classification (GPT-4 has known biases)
- May over-weight extreme (1-star/5-star) reviews relative to moderate reviews
- Does not detect review manipulation or fake reviews (requires separate fraud detection)
- May misinterpret sarcasm or cultural context in reviews

**❌ Competitive espionage:**
- Does not recommend unethical actions based on competitor analysis
- Only analyzes publicly available reviews
- Does not attempt to identify confidential competitor roadmaps

**❌ Data accuracy guarantees:**
- Feature extraction is ~85-90% accurate (some features may be missed/misclassified)
- Sentiment analysis confidence varies