---
name: vendor-evaluation
description: "Creates structured vendor and tool comparison matrices with weighted scoring, cost analysis, and recommendation summaries for making informed purchasing decisions. Use when a user needs to choose between software tools, service providers, or vendors and wants a systematic evaluation rather than a gut decision."
allowed-tools: Read Write Glob mcp__claude_ai_Notion__notion-create-database mcp__claude_ai_Notion__notion-create-pages mcp__claude_ai_Notion__notion-search
metadata:
  author: Salah-XD
  version: "1.0"
---

# Vendor Evaluation

## When to Use This Skill

Use this skill when the user needs to:
- Choose between 2-5 software tools, SaaS platforms, or digital products
- Compare service providers, agencies, contractors, or freelancers for a specific engagement
- Evaluate physical vendors or suppliers for their business operations
- Make a purchasing decision that involves multiple criteria beyond just price
- Present a structured recommendation to a business partner, co-founder, or team before committing

**DO NOT** use this skill for:
- Competitive analysis of the user's own market (use competitor-analysis)
- General product research with no purchasing intent
- Comparing internal team members or employees
- Single-vendor pricing negotiation (the decision is already made)
- Evaluating investment opportunities or financial instruments

---

## Core Principle

A VENDOR EVALUATION IS ONLY VALUABLE WHEN IT PRODUCES A CLEAR RECOMMENDATION WITH VISIBLE MATH — NEVER PRESENT A COMPARISON WITHOUT WEIGHTED SCORES AND A TOTAL COST OF OWNERSHIP CALCULATION.

---

## Evaluation Types

Every evaluation falls into one of these categories, which determines the default criteria:

| Type | Examples | Default Criteria Focus |
|------|----------|----------------------|
| **Software/SaaS** | Email tools, CRMs, project management, design tools | Features, pricing tiers, integrations, ease of use, scalability |
| **Agency/Service Provider** | Marketing agencies, dev shops, design studios | Portfolio quality, communication, pricing model, turnaround, specialization |
| **Contractor/Freelancer** | Designers, writers, developers, VAs | Relevant experience, rate, availability, communication, portfolio |
| **Physical Vendor/Supplier** | Print shops, fulfillment centers, equipment vendors | Unit cost, quality, lead time, minimum order, reliability |

---

## Step 1: Understand

Gather these inputs before building any comparison. Ask all questions at once to minimize back-and-forth.

1. **What are you buying?** — software, service, contractor, or physical product/supply
2. **What problem does this solve?** — the specific pain or need driving the purchase
3. **Budget range** — monthly or total budget, even approximate ("under $100/mo" or "$5K-$10K total")
4. **Must-have requirements** — dealbreakers that eliminate a vendor immediately (e.g., "must integrate with Shopify," "must offer Spanish-language support")
5. **Nice-to-have features** — important but not dealbreakers
6. **Candidates** — the 2-5 vendors or tools being considered, by name
7. **Current solution** — what they use now, if anything (and why it falls short)
8. **Team size** — how many people will use this tool or work with this vendor
9. **Decision timeline** — when they need to decide (this week, this month, no rush)

**If the user provides items 1, 6, and at least one must-have requirement, proceed with reasonable defaults for the rest.** Ask only about missing critical details.

**Brief template to present if the user gives a vague request:**

```
I will build a structured vendor evaluation for you. Quick answers needed:

1. What are you buying? (software, service provider, contractor, supplier)
2. What problem are you solving?
3. Budget range? (even approximate helps)
4. Dealbreaker requirements? (things a vendor MUST have or they are out)
5. Which vendors are you comparing? (2-5 names)
6. What do you use now, and why is it not working?
7. How many people will use this?
```

**GATE: Do not proceed to Step 2 until you have: the evaluation type, at least 2 named candidates, and at least 1 must-have requirement. If the user cannot name candidates, suggest 3-4 well-known options in the category and ask them to confirm.**

---

## Step 2: Evaluate

Build three analysis components. Complete all three before presenting anything to the user.

### 2A: Weighted Scoring Matrix

Select 5-7 criteria from the table below based on the evaluation type and user priorities. **Do not use more than 7 criteria — analysis paralysis makes the evaluation unusable.**

**Criteria Reference:**

