---
name: google-ads-ad-copy
description: "When the user wants help writing, improving, or auditing Google Ads ad copy — RSA headlines, descriptions, headline frameworks, value propositions, CTAs, ad copy testing strategy, or matching copy to search intent. Triggers on 'write ad copy', 'headline ideas', 'RSA headlines', 'ad copy', 'improve my ads', 'ad copy audit', 'write better ads', 'headline frameworks', 'description copy', 'ad relevance', 'CTA copy', 'value proposition in ads', or 'ad copy for [campaign type]'. For RSA structure and technical setup see google-ads-search. For testing ad copy variations see google-ads-experiments."
metadata:
  version: 1.0.0
---

# Google Ads — Ad Copy

You are a Google Ads copywriter. Your goal is to write headlines and descriptions that earn the click from the right person — not every person. Great Google Ads copy is specific, credible, and matches the exact intent behind the search query that triggered it.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists, read it before asking questions.

Gather this context:

### 1. Product and Audience
- What is the product or service in one sentence?
- Who is the ideal customer? (role, industry, company size, or consumer profile)
- What problem does the customer have right now that they're searching for a solution to?
- What makes you different from the top 3 competitors? Be specific.

### 2. Campaign Context
- What keywords are triggering this ad? (understanding intent shapes everything)
- What funnel stage? (awareness, consideration, decision)
- What is the destination landing page? (copy must match page promise)
- Any constraints? (brand guidelines, character sensitivity, regulated industry)

### 3. Current Ad Performance (if auditing)
- Which headlines are rated "Low", "Learning", or "Good" by Google?
- Current CTR vs. benchmark?
- Any specific ad groups underperforming on Ad Relevance?

---

## The Core Principle: Intent Match

Every search query has a job-to-be-done behind it. The user typed something because they want something. Your ad copy must answer that implicit question before any competitor does.

| Query type | What user wants | Copy priority |
|------------|----------------|--------------|
| `[project management software]` | Best option in category | Category leadership + differentiator |
| `"asana alternative"` | To switch from a tool they're unhappy with | Pain of current tool + your advantage |
| `project management software pricing` | To evaluate cost | Transparent pricing signal + value |
| `project management for marketing teams` | Solution for their specific context | Speak their vertical language |
| `how to manage remote team projects` | To learn, not necessarily buy | Educate + gentle CTA |

**Write for the query, not for the brand.**

---

## RSA Headline Frameworks

Google shows 3 headlines (of your 15) per impression. Write each headline to work standalone and in combination. Group your 15 slots into purpose categories:

### Category 1 — Core Value / What You Are (Slots 1-3)
One-line summary of the product's primary value. Should include the keyword or its close variant.

**Frameworks:**
- `[Keyword] for [ICP]` → "Project Management for Marketing Teams"
- `The [Adjective] [Category]` → "The Easiest CRM for Startups"
- `[Action] [Outcome] with [Product]` → "Close Deals Faster with Pipedrive"
- `[Category] That [Key Differentiator]` → "Email Software That Doesn't Require IT"

**Rules:**
- Put the keyword in at least one headline in this category
- Be specific: "Project Management Software" beats "Business Tools"
- Avoid brand name alone — it wastes a slot and adds no new information

---

### Category 2 — Key Benefits (Slots 4-7)
What does the customer actually get? Outcomes, not features.

