---
name: launch-page-copy-converter-ad-sales-page
description: "Convert high-performing ad copy into long-form sales pages with benefit stacking, social proof, and objection handling. Use when the user needs to transform Facebook/Google ads into complete sales funnels."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["OPENAI_API_KEY"],"bins":[]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"📄"}}
---

# Launch Page Copy Converter: Ad → Sales Page

## Overview

The **Launch Page Copy Converter** transforms short-form, high-converting ad copy (Facebook ads, Google Search ads, LinkedIn ads) into comprehensive long-form sales page copy. This skill preserves the proven hooks and messaging from your best-performing ads while expanding them into a complete narrative arc with:

- **Benefit stacking** — layering 5-7 key benefits in persuasive hierarchy
- **Social proof integration** — seamlessly weaving testimonials, case studies, and social proof
- **Objection handling** — pre-emptively addressing buyer hesitations with logic-based rebuttals
- **CTA optimization** — multiple call-to-action variations (primary, secondary, urgency-driven)
- **Storytelling framework** — hero's journey structure (problem → agitate → solve → validate → transform)

**Why it matters:** Ad copy (35-150 characters) requires different psychology than sales pages (1,500-3,000 words). Your winning ad hooks identify the *emotional trigger*, but sales pages need *proof*, *narrative*, and *reassurance*. This skill bridges that gap, reducing copywriting time from 6-8 hours to 30 minutes while maintaining conversion intent.

**Integrations & Compatibility:**
- WordPress (paste directly into page builders like Elementor, Divi)
- Leadpages, ConvertKit landing page builders
- Google Docs (formatted for easy editing)
- Slack (export summaries for team review)
- HubSpot (import as email sequences or content assets)

---

## Quick Start

Try these prompts immediately:

### Example 1: Facebook Ad → Sales Page
```
Convert this Facebook ad to a complete sales page:

AD COPY:
"Tired of spreadsheets eating your life? 
Our automation framework cuts admin time by 87%.
See the 3-step system →"

TARGET AUDIENCE: Small business owners, overwhelmed with manual tasks
PRODUCT: Automation workflow software
PRICE POINT: $97/month
KEY BENEFIT: Time savings (measure: hours per week)

---

Include:
- Opening hook from the ad
- 6-7 stacked benefits (time, money, peace of mind)
- 3 customer testimonials (realistic, specific metrics)
- Address: "Won't this break my current setup?" objection
- 2 CTAs: Primary (Sign Up Free Trial) + Secondary (Watch 5-Min Demo)
```

### Example 2: Google Ads → Sales Page with Social Proof
```
I'm converting a Google Search ad to a sales page. Here's the ad:

AD HEADLINE: "HVAC License Training | 60% Faster | Money-Back Guarantee"
AD COPY: "State-approved curriculum. 2,400+ contractors certified. Start Tuesday."

DETAILS:
- Product: Online HVAC licensing course
- Price: $299 (one-time)
- Audience: Trade professionals seeking fast certification
- Key objection: "Is this as rigorous as in-person training?"
- Unique angle: Fastest state-approved program

---

Create a sales page that:
- Leads with the "60% faster" hook
- Proves legitimacy (accreditations, state approvals, pass rates)
- Includes 5 success stories (specific names, earnings increases)
- Directly answers the accreditation concern with evidence
- Features 3 CTA variations with different urgency levels
```

### Example 3: LinkedIn B2B Ad → Enterprise Sales Page
```
LinkedIn ad to sales page conversion request:

ORIGINAL AD (LinkedIn Sponsored Content):
"Enterprise teams waste $400K/year on vendor sprawl.
Our platform consolidates 12+ tools into one dashboard.
ROI calculator inside →"

CONTEXT:
- Product: SaaS vendor consolidation platform
- Price: Custom pricing (enterprise)
- Decision makers: CTOs, procurement managers
- Sales cycle: 60-90 days

---

Build a sales page with:
- Credibility markers (logos of clients, analyst reports)
- ROI calculator preview
- 4 implementation case studies ($2M+ revenue companies)
- Objection: "Switching vendors is risky and disruptive"
- Executive summary section (C-suite friendly)
- Two CTAs: "Schedule Demo" + "Download ROI Case Study"
```

---

## Capabilities

### 1. **Hook Preservation & Amplification**
The skill extracts your proven ad hook (the emotional trigger that made people click) and amplifies it across the sales page:

- **Ad hook:** "Tired of spreadsheets eating your life?"
- **Sales page expansion:** Opens with the hook, then immediately proves the pain is real with statistics, expands into story, and circles back to the hook in the CTA.

**Usage:** Provide the ad copy; the skill identifies the core emotional trigger and weaves it throughout the narrative.

---

### 2. **Benefit Stacking (Layered Persuasion)**
Rather than listing features, the skill creates a benefit stack that moves from emotional → practical → aspirational:

