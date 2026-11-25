---
name: impakers-components-rules
description: "임패커스 UI 컴포넌트 개발 규칙 (shadcn/ui + Tailwind 기반). Claude가 .tsx/.jsx 편집, Dialog/Modal/AlertDialog/Sheet/Drawer/Popover 생성, Form(react-hook-form+zod) 구현, Table(TanStack/shadcn) 작성, Button/Select/Combobox/DropdownMenu/Badge/Skeleton/Tooltip 사용, Sonner toast 처리, 서버 액션 후 쿼리 invalidate 등을 수행할 때 자동 발동. 트리거 키워드 — shadcn, 모달, 다이얼로그, dialog, modal, sheet, drawer, popover, form, useForm, zodResolver, DataTable, useQuery, invalidateQueries, revalidatePath, toast, sonner, 컴포넌트 규칙, UI 규칙, COMPONENTS_RULES, 디자인 규칙. Use when editing React/Next.js UI code in any impakers frontend project (trusflow, place-real, lomelo-admin, dexter-krema, traction-13, etc.)."
version: 1.0.0
author: IMPAKERS
license: internal
---

# 임패커스 UI 컴포넌트 개발 규칙 (shadcn/ui 기반)

> **이 스킬이 활성화되면**, 아래 규칙을 **반드시 읽고 준수**한 뒤 컴포넌트 코드를 생성/수정한다.
> 규칙은 `WHEN <조건> → THEN <처리>` 형식으로 기술되어 있다.
> 기본 UI 라이브러리는 **shadcn/ui** (Radix 기반) + **Tailwind**.

---

## 사용 프로토콜 (Claude용)

1. **TSX/JSX 파일 편집/생성 직전**: 아래 §0–§12의 관련 섹션을 먼저 확인.
2. **충돌 시**: `§0. 핵심 원칙` (Depth 최소화) > `§11. 접근성` > 나머지 순서.
3. **Dialog 액션을 만들 때**: 반드시 §2.11 (invalidate/revalidate) 적용.
4. **규칙 미매칭 상황**: 추측하지 말고 사용자에게 짧게 확인. "이 경우는 규칙 문서에 없습니다. §X와 유사하게 적용할까요?"
5. **코드베이스에 이미 다른 패턴이 쓰이고 있다면**: 규칙을 우선하되, 일관성을 위해 해당 파일 내 기존 관습은 유지하고 **PR/커밋에 'follow-up: §X 위반'** 메모를 남긴다.

---

<!-- BEGIN:SYNCED-RULES -->

## 0. 핵심 원칙 (Global)

### 0.1 Depth 최소화

- **원칙**: 사용자가 목표 액션을 완료하기까지의 UI Depth를 최소화한다.
- **이유**: 임패커스 서비스는 비대면 환경에서 동작하므로 쉽고 간단해야 한다.
- **기준**: 주요 비즈니스 로직은 **3 depth 이하**로 도달 가능해야 한다.

### 0.2 복잡 로직은 백엔드로

- **WHEN** UI 상에서 여러 액션이 연쇄적으로 필요한 경우
- **THEN** 백엔드 자동화(서버 액션 등)로 전환을 먼저 제안한다.

### 0.3 shadcn 기본 사용 원칙

- **WHEN** 공식 shadcn 컴포넌트로 충분히 해결 가능한 경우
- **THEN** 프로젝트 전반에 반복되는 조합은 `components/ui/` 외 `components/{domain}/` 에 래퍼로 분리한다. (예: `searchable-select`, `confirm-dialog`, `date-picker`)

---

## 1. Table

### 1.1 헤더 내 기능 배치

#### 1.1.1 단일 컬럼 필터 / 정렬

- **위치**: 해당 컬럼 헤더의 **오른쪽 끝 아이콘**
- **동작**: 아이콘 클릭 → **Popover**로 필터/정렬 UI 표시

#### 1.1.2 단일 컬럼 검색

- **위치**: 해당 컬럼 헤더 내부
- **동작**: 해당 컬럼 값에 대해서만 검색

### 1.2 테이블 외부 검색 / 필터

#### 1.2.1 통합 검색 (2개 이상 컬럼 대상)

- **위치**: 테이블 **상단**에 별도 `<Input>` 배치
- **필수 요소**:
  - `<Label>`: 검색 대상 데이터 명시
  - `placeholder`: 검색 가능한 데이터 예시 힌트

