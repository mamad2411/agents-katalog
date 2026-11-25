---
name: vue-mvvm-arch
description: Vue/Nuxt 프론트엔드의 MVVM 아키텍처 규칙. View/composable 분리, Vue Query 컴포저블 래핑 + Query Key Factory, 캐시 무효화 범위 판단, Modal/Domain/Base 3계층 컴포넌트 품질 기준, SSR/CSR 데이터 페칭 선택. 프론트 기능 개발, 컴포넌트 설계, 데이터 페칭 전략, 캐시 무효화 결정 시 사용.
---

# Vue MVVM Architecture

운영 서비스(Vue 3 + Nuxt SSR/CSR 혼합)에서 다듬어진 프론트 아키텍처 규칙. 핵심 경계: **View는 데이터 페칭 라이브러리를 모른다** — 페이지가 Vue Query에 직접 의존하는 순간 페칭 전략 변경이 전 페이지 수정이 된다.

## MVVM 핵심 규칙

1. **View(Page)는 UI만.** 비즈니스 로직·API 호출은 composable에서. View 안 `await $api.service.save()`는 위반.
2. **Modal은 순수 View.** props로 데이터 수신, emit으로 액션 전달. Modal 내부 API 호출 금지 — 부모의 composable이 비즈니스 로직을 소유.
3. **Vue Query는 composable로 래핑.** 페이지/컴포넌트에서 `useQuery`/`useMutation` 직접 사용 금지. 상세: [references/query-composable.md](references/query-composable.md)
4. **CSR 라우터 컴포넌트는 동적 import.** `const Foo = () => import('@/views/...')` — 정적 import는 초기 번들에 전부 포함된다.

## References index

| File | Read when |
|---|---|
| [references/query-composable.md](references/query-composable.md) | 데이터 페칭 코드 작성 — Query Key Factory, 캐시 무효화 범위 매트릭스 |
| [references/component-quality.md](references/component-quality.md) | 컴포넌트 설계/리뷰 — Modal/Domain/Base 3계층 품질 기준, 분리 판단 |
| [references/ssr-csr-patterns.md](references/ssr-csr-patterns.md) | SSR(Nuxt) vs CSR 앱별 페칭·라우팅·상태관리 선택 |
| [references/vue-component-rules.md](references/vue-component-rules.md) | Vue 컴포넌트 공통 규칙 — script setup, watch 지양, 스타일, eventBus |
| [references/ssr-memory-safety.md](references/ssr-memory-safety.md) | SSR 페이지/composable 작성 — 사이드 이펙트 정리, 모듈 스코프 상태, hydration mismatch |
| [references/file-organization.md](references/file-organization.md) | 새 파일 생성 — 컴포넌트/composable/타입/문서 배치와 명명, 수정 vs 생성 판단 |
