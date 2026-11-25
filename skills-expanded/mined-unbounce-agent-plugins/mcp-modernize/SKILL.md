---
name: mcp-modernize
description: Rewrite an imported (absolutely-positioned) Unbounce Classic page variant as clean responsive HTML through Unbounce MCP. Use when the user asks to modernize a page, make a page responsive, get rid of absolute positioning, make a clean-HTML version of an existing Classic page, or edit a page that was hand-built in the Unbounce Classic builder — phrasings like "modernize this page", "make my page responsive", "convert my old page", "clean HTML version". Replication-faithful — this is a layout rewrite, never a redesign. Not for AI Builder pages, which stay editable as they are (mcp-ai-builder-authoring).
requires:
  mcpServers:
    - unbounce-mcp
---

# Modernizing an Unbounce page (responsive rewrite)

Turn a page built in the Unbounce builder into clean, responsive flexbox/grid
HTML — **pixel-faithful to the original on desktop, reflowing sensibly on
mobile**. This is a REPLICATION task with zero creative latitude: same copy,
same images, same fonts, same colors, same element counts. The only thing that
changes is the layout model (absolute positioning → flex/grid).

The pipeline is two deliberate stages:

1. **Import** — `create_variant_from_existing_variant` clones the builder-built
   source into an MCP-managed variant that renders identically (deterministic;
   every string, image URL, font, and form field lands in the copy verbatim).
2. **Rewrite** (this skill) — read that copy, restructure its layout to
   responsive flex/grid, and write it back **in place** with
   `update_variant_from_html`.

Extraction fidelity is stage 1's job and it is deterministic — never work from
the original builder page directly, and never re-derive content from screenshots
or memory. Your job is only the layout transformation.

## Language with the user

Never say "modernize", "modernization", "replica", or platform-internal terms
to the user. Their page is fine; say "make your page responsive" and "an
editable copy of your page". The result cannot be edited in the Unbounce
builder — all future edits go through MCP tools; say so at handover, and never
suggest the builder.

## Workflow

**Step 1 — Resolve the target.** Identify the page (`list_client_pages`) and
variant (`list_page_variants`). If the target variant is builder-built (not
MCP-managed), tell the user in one line what is about to happen — e.g. _"I'll
create an editable copy of your page, then make that copy responsive — your
original stays untouched"_ — then run `create_variant_from_existing_variant`
(no `target_page` ⇒ new page). No further permission ceremony is needed; the
copy is additive and safe. Relay any conversion warnings honestly. A
fixed-width "autoscale" source converts fine — the conversion report notes that
runtime viewport scaling isn't preserved; that is expected and harmless here,
because you rewrite the page responsive from scratch (Step 4), discarding the
scaling entirely. If the target is already an MCP-managed imported copy, skip
straight to Step 2.

**Step 2 — Read the copy.** `get_variant` on the imported variant. Download the
`html_ref` / `css_refs` sources and any `scripts` entry's `ref` (via `download`, or
`download_inband` if you cannot run shell commands). This body is the **sole
source of truth** for every value: copy strings, image URLs (with their
`srcset`), `@font-face` blocks, colors, dimensions, form fields, `<ub:dynamic>`
tags. Never guess a value, never take one from a screenshot, never reconstruct
from memory. If the copy came from an autoscale source, its CSS wraps lengths in
`calc(<px> * var(--scale, 1))` and it may carry a viewport scale script —
ignore both: read the plain px value (the `* var(--scale)` is the fixed-width
scaling you are removing) and never copy the scale script into the rewrite. Your
responsive layout comes from the Step 3 rows, not these fixed dimensions.