#### 1.2.2 종합 필터 (헤더 외부 필터)

- **필수 요소**: `<Label>`로 필터 기준 명시
- **선택 방식**:
  - **Single-select 필터** → `Select` (shadcn)
  - **Multi-select 필터** → `Combobox` (shadcn Command + Popover), 선택 항목은 상단에 `Badge`로 가시화

### 1.3 레이아웃 & 페이지네이션

#### 1.3.1 스크롤

- **WHEN** 컬럼 수 ≥ 7
- **THEN** 가로 + 세로 스크롤 모두 지원 (`ScrollArea` 또는 `overflow-auto`)

#### 1.3.2 페이지네이션

- **WHEN** 데이터 행 수 ≥ 20
- **THEN**
  - 페이지네이션 **필수 구현** (`Pagination` 컴포넌트)
  - 페이지당 행 수 **3가지 보기 옵션** 제공 (예: 10 / 25 / 50), 데이터 행 수가 500건을 넘지 않으며, 필요한 경우 전체 보기 옵션을 제공한다. 최대 페이지네이션 (pagination) 행 수 단위는 200이다.

### 1.4 액션

#### 1.4.1 행 단위 액션 (Row Action)

- **위치**: 각 행의 **맨 우측 컬럼**
- **WHEN** 해당 행의 액션 아이템이 2개 이상
- **THEN** `DropdownMenu`로 액션 목록 표시 (`MoreHorizontal` 아이콘 트리거)
- **WHEN** 해당 행의 액션 아이템이 1개
- **THEN** 액션 버튼 표시

#### 1.4.2 다중 행 액션 (Bulk Action)

- **트리거**: **좌측 fixed 체크박스**로 행 선택
- **실행 버튼 위치** (택1):
  - 테이블 **중앙 하단** 플로팅 액션 버튼
  - 테이블 **상단** 일괄 액션 버튼

---

## 2. Modal (Dialog)

### 2.1 Modal 사용 조건

- **WHEN** 페이지 전체 액션 아이템(= `actions.ts` / 서버 액션 기준)이 **2개 이하**
- **THEN** 별도 페이지를 만들지 않고 **Dialog로 처리**
- **목표**: 전체 UI Depth를 **3 이하**로 유지

### 2.2 Modal 제약

- ❌ **금지**: Dialog 내부에서 또 다른 Dialog 호출 (`AlertDialog` 제외)
- **제한**: Dialog 내부 모든 기능은 **1 depth**로 한정

### 2.3 레이아웃 (컨텐츠 / 액션 영역 분리)

- **컨텐츠 영역**: 중앙 배치, 내용이 많으면 **내부 스크롤** 허용
- **액션 영역**: `DialogFooter`로 **하단 고정(sticky)**, 스크롤 영역 밖에 유지
- **이유**: 사용자가 긴 컨텐츠를 훑어보는 도중에도 주요 액션(저장/발송 등)이 항상 보여야 한다.

### 2.4 닫힘 방지 (민감 액션 보호)

- **WHEN** 모달이 **수정 중인 입력값**을 갖거나 **민감한 액션**(결제, 삭제, 발송 등)을 포함
- **THEN** 아래 중 하나 이상 적용:
  - `onPointerDownOutside` / `onInteractOutside` 차단 → 바깥 클릭으로 닫히지 않게
  - Escape 키 차단 (`onEscapeKeyDown`)
  - 닫기 시도 시 **Unsaved Changes 경고 AlertDialog** 표시
- **이유**: 모달은 닫힘 시 상태 저장이 안 되므로 사용자 실수를 방지해야 한다.

### 2.5 숨겨진 로직 투명화

- **WHEN** 액션 버튼이 사용자가 바로 인지하기 어려운 부가 로직을 수행 (예: '저장' 클릭 시 자동 메일 발송, 결제 처리, 외부 API 연동)
- **THEN**
  - **실행 전**: 버튼 옆 helper text 또는 툴팁으로 부가 효과 명시 ("저장 시 담당자에게 알림이 발송됩니다")
  - **또는** 확인 체크박스(`Checkbox`) / `AlertDialog` 경유
  - **실행 후**: `toast`로 수행된 부가 작업을 피드백 ("저장 완료 · 메일 2건 발송됨")

### 2.6 모달 액션 개수

