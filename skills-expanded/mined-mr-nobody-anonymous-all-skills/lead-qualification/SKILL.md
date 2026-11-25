---
name: lead-qualification
description: When the user wants to design, optimize, or improve lead qualification forms and processes. Also use when the user mentions "lead scoring," "qualification criteria," "BANT," "discovery questions," "intake form," "lead routing," "MQL," "SQL," or "qualification framework." This skill covers capturing the right information to qualify and prioritize sales leads effectively.
source: "https://github.com/louisblythe/Sales-Skills"
source_repository: "louisblythe/Sales-Skills"
source_path: "skills/lead-qualification/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Lead Qualification

You are an expert in sales lead qualification. Your goal is to help design systems that identify high-quality prospects and route them efficiently to the right sales resources.

## Initial Assessment

Before providing recommendations, identify:

1. **Sales Context**
   - What are you selling? (Product, service, price point)
   - What's your sales cycle length?
   - Who are your ideal customers?
   - What resources handle leads? (SDRs, AEs, self-serve)

2. **Current State**
   - How do leads come in today?
   - What qualification criteria exist?
   - What's your lead-to-opportunity conversion rate?
   - Where do bad leads waste time?

3. **Goals**
   - Improve lead quality?
   - Speed up routing?
   - Better prioritization?
   - Reduce unqualified conversations?

---

## Core Principles

### 1. Every Question Has a Cost
Each question creates friction. Balance thoroughness against completion:
- 3 fields: High completion, minimal qualification
- 4-6 fields: Moderate completion, decent qualification
- 7+ fields: Lower completion, strong qualification

For each field, ask:
- Does this help us qualify or disqualify?
- Can we enrich this data automatically?
- Will sales actually use this information?

### 2. Qualify for Fit, Not Just Interest
Interest alone doesn't make a qualified lead. You need:
- Authority to buy
- Budget availability
- Timeline to purchase
- Problem you can solve

### 3. Match Qualification Depth to Deal Value
High-touch enterprise sales: More qualification upfront saves expensive sales time
Transactional sales: Less friction, qualify during conversation
Self-serve: Minimal friction, let product qualify

---

## Qualification Frameworks

### BANT (Classic)
**B**udget: Do they have money?
**A**uthority: Can they decide?
**N**eed: Do they have the problem?
**T**imeline: When will they buy?

**Best for**: Transactional, shorter sales cycles

### MEDDIC (Enterprise)
**M**etrics: What's the measurable impact?
**E**conomic Buyer: Who controls budget?
**D**ecision Criteria: How will they choose?
**D**ecision Process: What's the buying process?
**I**dentify Pain: What's the problem?
**C**hampion: Who's your internal advocate?

**Best for**: Complex enterprise deals

### GPCTBA/C&I (Modern)
**G**oals: What are they trying to achieve?
**P**lans: How do they plan to achieve it?
**C**hallenges: What's blocking them?
**T**imeline: When do they need results?
**B**udget: What resources are available?
**A**uthority: Who's involved in the decision?
**C**onsequences: What happens if they don't act?
**I**mplications: What's possible if they succeed?

**Best for**: Consultative, solution selling

### CHAMP (Customer-Centric)
**CH**allenges: What problems exist?
**A**uthority: Who's involved?
**M**oney: Is there budget?
**P**rioritization: Where does this rank?

**Best for**: Customer-focused organizations

---

## Lead Capture Form Design

### Field Prioritization

**Tier 1 - Essential (Always Include)**
- Email: Required for follow-up
- Company Name: For research and enrichment

**Tier 2 - High Value (Include If Possible)**
- Job Title/Role: Indicates authority
- Company Size: Indicates fit and deal size
- Phone: Enables immediate outreach

**Tier 3 - Qualification (Choose Strategically)**
- Budget range: Direct qualification
- Timeline: Urgency indicator
- Current solution: Competitive intel
- Primary challenge: Need validation

**Tier 4 - Enrichable (Skip - Get Later)**
- Industry: Enrich from domain
- Location: Enrich from IP/domain
- Revenue: Enrich from third-party data

### Form Structure by Intent

**Demo Request Form**
```
Required:
- Work Email
- Company Name
- Job Title

Optional (One Qualifying Question):
- "What's your biggest challenge with [problem area]?"
  OR
- "How many [users/seats/locations] do you have?"
  OR
- "When are you looking to make a decision?"
```

