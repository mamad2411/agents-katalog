---
name: zustand-use
description: (heropy) React 프로젝트에서 Zustand(주스탠드)로 전역 상태(스토어)를 설계, 작성할 때 사용한다. 사용자가 "zustand", "주스탠드", "전역 상태", "스토어 분리", "스토어 생성", "스토어 만들어 줘", "OO 스토어 생성", "상태 관리 라이브러리", "create 함수", "useShallow", "persist/immer/devtools 미들웨어"를 언급하거나, React 컴포넌트 간 prop drilling을 해소하려 할 때 반드시 이 스킬을 따른다. 스토어 정의 패턴(액션 분리, 초기화, 삭제), 선택자 사용 규칙, 미들웨어 합성 순서, TypeScript 작성법, 트리거 입력으로 스토어 파일을 자동 생성하는 절차까지 포함한다.
model: haiku
effort: max
metadata:
  author: ParkYoungWoong
  version: 1.0.2
---

# Zustand 사용 가이드

> 참고: https://www.heropy.dev/p/n74Tgc

Zustand는 작고 빠른 React 상태 관리 라이브러리다. `create` 함수 하나로 State와 Action을 통합 정의하고, Provider 없이 클로저 기반으로 동작하며, 선택자(Selector)로 부분 상태만 구독해 불필요한 리렌더링을 피한다. 이 스킬은 사용자가 Zustand로 스토어를 작성할 때 따라야 하는 패턴·관례·주의점을 모은다.

## 핵심 원칙 (먼저 읽기)

