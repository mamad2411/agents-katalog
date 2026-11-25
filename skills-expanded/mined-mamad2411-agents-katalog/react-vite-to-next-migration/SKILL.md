---
name: react-vite-to-next-migration
description: (heropy) Use when migrating an existing Vite + React (TypeScript) project to Next.js (App Router, v16). Converts entry points, routing (React Router → App Router), environment variables, path aliases, static assets, and styling setup.
license: MIT
metadata:
  author: ParkYoungWoong
  version: 1.0.0
---

# Vite React → Next.js App Router 마이그레이션

Vite + React(TS) 프로젝트를 Next.js(App Router, v16) 프로젝트로 변환하는 스킬.
기존 코드의 동작을 유지하면서 Next.js 구조로 옮기는 것이 목표.

## 동작 흐름

### 1단계: 프로젝트 상태 감지

다음 파일들을 확인하여 마이그레이션 가능 여부와 옮길 대상을 판별한다:

| 확인 대상 | 감지 방법 |
|-----------|-----------|
| Vite 프로젝트 | `vite.config.ts` 또는 `vite.config.js` 존재 |
| TypeScript | `tsconfig.json` 또는 `tsconfig.app.json` 존재 |
| React Router | `package.json`의 dependencies에 `react-router` 또는 `react-router-dom` 존재 |
| TanStack Query | `package.json`의 dependencies에 `@tanstack/react-query` 존재 |
| Zustand | `package.json`의 dependencies에 `zustand` 존재 |
| Tailwind CSS | `package.json`의 dependencies/devDependencies에 `tailwindcss` 존재 |
| 환경 변수 | `.env*` 파일에 `VITE_` 접두사 변수 존재 |
| 정적 자산 | `public/` 디렉토리 존재 |
| 진입점 | `index.html`, `src/main.tsx`, `src/App.tsx` 존재 |
| 패키지 매니저 | `pnpm-lock.yaml` → pnpm, `yarn.lock` → yarn, `bun.lockb`/`bun.lock` → bun, 그 외 → npm |

`vite.config.*`이 없다면 마이그레이션 대상이 아니므로 사용자에게 알리고 중단한다.

### 2단계: 마이그레이션 개요 안내

작업 시작 전 다음을 사용자에게 안내한다:

- App Router(`src/app`) 구조로 변환됨
- React Router 라우트는 App Router의 디렉토리 기반 라우트로 변환됨
- `VITE_` 환경 변수는 `NEXT_PUBLIC_` 접두사로 변경됨
- 브라우저 API/이벤트 훅을 사용하는 컴포넌트는 `'use client'`가 추가됨
- Vite 전용 파일(`index.html`, `vite.config.*`, `src/main.tsx`, `src/vite-env.d.ts`)은 제거됨
- 기존 컴포넌트/스타일/유틸 코드는 최대한 그대로 보존됨

### 3단계: 의존성 변경

Vite 관련 패키지 제거, Next.js 패키지 추가:

```bash
{pm} remove vite @vitejs/plugin-react @vitejs/plugin-react-swc vite-tsconfig-paths @tailwindcss/vite react-router react-router-dom
{pm} install next@latest react@latest react-dom@latest
{pm} install -D @types/node
```

> `{pm}`은 1단계에서 감지한 패키지 매니저로 대체한다. 존재하지 않는 패키지는 `remove` 대상에서 제외한다.

`package.json`의 `scripts`를 Next.js 기준으로 교체:

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  }
}
```

### 4단계: 설정 파일 교체

다음 파일을 제거한다:

- `vite.config.ts` / `vite.config.js`
- `index.html`
- `src/vite-env.d.ts`

`next.config.ts`를 새로 생성:

```ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  reactStrictMode: true
}

