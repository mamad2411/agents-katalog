---
name: moda-deck-theme
description: >-
  A deck's visual theme, designed with you before any content exists: four
  title directions, section heads and a closing, then eight workhorse
  layouts — placeholder only, approved phase by phase.
argument-hint: "[what the deck is for] [--brand <kit>]"
allowed-tools: Bash(moda:*), Read
---

# moda-deck-theme

<!-- moda:banner -->
**PREREQUISITE — load `moda-core` once per session** (step-0, write contract,
free/metered map). Already loaded? Skip ahead. If you cannot load it, the
non-negotiables: run `moda doctor --json` before anything; `moda brand list`
before creating; every write carries the latest revision — on
`stale_revision`, re-read and retry once (it heals); send the canvas link the
moment it exists; stuck or failed? `moda ask "<question>"` — free and fast,
never guess.
<!-- /moda:banner -->

## What this is

A wizard-style flow for establishing a deck's visual theme *with* the user before any real content exists. Runs on a blank 1920×1080 slides canvas — with a brand kit bound when one is in play — and ends with twelve placeholder slides that define a complete visual system. If the canvas already has designed slides, or the user wants specific content designed right now, say so and ask how they want to proceed.

Five phases, each gated on explicit approval. **Do not generate the next phase without it** — "what's next?" or "let's move on" is the gate. Anything the user said in their opening prompt supersedes the defaults below; acknowledge it so they know you read it.

Set up, then open by setting expectations in a sentence or two — four title directions, then section heads and a closing, then the workhorse layouts, pausing at each step, all content placeholder — and go straight into Phase 1:

1. `moda brand list`, then `moda canvas create --name "[Deck] theme" --intent "a slide theme: 4 title directions, ceremonial slides, 8 workhorse layouts" --size 1920x1080 --pages 1 --category slides --brand [KIT]`.
2. `moda canvas share CANVAS_REF` — send the link at once: "follow along live here."
3. A kit is bound → LOOK at its assets before designing anything (references/brand.md). No kit → read references/no-brand-design.md first. Either way, compute the type ladder from references/design-quality.md (1920×1080 → body ≈ 40px, floor 18px).

**No kit means the theme IS the identity** — never that you design plain.
`moda brand list` comes back empty, or the user declines one, so step 1 runs
without naming a kit. Read the binding the create reports back rather than
assuming it came out empty — a bound kit IS a kit, so design to it or unbind
(`moda canvas brand`), and say which you did. Genuinely unbound, the
wizard invents: a palette with two color worlds, distinctive faces, a motif,
all chosen for this deck's subject (references/no-brand-design.md). Phase 1's
four directions become four genuinely different *identities*, and Phase 3's
contract is what locks the chosen one in. A generic blue-and-gray theme is a
failed run, not a neutral one.

## Phase 1 — Title slide, 4 variants

`moda canvas add-pages CANVAS_REF --count 3`, then one `moda canvas markup CANVAS_REF --file - --page P` per variant: four title slides, each a genuinely different aesthetic axis. With a kit, all four use its real colors, type and logo — the variants explore *design language*, not brand attributes. Without one, each variant brings its own invented palette and type pairing, so the pick settles the identity as well as the language. Pick four from: type-led/anthemic · image-led · editorial · compositional/off-grid · minimalist/reductive · color-shock/block · maximalist/layered · geometric/constructivist · tactile/hand-made · technical/diagrammatic. With directional hints from the user, pick four that fit the direction; without hints, span clearly different territory — one type-driven, one image-driven, one color/composition-driven, one wildcard — and vary your picks across sessions.

Name each page with a letter and its approach ("A — Anthemic") so the user can reference them; page names are set in the edit lane (`update(pageId, { name: 'A — Anthemic' })`, references/edit-code.md). `moda canvas screenshot CANVAS_REF` and LOOK before presenting. Present them as a choice, noting that only one moves forward and the other three get deleted, so this is the moment to choose.

