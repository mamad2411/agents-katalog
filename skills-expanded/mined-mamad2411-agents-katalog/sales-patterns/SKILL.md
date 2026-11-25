---
name: sales-patterns
description: "When to activate: sales process, MEDDIC, discovery call, demo, objection handling, proposal, closing, pipeline management, CRM, quota, sales methodology"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: business
  domain: business-ops
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Sales Patterns

## Sales Methodologies

### MEDDIC (Enterprise)
```
M — Metrics        What measurable outcomes does the buyer want?
E — Economic Buyer Who has budget authority and final sign-off?
D — Decision       What's the formal decision-making process + timeline?
D — Decision       What criteria will they use to evaluate solutions?
I — Identify Pain  What's the cost of doing nothing? What's the trigger?
C — Champion       Who internally is selling for you when you're not there?
```

**MEDDPICC** adds:
- P = Paper process (legal, procurement, security reviews)
- C = Competition (who else is in the deal?)

### SPICED (Product-Led)
```
S — Situation      Current state, team size, stack, usage patterns
P — Pain           Specific friction points with evidence (quantified)
I — Impact         Business outcome if pain is solved (revenue, time, risk)
C — Critical Event Hard deadline (board meeting, renewal date, migration)
D — Decision       Who, how, when — explicit next steps agreed
```

### Challenger Sale
```
1. Teach    Reframe the buyer's problem with insight they didn't have
2. Tailor   Customize the message to economic buyer's priorities
3. Take     Lead the conversation; don't just respond to requests
```

---

## Discovery Call Framework

### Structure (45 min)
```
0:00–0:05  Agenda setting + confirm time
0:05–0:15  Situational questions (current state)
0:15–0:30  Problem exploration (pain + impact)
0:30–0:40  Qualification (MEDDIC)
0:40–0:45  Next steps (specific date + deliverable)
```

### Discovery Questions
```
Situation:
  - "Walk me through how your team handles [X] today."
  - "How many people are affected by this process?"
  - "What tools are you using now?"

Pain:
  - "Where does the current process break down?"
  - "How often does [problem] happen?"
  - "What's the impact when it does?"

Impact (quantify):
  - "If you fixed this, what would that mean for your team?"
  - "Have you tried to calculate what this costs you annually?"
  - "What happens if nothing changes?"

Qualification:
  - "What does your evaluation process look like?"
  - "Who else needs to be part of this decision?"
  - "Do you have budget allocated, or would this require approval?"
```

---

## Demo Structure

### Problem-Led Demo (not feature tour)
```
1. Recap pain (30 sec)   "You mentioned X costs you Y hours/week."
2. Reveal solution       "Let me show you exactly how we solve that."
3. Demo the fix          Show workflow end-to-end for their use case
4. Quantify              "Teams like yours save Z hours/week."
5. Handle questions      Address as they arise, not in batch
6. Next step             "Based on what you saw, does this solve X?"
```

**Anti-pattern**: Never do a feature tour. Always anchor to a specific pain from discovery.

---

## Objection Handling

### Framework: Feel / Felt / Found
```
"I understand why you feel that way. Others felt the same at first.
What they found was [specific outcome with evidence]."
```

### Common Objections
```
"Too expensive"
→ Reframe to ROI: "Compared to [current cost/pain], the payback is X months."
→ Unbundle: "What if we started with just [core module] at $Y?"

"We're happy with [competitor]"
→ "What would have to be true for you to consider a change?"
→ Find the wedge: where is competitor weakest for their use case?

"Not the right time"
→ Identify the critical event: "What's changing in [quarter] that makes timing matter?"
→ Cost of delay: "What does waiting another quarter cost you?"

"Need to talk to my team"
→ "Happy to help — what information would be most useful for them?"
→ Request multi-thread: ask to join the internal meeting

"We'll build it ourselves"
→ Total cost of build: "Typically takes X engineers Y months. What's your engineering cost?"
→ Opportunity cost: "What else could those engineers be building?"
```

---

## Proposal Writing

### Structure
```
1. Executive Summary (1 page)
   - Situation (their words)
   - Desired outcome
   - Our recommendation
   - Investment and ROI

2. Current State & Pain
   - Documented problems from discovery
   - Quantified impact

3. Solution Overview
   - How it maps to their specific use case
   - Differentiators vs alternatives

4. Implementation Plan
   - Phases with milestones
   - Resources required (theirs + ours)
   - Timeline

5. Investment
   - Clear pricing (no surprises)
   - ROI calculation
   - Payment terms

6. Next Steps
   - Specific actions with owners and dates
```

---

## Pipeline Management

### Stage Definitions
```
Stage 1: Qualified Lead     (BANT validated, meeting booked)         10%
Stage 2: Discovery          (Pain confirmed, champion identified)     25%
Stage 3: Technical Fit      (Demo done, technical win confirmed)      40%
Stage 4: Business Case      (Proposal sent, economic buyer engaged)   60%
Stage 5: Negotiation        (Legal/procurement, verbal commitment)     80%
Stage 6: Closed Won         (Signed contract)                        100%
Stage 7: Closed Lost        (Lost to competition or no decision)       0%
```

### Pipeline Health Checks
```
Weekly: 
  - Review every Stage 4+ deal: next step + date + risk?
  - Aging: any deal stuck > 2× average sales cycle?
  - Coverage: pipeline > 3× quota?

Monthly:
  - Conversion rates stage-by-stage
  - Average deal size trend
  - Win/loss analysis (top 5 wins, top 5 losses)

Quarterly:
  - Cohort analysis: what quarter's deals closed and when?
  - Forecast accuracy: predicted vs actual
```

### CRM Hygiene Rules
```
- Every opportunity must have: close date, amount, stage, next step date
- No stage advance without documented evidence of criteria met
- Discovery notes entered within 24 hours of call
- Forecast category: Commit / Best Case / Pipeline / Omit
```

---

## Closing Techniques

### Assumptive Close
```
"Based on our conversations, it sounds like [Solution] is a good fit.
Let's get the paperwork started — what's the best way to get the
contract to your legal team?"
```

### Summary Close
```
"We've confirmed that [A, B, C] are your top priorities, and you've
seen how we address each. The next step is to sign the MSA and kick
off implementation by [date]. Does that work?"
```

### Creating Urgency (Legitimate)
```
- Implementation capacity: "Our next available onboarding slot is [date]."
- Pricing: "Current pricing holds until [end of quarter]."
- Their critical event: "You mentioned your board review is [date] — 
  that means we'd need to start by [date] to show results."
```

---

## Sales Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| Win Rate | Won / (Won + Lost) | > 25% (enterprise) |
| Average Sales Cycle | Days from SQL to Close | Benchmark vs prior period |
| Average Contract Value | Total ARR / Deals Closed | Growing QoQ |
| Pipeline Coverage | Pipeline Value / Quota | > 3× |
| Forecast Accuracy | |Predicted - Actual| / Quota | < 10% |
| Activity Ratio | Meetings Booked / Outreach Attempts | > 5% |