1. **스토어 파일은 `src/store/<이름>.ts` 한 파일에 정의한다.** Redux처럼 슬라이스/스토어/리듀서를 여러 파일로 쪼개지 않는다. 이게 Zustand를 쓰는 이유다.
2. **스토어 훅 명명은 `use이름Store`.** `use` 접두사 + `Store` 접미사. 예: `useCountStore`, `useUserStore`.
3. **컴포넌트에서는 선택자 함수로 "하나의 상태(또는 액션)"만 꺼낸다.** 객체 통째로 꺼내면 무관한 상태 변경에도 리렌더링된다.
4. **여러 값을 한 번에 꺼낼 때는 반드시 `useShallow`** (`zustand/shallow`)로 감싼다. 그냥 객체/배열을 반환하면 매 렌더마다 새 참조라, React가 `getSnapshot should be cached to avoid an infinite loop` 경고를 띄우며 리렌더링이 반복된다.
5. **액션은 `actions` 객체로 모아둔다.** 컴포넌트가 액션 묶음을 한 번에 가져오기 쉽고, 상태 초기화 시 액션을 분리해 다루기 좋다. 단, `persist` 미들웨어를 쓸 때는 `actions`가 JSON 직렬화되지 않으므로 이 구조를 풀어야 한다(아래 [스토리지](#persist--스토리지에-상태-저장) 참고).
6. **TypeScript는 두 가지 방식.** 직접 타입 작성(`create<State & Actions>()`) 또는 `combine` 미들웨어로 추론. 새 스토어는 우선 `combine` + `immer` 조합을 기본으로 검토한다.

## 스토어 파일 자동 생성 (트리거 입력)

사용자가 **"OO 스토어 생성"**, **"OO 스토어 만들어 줘"** 처럼 스토어 이름과 생성 의도를 함께 말하면(예: "count 스토어 생성", "user 스토어 만들어 줘", "장바구니 스토어 생성"), 아래 절차로 **스토어 파일을 직접 만든다**. 코드 설명만 하지 말고 실제로 파일을 생성하라.

### 절차

1. **이름 정규화.** 트리거에서 스토어 이름을 뽑아 카멜케이스로 만든다. 파일명은 그 이름, 훅 이름은 `use` + PascalCase + `Store`.
   - `count` 스토어 생성 → 파일 `count`, 훅 `useCountStore`
   - `user profile` 스토어 → 파일 `userProfile`, 훅 `useUserProfileStore`
   - 한국어 이름이면 영문으로 옮긴다("장바구니" → `cart`). 적절한 영문이 모호하면 사용자에게 확인한다.

2. **언어 판별.** 프로젝트 루트(또는 가까운 상위)에 `tsconfig.json`이 있거나 `src` 아래 `.ts`/`.tsx` 파일이 있으면 **TypeScript**, 아니면 **JavaScript**로 본다. TypeScript면 확장자 `.ts`, 아니면 `.js`.

3. **스토어 폴더 탐색.** 다음 순서로 기존 폴더를 찾아 거기에 생성한다: `src/store` → `src/stores` → `src/state`. 모두 없으면 **`src/store`를 새로 만들어** 거기에 생성한다. (`src`가 없는 비표준 구조면 사용자에게 위치를 확인한다.)

4. **충돌 확인.** 같은 이름의 파일이 이미 있으면 덮어쓰지 말고 사용자에게 알린다.

5. **템플릿 작성.** 아래 기본 템플릿(언어별)을 채워 파일을 만든다. 생성 후 파일 경로와 훅 이름을 한 줄로 보고한다.

### 기본 템플릿 (TypeScript) - `combine` 사용

TypeScript 프로젝트는 타입을 직접 쓰지 않고 `combine`으로 추론시키는 것을 기본으로 한다.

```ts
import { create } from 'zustand'
import { combine } from 'zustand/middleware'

export const useCountStore = create(
  combine(
    {
      count: 0
    },
    () => ({
      increase() {}
    })
  )
)
```

### 기본 템플릿 (JavaScript)

JavaScript에는 추론할 타입이 없으므로 `combine` 없이 순수 `create`로 만든다.

```js
import { create } from 'zustand'

export const useCountStore = create(() => ({
  count: 0,
  increase() {}
}))
```

## 설치

```bash
npm i zustand
```

선택적 피어 의존성:

```bash
# Immer 미들웨어를 쓸 때
npm i immer

# 상태 삭제(omit) 패턴을 쓸 때
npm i lodash-es
npm i -D @types/lodash-es
```

v5는 `use-sync-external-store`가 피어 의존성으로 바뀌었다. React 18+ 환경에서는 별도 설치 없이 동작하나, 특정 환경에서 누락 경고가 뜨면 직접 설치한다.


## 스토어 작성 패턴

### 가장 단순한 형태

```ts --path=/src/store/count.ts
import { create } from 'zustand'

export const useCountStore = create<{
  count: number
  increase: () => void
  decrease: () => void
}>(set => ({
  count: 1,
  increase: () => set(state => ({ count: state.count + 1 })),
  decrease: () => set(state => ({ count: state.count - 1 }))
}))
```

- `create<타입>()` 제네릭으로 상태·액션 타입을 동시에 전달한다.
- `set`은 부분 상태 객체를 받아 **병합**한다. 콜백 형태 `set(state => ({...}))`를 쓰면 현재 상태 기반 갱신이 안전하다.
- `get`은 액션 내부에서 현재 스토어 객체(상태+액션)를 얻을 때 사용한다. 단순 갱신에는 `set` 콜백이 더 간결하다.

### 액션 분리 (`actions` 객체) — 권장 기본형

여러 컴포넌트가 단일 스토어의 액션을 자주 호출하면, 액션을 `actions` 한 객체로 묶는다. 컴포넌트가 `state => state.actions`로 액션 묶음만 가져오면 액션 참조는 변하지 않으므로 리렌더링도 발생하지 않는다.

```ts --path=/src/store/count.ts
import { create } from 'zustand'

interface State {
  count: number
}
interface Actions {
  actions: {
    increase: () => void
    decrease: () => void
  }
}

export const useCountStore = create<State & Actions>(set => ({
  count: 1,
  actions: {
    increase: () => set(state => ({ count: state.count + 1 })),
    decrease: () => set(state => ({ count: state.count - 1 }))
  }
}))
```

```tsx --path=/src/App.tsx
const count = useCountStore(state => state.count)
const { increase, decrease } = useCountStore(state => state.actions)
```

### 상태 초기화 (`resetState`)

상태와 액션 타입을 분리하고, `initialState`를 변수로 빼서 액션을 통해 되돌린다. 액션을 포함해 통째로 `set`하지 않도록 주의(액션이 사라진다).

```ts --path=/src/store/count.ts
const initialState: State = { count: 1, double: 2, min: 0, max: 99 }

export const useCountStore = create<State & Actions>(set => ({
  ...initialState,
  actions: {
    increase: () => set(state => ({ count: state.count + 1 })),
    decrease: () => set(state => ({ count: state.count - 1 })),
    resetState: keys => {
      if (!keys) {
        set(initialState)        // 전체 초기화
        return
      }
      keys.forEach(key => {      // 일부 키만 초기화
        set({ [key]: initialState[key] })
      })
    }
  }
}))
```

### 상태 삭제 (`set(..., true)` + `omit`)

`set` 함수의 두 번째 인수(기본값 `false`)에 `true`를 전달하면 병합하지 않고 **덮어쓴다**. `lodash-es`의 `omit`과 조합해 특정 키를 삭제한다.

```ts --path=/src/store/count.ts
import { omit } from 'lodash-es'

deleteState: keys => {
  set(state => omit(state, keys), true)
}
```

> 주의: `true`로 덮어쓰면 액션까지 사라질 수 있다. `actions` 객체로 분리해 두고 `keys`에 절대 `'actions'`를 포함하지 않도록 한다.


## 컴포넌트에서 사용하기

### 한 번에 하나씩 꺼낸다 (기본)

```tsx
const count = useCountStore(state => state.count)
const increase = useCountStore(state => state.actions.increase)
```

### 절대 하면 안 되는 패턴

```tsx
// ❌ 스토어 객체 전체를 받아오면 무관한 상태가 변경돼도 리렌더링됨
const store = useCountStore()
return <h2>{store.count}</h2>

// ❌ 선택자가 매번 새 객체를 반환 → React 경고(getSnapshot should be cached…) + 리렌더링 반복
const { count, increase } = useCountStore(state => ({
  count: state.count,
  increase: state.actions.increase
}))
```

### 여러 값을 한 번에: `useShallow`

`zustand/shallow`의 `useShallow`로 감싸 객체나 배열을 얕은 비교로 메모이즈한다.

```tsx
import { useShallow } from 'zustand/shallow'

// 객체 반환
const { count, increase, decrease } = useCountStore(
  useShallow(state => ({
    count: state.count,
    increase: state.actions.increase,
    decrease: state.actions.decrease
  }))
)

// 배열 반환 (구조 분해와 잘 맞음)
const [count, increase, decrease] = useCountStore(
  useShallow(state => [state.count, state.actions.increase, state.actions.decrease])
)
```


## 미들웨어

스토어는 미들웨어로 기능을 확장한다. 공식 문서는 합성 순서가 중요하지 않다고 제안하지만, `combine` 미들웨어를 가장 안쪽에 두고 `devtools` 미들웨어를 가장 바깥에 두는 것이 권장된다.

```ts
// 단일
create(미들웨어(콜백))

// 다중 — 안에서 바깥 순으로 적용된다
create(devtools(persist(subscribeWithSelector(immer(combine(state, actions))))))
```

### `combine` — 상태 타입 추론

타입을 직접 쓰지 않고 추론시키고 싶을 때.

```ts --path=/src/store/count.ts
import { create } from 'zustand'
import { combine } from 'zustand/middleware'

const initialState = { count: 1, double: 2, min: 0, max: 99 }

export const useCountStore = create(
  combine(initialState, set => ({
    actions: {
      increase: () => set(state => ({ count: state.count + 1 })),
      decrease: () => set(state => ({ count: state.count - 1 }))
    }
  }))
)
```

추론되지 않는 값은 `satisfies` / `as`로 명시한다.

```ts
type User = { email: string; displayName: string; isValid: boolean } | null

const initialState = {
  user: null satisfies User as User,
  isLoggedIn: false
}
```

#### 주의: `combine`에서는 `get()`이 액션 타입을 추론하지 못한다

`combine` 사용 중 액션 안에서 다른 액션을 호출해야 하면, `get().actions.xxx()`가 타입 에러를 낸다. **함수 호이스팅**을 활용해 액션을 별도 함수로 뽑아 쓴다.

```ts
combine(initialState, set => {
  function increase() {
    set(state => ({ count: state.count + 1 }))
    increaseDouble()  // OK
  }
  function increaseDouble() {
    set(state => ({ double: state.count * 2 }))
  }
  return { actions: { increase, increaseDouble } }
})
```

### `immer` — 중첩 객체 변경

`user.relations[0].emails[0].domain`처럼 깊은 중첩 객체를 변경할 때 스프레드 지옥을 피한다.

```ts
import { immer } from 'zustand/middleware/immer'

export const useUserStore = create(
  immer<State & Actions>(set => ({
    ...initialState,
    actions: {
      setDisplayName: name => {
        set(state => {
          if (state.user) {
            state.user.displayName = name   // 직접 대입 가능
          }
        })
      }
    }
  }))
)
```

`combine`과 함께 쓸 때:

```ts
create(immer(combine(initialState, set => ({ /* ... */ }))))
```

### `subscribeWithSelector` — 특정 상태 변경 구독

스토어 외부에서 특정 상태만 감시하고 부수효과를 수행한다. 계산된 상태(Computed) 패턴에 유용하다.

```ts --path=/src/store/count.ts
import { create } from 'zustand'
import { combine, subscribeWithSelector } from 'zustand/middleware'
import { immer } from 'zustand/middleware/immer'

const initialState = { count: 1, double: 2 }

export const useCountStore = create(
  subscribeWithSelector(
    immer(
      combine(initialState, set => ({
        actions: {
          increase: () => set(state => { state.count += 1 }),
          decrease: () => set(state => { state.count -= 1 })
        }
      }))
    )
  )
)

// 모듈 최상위에서 구독 (앱 시작 시 1회)
useCountStore.subscribe(
  state => state.count,          // Selector
  count => {                     // Listener
    useCountStore.setState({ double: count * 2 })
  }
)
```

컴포넌트 내부에서만 구독할 때는 `useEffect`에서 시작·해제한다.

```tsx
useEffect(() => {
  const unsubscribe = useCountStore.subscribe(
    state => state.count,
    count => setDouble(count * 2)
  )
  return unsubscribe
}, [])
```

### `persist` — 스토리지에 상태 저장

`name`은 필수. 기본은 `localStorage`, `createJSONStorage(() => sessionStorage)`로 변경할 수 있다.

```ts
import {
  combine,
  subscribeWithSelector,
  persist,
  createJSONStorage
} from 'zustand/middleware'
import { immer } from 'zustand/middleware/immer'

export const useCountStore = create(
  persist(
    subscribeWithSelector(
      immer(
        combine(initialState, set => ({
          // ⚠️ persist에서는 액션을 actions 객체로 묶지 말 것
          increase: () => set(state => { state.count += 1 }),
          decrease: () => set(state => { state.count -= 1 })
        }))
      )
    ),
    {
      name: 'countStore'
      // storage: createJSONStorage(() => sessionStorage)
    }
  )
)
```

> **중요**: `persist`는 JSON 직렬화가 불가능한 값을 저장하지 못한다. `actions` 객체에 함수만 있으면 빈 객체 `{}`로 저장되어 새로고침 후 액션이 사라진다. `persist`를 쓸 때는 액션 분리 패턴을 **풀어서** 액션을 상태 객체의 최상위 속성으로 둔다. 함수는 코드에서 새로 정의되니 영향이 없다(저장되는 건 상태 값뿐).

### `devtools` — Redux DevTools

크롬 확장 [Redux DevTools](https://chromewebstore.google.com/detail/redux-devtools/lmhkpmbekcpmknklioeibfkpmmfibljd)로 상태 추적. 가장 바깥에 둔다.

```ts
import { devtools } from 'zustand/middleware'

export const useCountStore = create(
  devtools(
    persist(
      subscribeWithSelector(
        immer(combine(initialState, set => ({ /* ... */ })))
      ),
      { name: 'countStore' }
    )
  )
)
```


## 비동기 / 컴포넌트 외부 사용

스토어 훅에는 정적 메서드가 있다.

```ts
useCountStore.getState()                 // 현재 상태(액션 포함)
useCountStore.setState({ count: 0 })     // 외부에서 상태 변경
useCountStore.subscribe(listener)        // 구독
```

API 호출 같은 비동기 로직은 그냥 액션 안에서 `async` 함수로 작성한다. 별도 미들웨어 불필요.

```ts
actions: {
  fetchUser: async (id: string) => {
    const res = await fetch(`/api/users/${id}`)
    const user = await res.json()
    set({ user })
  }
}
```


## 작성 체크리스트

새 스토어 또는 컴포넌트 사용 코드를 작성할 때 항상 검토:

- [ ] 파일 위치는 `src/store/<이름>.ts`, 훅 이름은 `use이름Store`
- [ ] 컴포넌트에서 `useStore()`로 객체 전체를 받지 않는다
- [ ] 다중 선택은 `useShallow`로 감싼다
- [ ] 액션을 자주 함께 쓰면 `actions: { ... }` 객체로 묶는다 (단, `persist` 사용 시는 풀어서 둔다)
- [ ] 미들웨어 합성 순서: `devtools(persist(subscribeWithSelector(immer(combine(...)))))`
- [ ] `combine` 사용 시 액션 간 호출은 함수 호이스팅으로 처리 (`get().actions.x()` 금지)
- [ ] 상태 초기화가 필요하면 `initialState` 변수 + `resetState` 액션 패턴
- [ ] `set(..., true)`로 덮어쓸 때 액션을 보존했는지 확인
- [ ] `persist`의 `name`은 프로젝트 내 유일하게


## 비교: Redux Toolkit vs Zustand 요약

| 항목 | Redux Toolkit | Zustand |
|---|---|---|
| Store 정의 | `createSlice` + `configureStore` 분리 | `create` 하나로 통합 |
| 액션/리듀서 | `reducers` 객체 + 별도 export | `set`을 쓰는 일반 함수 |
| 파일 구조 | 다수 파일 | 단일 파일 |
| 불변성 | Immer 내장(강제) | 직접 또는 `immer` 미들웨어 선택 |
| Provider | 필수 (Context) | 불필요 (클로저) |
| 선택적 구독 | `useSelector`에서 직접 구현 | 훅이 기본 제공 |
| 비동기 | `createAsyncThunk` / Saga | 액션 내 `async` |

Zustand를 선택했다는 건 "보일러플레이트를 줄이고 단일 파일로 끝낸다"는 결정이다. 그 결정을 코드에서도 유지하라.
