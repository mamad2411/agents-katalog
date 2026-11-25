---
name: sanity-module-catalog
description: Pictures of the project's sections. Main mode, insert-menu tiles — photograph each section's Sections Gallery fixture, drawn with the project's own components and tokens, into `web/public/admin/thumbnails/<type>.webp`, the tiles of the Studio "Add item…" grid view, and report types with no tile. Use when the insert menu shows blank or placeholder tiles, after /create-section, after restyling a section or changing tokens, fonts or `app.css`, or for "section thumbnails in the Studio" or "which sections have no tile". Optional mode, live-site catalog — screenshot every section instance on a deployed Sanity + Next.js site into a gitignored folder, with a URL→sections manifest and HTML viewers by page and by type (used vs unused). Use for "which sections are used on the live site", "module inventory", "screenshot all modules" or auditing which CMS blocks editors use.
---

# Section pictures: insert-menu tiles and live-site catalog

Two modes. Pick by what the user asks; when unclear, it is the tiles.

| Mode | Output | Committed |
|---|---|---|
| **A. Insert-menu tiles** (default) | `web/public/admin/thumbnails/<type>.webp`, one 800×600 tile per section type, from the Sections Gallery | Yes, with the change that caused it |
| **B. Live-site catalog** (only on request) | Screenshots of every section instance on a deployed site + a manifest and two HTML viewers | No, a gitignored folder |

The script lives in this skill's folder; in a project that is
`.agents/skills/sanity-module-catalog/`. Commands below run from the project root.

## Mode A: insert-menu tiles

### What it is for

An editor adds a section through **Add item…**. The insert menu has a **grid view** with
one tile per section type, so the editor picks "the band with three cards" by sight. The
Studio asks for each tile at `/admin/thumbnails/<type>.webp`, set in
`studio/src/sanity/schemaTypes/fragments/sections.ts` (`insertMenu.views` →
`previewImageUrl`) and again in `studio/src/sanity/schemaTypes/documents/shared-section.ts`.

A type with no file gets a blank tile. **Nothing fails**: the schema compiles, the page
renders, and the new section is the one entry nobody recognises. The tiles are drawn by
the project's own components with its own tokens and fonts, so they go stale whenever the
look changes.

### What the script does

`scripts/capture.mjs` (Node 22+, no npm dependencies, nothing to install in the project):

1. Reads the section types from `INNER_SECTIONS` in the schema **source**, so the list
   never drifts from what the menu offers.
2. Opens `/styleguide/sections/<type>` on a running web app. That Sections Gallery page
   renders the type's `gallery-fixture.ts` at full width, so the tile does not depend on
   the dataset's pages.
3. Scrolls so lazy images start, waits until every visible image has painted, and pauses
   animations.
4. Screenshots the first `[data-section="<type>"]` element (set by
   `web/src/lib/sectionProps.ts`) at 1440 px and makes an exact 800×600 WebP: a **tall**
   section is cropped from the top (the heading identifies it); a **short** band is scaled
   to the tile width and centred on its own background colour, never stretched.
5. Prints coverage: types with a tile, types **MISSING**, and **ORPHANED** files no type
   claims (left over from a removed or renamed section).

Chrome is driven over the DevTools protocol; resizing and WebP encoding happen in the
page's own `<canvas>`.

### What you need

| Input | Where it comes from |
|---|---|
| **Project dir** (`--project`) | The project root holding `web/` and `studio/`. |
| **Running web app** (`--base`, default `http://localhost:3000`) | `pnpm dev`. It must be a **dev** server: outside `next dev` the gallery is gated to logged-in Studio editors and the script would photograph the gate. If 3000 is taken, pass the port Next printed. |
| **Env** | `web/.env.local` (+ `studio/.env`) with the Sanity project id and dataset, or `pnpm dev` doesn't start. Ask the user; never invent them. `/project-setup` covers it. |
| **Fixture images** | Read `web/src/ui/styleguide/sections-gallery/mock-image.ts`: local files in `web/public/placeholders` work on an empty dataset; references to seeded assets need the demo data first (`pnpm seed`). |
| **A `gallery-fixture.ts` per section** | Next to each component in `web/src/ui/sections/`, registered in `SECTION_FIXTURES`. A type without one is skipped and the run exits 1. Write it first: `docs/agents/new-section.md`, step "Add the section to the Sections Gallery". |
| **Which types** (`--only`) | All by default. After /create-section or a restyle of one section: `--only=pricing,faq`. After a token, font or `app.css` change: all. |
| **Chrome** (`--chrome`, optional) | Auto-detected: Playwright's `chrome-headless-shell` in `~/Library/Caches/ms-playwright` first, then installed Chrome. If neither: `npx playwright install --only-shell chromium`. |

### Steps

1. **Check coverage** (no browser, no server):

   ```bash
   node .agents/skills/sanity-module-catalog/scripts/capture.mjs --project=. --report
   ```

2. **Start the app**: `pnpm dev` in a separate terminal or background process (seed the
   demo data first if the fixtures need it). Wait until
   `http://localhost:3000/styleguide/sections` answers.

3. **Capture**:

   ```bash
   node .agents/skills/sanity-module-catalog/scripts/capture.mjs --project=.
   node .agents/skills/sanity-module-catalog/scripts/capture.mjs --project=. --only=hero,faq
   ```

   Each line prints the type, the section's size and whether the tile was `cropped` or
   `padded`. The run ends with the coverage report and exits 1 if a type was skipped or
   is still missing.

