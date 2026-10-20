---
description: Fix UI — 사용자가 지정한 UI 문제를 스크린샷 → DOM 분석 → 코드 수정 → 재검증 순서로 해결한다.
---

# Fix UI

사용자가 지정한 UI 문제를 스크린샷 → DOM 분석 → 코드 수정 → 재검증 순서로 해결한다.

## 사용법

```
/fix-ui <문제 설명> [페이지 경로]
```

예시:
- `/fix-ui 모바일에서 결과 테이블이 잘려 보여`
- `/fix-ui 다크모드에서 텍스트가 안 보임`

## 전제조건

- Playwright MCP 활성화
- 프론트엔드 dev server 실행 중 (`npm run dev` in `frontend/`)

## 워크플로우

1. **현재 상태 캡처** — 문제 페이지 스크린샷
2. **DOM 분석** — 문제 영역 CSS/레이아웃 파악
3. **소스 수정** — 최소 범위 수정 적용
4. **재검증** — 수정 후 스크린샷으로 확인

The user's issue description: $ARGUMENTS

Use the **visual-qa** agent for this task with focus on the specific issue described above. Delegate all work to the agent now.
