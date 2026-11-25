---
name: system-design-interviews
description: >
  Prepare for and run system design interviews. Use for the 7-step interview
  process, requirements clarification, capacity estimation, structuring answers,
  common questions and mistakes, interview algorithms, and recommended study
  materials. Triggers: "system design interview", "interview prep", "how do I
  answer", "capacity estimation for interview", "ace the interview".
---

# System Design Interviews

A structured conversation about tradeoffs, not a trivia test.

## When to use
- Preparing for a system design interview.
- Practicing or mock-interviewing.
- Structuring a spoken design answer.

## The 7-step answer structure
1. **Requirements clarification** — functional + non-functional, ask questions,
   state assumptions.
2. **Capacity estimation** — users, QPS, storage, bandwidth; say the numbers.
3. **High-level design** — blocks + data flow diagram.
4. **Database design** — model, DB choice, schema, indexes.
5. **Interface design** — APIs/events, contracts.
6. **Scalability & performance** — caching, sharding, replication, CDN, async.
7. **Reliability & resiliency** — SPOF, failover, retries, idempotency.
Source: `...\how-to-ace-system-design-interviews-like-a-boss.md`.

## What interviewers score
- Problem framing and clarifying questions.
- Logical, structured progression (not jumping to boxes).
- Depth on the components you choose.
- Awareness of tradeoffs and failure modes.
- Communication and collaboration.
- Ability to go deep where asked.

## Reusable capacity numbers
- 1 day ≈ 86,400s (round to ~100k for math).
- QPS ≈ DAU × actions/user / 86400; peak = 2-5× average.
- Storage = records × size × replication × retention.
- Know latency numbers (L1/RAM/SSD/disk/DC RTT) at order-of-magnitude.

## Common questions
Design: URL shortener, rate limiter, chat, news feed, notifications, search,
Maps/Google Docs, stock exchange, S3, ticket booking, payment, proximity.
For each: requirements → API → data → scale → bottlenecks.

## Common mistakes
- Coding the solution instead of designing.
- No requirements; assuming scope.
- Over-focusing on one component; ignoring reliability/security.
- No tradeoffs; dogmatic choices.
- Silent thinking; not communicating.
- Ignoring non-functional requirements and cost.

## Study plan
1. Master fundamentals via `system-design-method` and component skills.
2. Study `architecture-case-studies` for patterns and vocabulary.
3. Practice 1-2 designs aloud per week; time them.
4. Review tradeoffs: `scalability-and-performance`,
   `high-availability-and-resilience`, `database-design`.
5. Mock interviews; get feedback on structure.

## Checklist (self-review after a mock)
- [ ] Clarified requirements + stated assumptions.
- [ ] Estimated capacity with numbers.
- [ ] Drew a high-level diagram.
- [ ] Chose DB + justified.
- [ ] Defined APIs.
- [ ] Addressed scale, latency, and failure.
- [ ] Named tradeoffs explicitly.
- [ ] Communicated continuously.

## References
- `...\how-to-ace-system-design-interviews-like-a-boss.md`
- `...\my-recommended-materials-for-cracking-your-next-technical-interview.md`
- `...\algorithms-you-should-know-before-taking-system-design-interviews.md`
- `...\what-happens-when-you-type-a-url-into-your-browser.md`, `...\what-happens-when-you-type-google.md`
- `...\how-do-sql-joins-work.md`, `...\visualizing-a-sql-query.md`
Base: `D:\Agent-Assets\system-design-101\data\guides\`

## Related skills
`system-design-method`, `architecture-case-studies`,
`scalability-and-performance`, `database-design`, `distributed-systems`.
