---
name: nextjs-architect
description: Refactor Next.js/React directories by splitting large components, extracting hooks and services, optimizing "use client" boundaries, and enforcing one-component-per-file with colocation best practices.
---

# Next.js Architect

Refactor a user-specified directory in a Next.js or React project. Split large components, extract logic into hooks, move API calls to services, optimize `"use client"` boundaries, and enforce one-component-per-file. Adapt to the project's conventions, framework version, and tooling. Do not assume a specific package manager, styling approach, or state management library.

## 1. Inspect the target directory

1. Identify the directory the user tagged. Scan all `.tsx`, `.ts`, `.jsx`, `.js` files recursively inside it.
2. Read project-level configuration to detect:
   - Framework: Next.js App Router, Next.js Pages Router, or plain React.
   - TypeScript or JavaScript.
   - Package manager (`package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `bun.lockb`).
   - Linter, formatter, and build scripts available in `package.json`.
3. For each file, analyze and record:
   - Total line count.
   - Number of exported React components (named and default).
   - Number of hooks used (`useState`, `useEffect`, `useRef`, `useMemo`, `useCallback`, custom hooks).
   - API calls: `fetch`, `axios`, `ky`, `ofetch`, tRPC calls, server actions, or any HTTP client usage.
   - Whether `"use client"` directive is present.
   - Import and export relationships (who imports whom).
   - TypeScript types/interfaces defined inline.
4. Detect shared usage: scan sibling and parent directories to find components imported from the target directory by other routes or features.

## 2. Build a complete refactor plan

Before editing any file, prepare and present a complete plan to the user. Include:

### 2.1 File inventory

For each file in the target directory, list:
- File path, line count, component count.
- Issues found (multiple components, mixed logic/UI, inline API calls, missing or unnecessary `"use client"`, deeply nested JSX).

### 2.2 Component splits

For each component that should be split:
- Original component name and file.
- Proposed new components with names, destination files, and reasoning.
- Which parts of the JSX tree become which new component.

Apply these splitting rules:
- Component body exceeds 80 lines → candidate for split.
- JSX return has more than 3 levels of nesting → extract inner blocks into separate components.
- A single file exports more than 1 React component → split into separate files.
- Repeated JSX patterns → extract into reusable component.

### 2.2.1 Component grouping

After identifying all splits, detect components that should be grouped into a subdirectory inside `_components/`:

- **Trigger:** A parent component has ≥3 sub-components that are exclusively used by that parent (imported only by that one component, nowhere else in the codebase).
- **Transitive inclusion:** If a sub-component (B) is exclusively used by another sub-component (A) that is being grouped, B must also move into the same group directory — even if B is not directly imported by the parent. Apply recursively: any component exclusively used within the group belongs in the group.
- **Action:** Create a subdirectory named after the parent component file (without extension, e.g., `music-library.tsx` → `music-library/`). Move the parent component and all its exclusive sub-components (including transitive ones) into this subdirectory.
- **Barrel export:** The subdirectory `index.ts` exports only the parent component. Sub-components are private implementation details.
- **Recursive grouping:** If a sub-component inside a group also has ≥3 exclusive sub-components of its own, nest another subdirectory within the group. Apply the same rules recursively.
- **Escape hatch:** If a previously-exclusive sub-component later needs to be used outside its parent, move it out of the group directory back to the root `_components/` level and update all imports.

For each proposed group, list:
- Parent component name.
- Exclusive sub-components that will be grouped with it.
- The resulting subdirectory structure.

### 2.3 Hook extractions

For each hook extraction:
- Original location (file, line range).
- New hook name (`useXxx`) and destination file in `_hooks/`.
- What state, effects, and logic move into the hook.
- What the hook returns (values, setters, handlers).

Apply these extraction rules:
- More than 3 `useState` + `useEffect` in one component → extract to custom hook.
- Inline event handler exceeding 5 lines → move logic to hook.
- Related state and effects that form a logical unit → group into one hook.
- A hook that mixes more than 2 distinct concerns (e.g., pagination + CRUD + audio playback + form state) → split into separate hooks, one per concern.
- A hook that returns more than 10 values → candidate for split by concern.
- When splitting a large hook, a composing hook may call the sub-hooks and aggregate their return values. Each sub-hook must be in its own file.
- Hooks must not re-export types, utilities, or other modules. Consumers import those directly from `_types/`, `_utils/`, etc.

### 2.4 Service extractions

For each service extraction:
- Original location (file, line range).
- API endpoint or action being called.
- New service function name and destination file in `_services/`.
- Parameters and return type.

Apply these extraction rules:
- Any `fetch`, `axios`, or HTTP client call inside a component or hook → move to `_services/`.
- Server actions that call external APIs → move to `_services/`.
- Group related API calls into one service file (e.g., `userApi.ts` for all user-related endpoints).

### 2.5 Type extractions

- Inline TypeScript interfaces/types used by more than one file → move to `_types/`.
- Props interfaces stay collocated unless shared across components.

### 2.6 `"use client"` optimization

- Components that have `"use client"` but contain no interactive code (no state, effects, event handlers, browser APIs) → remove directive, make server component.
- Components mixing server-compatible and client-only code → split into server wrapper + client interactive part.
- Components without `"use client"` that use client-only APIs → add directive.

### 2.7 Shared component detection

- Components imported by files outside the target directory → suggest moving to a `_shared/` directory at the nearest common ancestor, or to a project-level shared location.
- List each shared component, where it is imported from, and the proposed new location.

### 2.8 Proposed directory structure

Show a tree preview of the directory after refactor:
```
target-directory/
  page.tsx (or index.tsx)
  _components/
    ComponentA.tsx
    ComponentB.tsx
    component-c/           (grouped: ComponentC has ≥3 exclusive sub-components)
      index.ts             (exports only ComponentC)
      ComponentC.tsx
      SubComponentD.tsx
      SubComponentE.tsx
      SubComponentF.tsx
    index.ts
  _hooks/
    useFeatureData.ts
    useFeatureFilters.ts
    index.ts
  _services/
    featureApi.ts
    index.ts
  _types/
    feature.types.ts
    index.ts
  _utils/           (only if pure helpers are extracted)
    formatters.ts
    index.ts
```

### 2.9 Import changes

List every import path that will change, grouped by file.

### 2.10 Confirmation gate

Ask the user to confirm the proposal. Do not edit any file before explicit approval. If the user requests changes or rejects the plan, revise and ask again. Approval covers only the presented scope.

## 3. Create directory structure

After approval, create the necessary directories inside the target:
- `_components/` — extracted UI components.
- `_hooks/` — extracted custom hooks.
- `_services/` — extracted API call functions.
- `_types/` — extracted TypeScript types/interfaces (only if needed).
- `_utils/` — extracted pure helper functions (only if needed).

Use `_` prefix so Next.js App Router excludes these from routing.

## 4. Execute the refactor

Perform changes in this order:

### 4.1 Extract types (if applicable)
1. Move shared TypeScript interfaces and types to `_types/featureName.types.ts`.
2. Export them from `_types/index.ts`.

### 4.2 Extract services
1. Move API calls to `_services/featureNameApi.ts`.
2. Each function should be a named export, async, with typed parameters and return values.
3. Export them from `_services/index.ts`.

### 4.3 Extract hooks
1. Move state logic, effects, and handlers to `_hooks/useFeatureName.ts`.
2. Hooks import from `_services/` for API calls instead of calling APIs directly.
3. Each hook file exports exactly one hook as a named export.
4. Split large hooks by concern: each distinct concern (data fetching, pagination, search/filter, form/CRUD, delete, audio playback, status toggle, etc.) becomes its own hook file.
5. When sub-hooks need to be composed, create a parent hook that calls them and aggregates their return values. The parent hook file is separate from the sub-hook files.
6. Hooks must not re-export types, utilities, or other modules. Remove any re-exports; consumers import directly from `_types/`, `_utils/`, etc.
7. Export all hooks from `_hooks/index.ts`.

### 4.4 Extract components
1. Move each component to `_components/ComponentName.tsx`.
2. One component per file. File name matches component name in PascalCase.
3. Components import hooks from `_hooks/` for logic, not inline.
4. Components receive data via props; define props interface in the same file unless shared.
5. Export them from `_components/index.ts`. This barrel will be revised in §4.4.1 after grouping — components moved into subdirectories will be removed from the root barrel and only the parent component will be re-exported via the subdirectory barrel.

### 4.4.1 Group components into subdirectories

After extracting all components, apply grouping:

1. For each component that has ≥3 exclusive sub-components (sub-components imported only by that parent), create a subdirectory inside `_components/` named after the parent file (without extension).
2. Move the parent component file and all its exclusive sub-components into the subdirectory.
3. For each sub-component being moved, check if it has its own exclusive dependencies (components only imported by members of this group). Move those into the group directory as well. Repeat until no more transitive exclusive dependencies remain.
4. Create `index.ts` inside the subdirectory that exports only the parent component.
5. Update all internal imports within the group to use relative paths (e.g., `./sub-component`).
6. If recursive grouping applies (a sub-component inside a group also qualifies), create nested subdirectories following the same pattern.
7. Update `_components/index.ts`: remove direct exports of all components that were moved into a subdirectory. Replace them with a single re-export from the subdirectory's `index.ts`. Only the parent component should be visible to external consumers.
8. The root `_components/index.ts` re-exports from each subdirectory's `index.ts` so external consumers are unaffected.

### 4.5 Simplify the original file
1. The entry file (`page.tsx`, `index.tsx`, or the original component file) should compose extracted components.
2. Minimal code: imports + composition + layout. No inline logic, no API calls, no complex state.

### 4.6 Optimize `"use client"` boundaries
1. Remove `"use client"` from components that do not need it.
2. Add `"use client"` to components that require it.
3. Push `"use client"` as deep into the component tree as possible (leaf components).

### 4.7 Create barrel exports
1. Each `_components/`, `_hooks/`, `_services/`, `_types/`, `_utils/` directory gets an `index.ts`.
2. Re-export all public members from their respective files.
3. For grouped component subdirectories inside `_components/`: the subdirectory `index.ts` exports only the parent component (sub-components are private). The root `_components/index.ts` re-exports from each subdirectory's barrel.

### 4.8 Update all imports
1. Update every file that imported from the original locations.
2. Use relative paths consistent with the project's conventions.
3. Verify no import points to a nonexistent file.

### Rules during execution
- Preserve all existing functionality. Do not change behavior.
- Preserve styling (CSS modules, Tailwind classes, styled-components, etc.) exactly.
- Preserve existing test files. Update import paths in tests if needed.
- Do not rename existing public API exports that other parts of the codebase depend on.
- If a file being refactored re-exports something consumed externally, keep that re-export.
- If implementation reveals something not covered by the approved plan, stop, report the discrepancy, and request approval for an updated plan.

## 5. Verify

1. Search for broken imports: grep for imports pointing to moved/renamed files.
2. Check for circular dependencies in the new structure.
3. Run TypeScript type check (`tsc --noEmit` or `npx tsc --noEmit`) if TypeScript is used.
4. Run the project's linter if available.
5. Run the project's formatter if available.
6. Run tests if available.
7. Attempt a build if available.
8. If any check fails, fix within the approved scope. If the fix changes the plan, report and ask for approval.

## 6. Report results

Summarize:

- **Files created:** list each new file with purpose.
- **Files modified:** list each modified file with what changed.
- **Files deleted:** list any files removed (empty after extraction).
- **Components extracted:** count and names.
- **Hooks extracted:** count and names.
- **Services extracted:** count and names.
- **Types extracted:** count and names.
- **`"use client"` changes:** directives added, removed, or moved.
- **Shared components detected:** any suggestions for cross-feature sharing.
- **Verification results:** output of type check, lint, build, tests.
- **Manual review needed:** anything that could not be automated or verified.