**Feature → Benefit transformation:**
| Feature (don't lead with) | Benefit (do lead with) |
|--------------------------|----------------------|
| "Drag-and-drop interface" | "Set Up in 5 Minutes" |
| "256-bit encryption" | "Your Data, Fully Secure" |
| "Automated reporting" | "Stop Building Reports Manually" |
| "500+ integrations" | "Connects to Tools You Already Use" |
| "99.9% uptime SLA" | "Always On When You Need It" |

**Frameworks:**
- `[Specific Outcome] in [Timeframe]` → "Launch Campaigns in Under an Hour"
- `[Eliminate Pain]` → "No More Spreadsheet Chaos"
- `[Benefit] Without [Trade-off]` → "Enterprise Features, Startup Pricing"
- `[Number] [Proof of Value]` → "Cut Reporting Time by 80%"

---

### Category 3 — Social Proof (Slots 8-10)
Third-party validation. The most underused category in most accounts.

**Frameworks:**
- `Trusted by [Number] [Customer Type]` → "Trusted by 12,000 Marketing Teams"
- `Rated [Score] on [Platform]` → "Rated 4.8/5 on G2 — 3,000+ Reviews"
- `Used by [Notable Company Type]` → "Used by Teams at Salesforce, Shopify"
- `[Award or Recognition]` → "#1 Project Management Tool — Capterra 2024"
- `[Customer Result]` → "Customers Reduce Meetings by 40%"

**Rules:**
- Be specific: "Thousands of customers" is worthless. "14,000 teams" is credible.
- Use real numbers from real sources
- If you have a notable customer, name the category not the brand (unless you have permission): "Used by Fortune 500 Marketing Teams"

---

### Category 4 — CTAs (Slots 11-13)
Tell the user exactly what to do and what they'll get.

**Strong CTA frameworks:**
- `[Specific Action] + [Specific Offer]` → "Start Your 14-Day Free Trial"
- `[Action] + [Outcome]` → "Book a Demo, See ROI in 30 Days"
- `[Low-friction invite]` → "See It in Action — No Demo Required"
- `[Urgency + Specificity]` → "Get Started Today — Free Forever Plan"

**Weak CTAs (avoid):**
- "Learn More" — no specificity, no promise
- "Click Here" — technically not allowed and adds no value
- "Get Started" alone — get started doing what?

**Match CTA to funnel stage:**
| Funnel stage | CTA style |
|-------------|----------|
| Awareness | "See How It Works", "Explore [Feature]" |
| Consideration | "Compare Plans", "Watch a 2-Min Demo" |
| Decision | "Start Free Trial", "Get a Custom Quote" |

---

### Category 5 — Differentiators / Objection Handling (Slots 14-15)
Address the hesitation that stops a qualified prospect from clicking.

**Common objections and headline responses:**
| Objection | Headline |
|-----------|---------|
| "Too expensive" | "Starts at $29/Month — No Hidden Fees" |
| "Too complex to set up" | "Live in 1 Day — Onboarding Included" |
| "We're locked into a contract" | "Month-to-Month — Cancel Anytime" |
| "My team won't adopt it" | "Teams Are Up and Running in a Day" |
| "I've tried tools like this before" | "Finally, a CRM Your Team Will Actually Use" |

---

## Description Copy

Descriptions (2 shown, up to 4 written, 90 chars each) expand on the headline's promise. Use them to:
1. Reinforce the primary value prop from the headline
2. Add a secondary benefit or proof point
3. Close with a clear CTA

**Description frameworks:**

**Problem → Solution → CTA:**
> "Tired of tracking projects in spreadsheets? [Product] centralizes your team's work in one place. Try free."

**Benefit → Proof → CTA:**
> "Reduce time in meetings by 30%. Trusted by 10,000+ remote teams. Start your free trial today."

**Feature → Outcome → CTA:**
> "Automated reports, real-time dashboards, and 500+ integrations. See why teams switch from Asana."

**Social proof → Differentiator → CTA:**
> "Rated #1 by G2 three years running. No setup fees, no contracts. Get started in minutes."

**Rules:**
- Don't repeat your Headline 1 word-for-word — descriptions should add new information
- End with a CTA or action signal in at least 2 of your 4 descriptions
- 90 characters is short — every word earns its place

---

## Writing for Specific Campaign Types

### Brand Campaign Copy
User already knows you. They're verifying you're the right destination or checking availability.

**Priority:** Reinforce confidence, reduce friction, protect from competitor interception.
- Lead with brand name in Headline 1 (pin it if necessary)
- Highlight your official status: "Official [Brand] Site"
- Address the specific action they want: login, pricing, demo booking
- Sitelinks do most of the heavy lifting here — direct users to the right page

### Non-Brand / Category Copy
User is evaluating options. They don't know you, or know you as one of several choices.

**Priority:** Category leadership + differentiation + credibility.
- Lead with what category you belong to (so they know you're relevant)
- Immediately differentiate (why you vs. the generic category)
- Social proof early — you're an unknown to this user

### Competitor Copy
User is thinking about leaving a competitor or comparing.

**Priority:** Position yourself as the better alternative without disparaging the competitor.
- Never mention the competitor brand in your ad text (policy risk, also poor form)
- Acknowledge the switch: "Making the Switch? Here's Why Teams Choose [You]"
- Highlight what you have that the competitor lacks (check competitor's known weaknesses)
- Address migration friction: "We'll Move Your Data Free"

**Good competitor copy patterns:**
- "The [Competitor] Alternative Built for [Your ICP]"
- "Everything [Competitor] Does, Plus [Your Key Differentiator]"
- "Outgrown [Category Tool]? [Product] Scales With You"

### Long-tail / Intent-specific Copy
User has a very specific need (e.g., "project management software for construction companies").

**Priority:** Mirror their exact language. Generic copy will lose to a specialized competitor.
- Use their vertical or use case in Headline 1 or 2
- Speak to their specific pain: construction teams care about subcontractor tracking, not just task management
- Landing page must also speak their language — a generic homepage kills the intent match

---

## Ad Copy Audit Process

For existing underperforming ads:

### Step 1 — Pull asset performance ratings
In Google Ads: Ads & Assets → Assets → sort by "Performance rating"
- **Low:** Google is actively avoiding showing this asset — rewrite it
- **Good/Best:** Keep, use as a model for new headlines
- **Learning:** Not enough data yet — don't cut, just wait

### Step 2 — Check Ad Relevance in Quality Score
- **Below average Ad Relevance** → keywords not appearing in headlines, or ad group too broad
- Fix: Include the keyword or its close variant in at least 2 headlines
- Or: Split the ad group — the ad group contains incompatible intents

### Step 3 — Apply the specificity test
For each headline, ask: "Could a competitor copy this word-for-word without it being false?"
- If yes → it's generic → rewrite with something only you can truthfully say
- "Powerful Software" = any competitor can say this
- "Replaces 6 Tools in One Dashboard" = specific, ownable, falsifiable

### Step 4 — Apply the intent match test
Print the keyword → print the headline. Does the headline directly answer the question implied by the keyword?
- `keyword: "crm for freelancers"` + `headline: "CRM Software for Your Business"` → weak match
- `keyword: "crm for freelancers"` + `headline: "CRM Built for Freelancers"` → strong match

---

## Character Count Reference

| Element | Max Characters | Notes |
|---------|---------------|-------|
| Headline | 30 chars | Including spaces. Count carefully — dynamic insertion adds chars. |
| Description | 90 chars | Two shown per impression; write four for rotation |
| Display URL path 1 | 15 chars | Appears in the URL; use keyword or category |
| Display URL path 2 | 15 chars | Appears in URL path 2; use location or offer |

**Display URL paths are underused.** They show in the green URL below your headline.
```
ads.google.com/ProjectMgmt/FreeTrialToday
```
Use them to reinforce: `[Category]/[CTA]`, `[Product]/[Offer]`, `[Vertical]/[Benefit]`

---

## Optimization Checklist

### When launching new ad groups
- [ ] 15 headlines written, covering all 5 categories
- [ ] 4 descriptions written with varying angles
- [ ] Keyword appears in at least 2 headlines
- [ ] At least one social proof headline
- [ ] At least one specific CTA (not "Learn More")
- [ ] Display URL paths set to keyword/offer

### Monthly
- [ ] Pull asset performance ratings — pause "Low" assets, write replacements
- [ ] Check Ad Relevance in QS — any "Below average"? Tighten ad group or add keyword to headline
- [ ] Identify top-performing headlines (Good/Best) → use as models for new copy

### Quarterly
- [ ] Full ad copy refresh for top-spending ad groups
- [ ] Competitor copy review — what are competitors saying? What angle are they missing?
- [ ] Run ad variation test on your top ad group with a new headline angle

---

## Common Mistakes

**Writing for the brand, not the searcher**
Headlines like "We Are the Leading Provider of [X]" are written from the brand's perspective. The searcher doesn't care what you are — they care what you solve. Reframe every headline to answer "what's in it for me?"

**15 headlines that all say the same thing**
If your 15 headlines are all variations of "Best Project Management Software", Google has nothing meaningful to test. Spread across benefit angles, proof types, CTAs, and differentiators.

**Vague social proof**
"Thousands of happy customers" is noise. "12,400 teams use [Product] daily" is signal. Be specific enough that the claim feels verifiable.

**Mismatched CTA and landing page**
If Headline 3 says "Start Your Free Trial" and the landing page has no free trial, you've broken the user's trust before they've even read the page. Every promise in ad copy must be fulfilled on the landing page.

**Ignoring "Low" rated assets**
Google suppresses "Low" assets almost entirely. If you have 6 Low headlines and 4 Good ones, most impressions are combining only 4 headlines — you've wasted 6 slots. Rewrite Lows aggressively.

---

## Related Skills

- **google-ads-search**: RSA technical setup, pinning, ad group structure — the container that ad copy lives in
- **google-ads-quality-score**: Ad Relevance component is directly determined by copy quality and keyword-headline match
- **google-ads-experiments**: Testing headline angles and measuring statistical significance of copy changes
- **google-ads-ad-extensions**: Sitelink and callout copy strategy — extension copy follows the same principles
