---
name: ma-make-decisions
description: 작업 계획서(PRD + 설계 + 리뷰)에서 "확인 필요 / 미해결 / 후속 검토" 항목을 추출하여 브라우저 HTML 폼으로 변환. 각 항목에 의견 적고 일괄 복사 → CLI 붙여넣기로 PRD/설계 반영. "ma-decisions", "ma-make-decisions", "결정사항 정리", "워크플랜 체크", "오픈 이슈 정리", "확인사항 정리", "workplan open items" 시 사용. 단순 PRD 작성은 /ma-write, 계획 리뷰는 /ma-review plan.
---

# /ma-make-decisions

Extract **결정사항(decisions)** — PRD/design/PLAN/review에서 "확인 필요 / 미해결 / 후속 검토" 항목을 의미 — render HTML feedback form → user writes opinions per card → bulk copy → paste in CLI → batch apply to PRD/design/PLAN.

용어 통일: 본문은 **결정사항(decisions)**으로 통일. 동의어 — "오픈 이슈(open items/open issues)", "open decisions", "확인사항"은 사용자 트리거 매칭과 코드 식별자(파일명·localStorage key)에서만 유지하고 본문 설명에서는 사용하지 않는다.

HTML is a feedback collection form, not read-only. Doc edits happen only in Phase 5 after the user pastes.

## Args

```
/ma-make-decisions [issue-key]
/ma-make-decisions [issue-key] --no-open   # skip auto browser
```

- key: e.g. `{key}`. Omit → extract from recent `/ma-write` artifact.
- Default: open in browser via `open` (macOS).

## Precondition

At least one of:
- `{contextRoot}/{domain}/prd/{key}.md`
- `{contextRoot}/{domain}/design/{key}.md`
- `{contextRoot}/{domain}/plan/{key}-{project}.md`
- `{stateRoot}/{key}/review-plan.md`

If none → "/ma-write부터 실행하세요" + halt.

## Workflow

### Phase 1 — Source collection

Read PRD / design / per-project PLAN / review-plan in parallel. Tag each item `source: prd | design | plan | review`.
This skill is the implementation approval blocker resolver: run it after `/ma-review plan` if open decisions block approval.

Detail: `prompts/extract-rules.md` (Phase 1 section).

### Phase 2 — Normalize

Build per-item card objects (priority, owner, problem, why, check, tradeoff prose, risk, feedback placeholder).

**Fact or decision — filter before carding.** Every card spends the user's attention, so only decisions earn one:

- **Fact** — the answer already exists in the tracker, the repo, DB, logs, or docs. **Do not card it.** Look it up, resolve it, and report it under 해소됨 with the evidence. An item that reads as open only because nobody looked is legwork, not a decision.
- **Decision** — product policy, trade-off, priority, owner. Card it.

Detail: `prompts/extract-rules.md` (Phase 2 + priority/owner tables + hallucination guard).

### Phase 3 — Render HTML

Output: `{stateRoot}/{key}/check-decisions.html`.

Template (style guide, interaction contract, copy format, localStorage key): `templates/decisions-form.html`.

Required interactions
- localStorage autosave per issue key.
- Sticky action-bar: status counter + 초기화 + 모두 복사.
- 모두 복사 emits the payload defined in `prompts/apply-feedback.md` (skip empty entries).

Post-render check: 생성 직후 카드 수 == 추출 항목 수 검증, 불일치 시 재렌더.

### Phase 4 — Notice + auto-open

Auto-open unless `--no-open`. 기본은 macOS `open` 가정. 플랫폼별 fallback:
- macOS → `open {path}`
- Linux → `xdg-open {path}`
- Windows → `start "" {path}`
- 모두 실패하면 명령 실행 생략하고 path만 stdout으로 출력 (사용자가 수동 열기).

```
✓ {key} open-items report created
  path: {stateRoot}/{key}/check-decisions.html
  Critical {N} / High {N} / Medium {N}

Browser → write per-item opinion → click "모두 복사" → paste in this CLI →
  PRD/design/PLAN will be updated based on your feedback.
```

### Phase 5 — Apply pasted feedback

Parse the pasted payload, classify each block (decision / investigation / additional question), edit PRD/design/PLAN, emit change-log + per-section diff. Loop on remaining items.
If PLAN changes after plan review, re-run `/ma-review plan` before implementation approval.

파싱 실패 시: payload 포맷이 깨졌거나 빈 블록만 있으면 즉시 사용자에게 재포맷 요청. 예 — `붙여넣은 텍스트에서 카드 구분자/필드를 파싱하지 못했습니다. HTML의 "모두 복사" 버튼으로 다시 복사하거나, 빈 카드를 제외한 뒤 재전송 부탁드립니다.`

Detail: `prompts/apply-feedback.md`.

## References index

| File | When to read |
|---|---|
| [prompts/extract-rules.md](prompts/extract-rules.md) | Phase 1–2 — extraction, normalization, priority/owner tables, hallucination guard |
| [templates/decisions-form.html](templates/decisions-form.html) | Phase 3 — HTML form template + style/interaction contract + copy payload format |
| [prompts/apply-feedback.md](prompts/apply-feedback.md) | Phase 5 — pasted payload parsing + classification + post-apply rules |

## Output

- `{stateRoot}/{key}/check-decisions.html` — single HTML, overwrites prior runs.
- localStorage key per issue: `{key}-open-items-feedback` (no input loss across re-renders).
- Phase 5 edits PRD/design/PLAN in place; emits change-log summary. PLAN edits are valid only before handoff; after handoff worktree PLAN is SSOT.

## Resume

| Halt | State | Recovery |
|---|---|---|
| Phase 1 | source not collected | re-run |
| Phase 2 | mid-normalize | re-run (idempotent) |
| Phase 3 | mid-render | re-run (overwrite) |

Single HTML output → low recovery cost.

## Related skills

- `/ma-write` — PRD/design generation (source for this skill).
- `/ma-review` — plan review before impl / code review post-impl (this skill resolves plan-review blockers).
