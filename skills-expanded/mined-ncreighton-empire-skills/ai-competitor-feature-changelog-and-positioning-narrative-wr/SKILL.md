---
name: ai-competitor-feature-changelog-and-positioning-narrative-writer
description: "Generate positioning narratives and sales messaging from competitor product releases. Use when the user needs rapid competitive analysis, feature comparison matrices, or differentiation strategies within 2 hours of detection."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["OPENAI_API_KEY", "SLACK_WEBHOOK_URL", "GOOGLE_ALERTS_API_KEY"],
        "bins": ["curl", "jq"]
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "🎯"
    }
  }
---

# AI Competitor Feature Changelog & Positioning Narrative Writer

## Overview

This skill automates competitive intelligence workflows by ingesting competitor product announcements, pricing changes, and feature releases—then generating differentiation narratives, comparison matrices, and battle-card sales messaging in under 2 hours.

**Why it matters:** Sales teams lose deals when competitors announce new features. Marketing teams scramble to update positioning. This skill eliminates that lag by automatically:

- **Monitoring** competitor release notes via RSS feeds, Google Alerts, and Slack integrations
- **Analyzing** feature announcements against your product capabilities
- **Generating** comparison matrices (feature-by-feature breakdowns)
- **Drafting** positioning narratives that address competitive threats
- **Creating** battle cards for sales teams with talking points
- **Publishing** updates to Slack, WordPress blogs, and internal wikis in real-time

Works with **Slack**, **Google Workspace**, **WordPress**, **GitHub**, **Notion**, and **HubSpot CRM**.

---

## Quick Start

### Example 1: Analyze a Single Competitor Release

```
Analyze this competitor release and generate positioning narrative:

Product: Acme Analytics Pro
Release: "New AI-powered anomaly detection with 40% faster query times"
Your differentiators: Real-time streaming, custom ML models, 99.99% uptime SLA

Generate:
1. Feature comparison (table format)
2. Positioning narrative (200 words)
3. Sales talking points (5 bullet points)
4. Threat level assessment (1-10 scale)
```

### Example 2: Bulk Competitor Monitoring with Slack Alerts

```
Monitor these 5 competitors for product announcements:
- Competitor A (tech-news RSS feed)
- Competitor B (LinkedIn announcements)
- Competitor C (Product Hunt)
- Competitor D (Twitter/X API)
- Competitor E (Email newsletter)

When new releases detected:
1. Send Slack alert to #competitive-intelligence
2. Generate comparison matrix
3. Draft battle card
4. Flag to sales leadership if threat level > 7/10
```

### Example 3: Create Dynamic Pricing Response Strategy

```
Our competitor just dropped pricing from $500/mo to $299/mo.
Our current pricing: $399/mo (10 seats included, theirs: 5 seats).

Generate:
1. Value narrative explaining why we're still better value
2. ROI calculator showing total cost of ownership
3. Email template for customer retention
4. Sales objection handler for "why should we stay?"
```

---

## Capabilities

### 1. Automated Competitor Monitoring
- **RSS Feed Ingestion**: Automatically parse competitor blog feeds, Product Hunt launches, and press release wires
- **Google Alerts Integration**: Trigger analysis when competitor mentions spike
- **Email Newsletter Parsing**: Extract feature announcements from competitor marketing emails
- **Social Media Tracking**: Monitor Twitter/X, LinkedIn, and Reddit for announcements
- **GitHub Release Monitoring**: Track open-source competitor repos for version bumps and feature PRs

**Usage Example:**
```
Set up continuous monitoring for 8 competitors across 12 data sources.
Auto-trigger analysis when announcement confidence > 85%.
```

### 2. Feature Comparison Matrix Generation
Automatically creates side-by-side feature tables with:
- Your product vs. 1-5 competitors
- Feature availability (✓/✗/Partial)
- Pricing tiers comparison
- Integration ecosystem breadth
- Performance benchmarks (where available)
- Customer support SLAs

**Output Format:**
| Feature | Your Product | Competitor A | Competitor B |
|---------|-------------|--------------|--------------|
| AI Anomaly Detection | ✓ (Custom ML) | ✓ (Pre-trained) | ✗ |
| Real-time Streaming | ✓ (Sub-100ms) | Partial (500ms) | ✓ (200ms) |
| Custom Integrations | ✓ (Unlimited) | ✓ (Limited) | ✗ |

### 3. Positioning Narrative Generation
Drafts 200-500 word narratives that:
- Acknowledge competitor strengths (credibility)
- Highlight your differentiation (specificity)
- Address the customer pain point they're solving (empathy)
- Position your approach as superior (persuasion)
- Include proof points: customer testimonials, case studies, benchmarks

**Sample Output:**
> "While Competitor A excels at quick setup, they sacrifice customization. Our platform offers both—pre-built templates for fast deployment AND unlimited custom ML model integration. For enterprises managing 500+ data sources, this flexibility is non-negotiable."

