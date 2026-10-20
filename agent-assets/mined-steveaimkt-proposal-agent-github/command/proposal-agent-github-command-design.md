---
description: 디자인 레퍼런스 분석 + 도식화 전략 수립 (Step 4)
argument-hint: 테스트 XX
---

디자인 전략을 수립합니다. `design-analyzer` + `visualizer` 스킬을 사용하세요.

## 1. 전제 확인

`output/$ARGUMENTS/proposal_script.md` 가 없으면 중단:
"먼저 `/script $ARGUMENTS` 로 스크립트를 작성해주세요."

## 2. 레퍼런스 분석 → `design-analyzer`

`디자인 레퍼런스/` 폴더를 확인합니다.

- **파일 있으면**: PDF·JPG·PPTX 분석 → `output/$ARGUMENTS/design_analysis.md`
  - 컬러 팔레트 (픽셀 추출 권장 — 눈대중 금지)
  - 레이아웃 패턴 빈도순 3종+
  - 도식 스타일, 분위기 리듬
- **비어 있으면**: `.claude/rules/design-style.md` 의 기본 시스템 적용 후 그 사실을 명시

기존 분석본이 있으면 재사용합니다
(예: `디자인 레퍼런스/팀스파르타_AX리포트_장표분석.md`).

## 3. 도식화 전략 → `visualizer`

슬라이드별로 최적 도식을 배정해 `output/$ARGUMENTS/visualization_strategy.md` 작성.

패턴은 `.claude/skills/visualizer/references/diagram-patterns.md` **40종**에서 선택합니다.
임의 도식 생성 금지 — 라이브러리에 없으면 먼저 추가하고 쓰세요.

**명도 계단 규칙**: 단계·순서·강도가 있는 도식은 단일 색상 6단계 계단을 따릅니다.
회색 `--neutral-other` 는 "경쟁사·현행·미달" 전용입니다.

## 4. 체크리스트 검증 (4-1~4-8)

| 항목 | 심각도 |
|------|--------|
| (레퍼런스 있으면) `design_analysis.md` 생성 | MUST |
| `visualization_strategy.md` 생성 | MUST |
| 슬라이드 70%+ 에 권장 layout 지정 | MUST |
| 컬러 팔레트 Primary·Secondary 2색+ | SHOULD |
| 레이아웃 다양성 10종+ | SHOULD |
| `title_body` ≤ 30% | SHOULD |

컨펌 요청 후 `/convert $ARGUMENTS` 안내.
