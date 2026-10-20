---
description: RFP·마케팅 플랜 분석 단독 실행 (Step 1)
argument-hint: 테스트 XX
---

`제안요청서/$ARGUMENTS/` 를 분석합니다. `analyst` 스킬을 사용하세요.

## 1. 입력 확인

`제안요청서/$ARGUMENTS/` 파일 목록을 제시합니다.
비어 있으면 중단하고, 사용자에게 파일 배치를 요청하거나 구두 브리핑을 받습니다.

## 2. 유형 판정

- PDF에 "제안요청서 / 과업지시서 / 입찰공고" → **입찰 제안서**
- 마케팅 플랜 / 브리핑 → **마케팅 제안서**
- 애매하면 AskUserQuestion으로 질문

## 3. 분석

추출 항목 (체크리스트 1-1~1-9):

| 항목 | 심각도 |
|------|--------|
| 프로젝트명 | MUST |
| 발주처/클라이언트 | MUST |
| 과업 범위 (완전성) | MUST |
| (입찰) 평가 기준 배점표 | MUST |
| (마케팅) 마케팅 목표 + 타겟 | MUST |
| **Pain Point 3개 — 근거 기반** | MUST |
| 프로젝트 유형 5종 판별 | MUST |
| 예산 | SHOULD |
| 일정 | SHOULD |

**프로젝트 유형**은 SPARK-6 Part 가중치를 결정하므로 반드시 판별합니다
(Marketing/PR · Event · IT/System · Public · Consulting — `.claude/rules/spark6-framework.md`).

Pain Point는 **RFP 원문 근거**를 함께 인용합니다. 추측 금지.

## 4. 출력

- 입찰: `output/$ARGUMENTS/rfp_analysis.md`
- 마케팅: `output/$ARGUMENTS/mkt_analysis.md`

체크리스트 판정 후 컨펌 요청. 다음 단계로 `/research $ARGUMENTS` 안내.
