---
name: product-teardown-positioning-analyzer
description: "Analyze competitor product pages and pricing to identify positioning gaps and recommend 3-5 differentiation angles. Use when the user needs competitive intelligence, feature positioning strategy, or pricing benchmarking for market positioning."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["OPENAI_API_KEY", "GOOGLE_SEARCH_API_KEY"],
        "bins": []
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "🔍"
    }
  }
---

## Overview

The Product Teardown & Positioning Analyzer is a competitive intelligence skill that systematically deconstructs competitor product pages, pricing models, feature hierarchies, and messaging strategies to uncover market positioning gaps and opportunities.

**Why This Matters:**
Launching or repositioning a product without understanding competitor positioning is risky. This skill automates the competitive analysis that typically takes marketing teams 20+ hours to manually compile. It ingests competitor URLs, extracts positioning signals, benchmarks feature emphasis, analyzes pricing psychology, and generates actionable differentiation recommendations in minutes.

**Key Business Value:**
- **Faster GTM Strategy:** Reduce positioning research from weeks to hours
- **Data-Driven Positioning:** Base feature emphasis on competitor analysis, not hunches
- **Pricing Confidence:** Understand pricing ladders, anchor points, and psychological triggers
- **Team Alignment:** Generate consensus-building positioning statements and feature roadmap priorities
- **Integrations Ready:** Export findings to WordPress (product pages), Slack (team communication), Google Sheets (competitive matrices), and Notion (strategy docs)

---

## Quick Start

### Example 1: Analyze a Single Competitor
```
Analyze the product positioning of Intercom (https://www.intercom.com/product). 
I'm building a customer communication platform. Identify their top 5 positioning pillars, 
pricing structure, and 3 differentiation angles we could own.
```

### Example 2: Multi-Competitor Benchmarking
```
Compare positioning across these 4 customer service tools:
- Zendesk (https://www.zendesk.com/)
- Freshdesk (https://freshdesk.com/)
- Helpscout (https://www.helpscout.com/)
- Gorgias (https://www.gorgias.com/)

Create a feature matrix showing which competitor emphasizes what, then 
recommend 5 positioning gaps we could exploit for a new player.
```

### Example 3: Pricing Strategy Analysis
```
I'm repositioning our CRM. Analyze HubSpot, Pipedrive, and Close.io pricing pages.
Extract: tier names, price points, feature allocations per tier, psychological 
pricing tactics, and recommend our optimal pricing ladder and anchor strategy.
```

### Example 4: Full Competitive Teardown Report
```
Generate a complete competitive teardown for the email automation category:
- Analyze: Klaviyo, ConvertKit, Drip, and ActiveCampaign
- Output: positioning matrix, messaging themes, feature emphasis patterns, 
  pricing structure analysis, and 5 actionable differentiation recommendations
- Format as a Notion-ready markdown doc I can import directly
```

---

## Capabilities

### 1. **Automated Competitor URL Analysis**
Crawls product pages, extracts:
- Homepage headline and subheadline positioning
- Feature lists with hierarchy/emphasis signals (bold, placement, repetition)
- Use case framing (who is the target buyer)
- Pain point messaging alignment
- Call-to-action strategy and flow

**Usage:**
```
Crawl and analyze the positioning on [competitor URL]. 
Focus on: headline positioning, top 3 value props, target buyer signals, 
and primary vs. secondary feature emphasis.
```

### 2. **Pricing Structure Deconstruction**
Identifies and models:
- Tier names and psychological framing (Starter vs. Growth vs. Enterprise)
- Feature allocation patterns (what moves between tiers)
- Price anchors and psychological pricing tactics (e.g., $0.99 vs. $1.00)
- Usage-based vs. seat-based vs. flat-rate pricing models
- Free trial/freemium strategy signals
- Annual discount psychology

**Usage:**
```
Extract the full pricing model from [URL]. Model the feature ladder, 
identify the assumed buyer persona for each tier, and flag any price 
anchoring or scarcity tactics used.
```

### 3. **Feature Hierarchy & Emphasis Mapping**
Quantifies:
- Which features are "hero" features (large images, prominent placement, repeated mentions)
- Feature-to-use-case mapping (which features support which buyer problems)
- Feature novelty signals (new/beta labels, highlight colors)
- Competitive feature clustering (what features are assumed table stakes vs. differentiators)

**Usage:**
```
Map the feature hierarchy for [competitor]. Identify which features 
are positioned as differentiators vs. table stakes. Show me how they 
emphasize features differently from [other competitor].
```

### 4. **Messaging & Positioning Analysis**
Extracts and analyzes:
- Core positioning statement (explicit or inferred)
- Primary value proposition hierarchy
- Emotional vs. rational messaging balance
- Target audience segmentation signals
- Competitor-specific language patterns
- Use case emphasis (vertical vs. horizontal positioning)

**Usage:**
```
Analyze the messaging strategy across [3 competitor URLs]. 
Identify common positioning themes, messaging gaps, and unique 
language each competitor owns.
```