**Step 3 — Get the layout skeleton and fidelity signals.** `get_layout_hints`
on the same variant. It returns, per section: `rows` (element ids clustered
into visual rows, left-to-right), per-element geometry,
`cross_section_overlays` (elements whose vertical span crosses into later
sections), and `design_width` (the fixed canvas width). **The rows are your
flex/grid structure.** Do not derive structure from the absolute coordinates
yourself, and never translate `top`/`left` values through into the rewrite.
It also returns measured fidelity signals — `page_defaults` (the page's real
base text color and typography), per-section backgrounds, per-element
colors/typography/text/image/link inventories, `palette`, `loaded_fonts`,
`row_stats`, `content_extent`, `hidden_elements`. Those are ground truth:
author from them per [rules/color.md](rules/color.md), never from assumption.
If hints come back empty for a variant that plainly has a positioned tree,
stop and report it (see [rules/verification.md](rules/verification.md)).

**Step 4 — Audit, in writing, before any HTML.** Post a compact audit into the
conversation (it must survive context compaction): per section — the row
structure from hints, the element **counts** per row, every text string
(verbatim), every image URL + srcset, fonts, colors, form fields
(name/type/order/options/submit label), interaction states (`:hover`/`:focus`),
and every cross-section overlay with its pattern (column vs centered). Every
value in your output must trace back to an audit row.

**Step 5 — Write the responsive HTML.** Follow
[rules/layout.md](rules/layout.md) (section/inner max-width pattern, flex/grid
from hint rows, overlay handling) and
[rules/replication.md](rules/replication.md) (verbatim preservation). If the
user also asked for a change ("modernize it and swap the headline"), use
two-pass authoring: pass 1 is a content-identical rewrite, verified; only then
apply their change (see TWO-PASS in rules/replication.md).

**Step 6 — Self-check before writing back.** Run the checklist in
[rules/verification.md](rules/verification.md) — text walk, count checks, the
closure checks against the extracted signals (image-src, link-href, palette,
font sets; the WCAG contrast table from [rules/color.md](rules/color.md)), and
the hard stops (`position:absolute` budget, zero authored `cbc-*` references,
flex/grid present, per-section max-width, overlay columns reserved). Fix
failures before delivering; never rationalize past a hard stop.

**Step 6b — Carry GA click tracking across.** A Classic page's link clicks are
tracked by Unbounce's built-in GA link tracker, which keys off builder elements.
Your rewrite is hand-written `<a>` tags, so that tracker stops attaching and the
customer silently loses click data they had before. Preserving it is replication
fidelity, not a redesign — so include
[`../mcp-page-authoring/scripts/ga-click-tracking.js`](../mcp-page-authoring/scripts/ga-click-tracking.js)
as a `scripts` entry (name it e.g. "GA click tracking", placement `body_bottom`).
Never fork or hand-roll it. It feature-detects `gtag`/`ga` and no-ops on domains
without the integration, so it is safe to add unconditionally.

