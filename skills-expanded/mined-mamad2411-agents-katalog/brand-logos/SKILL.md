---
name: brand-logos
description: Fetch official brand/product/tool logos (Stripe, GitHub, Notion, AWS, Figma, etc.) as clean SVGs from SVGL (svgl.app) — as saved .svg files, inline markup, or installed React components. Check this whenever logos or SVGs come up, e.g. adding brand marks to integration/partner rows, footers, pricing tables, or slides; replacing a blurry logo with a vector; getting light/dark variants; or finding an official logo. Prefer it over hand-writing SVG markup or grabbing random files. Skip for generic UI icons, illustrations, charts, favicons from an existing logo, or designing a brand-new custom logo.
---

# SVGL Brand Logo

SVGL is a library of brand/product/tool logos served as clean, optimized SVGs. It exposes a free, unauthenticated REST API at `https://api.svgl.app` and a shadcn-compatible registry for installing logos as React components. Use it instead of hand-writing logo SVGs or pulling random files off the web, since the markup is consistent and maintained.

## When to use this skill

Trigger on any request to find, download, add, embed, or install a brand, product, company, or tool logo, even when the user does not name SVGL. Common phrasings: "add the X logo", "I need an SVG icon for X", "put a row of integration logos here", "get the dark-mode version of the Y logo", "install the Z logo as a component".

This skill is for *known brand/product logos*. It is not for generic UI icons (use an icon set like Lucide/Heroicons), illustrations, or a company's own custom logo that wouldn't be in a public library.

For social icons in app UI (e.g. share buttons, profile links, footer social rows), prefer the project's existing shared icon registry if it already has one — reuse it rather than fetching from SVGL and creating a parallel logo source. Only reach for SVGL when no such registry exists or the needed mark is missing from it.

## Choosing the approach

Decide between the two workflows based on what the user is building:

- **REST API (download the raw SVG)** — the default. Use when the user wants an `.svg` file on disk, inline SVG markup, or a logo for a non-React stack (plain HTML, Vue, Svelte, Astro, email, design files). Also use it for quick lookups and "does SVGL have X?" questions.
- **shadcn registry (install as a React component)** — use only when the project already uses React + shadcn (there's a `components.json`) and the user wants a reusable component rather than a static file. When unsure which the project uses, check for `components.json` and the framework before assuming. A request for "the SVGL CLI" means this flow (SVGL has no CLI of its own — it's the shadcn CLI against SVGL's registry).

## REST API workflow

Base URL: `https://api.svgl.app`. All responses are JSON except the raw SVG endpoint.

Each logo entry looks like this (note that `route` and `wordmark` may be either a single URL string or a `{ light, dark }` object, and `category` may be a string or array):

```json
{
  "id": 573,
  "title": "GitHub",
  "category": "Software",
  "route": {
    "light": "https://svgl.app/library/github_light.svg",
    "dark": "https://svgl.app/library/github_dark.svg"
  },
  "wordmark": {
    "light": "https://svgl.app/library/github_wordmark_light.svg",
    "dark": "https://svgl.app/library/github_wordmark_dark.svg"
  },
  "url": "https://github.com/",
  "brandUrl": "https://brand.github.com/"
}
```

### Endpoints

| Goal | Request |
| --- | --- |
| Search by title | `GET https://api.svgl.app?search=<query>` |
| List a category | `GET https://api.svgl.app/category/<category>` (e.g. `software`) |
| Discover categories | `GET https://api.svgl.app/categories` |
| All logos (optionally capped) | `GET https://api.svgl.app?limit=<n>` |
| Optimized SVG markup | `GET https://api.svgl.app/svg/<name>.svg` |
| Unoptimized SVG markup | `GET https://api.svgl.app/svg/<name>.svg?no-optimize` |

The `<name>` for the `/svg/` endpoint is the filename from a `route` URL without the path/extension prefix — e.g. the route `https://svgl.app/library/github_light.svg` maps to `/svg/github_light.svg`. The optimized version (run through svgo) is almost always what you want; only reach for `?no-optimize` if the user needs the original markup (e.g. to diff against a source file or preserve specific structure).

### Steps

1. **Search** by the brand name: `curl -s "https://api.svgl.app?search=stripe"`. If nothing returns, try a shorter or alternate spelling, or list the likely category to browse.
2. **Pick the right variant** from the result:
   - If `route` is a plain string, there's one universal logo — use it.
   - If `route` is `{ light, dark }`, choose based on where it will render: `dark` variants are designed to sit on dark backgrounds (light artwork), `light` variants on light backgrounds. When the app supports both themes, grab both and switch with CSS. Don't assume — match the destination background.
   - Use `wordmark` only when the user explicitly wants the logo *with the company name* (the wordmark/lockup) rather than the icon mark. If the user says "logo" generically, prefer `route` (the icon mark).
3. **Download** the chosen SVG into the project's existing asset location rather than inventing a new folder. Look for where other logos/icons already live (e.g. `public/`, `public/logos/`, `src/assets/`, `app/assets/icons/`, `static/`) and match that convention and naming style.
4. **Confirm** what you saved and where, and mention if both light/dark files were stored.

Example — download the GitHub icon (light + dark) into an existing assets dir:

```bash
curl -s -o public/logos/github-light.svg "https://api.svgl.app/svg/github_light.svg"
curl -s -o public/logos/github-dark.svg  "https://api.svgl.app/svg/github_dark.svg"
```

If the user wants it inline (e.g. to paste into a component), fetch the markup and embed it directly rather than saving a file:

```bash
curl -s "https://api.svgl.app/svg/stripe.svg"
```

## shadcn registry workflow

SVGL has no standalone CLI of its own. When a user asks for "the SVGL CLI", "svgl cli", or "install via the SVGL CLI", they mean this flow — the shadcn registry, driven by the standard `shadcn` CLI pointed at SVGL's registry. Don't go looking for a separate `svgl` command; route these requests here.

For React projects already on shadcn, logos can be installed as typed components. Just run the install command, using the project's existing package manager (check for `pnpm-lock.yaml`, `package-lock.json`, `yarn.lock`, or `bun.lockb` and match it — don't introduce a new one):

```bash
pnpm dlx shadcn@latest add @svgl/github
# npm:  npx shadcn@latest add @svgl/github
# yarn: yarn dlx shadcn@latest add @svgl/github
# bun:  bunx shadcn@latest add @svgl/github
```

The `@svgl/...` namespace resolves out of the box — current `shadcn` versions know how to fetch from `https://svgl.app/r/<name>.json` without any project config. This generates React components (e.g. a `GithubLight` component) that accept standard `SVGProps`, so the user can size and style them like any other component. The component name maps to the same logo names used by the API.

**Fallback:** only if the CLI can't resolve the `@svgl` namespace (e.g. an older shadcn version), register it explicitly in `components.json` and re-run:

```json
{
  "registries": {
    "@svgl": "https://svgl.app/r/{name}.json"
  }
}
```

## Cautions

- **Rate limits.** The API is open and unauthenticated but rate-limited to prevent abuse. Don't loop over hundreds of logos or poll it; search once, fetch the specific SVGs you need, and cache the files locally instead of re-downloading.
- **Brand usage rights.** SVGL distributes logos for convenience, but trademark and brand-guideline rules still apply. Follow the brand owner's guidelines (the entry's `brandUrl`/`url` often points to them) — don't recolor, distort, or imply an endorsement/partnership the user doesn't have.
- **Don't clone SVGL.** Per SVGL's own terms, the API is meant for extensions, plugins, and tools that help the community — not for scraping its catalog to rebuild a competing logo library.

## Output

After fetching or installing, tell the user concisely:

- Which logo(s) and variant(s) you used (icon vs wordmark, light/dark).
- Where files were saved or which component(s) were installed.
- Any follow-up they should handle themselves (theme switching wiring, brand-guideline review for prominent/marketing use).
