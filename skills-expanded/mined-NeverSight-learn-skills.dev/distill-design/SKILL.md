---
name: distill-design
description: Distill a DESIGN.md from a website — crawl and analyze a site's rendered design (colors, typography, spacing, components, signature motifs) and produce a brand-accurate DESIGN.md design-system spec. On request, also generate a token-preview page (preview.html) or a realistic website demo (demo.html). Use when the user gives a URL and asks to "make/generate a DESIGN.md", "extract this site's design system", "capture a brand's visual language", or "turn this website into design tokens".
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - WebFetch
  - Bash
---

# /distill-design — Distill a DESIGN.md from a website

Turn a live website into a `DESIGN.md`: a plain-text design-system spec (YAML
token frontmatter + 11 prose sections) that any AI agent can read to generate
on-brand UI. Concept and format follow
[VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md).

**Argument:** a website URL (`$ARGUMENTS`). If none was given, ask for one.

**What gets produced:** by default, **only `DESIGN.md`**. The visual `preview.html`
and the realistic `demo.html` are **opt-in** — generate them only when the user
asks (see the two "on request" sections below).

## Read these first
- `reference/format-spec.md` — the exact frontmatter schema and 11-section body.
- `reference/extraction-guide.md` — how to measure tokens off a live site.
- `reference/template.md` — the `DESIGN.md` skeleton you fill in.
- `reference/preview-template.html` — the **canonical, data-driven `preview.html`**.
  Copy it verbatim and inject only the token JSON (see "Generate the token preview").
