---
name: ma-plan
description: 승인 가능한 ma PRD/design을 프로젝트별 실행 PLAN으로 변환한다. 각 대상 레포의 규칙·유사 구현·테스트 패턴을 읽는 병렬 Plan Agent를 호출하고, 생성된 PLAN 구조와 AC 매핑을 검증한다. "ma-plan", "프로젝트별 PLAN 생성", "구현 계획 만들어줘" 요청에 사용. 전체 파이프라인은 `/ma`, PRD/design 작성은 `/ma-write`, 계획 검토는 `/ma-review plan`을 사용하며 일반 비-MA 계획이나 코드 구현에는 사용하지 않는다.
---

# /ma-plan

Generate one executable implementation PLAN per target project. Keep product code read-only; this skill writes only temporary PLAN files for later review and handoff. Each PLAN also decides whether the runtime E2E gate is required, so later phases do not invent verification scope after implementation.

## Invocation

```text
/ma-plan <issue-key> [--projects=project-a,project-b] [--auto]
```

| Input | Action | Output |
|---|---|---|
| `/ma-plan PROJ-123` | Derive projects, confirm, dispatch Plan Agents | One PLAN per project |
| `/ma-plan PROJ-123 --projects=example-frontend,example-backend` | Use the explicit registered projects | Two validated PLAN files |
| `/ma-plan PROJ-123 --auto` | Skip confirmation only when inputs and targets are unambiguous | Validated PLANs or `[BLOCKED]` evidence |

## Preconditions

1. Read the ma skill's scope gate (`../ma/references/scope-gate.md`) and retain a terminal scope of `plan`. Do not enter handoff or implementation.
2. Require PRD, design, and diagrams at their canonical `{contextRoot}/{domain}/` paths.
3. Scan PRD/design open-decision sections. If an unresolved `[Blocking]` product or contract decision remains, return `[BLOCKED]`; Important/Deferrable items may continue as PLAN risks.
4. Resolve projects from explicit `--projects`, otherwise from the PRD affected-project list and design `Cross-repo Impact` rows marked `Yes`.
5. Validate every project against the workspace config `projects` registry. If PRD and design disagree, ask for reconciliation; `--auto` does not guess the project set.
6. If a target PLAN already exists, update it as a resume only when its key/project identity matches. Do not create duplicate variants or silently overwrite a different target.

## Adaptive planning

Resolve `Small`, `Medium`, or `Large` from the design and affected surface. Apply the evidence budgets in `config/inputs.md` and step ranges in `templates/plan.md`; treat them as targets rather than quotas and never add filler.

## Workflow

### Phase 1 — Resolve and confirm inputs

1. Resolve the workspace root, issue key, domain, design size, and target projects.
2. Read `config/inputs.md` and prepare each project-specific input set.
3. Show project → output-path mappings unless `--auto` applies.

### Phase 2 — Dispatch in parallel

Dispatch one `executor`-role Task Agent per project in the same message using `prompts/dispatch.md` (map the role to your agent roster or run sequentially inline). Each agent reads only the relevant project rules and evidence, then writes `{contextRoot}/{domain}/plan/{key}-{project}.md` from `templates/plan.md`.

Require the compact return contract: `STATUS`, `CHANGED`, `EVIDENCE`, `VERIFIED`, `NOT_VERIFIED`, and `RISK`. Keep raw research and logs out of the response.

### Phase 3 — Collect, validate, and retry

1. Collect all parallel results; an `OK` result does not imply another agent should start.
2. For each `STATUS: OK`, verify the PLAN structurally (a deterministic validator script is not included in v1 — check by reading):
   - every template section present, no unresolved `{placeholder}` text
   - every Step has files, verification, and completion criteria
   - the AC-to-step mapping covers every PRD verification item
   - the runtime E2E decision is exactly `required` or `not_applicable` with a rationale
3. Treat a verification failure as `FAILED` with its exact diagnostics.
4. Retry only the failed project, up to two times. Include the prior failure evidence and correct missing inputs or prompt details; do not repeat an identical prompt blindly.
5. Preserve successful PLANs. Finish only when the validated output set exactly matches the target-project set.

### Phase 4 — Review handoff

Summarize each PLAN's candidate files, evidence, verification ladder, E2E decision, dependencies, and remaining risks. Route next to `/ma-review plan {key}`. `/ma-handoff` remains blocked until plan review and implementation approval pass.

## Ownership and lifecycle

- The workspace owns PRD/design contracts; each PLAN is a temporary single-repo execution asset.
- Write PLANs to `{contextRoot}/{domain}/plan/{key}-{project}.md` for plan review.
- `/ma-handoff` moves each approved PLAN to `{worktree}/{docsPath}/{key}/PLAN.md` and removes the original. The worktree then becomes PLAN SSOT.

## Halt rules

- Missing/Blocking artifacts or ambiguous/conflicting projects → return `[BLOCKED]`; `--auto` never guesses.
- One target still failing after two corrective retries → preserve successful PLANs and halt that target with evidence.
- Every target failing → report the shared input/prompt defect before retrying.

## References index

| File | When to read |
|---|---|
| [config/inputs.md](config/inputs.md) | Phase 1 — adaptive input/evidence checklist per project |
| [prompts/dispatch.md](prompts/dispatch.md) | Phase 2 — per-project Plan Agent prompt |
| [templates/plan.md](templates/plan.md) | Phase 2 — PLAN structure and sizing rules the agents fill |