```
LEVEL 1 (Emotional): "Reclaim 15 hours per week and actually spend time with family"
LEVEL 2 (Practical): "Eliminate manual data entry with one-click automation"
LEVEL 3 (Business): "Reduce operational costs by up to $18,000 annually"
LEVEL 4 (Aspirational): "Build a business that doesn't require your constant attention"
LEVEL 5 (Social): "Join 2,400+ entrepreneurs who've scaled without burnout"
```

---

### 3. **Social Proof Integration**
Embeds testimonials naturally into the narrative (not as an isolated section) while requesting specific elements:

- Short-form quotes (1-2 sentences) with metrics
- Full case studies (300-400 words) with problem → solution → results structure
- Authority markers (certifications, awards, media mentions, analyst reports)
- Social proof density calculation (recommendation: 1 proof element per 250 words)

---

### 4. **Objection Handling Framework**
Addresses buyer hesitations with a logic-based format:

```
OBJECTION: "Isn't this just like other tools I've tried?"
REBUTTAL (Logic): "Our platform differs because we combine X, Y, and Z (competitors offer only one)."
PROOF: "Case study: Company Z was skeptical. Results: 6-week implementation, 340% ROI."
CTA MICRO: "See the technical differences →"
```

---

### 5. **Multiple CTA Variations**
Generates 3-5 CTAs with different urgency levels and audience segments:

- **Primary CTA** (high-urgency, specific action): "Start Free 7-Day Trial"
- **Secondary CTA** (lower-friction): "Watch 5-Minute Demo"
- **Urgency-driven CTA** (scarcity): "Join 47 Early Adopters (Offer Ends Friday)"
- **Objection-addressing CTA** (for hesitant readers): "Schedule 15-Minute Consultation"
- **Micro-CTAs** (embedded throughout): "Learn more about X feature"

---

### 6. **Narrative Arc (Story Structure)**
Applies proven storytelling frameworks:

- **Setup:** Introduce the character (your customer) and their world
- **Inciting Incident:** The problem that changed everything
- **Rising Action:** Why standard solutions fail (objection handling)
- **Climax:** The transformation your product enables
- **Resolution:** Proof through testimonials and results
- **Call to Action:** The choice to join the transformation

---

## Configuration

### Required Environment Variables
```
OPENAI_API_KEY=sk-proj-xxxxx          # GPT-4 or GPT-4o for advanced rewriting
ANTHROPIC_API_KEY=sk-ant-xxxxx        # (Optional) Claude for A/B testing variants
```

### Optional Configuration Parameters
```json
{
  "tone": "professional|conversational|energetic|authority",
  "reading_level": "high_school|college|executive",
  "page_length": "short|medium|long",
  "audience_segment": "solopreneurs|small-business|enterprise",
  "industry": "saas|ecommerce|services|education|finance",
  "social_proof_count": 3,
  "cta_variations": 4,
  "include_objections": ["cost", "implementation", "learning_curve", "security"]
}
```

### Setup Instructions

1. **Paste your ad copy** into the input field (include ad platform, audience, product details)
2. **Select parameters** (tone, length, audience, industry)
3. **Provide optional details:**
   - Target price point
   - Ideal customer profile (ICP)
   - Key differentiators vs. competitors
   - Existing testimonials (or request framework for gathering them)
   - Current objections from sales team
4. **Run conversion** → Receive full sales page in Markdown, formatted for WordPress/Elementor
5. **Edit & deploy** → Copy to your page builder, adjust brand colors/images

---

## Example Outputs

### Sample Input (Facebook Ad)
```
PLATFORM: Facebook
AD: "Stop losing deals to your competitors. 
Our proposal software closes 3x faster. 
100+ agencies trust us. Free trial →"

AUDIENCE: Agency owners, $50K-$500K revenue
PRODUCT: B2B proposal management software
PRICE: $79/month
MAIN OBJECTION: "Will my team actually use this?"
```

### Sample Output (Condensed)
```markdown
# 3X Faster Proposals. Better Margins. Real Results.

[HERO SECTION]
Every month, you're losing deals to competitors who respond faster. 
Proposals that take you 3 hours? Your competitor finishes in 60 minutes.

**The Difference? A Proposal System Built for Agencies.**

---

## The Cost of Slow Proposals

You're already competitive. Your work is great. But slow proposals lose deals to faster-moving competitors. 

Here's the math:
- Average proposal time: 3 hours
- Average deal value: $4,200
- Months losing 2-3 deals per month to slow turnaround
- **Real cost: $100K+ annually in lost revenue**

---

## How Our Clients Close 3X Faster

**1. Pre-Built Templates (60 seconds setup)**
Stop starting from scratch. We've built 47 industry-specific templates.

**2. One-Click Personalization**
Your client's name, project details, and pricing auto-populate. Send in under 2 minutes.

**3. Digital Signature + Auto-Send**
No printing. No couriers. No delays. Clients sign and return in the same conversation.

---

## Real Results From 100+ Agencies

**"We went from 5 proposals/week to 18. Our close rate jumped from 22% to 38%."**
— Marcus T., Creative Director, Chicago

**"I used to spend Friday nights writing proposals. Now I spend Friday nights with my family."**
— Sarah J., Principal, Digital Strategy Firm

---

## [Objection Section]
### "Will our team actually use this?"

Yes. Here's why:
- 94% of users are productive within Day 1 (no training required)
- Mobile app for on-the-go proposal edits
- Slack integration for instant notifications
- 15-minute onboarding call (we set it up)

Case Study: TechPro Agency (8-person team)
- Adoption rate: 100% within week 1
- Time savings per team member: 6 hours/week
- Result: 18% margin improvement

---

## Ready to Close More Deals?

**[PRIMARY CTA] Start Your Free 14-Day Trial**
No credit card. No long contract. Full access to all templates + 1 setup call.

**[SECONDARY CTA] Watch How Marcus Went From 5 to 18 Proposals/Week** (3-min video)

---
```