### 4. Sales Battle Cards
Auto-generates one-pagers with:
- **Threat Level**: 1-10 assessment of competitive risk
- **Objection Handlers**: "Why not Competitor X?" with 3-4 response options
- **Talking Points**: 5-7 differentiators backed by data
- **Customer Stories**: Relevant case studies showing your advantages
- **Pricing Justification**: ROI calculator and cost-of-ownership comparison
- **Proof Points**: Benchmarks, certifications, awards, third-party validation

### 5. Real-time Slack Integration
- **Instant Alerts**: New competitor announcements → #competitive-intelligence channel in <5 min
- **Interactive Buttons**: "View Analysis", "Share with Sales", "Add to Battle Card Library"
- **Daily Digest**: Morning briefing on competitive landscape changes
- **Escalation Workflow**: Threat level > 8 → auto-notify VP of Product & Sales Leadership

### 6. WordPress Blog Publishing
Auto-draft competitive comparison blog posts:
- SEO-optimized titles ("How [Your Product] Compares to [Competitor] in 2024")
- Structured data markup for featured snippets
- Internal linking to product pages
- Call-to-action buttons to sales demos
- Publish to WordPress with scheduling (review before going live)

### 7. HubSpot CRM Sync
- Tag deals with relevant competitive threats
- Add battle card attachments to contacts
- Auto-create tasks for sales reps: "Respond to Competitor X mention in prospect email"
- Track win/loss reasons against specific competitors

---

## Configuration

### Required Environment Variables

```bash
# OpenAI API for narrative generation
export OPENAI_API_KEY="sk-proj-..."

# Slack for real-time alerts and publishing
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
export SLACK_BOT_TOKEN="xoxb-..."

# Google Alerts and Gmail for competitor monitoring
export GOOGLE_ALERTS_API_KEY="..."
export GMAIL_SERVICE_ACCOUNT_JSON="path/to/service-account.json"

# Optional: WordPress, HubSpot, GitHub integrations
export WORDPRESS_API_TOKEN="..."
export HUBSPOT_API_KEY="..."
export GITHUB_TOKEN="..."
```

### Setup Instructions

