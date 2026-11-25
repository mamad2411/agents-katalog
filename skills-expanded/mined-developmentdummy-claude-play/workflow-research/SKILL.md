---
name: workflow-research
description: 새 ComfyUI 워크플로우를 설계하거나 신규 모델, 양자화 모델, LoRA 개발 전략을 비교할 때 분석 틀을 잡는다.
allowed-tools: Read, Glob
---

# Workflow Research

## 절차
1. ./persona.md, ./worldview.md, ./variables.json, ./memory.md를 읽고 현재 연구 맥락을 파악한다.
2. 사용자의 요청을 다음 중 하나 이상으로 분류한다: 워크플로우 설계 / 신규 모델 테스트 / 양자화 탐색 / LoRA 훈련 개발 / 워크플로우 패키지 설계.
3. 각 분류에 대해 아래 5가지를 정리한다.
   - 목표
   - 제약 조건
   - 기준선
   - 비교 변수
   - 성공 판정 기준
4. ComfyUI 관점에서 노드 흐름 또는 실험 단계 순서를 제안한다.
5. package-first 방식이 필요한 경우, 아래 3가지를 추가로 정리한다.
   - 어떤 패키지 이름으로 분리할지
   - `params.json`만으로 충분한지, `resolver.mjs`가 필요한지
   - `comfyui_workflow`의 `list/get/save` 중 어떤 액션이 필요한지
6. 마지막에 가장 비용이 낮은 다음 실험 1개와, 가장 정보량이 큰 실험 1개를 분리해 제안한다.

## 세부 규칙
- 새 워크플로우 설계 시에는 입력 노드, 핵심 생성 구간, 제어/후처리 구간, 저장/검증 구간으로 나눠 설명한다.
- 패키지로 관리할 워크플로우라면 `workflow.json`, `params.json`, `resolver.mjs`의 역할을 분리해서 제안한다.
- 단순 node/field 매핑이면 resolver를 만들지 않는 쪽을 우선한다.
- 신규 모델 테스트 시에는 동일 프롬프트, 해상도, sampler, steps, seed를 가능한 한 고정한 기준선 비교를 우선한다.
- 양자화 탐색 시에는 속도, VRAM, 품질 저하, 호환성 리스크를 함께 본다.
- LoRA 개발 시에는 데이터셋 준비 상태, 캡션 규칙, 검증 샘플, 과적합 감시 포인트를 먼저 점검한다.
- 모르는 부분은 단정하지 말고 "확인 필요"로 두되, 무엇을 확인해야 하는지는 구체적으로 제시한다.