- **Picks one** → make any requested edits, then **delete the other three** (`moda canvas delete-items CANVAS_REF [PAGE_IDS]`) before proceeding. The clean canvas signals the lock-in.
- **Wants a hybrid** ("type from A, layout from C") → build a fifth variant, delete the rest.
- **None work** → ask one question — which axis was wrong (typography, layout, color, imagery)? — then generate a fresh four from the remaining approaches. **Never iterate on rejected variants.**

> Unsure which axes a second round should use? `moda ask "which aesthetic axes should the second round of slide title variants use after the first four were rejected?"`.

## Phase 2 — Ceremonial slides

`moda canvas add-pages CANVAS_REF --count 3` — three slides that set the deck's emotional register, all visibly siblings of the title (same type pairings, color logic, grid):

1. **Section head, punchy** — a moment. Large type, strong color, for major breaks.
2. **Section head, quiet** — restrained, more whitespace, for subsections. The pair is what gives the deck rhythm instead of every break landing the same.
3. **Closing / thank you** — mirrors the title's energy with a sense of arrival, often the title's composition with one clear shift (inverted color, mirrored alignment).

Screenshot all three, present them together, and iterate until approved.

## Phase 3 — Theme contract

Write the locked system out in plain prose to the user (not a slide, no approval needed — it's a status update): type scale (which font for display vs body, exact sizes, caps/weight rules), color roles (which kit color — or, with no kit, which invented hex — is background, accent, type, data emphasis), layout pattern (grid, alignment, margins, whether off-grid is in play), image treatment, and logo behavior (no kit and no mark from the user → none; never invent one). Close with: every workhorse slide will adhere to this — now's the moment to adjust. **Without this contract Phase 4 drifts**; it's the connective tissue and the thing specific feedback points back to.

## Phase 4 — Workhorse slides

Eight layouts, generated **2–3 at a time** with a feedback pause between batches so drift gets caught before it compounds: big number / stat hero · two-column comparison · quote / testimonial · 3-up grid · full-bleed image with caption · text-content slide · timeline / process flow · data slide. One `moda canvas markup` apply per slide, `moda canvas screenshot` after each batch, and LOOK. Every one must visibly inherit the theme contract; if a slide could belong to a different deck, redo it before moving on.

The text-content slide especially: **do not default to bullet lists.** Carry the 3–5 points with typographic hierarchy, color emphasis, or a numbered sequence.

## Phase 5 — Handoff

Summarize the twelve slides — title, two section-head styles, closing, eight workhorse layouts — point back to the live link, and offer the two natural next moves: apply the theme to real content, or refine a specific slide. Export only on the user's format words or one accepted offer: `moda export CANVAS_REF --format pptx|pdf -o …`.

## Throughout

- **Placeholder content only.** Never invent specific facts, real-sounding metrics, named people or company claims. "Section title here", "Key insight", "47%", "Discover / Build / Launch". Real-looking content invites the user to mistake it for a real claim.
- **One or two sentences of design rationale** per phase ("all-caps because your display font has strong caps"). Enough to make feedback precise, not an explanation of the design.
- **Vague feedback gets exactly one question** — which axis — then proceed.
- **Iterate refines the direction; pivot abandons it.** On a pivot, don't anchor to the previous attempt.
- A targeted fix to an approved slide is a small `moda canvas edit` code batch (references/edit-code.md); a whole-slide rebuild is `moda canvas markup --mode replace`.

## Errors

`invalid_markup` names the element it skipped — one page per apply, then re-run. `stale_revision` heals: re-read and retry once. Anything else → load moda-core and read its recovery reference.

See also: moda-deck — the full deck build once a theme exists ·
moda-core — the contract, recovery, everything Moda can do.

## References

| Doc | Load when |
|---|---|
| references/deck-design.md | before Phase 1 — concept-first covers, the layout bar |
| references/markup.md | before any markup apply |
| references/design-quality.md | the type ladder, imagery, shaders, the AI-slop list |
| references/brand.md | a kit is bound — look at its assets, not just its tokens |
| references/no-brand-design.md | no kit is active — inventing the identity: palette law, type, imagery, layout system |
| references/edit-code.md | page names; targeted edits to an approved slide |
