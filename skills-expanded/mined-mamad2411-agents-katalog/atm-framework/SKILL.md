# ATM Framework — Brand Visibility to Business Impact

Use the ATM framework (Audience Growth → Trust & Engagement → Monetization) to audit brand visibility and connect it directly to business impact. Developed by Lisa Cole / The Limitless CMO.

## Framework Architecture

```
AUDIENCE GROWTH        →   TRUST & ENGAGEMENT    →   MONETIZATION
Findability + Dominance    Engagement + Perception    Demand Progression + Business Impact
```

---

## Pillar 1 — Audience Growth

### Sub-pillars
**Findability** (how easily the brand is discovered):
- Earned Media Coverage
- Industry Event Coverage
- Social Media Followers
- Accounts Reached
- Backlinks
- Unique Web Visitors
- AI Answer Mention Rate

**Dominance** (share of voice and authority):
- Traditional SOV
- Social Media SOV
- Domain Authority
- Unbranded Search volume
- Branded Search volume
- Media Sentiment
- AI Share of Voice

### Prompt — Audience Growth Audit

```
Act as a brand strategist using the ATM Framework.

Audit [BRAND/COMPANY]'s AUDIENCE GROWTH across two dimensions:

FINDABILITY AUDIT:
- Earned Media Coverage: How many earned placements in the last quarter?
- Industry Events: Speaking slots, sponsorships, coverage?
- Social Media Followers: Total across key platforms + MoM growth rate?
- Accounts Reached: Total ICP accounts reached via all channels?
- Backlinks: Total referring domains + trend (growing or shrinking)?
- Unique Web Visitors: Monthly uniques + YoY change?
- AI Answer Mention Rate: % of relevant AI-generated answers that mention the brand?

DOMINANCE AUDIT:
- Traditional SOV: % of share of voice in earned media vs. top 3 competitors?
- Social Media SOV: % of relevant conversation owned by brand?
- Domain Authority: Score vs. category benchmark?
- Unbranded Search: Monthly search volume for category terms where brand ranks?
- Branded Search: Monthly searches specifically for brand name?
- Media Sentiment: % positive/neutral/negative across coverage?
- AI Share of Voice: % of AI-generated category answers where brand is cited?

For each metric:
1. State current value and trend (↑ ↓ →)
2. Benchmark against category median
3. Flag red if declining / green if growing
4. Prioritize the 3 highest-leverage improvements

Format as an executive scorecard table.
```

---

## Pillar 2 — Trust & Engagement

### Sub-pillars
**Audience Engagement** (behavioral proof of interest):
- ICP Accounts Engaged
- Identified Contacts Engaged
- Marketable Email DB size
- Community Members

**Audience Perception** (qualitative brand equity):
- Owned Event Attendance
- Brand Loyalty score
- NPS
- NRR (Net Revenue Retention)
- AI Message Accuracy
- AI Sentiment / Rec Quality
- Third-Party Citation Rate

### Prompt — Trust & Engagement Audit

```
Act as a brand strategist using the ATM Framework.

Audit [BRAND/COMPANY]'s TRUST & ENGAGEMENT:

AUDIENCE ENGAGEMENT:
- ICP Accounts Engaged: How many ideal customer profile accounts actively engaged with content?
- Identified Contacts Engaged: Named contacts who engaged across any channel?
- Marketable Email DB: Total size + MoM growth rate?
- Community Members: Active community size across all platforms?

AUDIENCE PERCEPTION:
- Owned Event Attendance: Average attendance at brand-hosted events?
- Brand Loyalty: Repeat purchase or renewal rate?
- NPS: Current score + trend?
- NRR: Net Revenue Retention % — are existing customers expanding?
- AI Message Accuracy: % of AI-generated content about the brand that is factually accurate?
- AI Sentiment/Rec Quality: When AI recommends the brand, is the framing positive?
- Third-Party Citation Rate: % of industry reports, analysts, and media that cite the brand unprompted?

For each:
1. Current value + direction
2. Industry benchmark
3. Root cause analysis if lagging
4. 30-day action to improve

Conclude with a Trust Score (0–100) and top 3 trust gaps.
```

