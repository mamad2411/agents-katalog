---
name: roadmap-planning
description: "Build a product roadmap that balances customer needs, business goals, and technical reality. A roadmap is a strategy communicated through planned work, not a feature list with dates. Use when building quarterly or annual plans, when stakeholders pull in different directions, or when the current roadmap feels reactive."
---

# Roadmap Planning

Build a roadmap that communicates strategy, not just a list of features with dates.

## How to use

- `/roadmap-planning` Apply roadmap constraints to this conversation.
- `/roadmap-planning <goals and context>` Build a roadmap for the described situation.

## Constraints

### Start with Outcomes
- MUST define 2-3 outcomes before listing features
- Every initiative MUST connect to at least one outcome
- If it doesn't connect to an outcome, it shouldn't be on the roadmap
- Outcomes should be measurable: "Improve Day-30 retention from 25% to 35%"

### Input Sources
A roadmap MUST synthesize multiple inputs:
- Customer feedback: support tickets, sales loss reasons, interviews, usage data
- Business strategy: revenue targets, market expansion, competitive responses
- Technical needs: debt, infrastructure scaling, security, compliance
- Market signals: competitor moves, trends, regulatory changes
- NEVER build a roadmap from a single input source

### Capacity Allocation
MUST allocate across buckets, not just features:
- Growth stage: 60% features, 20% technical, 10% experiments, 10% buffer
- Pre-PMF: 80% features, 10% technical, 10% experiments
- Scaling: 50% features, 30% technical, 10% experiments, 10% buffer
- Mature: 40% features, 30% technical, 20% optimization, 10% buffer

### Time Horizon Structure
- Now (current sprint/month): high confidence, specific, committed
- Next (1-3 months): medium confidence, scoped but flexible
- Later (3-6 months): low confidence, directional only
- Not Now: explicitly deprioritized. Listing what you're NOT doing is as valuable as what you are.
- NEVER plan beyond 6 months with false specificity

### Sequencing Principles
- Dependencies: map what needs to exist before something else can work
- Learning order: front-load experiments and uncertain bets. Information is worth more early.
- Value delivery cadence: ship incrementally. Don't bunch everything at quarter end.
- Team energy: alternate hard technical work with visible wins
- Market timing: competitive responses, seasonal features, partnership deadlines

### Communication
- For the team: full detail — what, why, who, dependencies, success metrics
- For leadership: outcomes-focused — business goals, resource allocation, milestones
- For customers: high-level themes only. NEVER promise features or dates externally.
- For sales: competitive context — what addresses loss reasons, with rough timing

### Anti-Patterns
- The Feature Factory: shipping because it's on the list, not because it serves an outcome
- The Wishlist Roadmap: everything anyone requested, ordered by who shouted loudest
- The Date-Driven Roadmap: obsessing over ship dates instead of outcomes
- The Secret Roadmap: only leadership knows the plan. Teams need context.
- The Infinite Roadmap: plans extending 12+ months with false specificity
- No Room for Discovery: every hour allocated, none for research or customer conversations
