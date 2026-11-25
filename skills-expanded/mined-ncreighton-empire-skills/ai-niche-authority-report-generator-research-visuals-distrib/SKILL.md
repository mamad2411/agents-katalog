---
name: ai-niche-authority-report-generator-research-visuals-distribution
description: "Generate comprehensive niche authority reports with AI research synthesis, branded infographics, and multi-channel promotional assets. Use when the user needs thought leadership content, client deliverables, or market trend reports with professional visuals and distribution templates."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["OPENAI_API_KEY", "GOOGLE_SEARCH_API_KEY", "SERPER_API_KEY"],
        "bins": ["python3", "node"]
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "📊"
    }
  }
---

## Overview

The **AI Niche Authority Report Generator** is an enterprise-grade skill that transforms niche research into polished, branded authority reports complete with data visualizations, infographics, and ready-to-distribute promotional assets. Perfect for agencies, consultants, and thought leaders who need to establish credibility in specific markets.

This skill automates the entire authority-building workflow:
- **Research Phase**: Conducts AI-powered trend analysis across 50+ sources (Google Search, Serper, industry databases)
- **Synthesis Phase**: Generates executive summaries, key findings, and data-backed insights
- **Visual Phase**: Creates branded charts, infographics, and data visualizations
- **Distribution Phase**: Produces multi-format assets (LinkedIn carousels, email sequences, press releases, Twitter threads)

**Why This Matters**: Building authority manually takes 40-60 hours per report. This skill reduces that to 2-3 hours of strategic oversight, enabling agencies to white-label reports as premium client deliverables or establish personal thought leadership at scale.

**Integrations**: Seamlessly works with WordPress (automated publishing), Slack (team notifications), Google Sheets (data export), Canva API (design templates), and HubSpot (email distribution).

---

## Quick Start

### Example 1: Generate a B2B SaaS Market Trend Report

```
Generate an AI Niche Authority Report on "B2B SaaS pricing trends in 2024"

Research scope: Top 50 sources (G2, Capterra, industry blogs, analyst reports)
Target audience: SaaS founders and CTOs
Report length: 8,000 words
Include: 
  - Market size and growth projections
  - Top 5 emerging pricing models
  - Competitor analysis (Stripe, Chargebee, Recurly)
  - Customer sentiment analysis
  - Recommendations for new entrants

Visuals needed:
  - Line chart: Market growth 2020-2024
  - Comparison matrix: Pricing models
  - Heatmap: Feature adoption rates
  - Infographic: 5 key takeaways

Distribution assets:
  - LinkedIn carousel (5 slides)
  - Email sequence (3-part nurture)
  - Press release template
  - Twitter thread (15 tweets)
```

### Example 2: Local Service Industry Deep Dive

```
Create an authority report: "The future of home services: AI adoption, pricing, and customer expectations"

Research parameters:
  - Geographic focus: United States
  - Industries: Plumbing, HVAC, electrical, cleaning
  - Data sources: HomeAdvisor, Angie's List, industry surveys
  - Competitor analysis: TaskRabbit, Handy, local players
  - Timeline: Last 24 months of trends

Report sections:
  - Executive summary
  - Market opportunity analysis
  - Customer journey mapping
  - Technology adoption barriers
  - Pricing psychology insights
  - 10 actionable recommendations

Visual requirements:
  - Customer acquisition cost trends
  - Service category breakdown (pie chart)
  - Seasonal demand patterns
  - Technology stack comparison

Social media assets:
  - Instagram carousel (8 slides)
  - LinkedIn article format
  - Email newsletter (2,000 words)
  - TikTok script (60-second hook)
```

### Example 3: Vertical-Specific Authority Report (E-Commerce)

```
Generate report: "Conversion rate optimization benchmarks for D2C fashion brands in 2024"

Research depth: Comprehensive (100+ sources)
Data points to include:
  - Average conversion rates by traffic source
  - Cart abandonment analysis
  - Customer acquisition cost trends
  - Retention rate benchmarks
  - Product page optimization metrics
  - Checkout flow analysis

Competitive analysis: Everlane, Warby Parker, Allbirds, Glossier

Deliverables:
  - 10,000-word research report
  - 15 custom data visualizations
  - 3 branded infographics
  - Email launch sequence (5 emails)
  - LinkedIn thought leadership post
  - Press release for industry publications
  - Webinar slide deck (30 slides)
  - PDF report with branded templates
```

---

## Capabilities

### 1. **AI-Powered Research & Synthesis**
- Aggregates data from 50+ sources (Google Search API, Serper, industry databases, academic papers)
- Uses GPT-4 to synthesize raw data into coherent insights
- Automatically identifies contradictions and validates claims
- Generates confidence scores for each finding
- Creates executive summaries and key takeaways
- Produces data-backed recommendations

**Usage Example:**
```
research_config = {
  "topic": "AI in healthcare diagnostics",
  "depth": "comprehensive",
  "sources": ["academic", "industry_reports", "news", "competitor_analysis"],
  "data_validation": true,
  "confidence_threshold": 0.85
}
```

