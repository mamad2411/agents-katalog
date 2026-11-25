---
name: team-topology-design
version: 1.0.0
min_mindforge_version: 10.1.0
status: stable
triggers: team topology, stream-aligned team, platform team, enabling team, complicated-subsystem team, cognitive load, team interaction mode, team API, team boundary, Conway law, team coupling, team autonomy
---

# Team Topology Design

## When this skill activates

This skill activates when designing, reorganizing, or evaluating team structures
and their interactions. It applies the Team Topologies framework to align team
boundaries with software architecture, manage cognitive load, and define clear
interaction modes between teams.

## Mandatory actions when this skill is active

### Before

1. **Map current state** — Document existing team structures, their responsibilities,
   communication patterns, and pain points.
2. **Identify architecture goals** — What system architecture do you want? Conway's Law
   means team structure will produce matching architecture.
3. **Assess cognitive load** — Survey teams on whether their responsibilities feel
   manageable or overwhelming. Overload is the primary signal for restructuring.

### During

4. **Apply the four fundamental team types:**

   - **Stream-aligned team** — The primary type. Aligned to a single flow of business
     value (feature, product, user journey, or persona). Delivers end-to-end without
     hand-offs. Has full ownership from ideation through production operation.
     Most teams should be this type.

   - **Platform team** — Provides self-service capabilities that stream-aligned teams
     consume via well-defined APIs. Reduces cognitive load by abstracting away
     infrastructure complexity. Treats internal teams as customers. Measures success
     by adoption and developer satisfaction, not features shipped.

   - **Enabling team** — Helps stream-aligned teams adopt new technologies or practices.
     Temporary collaboration, not permanent dependency. Measures success by the
     stream-aligned team's growing independence. Detects capability gaps across teams
     and bridges them through coaching, documentation, and pairing.

   - **Complicated-subsystem team** — Owns a component requiring deep specialist
     knowledge (ML model, video codec, financial calculation engine). Provides a
     simplified interface to stream-aligned teams. Only justified when the specialist
     knowledge truly cannot be distributed across stream-aligned teams.

5. **Define interaction modes (how teams work together):**

   - **Collaboration** — Two teams working closely together for a defined period.
     High bandwidth, high cost. Time-box to weeks/months, not permanent.
     Use when: discovering new interfaces, bootstrapping new capabilities.

   - **X-as-a-Service** — One team provides capability via API/platform that another
     team consumes. Low coupling, clear contract. The provider defines the interface.
     Use when: the boundary is well-understood and stable.

   - **Facilitating** — One team coaches another. No code ownership transfer, no
     permanent dependency. The facilitating team's goal is to make themselves
     unnecessary. Use when: enabling teams help stream-aligned teams grow.

6. **Manage cognitive load:**
   - A team should own no more domains than fit in collective working memory.
   - Signs of overload: constant context switching, shallow knowledge across many areas,
     slow delivery, high bug rates, burnout.
   - Response to overload: split the team, transfer ownership to a platform team, or
     reduce scope.
   - Intrinsic load (problem complexity) cannot be reduced — manage it with specialists.
   - Extraneous load (poor tooling, unclear ownership) — eliminate it aggressively.

7. **Apply Conway's Law intentionally:**
   - Do not fight Conway's Law. Design teams to match desired architecture.
   - If you want microservices, create teams with clear service boundaries.
   - If you want a cohesive platform, create a platform team.
   - Team boundaries become API boundaries. Choose them deliberately.

8. **Define team APIs:**
   - Every team should have a clear "team API" — how others interact with them.
   - Includes: code/service interfaces, documentation, on-call escalation paths,
     request intake process, SLA commitments.
   - Make team APIs explicit and discoverable.

### After

9. **Validate with evolution paths** — Team structures must evolve. Define how teams
   will split, merge, or change interaction modes as the system grows.
10. **Communicate the design** — Share team topology decisions with the full org.
    Explain the WHY, not just the WHAT.
11. **Set review cadence** — Reassess team topology quarterly. Look for: growing cognitive
    load, increasing inter-team dependencies, delivery bottlenecks.

## Self-check before task completion

- [ ] Every team classified as exactly one of the four types
- [ ] Stream-aligned teams can deliver end-to-end without blocking dependencies
- [ ] Platform teams have clear self-service interfaces (not ticket queues)
- [ ] Interaction modes explicitly defined for each team pair that collaborates
- [ ] Cognitive load assessed and within manageable bounds per team
- [ ] Conway's Law applied intentionally (team structure matches desired architecture)
- [ ] Team APIs documented and discoverable
- [ ] Evolution paths defined for growth scenarios
- [ ] Review cadence established
