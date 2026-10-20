---
name: system-design-method
description: >
  End-to-end method to design any system: requirements clarification, capacity
  estimation, high-level design, database design, interface design, scalability,
  and reliability. Use when designing a new system or feature, writing a design
  doc, doing a system design interview, or asking "how do I approach/design X",
  "system design blueprint", "capacity estimate", "back-of-envelope", "HLD".
---

# System Design Method

The repeatable process for going from a vague ask to a defensible architecture.

## When to use
- Starting any non-trivial system or feature design.
- Writing/refining a design doc or RFC.
- Preparing for or running a system design interview.
- Reviewing whether a proposed design covered all bases.

## 7-step process

1. **Requirements clarification.** Separate functional (what it does) from
   non-functional (scale, latency, availability, durability, cost, security,
   compliance). Ask questions; never assume. Write them down.
2. **Capacity estimation (back-of-envelope).** Users → QPS (average + peak),
   storage over N years, bandwidth, memory, compute. State assumptions; round
   aggressively. See `D:\Agent-Assets\system-design-101\data\guides\which-latency-numbers-should-you-know.md`.
3. **High-level design.** Draw blocks (client, LB, API gateway, services, cache,
   DB, queue, CDN, object store) and the data flow between them. Start simple.
4. **Database design.** Pick DB type, model entities, define schema, indexes,
   access patterns. See skill `database-design`.
5. **Interface design.** API contracts (REST/GraphQL/gRPC/events), payloads,
   error model, versioning, auth. See skill `api-design`.
6. **Scalability & performance.** Scaling strategy, caching, sharding,
   replication, CDN, async. See skills `scalability-and-performance`,
   `caching-and-cdn`.
7. **Reliability & resiliency.** Find single points of failure, add redundancy,
   failover, retries, idempotency, backups/DR. See
   `high-availability-and-resilience`.

## Tradeoff discipline
If you cannot name the tradeoff, you do not know the design. Always state the
alternative you rejected and why. Core pairs to force:
- Vertical vs horizontal scaling
- SQL vs NoSQL
- Normalization vs denormalization
- Consistency vs availability (CAP) / strong vs eventual
- Batch vs stream
- Sync vs async
- Stateful vs stateless
- Read-through vs write-through cache
Source: `...\10-system-design-tradeoffs-you-cannot-ignore.md`,
`...\top-5-trade-offs-in-system-designs.md`.

## Design review checklist
- [ ] Functional + non-functional requirements written and agreed.
- [ ] Capacity numbers estimated with assumptions stated.
- [ ] Component diagram with data flow.
- [ ] Data model + DB choice justified.
- [ ] API/event contracts defined.
- [ ] Scaling path identified (what breaks first at 10x).
- [ ] Failure modes enumerated; SPOF removed.
- [ ] Security, observability, cost addressed.
- [ ] Tradeoffs named explicitly.

## Common pitfalls
- Jumping to components before requirements.
- Ignoring non-functional requirements until the end.
- No capacity numbers → hand-wavy "it scales".
- Designing for Google scale when 100 QPS is the real target.
- Hiding tradeoffs instead of stating them.

## References (source guides)
- `...\system-design-blueprint-the-ultimate-guide.md`
- `...\a-cheat-sheet-for-system-designs.md`
- `...\system-design-cheat-sheet.md`
- `...\must-know-system-design-building-blocks.md`
- `...\8-common-system-design-problems-and-solutions.md`
- `...\how-to-ace-system-design-interviews-like-a-boss.md`
- `...\the-12-factor-app.md`
Base: `D:\Agent-Assets\system-design-101\data\guides\`

## Related skills
`scalability-and-performance`, `high-availability-and-resilience`,
`database-design`, `api-design`, `system-design-interviews`.
