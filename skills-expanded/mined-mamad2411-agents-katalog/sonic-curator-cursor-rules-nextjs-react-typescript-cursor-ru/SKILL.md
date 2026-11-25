---
globs: **/*.ts,**/*.tsx
alwaysApply: true
---

# Next 컴포넌트 작성 규칙

1. 컴포넌트 작성 시 서버 컴포넌트를 기본
2. 상호작용이 필요한 컴포넌트는 클라이언트 컴포넌트로 작성하며, `layout.tsx`와 `page.tsx`에 `"use client`를 추가하지 말고 컴포넌트를 분리

# React 작성 규칙

1. `useCallback` 사용 금지
2. `useMemo`는 데이터 크기가 클 것이 예상되는 부분에서만 제한적으로 사용
3. 이벤트 핸들러: prop 이름은 `on + <동작> + <대상>`, prop으로 전달하는 핸들러는 `handle + <동작> + <대상>`으로 작성
```tsx
// DON'T
const App = () => {
  const onChangeDate = () => {};
  const onDateChange = () => {};

  return <DatePicker onChange={onChangeDate}>
}

// DO
const App = () => {
  const handleChangeDate = () => {};

  return <DatePicker onChange={handleChangeDate}>
}
```
