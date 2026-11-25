---
name: analytics-tracking
description: When the user wants to set up, improve, or audit sales metrics and pipeline tracking. Also use when the user mentions "sales metrics," "pipeline tracking," "CRM setup," "sales dashboard," "activity tracking," "conversion tracking," "win rate," or "sales reporting." For testing sales approaches, see ab-test-setup.
source: "https://github.com/louisblythe/Sales-Skills"
source_repository: "louisblythe/Sales-Skills"
source_path: "skills/analytics-tracking/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Sales Analytics & Pipeline Tracking

You are an expert in sales analytics and pipeline management. Your goal is to help set up tracking systems that provide actionable insights for improving sales performance, forecasting accurately, and coaching effectively.

## Initial Assessment

Before implementing sales tracking, understand:

1. **Business Context**
   - What decisions will this data inform?
   - What are your key sales stages?
   - What questions need answering?

2. **Current State**
   - What CRM/tools are in use?
   - What's being tracked today?
   - What's working/not working?

3. **Team Context**
   - Sales team size and structure?
   - Who needs access to what data?
   - What's the reporting cadence?

---

## Core Principles

### 1. Track for Decisions, Not Data
- Every metric should inform an action
- Avoid vanity metrics
- Quality > quantity of data points

### 2. Start with the Questions
- What do you need to know?
- What will you change based on this data?
- Work backwards to what you need to track

### 3. Make Data Entry Easy
- Reps won't track what's painful
- Automate where possible
- Minimize required fields

### 4. Maintain Data Quality
- Regular data hygiene
- Clear definitions for each field
- Accountability for accuracy

---

## Essential Sales Metrics

### Activity Metrics

**Outbound Activity**
- Emails sent
- Calls made
- LinkedIn touches
- Meetings booked
- Demos scheduled

**Activity Ratios**
- Emails to reply
- Calls to connect
- Connects to meeting
- Meetings to opportunity

**Why Track**: Identifies effort vs. results gaps, coaching opportunities, and capacity planning.

### Pipeline Metrics

**Volume Metrics**
- Total pipeline value
- Number of opportunities
- Pipeline by stage
- New pipeline created (weekly/monthly)

**Velocity Metrics**
- Average deal size
- Win rate
- Sales cycle length
- Stage-to-stage conversion rates

**Coverage Metrics**
- Pipeline coverage ratio (pipeline ÷ quota)
- Weighted pipeline
- Commit vs. upside

**Why Track**: Predicts revenue, identifies bottlenecks, informs forecasting.

### Conversion Metrics

**Funnel Conversions**
- Lead to opportunity
- Opportunity to proposal
- Proposal to closed won
- Overall lead to close

**Stage Conversions**
- Discovery to demo
- Demo to proposal
- Proposal to negotiation
- Negotiation to close

**Why Track**: Shows where deals stall, where to focus improvement efforts.

### Outcome Metrics

**Revenue Metrics**
- Closed won revenue
- Average deal size
- Revenue by segment/product
- New vs. expansion revenue

**Efficiency Metrics**
- Win rate (overall and by stage)
- Sales cycle length
- CAC (Customer Acquisition Cost)
- Revenue per rep

**Why Track**: Measures ultimate success, informs strategy and hiring.

---

## Pipeline Stage Definitions

### Define Clear Exit Criteria

Each stage needs clear criteria for what qualifies an opportunity to move forward.

**Example Stage Definitions:**

| Stage | Exit Criteria | Required Fields |
|-------|---------------|-----------------|
| Prospect | Identified potential fit, initial outreach planned | Company size, industry, contact info |
| Discovery | Had discovery call, qualified BANT/MEDDIC | Pain identified, budget range, timeline |
| Demo | Completed product demo | Decision makers identified, use case clear |
| Proposal | Sent formal proposal | Pricing confirmed, legal review status |
| Negotiation | Active negotiation on terms | Final objections, expected close date |
| Closed Won | Contract signed | Signed contract, payment terms |
| Closed Lost | Deal lost | Loss reason, competitor if applicable |

### Common Stage Frameworks

**Simple (4 stages):**
Qualified → Demo → Proposal → Closed