**Send it as a `ref`, not a `tag`.** Read the file, `upload` it, and pass the
`upload://` reference it returns as the entry's `ref` — see
[Writing a `scripts` entry](../mcp-page-authoring/SKILL.md#writing-a-scripts-entry).
"Pass its contents verbatim" is not a shape `update_variant_from_html` accepts:
an entry is a bare `upload://` string, or an object with exactly one of `ref`,
`src` or `tag`. Handing it the raw JavaScript as a string fails loudly, which is
fine.

A `tag` is accepted, and what happens next depends on the tag. A bare
`<script>…</script>` is unwrapped on write and stored exactly as a `ref` would
be, so it does round-trip. An **attributed** one — `<script type="text/javascript">`
— is stored verbatim, opening tag and all, and comes back as a `tag` whose text
starts with `<script`. Use `ref` so there is a single shape either skill can
recognise, and so the entry you re-send later is the one you read.

**Pass back every `scripts` entry the variant already had, plus this one.** Step 7
has you send a complete `scripts` set, and in that call anything you leave out is
deleted — so "don't add a second copy" must not become "don't include it". You
already downloaded the existing entries in Step 2; re-send each one unchanged. If
you are making no script change at all, omit `scripts` entirely instead, which
preserves what is there.

**Recognising an entry that already carries this tracking:** its body **contains**
the line `// Google Analytics click tracking.` — the script is passed verbatim, so
that string is present in any entry either skill created. Test for the line being
present, not for the body starting with it: `get_variant` hands a JS-body script
back as a `ref` you must download, and the `scripts_preserved` / `removed_scripts`
reports give a `tag` that starts with `<script>`. Step 2 has already downloaded
every script here, so the bodies are to hand. If one is there, re-send it as-is
and add nothing; a second copy double-counts every click, which is worse than the
under-count it was meant to fix and much harder to notice.

The why and the guardrails (never add the GA loader) live in
[`../mcp-page-authoring/rules/google-analytics.md`](../mcp-page-authoring/rules/google-analytics.md).

**Step 7 — Write back in place and hand over.** `update_variant_from_html` on
the same variant. It is a TRUE FULL REPLACE: pass the complete artifact set
(html + all css + all js) every time — anything omitted is dropped. `scripts` is
the one exception to "every time", and only because omitting the array entirely
is how you say "change no scripts"; see the paragraph below before you pass it.

**`scripts` deserves its own care.** Passing the array replaces the complete set,
and a variant can carry entries nobody authored through these tools — an Unbounce
popup attaches itself as one. Dropping such an entry deletes a customer's popup or
tracking pixel, and nothing about the rendered page shows it happened. So re-send
every entry you read in Step 2, or omit `scripts` altogether if you are changing
none of them (omission preserves them). This is the one place where "pass
everything" and this skill's promise to _preserve user customizations verbatim_
can pull apart if you are not deliberate.

The change is staged, never published by you. Hand the user: what you did (one line), the
`preview_ref` from a fresh `get_variant` (plus the builder preview link from
`list_page_variants` for the original, so they can compare), the evidence
summary from the self-check, and any genuine differences — concrete and
specific, or "none". Publishing, traffic, and goals are the user's call.

## Hard invariants (the load-bearing rules)

- **No creative changes. No additions.** Same typo, same order, same counts.
  Nothing added that has no source element — no nav, no sticky header, no hover
  effects the source lacks. Conversion-optimization defaults from
  `mcp-page-authoring` do NOT apply to a rewrite — replication trumps
  landing-page best practices. **One deliberate exception:** the GA
  click-tracking script in Step 6b. It adds no content and changes nothing a
  visitor sees; it restores instrumentation the source page already had and the
  rewrite would otherwise drop. Nothing else earns an exception here.
- **Every source text string appears verbatim** in the rewrite (whitespace-
  insensitive). Element names, ids, and image filenames are NOT content.
- **Reuse every asset by its exact URL**, keeping `srcset`/`image-set` and
  `background-position`/`size`/`repeat` verbatim. Copy `@font-face` blocks and
  `<ub:dynamic>` tags through unchanged.
- **Forms:** plain `<form>` in your output; preserve field names, types, order,
  options, and the submit label exactly (the server re-wires submission on
  write). Preserve the hidden form-confirmation overlay (`cfm-*` markup) and
  its trigger script verbatim if the copy has one.
- **Preserve user customizations verbatim**: custom-HTML embeds, tracking
  scripts, hand-applied CSS classes. Flag (don't rewrite) any script selectors
  that target old ids.
- **No subagent delegation.** The source must stay in the same context as the
  build — a subagent without the verbatim source invents copy.
- **Stay in your lane at delivery**: staged in-place update, no publish, no
  traffic, no goal changes.

Long-form rules, worked examples, and the catalog of real past failures:
[rules/replication.md](rules/replication.md) ·
[rules/layout.md](rules/layout.md) ·
[rules/color.md](rules/color.md) ·
[rules/verification.md](rules/verification.md) ·
[rules/failure-catalog.md](rules/failure-catalog.md)