### 5. **Differentiation Gap Analysis**
Automatically identifies:
- Underserved buyer personas
- Feature gaps between competitors
- Messaging white space (what's NOT being emphasized)
- Pricing gaps (where no competitor sits)
- Emotional positioning opportunities (logic-only market, emotion-only market)

**Usage:**
```
Analyze [5 competitors] and identify 5 differentiation angles 
we could own. For each angle, explain: which competitor weakness 
it targets, which buyer personas care, and how to message it.
```

### 6. **Competitive Positioning Matrix**
Generates visual/tabular outputs:
- Feature comparison tables (auto-populated from analysis)
- Price vs. feature scatter plots (positioning in 2D space)
- Messaging theme clustering
- Target buyer persona mapping

**Usage:**
```
Create a competitive positioning matrix for [category]. 
Show price vs. ease-of-use positioning, highlight positioning clusters, 
and identify white space opportunities in the matrix.
```

### 7. **Strategic Recommendation Engine**
Outputs actionable recommendations:
- 3-5 differentiation angles with implementation guidance
- Recommended positioning statement options
- Feature emphasis recommendations for your roadmap
- Pricing strategy suggestions (tier structure, price points, anchor strategy)
- Go-to-market messaging priorities

**Usage:**
```
Based on your analysis of [competitors], recommend:
1. Our ideal positioning statement (2-3 options)
2. Top 5 features we should emphasize (in priority order)
3. Recommended pricing ladder and anchor strategy
4. Key messaging differentiators we should own
```

---

## Configuration

### Required Environment Variables
```bash
# OpenAI API for analysis and synthesis
OPENAI_API_KEY=sk-...

# Google Search API for competitor discovery and URL validation
GOOGLE_SEARCH_API_KEY=your-api-key

# Optional: Slack webhook for async report delivery
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...

# Optional: Notion API token for direct Notion export
NOTION_API_TOKEN=notion_...
```

### Setup Instructions

1. **Get API Keys:**
   - OpenAI: https://platform.openai.com/api-keys
   - Google Search: https://developers.google.com/custom-search/v1
   - Slack (optional): https://api.slack.com/apps
   - Notion (optional): https://www.notion.so/my-integrations

2. **Set Environment Variables:**
   ```bash
   export OPENAI_API_KEY="sk-..."
   export GOOGLE_SEARCH_API_KEY="your-key"
   ```

3. **Verify Setup:**
   ```bash
   # Test API connectivity
   openclaw test product-teardown-positioning-analyzer
   ```

### Configuration Options

```yaml
analysis_depth: "comprehensive"  # fast | standard | comprehensive
  # comprehensive: full page analysis, 2000+ words output
  # standard: headline/pricing/features only
  # fast: quick feature list, basic positioning

include_pricing_analysis: true
include_feature_matrix: true
include_messaging_analysis: true
output_format: "markdown"        # markdown | json | notion | slack
competitor_limit: 5              # analyze up to N competitors per run
```

---

## Example Outputs

### Sample Output 1: Single Competitor Analysis

```
## INTERCOM POSITIONING ANALYSIS

### Core Positioning Statement
"The business messenger for customer communication"
- Primary positioning: Speed & omnichannel unified inbox
- Target buyer: SaaS companies, e-commerce, 100-5000 employees
- Emotional hook: "Build the business relationships that make your company thrive"

### Feature Hierarchy
**HERO FEATURES (Massive emphasis):**
1. Unified Inbox (all channels in one place)
2. AI-Powered Responses (automation)
3. Omnichannel Support (web, email, SMS, WhatsApp)

**SECONDARY FEATURES (Moderate emphasis):**
- Messaging personalization
- Conversation segmentation
- Knowledge base integration

**TABLE STAKES (Brief mention):**
- Reporting & analytics
- Team management
- API integrations

### Pricing Structure
- **Starter: $39/month** → Basic messaging, small teams
  - Psychological tactic: Accessibility anchor (low enough for SMBs)
- **Growth: $99/month** → Team features, automation
  - Psychological tactic: Feature jump (leads to belief in value)
- **Pro: $399/month** → Advanced automation, custom integrations
  - Psychological tactic: Enterprise price anchor (legitimacy signal)

### Positioning Gaps We Could Own
1. **Transparency-first pricing** (Intercom's pricing is hidden until demo)
2. **Vertical solutions** (Intercom is horizontal—we could own e-commerce or SaaS)
3. **Emotional simplicity** (Intercom's UX is feature-rich; we could be "dead simple")
4. **Cost transparency** (emphasize 40% cheaper than Intercom for comparable features)
5. **Local data residency** (privacy angle Intercom doesn't highlight)

### Recommended Positioning Statement for Competitor
"The simple, transparent customer messenger for growing SaaS"
- Emphasize: cost, ease of use, data privacy
- De-emphasize: advanced automation (let Intercom own that)
```

### Sample Output 2: Competitive Positioning Matrix

```
## COMPETITIVE POSITIONING MATRIX

| Competitor  | Price Anchor | Feature Count | Target Size | Primary Positioning |
|-------------|-------------|---------------|-------------|-------------------|
| Zendesk     | $49/mo      | 120+          | Enterprise  | Omnichannel scale |
| Freshdesk   | $19/mo      | 90+           | SMB/mid     | Value for money   |
| Help Scout  | $25/mo      | 40            | SMB         | Simplicity        |
| Gorgias     | $10/mo      | 60            | E-commerce  | Vertical focus    |

## WHITE SPACE OPPORTUNITIES
- No competitor positions on "AI-native from the ground up"
- No competitor emphasizes "developer-first" (all are user-first)
- Mid-market ($5-30k/year) is crowded; enterprise ($50k+) is crowded; SMB (<$5k) is white space
- Privacy/data residency is completely unowned
```

### Sample Output 3: Differentiation Angles

```
## 5 RECOMMENDED DIFFERENTIATION ANGLES

### 1. AI-Native Positioning (Exploit: Intercom's AI feels bolted-on)
- Messaging: "Built for AI from the ground up. Every feature uses AI."
- Target: Fast-growth SaaS, CX leaders experimenting with automation
- Feature emphasis: AI response suggestions, smart routing, predictive analytics
- Pricing: $59/mo (between Freshdesk and Zendesk, "AI premium" anchor)

### 2. Vertical SaaS (Exploit: Gorgias owns e-commerce; no one owns SaaS)
- Messaging: "Customer support software built specifically for SaaS"
- Target: B2B SaaS companies, 20-500 employees
- Feature emphasis: Slack integration, developer API, billing-system hooks
- Pricing: $79/mo ("SaaS premium" vs. general-purpose tools)

### 3. Radical Simplicity (Exploit: Help Scout's simplicity + affordability gap)
- Messaging: "Support software that actually gets used without training"
- Target: lean teams, startups, non-technical founders
- Feature emphasis: 4-screen onboarding, smart defaults, best practices built-in
- Pricing: $9/mo (undercut Help Scout, own "affordable" positioning)

### 4. Developer Experience (Exploit: No competitor emphasizes dev experience)
- Messaging: "Customer support for developers, by developers"
- Target: Technical founders, developer-first products, API-first companies
- Feature emphasis: Webhooks, CLI tools, SDKs, local development
- Pricing: $89/mo ("developer premium," GitHub integration worth the cost)

### 5. Privacy & Data Residency (Exploit: GDPR, SOC 2, data sovereignty concerns unaddressed)
- Messaging: "Customer support with your data under your control"
- Target: EU companies, healthcare, finance, privacy-conscious enterprises
- Feature emphasis: On-premise option, data residency controls, encryption
- Pricing: $199/mo enterprise (premium for compliance peace of mind)
```

---

## Tips & Best Practices

### 1. **Analyze 3-5 Competitors, Not 1**
Analyzing a single competitor reveals what they do; analyzing 5 reveals what they all avoid (your white space).

**Pro Tip:** Include 1-2 "non-obvious" competitors (e.g., for CRM, analyze Notion—it's eating their lunch even though it's not positioned as a CRM).

### 2. **Look for Negative Space**
The most valuable insights are what competitors DON'T emphasize. If all 5 competitors are silent on pricing transparency, that's an opportunity.

**Action:** Ask the skill: "What are the 3 most common features that are NEVER mentioned in sales copy?"

### 3. **Separate Positioning from Reality**
Competitors position HOW THEY WANT to be perceived, not necessarily how they actually are. Focus on their positioning claims, not your own opinion of their product.

**Action:** Request analysis of "stated positioning" vs. "actual feature allocation" to spot positioning-reality gaps.

### 4. **Use Feature Matrices for Roadmap Prioritization**
Once you have the feature matrix, share it with your product team. It shows which features are "table stakes" (everyone has them—you must too) vs. "differentiators" (few have them—you should emphasize these).

**Workflow:** Competitive analysis → Feature matrix → Roadmap prioritization → Messaging strategy

### 5. **Benchmark Messaging Language Across Competitors**
Ask the skill to identify the most common words in competitor messaging (e.g., "simple" appears 47 times across 5 competitors). These are over-claimed. Own different language.

**Example Prompt:**
```
Analyze messaging across these 5 competitors. Which adjectives appear 
most frequently? Which words are completely absent? Recommend 5 
"unclaimed" positioning words we could own.
```

### 6. **Pricing is Psychological, Not Mathematical**
The skill extracts pricing structure, but remember: competitors' prices signal their target buyer. If competitor A is $9/mo and competitor B is $299/mo, they're not competing—they're serving different segments.

**Action:** Request "pricing psychology analysis" to understand why each competitor chose their tier names, price points, and feature allocation.

### 7. **Export Findings to Your Workflow**
This skill integrates with:
- **Slack:** Post findings to #marketing or #strategy channels
- **Notion:** Export analysis directly to Notion workspace (pre-formatted)
- **Google Sheets:** Populate competitive matrices for team collaboration
- **WordPress:** Auto-generate competitor comparison pages from analysis

**Quick Export:**
```
Run the analysis, then "Export this to Notion" or "Post summary to #marketing Slack channel"
```

---

## Safety & Guardrails

### What This Skill Will NOT Do

1. **Scrape Terms of Service:**
   - This skill only analyzes publicly displayed marketing copy and feature lists.
   -