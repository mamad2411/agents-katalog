---
name: distributed-systems-design
description: "Guides distributed system design using a structured 4-step framework: scope, high-level design, deep dive, wrap-up. Two modes: CHECKER audits existing designs for missing components, wrong tradeoffs, and anti-patterns. APPLIER walks through designing systems step-by-step with clarifying questions, component selection, and scaling strategies. Covers 15 system designs (rate limiter, consistent hashing, key-value store, unique ID generator, URL shortener, web crawler, notification system, news feed, chat system, search autocomplete, YouTube, Google Drive, scaling foundations, estimation, interview framework) plus cross-cutting techniques and review checklists. Triggers on: system design, distributed system design, design a system, design a distributed, scale system, architecture review, high-level architecture, back of envelope, capacity planning, design with load balancer, database sharding strategy, caching strategy for scale, CDN architecture, message queue design, microservices system design, API system design, scale my system, how would you build."
---

# Distributed System Design Skill Router

All reference files live in `references/`.

---

## 1. Quick Reference: Problem-to-Chapter Routing Table

| Problem / Question | Reference File | Key Content |
|---|---|---|
| How to structure a system design interview | `chapter-03-framework-for-system-design-interviews.md` | 4-step framework, time allocation, dos/don'ts, interviewer signals |
| How to scale from single server to millions of users | `chapter-01-scale-from-zero-to-millions.md` | Progressive scaling: LB, replication, cache, CDN, stateless tier, sharding, multi-DC |
| How to estimate QPS, storage, bandwidth, server count | `chapter-02-back-of-envelope-estimation.md` | DAU-to-QPS formula, latency numbers, availability nines, estimation template |
| Design a rate limiter / API throttling | `chapter-04-design-rate-limiter.md` | Token bucket, leaking bucket, sliding window; Redis counters; race conditions |
| How to distribute data across servers evenly | `chapter-05-design-consistent-hashing.md` | Hash ring, virtual nodes, affected-key redistribution, rehashing problem |
| Design a distributed key-value store | `chapter-06-design-key-value-store.md` | CAP theorem, quorum (N/W/R), vector clocks, gossip, Merkle trees, write/read path |
| Generate unique IDs in distributed systems | `chapter-07-design-unique-id-generator.md` | Snowflake (64-bit), UUID, ticket server, multi-master; bit layout tuning |
| Design a URL shortener | `chapter-08-design-url-shortener.md` | Base 62 vs hash+collision; 301/302 redirect; bloom filter; read-heavy caching |
| Design a web crawler | `chapter-09-design-web-crawler.md` | BFS traversal, URL frontier, politeness, robots.txt, dedup, content fingerprinting |
| Design a notification system | `chapter-10-design-notification-system.md` | Multi-channel (push/SMS/email), message queues, retry, dedup, templates, analytics |
| Design a news feed system | `chapter-11-design-news-feed-system.md` | Fan-out on write vs read, celebrity problem, feed publishing vs retrieval, graph DB |
| Design a chat system | `chapter-12-design-chat-system.md` | WebSocket, presence, service discovery, message sync, KV store for history |
| Design search autocomplete / typeahead | `chapter-13-design-search-autocomplete.md` | Trie data structure, top-k, data gathering vs serving, caching at browser/CDN |
| Design YouTube / video streaming | `chapter-14-design-youtube.md` | Video transcoding DAG, CDN delivery, blob storage, pre-signed URLs, streaming protocols |
| Design Google Drive / cloud file storage | `chapter-15-design-google-drive.md` | Block-level splitting, delta sync, dedup, notification service, conflict resolution, versioning |
| Which database: SQL vs NoSQL | `chapter-01-scale-from-zero-to-millions.md` | Decision criteria, tradeoff table |
| What is the CAP theorem | `chapter-06-design-key-value-store.md` | CP vs AP analysis, practical implications |
| How to handle server failures | `chapter-01-scale-from-zero-to-millions.md` + `chapter-06-design-key-value-store.md` | Failover at every tier (Ch1); gossip, hinted handoff, Merkle trees (Ch6) |
| How to choose a sharding key | `chapter-01-scale-from-zero-to-millions.md` + `chapter-05-design-consistent-hashing.md` | Celebrity/hotspot problem, resharding, virtual nodes |
| When to add a cache layer | `chapter-01-scale-from-zero-to-millions.md` | Read-through cache, expiration policy, cache SPOF, thundering herd |
| When to add a message queue | `chapter-01-scale-from-zero-to-millions.md` | Decoupling, async processing, independent scaling |
| How to handle rate-limiting race conditions | `chapter-04-design-rate-limiter.md` | Lua scripts, Redis sorted sets, centralized store vs sticky sessions |

