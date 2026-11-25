---
name: "react-dedup"
description: "Analyze React components for duplicate code, redundant patterns, and missed reuse opportunities, then refactor into clean DRY components. Use after writing React code, when cleaning up components, deduplicating UI code, or when asked to make React code more modular and reusable."
---

# React DRY Refactor

Analyze a directory of React components to find duplicate code, redundant patterns, and missed reuse opportunities. Produce a refactoring plan, then execute it — extracting shared components, consolidating duplicates, and wiring up existing reusable components that were overlooked.

## When to Use

- After a batch of React components have been written or modified
- When the user says: "deduplicate", "DRY up", "refactor components", "too much duplication", "make reusable", "clean up react code"
- As a follow-up review pass on any React feature work

## Execution Steps

### Phase 1 — Discovery

**CRITICAL: Read before you act. Do NOT skip or abbreviate this phase.**

1. **Identify the target directory** — Ask the user if not obvious. Default to the most recently modified component directory.

2. **Inventory existing shared components** — Before creating ANYTHING new, catalog what already exists:
   - Read the shared component library barrel exports (e.g. `repos/components/src/components/index.ts`)
   - Read the consuming app's local component directories (e.g. `repos/admin/src/components/`)
   - List every exported component, hook, HOC, and utility
   - Build a mental catalog: "these building blocks are already available"

3. **Scan target files** — Read every `.tsx` / `.ts` file in the target scope. For each file, note:
   - JSX patterns (layout wrappers, list renderers, form groups, card structures, empty states, loading states, error states)
   - Inline styles or `sx` props that repeat across components
   - Hook call patterns that appear in multiple components with similar logic
   - Prop drilling chains that could be replaced by context or composition
   - Render functions or sub-renders defined inside a component that could be standalone

4. **Cross-reference against existing components** — For every repeated pattern found in step 3, check:
   - Does an existing shared component already handle this? → **Reuse it** (do NOT create a new one)
   - Does an existing component handle 80% of this with minor extension? → **Extend it** via props/children
   - Is this truly novel and repeated 3+ times? → **Extract a new component**

### Phase 2 — Analysis Report

Present findings to the user as a structured report BEFORE making any changes:

```
## DRY Refactor Analysis — [Target Directory]

### Existing Components That Should Be Reused
| Pattern Found | Existing Component | Files Affected |
|---|---|---|
| [description] | `<ComponentName>` from `@tdsk/components` | file1.tsx, file2.tsx |

### New Components to Extract
| Proposed Component | Reason | Source Files | Estimated Reuse Count |
|---|---|---|---|
| `<Name>` | [what it encapsulates] | file1.tsx, file2.tsx, file3.tsx | N |

### Inline Logic to Consolidate
| Pattern | Proposed Hook/Utility | Files Affected |
|---|---|---|
| [repeated logic] | `useXxx()` or `xxxHelper()` | file1.tsx, file2.tsx |

### Redundant Code to Remove
| What | Where | Why It's Redundant |
|---|---|---|
| [code description] | file.tsx:L42-68 | Duplicates `<ExistingComponent>` |

### No Action Needed
[List any files reviewed that are already clean]
```

**Wait for user approval before proceeding to Phase 3.**

### Phase 3 — Refactor Execution

Execute approved changes in dependency order:

1. **Create new shared components first** (if any were approved)
   - Place in the appropriate directory (`repos/components/src/components/` for cross-app, or local `components/` for app-specific)
   - Follow existing patterns: named export, proper TypeScript types, `index.ts` barrel export
   - Keep components minimal — accept children/render props for flexibility

2. **Update existing components** (if extending with new props)
   - Add optional props with sensible defaults — never break existing consumers
   - Update the component's type definitions

3. **Refactor consuming files**
   - Replace duplicated JSX with the shared/extracted component
   - Replace duplicated hook logic with shared hooks
   - Remove dead code left behind after extraction
   - Update imports

4. **Update barrel exports** if new components were added to shared directories

### Phase 4 — Verification

- Run TypeScript checks: `pnpm types` (or per-repo `cd repos/<repo> && pnpm types`)
- Run tests: `pnpm test` (or per-repo)
- Confirm no regressions in the affected components

## Rules

### Reuse-First Hierarchy
1. **Reuse existing component as-is** — always the first choice
2. **Extend existing component** — add an optional prop, slot, or children pattern
3. **Extract new shared component** — only when patterns repeat 3+ times and nothing existing covers it
4. **Extract app-local component** — when duplication exists only within one app, not cross-app
5. **Do nothing** — if the "duplication" is coincidental and the components will diverge

### What Counts as Duplication
- **YES**: Same JSX structure with different data props (e.g., 4 card components with identical layout but different titles)
- **YES**: Same hook call sequence in 3+ components (e.g., `useState` + `useEffect` + fetch pattern)
- **YES**: Same `sx`/style object repeated across 3+ components
- **YES**: Same conditional rendering pattern (loading/error/empty/data) in multiple components
- **NO**: Two components that look similar now but serve fundamentally different purposes
- **NO**: Shared use of the same MUI primitive (e.g., both use `<Box>` — that's not duplication)
- **NO**: Two instances of a simple one-liner (e.g., `const [open, setOpen] = useState(false)`)

### Component Design Principles
- Props over configuration objects — keep interfaces flat and obvious
- Composition over props explosion — prefer `children` and render props over 15 boolean flags
- Sensible defaults — new props must be optional and backward-compatible
- Single responsibility — extracted components do one thing well
- Co-locate types — component props interface lives in the same file or a sibling `.types.ts`

### What NOT to Do
- Do NOT create wrapper components that just pass props through to a single child
- Do NOT extract components used only once — that's premature abstraction
- Do NOT refactor stable, working code that has no duplication just to "clean it up"
- Do NOT change component APIs in ways that break existing consumers without the user's explicit approval
- Do NOT create a `utils/` grab-bag — if a utility is component-specific, co-locate it

## Project-Specific Notes

### Shared Component Library
- Located at `repos/components/src/components/`
- 30+ existing components including: Accordion, Buttons, Card, Dialog, Drawer, Inputs, List, Loading, Menu, Monaco, Section, Tabs, Text, Tooltip
- 8 hook categories in `repos/components/src/hooks/`
- Always check here FIRST before creating anything new

### Admin App Components
- Located at `repos/admin/src/components/`
- 39+ component directories
- Uses `@TAF/*` path aliases
- State management via Jotai atoms
- API integration via TanStack React Query

### Patterns to Watch For
- **Drawer pattern**: Many drawers share create/edit form + title + actions layout — check if `<Drawer>` from `@tdsk/components` covers it
- **Card grid pattern**: `OrgCard`, `ProjectCard`, `UserCard` etc. — look for shared `<ItemCard>` or `<CardGrid>`
- **Empty state pattern**: `NoOrgs`, `NoProjects`, `NoUsers`, `NoEndpoints`, `NoFunctions` — check for shared `<EmptyState>`
- **Form sections**: Agent settings, endpoint configs — look for repeated label+input+help-text layouts
- **Loading/error states**: Repeated `if (loading) return <Loading />; if (error) return <Error />` — consider a shared wrapper or hook
