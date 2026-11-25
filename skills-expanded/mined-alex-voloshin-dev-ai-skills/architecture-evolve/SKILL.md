---
name: architecture-evolve
description: Use this skill when migrating between technologies (REST → gRPC, monolith → microservices, on-prem → cloud, framework upgrade), executing a major redesign driven by tech debt or scale, or a strategic platform shift (database engine, message bus, identity provider, observability vendor) — including when the user describes a "from X to Y" move without saying "evolve" or "migration" — to plan and document architecture migration and evolution — an ADR for the migration decision, target-state ARCHITECTURE.md, a phased migration plan (strangler fig, expand-contract, branch by abstraction), fitness functions, and a rollback strategy. Not for new feature design — use `/architecture-design` instead.
context: fork
argument-hint: "<migration initiative — from X to Y>"
---

# /architecture-evolve — Architecture Migration

Plan and document an architecture migration. Produces an ADR explaining the decision, a target-state ARCHITECTURE.md, a phased migration plan, fitness functions to enforce the transition, and a rollback strategy.

## When to use

- Cross-technology migration: REST → gRPC, monolith → microservices, on-prem → cloud, framework upgrade
- Major redesign initiative driven by tech debt or scale
- Strategic platform shift: change of database engine, message bus, identity provider, observability vendor

## Not for

