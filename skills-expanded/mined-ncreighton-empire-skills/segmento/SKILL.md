---
name: segmento
description: "Segment customers into AI-powered clusters using behavioral, demographic, and transactional data. Use when the user needs customer segmentation, audience targeting, or CRM list organization for marketing automation."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["SEGMENTO_API_KEY", "CRM_INTEGRATION_TOKEN"],
        "bins": []
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "🎯"
    }
  }
---

# Segmento: AI-Powered Customer Segmentation

## Overview

Segmento is an enterprise-grade customer segmentation skill that uses machine learning clustering algorithms to automatically group customers into meaningful, actionable segments. Instead of manually creating customer lists or relying on basic RFM analysis, Segmento analyzes behavioral patterns, purchase history, engagement metrics, and demographic data to discover hidden customer cohorts—then automatically syncs those segments to your CRM, email platform, or marketing automation tool.

**Why This Matters:**
- **Precision Targeting**: Move beyond broad demographics to behavior-driven segments
- **Marketing ROI**: Personalized campaigns to the right audience increase conversion by 20-40%
- **Churn Prevention**: Identify at-risk customers before they leave
- **Revenue Growth**: Upsell and cross-sell to high-value segments with proven propensity
- **Time Savings**: Automation replaces hours of manual list-building

**Integrations Supported:**
- HubSpot, Salesforce, Pipedrive (CRM sync)
- Mailchimp, ConvertKit, ActiveCampaign (email list push)
- Slack (segment notifications)
- Google Sheets (data export)
- Zapier webhooks (custom workflows)

---

## Quick Start

Try these prompts immediately:

### Example 1: Behavioral Segmentation
```
Segment my customer base by purchase frequency and recency. 
I have 5,000 customers with transaction history from the past 24 months.
Create segments for: high-value repeat buyers, dormant customers, and new customers.
Export to HubSpot as contact lists.
```

### Example 2: Churn Risk Detection
```
Analyze my customer engagement data and identify customers at risk of churning.
Use metrics: login frequency, feature usage, support tickets, last purchase date.
Flag customers with declining engagement in the last 90 days.
Create a "Save Me" segment for re-engagement campaigns.
```

### Example 3: Product Affinity Clustering
```
Group customers by product purchase patterns.
I sell: SaaS plans (Starter, Pro, Enterprise), add-ons, and professional services.
Create segments showing: plan tier affinity, add-on propensity, and upsell opportunities.
Suggest personalized product recommendations per segment.
```

### Example 4: Demographic + Behavioral Blend
```
Segment my e-commerce customers by location, purchase value, and category preferences.
I have customer data: geography, order history, browse behavior, email engagement.
Create 6-8 segments optimized for targeted email campaigns.
Include segment size, average LTV, and recommended offer per segment.
```

---

## Capabilities

### 1. **Intelligent Clustering**
Segmento uses k-means, hierarchical clustering, and DBSCAN algorithms to discover natural customer groupings:
- **Behavioral Clustering**: Purchase frequency, order value, category preferences, browsing patterns
- **Engagement Clustering**: Email opens, click-through rates, content consumption, feature usage
- **Demographic Clustering**: Location, company size, industry, customer lifecycle stage
- **RFM Analysis**: Recency, Frequency, Monetary value (classic + advanced variants)
- **Churn Prediction**: Identifies flight-risk customers with 85%+ accuracy

**Usage Example:**
```
Analyze my Shopify customer base and create 5 distinct segments.
Data sources: order history, customer lifetime value, product category affinity, email engagement.
Optimize for: marketing campaign personalization and retention strategy.
Output: Segment profiles with size, characteristics, and recommended actions.
```

### 2. **Customizable Segmentation Rules**
Define your own segmentation logic without coding:
- **Rule Builder**: Combine conditions (AND/OR logic) for manual segment creation
- **Weighted Scoring**: Assign importance to different attributes
- **Time-Based Rules**: Segment by recency windows (last 30/60/90 days)
- **Dynamic Thresholds**: Auto-adjust segment boundaries based on data distribution

**Usage Example:**
```
Create a "VIP" segment with custom rules:
- Customers with lifetime value > $5,000 AND
- Purchase frequency >= 10 orders AND
- Email engagement rate > 30% OR
- Product category = "Premium Plan"
Exclude: customers with active refund requests or support complaints.
```

### 3. **CRM & Marketing Platform Integration**
Automatically sync segments to your existing tools:
- **HubSpot**: Create/update contact lists and custom properties
- **Salesforce**: Push segments as Salesforce lists and account hierarchies
- **Pipedrive**: Sync to deal pipelines and organization segments
- **Mailchimp**: Create audience segments for targeted campaigns
- **ConvertKit**: Tag subscribers by segment for automation
- **ActiveCampaign**: Update contact records and trigger automations
- **Google Sheets**: Export segment data for analysis and reporting

