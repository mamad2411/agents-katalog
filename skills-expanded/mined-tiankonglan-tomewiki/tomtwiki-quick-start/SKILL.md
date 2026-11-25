---
name: tomtwiki-quick-start
description: >-
  Turns a fresh TomeWiki clone into a named unofficial fan wiki.
  Fills site identity, SEO, homepage copy, theme, and brand images from a short
  game brief. Use when the user names a game and wants this template customized,
  when Example Game placeholders remain, or when they say 建站, 快速接入,
  改成自己的站, or bootstrap a guide site from this repo.
---

# TomeWiki Quick Start

Keep this folder identical in three places: `.claude/skills/tomtwiki-quick-start/` (Claude Code), `.cursor/skills/tomtwiki-quick-start/` (Cursor), and `.agents/skills/tomtwiki-quick-start/` (Codex).

A new clone of [TomeWiki](https://github.com/tiankonglan/tomtwiki) still reads "Example Game". This skill swaps that identity using knobs the template already ships. It does not add routes, features, or a new content model.

Open a single file under `references/` when you need it. Do not dump the whole folder into context.

## Permitted edits

`references/07-checklist.md` is the full path list. Nothing else is in scope.

Leave these alone:

- App Router and most UI (`src/app/**`, `src/components/site/**` except the two brand/font entry files)
- `template-contract.json`
- Auth, databases, billing, admin screens
- Invented Steam IDs, patch numbers, loot tables, or publisher endorsement
- `src/app/favicon.ico` (clashes with `public/favicon.ico` and 500s the icon)
- Guide category folder names (must keep matching `content/guides/<slug>/`)
- Stock `public/logo.png`, `favicon.png`, or `og-image.png`

## Finish line

`pnpm install` once if `node_modules` is missing.

After the file edits:

- `pnpm validate:site`
- `pnpm build`

If the new logo does not appear, Next is serving a cached asset; delete `.next` and rebuild. `pnpm quality:gate` is optional and matches CI (format, lint, types, validate, build).

Repair failures only on permitted paths unless the user widens the job.

## Brief

`references/00-brief.md` — game title and domain are enough to start. Ask at most once for holes, then leave searchable `TODO:` comments. Ignore Steam ID, analytics, and extra languages unless the user gave them.

## Order of work

| Step | File |
|------|------|
| Worker + env | `references/01-env-and-worker.md` |
| Game / site identity | `references/02-identity.md` |
| Title, description, keywords | `references/03-seo.md` |
| Homepage strings (same blocks) | `references/04-homepage.md` |
| Accent color and visual preset | `references/05-theme.md` |
| Logo, favicon, social preview | `references/06-brand-assets.md` |
| Permitted paths and sign-off | `references/07-checklist.md` |

## Brand images

Call the generator that already lives in this repo. Do not add a new image script.

```bash
node scripts/gen-brand-assets.mjs \
  --game "<gameFullName>" \
  --short "<gameShortName>" \
  --domain "<domain>" \
  --color "<#RRGGBB>" \
  --tagline "<short tagline>"
```

Pass `--emblem path/to/emblem.png` when the user has a square mark. `sharp` is already a dependency.

## Hand off

Real guides belong in `content/guides/`; entity records in `content/entities/`. Extra locales follow `docs/QUICKSTART.md` section 7 (drop `// scaffold-default:en-only`). Domain bind, analytics, and `pnpm cf:deploy` / Vercel import stay with the user.
