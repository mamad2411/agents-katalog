---
name: peach-add-print
description: 인쇄 전용 페이지 생성 전문가. "인쇄 페이지 만들어줘", "프린트 페이지 생성", "출력 페이지" 키워드로 트리거. 레이아웃 없이 컨텐츠만 출력하는 세련된 인쇄 전용 Vue 컴포넌트와 라우트 설정 생성. Context7 MCP로 최신 TailwindCSS v4/Vue 문서 참조, Sequential Thinking으로 인쇄 디자인 분석.
---

# 인쇄 페이지 생성 스킬

## 개요

window.open 방식으로 새 창에서 레이아웃 없이 세련된 인쇄 전용 페이지 생성.

**핵심 패턴:**
- Context7 MCP: Vue.js, TailwindCSS v4 print variant 최신 문서 참조
- Sequential Thinking MCP: 복잡한 인쇄 레이아웃 설계 분석
- 인쇄 최적화 디자인: 가독성, 정보 계층, 페이지 구분

---

## MCP 도구 활용

### Context7 MCP 활용

인쇄 페이지 생성 시 최신 문서 참조:

```bash
# TailwindCSS v4 print variant 쿼리
mcp__context7__resolve-library-id: "TailwindCSS"
mcp__context7__query-docs: "print variant responsive design v4"

# Vue.js 라이프사이클
mcp__context7__resolve-library-id: "Vue.js"
mcp__context7__query-docs: "onMounted lifecycle composition API"
```

### Sequential Thinking MCP 활용

복잡한 인쇄 레이아웃 설계 시:

```
mcp__sequential-thinking__sequentialthinking:
- thought: "인쇄 대상 데이터 구조 분석"
- thought: "페이지 브레이크 위치 결정"
- thought: "헤더/푸터 반복 요소 설계"
- thought: "정보 계층 구조 최적화"
```

---

## 입력 방식

```bash
/peach-add-print [원본컴포넌트경로]
```

---

## 인쇄 디자인 원칙

### 인쇄 매체 특성 (웹과 다른 점)

| 구분 | 웹 | 인쇄 |
|------|-----|------|
| 상호작용 | 클릭, 호버, 스크롤 | 없음 (정적) |
| 색상 | RGB (발광) | CMYK (반사광) |
| 애니메이션 | 가능 | 불가능 |
| 크기 | 반응형 | 고정 (A4, Letter) |
| 해상도 | 72-96dpi | 300dpi 권장 |

### 인쇄 최적화 디자인 가이드

**[print-design-guide.md](references/print-design-guide.md)** 상세 CSS 참조

#### 1. 타이포그래피 (TailwindCSS v4 print variant)

```html
<!-- 인쇄용 타이포그래피 -->
<div class="print:font-sans print:text-[11pt] print:leading-relaxed print:text-black">
  <h1 class="print:text-[18pt] print:font-bold">제목</h1>
  <h2 class="print:text-[14pt] print:font-semibold">부제목</h2>
  <h3 class="print:text-[12pt] print:font-semibold">소제목</h3>
</div>
```

#### 2. 색상 (고대비, 잉크 절약)

```html
<!-- 인쇄 친화적 색상 -->
<span class="print:text-black">기본 텍스트</span>
<span class="print:text-gray-700">보조 텍스트</span>
<span class="print:text-blue-700">강조</span>
<span class="print:text-red-600">음수/경고</span>

<!-- 배경색 (절제하여 사용) -->
<div class="print:bg-gray-100">연한 배경</div>
<div class="print:border print:border-gray-300">테두리</div>
```

#### 3. 레이아웃 (페이지 브레이크)

```html
<!-- 페이지 브레이크 제어 -->
<div class="print:break-before-page">새 페이지 시작</div>
<div class="print:break-after-page">페이지 끝</div>
<div class="print:break-inside-avoid">분리 방지</div>

<!-- 테이블 헤더 반복 -->
<thead class="print:table-header-group">...</thead>
<tfoot class="print:table-footer-group">...</tfoot>

<!-- 인쇄 시 숨김/표시 -->
<div class="print:hidden">화면에서만 표시</div>
<div class="hidden print:block">인쇄에서만 표시</div>
```

#### 4. 정보 계층 구조

```
┌─────────────────────────────────────────┐
│  문서 타이틀 (18pt, Bold, 중앙)          │
├─────────────────────────────────────────┤
│  메타 정보 (기간, 작성자, 날짜)           │
│  ─────────────────────────────────────  │
│  요약 박스 (배경색, 테두리)               │
│  ┌─────────────────────────────────┐   │
│  │ 핵심 수치 / KPI                   │   │
│  └─────────────────────────────────┘   │
├─────────────────────────────────────────┤
│  섹션 타이틀 (14pt, Bold)               │
│  ─────────────────────────────────────  │
│  데이터 테이블                           │
│  ┌───┬───────┬─────┬─────┬─────┐      │
│  │   │       │     │     │     │      │
│  ├───┼───────┼─────┼─────┼─────┤      │
│  │   │       │     │     │     │      │
│  └───┴───────┴─────┴─────┴─────┘      │
├─────────────────────────────────────────┤
│  푸터 (페이지 번호, 인쇄일시)             │
└─────────────────────────────────────────┘
```

---

## 워크플로우

### 1단계: 원본 컴포넌트 분석 (Sequential Thinking)

```
Sequential Thinking 활용:
1. 데이터 구조 파악 (테이블, 목록, 차트 등)
2. 인쇄 시 필수 정보 vs 생략 가능 정보 분류
3. 페이지당 최적 데이터 양 계산
4. 페이지 브레이크 위치 결정
```

### 2단계: Context7로 최신 TailwindCSS 문서 참조

```bash
# TailwindCSS v4 print variant 최신 사양 확인
mcp__context7__query-docs:
  libraryId: "/tailwindlabs/tailwindcss"
  query: "print variant modifier responsive design"
```

### 3단계: 인쇄 컴포넌트 생성

**[print-component.md](references/print-component.md)** 템플릿 참조

### 4단계: 라우트 설정

**[print-routes.md](references/print-routes.md)** 템플릿 참조

### 5단계: 원본에 인쇄 버튼 추가

```vue
<u-button color="neutral" variant="outline" @click="actionPrint">
  <i class="i-heroicons-printer" />
  인쇄
</u-button>
```

---

## 생성 파일

```
front/src/modules-domain/[모듈명]/pages/
├── [원본]-print.vue           # 인쇄 전용 컴포넌트
└── _[모듈명]-print.routes.ts  # 인쇄 전용 라우트
```

---

## 참조 문서

- **[print-component.md](references/print-component.md)**: 인쇄 컴포넌트 템플릿
- **[print-routes.md](references/print-routes.md)**: 라우트 설정 템플릿
- **[print-design-guide.md](references/print-design-guide.md)**: 인쇄 디자인 상세 가이드

---

## 참조 코드

- `front/src/modules-domain/unpaid/pages/account-print.vue`
- `front/src/modules-domain/unpaid/pages/_unpaid-print.routes.ts`
- `front/src/assets/styles/components.css` (table_report)
