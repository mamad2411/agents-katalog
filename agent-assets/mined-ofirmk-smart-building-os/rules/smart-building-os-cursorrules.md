CRITICAL ARCHITECTURE RULES - ZERO REGRESSION POLICY:
1. NEVER delete, rename, or alter existing UI pages (page.tsx/layout.tsx) or their directories without explicit user permission.
2. The /pitch, /projects, and /contracts-engine routes are STRICTLY PROTECTED. Do not 'clean them up' during backend or unrelated frontend tasks.
3. Development must be strictly ADDITIVE.

Gate Before Push: run `npx playwright test tests/critical-routes-protection.spec.ts` and confirm green. Restore from git if red.

---

Rule 1: ZERO SCROLLING at shell level.
- App shells in dashboard routes must use `h-[calc(100dvh-4rem)]` (or equivalent) and `overflow-hidden`.
- Only inner panes/lists/tables/forms may scroll.

Rule 2: CANONICAL 70/30 ENTITY WORKSPACE.
- CRUD screens must use `EntityWorkspace` / `EntityWorkspaceLayout` pattern.
- Sidebar/List context occupies ~30% (`lg:col-span-3`), main detail/form occupies ~70% (`lg:col-span-7`).
- Focus interactions must use `Sheet`/FocusPane (not detached modal-only editing flows).

Rule 3: SEMANTIC DESIGN TOKENS ONLY.
- Do not ship hardcoded surface/text/border colors in app screens (`bg-white`, `text-slate-*`, `border-slate-*`, etc).
- Use semantic tokens/classes (`bg-card`, `bg-background`, `text-foreground`, `text-muted-foreground`, `border-border`, `ring-ring`, `text-primary`).
- Shared primitives must carry tokenized defaults so legacy screens remain readable in dark mode.

Rule 4: COMPACT, READABLE FORM DENSITY.
- Inputs/selects/combos must keep bounded widths (`max-w-*`) unless a full-width control is explicitly needed.
- Prefer dense form rhythm and consistent label hierarchy; avoid stretched single-field rows.

Rule 5: REQUIRED MICRO-INTERACTIONS.
- Interactive elements must include hover/focus feedback (hover tint/shadow + visible focus ring).
- Tables and cards should animate subtly (`transition-colors`/`transition-shadow`) and keep keyboard affordances.
- Sticky action bars/footers should use tokenized translucent surfaces (`bg-card/95` + backdrop blur).

Rule 6: DEPRECATION SAFETY.
- `MasterDetailWorkspace` and `DenseMasterDetailTemplate` are legacy; migrate new/edited routes to `EntityWorkspace`.
- If legacy templates remain, they must still obey these token + micro-interaction rules.

UI ARCHITECTURE: All screens must render within the dynamic Middle Area (`flex-1 min-h-0`). Never use `h-screen` or `h-[100vh]` inside specific page components. Overlays (Sheets/Menus) must always use portals or `z-[100]` to sit above the fixed top and bottom app bars.
