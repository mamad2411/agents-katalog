---
name: fabrico-building-lean-applications
description: "Builds cost-efficient, high-quality applications using a modular-monolith default, explicit service and dependency budgets, reusable golden paths, risk-based tests, and evidence-based scaling triggers. Use for every new application, material feature, architecture plan, deployment design, build-versus-buy decision, or cost and complexity review; prevents speculative microservices, Kubernetes, paid services, and premature infrastructure."
---

# Building Lean Applications

Choose the least expensive architecture that satisfies the product's current quality, security, recovery, and growth requirements. Optimize total cost of ownership, not only the hosting invoice.

<economic-default>

Start with a modular monolith, one repository, one deployable application image, one relational database, and the fewest operational dependencies allowed by the required stack. Keep business modules explicit so they can be tested or extracted later without paying distributed-system costs now.

Do not reduce cost by removing authorization, tenant isolation, validation, backups, restore tests, accessibility, or critical-path tests. Reduce waste, duplication, idle infrastructure, unnecessary dependencies, and speculative generality.

</economic-default>

## Lean Delivery Process

Track this checklist:

```text
Progress:
- [ ] Define the cost and quality profile
- [ ] Choose the lowest viable architecture tier
- [ ] Apply service and dependency admission gates
- [ ] Deliver thin vertical slices using reusable foundations
- [ ] Run a risk-based quality gate
- [ ] Measure production behavior and record escalation triggers
```

### 1. Define the cost and quality profile

Add a compact `Cost and Quality Profile` to the existing PRD or implementation plan. Record:

- product stage: `prototype`, `mvp`, `growth`, or `regulated`;
- critical user journeys and the cost of failure;
- expected users, request volume, data volume, and background workload;
- data classification, tenant-isolation model, and compliance constraints;
- availability target, tolerated data-loss window, and recovery-time target;
- monthly infrastructure ceiling and maximum cost per paid operation when known;
- team size, operational capacity, and explicitly approved paid services.

Do not invent numerical business targets. Mark unknowns and select the lowest reversible tier that is safe under the known constraints. Read `references/cost-quality-ladder.md` when choosing infrastructure, tenancy, testing, AI, search, or build-versus-buy tiers.

### 2. Choose the lowest viable architecture tier

- Default to a modular monolith organized by business capability, not technical-layer sprawl.
- Keep one source tree and one build artifact. Run web, worker, and scheduler as separate process roles from the same application image when required.
- Use a direct server-rendered or Inertia path for the product UI. Add a separate public API only for an actual mobile, partner, external automation, or independently deployed client requirement.
- Reuse the database, cache, queue, scheduler, mail, authorization, validation, rate limiting, and storage abstractions already supplied by the required framework.
- Start in one region. Use the simplest production topology that meets the declared recovery and availability targets; a single-host Docker deployment is valid only when its failure and recovery profile are explicitly acceptable and restore-tested.
- Keep module calls in process. Add a network boundary only when independent deployment, scaling, ownership, security, or failure isolation has measured value.

Do not add Kubernetes, microservices, a second database engine, a message broker beyond the required queue, a search cluster, a vector database, a data warehouse, a paid feature-flag service, or multi-region infrastructure without an escalation record.

### 3. Apply admission gates

Before adding a dependency or paid service, verify all of the following:

1. An acceptance criterion or measured bottleneck requires its capability.
2. The existing stack cannot meet the requirement at lower total cost.
3. The package or service has a compatible license, supported versions, acceptable security posture, and an exit path.
4. Ownership, failure behavior, observability, data handling, and recurring cost are understood.
5. The saved delivery and operational effort is greater than integration, migration, and lock-in cost.

Prefer framework primitives and small libraries over overlapping platforms. Pin direct dependencies and avoid packages that duplicate existing Laravel, Vue, shadcn-vue, MySQL, or Redis capabilities.

Verify current official documentation and pricing before committing to a versioned or paid dependency. Do not repeat stale prices inside code or architecture policy.

### 4. Reuse without building an internal framework

- Start from the official framework starter and retain its CI, authentication, and supported conventions.
- Maintain one versioned golden-path template for infrastructure, CI, authentication, tenant context, error handling, and test setup.
- Distribute stable shadcn-vue compositions through a private registry. Keep domain-specific columns, fields, policies, and workflows in the application.
- Extract a shared abstraction after the same shape is proven across real applications. Do not generalize a one-off requirement.
- Automate deterministic repetition with generators or skill scripts. Keep judgment, naming, and domain mapping in the model or application team.
- Make generated output ordinary owned code. Avoid a runtime meta-framework for standard CRUD screens.

Deliver one thin vertical slice at a time: migration, model, policy, validation, application operation, UI, and focused tests. Finish a slice before opening another cross-cutting subsystem.

### 5. Spend the quality budget where failure is expensive

Always run formatting, static analysis, type checking, focused automated tests, and production builds for changed surfaces. Match additional tests to risk:

| Change | Minimum high-value verification |
|---|---|
| Pure calculation or invariant | Fast unit tests, including boundaries |
| CRUD or HTTP workflow | Laravel feature tests for success, validation, and authorization |
| Tenant-owned data | Negative cross-tenant read and write tests |
| Transaction, queue, webhook, or retry | Integration tests for rollback, idempotency, and failure behavior |
| Complex Vue state | Focused component test |
| Critical user journey | One narrow Playwright golden-path test |
| Paid AI capability | Mocked default tests plus a small versioned evaluation set |

Prefer the cheapest test layer that catches the likely failure. Do not chase a universal coverage percentage, duplicate the same assertion at every layer, or make CI depend on paid APIs. Run MySQL and Redis integration tests where their real behavior matters.

### 6. Measure before escalating

Measure business outcomes and the constraints that drive architecture: successful-task cost, p95 latency, error rate, query count and duration, payload size, queue lag, memory, storage growth, tenant consumption, restore time, and developer lead time.

Require every escalation to state:

- the measured threshold and observation window;
- evidence that the current tier fails a requirement;
- the smallest next tier and expected improvement;
- new recurring and operational cost;
- rollback or exit path;
- owner and review date.

Remove unused services and abstractions when the evidence disappears. Architecture is allowed to become simpler.

## Verification Gate

```text
Validation:
- [ ] Cost and Quality Profile exists and contains no invented targets
- [ ] Architecture is a modular monolith unless an escalation record justifies otherwise
- [ ] Every paid service and non-trivial dependency passed the admission gate
- [ ] The solution reuses the golden path without introducing a generic internal framework
- [ ] Critical security, tenancy, backup, recovery, and accessibility controls remain intact
- [ ] Tests are concentrated on business risk and do not require paid APIs by default
- [ ] Production metrics can prove or reject each documented scaling trigger
- [ ] Total cost includes development, operations, infrastructure, usage, and exit cost
```

## Connected Skills

- `fabrico-architecture-designing` - for module boundaries and evidence-based evolution
- `fabrico-building-admin-dashboards` - for the required Laravel admin foundation
- `fabrico-building-admin-resources` - for cheap, repeatable CRUD forms and tables
- `fabrico-preparing-applications-for-ai` - for AI quality and cost per successful task
- `fabrico-preparing-applications-for-saas` - for pooled tenancy and tenant-aware cost controls
- `fabrico-implementing-ci-cd` - for fast, proportional delivery gates
- `fabrico-optimizing-cloud-cost` - for provider-specific infrastructure cost analysis
