---
name: ma-write
description: ma 파이프라인의 PRD 또는 기술 설계 문서를 작성·갱신한다. PRD는 요구사항 인터뷰와 리서치 후 검증 가능한 문서로, design은 승인 가능한 PRD를 기반으로 API·데이터·크로스 레포 계약과 다이어그램으로 만든다. "ma-write", "PRD 작성", "PRD 이어쓰기", "기술 설계 작성", "tech design" 요청에 사용. 구현 PLAN은 `/ma-plan`, 산출물 리뷰는 `/ma-review`를 사용하며 코드 구현이나 비-MA 일반 문서에는 사용하지 않는다.
---

# /ma-write

Create workspace-owned PRD or technical-design contracts. Stay within the `docs` scope; never hand off, implement, commit, push, or open an MR from this skill.

## Invocation

```text
/ma-write <issue-key> [prd|design] [--auto] [--no-interview]
```

| Input | Action | Output |
|---|---|---|
| `/ma-write PROJ-123 prd` | Run the PRD workflow and conditional gates | PRD plus optional blueprint/brief |
| `/ma-write PROJ-123 design` | Validate the PRD, then run the design workflow | Design plus diagrams |
| `/ma-write PROJ-123 prd --no-interview` | Draft from available evidence without Phase 0 Q&A | Ready PRD or `[BLOCKED]` draft with decisions |

## Resolve the mode

1. Use an explicit `prd` or `design` argument when provided.
2. Without a mode, inspect the canonical paths:
   - PRD missing → `prd`
   - PRD exists and design missing → `design`
   - Both exist → resume the artifact containing unresolved work; if neither is clearly in progress, ask whether to update PRD or design.
3. Require the issue key. Resolve the domain through the workspace config (`projects.{name}.domain`) before reading project code.

## Load only the selected workflow

- `prd`: read `references/modes/prd.md`. Load `checklists/prd-scenario-edge-cases.md` and `references/modes/blueprint.md` only when their gates match.
- `design`: read `references/modes/design.md`.

Do not load the other mode's reference; this is the primary context-budget boundary.

## References index

| File | When to read |
|---|---|
| [references/modes/prd.md](references/modes/prd.md) | PRD mode — full workflow |
| [references/modes/design.md](references/modes/design.md) | Design mode — full workflow |
| [references/modes/blueprint.md](references/modes/blueprint.md) | PRD mode — only when the blueprint gate matches (UI/flow/stakeholder-visible change) |
| [references/diagram-choice.md](references/diagram-choice.md) | Design docs — which diagram type fits which content |
| [checklists/prd-scenario-edge-cases.md](checklists/prd-scenario-edge-cases.md) | PRD mode — high-risk-domain features such as auth/payment/scheduling (gate list inside) |

Role dirs: `modes/` = per-artifact writing workflows (skill-specific).

## Shared gates

- Read the ma skill's scope gate (`../ma/references/scope-gate.md`) at entry. Record or retain a terminal scope of `docs`; ask once if the caller's terminal scope is ambiguous.
- Forward `--auto` only when the user explicitly requested unattended document generation. It skips Q&A and confirmation but never authorizes guessing a Blocking product decision.
- `--no-interview` skips only PRD Phase 0. Carry unanswered items into `## 확인이 필요한 사항`; unresolved Blocking items keep the artifact incomplete.
- A mode completes only after its output files exist, its self-check passes, and no Blocking item remains. Otherwise return `[BLOCKED]` with the artifact path and next decision required.
- Report concise paths and remaining decisions. Keep long research or logs outside the document and link their source paths.

## Outputs

- PRD: `{contextRoot}/{domain}/prd/{key}.md`
- Optional blueprint: `{contextRoot}/{domain}/blueprint/{key}.html`
- Optional stakeholder brief: `{contextRoot}/{domain}/plan/{key}-stakeholder-brief.md`
- Design: `{contextRoot}/{domain}/design/{key}.md`
- Design diagrams: `{contextRoot}/{domain}/design/{key}-diagrams.md`

## Caller contract

- Standalone: run one resolved mode; `design` requires a PRD.
- `/ma`: Phase 1 calls `prd`, then Phase 2 calls `design`. Pass `--auto` only under the explicit unattended rule above.
