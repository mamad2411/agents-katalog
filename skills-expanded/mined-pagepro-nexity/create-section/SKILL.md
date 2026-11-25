---
name: create-section
description: Create a new page section in this Next.js + Sanity starter, after first checking whether an existing section already covers it (reuse as-is, add a layout option or fields, or build a new type). Takes the look from DESIGN.md (plus any Figma link, screenshot or mockup the user gives) and the copy from BRAND.md (placeholder copy while it is still the template), models the code on the 2–3 closest sections in web/src/ui/sections/, and ships the schema, GROQ branch, component, gallery fixture, Markdown serializer, insert-menu entry and tile. Use when the user asks for a new band, block or section, or whether the site already has one that fits a design.
---

# Create a section

The **existing sections** decide whether anything needs building, **`DESIGN.md`** how it
**looks**, **`BRAND.md`** what it **says**, the **closest sections** the starting **code**, and
the registries whether an editor can ever **find** it.

Paths are relative to the project root (the folder that holds `web/` and `studio/`) and are
the same in projects made from `base/` and `theme-meridian/`; only the web package name
differs, so commands use `pnpm -C web …`.

This skill is the executable form of the checklist in `docs/agents/new-section.md` (root
`AGENTS.md` → **"Creating a New Section"**); keep the two in sync. Skim
[`references/gotchas.md`](references/gotchas.md) before Phase 2.

Several steps below fail **silently**. A section can compile, typecheck and render while
being invisible in the insert menu, blank in the gallery, or stripped from the document by a
stale Studio. Do not skip a phase because the page looks right.

**Reviewer agents.** Phases 0, 2, 3 and 4 hand off to four read-only reviewers in
`.agents/agents/`: `content-model-architect`, `styling-fidelity-reviewer`,
`sanity-schema-reviewer` and `groq-parity-reviewer` (plus `link-reviewer`, when installed, for
a section with links or CTAs). Claude Code runs them as subagents through `.claude/agents`. An
agent without named subagents opens the matching `.md` and walks its checklist itself, or
gives a general-purpose subagent the file's body as its prompt.

**Input.** What the section should do, plus any of: a description, a screenshot, an exported
mockup (HTML or image), or a Figma link the session can read.

---

## Phase 0 — Do we already have it?

Answer this before modelling anything. A second type that draws the same layout is the most
expensive outcome of this skill: two schemas, two components, and an editor left guessing.

### 0a. Inventory what exists

| Where | What it tells you |
|---|---|
| `web/src/ui/styleguide/sections-gallery/section-meta.ts` → `SECTION_META` | every section type with its title, a one-line `description` and an `accepts` list of fields: the fastest catalog |
| Sections Gallery: Studio → **Styleguide** → *Sections*, or `/styleguide/sections` on the web dev server | each type rendered from its `gallery-fixture.ts`, with where it is used on the site |
| `studio/src/sanity/schemaTypes/fragments/sections.ts` | `INNER_SECTIONS` (what the page builder offers) and the `insertMenu.groups` an editor sees |
| `studio/src/sanity/schemaTypes/sections/<type>.ts` (or a `<type>/` folder) | the fields, and in the `options` group the variants that already exist: `layout`, `imageLayout`, `cardStyle`, `textAlign` and similar radio fields |
| `web/src/ui/sections/<Name>/` (registered in `map.ts` → `INNER_SECTION_MAP`) | how each layout and variant is drawn |

Every section also has `section-options` (Color theme, dividers), so a "light/dark version"
of an existing band is that option, not a new type. A band repeated on several pages
is a `shared-section` document placed with `shared-section-ref`, not a new type either.

### 0b. Compare the request with the 2–3 closest types

