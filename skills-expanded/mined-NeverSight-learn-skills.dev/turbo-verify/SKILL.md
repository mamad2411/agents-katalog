---
name: turbo-verify
description:
  Verify that a theme implementation is complete and follows all project standards. Use
  after adding a new theme to turbo-themes.
---

# Verify Theme Implementation

Verify that a theme implementation is complete and follows all turbo-themes
standards. When asked to verify a theme (e.g., `/turbo-verify rose-pine`), run
through the sections below. The `turbo-add` skill holds the full add-time file map
and discovery approach — this skill checks the result.

## 1. Discover Touchpoints (do this first)

Do not trust a memorized file inventory. Compare the new theme's footprint against
a known-complete theme's footprint:

```bash
# Pick a known-good variant id from src/themes/registry.ts (e.g. rose-pine-moon)
rg -l 'rose-pine-moon' --hidden -g '!node_modules' -g '!dist' | sort > /tmp/ref.txt
rg -l '<new-variant-id>'  --hidden -g '!node_modules' -g '!dist' | sort > /tmp/new.txt
diff /tmp/ref.txt /tmp/new.txt

# Family-level touchpoints (type unions, family maps, vendor metadata)
diff <(rg -l 'rose-pine' src/ packages/ apps/ scripts/ | sort) \
     <(rg -l '<theme>'   src/ packages/ apps/ scripts/ | sort)
```

Also verify root-level registrations the greps can miss because they do not
mention variant ids:

- [ ] `theme:sync` script wiring in `package.json`
- [ ] Size limits in `test/integration/bundle-size.test.ts`

Every file present only in the reference list is a likely missing touchpoint.
Exclude files that auto-derive from core (imports from
`@lgtm-hq/turbo-themes-core/tokens`) and generated artifacts (rebuild instead).

## 2. Core Implementation

### Theme Pack (`src/themes/packs/<theme>.synced.ts` or `<theme>.ts`)

- [ ] Exports a `ThemePackage` with `id`, `name`, `homepage`, `license`
      (spdx/url/copyright, recommended), `source` (package/version/repository,
      recommended for synced), and `flavors`
- [ ] Each flavor has `id` (lowercase-hyphenated), `label` (full display name,
      e.g. "Gruvbox Dark Hard"), `vendor` (matches family), `appearance`
      (`light`/`dark`), and complete `tokens`
- [ ] No `iconUrl` in flavor definitions (icons resolve via `VENDOR_ICON_MAP`)

### Required Token Groups

- [ ] `background` — base, surface, overlay
- [ ] `text` — primary, secondary, inverse
- [ ] `brand` — primary
- [ ] `state` — info, success, warning, danger
- [ ] `border` — default
- [ ] `accent` — link
- [ ] `typography` — fonts (sans, mono), webFonts
- [ ] `content` — heading (h1-h6), body, link, selection, blockquote, codeInline,
      codeBlock, table

### Registry, Tokens, Icons

- [ ] Theme imported in `src/themes/registry.ts`, flavors spread into `allFlavors`
- [ ] W3C token JSON per variant in `schema/tokens/themes/<variant-id>.tokens.json`
      (`$value`/`$type` format, `$schema` →
      `../../turbo-themes.schema.json#/$defs/ThemeFile`)
- [ ] PNG icon per variant in `assets/img/<variant-id>.png` (typically 24x24)

## 3. Theme Selector Package

- [ ] `ThemeFamily` type union includes the family
      (`packages/theme-selector/src/types.ts`)
- [ ] `THEME_FAMILIES` has name + description
      (`packages/theme-selector/src/constants.ts`)
- [ ] `VENDOR_FAMILY_MAP` and `VENDOR_ICON_MAP` updated; `FLAVOR_DESCRIPTIONS`
      has an entry per variant (`packages/theme-selector/src/theme-mapper.ts`)

## 4. Site Integration

`apps/site/src/data/theme-meta.ts` is the **single source of truth** for the
site. `BaseLayout.astro` and `ThemeDropdown.astro` are data-driven from it —
never hand-edit theme lists in those files.

- [ ] Theme group in `themeGroups` (id, displayName, flavors)
- [ ] All variants in `themeNames` with short labels (e.g., "Mocha" — shorter
      than the token `label`)
- [ ] All variants in `themeIcons` with icon filenames
- [ ] `validThemeIds` auto-derives — verify the count matches the expected total
- [ ] `ThemeDropdown.astro` and `BaseLayout.astro` still import from
      `theme-meta.ts` (no hardcoded theme arrays crept back in)
