---
name: docs-sites
description: "Documentation sites: choosing a generator (Starlight, Docusaurus, VitePress, MkDocs Material, mdBook, Mintlify), information architecture and navigation, search, versioning, code blocks with tabs and copy buttons, docs as code with previews, link checking and prose linting, internationalisation, and feedback. Read before creating or reorganising a documentation site."
---

# Documentation sites

The generated docs site is the starter template with its example pages
still in the sidebar, navigation that mirrors the folder tree five levels
deep, search that finds nothing, every page versioned from day one, code
blocks with no language or copy button, a callout on every paragraph,
links broken by the last rename, and a "Was this helpful?" widget nobody
reads. This skill: choosing the generator, organising by what readers do,
search, versioning, code blocks, docs as code with checks in CI,
translation and feedback. The page layout is in `ui-page-docs`; what goes
on each page is in `docs` and its family.

## 1. Choose the generator

| Generator | Built on | Choose it when |
|---|---|---|
| Starlight | Astro | The default for a new static docs site in any stack: Pagefind search, i18n, code blocks with titles and copy buttons, tabs, asides, steps and file trees built in |
| Docusaurus | React | A React team, versioned docs, a blog beside the docs; versioning and i18n built in, MDX |
| VitePress | Vue and Vite | A Vue or Vite project; small and fast, local search built in, the build fails on dead links |
| Material for MkDocs | Python | A Python project, with API reference from docstrings through mkdocstrings; versions with mike |
| Sphinx | Python | A large existing reStructuredText project, cross-referenced API docs, Read the Docs; MyST for Markdown |
| mdBook | Rust | A book-shaped guide for a Rust project; `mdbook test` runs its Rust examples; API reference stays on docs.rs |
| Fumadocs or Nextra | Next.js | Docs inside an existing Next.js application |
| Mintlify, ReadMe, GitBook | Hosted | An API playground from OpenAPI, editors who are not engineers, no build to run; weigh the cost and the lock-in |

- The project's own stack wins: a React team keeps a Docusaurus site
  alive, and an unfamiliar generator gets abandoned.
- Material for MkDocs has been in maintenance mode since late 2025 while
  its team builds Zensical, which reads the same `mkdocs.yml`. Existing
  sites keep working; for a new one, check the state of both first.
- Never build a docs site from scratch: search, navigation, anchors and
  code blocks are solved problems.

```sh
npm create astro@latest -- --template starlight   # Starlight
npx create-docusaurus@latest docs classic          # Docusaurus
npx vitepress init                                 # VitePress
mdbook init docs                                   # mdBook
```

Then remove every example page, logo and link the template ships with.

## 2. Information architecture

- Top-level sections by what the reader is doing, named in their words:
  **Get started** (tutorials), **Guides** (how-to), **Concepts**
  (explanation), **Reference** (API, CLI, configuration), plus the
  changelog and troubleshooting.
- The landing page routes by task, with 3 to 6 entry points: "Install",
  "Build your first ...", "API reference", "Upgrade from v1". Not a
  marketing hero.
- A sidebar two or three levels deep, 5 to 9 items per group, in the order
  of use (reference may go alphabetically or by resource). Labels of 2 to
  4 words that match each page's title.
- Every page reachable from the navigation, or unlisted on purpose; no
  orphans.
- URLs lowercase, kebab-case, short and stable (`/guides/rotate-api-key`),
  with no dates, and no version unless the docs are versioned. A moved
  page gets a redirect: `redirects` in Astro's config for Starlight,
  `@docusaurus/plugin-client-redirects`, the `mkdocs-redirects` plugin, or
  the host's `_redirects` (Netlify, Cloudflare Pages) or `vercel.json`.
- Previous and next links in tutorials, an "on this page" list on long
  pages, breadcrumbs past two levels.

## 3. Search

- Static search, built in or added: Pagefind (Starlight's, or any static
  build with `npx pagefind --site dist`), VitePress's local search, the
  search in Material for MkDocs and in mdBook.
- Hosted: Algolia DocSearch (free for many open-source projects, on
  application), Typesense DocSearch run yourself, or the platform's own.
- Results depend on the content: titles and headings in the words readers
  type, one topic per page, generated noise kept out (once any page marks
  an element `data-pagefind-body`, Pagefind indexes only such elements;
  it always skips `data-pagefind-ignore`).
- Try the ten to twenty questions readers ask most (from support and from
  search logs): the right page comes first. Queries with no results are
  the best list of pages to write next.

## 4. Versioning

- Version the docs only when many users stay on older versions for long:
  self-hosted products, libraries with long-term support branches.
  Otherwise keep one current version, a changelog, upgrade guides, and
  "Added in 2.3" notes on features.
- When versioned: the latest at unversioned URLs, older ones under
  `/v2/`; a banner on old versions linking to the same page in the latest;
  canonical URLs pointing at the latest; only maintained versions built.
- Tools: Docusaurus (`npm run docusaurus docs:version 2.0`), mike for
  MkDocs (`mike deploy --push --update-aliases 2.0 latest`), Read the Docs
  builds per tag or branch, the `starlight-versions` plugin.

## 5. Code blocks and components

- Every block has a language; file contents get a title (the path); the
  lines that matter are highlighted; changes show as a diff; the copy
  button copies the command only, with no prompt and no output.
- Tabs per package manager or language, with the choice kept across the
  page and the site: Starlight `<Tabs syncKey="pm">`, Docusaurus
  `<Tabs groupId="pm">`, VitePress `::: code-group`, Material content tabs
  (`=== "npm"`) with the `content.tabs.link` feature.