- `reference/demo-guide.md` — how to build the realistic demo (only when asked).
(These ship next to this `SKILL.md`, so read them as siblings.)
The `preview.html` shell is the same for every brand — use the template above, never
hand-write it. For a bespoke `demo.html`, the sample folders `examples/stripe`,
`examples/linear`, `examples/spotify` in the source repo
([ake77-code/distill-design](https://github.com/ake77-code/distill-design)) are references.

## Where to write output
By default, write into the **current project** (not this skill's own folder):
- A single spec → `./DESIGN.md` (project root). An optional `preview.html` /
  `demo.html` go alongside it **only when requested**.
- Several specs → use a `distill-design/<brand>/` folder per brand.
- Always honor an explicit path the user gives.

## Workflow

### 1. Scope the target
Confirm the URL. Identify a few page types worth inspecting beyond the homepage:
marketing, pricing, docs, and the app/dashboard if reachable. Brands often flip
polarity (light marketing → dark app) — plan to capture both.

### 2. Inspect & measure
Prefer **measured** values over guesses. Drive a real headless browser and read
`getComputedStyle` — try these **in strict order**, stop at the first that works
(full snippets in `extraction-guide.md`):
1. **Playwright (preferred)** — script Chromium via Bash; install with
   `npx -y playwright install chromium` (or `bunx playwright install chromium`) if
   missing, then `page.$eval(sel, …)` to read exact hex, font stacks, radii, padding,
   shadows. Screenshot too. (`npx` and `bunx` are interchangeable throughout.)
2. **Puppeteer (fallback)** — same approach via `require("puppeteer")` if Playwright
   is unavailable; install with `npx -y puppeteer browsers install chrome` (or the
   `bunx` equivalent).
3. **Browser MCP (Chrome / Preview)** — only if one is already connected.
4. **`WebFetch` / fetch (LAST RESORT)** — text only, no pixel values. Use ONLY when no
   browser can run; combine with brand knowledge and **label the output an *inspired
   interpretation*** in the Colors note and `## Known Gaps`.

Sweep heros, body text, buttons, cards, nav, inputs, and footer. Pull colors → roles,
the type scale, radius scale, spacing base unit, elevation, per-component specs and
states, and the 2–3 signature motifs.

### 3. Map to tokens — go DEEP
The most common failure is a too-thin file. Real brands have many tokens; match that
depth (see `format-spec.md` for the targets):
- **Colors ~18–30+**, named by **role**, kept FLAT. Carry polarity inside `colors:`
  with `*-on-dark` text variants and `surface-dark-*` tiles; tier muted inks by
  approximate opacity in the name (`ink-muted-64`). Only dedupe same-role hexes within ~2%.
- **Typography ~12–20 SEMANTIC roles** (`hero-display`, `lead`, `tagline`,
  `body-strong`, `dense-link`, `caption-strong`, `button-large`, `fine-print`,
  `micro-legal`, `nav-link`), each with weight, line-height, `letterSpacing` in **px**,
  and `fontFeature` only when real. Capture rare weights (300 / 600-vs-700).
- **`rounded`** with `none:0` + `full`; **`spacing`** with measured oddities (17px) and
  a `section` step. Use measured values, not idealized 4/8/12.
- **Components ~15–30+**, each a `{group.token}` composition (literal padding/height/
  size allowed). Variants are SEPARATE keys (`-active`, `-focus`, `-selected`, `-2`).
  **Never document `hover`.**
- Choose an **open-source substitute** for any proprietary font.

### 4. Write `DESIGN.md`
Fill `reference/template.md` into the output path (default `./DESIGN.md` — see
"Where to write output"). Follow the **11-section structure** and the prose tone of the
bundled samples. `name:` is `<Brand>-design-analysis`. The frontmatter `description` is
the most important field — one dense paragraph on a single line (plain scalar, not a
`>` block) vivid enough to picture the site with eyes closed.

### 5. Self-check the DESIGN.md
- Frontmatter is valid YAML; run a quick parse if unsure (see verification below).
- Every `{group.token}` in the body resolves to a defined frontmatter key.
- All **11 sections** present and non-empty (Overview → Known Gaps), including the
  required `## Known Gaps`.
- Depth targets met (~18+ colors, ~12+ type roles, ~15+ components). `description` is
  inline. No `-hover` component keys (brief prose hover is fine). `letterSpacing` in px.
- Colors are role-named and deduped; proprietary fonts have a substitute.

### 6. Offer the visualizations (always end with this)
The `DESIGN.md` is the deliverable. **Do not auto-generate `preview.html` or
`demo.html`.** End your reply by reminding the user they can opt into either, e.g.:

> 已生成 `DESIGN.md`。需要的话我还能基于它生成:
> ① **`preview.html`** —— 设计系统可视化(色板 / 字阶 / 组件,带顶部导航与明暗切换);
> ② **`demo.html`** —— 像真实网站的 Web 落地页或移动端界面。
> 两者都按需生成,要哪个告诉我。

(Match the user's language.) Generate `preview.html` only if asked → follow
"Generate the token preview" below. Generate `demo.html` only if asked → follow
"Generate a realistic demo" below.

## Generate the token preview `preview.html` (on request)

**Do NOT hand-write per-brand HTML/CSS.** The preview shell is identical for every
website — only the injected data changes. The skill ships one canonical, data-driven
template: `reference/preview-template.html` — a polished design-system showcase page:
a sticky nav (the **brand wordmark** + a `distill-design` GitHub chip that links to
`github.com/ake77-code/distill-design` + section anchors + light/dark toggle + a CTA),
a **two-column hero** (`Design System Analysis of <displayName>` + the description + a
device-mock card), then **numbered sections**
("01 — Color Palette", "02 — Typography Scale", "03 — Components", "04 — Spacing &
Radius", "05 — Elevation & Depth", "06 — Responsive Behavior") rendering grouped swatch
cards, a type ladder, a component gallery, spacing/radius blocks, and a breakpoints
table. No footer. Zero dependencies (system fonts, no CDN).

To generate a brand's `preview.html`:
1. **Copy `reference/preview-template.html` verbatim** to `<output>/preview.html`.
2. **Replace ONLY the JSON** inside `<script type="application/json" id="design-data">`
   with the brand's tokens, derived from the DESIGN.md. Change nothing else — the shell,
   CSS, and renderer stay byte-identical across brands.

The injected JSON schema (see the comment above that block in the template):
- `meta`: `{ name, displayName, description, source, nativeTheme: "light"|"dark",
  navCta, heroCtas, sections? }`. `name` is the real brand; the hero reads "Design
  System Analysis of **`displayName`**" — set `displayName` to the **real brand name**
  (e.g. "Apple", "Stripe", "Figma"). Do NOT invent fictional product names — use the
  actual brand the URL belongs to. `description` is the
  frontmatter description verbatim; `source` is the live URL; `nativeTheme` is the
  brand's polarity (dark for Linear etc.). Optional **`navCta`** (nav button label, e.g.
  "Buy" / "Get started") and **`heroCtas`** `["Learn more","Buy"]` set the brand's CTA
  wording. Optional **`heroArt`** picks the hero visual to match the signature motif:
  `device` (default product mock), `mesh` (gradient-mesh fill — Stripe-like brands), or
  `glow` (dark glow — Linear-like brands). Optional **`sections`** = `{ colors:{heading,intro}, typography:{...},
  components:{...} }` gives each section a brand-voiced heading/intro (e.g. "One blue.
  Three near-blacks.") pulled from the matching DESIGN.md body sections; omit for defaults.
- `colors`: the flat palette as role→hex (rgba strings ok). Every role renders as a
  swatch, auto-grouped (Brand & Accent / Surface / Text / Hairlines & Borders / Semantic).
- **`colorRoles`** (optional, recommended): `{ role: "one-line description" }` — the
  per-color usage note from the DESIGN.md Colors section; shows as the swatch's 3rd line
  so cards match the reference depth. **`colorNames`** (optional): `{ role: "Friendly Name" }`
  → renders as "role (Friendly Name)".
- `colorsDark`: **optional** opposite-polarity overrides (else dark is synthesized).
- `typography`: role→`{ fontFamily, fontSize, fontWeight, lineHeight, letterSpacing }`.
- `rounded`, `spacing`: token→value maps.
- `components`: role→`{ backgroundColor, textColor, typography, rounded, padding, border,
  height, size }`; values may use `{group.token}` refs (resolved by the renderer) so each
  gallery sample renders in the real component style.
- **`responsive`** (optional): `{ breakpoints:[{name,width,changes}], touchTargets,
  collapsing, imageBehavior }` from the DESIGN.md Responsive Behavior section — drives
  "06 — Responsive Behavior". Omit the whole key to hide the section.

The template already provides the nav, hero, numbered sections, swatch grouping,
type ladder, component gallery, spacing/radius/elevation blocks, a responsive
breakpoints table, and the
**light/dark toggle** (`localStorage`). The nav wordmark shows the **brand name**
(not a third-party brand); the GitHub chip reads `distill-design` and points at
`github.com/ake77-code/distill-design`.
After injecting the data, verify it opens standalone (`file://`) and visually reads as
a polished design-system analysis page in the brand's colors. For pixel-level reference,
the awesome-design-md project renders each brand at `getdesign.md/design-md/<brand>/preview.html`.

## Generate a realistic demo `demo.html` (on request)

Goal: a **single `.html` file with zero external dependencies** (all CSS/JS inline,
no CDN, no network requests — system/`-apple-system` font stacks only) that reads
like a **real product**, not a token catalog. It is distinct from `preview.html`:
`preview.html` documents the system; the demo *uses* it to ship a believable page.

Read `reference/demo-guide.md` for the full recipe. In short:
1. **Ask form factor** if unclear: **Web** (responsive landing page) or **Mobile**
   (a phone-framed app screen). Default to Web.
2. **Build a real page from the tokens** — pull every color, font, radius, spacing,
   shadow and component straight from the `DESIGN.md`:
   - *Web*: sticky nav → hero (headline + sub + primary/secondary CTA) → social-proof
     logos → 3-up feature cards → pricing tiers → testimonial → CTA band → footer.
   - *Mobile*: a phone frame (status bar, notch) wrapping a real app screen — top bar,
     content list/feed/cards, and a bottom tab bar or now-playing/sticky CTA.
3. **Make it feel real** — plausible copy and product name, the brand's signature
   motif (e.g. gradient mesh, glow hairlines, green play button), realistic imagery
   via inline SVG/CSS gradients (never hot-link external images), and tasteful
   hover/scroll micro-interactions in a tiny inline `<script>`.
4. **Save** next to the spec as `demo.html` (or `demo-mobile.html`).
5. **Verify** it opens standalone (double-click / `file://`) with no console errors and
   visibly resembles a real site in the brand's language.

## Verify

```bash
# YAML frontmatter parses (frontmatter is between the first two '---' lines)
python3 - "$f" <<'PY'
import sys, yaml
t = open(sys.argv[1]).read().split('---', 2)
yaml.safe_load(t[1]); print("frontmatter OK")
PY
```

Then grep the spec for the two most common slips — both must return nothing:

```bash
grep -nE '^\s+[a-z0-9-]*-hover:' "$f"   # no hover-STATE component keys (prose ok)
grep -c '^## ' "$f"                     # must be 11 (Overview … Known Gaps)
```

If you generated a `preview.html` or `demo.html`, open it in a browser — or
screenshot it with a browser MCP — and confirm it renders in the brand's language.

## Notes
- Keep folder names lowercase, URL-safe (`stripe`, `together.ai`).
- `name:` is `<Brand>-design-analysis`. When values are interpreted (WebFetch-only,
  no measured CSS) rather than officially sanctioned, say so in the Colors source-pages
  note and the `## Known Gaps` section — don't fabricate precision.
- One brand per folder; document state variants as separate component keys; never hover.