4. **Look at every tile you wrote.** Each must show its section: real images, not blur
   smudges or grey boxes; no "Preview failed to render" card; no "No fixture yet"
   placeholder; no dev overlay. A wrong screenshot looks as complete as a right one, so
   the exit code is not enough.

5. **Delete orphans** the report lists (`git rm web/public/admin/thumbnails/<name>.webp`).

6. **Check in the Studio**: `/admin` → a page → **Add item…** → grid view. Tiles show only
   in the **embedded** Studio at `/admin`; the standalone Studio (`studio/`, its own
   origin) resolves `/admin/thumbnails/…` against its own host and shows blanks.

Commit the tiles with the change (they are static files the Studio loads). After changing
the scripts: `node --test .agents/skills/sanity-module-catalog/scripts/lib.test.mjs`.

### Exemptions (`scripts/lib.mjs`)

- `TYPES_WITHOUT_A_TILE`: types that never get a tile, with the reason.
  `shared-section-ref` renders whatever bundle an editor points it at, so it has no look
  of its own.
- `TYPES_AWAITING_A_TILE`: a tile that is owed, not refused (a fixture not written yet),
  with the command that clears it. `--report` still counts it as outstanding. Delete the
  entry once the tile exists.

### Traps that give a complete, plausible but wrong tile

1. **`next/image` keeps its blur placeholder until its own load event.** Shot too early,
   every card is a coloured smudge. The script waits for each visible image; if one still
   shows a blur, re-run that type.
2. **A hidden twin of a responsive pair never loads.** A `loading="lazy"` image inside a
   `display:none` variant stays incomplete for ever; only images with a layout box are
   waited for.
3. **Animations and players.** Animations are paused; a Lottie or video may come out as
   an empty box, and the 4:3 crop usually leaves it out. Don't change the component to
   make the tile prettier.
4. **Full Chrome in a sandbox** exits with `Failed to create a ProcessSingleton` /
   `bootstrap_check_in … Permission denied`. Use the Playwright headless shell
   (auto-detected, or `--chrome=`).
5. **An authenticating proxy** can't be passed to Chrome as a URL with credentials. Run a
   local relay that adds `Proxy-Authorization` and pass `--proxy=<relay>`.

### Don't

- Don't capture from a deployed site: the gallery is gated there.
- Don't hand-edit, upscale or stretch a tile; re-capture it.
- Don't copy tiles from another project: they show its styles, not this one's.
- Don't change `previewImageUrl` or the file names: the Studio asks for exactly
  `<type>.webp`.

## Mode B: live-site catalog

Screenshots every section instance on a deployed Sanity + Next.js site (this project or
another one, for example a site you are reworking) and builds a catalog: which sections
are used on which page, and which types nobody uses.

**Counts only?** In a project with a Sections Gallery, `/styleguide/sections` already shows
"used in N documents" per type, and each type's page lists the documents. Offer that
first; build the screenshot catalog only when the user wants the pictures.

### Output folder first

**Ask where the catalog goes before writing anything**; suggest `module-catalog/` in the
project root. It holds screenshots of a real (sometimes a client's) site, often hundreds
of PNGs, and goes stale in weeks, so it never gets committed:

```bash
OUT=module-catalog
mkdir -p "$OUT/screenshots"
git check-ignore -q "$OUT" || echo "$OUT/" >> .gitignore
```

Skip the `.gitignore` step for a folder outside the repo. Everything below is written
under `$OUT`:

```
$OUT/
├── url-index.json                    # URL → sections manifest
├── screenshots/<site>_<urlslug>_<NN>_<type>.png
├── <SITE>-MODULE-USAGE.md            # type → URLs table
├── <SITE>-MODULE-SCREENSHOTS.html    # by URL
└── <SITE>-MODULE-TYPES.html          # by type, used vs unused
```

### Prerequisites

Read access to the dataset (`npx sanity login` or a Viewer token; never print a token or
write it into `$OUT`), `jq`, Python 3 + Pillow (`pip3 install --user Pillow`), a
browser-automation CLI that can open a page, run JS and take a full-page screenshot (the
reference uses `agent-browser`), and the site's code for the section schemas.

### Phases

Full commands, the pipeline rules and the pitfalls table are in
[`references/live-catalog.md`](references/live-catalog.md). Read it before Phase 4.

1. **Schema**: list the section types and the document types that embed them, plus the
   URL rule per document type. In a project from this starter: types in
   `studio/src/sanity/schemaTypes/fragments/sections.ts`; embedders `page`, the
   `*-listing-page` singletons, `global-section` and `shared-section` (via
   `shared-section-ref`); URLs in `web/src/lib/resolveUrl.ts`.
2. **Query** the dataset (published only) for every routed document's sections,
   dereferencing shared sections and templates.
3. **Index**: write `url-index.json`, one entry per URL with each section's type, `_key`
   and a short headline snippet.
4. **Screenshot**: a fresh browser session per URL, dismiss the consent banner, check the
   URL, full-page screenshot, crop each section by content-based matching.
5. **Viewers**: by-URL and by-type HTML with relative paths into `screenshots/`, used vs
   unused badges, filters and a lightbox. For a type never used on the site, show its
   insert-menu tile (`web/public/admin/thumbnails/<type>.webp`, labelled as sample data)
   or, without one, a card with its fields and what it renders.

Done when `git status` shows no catalog files, every URL has as many crops as sections
(or a noted reason), three random crops match their recorded headline, and unused types
show a card, not a broken image.
