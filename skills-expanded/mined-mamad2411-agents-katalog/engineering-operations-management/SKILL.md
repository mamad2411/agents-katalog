# Engineering Operations Management Skill

**For managers running SRE, platform, and infrastructure teams - focusing on operations, on-call, incidents, and engineering metrics.**

> This skill helps engineering managers build sustainable operations practices, prevent burnout, run effective incident reviews, and measure what matters. Complements technical SRE skills with people and process management.

---
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 SKILL ACTIVATED: engineering-operations-management
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


## When to Use This Skill

**You're a manager who needs help with:**
- Structuring on-call rotations and compensation
- Preventing and addressing engineer burnout
- Running blameless postmortem reviews
- Negotiating SLOs with product teams
- Measuring engineering productivity (not vanity metrics)
- Managing toil and operational load
- Balancing feature work vs operational excellence
- Building sustainable operations culture

**This skill does NOT cover:**
- Hands-on incident response (see **sre** skill)
- Technical SLO/SLI implementation (see **sre** skill)
- Monitoring/observability setup (see **platform-engineering** skill)
- Team hiring and career development (see **engineering-management** skill)

---

## Core Areas

### 1. On-Call Management

**Core principle:** On-call is a necessary operational burden that should be **fair, sustainable, and compensated**.

#### On-Call Rotation Models

**Follow-the-Sun (Recommended for global teams):**
```
Americas Team:     6 AM - 2 PM PST (primary)
EMEA Team:         2 PM - 10 PM PST (primary)
APAC Team:        10 PM - 6 AM PST (primary)

Pros: No one wakes up at night, balanced load
Cons: Requires global team, handoff complexity
Best for: Teams with 15+ engineers across timezones
```

**Weekly Rotation (Most common):**
```
Week 1: Engineer A (primary), Engineer B (secondary)
Week 2: Engineer C (primary), Engineer D (secondary)
Week 3: Engineer E (primary), Engineer A (secondary)

Pros: Simple, fair rotation
Cons: Weekend coverage, potential burnout
Best for: Teams with 6-10 engineers in same timezone
```

**Tiered Escalation:**
```
Tier 1: Junior engineers (business hours only)
Tier 2: Senior engineers (24/7 primary)
Tier 3: Staff/Principal (escalation only)

Pros: Gradual responsibility increase
Cons: Can create "us vs them" dynamic
Best for: Large teams (15+) with clear skill levels
```

#### On-Call Compensation Models

**Option 1: On-Call Stipend**
```
Primary on-call: $500-$1,000/week
Secondary on-call: $250-$500/week

Pros: Predictable, simple
Cons: Doesn't account for actual pages
```

**Option 2: Pay-per-Page**
```
Business hours page: $50-$100
After-hours page: $150-$300
Weekend/holiday page: $300-$500

Pros: Fair - pays for actual disruption
Cons: Can incentivize ignoring issues
```

**Option 3: Hybrid (Recommended)**
```
Base stipend: $500/week
+ $100 per after-hours page
+ Comp time (1.5x hours worked after-hours)

Pros: Covers both availability and interruptions
Cons: More complex to administer
```

**Comp time policies:**
- For every hour worked after-hours, grant 1.5 hours comp time
- Comp time must be used within 30 days
- Encourage taking comp time day-after major incidents

#### Burnout Prevention

**Warning signs:**
- 🚨 Pages > 5 per week for extended period
- 🚨 Engineer mentions exhaustion, stress in 1-on-1s
- 🚨 Quality of work declining
- 🚨 Working late nights/weekends regularly
- 🚨 Cynicism, disengagement

**Interventions:**
1. **Immediate:** Rotate off on-call for 2-4 weeks
2. **Short-term:** Reduce project load, pair with senior engineer
3. **Long-term:** Fix underlying system issues causing pages

**Sustainable on-call rules:**
- No engineer on-call more than 1 week per month
- Maximum 2 weeks on-call per quarter
- Mandatory break after high-page-volume week
- No on-call during PTO or major life events

