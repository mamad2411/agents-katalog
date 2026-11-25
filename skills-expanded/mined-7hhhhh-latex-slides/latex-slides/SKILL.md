---
name: latex-slides
description: >-
  Build presentation decks with LaTeX/Beamer as the single source of truth and deliver
  vector PDF plus PowerPoint 365 PPTX (per-slide SVG with PNG fallback, speaker notes,
  embedded video, clickable links). Works with user-supplied templates (PPTX, PDF or
  image backgrounds). Use for talks, group meetings, lecture or conference slides,
  "make a PPT/deck", "turn this paper into slides", "export to pptx", or revising an
  existing latex-slides deck. Slide language follows the user.
---

# latex-slides

LaTeX is the only place content lives. The pipeline is fixed:

```
template (user's PPTX/PDF/PNG) ──import──▶ template.yaml + backgrounds
deck.tex + deck.yaml ──build──▶ PDF ──▶ per-page SVG + PNG ──▶ PPTX (notes, links, video)
                                   └──check──▶ verify/<version>.json
```

Slides in the PPTX are full-page vector pictures (text converted to paths). They look
identical to the PDF in PowerPoint 365, but are not editable as text: **to change a
slide, edit `deck.tex` and rebuild.** Say this to the user when you deliver.

`SKILL_DIR` below means the directory containing this file.

## Requirements

TeX Live (XeLaTeX, latexmk, beamer, pgfplots, textpos, xeCJK for CJK), poppler-utils
(`pdftoppm`, `pdftocairo`, `pdftotext`, `pdfseparate`), LibreOffice (template import and
render check), Python 3.9+ with `pip install -r SKILL_DIR/requirements.txt`.
Run `python3 SKILL_DIR/scripts/doctor.py` first; install what it reports missing (ask
the user before installing system packages).

## The seven stages

Do them in order. ★ = stop and get the user's confirmation before continuing.

### 1. Intake ★
Ask only what you cannot infer: purpose and audience, duration, slide language,
template (file or "default"), deliverables (PDF, PPTX or both), sourcing level
(`strict` for academic work with citations on every claim, `normal`, `off`), videos to
embed, deadline. Collect the source material (papers, data, figures, notes).

### 2. Template
- No template: use a built-in one, `SKILL_DIR/templates/paper` (warm paper, indigo and terracotta,
  serif headings) or `SKILL_DIR/templates/default` (white, navy and blue). Pass the name to
  `new_deck.py --template paper`.
- User template:
  ```bash
  python3 SKILL_DIR/scripts/import_template.py <deck_parent>/template_src --pptx their.pptx
  # or --pdf bg.pdf --map cover=1,body=2,closing=3   or --cover a.png --body b.png ...
  ```
  For PPTX, open `layouts.png`, choose layouts, rerun with `--map body=N,cover=N,... --force`.
  If every layout is blank (the design lives on the slides), use `--mode slides`: run it once
  without `--map` to get `slides.png`, then pick the cleanest slide per role. A slide that is a
  single full-page picture (an exported deck) already contains its text; ask for the original
  template or an empty background instead. Read the importer's warnings: it reports boxes that
  cover background decoration and colours it sampled from PDF/image backgrounds.
  Open `preview.png`: the green box (safe area) must cover the free content region of the
  body background, blue = title, red = page number. Edit `template.yaml` (boxes, palette,
  fonts) until it matches the template, regenerate the preview, and show it to the user ★.
  Details: `references/template-spec.md`.

### 3. Outline ★
Write the outline (in the slide language) as a table: slide id, title (a claim, not a
topic), key message, **planned visual**, seconds. Seconds must add up to the duration.
Get approval before writing LaTeX.

### 4. Scaffold
```bash
python3 SKILL_DIR/scripts/new_deck.py <deck_dir> --title "..." --presenter "..." \
    --date YYYY-MM-DD --language zh-CN --duration 900 --template <template_dir>
```
Creates `deck.tex`, `deck.yaml`, `template/`, `assets/`, `media/`, `output/`, `verify/`.

