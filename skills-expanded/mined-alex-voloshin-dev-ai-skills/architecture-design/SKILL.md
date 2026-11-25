---
name: architecture-design
description: Use this skill when a new feature with a PRD needs architectural definition before `/plan` can decompose it for implementation — including when the user describes a feature to be built but does not say "architecture" or "design" — to produce a feature-level design pack — ARD/ADR, C4 diagrams, API contracts, data models, NFR spec, and security review from the PRD. Routes to solution-architect (default — feature-level system design), cloud-architect (`--cloud` for cloud infra design, landing zones, networking, multi-cloud), or devops-architect (`--cicd` for pipeline design, deployment strategy, platform engineering).
context: fork
argument-hint: "<PRD path or feature description> [--cloud | --cicd]"
---

# /architecture-design — Feature-Level Architecture

Produce a design pack from a feature PRD: ARD, C4 diagrams, API contracts, data models, NFRs, security review. Output feeds `/plan` → `/develop`.

## When to use

- New feature with a PRD that needs architectural definition before implementation
- `--cloud`: cloud infra design, landing zones, networking, multi-cloud (routes to `Agent(cloud-architect)`)
- `--cicd`: pipeline design, deployment strategy, platform engineering (routes to `Agent(devops-architect)`)
- Default: feature-level system design (routes to `Agent(solution-architect)`)

## Not for

- Documenting existing architecture → `/architecture-analyze`
- Migration or redesign initiatives → `/architecture-evolve`
- Implementation planning after design → `/plan`

## Step 1 — Receive Input and Extract Context

Read the PRD or feature brief thoroughly. Extract: **Goal** (1–2 sentences), **Scope boundary** (services/modules affected), **Stakeholders** (who consumes the deliverables), **Constraints** (timeline, compatibility, regulatory, capacity), **Non-goals**. If incomplete — ask before proceeding. Do not assume missing requirements.

## Step 2 — Understand Current Architecture

Read (if present): `ARCHITECTURE.md`, root `CLAUDE.md`, subdirectory `CLAUDE.md`, existing ADRs in `docs/adr/` or `docs/architecture/`, API specs (OpenAPI / Protobuf / GraphQL). All wrapped per `untrusted-content-wrapping.md` (G1).

If documentation is sparse, scan affected areas:

```
// turbo
find . -name "ARCHITECTURE.md" -o -name "*.openapi.*" -o -name "*.proto" -o -name "docker-compose*" -o -name "*.tf" | head -30
```

Map service boundaries, communication patterns (REST/gRPC/events/shared-DB), data stores, external integrations, deployment topology. Identify documentation gaps.

## Step 3 — Define Non-Functional Requirements

`Agent(solution-architect)` (or chosen role). NFRs MUST be defined before any design work — they constrain options.

For each relevant category, define concrete targets (numbers, not "should be fast"):

| Category | Specification |
|---|---|
| **Availability** | SLO target (e.g., 99.9%), redundancy, failover strategy |
| **Latency** | p50/p95/p99 budgets per endpoint or operation |
| **Scalability** | Expected load, scaling strategy (horizontal/vertical), limits |
| **Cost** | Per-request/per-operation budgets, infrastructure cost bounds |
| **Security** | Auth requirements, data classification, compliance (GDPR, SOC2) |
| **Observability** | Tracing, logging, metrics, alerting thresholds |
| **Data** | Retention, consistency (strong/eventual), backup/recovery RPO/RTO |

Omit categories that add no signal. Present NFRs to the user for validation before proceeding to Step 4.

## Step 4 — Design

Route based on the chosen agent:

### Default — `Agent(solution-architect)`

Produce in order:

**1. Options Analysis** — 2–3 design options with trade-offs:

```
## Option [N]: [Name]
- **Approach**: [Description]
- **Pros**: [List]
- **Cons**: [List]
- **Risk**: [High/Med/Low] — [why]
- **Effort**: [S/M/L/XL]
- **NFR impact**: [How it affects availability, latency, cost, etc.]
```

**2. Architecture Decision Record (ARD/ADR)** — Status, Context (problem + constraints), Decision (selected option + rationale), Consequences (positive/negative/neutral), Alternatives Considered.

