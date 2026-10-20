---
name: phase
description: Phase 관리 명령어. Phase 상태 확인, 전환, 진행률 업데이트를 수행합니다. "phase", "단계", "진행", "progress" 키워드에 반응.
---

# Phase Management Command

프로젝트의 개발 Phase를 관리하는 명령어입니다.

## 사용법

```bash
# 현재 Phase 상태 확인
"phase status"
"/phase"

# 특정 Phase 상세 보기
"phase N 상세"
"phase-N tasks"

# Task 상태 업데이트
"phase update T{N}-01 complete"
"T{N}-03 완료"

# Phase 전환
"phase complete N"
"phase start N+1"

# 전체 요약
"phase summary"
```

## Phase 구조

```
docs/phases/
├── phase-1/     # [Phase 1 Name]
├── phase-2/     # [Phase 2 Name]
├── phase-3/     # [Phase 3 Name]
└── ...
```

## 문서 구조

각 Phase 폴더 내:
| 파일 | 용도 |
|------|------|
| SPEC.md | 기술 상세 설계 |
| TASKS.md | 작업 목록 및 상태 |
| CHECKLIST.md | 완료 조건 체크리스트 |

## 상태 표시

| 상태 | 아이콘 | 의미 |
|------|--------|------|
| Not Started | ⬜ | 시작 전 |
| In Progress | 🔄 | 진행 중 |
| Complete | ✅ | 완료 |
| Blocked | ⏸️ | 차단됨 |
| Planned | ⏳ | 계획됨 |

## 워크플로우

### 1. Phase 시작
```
1. SPEC.md 읽기 → 범위 확인
2. TASKS.md 읽기 → 작업 파악
3. 첫 번째 P0 task 시작
```

### 2. 개발 중
```
1. Task 완료 시 TASKS.md 업데이트
2. CHECKLIST.md 항목 체크
3. PROGRESS.md 자동 갱신
```

### 3. Phase 완료
```
1. 모든 TASKS 완료 확인
2. CHECKLIST 모든 항목 체크
3. 다음 Phase 활성화
```

## 연동

### phase-tracker agent
자동으로 phase-tracker 에이전트가 활성화되어 상태를 추적합니다.

### context-optimizer skill
현재 Phase 문서만 로드하여 토큰을 최적화합니다.

### phase-progress hook
Task 상태 변경 시 자동으로 PROGRESS.md를 업데이트합니다.

### doc-splitter agent
Phase 분할 시 문서 구조를 자동으로 생성합니다.
