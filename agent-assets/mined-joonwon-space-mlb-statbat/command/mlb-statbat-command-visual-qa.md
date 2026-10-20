---
description: Visual QA — AI가 직접 사이트에 접속해 UI 이슈를 탐지하고 수정 제안을 생성한다.
---

# Visual QA

AI가 직접 사이트에 접속해 UI 이슈를 탐지하고 수정 제안을 생성한다.

## 사용법

```
/visual-qa [페이지 경로]
```

예시:
- `/visual-qa` — 전체 페이지 검사
- `/visual-qa /stats` — 특정 페이지만 검사

## 전제조건

- Playwright MCP 활성화
- 프론트엔드 dev server: `cd frontend && npm run dev`

Use the **visual-qa** agent for this task. Delegate all work to the agent now.
