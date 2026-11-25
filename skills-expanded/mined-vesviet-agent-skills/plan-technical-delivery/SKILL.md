---
name: plan-technical-delivery
description: Turn architecture decisions and requirements into a delivery-ready technical plan with slices, quality gates, impact radius, and rollout notes. Use when Technical Lead breaks down implementation work for developers, QA, and release.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Plan Technical Delivery

Use with the **Technical Lead** role after requirements and architecture inputs exist to establish a spec-driven, milestone-gated delivery plan.

## When to Use

- Technical Lead breaking down implementation work into executable slices
- anchoring delivery to immutable interface specs and contract invariance
- defining blast radius, failure domain isolation, and regression risk matrices
- establishing intermediate milestone gates and sandbox execution tiers for dev/QA/release

## Core Rules

- **Spec-driven contract freeze**: interface contracts (OpenAPI 3.1, JSON Schema, Protobuf) must be validated and frozen before dispatching any implementation slice; slices must explicitly declare preserved invariants
- **Vertical thin slicing (Tracer Bullets & DAG Frontier)**: decompose features into thin vertical tracer-bullet slices (schema → API → UI → tests) delivering independent user value — sized for a single context window (≤400 lines diff); declare explicit `Blocked by` DAG dependencies to expose the parallelizable execution frontier; horizontal layer slicing is prohibited
- **Expand-Contract Refactoring**: execute breaking interface or schema migrations via 3 safe phases (*Expand* parallel surface → *Migrate* callers in slices → *Contract* legacy surface) rather than big-bang rewrites
- **Blast radius & regression risk matrix**: evaluate consumer fanout (High/Medium/Low), failure domain isolation, mutation vulnerability hotspots, and zero-downtime data migration rollback safety for every slice
- **Sequential milestone gates**: progression between dependent slices requires passing automated gates: Gate 1 (Contract Freeze), Gate 2 (Red Test in Sandbox), Gate 3 (Green Impl in Sandbox), and Gate 4 (Mutation Score ≥75–80% & Blast Radius Check)
- **Execution sandbox tier mapping**: map every slice to its required execution sandbox tier (Tier 1 Process, Tier 2 Docker container with `--network=none`, Tier 3 gVisor/MicroVM) per `core/policies/execution-sandbox.md`
- **Feature flag-first delivery**: every user-visible slice requires a flag name, kill-switch, progressive rollout stages (internal → canary → GA), and ISO 8601 cleanup target date
- **Hybrid slice governance**: specify compute budgets, HITL checkpoints, and agent output gates for agent-implemented slices
- **Uncertainty-bounded estimation**: use three-point estimates (optimistic P10, expected P50, pessimistic P90); balance delivery signals with DORA and SPACE metrics
- emit `contracts/schemas/technical-delivery-plan.json` for automated machine handoff
- do not implement production code — delegate slices to developer and QA roles
- detailed rubrics, matrix worksheets, and gate templates are maintained in [`references/spec-driven-planning.md`](references/spec-driven-planning.md)

## Suggested Process

### 1. Ingest Constraints & Freeze Invariant Specs

Read `contracts/schemas/feature-ticket.json`, `contracts/schemas/adr-spec.json`, and API specs. Validate and freeze interface schemas against meta-validators before slice dispatch.

### 2. Decompose Spec-Driven Slices & Assign Sandbox Tiers

Break work into vertical thin slices (≤400 lines diff). Order by dependency and risk. Map each slice to its required sandbox tier (e.g. Tier 2 Level 0 air-gapped container). Define ownership (Human, Agent, or Hybrid), setting compute budgets and HITL checkpoints.

### 3. Build Blast Radius & Regression Risk Matrix

Analyze downstream consumer fanout, failure domain boundaries, mutation test hotspots in legacy paths, and database expand/contract migration safety per [`references/spec-driven-planning.md`](references/spec-driven-planning.md).

### 4. Establish Sequential Milestone Gates

Define verifiable progression gates for each slice: Gate 1 (Spec Freeze), Gate 2 (Red Test Failing in Sandbox), Gate 3 (Green Implementation in Level 0 Sandbox), and Gate 4 (Mutation Score ≥75–80% & Blast Radius Verification).

### 5. Plan Feature Flags, Rollout & Documentation