**Usage Example:**
```
Push my 4 customer segments to HubSpot.
Segment 1 (High-Value): Create list "VIP Customers", set property "customer_tier=premium"
Segment 2 (At-Risk): Create list "Churn Risk", trigger HubSpot workflow "win-back campaign"
Segment 3 (New): Create list "New Customers", add to onboarding email sequence
Segment 4 (Dormant): Create list "Reactivation", tag with "dormant_90days"
```

### 4. **Advanced Analytics & Insights**
Get actionable intelligence from your segments:
- **Segment Profiles**: Size, growth rate, average metrics, composition
- **Cohort Analysis**: Track segment behavior over time
- **Predictive Scoring**: Next purchase likelihood, churn probability, LTV prediction
- **Comparison Reports**: Benchmark segments against each other
- **Visualization**: Charts, heatmaps, and trend analysis

**Usage Example:**
```
Generate a segment comparison report.
Show: size, average order value, purchase frequency, churn rate, email engagement for each segment.
Highlight: which segments are growing/shrinking, which are most profitable.
Recommend: top 3 actions per segment to increase revenue.
```

### 5. **Workflow Automation**
Set up recurring segmentation jobs:
- **Scheduled Runs**: Daily, weekly, or monthly re-segmentation
- **Trigger-Based**: Re-segment when new data arrives or thresholds are crossed
- **Change Notifications**: Slack alerts when customers move between segments
- **Audit Trail**: Track all segment changes and data lineage

**Usage Example:**
```
Set up automated weekly segmentation.
Data source: Shopify API (pull orders, customers, products)
Segmentation: RFM analysis + churn risk scoring
Sync: Push updated segments to HubSpot and Mailchimp every Monday at 9 AM
Notify: Send Slack summary to #marketing with segment changes and key metrics.
```

---

## Configuration

### Required Environment Variables
```bash
# Segmento API credentials
SEGMENTO_API_KEY=sk_live_xxxxxxxxxxxxx

# CRM integration (choose at least one)
HUBSPOT_API_KEY=pat-xxxxxxxxxxxxx
SALESFORCE_API_KEY=xxxxxxxxxxxxx
PIPEDRIVE_API_TOKEN=xxxxxxxxxxxxx

# Email platform (optional)
MAILCHIMP_API_KEY=xxxxxxxxxxxxx
CONVERTKIT_API_KEY=xxxxxxxxxxxxx

# Data source credentials (optional)
SHOPIFY_ACCESS_TOKEN=shpat_xxxxxxxxxxxxx
STRIPE_API_KEY=sk_live_xxxxxxxxxxxxx
GOOGLE_SHEETS_CREDENTIALS={"type":"service_account",...}
```

### Configuration Options
```yaml
segmentation:
  algorithm: "kmeans"  # Options: kmeans, hierarchical, dbscan, gaussian_mixture
  num_clusters: 5      # Auto-detect if null
  features:
    - purchase_frequency
    - order_value
    - category_affinity
    - email_engagement
    - churn_risk_score
  
  scaling: "standard"  # Options: standard, minmax, robust
  random_state: 42     # For reproducibility

sync:
  crm: "hubspot"       # Options: hubspot, salesforce, pipedrive, none
  email_platform: "mailchimp"
  sync_frequency: "weekly"  # Options: daily, weekly, monthly, manual
  
analytics:
  enable_cohort_analysis: true
  enable_predictive_scoring: true
  retention_days: 90
```

### Setup Instructions