---

## 2. The 4-Step Framework (from Ch3)

Every system design conversation follows these four steps. Never skip one.

| Step | Time (45 min) | What to Do | Failure Mode if Skipped |
|---|---|---|---|
| **1. Scope** | 3-10 min | Ask clarifying questions: features, users, scale, tech stack, growth. Write down assumptions. Get confirmation. | Design the wrong system; "huge red flag" per interviewers |
| **2. High-Level Design** | 10-15 min | Draw box diagrams (clients, APIs, servers, cache, DB, CDN, queues). Walk through use cases. Get buy-in. | Deep dive on wrong components; wasted effort |
| **3. Deep Dive** | 10-25 min | Prioritize 2-3 components based on interviewer cues. Discuss tradeoffs and alternatives. | Superficial design; no depth signal |
| **4. Wrap-Up** | 3-5 min | Identify bottlenecks. Discuss failures, monitoring, next scale curve. Never say "it's perfect." | Miss high-signal topics; weak finish |

**Key rules:**
- Think out loud. Silence gives zero signal.
- Treat the interviewer as a teammate. Seek feedback.
- Never over-engineer. Design for current requirements with clear extension points.
- Back-of-envelope calculations validate scale fitness (invoke Ch2 when needed).

---

## Red Flags -- STOP and Correct

| If You Hear This | STOP and Do This |
|---|---|
| "Skip scoping, just draw the diagram" | Refuse. Scoping prevents designing the wrong system. Ask at least features, scale, and latency. |
| "We don't have time for estimation" | Estimation takes 2 minutes. Without it, the design has no grounding. Do it. |
| "Just pick the most scalable option" | There is no universally "most scalable" option. Every choice has tradeoffs. Name them. |
| "Let's jump to the interesting parts" | Interesting without context is random. Establish high-level design first, then dive. |
| "The design looks fine, no need to review failures" | Failure analysis is not optional. Every component fails. State what happens when it does. |
| "Can you just give me the answer?" | System design is a conversation, not a lookup. Walk through the framework. |

---

## 3. CHECKER Mode -- Audit an Existing Design

Use this when reviewing a design document, architecture diagram, or interview answer.

### Infrastructure Completeness Checklist
- [ ] **Load balancer** in front of web tier?
- [ ] **Database replication** (master-slave or multi-master)?
- [ ] **Cache layer** for frequently read data? (Redis/Memcached)
- [ ] **CDN** for static assets?
- [ ] **Stateless web tier** (session in shared store)?
- [ ] **Message queue** for async/decoupled tasks?
- [ ] **Monitoring, logging, metrics** infrastructure?
- [ ] **Database sharding** strategy for large data?
- [ ] **Rate limiting** on public APIs?
- [ ] **Unique ID generation** strategy for distributed writes?

### Correctness Checks
- [ ] Writes go to master DB, reads to replicas?
- [ ] Cache expiration policy defined (not too short, not too long)?
- [ ] Sharding key distributes data evenly (no hotspots)?
- [ ] CAP theorem tradeoff explicitly chosen (CP or AP)?
- [ ] If W + R <= N, do NOT claim strong consistency.
- [ ] Failure scenarios discussed for every component?

### Scalability Checks
- [ ] Can handle 10x load by adding servers?
- [ ] Horizontal scaling path exists for web and data tiers?
- [ ] Back-of-envelope numbers validate the architecture?

### Reliability Checks
- [ ] No single point of failure at any tier?
- [ ] Failover defined for DB, cache, LB, and DC?
- [ ] Data replicated across data centers?

For component-specific audits, open the relevant chapter file and use its DESIGN REVIEW CRITERIA and COMPONENT AUDIT TABLE sections.

---

## 4. APPLIER Mode -- Guide a Design Step-by-Step

Use this when helping someone design a system from scratch.

### Phase 1: Scope (ask these questions)
1. What specific features are we building?
2. How many users? (DAU/MAU)
3. What is the read-to-write ratio?
4. What are the latency requirements?
5. What is the growth trajectory? (3mo, 6mo, 1yr)
6. What existing infrastructure can we leverage?

**Gate:** At least questions 1, 2, and 4 answered. Assumptions written down and confirmed. Do NOT proceed without scope confirmation.

