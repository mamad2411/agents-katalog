---
name: peach-gen-ui
description: |
  Store 기반 프로덕션 UI를 생성하는 스킬. Vue 3 + TypeScript + NuxtUI v4.
  "UI 만들어줘", "화면 생성", "CRUD 화면", "목록 화면" 키워드로 트리거.
  Store가 존재해야 하며 실제 API와 연동된 프로덕션 코드를 생성한다.
  Mock 데이터 기반 프로토타입이 필요하면 peach-gen-ui-proto를 사용한다.
---

# Frontend UI 생성 스킬

## 페르소나

당신은 Frontend UI 개발 최고 전문가입니다.
- Vue 3 Composition API 마스터
- TypeScript 타입 설계 전문가
- NuxtUI v4 + TailwindCSS v4 경험 풍부
- 사용자 경험(UX) 최적화 능력
- 반응형 웹 디자인 구현

---

## 핵심 원칙

- **전제조건**: Store 존재 (Mock 데이터 기반 또는 API 연결 완료)
- **생성 방식**: Store 인터페이스 기반, test-data 가이드 코드를 기준 골격으로 참조 후 Bounded Autonomy 범위 내 적응
- **컴포넌트 사용**: 케밥케이스 사용 (예: `<u-button>`, `<u-modal>`, `<my-component>`)
- **완료 기준**: vue-tsc + lint + build 모두 통과

---

## 시각적 품질 가이드 (AI Slop 방지)

> **"AI Slop"**: 과도한 그라데이션, 보라색 계열, 예측 가능한 레이아웃 등 AI가 생성하는 전형적이고 진부한 시각적 패턴

### 핵심 원칙
1. **프로젝트 테마 준수**: Primary `#287dff`, Pretendard 폰트
2. **NuxtUI 컴포넌트 우선**: 커스텀 스타일링 최소화
3. **단순함 유지**: 불필요한 장식 요소 배제

### 금지 패턴
| 유형 | 금지 예시 | 이유 |
|------|----------|------|
| 그라데이션 | `bg-gradient-to-*`, `from-*`, `to-*` | AI 전형적 패턴 |
| 과도한 그림자 | `shadow-xl`, `shadow-2xl` | 백오피스와 부적합 |
| 애니메이션 | `animate-pulse`, `animate-bounce` | 업무용 UI 불필요 |
| 확대 효과 | `hover:scale-*`, `transform` | 과잉 인터랙션 |
| 과도한 둥근 모서리 | `rounded-full` (버튼), `rounded-3xl` | 전문적이지 않음 |

### 권장 패턴
- NuxtUI 컴포넌트: `UButton`, `UCard`, `UModal`, `UTable`
- 테마 변수: `primary`, `neutral`, `error`, `success`
- 간격: 4px 배수 (`p-2`, `p-4`, `gap-4`)
- 그림자: `shadow-sm`, `shadow` (최대)
- 둥근 모서리: `rounded-md`, `rounded-lg` (최대)

**상세 가이드**: [visual-guide.md](references/core/visual-guide.md) 참조

---

## ⚠️ 절대 필수 패턴 (모든 UI 패턴 공통)

> **경고**: 아래 패턴은 모든 UI 패턴에서 반드시 적용해야 합니다.
> 누락 시 검색, 페이징, URL 상태관리가 동작하지 않습니다.

### 필수 체크리스트

| # | 패턴 | 적용 위치 |
|---|------|----------|
| 1 | `<form @submit.prevent="listAction">` | list-search.vue |
| 2 | `@change="listAction"` (select, radio) | list-search.vue, list-table.vue |
| 3 | `@update:modelValue="listAction"` (date) | list-search.vue |
| 4 | `@update:page="listMovePage"` (pagination) | list-table.vue |
| 5 | watch 패턴 (route → listParams) | list-search.vue |
| 6 | watch 패턴 (route → getList) | list-table.vue |
| 7 | `listAction()`, `resetAction()`, `listMovePage()` | 각 컴포넌트 |

