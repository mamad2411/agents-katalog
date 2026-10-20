# /swyp-sync — 기능명세서 → GitHub Issues 동기화 (PM 전용)

@_wood/agents/pm/workflows/06-doc-sync/steps-c/step-01-read-drive.md
@_wood/agents/pm/workflows/06-doc-sync/steps-c/step-02-diff.md
@_wood/agents/pm/workflows/06-doc-sync/steps-c/step-03-create-issues.md
@_wood/agents/pm/workflows/06-doc-sync/steps-c/step-04-update-docs.md

---

## 이슈 생성 규칙

- **단위**: 화면(C열)당 1개 이슈
- **제목**: `[FE] {B열 ID} - {C열 화면명}` / `[BE] {B열 ID} - {C열 화면명}`
- **본문**: `issue-screen.template.md` 사용
  - D열(섹션) 기준 그룹핑
  - 각 항목: `` `{E열 기능ID}` **{G열 필드명}** — {H~M열 설명} ``
- **Label**: N열 → `프론트엔드` / `백엔드` + O열 → `순위:높음` / `순위:보통` / `순위:낮음`
- **Assignee**: N열 담당자 (team-roles.yaml 매핑)
- **우선순위 매핑**:
  | 명세 값 | GitHub Label |
  |--------|-------------|
  | 높음 / High | 순위:높음 |
  | 보통 / Medium | 순위:보통 |
  | 낮음 / Low | 순위:낮음 |

## 흐름

1. Google Sheets MCP로 시트22 읽기
2. 기존 이슈와 diff → 미생성 항목 표시
3. 확인 후 이슈 생성 (화면 단위)
4. sprint-status.yaml `spec_last_synced` 업데이트
