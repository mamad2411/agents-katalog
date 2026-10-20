---
name: docker-orchestrator
description: Use when a Docker request in .NET environments spans multiple capability areas and needs one deterministic intake, explicit phase ownership, and a unified execution contract.
---

# Docker Orchestrator for .NET

## Specialization

Use this skill to coordinate cross-project Docker requests in .NET environments when work spans image design, build optimization, compose workflows, security, testing, and CI delivery gates.

This skill owns deterministic intake and orchestration. It does not replace deep execution guidance in specialized Docker skills.

## Objective

Produce one deterministic Docker .NET execution contract from one intake, with explicit phase ownership, required evidence, and completion checks.

## Trigger Conditions

- A Docker .NET request spans more than one capability area.
- Teams need one intake instead of disconnected Docker, security, test, and CI workflows.
- Cross-project reusability and discoverability are required.
- A change needs explicit ownership across Dockerfile, compose, security, testing, and CI outputs.

## Scope Boundaries

In scope:

- Deterministic Docker .NET intake and phase planning.
- Output ownership with exactly one owner per required output.
- Unified recommendation and handoff contract.

Out of scope:

- Deep implementation details owned by specialized skills.
- Kubernetes deployment architecture design.
- Product application feature changes outside container concerns.

## Inputs

- User objective and target .NET container surface.
- Scope boundaries and risk constraints.
- Required outputs and delivery constraints.
- Evaluation date in ISO format (YYYY-MM-DD).

## Required Outputs

- Intake contract with objective, boundaries, and required outputs.
- Phase-output ownership matrix.
- Unified execution recommendation.
- Rejected-candidate table with deterministic reason codes.
- Closure check confirming no unowned outputs.

## Capability Catalog

- Foundations and Dockerfile Baseline
- BuildKit and Optimization
- Compose Workflows
- Devcontainers and Inner-Loop Environments
- Multi-Platform Builds and Manifest Publishing
- Runtime Diagnostics and Recovery
- Security and Supply Chain
- Testcontainers and Integration Testing
- CI/CD and Promotion Gates
- Source Curation and Freshness
- Quality Gate and Review Readiness

## Deterministic Workflow

1. Lock objective, boundaries, risk profile, and required outputs.
2. Classify request into one or more capability phases.
3. Assign exactly one owner per required output.
4. Reject plans with unowned or multiply owned outputs.
5. Define evidence expectations and handoff criteria.
6. Produce one execution recommendation: narrow-execution, phased-execution, or stop-pending-blockers.
7. Publish closure status with residual risks and blockers.

## Phase-Output Ownership Matrix Template

| Required Output | Owning Phase | Evidence Expectation |
|---|---|---|
| Dockerfile baseline and build pattern | Foundations and Dockerfile Baseline | Template and source-backed rule mapping |
| Build cache and performance optimization | BuildKit and Optimization | Build logs or benchmark delta notes |
| Local and CI compose contract | Compose Workflows | Compose template set and validation notes |
| Containerized developer environment contract | Devcontainers and Inner-Loop Environments | Devcontainer template and validation notes |
| Multi-platform release contract | Multi-Platform Builds and Manifest Publishing | Platform matrix and manifest inspection evidence |
| Runtime failure diagnosis path | Runtime Diagnostics and Recovery | Logs, inspect output, and recovery summary |
| Security posture and supply-chain controls | Security and Supply Chain | Scan results, SBOM output, hardening checklist |
| Containerized integration test approach | Testcontainers and Integration Testing | Test fixture pattern and execution proof |
| Build, scan, and publish pipeline | CI/CD and Promotion Gates | Pipeline template and gate criteria |
| Source traceability and freshness | Source Curation and Freshness | Source ledger with date and relevance |
| Go or no-go quality disposition | Quality Gate and Review Readiness | Findings table and recommendation |

## Unified Decision Rules

- narrow-execution: One phase materially owns work, others are informational.
- phased-execution: Two or more phases are required and ownership is unambiguous.
- stop-pending-blockers: Required outputs are unowned, evidence missing, or risk unbounded.

## Rejected Candidate Reasons

- R1: Outside Docker .NET container scope.
- R2: Adds overlap without required-output coverage.
- R3: Expands scope beyond bounded objective.
- R4: Requires evidence or environment access that is unavailable.
- R5: Better handled by a narrower single-capability skill.

## Self-Contained Assets

- Example code: [routing-decision.example.json](./references/examples/routing-decision.example.json)
- Example configuration: [docker-orchestrator-routing.sample.yaml](./references/templates/config/docker-orchestrator-routing.sample.yaml)
- Reusable templates: [docker-execution-contract-template.md](./references/templates/docker-execution-contract-template.md) and [phase-ownership-matrix-template.md](./references/templates/phase-ownership-matrix-template.md)
- Script: [validate-docker-orchestrator-contract.ps1](./references/scripts/validate-docker-orchestrator-contract.ps1)

## Done Criteria

- Trigger conditions are met.
- Required outputs are complete.
- Ownership matrix has no unowned or multiply owned outputs.
- Decision mode is explicit.
- Source catalog is current for the evaluation cycle.

## Workflow

1. Capture inputs and constraints.
2. Execute this skill's deterministic steps.
3. Publish outputs with status and next actions.

## Execution Context
### Input Context

- Request objective and scope boundary.
- Applicable constraints and required outputs.

### Process Context

- Follow this skill's deterministic workflow from intake to closure.
- Record ownership and decisions for required outputs.

### Output Context

- Deliverables with explicit completion status.
- Residual risks and next actions.
## References Assets

- [Reference assets](./references/README.md)