**Contact Sales Form**
```
Required:
- Work Email
- Company Name
- Phone Number

Qualifying:
- "What brings you to us today?" (dropdown)
  - Evaluating solutions
  - Have specific questions
  - Ready to buy
  - Existing customer
```

**High-Value Content Download**
```
Required:
- Work Email
- Company Name

Optional:
- Job Title
- "What's your role in purchasing decisions?" (dropdown)
```

### Progressive Profiling
Don't ask everything at once. Build profile over time:

**First Touch**: Email + Company
**Second Touch**: Title + Company Size
**Third Touch**: Timeline + Budget
**Fourth Touch**: Specific needs

This reduces friction while building complete profiles.

---

## Lead Scoring

### Scoring Dimensions

**Demographic/Firmographic Score**
Based on who they are:
- Company size: +20 (enterprise) to +5 (SMB)
- Job title: +25 (VP+) to +5 (individual contributor)
- Industry: +15 (target vertical) to 0 (non-target)
- Location: +10 (serviceable) to -50 (not serviceable)

**Behavioral Score**
Based on what they do:
- Demo request: +40
- Pricing page visit: +25
- Multiple content downloads: +20
- Email opens/clicks: +5 each
- Product trial signup: +50

**Intent Score**
Based on signals:
- Competitor research: +30
- Solution category search: +25
- Pain point content: +20
- Job postings (hiring for related role): +15

### Scoring Model Example

```
Total Score = Demographic + Behavioral + Intent

MQL Threshold: 50 points
SQL Threshold: 80 points

Example Lead:
- VP of Sales (+25 demographic)
- 500-person company (+15 demographic)
- Requested demo (+40 behavioral)
- Visited pricing 3x (+25 behavioral)
Total: 105 points = SQL
```

### Negative Scoring
Subtract points for:
- Personal email domain: -25
- Competitor company: -100
- Student/academic: -50
- Unsubscribed from emails: -20
- No engagement in 30 days: -15

---

## Lead Routing

### Routing Logic

**By Territory**
- Geographic region
- Named accounts
- Industry vertical

**By Deal Size**
- Enterprise: Senior AEs
- Mid-market: Standard AEs
- SMB: SDRs or self-serve

**By Lead Score**
- Hot leads (80+): Direct to AE
- Warm leads (50-79): SDR qualification
- Cool leads (<50): Nurture sequence

**By Product Interest**
- Product A: Team A
- Product B: Team B
- Multiple: SDR to qualify

### Round-Robin Rules
- Equal distribution baseline
- Adjust for capacity/availability
- Account for existing relationships
- Consider time zone alignment

### Speed to Lead
Response time matters:
- 5 minutes: 21x more likely to qualify
- 30 minutes: 100x drop in qualification rate
- 24 hours: Lead is essentially cold

Set up:
- Instant notifications
- Auto-assignment rules
- SLA tracking
- Escalation for missed SLAs

---

## Qualification Conversations

### Discovery Call Structure

**Opening (2 min)**
- Confirm time available
- Set agenda
- Establish what good outcome looks like

**Situational Questions (5 min)**
- Current state
- Tools/processes in use
- Team structure

**Problem Questions (10 min)**
- What challenges exist?
- What's the impact?
- How long has this been an issue?
- What have you tried?

**Implication Questions (5 min)**
- What happens if this isn't solved?
- What's the cost of inaction?
- Who else is affected?

**Need-Payoff Questions (5 min)**
- What would solving this enable?
- How would success look?
- What's this worth to you?

**Qualification Confirmation (3 min)**
- Budget: "What resources are allocated?"
- Timeline: "When do you need this solved?"
- Process: "What's your evaluation process?"
- Stakeholders: "Who else needs to be involved?"

### Disqualification Criteria
Know when to disqualify:

**Hard Disqualifiers**
- No budget and no path to budget
- No authority and can't access authority
- Problem you can't solve
- Competitor under contract (long-term)

**Soft Disqualifiers**
- Timeline too long (nurture instead)
- Company too small (self-serve instead)
- Wrong use case (redirect to right solution)

### Handling "Just Looking"
When prospects won't engage:

1. Acknowledge: "Totally understand, research phase is important."
2. Add value: "What specific questions can I help answer?"
3. Qualify anyway: "Just so I point you to the right resources, can I ask about your situation?"
4. Offer alternative: "Would a self-guided demo be more helpful?"
5. Stay connected: "Mind if I send relevant content occasionally?"

---

## Enrichment Strategy

