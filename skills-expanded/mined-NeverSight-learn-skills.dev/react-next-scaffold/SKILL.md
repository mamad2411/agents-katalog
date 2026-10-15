---
name: react-next-scaffold
description: (heropy) Use when initializing a new Next.js (SSR) project or when an existing Next.js project needs missing configuration (ESLint, Prettier, TanStack Query, Tailwind CSS, VSCode settings, path aliases).
license: MIT
metadata:
  author: ParkYoungWoong
  version: 1.1.1
---

# Next.js React Project Scaffold

> 참고: https://www.heropy.dev/p/n7JHmI

Next.js 기반 React(SSR) 프로젝트를 스캐폴딩하거나, 기존 프로젝트의 누락된 설정을 자동 보완하는 스킬.

## 동작 흐름

### 1단계: 프로젝트 상태 감지

다음 파일들을 확인하여 현재 프로젝트 상태를 판별한다:

| 확인 대상 | 감지 방법 |
|-----------|-----------|
| 빈 디렉토리 여부 | 현재 디렉토리에 파일이 없거나 `package.json`이 없음 |
| Next.js 프로젝트 | `next.config.ts` 또는 `next.config.js` 또는 `next.config.mjs` 존재 |
| TypeScript | `tsconfig.json` 존재 |
| TanStack Query | `package.json`의 dependencies에 `@tanstack/react-query` 존재 |
| Tailwind CSS | `package.json`의 dependencies/devDependencies에 `tailwindcss` 존재 |
| ESLint 구성 | `eslint.config.js` 또는 `eslint.config.mjs` 존재 |
| Prettier 구성 | `.prettierrc` 존재 |
| VSCode 설정 | `.vscode/settings.json` 존재 |
| 패키지 매니저 | `pnpm-lock.yaml` → pnpm, `yarn.lock` → yarn, `bun.lockb`/`bun.lock` → bun, `package-lock.json` 또는 없음 → npm |

### 2단계: 분기 처리

**빈 디렉토리인 경우 (스캐폴딩 모드):**

1. 프로젝트 생성 명령 실행
2. 아래 설정 전부 자동 적용

**기존 Next.js 프로젝트인 경우 (보완 모드):**

1. 위 감지 기준으로 설치 상태 자동 판별
2. 누락된 설정만 식별하여 자동 생성
3. 이미 존재하는 설정 파일은 건드리지 않음

### 3단계: 프로젝트 생성

현재 디렉토리에 Next.js 프로젝트 생성:

> `{pm}`은 패키지 매니저 감지 규칙에 따라 결정된 패키지 매니저로 대체한다. (npm, pnpm, yarn, bun)
> `{pmx}`는 해당 패키지 매니저의 실행 명령어로 대체한다. (npx, pnpm dlx, yarn dlx, bunx)

> **참고:** `npx skills add`로 스킬을 설치하면 `.agents/`, `skills-lock.json` 등의 파일이 이미 존재할 수 있다. `create-next-app`은 디렉토리에 파일이 있으면 충돌로 판단하고 종료되므로, 스캐폴딩 모드에서는 다음 절차를 따른다:
>
> 1. 현재 디렉토리의 기존 파일/폴더 목록을 기억해 둔다
> 2. 기존 파일/폴더를 모두 삭제한다
> 3. `{pmx} create-next-app@latest .` 명령으로 프로젝트를 생성한다
> 4. 기억해 둔 파일/폴더 중 프로젝트 생성으로 만들어지지 않은 것들(`.agents/`, `skills-lock.json` 등)을 다시 생성한다

```bash
{pmx} create-next-app@latest .
```

대화형 선택지 (v16 기준):
- Would you like to use the recommended Next.js defaults?: **No, customize settings**
- Would you like to use TypeScript?: **Yes**
- Which linter would you like to use?: **ESLint**
- Would you like to use React Compiler?: **Yes**
- Would you like to use Tailwind CSS?: **Yes**
- Would you like your code inside a `src/` directory?: **Yes**
- Would you like to use App Router? (recommended): **Yes**
- Would you like to customize the import alias (`@/*` by default)?: **No**

### 4단계: 경로 별칭

`@/*` 경로 별칭은 `create-next-app`에서 기본 설정된다. 별도 구성 불필요.

### 5단계: ESLint + Prettier 구성

```bash
{pm} install -D prettier eslint-config-prettier eslint-plugin-prettier prettier-plugin-tailwindcss
```

