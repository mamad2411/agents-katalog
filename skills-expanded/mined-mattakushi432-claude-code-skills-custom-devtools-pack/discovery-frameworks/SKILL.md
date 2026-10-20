---
name: discovery-frameworks
description: "When to activate: product discovery, continuous discovery, opportunity solution tree, assumption testing, Teresa Torres, experiment design, fake door test, concierge test"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: business
  domain: product
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Discovery Frameworks

## Continuous Discovery Cadence

Weekly touchpoints with customers — not quarterly research sprints.

### Weekly Discovery Rhythm
| Activity | Frequency | Time investment |
|----------|-----------|----------------|
| Customer interviews | 1–2 per week | 30–60 min each |
| Interview synthesis | Weekly | 30 min |
| Opportunity tree update | Weekly | 30 min |
| Assumption review | Bi-weekly | 1 hour |
| Experiment read-out | As completed | 30 min |

### Interview Recruiting Pipeline
- Maintain a pool of 10–20 willing participants
- Recruit from: in-app prompts, CS team, community, power users
- Incentivize: gift cards, early access, recognition
- Always interviewing: don't wait until you have a decision to make

## Opportunity Solution Tree (OST)

Visual framework connecting outcomes → opportunities → solutions → experiments.

```
Outcome (desired business result)
├── Opportunity 1 (customer need / pain / desire)
│   ├── Solution A
│   │   └── Experiment: fake door test
│   └── Solution B
│       └── Experiment: prototype test
├── Opportunity 2
│   ├── Solution C
│   │   └── Experiment: concierge test
│   └── Solution D
│       └── Experiment: A/B test
└── Opportunity 3
    └── Solution E
        └── Experiment: wizard of oz
```

### Building the OST
1. Start with the product outcome (not a feature)
2. Interview to surface opportunities (pains, needs, desires)
3. Brainstorm multiple solutions per opportunity (min 3)
4. Design cheapest experiment to test each solution
5. Work top-down: don't jump to solutions before mapping opportunities

### Outcome Selection Criteria
- Measurable (has a metric)
- Within team's influence (not weather, market forces)
- Leads to business result (not vanity metric)
- Appropriate scope (not the entire company strategy)

## Assumption Mapping

Every solution rests on assumptions. Surface and test them before building.

### Four Assumption Types
| Type | Question | Risk if wrong |
|------|---------|--------------|
| **Desirability** | Do customers want this? | Build something nobody uses |
| **Viability** | Can we make money from it? | Build something unprofitable |
| **Feasibility** | Can we build it? | Commit to something impossible |
| **Usability** | Can customers use it? | Build something confusing |

### Assumption Mapping Process
1. Write solution on whiteboard
2. Brainstorm all assumptions (10–20 per solution)
3. Plot on 2×2: Importance (x) × Certainty (y)
4. Focus testing on: High importance + Low certainty (top-left)
5. Document evidence for each assumption as you learn

### Assumption Priority Matrix
```
High certainty  |  Not testing |  Monitor
                |              |
Low certainty   |  TEST FIRST  |  Test if time
                |  (critical)  |
                +----High------+----Low-----
                     Importance
```

## Experiment Types

### Fake Door Test
Test demand before building anything.

```
How: Show a button/link for a feature that doesn't exist yet
Measure: Click-through rate
Learn: Is there demand?
Risk: User frustration if CTA leads nowhere — always show "coming soon" message
Conversion benchmark: > 5–10% CTR suggests real interest
```

### Concierge Test
Deliver the solution manually to validate value before automating.

```
How: Do the thing a human would do that software would eventually do
Measure: Do customers find it valuable? Will they pay?
Learn: Is the solution worth building?
Example: Manual curation of recommendations before building ML model
Scale: Works for 5–20 customers; not a long-term strategy
```

### Wizard of Oz Test
Product appears to work automatically; humans operate it behind the scenes.

```
How: Build believable UI; humans fulfill the "automated" output
Measure: Do customers use it? Are they satisfied?
Learn: Does the solution deliver the expected value?
Risk: Team cost at scale — time-box to 2–4 weeks
```

### Smoke Test / Landing Page Test
Measure intent before building.

```
How: Create landing page describing the solution; add waitlist/buy CTA
Measure: Email signups, "buy" clicks
Learn: Is there pull for this solution?
Risk: Marketing cost; measure intent, not just curiosity
```

## Evidence Strength Scoring

Not all evidence is equal. Score before deciding to build.

| Evidence type | Strength | Example |
|--------------|---------|---------|
| Customers paying for it | Very strong | Pre-orders, pilots |
| Customers doing it manually | Strong | Concierge test usage |
| Customers say they will use it | Weak | Interview quotes |
| Your team thinks they will | Very weak | Internal opinion |
| One customer requested it | Weak | Single data point |

### Evidence Accumulation
Decision to build requires:
- ≥ 3 independent customer signals
- At least 1 behavioral signal (not just stated preference)
- Evidence from target customer segment (not edge cases)

## Discovery vs Delivery Balance

### Anti-Pattern: Big Bang Discovery
- Research for 3 months → build for 6 months → launch → wrong
- Root cause: too much time between learning and validating

### Continuous Model
```
Week 1-2: Interview, identify top opportunity
Week 2-3: Map solutions, design cheapest experiment
Week 3-4: Run experiment, measure
Week 4: Learn → iterate or move to next opportunity
Repeat
```

### Discovery Debt Signals
- Team ships features without talking to customers first
- PM writes specs without evidence section
- Roadmap decided top-down without customer input
- "We already know what customers want" mindset

## Discovery Anti-Patterns

| Anti-pattern | Why it fails |
|-------------|-------------|
| Asking customers what they want | Customers describe solutions, not needs |
| One mega-research phase per quarter | Too slow; world changes; bias confirmation |
| Only interviewing existing customers | Misses potential customers and churned users |
| Skipping experiment, going straight to build | Wastes engineering on unvalidated assumptions |
| Treating all interview feedback equally | One vocal customer ≠ market signal |
| Discovery → hand-off to engineering | Discovery should continue through delivery |
