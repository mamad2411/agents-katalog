---
name: peach-gen-ui-proto
description: |
  Backend 없이 Mock 데이터 기반 프로토타입 UI를 생성하는 스킬. Vue 3 + TypeScript + NuxtUI v4.
  "프로토타입 만들어줘", "Mock 화면", "proto UI", "기획 화면 빠르게" 키워드로 트리거.
  실제 API 연동 없이 기획자/디자이너 검토용 화면을 빠르게 생성한다.
  실제 API 연동이 필요하면 peach-gen-ui를 사용한다.
---

# Frontend UI 프로토타입 생성 스킬

## 페르소나

당신은 프로토타입 UI 개발 최고 전문가입니다.
- Vue 3 Composition API 마스터
- TypeScript 타입 설계 전문가
- NuxtUI v4 + TailwindCSS v4 경험 풍부
- Mock 데이터 기반 프로토타이핑 전문
- 기획자 친화적 바이브코딩 지원

---

## 핵심 원칙

- **Backend 없음**: 모든 API는 Mock interceptor 경유 (useApi() 호출 유지)
- **생성 방식**: test-data 가이드 코드를 기준 골격으로 참조 후 Mock 특화 적응
- **컴포넌트 사용**: 케밥케이스 사용 (예: `<u-button>`, `<u-modal>`, `<my-component>`)
- **완료 기준**: vue-tsc + lint + build 모두 통과
- **프로덕션 전환 대비**: API 시그니처 유지, Mock 교체만으로 실서버 연동 가능

---

## peach-gen-ui와의 핵심 차이

| 항목 | peach-gen-ui (프로덕션) | peach-gen-ui-proto (프로토타입) |
|------|----------------------|------------------------------|
| **Backend** | 실제 API 서버 필수 | 없음 (Mock Only) |
| **Store API 호출** | `useApi().get('/endpoint')` → 실서버 | `useApi().get('/endpoint')` → Mock interceptor |
| **Mock 데이터** | 없음 | `mock/[모듈명].mock.ts` 파일에 정의 |
| **파일 업로드** | 실서버 업로드 | Mock (FormData 로깅 + 가짜 UUID 반환) |
| **Excel** | 실서버 다운로드 | ExcelTemplateUtil 로컬 생성 |
| **검증 도구** | bun (vue-tsc/lint/build) | bun 기본 (`bunx` + `bun run`) |
| **사용자** | 개발자 | 기획자 (바이브코딩) |

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

## 절대 필수 패턴 (모든 UI 패턴 공통)

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

> **상세 코드와 금지 패턴**: [common-patterns.md](references/core/common-patterns.md) 참조 (필수)

---

## 입력 방식

```
/peach-gen-ui-proto [모듈명] [옵션]
```

### 옵션
| 옵션 | 기본값 | 설명 |
|------|--------|------|
| excel | N | 엑셀 다운로드/업로드 기능 (Mock) |
| file | N | 파일 업로드 기능 (Mock) |

### 예시
```
/peach-gen-ui-proto notice-board
/peach-gen-ui-proto member-manage excel=Y
/peach-gen-ui-proto product file=Y excel=Y
```

> UI 패턴은 실행 후 대화형으로 선택 (1단계)

---

## 워크플로우

### 1단계: UI 패턴 필수 선택

> **이 단계는 생략 불가!** 기획자에게 반드시 UI 패턴을 질문하고 선택을 받은 후 진행합니다.
> 선택 없이 코드 생성을 시작하면 안 됩니다.

기획자에게 **반드시** 아래 질문을 하고 선택을 받으세요:

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
| excel | 엑셀 다운로드/업로드 (Mock 로컬 생성) |
| file | 파일 업로드 (Mock UUID 반환) |

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

### 2단계: test-data 가이드 코드 확인 + 대상 프로젝트 감지