#### On-Call Scenarios

**Scenario: "What's a fair after-hours pay model?"**
- **Hybrid model (recommended):**
  - Base: $500/week on-call stipend
  - Plus: $100-150 per after-hours page
  - Plus: 1.5x comp time for hours worked
- **Example calculation:**
  - Week stipend: $500
  - 3 after-hours pages × $125 = $375
  - 4 hours worked × 1.5 = 6 hours comp time
  - **Total value:** $875 + 6 hours off

**Scenario: "Team blamed someone in incident review - how to fix?"**
- **Immediate:** Stop the review, reset the tone
- **Say:** "We don't blame people, we fix systems. Let's focus on what failed, not who."
- **Blameless culture principles:**
  - People make reasonable decisions based on information available
  - Systems should prevent single points of failure
  - Focus on "what" not "who"
- **Follow-up:** Coach manager running review on blameless principles

**Scenario: "During incident, what should I do as manager?"**
- **Monitor:** Watch incident channel, don't interrupt
- **Support:** "What do you need? More people? Communication handled?"
- **Shield:** Handle exec questions, keep pressure off team
- **Don't:** Take over, second-guess, or ask "why" questions mid-incident
- **After:** Thank team, schedule postmortem, ensure comp time taken

**Scenario: "How do we track incident trends?"**
- **Metrics to track:**
  - Incident frequency (per week/month)
  - MTTR (mean time to recovery)
  - Incidents by service/component
  - Incidents by root cause category
- **Look for patterns:**
  - Same service failing repeatedly → systemic issue
  - MTTR increasing → lack of familiarity or tooling gaps
  - Spike in incidents → recent deploy or infrastructure change
- **Action:** Address top 3 incident sources quarterly

**Scenario: "What incident communication plan do we need?"**
- **During incident:**
  - Sev 1: Updates every 30 minutes to execs, status page every 15 min
  - Sev 2: Updates every hour to stakeholders
  - Sev 3: Update when resolved
- **Channels:**
  - Internal: Dedicated Slack #incidents channel
  - External: Status page (Statuspage.io, etc.)
  - Executives: Email + Slack DM for Sev 1/2
- **Template:**
  ```
  [SEV 1] API Service Outage
  Impact: All users unable to login
  Status: Investigating
  Next update: 2:30 PM (15 minutes)
  ```

**Scenario: "What's the right retrospective format?"**
- **Timeline:** Within 48 hours of incident (while fresh)
- **Attendees:** Incident responders + anyone interested (open invitation)
- **Duration:** 45-60 minutes
- **Format:**
  1. Timeline walkthrough (10 min)
  2. What went well (10 min)
  3. What went poorly (15 min)
  4. Action items (15 min) - with owners and due dates
  5. Q&A (10 min)
- **Output:** Written postmortem + action items tracked

**Scenario: "How do we communicate incidents to executives?"**
- **During:** Brief, factual updates
  - "API down, 100% of users affected, team investigating"
- **After:** Business-focused summary
  - Revenue impact: "$50K in lost sales"
  - User impact: "10K users couldn't check out for 2 hours"
  - Prevention: "Adding rate limiting to prevent recurrence"
- **Avoid:** Deep technical details unless asked

---

### 2. Incident Management for Managers

**Your role as a manager during incidents:**

#### During the Incident (DO NOT take over unless critical)

```
✅ DO:
- Monitor incident channel, offer support
- Shield team from external pressure
- Bring in additional engineers if needed
- Coordinate with stakeholders (updates to execs)
- Order food if it's going long
- Take notes for postmortem

❌ DON'T:
- Take over incident response (unless you're most qualified)
- Ask "why didn't you..." questions during incident
- Pressure for faster resolution
- Blame individuals
- Second-guess decisions being made
```

**Incident Severity Levels (align with team):**