| Criterion | Applies To | What to Score |
|-----------|-----------|---------------|
| **Core Features** | All types | Does it solve the stated problem? Coverage of must-haves and nice-to-haves |
| **Pricing/Cost** | All types | Affordability relative to budget and value delivered |
| **Ease of Use** | Software, Services | Setup time, learning curve, day-to-day usability |
| **Support Quality** | Software, Services | Response time, channels available, documentation quality |
| **Scalability** | Software, Suppliers | Can it grow with the business? Pricing at 2x and 5x current usage |
| **Integration** | Software | Connects with existing tools (CRM, email, Shopify, Zapier, etc.) |
| **Reputation/Track Record** | All types | Reviews, testimonials, years in business, client references |

**Weighting rules:**
- Assign each criterion a weight from 1 (low priority) to 5 (critical priority)
- Must-have requirements always get weight 5
- The user's stated top priority gets weight 5
- Remaining criteria distribute across 2-4 based on relevance
- **NEVER weight all criteria equally — that defeats the purpose of weighting**

**Scoring rules:**
- Score each vendor 1-5 on each criterion
- 1 = poor/missing, 2 = below average, 3 = adequate, 4 = good, 5 = excellent
- Calculate weighted score per criterion: score x weight
- Sum weighted scores for each vendor to get the total

**Matrix format:**

```
| Criterion | Weight | ConvertKit | Mailchimp | Beehiiv |
|-----------|--------|------------|-----------|---------|
| Core Features | 5 | 4 (20) | 5 (25) | 4 (20) |
| Pricing | 4 | 4 (16) | 2 (8) | 5 (20) |
| Ease of Use | 4 | 5 (20) | 3 (12) | 4 (16) |
| Support | 3 | 4 (12) | 3 (9) | 3 (9) |
| Scalability | 3 | 3 (9) | 5 (15) | 4 (12) |
| Integration | 4 | 4 (16) | 5 (20) | 3 (12) |
| Reputation | 2 | 4 (8) | 5 (10) | 3 (6) |
| **TOTAL** | **25** | **101** | **99** | **95** |
```

### 2B: Cost Analysis

Build a cost comparison that goes beyond the sticker price. Calculate for both 1-year and 3-year horizons.

**Cost components to capture:**

| Component | Description | Example |
|-----------|-------------|---------|
| **Base cost** | Monthly or annual subscription / project fee / unit cost | $29/mo |
| **Per-user cost** | Additional cost per seat or team member | $10/user/mo |
| **Onboarding cost** | Setup fees, migration, training time valued at the user's hourly rate | $500 one-time |
| **Add-on costs** | Features that cost extra beyond the base plan | Premium support: $50/mo |
| **Migration cost** | Cost to switch from the current solution (data export, re-setup, downtime) | 8 hours at $75/hr = $600 |
| **Scaling cost** | What the price becomes at 2x current usage | $29/mo becomes $79/mo at 10K contacts |

**Cost table format:**

```
| Cost Component | ConvertKit | Mailchimp | Beehiiv |
|----------------|------------|-----------|---------|
| Base (monthly) | $29 | $20 | $0 (free tier) |
| Per-user add-on | $0 | $0 | $0 |
| Onboarding | $0 | $0 | $0 |
| Add-ons needed | $0 | Landing pages: $20/mo | Custom domain: $0 |
| Migration estimate | 4 hrs ($300) | 4 hrs ($300) | 4 hrs ($300) |
| **Year 1 total** | **$648** | **$780** | **$300** |
| **Year 3 total** | **$1,344** | **$1,740** | **$300** |
| At 2x scale (monthly) | $49 | $60 | $42 |
```

**If exact pricing is unavailable** (common for agencies and freelancers): use the user's budget range or known quotes. Mark estimates clearly with "(est.)" and note which figures are confirmed versus projected.

### 2C: Pros/Cons and Risk Assessment

For each vendor, produce:

**Pros/Cons** — 3-4 bullets each, specific to the user's situation (not generic marketing copy):

```
## ConvertKit

**Pros:**
- Creator-focused interface requires no technical skills to set up automations
- Free migration service moves your existing subscribers at no cost
- Visual automation builder makes complex sequences easy to understand

**Cons:**
- Limited landing page templates compared to Mailchimp
- No built-in ad network or monetization tools
- Reporting dashboard lacks granular click-map data
```

**Risk Assessment** per vendor:

| Risk Factor | What to Evaluate |
|-------------|-----------------|
| **Vendor stability** | How long have they been in business? Funded or profitable? Any acquisition rumors? |
| **Lock-in concern** | How hard is it to leave? Can you export your data? Are there proprietary formats? |
| **Migration difficulty** | LOW (export/import in hours), MEDIUM (requires manual re-setup of automations/settings), HIGH (significant data loss or rebuild required) |

---

## Step 3: Present

Deliver the evaluation in this exact order. Present everything before saving anything.

### Presentation Order

**1. Evaluation Summary** — one paragraph stating the candidates, the evaluation type, and the user's top priorities.

**2. Weighted Scoring Matrix** — full table with scores, weighted scores in parentheses, and totals.

**3. Cost Comparison Table** — all cost components, Year 1 total, Year 3 total, and at-scale pricing.

**4. Vendor Profiles** — pros/cons and risk assessment for each vendor.

**5. Recommendation:**

```
## Recommendation

### Top Pick: ConvertKit
**Weighted Score: 101/125 | Year 1 Cost: $648**

ConvertKit wins on the criteria that matter most to you: ease of use (scored 5)
and creator-focused features (scored 4) with the best balance of capability and
price. The free migration service eliminates switching cost, and the visual
automation builder means you will not need technical help to build sequences.

### Runner-Up: Mailchimp
**Weighted Score: 99/125 | Year 1 Cost: $780**

Mailchimp scores highest on raw features and integration breadth, but its
complexity works against you as a solo operator. It is the right choice if you
plan to hire a marketing team within the next 12 months and need enterprise-grade
automation. Otherwise, the learning curve costs more than the subscription saves.

### Not Recommended for Your Situation: Beehiiv
**Weighted Score: 95/125 | Year 1 Cost: $300**

Beehiiv is the cheapest option but scored lowest on integrations and support.
It excels for newsletter-first creators but lacks the email automation depth
you listed as a must-have. Consider Beehiiv if your needs simplify in the future.
```

**6. Suggested Next Steps:**

```
## Suggested Next Steps

1. Sign up for ConvertKit's free plan (up to 1,000 subscribers) to test the
   automation builder with your existing sequences before committing to paid
2. Run a 14-day pilot: migrate 500 subscribers and send 2-3 campaigns to
   validate deliverability and workflow
3. If the pilot succeeds, migrate fully and cancel your current tool by [date]
4. Re-evaluate in 12 months — your needs at 10K subscribers may differ from today
```

**GATE: Present the full evaluation and ask the user to review before saving. Offer to adjust any scores, weights, or the recommendation.**

---

## Step 4: Act

Save the evaluation based on the user's preference.

### Option A: Save to Notion Database

1. **Search for existing context** — call `notion-search` to check if the user has a vendor, tools, or operations page already. If found, confirm where to place the new database.

2. **Create the database** — call `notion-create-database` with these properties:

   | Property | Type | Purpose |
   |----------|------|---------|
   | **Vendor** | Title | Vendor or tool name |
   | **Type** | Select | Software/SaaS, Agency, Contractor, Supplier |
   | **Weighted Score** | Number | Total weighted score from the matrix |
   | **Year 1 Cost** | Number | Total cost of ownership for year one |
   | **Year 3 Cost** | Number | Total cost of ownership for three years |
   | **Recommendation** | Select | Top Pick, Runner-Up, Not Recommended |
   | **Key Strengths** | Rich text | Top 2-3 pros |
   | **Key Weaknesses** | Rich text | Top 2-3 cons |
   | **Lock-In Risk** | Select | LOW, MEDIUM, HIGH |
   | **Must-Have Coverage** | Rich text | Which must-have requirements this vendor meets |
   | **Notes** | Rich text | Additional context, trial details, decision rationale |
   | **Last Evaluated** | Date | Date of this evaluation |

   Database title: `Vendor Evaluation — [Category]` (e.g., "Vendor Evaluation — Email Marketing Tools")

3. **Populate entries** — call `notion-create-pages` to add each vendor as a row with all fields filled from the evaluation.

4. **Confirm:**

```
Notion database created: "Vendor Evaluation — Email Marketing Tools"

  3 entries: ConvertKit, Mailchimp, Beehiiv
  Properties: Type, Weighted Score, Year 1 Cost, Year 3 Cost, Recommendation,
  Strengths, Weaknesses, Lock-In Risk, Must-Have Coverage, Notes, Last Evaluated
  All entries dated to today

  Notion link: [database URL]

  This database serves as your decision record. Update it if pricing changes
  or new vendors enter your consideration set.
```