```bash
# test-data 모듈 존재 여부 확인
ls front/src/modules/test-data/ 2>/dev/null

# _common 래퍼 컴포넌트 존재 여부 확인
ls front/src/modules/_common/components/ 2>/dev/null

# 빌드 도구 감지
ls front/package.json && head -20 front/package.json
ls front/bun.lockb 2>/dev/null && echo "BUILD_TOOL=bun"
```

- **test-data 있음** → 가이드 코드 기반으로 생성
- **test-data 없음** → references 문서 기반으로 생성

#### 빌드 도구 기준

| 파일 존재 | 빌드 도구 | 검증 명령어 |
|-----------|----------|------------|
| `bun.lockb` | bun | `cd front && bunx vue-tsc --noEmit && bun run lint:fix && bun run build` |

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

test-data UI와 요청된 도메인을 비교 분석합니다:

1. **UI 복잡도 판단**: 필드 수, 검색 조건, 테이블 컬럼 구성
2. **Mock 데이터 설계**: 도메인에 맞는 현실적인 샘플 데이터 구상
3. **적응 결정**:
   - Must Follow → 그대로 (script setup, 필수 패턴, AI Slop 금지)
   - May Adapt → 도메인 맞춤 (테이블 컬럼, 검색 폼, 모달 폼 구성)

### 3단계: Mock 서비스 + Store + 코드 생성

선택된 패턴의 가이드 코드를 기준 골격으로 참조 후 도메인에 맞게 적응:

#### 3-1. Mock 데이터 생성 (필수)

**[mock-service-pattern.md](references/core/mock-service-pattern.md)** 참조

```
mock/[모듈명].mock.ts 생성:
- 도메인 맞춤 샘플 데이터 (5~10건)
- 동적 데이터 생성 함수
- API 시그니처 유지 (프로덕션 전환 대비)
```

#### 3-2. Store 생성 (Mock useApi() 경유)

**[mock-store-pattern.md](references/core/mock-store-pattern.md)** 참조

```
store/[모듈명].store.ts 생성:
- useApi() 경유 패턴 유지
- Mock interceptor가 요청을 가로채서 Mock 데이터 반환
- 프로덕션 전환 시 interceptor만 제거하면 됨
```

#### 3-3. 페이지 생성

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
# bun 프로젝트 기준
cd front && bunx vue-tsc --noEmit  # 타입 체크
cd front && bun run lint:fix      # 린트
cd front && bun run build         # 빌드
```

> 에러 발생 시: 원인 분석 → 코드 수정 → 다시 검증 → 통과할 때까지 반복

---

## 생성 파일 구조

```
front/src/modules/[모듈명]/
├── mock/
│   └── [모듈명].mock.ts          # Mock 데이터 + 동적 생성 함수
├── type/
│   └── [모듈명].type.ts          # 타입 정의 (백엔드 동일 구조)
├── store/
│   └── [모듈명].store.ts         # Pinia Option API (Mock useApi() 경유)
├── pages/
│   ├── list.vue                  # 목록 페이지 (껍데기)
│   ├── list-search.vue           # 검색 영역
│   ├── list-table.vue            # 테이블 영역
│   └── detail-page.vue           # 상세 페이지 (page 패턴)
├── modals/
│   ├── insert.modal.vue          # 등록 모달
│   ├── update.modal.vue          # 수정 모달
│   └── detail.modal.vue          # 상세 모달
├── _[모듈명].routes.ts           # 라우트 정의
└── _[모듈명].validator.ts        # Yup 검증 스키마
```

---

## Bounded Autonomy (자율 적응 규칙)

### Must Follow (절대 준수)
- `<script setup>` 필수
- NuxtUI 컴포넌트 우선, AI Slop 금지
- 필수 패턴: `listAction`, `resetAction`, `listMovePage`, watch 패턴
- `@submit.prevent="listAction"`, `@change="listAction"` 패턴
- 모듈 경계: `_common`만 import
- Mock 데이터는 `mock/` 디렉토리에 분리
- useApi() 경유 패턴 유지 (프로덕션 전환 대비)

### May Adapt (분석 후 보완)
- 테이블 컬럼 구성 (도메인 필드에 맞춤)
- 검색 폼 구성 (필드 수에 따른 레이아웃)
- 모달/페이지 폼 구성 (입력 필드 그룹핑)
- Mock 데이터 구성 (도메인 특수 샘플)
- UI 상호작용 흐름 (도메인 특수 UX)

### Adapt 조건
보완 시 반드시: (1) 이유 설명 (2) Must Follow 미침범 (3) vue-tsc + lint + build 통과

---

## 완료 조건

```
┌─────────────────────────────────────┐
│ 완료 체크리스트                     │
│ □ UI 패턴 선택 완료                 │
│ □ Mock 데이터 생성 완료             │
│ □ Store (Mock 경유) 생성 완료       │
│ □ 페이지/모달 컴포넌트 생성         │
│ □ vue-tsc (타입체크) 통과           │
│ □ lint 통과                         │
│ □ build 성공                        │
└─────────────────────────────────────┘
```

> 빌드 성공 없이 완료 선언 금지!

---

## 완료 후 안내

```
UI 프로토타입 생성이 완료되었습니다.

