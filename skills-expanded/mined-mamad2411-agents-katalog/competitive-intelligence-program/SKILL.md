---
name: competitive-intelligence-program
description: "When to activate: competitive intelligence program, battle cards, competitor monitoring, win/loss analysis, market positioning, competitive research, CI distribution, CI program setup, quarterly competitive review"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.1.0
  category: business
  domain: business-ops
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Competitive Intelligence Program

Program-management angle on CI: scope, tooling, battle cards, win/loss process, and distribution. For OSINT tradecraft (how to actually gather signals) see `skills/research/competitive-intelligence.md`.

## CI Program Setup

### Define Scope
- **Primary competitors**: head-to-head competition in core segments (2–4 companies)
- **Secondary competitors**: adjacent or emerging threats (4–8 companies)
- **Watch list**: early-stage startups, potential entrants (track quarterly)

### Signal Sources
| Source | Type | Cadence |
|--------|------|---------|
| Competitor website & blog | Positioning, product updates | Weekly scrape / alert |
| G2, Capterra, Trustpilot | Customer sentiment, feature gaps | Weekly |
| LinkedIn | Headcount trends, key hires, job postings | Weekly |
| Crunchbase / PitchBook | Funding, acquisitions | On alert |
| SEC filings (public competitors) | Revenue, strategy, risks | Quarterly |
| Job postings | Strategic priorities, tech stack | Weekly |
| Twitter / X, Reddit | Sentiment, complaints, launches | Daily alerts |
| Press releases | Product launches, partnerships | Google alerts |
| Customer interviews | How they talk about alternatives | Each sales/CS call |
| Win/loss interviews | Direct competitive comparison | Each closed deal |
| Conference talks | Strategy signals, roadmap hints | Per conference |
| Patent filings | R&D direction | Quarterly |

### Tooling
- **Monitoring**: Crayon, Klue, Kompyte (or free: Google Alerts, RSS)
- **Win/loss**: Clozd, Gong, or structured interview template
- **Distribution**: Notion / Confluence battle card pages; Slack CI channel
- **CRM tagging**: tag every opportunity with competitor(s) involved

---

## Battle Card Template

```
# Competitor: [Name]
Last updated: YYYY-MM-DD
Owner: [Product Marketing]

## One-line summary
[How to position against them in one sentence]

## Their strengths (be honest — salespeople will lose trust if you're not)
- [Strength 1]: [Why customers like it]
- [Strength 2]: [Why customers like it]
- [Strength 3]: [Why customers like it]

## Their weaknesses (with evidence)
- [Weakness 1]: [Source — G2 quote, customer feedback, product limitation]
- [Weakness 2]: [Source]
- [Weakness 3]: [Source]

## Why we win
- [Differentiator 1]: [Specific evidence or customer quote]
- [Differentiator 2]: [Specific evidence or customer quote]
- [Differentiator 3]: [Specific evidence or customer quote]

## Why we lose (be honest)
- [Reason 1]: [When we're at a disadvantage]
- [Reason 2]: [When we're at a disadvantage]

## Discovery questions (to expose their weaknesses naturally)
1. "[Question that surfaces pain with competitor]"
2. "[Question that highlights competitor limitation]"
3. "[Question that uncovers unmet need we address]"

## Objection handling
| Their claim | Our response |
|------------|-------------|
| "Competitor X is cheaper" | "[Total cost framing / ROI response]" |
| "Competitor X has feature Y" | "[Our roadmap / our alternative / their limitation]" |
| "Competitor X has more customers" | "[Quality vs. quantity / our segment focus]" |
| "We're already using X" | "[Displacement or coexistence approach]" |

## Trap questions (to plant in their mind)
1. "Ask them how they handle [known weakness]."
2. "Ask to see [feature they don't have or is poor quality]."
3. "Ask for a reference in your industry / use case."

## Proof points (customer wins against this competitor)
- [Customer logo]: switched from [Competitor] because [reason]
- [Customer logo]: chose us over [Competitor] in bakeoff because [reason]

## Pricing comparison (if known)
[Our pricing] vs [Their pricing] — note: verify with recent data
```

---

## Win/Loss Analysis

### Interview Template (30-minute call)

**For won deals:**
1. What initially prompted you to evaluate solutions in this space?
2. Which vendors did you evaluate? Who made the shortlist?
3. What were the top 3 criteria you used to make your decision?
4. Where did [our product] stand out vs. alternatives?
5. Where did you have concerns about us? How did we address them?
6. What almost made you choose a competitor?
7. Who was your internal champion? Who were the skeptics?

**For lost deals:**
1. What were the top 3 factors in your decision?
2. Who did you ultimately choose and why?
3. Where did we fall short in the evaluation?
4. What would have changed your decision?
5. How do you expect [competitor] to address [their known weakness]?
6. Would you be open to re-evaluating us if [specific thing] changed?

### Win/Loss Metrics
| Metric | Formula | Target (varies by company) |
|--------|---------|--------------------------|
| Win rate (overall) | Deals won / deals closed | Track trend |
| Win rate vs. [competitor] | Won vs. competitor / all deals involving competitor | > 50% |
| Competitive deal cycle length | Avg days for competitive vs. non-competitive | Track delta |
| Reasons won (top 3) | % of wins citing each reason | |
| Reasons lost (top 3) | % of losses citing each reason | |

---

## Monitoring Cadence

### Weekly CI Digest (internal Slack / email)
```
[Week of YYYY-MM-DD] Competitive Intel Digest

New this week:
- [Competitor A] launched [feature]: [link] — impact: [Low/Medium/High]
- [Competitor B] raised $Xm Series C: [link] — impact: [Medium]
- [Competitor C] job postings for [ML engineers]: signals [roadmap direction]

Customer sentiment (G2 / reviews):
- [Competitor A] new 1-star reviews mentioning [theme]: opportunity for us
- [Competitor B] response time complaints increasing

Action items:
- Update battle card for [Competitor A] by [date] — owner: [Name]
- Flag [Competitor B] funding to sales team — owner: [Name]
```

### Quarterly Competitive Review Agenda (2 hours)
1. Win rate trends by competitor (30 min)
2. Battle card accuracy review — what's stale? (30 min)
3. Competitor product updates since last quarter (30 min)
4. Emerging competitors / watch list update (15 min)
5. Positioning implications and messaging updates (15 min)

---

## CI Distribution

### Audience Segmentation
| Audience | What they need | Format | Cadence |
|----------|---------------|--------|---------|
| Sales (AEs) | Battle cards, objection handling, proof points | Concise, scannable | Updated on launches |
| Sales (SDRs) | Discovery questions, elevator pitch | Even shorter | Monthly refresh |
| Product | Feature gaps, roadmap implications | Detailed analysis | Quarterly |
| Marketing | Positioning, messaging, category definition | Strategic | Quarterly |
| Executive | Win rate trends, competitive threats, market moves | Dashboard + narrative | Monthly |
| CS | Competitive churn risk accounts, retention talking points | Account-specific | On alert |

### Battle Card Quality Checklist
- [ ] Updated within last 90 days
- [ ] Reviewed by at least 2 AEs who compete against this vendor regularly
- [ ] Contains customer quotes (not just internal assertions)
- [ ] Discovery questions tested in real calls
- [ ] Pricing data verified (not from memory)
- [ ] Linked from CRM opportunity for easy access during deals
