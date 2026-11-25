---
name: launch-planning
description: "Plan and execute product launches that actually drive adoption, not just announcements. Covers launch tiers, cross-functional coordination, rollout strategy, and post-launch monitoring. Use when preparing a feature or product launch, coordinating across teams, or when past launches haven't moved the needle."
---

# Launch Planning

Plan launches that drive adoption, not just press releases.

## How to use

- `/launch-planning` Apply launch planning constraints to this conversation.
- `/launch-planning <feature>` Build a launch plan for the described feature or product.

## Constraints

### Launch Tiers
Not every launch deserves the same effort. Tier them:
- Tier 1 (big deal): new product, major feature, pricing change. Full cross-functional coordination.
- Tier 2 (notable): significant improvement, new integration. Blog post, email, in-app announcement.
- Tier 3 (incremental): bug fixes, small improvements. Changelog entry, maybe a tooltip.
- MUST assign a tier before planning. Over-launching small things causes announcement fatigue.

### Pre-Launch
- MUST define success metrics before launch, not after
- MUST have a rollout plan: internal dogfood → beta → phased → GA
- SHOULD run through the launch checklist with every function: engineering, design, marketing, sales, support
- MUST ensure support and sales know about the launch before customers do
- NEVER launch without documentation and support readiness

### Launch Day
- MUST have a single owner for launch coordination
- SHOULD have a war room or dedicated channel for real-time issue tracking
- MUST monitor key metrics in real time during rollout
- MUST have a rollback plan if something goes wrong
- NEVER launch on a Friday unless you want to work the weekend

### Post-Launch
- MUST review metrics against success criteria within 1-2 weeks
- SHOULD gather early user feedback actively, not passively
- MUST run a retrospective: what went well, what didn't, what to change next time
- SHOULD have a fast-follow plan for known gaps and quick improvements
- NEVER move on immediately without measuring whether the launch actually worked

### Anti-Patterns
- The Silent Ship: launching without telling anyone and wondering why adoption is low
- Launch and Forget: big announcement, zero follow-through or measurement
- The Big Bang: months of secret building followed by a massive reveal. Ship incrementally instead.
- Support Surprise: customers asking about a feature support hasn't heard of
- The Premature Launch: announcing before the product is actually ready to handle real usage