### Phase 2: Estimate (invoke Ch2)
- Calculate QPS: `DAU * actions_per_user / 86,400`
- Calculate peak QPS: `QPS * 2` (or higher)
- Calculate storage: `daily_writes * object_size * retention_period`
- State all assumptions. Label all units. Round aggressively.

**Gate:** QPS and storage estimates calculated. Numbers sanity-checked. Do NOT draw diagrams without knowing the scale.

### Phase 3: High-Level Design
1. Draw the box diagram: Client -> LB -> Web Servers -> Cache -> DB
2. Add CDN if static assets exist
3. Add message queue if async processing needed
4. Walk through 2-3 use cases against the diagram
5. Get buy-in before going deeper

**Gate:** Box diagram covers all major use cases. User confirms the high-level design before deep dive. Do NOT dive into components without agreement on the overall shape.

### Phase 4: Deep Dive
Pick components from the routing table (Section 1) based on the problem:
- Rate limiting needed? -> Ch4
- Data partitioning needed? -> Ch5
- Distributed storage? -> Ch6
- Unique IDs across servers? -> Ch7
- URL shortening / aliasing? -> Ch8
- Web crawling? -> Ch9
- Notifications? -> Ch10
- Social feed? -> Ch11
- Real-time messaging? -> Ch12
- Autocomplete? -> Ch13
- Video streaming? -> Ch14
- File sync? -> Ch15

**Gate:** At least 2 components explored with tradeoffs discussed. Each deep dive references the relevant chapter file.

### Phase 5: Wrap-Up
- Name the top 3 bottlenecks and how to address them
- Discuss one failure scenario and recovery
- Mention monitoring and operational concerns
- Describe what changes at 10x scale

---

## 5. Component Selection Guide

When the design needs a specific infrastructure component, use this lookup.

| Need | Component | When to Use | When NOT to Use | Key Tradeoff | Reference |
|---|---|---|---|---|---|
| Distribute HTTP traffic | **Load Balancer** | Multiple web servers | Single server, minimal traffic | Adds infra; must itself be redundant | Ch1 |
| Speed up reads | **Cache** (Redis/Memcached) | High read:write ratio; repeated queries | Write-heavy; data changes constantly | Stale data risk; cache invalidation complexity | Ch1 |
| Serve static assets globally | **CDN** | Geo-distributed users; images/video/CSS/JS | Small local user base; infrequent assets | Cost per transfer; TTL tuning | Ch1 |
| Decouple components | **Message Queue** | Async tasks; independent scaling; buffering | All ops need sync response | Added latency; ordering complexity | Ch1 |
| Partition data across servers | **Consistent Hashing** | Dynamic server pool; elastic scaling | Static pool; single-server DB | Virtual node memory; ring maintenance | Ch5 |
| Replicate data for HA | **DB Replication** (master-slave) | Read-heavy; need failover | Write-heavy single-master bottleneck | Replication lag; failover complexity | Ch1 |
| Scale DB beyond one server | **Sharding** | Data too large for one node | Small data; need cross-record joins | Resharding; cross-shard joins; hotspots | Ch1, Ch5 |
| Throttle API traffic | **Rate Limiter** | Public APIs; cost control; DoS protection | Trusted internal services only | Adds latency; tuning rules | Ch4 |
| Generate distributed IDs | **Snowflake ID** | 64-bit, numeric, time-sortable, high throughput | Simple single-DB auto-increment suffices | Clock sync (NTP); 69-year epoch limit | Ch7 |
| Real-time bidirectional comms | **WebSocket** | Chat; live updates; presence | Request-response only | Stateful connections; harder to scale | Ch12 |
| Detect node failures | **Gossip Protocol** | Large distributed clusters | Small clusters (< 3 nodes) | Eventual detection; not instant | Ch6 |
| Sync divergent replicas | **Merkle Tree** | Permanent failure recovery | Small datasets (full compare is cheap) | Tree build/maintenance cost | Ch6 |
| Tune consistency vs latency | **Quorum (N/W/R)** | Distributed KV store with tunable consistency | Single-writer systems | Higher quorum = higher latency | Ch6 |
| Prefix-based suggestions | **Trie** | Autocomplete / typeahead | Full-text or substring search | Memory-intensive; serialization needed | Ch13 |
| Process video uploads | **Transcoding DAG** | Video platform; multi-resolution encoding | Text/image-only systems | CPU-intensive; parallelism needed | Ch14 |
| Sync files across devices | **Block-level splitting + delta sync** | Cloud drive; large file updates | Small files; write-once data | Complexity of block management | Ch15 |

