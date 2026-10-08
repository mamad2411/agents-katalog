---
name: amazon-product-research-skill
description: >-
  Amazon Best Sellers category analysis for e-commerce product research and
  selection decisions. Activates when users analyze Amazon categories, find
  black horse products, research competitors, or evaluate market entry
  opportunities. Triggers on phrases like analyze Amazon category, find
  high-potential products, Amazon Best Sellers research, product selection
  analysis, competitor analysis, market opportunity scan. Supports macro
  category analysis (price tiers, brand concentration, monopoly risk),
  micro product analysis (potential score calculation), AI-powered product
  labeling (category type, form factor, material, key tags), and strategic
  opportunity recommendations. Uses Apify actors for data collection and
  AI models for intelligent analysis. Calculates potential score using
  (sales / (reviews + 1)) * (365 / (days_online + 1)) formula to identify
  high-growth, low-competition products.
license: MIT
metadata:
  author: Agent Skill Creator
  version: 1.0.0
  created: 2026-03-12
  last_reviewed: 2026-03-12
  review_interval_days: 90
  dependencies:
    - url: https://apify.com/junglee/amazon-bestsellers
      name: Apify Amazon Bestsellers Scraper
      type: api
    - url: https://apify.com/axesso_data/amazon-product-details-scraper
      name: Apify Amazon Product Details Scraper
      type: api
    - url: https://platform.openai.com
      name: OpenAI API (for AI analysis)
      type: api
---

# /amazon-product-research — Amazon Best Sellers Analysis

You are an expert e-commerce product research analyst specializing in Amazon
marketplace analysis. Your job is to help sellers make data-driven product
selection decisions by analyzing Amazon Best Sellers categories.

## Trigger

User invokes `/amazon-product-research` followed by their input:

```
/amazon-product-research Analyze https://www.amazon.com/Best-Sellers-Portable-Changing-Pads
/amazon-product-research Find black horse products in electronics category
/amazon-product-research Research competitor strategy for ASIN B09B8V1LZ3
/amazon-product-research Generate market entry report for baby products
/amazon-product-research Weekly scan of kitchen gadgets category
```

## When to Use This Skill

- **Category Analysis**: Evaluate an entire Amazon Best Sellers category for
  market entry decisions
- **Black Horse Discovery**: Find high-potential, low-competition products
- **Competitor Research**: Analyze competitor product strategies and positioning
- **Investment Decisions**: Get AI-powered strategic recommendations
- **Weekly Monitoring**: Track category changes and emerging products

## Data Sources

This skill uses Apify Actors for data collection:

1. **junglee/amazon-bestsellers**: Scrapes Best Seller rankings (ASINs, rankings,
   basic info) from category pages
2. **axesso_data/amazon-product-details-scraper**: Scrapes detailed product
   information for each ASIN (price, reviews, ratings, features, seller info)

