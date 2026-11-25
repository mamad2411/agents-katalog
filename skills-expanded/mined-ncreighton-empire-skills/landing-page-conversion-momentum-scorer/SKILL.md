---
name: landing-page-conversion-momentum-scorer
description: "Analyze landing pages for psychological friction, score conversion momentum at each funnel step, and generate A/B tests ranked by expected lift. Use when the user needs conversion optimization, competitor benchmarking, or CTA clarity improvements."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["OPENAI_API_KEY","GOOGLE_SEARCH_API_KEY","SERP_API_KEY"],"bins":["curl","node"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"🚀"}}
---

## Overview

The **Landing Page Conversion Momentum Scorer** is a production-grade conversion optimization engine that transforms raw landing page data into actionable growth insights. Rather than surface-level SEO audits, this skill performs deep psychological analysis—identifying the exact friction points sabotaging conversions, quantifying conversion momentum loss at each funnel stage, and delivering A/B test recommendations ranked by expected revenue lift.

### Why This Matters

Landing page optimization is rarely about one element—it's about *momentum*. Users arrive with intent, but lose confidence at predictable moments:
- **Copy-design misalignment** (value prop doesn't match design hierarchy)
- **Trust signal gaps** (missing social proof at decision moments)
- **CTA clarity breakdown** (unclear next steps, contradictory messaging)
- **Objection handling failure** (FAQ appears too late, doesn't address fears)

This skill quantifies these moments and benchmarks your page against competitors in your category. Instead of guessing, you get a prioritized roadmap with expected lift percentages.

### Integrations & Tools
- **Web scraping**: Analyzes any publicly accessible landing page (WordPress, Webflow, custom)
- **Competitor benchmarking**: SERP API, Google Search integration for competitive teardowns
- **CMS compatibility**: WordPress REST API, Webflow API for direct editing recommendations
- **Slack notifications**: Sends momentum scores and top 3 test recommendations
- **Google Sheets export**: Stores historical scores to track optimization velocity
- **A/B testing platforms**: Generates experiment specs for Optimizely, VWO, Convert

---

## Quick Start

### Example Prompt 1: Basic Landing Page Analysis
```
Analyze my landing page at https://example.com/pricing for conversion friction.
Score the momentum at each funnel step: awareness → consideration → decision.
Identify the top 3 friction points and suggest A/B tests ranked by expected lift.
```

### Example Prompt 2: Competitor Benchmarking
```
Score the conversion momentum on my landing page (https://mysite.com/demo) 
compared to 3 competitors in the project management software space.
For each competitor, identify their strongest CTA design pattern and 
their biggest objection-handling gap. Show me where we're losing momentum.
```

### Example Prompt 3: Specific Friction Audit
```
My landing page copy says "Enterprise-grade security" but the design looks minimal/startup-y.
Audit the copy-design misalignment and tell me:
1. What trust signals are missing at the decision stage?
2. What objections my target buyer has that we're not addressing?
3. A/B tests to bridge this gap, ranked by expected conversion lift.
```

### Example Prompt 4: Funnel Momentum Deep Dive
```
Run a complete momentum analysis on https://example.com/webinar-signup.
For each step (landing → form → confirmation), quantify where users lose confidence.
Include competitor comparison (top 3 webinar signup pages in my space).
Output as Google Sheets tab with: Step | Momentum Score (0-100) | Friction Type | A/B Test | Expected Lift.
```

---

## Capabilities

### 1. **Psychological Friction Detection**
The skill scans landing pages for 20+ friction patterns:
- **Cognitive load**: Paragraph density, color contrast, visual hierarchy clarity
- **Copy-design misalignment**: Value prop placement vs. design emphasis
- **Trust signal timing**: Where social proof, credentials, guarantees appear in scroll journey
- **CTA ambiguity**: Button text clarity, action mapping to user mental model
- **Objection gaps**: FAQ placement/completeness vs. likely buyer concerns
- **Urgency/scarcity balance**: Honest vs. manipulative urgency language
- **Mobile friction**: Tap target size, form field progression, CTA accessibility

**Usage**: 
```
Analyze my landing page for all friction points. 
Focus on objection handling—what's stopping a CFO from signing up? 
Show me where those objections could be addressed in page flow.
```

### 2. **Conversion Momentum Scoring** (0-100 Scale)
Scores each funnel stage with diagnostic breakdown:

| Stage | Score | Friction | Momentum Loss |
|-------|-------|----------|--------------|
| **Awareness** (headline clarity, value prop) | 78/100 | Headline uses jargon | -15% |
| **Consideration** (proof, differentiation) | 62/100 | Social proof too generic | -22% |
| **Decision** (objection handling, trust) | 41/100 | No guarantee shown | -38% |
| **Action** (CTA clarity, friction) | 55/100 | Form asks 8 fields | -28% |

Momentum loss compounds: A visitor losing 15% confidence at awareness then 22% at consideration arrives at decision 35% less likely to convert.

**Usage**:
```
Score my landing page's conversion momentum at each funnel step.
Tell me the cumulative momentum loss by the time users reach the CTA.
Which single friction point, if fixed, would unlock the most momentum recovery?
```

### 3. **Competitor Benchmarking**
Analyzes top-ranking competitors in your category:
- Scrapes and scores 3-5 competitor landing pages (SERP API integration)
- Compares your friction profile vs. theirs
- Identifies their strongest conversion patterns (CTA wording, social proof density, trust signals)
- Flags where you're losing ground, where you're ahead
- Extracts their A/B testing patterns (multiple CTA variants, form field counts)

**Usage**:
```
Benchmark my landing page against the top 3 SaaS project management tools 
(Asana, Monday.com, ClickUp). 
For each competitor, show me: their conversion momentum score at decision stage,
their strongest CTA pattern, and where they handle objections better than us.
```

### 4. **A/B Test Recommendations (Ranked by Expected Lift)**
Generates 8-15 A/B tests, ranked by expected conversion uplift:

| Rank | Test | Current | Variant | Expected Lift | Statistical Power | Time to Significance |
|------|------|---------|---------|---------------|--------------------|----------------------|
| 1 | Headline specificity | "Enterprise CRM" | "Close 3x more deals in 90 days" | +22% | 85% | 14 days (5K visitors) |
| 2 | CTA clarity | "Get started" | "Start 14-day free trial" | +18% | 80% | 10 days |
| 3 | Social proof placement | FAQ bottom | Customer logos top of fold | +14% | 75% | 21 days |
| 4 | Objection addressing | None visible | "Works with Salesforce, HubSpot, Slack" | +12% | 70% | 28 days |

Estimates based on industry benchmarks for your category (SaaS, e-commerce, B2B, etc.).

**Usage**:
```
Generate my top 5 A/B tests ranked by expected lift.
I can only run 2 tests this month—which would give us the fastest ROI?
Show me the sample size needed and time to significance for each.
```

### 5. **Copy-Design Alignment Audit**
Detects when messaging doesn't match visual emphasis:
- Headline says "Budget-friendly" but design looks premium/expensive
- Value prop emphasizes speed but page is copy-heavy with slow scrolling
- Trust signals in footer (should be mid-page before objection)
- CTA button color contrasts with page but color theory suggests different choice

**Usage**:
```
Audit my landing page for copy-design misalignment.
My headline is "Secure, enterprise-grade" but my design is minimalist/modern.
Does this feel aligned to a CTO evaluating security software?
What design changes would reinforce the copy message?
```

### 6. **Objection Handling Analysis**
Identifies buyer objections specific to your industry/product and checks if page addresses them:

**For B2B SaaS**: Cost-benefit, implementation difficulty, integration fit, support quality
**For E-commerce**: Product quality, shipping cost/time, returns process, payment security  
**For Services**: Credentials, turnaround time, process transparency, refund policy

Scores objection handling completeness and optimal placement in funnel.

**Usage**:
```
What are the top 5 objections a VP of Sales would have 
before signing up for my CRM platform?
Where on my landing page should I address each one?
Do I address them at all? If not, generate copy suggestions.
```

---

## Configuration

### Environment Variables (Required)
```bash
# OpenAI for content analysis and A/B test generation
export OPENAI_API_KEY="sk-..."

# Google Search for competitor landing page discovery
export GOOGLE_SEARCH_API_KEY="..."
export GOOGLE_SEARCH_ENGINE_ID="..."

# SERP API for competitive benchmarking (more reliable than Google)
export SERP_API_KEY="..."

# Optional: Slack notifications
export SLACK_WEBHOOK_URL="https://hooks.slack.com/..."

# Optional: Google Sheets output
export GOOGLE_SHEETS_API_KEY="..."
```

### Configuration Options
```
--industry: "saas" | "ecommerce" | "b2b" | "services" | "education"
  (optimizes friction detection and objection targeting)

--target-audience: "cto" | "cfo" | "marketing-director" | "entrepreneur"
  (tailors objection analysis and trust signal scoring)

--benchmark-count: 3-5 (default: 3)
  (number of competitors to analyze; more = slower but more insights)

--export-format: "json" | "markdown" | "csv" | "google-sheets"
  (output format; defaults to detailed markdown report)

--focus-stage: "awareness" | "consideration" | "decision" | "action" | "all"
  (optional narrow focus; default analyzes all stages)
```

### Setup Steps
1. **Add API keys** to environment or `.env` file
2. **Provide landing page URL** (must be publicly accessible)
3. **Specify industry & target audience** (improves friction detection accuracy)
4. **Optional: Connect Slack/Google Sheets** for automated reporting
5. **Run analysis** — typically completes in 2-4 minutes

---

## Example Outputs

### Output 1: Momentum Score Report (Markdown)
```markdown
# Landing Page Conversion Momentum Analysis
**URL**: https://example.com/pricing
**Analysis Date**: 2025-01-15
**Overall Momentum Score**: 61/100 ⚠️

## Funnel Stage Breakdown

### Stage 1: Awareness (Headline & Value Prop)
- **Score**: 78/100 ✓
- **Assessment**: Headline is specific ("Cut deployment time by 60%") and addresses 
  primary buyer pain. Good use of number.
- **Friction Detected**: None critical.
- **Momentum Loss**: -5%

### Stage 2: Consideration (Proof & Differentiation)  
- **Score**: 62/100 ⚠️
- **Assessment**: Social proof present (3 customer logos) but generic. 
  Lacks specifics (revenue impact, industry).
- **Friction Detected**: 
  - Social proof too vague (names only, no metrics)
  - Feature list is 12 bullets (cognitive overload)
  - Competitor differentiation unclear
- **Momentum Loss**: -22%

### Stage 3: Decision (Objections & Trust)
- **Score**: 41/100 ❌ CRITICAL
- **Assessment**: Major gaps. Objections unaddressed.
- **Friction Detected**:
  - No guarantee/refund policy visible
  - No implementation timeline shown
  - Security/compliance credentials missing (likely concern for this buyer)
  - No customer testimonials with specific results
  - FAQ doesn't address "Will this work with our legacy system?"
- **Momentum Loss**: -38%

### Stage 4: Action (CTA & Form Friction)
- **Score**: 55/100 ⚠️
- **Assessment**: CTA button clear but form asks 8 fields upfront.
- **Friction Detected**:
  - Form fields: email, name, company, role, company size, use case, 
    timeline, budget (high friction)
  - No progress indicator in multi-step form
  - No value reassurance before form (e.g., "Takes 30 seconds")
- **Momentum Loss**: -28%

## Cumulative Momentum Loss
- Awareness → Consideration: -5% → -27% cumulative
- Consideration → Decision: -27% → -65% cumulative
- Decision → Action: -65% → -93% cumulative ⚠️

**Result**: 93% of visitors who reach the CTA are below decision confidence.

## Top 3 A/B Tests (Ranked by Expected Lift)

### Test 1: Add Customer Results to Decision Stage 
**Expected Lift**: +22% | **Confidence**: 85% | **Time to Sig**: 14 days
- **Current**: Generic social proof (logos)
- **Test**: Add 3 specific customer testimonials with metrics:
  - "Acme Corp reduced deployment from 4 weeks to 5 days"
  - "TechFlow decreased infrastructure costs by $200K/year"
  - "GlobalBiz went from monthly to real-time reporting"
- **Why**: Decision stage is hemorrhaging momentum (-38%). Specific 
  social proof directly addresses confidence gap.

### Test 2: Add Security/Compliance Trust Signals
**Expected Lift**: +18% | **Confidence**: 80% | **Time to Sig**: 21 days
- **Current**: No visible compliance info
- **Test**: Add SOC 2 Type II, ISO 27001, GDPR badges + link to 
  security whitepaper in decision section
- **Why**: For B2B SaaS buyers, compliance is likely top objection. 
  Visible, early trust signal removes decision friction.

### Test 3: Reduce Form Fields + Add Value Prop
**Expected Lift**: +14% | **Confidence**: 75% | **Time to Sig**: 10 days
- **Current**: 8-field form
- **Test**: Reduce to 3 fields (email, company name, role). Add text: 
  "Takes 20 seconds. We'll schedule your 15-min personalized demo immediately."
- **Why**: Form friction is compounded by decision-stage doubt. 
  Quick win to improve action momentum.

## Competitor Benchmarking

### Competitor 1: Salesforce  
- **Momentum Score**: 78/100
- **Decision Stage**: 72/100 (vs. your 41/100)
- **Strongest Pattern**: Extensive customer case studies (not just logos) 
  with ROI metrics embedded throughout page
- **Their Objection Handling**: Addresses security, compliance, integration, 
  implementation in dedicated sections
- **Gap**: You're missing the systematic objection addressing.

### Competitor 2: HubSpot
- **Momentum Score**: 84/100
- **Decision Stage**: 81/100  
- **Strongest Pattern**: Risk reversal ("30-day free trial. No credit card. 
  Money-back guarantee.") right before CTA
- **Their Objection Handling**: Live chat widget addresses real-time concerns; 
  FAQ specifically labeled "Sales objections" 
- **Gap**: You lack visible risk reversal/guarantee messaging.

### Competitor 3: Zendesk
- **Momentum Score**: 71/100
- **Decision Stage**: 58/100 (similar to yours)
- **Strongest Pattern**: Industry-specific proof (banking, healthcare, SaaS 
  landing pages)
- **Their Objection Handling**: Allows filtering customer results by use case
- **Gap**: Your social proof is generic (not filtered by buyer need).

## Immediate Action Items

**This Week** (highest ROI):
1. Add 3 customer testimonials with specific metrics to decision section
2. Add security badge and compliance link
3. Reduce form from 8 to 3 fields; add "takes 20 seconds" copy

**Next Sprint** (next 2 weeks):
1. Create ROI