1. **Obtain API Keys**
   - Segmento: Visit [segmento.app/api](https://segmento.app/api) and create an API key
   - HubSpot: Settings > Integrations > Private apps
   - Shopify: Admin > Apps > App and sales channel settings > Develop apps
   - Stripe: Dashboard > Developers > API keys

2. **Set Environment Variables**
   ```bash
   export SEGMENTO_API_KEY="sk_live_..."
   export HUBSPOT_API_KEY="pat-..."
   ```

3. **Connect Data Sources**
   - Upload customer CSV, or
   - Connect CRM/e-commerce platform via OAuth, or
   - Use webhook to stream real-time customer events

4. **Define Segmentation Strategy**
   - Choose algorithm (k-means recommended for most use cases)
   - Select features/attributes to include
   - Set number of segments (5-8 is typical)

5. **Test & Deploy**
   - Run segmentation on sample data
   - Review segment profiles and quality
   - Sync to CRM and test workflows
   - Schedule recurring jobs

---

## Example Outputs

### Segment Profile Report
```
SEGMENT: High-Value Repeat Buyers
├─ Size: 342 customers (6.8% of base)
├─ Growth: +12% month-over-month
├─ Avg Customer LTV: $8,450
├─ Avg Order Value: $245
├─ Purchase Frequency: 18.3 orders/year
├─ Email Engagement: 45% open rate, 8.2% CTR
├─ Churn Risk: 2% (very low)
├─ Top Product Categories: Premium Plans (78%), Add-ons (65%)
└─ Recommended Actions:
   ├─ VIP loyalty program enrollment
   ├─ Early access to new features
   ├─ Quarterly business reviews
   └─ Upsell: Enterprise tier (30% conversion potential)

SEGMENT: At-Risk Churners
├─ Size: 156 customers (3.1% of base)
├─ Growth: -8% month-over-month
├─ Avg Customer LTV: $1,200
├─ Days Since Last Purchase: 127 days
├─ Email Engagement: 12% open rate, 1.1% CTR
├─ Feature Usage: Declined 60% in last 30 days
├─ Churn Risk: 78% (critical)
└─ Recommended Actions:
   ├─ Trigger win-back email sequence
   ├─ Offer: 30% discount on renewal
   ├─ Sales outreach: Personal call from CSM
   └─ Feedback survey: Understand pain points

SEGMENT: New Customers
├─ Size: 890 customers (17.7% of base)
├─ Growth: +25% month-over-month
├─ Avg Customer LTV (projected): $2,100
├─ Days as Customer: 18 days average
├─ Email Engagement: 52% open rate, 9.5% CTR
├─ Product Adoption: 65% activated core features
├─ Churn Risk: 22% (moderate)
└─ Recommended Actions:
   ├─ Onboarding email sequence (3-email series)
   ├─ Product tutorial and best practices
   ├─ Offer: Early-bird discount on upgrade
   └─ Track: Feature adoption and support tickets
```

### Segment Comparison Matrix
```
Metric                High-Value    At-Risk    New        Dormant
─────────────────────────────────────────────────────────────────
Segment Size          342           156        890        1,240
% of Base             6.8%          3.1%       17.7%      24.6%
Avg LTV               $8,450        $1,200     $2,100     $450
Avg Order Value       $245          $89        $120       $65
Purchase Freq/Yr      18.3          2.1        4.2        0.3
Email Open Rate       45%           12%        52%        8%
Churn Risk %          2%            78%        22%        65%
Growth Rate           +12%          -8%        +25%       -15%
```

### Integration Output (HubSpot Sync)
```
✅ Synced 4 segments to HubSpot
├─ List: "VIP Customers" (342 contacts)
│  └─ Property: customer_segment = "high_value"
│  └─ Property: ltv_tier = "premium"
│  └─ Workflow: "VIP Engagement" triggered
├─ List: "Churn Risk" (156 contacts)
│  └─ Property: customer_segment = "at_risk"
│  └─ Property: churn_probability = 0.78
│  └─ Workflow: "Win Back Campaign" triggered
├─ List: "New Customers" (890 contacts)
│  └─ Property: customer_segment = "new"
│  └─ Property: onboarding_stage = "day_1"
│  └─ Workflow: "Onboarding Series" triggered
└─ List: "Dormant Customers" (1,240 contacts)
   └─ Property: customer_segment = "dormant"
   └─ Property: days_inactive = 180+
   └─ Workflow: "Reactivation Campaign" triggered

Sync completed: 2,628 contacts updated in 4.2 seconds
```

---

## Tips & Best Practices

### 1. **Choose the Right Algorithm**
- **K-means**: Best for balanced, spherical clusters (most common use case)
- **Hierarchical**: Best when you want to understand cluster relationships and dendrograms
- **DBSCAN**: Best when clusters are irregular or you have outliers to isolate
- **Gaussian Mixture**: Best for probabilistic assignments and soft boundaries

**Recommendation**: Start with k-means for 80% of use cases.

### 2. **Feature Selection is Critical**
- **Include**: Purchase frequency, order value, category affinity, engagement, recency
- **Exclude**: Customer name, email (PII), random identifiers
- **Weight**: Give higher importance to revenue-driving metrics
- **Normalize**: Ensure all features are on comparable scales

**Example:**
```
Features (with weights):
- purchase_frequency: 1.0
- order_value: 1.5 (revenue-weighted)
- email_engagement: 0.8
- product_category_diversity: 0.6
- churn_risk_score: 1.2 (retention-critical)
```

### 3. **Determine Optimal Cluster Count**
- **Elbow Method**: Run k=2 to k=10, plot inertia, find the "elbow"
- **Silhouette Score**: Higher is better (range: -1 to 1, aim for 0.5+)
- **Business Logic**: 5-8 segments is typical for mid-market, 10-15 for enterprise
- **Actionability**: Can you create distinct marketing/sales strategies for each?

**Rule of Thumb**: `num_clusters = sqrt(num_customers / 2)`

### 4. **Validate Segment Quality**
Before deploying to production:
- Review segment profiles manually
- Verify segments are distinct (not overlapping)
- Check for imbalanced clusters (one huge segment = bad)
- Get stakeholder feedback (marketing, sales, CS teams)
- A/B test personalized campaigns on segments

### 5. **Sync Strategy**
- **Daily Sync**: For high-velocity businesses (SaaS, e-commerce)
-