---
name: product-feedback-loop
description: "Designs product feedback loops connecting customer input to product decisions with transparency and communication. Use when systematizing how feedback drives your roadmap."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Product Feedback Loop

## When to Use This Skill

Use this skill when you need to:
- Design a system that connects customer feedback to product decisions
- Build transparency around how user input shapes the roadmap
- Create communication workflows that close the loop with customers
- Establish a repeatable process for collecting, prioritizing, and acting on feedback

**DO NOT** use this skill for feature request boards (use feature-request-system), user research plans, or NPS survey design. This is for the end-to-end feedback-to-decision loop.

---

## Core Principle

A FEEDBACK LOOP IS ONLY A LOOP IF INFORMATION FLOWS BACK TO THE CUSTOMER — COLLECTING FEEDBACK WITHOUT CLOSING THE LOOP TRAINS USERS TO STOP SHARING.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Product** | "What product is this feedback loop for?" | No default — must be provided |
| **Feedback volume** | "How many pieces of feedback do you receive monthly?" | Under 100 |
| **Current process** | "How do you handle feedback today?" | Ad hoc / no system |
| **Decision makers** | "Who decides what gets built?" | Solo founder |
| **Communication gap** | "Do customers know when their feedback influences a decision?" | No |

**GATE: Confirm the brief before designing the loop.**

---

## Phase 2: Design the Loop

### The Four-Stage Feedback Loop

```
COLLECT → ANALYZE → ACT → COMMUNICATE
   ↑                                    |
   └────────────────────────────────────┘
```

**Stage 1: Collect** — Gather feedback from all channels into one system
**Stage 2: Analyze** — Tag, categorize, and identify patterns
**Stage 3: Act** — Prioritize and decide what to build, improve, or ignore
**Stage 4: Communicate** — Tell customers what happened with their feedback

### Collection Channels Map

| Channel | Type | Capture Method |
|---------|------|---------------|
| In-app widget | Reactive | Auto-logged to central system |
| Support tickets | Reactive | CS team tags feedback items |
| NPS/CSAT surveys | Proactive | Scheduled quarterly |
| User interviews | Proactive | Monthly with 3-5 users |
| Social media | Reactive | Manual capture, weekly review |
| Sales calls | Reactive | CRM notes tagged as feedback |
| Review sites | Reactive | Weekly monitoring |

**GATE: Confirm loop design and channels before building the system.**

---

## Phase 3: Build the System

### Tagging Taxonomy

Every piece of feedback gets tagged with:
- **Category:** Feature area (billing, onboarding, reporting, etc.)
- **Type:** Bug, feature request, UX issue, praise, complaint
- **Sentiment:** Positive, neutral, negative
- **Impact:** Revenue risk, retention risk, growth opportunity
- **Source:** Channel it came from

### Analysis Cadence

| Frequency | Activity |
|-----------|----------|
| Daily | Triage incoming feedback (tag and categorize) |
| Weekly | Review patterns and rising themes |
| Monthly | Prioritization session — decide what to act on |
| Quarterly | Trend analysis and roadmap alignment |

### Decision Framework

For each feedback theme, answer:
1. How many users mentioned this? (Volume)
2. How does it impact revenue or retention? (Business impact)
3. How hard is it to address? (Effort)
4. Does it align with product vision? (Strategy fit)

Score and prioritize using a simple matrix:
- **High volume + high impact + low effort** = Do now
- **High volume + high impact + high effort** = Plan for next quarter
- **Low volume + low impact** = Acknowledge and defer
- **Conflicts with vision** = Decline with explanation

### Communication Templates

**Feedback received:**
"Thanks for sharing this. We have logged it and it will be reviewed in our next prioritization session."

**Feedback being worked on:**
"You asked for [feature]. We are building it now and expect to ship it by [timeframe]. We will let you know when it is live."

**Feedback shipped:**
"You asked, we built it. [Feature] is now live. Try it here: [link]. Thanks for helping us make [Product] better."

**Feedback declined:**
"We reviewed your suggestion for [feature]. After careful consideration, we decided not to pursue it because [reason]. We appreciate you sharing and encourage you to keep the ideas coming."

---

## Phase 4: Polish

### 1. Transparency Practices

- Publish a monthly "What we heard" summary (blog or email)
- Show a public roadmap with "Inspired by your feedback" labels
- Tag changelog entries that came from user feedback
- Share aggregate feedback stats: "We reviewed 147 pieces of feedback this month"

### 2. Feedback Health Metrics

```
## Loop Health Metrics

- **Collection rate:** Pieces of feedback per month (trending up = good)
- **Response time:** Average time to acknowledge feedback
- **Close rate:** % of feedback items with a final status (built, declined, deferred)
- **Action rate:** % of feedback that influenced a product decision
- **Customer satisfaction with feedback process:** Survey annually
```

### 3. Quality Checklist

```
## Feedback Loop Checklist

- [ ] All feedback channels feed into one central system
- [ ] Tagging taxonomy is documented and consistently applied
- [ ] Weekly pattern review is on the calendar
- [ ] Monthly prioritization session is scheduled
- [ ] Communication templates exist for received, building, shipped, and declined
- [ ] Customers hear back on their feedback within one business day
- [ ] Public transparency mechanism exists (roadmap, blog, changelog labels)
- [ ] Loop health metrics are tracked monthly
- [ ] Declined feedback includes a reason (never just silence)
- [ ] Feedback that ships is celebrated and attributed
```

---

## Example

**Monthly "What We Heard" email excerpt:**
"This month, we reviewed 83 pieces of feedback from 47 unique users. The top theme was invoice customization — 12 of you asked for custom branding on invoices. We are adding it to the March release. The second most-requested item was bulk actions on the dashboard. That is now in our Q2 plan. Three requests for Xero integration were declined for now — we are focusing on QuickBooks depth before adding new integrations."

---

## Anti-Patterns

- **Collecting without responding** — the fastest way to kill feedback is to ignore it. Acknowledge everything, even if briefly.
- **Building everything requested** — feedback informs decisions; it does not make them. You still need strategic direction.
- **Single-channel bias** — if you only read support tickets, you only hear from frustrated users. Diversify collection channels.
- **No decline path** — saying nothing to declined requests is worse than saying no. Always close the loop.
- **Feedback hoarding** — sitting on months of unreviewed feedback creates a backlog that becomes useless. Process weekly.

---

## Recovery

- **Overwhelmed by feedback volume:** Automate tagging where possible. Focus the weekly review on the top 10 themes, not every individual item.
- **Users do not give feedback:** Make it easier — reduce the form to one field. Proactively ask during support interactions.
- **Feedback is mostly complaints:** Actively solicit positive feedback too. Ask what users love, not just what is broken.
- **Team ignores the feedback data:** Tie feedback themes to revenue and retention metrics. Business impact gets attention.