- New feature design → `/architecture-design`
- Documenting existing state without migration intent → `/architecture-analyze`
- Implementation execution (use this skill's output as input to `/plan`)
- Routine library/version upgrades → `/migrate`

## Step 1 — Receive Input and Establish Baseline

Extract: **From → To** (current technology / pattern → target), **Why** (driver: tech debt, scale, cost, compliance, strategic), **Scope** (system-wide, single service, single module), **Constraints** (timeline, compatibility, downtime budget), **Stakeholders**.

Confirm a baseline exists (or run `/architecture-analyze` first). Migration without a documented current state is high-risk — the second-order effects are invisible. If no baseline → refuse and surface: "Run `/architecture-analyze` first to establish baseline."

## Step 2 — Define Target State NFRs

`Agent(solution-architect)`. NFRs for the target state, with delta vs current:

| Category | Current | Target | Delta |
|---|---|---|---|
| Availability | 99.5% | 99.95% | +0.45 % (10× fewer outage minutes) |
| Latency p95 | 800 ms | 200 ms | −75 % |
| Cost / month | $X | $Y | varies |
| Scalability | … | … | … |

Migration only makes sense if the delta justifies the cost. Present target NFRs to the user — if the user accepts a current → target step that NFRs alone do not justify, document the strategic rationale explicitly.

## Step 3 — Migration ADR

`Agent(solution-architect)`. Architecture Decision Record:

- **Status**: Proposed
- **Context**: Why the migration is needed (technical + business drivers)
- **Decision**: From → To, including the migration pattern (strangler fig / expand-contract / branch by abstraction / parallel run)
- **Consequences**: positive (target NFRs achieved, debt resolved), negative (transitional complexity, double-running costs, team learning curve), neutral (process/tooling changes)
- **Alternatives Considered**: keep-as-is, smaller-scope migration, different target tech, deferred timing

## Step 4 — Target-State Architecture

`Agent(system-architect)`. Produce:

- C4 diagrams (Context + Container) of the target state
- Component inventory of the target with responsibilities + tech stack
- Data flow diagrams for critical target-state paths
- Integration points + new contracts (API, events, schemas)
- Update `ARCHITECTURE.md` to reflect target state (in a sibling `ARCHITECTURE-TARGET.md` until migration completes — keeps the live doc accurate)

## Step 5 — Phased Migration Plan

Pick a migration pattern fit for the situation:

| Pattern | When to use | Key risk |
|---|---|---|
| **Strangler fig** | Replacing a monolith feature-by-feature; new system grows around the old | Edge cases stuck in the old system long-term |
| **Expand-contract** | Schema migrations; add new shape, dual-write, switch reads, remove old | Dual-write divergence; backfill correctness |
| **Branch by abstraction** | Refactoring inside a single codebase; abstract behind interface, swap impl | Interface drift; long-lived branches |
| **Parallel run** | High-risk cutovers; both systems run side-by-side, results compared | 2× cost; result-divergence triage |

Phase structure (typical):

| Phase | Goal | Exit criteria | Rollback |
|---|---|---|---|
| 0 | Baseline + observability parity | Telemetry on both systems matches | Skip — no production change |
| 1 | Stand up new system, no traffic | New system passes synthetic checks | Tear down, no traffic was routed |
| 2 | Shadow traffic / read-only | Result divergence < 0.1 % | Stop shadow, no user impact |
| 3 | 1 % canary | Error rate ≤ baseline, latency within SLO | Route back to old (instant) |
| 4 | 10 % → 50 % → 100 % | Error rate ≤ baseline at each step | Route back to old |
| 5 | Decommission old | All traffic on new for 2 weeks | N/A — old removed |

For schema migrations, use expand-contract semantics — never break-then-fix.

## Step 6 — Fitness Functions

Automated architectural checks that enforce the transition:

| Fitness function | What it checks | Where it runs |
|---|---|---|
| Coupling check | No imports from new → old after phase N | CI on PR |
| Dependency drift | New system stays on target tech versions | CI / dependabot |
| Latency budget | p95 of new system ≤ target | Production observability + alert |
| Result parity | Shadow-traffic divergence < threshold | Phase 2 dashboard |
| Coverage parity | New system test coverage ≥ old's | CI |

Fitness functions catch regression early — without them, the migration drifts off-target invisibly.

## Step 7 — Rollback Strategy

For each phase, document:

- **Detection signal**: alert that fires (latency, error rate, divergence, manual call)
- **Decision threshold**: when to roll back vs investigate vs press on
- **Rollback action**: exact runbook step (config flag, traffic route change, schema revert, code revert)
- **Time-to-rollback target**: should be measured in minutes for traffic, hours for schema, days for code

A migration without explicit rollback per phase is a one-way door. Reject the plan if rollback is missing for any phase that touches production.

## Step 8 — Quality Gates

- [ ] Migration pattern matches the change (no parallel-run for trivial refactors; no strangler-fig for schema changes)
- [ ] Each phase has explicit exit criteria + rollback procedure
- [ ] Target NFRs are concrete and delta-justified vs current
- [ ] Fitness functions cover the structural invariants that the migration relies on
- [ ] Dual-running cost is estimated (cloud cost, ops load, team capacity)
- [ ] Decommission phase is included (otherwise the old system lingers as debt)
- [ ] Security review covers BOTH systems during dual-run and the new system post-cutover
- [ ] Data migration (if any) has explicit backfill + verification plan

## Step 9 — Engineering Estimates

Per-phase estimates to feed `/plan`:

| Phase | Tasks | Complexity | Roles | Dependencies |
|---|---|---|---|---|
| 0 | Observability parity | M | `@sre-engineer`, `@devops-engineer` | none |
| 1 | Stand up new system | L | `@<stack>-engineer`, `@devops-engineer` | phase 0 |
| ... | ... | ... | ... | ... |

## Step 10 — Present and Persist

Present: migration ADR, target-state diagrams, phased plan + rollback per phase, fitness functions, total cost estimate, total timeline. Wait for user approval. The user may request changes — common ones: longer canary, additional shadow phase, smaller initial scope.

After approval, save:

1. **ADR** → `docs/adr/ADR-NNN-migrate-[from]-to-[to].md`
2. **Target architecture** → `docs/architecture/ARCHITECTURE-TARGET.md` (becomes live `ARCHITECTURE.md` at end of migration)
3. **Migration plan** → `docs/architecture/migrations/[migration-name]/PLAN.md`
4. **Rollback playbook** → `docs/architecture/migrations/[migration-name]/ROLLBACK.md`
5. **Fitness functions** → as actual code (CI checks) and as doc `docs/architecture/migrations/[migration-name]/FITNESS.md`

## Step 11 — Handoff

Run `/plan` for each phase. Phases run as separate `/develop` cycles to keep blast radius small.

## Integration

- **Input from**: `/architecture-analyze` (current state baseline), strategic initiative
- **Followed by**: `/plan` (per-phase decomposition), `/develop` (per-phase execution)
- **Roles**: `Agent(solution-architect)` (ADR), `Agent(system-architect)` (target state), plus `Agent(cloud-architect)` / `Agent(devops-architect)` for infra/pipeline-touching migrations
- **Output style**: `${CLAUDE_PLUGIN_ROOT}/output-styles/design-pack.md`
- **Templates**: `${CLAUDE_PLUGIN_ROOT}/skills/architecture/assets/` — `adr-template.md`, `c4-mermaid-template.md`, `nfr-template.md`, `tech-debt-register-template.md`
- **Related skills**: `/migrate` (library/schema-level migrations with RALF rollback gate; smaller scope than architecture-level evolution)
- **Knowledge**: `@owasp-coverage` (security during dual-run), `@observability-methods` (fitness functions for telemetry parity), `@supply-chain-security` (target-state SBOM/SLSA)