```
Sev 1 (Critical):
├── Complete service outage
├── Data loss or security breach
├── Revenue impact > $10K/hour
└── Response: All hands, exec updates every 30 min

Sev 2 (High):
├── Major feature degraded
├── Significant user impact
├── Revenue impact > $1K/hour
└── Response: On-call + expert, updates every hour

Sev 3 (Medium):
├── Minor feature degraded
├── Limited user impact
└── Response: On-call handles, regular updates

Sev 4 (Low):
├── Internal tooling issue
├── No user impact
└── Response: Fix during business hours
```

#### After the Incident: Blameless Postmortem

**Blameless postmortem framework:**

```
Postmortem Template:

## Incident Summary
- Date/Time: When did it happen?
- Duration: How long?
- Impact: Who was affected? How many users?
- Severity: Sev 1-4

## Timeline
- 14:32 - First alert fired
- 14:35 - Engineer A acknowledged, began investigation
- 14:45 - Root cause identified (database connection pool exhausted)
- 15:00 - Mitigation applied (increased pool size)
- 15:15 - Service fully recovered

## Root Cause
What actually caused this? (Technical, not "Engineer X did...")

## What Went Well
- Alert fired within 2 minutes
- Communication was clear
- Rollback was smooth

## What Went Poorly
- No automated mitigation
- Monitoring didn't catch early warning signs
- On-call engineer not familiar with this service

## Action Items
1. [P0] Add automated connection pool scaling (Owner: Alice, Due: 2 weeks)
2. [P1] Improve monitoring for connection pool saturation (Owner: Bob, Due: 1 month)
3. [P2] Add service to on-call training rotation (Owner: Manager, Due: 2 weeks)

## Lessons Learned
- Database connection pool defaults are too conservative
- Need better pre-production load testing
```

**Blameless postmortem meeting (45-60 min):**

```
1. Introduction (5 min)
   └── Remind: This is blameless, focus on systems not people

2. Timeline Review (15 min)
   └── Walk through what happened, when

3. Root Cause Analysis (15 min)
   └── "Why did this happen?" (ask "why" 5 times)

4. What Went Well / What Went Poorly (10 min)
   └── Balanced reflection

5. Action Items (10 min)
   └── Specific, assigned, with due dates
   └── Priority: P0 (this week), P1 (this month), P2 (nice to have)

6. Close (5 min)
   └── Thank the team, emphasize learning
```

**Red flags in postmortems:**
- ❌ Blaming individuals ("Alice should have...")
- ❌ Vague action items ("Improve monitoring")
- ❌ No follow-up on action items
- ❌ Defensive posturing
- ❌ Skipping postmortems for "small" incidents

**Manager's job:** Enforce blameless culture, track action items, ensure learning.

---

### 3. SLO Negotiation with Product Teams

**The tension:** Product wants features fast. SRE/Platform wants stability. You balance both.

#### Understanding SLOs (Simple Version for Managers)

```
SLI (Service Level Indicator):
What you measure (e.g., "API latency p99")

SLO (Service Level Objective):
Target for reliability (e.g., "API latency p99 < 500ms, 99.9% of the time")

SLA (Service Level Agreement):
Contractual promise to customers (e.g., "99.95% uptime or we give refund")

Example:
SLI: Request success rate
SLO: 99.9% of requests succeed (internal target)
SLA: 99.5% uptime (customer-facing promise)
```

**Error budget concept:**

```
SLO: 99.9% availability = 0.1% allowed downtime

Per month (30 days):
├── Total time: 43,200 minutes
├── Allowed downtime: 43.2 minutes
└── Error budget: 43.2 minutes

If error budget exhausted:
├── Freeze feature releases
├── Focus on reliability improvements
└── Pay down tech debt
```

#### SLO Negotiation Framework

**When product pushes for aggressive feature timeline:**

```
Product: "We need to ship this feature in 2 weeks"

You (as manager):
"Let's check our error budget first. If we have budget, we can move fast.
 If we're out of budget, we need to stabilize first."

Scenario 1: Error budget healthy (50% remaining)
├── ✅ Green light for feature work
├── 70% capacity on features
└── 30% on reliability

Scenario 2: Error budget exhausted (0% remaining)
├── 🛑 Feature freeze
├── 100% capacity on reliability
└── Resume features when budget recovers
```