### 5. Write
- `deck.tex`: one `frame` per outline row, each with `\slideid{<id>}`. Use the layout
  macros in `references/macros.md` (`\lead`, `\splitpic`, `\textpic`, `\figat`, `\at`,
  `\pic`, `\point`, `\takeaway`, `\lsvideo`, `\lsrole{cover|agenda|section|closing}`, and the
  dense layouts `lsgrid` with `\card`, `\cardpic`, `\fig`, `\stat`, `\callout`).
  Absolute coordinates are bp from the top-left corner; keep content inside the safe area.
- `deck.yaml`: for every id, `title`, `seconds`, `script` (what the speaker says, spoken
  style, ending with a bridge to the next slide) and `sources`. This file is the only
  place for notes; build.py writes them into the PPTX and `output/*.notes.md`.
- Record every asset's origin in `assets/SOURCES.md` and every reference in
  `references.md`. Images with transparency: flatten to opaque PNG first.

### 6. Build and verify
```bash
python3 SKILL_DIR/scripts/build.py <deck_dir>      # --pdf-only while iterating, --raster-only if needed
python3 SKILL_DIR/scripts/check.py <deck_dir>
```
Fix every FAIL, then rebuild. Report every WARN to the user. Then do the **visual
review**: open each `build/png/slide-NN.png` (or a contact sheet of them) and check
clipping, overlap, alignment, readability from the back of the room, consistent styling.
Write the findings into the `visual_review` field of `verify/<version>.json`. If you
cannot view images, say so explicitly and ask the user to review the PDF.

### 7. Deliver ★
Give the user: `output/<name>.pptx`, `output/<name>.pdf`, `output/<name>.notes.md`,
what changed, check results, anything not verified (for example, video playback inside
PowerPoint itself cannot be tested headlessly). Builds never overwrite: a rebuild
writes `<name>_v2`, `_v3`, ... Keep `deck.yaml`, notes and sources in sync with every
change.

## Rules

1. **Single source.** Content in `deck.tex`, notes/timing/sources in `deck.yaml`. Never
   edit the generated PPTX, `ls-config.tex` or files in `build/`.
2. **Text and visuals on every slide (图文并茂), with real information.** Every content slide
   carries at least one visual: original figure, TikZ diagram, pgfplots chart, table,
   screenshot or video. Text explains the visual and adds what the picture cannot show:
   the key numbers, the comparison, the conditions. A good content slide has one main
   visual (40–60 % of the safe area) plus 2–4 annotated points or headline numbers
   (`\stat`); use `lsgrid` to put several figures, cards or numbers side by side instead of
   one lonely picture. Body text budget ≈ 150 CJK characters or 90 English words; split the
   slide instead of shrinking fonts. Slides with almost no explanation get a density
   warning. Preferred visual sources, in order: original figures (cited) → charts/diagrams
   drawn from real data → schematic diagrams → generated illustrations (label them
   "illustrative"). A text-only slide needs a `text_only_reason` in `deck.yaml`. check.py
   enforces this.
3. **One message per slide.** Claim-style title, `\lead` states the question, `\takeaway`
   states the conclusion and bridges to the next slide.
4. **Honest sourcing.** Every number and borrowed figure has a source (per sourcing
   level). Separate verified results from plans, hypotheses and illustrative data, and
   say so on the slide or in the notes. Never invent data, citations or quotes.
5. **Template fidelity.** Use the template's backgrounds, palette (`lsPrimary`,
   `lsAccent`, `lsMuted`, `lsText`, `lsRule`, `lsInverse`), fonts and boxes. No ad-hoc
   colours or font sizes outside the template unless the user asks.
6. **Language.** Skill files are English; slides, notes and outline use the user's
   language (`language` in deck.yaml selects fonts and note labels).
7. **Overlays** (`\pause`, `\onslide`) become separate slides in the PPTX, not
   animations; notes go on the first page of the frame.
8. **Never overwrite** deliverables; never delete the user's files.

## References
- `references/macros.md` – layout macros and coordinates
- `references/template-spec.md` – template.yaml fields and import tips
- `references/deck-yaml.md` – deck.yaml fields and checks configuration
- `references/troubleshooting.md` – common build and viewer problems
- `examples/demo/` – complete example deck