Compare by **slots** (the layout skeleton: heading + grid of cards, media beside copy, a row of
logos, a table), then **fields**, **mechanics** (client state such as tabs or a carousel;
inline items vs referenced documents) and **purpose**. Ignore the copy: a heading plus three
cards is a `feature-grid` even when the copy reads like a testimonial, and "one big quote with
its author" is `testimonials` with the **Featured** layout. Show the user a short table: each
candidate, what matches, what is missing.

### 0c. Decide with the user

| Decision | When | What runs next |
|---|---|---|
| **Reuse as-is** | an existing type, with a layout option or Color theme it already has, draws the request | Stop building. Tell the user which type and which options to pick; offer Phase 6 (one instance) only |
| **Extend** | an existing type covers ~80% of the slots and fields, and its form stays clear with the addition | Phases 1–6 on the existing files: add a `layout`/variant option or the missing fields. Skip the registrations (Phase 4 steps 1, 2, 5; gallery registries); update the GROQ branch, fixture, `markdown.ts`, `accepts` and tile |
| **New type** | nothing covers the slots, the mechanics differ (inline content where the existing type references documents, or the reverse), or extending would make an existing form confusing | Phases 1–6 in full |

**Ask; do not decide silently.** When two types both fit, or the content model is unclear,
run the `content-model-architect` agent (inline object vs document-backed listing vs shared
section, `cta` vs `link`, rich-text variant) and put its recommendation to the user.

When extending, existing documents must render exactly as before: new fields stay optional,
a missing value renders the current look (`initialValue` only reaches new instances), and no
field is renamed or retyped (that needs a content migration). When building new
despite a close match, write the reason into the report and into the new type's gallery
`description`, so the next person sees which one to pick.

---

## Phase 1 — Gather the three sources: look, code, content

### 1a. Look — `DESIGN.md` first, then the user's reference

Read the root **`DESIGN.md`** before drawing anything; the `styling-fidelity-reviewer` checks
against it. **Colors** says which semantic token plays which role, **Typography** which block
style or utility each level maps to, **Layout** the section anatomy and vertical padding,
**Elevation & Depth** and **Shapes** the shadows, radius and borders, **Components** the
button, card and surface recipes to reuse, then **Do's and Don'ts**. From `base/` it describes
neutral defaults until the project replaces it; in `theme-meridian` it is the full design
system, and product imagery comes from the `product-mock` skill, not stock shots.

Then the user's reference, if any. A **screenshot**: list every element top to bottom
(eyebrow, title, body, buttons, media, badges) and map each to a token or recipe. An **HTML
mockup**: measure it in a browser (`getBoundingClientRect`, `getComputedStyle`); its classes
are intent, not markup to paste. A **Figma link**: read it through whatever Figma tool the
session has and map literal values to the nearest token. **Only a description**: propose a
look built from `DESIGN.md` recipes and confirm it before writing markup.

**The user asks for several variants** to choose from: when the `impeccable` skill is
installed, use it to develop them, with `DESIGN.md` and `BRAND.md` still binding over its
defaults. Without it, draw them yourself from `DESIGN.md` recipes. Say which path you took.
Either way, show each variant in the page it will sit in, on a temporary uncommitted route,
and write no schema, query or registry entry until the user has picked one. Delete the route
before Phase 3.

Where the reference and `DESIGN.md` disagree, follow `DESIGN.md` and raise the conflict;
change `DESIGN.md` (with `web/src/styles/app.css`, and `web/src/ui/fonts.ts` for fonts) only
when the user confirms the reference is the new rule. A reference that departs from every
token of a still-neutral `DESIGN.md` means the project's design system is not set up yet; say
so instead of hard-coding its colours into one section. The `section` container is 1280px
wide; measure natural widths rather than copying pixel widths from a wider canvas.

### 1b. Code — the 2–3 closest existing sections

