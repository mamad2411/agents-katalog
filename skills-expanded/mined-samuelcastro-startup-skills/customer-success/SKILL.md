---
name: customer-success
description: Guide founders through customer success strategy including onboarding, support processes, churn prevention, and satisfaction measurement. Use when a founder says "help me design an onboarding flow for new customers", "how do I reduce churn?", "create an NPS survey for my product", "build a customer health scoring system", "help me set up a support ticketing process", "how to improve my customer satisfaction?", "QBR template", "customer success playbook", or asks about retention, customer experience, or building a CS team.
---

# Customer Success

Guide founders from reactive support to proactive customer success—from first customers through building a scalable CS organization.

## Reference Files

- `references/onboarding.md` — Onboarding flows, email sequences, activation checklists
- `references/churn-prevention.md` — Churn analysis frameworks, intervention playbooks, exit surveys
- `references/nps-csat.md` — NPS/CSAT survey templates, follow-up workflows, benchmarks
- `references/health-scoring.md` — Health score models, risk indicators, early warning systems
- `references/support-processes.md` — Support ticketing, escalation paths, QBR templates

## Workflow

### 1. Diagnose Stage & Need

Ask: "Where are you in your customer success journey?"

| Stage | Signals | Focus |
|-------|---------|-------|
| **Early-stage** (1-100 customers) | Founder handles support, no formal processes | → Lightweight onboarding, manual health checks |
| **Growth** (100-500 customers) | Can't personally know every customer | → Systematize onboarding, implement health scoring |
| **Scale** (500+ customers) | Building CS team, need playbooks | → Full CS org, automation, QBRs |

**Primary Need Identification:**

| Need | Signals | Next Step |
|------|---------|-----------|
| **Onboarding** | "Customers don't activate", "time to value is long" | → Step 2: Onboarding |
| **Churn** | "Customers leaving", "high churn rate", "why are we losing customers?" | → Step 3: Churn Prevention |
| **Satisfaction** | "Need NPS", "measure satisfaction", "customer feedback" | → Step 4: NPS & CSAT |
| **Health Scoring** | "Predict at-risk customers", "proactive CS" | → Step 5: Health Scoring |
| **Support** | "Support process", "ticketing", "QBRs" | → Step 6: Support & QBRs |

### 2. Onboarding

Transform new customers into successful, activated users. See `references/onboarding.md` for complete templates.

#### Onboarding Framework

**The Goal:** Deliver first value as fast as possible.

```
Signup → First Value Moment → Habit Formation → Expansion
         (Time-to-value)       (Stickiness)      (Growth)
```

**Define Your Activation Moment:**

| Business Type | Typical Activation | Why |
|---------------|-------------------|-----|
| B2B SaaS | First workflow completed | Core value realized |
| Collaboration tool | Team member invited | Network effect |
| Analytics | First report generated | Insight delivered |
| Marketplace | First transaction | Both sides connected |

#### Onboarding Stages

| Stage | Goal | Timeframe | Key Actions |
|-------|------|-----------|-------------|
| **Welcome** | Set expectations | Day 0 | Welcome email, account setup |
| **Setup** | Configure product | Day 1-3 | Core settings, integrations |
| **Activation** | Reach first value | Day 3-7 | Guided workflow, first success |
| **Engagement** | Build habit | Day 7-30 | Feature education, check-ins |
| **Expansion** | Deepen usage | Day 30+ | Advanced features, team growth |

#### Stage-Appropriate Onboarding

**Early-Stage (Manual, High-Touch):**
- Personal welcome call for every customer
- White-glove setup assistance
- Direct founder/CEO communication
- Learn what customers actually need

**Growth (Hybrid):**
- Self-serve for SMB, high-touch for enterprise
- Automated email sequences with personal check-ins
- In-app guidance (tooltips, checklists)
- Segment by customer size/value

**Scale (Automated with Exceptions):**
- Fully automated self-serve onboarding
- Tech-touch for most, high-touch for strategic accounts
- CSM assignment based on ARR threshold
- Onboarding metrics dashboard

#### Onboarding Email Sequence

| Email | Timing | Purpose | Key Elements |
|-------|--------|---------|--------------|
| **Welcome** | Immediately | Confirm, set expectations | Login link, what's next, support contact |
| **Quick Win** | Day 1 | Drive first action | One specific task to complete |
| **Setup Help** | Day 3 | Remove friction | Common setup issues, FAQ link |
| **Activation Push** | Day 5 | Drive to value moment | "Here's what successful users do first" |
| **Check-in** | Day 7 | Personal touch | "How's it going? Questions?" |
| **Feature Intro** | Day 14 | Deepen engagement | One underused feature |
| **Success Story** | Day 21 | Social proof | Customer similar to them |
| **Expansion** | Day 30 | Grow usage | Team features, advanced use cases |