**Prerequisites**:
- Apify API token (get free tier at https://apify.com)
- OpenAI API key for AI analysis (optional, for enhanced recommendations)

## Workflows

### Workflow 1: Complete Category Analysis

Analyze an entire Amazon Best Sellers category end-to-end:

```bash
# Set environment variables
export APIFY_API_TOKEN="your_apify_token"
export OPENAI_API_KEY="your_openai_key"  # Optional

# Run complete analysis
python3 scripts/analyze_category.py \
  --category-url "https://www.amazon.com/Best-Sellers-Portable-Changing-Pads" \
  --output-format markdown \
  --include-ai-analysis
```

**What it does**:
1. Scrapes Best Sellers list (up to 100 products)
2. Collects detailed product information
3. Performs macro analysis (price tiers, brand share, monopoly risk)
4. Calculates potential scores for each product
5. Identifies black horse candidates
6. Generates comprehensive report

### Workflow 2: Black Horse Discovery

Find high-potential products with low competition:

```bash
python3 scripts/find_black_horses.py \
  --category-url "https://www.amazon.com/Best-Sellers-Electronics/zgbs/electronics" \
  --min-potential-score 1.0 \
  --max-reviews 100 \
  --output black_horses.json
```

**Black Horse Criteria** (configurable):
- Potential Score >= 1.0
- Reviews <= 100
- Days online < 180 (new products)

### Workflow 3: AI-Powered Opportunity Analysis

Get strategic recommendations from AI:

```bash
python3 scripts/ai_opportunity_analysis.py \
  --input-file category_data.json \
  --analysis-type comprehensive \
  --output report.md
```

**Analysis Types**:
- `label-extraction`: Extract category_type, form_factor, material_core, key_tags
- `basic-analysis`: Category macro report + product audit by tags
- `opportunity-analysis`: Strategic recommendations with investment advice
- `comprehensive`: All analyses combined

### Workflow 4: Quick Category Scan

Fast overview without detailed scraping:

```bash
python3 scripts/quick_scan.py \
  --category-url "https://www.amazon.com/Best-Sellers-Cell-Phones/zgbs/wireless" \
  --limit 50
```

## Available Scripts

| Script | Purpose | Inputs | Outputs |
|--------|---------|--------|---------|
| `analyze_category.py` | Complete end-to-end analysis | Category URL | Full report (JSON/Markdown) |
| `find_black_horses.py` | Find high-potential products | Category URL | Black horse list |
| `ai_opportunity_analysis.py` | AI-powered recommendations | Product data | Strategic report |
| `quick_scan.py` | Fast category overview | Category URL | Summary stats |
| `fetch_bestsellers.py` | Raw data collection | Category URL | Raw JSON data |
| `calculate_metrics.py` | Metric calculations | Product data | Scored products |

## Available Analyses

### Macro Analysis (Category Overview)

**Metrics Calculated**:
- **Price Tiers**: Average prices for Top 20, 21-50, 51-100 rankings
- **Brand Analysis**: Brand occurrence counts, market share calculations
- **Seller Structure**: Amazon Direct vs FBA vs FBM distribution
- **Monopoly Risk**: Top 5 brand concentration percentage (CR5)
- **Amazon Competition**: Amazon Direct products percentage

**Interpretation**:
- Monopoly Risk > 60%: HIGH - Difficult for new entrants
- Monopoly Risk 40-60%: MODERATE - Possible with differentiation
- Monopoly Risk < 40%: LOW - Favorable for new entrants
- Amazon Direct > 20%: SEVERE competition from Amazon

### Micro Analysis (Product-Level)

**Potential Score Formula**:
```
Potential Score = (monthly_sales / (review_count + 1)) * (365 / (days_online + 1))
```

**Logic**:
- Higher sales = higher score (market demand)
- Lower reviews = higher score (less competition)
- Fewer days online = higher score (new product opportunity)

**Black Horse Thresholds**:
- Potential Score >= 1.0
- Reviews <= 100
- Days online < 180

### AI Label Extraction

Extracts standardized product attributes:
- **category_type**: Product type (e.g., "Diaper Pad", "Earbuds")
- **form_factor**: Physical structure (e.g., "Foldable Mat", "Cylindrical Box")
- **material_core**: Main material (e.g., "PU Leather", "Silicone")
- **key_tags**: 3 core selling points (e.g., ["Waterproof", "Wireless", "Non-slip"])

### AI Opportunity Analysis

Strategic recommendations including:
- **Premium Ceiling Analysis**: What drives higher pricing
- **Winning DNA Formula**: Recommended product characteristics
- **Giant Blind Spots**: Opportunities big brands miss
- **Investment Recommendation**: Price range and competitive advantage strategy

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `ApifyAuthError` | Invalid API token | Check APIFY_API_TOKEN env var |
| `RateLimitError` | Too many requests | Wait and retry; check Apify dashboard |
| `NoProductsError` | Empty category or blocking | Try different category or proxy |
| `AIAnalysisError` | OpenAI API failure | Check OPENAI_API_KEY; retry without AI |
| `DataValidationError` | Missing required fields | Check input data format |

## Keywords for Automatic Detection

**Entities**: Amazon, Best Sellers, ASIN, category, product, brand, seller, FBA, FBM

**Metrics**: potential score, monopoly risk, market share, price tier, BSR (Best Seller Rank), reviews, rating, sales volume

**Actions**: analyze, research, scan, discover, find, compare, evaluate, monitor

**Geography**: amazon.com, amazon.co.uk, amazon.de, amazon.co.jp, amazon.ca

**Activation examples**:
- "Analyze this Amazon category for me"
- "Find black horse products in electronics"
- "Research Amazon Best Sellers for baby products"
- "What's the monopoly risk in this category?"
- "Generate a product selection report"

**Does NOT activate for**:
- General e-commerce questions (not Amazon-specific)
- Product listing optimization
- Amazon advertising analysis
- Inventory management

## Usage Examples

### Example 1: Category Entry Decision

**User**: "Should I enter the portable changing pads market?"

**Flow**:
1. Skill scrapes https://www.amazon.com/Best-Sellers-Portable-Changing-Pads
2. Calculates monopoly risk (e.g., 45% - MODERATE)
3. Identifies 5 black horse candidates
4. AI recommends: "Enter at $25-35 price point with waterproof silicone material"

**Output**: Comprehensive report with go/no-go recommendation

### Example 2: Black Horse Discovery

**User**: "Find me high-potential products with low competition"

**Flow**:
1. User provides category URL
2. Skill calculates potential scores for all products
3. Filters for score >= 1.0 and reviews <= 100
4. Returns ranked list with ASINs and analysis

**Output**: JSON/Markdown list of black horse products

### Example 3: Competitor Analysis

**User**: "Analyze the top 10 products in this category"

**Flow**:
1. Scrapes top 10 Best Sellers
2. Extracts brand distribution
3. Analyzes price positioning
4. Identifies feature gaps

**Output**: Competitor positioning map

### Example 4: Weekly Monitoring

**User**: "Weekly scan of kitchen gadgets category"

**Flow**:
1. Scheduled execution (via cron or similar)
2. Compares with previous week's data
3. Identifies new entrants and ranking changes
4. Sends alert if new black horses appear

**Output**: Change report with new opportunities

## References

| File | Content |
|------|---------|
| `references/api-guide.md` | Apify API setup, authentication, rate limits |
| `references/analysis-methods.md` | Detailed formulas and methodologies |
| `references/troubleshooting.md` | Common issues and solutions |
| `assets/config.json` | Default configuration and thresholds |

## Configuration

Edit `assets/config.json` to customize:

- **Scraping limits**: max products per category
- **Black horse thresholds**: potential score, review count
- **AI models**: which model to use for analysis
- **Output formats**: default report format
- **Rate limiting**: request delays and concurrency
