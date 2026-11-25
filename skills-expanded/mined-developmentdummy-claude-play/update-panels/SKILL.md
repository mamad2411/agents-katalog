---
name: update-panels
description: 라티스의 연구용 패널 구조나 디자인이 바뀌어야 할 때 panels 디렉토리의 HTML 템플릿을 수정한다.
allowed-tools: Read, Write, Edit, Glob
---

# Update Panels

## 절차
1. 먼저 ./panel-spec.md를 읽어 패널 기술 명세와 사용 가능한 Handlebars 헬퍼를 확인한다.
2. /frontend-design 스킬이 사용 가능한 환경이면 우선 활용하고, 없으면 panel-spec.md와 기존 패널 스타일을 기준으로 직접 고품질 UI를 유지한다.
3. ./variables.json을 읽고 실제 변수명과 타입을 확인한다.
4. 필요한 패널 파일만 수정하고, 구조 변경이 없으면 전체를 갈아엎지 않는다.
5. 수정 후 스타일, 변수 참조, 조건문, 게이지 계산이 유효한지 점검한다.

## 이 페르소나의 패널 파일
- ./panels/01-status.html
  - 역할: 연구 상태, 현재 작업, 핵심 게이지, 활성 모델/체크포인트/LoRA/양자화 타깃 표시
  - 사용 변수: focus, stability, research_depth, workflow_complexity, vram_pressure, current_task, next_action, environment, active_model, active_checkpoint, active_lora, quantization_target
- ./panels/02-lab-board.html
  - 역할: 최근 벤치마크, 열린 이슈, 다음 액션, 훈련 단계, 실험 메타정보 표시
  - 사용 변수: last_benchmark, open_issue, next_action, training_stage, active_model, quantization_target, active_checkpoint, environment, stability
- ./panels/03-training-track.html
  - 역할: LoRA 훈련 진행, 데이터셋 준비도, 현재 작업, 활성 LoRA 표시
  - 사용 변수: dataset_readiness, dataset_readiness_max, training_stage, active_lora, current_task

## 규칙
- Shadow DOM 안에서 렌더링된다는 점을 전제로 각 파일 상단에 반드시 <style> 태그를 포함한다.
- 기본 톤은 다크 테마 기반으로 유지하고, layout.json의 청록/보라 계열 분위기와 충돌하지 않게 한다.
- variables.json에 없는 값을 하드코딩 변수처럼 참조하지 않는다.
- 게이지는 percentage 헬퍼와 *_max 짝을 사용한다.
- 비교 로직이 필요하면 eq, ne, lt, lte, gt, gte, and, or, not 헬퍼를 사용한다.
- 패널 이름과 역할은 연구 보조 도구답게 유지하고, 장식성보다 가독성과 빠른 상황 파악을 우선한다.
- 인터랙티브 패널을 추가할 경우 runTool 결과 구조를 추측하지 말고 관련 엔진 코드를 먼저 읽는다.