The candidates from Phase 0 are your neighbours. Read each in full: its folder
`web/src/ui/sections/<Name>/` (`index.tsx`, `types.ts`, `gallery-fixture.ts`, `markdown.ts`,
any `client.tsx` / `client-lazy.tsx` and sub-components), its schema
`studio/src/sanity/schemaTypes/sections/<type>.ts` (or a `<type>/` folder), and its
`_type == '<type>' => { … }` branch in `SECTION_BRANCHES_QUERY` (`web/src/sanity/lib/queries.ts`).

Prefer the **same slots** (`FeatureGrid`, `FeatureBlockSection`, `SplitSections`, `Stats`,
`CtaBanner`, `FaqSection` and `HeroSection` cover most marketing bands), then the **same
mechanics**: client state → a section with `client.tsx` + `client-lazy.tsx` (`Pricing`,
`TestimonialsSection`, `LogosCarousel`); referenced documents → `TestimonialsSection`; a
paginated grid → a listing section and `web/src/ui/listing/`. Copy how the neighbour projects
and renders CTAs, images and rich text instead of inventing a new shape. Write down which
neighbour each part (component, schema, query, fixture) is modelled on.

### 1c. Content — `BRAND.md`

Read the root **`BRAND.md`**. Check its first line: a `<!-- brand-template: … -->` comment
means it is still the unfilled template (a fresh `base/` project ships it that way).

- **Filled in** (as in `theme-meridian`): every copy string, name and figure in the section,
  its fixture and its first Studio instance comes from it or from the user's reference, never
  invented on the spot. **Voice and tone** and **Messaging** govern headings, body and button
  labels, including literals the component hardcodes (`constants.ts`); **Product facts** gives
  names and numbers; **The invented world** and **Evidence on hand** say which customers,
  quotes and statistics may appear and what must never be presented as real.
- **Template or missing** → treat it as absent. Use the copy the user gave you; if there is
  none, write short, neutral, obviously placeholder copy (no real company, person, logo or
  statistic) and say so in the report. Do not fill `BRAND.md` in as a side effect of this
  skill; suggest the user fills it (the `project-setup` skill can do it as an interview).
- **Partly filled** → use the sections that are filled; a heading still holding `<…>`
  placeholders counts as missing.

`BRAND.md` decides what the section says, never what it is called: name the type, component
and fields after the layout and content kind (`logo-wall`, `pricingTiers`), not after the
company or a campaign.

---

## Phase 2 — Build the component in the starter's idiom

Copy the mechanics from your neighbours; these are the conventions they all share:

| Concern | Convention (`web/`) |
|---|---|
| Props | from Sanity: `types.ts` → `export type XProps = ExtractSectionProps<"my-section">` (`@/types/sections`) |
| Wrapper | `<section {...sectionProps(props)}>` (`@/lib/sectionProps`) + the **`section`** utility on the content container (on the `<section>` or an inner div for full-bleed backgrounds), never raw `px-*` / `max-w-* mx-auto` |
| Images | default export of `@/ui/components/image` with `sanityImage={…}` (parent `relative` for `fill`) |
| Buttons and links | `ButtonLink` (`@/ui/components/button/button-link`) for CMS CTAs, `BaseLink` (`@/ui/components/Link/BaseLink`) for plain links |
| Rich text | `RichText` (`@/ui/RichText`) with CMS block styles, no `[&_p]` overrides |
| Colors, type, radius, shadow | the semantic tokens (`bg-background`, `text-muted-foreground`, …, from `web/src/styles/app.css`) and recipes `DESIGN.md` assigns to each role; never palette colors or hex |
| Dark band | `section-options.colorTheme`; the `Sections` renderer wraps the section with the classes from `web/src/ui/sections/section-theme.ts` (`.dark` flips the tokens). A requested "light/dark background" variant IS this option: no extra schema field, no `dark:` branch in the component |
| Vertical padding | per section (`py-*`), from `DESIGN.md` → Layout or the neighbour you copy |

**Reuse before you write**, in this order:

1. `web/src/ui/components/`: `button/` (`ButtonLink`), `Link/` (`BaseLink`), `image/`, `Icon/`,
   `arrow-link/`, `author-byline`, `feature-icon`, `quote/`, `ImageOverlay/`, `Spinner/`.
2. `web/src/components/ui/`: the trimmed shadcn `carousel.tsx` (embla) and `hover-card.tsx`.
3. Sub-components of sibling sections (cards, tiles, rows), e.g. `FeatureGrid/feature-card.tsx`,
   and `web/src/ui/listing/` for paginated grids.

Add a new shadcn primitive to `web/src/components/ui/` only if nothing above fits.

Structure (see `web/AGENTS.md` → "Section Component Structure"): simple sections = `index.tsx`
+ `types.ts`; complex ones (client state, tabs, filters) split into `index.tsx` (server) +
`client.tsx` + `constants.ts` + `utils.ts` + kebab-case sub-components, all in one folder.
`index.tsx` imports the client part from a `client-lazy.tsx` (`"use client"` +
`dynamic(() => import("./client"))`), never `./client` directly, and nothing under
`client.tsx` imports `RichText`, `<Image>`, `ButtonLink` or `cn()` (render them on the server
and pass them in as nodes). See `docs/agents/web-client-performance.md`; `pnpm lint`
runs `check:client`, which enforces it. `stegaClean()` strings before comparing them.

No arbitrary values (`[23px]`), `body-3` as the default body style, and `cn()` drops a
custom `text-NN` size next to a `text-{color}` (put the size on a parent). Run the
**`styling-fidelity-reviewer`** agent once the component is drawn; pass it the reference
image if there is one.

---

## Phase 3 — Model the schema by reading three neighbours

Create `studio/src/sanity/schemaTypes/sections/<my-section>.ts` (or edit the existing one when
extending) and mirror the Phase 1b neighbours' field names, order and groups. `studio/AGENTS.md`
holds the full rules and the section template; the ones that cost the most when missed:

- `section-options` first, always, in the `options` group.
- **Never a single `reference`**, always an array of references (`min(1)`).
- **Never name a field `groups`**: it shadows the schema-level field-group key.
- Reusable entities (testimonials, team members, case studies) are **documents** referenced by
  the section (`docs/agents/content-patterns.md` → "Document-Backed Listing Section"); inline
  objects only when the content belongs to that one instance.
- Radio lists, not booleans. An `icon` and a customised `preview` on every object type.
- Images are the `img` object type (`type: "img"`; it already sets `hotspot: true` and holds
  alt and loading), with a `description` giving the aspect ratio and recommended size. The
  GROQ branch expands it with `IMAGE_FRAGMENT`.
- Short fields that belong together (author + role, label + value) share a `fieldset` with
  `options: { columns: 2 }`; the `sanity-schema-reviewer` flags a pair without one.
- Pick the rich-text type deliberately: `simpleRichText`, `pageRichText`, `richText`
  (decision matrix in `studio/AGENTS.md`). `cta` when the editor picks the button style,
  `link` when the component hardcodes it.
- Keep optional fields optional: typegen runs with `--enforce-required-fields`, so a
  `required()` flips the generated type non-null.
- Field titles use the neighbours' terms; an `initialValue` holding copy follows `BRAND.md`.

### Field groups — two tabs, unless `content` reaches 5 fields

`[{ name: "content", default: true }, { name: "options" }]` is right for most sections (an
image or two stays in `content` then). Past four or five content fields the tab stops being a
place an editor can find anything. **When you split, draw from this vocabulary and no other**,
in this order; a section omits any group it has no fields for:

| Group | Tab title | Holds |
|---|---|---|
| `content` | **Heading** | `pretitle`, `content`, `title`, `description` |
| `items` | **Cards** / **Questions** / **Rows** / **Table**, named after the content | the array, and the labels that govern every member |
| `form` | **Form** | the input widget's copy: placeholder, submit label, disclaimer |
| `media` | **Media** | every image, video and file field (new sections: never call it `image`) |
| `links` | **Links** | `ctas`, `footerLink`, `link` |
| `options` | Options | `section-options`, `layout`, alignment, counts, speed |