### 2. **Data Visualization & Infographics**
- Generates branded charts (line, bar, pie, scatter, heatmaps)
- Creates custom infographics with your brand colors
- Produces comparison matrices and frameworks
- Builds interactive dashboards (HTML/React)
- Supports SVG export for print and web
- Automatically selects optimal chart types for data

**Output Formats**: PNG (high-res), SVG (scalable), PDF (print), HTML (interactive)

### 3. **Multi-Format Asset Generation**
- **LinkedIn Carousels**: 5-10 slide decks optimized for engagement
- **Email Sequences**: 3-7 part nurture campaigns with copy and CTA optimization
- **Press Releases**: AP-style formatted, ready for distribution
- **Twitter Threads**: 10-20 tweet sequences with hooks and call-to-actions
- **Blog Posts**: SEO-optimized articles (2,000-5,000 words)
- **Webinar Scripts**: Slide decks with speaker notes
- **PDF Reports**: Branded templates with your logo, colors, and fonts

### 4. **Brand Customization**
- Logo integration (PNG, SVG)
- Custom color palettes (HEX, RGB)
- Font selection (Google Fonts, custom uploads)
- Branded header/footer templates
- Watermark options
- Custom domain branding

### 5. **Competitive Intelligence**
- Identifies 10-20 key competitors in your niche
- Analyzes their positioning, messaging, and pricing
- Extracts differentiation opportunities
- Benchmarks your authority against competitors
- Suggests competitive advantages

### 6. **Distribution & Publishing**
- WordPress integration (auto-publish blog posts)
- Slack notifications (team updates, approval workflows)
- Google Sheets export (data for further analysis)
- HubSpot CRM integration (contact enrichment)
- Zapier/Make support (workflow automation)
- Email list management (direct SendGrid/Mailchimp integration)

---

## Configuration

### Required Environment Variables

```bash
# OpenAI API for content synthesis and analysis
export OPENAI_API_KEY="sk-..."

# Google Search API for research
export GOOGLE_SEARCH_API_KEY="AIzaSy..."

# Serper API for enhanced search results
export SERPER_API_KEY="..."

# Optional: For publishing and distribution
export WORDPRESS_API_KEY="..."
export HUBSPOT_API_KEY="..."
export SLACK_WEBHOOK_URL="https://hooks.slack.com/..."
```

### Configuration File (config.json)

```json
{
  "report_settings": {
    "word_count": 8000,
    "sections": ["executive_summary", "market_analysis", "trends", "recommendations"],
    "research_depth": "comprehensive",
    "confidence_threshold": 0.85,
    "include_competitor_analysis": true
  },
  "brand_settings": {
    "logo_url": "https://yourcompany.com/logo.png",
    "primary_color": "#0066CC",
    "secondary_color": "#00D9FF",
    "font_family": "Inter",
    "company_name": "Your Company"
  },
  "distribution": {
    "linkedin": true,
    "email": true,
    "twitter": true,
    "wordpress": false,
    "pdf": true
  },
  "research_sources": {
    "google_search": true,
    "serper": true,
    "industry_databases": true,
    "competitor_sites": true,
    "academic_papers": false
  }
}
```

### Setup Instructions

1. **Install dependencies**:
   ```bash
   pip install openai google-search-api serper requests pillow matplotlib
   npm install axios chart.js canva-api
   ```

2. **Authenticate APIs**:
   - OpenAI: Get API key from platform.openai.com
   - Google Search: Create project in Google Cloud Console
   - Serper: Sign up at serper.dev (recommended for better results)

3. **Configure branding**:
   - Upload logo (PNG/SVG recommended)
   - Define color palette in config.json
   - Set company name and domain

4. **Test the skill**:
   ```bash
   claw skill test ai-niche-authority-report-generator
   ```

---

## Example Outputs

### 1. Research Report Structure

```
# AI in Healthcare Diagnostics: Market Trends & Opportunities (2024)

## Executive Summary
- Market size: $XX billion (projected growth: XX% CAGR)
- Key trend: AI-assisted diagnosis adoption increasing 45% YoY
- Opportunity: Regulatory clarity enabling faster market entry
- Recommendation: Focus on FDA-cleared pathways

## Market Analysis
- Total addressable market: $XX billion
- Current penetration: X%
- Growth drivers: Regulatory approval, reimbursement expansion, talent availability
- Barriers: Data privacy concerns, integration complexity, clinician adoption

## Top 5 Trends
1. Federated Learning for Privacy-Preserving Models
2. Multimodal AI (combining imaging, text, genomics)
3. Real-Time Clinical Decision Support
4. Regulatory Harmonization (FDA, CE, PMDA alignment)
5. Enterprise Integration Platforms

## Competitive Landscape
[Detailed analysis of 15 key players with positioning matrix]

## Recommendations
1. Invest in regulatory expertise early
2. Partner with healthcare systems for validation
3. Build for interoperability (HL7, FHIR standards)
4. Develop clear ROI metrics for hospital buyers
5. Create customer success programs for retention
```

### 2. LinkedIn Carousel (5 Slides)