#### Onboarding Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| **Time to First Value** | Days from signup to activation | <7 days (SaaS) |
| **Activation Rate** | Users reaching activation / Total signups | >60% |
| **Onboarding Completion** | Users completing all steps / Total signups | >80% |
| **Day 7 Retention** | Active day 7 / Total signups | >40% (B2B) |

### 3. Churn Prevention

Stop customers before they leave. See `references/churn-prevention.md` for intervention playbooks.

#### Understanding Churn

**Types of Churn:**

| Type | Cause | Prevention |
|------|-------|------------|
| **Voluntary** | Customer decides to leave | Value delivery, engagement |
| **Involuntary** | Payment failure | Dunning emails, payment recovery |
| **Downgrade** | Reduced spend | Demonstrate value, right-size plans |

**Churn Timing Patterns:**

| When | Likely Cause | Intervention |
|------|--------------|--------------|
| **First 30 days** | Poor onboarding, no value found | Activation focus, onboarding calls |
| **At renewal** | Didn't see ROI | QBR before renewal, value recap |
| **After price increase** | Price/value mismatch | Communicate value, offer options |
| **After champion leaves** | Relationship-dependent | Multi-thread contacts |

#### Churn Analysis Framework

**Step 1: Calculate Churn Rate**

```
Monthly Logo Churn = Customers lost / Customers at start of month
Monthly Revenue Churn = MRR lost / MRR at start of month
Net Revenue Retention = (MRR at end + expansion - churn) / MRR at start
```

**Step 2: Segment Churn**

Analyze churn by:
- Customer segment (SMB/Mid/Enterprise)
- Tenure (first 90 days vs. established)
- Acquisition channel
- Plan type
- Use case / vertical

**Step 3: Identify Patterns**

| Question | What It Reveals |
|----------|----------------|
| When do they churn? | Onboarding vs. renewal problem |
| Who churns? | Segment fit issues |
| What predicts churn? | Leading indicators |
| Why do they say they're leaving? | Root cause |

#### Churn Intervention Playbook

| Risk Level | Indicators | Action | Owner |
|------------|------------|--------|-------|
| **Critical** | Cancellation request, angry ticket | Same-day call, escalate | CS Leader |
| **High** | Usage dropped >50%, no login 14+ days | Outreach within 24h | CSM |
| **Medium** | Usage declining, support tickets up | Automated + personal touch | CSM/Automated |
| **Low** | Minor engagement dip | Automated nurture | Automated |

#### Exit Survey

When customers churn, learn why:

**Exit Survey Questions:**
1. What was your primary reason for canceling? (Required, single select)
   - Found a better alternative
   - Too expensive
   - Missing features we needed
   - Didn't use it enough
   - Poor customer support
   - Company/budget changes
   - Other

2. What could we have done differently? (Optional, open text)

3. Would you consider us again in the future? (Required, Yes/No/Maybe)

4. How likely are you to recommend us to others? (NPS scale)

### 4. NPS & CSAT

Measure and improve customer satisfaction. See `references/nps-csat.md` for survey templates.

#### NPS (Net Promoter Score)

**The Question:**
> "On a scale of 0-10, how likely are you to recommend [Product] to a friend or colleague?"

**Scoring:**
- **Promoters (9-10):** Loyal enthusiasts who refer others
- **Passives (7-8):** Satisfied but vulnerable to competition
- **Detractors (0-6):** Unhappy customers who can damage brand

**NPS Calculation:**
```
NPS = % Promoters - % Detractors
Range: -100 to +100
```

**NPS Benchmarks:**

| NPS Score | Rating | Context |
|-----------|--------|---------|
| 70+ | World-class | Top companies (Apple, USAA) |
| 50-69 | Excellent | Strong customer loyalty |
| 30-49 | Good | Healthy, room to improve |
| 0-29 | Needs work | More detractors than ideal |
| Negative | Critical | Urgent action needed |

**B2B SaaS NPS Benchmarks:**

| Segment | Median | Top Quartile |
|---------|--------|--------------|
| SMB | 30 | 50+ |
| Mid-market | 35 | 55+ |
| Enterprise | 40 | 60+ |

#### CSAT (Customer Satisfaction Score)

**The Question:**
> "How satisfied are you with [specific interaction/product]?"

Scale: 1-5 or 1-7

**CSAT Calculation:**
```
CSAT = (Satisfied responses / Total responses) × 100
"Satisfied" = top 2 scores (4-5 on 5-point scale)
```