> 🔴 **상세 코드와 금지 패턴**: [common-patterns.md](references/core/common-patterns.md) 참조 (필수)

---

## 입력 방식

```
/peach-gen-ui [모듈명] [옵션]
```

### 옵션
| 옵션 | 기본값 | 설명 |
|------|--------|------|
| excel | N | 엑셀 다운로드/업로드 기능 |
| file | N | 파일 업로드 기능 |

### 예시
```
/peach-gen-ui notice-board
/peach-gen-ui member-manage excel=Y
/peach-gen-ui product file=Y excel=Y
```

> UI 패턴은 실행 후 대화형으로 선택 (1단계)

---

## 워크플로우

### 1단계: UI 패턴 필수 선택

> **이 단계는 생략 불가!** 개발자에게 반드시 UI 패턴을 질문하고 선택을 받은 후 진행합니다.
> 선택 없이 코드 생성을 시작하면 안 됩니다.

개발자에게 **반드시** 아래 질문을 하고 선택을 받으세요:

```
## UI 패턴 선택 (필수)

어떤 UI 패턴을 사용할까요?

### 기본 UI 패턴 (test-data 가이드 있음)
| 패턴 | 설명 | 사용 시기 |
|------|------|----------|
| **crud** | 목록 + 모달 | 일반적인 CRUD, 입력 10개 미만 |
| page | 목록 + 별도 페이지 | 입력 10개 이상, URL 공유 필요 |
| two-depth | 좌우 분할 | 목록/상세 동시 표시 |
| infinite-scroll | 무한 스크롤 | 피드형, 모바일 최적화 |
| select-list | 선택 모달 | 다른 화면에서 데이터 참조 |
| show-more | 더보기 버튼 | 적은 데이터, 단계별 로드 |
| batch-process | 일괄 처리 | 순차 작업 진행바 |

### 추가 옵션 (기본 패턴과 조합)
| 옵션 | 설명 |
|------|------|
| excel | 엑셀 다운로드/업로드 |
| file | 파일 업로드 |

### 고급 UI 패턴 (MCP 활용, test-data 없음)
| 패턴 | 설명 |
|------|------|
| adv-search | 복합 검색 (5개 이상 조건) |
| calendar | 달력 UI |
| kanban | 칸반 보드 |
| mega-form | 대량 입력 폼 (50개+) |
| tab-list | 탭 내 리스트 |

선택해주세요 (예: crud, excel=Y)
```

**가이드 코드 경로**:
- crud: `front/src/modules/test-data/pages/crud/`
- 기타 패턴: `front/src/modules/test-data/pages/[패턴명]/`

---

### 2단계: Store 확인/생성 + _common 래퍼 확인

```bash
ls front/src/modules/[모듈명]/store/
cat front/src/modules/[모듈명]/store/[모듈명].store.ts

# _common 래퍼 컴포넌트 존재 여부 확인 (조건부)
ls front/src/modules/_common/components/ 2>/dev/null
```

- **Store 있음** → Store 기반으로 UI 개발 진행
- **Store 없음** → Mock 기반 Store 먼저 생성 → [mock-store-pattern.md](references/core/mock-store-pattern.md) 참조

#### _common 래퍼 우선 사용 (조건부)

> 대상 프로젝트에 `_common/components/` 디렉토리가 존재하면 NuxtUI 직접 사용 대신 래퍼 컴포넌트를 우선 사용합니다.

| NuxtUI | _common 래퍼 (있는 경우 우선) |
|--------|------------------------------|
| `<UInput>` | `<p-input-box>` |
| `<USelect>` | `<p-nuxt-select>` |
| `<UFormField>` | `<p-form-field>` |
| `<UFileInput>` | `<p-file-upload>` |

- `_common/components/` 없으면 → NuxtUI 직접 사용 (기존 방식 유지)

---

### 2.5단계: 도메인 분석 (Analyze)

