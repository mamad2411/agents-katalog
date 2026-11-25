---
name: opportunity-sizing
description: "Estimate the potential value of a product opportunity before committing resources. Covers TAM/SAM/SOM, bottom-up and top-down estimation, scenario modeling, and key assumption identification. Use when evaluating new ideas, deciding between directions, or building a business case."
---

# Opportunity Sizing

Figure out if something is worth building before you build it.

## How to use

- `/opportunity-sizing` Apply opportunity sizing constraints to this conversation.
- `/opportunity-sizing <idea>` Size the opportunity for the described product or feature idea.

## Constraints

### Opportunity Statement
MUST state the opportunity in one sentence before sizing:
"If we build [X], [target users] will be able to [outcome], which drives [business metric]."
If you can't fill this in, the opportunity isn't defined enough to size.

### Market Sizing
Work through three layers:
- TAM (Total Addressable Market): everyone who could theoretically use this. Your ceiling.
- SAM (Serviceable Addressable Market): the portion you can realistically reach. Usually 10-30% of TAM.
- SOM (Serviceable Obtainable Market): what you can actually capture in a reasonable timeframe. Usually 1-5% of SAM.
- MUST calculate all three. NEVER cite TAM as if it's achievable.

### Revenue Estimation
- Bottom-up (preferred): reachable users × conversion rate × price × retention rate
- Top-down (sanity check): total market revenue × realistic market share
- If bottom-up and top-down diverge wildly, assumptions need work
- MUST run three scenarios: conservative (50% reach, 70% conversion, 150% cost), base case, optimistic (150% reach, 120% conversion)
- Opportunity is worth pursuing if conservative case is acceptable and base case is compelling

### Cost Assessment
MUST include all four cost types:
- Build cost: engineering, design, product time (include QA, docs, infrastructure)
- Go-to-market cost: marketing, sales, partnerships, education
- Ongoing cost: infrastructure, support, maintenance, iteration
- Opportunity cost: what you're NOT building while you build this. The hidden cost most teams ignore.

### Key Assumptions
- MUST list top 5 assumptions the sizing depends on
- For each: confidence level (1-10), impact if wrong, how to test before committing
- Low confidence + high impact = validate this first, before going all-in

### Quick Sizing (Smaller Decisions)
For features or experiments that don't warrant full analysis:
- Who benefits × how much per user = total value
- If maximum possible impact < cost to build, stop here
- If maximum possible impact > 10× cost, stop analyzing and start building

### Anti-Patterns
- Optimism bias: founders consistently overestimate. Deliberately discount first estimates by 30-50%.
- TAM delusion: "$50B market" means nothing about your ability to capture any of it
- Ignoring alternatives: users have options including doing nothing
- Static analysis: size where the market will be, not just where it is
- Ignoring time dimension: $10M over 5 years is very different from $10M over 1 year
