---
name: beacon-dev-workflow
description: Repository-local Beacon workflow for plan/design/slice/execute/verify/recover/archive work through .beacon/. Use when creating or following Beacon artifacts, promoting a slice to CURRENT.md, verifying a slice, handling recovery, or archiving completed work.
metadata:
  origin: silavater-beacon
---

# Beacon Dev Workflow

Use this skill to make repository work auditable through `.beacon/`: plan, design, slice, execute one active slice, verify, recover, and archive.

## Trigger

- user mentions Beacon, `.beacon/`, PLAN, PART DESIGN, TODO slices, CURRENT, UnitTestCore, incidents, recovery, or archive
- work needs a durable plan before implementation
- active work must be resumed, verified, recovered, or archived
- backlog or ideas need triage into executable work

## Read Order

1. Read `AgentRule.md` or equivalent project rules if present.
2. If `.beacon/` is missing, initialize planning; do not code yet.
3. Read `.beacon/CURRENT.md` if present.
4. Read the active `.beacon/parts/part-XXX/DESIGN.md`.
5. Read the active `.beacon/parts/part-XXX/TODO.md`.
6. Read `.beacon/BACKLOG.md` only for triage, never as execution permission.
7. Read `.beacon/incidents/` only when CURRENT points to recovery or conflict context is needed.
8. Read `.beacon/done/` only when historical evidence is needed.

## Workflow

1. **Plan**: maintain `.beacon/PLAN.md` as the long-term PART map.
2. **Design**: create one design authority at `.beacon/parts/part-XXX/DESIGN.md` before executable TODO work.
3. **Slice**: create `.beacon/parts/part-XXX/TODO.md` with verifiable SLICEs.
4. **Promote**: expand exactly one ready SLICE into `.beacon/CURRENT.md`.
5. **Execute**: implement only the allowed scope in CURRENT.
6. **Verify**: run or report the UnitTestCore target and manual QA status.
7. **Recover**: open an incident when work becomes unsafe, invalid, blocked, drifting, or verification fails non-trivially.
8. **Archive**: snapshot completed CURRENT/TODO and verification evidence under `.beacon/done/`.

## State Rules

- `.beacon/CURRENT.md` is the only active executable authority.
- `BACKLOG.md` is never executable permission.
- A PART `DESIGN.md` must exist before that PART `TODO.md` can be treated as executable.
- Only one SLICE may be active at a time.
- Every SLICE must have a verification target before implementation.
- `CURRENT.md` must stay short; history belongs in `done/` or `incidents/`.
- Completed CURRENT and PART TODO states must be archived.
- If CURRENT conflicts with PLAN, DESIGN, TODO, BACKLOG, done, or incidents, stop and reconcile before implementation.

## Hard Stops

Stop and ask or open an incident before continuing when:

- requirements have multiple reasonable interpretations
- PART design authority is missing
- selected SLICE lacks verification target or done gate
- implementation would exceed CURRENT allowed scope
- scope drift, invalid design assumption, unsafe diff, rejected outcome, or non-obvious verification failure appears
- rollback, abandon, destructive cleanup, or broad rework is being considered
- manual QA is needed but cannot be reported honestly

## Reference Routing

- Workflow structure, artifact authority, and closure rules: `references/workflow-structure.md`
- Artifact responsibilities and templates: `references/beacon-artifacts.md`
- SLICE contract, sizing, split/merge rules: `references/slice-contract.md`
- Incident V1 and recovery gates: `references/recovery-protocol.md`
- UnitTestCore V1, manifest, and QA reporting: `references/verification.md`
- Optional helpers: `scripts/init_beacon.ps1`, `scripts/UnitTestCore.ps1`

## Verification

Before claiming completion, prove:

- exactly one executable CURRENT exists or the state is intentionally planning-only
- BACKLOG was not used as execution permission
- changed Beacon artifacts match their reference responsibilities
- verification command or manual QA report is named
- incidents were opened/resolved when recovery rules required them
