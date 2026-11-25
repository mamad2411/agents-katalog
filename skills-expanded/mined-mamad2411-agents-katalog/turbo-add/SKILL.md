---
name: turbo-add
description:
  Guide for adding a new theme family to turbo-themes. Use when implementing Nord,
  Solarized, Gruvbox, Tokyo Night, One Dark, Ayu, Kanagawa, Everforest, Radix, or any
  new theme.
---

# Adding a New Theme to Turbo-Themes

Turbo-themes uses a token-based theming system: theme definitions in
`src/themes/packs/` define color tokens, `src/themes/registry.ts` collects them, the
build generates CSS from tokens, the theme-selector package provides UI components,
and the site plus example projects consume the themes.

## Related Skills

- `stand-ts`: TypeScript coding standards
- `commit`: semantic commit format when committing changes
- `turbo-verify`: use after implementation to verify completeness

## How to Implement: Copy a Reference, Discover the Touchpoints

Do NOT write theme packs from a template or trust a memorized file list. Instead:

1. **Pick a reference theme** and mirror its files:
   - Synced theme with npm package: `src/themes/packs/catppuccin.synced.ts` +
     `scripts/sync-catppuccin.mjs`
   - Synced theme: `src/themes/packs/rose-pine.synced.ts`
   - Manual theme with license/source metadata: `src/themes/packs/nord.ts`
   - Manual theme: `src/themes/packs/bulma.ts`, `src/themes/packs/dracula.ts`
2. **Discover every touchpoint** by grepping for an existing theme's variant id
   (pick one from `src/themes/registry.ts`, e.g. a rose-pine or catppuccin variant):

   ```bash
   # Every file that mentions an existing variant — the new theme needs the
   # same touchpoints (packs, token JSON, icons, site data, examples, tests)
   rg -l 'rose-pine-moon' --hidden -g '!node_modules' -g '!dist'

   # Family-level touchpoints (type unions, family maps, vendor metadata)
   rg -l 'rose-pine' src/ packages/ apps/ scripts/
   ```

3. Also check root-level registrations the greps can miss because they do not
   mention variant ids: the `theme:sync` script wiring in `package.json` and
   size limits in `test/integration/bundle-size.test.ts`.

4. Verify with the current repo, not this skill: if a file in the grep output is
   generated (check for a "generated" header or a `build`/`theme:sync` script that
   writes it), update the source and rebuild instead of hand-editing.

## Files to Create

```text
scripts/sync-<theme>.mjs                     # Optional: sync from npm package
src/themes/packs/<theme>.synced.ts           # Theme definitions (or <theme>.ts for manual)
schema/tokens/themes/<theme-id>.tokens.json  # W3C Design Token file, one per variant
assets/img/<theme-id>.png                    # Theme icon, one per variant
```

- **Theme pack**: copy the structure of the reference pack — `id`, `name`,
  `homepage`, `license` (spdx/url/copyright), `source` (package/version/repository
  for synced themes), and `flavors` with complete token groups (`background`,
  `text`, `brand`, `state`, `border`, `accent`, `typography`, `content`). Do NOT
  add `iconUrl` to flavors — icons resolve via `VENDOR_ICON_MAP` in theme-mapper.ts.
- **W3C token files**: mirror an existing file in `schema/tokens/themes/` —
  `$value`/`$type` format, `$schema` pointing to
  `../../turbo-themes.schema.json#/$defs/ThemeFile`.
- **Icons**: PNG per variant (typically 24x24), visually distinct for light/dark.

### Sync Script Best Practices (if the theme has an npm palette package)

Copy `scripts/sync-catppuccin.mjs` and adapt. Key rules:

1. **Output path must be `src/themes/packs/`** — the registry imports from there,
   NOT `packages/core/src/themes/packs/`.
2. **Read the version from `node_modules/<pkg>/package.json`** and populate
   `source.version` for traceability.
3. **Normalize hex colors** — source packages include `#` inconsistently.
4. **Deterministic ordering** — sort variant keys for reproducible builds.
5. **Add the script to `theme:sync` in package.json** — the build pipeline must
   generate the file before TypeScript compilation.

## Files to Update

Enumerate with the discovery greps above; the recurring touchpoints are:

- `src/themes/registry.ts` — import the pack and spread its flavors into
  `allFlavors`
