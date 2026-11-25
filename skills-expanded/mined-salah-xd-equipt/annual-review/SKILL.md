---
name: annual-review
description: "Compiles annual business reviews with year-over-year metrics, milestone highlights, lessons learned, and strategic goals for the upcoming year. Use when a user needs to reflect on their business year, wants to create a year-in-review document for stakeholders, or is setting annual goals and needs to assess where they stand."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Annual Business Review

## When to Use This Skill

- A founder or operator wants to reflect on their business year
- Someone needs a year-in-review document for investors, partners, or their team
- A creator wants to publish an annual recap for their audience or newsletter
- A business owner is setting next-year goals and needs to assess where they stand
- End of fiscal year or calendar year triggers a need for structured review

**EVERY NUMBER TELLS A STORY. DO NOT LIST METRICS WITHOUT EXPLAINING WHAT THEY MEAN FOR THE BUSINESS GOING FORWARD.**

---

## Step 1: Understand the Business Year

Gather the following from the user before writing anything.

### Required Information (minimum 5 data points)

1. **Business name** and what the business does
2. **Year being reviewed** (e.g., 2025)
3. **Key metrics** — ask for whichever apply:
   - Revenue (total, MRR, or ARR)
   - Customer/client count
   - Email subscribers or audience size
   - Products or services launched
   - Content published (episodes, posts, videos)
   - Website traffic or conversion rates
   - Team size changes
4. **Top 3-5 wins** — what went well and why
5. **Biggest 2-3 challenges** — what did not go as planned
6. **Major milestones** — launches, hires, pivots, partnerships, press
7. **Last year's goals** (if they had them) — what were they aiming for?
8. **Financial summary** — optional, only if comfortable sharing
9. **Tools or systems adopted** — new software, processes, workflows

### Review Type

Ask the user which audience the review is for:

| Type | Audience | Tone | Focus |
|------|----------|------|-------|
| Internal | The founder themselves | Honest, reflective | Lessons + next-year strategy |
| Stakeholder | Investors, partners, board | Professional, data-driven | Metrics + growth trajectory |
| Public | Newsletter subscribers, social audience | Transparent, narrative | Story + wins + lessons |
| Team | Employees, contractors | Motivational, clear | Wins + priorities + team role |

**Default:** Internal founder review.

### Gate

Do not proceed until you have at least 5 concrete data points about the year. If the user provides fewer than 5, ask targeted follow-up questions:

- "What was your approximate revenue this year?"
- "How many customers or clients did you serve?"
- "What was the single biggest win of the year?"
- "What was one thing that did not go as planned?"
- "Did you launch anything new — a product, service, or content series?"

---

## Step 2: Analyze and Organize

Structure the review into these seven sections. Apply the **"So What?" test** to every item — if a data point does not connect to a lesson, a trend, or a forward-looking action, cut it or reframe it.

### Section Breakdown

**1. Executive Summary**
Three sentences maximum. Cover: what the business did this year, the single biggest result, and the primary focus for next year.

Example:
> In 2025, Oakridge Creative grew from a solo freelance operation to a 3-person agency serving 14 retainer clients. Revenue hit $192K, a 68% increase over 2024. In 2026, the priority is systemizing delivery to support 20 clients without adding headcount.

**2. By the Numbers**
Present a metrics table. Include year-over-year comparison when prior-year data is available. Mark direction with arrows.

Example:

| Metric | 2024 | 2025 | Change |
|--------|------|------|--------|
| Revenue | $114K | $192K | +68% |
| Retainer clients | 8 | 14 | +75% |
| Team size | 1 | 3 | +2 |
| Email subscribers | 1,200 | 3,800 | +217% |
| Blog posts published | 24 | 41 | +71% |
| Average project value | $3,200 | $4,100 | +28% |

When prior-year data is not available, present current-year numbers alone without fabricating comparison figures.

**3. Top Wins**
List 3-5 highlights. For each win, include:
- What happened
- Why it mattered
- What it unlocked going forward

Example:
> **Landed first $10K/month retainer client (March)**
> Signed a SaaS company for ongoing content strategy at $10K/month. This single client covered 62% of monthly overhead, which removed the pressure to chase small projects and freed up bandwidth to be selective about new work.

**4. Challenges and Lessons**
List 2-4 challenges. For each, include:
- What happened
- What was learned
- What will change as a result

Example:
> **Underpriced the first two retainer deals (Q1)**
> Signed initial retainer clients at $2,500/month based on freelance-era pricing. Within 60 days, scope creep made both unprofitable. Lesson: price retainers based on delivered value, not hourly estimates. All subsequent retainers used value-based pricing and averaged $4,100/month.

**5. Key Milestones**
Present as a timeline. Include month and event.

Example:

| Month | Milestone |
|-------|-----------|
| January | Launched redesigned website with case studies |
| March | Signed first $10K/month retainer client |
| May | Hired first full-time team member (content writer) |
| July | Hit $15K MRR for the first time |
| September | Spoke at CreatorCon — generated 6 inbound leads |
| November | Crossed 3,000 email subscribers |

**6. Goals Review**
If the user had prior-year goals, compare targets to actuals.

Example:

| Goal | Target | Actual | Status |
|------|--------|--------|--------|
| Reach $150K revenue | $150K | $192K | Exceeded |
| Grow to 12 retainer clients | 12 | 14 | Exceeded |
| Publish weekly newsletter | 52 issues | 41 issues | Missed |
| Launch online course | 1 course | 0 | Not started |

If no prior-year goals exist, skip this section and note: "No formal goals were set for the reviewed year. This review establishes the baseline for goal-setting going forward."

**7. Next Year Priorities**
Define 3-5 strategic goals. Each goal must have:
- A measurable target
- A rationale (why this goal matters now)
- A key action or first step

