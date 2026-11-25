---
name: athena-auth-ui-tables
description: >
  Build, integrate, inspect, debug, customize, document, test, or release Athena
  Auth UI table surfaces from packages/athena-auth-ui/packages/heroui. Covers
  AthenaTable, AuthTable, AthenaTableActionBar, TableEmptyState, TableSkeleton,
  AuthTableMobileCards, TableRowActionsMenu; chips (AthenaTableChipConfig,
  createChipRenderer, statusChipRenderer, columnsFromAthenaModel chips);
  AthenaModelRow / RowOf / columnsFromAthenaModel / toAthenaTableColumns;
  useAthenaQuery, useAthenaTableView, useAthenaTableQuery; sorting, selection,
  pagination, virtualization; row/bulk actions and feedback; portable table
  builder presets and codegen; createAthenaTableQueryRoute data proxy; and the
  next-heroui-example tables showcase (/tables, table-showcase-page,
  use-table-showcase, portable presets). Use when the user runs
  /athena-auth-ui-tables or works on *table* under packages/heroui/src.
---

# Athena Auth UI Tables

Package surface lives under:

- **Library:** `packages/athena-auth-ui/packages/heroui`
- **Public barrel:** `src/tables.ts` → `@xylex-group/athena-auth-ui/tables`
- **Narrow query re-export:** `@xylex-group/athena-auth-ui/athena/table-query`
- **Reference consumer:** `packages/athena-auth-ui/examples/next-heroui-example`
  - Route: `src/app/(site)/tables/page.tsx`
  - Showcase: `src/components/table-showcase-page.tsx` +
    `src/components/table-showcase/use-table-showcase.ts` +
    `src/lib/table-showcase*.ts`

Also use `$athena-auth-ui` for package-wide exports/providers/styles/release.
Use `$athena-js` when the issue is SDK model/query/execute semantics (not UI).

## Source of truth (read order)

1. `packages/heroui/package.json` — confirm `./tables` and `./athena/table-query`.
2. `packages/heroui/src/tables.ts` — **complete** public symbol surface
   (components, hooks, chips, models, builder, feedback, toasts).
3. Docs: `docs/entrypoints/tables.mdx`, `docs/athena-tables.mdx`,
   `docs/data-hooks.mdx`, plus generated component/hook pages.
4. Implementation families in
   [references/implementation-map.md](references/implementation-map.md).
5. Chips / models / rows contracts in
   [references/chips-models-rows.md](references/chips-models-rows.md).
6. Query + portable builder in
   [references/query-and-builder-contracts.md](references/query-and-builder-contracts.md).
7. Example wiring in
   [references/example-showcase.md](references/example-showcase.md).
8. Nearest `packages/heroui/tests/table-*.test.*` and showcase tests.

When artifacts disagree: **export map + barrels + source** win; regenerate docs
with `bun run docs:generate`. Never recommend deep `src/**` or `dist/**` imports.

## Route the task

### Compose / render a table

- Prefer **`AthenaTable<Row>`** for the full generic surface (sort, search,
  status filters, pagination, resize, virtualization, mobile cards, actions,
  async loading).
- Use **`AuthTable`** when you need the auth empty-state wrapper.
- Define stable **`getRowKey`**, typed **`AthenaTableColumn<Row>[]`**, loading
  skeleton, empty state, sort mode, pagination, and a11y labels explicitly.
- Column display precedence: custom `render` → declarative **`chip`** →
  **`format`** → default stringify (`resolveColumnRender`).
- Empty states: treat as one centered composition. `TableEmptyState` owns
  `min-h-44` and has **no** action slot — never append actions below it; collapse
  min-height in one wrapper or use an action-capable empty primitive.

### Athena models → columns / rows

```ts
import { table } from "@xylex-group/athena"
import {
  type AthenaModelRow,
  columnsFromAthenaModel,
  AthenaTable,
} from "@xylex-group/athena-auth-ui/tables"

const tasks = table("tasks").schema("public").columns({ /* … */ }).primaryKey()
type TaskRow = AthenaModelRow<typeof tasks>

const columns = columnsFromAthenaModel(tasks, {
  labels: { title: "Task" },
  rowHeaders: ["title"],
  chips: {
    status: { color: "status", variant: "soft" },
    active: { color: "boolean", variant: "soft" },
  },
})
```

- `AthenaModelRow<TModel>` = `RowOf<TModel>` from `@xylex-group/athena`.
- Also re-exported: `AthenaRow`, `AthenaInsert`, `AthenaUpdate`,
  `AthenaFormValues`, `AthenaTableDef`.
- Keep metadata compatible with real `meta.columns` / relations — do not invent
  colliding wrapper model types.

### Chips

- Types: `AthenaTableChipConfig`, `AthenaTableChipOptions`, descriptors,
  when-rules, sizes/variants.
