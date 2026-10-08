# kui-react — Cursor rules (legacy single-file format)
# Canonical source: AGENTS.md
# Modern rules: .cursor/rules/kui-react.mdc

Before writing code, fetch the catalog so you know what already exists:
  GET /api/registry?index=1   (full list, ~5x smaller — no source)
  GET /api/registry           (full registry incl. source per component)
  GET /llms-full.txt          (markdown dump)
Offline fallback: public/registry/components.json

⚠️ CATALOG SYNC — REQUIRED
After adding, renaming, or removing a component (modules/ui/, modules/app/, modules/domains/<vertical>/),
a theme (app/theme/<vertical>/), a showcase section file, or a showcase.menu.ts entry, run:
  npm run registry:snapshot
before committing. This regenerates public/registry/* and public/components/*.md from the showcase data.
The same script also runs via the `prebuild` npm hook before `npm run build`, but commit the regenerated
files so the catalog stays in lockstep with the code. A stale catalog misleads every AI agent.

Hard rules (see AGENTS.md for full detail):
1. 'use client'; at the top of every modules/ui/, modules/app/, modules/domains/ file.
2. Named exports only — no default exports.
3. Use cn() from @/libs/utils/cn for classNames. No template literals, no string concat.
4. Token-only styling: bg-primary, text-text-secondary, border-border-focus. No raw hex / rgb / hsl.
5. Icons: Font Awesome only. Named imports from @fortawesome/free-solid-svg-icons or free-brands-svg-icons.
   No lucide-react, no heroicons, no react-icons, no inline SVG, no emoji as icons.
6. Accessibility: focus-visible:ring-2 focus-visible:ring-border-focus on interactive elements,
   aria-* attributes per pattern, disabled:opacity-50 disabled:cursor-not-allowed,
   aria-hidden="true" on decorative FontAwesomeIcon.
7. Spread ...rest to the root element.
8. No business logic in modules/ui/.

Where new code goes:
  modules/ui/                              — atoms & molecules
  modules/app/                             — organisms, shells, forms, providers
  modules/domains/<vertical>/              — industry-specific components
  app/theme/<vertical>/                    — full multi-page demos

When adding a domain vertical, also:
  - add a section file in modules/showcase/data/sections/domain-<vertical>.showcase.tsx
  - register entries in modules/showcase/data/showcase.menu.ts (sidebar is static-driven)

When porting a component, follow composes[] recursively. usedBy[] is the inverse.