`eslint.config.js` (또는 `eslint.config.mjs`)에 Prettier 통합 추가:

```js
import prettierRecommended from 'eslint-config-prettier'

const eslintConfig = defineConfig([
  {
    extends: [prettierRecommended]
  }
])

export default eslintConfig
```

TanStack Query가 포함된 경우, 같은 `extends` 배열에 추가:

```js
import prettierRecommended from 'eslint-config-prettier'
import tanstackQuery from '@tanstack/eslint-plugin-query'

const eslintConfig = defineConfig([
  {
    extends: [
      prettierRecommended,
      tanstackQuery.configs.recommended
    ]
  }
])

export default eslintConfig
```

#### 패키지 역할 참고

| 패키지 | 설명 |
|--------|------|
| `prettier` | Prettier 코어 패키지 |
| `eslint-config-prettier` | ESLint와 Prettier의 충돌 방지 |
| `eslint-plugin-prettier` | Prettier 규칙을 ESLint 규칙으로 통합 |
| `prettier-plugin-tailwindcss` | Tailwind CSS 클래스 자동 정렬 |
| `@tanstack/eslint-plugin-query` | TanStack Query 규칙 (TanStack Query 사용 시) |

### 6단계: .prettierrc

`.prettierrc` 파일이 없으면 프로젝트 루트에 생성:

```json
{
  "semi": false,
  "singleQuote": true,
  "singleAttributePerLine": true,
  "bracketSameLine": true,
  "endOfLine": "auto",
  "trailingComma": "none",
  "arrowParens": "avoid",
  "plugins": ["prettier-plugin-tailwindcss"]
}
```

### 7단계: .vscode/settings.json

`.vscode/settings.json` 파일이 없으면 생성:

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode"
}
```

### 8단계: TanStack Query

> 참고: https://www.heropy.dev/p/HZaKIE#h2_with_Nextjs

`@tanstack/react-query`가 `package.json`에 없으면:

Next.js에서는 `@tanstack/react-query-next-experimental` 패키지를 추가로 설치해야 한다.

1. 패키지 설치:
   ```bash
   {pm} install @tanstack/react-query @tanstack/react-query-next-experimental
   {pm} install -D @tanstack/eslint-plugin-query
   ```

2. ESLint Flat Config(`eslint.config.js`)에 TanStack Query 플러그인 추가 (5단계 참조)

3. `src/providers/query.tsx` 생성:
   ```tsx
   'use client'
   import {
     QueryClient,
     QueryClientProvider,
     isServer,
   } from '@tanstack/react-query'
   import { ReactQueryStreamedHydration } from '@tanstack/react-query-next-experimental'

   function makeQueryClient() {
     return new QueryClient({
       defaultOptions: {
         queries: {
           // 클라이언트의 즉시 다시 요청에 대응하도록, 기본 캐싱 시간(min)을 지정
           staleTime: 60 * 1000
         }
       }
     })
   }

   let browserQueryClient: QueryClient | undefined = undefined

   function getQueryClient() {
     if (isServer) {
       return makeQueryClient()
     } else {
       if (!browserQueryClient) browserQueryClient = makeQueryClient()
       return browserQueryClient
     }
   }

   export function QueryProvider({ children }: { children: React.ReactNode }) {
     const queryClient = getQueryClient()
     return (
       <QueryClientProvider client={queryClient}>
         <ReactQueryStreamedHydration>
           {children}
         </ReactQueryStreamedHydration>
       </QueryClientProvider>
     )
   }
   ```

4. `src/app/layout.tsx`에서 `QueryProvider`로 `children`을 래핑:
   ```tsx
   import { QueryProvider } from '@/providers/query'

   export default function RootLayout({
     children
   }: Readonly<{
     children: React.ReactNode
   }>) {
     return (
       <html lang="ko">
         <body>
           <QueryProvider>{children}</QueryProvider>
         </body>
       </html>
     )
   }
   ```

## 주의사항

- 이미 존재하는 설정 파일은 덮어쓰지 않는다
- 기존 프로젝트 보완 모드에서는 질문 없이 자동으로 진행한다
- 패키지 매니저는 기존 프로젝트의 lock 파일로 판별한다:
  - `pnpm-lock.yaml` → `pnpm`
  - `yarn.lock` → `yarn`
  - `bun.lockb` 또는 `bun.lock` → `bun`
  - `package-lock.json` 또는 lock 파일 없음 → `npm`
- 빈 디렉토리(스캐폴딩 모드)에서는 `npm`을 사용한다