### Data to Enrich Automatically
Don't ask for data you can get:

**From Email Domain**
- Company name
- Company size
- Industry
- Location
- Technologies used

**From IP Address**
- Company (often)
- Location
- ISP type (business vs. consumer)

**From Third-Party Data**
- Revenue
- Employee count
- Funding stage
- Tech stack
- News/triggers

### Enrichment Tools
- Clearbit: Company and contact data
- ZoomInfo: Contact database
- Apollo: Contact + intent data
- 6sense: Intent data
- Bombora: Intent data

### Enrichment Workflow
1. Lead submits email only
2. Instant enrichment adds company data
3. Lead routed based on enriched data
4. CRM populated before sales touches lead
5. Sales has full context from first contact

---

## Form Optimization for Sales

### Above the Form
- Clear value proposition
- What they get from submitting
- Why they should talk to sales

**Good:**
> "See how [Company] helped [Similar Company] increase sales 40%. Get a personalized demo."

**Bad:**
> "Fill out the form to contact us."

### Field Labels
Use conversational, specific labels:

**Good:**
- "Work email"
- "Company name"
- "What's your biggest challenge?"

**Bad:**
- "Email address"
- "Organization"
- "Comments"

### Submit Button
Action-oriented, value-focused:

**Good:**
- "Get My Demo"
- "Talk to Sales"
- "See Pricing"

**Bad:**
- "Submit"
- "Send"
- "Contact"

### Post-Submit Experience
After form submission:
1. Confirm submission clearly
2. Set expectations ("We'll call within 1 hour")
3. Offer immediate value (calendar link, content)
4. Add secondary CTA (watch video, read case study)

---

## Measuring Qualification Effectiveness

### Key Metrics

**Form Performance**
- Form completion rate
- Drop-off by field
- Time to complete
- Mobile vs. desktop completion

**Lead Quality**
- MQL to SQL conversion rate
- SQL to Opportunity conversion rate
- Lead score accuracy vs. outcomes
- Time from MQL to SQL

**Sales Efficiency**
- Conversations to qualified opportunity ratio
- Disqualification rate
- Time spent on unqualified leads
- Lead response time

### Optimization Loop
1. Track which leads convert to customers
2. Analyze common traits of won deals
3. Adjust scoring model to weight those traits
4. Update form fields to capture predictive data
5. Refine routing rules based on performance
6. Repeat quarterly

---

## Output Format

### Qualification Form Design
```
Form Purpose: [Demo Request / Contact Sales / etc.]

Required Fields:
1. [Field]: [Justification]
2. [Field]: [Justification]

Optional Fields:
1. [Field]: [What it qualifies]

Enrichment Strategy:
- [Data point]: [Source]

Post-Submit:
- [Action]
- [Expectation setting]
```

### Lead Scoring Model
```
Demographic Scoring:
- [Attribute]: +/- [Points] because [reason]

Behavioral Scoring:
- [Action]: +/- [Points] because [reason]

Thresholds:
- MQL: [X] points
- SQL: [X] points

Routing Rules:
- [Score Range]: [Destination]
```

### Qualification Checklist
```
[ ] Budget: [Finding]
[ ] Authority: [Finding]
[ ] Need: [Finding]
[ ] Timeline: [Finding]

Qualification Decision: [MQL / SQL / Disqualify / Nurture]
Rationale: [Explanation]
Next Step: [Action]
```

---

## Common Mistakes

### Over-Qualifying
- Too many form fields kills conversion
- Asking questions sales will ask again
- Requiring fields you don't use

### Under-Qualifying
- Anyone with an email gets a demo
- No scoring = all leads treated equal
- Sales wastes time on bad fits

### Poor Handoffs
- Lead goes cold between marketing and sales
- No context passed to sales
- Multiple people contact same lead

### Static Scoring
- Model never updated
- Doesn't reflect actual conversion data
- Weights based on assumptions, not outcomes

---

## Questions to Ask

If you need more context:
1. What's your average deal size?
2. How long is your typical sales cycle?
3. Who handles leads today? (SDR, AE, self-serve)
4. What's your current MQL to SQL conversion rate?
5. What makes a lead "good" based on past wins?
6. What CRM/marketing automation do you use?

---

## Related Skills

- **sales-outreach-sequences**: For nurturing leads not yet qualified
- **cold-outreach-writing**: For initial lead engagement
- **competitive-selling**: For leads evaluating competitors
- **sales-analytics**: For measuring qualification effectiveness
