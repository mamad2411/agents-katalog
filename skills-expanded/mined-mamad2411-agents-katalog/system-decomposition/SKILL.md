---
name: system-decomposition
description: Decompose a system into bounded contexts and services using DDD strategic patterns and Team Topologies. Use when designing a new platform, splitting a monolith, or realigning services to teams and business capabilities.
---

# System Decomposition

Decomposition is where most architecture wins or loses. The goal is service and team boundaries that match how the business actually changes - cohesive inside, loosely coupled outside, owned end-to-end.

## Stack Baseline (2026)

| Concern | Recommended |
| --- | --- |
| Discovery | EventStorming, Domain Storytelling, Wardley Mapping, Core Domain Charts |
| Strategic DDD | Bounded contexts, context maps, Published Language, Anti-Corruption Layer |
| Org model | Team Topologies (stream-aligned, platform, enabling, complicated subsystem) |
| Modular runtime | Spring Modulith, .NET Aspire, NestJS modules, Bazel / Nx workspaces |
| Integration | OpenAPI 3.1, AsyncAPI 3.0, gRPC, Kafka 3.7 / EventBridge, MCP for AI tools |
| Fitness functions | ArchUnit, ts-arch, NetArchTest, dependency-cruiser; enforced in CI |
| Quality model | ISO/IEC 25010:2023; AWS / Azure / GCP Well-Architected pillars |

## When to Use
- Designing a new platform or product line above a single service.
- Breaking up a monolith where teams contend on the same code or DB.
- Realigning service boundaries after a reorg, M&A, or major strategy shift.
- Resolving recurring cross-team coordination tax.

## Prerequisites
- Access to domain experts and product leaders for discovery sessions.
- Current architecture diagrams, dependency graph, and Git history (>=12 months).
- Org chart with team sizes, missions, and cognitive-load assessment.
- Strategic context: Wardley map or roadmap of what is Core vs Generic.

## Instructions

1. **Map business capabilities, not tech**: Build a capability map (Sales, Pricing, Fulfillment, Identity, Billing). This is the candidate space for contexts; tech components like "UserService" are not capabilities.

2. **Run EventStorming on top capabilities**: Surface domain events, commands, actors, policies, and aggregates. Cluster events into candidate bounded contexts; capture the ubiquitous language verbatim per cluster.

3. **Draw the context map**: Name each bounded context, classify as Core / Supporting / Generic, and label relationships (Customer-Supplier, Conformist, ACL, Open Host Service, Published Language, Shared Kernel, Separate Ways). Invest engineering depth in Core; buy or adopt Generic.

   ```mermaid
   flowchart LR
     subgraph Core
       PR[Pricing] --- PROMO[Promotions]
     end
     subgraph Supporting
       OR[Ordering] -->|Customer/Supplier| PR
       INV[Inventory] -->|Published Language (events)| OR
     end
     subgraph Generic
       ID[Identity] -. ACL .- OR
       BILL[Billing]
     end
   ```

4. **Score each candidate context**: Rate cohesion, coupling, change rate, scaling needs, data ownership, compliance scope, and team fit (1-5). Promote contexts that score high on multiple axes; merge or defer the rest.

5. **Apply Inverse Conway**: Shape teams to match the desired architecture - stream-aligned teams own contexts end-to-end; a thin platform team owns shared runtime; enabling teams move capability between streams. Check team cognitive load before adding contexts.

6. **Choose the runtime form per context**: Modular monolith (Spring Modulith / .NET Aspire) when team count is low; service per context when independent deploy and scale are required; serverless functions for spiky, event-shaped workloads.

7. **Define integration contracts**: Per relationship, specify sync API (OpenAPI 3.1 / gRPC) or async events (AsyncAPI 3.0 on Kafka / EventBridge). Add ACLs at the boundary of any legacy or third-party model.

8. **Encode boundaries as fitness functions**: Architecture tests forbid one context from importing another's internals; CI rejects schema-incompatible event changes; dashboards track cross-context call rates and SLOs.

## Common Pitfalls

| Pitfall | Why it bites | Mitigation |
| --- | --- | --- |
| Decomposing by tech layer | "UserService", "DBService" - no business meaning, high coupling | Decompose by capability and bounded context |
| Distributed monolith | Many services, one shared DB and release train | Move data ownership with the service; independent CI/CD |
| Boundaries ignore team topology | Constant cross-team coordination tax | Apply Inverse Conway; one team owns each Core context |
| Too-fine contexts too early | Sprawl, high ops burden | Modular monolith first; split when pain is measured |
| No ACL against legacy | Legacy schema poisons new model | ACL at every boundary with a different model |
| Boundaries drift | Coupling re-emerges within months | Architecture tests + dependency dashboards in CI |

## Output Format

Deliver a decomposition pack: capability map, EventStorming artifacts, context map with relationship types, subdomain classification, per-context scorecard, target team topology, runtime choice per context, integration contracts (OpenAPI / AsyncAPI), and fitness functions to add. Include a phased migration plan with reversibility notes.

## Authoritative References

- [Domain-Driven Design Reference (Eric Evans)](https://www.domainlanguage.com/ddd/reference/)
- [Martin Fowler - BoundedContext](https://martinfowler.com/bliki/BoundedContext.html)
- [microservices.io - Decomposition patterns](https://microservices.io/patterns/decomposition/index.html)
- [Team Topologies](https://teamtopologies.com/)
- [Wardley Mapping](https://learnwardleymapping.com/)
- [ThoughtWorks Technology Radar](https://www.thoughtworks.com/radar)
- [ISO/IEC 25010:2023](https://www.iso.org/standard/78176.html)