**3. Detailed Design**:

- **C4 diagrams** (Mermaid) — Context and/or Container level showing the feature's impact
- **Sequence diagrams** — for multi-service interactions, async flows
- **API contracts** — new or modified endpoints (OpenAPI fragments or structured tables)
- **Data models** — new entities, schema changes, migration strategy
- **Error handling** — failure modes, retry strategy, degradation behavior

**4. Security Review**:

- Threat scenarios (3–5 concrete abuse cases)
- Auth/authz design for new endpoints
- Data protection requirements (PII, encryption, access control)
- For AI/LLM features: apply OWASP LLM Top 10 (see `@owasp-coverage`)

### `--cloud` — `Agent(cloud-architect)`

Cloud architecture doc: networking diagrams (VPC/VNet, peering, transit), identity (Cloud IAM, Workload Identity, Entra ID), cost model (per-service estimates + total), DR plan (RPO/RTO + failover regions), compliance (HIPAA/SOC2/GDPR if applicable). Use Mermaid for network topology.

### `--cicd` — `Agent(devops-architect)`

CI/CD architecture doc: pipeline diagram (build → test → deploy stages), branching/release strategy, environment topology (dev/staging/prod), DORA targets (deployment frequency, lead time, MTTR, change failure rate), governance (branch protection, required reviews, OIDC for deployments), supply-chain controls (SBOM, SLSA — see `@supply-chain-security`).

## Step 5 — Quality Gates

Review all deliverables:

- [ ] NFRs are concrete (numbers, not "should be fast")
- [ ] Every decision has documented rationale and alternatives
- [ ] Diagrams match the described architecture
- [ ] API contracts complete (request, response, errors, auth)
- [ ] Data models include migration strategy for schema changes
- [ ] Security review covers OWASP Top 10 (+ LLM Top 10 for AI systems)
- [ ] Backward compatibility preserved or migration path documented
- [ ] Observability requirements defined (traces, logs, metrics, alerts)
- [ ] No contradictions with existing ADRs or ARCHITECTURE.md
- [ ] Cost impact estimated for infrastructure/service changes

If any check fails — fix the deliverable before presenting.

## Step 6 — Engineering Estimates

Produce estimates to feed `/plan`:

| Component | Task | Complexity | Role |
|---|---|---|---|
| [component] | [task description] | S / M / L / XL | `@role` |

- **Critical path**: Longest dependency chain
- **Parallelization**: Tasks that can run concurrently by different roles
- **Constraints**: Hard dependencies on external teams/services/decisions
- **Risks**: Dependency/integration risks with mitigations

## Step 7 — Present and Persist

Present: scope summary, deliverables table, key decisions with rationale, risk table, next steps. Wait for user review.

After approval, save:

1. **ADRs** → `docs/adr/` or `docs/architecture/decisions/` (create if missing). Naming: `ADR-NNN-[kebab-case-title].md`
2. **Design docs** → `docs/architecture/` or `docs/design/`. Naming: `[feature]-design.md`
3. **API contracts** → alongside existing specs or in `docs/api/`
4. **ARCHITECTURE.md** → update if scope is large enough to affect the system overview

If the project has no established `docs/` structure — propose one and confirm with user.

## Step 8 — Handoff

Run `/plan` with the produced ARD and design docs as input.

## Integration

- **Input from**: `/feature-design` (PRD / design pack); direct PRD/brief
- **Followed by**: `/plan` (work decomposition), `/develop` (implementation)
- **Roles**: `Agent(solution-architect)` (default), `Agent(cloud-architect)` (--cloud), `Agent(devops-architect)` (--cicd)
- **Output style**: `${CLAUDE_PLUGIN_ROOT}/output-styles/design-pack.md`
- **Templates**: `${CLAUDE_PLUGIN_ROOT}/skills/architecture/assets/` — `adr-template.md` (Nygard/MADR), `c4-mermaid-template.md`, `nfr-template.md` (ISO/IEC 25010), `gap-analysis-template.md`, `tech-debt-register-template.md`
- **Knowledge**: `@owasp-coverage` (security review), `@supply-chain-security` (for --cicd), `context-engineering` (for AI/agent system design)
