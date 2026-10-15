---
name: snap-visual
description: Create a single-page HTML visual brief to explain a concept, plan, architecture, comparison, or proposal — then open it in the browser. Use whenever the user asks to "explain this visually", "show me an HTML page", "make a visual", "diagram this", "visualize X", or wants something rendered as a page instead of prose. Also reach for this proactively when a dense explanation (an architecture, a migration plan, a set of tradeoffs, a design proposal) would clearly land better as a visual document than a wall of text.
---

# Snap Visual

Turn an explanation into a single, self-contained HTML page in one consistent visual language, and open it in the user's browser. The output is a *brief* — a calm, readable explainer document with prose, diagrams, comparisons, and timelines — not a dashboard or an app.

The visual language is fixed and opinionated on purpose. The user has tuned it; every brief should look like it came from the same hand. Your job is to compose *content* into that language, not to redesign it.

## Workflow

`references/template.html` and `references/patterns.html` are bundled with this skill. Resolve them against **this skill's own directory** — the path your harness gave you when it loaded the skill. Never hardcode an absolute skills path: it differs across harnesses (`~/.claude/skills/…`, `~/.agents/skills/…`, project-local `.claude/skills/…`, and others). If you're unsure of the base directory, locate the skill first (e.g. find the `snap-visual/SKILL.md` you're currently following) and work relative to that.

1. **Pick a slug** from the topic — short, kebab-case (e.g. `auth-refactor`, `cache-tradeoffs`).
2. **Copy the template** to `/tmp`, resolving the source against this skill's directory:
   ```
   cp "<this-skill-dir>/references/template.html" /tmp/<slug>.html
   ```
   The template already carries the design system (Tailwind config, palette, helper classes, the container, header, footer). You never rebuild that chrome.
3. **Read `references/patterns.html`** (same directory as the template) — it's the catalog of composable blocks: `section-header`, `prose`, `big-statement`, `columns-divided`, `accent-subpoints`, `divided-list`, `labelled-list`, `timeline`, `inline-relation`, `code-block`, `callout`, `diagram-panel`, `closing-statement`. Each block is marked with a `PATTERN:` comment in the source. Compose the brief from these blocks; don't invent new layouts.
4. **Edit `/tmp/<slug>.html`**: fill the header placeholders (`__KICKER__`, `__TITLE__`, `__STANDFIRST__`, `__FOOTER__`), replace the `CONTENT` comment with your composed sections, keeping the `~mb-20` rhythm between them.
5. **Open it**: `open /tmp/<slug>.html`
6. **Tell the user** the path and give a one-line tour of what's on the page.

The page must stay **one self-contained file** — the only external dependency is the Tailwind CDN already in the template. No local assets, no second file.

## The design language

These are not suggestions. A brief that drifts from them stops looking like the others, which defeats the skill.

**Palette — these five colours only.** They're wired into the Tailwind config as named colours:
- `bg` `#000000` — page background
- `panel` `#1F1F1F` — the *only* raised surface
- `fg` `#EDEDED` — headings and the words that carry the point
- `muted` `#A1A1A1` — body text, secondary labels
- `accent` `#FF9574` — emphasis *only*: kickers, section numbers, the bullet marker, one highlight per diagram, the consequence in a callout

If you find yourself wanting a sixth colour, you're decorating. Use weight, spacing, or `fg`-vs-`muted` contrast instead.

**Sharp corners — this is a hard default.** No `rounded-*` anywhere. If you're reaching for a rounded corner, stop and ask whether the element should be a surface at all — a rounded bordered box is almost always a card you didn't need. The fix is never "round it less"; it's "don't box it." Flatten to columns with hairline dividers, a left accent rail (`border-l-2 border-accent`), or plain dividers. Rounding is a rare, deliberate exception you justify to yourself first.

**Minimal cards — even rarer than sharp corners suggest.** Separation comes from hairlines, columns, accent rails, and whitespace — not from boxes. Concretely:
- Three peers → the `columns-divided` pattern (columns split by `border-x hair`), never three cards.
- A code snippet → `code-block`: a *flat* `bg-panel` surface, sharp corners, no shadow. It reads as code because it's mono on a panel, not because it's a card.
- A relationship between named things → `inline-relation`: mono text joined by an accent glyph, **no boxes** (boxing each term is the mistake to avoid).
- A load-bearing statement → `callout`: a left accent rail, not a box.
- Only a genuine SVG **diagram** gets a full bordered panel — and even that is flat and sharp.
- The single sharpest mistake is wrapping each item of a list in its own box: a list is a list. If you've made more than ~1–2 bordered panels on a page, you're over-boxing.

**Borders.** Hairline only — the `.hair` class (`rgba(255,255,255,0.12)`, 1px). Prefer a single `border-b` or `border-y` to a four-side box wherever it reads cleanly.

**Layout.** The template's `max-w-5xl` column and `border-b hair` section dividers are deliberate — a brief reads as one continuous document, sections separated by hairlines and vertical padding, never boxed. Keep the generous rhythm (`~mb-20` between blocks). Number top-level sections with a mono accent marker (`01`, `02`, …) per `section-header`.

**Type — the thesis is the loudest thing on the page.** The chrome is quiet so the argument can shout. The header `<h1>` is `font-black`, large (`text-4xl md:text-7xl`), tight negative tracking — someone should get the whole point from the header alone. Re-use `big-statement` to open a major section, and `closing-statement` to end the brief on a restatement of the same weight. Body text is `muted`; lift the words that carry the point to `fg`; identifiers, paths, code, enum values go in `.mono`.

**Diagrams.** Inline SVG, same palette: `panel` fill, hairline stroke for normal nodes, **accent stroke for the one node being emphasised**. Sharp rects — no `rx`. Always `viewBox` + `class="w-full h-auto"` so it scales. A diagram earns its panel only if it's genuinely clearer than a sentence — if not, cut it and write the sentence.

**Tailwind, not hand-written CSS.** Compose with utility classes. The palette lives once in the template's `:root` block as design tokens (`--bg`, `--panel`, `--fg`, `--muted`, `--accent`, `--hair`); the `tailwind.config` reads them via `var(--*)`, so the named colour utilities (`bg-bg`, `text-fg`, …) and the `<style>` rules share one source of truth. The rest of the `<style>` block (font stack, `.mono`, `.hair`, `.tag`, `::selection`, the optional `.grid-bg` texture) covers the few things utilities genuinely can't express — don't add to it, and don't restate the palette anywhere else.

## Composing good content

**This is a *visual* brief — the structure carries the explanation; prose only connects it.** The most common failure is writing paragraphs and dropping them into styled containers. That's not a brief, it's an article with a dark theme. Before you write a paragraph, ask whether it should be a diagram, an `inline-relation`, a `columns-divided`, a `timeline`, or a `divided-list`. If the relationship *between* things is the point, draw the relationship — don't describe it.

Keep prose thin:
- Section bodies are short. A block that runs to three dense paragraphs has failed — split it into a diagram plus a caption, a `columns-divided`, or a list.
- Lean on fragments and labels. The `<h3>`s, kickers, mono identifiers, and diagram labels should carry most of the meaning; sentences just join them up.
- **Every section needs at least one visual element** — a diagram, a column split, a timeline, an inline-relation, a code block — not headings over paragraphs.
- A `diagram-panel` is not a once-per-brief luxury. Reach for it whenever there's a flow, a boundary, or a set of things related by arrows. Five sections with one diagram is under-drawn.

The design is calm so the *thinking* can be loud. A brief works when its structure mirrors the argument:

- Open with a **header** whose `<h1>` states the thesis big and whose standfirst carries the detail.
- Use **columns-divided** for a set of peers (provider/seam/domain, before/during/after) — siblings split by hairlines, not boxed.
- Use **accent-subpoints** for paired questions or facets under a heading.
- Use **timeline** for anything ordered — steps, phases, a sequence of decisions.
- Use **inline-relation** for id mappings and equivalences; **code-block** for snippets.
- Use a **callout** for the one or two load-bearing constraints the reader must not miss.
- Use a **diagram-panel** only for relationships genuinely clearer as boxes-and-arrows than as prose.
- Close with a **closing-statement** — the brief's thesis restated at full weight — then a quiet **footer** (what this is, what it isn't).

Match the brief's length to the idea. A single tradeoff might be a header, one `columns-divided`, and a `closing-statement`. An architecture proposal might be five numbered sections. Don't pad to look substantial, and don't cram.

## Example

Input: *"explain the auth refactor visually — the current mess, the proposed module, and how we migrate"*

Output: `/tmp/auth-refactor.html` — header with a `font-black` thesis; section `01` the current problem (a `columns-divided` of the scattered packages, plus a `diagram-panel` of the request flow); section `02` the proposed shape (`big-statement` opener, `divided-list`s, an `inline-relation` for the id binding); section `03` the migration (a `timeline`, then a `labelled-list` of hazards); a `closing-statement` restating the thesis; a quiet footer marking it a draft. Opened with `open /tmp/auth-refactor.html`.
