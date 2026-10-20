# React Hooks Best Practices

## Summary

**One-sentence:** Configures a React-hooks correctness spec — unconditional top-level calls, exhaustive `useEffect` deps, mandatory cleanup, derivation over state-sync — and an ESLint `react-hooks` plugin gate.

**One-paragraph:** The two biggest sources of React bugs in 2026 are hooks called conditionally (early-return on loading state before `useState`) and effects with stale-closure dependency lists. React 19 compiler reduces but does not eliminate either. This methodology mandates `eslint-plugin-react-hooks` with `exhaustive-deps` set to `error` (never `warn`), forbids hooks inside `if`/`for`/`switch`, requires every `useEffect` that subscribes to return a cleanup function, prefers derivation (compute in render) over `useState + useEffect` synchronization, and pulls memoization out of "default" status — `useMemo`/`useCallback` only when (a) passed to a `React.memo`'d child or (b) listed as a hook dependency. Output is a `.eslintrc` snippet plus a hook-correctness JSON spec.

**Ефективно для:**

- Команди мігрують з React 16-class на React 18/19 functional + hooks.
- Аудит продуктивності: зайві re-render через unstable callbacks + неконтрольовану мемоізацію.
- AI-loop генерації UI компонентів: lint catches early-return + dependency-array drift, які агент часто пропускає.
- Refactoring legacy: видалити `useState + useEffect` синхронізацію → derivation.

## Applies If (ALL must hold)

- React ≥16.8 (hooks introduced) — preferably 18+ for concurrent rendering correctness.
- Project uses functional components + hooks (not class lifecycle).
- ESLint is wired into PR CI or pre-commit.

## Skip If (ANY kills it)

- React Server Components — hooks are client-only; needs `'use client'` boundary first.
- Pre-React 16.8 codebases — upgrade React before adopting.
- Heavy cross-page state (optimistic updates, conflict resolution) — use Zustand / Redux Toolkit / TanStack Query, hooks alone are insufficient.
- Pure presentational components with no state — memoization without measurement is premature.
- Form submits in Next.js App Router — use `'use server'` actions instead of client-side hooks.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| `package.json` | JSON | repo root (verify React ≥16.8) |
| ESLint config | `.eslintrc.cjs` / `eslint.config.js` | repo root |
| Component file(s) | `.tsx` / `.jsx` | `src/` |
| React version pin | semver | `package.json dependencies.react` |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Foundational for any React project. Pairs with [[react-patterns]] for design choices. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: unconditional-call, exhaustive-deps-error, cleanup-mandatory, derive-not-sync, memo-with-measurement, custom-hook-prefix | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for hook-correctness spec + ESLint config block | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: conditional-hook-call, stale-closure-effect, sync-state-via-effect, memo-everywhere | 700 |
| `content/04-procedure.xml` | essential | 5-step audit + fix procedure for an existing React project | 800 |
| `content/05-examples.xml` | optional | One worked example: refactor a buggy data-fetch component | 800 |
| `content/06-decision-tree.xml` | essential | Routing: state-or-derive → memo decision → effect vs event handler | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `lint_detect` | haiku | ESLint output → JSON parse; deterministic. |
| `classify_state_vs_derive` | sonnet | Needs to read render body + decide if value is derivable. |
| `rewrite_effect` | sonnet | Per-component cleanup + dep array fix. |
| `architectural_split` | opus | Decide custom-hook extraction vs component split — cross-file. |

## Templates

| File | Purpose |
|------|---------|
| `templates/eslint-react-hooks.config.js` | ESLint config block enabling `react-hooks/exhaustive-deps` as error |
| `templates/use-fetch.example.tsx` | Reference custom hook with cleanup + abort signal |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-react-hooks.py` | Validate hook-correctness spec JSON against schema | After spec generation |

## Related

- [[react-patterns]] — design patterns (composition, context boundaries) built on top of correct hooks.
- [[typescript-strict-mode]] — TS-strict catches a different class of hook bugs (typed deps).

## Decision tree

See `content/06-decision-tree.xml`. Tree branches on: does state need to live across renders? → yes → `useState`; no → derive. Then: is value passed to memo'd child or used as hook dep? → yes → `useMemo`/`useCallback`; no → leave unmemoized. Then: does the side-effect subscribe to anything? → yes → return cleanup. All leaves reference rules from `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/eslint-react-hooks.config.js`

```javascript
import reactHooks from 'eslint-plugin-react-hooks';

export default {
  plugins: {
    'react-hooks': reactHooks,
  },
  rules: {
    // Both MUST be "error", never "warn".
    'react-hooks/rules-of-hooks': 'error',
    'react-hooks/exhaustive-deps': 'error',
  },
};
```

### `templates/use-fetch.example.tsx`

```tsx
import {useEffect, useState} from 'react';

export function useFetch<T>(url: string, init?: RequestInit) {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const controller = new AbortController();
    setLoading(true);
    fetch(url, {...init, signal: controller.signal})
      .then(r => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json() as Promise<T>;
      })
      .then(j => setData(j))
      .catch(e => {
        if (e.name !== 'AbortError') setError(e);
      })
      .finally(() => setLoading(false));

    return () => controller.abort();
  }, [url, init]);

  return {data, error, loading};
}
```
