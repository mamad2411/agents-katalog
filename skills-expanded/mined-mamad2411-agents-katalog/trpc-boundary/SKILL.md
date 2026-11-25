---
name: trpc-boundary
label: tRPC boundary 변경
category: optional
order: 8
description: Use when you are changing tRPC contracts, app-router shape, or client and server import order across the shared boundary. Do not use for provider runtime layout, remote operations, or generic route and UI work.
---

# tRPC Boundary Skill

Cloudflare + tRPC 조합에서 client-server 경계를 수정할 때 사용하는 Skill입니다.

## Use when

- `packages/contracts`, `packages/app-router`, `server`, `frontend`, `backoffice` 순서로 변경을 전파할 때
- boundary type, router shape, client import 방향을 다시 맞춰야 할 때

## Do not use for

- Cloudflare Worker binding/runtime/layout 자체: `cloudflare-worker`
- MiniApp route/page/navigation 설계: `granite-routing`
- TDS UI 선택: `tds-ui`

## 읽는 순서

1. `references/change-flow.md`를 먼저 읽는다.
2. package 책임과 import boundary는 `docs/engineering/workspace-topology.md`를 같이 확인한다.

## 핵심 원칙

- boundary shape는 `packages/contracts`
- router shape와 `AppRouter`는 `packages/app-router`
- consumer는 shared package root import만 사용하고 서로를 직접 참조하지 않는다.
- provider runtime layout이나 원격 작업 절차는 여기서 설명하지 말고 해당 provider skill로 넘긴다.