**When to Use Each:**

| Metric | Best For | Timing |
|--------|----------|--------|
| **NPS** | Overall relationship, loyalty | Quarterly, after key milestones |
| **CSAT** | Specific interactions | After support ticket, after onboarding |
| **CES** | Ease of experience | After specific task completion |

#### NPS Survey Implementation

**Timing Strategy:**

| Trigger | Rationale |
|---------|-----------|
| **Quarterly** | Regular pulse on relationship |
| **Post-onboarding** (Day 30) | Measure first impression |
| **Post-support resolution** | Measure support quality |
| **Pre-renewal** (60 days out) | Identify at-risk before too late |

**Follow-up Questions (by segment):**

For **Promoters (9-10):**
> "What do you love most about [Product]?"
> "Would you be open to leaving a review or being a reference?"

For **Passives (7-8):**
> "What would make you rate us higher?"
> "What's one thing we could improve?"

For **Detractors (0-6):**
> "We're sorry to hear that. What's the main reason for your score?"
> "What would it take to improve your experience?"

#### NPS Follow-up Workflow

| Segment | Response SLA | Action | Owner |
|---------|--------------|--------|-------|
| **Detractors** | 24 hours | Personal call, understand issue | CSM/CS Leader |
| **Passives** | 48 hours | Email follow-up, gather feedback | CSM |
| **Promoters** | 1 week | Thank you, referral/review ask | CSM/Marketing |

### 5. Customer Health Scoring

Predict and prevent churn before it happens. See `references/health-scoring.md` for detailed models.

#### Health Score Components

Build a composite score from multiple signals:

| Category | Weight | Signals |
|----------|--------|---------|
| **Product Usage** | 40% | Login frequency, feature adoption, breadth of use |
| **Engagement** | 25% | Support tickets, NPS responses, event attendance |
| **Relationship** | 20% | Executive sponsor, champion strength, multi-threading |
| **Financial** | 15% | Payment history, contract value, expansion potential |

#### Simple Health Score Model

**For Early-Stage (Spreadsheet-Based):**

| Dimension | Red (0 pts) | Yellow (1 pt) | Green (2 pts) |
|-----------|-------------|---------------|---------------|
| **Login Frequency** | No login 14+ days | 1-2x/week | 3+ times/week |
| **Feature Adoption** | Only 1 feature | 2-3 features | 4+ features |
| **Support Sentiment** | Negative tickets | Neutral | Positive/none |
| **Stakeholder Access** | No response | Single contact | Multi-contact |
| **NPS Score** | Detractor | Passive | Promoter |

**Score Interpretation:**
- 8-10: Healthy (Green)
- 5-7: Needs attention (Yellow)
- 0-4: At risk (Red)

#### Stage-Appropriate Health Scoring

**Early-Stage (1-100 customers):**
- Manual health check spreadsheet
- Gut feel + basic usage data
- Review weekly with founder
- Focus on learning patterns

**Growth (100-500 customers):**
- Simple scoring model in CRM
- Automated alerts for red accounts
- Weekly health review meeting
- Start documenting playbooks

**Scale (500+ customers):**
- Automated health scoring platform
- ML-based churn prediction
- Real-time dashboards
- Tiered response playbooks

#### Acting on Health Scores

| Health | Action | Frequency | Goal |
|--------|--------|-----------|------|
| **Green** | Expansion focus | Quarterly QBR | Grow and advocate |
| **Yellow** | Engagement boost | Bi-weekly check-in | Return to green |
| **Red** | Intervention | Immediate | Save or learn |

### 6. Support Processes & QBRs

Build support systems that scale. See `references/support-processes.md` for templates.

#### Support Tier Structure

| Tier | Handles | Response Time | Escalation |
|------|---------|---------------|------------|
| **Tier 1** | FAQs, how-to, basic issues | <4 hours | Can't resolve in 1 interaction |
| **Tier 2** | Technical issues, bugs | <8 hours | Requires engineering |
| **Tier 3** | Engineering escalation | <24 hours | Product decisions needed |

#### Support Metrics

| Metric | Definition | Target |
|--------|------------|--------|
| **First Response Time** | Time to first human reply | <4 hours (business) |
| **Resolution Time** | Time to fully resolve | <24 hours (Tier 1) |
| **First Contact Resolution** | % resolved in one interaction | >70% |
| **CSAT (Support)** | Post-ticket satisfaction | >90% |
| **Ticket Volume per Customer** | Tickets / Active customers | Decreasing trend |

#### QBR (Quarterly Business Review)

**Purpose:** Demonstrate value, align on goals, identify expansion.

**QBR Agenda (60 min):**