Design feature flag controls, kill-switches, progressive rollout stages, and cleanup target dates. Document rollback procedures and list `documentation_deltas` for the Technical Writer.

### 6. Emit Delivery Plan

Validate and output `contracts/schemas/technical-delivery-plan.json`. Hand off to developers, QA, and Reviewer with explicit slice and gate references.

## Inputs

- `contracts/schemas/feature-ticket.json` from Business Analyst
- `contracts/schemas/adr-spec.json` from Technical Architect
- `contracts/schemas/api-contract-spec.json` when API work is in scope
- `contracts/schemas/ux-flow-spec.json` when UI is in scope
- `contracts/schemas/implementation-result.json` from developers when updating readiness

## Role Boundaries

| Role | Owns |
| ---- | ---- |
| Technical Lead | This plan, slices, gates, regression risk, readiness |
| Technical Architect | adr-spec.json, system boundaries |
| Reviewer | code-review-finding disposition |
| QA Engineer | test-report.json, validation-result.json, red tests |
| Agent Coordinator | coordination-plan.json phase graph |

## Checklist

- [ ] interface contracts (OpenAPI 3.1/JSON Schema) validated and frozen as invariant specs
- [ ] all slices sliced vertically (UI → API → DB) and targeted at ≤400 lines diff
- [ ] blast radius, failure domain isolation, and regression risk matrix documented
- [ ] sequential milestone gates (Contract, Red Test, Green Impl, Mutation) defined
- [ ] sandbox execution isolation tiers mapped per slice per `core/policies/execution-sandbox.md`
- [ ] every user-visible slice has feature flag name, kill-switch, rollout plan, and cleanup target date
- [ ] hybrid slices have compute budgets, HITL checkpoints, and agent output gates defined
- [ ] all slices estimated with explicit uncertainty bounds (P10, P50, P90)
- [ ] documentation_deltas listed for Technical Writer
- [ ] `technical-delivery-plan.json` emitted and validated against schema

## Related Skills

- **review-code**: Validate implementation against plan
- **review-service**: Service-level readiness
- **agent-delegation**: Assign slices to specialist roles
- **write-documentation**: Downstream doc work — Technical Writer role

## Output Contracts

- `contracts/schemas/technical-delivery-plan.json`

When the plan is consumed by an infra agent, release manager, or coordinating role, emit the JSON plan and a markdown summary. The JSON must list every slice with its `owner`, `compute_budget`, `hitl_checkpoints`, `feature_flag`, `rollout_stages`, `cleanup_target_date`, `sandbox_isolation_tier`, `blast_radius`, and three-point estimate (P10/P50/P90).

## Failure Modes

- **Horizontal slicing**: plan decomposes by layer (DB → API → UI) instead of user-visible slices. Mitigation: enforce vertical slicing; reject plans where slices do not deliver end-to-end user value.
- **Spec drift / unvalidated contracts**: code authored before API schemas are validated and frozen. Mitigation: enforce Gate 1 Spec Freeze as a mandatory pre-condition.
- **Missing blast radius assessment**: slice touches shared modules without evaluating consumer fanout or legacy mutation hotspots. Mitigation: reject plans lacking regression risk matrix.
- **Missing flag or permanent flag**: slice lacks kill-switch or ISO 8601 cleanup target. Mitigation: enforce feature flag lifecycle fields in plan validation.
- **Hybrid ambiguity**: slice marked hybrid without compute budget, HITL checkpoints, or output gates. Mitigation: require all three fields for hybrid assignments.
- **Point estimate**: single duration estimate without uncertainty bounds. Mitigation: require P10/P50/P90 estimation.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: cross-check each slice against source `feature-ticket.json` and `adr-spec.json`; reject off-scope work.
- **ASI03 Identity & Privilege Abuse**: validate each slice's required tools against assigned role's `action-boundaries.yaml`; do not bypass role boundaries.
- **ASI05 RCE Guard**: enforce execution sandbox tiers (`core/policies/execution-sandbox.md`) for all build and test execution steps.
- **ASI07 Inter-Agent Communication**: emit structured `technical-delivery-plan.json` so downstream roles share the identical source of truth.
- **ASI08 Cascading Failures**: surface dependency blocks in the coordination plan; evaluate failure domain isolation in the blast radius matrix.
- **ASI09 Human-Agent Trust Exploitation**: never mark hybrid slices ready while missing HITL checkpoints.
