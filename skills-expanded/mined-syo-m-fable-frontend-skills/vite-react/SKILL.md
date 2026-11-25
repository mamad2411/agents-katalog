---
name: vite-react
description: Standalone Vite + React SPA conventions — project structure, env vars, code splitting, vite.config. Use ONLY for standalone Vite + React SPAs — NOT for Astro or Next.js projects, and not merely because Vitest/Storybook use Vite under the hood. 日本語の依頼例:「Vite + ReactのSPA」「素のViteプロジェクト」「vite.config」(※Astro/Next.jsプロジェクトでは使わない)。
---

# Vite + React SPA

## Structure

```
src/
  app/          # app shell: router, providers, global error boundary
  features/<name>/   # feature code: components, hooks, api, tests colocated
  components/   # shared presentational components
  lib/          # framework-agnostic utilities
  styles/       # tokens.css, reset.css, globals.css
```

- Feature code imports shared code; features do not import other features' internals (export via the feature's `index.ts` if sharing is needed).
- Path alias `@/` → `src/` — define it once and mirror it in `vite.config.ts`, `tsconfig.json` (`paths`), and Vitest config (or use `vite-tsconfig-paths`).

## Env vars

- Only `VITE_`-prefixed vars reach client code, via `import.meta.env.VITE_X`. Everything in a Vite SPA bundle is public — never put secrets in any env var a SPA reads; secrets belong on a backend.
- Type them in `src/vite-env.d.ts` (`ImportMetaEnv`). Validate required vars at startup with a small zod schema so misconfiguration fails fast, not deep in runtime.

## Routing & splitting

- Code-split at route level: `React.lazy` + `Suspense` per route. Don't micro-split small components.
- Handle stale-chunk errors after deploys: lazy import rejection → full reload, guarded by a sessionStorage flag so it reloads at most once (otherwise you ship an infinite reload loop).

## Data

- Use a query library (TanStack Query) for server state instead of `useEffect` + `useState` fetching. Keep server cache state out of global client stores.

## Config hygiene

- Keep `vite.config.ts` minimal; resist plugin accumulation. Every plugin must justify itself.
- `build.sourcemap: true` for production debugging only if maps are not publicly served (or use `hidden`).
- Check bundle size when adding dependencies: `npx vite-bundle-visualizer` or `rollup-plugin-visualizer`.

## Tests

- Vitest shares the Vite pipeline — use a single `vite.config.ts` with a `test` block (or `vitest.config.ts` that merges it) so aliases/plugins never diverge between app and tests.
