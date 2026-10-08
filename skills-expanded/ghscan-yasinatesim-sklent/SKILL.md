---
name: wtf-js-react
description: Strict TS/React review for this repo. Triggered by wtf-code-reviewer dispatcher on any *.ts/*.tsx change. Enforces arrow-only, one-component/file, default-export-bottom, status-state, dispatch-object, no inline style, modal store, no React.* namespace, exhaustive-deps.
---

# wtf-js-react (skill)

Invoke when the diff touches `web/src/**/*.{ts,tsx}`.

Usage:

```
Agent(subagent_type: "wtf-js-react", prompt: "Review these TS/React files: <list>. Branch: <name>. Changes: <one-line>.")
```

The `wtf-js-react` agent will:

1. Read `.claude/references/frontend-standards.md` + `code-quality/{js-ts,react-nextjs}.md`
2. Check rejection-grade rules: arrow-only, one-component/file, default-export-bottom, no inline style, no Tailwind, no React.* namespace, status-state pattern, dispatch-object map, modal store, Zustand-only state
   - Dispatch map values MUST be component references at module scope (`[STATUS.LOADING]: LoadingView`), rendered as `const CurrentView = STATE_VIEWS[state.status]; <CurrentView ... />`. JSX elements as map values, or view components declared inside the parent body, are blockers.
   - Every component in its own eponymous folder (`components/X/X.tsx`, not flat `components/X.tsx`) with an `index.ts` re-exporting it; feature-scoped helpers in `<module>/helpers/`, exported types in `<module>/types/<name>.types.ts`, neither loose at the module root. Imports sorted by `simple-import-sort` (auto-fixable). Reuse before writing: grep for an existing component/util covering the case first.
3. Check type safety: no `any`, no unsafe `as`, catch typed `unknown`
4. Check hooks: exhaustive-deps, no conditional hook, no setState in render
5. Check async: all promises handled, error paths covered
6. Check naming, file limits, i18n key reuse

Returns aggregated report. Re-dispatch if `NEEDS_FIXES`. Max 3 iterations.
