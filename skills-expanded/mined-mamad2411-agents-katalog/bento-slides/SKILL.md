---
name: bento-slides
description: Create, edit, and validate self-contained Bento slide decks (`.bento.html`) by authoring the plain JSON document inside the `#bento-doc` script block. Use when Codex needs to turn source material into an interactive presentation, create a deck from the bundled Bento template, revise an existing Bento deck, or add charts, tables, morph transitions, state slides, motion, media, and speaker notes while preserving the embedded editor runtime.
---

# Bento Slides

Create polished Bento presentations without rebuilding the HTML runtime. Treat the JSON document as source and the bundled `.bento.html` file as an immutable application shell.

## Load the authoring rules

Read [references/authoring-guide.md](references/authoring-guide.md) before designing or editing a deck. Use it for the document schema, element requirements, motion patterns, layout rules, and preflight checklist.

Use these bundled resources:

- `assets/Bento_Slides.bento.html`: clean self-contained editor template for a new deck.
- `scripts/bento_doc.py`: extract, replace, and validate the `#bento-doc` JSON without touching the compressed runtime.

## Choose the workflow

### Create a new deck

1. Gather the audience, purpose, source material, presentation length, and desired tone from the request and available files. Make reasonable assumptions when details are absent.
2. Plan the narrative before writing JSON. Give every slide one job and prefer visual evidence over paragraphs.
3. Create a normal JSON file from the minimal document in the authoring guide. Omit `docId` and `collab`; Bento creates them on first open.
4. Produce the deck from the bundled template:

```bash
python3 <skill-dir>/scripts/bento_doc.py replace \
  <skill-dir>/assets/Bento_Slides.bento.html \
  --json /path/to/document.json \
  --output /path/to/topic.bento.html
```

### Edit an existing deck

1. Extract and inspect the current document:

```bash
python3 <skill-dir>/scripts/bento_doc.py extract \
  /path/to/deck.bento.html \
  --output /path/to/document.json
```

2. Preserve unknown keys, existing asset entries, `docId`, collaboration data, and stable element IDs unless the user explicitly requests a reset.
3. Edit the extracted JSON and replace the document in place:

```bash
python3 <skill-dir>/scripts/bento_doc.py replace \
  /path/to/deck.bento.html \
  --json /path/to/document.json
```

Never regenerate the full HTML file. Never alter the compressed `bento-rt-css` or `bento-rt` blocks.

## Design the deck

Map content to Bento features deliberately:

- Compare numbers with a `chart`; use a `table` for categorical grids.
- Reuse deterministic element IDs across adjacent slides and set the later slide to `transition: "morph"` when the same subject changes.
- Use a linked state slide for optional drill-down detail.
- Use full-bleed imagery with a scrim and slow ken-burns motion for a visual hero.
- Animate a process with a path or line, or morph a highlight through its stages.
- Apply `countUp` to a headline metric.
- Keep repeated chrome and logos on stable IDs.
- Write useful `notes` for every non-state slide.

Do not default to bullet-heavy slides. Keep one accent color, no more than two typefaces, and a consistent grid with 96 px side margins for normal content.

## Validate and inspect

Run structural validation after every write:

```bash
python3 <skill-dir>/scripts/bento_doc.py validate /path/to/deck.bento.html
```

Then open the output in a modern browser and inspect the full deck:

1. Confirm the editor loads without an error screen.
2. Review every slide at fit-to-window scale for overflow, collisions, tiny text, and poor contrast.
3. Present the deck and verify morphs, entrances, state links, charts, media, and notes.
4. Iterate on the JSON and rerun validation after changes.

If browser inspection is unavailable, complete structural validation and state that visual QA remains outstanding.

## Preserve safety and portability

- Escape literal `<` characters in the embedded JSON. The helper performs this automatically.
- Embed images and fonts as data URIs in `doc.assets` and reference them as `asset:<key>` when the deck must remain self-contained.
- Embed only short media clips; link large media and explain that playback then needs network access.
- Keep `template: true` only for distributable templates. Remove it for a personal deck.
- Set `readonly: true` only when the user requests a player-only handout.
- Keep the Bento copyright and third-party notices already carried by the template.
