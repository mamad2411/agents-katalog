---
name: react-router-use
description: (heropy) Use when adding React Router (Data Mode) to an existing React (Vite/CSR) project, configuring routes/layouts/navigation, or implementing route-level features such as loaders, protected routes, dynamic segments, nested routing, 404 pages, lazy loading, page transition animations, or SPA hosting redirects (Vercel/Netlify/Firebase).
model: haiku
effort: max
metadata:
  author: ParkYoungWoong
  version: 1.0.0
---

# React Router (Data Mode) Use

> 참고: https://www.heropy.dev/p/9tesDt

기존 React(Vite/CSR) 프로젝트에 React Router 7.x **Data Mode**(`createBrowserRouter` + `RouterProvider`)를 도입하거나, 이미 react-router가 구성된 프로젝트에 라우트/레이아웃/내비게이션/Loader 등 부분 기능을 추가하는 스킬.

이 스킬은 **Data Mode** 기준이다. `<BrowserRouter><Routes><Route>`로 구성되는 Declarative Mode 또는 Remix 기반 Framework Mode(`@react-router/dev`)가 필요하면 이 스킬은 적합하지 않다.

## 필수 실행 체크리스트 (MANDATORY)

**스킬 시작 즉시, 아래 항목을 TodoWrite에 1:1로 등록한 뒤 순서대로 진행한다. 건너뛰기 금지.**