**How to set SLOs (practical guide):**

1. **Start with current performance:**
   - "Our API latency p99 is currently 300ms"
   - Don't set SLO at 300ms - give yourself buffer

2. **Set realistic target:**
   - "Let's set SLO at p99 < 500ms"
   - This gives 200ms buffer for growth/issues

3. **Align with customer expectation:**
   - "Customers complain if latency > 1s"
   - SLO should prevent customer pain

4. **Review quarterly:**
   - Too easy? (Always meeting SLO) → Tighten SLO or invest in features
   - Too hard? (Always missing SLO) → Loosen SLO or invest in reliability

**Common SLOs by service type:**

```
API Services:
├── Availability: 99.9% (43 min downtime/month)
├── Latency p50: < 100ms
├── Latency p99: < 500ms
└── Error rate: < 0.1%

Batch Processing:
├── Job success rate: 99.5%
├── Job completion time: < 4 hours
└── Data accuracy: 99.99%

Data Pipeline:
├── Data freshness: < 15 min lag
├── Pipeline availability: 99.9%
└── Data quality: 99.95%
```

---

### 4. Engineering Metrics That Matter

**The problem:** Easy to measure vanity metrics. Hard to measure real productivity.

#### Vanity Metrics (Avoid)

```
❌ Lines of code written
❌ Number of commits
❌ Hours worked
❌ Number of deploys (without context)
❌ Ticket velocity (without quality)
❌ Code coverage % (without context)
```

**Why these are bad:**
- Lines of code: Good engineers often delete code
- Number of commits: Encourages small, meaningless commits
- Hours worked: Encourages burnout, not productivity
- Deploys without context: Could be hotfixes for bugs you introduced
- Ticket velocity: Encourages cherry-picking easy tickets
- Code coverage: Can write useless tests to hit %

#### Metrics That Actually Matter

**1. DORA Metrics (Use these)**

```
Deployment Frequency:
├── How often do you deploy to production?
├── Elite: Multiple times per day
├── High: Daily to weekly
├── Medium: Weekly to monthly
└── Low: Monthly to every 6 months

Lead Time for Changes:
├── How long from commit to production?
├── Elite: < 1 hour
├── High: 1 day to 1 week
├── Medium: 1 week to 1 month
└── Low: 1 month to 6 months

Time to Restore Service:
├── How long to recover from incident?
├── Elite: < 1 hour
├── High: < 1 day
├── Medium: 1 day to 1 week
└── Low: > 1 week

Change Failure Rate:
├── What % of changes cause incidents?
├── Elite: 0-15%
├── High: 16-30%
├── Medium: 31-45%
└── Low: > 45%
```

**How to use DORA metrics:**
- Track quarterly, not daily (avoid gaming)
- Trend over time (are we improving?)
- Compare to benchmarks (elite, high, medium, low)
- Use to identify improvement areas

**2. SRE Metrics**

```
Toil Percentage:
├── What % of engineer time is manual ops work?
├── Target: < 30% toil
├── Intervention needed: > 50% toil
└── Measure: Time tracking, surveys

On-Call Load:
├── Pages per week per engineer
├── Target: < 3 pages/week
├── Intervention: > 5 pages/week
└── Measure: PagerDuty analytics

SLO Compliance:
├── Are we meeting our SLOs?
├── Target: 99%+ SLO compliance
└── Measure: Observability dashboards
```

**3. Team Health Metrics**

```
Engineer Satisfaction:
├── Quarterly survey (1-10 scale)
├── Questions: "Satisfied with work?", "Would recommend team?"
├── Target: 8+ average
└── Red flag: < 6 average or declining trend

Retention Rate:
├── % of engineers staying > 1 year
├── Target: > 85% annual retention
└── Red flag: < 70% retention

Time to Productivity (New hires):
├── How long until new hire is productive?
├── Target: < 90 days
└── Measure: Manager assessment + self-assessment
```

