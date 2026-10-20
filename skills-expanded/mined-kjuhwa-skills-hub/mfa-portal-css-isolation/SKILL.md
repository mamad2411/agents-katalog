---
tags: [design, mfa, portal, css, isolation]
name: mfa-portal-css-isolation
description: Isolate Tailwind CSS in Module Federation portals using lazyStyleTag injection, postcss-prefix-selector with :where() specificity control, scoped root elements, and Headless UI PortalGroup
category: design
trigger: When adding Tailwind CSS to a Module Federation remote that must not pollute host or sibling remotes, or when overlay components (Dialog, Tooltip, Popover) render outside the scoped root
version: 1.1.0
source_project: lucida-ui
linked_knowledge:
  - tailwind-mfa-css-isolation-pitfalls
  - multi-layer-css-architecture
---

# MFA Portal CSS Isolation

## Problem
Tailwind's preflight resets (`*`, `html`, `body`) and global styles leak across Module Federation boundaries, breaking sibling remotes. Portal-based overlays (Dialog, Tooltip) render outside the scoped container, losing Tailwind styles entirely.

## Steps

1. **Separate webpack CSS rule** for the Tailwind module:
   - `include` targets only the Tailwind module path
   - Main CSS rule must `exclude` the same path to avoid double-processing
   - Use `style-loader` with `injectType: 'lazyStyleTag'` (on-demand injection)
   - `css-loader` with `importLoaders: 1, import: false` (let PostCSS handle @import)

2. **postcss-prefix-selector** with `:where()` wrapper:
   - Prefix: `:where(.nds-root)` — zero specificity, overridable by host
   - `:root`/`:host` → `:where(.nds-theme)` (token scoping)
   - `[data-theme="dark"]` → `:where(.nds-theme)[data-nds-theme="dark"]` (namespaced theme attributes)
   - Class selectors: generate both descendant and self forms (`.btn` → `:where(.nds-root) .btn, :where(.nds-root).btn`)
   - Exclude `@keyframes`, `@property`, `@font-face` internals from prefixing

3. **lazyStyleTag lifecycle**:
   - `portalStyles.use()` on mount, `portalStyles.unuse()` on unmount
   - CSS only active while the remote is rendered

4. **NdsPortalProvider** — body-level portal root:
   - `useLayoutEffect` creates `<div id="nds-portal-root" class="nds-root nds-theme">` on `<body>`
   - Headless UI `<PortalGroup target={portalRef}>` redirects all portals
   - `useEffect` syncs `data-nds-theme` attribute when theme changes
   - Singleton: checks for existing `#nds-portal-root` (supports HMR)
   - React context exposes portal root for custom consumers

5. **Wrap all overlay consumers**:
   - Every Dialog, Tooltip, Menu, Popover renders inside the PortalGroup target
   - Never nest PortalProviders — one per remote boundary

## Pitfalls
- `@keyframes` must be excluded from prefixing — scoped keyframe names break animations
- `@property` (CSS Houdini) declarations must also be excluded
- `useLayoutEffect` not `useEffect` for portal root — must exist before first child render
- `overflow: hidden` on main container clips portals rendered as children — body-level root avoids this
- Portal.Group typing: not publicly exported in Headless UI types, requires cast
- Multiple MFA remotes: each should check for existing portal root element before creating

## See also
- `content.md` for full webpack config, selector transform function, and provider implementation
