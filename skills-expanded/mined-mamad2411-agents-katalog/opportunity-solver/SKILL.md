---
name: opportunity-solver
description: "JTBD-based product opportunity discovery, customer interview analysis, and competitive landscape mapping. Use when identifying unmet user needs or market gaps."
version: 1.0.0
platforms: [linux, macos]
---

# Opportunity Solver

## What It Does
Applies Jobs-to-be-Done (JTBD) framework to discover high-value product opportunities. Analyzes customer interviews to uncover unmet needs, scores opportunities by importance vs. current satisfaction, maps competitive landscapes to identify whitespace, and applies Build/Buy/Partner decision frameworks to determine the best execution path.

## Iron Laws (NEVER violate)
1. **Job, not solution** — Define the job customers are hiring your product to do. Never start with a solution looking for a problem.
2. **Importance × Satisfaction gap** — Only pursue opportunities where Importance is HIGH and current Satisfaction is LOW. Everything else is a distraction.
3. **Customer voice, not your voice** — Every insight must trace back to actual customer data (interview, survey, support ticket, usage data). No invented personas.
4. **Competitive honesty** — Acknowledge where competitors are better. Wishful thinking about competitive advantages leads to wasted investment.

## Red Flags (STOP immediately)
- **Solution-first thinking** — Discussion focuses on features without a defined job → reframe to JTBD
- **Satisfaction illusion** — "Customers seem happy" without quantitative satisfaction data → collect real data
- **Feature factory** — Building features because competitors have them, not because customers need them
- **Underserved vs unserved confusion** — Targeting a market that doesn't exist vs one that's poorly served

## Common Rationalizations (self-deception)
- "We know what customers need, we talk to them all the time" → Confirmation bias. Structured interviews reveal surprises.
- "This competitor feature is table stakes, we need it" → Table stakes = low opportunity score. Differentiate, don't copy.
- "The market is too small to analyze" → Every market has data. If you can't find it, the market may not exist.

## When To Use
- Exploring new product ideas or feature opportunities
- User says "what should we build next?"
- Analyzing why a product feature isn't gaining traction
- Competitive analysis to find market gaps
- Build vs. Buy vs. Partner decision for a capability

## Human Partner Signals (escalate to human)
- **Strategic pivot** — Opportunity requires changing company's core value proposition → executive decision
- **Market entry** — Opportunity involves entering a regulated market (finance, health, defense) → legal/compliance review
- **Resource commitment** — Opportunity requires 3+ months of engineering investment → funding approval
- **Customer access** — Need to interview specific customer segments the team can't reach → sales/CS coordination

## Pipeline
1. Discover: conduct customer interviews (at least 12 per segment), mine support tickets and NPS comments
2. Map: identify all jobs customers are trying to accomplish, group into job categories
3. Score: rate each job on Importance (1-10) and current Satisfaction (1-10), calculate opportunity score
4. Landscape: map competitors' solutions to each job, identify underserved jobs (high importance, low satisfaction, weak competition)
5. Decide: apply Build/Buy/Partner framework to top opportunities
6. Recommend: present top 3 opportunities with evidence, competitive context, and execution recommendation

## Verification Checklist
- [ ] At least 12 customer interviews conducted per target segment
- [ ] Every opportunity traced to specific customer data (quote, ticket, survey response)
- [ ] Opportunity scores calculated with Importance × (10 - Satisfaction) formula
- [ ] Competitive landscape mapped for top 5 opportunities
- [ ] Build/Buy/Partner recommendation justified with cost/time/strategic-fit analysis
- [ ] No solution ideas presented without a defined JTBD

## Related Skills
- `validation-designer` — Validated opportunities move to experiment design
- `roadmap-prioritizer` — Scored opportunities feed roadmap prioritization
- `grill` — Selected opportunities become user stories
- `competitive-agent-research` — Competitive landscape intelligence gathering
