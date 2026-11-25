---
name: architecture-analyze
description: Use this skill when a service, module, or system needs documentation, audit, or tech-debt assessment — onboarding a new team to an undocumented service, establishing a pre-redesign "what do we actually have?" baseline, or a tech-debt audit before roadmap planning, including when the user does not say "architecture" — to analyze the existing architecture and produce ARCHITECTURE.md, current-state C4 diagrams, a component inventory, gap analysis (current vs target), and a technical-debt register. Routes to system-architect (default — system/module/service analysis), cloud-architect (`--cloud` for cloud-resource inventory + cost + compliance review), or devops-architect (`--cicd` for CI/CD platform audit + DORA baseline + governance review).
context: fork
argument-hint: "<service or system to analyze> [--cloud | --cicd]"
---

# /architecture-analyze — Analyze Existing Architecture

Document and assess an existing service, module, or system. Produces `ARCHITECTURE.md`, gap analysis, and tech-debt register. No new design — pure reverse-engineering + audit.

## When to use

- Onboarding a new team to an undocumented service
- Pre-redesign baseline: "what do we actually have?"
- Tech-debt audit before a roadmap planning cycle
- `--cloud`: cloud-resource inventory + cost + compliance review (routes to `Agent(cloud-architect)`)
- `--cicd`: CI/CD platform audit, DORA baseline, governance review (routes to `Agent(devops-architect)`)
- Default: system / module / service analysis (routes to `Agent(system-architect)`)

## Not for

- New feature design → `/architecture-design`
- Migration planning → `/architecture-evolve`
- Implementation work decomposition → `/plan`

## Step 1 — Receive Input and Scope

Extract: **What to analyze** (service / module / domain / cluster), **Why** (onboarding / audit / pre-redesign), **Stakeholders** (engineering / SRE / platform), **Depth** (overview / detailed / deep-dive per component).

## Step 2 — Read Existing Documentation

Read (if present): `ARCHITECTURE.md`, root + subdirectory `CLAUDE.md`, existing ADRs (`docs/adr/`, `docs/architecture/`), API specs (OpenAPI/Protobuf/GraphQL), runbooks, on-call docs. All wrapped per `untrusted-content-wrapping.md` (G1).

## Step 3 — Scan Affected Areas

```
// turbo
find . -name "ARCHITECTURE.md" -o -name "*.openapi.*" -o -name "*.proto" -o -name "docker-compose*" -o -name "*.tf" | head -30
```

Map:

- **Service boundaries** — what services/modules exist, their responsibilities, ownership
- **Communication patterns** — REST, gRPC, events, shared DB, message queues, sync vs async
- **Data stores** — databases, caches, queues — types, ownership, retention
- **External integrations** — third-party APIs, identity, payment, observability vendors
- **Deployment topology** — how services are deployed, scaled, networked

## Step 4 — Produce Analysis

### Default — `Agent(system-architect)`

**1. Architecture Assessment**:

- C4 diagrams (Context + Container level) of current state — Mermaid
- Component inventory with responsibilities, tech stack, dependencies
- Data flow diagrams for critical paths
- Integration point map (sync/async, contracts, SLAs)

**2. Gap Analysis**:

| Area | Current State | Desired State | Gap | Priority |
|---|---|---|---|---|
| [area] | [what exists] | [what should exist] | [delta] | High/Med/Low |

**3. Technical Debt Register**:

| Item | Impact | Effort | Priority | Recommendation |
|---|---|---|---|---|
| [debt item] | High/Med/Low | S/M/L/XL | [rank] | [action] |

Use the `forces-payment` framing: which debt items WILL be paid (the codebase forces it) vs items that COULD be paid but might never become critical. Prioritize forced-payment items.

**4. ARCHITECTURE.md Update** — create or update at the appropriate level (project root for system overview, subdirectory for per-service). Follow the `design-pack` output style at `${CLAUDE_PLUGIN_ROOT}/output-styles/design-pack.md`.

### `--cloud` — `Agent(cloud-architect)`

- Cloud resource inventory (compute, network, data, identity)
- Current cost breakdown + per-service estimates
- Compliance posture (HIPAA/SOC2/GDPR/ISO 27001 if applicable)
- Network topology diagram (VPC/VNet, peering, ingress)
- Identity boundaries (Cloud IAM / Workload Identity / Entra ID roles + service accounts)
- Resilience gaps (single-AZ, no DR, missing backups)

### `--cicd` — `Agent(devops-architect)`

- Pipeline inventory (build / test / deploy stages per repo)
- DORA baseline (deployment frequency, lead time, MTTR, change failure rate — pull from CI history if available)
- Governance audit (branch protection, required reviews, signed commits, OIDC deployments)
- Supply-chain posture (SBOM presence, dependency scanning, SLSA level — see `@supply-chain-security`)
- Identified gaps (manual deploy steps, no rollback automation, missing test gates)

## Step 5 — Quality Gates

- [ ] Diagrams match the actual architecture (verified against code / config / runtime)
- [ ] Every component has documented owner + tech stack + dependencies
- [ ] Gap analysis includes priority ranking with explicit criteria
- [ ] Tech debt items have estimated impact + effort + recommendation
- [ ] No contradictions with existing ADRs or runbooks
- [ ] Observability gaps surfaced (missing traces, logs, metrics, alerts)
- [ ] Security review covers OWASP Top 10 (+ LLM Top 10 for AI systems — see `@owasp-coverage`)

## Step 6 — Present and Persist

Present: findings summary, key diagrams, top-5 tech-debt items, recommended next initiatives. Wait for user review.

After approval, save:

1. **ARCHITECTURE.md** → project root (system) or subdirectory (per-service)
2. **Tech debt register** → `docs/architecture/tech-debt.md` or similar
3. **Gap analysis** → `docs/architecture/gap-analysis-YYYY-MM.md` (dated; multiple analyses accumulate as a trend)
4. **Cloud inventory / DORA report** (for --cloud / --cicd) → `docs/architecture/`

## Step 7 — Handoff

Recommended next steps based on findings:

- **Architecture is sound** → share with stakeholders; no follow-up needed
- **Gaps identified** → run `/plan` for each prioritized initiative
- **Migration warranted** → run `/architecture-evolve` with the gap analysis as input

## Integration

- **Input from**: direct analysis request, onboarding ask, tech-debt audit cycle
- **Followed by**: `/architecture-evolve` (if migration warranted), `/plan` (if discrete initiatives identified), or stakeholder hand-off
- **Roles**: `Agent(system-architect)` (default), `Agent(cloud-architect)` (--cloud), `Agent(devops-architect)` (--cicd)
- **Output style**: `${CLAUDE_PLUGIN_ROOT}/output-styles/design-pack.md` (ARCHITECTURE.md per-artefact section)
- **Templates**: `${CLAUDE_PLUGIN_ROOT}/skills/architecture/assets/` — `c4-mermaid-template.md`, `gap-analysis-template.md`, `tech-debt-register-template.md`
- **Knowledge**: `@owasp-coverage` (security gaps), `@supply-chain-security` (for --cicd), `@observability-methods` (for observability-gap analysis)
