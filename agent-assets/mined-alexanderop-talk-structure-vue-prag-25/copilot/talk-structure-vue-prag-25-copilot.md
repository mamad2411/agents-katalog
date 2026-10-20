# AI Coding Agent Guide

Project Snapshot
- Tech: Slidev + Vue 3 + TypeScript; local theme in `theme/`.
- Entry: `slides.md` with `theme: ./theme`; MDC + `<script setup lang="ts">`.
- Components: auto-registered from `components/` (e.g., `Counter.vue`).
- Theme provides `layouts/*`, `components/LayoutFooter.vue`, `styles/*`.
- Output: static SPA in `dist/`.

Dev Commands
- Install: `pnpm install`
- Dev: `pnpm dev` (http://localhost:3030)
- Build: `pnpm build` → `dist/`
- Export: `pnpm export` (PDF/PNG via Slidev)

Structure Map
- `slides.md`: canonical feature examples; imports `pages/imported-slides.md` via `src:`.
- `components/`: slide-level Vue SFCs; use directly (`<Counter :count="10" />`).
- `snippets/`: external code for Shiki includes; keep `#region` tags stable (`<<< @/snippets/external.ts#snippet`).
- `theme/layouts/*.vue`: named layouts via frontmatter (`layout: cover|default|quote|...`).
- `theme/components/LayoutFooter.vue`: page number + gradient; included by `theme/layouts/default.vue`.
- `theme/styles/index.ts`: imports base + `layouts.css` and `prism.css`.

Patterns That Matter
- Clicks/marks: `v-click`, `v-mark.*`; motions via `v-motion`.
- Code hovers/errors: `twoslash` code blocks; Monaco via `{monaco}` / `{monaco-run}`.
- Backgrounds/assets: prefer `handleBackground()` / `resolveAssetUrl()` in `theme/layoutHelper.ts`.
- Dark mode: `isDark` from `@slidev/client/logic/dark.ts` is available in theme components.
- Multi-file slides: split under `pages/` and reference with frontmatter `src:`.

Where to Edit
- New slides/content: `slides.md` or `pages/*` with `src:`.
- Global footer/branding: `theme/components/LayoutFooter.vue`.
- New reusable layout: add to `theme/layouts/` and use `layout: <name>`.
- Theme-wide styles: `theme/styles/layouts.css` or `prism.css`.

Deploy/Hosting
- Netlify: `netlify.toml` uses `npm run build`, publishes `dist`, `NODE_VERSION=20`.
- Vercel: `vercel.json` `buildCommand: npm run build`, `outputDirectory: dist`, rewrite to `index.html`.

Checks Before PR
- Run `pnpm dev` and click through multiple layouts; verify dark/light.
- Keep snippet region tags unchanged to avoid breaking includes.
- If changing output dir, update both Netlify and Vercel configs.
