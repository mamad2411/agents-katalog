---
name: lean-canvas
description: "Builds a one-page Lean Canvas capturing the core business model: problem, solution, key metrics, unfair advantage, channels, customer segments, and cost/revenue structure. Based on Ash Maurya's adaptation of the Business Model Canvas for startups."
category: strategy
default_depth: standard
---

# Lean Canvas / Business Model

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

Builds a one-page Lean Canvas capturing the core business model: problem, solution, key metrics, unfair advantage, channels, customer segments, and cost/revenue structure. Based on Ash Maurya's adaptation of the Business Model Canvas for startups.

## When to Use

- Evaluating a new product or feature idea quickly
- Communicating a business case to stakeholders in a single page
- Comparing multiple product concepts side-by-side
- Starting a new venture or product line
- Investor pitch preparation

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | Quick idea screening or comparing multiple concepts | Problem, Customer Segments, Unique Value Proposition only (following the recommended working order: Problem → Customer Segments → UVP) |
| **Standard** | Building a business case or preparing a pitch | All 9 boxes + Riskiest Assumptions + Experiment Suggestions |
| **Deep** | Investor due diligence or pre-launch validation planning | All sections + per-assumption experiment design with success criteria, TAM/SAM/SOM sizing, unit economics model |

**Omit rules:** At Light depth, skip Solution, Channels, Revenue Streams, Cost Structure, Key Metrics, and Unfair Advantage. Produce only the three core boxes (Problem, Customer Segments, Unique Value Proposition) with existing alternatives noted.

## Framework

### The Nine Boxes

Work through each box in the recommended order (not left-to-right):

**Order: Problem → Customer Segments → Unique Value Proposition → Solution → Channels → Revenue Streams → Cost Structure → Key Metrics → Unfair Advantage**

```markdown
# Lean Canvas: [Product / Feature Name]

## 1. Problem (Top 3)
List the top 3 problems your target customer faces:
1. [Problem 1, specific, evidence-based]
2. [Problem 2]
3. [Problem 3]

**Existing alternatives:**
- [How customers solve this today]

## 2. Customer Segments
**Target customer:** [Specific persona or segment]
**Early adopters:** [Who will use this first and why]

Characteristics of early adopters:
- [Trait 1, e.g., "Already spending money on workarounds"]
- [Trait 2, e.g., "Actively searching for a solution"]

## 3. Unique Value Proposition
**Single clear message that states why you're different and worth buying:**
[One sentence, what is the end result for the customer?]

**High-concept pitch:**
[X for Y, e.g., "Uber for dog walking"]
(Only if genuinely clarifying, not forced)

## 4. Solution
Map each problem to a solution:
| Problem | Solution |
|---|---|
| [Problem 1] | [Feature / approach that addresses it] |
| [Problem 2] | [Feature / approach] |
| [Problem 3] | [Feature / approach] |

## 5. Channels
How will you reach your target customer?
- **Awareness:** [How they discover you, content, ads, referrals]
- **Evaluation:** [How they assess you, free trial, demo, reviews]
- **Adoption:** [How they start using, onboarding, setup]
- **Retention:** [How they keep using, email, community, success]
- **Revenue:** [How they pay, self-serve, sales, marketplace]

## 6. Revenue Streams
**Pricing model:** [Subscription / Usage / Transaction / Freemium / etc.]
**Price point:** $[X] per [unit / month / seat]
**Revenue target:** $[X] ARR by [date]
**Basis:** [How you arrived at this price, competitor benchmarks, willingness-to-pay research, cost-plus]

## 7. Cost Structure
**Fixed costs:**
- [e.g., Team salaries: $X/mo]
- [e.g., Infrastructure: $X/mo]

**Variable costs:**
- [e.g., Customer acquisition: $X per customer]
- [e.g., Support: $X per ticket]

**Break-even:** [X] customers at $[Y] ACV

## 8. Key Metrics
The 3-5 numbers that tell you if the business is working:
1. [Metric 1, e.g., "Weekly active users"]
2. [Metric 2, e.g., "Trial-to-paid conversion rate"]
3. [Metric 3, e.g., "Net revenue retention"]

**Pirate Metrics (AARRR):**
- Acquisition: [metric]
- Activation: [metric]
- Retention: [metric]
- Revenue: [metric]
- Referral: [metric]

## 9. Unfair Advantage
Something that cannot be easily copied or bought:
- [e.g., "Proprietary dataset from 5 years of customer usage"]
- [e.g., "Network effects, value increases with each user"]
- [e.g., "Deep domain expertise in [regulated industry]"]

**Note:** It's okay to leave this blank initially. Most startups don't have an unfair advantage on day one, but you should be building toward one.
```

## Minimum Evidence Bar

**Required inputs:** A specific problem statement with at least one identified customer segment, and a proposed solution concept.

**Acceptable evidence:** Customer interviews, support tickets, survey data, competitor pricing pages, usage analytics, published market research, founder domain experience with concrete examples.

**Insufficient evidence:** If the problem is stated without any customer evidence (interviews, data, or observed behavior), produce a partial artifact with unanswered sections marked `[TBD, requires: customer interviews or observed behavior data]` and flag the artifact as draft-only.

**Hypotheses vs. findings:**
- **Findings:** Problem (top 3), Customer Segments, and Existing Alternatives must be grounded in observed customer behavior or data.
- **Hypotheses:** Solution mapping, Unfair Advantage, Revenue Streams pricing, and Key Metrics targets are allowed to be speculative, must be labeled as assumptions to test.

## Output Format

Produce:
1. **Lean Canvas (single page)**, all nine boxes completed
2. **Riskiest Assumptions**, top 3 assumptions that could invalidate the canvas
3. **Experiment Suggestions**, how to test each risky assumption cheaply

**Shipwright Signature (required closing):**
4. **Decision Frame**, Go/no-go recommendation on pursuing this concept, key trade-off, confidence with evidence quality, owner, decision date, revisit trigger
5. **Unknowns & Evidence Gaps**, Unvalidated willingness-to-pay, untested channel assumptions, assumed early adopter characteristics
6. **Pass/Fail Readiness**, PASS if Problem and Customer Segments are evidence-backed and each identified riskiest assumption has a testable experiment (at Light depth: PASS if Problem and Customer Segments are evidence-backed, experiment design is deferred); FAIL if Problem is speculative with no customer evidence
7. **Recommended Next Artifact**, Which Shipwright skill to run next and why

## Common Mistakes to Avoid

- **Solution-first thinking**, Start with Problem and Customer Segments, not Solution
- **Vague problems**, "Communication is hard" is not actionable; "Remote teams lose context on decisions made in meetings they missed" is
- **No early adopter definition**, "Everyone" is not a customer segment
- **Confusing features with UVP**, "Has AI" is a feature; "Get board-ready reports in 10 minutes instead of 3 hours" is a UVP
- **Missing unfair advantage**, It's fine to leave blank, but don't claim one you don't have

## Weak vs. Strong Output

**Weak:**
> **Problem 1:** Teams struggle with communication and productivity.

No specificity on who, when, or how much it costs them, could describe any product pitch ever written.

**Strong:**
> **Problem 1:** Series A engineering teams (15-40 devs) lose ~6 hours/week per engineer to context-switching between Slack threads, Jira tickets, and design docs when triaging production incidents.

Named segment, quantified pain, specific workflow trigger, testable with 5 customer interviews.
