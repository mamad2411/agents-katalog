---
name: backoffice-react
label: backoffice React 작업
category: optional
order: 4
description: Use when you are changing the optional backoffice React/Vite workspace, its state flow, or bundle boundaries. Do not use for MiniApp route work, provider runtime layout, or tRPC contract order.
---

# Backoffice React Skill

`backoffice`를 수정할 때 사용하는 Skill입니다.

## Use when

- Vite 기반 `backoffice` 화면, state, async flow, render boundary를 수정할 때
- table/search/form처럼 브라우저 운영 화면을 나눠야 할 때
- bundle 크기나 lazy import 경계를 점검할 때

## Do not use for

- MiniApp capability 탐색: `miniapp-capabilities`
- Granite route/page/navigation 설계: `granite-routing`
- TDS UI 선택: `tds-ui`
- provider runtime layout, 원격 상태, client 연결 점검: provider skill

## 읽는 순서

1. `references/best-practices.md`를 먼저 읽는다.
2. 화면 역할과 import boundary는 `docs/engineering/workspace-topology.md`를 같이 확인한다.

## 체크 포인트

- state를 실제로 쓰는 곳 근처에 뒀는가
- `useEffect`를 동기화 용도로만 쓰고 있는가
- 검색/테이블/폼처럼 무거운 화면은 경계를 나눴는가
- 번들 큰 의존성은 lazy import 대상인지 봤는가
