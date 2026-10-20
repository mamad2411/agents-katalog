---
description: E2E Check — Playwright MCP로 핵심 사용자 플로우를 자동 검증한다.
---

# E2E Check

핵심 사용자 플로우를 Playwright MCP로 자동 검증하고 성공/실패 리포트를 생성한다.

## 사용법

```
/e2e-check [flow]
```

`flow` 생략 시 전체 플로우를 순서대로 실행한다.

| flow 인자 | 검증 내용 |
|-----------|----------|
| `query` | 자연어 쿼리 입력 → 결과 표시 |
| `query-types` | 다양한 쿼리 타입 (타율, 비교, 시즌별) |
| `error-handling` | 에러 처리 (빈 쿼리, 무의미한 입력) |
| `responsive` | 반응형 UI (모바일/태블릿/데스크탑) |

예시:
- `/e2e-check` — 전체 플로우
- `/e2e-check query` — 쿼리 플로우만

## 전제조건

- Playwright MCP 활성화
- 프론트엔드 dev server: `cd frontend && npm run dev`
- 백엔드 dev server: `cd backend && uvicorn app.main:app --reload`
- PostgreSQL 실행 중

Use the **e2e-runner** agent for this task. Delegate all work to the agent now.