### Option B: Save as Markdown File

If the user prefers a local file or does not have Notion connected:

1. Write the full evaluation to a markdown file at the user's preferred path
2. Default filename: `vendor-evaluation-[category].md`
3. Include all sections: scoring matrix, cost analysis, vendor profiles, recommendation, next steps

### Decision Summary for Stakeholders

If the user needs to share the decision with a partner, co-founder, or team, generate a concise summary following this format:

```
## Decision Summary: [Category]

**Decision:** [Action + chosen vendor]
**Evaluated:** [All candidates] | **Date:** [Today]
**Why [Winner]:** [3-4 bullet points citing scores and costs]
**Key tradeoff:** [One sentence on what was sacrificed]
**Next step:** [Pilot details with date]
```

### Suggest Trial/Pilot Approach

Regardless of save format, close with a structured pilot: sign up for the top pick's free tier or trial, test 2-3 critical workflows, migrate a small data subset, set a 14-day decision deadline, and fall back to the runner-up if any must-have fails during the pilot.

---

## Example 1: Solo Creator Choosing an Email Marketing Platform

**User says:** "I need to pick an email marketing tool. I am choosing between ConvertKit, Mailchimp, and Beehiiv. I have 3,000 subscribers, I am a solo content creator, and my budget is under $50/month. I need good automation and it has to integrate with Shopify."

**Step 1 — Understand:**
- Buying: Software/SaaS (email marketing)
- Problem: Needs an email platform that handles automation and connects to Shopify
- Budget: Under $50/month
- Must-haves: Email automation, Shopify integration
- Nice-to-haves: Landing pages, analytics, free migration
- Candidates: ConvertKit, Mailchimp, Beehiiv
- Current solution: Not specified
- Team size: 1 (solo creator)
- Timeline: Not specified (default: within 2 weeks)

**Step 2 — Evaluate:**

Weighted Scoring Matrix:

| Criterion | Weight | ConvertKit | Mailchimp | Beehiiv |
|-----------|--------|------------|-----------|---------|
| Core Features | 5 | 4 (20) | 5 (25) | 3 (15) |
| Pricing | 4 | 4 (16) | 2 (8) | 5 (20) |
| Ease of Use | 4 | 5 (20) | 3 (12) | 4 (16) |
| Automation | 5 | 4 (20) | 5 (25) | 2 (10) |
| Shopify Integration | 5 | 4 (20) | 5 (25) | 2 (10) |
| Support | 2 | 4 (8) | 3 (6) | 3 (6) |
| **TOTAL** | **25** | **104** | **101** | **77** |

Cost Analysis:

| Cost Component | ConvertKit | Mailchimp | Beehiiv |
|----------------|------------|-----------|---------|
| Base (monthly) | $29 (3K subs) | $20 (Standard plan) | $0 (free tier) |
| Add-ons needed | $0 | Landing pages: $20/mo | Newsletter only, no automations |
| Migration effort | 3 hrs ($225 est.) | 3 hrs ($225 est.) | 3 hrs ($225 est.) |
| **Year 1 total** | **$573** | **$705** | **$225** |
| **Year 3 total** | **$1,269** | **$1,665** | **$225** |
| At 10K subs (monthly) | $79 | $100 | $42 |

Recommendation:
- **Top Pick: ConvertKit** — highest weighted score (104), best balance of automation depth and usability for a solo creator. Shopify integration is native and well-documented. Year 1 cost of $573 is within budget.
- **Runner-Up: Mailchimp** — strongest raw feature set and deepest Shopify integration, but the interface complexity and higher scaled pricing work against a solo operator.
- **Not Recommended: Beehiiv** — cheapest option but scored 2/5 on both automation and Shopify integration, which are the user's must-haves. Beehiiv excels at newsletters but is not built for e-commerce email automation.

**Step 4 — Act:** User chose markdown. Full evaluation saved to `vendor-evaluation-email-marketing.md`. Pilot recommendation: sign up for ConvertKit free plan, migrate 500 subscribers, test 2 automation sequences and the Shopify integration over 14 days.

---

## Example 2: Agency Owner Evaluating Freelance Designers for a Rebrand

