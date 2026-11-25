---
name: product-waitlist-copy-converter
description: "Transform product descriptions into high-converting waitlist copy with persuasion frameworks, competitor analysis, and A/B variations. Use when the user needs landing page copy, email sequences, or pre-launch marketing for SaaS, apps, or digital products."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["OPENAI_API_KEY","ANTHROPIC_API_KEY"],"bins":[]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"✨"}}
---

# Product Waitlist Copy Converter

Transform boring product descriptions into persuasive, conversion-optimized waitlist and landing page copy. This skill automates the entire copywriting process for indie hackers, startups, and pre-launch products by analyzing competitor messaging, applying proven persuasion frameworks (urgency, scarcity, social proof, FOMO), and generating multiple A/B test variations ready to deploy.

## Overview

**Why This Skill?**

Launching a product without compelling copy is like building a car without an engine. Most indie hackers spend 2-4 weeks manually crafting waitlist copy, testing messaging, and iterating on positioning. This skill compresses that work into minutes.

**What It Does:**
- Analyzes your raw product description and identifies key value propositions
- Researches competitor messaging (optional) to find positioning gaps
- Applies 6+ persuasion psychology frameworks (Cialdini principles, Agora, VSL structures)
- Generates 5-7 copy variations (headlines, subheadlines, body copy, CTAs)
- Creates A/B test variations optimized for different audience segments
- Produces email sequence hooks for waitlist nurture campaigns
- Formats output for direct paste into WordPress, Webflow, ConvertKit, or Slack announcements

**Integrations:**
- WordPress (paste directly into pages/posts)
- Webflow (copy to custom forms & landing pages)
- ConvertKit/Substack (email subject lines and body copy)
- Slack (share variants with your launch team)
- Google Docs (collaborative editing)
- Notion (store and organize copy variations)

---

## Quick Start

Try these prompts to see the skill in action:

### Prompt 1: Basic Waitlist Copy Generator
```
Convert this product description into high-converting waitlist copy:

PRODUCT: TimeBlock - A calendar app that uses AI to auto-schedule deep work sessions
DESCRIPTION: Helps knowledge workers protect focused time by automatically identifying 
gaps in their calendar and filling them with smart time blocks. Built with OpenAI API.
TARGET AUDIENCE: Indie developers, designers, remote workers
LAUNCH DATE: 2 weeks

Generate:
1. Headline (10 words max, uses curiosity or benefit)
2. Subheadline (15 words max)
3. Body copy (3 paragraphs, 80 words each)
4. CTA button text (3 variations)
```

### Prompt 2: Competitor Analysis + Positioning
```
Analyze competitors and create waitlist copy:

MY PRODUCT: NotionAI - a Notion plugin for AI-powered content generation
COMPETITORS: Copy.ai, Jasper.ai, ChatGPT plugins
UNIQUE ANGLE: 10x faster for Notion users, no context switching, $10/mo vs $25/mo

Create:
1. Positioning statement that differentiates from competitors
2. 3 headline variations emphasizing our unique angle
3. Urgency copy (scarcity + FOMO angle)
4. Social proof section template (what should we include?)
```

### Prompt 3: Email Nurture Sequence + A/B Tests
```
Build a 5-email waitlist nurture sequence with A/B variants:

PRODUCT: MockupPro - design tool for creating product mockups in 60 seconds
WAITLIST SIZE: 2,500 people
LAUNCH: 3 weeks away

For each email, provide:
- Subject line (A/B variant)
- Hook (first 2 sentences)
- Body (150 words, one persuasion angle per email)
- CTA

Email sequence arc:
1. Education email (teaches a pain point)
2. Social proof email (testimonials/use cases)
3. Scarcity email (limited beta spots, early bird pricing)
4. Feature breakdown (show the product solving pain)
5. Final CTA (launch day announcement)
```

### Prompt 4: Audience Segment Variations
```
Generate segment-specific copy for our waitlist:

PRODUCT: DevOps.cloud - infrastructure management platform
SEGMENTS: 
- Segment A: Startups (cost-conscious, speed matters)
- Segment B: Enterprises (security, compliance, support)
- Segment C: Freelance developers (simplicity, learning curve)

For each segment, create:
1. Personalized headline
2. Value prop statement (2 sentences)
3. Pain point acknowledgment
4. Feature benefit mapping
5. Social proof angle (case study hook or testimonial type)
```

---

## Capabilities

### 1. Copy Generation Frameworks
The skill applies multiple persuasion models:

**Framework Support:**
- **AIDA Model** (Attention, Interest, Desire, Action) - structured narrative flow
- **Problem-Agitation-Solution (PAS)** - emotional pain → relief narrative
- **Curiosity Gap** - headline hooks that demand a click
- **Scarcity + Urgency** - limited spots, founding member pricing, launch countdown
- **Social Proof** - testimonials, user count, press mentions
- **Fear of Missing Out (FOMO)** - exclusive access, beta closures, timeline pressure
- **Feature-Benefit Translation** - "smart scheduling" → "reclaim 5+ hours/week of deep work"

