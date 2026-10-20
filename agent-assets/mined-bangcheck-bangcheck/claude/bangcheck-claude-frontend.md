# Frontend Conventions

## Module Rules

- **`components/ui/`** — 도메인 무관 공유 UI (Button, Modal, Input, Tabs, Dropdown 등). 2개 이상 페이지에서 재사용 가능한 것만.
- **`features/{domain}/`** — 특정 도메인에서만 쓰는 컴포넌트·훅·로직 (예: `features/checklist/`). 도메인 밖에서 import 금지.
- **`app/`** — 라우트와 페이지. 비즈니스 로직 인라인 금지 — `features/`로 추출.

## 의존 방향

```
app → features → services → lib/api → (외부 HTTP)
                          ↘ types
        ↘ components/ui
        ↘ store (Zustand)
```

`lib/api`는 `store`를 import하지 않음 — `react-query-provider.tsx`에서 `configureApi`로 콜백 주입.

## 라우트와 타입

- 페이지 경로는 항상 `@/lib/routes`의 `ROUTES` 상수 사용. 리터럴 `'/login'` 직접 박지 말 것.
- 도메인 타입은 `@/types`에 정의하고 import. 인라인 interface 금지.

## API 호출

- 모든 API 호출은 `services/{domain}-service.ts` 함수 통해서만.
- 페이지에서 `axios.get` 직접 호출 금지.
- 응답 타입은 `ApiResponse<T>` 제너릭으로 명시.
