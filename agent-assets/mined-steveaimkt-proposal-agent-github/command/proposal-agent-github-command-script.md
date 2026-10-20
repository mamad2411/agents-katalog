---
description: SPARK-6 콘텐츠 기획 단독 실행 (Step 3, ★필수 승인)
argument-hint: 테스트 XX
---

제안서 스크립트를 작성합니다. `script` 스킬을 사용하세요.

## 1. 전제 확인

| 파일 | 없을 때 |
|------|--------|
| `rfp_analysis.md` / `mkt_analysis.md` | 중단 — "`/analyze $ARGUMENTS` 먼저 실행" |
| `research_brief.md` | 경고 후 진행 — Evidence에 쓸 출처 데이터가 없어 품질이 크게 떨어집니다. `/research $ARGUMENTS` 를 권합니다 |
| `campaign_brief.md` | 캠페인 모드 — 위 둘 없이도 진행 가능 |

## 2. 작성

`.claude/rules/spark6-framework.md` 의 **프로젝트 유형별 가중치**를 적용해
Part별 슬라이드 수를 먼저 배분한 뒤 작성합니다.

필수 요소:

- **Win Theme 3개** — Pain Point에 1:1 대응, 모든 슬라이드에 태깅
- **Action Title** — Topic Title 금지, 인사이트+데이터 기반 15~35자
- **S-E-P** — 모든 콘텐츠 슬라이드에 Story / Evidence / Promise
- **Evidence 출처** — `research_brief.md` 데이터 우선, 출처 없으면 사용 금지
- **Bridge** — Part 전환점 5곳 전부
- **KPI 산출근거** — 계산식 + 데이터 출처
- **Part 3 필수 장표** — Concept Reveal + Strategy Framework

## 3. 출력

`output/$ARGUMENTS/proposal_script.md`

## 4. ★ 필수 승인

체크리스트 3-1~3-13 자가 검증 후, 아래를 제시하고 **반드시 승인을 받습니다.**

- 목차 (Part별 슬라이드 수 + 비중 % + 유형 가중치 대비 편차)
- Win Theme 3개 → Pain Point 대응 관계
- 총 슬라이드 수 (40~80장 권장)
- KPI 요약 + 산출근거
- 패턴 다양성 (10종+) / 분위기 리듬 (white 5장 연속 없음)

승인 전까지 다음 Step으로 넘어가지 마세요.
수정 요청 시 반영 후 재확인합니다. 이후 편집은 `/e $ARGUMENTS`.
