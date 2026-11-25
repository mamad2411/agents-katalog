---
name: design-token-system
description: Architects a framework-agnostic design-token system with primitive/semantic/component tiers, theming and multi-brand/dark-mode alias contracts, and multi-platform export (CSS vars, Tailwind, JS/TS, iOS/Android) from one W3C-DTCG source via Style Dictionary.
when_to_use: Setting up or refactoring a token architecture, building a theme/multi-brand/dark-mode system, exporting one token source to web + native, or adopting Style Dictionary / the W3C Design Tokens format. Distinct from style-responsive-tailwind (consuming tokens in markup) and brainstorm-design (choosing the palette/visual direction).
---

## When to Use

Reach for this skill when the problem is the **token architecture and export pipeline**, not a single component's styling:

- "Set up design tokens / a theme system from scratch"
- "Add dark mode without forking every color"
- "Support multiple brands / white-label from one codebase"
- "Export the same tokens to CSS, Tailwind, and our iOS + Android apps"
- "Adopt Style Dictionary / the W3C Design Tokens (DTCG) format"
- "We have 300 hardcoded hex/px values — give us a governed token layer"

NOT this skill:
- Writing the markup/utility classes that *consume* tokens → style-responsive-tailwind
- Picking the actual palette, type pairing, or visual mood → brainstorm-design
- Translating one Figma frame into a component → implement-from-design
- Building the React component that renders from tokens → build-react-component
- Wiring a cross-platform app shell/build → scaffold-cross-platform-app
- Certifying contrast ratios meet WCAG → audit-accessibility-wcag (this skill *structures* color; it does not verify contrast)

## Steps

1. **Build exactly three tiers — never let a component read a primitive.** This is the whole architecture; get it wrong and theming is impossible.

   | Tier | Names mean | References | Example | Rule |
   |---|---|---|---|---|
   | **Primitive** (global/core) | nothing — raw scale | literal values only | `blue.500 = #2563EB`, `space.4 = 16px` | No semantics. Never themed. Never imported by components. |
   | **Semantic** (alias) | role/intent | → primitives | `color.bg.surface → gray.50`, `color.intent.danger → red.600` | The *only* layer that swaps per theme/brand. |
   | **Component** (scoped) | one part | → semantics | `button.primary.bg → color.intent.brand` | Optional; add only when a component overrides a semantic. |

   Default to **2 tiers (primitive + semantic)**; add component tokens only where a component genuinely diverges. Components and Tailwind/CSS consume **semantic tokens only**.

2. **One source of truth in W3C DTCG JSON.** Use the spec's `$value` / `$type` and `{dot.path}` references so any compliant tool (Style Dictionary v4+, Tokens Studio) can read it. No per-platform hand-edited files.

   ```jsonc
   // tokens/primitive/color.json
   { "color": { "blue": { "500": { "$type": "color", "$value": "#2563EB" } } } }

   // tokens/semantic/color.json  — alias, NOT a literal
   { "color": { "intent": { "brand": { "$type": "color", "$value": "{color.blue.500}" } },
                "bg":     { "surface": { "$type": "color", "$value": "{color.gray.50}" } } } }
   ```
   A semantic token whose `$value` is a literal hex is a bug — it must be a `{reference}`.

3. **Theming = swap the semantic layer, never fork the palette.** Light, dark, and each brand are *alternate semantic files* pointing at the *same* primitives. One `primitive/` set; `semantic/light.json`, `semantic/dark.json`, `semantic/brand-acme.json`. Dark mode flips `bg.surface → gray.900` instead of `gray.50` — the primitives don't move. Never create `blue.500.dark`.