| Section | Time | Content |
|---------|------|---------|
| **Business Update** | 5 min | Their company news, priorities |
| **Usage & Value** | 15 min | Metrics, ROI achieved |
| **Wins & Challenges** | 10 min | What's working, what's not |
| **Product Roadmap** | 10 min | Relevant upcoming features |
| **Goals & Action Plan** | 15 min | Next quarter objectives |
| **Expansion Discussion** | 5 min | Growth opportunities |

**QBR Preparation Checklist:**
- [ ] Usage data and trends pulled
- [ ] ROI/value metrics calculated
- [ ] Support ticket summary reviewed
- [ ] Renewal date confirmed
- [ ] Expansion opportunities identified
- [ ] Stakeholder list updated
- [ ] Previous QBR action items reviewed

#### When to Start QBRs

| Customer Segment | QBR Frequency | Delivery |
|------------------|---------------|----------|
| **Enterprise** ($100K+) | Quarterly | In-person or video |
| **Mid-market** ($25-100K) | Bi-annually | Video call |
| **SMB** (<$25K) | Annually or trigger-based | Email summary |

### 7. Building a CS Team

**When to Hire First CSM:**
- [ ] 50+ customers
- [ ] Founder can't personally manage all relationships
- [ ] Churn is becoming a problem
- [ ] Clear patterns in what makes customers successful

**CSM-to-Account Ratios:**

| Segment | Ratio | Why |
|---------|-------|-----|
| **Enterprise** | 1:10-20 | High-touch required |
| **Mid-market** | 1:30-50 | Balanced touch |
| **SMB** | 1:100-200 | Tech-touch + pooled |

**First CS Hire Profile:**
- Previous startup experience at similar stage
- Can build process, not just follow it
- Strong communication + empathy
- Comfortable with ambiguity
- Technical enough to understand product

## Deliverables

### 1. Onboarding Email Sequence
Create using `docx` skill:
- 6-8 email sequence with timing
- Subject lines and body copy
- Personalization placeholders
- Success metrics to track

### 2. Onboarding Checklist
Create using `xlsx` skill:
- Step-by-step activation checklist
- Owner assignments
- Timeline targets
- Completion tracking

### 3. Churn Analysis Framework
Create as markdown:
- Churn calculation formulas
- Segmentation dimensions
- Analysis template
- Intervention triggers

### 4. NPS Survey + Workflow
Create using `docx` skill:
- Survey questions
- Follow-up sequences by segment
- Response SLAs
- Reporting template

### 5. Customer Health Scorecard
Create using `xlsx` skill:
- Scoring dimensions and weights
- Red/yellow/green thresholds
- Account list with scores
- Action triggers

### 6. QBR Template
Create using `pptx` skill:
- 8-10 slide deck template
- Agenda and discussion guide
- Metrics dashboard slide
- Action plan format

### 7. Support Process Document
Create using `docx` skill:
- Tier definitions and escalation paths
- Response time SLAs
- Ticket categorization
- Metrics and reporting

## Anti-Patterns

**Onboarding Mistakes:**
- No defined activation moment (unclear success)
- Same onboarding for all customers (one-size-fits-none)
- Too many emails too fast (overwhelm)
- No measurement (can't improve what you don't track)

**Churn Prevention Mistakes:**
- Reactive only (waiting for cancellation request)
- Not segmenting churn (treating all churn the same)
- No exit interviews (missing root causes)
- Focusing on save rate, not prevention

**NPS Mistakes:**
- Survey fatigue (too frequent)
- No follow-up on responses (especially detractors)
- Gaming the score (only surveying happy customers)
- NPS as only metric (missing context)

**Health Score Mistakes:**
- Too complex initially (analysis paralysis)
- Not acting on scores (dashboard without action)
- Static thresholds (not updating as you learn)
- Missing qualitative signals (relationship quality)

**Support Mistakes:**
- No SLAs defined (inconsistent experience)
- No escalation path (tickets stuck in limbo)
- Not connecting support to product (missing feedback loop)
- Measuring volume, not quality

## Integration with Other Skills

- Use `product` skill for feature prioritization from CS feedback
- Use `growth-analytics` skill for retention metrics and cohort analysis
- Use `sales` skill for handoff process from sales to CS
- Use `operations` skill for CS team OKRs and hiring
- Use `business-model` skill for LTV/CAC and expansion revenue
- Use `docx` skill for process documentation and playbooks
- Use `xlsx` skill for health scorecards and metrics tracking
- Use `pptx` skill for QBR decks

---

*Adapted from [Linas Beliūnas's](https://linas.substack.com/p/onepersonunicorn) **The One-Person Unicorn** founder skill set.*