1. **Create Google Alert projects** for each competitor name + "pricing" + "feature release"
2. **Add RSS feeds** to monitoring queue (competitor blogs, Product Hunt, Hacker News)
3. **Configure Slack channel** (#competitive-intelligence) and webhook
4. **Map your product features** to taxonomy (used for comparison matrix generation)
5. **Define threat thresholds** (what triggers escalation to leadership)
6. **Set publishing rules** (auto-publish battle cards vs. review-first)

### Configuration File Example

```yaml
competitors:
  - name: "Competitor A"
    data_sources:
      - type: "rss"
        url: "https://competitora.com/blog/feed"
      - type: "google_alerts"
        query: "Competitor A product release"
      - type: "github"
        repo: "competitora/public-roadmap"
    threat_level_baseline: 7
    
  - name: "Competitor B"
    data_sources:
      - type: "twitter"
        handle: "@competitorb"
      - type: "email_newsletter"
        address: "updates@competitorb.com"
    threat_level_baseline: 5

positioning:
  your_product_name: "Your Product"
  key_differentiators:
    - "Real-time streaming at sub-100ms latency"
    - "Custom ML model training (not pre-trained only)"
    - "99.99% uptime SLA with guaranteed support"
  
publishing:
  slack_enabled: true
  wordpress_enabled: true
  auto_publish_battle_cards: false  # Review first
  threat_threshold_for_escalation: 8
```

---

## Example Outputs

### Output 1: Feature Comparison Matrix

```
COMPETITOR ANALYSIS: Acme Analytics Pro vs. Your Product
Generated: 2024-01-15 14:32 UTC
Threat Level: 8/10 (ESCALATED TO LEADERSHIP)

| Feature | Your Product | Acme Analytics Pro | Winner |
|---------|-------------|-------------------|--------|
| Query Speed | 120ms (p95) | 72ms (p95) | Acme |
| Custom ML Models | ✓ Unlimited | ✗ Pre-trained only | You |
| Real-time Streaming | ✓ <100ms | ✗ Batch only | You |
| Data Connectors | 150+ | 80+ | You |
| Uptime SLA | 99.99% | 99.9% | You |
| Price (100 users) | $4,999/mo | $2,999/mo | Acme |
| Support Response | 15 min (P1) | 1 hour (P1) | You |
```

### Output 2: Sales Battle Card

```
BATTLE CARD: "Acme Analytics Pro"
Threat Level: 8/10 | Date: Jan 15, 2024

COMPETITIVE POSITIONING
Acme just released v3.0 with "40% faster queries." They're positioning 
this as the speed leader. Our advantage: we're faster for custom workloads 
(their speed is pre-trained models only). For custom ML, we're 3x faster.

OBJECTION HANDLERS
Q: "Acme is 40% faster than you."
A: "That's on their pre-built models. For custom ML—which 60% of 
   enterprises need—we're 3x faster. See this benchmark: [link]"

Q: "Acme is $1,500/mo cheaper."
A: "Their pricing excludes custom integrations ($800/mo add-on). 
   Our all-in cost is $500/mo lower. Plus, your data scientists 
   save 40 hours/month with our ML tools—that's $15k in labor."

TALKING POINTS
✓ Custom ML models (Acme: pre-trained only)
✓ Real-time streaming (Acme: batch only)
✓ 99.99% SLA (Acme: 99.9%)
✓ 150 data connectors (Acme: 80)
✓ 15-min P1 support (Acme: 1 hour)

PROOF POINTS
- TechCrunch: "Best-in-class for enterprise ML" (Jan 2024)
- Gartner: Leader in Data Analytics Magic Quadrant
- Case Study: Fortune 500 Bank saved $2.3M annually with custom models
```

### Output 3: WordPress Blog Draft

```
Title: "Acme Analytics Pro vs. Your Product: Full Feature Comparison (2024)"

Slug: acme-analytics-pro-vs-your-product-comparison

Meta Description: "Compare Acme Analytics Pro vs. Your Product. 
See pricing, features, speed, and integrations side-by-side. 
Which is right for your team?"

---

BLOG BODY:

Acme Analytics Pro just released v3.0, claiming 40% faster queries. 
But speed isn't everything. Here's how Your Product stacks up—and 
where we actually outperform.

## Speed: Acme Wins (But With Caveats)

Acme's 40% speed improvement applies to pre-built models. For custom 
machine learning—which 60% of enterprises require—Your Product is 
3x faster...

[Comparison table embedded]

## Custom ML Models: Your Product Wins

Acme offers pre-trained models only. Your Product lets data scientists 
train custom models without touching infrastructure...

[Feature comparison]

## The Real Cost: Your Product Wins

Acme's $2,999/mo doesn't include custom integrations. Add those, and 
you're at $3,799/mo. Your Product is $4,999/mo all-in, but includes...

[ROI calculator embedded]

## Verdict

For teams needing speed on pre-trained models: Acme wins.
For enterprises needing custom ML, real-time streaming, and 99.99% 
uptime: Your Product is the clear choice.

[CTA: "Schedule a 20-min demo to see custom ML in action"]
```

---

## Tips & Best Practices

### 1. Prioritize High-Signal Competitors
Not all competitors are equal. Focus monitoring on:
- **Direct Competitors**: Same use case, overlapping customer base
- **Upmarket Threats**: Smaller competitors growing into your space
- **Downmarket Threats**: Simpler/cheaper solutions stealing SMB deals

Deprioritize:
- Tangential competitors (different use case entirely)
- Mature, stable competitors (predictable releases)

### 2. Update Your Feature Taxonomy Quarterly
As you add features, update the comparison matrix template. This ensures:
- New differentiators are highlighted in battle cards
- Competitive analyses stay relevant
- Sales team sees your latest advantages

### 3. Create "Threat Tiers" for Escalation
```
Tier 1 (Threat 1-3): Monitor only, no escalation
Tier 2 (Threat 4-6): Alert sales team, add to weekly briefing
Tier 3 (Threat 7-9): Escalate to VP Product, VP Sales, CEO
Tier 4 (Threat 10): Emergency all-hands, immediate response required
```

### 4. Leverage Customer Feedback in Positioning
When a prospect mentions a competitor's new feature:
- Add it to the monitoring queue
- Ask: "What problem does that solve for you?"
- Use the answer to refine your positioning narrative
- Share insights with product team

### 5. A/B Test Battle Card Messaging
Different sales reps, different messaging. Track:
- Which objection handlers close deals?
- Which talking points resonate with which personas?
- Which proof points (case studies, benchmarks) drive demos?

Use this data to refine battle cards monthly.

### 6. Automate Competitive Win/Loss Analysis
Tag every closed deal with:
- Competitors evaluated
- Why customer chose you (or didn't)
- Which battle card messaging was used

This feedback loop improves positioning over time.

---

## Safety & Guardrails

### What This Skill Will NOT Do

❌ **Misrepresent competitor capabilities.** All positioning narratives include factual acknowledgment of competitor strengths.

❌ **Violate terms of service.** No scraping of competitor websites without permission. Uses only:
- Public RSS feeds
- Published press releases
- Social media (via official APIs)
- Email newsletters (opted-in)
- Google Alerts (public monitoring)

❌ **Make false claims about your product.** Battle cards require proof points (benchmarks, case studies, third-party validation) for all claims.

❌ **Publish without review.** By default, battle cards and blog posts go to draft status. Humans review before publishing.

❌ **Target individuals or teams.** Positioning is product-focused, not personal attacks on competitor employees.

### Limitations

- **Pricing data accuracy**: Competitor pricing changes frequently; verify before quoting in sales calls
- **Feature availability**: Announcements may not reflect GA (general availability) dates; confirm before claiming advantage
- **Latency**: Monitoring has 5-30 minute lag depending on data source (RSS slower than Twitter)
- **Language support**: Currently English-only; multi-language support coming Q2 2024
-