**Declare the short fields BEFORE the array they govern**: a group renders fields in
declaration order, so grouping alone leaves a card label below a stack of expanded cards.
Keep every tab title to one word; the dialog is narrow and a two-word title wraps.

Run the **`sanity-schema-reviewer`** agent when the file is written.

---

## Phase 4 — Register it in TWO files, query it, typegen, map it

1. `studio/src/sanity/schemaTypes/index.ts`: import the schema and add it to the schema types
   array next to the other sections.
2. `studio/src/sanity/schemaTypes/fragments/sections.ts`: add `{ type: "my-section" }` to
   `INNER_SECTIONS` **and** the `_type` string to the matching `insertMenu.groups` entry
   (usually `content`; listings go in `lists`).

**Skipping the second is the most common silent gap.** The schema compiles, typegen succeeds,
and the section never appears in any page's insert menu. Nothing errors.

3. Add a `_type == 'my-section' => { … }` branch to `SECTION_BRANCHES_QUERY` in
   `web/src/sanity/lib/queries.ts`. `SECTIONS_QUERY` reuses those branches both inline and
   inside the `shared-section-ref` branch, so add it once. Reuse the fragments
   (`IMAGE_FRAGMENT`, `CTA_FRAGMENT`, which carries `buttonIcon`, `LINK_FRAGMENT`,
   `RICHTEXT_QUERY`); dereference reference arrays with `field[]->{ _id, … }`. Field names
   match the schema exactly, never alias. A listing page gets its own query file instead
   (`docs/agents/new-document-type.md` → "Listing Page Pattern").
4. `pnpm -C web ts:typegen` (regenerates `web/src/types/sanity.types.ts`; it loads the web env,
   so it fails with "Missing NEXT_PUBLIC_…" until `web/.env.local` is filled, see the
   `project-setup` skill). From here on `pnpm typecheck` lists every registry still missing
   the type (`SECTION_MAP` until step 5, then gallery `SECTION_TYPES` + `SECTION_META`,
   Markdown serializers, JSON-LD contributors); that list is the to-do for Phases 5 and 5b.
