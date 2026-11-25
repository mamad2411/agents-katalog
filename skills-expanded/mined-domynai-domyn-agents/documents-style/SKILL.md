---
name: documents-style
description: Write documents (reports, briefs, white papers, one-pagers, memos, analysis write-ups) in any format, e.g. PDF, HTML or Word, in the house style shared with the slides, with its palette, fonts and backgrounds. Use when asked for a report or a document in any format.
external_files:
  - scripts/
  - ../../resources/seaborn_style.py
  - ../../resources/palette.json
  - ../../resources/typography.json
  - ../../resources/assets/fonts/
---

# Documents

Documents in the house style, the one the slides use, in whatever format is asked for. The
house style below holds for every format. PDF has a module of its own that applies it for you
(see PDF); HTML is an example of a format without one, and any other format (Word, …)
follows the house style the same way.

## The house style (every document)

Paths in this file are relative to this SKILL.md, whose location is the `[file: …]` line above this text: resolve
them from its directory, never from the working directory.

Every document takes its look from the resources shared by every builtin skill, the same ones
the slides and charts use:

| Path | What it is |
|---|---|
| `../../resources/typography.json` | the fonts and the text sizes, by role (`title`, `heading`, `intro`, `body`, `caption`, `table_cell`…), shared with the slides. Each role names a style (the face and whether it is bold, and the font file) and a size in points |
| `../../resources/palette.json` | every colour, by key: `primary` and the other accents, `text.light_background.*` / `text.dark_background.*`, `surfaces.*`, `lines.*`, `backgrounds.*` (the page backgrounds: `white`, `tint`, `blue`, `navy`, `violet`), `charts` |
| `../../resources/assets/fonts/` | DM Sans, the only font (OFL) |
| `../../resources/seaborn_style.py` | the chart style (the `charts` skill), for every chart in the document |

- **Font**: DM Sans for every piece of text, in the style and size of the element's role in
  `typography.json`. Never another font.
- **Colours**: only from `palette.json`, by key; never a colour of your own. Text on white or
  light backgrounds (`white`, `tint`) takes `text.light_background`, on `blue`, `navy`,
  `violet` or `card_highlight` `text.dark_background`.
- **Backgrounds** are the palette's `backgrounds.*`: plain white, or a gradient between its
  colours (`gradient` linear at `angle` degrees clockwise, or radial from the top-left corner),
  never an image. The house style has no
  logo of its own.
- **Never blue on blue**: on a blue, navy or violet background, no text in `primary`, `secondary`,
  `tertiary` or `quaternary`, links included. A link keeps the colour of the text around it,
  underlined.
- **Charts**: drawn with the `charts` skill, never with colours of their own.

## Formats without a module (HTML, and any other)

Build the document with whatever the format calls for, in the house style above: DM Sans from
`assets/fonts/` (embedded or linked as the format allows, e.g. `@font-face` in HTML), every
colour from `palette.json` (backgrounds from its `backgrounds`), every size from
`typography.json`. Give links an explicit colour, the surrounding text's: the default in browsers and
word processors is blue.

## PDF

You write the document as a short Python script that builds it with **`pdf_layout.py`**, this
skill's module (in `scripts/`), on reportlab. The module holds the look: the cover, the page
background, the page number, the type styles, tables, callouts, the closing
page. You write only the content, as a list of blocks (the *story*).

Every page setting the module uses (page size, margins, type spacing, table and callout
geometry, positions on the cover and closing pages, which backgrounds a page may use) is in
**`scripts/pdf_layout.json`**, and the module reads it at import (`d.LAYOUT`). Its colours are
palette keys, never hex, and its type is the slides': the fonts and the size of every element
the slides also have (titles, body, captions, tables…) are roles of
`../../resources/typography.json`, which the layout names by role. Change a setting there, for
every document, never by restyling blocks in a build script.

The module reads everything from the resources above: it takes each colour from `PALETTE` by its
key, draws each page's background gradient, and **embeds** DM Sans in the PDF, so it looks
the same on any machine. Never type a hex colour or load another font.

### Setup

Check `python -c "import reportlab, pymupdf"`; install what is missing (`pip install reportlab
pymupdf`, or `uv pip install ...` in a uv project) and say in one line that you did. pymupdf
runs the collision check before delivery. Charts also need
`seaborn` (see the `charts` skill).

Import the module from the skill, by its absolute path; never copy it out, since it finds the
resources from its own place in the tree:

```python
import sys
from pathlib import Path

sys.path.insert(0, "<dir of this SKILL.md>/scripts")
import pdf_layout as d
```

### Step 1: Settle the content

- Work from what the person gave you (notes, data, a draft, an analysis). Don't invent figures,
  client names or claims. If something essential is missing (audience, purpose), ask once.
- **Internal or external?** External documents end with the closing page (`closing=True`).

### Step 2: Plan the document

- **One idea per section**, and the section titles alone should tell the story. Write a title as
  the takeaway ("Agents cut onboarding time by 40%"), not a topic label ("Onboarding").
- Standard shape: an executive summary first (an `intro()` line with the main finding, then the
  few points that support it), then one section per question, then next steps.
- Prefer a table for comparison data, a chart for a trend or a distribution, a callout for the
  one thing the reader must not miss. Never more than one callout per page.

### Step 3: Write the story

