---
name: architecture-ready
description: "Given a PRD, produce an architecture that says what system shape to build and why, before any code is written or any tool is chosen. Triggers on 'design the architecture,' 'system diagram,' 'monolith or microservices,' 'integration shape,' 'service boundaries,' 'data architecture,' 'how do the pieces fit,' 'ADR,' 'trust boundaries,' 'C4 diagram,' 'arc42,' 'non-functional requirements map to architecture.' Refuses architecture theater (diagrams with no load-bearing decisions), paper-tiger architecture (looks robust until first real load), cargo-cult cloud-native (Kubernetes and Kafka for a ten-user CRUD), stackitecture (stack picked and called architecture), resume-driven architecture, and 'scalable' as a claim with no numbers. Planning tier; consumes .prd-ready/PRD.md; produces .architecture-ready/ARCH.md for stack-ready, roadmap-ready, and production-ready. Does not pick tools (stack-ready), sequence milestones (roadmap-ready), or build the app (production-ready). Full trigger list in README."
version: 3.1.0
updated: 2026-11-23
changelog: CHANGELOG.md
suite: ready-suite
tier: planning
upstream:
  - prd-ready
downstream:
  - roadmap-ready
  - stack-ready
  - production-ready
pairs_with:
  - prd-ready
  - roadmap-ready
  - stack-ready
compatible_with:
  - claude-code
  - codex
  - cursor
  - windsurf
  - antigravity
  - pi
  - openclaw
  - any-agentskills-compatible-harness
---

# Architecture Ready

This skill exists to solve one specific failure mode. A founder, tech lead, or staff engineer asks Claude or ChatGPT or Gemini to "design the architecture" for a project and gets back a seven-page document with a C4 context diagram, a container diagram, a microservices breakdown, a Kafka event bus, a Redis cache, a Kubernetes deployment topology, an API gateway, and a "scalable, resilient, observable" summary. The document looks professional. It names twelve components. It cites "industry best practices." It decides nothing. Every decision is either the default a senior engineer would never write down (use HTTPS, log errors, back up the database) or the impressive-looking option that matches no constraint in the PRD (event sourcing for a CRUD app, a service mesh for a team of three, eventual consistency for an accounting ledger). The team starts building. In month three the architecture is quietly abandoned and the real architecture, the one the code actually shipped, is something else entirely, undocumented, and unexamined.

The job here is the opposite. Produce an architecture document whose every decision names the PRD number it serves, the failure mode that would flip it, the blast radius if it breaks, and the evolutionary path if it needs to change. Whose system shape is argued, not assumed. Whose component boundaries are drawn where responsibility actually transitions, not where cloud diagrams happen to line up. Whose data shape decisions precede the database pick. Whose trust boundaries are the input to production-ready's threat model, not a section anyone skims. Whose ADRs are short, dated, and retired honestly when superseded. Whose diagrams have arrows with semantics, not arrows as decoration.

This is harder than it sounds because architecture fails in a narrow but lethal band. The industry has documented the failure modes (Richards and Ford, Ford/Parsons/Kua, Kleppmann, Hohpe, the ThoughtWorks Tech Radar, the public postmortems of Knight Capital, Amazon S3, Cloudflare, Facebook BGP, Roblox Consul, and the high-profile monolith-to-microservices retreats of Amazon Prime Video, Segment, and Istio). Tooling does not catch them. C4 renderers will happily draw any diagram you hand them. Draw.io, Lucidchart, Excalidraw, Mermaid, Structurizr, Miro: none of them will tell you your container diagram has no rationale, your service boundaries cross a trust boundary without noticing, or your event-sourcing decision has no use case. The skill is the layer above the tool that catches the architecture before it ships downstream.

## Core principle: every box, every arrow, every ADR is a decision with a flip point

> **Every architectural element in the document is either a load-bearing decision (we chose X over Y, here is why, here is what would flip it, here is the blast radius if we are wrong) or it is decoration and must be deleted.**

This principle is non-negotiable. The whole taxonomy of architecture failure reduces to "elements that pretend to be decisions but are not." The architecture-theater document is diagrams without decisions. The paper-tiger architecture is decisions without failure-mode analysis. The cargo-cult cloud-native architecture is decisions without PRD grounding. The stackitecture is tool choices dressed up as architecture. The resume-driven architecture is decisions picked for the writer's career rather than the system's constraints. The non-architecture ("we'll figure it out later") is the absence of decision masquerading as agility. Every one of these fails the same test: read the architecture, point at any box, any arrow, any ADR, any threshold, and ask "what would flip this." If the answer is "nothing in particular" or "it depends," the element is not a decision, it is decoration.

The substitution corollary applies at the architectural level too. For any container, component, queue, cache, or service named in the document, substitute a near-equivalent (Postgres for MySQL, Kafka for RabbitMQ, service mesh for API gateway, modular monolith for microservices). If the rationale still reads plausibly, the rationale decided nothing specific. "We chose microservices for scale" substitutes against almost any decision; "we chose a modular monolith with three bounded contexts (orders, billing, identity) because the PRD's scale ceiling is 10k org-users and the team is 4 engineers, and we cannot afford the 3x ops overhead of distributed systems until we clear $5M ARR" does not. Specificity is the discipline. See [references/architecture-antipatterns.md](references/architecture-antipatterns.md) for the full substitution-test procedure applied to architecture documents.

## When this skill does NOT apply

Route elsewhere if the request is:

- **Product requirements** ("what should we build," "who is this for," "what are the success metrics," "write a PRD"). That is [`prd-ready`](https://github.com/hannsxpeter/ready-suite/tree/main/skills/prd-ready). architecture-ready reads `.prd-ready/PRD.md` and does not redefine the product; if the PRD is absent or empty, warn the user that designing architecture without a PRD is guessing and offer to invoke prd-ready first.
- **Specific tools, frameworks, ORMs, databases, auth providers, hosting platforms** ("Next.js or Remix," "Postgres or Mongo," "pick an auth provider," "Supabase or Firebase," "which queue"). That is [`stack-ready`](https://github.com/hannsxpeter/ready-suite/tree/main/skills/stack-ready). architecture-ready says "we need a relational store with strong consistency for orders and an event log for audit"; stack-ready picks Postgres, or Postgres plus Kafka, or whatever fits the constraints. A recommendation that names a specific tool is either out of scope (delegate to stack-ready) or an ADR that cites the stack-ready DECISION.md by reference.
- **Timeline, sequencing, milestone plans, release plans** ("build a quarterly roadmap," "what ships first," "when does the beta happen"). That is `roadmap-ready` (not yet released). architecture-ready produces the component dependency graph; roadmap-ready consumes it to produce the calendar.
- **Implementation, code organization inside a service, vertical slices, component hierarchy at the file level** ("build the user management slice," "organize the folder layout," "wire the dashboard"). That is [`production-ready`](https://github.com/hannsxpeter/ready-suite/tree/main/skills/production-ready). architecture-ready ends at service boundaries, interfaces, and responsibilities; production-ready builds the app inside those boundaries.
- **Deployment pipeline, environments, release cadence, rollback protocol** ("CI/CD pipeline," "blue-green," "canary," "rollback plan"). That is [`deploy-ready`](https://github.com/hannsxpeter/ready-suite/tree/main/skills/deploy-ready). architecture-ready names the deployment topology ("three services, edge plus two regions") as a decision; deploy-ready wires the pipeline that actually ships it.
- **Observability instrumentation, dashboards, alerts, SLOs, runbooks** ("add Honeycomb," "define SLOs," "write alert rules," "on-call runbook"). That is [`observe-ready`](https://github.com/hannsxpeter/ready-suite/tree/main/skills/observe-ready). architecture-ready names observability boundaries (where traces must propagate across services, what audit events cross trust boundaries); observe-ready wires the instrumentation.
- **Repo structure, monorepo vs. polyrepo, CI configuration, CODEOWNERS, release automation** ("set up the repo," "monorepo or polyrepo," "CI pipeline"). That is [`repo-ready`](https://github.com/hannsxpeter/ready-suite/tree/main/skills/repo-ready). architecture-ready's service count and team topology shape the decision (one repo per bounded context vs. a single monorepo with code-owner boundaries), but repo-ready owns the actual structure and tooling.
- **Adversarial security review, compliance-controls mapping, penetration testing, threat-modeling workshops.** That is the future `harden-ready` skill (not yet released). architecture-ready names trust boundaries and the high-blast-radius mutations that a threat model must cover; harden-ready tests them adversarially. The current contract: architecture-ready produces the trust-boundary inputs that production-ready's Step 2 threat model consumes.
- **UI architecture, component hierarchy, state management, client-side routing, design tokens.** That is production-ready's territory. architecture-ready operates at service and module level, not component level. "Should we use Zustand or Redux" is not an architecture decision.
- **Launch, positioning, marketing, SEO, landing pages.** That is [`launch-ready`](https://github.com/hannsxpeter/ready-suite/tree/main/skills/launch-ready). architecture-ready is internal-audience; launch-ready is external.
- **"Just ship it" requests for projects where architecture is not load-bearing.** A single-file CLI, a one-off script, a static marketing site, a toy personal project: architecture-ready should explicitly say "architecture is not load-bearing here" and skip the skill. See Step 1 for the load-bearing check; see [references/system-shape.md](references/system-shape.md) Section 1 for the "skip architecture-ready entirely" criteria.

This section is the scope fence. Every plausible trigger overlap with a sibling gets a route-elsewhere line.

## Workflow

Follow this sequence. Skipping steps produces the exact class of failure this skill exists to prevent: an architecture document that looks professional, fills every section, and decides nothing.

### Step 0. Detect state, mode, and upstream inputs

Read [references/architecture-research.md](references/architecture-research.md) and run the mode detection protocol.

- **Mode A (Greenfield).** Net-new system, no prior architecture document. Start from the PRD; if the PRD is absent, stop and invoke prd-ready first. Proceed to Step 1.
- **Mode B (Assessment).** An existing codebase already has an architecture, documented or not. Produce ARCH.md as a retroactive description of the architecture as it actually is, not as it was originally intended. Run the assessment scan before Step 1. The output replaces guesswork.
- **Mode C (Theater audit).** A prior AI-generated ARCH.md exists and fails the core principle. The ask is "fix this before it misroutes stack-ready and production-ready." Run the theater audit (Step 1.5); rewrite sections that fail.
- **Mode D (Iteration / refresh).** Existing ARCH.md is stale because the system evolved. Update with a dated changelog entry and new ADRs; do not silently rewrite past decisions. Superseded decisions get ADR status `Superseded by NNN`, not deletion.
- **Mode E (Evolution / rearchitecture).** The current architecture is breaking and a material change is planned (monolith to service extraction, service consolidation back to a modular monolith, read-replica to event-sourced projection, sync to async integration). Fork a new ARCH.md labeled with the target state; keep the current one as the "from" state; link both. Produce an evolution plan in [references/evolutionary-architecture.md](references/evolutionary-architecture.md) style.
- **Mode F (Rescue).** The architecture was approved, the team built, the system shipped, and now it is misbehaving in a way traceable to the architecture (the distributed monolith retrofit, the storage-shape mismatch, the blast-radius surprise). Diagnose the architectural root cause and plan the remediation; do not just patch the symptom.

**Upstream inputs.** If `.prd-ready/PRD.md` exists, read it. Extract: entities, flows, NFRs (latency, throughput, availability, scale ceilings), integration points, trust boundaries, compliance constraints, appetite, explicit deferrals to architecture. If `.prd-ready/HANDOFF.md` exists, it already pre-fills the Architecture-ready inputs section; use it. If neither exists, warn the user: "architecture-ready without a PRD is guessing. Either produce one (invoke prd-ready) or state the PRD-equivalent inputs inline as assumptions." Do not proceed silently.

**Passes when:** a mode is declared in writing, the corresponding research block from `architecture-research.md` is produced, the PRD (or PRD-equivalent assumptions) is read and summarized in one paragraph, and for Mode C, at least one failing element is quoted.

### Step 1. Architecture load-bearing check and pre-flight

Read [references/system-shape.md](references/system-shape.md) Section 1. Not every project needs architecture-ready. Before running the full skill, answer the load-bearing check:

**Architecture is load-bearing here if any of these are true:**

1. **More than one persistence layer is in play.** A database plus an object store, a database plus a queue, a database plus an event log, a database plus a cache that is load-bearing (not just hot-path). Single Postgres is rarely load-bearing architecture; Postgres plus S3 plus Redis plus Kafka usually is.
2. **More than one deployable service is in play.** Even two is enough: the interface between them is architectural, whether it is a REST call, a queue, or a shared database.
3. **A third-party integration is load-bearing in a failure mode.** Stripe, Twilio, a partner API, an internal service the team does not own: the failure mode, retry policy, idempotency discipline, and trust boundary are all architectural.
4. **A non-functional target in the PRD constrains the shape.** A p95 latency budget tighter than 200ms for a multi-step operation, a compliance requirement that forbids PII in one component, a data-residency requirement that constrains where data is stored, a consistency requirement that forbids eventual consistency in an accounting path.
5. **The team is larger than two engineers and will grow.** Team Topologies and Conway's Law: communication structure becomes software structure. Architectural boundaries set team boundaries, and team boundaries set architectural boundaries. If the team plans to grow beyond Dunbar ranges (5-7 engineers for a single cognitive load per Team Topologies), architecture is load-bearing now.
6. **The product will live longer than 12 months and will be maintained by people other than the original authors.** Architecture is for the future team.

**Architecture is NOT load-bearing if all of these are true:**

- One engineer, one service, one database, no partner integration, no compliance constraint, appetite under 8 weeks, no intent to scale the team, no intent to maintain past the initial launch.
- The problem fits in a Rails-style "just ship it" shape: single datastore, single deployable, sync request-response everywhere, no queues, no events, no multi-region.

If the load-bearing check fails (none of the "load-bearing" criteria are true), say so in one paragraph, write a one-page "minimal ARCH.md" covering only the system shape ("one service, one database, sync"), the data shape (entities, relationships), and the trust boundary (who can mutate what), and stop. Do not produce a ten-page architecture document for a single-service CRUD app. That is itself a failure mode.

If the check passes, answer the 8 pre-flight questions in writing:

1. **What is the system for.** One paragraph copied or adapted from the PRD's Problem section.
2. **What is the appetite.** Weeks, months, quarters. From the PRD.
3. **What is the honest scale ceiling in 12 months.** Users, requests per second, data volume, tenants. From the PRD or stated as an explicit assumption.
4. **What are the binding non-functional constraints.** Latency, throughput, availability, consistency, compliance, data-residency. From the PRD, or flagged as an open question with owner and due date if absent. Silence on these is not an answer; guessing is worse.
5. **What is the team shape.** Size now, size in 12 months, language depth, on-call posture. From the PRD, or stated as assumption.
6. **What is the incumbent stack, if any.** Brownfield projects inherit constraints; greenfield declares them open. Do not pre-pick; note what would bias the decision.
7. **What are the external integrations, now and projected.** Named, with the failure mode each introduces.
8. **What is explicitly deferred from the PRD to architecture.** The PRD's "Explicitly deferred to architecture" block, copied verbatim. These are the decisions the PRD intentionally did not make and architecture-ready must resolve.

If any answer is "I don't know yet," flag it as an open question with an owner and a due date; do not fabricate. If the user's input is one sentence ("design the architecture for my app"), do not invent eight answers. Read the PRD; if the PRD does not have the answer, ask the user the minimum set that default assumptions cannot cover, state explicit assumptions for the rest, and proceed.

**Passes when:** the load-bearing check is run and recorded, all 8 pre-flight questions are answered in writing (or flagged as open questions with owners), and explicit assumption statements replace any missing PRD content.

### Step 1.5. Mode C theater audit (only if a prior AI-generated ARCH.md exists)

Skip if not Mode C. Otherwise, read [references/architecture-antipatterns.md](references/architecture-antipatterns.md) and run the audit:

- Quote every C4 container or component in the existing ARCH.md. For each, apply the flip-point test: "what would flip this choice." Elements with no flip-point answer are marked for rewrite or deletion.
- Quote every ADR. An ADR that reads "we chose X because it is industry-standard" or "we chose X because it scales" is not an ADR, it is an assertion; mark for rewrite with a concrete trade-off.
- Scan for banned phrases: `scalable`, `resilient`, `observable`, `cloud-native`, `industry-standard`, `best-in-class`, `future-proof`, `microservices-based` used as a claim without a number, a threshold, or a stated trade-off. Every instance is a defect.
- Scan for cargo-cult: Kubernetes, Kafka, service mesh, event sourcing, CQRS, API gateway mentioned without a PRD-grounded justification tied to a specific non-functional constraint. If the justification is "scale" without a number, the element is cargo-cult.
- Scan for stackitecture: tool choices presented as architecture ("we use Next.js plus Postgres plus Prisma" without a system-shape decision above it). If the architecture is a stack list, it is not architecture.
- Check the data architecture section: storage-shape decisions (relational vs. document vs. key-value vs. time-series vs. event-log vs. graph) must precede the database pick. If the section jumps to "Postgres" without naming a storage shape first, it is stackitecture in data clothing.
- Check the trust boundaries section: is it empty, missing, or three words ("auth, authz, encryption")? That is the missing-threat-model failure mode.

Output the audit as a list of specific defects with the failing quote and the required remediation. Do not rewrite yet; decide first what fails, then proceed to the regular workflow.

**Passes when:** every failing section has a specific defect quote, the dominant failure mode is named (architecture theater / paper tiger / cargo-cult cloud-native / stackitecture / resume-driven / non-architecture), and the Mode C remediation plan is listed in writing.

### Step 2. System shape

Read [references/system-shape.md](references/system-shape.md). The most load-bearing decision in the document. Pick one shape; do not hedge.

The seven shapes:

1. **Single-service monolith.** One deployable, one database, synchronous request-response. The default. The Rails / Django / Phoenix / Laravel shape. The Basecamp / 37signals shape (Kamal plus a single Rails app). Cheapest to operate; lowest coordination cost; hardest-scaling at the extreme.
2. **Modular monolith.** One deployable, one database, but internal bounded contexts with module boundaries the compiler or the test suite enforces. The Shopify shape. The GitHub shape. The current Stack Overflow shape. The sweet spot for teams of 3-30 engineers with clear bounded contexts but no operational maturity for distributed systems.
3. **Service-oriented (coarse-grained services).** A handful of deployables (3-7), each owning a bounded context with its own database. Synchronous request-response between services, often with some async events for audit. The Amazon-pre-microservices shape, before Bezos's two-pizza-team memo.
4. **Microservices (fine-grained services).** Many deployables (20+), each with its own database, each owned by a small team, orchestrated by a service mesh or an API gateway. Conway's-Law-driven. Worth it above a team-count threshold (Team Topologies puts the threshold around 50-100 engineers; real-world examples below 20 engineers almost always regret it).
5. **Serverless / function-as-a-service.** Functions over a managed runtime (Lambda, Cloudflare Workers, Vercel), with an external datastore. Strong for bursty, event-driven, or sparsely-triggered workloads; cold start and vendor-lock-in pain for long-lived, stateful, or low-latency workloads.
6. **Event-driven.** The system's primary integration shape is asynchronous events on a log (Kafka, Kinesis, Redpanda, RabbitMQ streams). Read-sides project off the event log. CQRS optional. Event sourcing optional and separable. Strong for audit, replay, integration-heavy systems; high operational complexity; wrong for sync-heavy CRUD.
7. **Edge-native.** Compute at the edge (Cloudflare Workers, Deno Deploy, Vercel Edge), data replicated to the edge or held in edge-friendly stores (D1, Turso, Durable Objects). Strong for global-low-latency read-heavy workloads; wrong for strong-consistency write-heavy workloads.

The rules:

- **Default to modular monolith unless a specific constraint rules it out.** This is the industry lesson of 2020-2026: Amazon Prime Video's audio-quality monitoring team consolidated a specific distributed pipeline to a single service in 2023 and published a 90% cost reduction (commonly mis-cited as "Amazon abandoned microservices"; read the post directly before citing); Segment consolidated microservices to a monolith in 2018; Istio merged its control-plane microservices back to a single binary in 2020. Shopify and GitHub continue to operate modular monoliths at internet scale. ThoughtWorks has kept microservices at "Trial" not "Adopt" on the Tech Radar since 2018. The default "microservices" answer is the 2014-2019 pattern and has not aged well.
- **Microservices require a forcing function.** The three acceptable forcing functions: (1) team size requires independent deploy cadences, (2) services have genuinely different scale or availability curves that justify independent scaling, (3) regulatory or security boundaries require physical separation. Absent one of these, microservices are a cost, not a benefit.
- **Serverless is right for bursty, event-driven, and stateless workloads; wrong for long-lived stateful workloads.** The vendor-lock-in argument is secondary to the workload-shape argument.
- **Event-driven is right for integration-heavy systems where the event log is load-bearing for audit, replay, or multi-consumer fan-out; wrong for simple CRUD.** Event sourcing is a further step beyond event-driven and is almost always wrong unless the audit/replay need is concrete.
- **Edge-native is right for global-low-latency read-heavy workloads; wrong for write-heavy or strong-consistency workloads.**

The decision record: write ADR-001-system-shape.md documenting which shape you picked, the PRD constraints it satisfies, the alternatives you rejected and why, the flip point that would reverse the choice, and the blast radius if you are wrong. Keep it to two pages maximum. See [references/adr-discipline.md](references/adr-discipline.md).

**Passes when:** one shape is picked, ADR-001 is written, the alternatives are named and rejected with reasons, the flip point is stated, and the blast radius is named. "It depends" is not an acceptable answer; name the weights you applied.

### Step 3. Component breakdown

Read [references/component-breakdown.md](references/component-breakdown.md). Given the system shape, name the components. "Component" means the internal bounded contexts in a modular monolith, the services in a service-oriented or microservices architecture, the functions or function-groups in a serverless architecture, or the consumers and producers in an event-driven architecture.

For each component, name:

1. **A bounded context.** Ordering. Identity. Billing. Inventory. Catalog. Not "UserService" or "CoreAPI" (Conway's-Law, layer-by-layer, too generic). The bounded context comes from the domain (Eric Evans' DDD) and is named in the PRD's entities.
2. **A responsibility.** One sentence. "Owns the order lifecycle from cart to fulfillment, including pricing at time of order and state transitions." Not "handles orders."
3. **An interface.** The shape of communication in and out. "REST over JSON, authenticated with tenant-scoped API keys." "Consumes OrderPlaced events from the event log; emits OrderFulfilled." "Synchronous Postgres row-level reads from the Catalog schema." Specify sync or async, the wire format, and the idempotency posture.
4. **Ownership of data.** Which entities it writes. The canonical rule: one writer per entity, many readers. The "distributed monolith" antipattern is two services writing to the same table; if that appears, either merge the services or split the table.
5. **Dependencies.** Other components it depends on. Outputs the component dependency graph, consumed by roadmap-ready.
6. **Failure posture.** What happens if this component fails. "Orders is the critical path; downtime stops revenue." "Inventory sync is eventually consistent; degrades to last-known stock counts for 60 seconds before flagging stale." Every component has a failure posture; silence here is the "cascading failure surprise" antipattern.

The rules:

- **A component does one thing.** If the responsibility sentence is a compound ("handles orders AND pricing AND inventory"), split it or consolidate the others into it. The compound is a red flag for a boundary drawn wrong.
- **Granularity is a decision.** There is no "right" number of components. The Shopify modular monolith has hundreds of internal modules; Amazon has thousands of microservices; a single-founder SaaS has one component. The question is: does a proposed split or merger serve a constraint in the PRD (team size, deploy cadence, scale curve, security boundary)? If yes, do the split; if no, keep the simpler shape.
- **Avoid anemic services.** A service that is a thin wrapper over a database table is not a service, it is a CRUD endpoint that belongs inside the bounded context that owns the entity. The "user service," "auth service," "notification service" decompositions are almost always anemic in small systems.
- **Avoid God services.** A service that owns half the domain is the inside of a monolith with a REST API painted on. Split by bounded context, not by "big thing" vs. "small thing."

Output a table of components with all six fields filled, plus a text description of the boundaries (what goes in each, what does not) that a new engineer could use to place a new feature on day one.

**Passes when:** every component has all six fields; the component dependency graph is explicit (consumed by roadmap-ready); no component has a compound responsibility; no component is anemic (thin-wrapper-over-table); no component is a god (owns half the domain).

### Step 4. Data architecture

Read [references/data-architecture.md](references/data-architecture.md). Data outlives code. The data architecture section is the most load-bearing in the entire document on a multi-year horizon.

Three decisions:

1. **Entities and relationships.** Copied or refined from the PRD's entity list. For each entity, name: key attributes, cardinality relationships, tenancy model (single-tenant, multi-tenant shared-schema, multi-tenant per-tenant-schema, multi-tenant per-tenant-database), lifecycle (immutable, append-only, mutable, soft-delete, hard-delete), and retention policy. Produce a simple ERD (text or Mermaid) showing the top 5-15 entities; deeper detail belongs in production-ready's schema work.
2. **Storage shape per entity group.** NOT a database pick. A storage shape. The shapes:
   - **Relational (row-oriented, strong-consistency, transactional).** The default. Entities with relationships, transactional operations, strong-consistency needs (orders, inventory, accounting, identity).
   - **Document (JSON-shaped, flexible schema, read-heavy).** Content, profile data, product catalogs with variant explosions, configuration. Use when schema flexibility exceeds transactional need.
   - **Key-value (fast lookup, simple structure).** Sessions, caches, feature flags, short-lived state. Redis, Memcached, DynamoDB.
   - **Time-series (append-only, time-indexed, aggregation-heavy).** Metrics, audit logs at high volume, IoT, analytics events. TimescaleDB, InfluxDB, Prometheus, ClickHouse.
   - **Event log (immutable, append-only, ordered).** The source of truth in an event-driven architecture. Kafka, Kinesis, Redpanda, EventStoreDB.
   - **Search (inverted index, relevance-ranked).** Full-text search, faceted search, log search. Elasticsearch, OpenSearch, Meilisearch, Typesense, Postgres `tsvector`.
   - **Graph (traversal, relationship-first).** Social graphs, org charts, recommendation graphs, fraud-ring detection. Neo4j, NebulaGraph, Postgres with recursive CTEs for small scale.
   - **Object store (blob, large, read-heavy).** Files, images, videos, backups. S3, GCS, Cloudflare R2.
   
   For each entity group, name the shape and one-sentence reason. The shape decision precedes and constrains the database pick, which is stack-ready's job.
3. **Consistency, transactionality, and cross-entity invariants.** Which operations are atomic. Which are eventually consistent. Which invariants must hold (e.g., "an order's total equals the sum of its line items at commit time"). The PRD's NFRs constrain this; the architecture names the invariants and their enforcement point. Document distributed-transaction antipatterns explicitly rejected: "we do not span transactions across services; instead, we use the outbox pattern for cross-service state."

For each load-bearing entity group, write an ADR if the storage-shape choice is non-obvious. Example: ADR-003: Event log for order audit trail. Cite the PRD number that drives it (compliance retention, regulatory replay, partner reconciliation).

**Passes when:** every entity has a tenancy model and a lifecycle; every entity group has a named storage shape; cross-entity invariants are named with enforcement points; no database is picked by name in this section (that is stack-ready's job); ADRs cover non-obvious storage-shape choices.

### Step 5. Integration architecture

Read [references/integration-architecture.md](references/integration-architecture.md). How components and external systems talk. The dimension that most often gets handwaved in AI-generated architecture.

Four decisions per integration:

1. **Sync or async.** The most load-bearing choice in integration. Sync is request-response, caller blocks on callee, failure is visible immediately. Async is send-and-move-on, failure is invisible until something drains, coupling is looser. The rule: sync for tight coupling where the caller genuinely needs the callee's response to continue; async for fan-out, audit, and eventual-consistency flows. Mixing sync and async in the same flow without a clear handoff is the "distributed monolith" antipattern.
2. **Transport shape.** REST/JSON, gRPC, GraphQL, event log, message queue, webhook, RPC over shared DB, file transfer. Name the choice and the failure mode each transport introduces.
3. **Idempotency posture.** At-least-once, at-most-once, exactly-once (never real; always at-least-once plus idempotent receivers). Name the idempotency key, the retry policy, the dedup window. Idempotency is especially load-bearing for mutations over unreliable networks (webhooks, partner integrations, payment flows).
4. **Failure mode and blast radius.** What happens if the integration fails. Circuit breaker, retry with exponential backoff plus jitter, dead-letter queue, graceful degradation, hard failure. The PRD's availability NFRs constrain which failure modes are acceptable.

Named patterns that come up repeatedly:

- **Outbox pattern.** Write-to-DB and emit-event in the same local transaction. Avoids the dual-write problem.
- **Saga pattern.** Long-running distributed transaction coordinated by events or a workflow orchestrator. Compensating actions instead of rollback.
- **CQRS.** Read and write models separate. Valid when read and write patterns genuinely differ; overkill when they do not.
- **Event sourcing.** The event log IS the source of truth; state is a projection. Valid when audit or replay is load-bearing; overkill when it is not.
- **API gateway.** Single entry point for external traffic. Valid at microservices scale with cross-cutting auth, rate-limiting, and routing needs; overkill for monoliths.
- **Service mesh.** Sidecar proxies enforcing network policy, mTLS, observability. Valid at 20+ services with consistent networking needs; overkill below that.

**The cargo-cult check.** For each of the patterns above, if it appears in the architecture, the ADR must name a concrete PRD constraint it serves. "We use event sourcing" is not an ADR; "we use event sourcing for the order ledger because the PRD mandates 7-year regulatory retention with replay for audit, and the alternative of audit-log-as-projection on a mutable schema cannot guarantee replay fidelity" is an ADR.

**Passes when:** every integration has all four decisions stated; idempotency is explicit for every mutation over the network; cargo-cult patterns (event sourcing, CQRS, service mesh, API gateway) are either justified with a PRD-grounded ADR or rejected with a reason.

### Step 6. Non-functional architecture (the numbers)

Read [references/non-functional-architecture.md](references/non-functional-architecture.md). The PRD stated NFRs as targets. The architecture maps them to shape: what does the system have to look like to meet those targets.

For each NFR dimension, answer:

1. **Latency budget.** p50, p95, p99 targets from the PRD. Map the budget across the request path: network, auth, DB query, business logic, external calls, response serialization. If the budget does not fit the shape, the shape is wrong or the budget is wrong; name which. Example: if the PRD says p99 under 100ms for a request that fans out to three external APIs averaging 80ms each, the budget is infeasible with that shape; either the shape must change (precompute, cache, remove the fan-out) or the budget must change.
2. **Throughput capacity.** Requests per second or events per second at the scale ceiling from the PRD. Capacity per component. Bottleneck identification. Scaling strategy per component (horizontal, vertical, read replicas, sharding, caching). If a component cannot hit the capacity, the architecture must change.
3. **Availability target.** The PRD's monthly uptime target mapped to component-level availability. A 99.9% end-to-end target with three components on the critical path requires each component at ~99.97% or higher, minus the correlated-failure slack. Document the availability chain. If the math does not add up, the architecture must add redundancy or the target must change.
4. **Scale horizons.** Where does this architecture hit its ceiling. Concrete numbers. "Single-writer Postgres: writes hit a ceiling around 5-10k TPS on standard hardware without partitioning." "Serverless cold starts add 100-500ms at the p99 for low-traffic functions." Name the ceiling per load-bearing component so the team knows when rearchitecture becomes necessary.
5. **Resource envelope.** Honest estimate of the infra the architecture requires: compute, storage, network egress, managed-service tiers. Cost envelope per month at launch and at 12-month scale. The stack-ready skill picks the specific SKUs; this section names the shape of the envelope.
6. **Data-residency and compliance posture.** Where data lives, which jurisdictions, which compliance regimes apply, which components are in-scope vs. out-of-scope for each regime. Every PRD compliance constraint maps to a component placement decision.

The mandatory math check: write out the latency chain, the availability chain, and the throughput chain. If any chain fails the math, the architecture does not meet the PRD and must change. "Scalable" is not a number. "Sub-second" is not a number. p95 is a number; p99 is a stronger number; p99.9 is the strongest.

**Passes when:** every PRD NFR dimension has a concrete architectural mapping with numbers; the latency, availability, and throughput chains compute to targets the PRD requires; every "scalable," "performant," "reliable," "observable" claim has been replaced with a number or flagged as an open question with an owner.

### Step 7. Trust boundaries

Read [references/trust-boundaries.md](references/trust-boundaries.md). Where authority transitions in the system. The canonical input to production-ready's Step 2 threat model.

Four boundaries to name:

1. **Network edge.** Where external traffic enters the system. Who speaks HTTP/WSS/gRPC from outside; what is exposed publicly; what sits behind the edge. Name: TLS termination, WAF posture, rate limiting, bot defense, edge caching if any.
2. **Authentication.** How identity is established. Users, machines, services. Session or token model, issuer, audience, expiry, refresh posture. The boundary between authenticated-unidentified and authenticated-identified.
3. **Authorization.** How an authenticated identity is allowed to do a thing. RBAC, ABAC, ReBAC, tenant isolation. The boundary between any-authenticated-user and this-specific-authenticated-user for a specific resource.
4. **Tenant / data isolation.** In multi-tenant systems, the boundary between one tenant's data and another's. Shared-schema with tenant-column filters, per-tenant schema, per-tenant database, per-tenant deployment. The consequences of a breach of this boundary are catastrophic; the boundary must be explicit and tested.

For each boundary, name:

- **Where it sits in the component diagram.** Edge router vs. auth service vs. DB row-level security vs. middleware. Multiple reinforcing layers are acceptable and common; a single weak layer is a risk.
- **What it protects.** The asset on the other side. Customer data, payment data, internal metadata, admin actions.
- **What an attacker gains if it falls.** Concrete blast radius. "Cross-tenant data read" is concrete; "compromised security" is not.
- **How it is enforced.** Cryptographic, code-level, DB-level, network-level, policy-level. Defense-in-depth means at least two independent enforcement layers for load-bearing boundaries.

The highest-blast-radius mutations deserve explicit callout: cross-tenant DELETE, admin impersonation, billing modifications, password resets, API key rotations, export-all-data endpoints. These are what production-ready's threat model will scrutinize; they must be named here.

**Passes when:** all four boundaries are named with all four attributes; the highest-blast-radius mutations are explicitly listed; defense-in-depth is in place for load-bearing boundaries (or the single-layer boundary is explicitly acknowledged as an accepted risk with rationale).

### Step 8. ADR discipline

Read [references/adr-discipline.md](references/adr-discipline.md). Architectural Decision Records are short, dated, and retired honestly. The skill requires at least three foundational ADRs produced during the workflow (ADR-001 system shape from Step 2, ADR-002 storage shape from Step 4, ADR-003 trust-boundary model from Step 7) and additional ADRs for every non-obvious decision.

Format (Michael Nygard 2011, lightly adapted):

```markdown
# ADR-NNN: [Decision title, short, imperative]

## Status
[Proposed | Accepted | Superseded by ADR-MMM | Rejected | Deprecated]

## Date
YYYY-MM-DD

## Context
[The forces at play. The PRD constraints. The state of the system at decision time.]

## Decision
[What we chose. One paragraph.]

## Rationale
[Why we chose it over the alternatives. Cite the PRD number or architectural constraint that drove it.]

## Alternatives rejected
- [Alternative X]: rejected because [reason].
- [Alternative Y]: rejected because [reason].

## Consequences
[What becomes easier. What becomes harder. What is now constrained.]

## Flip point
[The signal that would force us to reverse this decision. Concrete: a scale number, a team-size threshold, a cost curve, a compliance event.]

## Blast radius if wrong
[If we are wrong about this, what has to change. Weeks, months, rewrite level.]
```

Rules:

- **Write ADRs at decision time, not retroactively.** Retroactive ADRs rationalize; real ADRs record. If you find yourself writing an ADR months after the decision, label it `ADR-NNN (retroactive)` and note the date the decision actually shipped.
- **Superseded, not deleted.** When a decision is reversed, the old ADR stays with status `Superseded by ADR-MMM`, and the new ADR cites the old one. The history is the point.
- **Keep ADRs short.** Two pages maximum. Long ADRs are design documents pretending to be decisions.
- **One decision per ADR.** If you are writing an ADR that covers three choices, split it.
- **Store ADRs with the project, not in a wiki.** `.architecture-ready/adr/NNN-slug.md`. They live with the code, version with it, and get reviewed in PRs when they change.

**Passes when:** at least ADR-001, ADR-002, and ADR-003 are written; every non-obvious architectural decision has an ADR; every ADR has all eight required fields (Status, Date, Context, Decision, Rationale, Alternatives rejected, Consequences, Flip point, Blast radius).

### Step 9. Diagrams (C4 as default)

Read [references/diagrams.md](references/diagrams.md). Diagrams carry decisions, not decoration. The skill uses the C4 model (Simon Brown) as the default; arc42 and 4+1 views are alternatives for specific contexts.

The C4 levels to produce:

1. **Level 1: System Context diagram.** Required for Tier 1. One diagram: the system as a box, the users as actors, the external systems as boxes, with arrows labeled with the interaction (not with technology). Answers "what is this system, who uses it, what does it depend on."
2. **Level 2: Container diagram.** Required for Tier 2. One or more diagrams: the deployables inside the system (services, databases, queues, caches, frontends), with arrows labeled with protocol and purpose. Answers "what does the system look like inside, what talks to what."
3. **Level 3: Component diagram.** Required for Tier 2 for each bounded context of load-bearing complexity. Shows internal components of a container (modules, packages, classes of sufficient architectural weight). Do not over-diagram: not every container needs a component diagram; the ones with architectural decisions worth recording do.
4. **Level 4: Code diagram.** Almost never worth drawing. Code is better read than diagrammed.

Rules for every diagram:

- **Every arrow has a label.** "Uses" is not a label. "POST /api/orders (REST/JSON, authenticated)" is a label. "Emits OrderPlaced events (async, Kafka, at-least-once)" is a label.
- **Every box has a responsibility.** The responsibility is the box's one-sentence role; if the responsibility does not fit on the diagram, put it in the caption, not in the diagram legend.
- **Diagram what the ADRs record, not more.** If the diagram shows a component, a database, a queue, or an edge that is not covered by an ADR, either write the ADR or remove the element. Diagrams without ADRs are decoration.
- **Use text formats that version-control well.** Mermaid, PlantUML, Structurizr DSL, D2, Graphviz DOT. Not PNG exports from Lucidchart or Miro screenshots. The diagram must be editable by the next person without re-buying a license.
- **Keep diagrams current.** A diagram out of date is worse than no diagram. At every tier boundary and every ADR that changes the shape, re-render. Consider generating C4 diagrams from Structurizr DSL in CI so drift is visible.

Anti-patterns to refuse:

- **Diagrams with cloud-vendor icons as architecture.** AWS boxes, GCP hexagons, Azure slabs. These diagram the deployment, not the architecture; they belong in deploy-ready, not here.
- **Diagrams that mix abstraction levels.** A container diagram with code-level functions on it is confused.
- **Diagrams with more than 15 boxes.** If it does not fit, split into multiple diagrams at consistent abstraction levels.
- **Rainbow diagrams where color carries information but is not in the legend.** Color is decoration unless legended.

**Passes when:** Level 1 Context diagram exists (Tier 1); Level 2 Container diagram exists with every arrow labeled (Tier 2); Level 3 Component diagrams exist for every architecturally-weighty bounded context (Tier 2); all diagrams are in a version-controllable text format; every element in every diagram is covered by an ADR or is a labeled PRD-sourced actor.

### Step 10. Evolutionary architecture and fitness functions

Read [references/evolutionary-architecture.md](references/evolutionary-architecture.md). Architecture decays. The team forgets the decisions, the constraints drift, new features push the shape into places the architecture did not anticipate. Without conformance testing, the architecture as documented and the architecture as implemented diverge. This is the classic "architecture document and reality are not the same thing" failure.

Fitness functions (Ford, Parsons, Kua) are automated tests that fail when the architecture drifts from its intent. The skill requires at least three fitness functions written or named per Tier 3:

1. **A dependency conformance check.** "Module A must not depend on Module B." Tools: ArchUnit (Java/Kotlin), NetArchTest (.NET), dependency-cruiser (JS/TS), archlint or custom Python scripts for Python. Runs in CI. Fails the build if the dependency graph violates the ADR-named boundaries.
2. **A data-ownership conformance check.** "Only Component X writes to Table T." Query the schema's grants, or inspect static-analysis of write paths. Runs in CI or nightly.
3. **An NFR conformance check.** A load test, synthetic probe, or SLO alert that fires when a p95 latency, throughput, or availability target from Step 6 is violated. Crosses into observe-ready's territory; architecture-ready names the function; observe-ready wires it.

Additional fitness functions are encouraged:

- **Trust-boundary conformance.** Lint rule that forbids bypassing the middleware that enforces a trust boundary.
- **Idempotency conformance.** Test that retries of every mutation produce the same end state.
- **Tenant-isolation conformance.** Integration test that tenant A cannot read tenant B's data through any public endpoint.
- **Schema-drift detection.** CI check that migrations are forward-only and backward-compatible for the rollout window.

The fitness-function section is not "nice-to-have." It is the mechanism by which the architecture stays alive. Without it, the ARCH.md becomes a historical document the next team ignores.

**Passes when:** at least three fitness functions are named with their enforcement point (CI, runtime, nightly); tooling is identified for each; for Tier 3, at least one is actually wired and running (not just documented).

### Step 11. Downstream handoff block

Read [references/architecture-research.md](references/architecture-research.md) Section 8. Write `.architecture-ready/HANDOFF.md` in the user's project directory. This artifact is the contract with the three downstream skills.

The handoff block has three sub-sections, one per downstream consumer:

#### To stack-ready (live, v1.1.5)

Populates the constraint map that stack-ready consumes as pre-filled input:

```markdown
## Stack-ready inputs from architecture

### Storage shapes
- [Entity group X]: [storage shape]. Rationale: [one line citing PRD or NFR].
- [Entity group Y]: [storage shape]. Rationale: [one line].

### Compute shapes
- [Component A]: [runtime shape: long-running process / serverless function / edge worker / batch job].
- [Component B]: [runtime shape].

### Integration shapes
- [Integration X]: [sync REST / async events / queue / webhook / file transfer]. Requirements: [idempotency, retry, DLQ].

### Non-functional constraints (from Step 6)
- Latency budget per request path: [...]
- Throughput target at 12 months: [...]
- Availability target: [...]
- Compliance: [HIPAA / PCI / SOC 2 / GDPR / none]. In-scope components: [...]

### Hard constraints for stack picks
- [e.g., "Data must reside in EU"]
- [e.g., "Must have BAA for PHI-handling components"]
- [e.g., "Single Postgres per component (no distributed transactions)"]
```

#### To roadmap-ready (not yet released)

```markdown
## Roadmap-ready inputs from architecture

### Component dependency graph
[Textual representation: component X depends on Y, Y depends on Z. Cycle-free. The order of build follows the topological sort of this graph.]

### Load-bearing-first ordering
[Which components must exist before others can be meaningfully built: the trust-boundary layer, the data layer, the core domain components, then integration components, then peripheral components.]

### Risk-ordered items
[Rabbit holes from the PRD that architecture now has more insight on: what is known to be hard, what the team should tackle while they are fresh, what they can defer.]

### Evolution plan (if Mode E)
[Sequence of architectural changes, each paired with a reversible step and a fitness function that fires on the transition.]
```

#### To production-ready (live, v2.5.6)

```markdown
## Production-ready inputs from architecture

### System shape
[Copy the ADR-001 decision title and the one-paragraph decision.]

### Component boundaries
[Per component: bounded context, responsibility, interface, data ownership. Copied from Step 3.]

### Trust boundaries for Step 2 threat model
[Copy Step 7 wholesale. The four boundaries with their four attributes each. The highest-blast-radius mutations.]

### Data model shape
[Entities, tenancy model, lifecycle, storage shape per entity group. Copied from Step 4.]

### Integration shapes and idempotency
[Per integration: sync/async, transport, idempotency key, retry posture. Copied from Step 5.]

### Non-functional targets for Step 6 and Step 8
[Latency, throughput, availability, compliance. Copied from Step 6.]

### ADRs
[Pointers to .architecture-ready/adr/ directory. production-ready's Step 5 ADR discipline extends this corpus; it does not create a parallel one.]

### Fitness functions
[Pointers to Step 10 outputs. production-ready's Step 7 tests extend these; they do not duplicate.]
```

**Passes when:** `.architecture-ready/HANDOFF.md` exists, every sub-section is filled or explicitly deferred with reason, and the artifact reads standalone (a downstream skill reads it without having to open ARCH.md to make its own pre-flight work).

### Step 12. Alignment and sign-off

Architecture docs need stakeholder attestation, same as PRDs. The sign-off roster is lighter than a PRD's but real.

| Tier | Required signers |
|---|---|
| Tier 1 (Sketch) | Tech lead, one senior engineer |
| Tier 2 (Contract) | Tier 1 signers plus one principal/staff engineer or architect, plus PM (for scope check against PRD) |
| Tier 3 (Living) | Tier 2 signers plus security/compliance lead (for regulated domains), plus SRE/platform lead (for operational posture) |

Each signer attests to a specific thing:

- **Tech lead** attests to: system shape is appropriate, component boundaries are buildable, ADRs are sound.
- **Senior engineer** attests to: the data model is workable, the integration patterns are implementable, the fitness functions are real.
- **Principal/staff/architect** attests to: the architecture serves the PRD's non-functionals, the evolutionary posture is sound, the blast-radius analysis is honest.
- **PM** attests to: scope matches the PRD, no features the PRD cut have been re-added, the appetite has not been silently stretched.
- **Security/compliance** attests to: trust boundaries are real, compliance components are correctly scoped.
- **SRE/platform** attests to: NFR chains are achievable, operational posture is within the team's capacity.

The sign-off section records each signer's name, date, and specific attestation. No blanket "approved."

**Passes when:** for the current tier, every required signer has attested in writing with name, date, and specific attestation. Missing signatures block the tier.

### Step 13. Iterate-vs-freeze lifecycle

Architecture is living. Four states:

1. **Draft.** Pre-Tier 1 sign-off. Anyone can edit; no changelog required.
2. **Living.** Tier 1 or Tier 2 signed. Edits allowed; every edit requires a changelog entry (date, author, section, ADR number if a decision, one-line summary). Every decision reversal is a new ADR that supersedes the old one; the old ADR is not deleted.
3. **Soft-frozen.** Tier 2 signed, build in progress, Tier 3 pending. Changes require tech-lead approval and broadcast. Additions and refinements are welcome; reversals trigger a new Tier 2 sign-off.
4. **Living-with-conformance.** Tier 3. Fitness functions are running. Drift is visible in CI. The ARCH.md is the source of truth, checked against reality continuously.

Change classification:

- **Refinement.** Clarification, diagram update, new ADR for a previously-unrecorded decision. Stays in the document; logged.
- **Extension.** New component, new integration, new ADR. Requires tech-lead approval; may trigger a new Tier 2 sign-off if the system shape changes.
- **Reversal.** An existing decision is overturned. New ADR supersedes old one; requires the tier's original signers to re-attest or a new principal/staff engineer to sign off.
- **Rearchitecture.** A material change (monolith-to-services, sync-to-async, cloud migration). Fork a new ARCH.md labeled by target state; old ARCH.md stays live as the "current" until the new one is signed and built.

Broadcast discipline: every change in Living or Soft-frozen state is announced. Engineering cannot discover architectural changes by re-reading the ARCH.md; the broadcast is mandatory. Silent edits are how architecture documents become ignored.

**Passes when:** the ARCH.md has a current state declared, a changelog section with every edit dated and attributed, an ADR-supersession chain where applicable, and a broadcast record for changes in Living or Soft-frozen state.

### Step 14. Staleness check

At the end of every run, print:

```
Skill version: architecture-ready [current skill version]
Last updated: [frontmatter updated date]
Current date: [today]
```

If the skill version is older than 6 months relative to today, warn the user. Dimensions most likely to have shifted: cloud-vendor primitives (managed databases, edge runtimes, serverless), the microservices/monolith sentiment (this has moved meaningfully between 2014, 2020, and 2026), event-driven tooling (Kafka ecosystem, competitors like Redpanda and Warpstream), and fitness-function tooling (ArchUnit successors, CI-runnable conformance frameworks).

**Passes when:** skill version and dates are printed, and a staleness warning surfaces if >6 months old.

## Completion tiers

Three tiers. Each independently shippable; each declarable at a boundary; each audit-able.

### Tier 1: Sketch (mandatory; unblocks downstream skills)

The architecture has enough shape to let stack-ready start picking tools, roadmap-ready start sequencing, and production-ready start Step 2.

| # | Requirement |
|---|---|
| 1 | **Mode declared.** A through F, with the Step 0 research block. |
| 2 | **Load-bearing check run.** If architecture is not load-bearing, a minimal one-page ARCH.md is written and the skill stops. |
| 3 | **Pre-flight answered.** All 8 questions from Step 1 in writing, or explicit assumptions flagged as open questions. |
| 4 | **System shape chosen.** ADR-001 with all eight required fields. |
| 5 | **Component breakdown drafted.** Each component with all six fields (bounded context, responsibility, interface, data ownership, dependencies, failure posture). |
| 6 | **Data architecture drafted.** Entities, tenancy, lifecycle, storage shape per entity group. ADR-002. |
| 7 | **Trust boundaries named.** All four boundaries (edge, authN, authZ, tenant isolation) with all four attributes each. ADR-003. |
| 8 | **C4 Level 1 Context diagram exists.** Text format (Mermaid / PlantUML / Structurizr DSL / D2). |
| 9 | **Handoff block written.** `.architecture-ready/HANDOFF.md` with all three sub-sections filled or explicitly deferred. |

**Proof test:** a stack-ready session started from this ARCH.md can run its pre-flight and constraint map without asking the user another question. A production-ready session can copy Step 7 verbatim into its Step 2 threat model.

### Tier 2: Contract (recommended for real builds)

The architecture is signed off by the right stakeholders, diagrams are complete, and the integration and NFR chains are fleshed out.

| # | Requirement |
|---|---|
| 10 | **Integration architecture written.** Step 5: every integration has sync/async, transport, idempotency, failure mode. |
| 11 | **NFR chains computed.** Step 6: latency, availability, throughput chains each compute to the PRD's targets. Infeasible chains are called out, and either the shape or the target is adjusted. |
| 12 | **ADRs complete.** Every non-obvious architectural decision has an ADR with all eight fields. At minimum ADR-001, ADR-002, ADR-003 plus one ADR per load-bearing integration. |
| 13 | **C4 Level 2 Container diagram complete.** Every arrow labeled with protocol and purpose. |
| 14 | **C4 Level 3 Component diagrams.** At least one, covering the most architecturally-weighty bounded context. |
| 15 | **Fitness functions named.** At least three, with enforcement points identified. |
| 16 | **Tier 2 sign-off attested.** Tech lead, senior engineer, principal/staff/architect, PM. |
| 17 | **Prior art section.** Three comparable systems or deployments with public evidence (postmortems, engineering blog posts, conference talks) that informed the architecture. Borrowed from stack-ready and the Rust RFC process. |

**Proof test:** a new engineer reads ARCH.md six months later and can start a feature on day one without ambiguity about where it goes, what it owns, or what it integrates with. A security reviewer can extract the threat model inputs without interpreting prose.

### Tier 3: Living (architecture stays alive)

Fitness functions are running, conformance is tested in CI, drift is visible. The architecture does not just describe the intent; it enforces it.

| # | Requirement |
|---|---|
| 18 | **At least one fitness function wired.** Dependency conformance, data ownership, or NFR SLO probe running in CI or runtime. |
| 19 | **ADR supersession protocol in effect.** Any decision reversed since Tier 2 is a new ADR with `Superseded by ADR-MMM` pointing at it. |
| 20 | **Change-control protocol in effect.** ARCH.md is Living-with-conformance; changelog is maintained; broadcast record shows changes are announced. |
| 21 | **Tier 3 sign-off attested.** Tier 2 signers plus security/compliance lead (for regulated domains) plus SRE/platform lead. |
| 22 | **Post-build audit scheduled.** 30, 60, or 90 days post-initial-build, a review confirming the architecture-as-built matches the architecture-as-documented. Drift is reconciled with either a doc update or an ADR. |
| 23 | **No have-not remains.** Every item in the disqualifier list below passes. |

**Proof test:** a fresh agent session or a new engineer, reading ARCH.md cold, can answer (a) what the system shape is and why, (b) what invariants must hold, (c) where the trust boundaries sit, (d) what the failure modes are, (e) what fitness functions guard against drift, and (f) which decisions are open and who owns them. If any answer requires opening the code or asking the user, Tier 3 is not complete.

## The "have-nots": things that disqualify the architecture at any tier

If any of these appear, the architecture fails its contract and must be fixed:

- **Architecture theater.** A box, arrow, ADR, or diagram with no flip-point answer. "What would make us reverse this decision? Nothing in particular." That is decoration; delete or rewrite.
- **Paper-tiger architecture.** A shape that looks robust but has not been stress-tested on paper. The latency chain, throughput chain, and availability chain have not been computed. "Scalable" is claimed; the number is not cited.
- **Cargo-cult cloud-native.** Kubernetes, service mesh, Kafka, event sourcing, CQRS, or API gateway adopted with no PRD-grounded justification tied to a specific non-functional constraint. "Because it scales" without a number is cargo-cult.
- **Stackitecture.** The architecture section is a stack list. Next.js plus Postgres plus Prisma plus Clerk, with no system-shape decision above it. This is stack-ready's output, not architecture-ready's. Rewrite or delegate.
- **Resume-driven architecture.** A shape chosen because it is interesting to the writer, not because it serves the PRD. Symptom: the flip point would require the PRD to change in ways the PRD does not mention.
- **Non-architecture.** "We'll figure it out later" dressed up as agility. Zero ADRs; zero constraints; zero failure-mode analysis. An architecture document that is a hopes list is not architecture.
- **Invisible architecture.** A document that reads the same across any system in the same domain. The substitution test: replace "orders" with "tickets" or "invoices" or "bookings." If the architecture still reads plausibly, it is invisible and has not decided anything specific.
- **Horoscope architecture.** An ARCH.md whose prose reads plausibly for any product category. "The system uses a scalable backend with a well-designed data layer and a modern frontend" is horoscope prose. Rewrite with the PRD's actual entities, numbers, and constraints, or cut.
- **Ghost architecture.** The ARCH.md describes one system; the running system is a different one. This happens when ARCH.md is not maintained post-build and no fitness function catches the drift. At Tier 3, a post-build audit is mandatory precisely to refuse ghost architecture.
- **Distributed monolith.** Multiple services writing to the same table, or multiple services sharing a database schema for writes, or synchronous call chains across services for every user request. This is the worst of both worlds: the operational cost of microservices without the independence benefit.
- **Anemic services.** A service that is a thin wrapper over a single database table. Usually "UserService," "AuthService," "NotificationService." These are CRUD endpoints, not services. Consolidate into the bounded context that owns the entity.
- **God services.** A service whose responsibility sentence covers half the domain. "Handles users, auth, billing, orders, and notifications." Split by bounded context.
- **Microservices without a forcing function.** A microservices decomposition for a team of fewer than 20 engineers with no regulatory or independent-scaling justification. The complexity floor is higher than the complexity being avoided.
- **Event sourcing or CQRS without a justified use case.** Adopting either because "it is a best practice" or "it enables audit." Audit is solved by audit logs, not event sourcing. CQRS is justified when read and write patterns genuinely differ; most systems do not need it.
- **Silent NFR numbers.** "Scalable," "performant," "reliable," "observable," "cloud-native" as claims without numbers. Every instance is a defect.
- **Silent trust boundaries.** A multi-tenant architecture with no named tenant-isolation boundary. A payment-processing system with no named authorization boundary. A public API with no named edge or authentication boundary. Silence is not an answer.
- **Data architecture that jumps to database names.** "Use Postgres" or "use MongoDB" without first naming a storage shape. Shape precedes pick; stack-ready picks.
- **Diagrams without labeled arrows.** "Uses," "calls," "talks to" as arrow labels. Replace with protocol, purpose, and semantics.
- **Diagrams with cloud-vendor icons as architecture.** AWS boxes and GCP hexagons diagram deployment, not architecture. Move to deploy-ready.
- **ADRs retroactively rationalized.** Writing an ADR that claims the decision was made for reason X when the decision was actually made for reason Y (or for no reason at all). Retroactive ADRs are acceptable only if labeled as such.
- **ADRs without flip points or blast-radius fields.** Missing fields from the required template.
- **Architecture document longer than three pages of prose plus ADRs.** Long-form prose is a symptom of theater. Decisions are short; narrative is long. Move narrative to references; keep ARCH.md to decisions.
- **Unowned open questions.** Every open question must have an owner and a due date. Every unknown is somebody's to answer.
- **Unsigned tier.** A tier declared complete without the tier's required signers attested in writing.
- **Fitness functions named but not wired at Tier 3.** If no fitness function is actually running in CI or runtime, Tier 3 fails. Names without mechanisms are theater.
- **Banned phrases.** "Industry-leading," "enterprise-grade" (without definition), "seamlessly," "cloud-native" (as adjective claim), "cutting-edge," "future-proof," "best-in-class," "game-changing," "revolutionary," "AI-powered" (for non-AI components), "scalable" (as bare claim), "resilient" (as bare claim). These are marketing phrases; replace with the concrete claim the adjective was covering for, or cut.
- **Architecture written from a single-sentence prompt.** If the user input was "design the architecture for my app" and the skill produced a full ARCH.md without at least a Mode declaration, the load-bearing check, and the pre-flight, it is architecture slop. Refuse.
- **Architecture without a PRD.** If `.prd-ready/PRD.md` is absent and the user has not provided PRD-equivalent inputs, refuse to produce a detailed ARCH.md. Warn explicitly: "architecture without a PRD is guessing. Either produce one (invoke prd-ready) or state the entities, NFRs, and appetite inline as assumptions."

When you catch yourself about to write any of these, fix it before proceeding. An architecture document that ships with any of these misroutes stack-ready, roadmap-ready, and production-ready all at once; the cost compounds.

## Reference files: load on demand

The body above is enough to start. Load each reference *before* the step that uses it, not after.

| Reference file | When to load | ~Tokens |
|---|---|---|
| `architecture-research.md` | **Always.** Start of every session (Step 0). | ~5K |
| `system-shape.md` | **Always.** Step 1 load-bearing check; Step 2 shape decision. | ~10K |
| `component-breakdown.md` | **Tier 1.** Step 3 component breakdown. | ~8K |
| `data-architecture.md` | **Tier 1.** Step 4 entities, tenancy, storage shape. | ~10K |
| `integration-architecture.md` | **Tier 2.** Step 5 integration patterns, idempotency. | ~9K |
| `non-functional-architecture.md` | **Tier 2.** Step 6 NFR numbers and chains. | ~8K |
| `trust-boundaries.md` | **Tier 1.** Step 7 trust-boundary map. | ~7K |
| `adr-discipline.md` | **Tier 1 and beyond.** Step 8 ADRs. | ~6K |
| `diagrams.md` | **Tier 1 (context) and Tier 2 (container, component).** Step 9. | ~8K |
| `evolutionary-architecture.md` | **Tier 3.** Step 10 fitness functions. | ~7K |
| `architecture-antipatterns.md` | **On demand.** Mode C audits and tier-gate checks. | ~10K |
| `RESEARCH-2026-04.md` | **On demand.** When the user asks "why this rule"; source citations for the initial release. | ~35K |
| `EXAMPLE-ARCH.md` | **On demand.** A complete worked example architecture for a fictional B2B SaaS product (Pulse, a Customer Success ops platform). Demonstrates C4 context + container diagrams in ASCII, component breakdown, multi-tenant data architecture, named trust boundaries each carrying a code path, NFR-to-mechanism mapping, three ADRs with named alternatives. Passes the skill's grep tests for architecture-theater / paper-tiger / cargo-cult / stackitecture / scalable-without-numbers failure modes. Consumes the worked PRD; feeds the worked roadmap and stack-decision examples in their respective sibling repos. | ~17K |

Skill version and change history live in `CHANGELOG.md`. When resuming an architecture across sessions, confirm the skill version matches the version recorded in the ARCH.md's front matter if one exists. A skill update between sessions can shift have-nots (the banned-phrase list evolves as AI outputs shift), add sections (downstream-skill interfaces tighten), or change tier gates.

## Session state and handoff

Architectures span sessions; maintain `.architecture-ready/STATE.md` when the work is ongoing.

**Template:**

```markdown
# Architecture-Ready State

## Skill version
architecture-ready [current skill version], [frontmatter updated date].

## Current tier
Working toward Tier [N]. Last completed tier: [N-1].

## Mode
A / B / C / D / E / F.

## Load-bearing check
[Result: load-bearing / not load-bearing. Criteria that applied.]

## Pre-flight answers
(copied from Step 1)

## Active sections
- System shape: [status, ADR-001]
- Component breakdown: [status]
- Data architecture: [status, ADR-002]
- Integration: [status]
- Non-functional: [status]
- Trust boundaries: [status, ADR-003]
- Diagrams: [status, C4 levels present]
- Fitness functions: [status]
- Handoff block: [status]

## ADR ledger
- ADR-001-system-shape.md [status: Accepted | Superseded by ADR-NNN]
- ADR-002-storage-shape.md [status]
- [etc.]

## Sign-off ledger
- Tech lead: [name, date, attestation]
- Senior engineer: [name, date, attestation]
- [etc.]

## Open questions blocking next tier
- [Q]: [owner], [due date]

## Last session note
[ISO date] [what happened, what's next]
```

**Rules:**

- STATE.md is the contract with the next session. Update at every tier boundary and every context compaction.
- Never delete STATE.md.
- If `ARCH.md` and `HANDOFF.md` exist at Tier 3, STATE.md can be collapsed into the ARCH.md changelog; the ARCH.md becomes the source of truth.

## Suite membership

This skill is part of the **ready-suite**. See [`SUITE.md`](SUITE.md) for the full map.

- **Planning tier:** `prd-ready` (what), `architecture-ready` (how, this skill), `roadmap-ready` (when), `stack-ready` (with what tools).
- **Building tier:** `production-ready` (the app), `repo-ready` (the repo scaffolding).
- **Shipping tier:** `deploy-ready` (ship it), `observe-ready` (keep it healthy), `launch-ready` (tell the world), `harden-ready` (survive adversarial attention).

architecture-ready sits in the planning tier, between prd-ready upstream and three downstream consumers. The harness is the router; this skill tells the user which sibling to invoke next and why.

## Consumes from upstream

When the agent starts, it checks for upstream artifacts and pre-fills the pre-flight rather than asking the user to repeat decisions already made. Absence is handled with a warning: architecture without a PRD is guessing.

| If present | This skill reads it during | To pre-fill |
|---|---|---|
| `.prd-ready/PRD.md` | Step 0 mode detection and Step 1 pre-flight | Entities, flows, NFRs (latency, throughput, availability, scale), integration points, trust boundaries, compliance constraints, appetite, explicitly deferred items |
| `.prd-ready/HANDOFF.md` Architecture-ready subsection | Step 1 pre-flight | Pre-filled answers to all 8 pre-flight questions |

If the PRD is absent, the skill warns the user and offers two paths: (1) invoke prd-ready to produce one, or (2) proceed with explicit PRD-equivalent inputs stated inline as assumptions. Do not proceed silently.

## Produces for downstream

Three downstream siblings consume this skill's output. Writing these is part of the skill's definition of done.

| Artifact | Path | Consumed by |
|---|---|---|
| **ARCH.md** (Sketch / Contract / Living) | `.architecture-ready/ARCH.md` | stack-ready (storage shapes, compute shapes, constraints), roadmap-ready (component dependency graph, load-bearing ordering), production-ready (system shape, boundaries, trust boundaries, NFR targets) |
| **Downstream handoff block** | `.architecture-ready/HANDOFF.md` | Each downstream skill reads its sub-section directly |
| **ADRs** | `.architecture-ready/adr/NNN-slug.md` | production-ready extends the same corpus; future maintainers read them for decision archaeology |
| **Diagrams** | `.architecture-ready/diagrams/` (Mermaid, Structurizr DSL, or equivalent) | Everyone; the diagrams are the architecture's public face |
| **Session state** | `.architecture-ready/STATE.md` | Next architecture-ready session resumes here |

## Handoff: tools, sequencing, and implementation are not this skill's jobs

architecture-ready stops at "this is the shape of the system we will build, here is what decides each boundary, here is what must hold, here are the ADRs." What comes next:

- To **`stack-ready`** (live, v1.1.5): the ARCH.md's storage shapes, compute shapes, NFR numbers, and compliance constraints are read from `.architecture-ready/HANDOFF.md` and become pre-filled inputs to stack-ready's Step 1 pre-flight and Step 2 constraint map. stack-ready picks Postgres vs. MySQL vs. Convex; architecture-ready says "relational store with strong consistency" and stops.
- To **`roadmap-ready`** (not yet released): the component dependency graph and load-bearing ordering from HANDOFF.md become the sequencing inputs. architecture-ready does not produce a calendar; roadmap-ready does.
- To **`production-ready`** (live, v2.5.6): the system shape, component boundaries, trust boundaries, data model shape, integration shapes, and NFR targets are read from HANDOFF.md and become the Step 2 architecture-note inputs wholesale. production-ready's threat model in Step 2 adopts the trust boundaries from Step 7; production-ready does not redo the boundary analysis.

**If your harness exposes a skill-invocation tool** (e.g., Claude Code's Skill tool), invoke the next sibling directly when the handoff trigger fires. **Otherwise**, surface the handoff to the user: "This step needs `stack-ready`. Install it or handle the sibling layer separately." Do not attempt to generate the sibling's output inline from architecture-ready.

## Keep going until every element is a decision with a flip point

The system shape is roughly 20% of the work. The component breakdown, data architecture, and integration architecture are another 40%. The non-functional chains, trust boundaries, ADRs, diagrams, fitness functions, and handoff block are the remaining 40%. A user who walks away with "we think we'll use a modular monolith with Postgres" but no ADRs, no trust boundary map, no NFR chains, and no fitness functions does not have an architecture; they have a sketch on a napkin that will be re-litigated at every sibling skill and re-invented when the first feature ships.

When in doubt, ask whether a new engineer on the team could read the document in six months, place a new feature correctly, name the invariants the feature must respect, and identify the failure mode they need to test against. The first question they would have to ask a teammate is the next thing to write down.
