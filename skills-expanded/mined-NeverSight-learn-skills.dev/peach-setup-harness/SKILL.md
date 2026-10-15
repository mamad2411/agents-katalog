---
name: peach-setup-harness
description: |
  대상 프로젝트에 피치 하네스 시스템을 설정합니다. CLAUDE.md를 최소 진입점으로 정리하고, AGENTS.md를 70~90줄 규모로 생성/업데이트합니다.
  Use when: "하네스 설정", "프로젝트 초기 설정", "CLAUDE.md 정리", "AGENTS.md 업데이트", "세션 시작 설정" 키워드.
model: opus
---

# peach-setup-harness — 하네스 시스템 설정

대상 프로젝트의 CLAUDE.md와 AGENTS.md를 하네스 시스템에 맞게 설정한다.
CLAUDE.md는 20줄 이내 최소 진입점, AGENTS.md는 70~90줄 핵심 규칙.

## 페르소나

하네스 시스템 설정 전문가.
CLAUDE.md에서 AGENTS.md와 중복되는 내용을 제거하고, AGENTS.md 5개 섹션을 점검하여 누락 시 보완한다.
cursor rules는 삭제한다.

---

## 전제조건

- **대상 프로젝트 루트**에서 실행 (peach-harness 자체가 아닌 대상 프로젝트)
- peach-harness 스킬이 설치되어 있어야 함

---

## Workflow

### Step 1: 현재 상태 분석

다음을 확인한다:

```bash
# CLAUDE.md 존재 여부 + 내용
cat CLAUDE.md 2>/dev/null || echo "CLAUDE.md 없음"

# AGENTS.md 존재 여부 + 내용
cat AGENTS.md 2>/dev/null || echo "AGENTS.md 없음"

# 프로젝트 구조 감지
ls -d api/ front/ 2>/dev/null || echo "모노레포 아님"

# Controller 프레임워크 감지 (Koa vs Elysia)
head -3 api/src/modules/test-data/controller/test-data.controller.ts 2>/dev/null || echo "controller 없음"

# DAO 라이브러리 감지 (bunqldb vs sql-template-strings)
head -5 api/src/modules/test-data/dao/test-data.dao.ts 2>/dev/null || echo "dao 없음"

# DB 종류 감지
grep -i "host\|database\|mysql\|postgres" api/env.local.yml 2>/dev/null | head -5 || echo "env.local.yml 없음"

# cursor rules 존재 여부
ls api/.cursor/rules/ 2>/dev/null && echo "api cursor rules 존재" || echo "api cursor rules 없음"
ls front/.cursor/rules/ 2>/dev/null && echo "front cursor rules 존재" || echo "front cursor rules 없음"
ls .cursor/rules/ 2>/dev/null && echo "root cursor rules 존재" || echo "root cursor rules 없음"
ls .cursorrules 2>/dev/null && echo ".cursorrules 존재" || echo ".cursorrules 없음"
```

분석 결과를 정리:
- CLAUDE.md: 존재 여부, 현재 줄 수, AGENTS.md와 중복되는 섹션 목록
- AGENTS.md: 존재 여부, 5개 섹션 존재 여부
- 프로젝트 유형: `api/ + front/` 모노레포 / 단독 `api/` / 단독 `front/`
- Controller 프레임워크: Koa (routing-controllers) 또는 Elysia (api/ 없으면 해당 없음)
- DB 종류: MySQL 또는 PostgreSQL (api/ 없으면 해당 없음)
- cursor rules: 존재 여부 및 파일 목록

### Step 2: AGENTS.md 5개 섹션 점검

AGENTS.md가 존재하는 경우, 아래 5개 섹션이 있는지 확인한다:

```bash
grep -l "공통 원칙\|_common.*import" AGENTS.md 2>/dev/null && echo "§1.공통원칙 존재" || echo "§1.공통원칙 누락"
grep -l "백엔드 규칙\|ErrorHandler" AGENTS.md 2>/dev/null && echo "§2.백엔드 존재" || echo "§2.백엔드 누락"
grep -l "프론트엔드 규칙\|computed" AGENTS.md 2>/dev/null && echo "§3.프론트엔드 존재" || echo "§3.프론트엔드 누락"
grep -l "테스트\|TDD" AGENTS.md 2>/dev/null && echo "§4.테스트 존재" || echo "§4.테스트 누락"
grep -l "Bounded Autonomy\|Must Follow" AGENTS.md 2>/dev/null && echo "§5.BA 존재" || echo "§5.BA 누락"
```

누락 섹션 발견 시 아래 references를 소스로 사용한다:

| 섹션 | 소스 파일 |
|------|---------|
| 1. 공통 원칙 | `peach-setup-harness/references/01-common.md` |
| 2. 백엔드 규칙 (Koa) | `peach-setup-harness/references/02-backend-koa.md` |
| 2. 백엔드 규칙 (Elysia) | `peach-setup-harness/references/02-backend-elysia.md` |
| 3. 프론트엔드 규칙 | `peach-setup-harness/references/03-frontend.md` |
| 4. 테스트 및 품질 | `peach-setup-harness/references/04-testing.md` |
| 5. Bounded Autonomy | `peach-setup-harness/references/05-bounded-autonomy.md` |

**Koa/Elysia 분기:** 02번 파일 선택만으로 처리
- Koa → `01 + 02-backend-koa + 03 + 04 + 05`
- Elysia → `01 + 02-backend-elysia + 03 + 04 + 05`