- `packages/theme-selector/src/types.ts` — add to the `ThemeFamily` type union
- `packages/theme-selector/src/constants.ts` — add to `THEME_FAMILIES`
  (name + description)
- `packages/theme-selector/src/theme-mapper.ts` — add to `VENDOR_FAMILY_MAP`,
  `VENDOR_ICON_MAP` (string, or `{light, dark}` AppearanceIcons object when the
  family has both appearances), and `FLAVOR_DESCRIPTIONS` per variant
- `apps/site/src/data/theme-meta.ts` — **single source of truth for the site**:
  add to `themeGroups`, `themeNames` (short dropdown labels), and `themeIcons`.
  `validThemeIds` is derived automatically; `BaseLayout.astro` and
  `ThemeDropdown.astro` are data-driven from this file — no direct edits there.
- `apps/site/src/pages/themes.astro` — sidebar family section + JS `themeNames`
- `apps/site/src/pages/index.astro` — hero preview strip buttons
- `scripts/prepare-style-dictionary.mjs` — add to `vendorMeta` (name + homepage)
- `test/integration/bundle-size.test.ts` — increase budget only if needed
- `package.json` — append sync script to `theme:sync` (if using one)

### Example projects

Example files hardcode theme lists; discover the current set instead of assuming:

```bash
# Web examples with hardcoded theme arrays / dropdowns
rg -l 'VALID_THEMES|LIGHT_THEMES|lightThemes' examples/
rg -l 'THEMES' examples/stackblitz/react examples/stackblitz/vue

# Swift example touchpoints
rg -l 'ThemeId|ThemeDefinition' examples/swift-swiftui/
```

In each hit, add the new variants everywhere an existing variant appears:
`<select>` options, `VALID_THEMES`/`LIGHT_THEMES`/`THEMES` arrays, Swift
`ThemeId.swift` enum cases, `ThemeRegistry.swift` `ThemeDefinition` palettes, and
`ThemeRegistryTests.swift` counts/labels. Files that import from
`@lgtm-hq/turbo-themes-core/tokens` (React hooks, Vue composables, Bootstrap
main.ts) auto-update — skip any file where the grep hit is an import, not a
hardcoded list.

## Naming Conventions

- **Theme ID**: lowercase with hyphens (e.g., `rose-pine-moon`)
- **Variant label** (token `label` field): full display name including family
  (e.g., "Gruvbox Dark Hard") — match existing `.tokens.json` files
- **Short label** (`themeNames` in theme-meta.ts): condensed dropdown label
  (e.g., "Dark Hard", "Moon")
- **Vendor / family**: the theme family identifier (e.g., `rose-pine`)

## Build and Test

```bash
uv run lintro chk          # Lint
bun run build              # Core build
bun run examples:build     # Example projects
bun run test               # Unit tests
bun run examples:test      # Example E2E tests
cd apps/site && bun run build   # Site build
cd apps/site && bun run dev     # Visual check
```

**Tip:** the `turbo-test` skill runs the full pipeline automatically.

## Common Gotchas

1. **Theme reverts on navigation / wrong label / missing icon**: variants missing
   from `themeGroups`/`themeNames`/`themeIcons` in
   `apps/site/src/data/theme-meta.ts` (the site is data-driven from this file —
   do not edit BaseLayout.astro for these)
2. **Theme not in dropdown / wrong group**: `VENDOR_FAMILY_MAP` missing or wrong
3. **Tests fail on theme order**: use `data-theme-id` attribute lookups, not
   array indices
4. **Bundle size test fails**: increase the budget in bundle-size.test.ts
5. **CI `Cannot find module './packs/<theme>.synced.js'`**: sync script missing
   from `theme:sync` in package.json
6. **tokens.json shows wrong name/homepage**: missing from `vendorMeta` in
   prepare-style-dictionary.mjs
7. **Generated assets outdated**: run `bun run build` and commit the generated
   files (theme-selector bundles, tokens.json in core/python/swift)
8. **Type changes**: if adding interfaces, update BOTH `src/themes/types.ts` AND
   `packages/core/src/themes/types.ts` — separate files kept in sync
9. **Visual regression fails after hero changes**: snapshots are generated on
   Linux CI — run the `maintenance-generate-snapshots.yml` workflow
10. **Missing from examples**: re-run the example discovery greps and diff the new
    theme's hits against an existing theme's hits
