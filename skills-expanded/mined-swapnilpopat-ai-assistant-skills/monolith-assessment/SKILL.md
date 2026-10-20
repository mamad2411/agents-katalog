---
name: monolith-assessment
description: Assess a monolith for fitness, modularization, and extraction candidates before any service split. Use when team velocity, scaling, or compliance pressure raises the question of breaking up a monolith.
---

# Monolith Assessment

Produce an evidence-based recommendation - keep, modularize, strangle, or rewrite - grounded in metrics, team topology, and architectural fitness functions, not fashion.

## Stack Baseline (2026)

| Concern | Recommended |
| --- | --- |
| Codebase analysis | CodeScene, NDepend, jQAssistant, Structure101, ArchUnit / ts-arch fitness tests |
| Coupling / change metrics | Git temporal coupling, hotspot analysis (CodeScene), LCOM4, SonarQube 10 |
| Runtime profiling | OpenTelemetry 1.x, Pyroscope, async-profiler, eBPF (Parca) |
| DDD discovery | EventStorming, Domain Storytelling, Context Mapper |
| Migration patterns | Strangler Fig, Branch by Abstraction, Parallel Run, Expand-Contract |
| Team topology | Team Topologies (stream-aligned, platform, enabling, complicated subsystem) |
| Quality model | ISO/IEC 25010:2023 (maintainability, performance efficiency, reliability) |

## When to Use
- Deploy frequency, lead time, or change-failure rate (DORA) is degrading.
- Multiple teams contend on the same codebase or database.
- A specific subdomain has different scaling, compliance, or release cadence needs.
- Leadership is debating a microservices migration and needs an objective baseline.

## Prerequisites
- Read access to repo history (>= 12 months), CI/CD metrics, and incident records.
- Production telemetry: latency, throughput, error rate, resource usage by endpoint.
- Org chart and team-to-codepath ownership.
- Business roadmap and known regulatory drivers (PCI, HIPAA, GDPR, data residency).

## Instructions

1. **Establish baseline metrics**: Capture DORA (deploy frequency, lead time, MTTR, change-failure rate), build time, test runtime, mean PR review time, and incident frequency by module. These become the success criteria for any change.

2. **Run a structural scan**: Compute package coupling, cyclomatic complexity, and temporal coupling from Git. Identify hotspots (high churn + high complexity) and god classes/modules.

   ```mermaid
   quadrantChart
     title Hotspot Map
     x-axis Low Churn --> High Churn
     y-axis Low Complexity --> High Complexity
     quadrant-1 Refactor first
     quadrant-2 Watch
     quadrant-3 Healthy
     quadrant-4 Stable but risky
     Checkout: [0.85, 0.82]
     Pricing: [0.7, 0.4]
     Auth: [0.3, 0.6]
     Reporting: [0.2, 0.2]
   ```

3. **Map domains via EventStorming**: With domain experts, surface bounded contexts and aggregates. Overlay them on the code structure to find misaligned modules and shared-kernel risks.

4. **Apply fitness functions**: Encode architectural rules (e.g. "billing must not import shipping") as automated tests so the assessment becomes continuous.

   ```java
   // ArchUnit
   @ArchTest
   static final ArchRule billing_independent_of_shipping =
       noClasses().that().resideInAPackage("..billing..")
           .should().dependOnClassesThat().resideInAPackage("..shipping..");
   ```

5. **Score each candidate module**: Rate on a 1-5 scale across business criticality, change rate, scaling needs, team independence, data isolation, and compliance scope. Promote only modules scoring high on multiple axes.

6. **Choose an evolution path per module**:
   - Modular monolith (Spring Modulith, .NET Aspire, NestJS modules) when team count is low.
   - Strangler Fig with Branch by Abstraction for risky extractions.
   - Service extraction only when data ownership and team ownership can both move.

7. **Sequence with risk and ROI**: Order extractions by (DORA improvement * strategic value) / (extraction cost + operational burden). Reassess after each step.

8. **Define success and reversibility**: Set explicit DORA and SLO targets per step. Keep the modular monolith deployable until the new service is proven, so you can roll back.

## Common Pitfalls

| Pitfall | Why it bites | Mitigation |
| --- | --- | --- |
| Splitting before modularizing | Creates a distributed monolith with shared DB | Modular monolith first; extract only proven seams |
| Ignoring data ownership | Two services writing one table = tight coupling | Move data ownership with the service; use outbox + CDC |
| Optimizing tech, not org | Architecture fights Conway's Law and loses | Align extractions to stream-aligned teams |
| No fitness functions | Boundaries erode within months | Enforce package and dependency rules in CI |
| Big-bang rewrite | High cost, high risk, late value | Strangler Fig with parallel run and feature flags |
| Missing baseline metrics | Cannot prove improvement, cannot stop | Capture DORA + SLOs before any change |

## Output Format

Deliver an assessment report with: current-state metrics, hotspot map, bounded-context overlay, per-module scorecard, recommended evolution path (keep / modularize / strangle / rewrite) with rationale, prioritized extraction backlog, fitness functions to add, and exit criteria with reversibility plan.

## Authoritative References

- [Martin Fowler - MonolithFirst](https://martinfowler.com/bliki/MonolithFirst.html)
- [Martin Fowler - StranglerFigApplication](https://martinfowler.com/bliki/StranglerFigApplication.html)
- [microservices.io - Pattern: Monolithic Architecture](https://microservices.io/patterns/monolithic.html)
- [Team Topologies](https://teamtopologies.com/)
- [ThoughtWorks Technology Radar](https://www.thoughtworks.com/radar)
- [DORA / Accelerate State of DevOps](https://dora.dev/)
- [ISO/IEC 25010:2023](https://www.iso.org/standard/78176.html)
