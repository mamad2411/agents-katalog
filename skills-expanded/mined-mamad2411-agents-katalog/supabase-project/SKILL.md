---
name: supabase-project
label: Supabase project 작업
category: optional
order: 6
description: Use when you need Supabase project layout, local dev context, or client connection checks. Do not use for remote db/functions apply procedures or unrelated UI and routing work.
---

# Supabase Project Skill

`server`가 Supabase workspace일 때 사용하는 Skill입니다.

## Use when

- Supabase workspace 표면, local dev 맥락, client 연결 파일을 확인할 때
- 작업 전에 현재 scaffold state와 env ownership을 읽어야 할 때
- DB/Edge Function 코드를 어디서 관리하는지 다시 확인할 때

## Do not use for

- remote `db:apply`, `functions:deploy`, seed 절차 실행
- MiniApp route/page/navigation 설계: `granite-routing`
- TDS UI 선택: `tds-ui`

## 읽는 순서

1. `server/.create-rn-miniapp/state.json`과 `server/README.md`를 먼저 확인한다.
2. `references/overview.md`를 본다.
3. 로컬 실행은 `references/local-dev.md`, client 연결은 `references/client-connection.md`, 문제 해결은 `references/troubleshooting.md`로 이동한다.
4. 구조/ownership 규칙은 `docs/engineering/workspace-topology.md`를 같이 확인한다.

## 체크 포인트

- state.json의 `remoteInitialization`이 현재 상황과 맞는가
- `frontend`/`backoffice`의 Supabase env와 project ref가 같은 대상을 가리키는가
- 원격 mutate 절차는 이 Skill에 적지 말고 `server/README.md`의 Remote Ops로 넘긴다.