**4. Operational Excellence Metrics**

```
Incident Trends:
├── Number of Sev 1/2 incidents per month
├── Target: Declining or stable
└── Red flag: Increasing trend

Postmortem Action Item Completion:
├── % of action items completed on time
├── Target: > 80% completion
└── Red flag: < 50% completion

Automated Test Coverage:
├── % of critical paths covered
├── Target: > 70% for critical paths
└── Not a vanity metric if focused on high-risk areas
```

#### How to Present Metrics to Leadership

**Dashboard structure:**

```
1. Health at a Glance (Top metrics)
   ├── 🟢 SLO Compliance: 99.8% (Target: 99%)
   ├── 🟡 Deployment Frequency: 3x/week (Target: Daily)
   ├── 🟢 Incident Rate: 2 Sev2 this month (Last month: 4)
   └── 🟢 Team Satisfaction: 8.2/10 (Target: 8+)

2. DORA Metrics Trend (Quarterly)
   [Chart showing improvement over time]

3. Focus Areas
   ├── ✅ Reduced incident rate by 50% this quarter
   ├── 🚧 Working on deployment frequency (automation initiative)
   └── ⚠️ Toil still high at 40% - hiring 2 more engineers

4. Asks
   ├── Budget for observability tooling ($50K)
   └── Approval to pause feature work next sprint for reliability
```

---

### 5. Balancing Feature Work vs Operational Excellence

**The eternal tension:** Product wants features. You want stability.

#### Resource Allocation Models

**70-20-10 Rule (Recommended):**
```
70% Feature Work:
├── New features product wants
├── Customer-facing improvements
└── Revenue-generating projects

20% Operational Excellence:
├── Tech debt paydown
├── Reliability improvements
├── Monitoring enhancements
└── Automation

10% Innovation/Learning:
├── Explore new technologies
├── Hackathons
├── Learning time
└── Experimentation
```

**Adjust based on phase:**

```
High Growth Phase:
├── 80% Features
├── 15% Ops Excellence
└── 5% Innovation

Stability Phase:
├── 50% Features
├── 40% Ops Excellence
└── 10% Innovation

Crisis Phase (Post-Incidents):
├── 30% Features
├── 60% Ops Excellence
└── 10% Innovation
```

#### Negotiating with Product

**When product asks for all-feature, no-ops time:**

```
Scenario: "We need all engineers on Feature X for Q4"

Your response framework:
1. Acknowledge business need
   "I understand Feature X is critical for revenue"

2. State operational reality
   "Our on-call load is high (8 pages/week) and error budget is 80% exhausted"

3. Present options
   Option A: All-in on features, risk of incidents and burnout
   Option B: 70-30 split, sustainable pace, less feature risk
   Option C: Hire 2 more engineers to do both

4. Recommend
   "I recommend Option B - we'll deliver 70% of Feature X this quarter,
    and ensure we don't have outages that impact customers"

5. Make it their decision
   "What's your preference given these trade-offs?"
```

**Using error budgets as negotiation tool:**

```
Error budget = objective metric, not subjective

If product wants to move fast:
├── Check error budget: 50% remaining?
├── ✅ Green light: "We have budget, let's ship!"
└── 🛑 Budget exhausted: "We need to stabilize first"

This removes emotion from discussion. It's data-driven.
```

---

### 6. Building Sustainable Operations Culture

**Culture eats process for breakfast.**

#### Key Cultural Values

**1. Blameless Culture**
```
When incidents happen:
❌ "Who broke it?" → ✅ "What broke?"
❌ "Why didn't you..." → ✅ "What can we learn?"
❌ Hide mistakes → ✅ Share failures openly
```

**2. Automate Toil**
```
Manual work is not a badge of honor.
├── Track toil percentage
├── Reward automation, not heroics
└── "If you do it twice, automate it"
```