| Generator | Title and highlighted lines |
|---|---|
| Starlight | ` ```js title="astro.config.mjs" {2-3} ins={4} del={5} ` |
| Docusaurus | ` ```js title="docusaurus.config.js" {2-3} `, or `// highlight-next-line` |
| VitePress | ` ```ts{2,4-5} `, or `// [!code ++]`, `// [!code --]`, `// [!code focus]` |
| Material for MkDocs | ` ```py title="app.py" hl_lines="2 3" ` |

- Code comes from files that CI builds and tests, included rather than
  pasted:
  - VitePress: `<<< @/snippets/create-order.ts#usage`, for a
    `#region usage` in the file;
  - Material for MkDocs: `--8<-- "examples/create_order.py"` inside the
    block, with the `pymdownx.snippets` extension;
  - Starlight: `import source from "../../examples/order.ts?raw";` in MDX,
    shown with Starlight's `<Code code={source} lang="ts" />`;
  - Docusaurus: the file through `raw-loader` into `<CodeBlock>`;
  - mdBook: `{{#include ../examples/order.rs:usage}}`, between
    `// ANCHOR: usage` and `// ANCHOR_END: usage` lines.
- Callouts (note, tip, caution, danger) sparingly: one or two on a page at
  most, caution and danger only for data loss, security or cost. Syntax:
  `:::note` in Starlight and Docusaurus, `::: tip` in VitePress, `!!! note`
  in Material, `> [!NOTE]` on GitHub.
- Cards and grids on the landing page only; a steps component for
  tutorials.

## 6. Docs as code

- Markdown or MDX in the repository (`docs/` or `apps/docs/`), reviewed in
  pull requests like code, with a CODEOWNERS entry.
- A preview deploy per pull request (Netlify, Vercel, Cloudflare Pages,
  Read the Docs pull request builds), linked in the pull request.
- On every pull request, CI:
  - builds strictly: Docusaurus throws on broken links by default
    (`onBrokenLinks`), VitePress fails on dead links,
    `mkdocs build --strict`, `sphinx-build -W --keep-going`, Starlight
    with the `starlight-links-validator` plugin;
  - checks links with lychee (`lychee --no-progress 'docs/**/*.md'`, or
    on the built site). External links fail for reasons outside your
    control: check them on a schedule, weekly, with `--cache`, a GitHub
    token against rate limits, and exclusions in `.lycheeignore`;
  - lints prose with Vale, with a style (Google, Microsoft or your own)
    and a vocabulary of project terms: warnings first, errors once the
    backlog is clean;
  - checks spelling with cspell (with a project word list) or typos (fast,
    few false positives), and Markdown with markdownlint-cli2;
  - runs the doctests and builds the included examples.

```ini
# .vale.ini
StylesPath = .github/vale
MinAlertLevel = warning
Packages = Google
Vocab = Project

[*.{md,mdx}]
BasedOnStyles = Vale, Google
```

Project terms go in `.github/vale/config/vocabularies/Project/accept.txt`,
one per line; `vale sync` downloads the packages, and `vale docs` runs it.

## 7. Translation

- Translate once the source docs are stable and there are readers who
  need it. A half-translated site with stale pages serves them worse than
  one good language.
- The source language is canonical. Translations follow it with a tracked
  lag, and a page says when its translation is out of date or falls back
  to the source (Starlight shows the fallback with a notice).
- Built in: Starlight, Docusaurus (`npm run write-translations` for the
  interface strings), VitePress locales; the `mkdocs-static-i18n` plugin
  for MkDocs. Platforms: Crowdin, Lokalise, Weblate. A machine draft is
  reviewed by someone fluent before it ships.
- Never translate code, identifiers, flags, config keys or field names,
  and keep the terms the audience keeps in English (`i18n`).
- The language switcher keeps the reader on the same page; `hreflang`
  links connect the versions.

## 8. Feedback, analytics and machine readers

- Analytics only if someone acts on them, and privacy-respecting
  (Plausible, Umami, or the host's): the top pages, searches with no
  results, 404s, where readers leave a tutorial.
- An "Edit this page" link (`editLink` in Starlight, `editUrl` in
  Docusaurus) and a "Report a problem" link to the issues; a "Was this
  helpful?" widget only if someone reads the answers every week.
- A 404 page with search and the main entry points.
- A unique title and description per page, a sitemap, canonical URLs, a
  social preview image.
- Agents read docs too: many sites publish `/llms.txt` (an index of the
  pages) and Markdown copies of pages, and community plugins generate them
  for Starlight, Docusaurus and VitePress. Generate them from the same
  source, never as a second copy kept by hand.

## 9. Speed and accessibility

- Static output, with JavaScript only for search, tabs and the theme
  switch: every content page reads with JavaScript off; only search needs
  it.
- The layout, the widths and the sticky parts are in `ui-page-docs`. Light
  and dark themes, with code colours readable in both; a skip link;
  visible focus; search that opens with `/` or `Ctrl+K` and works from the
  keyboard; headings in order; alt text; AA contrast.

## Check it

- The site builds strictly with no warnings, and the link checker is clean
  for internal links.
- With `preview` when you have it, on the landing page, a guide and a
  reference page at 360, 768 and 1440px: nothing wider than the screen,
  long code scrolling inside its block, the sidebar turning into a menu on
  a phone, contrast passing, every control named.
- The ten questions readers ask most each find the right page first.
- No template leftovers: example pages, the generator's logo, a demo
  blog, placeholder social links.
- Every moved URL redirects.

## Avoid

The template's example pages left in; navigation that mirrors folders
five levels deep; versioning nobody needs; code blocks with no language,
or copy buttons that copy the prompt; callouts on every section; pasted
code that CI never runs; external link checks that fail every pull
request; half-translated sites; a feedback widget nobody reads; a docs
site built from scratch.
