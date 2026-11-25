---
name: expand-site-language
description: >
  Add a NEW language to an EXISTING site across ALL its content, and translate the pages later
  without blocking. Use when the owner says "add Armenian / Spanish / French to the whole site",
  "make the site multilingual", "translate the whole site into X", "scale this to more languages",
  "add a new language to all pages/sections", or "add a locale". This is the ONLY correct way to
  add a language to existing content. Do NOT improvise it by hand and do NOT re-compose a group —
  neither adds a per-page locale to existing pages, and re-composing overwrites what is there. Two
  scripts in this skill's own folder do the work: fan-out-site-language.mjs (fans the language out,
  seeded with the default language so the site is valid instantly, no translation API) and
  translate-content-page.mjs (the non-blocking runner — you translate the strings later). Self-
  sufficient: plain Node, no external service, no other agent.
version: 1.0.0
metadata:
---

# expand-site-language

> Informational, not binding. **Know a better way for the case in front of you — do it your way and
> say so.** You are trusted with the creative work on this project.

The ONE way to take a site that already has content in one or two languages and **safely scale it
to another language**. Deterministic file operations, **NO code generation, NO external translation
API** (you are the translator — subscription rule). Self-sufficient: any single agent can do it.

## 🛑 Why a dedicated capability (do not improvise)

Adding a language to an **existing** site means creating a `_data/<lang>.ts` for **every** group and
**every** post, patching each `index.ts` + `group.ts`, and protecting SEO. **No other tool does this:**

- **Creating a page by hand** — a new page is a new page; it does nothing for the dozens that already
  exist, and each of them needs its own `_data/<lang>.ts`.
- **Adding the language to the menu manifest only** — the language then shows in the switcher while the
  pages behind it do not exist. A visible broken language is worse than an absent one.
- **Re-composing a group** — it **overwrites** existing content. Never use it to add a language.

If you are tempted to reach for one of those to add a language: **stop and use this skill instead.**

## The model

- Languages are **build-time** (`NEXT_PUBLIC_SUPPORTED_LANGUAGES`). A language must be in the set
  **before** you fan it out — add it via **manage-app-settings** first, then rebuild.
- Each post = `_data/{meta, en(base), <lang>(override), index}`. Each group = `_data/{en, <lang>, index,
  group.ts}`. The fan-out writes the `<lang>` files and patches the indexes — by construction.
- 🪦 **SEEDING IS CANCELLED IN THIS PROJECT (step 256, 2026-09-20). Do NOT copy the default language
  into `_data/<lang>.ts`.** This bullet used to say the opposite, and following it now would build
  exactly the doorway it was written to prevent. Two reasons, both measured:

  1. **The fallback already does the job.** `resolveLocalizedBody` serves the base language for any
     language without a cell, so the site is valid the instant the build finishes — **without writing
     a single seed file**. The seed bought nothing and cost one file per page.
  2. **A seed is now indistinguishable from a real translation.** Indexability is DERIVED from the
     data (`lib/seo/translation-state.ts`): a page counts as translated when it has its **own
     non-empty cell**. A cell copied from `en` IS non-empty — so the seeded page would declare itself
     a translation, enter `hreflang`, enter the sitemap and sit in the index as a cross-language
     duplicate of the original.

- **🔒 Doorway guard — now BY CONSTRUCTION, not by a marker.** The `needsTranslation` marker this
  skill relied on **does not exist in this project**. Instead: no cell → the language is not
  translated → the page is served `noindex`, is absent from every `hreflang` set and from the
  sitemap, while staying fully visible to a human. When a real translation is written, all three
  signals switch on together, because all three read one source. `npm run check:seo-html` enforces
  this on the BUILT HTML and refuses to deploy a build that breaks it.

- **Translation itself is a separate run** — the `translate-pending` skill, by the agent, on the
  owner's subscription. This skill enables a language; that one fills it.
- **Non-blocking.** The fan-out returns the pages that need translating in `pagesNeedingTranslation`;
  **name them to the owner so a step per language can be opened in the panel**, listing those pages in
  its plan. Translation happens later, in that step, possibly with a different model — the main work is
  never blocked by translation limits. The scripts write no steps themselves: steps live in the
  product's dossier, and one writer keeps them, not three.

## Flow

1. **Ensure the language is in the set.** Not there yet → add it with **manage-app-settings**
   (the panel's Languages page, or `POST /api/config/languages`) and rebuild. The fan-out refuses a language not in the set.
2. **Fan it out.** `node fan-out-site-language.mjs --out <slot-root> --lang <L>` — `--dry-run` first (restate +
   confirm, §8.2), then for real. **REBUILD** (Deploy in the panel's footer) to publish the new routes
   (seeded, noindex). The menus (header / footer / left / right) update automatically.
3. **Translate later (non-blocking), when you choose.** `node translate-content-page.mjs --out <slot-root> --lang <L> --op next` in a
   loop: it returns the next pending page → you translate the **strings only** (keep the block kinds and
   order, keep the root anchor and `/<lang>/` links) → call again with `{ op:"write", tab, slug,
   translations }`. Repeat until `remaining: 0`. Honor any owner notes on the dev-step (e.g. "focus on
   Spanish law, link real statutes") for regional value.
4. **The runner does NOT deploy.** When translations are written, tell the owner: *press **Deploy** in
   the footer* to publish — the translated pages then flip from noindex to indexable.

## Confirm before mutating (§8.2)

> If I understood correctly: **add language «<lang>»** across <N> groups / <M> pages, seeded with the
> default language «<def>» (noindex until translated), and open one translation step. Shall I proceed?

`--dry-run` → preview → owner yes → the real run.

## If the tool errors (not a refusal)

A **refusal** (`ok:false, refused:true` — language not in the set, structure-parity violation) → fix
and retry. A crash (`MODULE_NOT_FOUND`, an exception) means the script is **broken** — stop, report the
exact error, wait. Never hand-author the locale files as a workaround; a broken script is repaired,
never bypassed.

## How to call

- **The two commands:**
  - `node fan-out-site-language.mjs --out <slot-root> --lang <L> [--dry-run]`
  - `node translate-content-page.mjs --out <slot-root> --lang <L> --op next` → then `--op write --tab <tab> --slug <slug>` with the translated strings
- **Standalone (no panel at hand)** — plain file edits:
  ```bash
  # 1) fan out (default-language seed + noindex + per-language step)
  node .claude/skills/expand-site-language/fan-out-site-language.mjs --out . --lang hy --dry-run
  node .claude/skills/expand-site-language/fan-out-site-language.mjs --out . --lang hy
  # 2) translate, page by page (you supply the translated strings)
  node .claude/skills/expand-site-language/translate-content-page.mjs --out . --lang hy --op next
  node .claude/skills/expand-site-language/translate-content-page.mjs --out . --lang hy --op write \
    --tab news --slug sample-1 --data translations.json
  npx tsc --noEmit   # then REBUILD (Deploy) to publish
  ```

## Self-sufficient

The skill lives in this project (`.claude/skills`) and depends on nothing outside it — a single agent
can extend a site's languages on its own.