- [ ] Theme family in the `themes.astro` sidebar (header with icon/name/count,
      button per variant) and in its JS `themeNames` object
- [ ] Hero preview strip buttons added in `index.astro`

## 5. Build Pipeline

- [ ] If synced: script in `theme:sync` (package.json), output path is
      `src/themes/packs/` (NOT `packages/core/...`), version read from
      `node_modules/<pkg>/package.json` into `source.version`, and the build
      succeeds from a clean state (delete the `.synced.ts` file, run
      `bun run build`, confirm it regenerates)
- [ ] `vendorMeta` in `scripts/prepare-style-dictionary.mjs` has correct
      name/homepage; generated `tokens.json` files show them
- [ ] Generated assets rebuilt and committed — discover them with
      `git status` after `bun run build` (theme-selector JS bundles,
      `tokens.json` in core/python/swift trees)

## 6. Examples

Use the section-1 diff to enumerate example files. Then confirm, per hit:

- [ ] Web examples: new variants in `<select>` options and
      `VALID_THEMES`/`LIGHT_THEMES`/`THEMES` arrays (FOUC and main scripts)
- [ ] Files that import from `@lgtm-hq/turbo-themes-core/tokens` were NOT
      hand-edited (they auto-update)
- [ ] Swift example: `ThemeId.swift` enum cases, `ThemeRegistry.swift`
      `ThemeDefinition` palettes, `ThemeRegistryTests.swift` counts, labels, and
      raw values

## 7. Build Verification

```bash
uv run lintro chk          # Expected: 0 issues (run first for fast failure)
bun run build              # Expected: "Build complete!" with new theme count
bun run examples:build     # Expected: all example projects build
bun run test               # Expected: all unit tests pass
bun run examples:test      # Expected: all example E2E tests pass
cd apps/site && bun run build   # Expected: no errors
```

**Visual regression note**: if E2E visual tests fail after adding themes to the
hero strip, that is expected — snapshots are generated on Linux CI. Run the
`maintenance-generate-snapshots.yml` workflow (Actions → Maintenance: Generate
Playwright Snapshots → Run workflow).

## 8. Functional Testing

- [ ] Theme appears in the header dropdown under the correct family group
- [ ] Selecting it updates page styling; header shows the correct icon and short
      label (not the id or full name)
- [ ] Theme persists across refresh and page navigation (no revert to default)
- [ ] Explorer page: family in sidebar, all variants selectable, palette and live
      preview render per variant
- [ ] CSS file generated per variant; CSS variables set when applied

## Quick Fix Reference

| Issue                         | Solution                                              |
| ----------------------------- | ----------------------------------------------------- |
| Theme reverts on navigation   | Add variants to `themeGroups` in theme-meta.ts        |
| Wrong/missing header label    | Fix `themeNames` in theme-meta.ts                     |
| Missing icon                  | Fix `themeIcons` in theme-meta.ts + add PNG           |
| Theme in wrong group          | Fix `VENDOR_FAMILY_MAP` in theme-mapper.ts            |
| Theme not appearing           | Check `ThemeFamily` type, `THEME_FAMILIES` constant   |
| Tests fail on theme order     | Use `data-theme-id` lookups, not array indices        |
| Bundle too large              | Review asset diff; raise bundle budget if intentional |
| CI "Cannot find module"       | Add sync script to `theme:sync` in package.json       |
| tokens.json wrong metadata    | Add to `vendorMeta` in prepare-style-dictionary.mjs   |
| Generated assets outdated     | Run `bun run build` and commit generated files        |
| Missing descriptions          | Add to `FLAVOR_DESCRIPTIONS` in theme-mapper.ts       |
| Sync writes to wrong path     | Change outPath to `src/themes/packs/`                 |
| Visual regression fails       | Run `maintenance-generate-snapshots.yml` workflow     |
| Missing from examples/Swift   | Re-run the section-1 diff and fill the gaps           |

## Review Output Format

```text
## Theme Review: <theme_name>

### Status: PASS / FAIL / PARTIAL

### Checklist Summary
- Discovery diff: clean / N missing files
- Core Implementation: X/Y items
- Theme Selector Package: X/Y items
- Site Integration: X/Y items
- Build Pipeline & Examples: X/Y items
- Build Verification: X/Y items
- Functional Testing: X/Y items

### Missing Items
1. [item]

### Recommendations
1. [recommendation]
```