```python
story = [
    d.h1("Agents cut onboarding time by 40%"),
    d.intro("New analysts reached their first answer in five days instead of nine."),
    d.p("The pilot ran for <b>six weeks</b> with 42 analysts in risk, credit and operations."),
    d.bullets(["Faster first answer for new analysts", "Fewer escalations to senior staff"]),
    d.callout("<b>Recommendation.</b> Extend the pilot to the legal team in Q4."),
    d.h2("Results by team"),
    d.chart(Path("onboarding.png"), caption="Days to first answer, by team"),
    d.table(
        [["Team", "Before", "After"], ["Risk", "9 days", "5 days"], ["Credit", "7 days", "5 days"]],
        align=["left", "right", "right"],
    ),
]
d.build(
    Path("Pilot report.pdf"),
    story,
    title="Pilot report: agents for analyst onboarding",
    subtitle="Internal review · October 2026",
)
```

| Block | What it is |
|---|---|
| `h1(text)` | a section title: 23pt, with the slides' title rule under it |
| `h2(text)`, `h3(text)` | subsection headings: 15pt and 12pt bold |
| `intro(text)` | the lead line under a section title (14pt), at most two lines |
| `p(text)` | a body paragraph, 11pt |
| `bullets(items)`, `numbered(items)` | lists, one string per item, **without** a typed `•`, `-` or `1.` |
| `table(rows, col_widths=None, align=None)` | the template's table; the first row is the header and repeats on every page. ≤ 6 columns, short cell text; numbers right-aligned |
| `chart(png, caption=None, width=None)` | a chart PNG at the text width, proportions kept, caption under it |
| `callout(text, kind="highlight")` | a card with one short message: `"highlight"` (`primary` blue) for the key finding, `"light"` (outlined) for a note |
| `spacer(points)`, `page_break()` | spacing and a forced new page; rarely needed |

Text in `p`, `intro`, `bullets`, table cells and callouts is **reportlab markup**: `<b>`,
`<i>`, `<u><a href="https://...">link</a></u>`. A literal `&`, `<` or `>` in text you did not
write as markup must go through `d.escape(...)`, or the build fails. `title` and `subtitle`
are plain text.

`build(path, story, *, title, subtitle="", cover=None,
page_background=None, closing=False, contacts=())` adds the rest (`cover` and
`page_background` default to the layout's `default_cover` and `default_content`):

- **The cover**: the title (44pt, at most three lines, about 20 characters each), the
  rule and the subtitle (one line, e.g. audience · date). `cover` is one of
  `blue` (default), `navy`, `violet`; use another only if the person asks for a different look.
- **Content pages**: on `white` (default) or `tint`, the page number bottom left.
- **The closing page** (`closing=True`): "Thank you", on the cover's background. With
  `contacts=[...]` (one line each, markup, a link as `<u><a href="...">...</a></u>`) it also
  shows "Explore more" and the contacts, as on the deck's closing slide. Pass contacts only if
  the person gives them; never invent any.

A heading starts a new page by itself when too little of the page is left under it; don't
add page breaks to keep a heading with its text.

### Charts

Draw every chart with the `charts` skill: `seaborn_style.py` (copied, with `palette.json`,
`typography.json` and `fonts/`, next to the build script) gives it the same palette, font and
text sizes as the document. Draw a full-width chart at the text width,
`seaborn_style.figure(width=642, height=370)`: `d.chart(...)` then places it at its own size, so
its labels have the document's body size (a wider figure is scaled down, and its text with
it); for a half-height one, `height=240`. Save it with `seaborn_style.save(fig, out, name)` and
place the PNG with `d.chart(...)`. Never a chart from another library, or colours of your own.

### Writing

- Tone: confident and specific. Short paragraphs: three to five sentences.
- Sentence-case headings, no full stop at the end of a heading.
- Put the conclusion first, in each section and in the document.
- Name the file after the document, e.g. `Q3 Board Update.pdf`.

### Check before you deliver (required)

1. **Run the collision check** on the built PDF, and deliver only when it says
   `no collisions`:

   ```sh
   python "<dir of this SKILL.md>/scripts/check_pdf.py" "Pilot report.pdf"
   ```

   It reads where every glyph actually landed and exits with status 1, listing each one, if
   any text is printed on other text, on a chart, is crossed by a line, or runs past
   the margins or off the page. What each finding usually means:

   | Finding | Usual cause | Fix |
   |---|---|---|
   | text on text | a style or a `Paragraph` of your own with a leading smaller than its size; text drawn on the canvas yourself | use the blocks only; never build your own styles or draw on the canvas |
   | text on an image | a label placed over a chart | put it in the caption, or in the chart itself |
   | text crossed by a line | a flowable of your own in a table cell, wider than its column | plain text in cells, or a wider column |
   | text outside the margins / off the page | a flowable of your own sized past the text width | sizes from the blocks; `table` and `chart` already keep within the text width |

   The module itself prevents the collisions it can: a line with larger inline text grows to
   fit it, a numbered list makes room for its widest number, `table` scales column widths that
   add up to more than the text width, `chart` scales a picture to the text width and to the
   page, `spacer` ignores a negative height, and the cover makes a long title or subtitle
   smaller (to 60% at most). A cover title that does not fit even then stops the build with
   `cover title too long`: shorten it.
2. Render the pages to images: `pdftoppm -r 60 -png doc.pdf page` if poppler is installed, or
   with `pymupdf` (`page.get_pixmap(dpi=60).save(...)`).
3. Look at every page. Fix before delivering:
   - a heading or a lone line at the bottom of a page, a page nearly empty for no reason;
   - a table wider than the text, wrapped headers, cells broken mid-word: cut words, or fewer
     columns;
   - a chart with overlapping labels, or a legend covering data;
   - text that is hard to read against what is behind it;
   - anything the person asked for that is missing.

Fix problems in the build script and rebuild; never edit the PDF.
