---
name: granite-routing
label: route / page / navigation 패턴
category: core
order: 2
description: Use when you are changing Granite route paths, page entries, params, or navigation flow in the MiniApp frontend. Do not use for capability lookup, provider runtime work, or TDS component selection.
---

# Granite Routing Skill

이 Skill은 `frontend`의 route, page entry, navigation 흐름을 설계하거나 수정할 때 사용합니다.

## Use when

- route path, page file, params 설계를 결정할 때
- `createRoute`, `validateParams`, navigation usage 예시가 필요할 때
- entry layer와 implementation layer를 어떻게 나눌지 정할 때

## Do not use for

- MiniApp capability / 공식 API 탐색: `miniapp-capabilities`
- TDS component 선택과 UI boundary: `tds-ui`
- tRPC contract/app-router 변경 순서: `trpc-boundary`

## 읽는 순서

1. `references/patterns.md`에서 route/page/navigation 패턴을 확인한다.
2. 강제 규칙과 금지 import는 `../shared/references/frontend-policy.md`를 기준으로 본다.
3. 기능 존재 여부는 `miniapp-capabilities`, UI 선택은 `tds-ui`로 넘긴다.

## 핵심 원칙

- 규칙은 `../shared/references/frontend-policy.md`가 소유한다.
- 이 Skill은 구현 패턴과 예시를 제공하고, 규칙의 근거 문서를 대체하지 않는다.
- route 설계 전에는 entry file, impl file, params 흐름, `router.gen.ts` 동기화까지 같이 본다.