- **권장**: 주요 액션 **2개 이하** (예: 취소 + 저장)
- ❌ **금지**: 3개 이상의 주요 액션 버튼을 한 모달에 배치
- **WHEN** 3개 이상이 필요해 보이는 경우
- **THEN** 더 작은 단위 모달로 분리하거나, 보조 액션을 `DropdownMenu`로 묶는다.

### 2.7 액션 없는 안내는 Popover/HoverCard로

- **WHEN** 유저 입력이나 액션 버튼 없이 **단순 안내/도움말**만 필요한 경우
- **THEN** `Dialog` 대신 `Popover`(클릭) 또는 `Tooltip`(호버 <20자) 사용
- **이유**: 모달은 컨텍스트 중단 비용이 크다. 안내에는 과도하다.

### 2.8 AlertDialog 사용 (파괴적/되돌릴 수 없는 액션)

- **WHEN** 삭제, 결제, 일괄 발송 등 **되돌릴 수 없는 액션** 확인
- **THEN** `Dialog`가 아닌 **`AlertDialog`** 사용
  - 기본 포커스: **취소(Cancel)** 버튼
  - 확정 버튼: `variant="destructive"`
  - 본문: 해당 액션의 **결과(무엇이 몇 건 바뀌는지)** 를 명시

### 2.9 접근성 (a11y)

- **필수**: `DialogTitle` + `DialogDescription` 지정 (screen reader)
- **초기 포커스**: 모달이 열리면 **첫 번째 입력 필드** 또는 **제목**에 포커스
- **아이콘 전용 닫기 버튼**: `aria-label="닫기"` 필수

### 2.10 Dialog vs Sheet vs Drawer

- `Dialog` — 중앙 모달, 폼/확인창 (기본)
- `Sheet` — 측면 슬라이드. 폼이 길거나, 테이블 옆에서 상세 미리보기
- `Drawer` — **모바일 전용 바텀시트**. 같은 UI가 데스크톱에선 `Dialog`, 모바일에선 `Drawer`로 전환 (반응형)
- 선택 기준: 컨텐츠 높이가 화면을 넘을 정도로 많다 → `Sheet`. 모바일 UX 우선 → `Drawer`.

### 2.11 액션 실행 후 데이터 동기화

- **WHEN** Dialog의 액션(저장/삭제/발송 등)이 **현재 머무는 페이지의 데이터**를 변경하는 경우
- **THEN** 액션 성공 후 해당 데이터에 의존하는 **쿼리를 무효화(invalidate)** 하거나 **재요청**한다.
  - **TanStack Query**: `queryClient.invalidateQueries({ queryKey: [...] })`
  - **Next.js 서버 컴포넌트 / 서버 액션**: `revalidatePath('/...')` 또는 `revalidateTag('...')`
  - **SWR**: `mutate(key)`
- **금지**: 화면 전체 `router.refresh()`로 대충 덮는 것 (해당 섹션만 타겟팅). 단, 여러 섹션이 동시에 영향받으면 허용.
- **이유**: 모달은 컨텍스트를 유지한 채 닫히므로, 닫힌 뒤 stale 데이터가 보이면 사용자가 액션 성공 여부를 의심한다.
- **체크리스트**:
  - [ ] 액션 성공 응답 → `toast.success` → 쿼리 invalidate **같은 핸들러 안에서** 순서대로
  - [ ] 낙관적 업데이트(`onMutate`)를 쓰는 경우, 실패 시 `onError`에서 롤백 + invalidate

---

## 3. Card

### 3.1 사용 금지 케이스

- **WHEN** 페이지 상단 **통계(숫자 요약)** 를 표현할 때
- **THEN** `<Card>` 사용 **지양**
  - 대신: 컴포넌트 **타이틀 하단** 또는 **테이블 상단**에 `<p>` 태그로 표시

### 3.2 올바른 사용 케이스

- **WHEN** 한 페이지 내에서 **여러 컴포넌트를 그룹화**해야 할 때
- **THEN** `<Card>`로 그룹 감싸기

---

## 4. Form (react-hook-form + zod)

### 4.1 표준 스택

- **필수**: `react-hook-form` + `zodResolver` + shadcn `Form` 컴포넌트
- **구조**: `FormField` → `FormItem` → `FormLabel` + `FormControl` + `FormDescription` + `FormMessage`

### 4.2 유효성 검증