---

## Tips & Best Practices

### 1. **Provide Specific Ad Copy (Not "Just Convert It")**
**Good:** "Tired of spreadsheets eating your life? 87% time savings. Join 2,400 users →"
**Vague:** "Convert my ad about productivity software"

Specific ad copy helps the skill identify your proven hook and emotional trigger.

---

### 2. **Include Your Biggest Objection**
The skill will pre-emptively address it. If you know sales reps hear "Will this break our current systems?" — mention it. The conversion will feel like it was written specifically for your buyer.

---

### 3. **Provide 1-2 Real Testimonials**
If available, share actual customer quotes. The skill will:
- Expand them into case studies
- Extract key metrics for benefit stacking
- Find the emotional core and amplify it

---

### 4. **Specify Your Audience Segment**
Solopreneurs read differently than CTOs. Ecommerce audiences respond differently than B2B. Include:
- Job title
- Revenue/company size
- Main pain point (technical or emotional)

---

### 5. **Use the Generated Copy as a Template, Not Final**
The skill generates 80-90% of the work. You should:
- Add specific brand voice adjustments
- Insert your actual customer images/logos
- Update pricing or guarantees
- Test different CTA button colors

---

### 6. **A/B Test Your CTAs**
The skill generates 4-5 CTA variations. Deploy them:
- 50% of traffic → "Start Free Trial" (high-conversion)
- 30% of traffic → "Watch Demo" (lower-friction)
- 20% of traffic → "Schedule Call" (high-value)

Track which converts best. CTA wording alone can move conversion rates by 15-30%.

---

### 7. **Customize Length Based on Sales Cycle**
- **Short cycle (ecommerce, $50 products):** 800-1,200 words
- **Medium cycle (SaaS, $79-$500/month):** 1,500-2,200 words
- **Long cycle (enterprise, $10K+):** 2,500-3,500 words (allow for deeper case studies)

---

### 8. **Update Social Proof Quarterly**
Generated pages reference "100+ customers" or "2,400 users." Replace with current numbers. Outdated social proof reduces trust.

---

## Safety & Guardrails

### What This Skill Will NOT Do

- **❌ Make false claims:** The skill will not fabricate testimonials, fake case study metrics, or unverified statistics. If you provide proof, it uses it; if you don't, it requests it.
  
- **❌ Violate FTC disclosure rules:** Generated copy includes clear space for required disclaimers (affiliate relationships, sponsored content, etc.). You must add these before publishing.

- **❌ Create manipulative dark patterns:** The skill avoids:
  - Countdown timers that are fake (unless genuinely limited)
  - Fake scarcity ("Only 3 spots left!" if untrue)
  - High-pressure urgency tactics for low-value products
  - Misleading guarantees

- **❌ Promise unsubstantiated results:** If your ad says "87% time savings," the sales page will expand on *how* (specific features that enable this), not inflate to "92%". It cites the original claim.

- **❌ Copy competitor language exactly:** The skill rewrites and adapts competitor angles but does not plagiarize. Unique value propositions are created fresh.

- **❌ Replace human judgment:** This is a *tool*, not a decision-maker. You decide:
  - What claims are true
  - What objections are valid
  - What CTAs align with your business model
  - Whether generated copy matches your brand voice

### Limitations

- **Requires ad copy input:** The skill cannot generate sales pages from scratch. It needs a proven ad as the starting point.
  
- **Social proof must be real:** If you request 5 testimonials but only have 2, the skill will flag this and request you provide more (or it will generate a framework for gathering them).

- **Industry-specific complexity:** Highly regulated industries (healthcare, finance, law) require additional compliance review. Generated copy is marketing-ready but not legal-reviewed.

- **Cultural adaptation:** The skill assumes Western (primarily US) buyer psychology. For international audiences, manual cultural adjustment is recommended.

---

## Troubleshooting

### "The output feels generic"
**Problem:** You provided minimal