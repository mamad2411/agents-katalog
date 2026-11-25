---
name: campaign-plan
description: >
  Plan marketing campaigns end-to-end: objectives, audience, channels, budget,
  timeline, creative brief, and success metrics.
  TRIGGER when: user says /campaign-plan, "plan a campaign", "marketing campaign", "campaign strategy", "launch plan".
argument-hint: "[campaign goal or product/service name]"
user-invocable: true
---

# Campaign Plan

Plan and structure a complete marketing campaign from objective-setting through post-campaign analysis. Produces a ready-to-execute campaign document that aligns stakeholders, guides creative production, and defines measurable success.

---

## Process

### Step 1 — Define Campaign Objective

Clarify the single primary objective and up to two secondary objectives. Every downstream decision flows from this.

| Objective Type | Example | Primary KPI |
|---|---|---|
| Awareness | Launch new brand in market | Impressions, Reach |
| Consideration | Drive whitepaper downloads | Leads, CTR |
| Conversion | Increase trial sign-ups by 30% | Sign-ups, CPA |
| Retention | Re-engage churned users | Reactivation rate |
| Advocacy | Generate customer referrals | Referral count, NPS |

Ask the user:
- What is the single most important outcome?
- Is there a revenue or pipeline target attached?
- What does failure look like?

### Step 2 — Identify Target Audience

Build one or more audience segments with enough detail to inform channel selection and creative tone.

For each segment, capture:

| Field | Detail |
|---|---|
| Segment name | e.g., "Mid-market SaaS CTOs" |
| Demographics | Age range, title, company size, geography |
| Psychographics | Pain points, motivations, objections |
| Current awareness | Unaware / Problem-aware / Solution-aware / Product-aware |
| Preferred channels | Where they spend attention |
| Decision triggers | What moves them to act |

If the user provides minimal input, infer reasonable defaults and flag assumptions explicitly.

### Step 3 — Select Channels and Tactics

Map channels to the audience and objective. Use the matrix below as a starting framework.

| Channel | Best For | Typical CPM/CPC | Lead Time |
|---|---|---|---|
| Paid Search (Google Ads) | High-intent conversion | $1-8 CPC | 1-2 weeks |
| Paid Social (LinkedIn) | B2B awareness & leads | $6-12 CPC | 1-2 weeks |
| Paid Social (Meta) | B2C awareness & retargeting | $0.50-3 CPC | 1 week |
| Email (owned list) | Nurture & retention | ~$0 marginal | 3-5 days |
| Content / SEO | Long-term organic traffic | $0 marginal | 2-6 months |
| Influencer / Creator | Trust & reach in niche | Varies widely | 3-6 weeks |
| Events / Webinars | Pipeline & relationships | $2K-50K per event | 4-8 weeks |
| PR / Media | Credibility & reach | Agency retainer | 4-8 weeks |
| Direct Mail | Account-based marketing | $5-25 per piece | 3-4 weeks |

For each selected channel, specify:
1. Tactic (e.g., "LinkedIn Sponsored Content — single image ads")
2. Audience targeting parameters
3. Creative requirements (format, dimensions, copy length)
4. Expected volume and cost

### Step 4 — Set Budget and Allocate

Provide a budget breakdown table:

| Line Item | Estimated Cost | % of Total | Notes |
|---|---|---|---|
| Paid media spend | | | |
| Creative production | | | |
| Tools / Software | | | |
| Agency / Freelancer fees | | | |
| Events / Sponsorships | | | |
| Contingency (10-15%) | | | |
| **Total** | | **100%** | |

Rules of thumb:
- Allocate 60-70% to the top 2 channels by expected ROI.
- Reserve 10-15% for testing new channels or creative variants.
- Include a contingency buffer of 10-15%.

### Step 5 — Build Timeline

Create a phased timeline with owners and dependencies.