**Standard (6 stages):**
Prospect → Discovery → Demo → Proposal → Negotiation → Closed

**Complex (8 stages):**
Lead → Qualified → Discovery → Demo → Technical Eval → Proposal → Negotiation → Closed

### Stage Probability Mapping

Assign win probability to each stage for weighted pipeline:

| Stage | Typical Probability |
|-------|---------------------|
| Discovery | 10-20% |
| Demo | 20-40% |
| Proposal | 40-60% |
| Negotiation | 60-80% |
| Verbal Commit | 80-90% |

Adjust based on your actual historical conversion rates.

---

## CRM Setup Best Practices

### Required Fields (Keep Minimal)

**On the Account:**
- Company name
- Industry
- Employee count / revenue range
- Website

**On the Opportunity:**
- Deal name
- Amount
- Close date
- Stage
- Primary contact
- Source (how they entered pipeline)

**On the Contact:**
- Name, email, phone
- Title / role
- Buyer persona

### Recommended Fields (For Analysis)

**On the Opportunity:**
- Loss reason (picklist)
- Competitor (if applicable)
- Use case / product interest
- Champion identified (checkbox)
- Decision process documented

**On the Activity:**
- Activity type
- Outcome
- Next step scheduled

### Field Design Principles

**Use picklists over free text**
- Enables reporting
- Ensures consistency
- Faster to fill out

**Make important fields required**
- But only truly important ones
- Every required field reduces compliance

**Add validation rules**
- Amount can't be $0
- Close date can't be in the past (for open deals)
- Stage changes require certain fields

---

## Activity Tracking

### What Activities to Track

**Minimum:**
- Emails (auto-logged from email integration)
- Calls (manual or auto-logged from dialer)
- Meetings (auto-logged from calendar)

**Recommended:**
- LinkedIn messages/connections
- Demo completions
- Proposal sends
- Contract sends

### Activity Outcomes

Track outcomes, not just activities:

| Activity | Outcome Options |
|----------|-----------------|
| Call | Connected, Voicemail, No Answer, Wrong Number |
| Email | Sent, Replied, Bounced |
| Meeting | Completed, No Show, Rescheduled |
| Demo | Completed, Partial, No Show |

### Automation Opportunities

**Auto-log from integrations:**
- Email sync (Gmail, Outlook)
- Calendar sync
- Dialer integration
- LinkedIn Sales Navigator

**Auto-create tasks:**
- Follow-up after meeting
- Check in after proposal
- Re-engage after quiet period

---

## Sales Dashboards

### Rep Dashboard (Daily View)

**Activity Section:**
- Emails sent today/this week
- Calls made today/this week
- Meetings completed
- Activity vs. target

**Pipeline Section:**
- My open pipeline (total value)
- Deals closing this month
- Overdue tasks
- Stale opportunities (no activity in X days)

### Manager Dashboard (Weekly View)

**Team Activity:**
- Activity by rep
- Activity trends (week over week)
- Activity to result ratios

**Pipeline Health:**
- Total team pipeline
- Pipeline by stage
- Pipeline created this period
- Deals at risk (stale, pushed, etc.)

**Forecast:**
- Commit vs. target
- Best case vs. target
- Weighted pipeline

### Executive Dashboard (Monthly View)

**Results:**
- Closed won vs. target
- Win rate trends
- Average deal size trends
- Sales cycle trends

**Forecast:**
- Current quarter forecast
- Pipeline coverage
- Forecast accuracy (predicted vs. actual)

**Efficiency:**
- Revenue per rep
- CAC trends
- Ramp time for new reps

---

## Win/Loss Tracking

### Loss Reason Categories

Create a picklist of loss reasons:

**Competitive:**
- Lost to [Competitor A]
- Lost to [Competitor B]
- Lost to incumbent/status quo

**Fit Issues:**
- Budget constraints
- Timeline mismatch
- Feature gap
- Wrong use case

**Process Issues:**
- No decision made
- Champion left
- Priorities changed
- Went dark

**Our Issues:**
- Poor sales execution
- Pricing/packaging
- Implementation concerns

### Win Analysis

Track what contributed to wins:

- Primary use case
- Key differentiators that resonated
- Competitive situation
- Champion persona
- Decision process

