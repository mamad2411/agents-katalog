---
name: dev-doc-planner
description: 개발 문서 프롬프트 작성 도우미. PRD, 기술 설계서, 진행상황 체크 문서 작성 시 사용. "문서 작성", "PRD", "설계서", "진행상황", "개발 계획" 키워드에 반응.
---

# 개발 문서 플래너 (Dev Doc Planner)

개발 프로젝트의 문서화를 체계적으로 지원하는 스킬입니다.

## 문서 저장 규칙

- **위치**: `{project_root}/docs/`
- **형식**: Markdown (.md)
- **네이밍**: kebab-case (예: `user-authentication-prd.md`)

## 문서 유형별 가이드

### 1. PRD (Product Requirements Document)

**용도**: 제품 요구사항 정의
**템플릿**: [PRD-TEMPLATE.md](dev-doc-planner/PRD-TEMPLATE.md)
**권장 길이**: 섹션당 1,500-2,000자

```
docs/
├── prd/
│   ├── {feature-name}-prd.md
│   └── ...
```

### 2. 기술 설계서 (Technical Specification)

**용도**: 구현 상세 설계
**템플릿**: [TECH-SPEC-TEMPLATE.md](dev-doc-planner/TECH-SPEC-TEMPLATE.md)
**권장 길이**: 섹션당 2,000-2,500자

```
docs/
├── tech-specs/
│   ├── {feature-name}-spec.md
│   └── ...
```

### 3. 진행상황 체크 (Progress Tracking)

**용도**: 개발 진척 관리
**템플릿**: [PROGRESS-TEMPLATE.md](dev-doc-planner/PROGRESS-TEMPLATE.md)
**권장 길이**: 800-1,200자

```
docs/
├── progress/
│   ├── {feature-name}-progress.md
│   └── ...
```

## 개발 생명주기 매핑

| Phase | 문서 | 서브에이전트 |
|-------|------|-------------|
| 기획 | PRD 작성 | prd-writer |
| 설계 | 기술 설계서 | tech-spec-writer |
| 개발 | 진행상황 체크 | progress-tracker |
| 검증 | 문서 완성도 | doc-validator |
| 테스트 | 테스트 케이스 | progress-tracker |
| 배포 | 배포 체크리스트 | doc-validator |

## 토큰 최적화 규칙

1. **섹션 분리**: 하나의 문서에 3,000자 이상 작성 금지
2. **참조 링크**: 상세 내용은 별도 파일로 분리 후 링크
3. **코드 블록**: 핵심 코드만 포함, 전체 코드는 파일 경로로 참조

## 빠른 시작

```bash
# PRD 작성 시작
"user-authentication 기능의 PRD를 작성해줘"

# 기술 설계서 작성
"user-authentication의 기술 설계서를 작성해줘"

# 진행상황 체크
"user-authentication 개발 진행상황을 업데이트해줘"

# 문서 검증
"user-authentication 문서들의 완성도를 검증해줘"
```

## 관련 서브에이전트

- **prd-writer**: PRD 문서 작성 전문
- **tech-spec-writer**: 기술 설계서 작성 전문
- **progress-tracker**: 진행상황 추적 및 업데이트
- **doc-validator**: 문서 완성도 검증
- **doc-splitter**: 대용량 문서 분할 및 Phase 관리
- **dev-docs-writer**: 프로젝트 개시 시 개발 문서 자동 생성

## 개발 Phase 분할 전략

### doc-splitter 연동 규칙

대규모 개발 프로젝트의 경우 상세 코드 작성 효율성을 위해 Phase 단위로 문서를 분할합니다.

**분할 기준**:
```yaml
Phase 분할 조건:
  - 기능 복잡도: HIGH (3개 이상 모듈 연동)
  - 예상 코드량: >1,000 lines
  - 개발 기간: >1 week
  - 의존성 복잡도: 3개 이상 외부 의존성
```

**분할 구조**:
```
docs/
├── PRD.md                    # 전체 요구사항 (개요)
├── TECH-SPEC.md              # 전체 기술 설계 (개요)
├── PROGRESS.md               # 전체 진행 현황
├── CONTEXT.md                # 컨텍스트 최적화용
└── phases/                   # Phase별 상세 문서
    ├── phase-1/
    │   ├── SPEC.md           # Phase 1 상세 설계
    │   ├── TASKS.md          # Phase 1 작업 목록
    │   └── CHECKLIST.md      # Phase 1 완료 체크리스트
    ├── phase-2/
    │   ├── SPEC.md
    │   ├── TASKS.md
    │   └── CHECKLIST.md
    └── ...
```

### Phase 문서 템플릿

**phases/phase-N/SPEC.md**:
```markdown
# Phase N: [Phase Name]

**Status**: [Planned | In Progress | Complete]
**Dependencies**: Phase N-1
**Target**: [Description]

## Scope
- [Feature 1]
- [Feature 2]

## Technical Details
[상세 구현 사항]

## Files to Create/Modify
| File | Action | Description |
|------|--------|-------------|

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
```

### 자동 분할 워크플로우

```bash
# 프로젝트 개시 시
"새 프로젝트 시작: [프로젝트명]"
↓
dev-docs-writer 활성화 → 기본 문서 생성
↓
doc-splitter 활성화 (복잡도 HIGH 시)
↓
Phase별 문서 자동 분할
↓
context-optimizer 연동 → 토큰 효율화

# Phase 작업 시
"Phase 2 개발 시작"
↓
docs/phases/phase-2/SPEC.md 로드
↓
TASKS.md 기반 작업 수행
↓
CHECKLIST.md 업데이트
↓
PROGRESS.md 자동 반영
```

### 컨텍스트 최적화 연동

Phase 분할은 `context-optimizer` skill과 연동되어 토큰 효율성을 극대화합니다:

```yaml
Context Loading 전략:
  Quick (2K tokens):
    - CONTEXT.md
    - Current phase SPEC.md

  Standard (10K tokens):
    - CONTEXT.md + PROGRESS.md
    - Current phase 전체 문서
    - 이전 phase CHECKLIST.md

  Full (30K+ tokens):
    - 모든 문서
    - 소스 코드 포함
```
