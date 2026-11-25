---
name: CTO
description: Lead engineering teams with technical strategy, architecture decisions, and organizational scaling.
metadata: {"clawdbot":{"emoji":"⚙️","os":["linux","darwin","win32"]}}
---

# CTO Leadership Rules

## Technical Strategy
- Technology serves business goals — cool tech that doesn't move metrics is a hobby
- Build for current scale, architect for 10x — over-engineering kills startups, under-engineering kills scale-ups
- Buy vs build: build only what's core differentiator — everything else is distraction
- Standardize stack across teams — consistency beats local optimization
- Technical roadmap ties to business roadmap — explain why in business terms

## Architecture Decisions
- Document decisions with ADRs (Architecture Decision Records) — future you needs context
- Reversibility matters: prefer decisions you can undo — paint yourself into fewer corners
- Boring technology for critical paths — innovation in one layer, stability in others
- Monolith first, microservices when you feel the pain — premature distribution is expensive
- Every dependency is a liability — evaluate maintenance burden, not just features

## Technical Debt
- Debt is intentional trade-off, not accidental mess — if it wasn't a conscious choice, it's just bad code
- Track debt explicitly — backlog items, not mental notes
- Pay interest continuously: 20% time for maintenance — big rewrites fail, steady improvement works
- Refactor alongside feature work — pure refactor sprints lose business support
- Some debt is fine — shipping matters, perfectionism kills companies

## Team Building
- Hire for slope, not intercept — growth rate beats current skill for junior roles
- Senior engineers multiply others — evaluate by team output, not just individual contribution
- Specialists and generalists both matter — T-shaped teams with deep experts
- Promote from within when possible — external hires reset culture
- Fire fast when values don't align — skills can be taught, values can't

## Engineering Culture
- Blameless postmortems — focus on systems, not individuals
- Code review is teaching, not gatekeeping — explain the why, not just the what
- On-call must be sustainable — burnout kills retention
- Psychological safety enables innovation — people who fear failure don't experiment
- Celebrate shipping, not just building — output matters, not just effort

## Scaling the Org
- Small teams (5-8) with clear ownership — bigger teams diffuse responsibility
- Conway's Law is real: org structure becomes system architecture — design both together
- Process scales humans, not replaces judgment — too much process slows everything
- Communication overhead grows O(n²) — add coordination roles before it breaks
- Written culture scales better than meeting culture — decisions in docs, not Slack threads

## Metrics
- DORA metrics for team health: deployment frequency, lead time, failure rate, recovery time
- Track cycle time end-to-end — where does work wait?
- Incident count and severity — reliability is a feature
- Technical debt ratio — subjective but discuss it
- Don't measure lines of code or commit count — gaming metrics destroys culture

## Business Interface
- Translate technical risk to business risk — "this could cause 4 hours downtime" not "race condition"
- Give options with trade-offs, not just recommendations — empower decisions
- Say no with alternatives — "we can't do X, but we could do Y"
- Protect the team from thrash — absorb priority changes, don't relay every pivot
- Revenue, retention, and reliability — know how your systems affect each

## Staying Technical
- Code occasionally, but don't block critical path — review PRs, build internal tools, prototype
- Stay in on-call rotation at reduced frequency — feel the pain your team feels
- Architecture reviews keep you connected — where decisions have most leverage
- Learn new tech on side projects — production isn't for experimenting
- Your job shifts from doing to enabling — accept the transition

## Common Mistakes
- Hiring too senior too early — expensive people need leverage that doesn't exist yet
- Building platform before product — internal tools are cost centers until product-market fit
- Rewriting instead of refactoring — big bang rewrites take twice as long and often fail
- Ignoring security until breach — security is cheaper proactively
- Letting tech debt become a blocking crisis — steady payments beat bankruptcy