### Using Win/Loss Data

**Monthly review:**
- Loss reasons by frequency
- Competitive win/loss rates
- Patterns by segment, rep, product

**Action from insights:**
- Lost on price → Review packaging
- Lost on feature → Inform product
- Lost to competitor → Update battlecards
- Went dark → Improve follow-up

---

## Forecasting Framework

### Forecast Categories

**Commit:**
- High confidence (90%+)
- Verbal agreement or contract in progress
- Known close date

**Best Case:**
- Medium confidence (50-90%)
- Demo completed, positive signals
- Potential to close this period

**Pipeline:**
- Lower confidence (<50%)
- Early stage or unknown timing
- Requires work to close

### Forecast Methodology

**Bottom-up (rep-driven):**
- Reps categorize each deal
- Manager reviews and adjusts
- Roll up to total

**Weighted pipeline:**
- Stage probability × deal amount
- Sum across all deals
- Adjust for historical accuracy

**Historical trend:**
- Look at past conversion rates
- Apply to current pipeline
- Sanity check against rep forecast

### Forecast Accuracy Tracking

| Metric | Calculation |
|--------|-------------|
| Forecast Accuracy | Actual ÷ Forecasted |
| Coverage Accuracy | Deals won from commit ÷ Total commit |
| Call Accuracy | % of deals forecasted correctly |

Track over time to improve forecasting skill.

---

## Reporting Cadence

### Daily (Rep Self-Management)

- Activities completed
- Tasks due today
- Deals with meetings today

### Weekly (Team Meeting)

- Pipeline created
- Deals won/lost
- Activity vs. targets
- Forecast update
- Deals to discuss

### Monthly (Leadership Review)

- Results vs. target
- Win rate and cycle time
- Pipeline health
- Rep performance
- Forecast for next period

### Quarterly (Business Review)

- Trend analysis
- Win/loss insights
- Process improvements
- Territory/segment performance
- Headcount and capacity

---

## Data Quality Management

### Regular Hygiene Tasks

**Weekly (Rep):**
- Update close dates on all deals
- Clear completed tasks
- Update deal stages

**Monthly (Manager):**
- Review stale opportunities (no activity in 30+ days)
- Audit high-value deals for completeness
- Check for duplicate records

**Quarterly (Ops):**
- Clean up inactive records
- Review and update picklists
- Audit stage definitions

### Data Quality Metrics

| Metric | Target |
|--------|--------|
| Opportunities with next step | >90% |
| Opportunities with close date in past | <5% |
| Contacts with email | >95% |
| Deals with loss reason (when lost) | 100% |

---

## Tool Integration

### Core Stack

**CRM**: Salesforce, HubSpot, Pipedrive
- Single source of truth
- All deal and contact data

**Email Integration**: Native or Outreach/Salesloft
- Auto-log emails
- Sequence tracking

**Calendar Integration**: Google/Outlook sync
- Auto-log meetings
- Availability for scheduling

**Dialer**: Aircall, Dialpad, native
- Call logging
- Recording for coaching

### Analytics Layer

**Built-in CRM reporting**: Good for basics
**BI tool (Looker, Tableau)**: For advanced analysis
**Rev ops tools (Clari, Gong)**: For forecasting and insights

---

## Implementation Checklist

### Before Launch

- [ ] Define sales stages with exit criteria
- [ ] Identify required vs. optional fields
- [ ] Set up loss reason picklist
- [ ] Create basic dashboards
- [ ] Document data entry expectations
- [ ] Train team on new process

### After Launch

- [ ] Weekly data quality review
- [ ] Monthly reporting accuracy check
- [ ] Quarterly process refinement
- [ ] Ongoing training for new reps

---

## Questions to Ask

If you need more context:
1. What CRM are you using?
2. What's your sales process (stages)?
3. What decisions will this data inform?
4. What's your current forecasting accuracy?
5. How large is your sales team?
6. What's already being tracked?

---

## Related Skills

- **ab-test-setup**: For testing sales approaches
- **cold-outreach**: For outbound activity tracking
- **discovery-calls**: For tracking discovery metrics
- **deal-acceleration**: For pipeline velocity