---

## 6. Anti-Rationalization Table

Common excuses engineers make and why they are wrong.

| Excuse | Why It Is Wrong | What to Do Instead |
|---|---|---|
| "We don't need a load balancer yet" | Single server failure = total outage. Zero redundancy. | Always include LB when discussing scaling. Even if not needed today, discuss when you would add it. |
| "Vertical scaling is fine for now" | Hard ceiling on CPU/RAM. No failover. Exponentially more expensive. | Acknowledge limits. Always describe the horizontal scaling path. |
| "We don't need to discuss failures" | Failure handling is one of the top evaluation criteria in interviews and real designs. | For every component, state what happens when it fails. |
| "Cache isn't needed; the DB can handle it" | For high read:write ratios, cache reduces DB load by orders of magnitude. | If reads >> writes, cache is mandatory. Not using it is a red flag. |
| "NoSQL is always better for scale" | Relational DBs work for most applications. 40+ years of proven reliability. | Choose NoSQL only for specific, justified reasons (unstructured data, super-low latency, massive scale). |
| "We'll just scale horizontally" without numbers | Estimation tells you WHEN and HOW MUCH to scale. Without it, you are guessing. | Do back-of-envelope math. State assumptions. Show the work. |
| "My design is perfect" | There is always something to improve. Saying this is a red flag. | Proactively identify bottlenecks and propose improvements. |
| "Client-side rate limiting is enough" | Client requests can be forged. You may not control the client. | Implement server-side or middleware rate limiting. |
| "We can just use auto_increment for IDs" | Does not work in distributed environments. Single DB is a bottleneck and SPOF. | Use Snowflake or equivalent distributed ID generator. |
| "I'll skip the high-level and go to the interesting parts" | Without a blueprint and buy-in, deep dive may target the wrong components entirely. | Always establish high-level design first. Get agreement. Then dive. |
| "Clock synchronization is not a real problem" | Multi-machine setups experience clock drift. IDs can collide or become non-monotonic. | Address NTP. Discuss what happens under clock skew. |
| "Sticky sessions solve multi-server state" | Not scalable. Server failure loses all sticky sessions. | Use centralized shared store (Redis). Make web tier stateless. |
| "99.9% availability is good enough for everything" | 99.9% = 8.77 hours downtime/year. Payment and health systems often need 99.99%+. | Map nines to concrete downtime. Design redundancy accordingly. |
| "Monitoring can be added later" | Without monitoring, you are blind to failures. No baselines, no alerts. | Include monitoring from the start at any meaningful scale. |
| "Over-engineering shows I'm thorough" | Companies pay a high price for over-engineering. It is a "real disease." | Show practical, balanced design. Design for now, plan for growth. |

---

## 7. Scaling Triggers Quick Reference

When you see this state, add this component:

| Current State | Signal | Add | Result |
|---|---|---|---|
| Single server | Any failure = total outage | Separate web + data tiers | Independent scaling |
| Single web server | Overloaded; no failover | LB + multiple servers | Traffic distributed; auto-failover |
| Single DB | Read latency rising; CPU maxed | Master-slave replication | Reads distributed; write isolation |
| High DB read load | Repeated identical queries | Cache (Redis/Memcached) | Most reads from memory |
| Slow static content | High latency for distant users | CDN | Edge delivery |
| Stateful web servers | Cannot autoscale; sticky sessions | Stateless tier + shared session store | Free horizontal scaling |
| Single data center | Regional outage = total outage | Multi-DC + geoDNS | Geo-redundancy |
| Tightly coupled components | One slow part blocks everything | Message queue | Decoupled; async; independent scaling |
| Single DB at capacity | Disk full; queries slow | Sharding (consistent hashing) | Horizontal data distribution |
| hash(key) % N with dynamic pool | Cache miss storms on pool change | Consistent hashing + virtual nodes | Only k/n keys redistributed |
| Public APIs with no throttling | DoS; abuse; cost overruns | Rate limiter | Protected endpoints |
| Auto-increment IDs across servers | ID collisions; SPOF | Snowflake ID generator | Distributed, collision-free |

---

## 8. Integration

Standalone skill. No dependencies on other skills.

Future integration points:
- Code implementation skills could consume the architecture output from APPLIER mode
- Documentation skills could format CHECKER audit results
