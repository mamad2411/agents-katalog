---
description: 입찰 제안서 8-Step 실행 (HTML→Figma 기본, 스마트 시작)
argument-hint: 테스트 XX [--format pptx]
---

`제안요청서/$ARGUMENTS/` 를 분석한 후 제안서를 제작합니다.
`generate` 스킬로 **8-Step 파이프라인**을 **입찰 제안서** 모드로 실행하세요.

## 모드

- 유형: **입찰 제안서** 고정 (Step 0 유형 질문 생략)
- 출력: **HTML→Figma** 기본 / `--format pptx` 지정 시 PPTX 모드

## 스마트 시작

`.claude/rules/smart-start.md` 의 감지 순서를 따릅니다.
판정 결과를 **먼저 사용자에게 알린 뒤** 해당 Step부터 시작하세요.

## 진행 방식

각 Step 완료 후 `.claude/rules/step-checklists.md` 의 컨펌 포맷으로
체크리스트 + 결과 요약을 제시하고 사용자 컨펌 후 진행.
**Step 3(콘텐츠 기획)은 ★ 필수 승인** 단계입니다.

각 Step의 상세 절차는 `/start` 커맨드 정의를 따릅니다.
