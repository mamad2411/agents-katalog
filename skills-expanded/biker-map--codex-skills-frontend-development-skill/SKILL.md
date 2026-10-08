---
name: biker-map-frontend-development
description: Use when working on Biker Map web frontend UI, FSD structure, TanStack Query, react-hook-form, Zod validation, Supabase client boundaries, toast, and optimistic updates.
metadata:
  short-description: Web frontend guidance
---

# Frontend Development Skill

<strong>버전 : </strong> v2.2

<strong>생성 날짜 : </strong> 2026-05-21

<strong>최신 업데이트 날짜 : </strong> 2026-06-25

이 skill은 Biker Map의 프론트엔드 구현 컨벤션을 따를 때 사용합니다.

## 사용 시점

다음 작업을 할 때 이 skill을 사용합니다.

- `web` client component, page, widget, feature 구현
- TanStack Query query/mutation hook 작성
- `react-hook-form` + `zod` 기반 form 검증 셋업
- form, env, API payload Zod 검증
- Supabase browser/realtime/API client 경계 확인
- toast, optimistic update, cache invalidation 설계
- FSD 구조에서 entity, feature, widget 조합 기준 확인

## 먼저 읽을 문서

- TanStack Query 서버 상태 관리: `.codex/skills/frontend-development/tanstack-query.md`
- Zod 검증 규칙: `.codex/skills/frontend-development/zod.md`
- Supabase client 사용 규칙: `.codex/skills/frontend-development/supabase-client.md`
- 지도 사이드패널 Parallel Route 기준: `.codex/skills/frontend-development/map-panel-parallel-route.md`
- auth 플로우 테스트: `.codex/skills/frontend-development/auth-flow-test-plan.md`

## 공통 전제

이 섹션은 같은 폴더의 세부 문서가 반복해서 적지 않는 프론트엔드 공통 전제입니다.

### FSD 경계

- `entities`는 도메인 데이터와 도메인 UI를 둡니다.
- `features`는 사용자 액션 단위 기능을 둡니다.
- `widgets`는 여러 entity와 feature를 조합한 화면 블록을 둡니다.
- 댓글, 반응, 즐겨찾기처럼 함께 쓰이는 기능은 세부 feature를 분리하되 화면에서는 widget에서 조합합니다.

### Server Action

- Next.js Server Action은 사용자 액션의 서버 실행 entrypoint로 보고 `features/{feature}/actions` 하위에 둡니다.
- `"use server"` boundary, form submit 처리, redirect, cookie, server-side auth 호출은 `model`이 아니라 `actions`에서 시작합니다.
- `model`에는 schema, mapper, hook, 상태, 클라이언트/서버 공용 도메인 로직을 둡니다.
- Server Action에서 사용하는 Zod schema나 순수 helper는 재사용성이 있으면 `model`로 분리하고, action 파일에서는 흐름 조합만 담당하게 합니다.
- `react-hook-form` + `zodResolver`를 쓰는 form과 Server Action을 함께 쓰더라도, action 내부 parse는 최종 방어선으로 유지합니다.
- 다만 action state는 입력 validation 채널이 아니라 서버 에러 채널로만 사용합니다. action state 필드는 `message` 같은 범용 이름보다 `serverError` 의미를 우선합니다.
- action 내부 parse 실패는 RHF field error를 대체하는 UI 채널로 다시 노출하지 않습니다. 사용자가 정상 흐름에서 보게 되는 입력 에러는 RHF가 담당하고, action state는 인증 실패, 중복 이메일, 자동 로그인 실패 같은 서버 결과만 다룹니다.

### Server State

- API 응답 데이터, 로딩, 에러, 캐시, invalidation은 TanStack Query가 담당합니다.
- query hook과 mutation hook은 도메인별 model에 분리합니다.
- mutation 성공/실패 피드백은 가능한 mutation hook의 `onSuccess`, `onError`에서 처리합니다.
- reaction, favorite처럼 즉시 반응성이 필요한 기능은 optimistic update를 우선 검토합니다.

### Runtime Validation

- TypeScript 타입만으로 외부 입력을 신뢰하지 않습니다.
- API body, form input, env, 불확실한 error payload는 Zod로 런타임 검증합니다.
- form input은 가능한 한 클라이언트에서 먼저 검증하고, validation 실패 시 mutation, fetch, server action, BFF request를 호출하지 않습니다.
- BFF route의 validation은 유지합니다. 클라이언트 validation은 서버 validation을 대체하지 않고, 잘못된 요청을 미리 차단하는 첫 번째 방어선입니다.
- form UI는 `react-hook-form`을 기본값으로 보고, `zodResolver`를 붙여 schema와 에러 메시지를 단일 source로 관리합니다.
- schema는 feature `model`에 두고, UI는 `useForm`과 field component 조합에 집중하게 분리합니다.
- Server Action과 함께 쓰는 form에서도 field validation은 RHF가 전부 담당합니다. action state는 form-level server error만 렌더링하고, validation 에러를 다시 싣지 않습니다.
- ZodError 내부 구조를 사용자 응답에 그대로 노출하지 않습니다.

### Supabase Boundary

- 클라이언트 컴포넌트는 service role을 절대 사용하지 않습니다.
- 일반 데이터 접근과 비용성 외부 API 호출은 BFF API route를 통합니다.
- Realtime 수신 후 nav, dropdown처럼 즉시성이 필요한 UI는 query cache 직접 갱신을 우선 검토합니다.

### Test

- Playwright `test.describe()`와 `test()` 설명은 사용자가 결과를 읽기 쉽도록 한글로 작성합니다.
- E2E 파일명은 도구 호환성과 git 출력 가독성을 위해 영어 kebab-case를 사용합니다.
- 인증, 회원가입, refresh, Realtime처럼 DB/Auth 데이터를 생성하는 테스트는 개발/운영 Supabase를 직접 사용하지 않습니다.
- DB 오염 방지를 위해 실제 Supabase Auth 흐름이 필요한 테스트는 Supabase local stack과 테스트 fixture를 기준으로 작성합니다.
- Supabase local 테스트는 `supabase db reset`으로 재현 가능한 상태를 만든 뒤 실행하고, DBeaver 확인은 local DB 포트에만 연결합니다.

## 세부 문서 역할

- `.codex/skills/frontend-development/tanstack-query.md`: query/mutation hook, toast, optimistic update, cache 기준입니다.
- `.codex/skills/frontend-development/zod.md`: API/form/env/error payload 런타임 검증 기준입니다.
- `.codex/skills/frontend-development/supabase-client.md`: Supabase client 종류, env, browser/server 경계 기준입니다.
- `.codex/skills/frontend-development/map-panel-parallel-route.md`: 지도 `@panel` parallel route, route-local UI, `/map/list` path 기준입니다.
- `.codex/skills/frontend-development/auth-flow-test-plan.md`: 인증 E2E 우선순위, Supabase local 테스트 DB, DBeaver 확인 기준입니다.
- `.codex/skills/bff-development/bff.md`: API route authorization과 response contract의 source of truth입니다.
- `.codex/skills/db-engineering/SKILL.md`: RLS, baseline, service role 공통 전제의 source of truth입니다.