**생성된 파일**:
- front/src/modules/[모듈명]/mock/     ← Mock 데이터
- front/src/modules/[모듈명]/store/    ← Mock Store
- front/src/modules/[모듈명]/pages/    ← UI 페이지
- front/src/modules/[모듈명]/modals/   ← 모달 컴포넌트

**검증 결과**:
- vue-tsc: 통과
- lint: 통과
- build: 통과

**확인 방법**:
cd front && bun run dev
# 브라우저에서 http://localhost:3000/[모듈명]/list 접속

**프로덕션 전환 시**:
1. mock/ 디렉토리 삭제
2. Store에서 Mock interceptor 제거
3. 실제 API 엔드포인트 연결
→ useApi() 호출 코드는 그대로 유지됩니다.
```

---

## 조건부 참조 가이드 (토큰 절약)

> **중요**: 선택된 패턴의 참조 파일만 읽으세요!
> 모든 references를 한 번에 로드하지 마세요.

### 필수 참조 (반드시 읽기 - 생략 금지!)

> **경고**: 아래 파일은 **어떤 패턴을 선택하든 반드시 먼저 읽어야 합니다!**
> 이 파일을 읽지 않으면 검색, 페이징, URL 상태관리 패턴이 누락됩니다.

- **[common-patterns.md](references/core/common-patterns.md)** - URL Watch 패턴, Selectbox, Router 동기화, Date 검색, 모달 오픈 패턴
- **[mock-service-pattern.md](references/core/mock-service-pattern.md)** - Mock 데이터 정의, 동적 생성, API 시그니처 유지
- **[mock-store-pattern.md](references/core/mock-store-pattern.md)** - Mock useApi() 경유 Store 패턴

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
| 로딩 상태 필요 | core/loading-state-pattern.md |
| 에러 처리 필요 | core/error-handling-pattern.md |

---

## references 전체 목록 (참고용)

| 카테고리 | 파일 | 용도 |
|----------|------|------|
| **core/** | mock-service, mock-store, store, type, common, loading-state, error-handling, ui-patterns, visual-guide, common-component-guide | 핵심 가이드 |
| **basic/** | page, modal, two-depth, infinite-scroll, select-list, batch-process | 기본 UI 패턴 |
| **advanced/** | adv-search, calendar, kanban, mega-form, tab-list | 고급 패턴 |
| **options/** | excel, file-upload, validator | 추가 옵션 |
| **guides/** | validation, completion | 프로세스 가이드 |

---

## 참조

- **가이드 코드 (필수)**: `front/src/modules/test-data/`
- **Mock 데이터**: `front/src/modules/[모듈명]/mock/`
- **Store**: `front/src/modules/[모듈명]/store/`

> test-data 가이드 코드를 기준 골격으로 참조하되, Mock 특화 + 도메인 특성에 맞게 Bounded Autonomy 범위 내에서 적응