**Usage Example:**
```
Apply the PAS framework to this feature:
FEATURE: Real-time collaboration with 100+ concurrent users
OUTPUT: 
- Problem: "Your team wastes 30% of work time context-switching between tools"
- Agitate: "Jumping between apps kills focus, breeds miscommunication, delays shipping"
- Solution: "One unified workspace for the entire product team. See every update. 
  Ship faster."
```

### 2. Competitor Intelligence Module
Analyzes 3-5 competitor messaging patterns:
- Headlines (benefit vs. curiosity vs. feature-focused)
- Value prop clarity ranking
- Emotional vs. rational appeals
- CTA strength analysis
- Positioning gaps (what they DON'T emphasize)

**Usage Example:**
```
Competitor analysis for: AI writing assistant space
Analyze: Copy.ai, Jasper, Sudowrite, Contently
Output: Messaging matrix showing which angles are saturated and which are open
```

### 3. A/B Testing Variant Generation
Produces 3-5 variations per element:

**Headlines (5 variations):**
1. Benefit-driven ("Reduce meeting time by 70%")
2. Curiosity-based ("The calendar hack that changed everything")
3. Problem-focused ("Tired of back-to-back meetings?")
4. Feature-led ("AI-powered deep work protection")
5. Social proof ("Used by 5,000+ developers")

**CTAs (4 variations):**
1. Action-oriented ("Get Early Access Now")
2. Urgency-focused ("Claim Your Founding Member Spot")
3. Curiosity-based ("See How It Works")
4. Low-friction ("Join the Waitlist (30 seconds)")

### 4. Email Sequence Automation
Creates multi-email campaigns with:
- Progression arc (education → proof → urgency → conversion)
- Subject line variants (A/B optimized)
- Open rate psychology (curiosity, urgency, personalization)
- Conversion triggers (countdown timers, seat count, testimonials)
- Segment-specific variations

### 5. Landing Page Copy Blocks
Generates modular copy sections:
- Hero headline + subheadline
- Problem statement + agitation
- Solution explanation
- Feature-benefit section (3-5 features)
- Social proof block (testimonials, metrics)
- FAQ answers
- Closing CTA
- Footer messaging

---

## Configuration

### Environment Variables
```bash
OPENAI_API_KEY=sk-...              # For GPT-4 copy generation
ANTHROPIC_API_KEY=sk-ant-...       # Optional: Claude for alternative frameworks
COMPETITOR_RESEARCH_API=perplexity # Optional: web research for competitor analysis
```

### Setup Instructions

1. **Provide Your Product Info:**
   - Product name & category
   - Raw description (200+ words)
   - Target audience (demographic + psychographic)
   - Unique selling proposition (1-2 sentences)
   - Launch timeline (days until launch)
   - Budget if using competitor research API

2. **Select Copy Variants:**
   - Which frameworks to prioritize? (PAS, AIDA, Curiosity, Scarcity)
   - Tone preference (formal, conversational, playful, urgent)
   - Length constraints (short-form mobile vs. long-form desktop)

3. **Choose Output Formats:**
   - Plain text (email, Slack)
   - Markdown (Notion, GitHub)
   - HTML (WordPress, custom landing pages)
   - JSON (developer integration)

4. **A/B Testing Setup:**
   - How many variations per element? (3-7)
   - Which audience segments to target?
   - Export format (CSV for analytics tools, JSON for experiments)

---

## Example Outputs

### Example 1: SaaS Landing Page Copy

**INPUT:**
```
Product: DataViz Pro - no-code dashboard builder
Description: Connects to 50+ data sources, builds interactive dashboards 
in under 5 minutes, no SQL knowledge required
Audience: Non-technical business analysts, marketing teams
USP: Fastest time-to-insight for non-technical teams
```

**OUTPUT:**

**Hero Headline (Option A - Benefit):**
"Get Your Data Story in 5 Minutes, Not 5 Days"

**Hero Headline (Option B - Curiosity):**
"The Dashboard Builder Wall Street Analysts Aren't Telling You About"

**Subheadline (Best performing):**
"Connect your data sources. Build custom dashboards. Zero SQL. Launch in minutes."

**Body Copy (PAS Framework):**

**Problem:** "Your team drowns in spreadsheets. Data sits in disconnected silos. By the time you've extracted insights, the business has moved on."

**Agitation:** "Non-technical team members can't self-serve. They wait for engineers. Engineers resent building dashboards. Everyone's frustrated. Decisions get made without data."

**Solution:** "DataViz Pro is the first dashboard builder built for analysts, not engineers. Connect Postgres, Salesforce, Google Sheets, HubSpot—or all of them. Drag to visualize. Click to publish. Your team makes decisions in real-time."

**Social Proof Section:**
"Trusted by 2,400+ teams at Microsoft, Stripe, and 47 other Fortune 500 companies"

**CTA Variations:**
1. "Try DataViz Free (No Credit Card)"
2. "Get 30-Day Founding Member Discount"
3. "Watch 4-Min Demo"
4. "Join 500+ on Our Launch Waitlist"

---

### Example 2: Email Sequence (5-Part Launch Campaign)

**Email 1: Education Hook**
```
Subject Line A: "Why Your Team Wastes 12 Hours/Week on Dashboards"
Subject Line B: "The #1 mistake non-technical analysts make (and how to avoid it)"

Hi [Name],

Here's something we've noticed: most teams rebuild the same dashboard 3x.

Why? Because connecting data sources is hard. SQL is intimidating. 
Spreadsheets can't handle real-time data. So analysts end up waiting 
for engineers, or building brittle workarounds.

What if there was a better way?

[CTA: "See how analysts at Stripe build dashboards in 5 minutes"]

Cheers,
DataViz Team
```

**Email 3: Scarcity (Day 14)**
```
Subject Line A: "⏰ Founding Member Pricing Ends in 7 Days"
Subject Line B: "We're closing the early access door Friday"

We promised our first 100 users lifetime discounts. We're at 97 now.

When this tier fills, the next batch pays 3x more.

[CTA: "Claim Your Founding Member Spot ($29/mo forever)"]
```

**Email 5: Final CTA (Launch Day)**
```
Subject Line A: "🚀 DataViz Pro is live—here's what changed"
Subject Line B: "Your waitlist invitation is ready (limited to 48 hours)"

We're officially out of beta. DataViz Pro is live.

And we're giving you a special launch-day bonus: free setup consultation 
+ 3 months at 50% off.

This offer expires in 48 hours.

[CTA: "Launch Your First Dashboard Now"]
```

---

## Tips & Best Practices

### 1. Position Before You Polish
Before running copy generation, nail your positioning:
- What problem do you *uniquely* solve?
- Who else claims to solve it (be honest about competition)?
- What's different about your approach?
- Why does it matter *now*?

**Better Copy = Crystal-Clear Positioning First**

### 2. Test Your Biggest Claim First
Don't just test button colors. Test your core claim:
- "Get X in Y time" vs. "Get X without Z friction"
- "For everyone" vs. "Built for [specific type]"
- Lead with your competitive advantage, not your feature list

**Example:** "Dashboards in 5 minutes (no SQL)" beats "50+ integrations"

### 3. Use Real Data in Social Proof
Don't make up metrics. If you don't have proof yet:
- Use beta user testimonials (even better than numbers)
- Reference press/competitions/awards
- Show before/after examples
- Include founding member count as a progress indicator

### 4. Segment Your Copy
Different audiences respond to different angles:
- **Cost-conscious:** emphasize savings, pricing transparency
- **Enterprise:** emphasize security, compliance, support
- **Developers:** emphasize API quality, documentation, speed
- **Non-technical:** emphasize simplicity, no-code, time savings

Run different copy to each segment. One size does NOT fit all.

### 5. Create a Copy Swipe File
Save what works for your market:
- Top 10 SaaS headlines from your category
- Email sequences that drove conversions
- Product launch announcements with high engagement
- Reference these when asking for new copy variations

### 6. Test Copy on Real Humans First
Before running paid ads, share variants with:
- Your target audience (get their reactions in Slack/email)
- Your advisor/founder network (10-15 people)
- Your beta users (they know the pain point)
- Look for which version gets the most "tell me more" responses

### 7. Prioritize Clarity Over Cleverness
Avoid:
- Puns that distract from the value prop
- Trendy language that dates quickly
- Insider jargon your audience won't understand
- False scarcity (this damages trust)

### 8. Update Copy Based on Real Questions
Track questions you get:
- What confuses people on your landing page?
- What do 3+ people ask about? That's content you need.
- Clarify in your copy *before* people hit support

---

## Safety & Guardrails

### What This Skill Will NOT Do

**1. Generate False or Misleading Claims**
- Will not create scarcity/urgency if it's fake ("Limited spots!" with infinite capacity)
- Will not exaggerate features you don't have
- Will not promise results you can't deliver
- *Guidance:* Always validate copy against your actual product

**2. Create Unethical Dark Patterns**
- Will not generate manipulative countdown timers (unless real)
- Will not pressure people with false social proof
- Will not encourage spam tactics
- *Guidance:* Persuasion ≠ manipulation. Be honest.

**3. Plagiarize Competitor Copy**
- Will not copy competitor messaging verbatim
- Will analyze positioning but create original copy
- *Guidance:* Use competitor analysis for gaps, not as templates

**4. Guarantee Conversion Rates**
- This skill generates *better* copy, not miracle copy
- Conversion rates depend on audience fit, targeting, product quality
- *Guidance:* Test, measure, iterate. No shortcuts.

### Limitations & Boundaries

- **Input Length:** Best results with 200-1,000 word product descriptions (too short = missing context; too long = dilutes focus)
- **Market Research:** Uses public competitor analysis (not internal data or confidential positioning)
- **Personalization:** Best for B2B SaaS, apps, digital products (works less well for physical