- Builders: `createDefaultAthenaTableChipConfig`, `normalizeAthenaTableChipConfig`,
  `serializeAthenaTableChipConfig`, `chipConfigToOptions`,
  `createChipRenderer` / `createChipRendererFromConfig`, `statusChipRenderer`,
  `renderChip`, `resolveAthenaTableChipDescriptors`,
  `resolveStatusColor` / `resolveBooleanColor`.
- Portable builder columns carry a JSON-serializable `chip` field
  (export/import snake_case boundary).
- Showcase demos chips via model columns + builder column config
  (`buildChipDemoModelColumnsSample`, chip map text editors).

### Connect data (query stack)

| Path | API |
| --- | --- |
| Server / proxy / worker | `@xylex-group/athena` `executeAthenaReadQuery` (alias `executeAthenaTableQuery`) |
| Auth UI TanStack tables | `useAthenaQuery` / `useAthenaInfiniteQuery` (+ table-prefixed aliases) |
| Composed columns+query | `useAthenaTableView` or `toAthenaTableColumns` + `useAthenaQuery` |
| Athena-native React only | `@xylex-group/athena/react` `useAthenaReadQuery` |

Do **not** mix TanStack `useAthenaQuery` and Athena-native `useAthenaReadQuery`
for the same screen data. Hooks never construct clients — pass v3
`createClient` / server façades / `withContext` views.

Data proxy (example pattern):

```ts
import { createAthenaTableQueryRoute } from "@xylex-group/athena-auth-ui/tables"
export const { POST } = createAthenaTableQueryRoute({
  authorize: async ({ request }) => Boolean(request.headers.get("cookie")),
  getClient: async () => createAthenaServerClient({ url, key }),
})
```

### Sorting, selection, pagination

Trace controlled props ↔ Zustand stores ↔ TanStack conversion ↔ server
`orderBy` together. Keep:

- client sort out of server query mutation and vice versa
- multi-column sort priority + null strategies
- page reset on filter/sort changes
- `page`/`pageSize` as fetch window; `query.limit` as optional **total-row cap**
  (not a second SQL LIMIT)

### Actions, feedback, mobile rows

Keep enablement, disabled reasons, invocation, templates, toast adapters,
copy/download/href helpers, desktop rows, and `AuthTableMobileCards` aligned.
`AthenaTableActionBar` selection props stay **optional** for standalone use.

### Portable builder + generated code (showcase)

Treat example builder JSON as a **public contract**:

- snake_case file boundary; camelCase OK in React state
- table paths as objects `{ schema_name, table_name }`
- columns: `index`, `translation_key`, optional `chip` / format / sort
- `config_hash`, `config_seed`, package versions for athena + athena-auth-ui
- importers accept legacy camelCase + dotted paths; exporters emit current shape

Update serializer, normalizer, hash/seed, preview, codegen, localStorage, tests,
and docs **together**.

Primary code: package `components/auth/table/builder/**` + example
`src/lib/table-showcase*.ts` + `table-showcase-codegen/`.

### Exports / docs

When adding symbols: implementation → `src/tables.ts` → root `src/index.ts` if
intended → `package.json` for new subpaths → `bun run docs:generate` → example
imports + tests.

## Invariants

- Derive rows/metadata from `@xylex-group/athena` models (`AthenaModelRow`).
- Stable row keys across pagination, sort, refetch, desktop, and mobile.
- Chip configs stay JSON-serializable for builder export.
- Server vs client sorting ownership is explicit at one conversion boundary.
- Loading = skeletons; unavailable actions stay disabled before invoke.
- Empty-state surface is one centered composition (no stacked full-height shells).
- Avoid idle drop-zone borders on empty tables unless the boundary is meaningful;
  keep rounded drag-hover.
- Deterministic query keys include every input that changes rows.
- Backwards-compatible preset import; current format on export only.

## Validation

| Seam | Proof |
| --- | --- |
| Query / sort / format / chips / import | `packages/heroui/tests/table-*.test.ts`, `to-athena-table-columns`, `table-chip-config`, `athena-table-query` |
| Components / selection / virtualization | browser Vitest (`test:browser`) |
| Types / exports | package `build` + type verify scripts |
| Public API | `bun run docs:generate` |
| Showcase / presets | `examples/.../src/lib/table-showcase*.test.ts`, example `tsc` / `nx run next-heroui-example:build` |

```bash
cd packages/athena-auth-ui
bun run athena-js:build
bunx nx run @xylex-group/athena-auth-ui:build
# package tests under packages/heroui
bunx nx run next-heroui-example:dev   # open /tables
```

Windows OpenNext `EPERM` after a green Next compile is environment, not a table
regression — confirm page generation first.

## Related skills

- `$athena-auth-ui` — full package + next-heroui-example
- `$athena-js` / `$athena-js-typed-schema-registry` — models, RowOf, table DSL
- `$update-skill` — rebuild this skill from library after large surface changes