- **WHEN** 입력 제약이 있는 필드
- **THEN** Zod 스키마로 **서버와 동일한 스키마 공유** (`lib/validations/*.ts` 등)
- **에러 메시지**: `FormMessage`가 필드 하단에 자동 표시

### 4.3 제출 상태 UX

- **WHEN** 폼 제출 중 (`isSubmitting` 또는 `isPending`)
- **THEN**
  - 제출 버튼 `disabled` + `Spinner` 표시, **텍스트는 그대로 유지** (폭 변화 방지)
  - 취소/닫기 버튼도 `disabled` (중복 트리거 방지)
  - 서버 에러는 `FormMessage` 또는 `toast.error`로 표시

### 4.4 필드 배치

- **WHEN** 필드 수 ≤ 6 → 1열 배치
- **WHEN** 필드 수 ≥ 7 또는 관련 필드 그룹이 있는 경우 → `grid` 2열 또는 섹션 분리
- **연관 필드**는 같은 행(row)에 배치 (예: 시작일/종료일)

### 4.5 필수 / 선택 표기

- **필수 필드**: `FormLabel`에 `*` 표시 + `aria-required="true"`
- **선택 필드**: "(선택)" 라벨 뒤에 표기, 별도 색상 강조 금지

---

## 5. Feedback — Toast (Sonner)

### 5.1 표준 라이브러리

- 토스트는 **`sonner`** 사용 (shadcn 기본). `useToast` (구 토스트)는 사용하지 않는다.

### 5.2 상황별 API

- **성공** → `toast.success("저장 완료")`
- **실패** → `toast.error("저장 실패", { description: "…" })`
- **진행 중 액션** → `toast.promise(asyncFn, { loading, success, error })`
- **일반 알림** → `toast.info` / `toast.warning`

### 5.3 작성 가이드

- **성공 메시지**: **과거형 짧은 문장** ("발송 완료", "삭제됨")
- **에러 메시지**: **원인 + 다음 액션** 한 문장 ("서버 연결 실패 · 잠시 후 다시 시도해주세요")
- ❌ "오류가 발생했습니다" 같은 의미 없는 메시지 금지

### 5.4 사용 제약

- **WHEN** 같은 종류의 토스트가 연속으로 발생할 가능성이 있는 경우
- **THEN** `id` 옵션으로 **중복 토스트 병합** (`toast.success(..., { id: "save-xyz" })`)
- 동시 표시 토스트는 **최대 3개**로 제한 (`<Toaster visibleToasts={3} />`)

### 5.5 서버 액션 연동

- 서버 액션 결과는 **컴포넌트에서 toast로 피드백**하는 것을 표준으로 한다.
- 페이지 리다이렉트가 일어나는 액션은 **리다이렉트 직후** 토스트가 잡히도록 `cookies()` 기반 flash 패턴 사용.

---

## 6. Selection — Select / Combobox / Dropdown

### 6.1 선택 UI 분기 기준

| 옵션 수   | 검색 필요 | 컴포넌트                                |
| --------- | --------- | --------------------------------------- |
| 1–6       | X         | `Select` (shadcn)                       |
| 7 이상    | O         | `Combobox` (Command + Popover)          |
| 다중 선택 | —         | `Combobox` + `Badge` (선택된 항목 표시) |

### 6.2 Native Select 금지

- ❌ `<select>` 네이티브 태그 직접 사용 금지 (스타일 불일관)
- **예외**: 모바일 우선 폼에서 네이티브 UX가 더 나은 경우 `select-native.tsx` 래퍼만 사용

### 6.3 옵션 로딩

- **WHEN** 옵션이 **비동기** 로드
- **THEN** `Combobox` 내부에 `Skeleton` 3줄, 에러 시 "재시도" 버튼

### 6.4 Dropdown vs Select

- `Select` — **값 선택** (폼 입력)
- `DropdownMenu` — **액션 트리거** (행 액션, 메뉴). 값 바인딩 금지.

---

## 7. Button

### 7.1 variant 의미 고정

| variant       | 용도                                |
| ------------- | ----------------------------------- |
| `default`     | 주요 액션 (Primary)                 |
| `secondary`   | 보조 액션                           |
| `outline`     | 취소, 보조                          |
| `ghost`       | 아이콘 버튼, 인라인 액션            |
| `destructive` | **파괴적 액션 전용** (삭제/탈퇴 등) |
| `link`        | 텍스트 링크 대체                    |