Example:
> **1. Reach $300K revenue**
> Rationale: Current trajectory and pipeline support 56% growth. Two additional retainer clients at $5K/month plus one productized service launch close the gap.
> First step: Audit current pipeline and identify 5 warm leads to contact in January.
>
> **2. Launch a productized content audit service at $2,500 flat rate**
> Rationale: Repeating the same audit process for 6 clients this year proved it is systematizable. A fixed-price offer removes scope negotiation and shortens the sales cycle.
> First step: Document the current audit process as an SOP by end of January.
>
> **3. Grow email list to 6,000 subscribers**
> Rationale: Email drives 70% of inbound leads. Doubling the list supports the revenue goal without increasing ad spend.
> First step: Create a lead magnet based on the top-performing blog post from this year.

---

## Step 3: Present the Review

### Assembly

Combine all seven sections into a single markdown document with this structure:

```
# [Business Name] — [Year] Annual Review

## Executive Summary
[3-sentence overview]

## By the Numbers
[Metrics table]

## Top Wins
[3-5 wins with context]

## Challenges and Lessons
[2-4 challenges with takeaways]

## Key Milestones
[Timeline table]

## Goals Review
[Target vs. actual table, or baseline note]

## Next Year Priorities
[3-5 goals with targets and first steps]
```

### Tone Adjustments by Review Type

- **Internal:** Direct, no sugarcoating. Include financial details. Emphasize lessons and honest assessment.
- **Stakeholder:** Professional, metrics-forward. Lead with growth numbers. Frame challenges as "areas of investment."
- **Public:** Narrative-driven, transparent. Lead with the story. Include vulnerability about challenges. End with what is next.
- **Team:** Celebratory but clear. Emphasize collective wins. Connect next-year priorities to each team member's role.

### Gate

Present the full review to the user. Ask: "Does this accurately reflect your year? Anything to add, remove, or adjust?" Do not save until the user confirms.

---

## Step 4: Act

### Save the Review

Save the completed review as a markdown file:

```
[business-name]-[year]-annual-review.md
```

Example: `oakridge-creative-2025-annual-review.md`

Save to the current working directory unless the user specifies a different path.

### Offer Follow-Up Outputs

After saving, offer these options:

1. **Standalone Goals Document** — Extract just the "Next Year Priorities" section as a separate file (`[business-name]-[year+1]-goals.md`) for use as a working reference throughout the new year
2. **Newsletter Excerpt** — Rewrite the Executive Summary, Top Wins, and Challenges sections in a conversational tone suitable for a newsletter or blog post (800-1,200 words)
3. **Team Presentation Outline** — Restructure the review as a slide-by-slide outline for an all-hands meeting (8-12 slides)
4. **Investor Update** — Condense to a one-page summary with metrics table, growth narrative, and funding/resource ask if applicable

Only offer options relevant to the chosen review type. For example, do not offer "Investor Update" for an Internal review unless the user mentions investors.

---

## Anti-Patterns

- **DO NOT invent metrics the user did not provide.** If revenue was not shared, leave it out. Never estimate or assume financial figures.
- **DO NOT skip the Challenges section.** A review without honest challenges is a vanity document. If the user says "nothing went wrong," ask: "What took longer than expected? What would you do differently?"
- **DO NOT set goals without measurable targets.** "Grow the business" is not a goal. "$300K revenue by December" is a goal.
- **DO NOT compare to industry benchmarks** unless the user explicitly requests it. Unsolicited benchmark comparisons feel judgmental and may be inaccurate.
- **DO NOT inflate language.** "Unprecedented growth" for 12% revenue increase is dishonest. State the numbers and let them speak.
- **DO NOT include metrics that fail the "So What?" test.** If a number does not connect to a lesson, trend, or action, it does not belong in the review.
- **DO NOT combine multiple years into one review.** Each review covers exactly one year. If the user wants a multi-year comparison, that is a separate document.
- **DO NOT write goals that contradict the data.** If the business shrank this year, a "10x revenue" goal for next year needs serious justification or it should be reframed.
- **DO NOT present the review in a different format than the user's chosen review type.** An internal review should not read like a press release.

---

## Recovery Scenarios

**User provides fewer than 5 data points:**
Ask 3 targeted questions from the gate checklist in Step 1. If the user still cannot provide enough data, build the review around what is available and flag the gaps: "Note: This review is based on limited data. Sections marked [incomplete] can be updated when additional figures are available."

**User has no prior-year data for comparison:**
Skip the YoY columns in the metrics table. Frame the current year as the baseline: "This is Year 1 of tracked metrics. Next year's review will include year-over-year comparisons."

**User says nothing went wrong:**
Push back respectfully: "Every year has friction points. What took longer than expected? What would you handle differently with hindsight? Even small frustrations reveal useful patterns." If they still decline, note in the review: "The founder reported no significant challenges this year. Next year's review should revisit this section with specific attention to operational friction and opportunity costs."

**User wants to include aspirational numbers instead of actuals:**
Redirect: "This review captures what actually happened. Aspirational targets belong in the Next Year Priorities section. Shall I add those goals there instead?"

**User's goals from last year do not exist or are vague:**
Skip the Goals Review section. Add a note: "No formal goals were documented for the reviewed year. The Next Year Priorities section below establishes measurable targets for the first time."

**User requests a review for a year that is not yet complete:**
Proceed with a "Year-to-Date Review" label. Adjust the title to "[Business Name] — [Year] Year-to-Date Review (through [Month])." Note that final figures may change and goals should be revisited after year-end.

**User provides conflicting data:**
Flag the inconsistency before proceeding: "You mentioned $192K in total revenue but also $10K/month in retainer revenue for 12 months, which is $120K. That leaves $72K from other sources — is that correct, or should we adjust the revenue figure?"
