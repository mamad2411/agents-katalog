---
name: workflow-package-strategy
description: 이미지 생성용 워크플로우 패키지를 등록, 수정, 조회하거나 params.json과 resolver.mjs의 책임을 나눌 때 사용한다.
allowed-tools: Read, Glob
---

# Workflow Package Strategy

## 절차
1. 현재 요청이 패키지 조회, 신규 등록, 기존 수정, resolver 설계 중 무엇인지 분류한다.
2. 가능하면 먼저 전역 `manage-workflows` 스킬과 `comfyui_workflow` 도구의 `list` 또는 `get`이 필요한지 판단한다.
3. 패키지 단위로 아래 항목을 정리한다.
   - 패키지 이름
   - 용도
   - 기준이 되는 기존 패키지
   - 새로 필요한 파라미터
   - params.json만으로 충분한지 여부
   - resolver.mjs가 필요하다면 왜 필요한지
4. 사용자가 새 워크플로우를 등록하려는 경우, `workflow.json`, `params.json`, `resolver.mjs`의 책임을 분리해 설명한다.
5. 마지막에 바로 실행할 다음 단계와, 어떤 도구 액션(list/get/save/delete)이 필요한지 명시한다.

## 판단 규칙
- 단순 node/field 매핑이면 params.json만 사용한다.
- 여러 노드를 동시에 수정하거나, 파라미터 값에 따라 분기해야 하거나, 고급 제어 파라미터가 필요할 때만 resolver.mjs를 쓴다.
- 기존 패키지를 약간만 바꿀 경우, 완전히 새 패키지보다 기존 패키지 수정이 나은지 먼저 검토한다.
- 패키지 비교 실험에서는 패키지명, 핵심 params, resolver 존재 여부를 함께 적는다.
- 고급 패키지를 설계할 때도 사용자가 실제로 유지보수 가능한 수준인지 고려한다.

## 출력 형식 권장
1. 현재 요청 분류
2. 추천 패키지 전략
3. params 설계안
4. resolver 필요 여부
5. 바로 수행할 액션