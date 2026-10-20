---
name: customer-journey
description: "When to activate: customer journey mapping, touchpoint audit, moments of truth, experience map, persona journey, friction analysis, CSAT by stage, NPS by stage"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: business
  domain: marketing
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Customer Journey Mapping

## Journey Stages (Universal)

| Stage | Customer goal | Company goal |
|-------|--------------|--------------|
| Awareness | Understand the problem | Get found |
| Consideration | Evaluate options | Educate and differentiate |
| Decision | Choose a solution | Convert |
| Onboarding | Get value fast | Activate |
| Adoption | Build habits | Retain |
| Expansion | Get more value | Upsell/cross-sell |
| Advocacy | Share with others | Drive referrals |

---

## Journey Mapping Methodology

### Step 1: Pick One Persona
Map one persona at a time. Mixing personas creates an average that fits no one.

**Persona snapshot:**
- Name, role, company size
- Primary job to be done
- Tech sophistication
- Decision-making authority

### Step 2: Identify Touchpoints

For each stage, list every interaction point:

**Awareness touchpoints:**
- Google search → SEO blog post
- LinkedIn ad → landing page
- Friend referral → homepage
- Podcast mention → direct traffic

**Consideration touchpoints:**
- Pricing page visit
- Docs/feature pages
- Competitor comparison search
- G2 / Capterra review read
- Demo request

**Decision touchpoints:**
- Sales call
- Trial signup
- Proof of concept
- Procurement/legal review

**Onboarding touchpoints:**
- Welcome email
- In-app onboarding checklist
- First value action
- Support chat

**Adoption touchpoints:**
- Weekly digest / newsletter
- Feature announcements
- Customer success check-in
- Community

### Step 3: Map Emotions

For each touchpoint, rate customer emotion:
- 😊 Positive (excited, confident, delighted)
- 😐 Neutral (indifferent, going through motions)
- 😟 Negative (confused, frustrated, anxious)

Plot on a graph: touchpoints on X-axis, emotion on Y-axis. Low points = intervention opportunities.

### Step 4: Identify Moments of Truth

3 critical moments that define the relationship:

1. **First moment** — First impression (ad, homepage, search result)
2. **Zero moment** — Research phase (reviews, word of mouth, content)
3. **Ultimate moment** — First use experience (does it deliver?)

Concentrate improvement effort here first.

---

## Touchpoint Audit Framework

For each touchpoint, score 1–5:

| Dimension | Question | Score |
|-----------|----------|-------|
| Clarity | Does the customer know what to do next? | /5 |
| Speed | Does it load/respond quickly enough? | /5 |
| Relevance | Is the content right for this stage? | /5 |
| Consistency | Does it match other touchpoints? | /5 |
| Delight | Does it exceed expectations? | /5 |

**Priority matrix:** Low score + high traffic touchpoint = fix first.

---

## Friction Identification

### Common Friction Points by Stage

**Awareness:**
- Page load > 3s → 53% bounce
- Value prop unclear in first 5 seconds
- No mobile optimization

**Consideration:**
- Pricing hidden or confusing
- No social proof near CTAs
- Demo form asks > 5 fields

**Decision:**
- Contract red tape / lengthy legal review
- No self-serve trial available
- Pricing too high relative to perceived value

**Onboarding:**
- Too many steps before first value
- No progress indicator
- Support hard to find

**Adoption:**
- Feature discoverability poor
- No habit-forming mechanisms
- No personalization

### Friction Scoring
Rate each friction: **Frequency × Severity × Fixability**
- Frequency: How often does it happen? (1–3)
- Severity: How much does it hurt? (1–3)
- Fixability: How easy to fix? (1 = hard, 3 = easy)

Score = F × S × Fix. Fix highest scores first.

---

## CSAT and NPS by Stage

### Measurement Triggers

| Stage | Trigger | Survey type |
|-------|---------|-------------|
| Onboarding | Day 3 after signup | CSAT (5-star) |
| First value | After first key action | CES (effort) |
| Adoption | Day 30 | NPS |
| Support | After ticket closed | CSAT |
| Expansion | After upsell | CSAT |

### CSAT by Stage Benchmarks

| Stage | Poor | Acceptable | Good | Excellent |
|-------|------|-----------|------|-----------|
| Onboarding | <3.5 | 3.5–4.0 | 4.0–4.5 | >4.5 |
| Support | <3.5 | 3.5–4.0 | 4.0–4.5 | >4.5 |
| Overall product | <3.0 | 3.0–3.5 | 3.5–4.2 | >4.2 |

### NPS by Stage
- Detractors (0–6): Churn risk; reach out within 48h
- Passives (7–8): Upgrade experience; find what's missing
- Promoters (9–10): Ask for referral or case study

---

## Journey Improvement Prioritization

Use the RICE framework per touchpoint improvement:

| Factor | Question | Score |
|--------|----------|-------|
| Reach | How many customers impacted? | # per month |
| Impact | How much does it move the needle? | 0.25 / 0.5 / 1 / 2 / 3 |
| Confidence | How sure are we? | % |
| Effort | Person-weeks | # |

**RICE Score = (Reach × Impact × Confidence) / Effort**

Top 3 RICE scores = Q1 roadmap items.

---

## Journey Map Template (Simple)

```
Persona: [Name]
Stage: [Awareness → Advocacy]

Touchpoint | Channel | Emotion | Friction | Improvement
-----------|---------|---------|----------|------------
Google search | SEO | 😐 | Ranking #5 | Optimize H1, add FAQ schema
Homepage | Web | 😊 | None | —
Pricing page | Web | 😟 | Price shock | Add "Start free" CTA
Trial signup | Web | 😊 | 4-field form | Reduce to 2 fields
Welcome email | Email | 😐 | Generic copy | Personalize by use case
First action | In-app | 😟 | No guidance | Add inline tooltip
```
