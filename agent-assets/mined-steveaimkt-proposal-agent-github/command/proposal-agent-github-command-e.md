---
description: proposal_script.md 편집 — 3뷰 분석 후 수정 (Step 3 재작업)
argument-hint: 테스트 XX
---

`output/$ARGUMENTS/proposal_script.md` 를 분석하고 편집합니다.
`script-editor` 스킬을 사용하세요.

## 전제

`output/$ARGUMENTS/proposal_script.md` 가 없으면 중단하고 안내:
"먼저 `/script $ARGUMENTS` 로 스크립트를 작성해주세요."

## 1. 3뷰 분석 제시

편집 전에 현재 스크립트를 세 가지 관점으로 보여줍니다.

| 뷰 | 내용 |
|----|------|
| **Overview** | Part별 슬라이드 수·비중, 프로젝트 유형 가중치 대비 편차 |
| **Strategy** | Win Theme 3개, Pain Point 대응 관계, KPI 산출근거 |
| **Slide List** | 슬라이드 번호 · Action Title · 패턴 · Win Theme 태그 |

## 2. 진단

`.claude/rules/step-checklists.md` Step 3 체크리스트(3-1~3-13)로 자가 진단하고
미달 항목을 먼저 제시합니다. 특히:

- Part별 비중이 프로젝트 유형 가중치와 맞는가 (3-2)
- Action Title이 Topic Title로 퇴화하지 않았는가 (3-6)
- Bridge가 5개 전환점에 다 있는가 (3-8)
- white 5장 연속이 없는가 (3-11)

## 3. 편집

사용자 지시를 받아 수정합니다. 수정 후:

- 영향 범위를 먼저 알립니다 (예: "Part 4를 줄이면 비중이 35%→28%가 됩니다")
- 수정한 슬라이드 번호를 명시합니다
- 체크리스트를 재검증합니다

## 4. 후속 안내

스크립트가 바뀌면 하위 산출물이 무효화됩니다.
`proposal_slides.json` · `preview.html` 이 이미 있으면 사용자에게 알리고
`/convert $ARGUMENTS` 재실행을 권합니다.
