---
name: slides
description: Generate an editable 16:9 .pptx deck from a JSON spec. Use whenever the user asks for slides, a deck, a presentation, a PPT/PPTX, 簡報, 投影片, or to turn notes, a doc or data into a presentation, for any purpose (class, pitch, update, lecture, workshop).
---

# slides — generate a deck from a JSON spec

Every deck in this style comes out of `build_deck.js` from a spec: native shapes, text
and charts, so the user can keep editing in PowerPoint, Keynote or Google Slides. You
write content into the spec; the renderer owns layout, colour and typography.

`$SKILL` below is the directory containing this file (`~/.claude/skills/slides` in a
default Claude Code install).

## Setup (once per machine)

```bash
npm install --prefix $SKILL      # installs pptxgenjs locally
```

Visual QA needs LibreOffice (`soffice`) and `pdftoppm` (poppler). On macOS the render
script finds `/Applications/LibreOffice.app` automatically.

## Workflow

1. **Pin down purpose, audience, length.** Homework, pitch, update, lecture, workshop?
   Who is in the room, how many minutes? If the user gave material (notes, doc, repo,
   data), read it before outlining. Pick a storyline skeleton from
   `references/storylines.md` and a theme preset (`gold`, `navy`, `forest`, `coral`,
   `violet`, `sky`, `mono`) that fits the audience. Ask only if the purpose is unclear.
2. **Write the storyline as action titles first.** One full-sentence takeaway per slide
   ("Cost per shipment falls below single-use by cycle three"), not a label ("Costs").
   Read the titles alone: they must tell the whole story. 1 slide ≈ 1 minute of talk.
3. **Pick a slide type per slide** from `references/slide-types.md`. Never the same
   type twice in a row; never more than two `bullets` slides in a deck. Numbers go in
   `stats` or `chart`, processes in `flow` or `timeline`, comparisons in `table`,
   evidence or a product in `image`, a single idea in `quote`.
4. **Fill `deck.json`** (copy the closest file in `examples/`). Writing rules:
   - Title ≤ 60 chars, subtitle ≤ 110, callout ≤ 105, source ≤ 140.
   - Card / step / item bodies ≤ 3 short lines. Break lines with `\n` like a designer;
     `**bold**` works inside any string. Speaker notes go in `notes`.
   - `callout` is the one sentence to remember; `note` is a caveat above it. Both are
     optional; leave them out on cover, section, closing, and light slides that stand alone.
   - Every number needs a unit and a source; borrowed facts get `[n]` and a
     `references` slide. Every source is one the user supplied or you verified;
     anything else is labelled unverified on the slide.
   - Chinese / Japanese / Korean decks: set `"theme": { "preset": "sky", "font": "Microsoft JhengHei" }`
     (or `PingFang TC`, `Noto Sans TC`); Calibri has no CJK glyphs. CJK text is ~2.3× wider
     per character, so keep titles ≤ 26 characters and card lines ≤ 14 characters.
   - Images: pass paths relative to the JSON (`image`, `cards[].image`, `cover.image`).
     Use only files the user supplied or that you generated.
5. **Build.**
   ```bash
   node $SKILL/scripts/build_deck.js deck.json out/deck.pptx
   ```
   Exit code 3 = the estimator flagged possible overflow or a missing image. The
   estimator guesses; the render is the truth. Shorten text or add `\n`, rebuild.
6. **Render and look at every slide.**
   ```bash
   sh $SKILL/scripts/render.sh out/deck.pptx out/render
   ```
   Read `out/render/deck-sheet.png`, then any suspicious slide at full size. Done when
   every slide has been viewed and none shows: text touching a panel edge, a wrapped
   title, a half-empty slide, a missing logo, a two-line callout. Rebuild and re-render
   after each fix.
7. **Deliver** the `.pptx` path and a 3-line summary: storyline, sources used, what
   the user should still check or replace. The summary is those three lines and nothing else.

## Spec essentials

```jsonc
{
  "title": "File title",
  "brand": { "kicker": "GEOG 240", "logo": "logo.png" },   // chip text + top-right logo, both optional
  "theme": "navy",                                         // preset name, or { "preset": "navy", "accent": "123456", ... }
  "section": "Urban heat islands",                         // default grey label beside the chip; per-slide "section" overrides
  "footer": "Group 4 · Week 6",                            // default footer text when a slide has no "source"
  "slides": [ { "type": "cover", ... }, ... ]
}
```

Per-slide keys on light slides: `title`, `subtitle`, `section`, `source`, `note`
(string or `{ "text": "...", "muted": true }`), `callout`, `notes`.
Types: `cover`, `section`, `cards`, `bullets`, `table`, `stats`, `flow`, `timeline`,
`chart`, `image`, `quote`, `options`, `next`, `references`, `closing`.
Dark slides are `cover`, `section`, `next`, `closing`; everything else is white.
Deck-level and per-type fields: `references/slide-types.md`. Tokens and geometry:
`references/design-system.md`.

## Guardrails

- Change colours through `theme`, never by editing the script during a deck job.
- To add a new pattern, finish the deck with existing types first, then propose the
  pattern separately and add it to `build_deck.js` + `references/slide-types.md` together.
- To update an existing `.pptx` in this style, rebuild from its spec (keep specs next to
  decks). For decks not made here, use the Anthropic `pptx` skill's OOXML editing instead.