| Phase | Duration | Key Activities | Owner | Dependencies |
|---|---|---|---|---|
| Planning | Week 1-2 | Brief sign-off, audience research | Marketing lead | Stakeholder alignment |
| Creative Production | Week 2-4 | Copy, design, landing pages | Creative team | Approved brief |
| Setup & QA | Week 4-5 | Ad accounts, tracking pixels, UTMs | Growth/Ops | Creative assets ready |
| Soft Launch | Week 5 | Small-budget test flight | Growth | QA sign-off |
| Full Launch | Week 6-8 | Scale spend, monitor daily | Growth | Soft launch learnings |
| Optimization | Week 8-10 | A/B tests, bid adjustments, reallocation | Growth | Performance data |
| Wrap-up & Report | Week 11-12 | Post-mortem, final report | Marketing lead | Campaign end |

### Step 6 — Write the Creative Brief

Produce a concise creative brief document:

```
CREATIVE BRIEF
==============
Campaign name:
Objective:
Target audience:
Key message (single sentence):
Supporting proof points (up to 3):
Desired action (CTA):
Tone & style:
Mandatory inclusions (logos, disclaimers, legal):
Deliverables list:
Due date:
```

### Step 7 — Define Success Metrics and Reporting

| Metric | Target | Measurement Tool | Reporting Cadence |
|---|---|---|---|
| Impressions | | Ad platform | Weekly |
| Click-through rate (CTR) | | Ad platform | Weekly |
| Cost per click (CPC) | | Ad platform | Weekly |
| Leads / Sign-ups | | CRM / Analytics | Weekly |
| Cost per acquisition (CPA) | | Calculated | Bi-weekly |
| Conversion rate | | Analytics | Bi-weekly |
| Revenue attributed | | CRM | Monthly |
| ROAS / ROI | | Calculated | End of campaign |

---

## Output Format

Return the campaign plan as a structured document with these sections:

1. **Executive Summary** — 3-5 sentences covering objective, audience, channels, budget, and timeline.
2. **Objective & KPIs** — Table of primary and secondary objectives with targets.
3. **Target Audience** — Segment profiles.
4. **Channel Strategy** — Channel-tactic matrix with rationale.
5. **Budget** — Allocation table.
6. **Timeline** — Gantt-style phase table.
7. **Creative Brief** — Filled-in brief template.
8. **Measurement Plan** — Metrics table with targets and tools.
9. **Risks & Mitigations** — Top 3-5 risks with contingency actions.

---

## Quality Checklist

- [ ] Objective is specific, measurable, and time-bound
- [ ] Audience segments have enough detail to guide targeting and creative
- [ ] Channel selection is justified by audience behavior, not habit
- [ ] Budget includes contingency and testing allocation
- [ ] Timeline has clear owners and dependencies
- [ ] Creative brief is complete and actionable
- [ ] Every KPI has a target number, not just a metric name
- [ ] Risks are identified with concrete mitigations
- [ ] UTM and tracking plan is specified
- [ ] Legal / compliance requirements are noted (disclaimers, opt-outs, GDPR)

---

## Edge Cases

- **No budget provided**: Ask for at least a range. If none given, produce a plan at three tiers (low / medium / high) with trade-offs explained.
- **Vague objective** ("grow the brand"): Push back with clarifying questions. If the user insists, default to an awareness objective with reach and impression KPIs, and note the ambiguity.
- **Single-channel request**: Still produce the full plan but focus depth on that channel. Suggest one complementary channel with rationale.
- **Very short timeline** (< 2 weeks): Flag that paid media learning periods and creative production may be compressed. Recommend simplified creative and higher initial bids.
- **Regulated industry** (finance, healthcare, alcohol): Add a compliance review step to the timeline and flag industry-specific ad policies (e.g., Meta financial services restrictions, HIPAA).
- **International / multi-market campaigns**: Add localization requirements, time-zone considerations, and per-market budget splits.
- **No existing audience data**: Recommend a discovery phase with broad targeting and rapid iteration before committing full budget.
