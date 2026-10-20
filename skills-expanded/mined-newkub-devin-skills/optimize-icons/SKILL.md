---
name: follow-lib-iconify-optimize icons
description: Optimize Iconify — offline bundles, on-demand loading, subsetting
argument-hint: "[scope]"
related:
  - follow-lib-iconify
  - run-bench
  - deep-review-codebase
  - report-bundle
  - report-before-after
---

## Goal

Reduce the bundle size and network cost of Iconify usage — offline bundles, on-demand loading and subsetting icon data

## Scope

Use when optimizing icons that use Iconify — covers bundle analysis, converting runtime API → offline data, custom subsets and lazy loading

## Execute

### 1. Baseline

> Goal: measure the current icon cost before optimizing

1. Do `/deep-review-codebase` or `/report-bundle` to see the size of icon-related code in the bundle
2. Check usage patterns: `import { Icon }`, `icon="..."` strings, `@iconify-json/*` imports — scan which sets and which icons are used
3. Identify anti-patterns: importing the whole `icons.json`, dynamic icon names hitting the API at runtime, unused icons

### 2. Prefer Offline Bundles

> Goal: convert runtime API fetching to bundled icon data

1. Install `@iconify-json/<set>` for every set in use — replacing fetches from `api.iconify.design`
2. Pass icon data directly to the component: `<Icon icon={mdiHome} />` importing from `@iconify-json/mdi` (tree-shakeable per-icon)
3. Keep the API runtime only for icon names genuinely defined at runtime (e.g. an icon picker)

### 3. Subset Icon Data

> Goal: bundle only the icons actually used

1. Use `@iconify/utils` (`getIcons`, `minifyIconSet`) to generate a subset JSON containing only the icons used — see official docs for the latest API
2. For UnoCSS `presetIcons`: import only the collections used in `uno.config.ts`
3. For the Tailwind plugin: specify the icon sets in the plugin config — never load every set
4. If there are very few icons, consider inline SVG instead of Iconify entirely

### 4. Lazy-Load Dynamic Icons

> Goal: shrink the initial bundle for icons not needed at load time

1. Dynamically import icon data for non-critical sections
2. Use `@iconify/utils` loader functions for on-demand icon loading — see official docs
3. For the `iconify-icon` web component — icons already load on demand but you pay the API runtime; weigh against an offline bundle

### 5. Verify And Compare

> Goal: measure after optimizing, against the baseline

1. Re-run `/report-bundle` or `/deep-review-codebase`, then compare with the baseline via `/report-before-after`
2. Check that all icons still render correctly — no missing icon
3. If the bundle didn't shrink or an icon disappeared → revert that point and report

## Rules

- Offline data (`@iconify-json/*`) always comes before the API runtime — unless the icon truly must be dynamic
- Never import a large set's whole `icons.json` file (e.g. mdi has thousands of icons)
- The subset must cover every icon actually used — scan usage before generating
- Preserve behavior — optimizing must not make icons disappear or flicker
- Use `/follow-lib-iconify` for the overview
- Use `/run-bench` if load/render impact must be measured numerically

## Expected Outcome

- Icon bundle smaller versus the baseline, with real numbers
- No runtime API calls for static icons
- Every icon still renders correctly