### 7.2 로딩 / 비활성 상태

- **로딩 중**: `disabled` + 좌측에 `Loader2` 스피너, 버튼 **텍스트/너비 유지**
- **비활성 사유**: 마우스 오버 시 `Tooltip`으로 **왜 비활성인지** 제공

### 7.3 아이콘 전용 버튼

- `size="icon"` + `aria-label` 필수
- 의미 없는 장식 아이콘은 `aria-hidden="true"`

---

## 8. Status Indicators — Badge / Skeleton

### 8.1 Badge

- **용도**: 상태값(Status), 카운트, 태그
- **색상**: 의미 고정 — success(초록) / warning(주황) / error(빨강) / info(회색)
- ❌ 장식용 Badge 금지 (눈에 띈다고 남발 X)

### 8.2 Skeleton

- **WHEN** 서버 데이터 로딩 중
- **THEN** `Spinner`보다 **`Skeleton`** 우선 (레이아웃 쉬프트 방지)
- 실제 최종 레이아웃과 **동일한 크기/개수**로 배치

---

## 9. Tooltip vs Popover vs HoverCard

| 상황                                           | 컴포넌트             |
| ---------------------------------------------- | -------------------- |
| 짧은 설명 (<20자), hover 전용                  | `Tooltip`            |
| 클릭 후 상세 정보/미니 폼                      | `Popover`            |
| 프리뷰 카드 (유저 hover 시 프로필 미리보기 등) | `HoverCard`          |
| 확정 필요한 확인                               | `AlertDialog` (§2.8) |
| 전체 입력 폼                                   | `Dialog` / `Sheet`   |

---

## 10. Loading / Empty / Error 상태

### 10.1 Loading

- **페이지 레벨**: Next.js `loading.tsx` + `Suspense` + `Skeleton`
- **컴포넌트 레벨**: `Skeleton`, 버튼 내부 `Loader2`

### 10.2 Empty State

- **필수 요소**: ① 아이콘 or 일러스트, ② 안내 문구 (한 줄), ③ **CTA 버튼 1개** (추가/생성 유도)
- **WHEN** 필터로 인한 빈 결과
- **THEN** "필터 초기화" CTA로 전환

### 10.3 Error

- **페이지 레벨**: `error.tsx` + `reset()` 버튼
- **부분 실패**: 인라인 `Alert` + 재시도 버튼
- **네트워크 에러**: `toast.error` + 재시도

---

## 11. 접근성 (a11y)

- **키보드**: 모든 인터랙티브 요소는 `Tab`, `Enter`, `Esc`로 조작 가능 (Radix 기본 유지)
- **포커스 트랩**: Dialog / Sheet / Drawer 내부 포커스 순환 (Radix 기본)
- **라벨**: 모든 `Input`은 `Label` 연결 (id ↔ htmlFor)
- **색 대비**: 텍스트 대비 **WCAG AA 이상**
- **아이콘 전용 버튼**: `aria-label` 필수

---

## 12. 반응형 (Responsive)

### 12.1 Breakpoint 기본

- Tailwind 기본 사용: `sm(640) · md(768) · lg(1024) · xl(1280)`
- 모바일 퍼스트 원칙 (`className="flex flex-col md:flex-row"`)

### 12.2 모달의 반응형 전환

- **WHEN** 모바일(`<md`)에서 긴 폼 모달
- **THEN** `Dialog` → **`Drawer`로 전환** (`useMediaQuery` + 분기)

### 12.3 테이블의 반응형

- **WHEN** 모바일에서 컬럼 7개 이상
- **THEN** 주요 컬럼만 표시하거나 `Card` 리스트 뷰로 전환

---

## 규칙 적용 우선순위

1. `§0. 핵심 원칙` (Depth 최소화, shadcn 기본) — 항상 최우선
2. `§11. 접근성` — 기능 요구사항과 동급
3. 컴포넌트별 규칙 (§1 ~ §10, §12)
4. 규칙 간 충돌 시 → Depth 최소화 & 접근성 기준으로 판단

<!-- END:SYNCED-RULES -->

---

## 원본 문서

이 스킬은 `workflow/docs/brand/COMPONENTS_RULES.md`를 원본으로 한다.
규칙 수정은 **원본 문서에서만** 진행하고, 본 SKILL.md는 `scripts/sync-components-skill.sh`로 동기화한다.
