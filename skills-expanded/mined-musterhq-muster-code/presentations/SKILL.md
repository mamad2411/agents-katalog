---
name: presentations
description: Create, edit and review PowerPoint decks (.pptx) with Muster. Use whenever the person asks for slides, a deck, a pitch or a presentation, or to change an existing .pptx. Builds slides with pptxgenjs on a slide master, renders every slide to an image with office_render and fixes text that overflows or overlaps until each slide is clean.
metadata:
  short-description: PowerPoint decks (.pptx) with a slide-by-slide render check
---

# Presentations (.pptx)

Use this skill for any slide deck: new ones, edits to an existing .pptx, and reviews of how one looks.

## Tools

- `muster_office` `office_setup`: call it once per chat before the first script. It answers with the command that
  runs a script (`<node> script.mjs`); with it `import pptxgen from 'pptxgenjs'` works from any folder. Do not
  `npm install` anything into the person's project.
- `muster_office` `office_render`: renders every slide to a PNG and shows you the first ones (pass
  `inline_pages` up to 8 to see more at once). The first render may download LibreOffice; wait for it.
- Libraries: `pptxgenjs` writes new decks (text, bullets, shapes, tables, pictures and native charts); `jszip` edits
  an existing deck's XML in place.

`example.mjs` next to this file is a tested starting point (slide master, title, bullets, a native chart, a table, a
picture, speaker notes). Copy it into the working folder and change it.

## The loop

1. Plan the deck: one message per slide, a title for each, what goes on it (bullets, chart, table, picture).
2. Write a script in the working folder. Keep the slide content as data at the top; one function per slide kind.
3. Run it with the command from `office_setup`.
4. Call `office_render` on the .pptx and look at every slide image.
5. Fix the script, run and render again until every slide passes the checks. Reply with the path and an outline.

## Quality checks (on every slide image)

- No text overflows its box, runs off the slide or is cut off. Titles fit on one or two lines.
- Nothing overlaps unless it is meant to; there is clear space between items and around the edges (at least 0.4 in).
- Text is large enough to read: titles 28-40 pt, body 16-24 pt, nothing under 12 pt. At most about six bullets.
- Fonts and colours are consistent across slides; text contrasts with its background.
- Charts have readable labels and the values the person gave; tables fit the slide.
- Pictures keep their aspect ratio and are not blurry.

When text does not fit: cut words first, then split the slide, then make the box bigger, and only then make the font
smaller. `fit: 'shrink'` helps titles in PowerPoint, but the render shows the size as written, so still check.

## pptxgenjs rules that prevent most problems

- Set `pptx.layout` first (`LAYOUT_WIDE` is 13.33 x 7.5 in, `LAYOUT_16x9` is 10 x 5.625 in). Every `x`, `y`, `w`, `h`
  is in inches; keep `x + w` and `y + h` inside the slide.
- Use `defineSlideMaster` for the shared background, footer and slide number, and `addSlide({ masterName })`.
- Bullets: one text object with an array of runs, each `{ text, options: { bullet: true } }`; do not type "•".
- Charts: `slide.addChart(pptx.ChartType.bar | line | pie | doughnut | area | scatter, data, options)` with
  `data = [{ name, labels, values }]`. These are real, editable charts.
- Pictures: `addImage({ path | data, x, y, w, h, sizing: { type: 'contain', w, h } })` to keep the aspect ratio.
- Fonts: Arial, Calibri, Georgia or Verdana render the same everywhere.
- `await pptx.writeFile({ fileName })` writes the file; the script must await it.

## Editing an existing deck

pptxgenjs cannot open a deck. To change one, keep its layouts and theme and edit it with `jszip`:

- Slides are `ppt/slides/slideN.xml`; text is in `<a:t>` elements inside shapes (`<p:sp>`). A sentence can be split
  over several `<a:r>` runs.
- Layouts and masters (`ppt/slideLayouts/`, `ppt/slideMasters/`) and the theme (`ppt/theme/`) hold the look; leave
  them alone so the deck keeps its design.
- To add a slide, copy an existing slide XML that uses the layout you want, together with its `_rels` file, and
  register it in `ppt/presentation.xml`, `ppt/_rels/presentation.xml.rels` and `[Content_Types].xml`.

```js
import JSZip from 'jszip';
import { readFile, writeFile } from 'node:fs/promises';
const zip = await JSZip.loadAsync(await readFile('deck.pptx'));
const path = 'ppt/slides/slide2.xml';
zip.file(path, (await zip.file(path).async('string')).replace('<a:t>Q2</a:t>', '<a:t>Q3</a:t>'));
await writeFile('deck-updated.pptx', await zip.generateAsync({ type: 'nodebuffer', compression: 'DEFLATE' }));
```

Escape `&`, `<` and `>` in text you put into XML. Render the original and the edited deck and compare them. Write to a
new file unless the person asked you to change theirs in place.