**User says:** "I need to hire a freelance designer for a client rebrand. I have two candidates: Sarah Chen (portfolio at sarahchendesign.com, quoted $4,500) and Marcus Rivera (portfolio at marcusrivera.co, quoted $3,200). The rebrand includes a new logo, brand guidelines, and social media templates. Budget is $3K-$5K."

**Step 1 — Understand:**
- Buying: Contractor/Freelancer (brand designer)
- Problem: Needs a reliable designer for a client rebrand project
- Budget: $3,000-$5,000
- Must-haves: Logo design experience, ability to produce brand guidelines document
- Nice-to-haves: Social media template experience, fast turnaround, revisions included
- Candidates: Sarah Chen ($4,500), Marcus Rivera ($3,200)
- Current solution: No existing designer relationship
- Team size: 1 (agency owner managing the project)
- Timeline: Need to start within 2 weeks

**Step 2 — Evaluate:**

Weighted Scoring Matrix:

| Criterion | Weight | Sarah Chen | Marcus Rivera |
|-----------|--------|------------|---------------|
| Portfolio Quality | 5 | 5 (25) | 4 (20) |
| Brand Guidelines Experience | 5 | 5 (25) | 3 (15) |
| Pricing | 4 | 3 (12) | 4 (16) |
| Communication | 3 | 4 (12) | 4 (12) |
| Turnaround Time | 3 | 3 (9) | 4 (12) |
| Revisions Included | 3 | 3 rounds (12) | 2 rounds (9) |
| **TOTAL** | **23** | **95** | **84** |

Cost Analysis:

| Cost Component | Sarah Chen | Marcus Rivera |
|----------------|------------|---------------|
| Project quote | $4,500 | $3,200 |
| Revisions included | 3 rounds | 2 rounds |
| Extra revision cost | $200/round | $150/round |
| Social templates (if separate) | Included | $500 add-on |
| **Total with templates** | **$4,500** | **$3,700** |
| Risk-adjusted total (1 extra revision) | $4,500 | $3,850 |

Recommendation:
- **Top Pick: Sarah Chen** — weighted score of 95 vs. 84. Her portfolio shows 6 complete rebrands with brand guideline documents, which is the most critical deliverable. The $4,500 quote includes social templates and 3 revision rounds. Higher upfront cost but lower risk of scope creep or add-on charges.
- **Runner-Up: Marcus Rivera** — strong visual style and faster turnaround, but only 1 brand guideline in his portfolio. Social templates are an add-on ($500), bringing effective cost to $3,700 with fewer revisions. Better choice if the budget is firm at $3,200 and the user can provide more art direction on the guidelines.

**Step 4 — Act:** User chose Notion. Database created with 2 entries. Decision summary generated for sharing with the client stakeholder. Pilot recommendation: commission a single logo concept from each designer ($500-$800 test project) before committing to the full rebrand if budget allows.

---

## Anti-Patterns

- **DO NOT recommend a vendor without showing the scoring math.** The user must see how you arrived at the recommendation. A recommendation without visible criteria and scores is just an opinion.
- **DO NOT weight all criteria equally.** Equal weights (all 3s or all 5s) eliminate the purpose of a weighted evaluation. If everything matters equally, nothing matters most — push the user to prioritize.
- **DO NOT ignore total cost of ownership.** The cheapest monthly subscription is not always the cheapest solution. Onboarding time, migration effort, add-on costs, and scaling costs change the math.
- **DO NOT present more than 7 evaluation criteria.** Beyond 7, the matrix becomes noise. If the user insists on 10 criteria, combine related items (e.g., merge "email support" and "chat support" into "Support Quality").
- **DO NOT fabricate pricing, feature availability, or review scores.** If you do not have accurate data for a vendor, say so and score conservatively. Mark uncertain data with "(est.)" or "(unverified)."
- **DO NOT skip the runner-up recommendation.** The top pick might fail during the pilot. The user needs a fallback they can switch to without re-running the entire evaluation.
- **DO NOT present the recommendation before the scoring matrix and cost analysis.** The user must see the data before the conclusion. Recommendation first invites bias.
- **DO NOT evaluate vendors the user did not ask about.** Adding unsolicited options creates scope creep and delays the decision. If you think they are missing a strong candidate, mention it as a note after the evaluation, not as a scored entry.
- **DO NOT save to Notion before the user reviews and approves the evaluation.** Always present first, save second.

