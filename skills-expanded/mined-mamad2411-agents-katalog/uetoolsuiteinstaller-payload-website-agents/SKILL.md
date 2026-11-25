# Docusaurus website instructions

## Source of truth

- Docs content lives in `../Docs`, not `website/docs`.
- Navigation is derived from `Docs/`, `_domains.json`, `_category_.json`, front matter, and `domainCatalog.ts`.
- `sidebars.ts` is a thin shell.
- Never edit `.docusaurus/`, `build/`, `build-debug/`, or `node_modules/`.

## Frontend rules

- Keep browser-visible paths Docs-relative.
- Put pure path/tree/Markdown transformations in standalone modules with unit tests.
- Keep React components responsible for rendering and interaction, not filesystem/domain policy.
- Keep API transport and runtime discovery outside presentational components.
- Preserve SSR safety around `window`, `localStorage`, and browser APIs.
- Treat editor serialization as data preservation.
- Do not enable rich editing for syntax that cannot round-trip safely.
- Prefer explicit types over new `as any` casts.

## Validation

Current baseline:

```powershell
npm run typecheck
npm run build
```

After the proposed test harness exists:

```powershell
npm run test:unit
npm run test:editor
npm run test:e2e -- --project=chromium
```

Use `npm ci` when validating the committed lockfile.