---

## Pillar 3 — Monetization

### Sub-pillars
**Demand Progression** (pipeline creation from brand):
- Targeted-to-Engaged Conversion rate
- MQA (Marketing Qualified Account) to Opportunity Conv.
- Opportunity to Sales Conv.
- Lead-to-Sale Velocity (days)
- AI-Influenced Engaged
- AI-Assisted Opportunity Creation

**Business Impact** (revenue outcomes):
- Avg Account Growth
- Opportunity Pipeline ($)
- Net New Revenue ($)
- Average Deal Size / ACV
- AI-Influenced Pipeline ($)
- AI-Assisted Revenue ($)

### Prompt — Monetization Audit

```
Act as a revenue-focused CMO using the ATM Framework.

Audit [BRAND/COMPANY]'s MONETIZATION outcomes:

DEMAND PROGRESSION:
- Targeted-to-Engaged Conv.: What % of targeted ICP accounts become engaged?
- MQA-to-Opportunity Conv.: Of engaged accounts, what % create pipeline?
- Opportunity-to-Sales Conv.: Win rate?
- Lead-to-Sale Velocity: Average days from first touch to close?
- AI-Influenced Engaged: How many accounts engaged via AI-generated touchpoints?
- AI-Assisted Opp Creation: Opportunities where AI interaction preceded creation?

BUSINESS IMPACT:
- Avg Account Growth: YoY revenue growth per account?
- Opportunity Pipeline: Total pipeline value attributable to brand programs?
- Net New Revenue: New ARR/revenue from brand-attributed channels?
- Average Deal Size / ACV: Trend vs. prior year?
- AI-Influenced Pipeline: $ pipeline where AI touchpoints played a role?
- AI-Assisted Revenue: $ closed revenue where AI-assisted interactions occurred?

Produce:
1. A monetization scorecard with RAG (Red/Amber/Green) status
2. The single biggest conversion leak in the funnel
3. A 90-day brand-to-revenue action plan
```

---

## Full ATM Audit (All 3 Pillars)

### Prompt — Complete ATM Audit

```
You are a strategic CMO advisor. Run a complete ATM Framework audit for [BRAND/COMPANY]:

THE ATM FRAMEWORK connects Brand Visibility to Business Impact across 3 pillars:

PILLAR 1 — AUDIENCE GROWTH
Findability: Earned media, events, social followers, accounts reached, backlinks, web visitors, AI mention rate
Dominance: Traditional SOV, social SOV, domain authority, unbranded search, branded search, media sentiment, AI share of voice

PILLAR 2 — TRUST & ENGAGEMENT
Engagement: ICP accounts engaged, contacts engaged, email DB, community size
Perception: Event attendance, brand loyalty, NPS, NRR, AI message accuracy, AI sentiment, third-party citation rate

PILLAR 3 — MONETIZATION
Demand Progression: Targeted→Engaged conv., MQA→Opp conv., Opp→Sales conv., velocity, AI-influenced engagement
Business Impact: Account growth, pipeline, net new revenue, ACV, AI-influenced pipeline, AI-assisted revenue

FOR THE AUDIT:
1. Score each sub-pillar 1–10 based on available data or reasonable estimates
2. Identify the #1 bottleneck in each pillar
3. Map where brand investments have the most leverage on revenue
4. Produce a 3-pillar executive scorecard
5. Recommend the top 5 actions ranked by ROI

[Paste available metrics or describe the business context]
```

---

## Commands Reference

| Command | Purpose |
|---------|---------|
| `/atm-audit [brand]` | Full 3-pillar ATM audit |
| `/atm-audience [brand]` | Audience Growth pillar only |
| `/atm-trust [brand]` | Trust & Engagement pillar only |
| `/atm-monetization [brand]` | Monetization pillar only |