5. Register the component in `web/src/ui/sections/map.ts` → `INNER_SECTION_MAP`, static
   import, in alphabetical order. (`index.tsx` spreads it into `SECTION_MAP` and adds
   `shared-section-ref`; don't register there.)

Run the **`groq-parity-reviewer`** agent after step 5: schema ↔ GROQ ↔ frontend field-name
parity, the empty-`href` trap, `buttonIcon` projection. When the section renders links or
CTAs, run `link-reviewer` too if it is installed.

---

## Phase 5 — The Sections Gallery (three edits, two enforced by typecheck)

The gallery (`web/src/ui/styleguide/sections-gallery/`, Studio → **Styleguide** → *Sections*)
is derived from the generated section-type union, so **`pnpm typecheck` fails until
`SECTION_TYPES` and `SECTION_META` are wired**. `SECTION_FIXTURES` is optional per key: a
forgotten fixture compiles, shows a "Needs fixture" card and skips the Markdown fixture test.

1. `fixtures-registry.ts` → add the `_type` string to `SECTION_TYPES` (the `_AssertComplete`
   guard errors otherwise), import the fixture and add it to `SECTION_FIXTURES`.
2. `section-meta.ts` → a `SECTION_META` entry: `title`, `description`, a hand-authored
   `accepts` hint, and a `group` from `SECTION_GROUPS`. It is an exhaustive `Record`, so a
   missing key is a compile error. **`accepts` is hand-authored: the web app must never import
   the Studio schema runtime.** The `description` says when to pick this type over its closest
   neighbour; it is what the next Phase 0 reads.
3. A co-located `web/src/ui/sections/<Name>/gallery-fixture.ts`:
   `export const <camelType>Fixture = {…} satisfies ExtractSectionProps<"<type>">`. Copy the
   fixture of the neighbour you modelled the section on. **Pure data**: import only
   `ExtractSectionProps` (type) and the image helpers from `sections-gallery/mock-image.ts`
   that the neighbouring fixtures use; never the component. It is the **resolved GROQ shape**:
   references dereferenced, image `asset` expanded. Copy comes from Phase 1c.

   Images: **model them on the neighbouring fixtures**; the helpers differ per starter, so read
   `mock-image.ts` first. From `base/`, `mockImage(shape, alt)` points at local SVGs in
   `web/public/placeholders/` (logo rows cycle `PLACEHOLDER_LOGOS`), so the gallery renders on
   an empty dataset; never reference a dataset asset there. In `theme-meridian`,
   `mockImage(orientation, alt)` and `` imageFromUrl(`${CDN_BASE}/…`, alt) `` resolve assets
   from the demo dataset (`pnpm seed`); a missing asset makes `<Image>` throw, and a new image
   must go into the seed archive too. Pick the shape closest to the real aspect ratio; a typo
   in it is a compile error.

   The gallery shows the fixture as written, with no `options`. To look at the Dark theme or
   an empty optional field, temporarily add `options: { colorTheme: "dark" }` (or set the
   field to `null`), check `/styleguide/sections/<type>`, then revert.

**`--enforce-required-fields`** generates every optional schema field as `T | null`
(required *and* nullable). Set `field: null` explicitly on every item that omits it, or
typecheck fails with "Property 'x' is missing".

### Phase 5b — Markdown and structured data (two registries, enforced by typecheck)

Both registries carry a drift guard over the generated section union, so `pnpm typecheck`
names the type until it has an entry.

1. **Markdown for agents**: a co-located `web/src/ui/sections/<Name>/markdown.ts` exporting
   `<camelType>ToMarkdown: SectionMarkdownSerializer<SectionData<"<type>">>`, registered in
   `SECTION_MARKDOWN_SERIALIZERS` (`web/src/lib/markdown/section-serializers.ts`). Copy a
   neighbour (`FaqSection/markdown.ts`, `Stats/markdown.ts`, `Pricing/markdown.ts`). It says
   what the component shows (a layout that hides a field hides it here too): images as
   `imageHint`, an interactive widget as a `presenceHint`, rich text through
   `portableTextToMarkdown`, CTAs through `ctaList`. Pure: `import type` from the component
   side, no `next-sanity`, no React; literals the component renders go in `constants.ts` so
   both read them. Add the type's key snippets to
   `web/src/lib/markdown/section-serializers.test.mts`, which runs every gallery fixture
   through its serializer. Background: `web/AGENTS.md` → "Markdown for AI agents".
2. **JSON-LD**: an entry in `SECTION_SCHEMA_CONTRIBUTORS` (`web/src/lib/schema-org/build-graph.ts`),
   usually `null` with a one-line reason. A contributor must be pure, and every field it reads
   must be projected by the section's GROQ branch.

### Phase 5c — Feature inventory

Add the section to the page-builder table in `docs/FEATURES.md` and adjust **both** counts:
the "Page builder — N ready-made content blocks" heading and the "Sections gallery" bullet
("all N blocks"). Nothing fails when it is stale, so this step is the only guard.

---

## Phase 6 — Restart, then check the gallery, the tile and ONE instance

**Restart the Studio AND the web dev server first** (ask the user to; don't start
long-running servers yourself unless asked). Schemas are not hot-reloaded: a Studio holding
the old schema does not recognise the new type and **silently strips it on save**, and a stale
web server under-fetches it.

Then check it in three places:

1. **Sections Gallery** — Studio → **Styleguide** → *Sections* (or `/styleguide/sections/<type>`
   on the web app). The card renders the fixture; a "Needs fixture" card or a render error
   means Phase 5 is incomplete.
2. **Insert-menu tile** — `web/public/admin/thumbnails/<type>.webp`, shown in the grid view of
   **Add item…**. Capture it from the fixture with the thumbnail step of the
   `sanity-module-catalog` skill (`--only=<type>`, `pnpm dev` running; also when an extended
   type's look changed), look at it, and commit it. A missing tile fails nothing.
3. **A real instance** — in the Studio (`/admin` on the web app, or `pnpm dev:studio`), create
   a page (or a draft of a test page), add the section through **Add item** (listed under the
   Phase 4 group), and fill every field with the Phase 1c copy and real images. Open it in the
   **Presentation** tool and compare it with the reference at mobile and desktop widths.

Authoring by hand is the only check that sees the **authoring form**. Look for a field that
should be Portable Text, a nested array wanting a custom input, a list an editor must keep in
step with another, a tab title that wraps, and a short field stranded below a tall array. Set
block styles explicitly (`body-3` for body text, never `normal`).

Create content only in the dataset the user is working in, and only with their go-ahead.
Leave the test page as a draft (or delete it) unless the user wants it published.

---

## Security gate — only for a section that takes input, posts, or renders a URL

Most sections trigger nothing here. Run it when the section draws a form or field, adds or
changes a route under `web/src/app/api/` or a server action in `web/src/app/actions/`, renders
CMS text as HTML, puts an editor URL into a `src`, or needs a third-party script or env var:

1. **One Zod schema validates the input** (`zod` is a web dependency; see
   `web/src/app/actions/sales-inquiry.ts`) and the server parses it again; never trust the
   client. Cap string lengths.
2. **No secret in code or logs.** Declare every new env var in `web/src/setup/envVariables.ts`.
   `NEXT_PUBLIC_*` ships to the browser; a token never carries that name.
3. **Public forms carry a honeypot**: a hidden input in the form and a `honeypot` field in the
   Zod schema; when it is filled the server action returns success without doing anything (as
   `ContactForm/client.tsx` + `sales-inquiry.ts` do). State a missing rate limit instead of
   hiding it.
4. **No `dangerouslySetInnerHTML`**, and an editor-supplied URL reaching a `src`/`href` passes
   an allowlist or `resolveUrl`.
5. **A third-party script goes through the c15t consent manager**
   (`web/src/ui/cookie-consent/consent-manager.tsx`), never a bare `<script>`.

---

## Verify

```bash
pnpm typecheck      # the fixture's `satisfies`, the gallery and the two registry guards catch drift
pnpm lint           # oxlint + check:client
pnpm -C web test    # the Markdown serializer runs over every gallery fixture
pnpm format:check   # oxfmt; `pnpm format` fixes it (long test expectations get rewrapped)
pnpm build
curl -s localhost:3000/<page-with-the-section>.md   # after Phase 6: read what an agent gets
```

Check the page in a real browser at mobile and desktop widths (console free of errors). When
the user gave a reference, screenshot the rendered section at both widths and pass the
screenshots and the reference to the `styling-fidelity-reviewer`.

## Report

Say plainly: the Phase 0 decision and the types compared; the neighbours each part was
modelled on; where the copy came from (`BRAND.md`, the user, or placeholder) and any
`DESIGN.md` conflict raised or change approved; which phases ran and what was left out.

## The one-line version

Inventory, compare, decide reuse / extend / new with the user → `DESIGN.md` for the look, the
2–3 closest sections for the code, `BRAND.md` (unless still the template) for the copy →
component from our primitives and tokens → schema off the neighbours → register in **two**
files, query, typegen, `INNER_SECTION_MAP` → **three** gallery edits, `markdown.ts`, JSON-LD,
`FEATURES.md` → restart Studio + web, gallery, tile, one instance by hand → security gate if it
takes input, posts, or renders a URL.
