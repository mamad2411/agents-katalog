---
tags: [backend, dry, run, confirm, retry, write]
name: dry-run-confirm-retry-write-flow
description: "[Backend] 트래커/외부 API 쓰기 작업에 적용하는 공통 플로우: 미리보기 → 사용자 확인 → 쓰기 → 재시도."
argument-hint: <context>
version: 1.0.0
source_project: nkia-skills
category: backend
---

# dry-run-confirm-retry-write-flow

외부 트래커(PIMS/Jira/Redmine 등)나 외부 API에 **데이터를 쓰는 스킬**이라면 반드시 이 플로우를 적용합니다.

## Usage

스킬 Instructions의 write 단계에 아래 절차를 포함시킵니다.

## Description

스킬이 사용자에게 보이지 않는 부작용(시간 기록, 상태 변경, 제출 등)을 만들 때 실수·중복·네트워크 오류로부터 방어하는 공통 패턴. `--dry-run` 플래그와 상호작용합니다.

## Instructions

### Step 1: 대상 조회 + 중복 감지
쓰기 직전 현재 상태를 읽어 중복/충돌이 있는지 경고.
- 동일 키 + 동일 값 → 🔴 강한 경고.
- 다른 값 → 추가/갱신 의도 확인.

### Step 2: Dry-run 미리보기
변경될 내용(필드별 before/after)을 **표 형태**로 출력.

### Step 3: `--dry-run` 플래그 분기
- 플래그 존재 → 미리보기만 출력 후 **즉시 종료**. API 쓰기 호출 절대 없음.
- 없음 → 다음 단계.

### Step 4: 명시적 사용자 확인
`"진행할까요?"` 프롬프트. 사용자가 명시적으로 승인해야 Step 5로 진행.

### Step 5: 쓰기 실행 + Retry-with-Confirmation
- 네트워크/타임아웃 → "재시도할까요?" (최대 2회).
- 권한 오류 → 즉시 중단 + 수동 처리 안내.
- 데이터 오류 → 입력 수정 제안 후 중단.
- 기타 → 원본 에러 + 가이드.

### Step 6: 결과 요약
변경된 항목 before/after + 누적값.

## Notes
- 쓰기 후 복구가 어려운 작업(예: 제출/삭제)은 확인 단계를 2회 걸 것.
- **삭제 동작은 이 플로우로 지원하지 않음** — 별도 스킬로 분리.
- 모든 단계에서 사용자 언어로 출력.