1. 프로젝트 상태 감지 (1단계)
2. 작업 모드 결정: 초기 도입 vs 기능 추가 (2단계)
3. `react-router` 설치 [미설치 시] (3단계)
4. 기본 라우터 골격 생성 [라우터 파일 없을 때] (4단계)
5. 사용자가 추가로 요청한 기능을 [기능 가이드](#기능-가이드) 섹션에서 찾아 적용 (5단계)
6. **최종 검증** — 1단계 감지 표를 다시 돌며 누락된 자동 적용 항목이 있으면 재실행 (6단계)

각 항목은 조건 충족 시 "skipped"로 완료 처리하되, **조건 판단 근거(파일/패키지 존재 여부)를 명시**한 뒤 넘어간다.

## 동작 흐름

### 1단계: 프로젝트 상태 감지

| 확인 대상 | 감지 방법 |
|-----------|-----------|
| React 프로젝트 | `package.json`의 `dependencies`에 `react` 존재 |
| TypeScript | `tsconfig.json` 또는 `tsconfig.app.json` 존재 |
| react-router 설치 | `package.json`의 `dependencies`에 `react-router` 존재 |
| `react-router-dom` 사용 여부 | `package.json`의 dependencies 또는 `src/` 소스에 `from 'react-router-dom'` 임포트 존재 (v6→v7 마이그레이션 감지용) |
| 라우터 파일 | `src/routes/index.tsx` 존재 여부 |
| 레이아웃 파일 | `src/routes/layouts/Default.tsx` 존재 여부 |
| 헤더 컴포넌트 | `src/components/TheHeader.tsx` 존재 여부 |
| `main.tsx` 렌더 구조 | `src/main.tsx`의 `createRoot(...).render(...)` 자식이 (a) 단순 `<App />`인지, (b) 이미 `<Router />`/`<RouterProvider>`가 연결되어 있는지, (c) 다른 Provider/Wrapper(ThemeProvider, ErrorBoundary, i18n 등)가 감싸고 있는지 |
| `@/*` 경로 별칭 | `tsconfig` 또는 `vite.config`에 `@/*` alias 존재 (이 스킬의 예제는 `@/components/...` 임포트 사용) |
| 패키지 매니저 | `pnpm-lock.yaml` → pnpm, `yarn.lock` → yarn, `bun.lockb`/`bun.lock` → bun, `package-lock.json` 또는 없음 → npm |

### 2단계: 작업 모드 결정

**초기 도입 모드** — `react-router` 미설치 **그리고** `react-router-dom` 미사용 **그리고** `src/routes/index.tsx` 없음:
1. 3단계로 `react-router`를 설치한다
2. 4단계로 기본 라우터 골격(`src/routes/index.tsx`, `src/routes/layouts/Default.tsx`, `src/components/TheHeader.tsx`, `src/routes/pages/Home.tsx`/`About.tsx`)을 자동 생성하고 `src/main.tsx`의 렌더 호출을 **surgical하게** 라우터 연결로 바꾼다(자세한 규칙은 4단계 `src/main.tsx` 절 참고)
3. 사용자가 추가로 요청한 기능만 5단계에서 적용한다

**기능 추가 모드** — `react-router` 이미 설치되어 있거나 라우터 파일이 이미 존재:
1. 3·4단계는 skipped로 처리한다 (조건 미충족)
2. 5단계에서 사용자 요청에 해당하는 기능 가이드만 골라 적용한다

**마이그레이션 모드** — 1단계 감지에서 `react-router-dom` 사용이 확인됨:
1. 사용자에게 v6 `react-router-dom` → v7 `react-router` 마이그레이션을 진행할지 **명시적으로 확인**한다. 동의 없이 임의로 임포트를 바꾸지 않는다.
2. 동의가 있으면, 모든 `from 'react-router-dom'` 임포트를 `from 'react-router'`로 일괄 변경하고 `react-router-dom`을 제거(`{pm} uninstall react-router-dom`)한 뒤 `react-router`를 설치한다. 그 외 기존 라우트 구조는 그대로 둔다.
3. 마이그레이션 후 사용자가 새로 요청한 기능만 5단계에서 적용한다.

> **이미 존재하는 파일은 덮어쓰지 않는다.** 기존 파일은 사용자가 명시적으로 변경을 요청한 부분만 최소한으로 수정한다.

### 3단계: react-router 설치 [조건: 미설치 시]

> v7부터는 `react-router-dom`을 사용하지 않는다. 항상 `react-router`만 설치한다.

명령:

    {pm} install react-router

`{pm}`은 1단계의 패키지 매니저 감지 결과(npm/pnpm/yarn/bun)로 대체한다.

### 4단계: 기본 라우터 골격 생성 [조건: 라우터 파일 없을 때]

다음 폴더/파일 구조를 생성한다. 이미 존재하는 파일은 건드리지 않는다.

```
src/
├─components/
│  └─TheHeader.tsx
├─routes/
│  ├─layouts/
│  │  └─Default.tsx
│  ├─pages/
│  │  ├─About.tsx
│  │  └─Home.tsx
│  └─index.tsx
└─main.tsx
```

각 파일의 초기 내용은 다음과 같다.

`src/routes/pages/Home.tsx`:

```tsx
export default function Home() {
  return <h1>Home</h1>
}
```

`src/routes/pages/About.tsx`:

```tsx
export default function About() {
  return <h1>About</h1>
}
```

`src/components/TheHeader.tsx` — `<Link>`/`<NavLink>`를 쓰면 페이지 이동 시 전체가 다시 로드되지 않고 필요한 부분만 업데이트된다:

```tsx
import { NavLink } from 'react-router'

const navigations = [
  { to: '/', label: 'Home' },
  { to: '/about', label: 'About' }
]

export default function TheHeader() {
  return (
    <header>
      <nav>
        {navigations.map(nav => (
          <NavLink
            key={nav.to}
            to={nav.to}>
            {nav.label}
          </NavLink>
        ))}
      </nav>
    </header>
  )
}
```

`src/routes/layouts/Default.tsx` — `<Outlet>` 자리에 자식 라우트가 렌더링된다. `<ScrollRestoration>`은 페이지 이동 시 스크롤 위치를 자동으로 처리한다:

```tsx
import { Outlet, ScrollRestoration } from 'react-router'
import TheHeader from '@/components/TheHeader'

export default function DefaultLayout() {
  return (
    <>
      <TheHeader />
      <Outlet />
      <ScrollRestoration />
    </>
  )
}
```

`src/routes/index.tsx` — 경로(`path`) 없이 `element`만 지정한 최상위 라우트의 `children`에 페이지 라우트를 둔다. 그러면 자식 라우트가 렌더링될 때 부모 `<DefaultLayout />`도 같이 렌더링된다:

```tsx
import { createBrowserRouter, RouterProvider } from 'react-router'
import DefaultLayout from './layouts/Default'
import Home from './pages/Home'
import About from './pages/About'

const router = createBrowserRouter([
  {
    element: <DefaultLayout />,
    children: [
      {
        path: '/',
        element: <Home />
      },
      {
        path: '/about',
        element: <About />
      }
    ]
  }
])

export default function Router() {
  return <RouterProvider router={router} />
}
```

`src/main.tsx` — **항상 이미 존재하는 파일이므로 전체를 덮어쓰지 않는다.** 1단계의 `main.tsx` 렌더 구조 감지 결과에 따라 다음과 같이 처리한다.

- **(a) 자식이 단순 `<App />`인 경우** (Vite 기본 템플릿) — `App` 임포트를 제거하고 `Router` 임포트를 추가한 뒤 렌더 자리의 `<App />`만 `<Router />`로 교체한다. `<StrictMode>` 등 기존 wrapper는 그대로 유지한다. `App.tsx`가 더 이상 어디에서도 사용되지 않으면 사용자에게 삭제 여부를 확인한 뒤 제거한다.
- **(b) 이미 `<Router />`/`<RouterProvider>`가 연결되어 있는 경우** — `main.tsx`는 건드리지 않는다.
- **(c) 다른 Provider/Wrapper(ThemeProvider, ErrorBoundary, i18n 등)가 `<App />`을 감싸고 있는 경우** — 임의로 손대지 말고 사용자에게 다음 두 가지 중 어떤 구조를 원하는지 확인한다.
  1. 기존 wrapper들 안에 `<Router />`를 그대로 끼워 넣어 wrapper → Router 순서를 유지
  2. `<Router />`를 가장 바깥으로 빼서 라우트별로 wrapper의 영향을 받지 않게 할지

원하는 결과 예시(가장 단순한 (a) 케이스):

```tsx
import { createRoot } from 'react-dom/client'
import Router from './routes'

createRoot(document.getElementById('root')!).render(
  <>
    <Router />
  </>
)
```

> `@/components/TheHeader` 임포트는 `@/*` 경로 별칭이 필요하다. 1단계 감지 결과 별칭이 없으면 임포트를 상대 경로(`../../components/TheHeader`)로 바꾸거나, 사용자에게 별칭 설정을 권유한다(별칭 설정은 별도 스캐폴딩 스킬의 책임이며, 이 스킬에서 자동으로 건드리지 않는다).

### 5단계: 사용자 요청에 따른 기능 적용

사용자가 명시적으로 추가 기능을 요청한 경우에만 [기능 가이드](#기능-가이드) 섹션에서 해당 항목을 찾아 적용한다. 요청이 없으면 기본 골격만 두고 종료한다.

요청과 기능의 매핑 예:

| 사용자 요청 예시 | 적용할 기능 |
|------------------|-------------|
| "/movies/:movieId 같은 동적 페이지 만들어 줘" | [동적 세그먼트](#동적-세그먼트) |
| "검색 결과를 모달로 띄우고 싶어" / "중첩 라우트로 처리" | [중첩 라우팅](#중첩-라우팅) |
| "404 페이지 만들어 줘" | [찾을 수 없는 페이지](#찾을-수-없는-페이지) |
| "로그인한 사용자만 접근하게 해 줘" / "Protected Route" | [보호된 경로](#보호된-경로) |
| "초기 로딩 줄이게 코드 스플리팅" / "lazy 적용" | [페이지 지연 로딩](#페이지-지연-로딩) |
| "페이지 바뀔 때 페이드 효과" | [페이지 전환 애니메이션](#페이지-전환-애니메이션) |
| "Vercel/Netlify/Firebase 배포 시 새로고침에서 404" | [배포 설정](#배포-설정) |
| "NavLink 활성 스타일 / end / caseSensitive" | [NavLink 활용](#navlink-활용) |
| "프로그래밍 방식으로 페이지 이동" | [useNavigate / Navigate / redirect](#usenavigate--navigate--redirect) |
| "Declarative/Framework 모드 차이" | [모드 비교](#모드-비교) |

### 6단계: 최종 검증 (MANDATORY)

모든 단계 수행 후, 1단계의 감지 표를 **다시 한 번 스캔**해 다음을 확인한다.

- [ ] **초기 도입 모드였던 경우:** `package.json`에 `react-router` 존재, `src/routes/index.tsx`, `src/routes/layouts/Default.tsx`, `src/components/TheHeader.tsx`, `src/routes/pages/Home.tsx`/`About.tsx` 존재, `src/main.tsx`가 `<Router />`를 렌더링하고 기존의 wrapper(`<StrictMode>` 등)는 보존됨
- [ ] **마이그레이션 모드였던 경우:** `package.json`에서 `react-router-dom`이 제거되고 `react-router`가 추가됨, `src/`의 어느 파일에도 `from 'react-router-dom'` 임포트가 남아 있지 않음
- [ ] **모든 모드 공통:** 사용자가 명시적으로 요청한 기능별 가이드의 결과 파일(예: `src/routes/loaders/requiresAuth.ts`)이 모두 존재하고, 라우트 트리에 올바르게 연결됨
- [ ] 사용자가 별도로 요청하지 않은 영역의 기존 파일은 수정되지 않음 (특히 기존 `main.tsx`의 커스텀 Provider/Wrapper가 보존됨)

**누락 항목이 있으면 해당 단계로 돌아가 즉시 보완한다.** 검증 통과 전에는 작업 종료 금지.

---

## 기능 가이드

사용자가 명시적으로 요청한 기능만 골라 적용한다. 각 항목의 변경 사항은 누적되도록 설계되어 있으므로, 이미 다른 항목이 적용된 상태에서 추가로 적용해도 충돌하지 않는다.

### 모드 비교

React Router는 선언적(Declarative), 데이터(Data), 프레임워크(Framework)의 3가지 모드를 제공하며 기능이 누적적으로 확장된다. 이 스킬은 **Data 모드**를 기준으로 한다.

- **Declarative 모드** — `<BrowserRouter><Routes><Route>` 기반. 가장 기본적인 API. 단순한 SPA에 적합.
- **Data 모드** — `createBrowserRouter` + `RouterProvider`. Loader/Action/Fetcher 등 데이터 기능 추가. 좀 더 복잡한 CSR 프로젝트에 적합.
- **Framework 모드** — Remix와 통합. SSR, Type-Safe href 등 추가 기능. 풀 스택 프로젝트에 적합. `@react-router/dev`가 필요하므로 이 스킬의 범위 밖.

자세한 모드별 기능 비교는 React Router 공식 문서의 [API & Mode availability table](https://reactrouter.com/start/modes#api--mode-availability-table)을 참고한다.

### 레이아웃과 ScrollRestoration

기본 골격(4단계)이 이미 `<DefaultLayout>`과 `<ScrollRestoration>`을 포함한다. 추가 레이아웃이 필요한 경우(예: 인증 후 영역 전용 레이아웃) 동일한 방식으로 `routes/layouts/`에 컴포넌트를 만들고 라우트 트리의 적절한 위치에 `element`로 끼워 넣는다.

`<ScrollRestoration>`은 최상위 레이아웃에 **한 번만** 추가한다. 페이지 이동 시 스크롤 위치를 복원하거나 새 페이지의 스크롤을 최상단으로 이동시킨다.

### Link 활용

`<Link>`는 가장 기본적인 탐색 컴포넌트로, `to` 속성의 경로로 이동한다. `<a>`와 달리 페이지 전체를 다시 로드하지 않고 필요한 부분만 업데이트한다.

```tsx
import { Link } from 'react-router'

<Link to="/about">About</Link>
```

탐색 히스토리를 변경하지 않고 현재 항목을 대체하려면 `replace` 속성을 사용한다. 로그인 페이지처럼 뒤로 가기로 돌아가지 않아야 하는 경우에 유용하다.

```tsx
<Link
  to="/about"
  replace>
  About
</Link>
```

스크롤 복원을 끄고 싶다면 `preventScrollReset` 속성을 사용한다. 중첩 라우팅에서 하위 페이지로 이동할 때 유용할 수 있다.

```tsx
<Link
  to={`/movies/${movie.imdbID}`}
  preventScrollReset={true}>
  {movie.Title}
</Link>
```

### NavLink 활용

`<NavLink>`는 현재 경로와 비교해 활성 상태를 자동으로 표시하는 `<Link>`의 확장형이다. 일치하는 경우 자동으로 `active` 클래스가 추가된다.

`className`에 함수를 전달하면 `isActive`로 활성 상태에 따라 스타일을 다르게 적용할 수 있다.

```css
/* src/components/TheHeader.module.css */
.nav {
  display: flex;
  gap: 14px;
}
.active {
  color: red;
  font-weight: bold;
}
```

```tsx
// src/components/TheHeader.tsx
import { NavLink } from 'react-router'
import styles from './TheHeader.module.css'

const navigations = [
  { to: '/', label: 'Home' },
  { to: '/about', label: 'About' }
]

export default function TheHeader() {
  return (
    <header>
      <nav className={styles.nav}>
        {navigations.map(nav => (
          <NavLink
            key={nav.to}
            to={nav.to}
            className={({ isActive }) => (isActive ? styles.active : '')}>
            {nav.label}
          </NavLink>
        ))}
      </nav>
    </header>
  )
}
```

활성 상태를 `children`에서 활용하고 싶다면 함수를 `children`으로 전달한다.

```tsx
<NavLink to="/about">
  {({ isActive }) => (
    <>
      <span className={isActive ? styles.active : ''}>About</span>
      페이지로 이동
    </>
  )}
</NavLink>
```

`end` 속성은 현재 경로가 `to`와 **정확히** 일치할 때만 활성화한다.

| 컴포넌트 사용 | 현재 URL | 활성화 여부 |
|--|--|--|
| `<NavLink to="/about" />` | `/about` | `true` |
| `<NavLink to="/about" />` | `/about/team` | `true` |
| `<NavLink to="/about" end />` | `/about` | `true` |
| `<NavLink to="/about" end />` | `/about/team` | `false` |
| `<NavLink to="/about/" end />` | `/about` | `false` |
| `<NavLink to="/about/" end />` | `/about/` | `true` |

`caseSensitive`로 대소문자 구분을 켤 수 있다.

| 컴포넌트 사용 | 현재 URL | 활성화 여부 |
|--|--|--|
| `<NavLink to="/about/A" />` | `/about/a` | `true` |
| `<NavLink to="/about/A" caseSensitive />` | `/about/a` | `false` |

### useNavigate / Navigate / redirect

**`useNavigate` 훅** — 프로그래밍 방식으로 페이지 이동. 문자열 경로, 숫자(`-1` 뒤로 가기, `1` 앞으로 가기), 또는 `{ pathname, search, hash }` 객체를 인수로 받는다.

```tsx
import { useNavigate } from 'react-router'

export default function LoginButton() {
  const navigate = useNavigate()

  function push() {
    navigate('/about')
  }
  function replace() {
    navigate('/about', { replace: true })
  }
  function go(n: number) {
    navigate(n)
  }

  return (
    <>
      <button onClick={push}>페이지 이동</button>
      <button onClick={replace}>페이지 이동(뒤로가기 불가)</button>
      <button onClick={() => go(1)}>앞으로 가기</button>
      <button onClick={() => go(-1)}>뒤로 가기</button>
    </>
  )
}
```

쿼리스트링/해시는 객체(`To` 타입)로 구조화해 전달할 수 있다.

```tsx
import { useNavigate } from 'react-router'

// To 객체의 타입(참고용)
// interface To {
//   pathname?: string
//   search?: string
//   hash?: string
// }

export default function GoTo() {
  const navigate = useNavigate()
  const query = { name: 'Neo', age: '85' }
  const hash = '#h1-title'

  // 직접 작성
  navigate('/signin?name=Neo&age=22#h1-title')

  // URLSearchParams 사용
  navigate(`/signin?${new URLSearchParams(query).toString()}${hash}`)

  // 객체 사용
  navigate({
    pathname: '/signin',
    search: new URLSearchParams(query).toString(),
    hash
  })
}
```

**`<Navigate>` 컴포넌트** — 렌더링되는 즉시 다른 경로로 리다이렉트. 조건부 렌더링 단계에서 유용하다.

```tsx
import { Navigate } from 'react-router'

export default function PrivatePage({ isAuth }: { isAuth: boolean }) {
  if (!isAuth) {
    return <Navigate to="/signin" replace />
  }
  return <h1>비공개 내용</h1>
}
```

**`redirect` 함수** — Loader/Action 등 라우트 정의 외부에서 리다이렉트를 반환할 때 사용한다. 자세한 활용은 [보호된 경로](#보호된-경로) 항목 참고.

### 동적 세그먼트

URL의 일부를 변수처럼 사용한다. `:`로 표현한다.

```tsx
// src/routes/index.tsx (라우트 트리 일부)
import MovieDetails from './pages/MovieDetails'

// children 배열에 다음 항목 추가
{
  path: '/movies/:movieId',
  element: <MovieDetails />
}
```

`useParams` 훅으로 값을 추출한다.

```tsx
// src/routes/pages/MovieDetails.tsx
import { useState, useEffect } from 'react'
import { useParams } from 'react-router'

interface Movie {
  Title: string // 영화 제목
  Poster: string // 영화 포스터 URL
}

export default function MovieDetails() {
  const [movie, setMovie] = useState<Movie | null>(null)
  const { movieId } = useParams()

  useEffect(() => {
    fetchMovie()
  }, [movieId])

  async function fetchMovie() {
    const res = await fetch(`https://www.omdbapi.com/?apikey=7035c60c&i=${movieId}`)
    const movie = await res.json()
    setMovie(movie)
  }

  return <h1>{movie?.Title}</h1>
}
```

`TheHeader`의 `navigations`에 항목을 추가하면 헤더에서 진입할 수 있다.

```tsx
const navigations = [
  { to: '/', label: 'Home' },
  { to: '/about', label: 'About' },
  { to: '/movies/tt4154796', label: 'Movie(Avengers: Endgame)' }
]
```

### 중첩 라우팅

라우트의 `children`과 `<Outlet>`을 조합해 부모 라우트 안에서 자식 라우트를 렌더링한다. 자식 라우트의 `path`는 부모 경로를 자동으로 상속한다.

```tsx
createBrowserRouter([
  {
    path: '/parent',
    element: <Parent />,
    children: [
      {
        path: 'child', // '/parent/child'
        element: <Child />
      }
    ]
  }
])

function Parent() {
  return (
    <>
      <h1>Parent</h1>
      <Outlet />
    </>
  )
}
function Child() {
  return <h2>Child</h2>
}
```

예: 영화 검색 결과에서 특정 항목을 선택하면 같은 페이지 위에 상세 정보를 모달처럼 띄우는 패턴. 검색 페이지(`<Movies>`)의 자식으로 상세 페이지(`<MovieDetails>`)를 두면, URL은 바뀌지만 검색 페이지의 일부만 업데이트된다.

```tsx
// src/routes/index.tsx (라우트 트리 일부)
{
  path: '/movies',
  element: <Movies />,
  children: [
    {
      path: ':movieId', // '/movies/:movieId'
      element: <MovieDetails />
    }
  ]
}
```

```tsx
// src/routes/pages/Movies.tsx
import { useState } from 'react'
import { Link, Outlet } from 'react-router'

interface Movie {
  imdbID: string
  Title: string
  Poster: string
}

export default function Movies() {
  const [title, setTitle] = useState('')
  const [movies, setMovies] = useState<Movie[]>([])

  async function fetchMovies() {
    const res = await fetch(`https://www.omdbapi.com/?apikey=7035c60c&s=${title}`)
    const { Search: movies } = await res.json()
    setMovies(movies)
  }

  return (
    <>
      <h1>Movies</h1>
      <input
        value={title}
        onChange={e => setTitle(e.target.value)}
        onKeyDown={e => { if (e.key === 'Enter') fetchMovies() }}
      />
      <button onClick={fetchMovies}>Search</button>
      <ul>
        {movies.map(movie => (
          <li key={movie.imdbID}>
            <Link to={`/movies/${movie.imdbID}`}>{movie.Title}</Link>
          </li>
        ))}
      </ul>
      <Outlet />
    </>
  )
}
```

상세 페이지를 모달 형태로 표시한다.

```tsx
// src/routes/pages/MovieDetails.tsx (모달 버전)
import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router'
import styles from './MovieDetails.module.css'

interface Movie {
  Title: string
  Poster: string
}

export default function MovieDetails() {
  const [movie, setMovie] = useState<Movie | null>(null)
  const { movieId } = useParams()
  const navigate = useNavigate()

  useEffect(() => {
    fetchMovie()
  }, [movieId])

  async function fetchMovie() {
    const res = await fetch(`https://www.omdbapi.com/?apikey=7035c60c&i=${movieId}`)
    const movie = await res.json()
    setMovie(movie)
  }

  return (
    <div className={styles.modal}>
      <div
        className={styles.overlay}
        onClick={() => navigate(-1)}
      />
      <div className={styles.content}>
        <h1>{movie?.Title}</h1>
      </div>
    </div>
  )
}
```

```css
/* src/routes/pages/MovieDetails.module.css */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}
.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  cursor: pointer;
}
.content {
  position: relative;
  max-width: 500px;
  padding: 20px 30px;
  border-radius: 10px;
  box-shadow: 0 10px 10px rgba(0, 0, 0, 0.1);
  background-color: white;
}
```

자식 라우트 렌더링은 보통 `<Outlet>`을 쓰지만, `useOutlet` 훅을 쓰면 자식 라우트를 데이터로 받아 페이지 전환을 감지하거나 애니메이션을 트리거하는 데 활용할 수 있다([페이지 전환 애니메이션](#페이지-전환-애니메이션) 참고).

```tsx
// useOutlet 훅 버전
import { useState } from 'react'
import { Link, useOutlet } from 'react-router'

export default function Movies() {
  const outlet = useOutlet()
  // ...

  return (
    <>
      {/* ... */}
      {outlet}
    </>
  )
}
```

### 찾을 수 없는 페이지

다른 라우트와 일치하지 않을 때만 렌더링되도록 **라우트 트리의 가장 마지막**에 `path: '*'`를 둔다.

```tsx
// src/routes/pages/NotFound.tsx
export default function NotFound() {
  return <h1>404 Page Not Found / 페이지를 찾을 수 없습니다.</h1>
}
```

```tsx
// src/routes/index.tsx (라우트 트리 일부, 가장 마지막에 위치!)
import NotFound from './pages/NotFound'

{
  path: '*',
  element: <NotFound />
}
```

### 보호된 경로

승인된 사용자만 특정 라우트에 접근하도록 제한한다. 라우트 정의의 `loader` 속성에 Loader 함수를 두고, 함수 안에서 인증을 확인해 미인증이면 `redirect`로 로그인 페이지로 보낸다.

Loader 함수는 페이지 렌더링 **전에** 호출되며, 요청 정보(`request`)를 받는다.

```ts
// src/routes/loaders/requiresAuth.ts
import { redirect } from 'react-router'

export interface User {
  name: string
  age: number
}

async function getUser() {
  const token = localStorage.getItem('access_token')
  // const res = await fetch('https://api.heropy.dev/user/me', {
  //   headers: { 'Authorization': `Bearer ${token}` }
  // })
  // return res.json()

  // 토큰 정보가 있으면, 사용자 정보를 반환합니다.
  if (token) return { name: 'Neo', age: 22 } satisfies User
  return null
}

// 페이지 접근 시 호출되는 로더(Loader) 함수
export async function requiresAuth({ request }: { request: Request }) {
  const user = await getUser()
  if (!user) {
    const url = new URL(request.url) // 요청 페이지의 URL 정보를 가져옵니다.
    const redirectTo = url.pathname + url.search // 요청 페이지의 경로 + 쿼리스트링
    return redirect(`/signin?redirectTo=${encodeURIComponent(redirectTo)}`)
  }
  return user // 반환 데이터는 `useLoaderData`로 사용할 수 있다.
}
```

로그인 페이지는 `useSearchParams`로 `redirectTo`를 읽어, 인증 후 원래 페이지로 돌려보낸다.

```tsx
// src/routes/pages/SignIn.tsx
import { useSearchParams, useNavigate } from 'react-router'

export default function SignIn() {
  const navigate = useNavigate()
  // 쿼리스트링 정보를 가져와 사용하기 쉽게 객체로 변환합니다.
  const [searchParams] = useSearchParams()
  const query = Object.fromEntries(searchParams)

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    // `<form>`의 새로고침(기본 동작)을 방지합니다.
    event.preventDefault()
    // `<form>`의 데이터를 가져와 사용하기 쉽게 객체로 변환합니다.
    const formData = new FormData(event.currentTarget)
    const { email, password } = Object.fromEntries(formData) as Record<string, string>
    // 로그인 정보가 모두 있으면, 임시로 로그인 처리합니다.
    if (email && password) {
      localStorage.setItem('access_token', 'abcd1234')
      navigate(query.redirectTo || '/')
    }
  }

  return (
    <>
      <h1>Sign In</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          name="email"
          placeholder="Email"
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
        />
        <button type="submit">Sign In</button>
      </form>
    </>
  )
}
```

라우트 트리에 `loader`를 붙인다. 이제 `/movies` 및 그 하위로 접근하면 Loader가 먼저 실행된다.

```tsx
// src/routes/index.tsx (라우트 트리 일부)
import SignIn from './pages/SignIn'
import { requiresAuth } from './loaders/requiresAuth'

// children 배열에 SignIn 라우트를 추가하고, 보호 대상 라우트에 loader 부착
{
  path: '/signin',
  element: <SignIn />
},
{
  path: '/movies',
  element: <Movies />,
  loader: requiresAuth,
  children: [
    {
      path: ':movieId',
      element: <MovieDetails />
    }
  ]
}
```

Loader가 반환한 데이터는 페이지 컴포넌트에서 `useLoaderData`로 사용한다.

```tsx
// src/routes/pages/Movies.tsx
import { useLoaderData } from 'react-router'
import type { User } from '@/routes/loaders/requiresAuth'

export default function Movies() {
  const user = useLoaderData() as User | undefined
  // ...
}
```

### 페이지 지연 로딩

초기 로딩 시간을 줄이기 위해 페이지 컴포넌트를 동적으로 로드한다. 페이지가 처음 사용될 때 번들이 로드된다.

- 번들 크기 감소 → 초기 로딩 시간 단축
- 네트워크 대역폭 절약
- 페이지가 크면 전환 시 지연 발생 가능
- 로딩/에러 처리로 인한 복잡성 증가

기본 사용은 `lazy` + 동적 `import`이다.

```tsx
// src/routes/index.tsx
import { lazy } from 'react'
import { createBrowserRouter, RouterProvider } from 'react-router'

const Home = lazy(() => import('./pages/Home'))
const About = lazy(() => import('./pages/About'))

const router = createBrowserRouter([
  {
    path: '/',
    element: <Home />
  },
  {
    path: '/about',
    element: <About />
  }
])
```

**로딩 처리** — `Suspense`로 로딩 상태를 표시한다.

```tsx
import { lazy, Suspense } from 'react'
import { createBrowserRouter, RouterProvider } from 'react-router'

const Home = lazy(() => import('./pages/Home'))
const About = lazy(() => import('./pages/About'))

const router = createBrowserRouter([
  {
    path: '/',
    element: (
      <Suspense fallback={<div>Loading...</div>}>
        <Home />
      </Suspense>
    )
  },
  {
    path: '/about',
    element: (
      <Suspense fallback={<div>Loading...</div>}>
        <About />
      </Suspense>
    )
  }
])
```

**에러 처리** — `react-error-boundary`의 `ErrorBoundary`로 감싼다.

설치:

    {pm} install react-error-boundary

```tsx
import { lazy, Suspense } from 'react'
import { ErrorBoundary } from 'react-error-boundary'
import { createBrowserRouter, RouterProvider } from 'react-router'

const Home = lazy(() => import('./pages/Home'))
const About = lazy(() => import('./pages/About'))

const router = createBrowserRouter([
  {
    path: '/',
    element: (
      <ErrorBoundary fallbackRender={({ error }) => <div>Error: {error.message}</div>}>
        <Suspense fallback={<div>Loading...</div>}>
          <Home />
        </Suspense>
      </ErrorBoundary>
    )
  },
  {
    path: '/about',
    element: (
      <ErrorBoundary fallbackRender={({ error }) => <div>Error: {error.message}</div>}>
        <Suspense fallback={<div>Loading...</div>}>
          <About />
        </Suspense>
      </ErrorBoundary>
    )
  }
])
```

**커스텀 로드 함수** — 라우트마다 반복되는 `<ErrorBoundary>` + `<Suspense>` 래핑을 한 곳에 정리하기 위해 `dynamic` 헬퍼를 만든다. 공통 기본 처리에 더해 라우트별 개별 로딩/에러 처리도 지정할 수 있다.

```tsx
// src/routes/dynamic.tsx
import { lazy, Suspense } from 'react'
import { ErrorBoundary } from 'react-error-boundary'
import type { FallbackProps } from 'react-error-boundary'

interface DynamicOptions {
  error?: ({ error }: FallbackProps) => React.ReactNode
  loading?: React.ReactNode
}

export function dynamic(
  importFn: () => Promise<{ default: React.ComponentType }>,
  options: DynamicOptions = {}
) {
  const Component = lazy(() => importFn())

  return function DynamicComponent() {
    return (
      <ErrorBoundary
        fallbackRender={
          options.error ||
          (({ error }) => (
            <div>Error: {(error as Error)?.message || 'Unknown error!!'}</div>
          ))
        }>
        <Suspense fallback={options.loading || <div>Loading...</div>}>
          <Component />
        </Suspense>
      </ErrorBoundary>
    )
  }
}
```

라우트 정의에서 `element` 대신 **`Component`** 속성에 `dynamic(...)`의 반환값을 전달한다.

```tsx
// src/routes/index.tsx
import { createBrowserRouter, RouterProvider } from 'react-router'
import { dynamic } from './dynamic'
import DefaultLayout from './layouts/Default'

const router = createBrowserRouter([
  {
    element: <DefaultLayout />,
    children: [
      {
        path: '/',
        Component: dynamic(() => import('./pages/Home'))
      },
      {
        path: '/about',
        Component: dynamic(() => import('./pages/About'), {
          error: ({ error }) => <div>페이지를 출력할 수 없어요!({error.message})</div>
        })
      }
    ]
  }
])
```

### 페이지 전환 애니메이션

[Framer Motion](https://framer.com/motion/)으로 페이지 전환 애니메이션을 적용한다.

설치:

    {pm} install framer-motion

핵심 아이디어:

- `<motion.div>`의 `initial` / `animate` / `exit` / `transition` 속성으로 진입·진출 애니메이션 정의
- 페이지 전환 시 이전 페이지에도 애니메이션을 적용하려면 `<AnimatePresence>`로 감싸고 `<motion.div>`의 `key`에 고유 값(보통 `location.pathname`)을 전달
- `<Outlet>` 대신 **`useOutlet`** 훅을 사용해 자식 라우트를 데이터로 받아 와야 `<AnimatePresence>`가 페이지 변화를 감지해 트리거할 수 있다

기본 레이아웃을 다음과 같이 수정한다.

```tsx
// src/routes/layouts/Default.tsx
import { motion, AnimatePresence } from 'framer-motion'
import { useLocation, useOutlet, ScrollRestoration } from 'react-router'
import TheHeader from '@/components/TheHeader'

export default function DefaultLayout() {
  const location = useLocation()
  const outlet = useOutlet()

  return (
    <>
      <TheHeader />
      <AnimatePresence>
        <motion.div
          key={location.pathname}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0, position: 'absolute' }}
          transition={{ duration: 0.3 }}>
          {outlet}
        </motion.div>
      </AnimatePresence>
      <ScrollRestoration />
    </>
  )
}
```

애니메이션 확인이 잘 안 되면 `transition.duration`을 1초 이상으로 늘려서 확인한다.

### 배포 설정

`createBrowserRouter`는 클라이언트 라우팅이므로, 사용자가 직접 URL을 입력하거나 새로고침해도 SPA가 정상 동작하려면 호스팅 측에서 모든 요청을 `index.html`로 리라이트(rewrite/redirect)해야 한다.

> 이 프로젝트에는 별도의 Vercel 배포 스킬(예: `deploy-to-vercel`, `vercel-cli-with-tokens`)이 존재할 수 있으니, 배포 자체는 그 스킬을 활용한다. 여기서는 SPA 리라이트 설정만 다룬다.

**Vercel** — 프로젝트 루트에 `vercel.json` 생성:

```json
{
  "rewrites": [{ "source": "/:path*", "destination": "/index.html" }]
}
```

**Netlify** — 공개 폴더(`/public`) 경로에 `_redirects` 생성:

```
/*  /index.html  200
```

또는 프로젝트 루트에 `netlify.toml` 생성:

```toml
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

**Firebase** — 프로젝트 루트에 `firebase.json` 생성:

```json
{
  "hosting": {
    "public": "dist",
    "rewrites": [
      {
        "source": "**",
        "destination": "/index.html"
      }
    ]
  }
}
```

## 주의사항

- 이미 존재하는 설정/소스 파일은 덮어쓰지 않는다. 사용자가 명시적으로 요청한 부분만 수정한다.
- Declarative Mode(`<BrowserRouter>`) 또는 Framework Mode(`@react-router/dev`) 기반 코드를 작성해 달라는 요청은 이 스킬의 범위가 아니다. 사용자에게 모드 선택을 한 번 더 확인한 뒤, 필요하면 이 스킬을 사용하지 않는다는 사실을 알린다.
- React Router v7부터 `react-router-dom`은 사용하지 않는다. 1단계에서 `react-router-dom` 사용이 감지되면 2단계의 **마이그레이션 모드**로 동작한다(사용자 동의 없이 임의로 임포트를 바꾸지 않는다).
- Loader 함수는 페이지 컴포넌트 렌더링 전에 실행되므로, 그 안에서 동기적으로 무거운 작업을 수행하지 않는다. 외부 요청은 `await`로 처리하되 사용자 경험을 해치지 않는 최소한의 작업으로 제한한다.
- `<ScrollRestoration>`은 라우터 트리에 **한 번만** 둔다. 여러 레이아웃에 중복으로 두면 동작이 예측 불가능해진다.
- `dynamic` 헬퍼 적용 시 라우트 정의의 `element`가 아니라 **`Component`** 속성을 사용해야 한다. `element`는 React 엘리먼트(`<Foo />`)를, `Component`는 컴포넌트 타입(`Foo`)을 받는다.
- 패키지 매니저는 기존 lock 파일로 판별한다. lock 파일이 없거나 `package-lock.json`만 있으면 `npm`을 사용한다.
