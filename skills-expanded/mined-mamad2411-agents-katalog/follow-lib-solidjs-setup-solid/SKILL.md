---
name: follow-lib-solidjs-setup-solid
description: Install SolidJS — vite plugin, JSX/TS config, render root, dev/build setup
argument-hint: "[template]"
related:
  - follow-lib-solidjs
  - follow-tool-vite
  - run-dev
  - run-build
  - resolve-errors
---

## Goal

Install a SolidJS app — vite + babel-preset-solid, tsconfig JSX config, render root, dev/build pipeline

## Scope

first-time SolidJS setup — SolidStart (SSR framework) is the alternative; writing components → `build-components`

## Execute

### 1. Scaffold Or Add

```bash
bun create solid my-app          # official templates (vite + solid-ts / solid-js)
cd my-app && bun i
```

or add into an existing vite project:

```bash
bun i solid-js && bun i -D vite-plugin-solid
```

```ts
// vite.config.ts
import solid from 'vite-plugin-solid'
export default defineConfig({ plugins: [solid()] })
```

### 2. TSConfig JSX

```json
{
  "compilerOptions": {
    "jsx": "preserve",
    "jsxImportSource": "solid-js",
    "strict": true
  }
}
```

- `jsx: "preserve"` + `jsxImportSource: "solid-js"` — vite-plugin-solid transforms via babel

### 3. Entry Point

```tsx
// src/index.tsx
import { render } from 'solid-js/web'
import App from './App'
render(() => <App />, document.getElementById('root')!)
```

- `render(() => <App/>, root)` — mounts once; there is no React-style root re-render pattern

### 4. Dev And Build

1. `bun run dev` — vite dev + solid HMR
2. `bun run build` — production bundle
3. `/run-dev` verify; fail → `/resolve-errors` max 3 rounds

### 5. Ecosystem Add-ons (optional)

- `@solidjs/router` — file/app routing; `@solidjs/meta` — head management
- `@solid-primitives/*` — utility primitives; `@tanstack/solid-query` — data fetching
- SolidStart when SSR/SSR+streaming is needed (a separate framework)

## Rules

- `jsxImportSource: "solid-js"` in every tsconfig — otherwise JSX compiles as React
- Choose `solid-js` core or `solid-start` (app framework) — never mix them
- The `solid()` vite plugin is mandatory — solid's JSX transform goes through babel only
- Component files are `.tsx`; `entry server` uses `renderToString` for SSR only

## Expected Outcome

- `bun run dev` starts, JSX compiles correctly, HMR works
- build outputs a deploy-ready bundle
