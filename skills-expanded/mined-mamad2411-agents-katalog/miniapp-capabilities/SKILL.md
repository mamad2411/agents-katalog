---
name: miniapp-capabilities
label: MiniApp capability / 공식 API 탐색
category: core
order: 1
description: Use when you need MiniApp or AppInToss capability lookup, official API discovery, or pre-implementation capability checks. Do not use for route design, navigation structure, or TDS component choice.
---

# MiniApp Capabilities Skill

이 Skill은 MiniApp 기능의 존재 여부와 공식 API를 확인할 때 가장 먼저 씁니다.

## Use when

- 필요한 기능이 MiniApp framework나 Granite에서 공식 지원되는지 확인할 때
- 권한, 로딩, 에러, analytics 체크가 필요한 기능인지 빠르게 점검할 때
- 공식 문서 진입점과 API 카탈로그를 함께 보고 싶을 때

## Do not use for

- route path, page entry, navigation 설계: `granite-routing`
- TDS component 선택과 UI boundary: `tds-ui`
- provider runtime layout이나 server 연결 상태 점검: provider skill

## 읽는 순서

1. `references/feature-map.md`에서 필요한 기능 축이 존재하는지 먼저 찾는다.
2. 정확한 URL, 타입, 에러, 제약은 `references/full-index.md`에서 확인한다.
3. 라우팅, import, UI boundary 같은 강제 규칙은 `../shared/references/frontend-policy.md`를 따른다.
4. 페이지/route 설계는 `granite-routing`, UI 컴포넌트 선택은 `tds-ui`로 넘긴다.

## 구현 전 체크

- 공식 공개 문서 링크를 다시 열었는가
- permission, loading, error, analytics 요구를 확인했는가
- unsupported platform 또는 구버전 fallback이 필요한가
- import source가 `@apps-in-toss/framework`인지 `@granite-js/*`인지 확인했는가

## 산출물 기대

- `Plan`에 참고한 framework/Granite 문서와 체크 포인트가 남아 있어야 한다.
- 기능 존재 여부만 확인한 상태에서 바로 구현하지 말고, 원문 시그니처와 제약을 최종 확인한다.
