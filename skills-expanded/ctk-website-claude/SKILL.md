# CTK Website

Next.js static export (`output: export`) for Christ The King Anglican Church, St. Augustine FL.
Repo: `ChristTheKing-ASA/ctk-website`. Collaborators: wallscaler (Fred), WazDevZm, ctkcraig (Craig).

## Deploy and staging

- **Production**: Cloudflare, serving `ctkasa.com` from the domain root. Builds without any
  `NEXT_BASE_PATH`, so asset paths are `/_next/...`. Verified serving as of 2026-08-12.
- **Staging**: GitHub Pages at `https://christtheking-asa.github.io/ctk-website/`, deployed from the
  `staging` branch by `.github/workflows/staging.yml`. Builds with `NEXT_BASE_PATH=/ctk-website` and
  `NEXT_PUBLIC_NOINDEX=1`, so it is `noindex, nofollow` and does not compete with the real site in
  search. Merge to `staging` to show the parish something; merge to `main` to ship it.
- **No PR previews exist.** An earlier version of this file described per-PR Cloudflare URLs at
  `pr-<n>-ctk-website.fredesere.workers.dev` via a `preview.yml`. That workflow is not in the repo on
  any branch and those URLs 404. Do not rely on it without building it first.
- Cloudflare Workers Builds git integration also runs on PRs and reports a `Workers Builds` check.
  It produces no reviewable URL; the check is a build signal only.

## Keystatic CMS

- Editor at `/keystatic` on every deploy and preview. There is no `/admin` alias; it was removed deliberately.
- Storage: `local` in dev (needs `src/app/api/keystatic/[[...params]]/route.dev.ts`), `cloud` in
  production (Keystatic Cloud project `christ-the-king/ctk-website`, email sign-in, no GitHub needed).
- Editors are invited from the keystatic.cloud dashboard (Fred's account only).
- **Saves through Keystatic Cloud are real commits to this repo.** Test edits belong on a branch via
  the editor's branch switcher, not main.
- `@keystatic/core` is patched via patch-package (`patches/`); `postinstall` applies it. The patch
  reads `NEXT_PUBLIC_KEYSTATIC_PATH` for UI/OAuth routes.

## Commands

- `npm run dev` — local dev with local-filesystem editing
- `npm run build` — static export to `out/`
- `npm run test:run`, `lint`, `npx tsc --noEmit` — CI runs all three before deploy
- `npm run test:pages` / `test:cloudflare` — verify the export for each hosting target

## Conventions

- Content lives in `src/content/` (edited via Keystatic, plain commits like "Update src/content/…").
- Never commit secrets; CF tokens live in `~/Documents/TOOLS/.credentials/`.
