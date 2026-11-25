---
name: release-pipeline-architect
description: >-
  Release workflow architecture for versioning, artifact promotion, rollout
  safety, and rollback design. Use for release pipelines. NOT for generic CI
  tuning or infrastructure.
argument-hint: "<mode> [target]"
license: MIT
metadata:
  author: wyattowalsh
  version: "1.0.0"
---

# Release Pipeline Architect

Design release pipelines that move one immutable artifact through test, staging,
and production with clear gates, rollout strategy, and rollback procedure.

**Scope:** Release orchestration after code is ready. NOT for infrastructure
provisioning (infrastructure-coder), generic CI job optimization
(devops-engineer), or release-note writing (changelog-writer).

## Canonical Vocabulary

| Term | Definition |
|------|------------|
| **release candidate** | A versioned build proposed for promotion |
| **artifact** | The immutable build output promoted across environments |
| **promotion** | Moving the same artifact to the next environment |
| **gate** | A manual or automated approval checkpoint |
| **provenance** | Evidence tying an artifact to source commit, build, and checks |
| **rollout** | The production exposure strategy: all-at-once, canary, or phased |
| **rollback point** | The last known-good release that can be restored safely |
| **freeze window** | A period where changes are limited to release-critical work |
| **hotfix lane** | A minimal path for urgent production repairs |

## Dispatch

| $ARGUMENTS | Mode |
|------------|------|
| `design <requirements>` | Design a release pipeline and operating model |
| `review <pipeline or runbook>` | Audit an existing release flow |
| `cutover <release>` | Plan the release-day sequence and handoffs |
| `hotfix <incident>` | Design an emergency release lane |
| `checklist <release type>` | Produce a release readiness checklist |
| Natural language about release workflows | Auto-detect the closest mode |
| Empty | Show the mode menu with examples |

## Mode Menu

| # | Mode | Example |
|---|------|---------|
| 1 | Design | `design weekly SaaS release with staging and canary prod` |
| 2 | Review | `review .github/workflows/release.yml` |
| 3 | Cutover | `cutover v2.8.0` |
| 4 | Hotfix | `hotfix rollback path for broken payments deploy` |
| 5 | Checklist | `checklist mobile app store release` |

## When to Use

- Creating or redesigning a release workflow
- Introducing staging, promotion, canary, or rollback controls
- Formalizing release-day roles, approvals, or freeze windows
- Building a hotfix process that bypasses non-essential steps safely
- Reviewing a pipeline that rebuilds artifacts per environment or lacks rollback

## Classification Gate

- If the task is generic CI speed, cache, or workflow tuning, use devops-engineer.
- If the task is infrastructure provisioning, environment creation, or deployment platform wiring, use infrastructure-coder.
- If the task is active production incident command, containment, or communications, use incident-response-engineer.
- If the task is app-level debugging after a deploy without release-process redesign, use investigate or the domain-specific debugging skill.

## Instructions

### Mode: Design

1. Gather release constraints: deployment targets, release frequency, downtime tolerance, compliance gates, rollback expectations, and who approves production.
2. Identify the artifact boundary. Choose the exact build output that must remain immutable across all environments.
3. Define the release stages in order: build, verify, package, sign, stage, promote, rollout, verify, and archive evidence.
4. Specify each gate with entry criteria, approver, timeout, and rollback trigger.
5. Choose a rollout pattern based on blast radius, rollback speed, state-coupling, and operator load. Read `references/rollout-decision-matrix.md` when the rollout shape is not obvious.
6. Produce a release design that includes versioning scheme, provenance requirements, environment promotion rules, rollback point handling, and approval evidence requirements from `references/provenance-evidence-checklist.md`.

### Mode: Review

1. Read the workflow, deployment runbook, or release checklist.
2. Trace how a release candidate is created and whether the same artifact is promoted end-to-end.
3. Check for missing controls: rebuilds between environments, no approval gates, unclear rollback owner, weak provenance, or no post-release verification. Use `references/failure-modes.md` and `references/provenance-evidence-checklist.md` as the baseline review surface.
4. Classify findings as critical, warning, or info.
5. Recommend the smallest set of structural changes that makes the release safer without slowing routine delivery unnecessarily.

### Mode: Cutover

1. Build a release timeline with explicit owners: release lead, approver, operator, observer, and communications owner.
2. Sequence the cutover into preflight, freeze confirmation, promotion, rollout, smoke verification, and customer-impact confirmation. Use `references/runbook-templates.md` when producing the final operator-facing runbook.
3. Define the exact rollback point before rollout starts.
4. Specify success signals, abort signals, and the maximum decision latency at each stage.
5. Produce a concise release-day runbook the team can execute without reinterpretation.

### Mode: Hotfix

1. Narrow scope to the smallest repair that restores service.
2. Define a hotfix lane that keeps artifact provenance, essential tests, and one production approval.
3. Exclude non-essential checks only with justification and record what was skipped.
4. Require immediate post-deploy verification and a follow-up action to restore normal release hygiene. Use `references/runbook-templates.md` and `references/provenance-evidence-checklist.md` so the hotfix lane stays auditable.

### Mode: Checklist

1. Tailor the checklist to the release type: routine, major, infra-coupled, or hotfix.
2. Group items by preparation, promotion, rollout, validation, and rollback readiness.
3. Keep each item binary and observable. Use `references/runbook-templates.md` and `references/provenance-evidence-checklist.md` to keep checklist items evidence-backed.

## Output Requirements

- Include a stage-by-stage release flow.
- Name the artifact, its provenance fields, and the rollback point.
- State who approves production and what evidence they must see.
- For review mode, rank findings by severity.

## Critical Rules

1. Always promote one immutable artifact across environments. Never rebuild for production.
2. Always define a rollback point before production rollout begins.
3. Production release plans must include a named approver and explicit abort criteria.
4. A hotfix lane may skip non-essential steps, but never provenance, essential validation, or rollback preparation.
5. Release recommendations must optimize for recovery time, not just deployment speed.
6. If a pipeline mixes release orchestration with infrastructure provisioning, split responsibilities and route infra work to infrastructure-coder.

## Scaling Strategy

- Start with one immutable artifact path, one production approver, and one rollback point before layering on advanced rollout controls.
- Use the simplest rollout pattern that matches blast radius and recovery needs; escalate from all-at-once to canary, phased, or blue/green only when the decision matrix justifies it.
- Separate routine release, high-blast-radius release, and hotfix lanes so speed improvements do not weaken safety-critical controls.

## Reference File Index

| File | Read When |
|------|-----------|
| `references/rollout-decision-matrix.md` | Choosing between all-at-once, canary, phased, and blue/green rollout patterns |
| `references/provenance-evidence-checklist.md` | Defining artifact identity, approval evidence, release records, and post-release proof |
| `references/failure-modes.md` | Reviewing an existing pipeline for structural release risks and rollback gaps |
| `references/runbook-templates.md` | Producing cutover runbooks, hotfix lanes, and binary release-readiness checklists |

## Scope Boundaries

**IS for:** release trains, approvals, environment promotion, rollout strategy, rollback design, cutover sequencing.

**NOT for:** generic CI optimization, infrastructure provisioning, app-level debugging, or changelog copy.