Store 인터페이스와 test-data UI를 비교 분석합니다:

1. **Store 액션 비교**: test-data 대비 액션 수, 특수 동작, 파일/엑셀 기능
2. **UI 복잡도 판단**: 필드 수, 검색 조건, 테이블 컬럼 구성
3. **적응 결정**:
   - Must Follow → 그대로 (script setup, 필수 패턴, AI Slop 금지)
   - May Adapt → 도메인 맞춤 (테이블 컬럼, 검색 폼, 모달 폼 구성)

### 3단계: 코드 생성

선택된 패턴의 가이드 코드를 기준 골격으로 참조 후 도메인에 맞게 적응:

| 패턴 | 가이드 코드 경로 | 참조 문서 |
|------|-----------------|----------|
| crud | `test-data/pages/crud/` | [page-pattern.md](references/basic/page-pattern.md) + [modal-pattern.md](references/basic/modal-pattern.md) |
| page | `test-data/pages/crud/` + `detail-page.vue` | [page-pattern.md](references/basic/page-pattern.md) |
| two-depth | `test-data/pages/two-depth/` | [two-depth-pattern.md](references/basic/two-depth-pattern.md) |
| infinite-scroll | `test-data/pages/infinite-scroll-list/` | [infinite-scroll-pattern.md](references/basic/infinite-scroll-pattern.md) |
| select-list | `test-data/pages/select-list/` | [select-list-pattern.md](references/basic/select-list-pattern.md) |
| batch-process | `test-data/modals/list-table-progress.modal.vue` | [batch-process-pattern.md](references/basic/batch-process-pattern.md) |

**필수 표준 패턴**: [common-patterns.md](references/core/common-patterns.md) 참조
- Selectbox 패턴 (전체 옵션 value='')
- Router 동기화 패턴 (listAction, resetAction, watch)
- Date 검색 패턴 (초기값: 5년 전 ~ 오늘)

---

### 4단계: 검증 & 완료

```bash
cd front && bunx vue-tsc --noEmit  # 타입 체크
cd front && bun run lint:fix      # 린트
cd front && bun run build         # 빌드
```

> 에러 발생 시: 원인 분석 → 코드 수정 → 다시 검증 → 통과할 때까지 반복

---

## 생성 파일 구조

```
front/src/modules/[모듈명]/
├── pages/
│   ├── list.vue              # 목록 페이지 (껍데기)
│   ├── list-search.vue       # 검색 영역
│   ├── list-table.vue        # 테이블 영역
│   └── detail-page.vue       # 상세 페이지 (page 패턴)
├── modals/
│   ├── insert.modal.vue      # 등록 모달
│   ├── update.modal.vue      # 수정 모달
│   └── detail.modal.vue      # 상세 모달
├── _[모듈명].routes.ts       # 라우트 정의
└── _[모듈명].validator.ts    # Yup 검증 스키마
```

---

## Bounded Autonomy (자율 적응 규칙)

### Must Follow (절대 준수)
- `<script setup>` 필수
- NuxtUI 컴포넌트 우선, AI Slop 금지
- 필수 패턴: `listAction`, `resetAction`, `listMovePage`, watch 패턴
- `@submit.prevent="listAction"`, `@change="listAction"` 패턴
- 모듈 경계: `_common`만 import

### May Adapt (분석 후 보완)
- 테이블 컬럼 구성 (도메인 필드에 맞춤)
- 검색 폼 구성 (필드 수에 따른 레이아웃)
- 모달/페이지 폼 구성 (입력 필드 그룹핑)
- UI 상호작용 흐름 (도메인 특수 UX)

### Adapt 조건
보완 시 반드시: (1) 이유 설명 (2) Must Follow 미침범 (3) vue-tsc + lint + build 통과

---

## 완료 조건

