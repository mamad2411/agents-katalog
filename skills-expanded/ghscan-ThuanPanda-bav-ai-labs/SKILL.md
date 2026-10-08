---
name: react-feature
description: Scaffold a complete feature end-to-end following the project's feature-based architecture. Use when creating a new page, new feature, new module, or new route.
triggers:
  - new feature
  - scaffold feature
  - create feature
  - new page
  - new module
  - add feature
  - new route
argument-hint: "<feature-name> (e.g. 'settings', 'user-profile')"
---

# Feature Scaffolding

Scaffold a complete feature folder following the project's feature-based architecture (see `CLAUDE.md` section "Architecture").

## When to Activate

- User says "create a new feature", "scaffold X", "add a new page for Y"
- Setting up a new route that needs its own UI, state, and (optionally) data fetching

## Workflow

1. **Clarify** (if not provided):
   - Feature name in kebab-case (e.g., `user-profile`)
   - Does it need data fetching? Forms?
   - Is it behind the authenticated layout (`_app/`) or public (top-level route)?

2. **Create the feature folder** under `src/features/<feature-name>/`:
   ```
   src/features/feature-name/
   ├── feature-name-page.tsx     # main component, named export (e.g. FeatureNamePage)
   ├── index.ts                  # barrel — only export what routes/other code need
   ├── components/               # (when needed) UI pieces private to this feature
   └── mock-data.ts              # (when needed) mock data private to this feature
   ```

3. **Create the thin route file**:
   ```
   src/routes/_app/feature-name.tsx     # authenticated route
   # or
   src/routes/feature-name.tsx          # public route
   ```

4. **Add i18n keys** under a matching namespace (same name as the feature folder, camelCase if multi-word) in both:
   - `src/i18n/locales/en/feature-name.json`
   - `src/i18n/locales/de/feature-name.json`

   Then register the namespace in `src/i18n/index.ts` (`resources`, `namespaces`) and add its type to `src/i18n/react-i18next.d.ts`.

5. **Verify** before finishing:
   - Route file only declares `Route` (+ `beforeLoad`/`loader` if needed) and wires `component`
   - All imports use `@/*` aliases
   - `Link`/`useNavigate` come from `@tanstack/react-router`
   - All static text uses `useTranslation()`
   - Both `en` and `de` locale files updated together
   - `index.ts` barrel only re-exports what's actually consumed elsewhere

## Key Templates

### index.ts (barrel)
```ts
export { FeatureNamePage } from './feature-name-page'
```

### Route file (authenticated, under `_app/`)
```tsx
import { createFileRoute } from '@tanstack/react-router'
import { FeatureNamePage } from '@/features/feature-name'

export const Route = createFileRoute('/_app/feature-name')({
  component: FeatureNamePage,
})
```

### feature-name-page.tsx
```tsx
import { useTranslation } from 'react-i18next'

export function FeatureNamePage() {
  const { t } = useTranslation('featureName')

  return (
    <div className="space-y-6 p-6">
      <h1 className="text-2xl font-semibold text-foreground">{t('title')}</h1>
    </div>
  )
}
```

## Key Conventions

- **Kebab-case for all files and folders** — never camelCase, PascalCase, or snake_case
- `<feature-name>-page.tsx` is the main component, always a **named export** (e.g. `SettingsPage`, not `default`)
- Route files are **thin wrappers** — no UI, no business logic, only `Route` + guards + `component`
- Feature-scoped components stay in `components/` inside the feature folder; only promote to `src/components/` when reused by 3+ features
- Namespace name matches the feature folder name (camelCase for multi-word folders, e.g. `user-profile` → `userProfile`)
## Agent Skill Synchronization

Follow [SKILL-SYNC.md](../../../SKILL-SYNC.md) whenever creating or changing this skill. Keep the same folder name and identical `SKILL.md` content in `.github/skills/`, `.claude/skills/`, `.codex/skills/`, and `.omc/skills/` so Copilot, Claude Code, Codex, and OpenCode stay synchronized.
