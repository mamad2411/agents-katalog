---
name: landing-page-micro-copy-persuasion-auditor
description: "Audit landing page micro-copy (buttons, forms, errors, tooltips) against psychological principles and A/B benchmarks. Use when the user needs conversion optimization, copy scoring, or persuasion improvements for any landing page."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["OPENAI_API_KEY"],"bins":["curl"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"📝"}}
---

# Landing Page Micro-Copy Persuasion Auditor

## Overview

The **Landing Page Micro-Copy Persuasion Auditor** is a production-grade skill that systematically reviews every micro-copy element on your landing page—buttons, CTAs, form labels, error messages, tooltips, urgency claims, social proof statements, and guarantee copy—against proven psychological principles (scarcity, reciprocity, social proof, authority) and industry A/B test benchmarks.

This skill automatically:
- **Scores persuasion strength** (0-100) for each element
- **Flags weak, generic, or missed-opportunity copy** with confidence ratings
- **Suggests high-conviction alternatives** backed by conversion psychology research
- **Identifies compliance risks** in urgency/scarcity claims
- **Generates actionable rewrite recommendations** with implementation priority

Perfect for SaaS founders, e-commerce teams, conversion specialists, and agencies. Integrates seamlessly with **Figma**, **WordPress**, **Webflow**, **Google Sheets**, and **Slack** for team collaboration.

---

## Quick Start

### Example 1: Audit a Complete Landing Page

```
Audit this landing page micro-copy for persuasion strength:

HEADLINE: "Software Solutions"
SUBHEADLINE: "We help businesses grow"
PRIMARY CTA BUTTON: "Get Started"
SECONDARY CTA: "Learn More"
FORM LABEL (Email): "Email Address"
ERROR MESSAGE: "Please enter a valid email"
URGENCY CLAIM: "Limited spots available"
SOCIAL PROOF: "1,000+ happy customers"
GUARANTEE: "30-day money back guarantee"

Please score each element, flag weak copy, and suggest rewrites.
```

### Example 2: Deep-Dive on CTA Button Copy

```
I'm getting 2.1% conversion rate on my SaaS landing page. 
My primary CTA button currently says "Sign Up Free."

Audit this button copy specifically. What psychological principles 
am I missing? What do high-converting alternatives look like? 
Compare against benchmark data for B2B SaaS.

Current: "Sign Up Free"
Page context: Enterprise data analytics platform, $99-$999/month plans
```

### Example 3: Form Micro-Copy Optimization

```
Audit the micro-copy on this lead capture form:

FORM HEADLINE: "Get Your Free Trial"
FORM SUBTEXT: "No credit card required"
EMAIL LABEL: "Email"
COMPANY LABEL: "Company Name"
BUTTON TEXT: "Start Free Trial"
DISCLAIMER: "We'll never share your information"
POST-SUBMIT MESSAGE: "Check your email"

Score each field. What's converting weakly? What am I not capitalizing on 
given the context (B2B SaaS, enterprise buyers, 45-year-old decision makers)?
```

---

## Capabilities

### 1. Micro-Copy Element Scoring
Evaluates every customer-facing text snippet against 12+ psychological principles:

- **Scarcity** (limited availability language)
- **Urgency** (time-sensitivity framing)
- **Social Proof** (specificity, recency, similarity)
- **Reciprocity** (what you're giving upfront)
- **Authority** (credentials, certifications, data)
- **Specificity** (numbers vs. vague claims)
- **Pain Point Resonance** (emotional relevance)
- **Clarity** (jargon, complexity, readability)
- **Action Orientation** (verb strength, specificity)
- **Trust Signals** (guarantees, money-back promises)
- **Friction Reduction** ("free," "no CC required," etc.)
- **Benefit Clarity** (outcome vs. feature)

**Output:** Each element gets a persuasion score (0-100) with subsection breakdowns.

### 2. Weakness Detection & Flagging

The auditor automatically identifies:
- Generic/overused phrases ("Learn More," "Click Here," "Submit")
- Missed scarcity/urgency opportunities
- Weak social proof (outdated, non-specific, low-relevance)
- Vague benefit statements
- Trust deficit indicators
- Compliance red flags (false urgency, unsubstantiated claims)
- Friction-inducing language

**Output:** Flagged elements with severity rating (High/Medium/Low) and reason.

### 3. High-Conviction Rewrite Suggestions

For each weak element, generates 3-5 alternative wordings:

```
ORIGINAL: "Get Started"
REWRITE OPTIONS:
1. "Start Your Free Trial" [+15 pts - Specificity & Friction Reduction]
2. "Claim Your 14-Day Access" [+22 pts - Scarcity & Urgency]
3. "Join 5,000+ Teams Using [Product]" [+18 pts - Social Proof]
4. "Access Your Dashboard Now" [+12 pts - Action Orientation]
```

Each rewrite includes:
- Persuasion principle applied
- Expected uplift (based on benchmark data)
- Compliance status (if applicable)

### 4. A/B Test Benchmark Comparisons

Compares your copy against industry benchmarks for:
- SaaS (landing pages, free trial flows)
- E-commerce (product pages, checkout)
- B2B (lead forms, demo CTAs)
- Nonprofit (donation pages, volunteer signups)

Shows percentile ranking and gap analysis.

### 5. Compliance & Risk Assessment

Flags potential legal/ethical issues:
- Unsubstantiated urgency claims ("Last chance!", "Ending today")
- Misleading scarcity language
- Privacy statement gaps
- Guarantee limitations not clearly stated

---

## Configuration

### Environment Variables

```bash
# Required for AI-powered analysis
export OPENAI_API_KEY="sk-..."

# Optional: For Figma/Slack integrations
export FIGMA_API_TOKEN="figma_..."
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
```

### Setup Instructions

1. **Paste your landing page copy** (HTML, text, or screenshot description)
2. **Specify your context:** industry, audience, conversion goal, current metrics
3. **Choose audit depth:** quick-scan (5 min), standard (15 min), or deep-dive (30 min)
4. **Set baseline metrics:** current conversion rate (if known) for personalized benchmarking

---

## Example Outputs

### Sample Audit Report

```
LANDING PAGE MICRO-COPY PERSUASION AUDIT
Date: 2024-01-15 | Industry: B2B SaaS | Page: Product Landing

═══════════════════════════════════════════════════════════════

PRIMARY HEADLINE: "Transform Your Data Into Action"
Persuasion Score: 78/100
├─ Specificity: 6/10 (could name the benefit more concretely)
├─ Action Orientation: 9/10 ✓
├─ Emotional Resonance: 8/10 ✓
└─ Authority/Proof: 2/10 (no data backing up claim)

RECOMMENDATIONS:
1. Keep headline structure (strong action verb)
2. Add specific metric: "Transform Your Data Into 40% Faster Decisions"
3. Add credibility marker: "Used by 2,000+ enterprises"

SEVERITY: Medium | Expected Uplift: +3-5% CTR
─────────────────────────────────────────────────────────────

PRIMARY CTA BUTTON: "Get Started"
Persuasion Score: 34/100 ⚠️ WEAK
├─ Specificity: 1/10 (generic)
├─ Friction Reduction: 2/10 (doesn't address objections)
├─ Scarcity/Urgency: 0/10 (none)
└─ Benefit Clarity: 4/10 (no outcome promised)

REWRITE OPTIONS:
1. "Start Your Free Trial" [+18 pts]
   Psychology: Specificity, Friction Reduction
   
2. "Access Free for 14 Days" [+22 pts]
   Psychology: Scarcity, Urgency, Friction Reduction
   
3. "See 40% Faster Decisions" [+25 pts]
   Psychology: Benefit Clarity, Pain Point Resonance

RECOMMENDED: #2 (balanced uplift + compliance safe)
SEVERITY: High | Expected Uplift: +8-12% CTR
─────────────────────────────────────────────────────────────

SOCIAL PROOF STATEMENT: "1,000+ happy customers"
Persuasion Score: 42/100
├─ Specificity: 5/10 (number good, but what type of customers?)
├─ Recency: 2/10 (no date)
├─ Similarity: 3/10 (no audience callout)
└─ Authority: 6/10 (respectable volume)

REWRITE OPTIONS:
1. "Trusted by 1,200+ enterprise customers (growing 15% MoM)"
   [+24 pts] - Adds growth signal + recency

2. "1,000+ companies including Fortune 500 firms rely on [Product]"
   [+18 pts] - Adds authority + similarity

SEVERITY: Medium | Expected Uplift: +2-4% conversion
─────────────────────────────────────────────────────────────

OVERALL PAGE SCORE: 51/100 (Below Average)
Estimated Current Conversion Rate Impact: -40% vs. best-in-class

QUICK WINS (Implement First):
1. Rewrite CTA button (+8-12% estimated)
2. Strengthen social proof (+2-4% estimated)
3. Add specific headline metric (+3-5% estimated)

Total Potential Uplift: +13-21% conversion rate increase
```

---

## Tips & Best Practices

### 1. Provide Rich Context
The more context you give, the better the recommendations:
- Industry & customer profile
- Current conversion rate
- Customer acquisition cost (CAC)
- Average customer lifetime value (LTV)
- Competitor positioning
- Audience pain points

**Example:**
```
Context: B2B SaaS, $5K-$50K/year pricing
Audience: CFOs & finance managers, 40-60 years old
Current CVR: 1.8% (below industry 2.2% benchmark)
Main objection: "We already use [Competitor]"
```

### 2. Test Rewrites A/B-Style
Don't implement all recommendations at once. Prioritize:
- **High-impact + Low-risk** first (CTA buttons, primary headlines)
- **Medium-risk** second (urgency claims, social proof updates)
- **Compliance-sensitive** last (guarantee statements, scarcity claims)

### 3. Align with Brand Voice
The auditor suggests generic high-converting alternatives. Adapt them to match your brand:
- Playful brands: "Jump In" instead of "Get Started"
- Enterprise: "Request Access" instead of "Sign Up"
- Nonprofits: "Make Your Impact" instead of "Donate Now"

### 4. Combine with Heatmaps & Session Recordings
Use insights from **Hotjar**, **Fullstory**, or **Microsoft Clarity** to understand where users are getting stuck. Then use this auditor to rewrite that friction point.

### 5. Monitor Benchmark Shifts
Copy that converts well today might be saturated tomorrow. Re-audit quarterly or after every major design refresh.

### 6. Focus on Your Bottleneck
If your landing page bounces at 60% without scrolling, focus on headline & primary CTA rewrites. If it bounces after scrolling, focus on form labels & error messages.

---

## Safety & Guardrails

### What This Skill Will NOT Do

❌ **Violate FTC Regulations** – The auditor flags potentially misleading claims (e.g., "last chance," false scarcity) and recommends compliance-safe language. Always verify urgency claims with legal.

❌ **Guarantee Conversion Rate Improvements** – Suggested uplift percentages are based on A/B test benchmarks, not predictions. Your results will vary based on audience, offer, and creative execution.

❌ **Create Deceptive Copy** – The skill prioritizes ethical persuasion. It will not suggest:
   - False scarcity ("Only 3 spots left!" when you have unlimited inventory)
   - Fake urgency ("Ending tonight!" for permanent offers)
   - Unsubstantiated health/legal claims

❌ **Replace Strategy with Tactics** – Strong micro-copy can't rescue a weak offer or poor targeting. Use this tool as part of a broader conversion strategy, not in isolation.

❌ **Audit Non-Landing Page Copy** – Optimized for landing pages, CTAs, and forms. Less effective for email bodies, social media ads, or long-form content (use other skills for those).

❌ **Guarantee Legal Compliance** – Always have a lawyer review guarantee statements, privacy claims, and industry-specific copy (financial services, healthcare, etc.).

### Known Limitations

- **Audience-Specific Testing:** The auditor uses general benchmarks. Your specific audience may respond differently (always A/B test).
- **Visual Context:** Copy lives within design. The auditor can't see button size, color, or page layout—provide context for nuanced recommendations.
- **Tone of Voice:** The skill suggests high-converting alternatives; you adapt them to match your brand voice.
- **Industry Nuance:** Benchmarks for B2B SaaS differ vastly from e-commerce or nonprofits. Specify your industry.

---

## Troubleshooting

### Q: "The auditor flagged my CTA as weak, but my conversion rate is already 3.5%. Should I change it?"

**A:** High absolute CVR doesn't mean the micro-copy is optimal—just that your offer is strong. Test the rewrite recommendations on 10-20% of traffic. If they don't improve, keep your current copy. If they do (+0.5%+ absolute uplift), implement broadly.

### Q: "I got conflicting recommendations (button text vs. urgency messaging). Which do I prioritize?"

**A:** The audit report ranks by severity and expected impact. Start with **High severity + High impact** (usually CTAs). Test urgency claims separately after baseline lifts from CTA rewrites.

### Q: "The auditor suggested urgency language, but I worry about being deceptive. What's the line?"

**A:** 
- ✓ **Ethical:** "Join 500 founders using [Product] this week" (factual, time-bound)
- ✓ **Ethical:** "Limited capacity: 10 spots left for launch pricing" (specific, verifiable)
- ❌ **Deceptive:** "Last chance! Only 3 seats left!" (if you have unlimited inventory)

When in doubt, check with legal. The auditor flags these risks—your job is to honor them.

### Q: "My landing page is very long (5+ sections). How do I prioritize what to audit?"

**A:** Audit in order of user drop-off:
1. **Headline + primary CTA** (70% of users see this)
2. **Form micro-copy** (50% reach the form)
3. **Social proof + guarantee** (30% scroll deep)
4. **Secondary CTAs + error messages** (10% interact fully)

### Q: "Can I use this skill for email copy or ad copy?"

**A:** The skill is optimized for landing pages and forms. For email or ads, micro-copy principles still apply, but email body copy and ad headlines have different benchmarks. Consider using a dedicated email copy auditor or ad copy optimizer for those channels.

### Q: "How often should I re-audit my landing page?"

**A:** 
- After design changes: immediately
- After offer changes: immediately
- Quarterly refresh: if no changes (competitive landscape shifts)
- Post-A/B test: to lock in winning variants and audit the next element
- After traffic surge: to ensure copy holds up at scale

---

## Integration Examples

### WordPress Landing Page Plugin
```
Plugin: Elementor Pro + LandingPage Builder
Workflow: Export landing page copy → Paste into auditor 
→ Implement recommendations via Elementor editor
```

### Figma Design Handoff
```
Designer creates mockup in