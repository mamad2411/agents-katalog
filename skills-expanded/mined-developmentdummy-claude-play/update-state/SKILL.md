---
name: update-state
description: ComfyUI 연구 상태 변수와 실험 메타데이터를 현재 대화 흐름에 맞게 갱신한다.
allowed-tools: Read, Edit
---

# Update State

## 절차
1. 먼저 ./variables.json을 읽고 현재 값을 확인한다.
2. 이번 턴에서 실제로 변한 값만 최소 범위로 수정한다.
3. 수치형 변수는 범위를 벗어나지 않게 조정한다.
4. 문자열 변수는 사용자가 현재 진행 중인 작업과 정확히 맞게 유지한다.
5. 수정 후 JSON 문법이 유효한지 다시 확인한다.

## 이 페르소나의 변수 목록
- focus / focus_max
- stability / stability_max
- research_depth / research_depth_max
- workflow_complexity / workflow_complexity_max
- vram_pressure / vram_pressure_max
- dataset_readiness / dataset_readiness_max
- current_task
- active_model
- active_checkpoint
- active_lora
- quantization_target
- training_stage
- last_benchmark
- environment
- next_action
- open_issue

## 수치형 변수 규칙
- focus: 연구 목표가 선명해지고 작업 범위가 정리되면 +4~10, 논점이 분산되거나 요구가 충돌하면 -4~10.
- stability: 재현 가능한 설정 확보, 에러 해소, 기준선 고정 시 +5~15. OOM, 노드 충돌, 출력 붕괴, 재현 실패 시 -8~18.
- research_depth: 비교 실험, 아키텍처 분석, 병목 추론, 로그 검토가 깊어질수록 +5~12.
- workflow_complexity: 새 분기, 제어 모듈, 후처리 체인, 멀티모델 조합이 추가되면 +4~12. 구조 단순화 시 -4~10.
- vram_pressure: 큰 모델, 고해상도, 배치 증가, 다중 로더, 무거운 후처리 추가 시 +5~15. 양자화, 해상도 조정, 구조 경량화 시 -5~12.
- dataset_readiness: 데이터 수집, 정제, 캡션 정리, 검증 세트 분리, 품질 기준 확정 시 +6~15. 데이터셋 결함이 드러나면 -4~10.
- 모든 게이지형 변수는 0 이상 각 *_max 이하로 유지한다.
- *_max 값은 특별한 이유가 없는 한 유지한다.

## 문자열 변수 규칙
- current_task: 이번 세션의 가장 우선순위 높은 연구 작업으로 유지한다.
- active_model: 현재 논의나 테스트의 중심이 되는 모델명으로 갱신한다.
- active_checkpoint: 실제 사용 중이거나 비교 기준이 되는 체크포인트명으로 갱신한다.
- active_lora: 사용 중인 LoRA가 없으면 "없음"으로 둔다.
- quantization_target: 양자화 탐색 대상 모델이나 상태를 기록한다.
- training_stage: 예: 대기, 데이터셋 정리, 캡션 정제, 학습 중, 검증 중, 재학습 검토.
- last_benchmark: 최근 비교 결과를 짧게 기록한다. 예: "Z-Image FP16 1024px 6.2s / Q8 4.1s, 품질 저하 경미".
- environment: 작업 중인 환경이나 하드웨어 맥락이 명확해지면 반영한다.
- next_action: 바로 다음에 수행할 가장 구체적인 행동 한 줄.
- open_issue: 아직 해결되지 않은 가장 중요한 문제 한 줄.

## 추가 규칙
- 사용자가 추측만 말했을 뿐 확정하지 않은 정보는 변수에 단정적으로 적지 않는다.
- 여러 값이 동시에 변해도 실제 대화에서 근거가 생긴 것만 수정한다.
- 값이 불명확하면 기존 값을 유지하고 memory.md에 확인 필요 사항으로 남기는 쪽을 우선한다.