export default nextConfig
```

`tsconfig.json`을 Next.js용으로 갱신 (기존 `paths`는 유지):

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

> 기존 `tsconfig.app.json`, `tsconfig.node.json`은 삭제한다.

### 5단계: 진입점 변환 (App Router 구조 생성)

`src/app/layout.tsx`를 생성하고, 기존 `index.html`의 `<head>` 정보(타이틀, lang, 메타)를 옮긴다:

```tsx
import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'App',
  description: ''
}

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="ko">
      <body>{children}</body>
    </html>
  )
}
```

기존 `src/index.css`를 `src/app/globals.css`로 이동.
Tailwind 사용 프로젝트라면 상단에 다음 지시문이 유지되어야 한다:

```css
@import 'tailwindcss';
```

`src/main.tsx`, `src/App.tsx`, `src/App.css`는 라우팅 변환(6단계) 후 제거한다.

### 6단계: 라우팅 변환 (React Router → App Router)

기존 React Router 라우트 정의(`createBrowserRouter`/`<Routes>`)를 분석한 뒤, 각 경로를 App Router 디렉토리 구조로 매핑한다.

| React Router | App Router |
|--------------|------------|
| `path: '/'` → `<Home />` | `src/app/page.tsx` |
| `path: '/about'` → `<About />` | `src/app/about/page.tsx` |
| `path: '/posts/:id'` → `<Post />` | `src/app/posts/[id]/page.tsx` |
| `path: '*'` → `<NotFound />` | `src/app/not-found.tsx` |
| 공통 레이아웃 컴포넌트 | `src/app/layout.tsx` 또는 하위 `layout.tsx` |

각 페이지 컴포넌트는 다음 규칙으로 옮긴다:

- 기존 컴포넌트 본문은 최대한 그대로 유지
- `useNavigate`, `useLocation`, `useParams`, `<Link>` 등 React Router API 사용 지점은 다음과 같이 치환:
  - `useNavigate()` → `useRouter()` (`next/navigation`)
  - `useParams()` → 페이지 컴포넌트의 `params` prop (`async` 페이지에서는 `await params`)
  - `useLocation().pathname` → `usePathname()` (`next/navigation`)
  - `<Link to="...">` → `<Link href="...">` (`next/link`)
- 위 훅 중 하나라도 사용하거나, `useState`/`useEffect`/이벤트 핸들러/브라우저 API를 사용하는 페이지는 파일 최상단에 `'use client'`를 추가한다.
- 그렇지 않은 정적 페이지는 서버 컴포넌트(기본값)로 둔다.

작업이 끝나면 `src/main.tsx`, `src/App.tsx`, `src/App.css`, 기존 라우터 정의 파일(`src/routes/index.tsx` 등 라우팅 정의에만 쓰인 파일)을 제거한다. 단, 페이지 컴포넌트 본체는 `src/app/**/page.tsx`로 옮겨지므로 보존된다.

### 7단계: 환경 변수 변환

`.env`, `.env.local`, `.env.development`, `.env.production` 등 모든 `.env*` 파일에서:

- `VITE_FOO=bar` → `NEXT_PUBLIC_FOO=bar`

소스 코드 전반에서:

- `import.meta.env.VITE_FOO` → `process.env.NEXT_PUBLIC_FOO`
- `import.meta.env.MODE` → `process.env.NODE_ENV`
- `import.meta.env.DEV` → `process.env.NODE_ENV !== 'production'`
- `import.meta.env.PROD` → `process.env.NODE_ENV === 'production'`
- `import.meta.env.BASE_URL` → 사용처 검토 후 제거 또는 `next.config.ts`의 `basePath`로 대체

### 8단계: 정적 자산 처리

- `public/` 디렉토리는 그대로 사용 가능. 별도 이동 불필요.
- 단, Vite에서 `/vite.svg` 같이 루트 절대경로로 참조했던 기본 자산이 더 이상 필요 없다면 제거한다.
- 소스 코드 내부에서 `import logo from './assets/logo.svg'` 같은 임포트 형태는 그대로 동작하지만, `public/` 자산을 `next/image`로 사용하는 형태(`<Image src="/logo.svg" ... />`)도 안내한다.

### 9단계: Tailwind CSS (사용 중인 경우)

기존 `@tailwindcss/vite` 플러그인은 3단계에서 이미 제거되었다. Next.js에서는 PostCSS 기반 설정으로 전환한다.

```bash
{pm} install -D tailwindcss @tailwindcss/postcss postcss
```

프로젝트 루트에 `postcss.config.mjs` 생성:

```js
export default {
  plugins: {
    '@tailwindcss/postcss': {}
  }
}
```

`src/app/globals.css` 상단의 `@import 'tailwindcss';`는 그대로 유지된다.

### 10단계: TanStack Query (사용 중인 경우)

기존 `QueryClientProvider` 래핑 코드는 Next.js App Router 구조에 맞게 별도 Provider 컴포넌트로 분리한다. 자세한 구성은 `react-next-scaffold` 스킬의 TanStack Query 단계와 동일하게 처리한다.

요약:

1. `{pm} install @tanstack/react-query-next-experimental` 추가 설치
2. `src/providers/query.tsx` 생성 (`'use client'` + `QueryClientProvider` + `ReactQueryStreamedHydration`)
3. `src/app/layout.tsx`의 `<body>` 안쪽 `children`을 `<QueryProvider>`로 래핑

### 11단계: Zustand (사용 중인 경우)

기존 store 파일은 그대로 사용 가능하다. 단, store를 사용하는 컴포넌트는 클라이언트 컴포넌트여야 하므로 해당 파일 상단에 `'use client'`를 보장한다.

### 12단계: 정리 및 검증

다음 작업을 수행한다:

1. `node_modules` 및 lock 파일 재생성:
   ```bash
   rm -rf node_modules
   {pm} install
   ```
2. `.gitignore`에 `.next/`, `next-env.d.ts` 추가 (없는 경우)
3. 빌드 검증:
   ```bash
   {pm} run build
   ```
4. 빌드 에러가 있을 경우, 에러 메시지에 따라 다음을 우선 점검:
   - 서버 컴포넌트에서 브라우저 전용 API 사용 → 해당 컴포넌트에 `'use client'` 추가
   - `import.meta.env` 잔존 → 7단계 규칙으로 치환
   - React Router API 잔존 → 6단계 규칙으로 치환

## 주의사항

- 라우팅 구조와 페이지별 클라이언트/서버 컴포넌트 결정은 자동으로 판별하되, 모호한 경우 안전을 위해 `'use client'`를 추가한다.
- 기존 컴포넌트 코드는 라우팅/환경변수/임포트 경로 외에는 수정하지 않는다.
- 패키지 매니저는 기존 프로젝트의 lock 파일로 판별한다:
  - `pnpm-lock.yaml` → `pnpm`
  - `yarn.lock` → `yarn`
  - `bun.lockb` 또는 `bun.lock` → `bun`
  - `package-lock.json` 또는 lock 파일 없음 → `npm`
- 마이그레이션 후 추가 설정(ESLint + Prettier, VSCode, Tailwind 통합 등)이 필요하다면 `react-next-scaffold` 스킬을 이어서 실행하면 된다.