Elysia 감지 시 추가 확인:
```bash
grep -l "Plugin System\|try-catch 금지" AGENTS.md 2>/dev/null && echo "Elysia 규칙 존재" || echo "Elysia 규칙 누락"
```

누락 섹션 목록을 기록한다.

### Step 3: 변경 계획 생성

사용자에게 변경 계획을 제시한다:

**CLAUDE.md 변경:**
- 제거할 중복 섹션 (AGENTS.md에 이미 있는 내용)
- 최종 예상 줄 수

**AGENTS.md 변경:**
- 누락된 섹션 목록 + 추가할 내용 요약
- 전체 5개 섹션 구성 확인

**cursor rules 삭제 (존재하는 경우):**
- 삭제 대상 파일/디렉토리 목록
- 삭제 사유: "기본 지침(AGENTS.md) + 스킬 베이스로 작업 진행. cursor rules는 더 이상 사용하지 않음"

### Step 4: 사용자 확인

변경 계획에 대해 사용자 동의를 받는다. 수정 요청이 있으면 반영한다.

### Step 5: 적용

승인 후 변경을 적용한다:

1. **CLAUDE.md 정리**
   - AGENTS.md와 중복되는 섹션 제거
   - 프로젝트별 고유 지침은 보존 (Electron IPC, 특수 설정 등)
   - 20줄 이내 유지

2. **AGENTS.md 생성 또는 업데이트**
   - 섹션별 references를 조합하여 5개 섹션 구성
   - Koa/Elysia 분기는 02번 파일 선택만으로 처리
   - AGENTS.md 없음 → 5개 references 조합하여 전체 생성
   - AGENTS.md 있음 → 누락/불일치 섹션만 references에서 추출하여 추가/수정

3. **cursor rules 삭제** (존재하는 경우)
   - `api/.cursor/rules/` 디렉토리 삭제
   - `front/.cursor/rules/` 디렉토리 삭제
   - 루트 `.cursor/rules/` 디렉토리 삭제
   - 루트 `.cursorrules` 파일 삭제

### Step 6: 완료 확인

적용 결과를 출력한다:
- CLAUDE.md 변경 전/후 줄 수
- AGENTS.md 추가/업데이트된 섹션 목록
- 삭제된 cursor rules 파일 목록

---

## AGENTS.md 최소화 원칙

AGENTS.md를 새로 생성하거나 보완할 때 아래 원칙을 적용한다.

**핵심:** "가이드 코드가 말 못하는 것만 남긴다."
스킬 미사용 케이스를 별도로 고려하지 않는다.

**유지 (4가지 카테고리):**

| 카테고리 | 내용 |
|---------|------|
| 금지사항 | `_common`만 import, FK 금지, 옵셔널/null/undefined 금지, try-catch 금지(Elysia), isLoading 금지 |
| 설계 철학 | 에러 처리(200+success:false / ErrorHandler), 완전 독립 도메인, TDD/실DB/모킹 금지 |
| 컨벤션 | 네이밍 4종(snake_case/kebab-case/PascalCase/camelCase), PK `seq` 접미사, 감사 칼럼, DB Boolean CHAR(1) |
| 포인터 | 가이드 코드 경로, 품질 검증 명령어, DB 마이그레이션 명령어 |

**제거:**
- 가이드 코드에서 추론 가능한 내용 → 가이드 코드 포인터로 대체
- 린터(Biome/ESLint)가 잡을 수 있는 규칙
- 코드 예시 → `파일 경로 참조` 1줄로 대체

**목표 크기:** 70~90줄

---

## CLAUDE.md 표준 템플릿

대상 프로젝트의 CLAUDE.md를 아래 형식으로 정리한다.
프로젝트별 고유 지침은 별도 섹션으로 보존한다.

```markdown
# {프로젝트명}

{한 줄 설명}

## 규칙 참조

모든 개발 규칙은 @AGENTS.md 를 참조하라.

## 세션 시작

`git status && git branch`로 현재 상태를 확인하세요.

## 가이드 코드

코드 생성 = **가이드 코드 참조** → 도메인 분석 → Bounded Autonomy 범위 내 적응
- Backend: `api/src/modules/test-data/`
- Frontend: `front/src/modules/test-data/`
```

### 핵심 원칙

- CLAUDE.md는 **20줄 이내** 유지
- AGENTS.md와 중복되는 섹션은 제거 ("Claude 특화 지침", "코딩 규칙" 등)
- 프로젝트별 고유 지침(Electron IPC, 특수 환경변수 등)은 별도 섹션으로 보존
- "가이드 코드" 섹션:
  - 모노레포(api/+front/): `Backend: api/src/modules/test-data/` + `Frontend: front/src/modules/test-data/`
  - 단독 front/: `Frontend: front/src/modules/test-data/`

---

## 완료 조건 체크리스트

기본:
- [ ] CLAUDE.md가 20줄 이내로 정리됨
- [ ] CLAUDE.md에서 AGENTS.md 중복 내용이 제거됨
- [ ] AGENTS.md가 5개 섹션(공통, 백엔드, 프론트엔드, 테스트, BA)으로 구성됨
- [ ] AGENTS.md가 70~90줄 범위
- [ ] 프로젝트별 고유 지침이 보존됨

추가:
- [ ] Elysia 프로젝트인 경우 Elysia 전용 항목이 포함됨
- [ ] 기술 스택이 정확히 반영됨
- [ ] references 구조가 올바름 (01, 02-koa/02-elysia, 03, 04, 05)
- [ ] cursor rules 삭제됨 (존재했던 경우)
- [ ] 프로젝트 환경(Koa/Elysia, DB종류)에 맞는 내용으로 작성됨