4. **Author color in OKLCH so themes shift predictably.** Build scales in OKLCH (fall back to HSL only if tooling can't): equal lightness steps stay perceptually even and a brand hue rotation keeps contrast. Hardcoded hex per shade drifts. Emit hex/rgb as a *build output* for legacy targets, not as the source.

5. **Cover every token type — color is the easy half.** Define and `$type` all of: `color`, `dimension` (spacing/sizing), `fontFamily`/`fontWeight`/`fontSize`/`lineHeight`/`letterSpacing` (typography), `borderRadius`, `shadow` (elevation), `duration`/`cubicBezier` (motion), and z-index. Derive primitives from a **base scale** (4px grid for spacing, a modular ratio for type); semantics name the use (`space.inline.sm`, `text.heading.lg`).

6. **Export everything from one Style Dictionary config.** One source → many platforms, each with the right transform group and output format:

   ```js
   // style-dictionary.config.js  (v4 — ESM)
   export default {
     source: ['tokens/primitive/**/*.json', 'tokens/semantic/light.json'],
     platforms: {
       css:      { transformGroup: 'css', buildPath: 'build/css/',
                   files: [{ destination: 'vars.css', format: 'css/variables',
                             options: { outputReferences: true } }] }, // keeps var(--x) chains
       tailwind: { transformGroup: 'js', buildPath: 'build/tw/',
                   files: [{ destination: 'tokens.cjs', format: 'javascript/module-flat' }] },
       ts:       { transformGroup: 'js', buildPath: 'build/ts/',
                   files: [{ destination: 'tokens.ts', format: 'javascript/es6' }] },
       ios:      { transformGroup: 'ios-swift', buildPath: 'build/ios/',
                   files: [{ destination: 'Tokens.swift', format: 'ios-swift/class.swift' }] },
       android:  { transformGroup: 'android', buildPath: 'build/android/',
                   files: [{ destination: 'tokens.xml', format: 'android/resources' }] }
     }
   };
   ```
   Run `style-dictionary build`. For each extra theme, run the same config with `semantic/dark.json` swapped into `source` and scope output under `[data-theme="dark"]` (CSS `options.selector`).

7. **Wire Tailwind to the generated tokens — do not retype them.** `tailwind.config` imports `build/tw/tokens.cjs` into `theme.colors/spacing/...`. CSS vars drive runtime theme switching: Tailwind utilities resolve `var(--color-bg-surface)`, and the `[data-theme]` attribute swaps which value that var resolves to. One toggle, zero recompiled CSS.

8. **Forbid raw values in app code with a linter.** Add `stylelint-declaration-strict-value` (web CSS) or an ESLint/lint rule that bans hex, `rgb(`, and bare `px` outside `tokens/` and `build/`. Raw values must fail CI, not slip through code review.

9. **Govern it as a published API.** Fix a naming grammar `category.role.variant.state` (e.g. `color.bg.surface.hover`); semver the published token package (removed/renamed semantic token = **major**, added = minor, primitive value tweak = patch); keep a CHANGELOG; treat the `semantic` layer as the public API and primitives as private/internal.

## Common Errors

- **Components reading primitives** (`button { color: blue.500 }`). Dark mode and rebrand degrade to find-and-replace. Components must reference semantics only.
- **Forking the palette per theme** (`blue.500.dark`). Palette count explodes and brands drift. Themes swap the *semantic* alias target; primitives are shared and immutable.
- **Semantic tokens holding literal values** instead of `{references}`. The indirection is the entire point — a literal hex in a semantic token can't be retargeted by a theme.
- **`outputReferences: false` (the default) flattening CSS vars.** The build bakes `#2563EB` into every rule, killing runtime theme switching. Set `options: { outputReferences: true }` so `var(--color-intent-brand)` chains survive.
- **Duplicating tokens into `tailwind.config` by hand.** They desync within the first week. Import the Style Dictionary build output; never maintain two sources.
- **No grid/scale — arbitrary `13px`, `17px` primitives.** Defeats consistency. Primitives come from a 4px (or 8px) grid and a modular type ratio.
- **Treating contrast as solved because colors are tokenized.** Tokens organize color; they don't guarantee `bg.surface`/`text.primary` meet 4.5:1. Run audit-accessibility-wcag on each theme.
- **Component tokens for everything**, including parts that never override a semantic. Pure bloat. Add a component token only where it diverges from the semantic.
- **Per-platform manual edits to `build/` outputs.** They're regenerated; your edit vanishes on the next build. Fix the source and rebuild.
- **No versioning/changelog on the token package.** A renamed semantic token silently breaks every consumer. Semver it; a rename is a breaking (major) change.

## Verify

1. **Tier discipline:** `grep` app/component source — zero references to primitive names (`blue.500`, `space.4`) and zero raw hex/`rgb(`/bare `px`. Every match is a violation.
2. **Aliases resolve:** every semantic `$value` is a `{reference}`, not a literal; `style-dictionary build` reports **0 unresolved references** and exits `0`.
3. **One source, many outputs:** a single `style-dictionary build` produces CSS, Tailwind, TS, iOS, and Android artifacts from the same `tokens/` tree (no hand-edited platform file).
4. **Theme swap is alias-only:** diff `semantic/light.json` vs `semantic/dark.json` — they differ only in reference *targets*; `primitive/` is byte-identical across themes. Adding a brand touches no primitive.
5. **Runtime switch works:** toggling `[data-theme="dark"]` on the built CSS recolors the page with **no CSS recompile** (proves `outputReferences` chains survived).
6. **Lint gate is live:** committing a raw `#fff` or `12px` in app code fails CI, not review.
7. **Native parity:** the same semantic token (e.g. `color.intent.brand`) yields the same color in `build/css/vars.css`, `build/ios/Tokens.swift`, and `build/android/tokens.xml`.
8. **Governance:** naming matches `category.role.variant.state`, the package carries a semver + CHANGELOG, and a token rename ships as a major bump.

Done = one W3C-DTCG source builds all platforms with zero unresolved references, components reference semantics only (lint-enforced in CI), themes/brands swap via alias targets over shared immutable primitives, and runtime theme switching recolors with no recompile.