```
┌─────────────────────────────────┐
│ 완료 체크리스트                 │
│ □ UI 패턴 선택 완료             │
│ □ Store 연결 확인               │
│ □ 페이지/모달 컴포넌트 생성     │
│ □ bunx vue-tsc --noEmit 통과     │
│ □ bun run lint:fix 통과         │
│ □ bun run build 성공            │
└─────────────────────────────────┘
```

> 빌드 성공 없이 완료 선언 금지!

---

## 완료 후 안내

```
UI 컴포넌트 생성이 완료되었습니다.

📁 **생성된 파일**:
- front/src/modules/[모듈명]/pages/
- front/src/modules/[모듈명]/modals/
- front/src/modules/[모듈명]/_[모듈명].routes.ts

✅ **검증 결과**:
- vue-tsc: 통과
- lint: 통과
- build: 통과

**확인 방법**:
cd front && bun run dev
# 브라우저에서 http://localhost:3000/[모듈명]/list 접속
```

---

## 조건부 참조 가이드 (토큰 절약)

> **중요**: 선택된 패턴의 참조 파일만 읽으세요!
> 모든 references를 한 번에 로드하지 마세요.

### 🔴 필수 참조 (반드시 읽기 - 생략 금지!)

> **경고**: 아래 파일은 **어떤 패턴을 선택하든 반드시 먼저 읽어야 합니다!**
> 이 파일을 읽지 않으면 검색, 페이징, URL 상태관리 패턴이 누락됩니다.

- **[common-patterns.md](references/core/common-patterns.md)** - URL Watch 패턴, Selectbox, Router 동기화, Date 검색, 모달 오픈 패턴
  - ⚠️ URL Watch 패턴 (list-search.vue, list-table.vue)
  - ⚠️ listAction, resetAction, listMovePage 함수
  - ⚠️ `@change="listAction"`, `@submit.prevent="listAction"` 패턴

### 패턴별 참조 매핑

| 선택 패턴 | 읽어야 할 파일 |
|----------|---------------|
| **crud** | basic/page-pattern.md + basic/modal-pattern.md |
| **page** | basic/page-pattern.md |
| **two-depth** | basic/two-depth-pattern.md |
| **infinite-scroll** | basic/infinite-scroll-pattern.md |
| **select-list** | basic/select-list-pattern.md |
| **batch-process** | basic/batch-process-pattern.md |
| **adv-search** | advanced/adv-search-pattern.md |
| **calendar** | advanced/calendar-pattern.md |
| **kanban** | advanced/kanban-pattern.md |
| **mega-form** | advanced/mega-form-pattern.md |
| **tab-list** | advanced/tab-list-pattern.md |

### 옵션별 추가 참조

| 옵션 | 읽어야 할 파일 |
|------|---------------|
| excel=Y | options/excel-pattern.md |
| file=Y | options/file-upload-pattern.md |
| validator 필요 | options/validator-pattern.md |

### 조건부 참조

| 상황 | 읽어야 할 파일 |
|------|---------------|
| Store 없음 | core/mock-store-pattern.md, core/store-pattern.md |
| 로딩 상태 필요 | core/loading-state-pattern.md |
| 에러 처리 필요 | core/error-handling-pattern.md |

---

## references 전체 목록 (참고용)

| 카테고리 | 파일 | 용도 |
|----------|------|------|
| **basic/** | page, modal, two-depth, infinite-scroll, select-list, batch-process | 기본 UI 패턴 |
| **advanced/** | adv-search, calendar, kanban, mega-form, tab-list | 고급 패턴 |
| **options/** | excel, file-upload, validator | 추가 옵션 |
| **core/** | store, type, mock-store, common, loading-state, error-handling, ui-patterns | 핵심 가이드 |
| **guides/** | validation, completion | 프로세스 가이드 |

---

## 참조

- **가이드 코드 (필수)**: `front/src/modules/test-data/`
- **Store**: `front/src/modules/[모듈명]/store/`

> test-data 가이드 코드를 기준 골격으로 참조하되, 도메인 특성에 맞게 Bounded Autonomy 범위 내에서 적응