```
Slide 1: Hook
"We analyzed 200+ AI healthcare companies. Here's what separates winners from the rest 👇"

Slide 2: Stat
"45% YoY growth in AI diagnostic adoption
But only 15% of implementations hit ROI targets"

Slide 3: Key Finding
"The difference? Clinical integration strategy
Winners spent 6 months on workflow design before launch"

Slide 4: Recommendation
"Your playbook:
1. Map existing workflows
2. Identify friction points
3. Design AI touchpoints
4. Pilot with power users
5. Scale with support"

Slide 5: CTA
"Download our full 40-page AI in Healthcare report
[Link to PDF]"
```

### 3. Email Sequence (3-Part)

```
Email 1: Hook (Subject: "The 45% AI adoption statistic nobody talks about")
Body: Teaser of key finding, social proof, soft CTA

Email 2: Value (Subject: "Why 85% of AI healthcare projects fail (and how to avoid it)")
Body: Deep dive into one key insight, case study, medium CTA

Email 3: Conversion (Subject: "Get the complete AI healthcare authority report")
Body: Full benefits, testimonials, strong CTA with download link
```

### 4. Visual Assets

- **Line Chart**: Market size projections (2020-2026)
- **Comparison Matrix**: 15 competitors across 8 dimensions
- **Heatmap**: Technology adoption by hospital size/geography
- **Infographic**: "5 Keys to AI Healthcare Success" (vertical scroll)
- **Pie Chart**: Market segment breakdown (diagnostic imaging, pathology, etc.)

---

## Tips & Best Practices

### 1. **Research Strategy**
- **Narrow your niche**: Broader topics = less differentiated insights. Focus on specific use cases, industries, or geographies.
- **Validate contradictions**: When sources disagree, the skill flags these. Use them as research opportunities, not problems.
- **Include primary research**: If possible, add customer interviews or survey data. The skill will weight primary sources higher.
- **Update quarterly**: Authority compounds. Generate updated reports every 90 days to stay ahead of trends.

### 2. **Visual Design**
- **Limit color palette**: Use 2-3 colors max. More looks amateur. The skill defaults to this, but override if needed.
- **Label everything**: Charts without clear labels confuse readers. The skill auto-labels, but review for clarity.
- **Use consistent fonts**: Pick 1-2 fonts for the entire report. Mix-and-match looks unprofessional.
- **Export high-res**: Always export as PNG (300 DPI) for print, SVG for web. Never use JPEG for charts.

### 3. **Distribution Timing**
- **Release on Tuesday-Thursday**: Research shows 40% higher engagement mid-week vs. weekends.
- **Stagger assets**: Release LinkedIn carousel Day 1, email sequence Day 3-5, press release Day 7.
- **Repurpose heavily**: One report = 20+ pieces of content (tweets, LinkedIn posts, email, blog, webinar, podcast topics).
- **Track metrics**: Monitor engagement by format. Double down on what works.

### 4. **Authority Building**
- **Add personality**: Data is boring. Add your perspective, contrarian takes, and recommendations.
- **Include case studies**: Real examples beat generic insights. The skill extracts these automatically.
- **Make it actionable**: End with 5-10 specific recommendations readers can implement immediately.
- **Build on previous reports**: Reference your past research to show consistency and depth.

### 5. **Client Deliverables**
- **White-label completely**: Remove all skill branding. Use client logos, colors, and domain.
- **Add client testimonials**: If this is for a client, include quotes from their customers in the report.
- **Create executive summary**: Busy executives won't read 8,000 words. Provide a 2-page summary.
- **Build interactive version**: Export as HTML dashboard for client presentations.

---

## Safety & Guardrails

### What This Skill Will NOT Do

**❌ Make medical claims**: This skill synthesizes healthcare research but will NOT claim to provide medical advice. All health-related reports include disclaimers.

**❌ Guarantee accuracy**: The skill validates sources and flags low-confidence findings, but research is inherently uncertain. Always include methodology and confidence scores.

**❌ Plagiarize content**: The skill synthesizes and paraphrases. It does NOT copy-paste from sources. All content is original, with proper citations.

**❌ Create misleading visuals**: Charts are designed to accurately represent data. The skill will refuse to create misleading visualizations (e.g., truncated Y-axes, cherry-picked date ranges).

**❌ Ignore regulatory requirements**: For regulated industries (healthcare, finance, legal), the skill flags compliance considerations and recommends legal review.

**❌ Generate fake data**: If sources are insufficient, the skill will tell you. It will NOT invent statistics or trends.

### Limitations & Boundaries

- **Language**: Currently supports English only (Spanish, French coming Q2 2024)
- **Real-time data**: Research cutoff is 6 months. Very recent trends may be incomplete.
- **Proprietary data**: Cannot access private databases or paywalled content. Serper API has rate limits (500 requests/day on free tier).
- **Visual complexity**: Interactive dashboards work best with <50 data points. Large datasets may require simplification.
- **Distribution**: Email integrations require valid SMTP credentials. WordPress requires API access.

### Recommended Practices

1. **Always include disclaimers**: "This report synthesizes