**3. Sustainable On-Call**
```
On-call is not punishment.
├── Fair rotation
├── Compensated fairly
├── Protected from burnout
└── Escalation is encouraged, not weakness
```

**4. Continuous Improvement**
```
Every incident is a learning opportunity.
├── Postmortems are required, not optional
├── Action items are tracked and completed
└── Celebrate fixes, not just features
```

#### Manager Actions to Reinforce Culture

**1. Lead by Example**
- Participate in on-call rotation (if you're technical)
- Admit your own mistakes publicly
- Take postmortem action items yourself

**2. Celebrate Operational Wins**
- Shout out engineers who reduce toil
- Highlight reliability improvements in team meetings
- Give "Operational Excellence" awards

**3. Protect Your Team**
- Say no to unrealistic timelines
- Push back on "just ship it" pressure
- Shield team from org politics

**4. Invest in Automation**
- Allocate 20% capacity to ops excellence
- Approve tool/platform budgets
- Hire for automation skills

---

## Quick Reference for Managers

**On-Call:**
- Rotation: Weekly or follow-the-sun
- Compensation: $500-$1000/week + pay-per-page
- Burnout prevention: Max 1 week/month, comp time after incidents

**Incidents:**
- Your role: Support, don't take over
- Blameless postmortems: Required for all Sev 1/2
- Action items: Track and ensure completion

**SLOs:**
- Start with current performance + buffer
- Use error budgets to negotiate with product
- Review quarterly

**Metrics:**
- Use DORA metrics (deployment freq, lead time, MTTR, change failure rate)
- Avoid vanity metrics (lines of code, commits, hours)
- Track team health (satisfaction, retention)

**Resource Allocation:**
- 70% features, 20% ops excellence, 10% innovation
- Adjust based on phase (growth vs stability)

**Culture:**
- Blameless, automate toil, sustainable on-call
- Lead by example, celebrate ops wins
- Protect team from burnout

### Culture Building Scenario

**Scenario: "How do we build a sustainable ops culture?"**
- **Blameless:**
  - Never "who broke it?" Always "what broke and how do we prevent it?"
  - Share postmortems openly - learn from all incidents
  - Reward transparency (caught early) over hiding (festered)
- **Automate toil:**
  - Track toil percentage (target < 30%)
  - Dedicate 20% time to automation
  - Celebrate "we automated ourselves out of that problem"
- **Sustainable on-call:**
  - No hero culture - don't celebrate all-nighters
  - Enforce comp time and breaks
  - Fix systems that cause repeated pages
- **Recognition:**
  - Highlight ops wins in all-hands: "Automated X, saved 50 hours/month"
  - Incident response recognition: "Great job handling outage calmly"
  - Quality over speed: "Prevented incident with thorough testing"

**Scenario: "How do we prevent hero culture?"**
- **Heroes are a symptom of broken systems**
- **Signs of hero culture:**
  - Same engineer always saves the day
  - Working nights/weekends is celebrated
  - "We need you" used as motivation
- **How to fix:**
  - Document hero's knowledge → spread it
  - Automate hero's manual tasks
  - Create runbooks for common issues
  - Rotate responsibilities - don't depend on one person
- **Say:** "I appreciate your dedication, but this is unsustainable. Let's fix the system so you don't need to be a hero."

---

## Integration with Other Skills

**This skill works with:**
- **engineering-management** - Hiring, career development, 1-on-1s
- **technical-leadership** - Making technical decisions, risk assessment
- **infrastructure-strategy** - Long-term planning, platform investment
- **budget-and-cost-management** - On-call budgets, tooling costs

**Technical skills your team uses:**
- **sre** - Hands-on SLO implementation, incident response
- **platform-engineering** - Building internal platforms that reduce toil
- **cybersecurity** - Security incident response, compliance

---

**Remember:** Your job is to build sustainable operations practices that enable long-term success, not short-term heroics. Protect your team from burnout. Measure what matters. Learn from every incident.