---

## Recovery and Troubleshooting

### User Names Only 1 Candidate

1. Ask: "A vendor evaluation works best with at least 2 options to compare. Who else are you considering, or would you like me to suggest 2-3 alternatives in this category?"
2. Suggest 2-3 well-known options based on the evaluation type and budget range
3. If the user truly wants to evaluate just 1 vendor: reframe as a vendor audit instead of a comparison. Score the single vendor against the criteria and provide a "go/no-go" recommendation with a threshold score (e.g., "vendors scoring below 70% of maximum weighted score are not recommended").

### Pricing Information Is Unavailable

1. Check the vendor's public pricing page for published rates
2. If pricing is hidden behind "Contact Sales" or "Get a Quote": mark the cost as "Quote required" and assign a score of 3 (neutral) on the pricing criterion
3. If the user has received quotes, use those exact figures
4. **Do not fabricate pricing.** State what you know and what you do not. A cost analysis with honest gaps is more useful than one with invented numbers.
5. If no pricing data exists for any vendor, skip the cost analysis table and note: "Cost comparison omitted — pricing requires direct quotes from each vendor. I recommend requesting quotes before finalizing the decision."

### Must-Have Requirement Eliminates a Candidate

1. Score the eliminated vendor normally on all other criteria but assign a score of 0 on the must-have criterion
2. Mark the vendor clearly in the matrix: "Beehiiv: 0 (MISSING: no Shopify integration)"
3. Include the vendor in the final presentation but note: "Beehiiv is disqualified from consideration because it does not meet the must-have requirement for Shopify integration. It is included in the matrix for reference."
4. If all candidates except one are eliminated: inform the user that only one option meets their requirements and ask if they want to relax any must-haves or add more candidates.

### Scores Are Too Close to Call

If two vendors are within 5 points of each other on the weighted total:
1. Flag the tie explicitly: "ConvertKit (101) and Mailchimp (99) are within the margin of uncertainty. The difference is not meaningful."
2. Break the tie with cost analysis: the vendor with the lower total cost of ownership wins the tiebreak
3. If cost is also similar: break on the highest-weight criterion. Whoever scores higher on the user's top priority wins.
4. If still tied: recommend both for a head-to-head pilot. "Run a 1-week trial of each and decide based on hands-on experience."

### Notion Save Fails

1. Call `notion-search` to verify workspace access — if no results return, the user may not have connected their Notion workspace
2. Inform the user: "I cannot access your Notion workspace. Please make sure the Notion integration is connected."
3. **Fallback:** Save the full evaluation as a markdown file at the user's preferred path. Include all tables, scores, cost analysis, and recommendations in the markdown.
4. If the user wants to try Notion again later, the markdown file serves as the source — all data can be transferred.

### User Disagrees with the Recommendation

1. Do not defend the recommendation. Ask: "Which vendor do you think should be the top pick, and what criteria am I underweighting?"
2. Adjust the weights based on the user's feedback and recalculate scores
3. If the recalculated scores still disagree with the user's preference, present both results: "Based on the revised weights, Mailchimp scores 105 vs. ConvertKit at 101. The data now supports your preference."
4. If the user overrides the data entirely: respect the decision. Note it in the recommendation as: "User selected Mailchimp based on preference despite ConvertKit scoring higher on the weighted matrix. Primary reason: [user's stated reason]."

---

## Pre-Delivery Checklist

Before delivering the final evaluation, verify:

- [ ] Weighted scoring matrix has 5-7 criteria with non-equal weights
- [ ] Every score has a weighted value shown in parentheses
- [ ] Cost analysis includes Year 1 total, Year 3 total, and at-scale pricing
- [ ] Hidden costs (onboarding, migration, add-ons) are accounted for
- [ ] Each vendor has a pros/cons section with specific, non-generic bullets
- [ ] Risk assessment covers vendor stability, lock-in, and migration difficulty
- [ ] Recommendation names a top pick AND a runner-up with reasoning
- [ ] Recommendation cites specific scores and costs, not just opinions
- [ ] Trial/pilot approach is suggested for the top pick
- [ ] No fabricated pricing or feature claims — uncertain data is marked
- [ ] Decision summary is ready if the user needs to share with stakeholders
- [ ] No placeholder text like [TBD] remains in the final output
