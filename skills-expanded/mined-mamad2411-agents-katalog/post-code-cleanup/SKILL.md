---
name: post-code-cleanup
description: Mandatory cleanup pass after writing or changing code — finds and removes duplicate code, unnecessary components, unused files/exports/dependencies, extra complexity and dead code, then verifies nothing broke. Use at the end of EVERY coding task before saying "done", and whenever the user says cleanup, refactor, remove unused, dead code, or duplicate code.
---

# Post-Code Cleanup

Written for this agent-kit (Prashant's own rule: every task ends with this pass). Works with `ponytail-review` / `ponytail-audit` for deeper "write less code" reviews.

## Scope

- Default: only files you created or changed in this task, plus anything they import or that imports them.
- Whole-repo cleanup only when the user asks. Never delete someone else's in-progress work.

## The 5 checks (do all five, in order)

### 1. Duplicate code
- Same or near-same logic/markup in 2+ places → extract ONE function/component/hook/util and reuse it.
- Tool: `npx jscpd <src-folder> --min-tokens 50 --reporters console` (add `--ignore "**/*.test.*"` if tests are noisy).
- Don't abstract things that are only coincidentally similar or used once — wait for the second real use (rule of three for tiny snippets).

### 2. Unnecessary components
- Wrapper components that only pass props through, one-use components split out for no reason, components that duplicate a library component already in the project (e.g. a custom Button when `components/ui/button` exists).
- Merge or inline them. Prefer the project's existing design-system component.

### 3. Unused files, exports and dependencies
- Tool (JS/TS): `npx knip` — reports unused files, exports, types and dependencies. Review each finding before deleting (dynamic imports, config files, and framework entry files like Next.js `page.tsx`/`layout.tsx` can be false positives).
- Also check: unused images/fonts in `public/` or `assets/`, leftover demo/starter files (Vite/Next boilerplate, `App.css`, sample SVGs), unused env vars, unused npm packages (remove with the package manager, not by editing the lockfile).
- Python: `ruff check --select F401,F841` (unused imports/variables) if ruff is available.

### 4. Extra complexity
- Deep nesting (> 3 levels) → early returns / guard clauses.
- Functions > ~50 lines or components > ~200 lines → split by responsibility.
- Premature abstraction: generic factories, config objects, context providers or state libraries for something used in one place.
- `useEffect` used to derive state → compute during render. `useMemo`/`useCallback` sprinkled without a measured reason → remove.
- Over-engineered types (5-level generics) where a simple type works.

### 5. Dead code
- Commented-out code blocks, unreachable branches, always-true/false conditions, feature flags that are fully rolled out, unused variables/params/imports.
- `console.log` / `debugger` / temporary test data / `markers: true` (GSAP) / TODOs that were actually done.
- ESLint: `npx eslint . --max-warnings 0` if configured; TypeScript: `npx tsc --noEmit` (with `noUnusedLocals` / `noUnusedParameters` on when possible).

## Safety rules

- Delete only what you have evidence is unused (tool output + a search for the name, including string/dynamic usage).
- Run after cleanup: type-check, lint, tests, and a production build (`npm run build`). If any fail, fix or revert that removal.
- Don't mix a big cleanup with a feature change in one commit when committing is part of the task — separate "refactor:" commit.
- If a removal is risky or outside this task's scope, list it in the report instead of doing it.

## Report (write this at the end)

```
Cleanup report
- Duplicates: <what was merged, or "none found">
- Components removed/merged: <...>
- Unused files/exports/deps removed: <...>
- Complexity reduced: <...>
- Dead code removed: <...>
- Left as-is (needs your call): <...>
- Verified: typecheck ✅ lint ✅ tests ✅ build ✅
```
