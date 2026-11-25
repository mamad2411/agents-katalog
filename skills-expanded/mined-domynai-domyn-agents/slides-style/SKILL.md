---
name: slides-style
description: Build PowerPoint slides in the house style with python-pptx, through this skill's slides module, using the shared palette (backgrounds included), DM Sans type scale and the layouts specified here. Use when asked for slides, a deck, a pitch or a presentation as a .pptx and no template file is to be used.
external_files:
  - scripts/
  - template/
  - ../../resources/seaborn_style.py
  - ../../resources/palette.json
  - ../../resources/typography.json
  - ../../resources/assets/
---

# Slides

You build the deck with **`scripts/slides.py`**, this skill's module: one call per slide, which
takes only the slide's content (titles, points, cards, table cells). The slide is made from one
of the layouts of **`template/layouts.pptx`**, a PowerPoint template, so it is a real slide of
that layout (placeholders, outline, "Reset slide"); its positions, sizes, fonts, colours,
background and slide number are the template's, with every colour and font written in from
the shared resources when the deck is opened. Your build script is a short list of those calls. **Never copy the module, and
never place a title, card or rule yourself**: what no layout covers is the one exception
(see "Other content").

**A deck is finished only when `deck.save()` says so.** It saves the deck, runs the collision
check (`scripts/check_pptx.py`) and only if no text collides — overflows its box, runs into a
rule, another text or a card's edge — does the file get the name you asked for, with
`<file>: no collisions` printed. Otherwise it raises, and the deck stays as
`<name>.unchecked.pptx`: not deliverable. Never catch that error, never save another way
(`deck.prs.save()`), and never deliver an `.unchecked` file. In your reply, quote the line
`<file>: no collisions` that the save printed: it names the file that passed.

**When text does not fit, change the content, never the font size.** Every call measures its
text as it writes it. What does not fit is not raised on the spot: the `Deck` method records it
and carries on, and `save()` then lists **every** problem of the deck in one go, each with its
slide, its layout and field, and **exactly what fits** — for one line, the words that fit
("what fits is 'Agents are ready for' (20 characters)"); for a list, how many lines the box holds.
Fix all of them in one pass, each to the length it names or shorter, then run the script once
more. Never fix one, run, and fix the next: one run tells you everything. The answer is always to
rewrite, reorganize or re-split the content (Step 3).

## What it uses

Paths in this file are relative to this SKILL.md, whose location is the `[file: …]` line above this text: resolve
them from its directory, never from the working directory.

| Path (relative to this SKILL.md) | What it is |
|---|---|
| `scripts/slides.py` | The module: `Deck`, one method per layout, and `save()`. Import it, never copy it |
| `template/layouts.pptx` | The template: one slide layout per layout below and per background variant. Edited in PowerPoint, never by a build script (see "The template") |
| `scripts/check_pptx.py` | The collision check `save()` runs; also runnable by hand (see the last section) |
| `../../resources/palette.json` | Every colour (`sl.P` in the module), the slide backgrounds included (`backgrounds`) |
| `../../resources/typography.json` | Every font and text size: the styles, the type scale and the text roles (`sl.T`), shared with documents |
| `../../resources/assets/fonts/` | The DM Sans files (`DM Sans`, `DM Sans Light`, `DM Sans SemiBold`, `DM Sans Medium`, with their italics), OFL-licensed |
| `../../resources/seaborn_style.py` | The chart style (the `charts` skill), for a chart placed on a slide as a PNG |

## Setup

Check `python -c "import pptx"`; if it fails, install it (`pip install python-pptx`, or
`uv pip install python-pptx` in a uv project) and say in one line that you did.

The deck names its fonts; it does not embed them. Check that the families are installed
(`fc-list | grep "DM Sans"`, or look in `~/Library/Fonts` on macOS). If they are not, copy
`../../resources/assets/fonts/*.ttf` to `~/Library/Fonts` (macOS) or `~/.local/share/fonts` followed by
`fc-cache -f` (Linux), and say in one line that you did. Tell the person that whoever opens the
deck needs the same fonts installed, or PowerPoint substitutes another font. `DM Sans Thin` (the
two-card numbers) is not among these files; it falls back if it is missing.

## Step 1: Settle the content

- Work from what the person gave you (notes, a doc, bullet points, a brief). Don't invent figures,
  client names or claims. If something essential is missing (audience, purpose), ask once.

## Step 2: Plan the deck

Write a short plan: one line per slide with its layout and its message. Rules:

- **One message per slide**, and the slide titles alone should tell the story.
- Standard shape: title → agenda if there are 3+ sections → section dividers between sections →
  content slides → closing.
- **Every slide is one of the layouts below.** Pick by content shape: a list of points → text
  slide; 2 items → two cards; 3 items → three cards; 4 items → four cards; comparison data →
  table. Content none of them takes (a chart, a single image) goes under "Other content"; a
  grid of cards of your own is never one. Vary layouts; don't use the same layout more than
  twice in a row.
- **Fit the capacity.** Every layout gives its capacity (lines, characters, items). Write the
  content to it while planning: a slide's text is a summary of the source, not a copy of it. If
  content exceeds a layout's capacity, apply Step 3 while planning, before writing any code.
- **Most slides are plain white with black text.** A coloured background is an accent, here and
  there: the title, the section dividers and the closing, and at most one content
  slide in four, never two in a row (the layouts' `dark=True`, or `background=` on
  `content_slide`). Mark in the plan which slides get one.

Show the plan to the person only if they asked to review it; otherwise build.

## Step 3: When text does not fit

A problem `save()` lists (or a refusal from `text()` or `bullets()` on "Other content") means
the content does not suit the slide. **The sizes are fixed**: every element keeps the size its layout
gives it, whatever its text. Change the content instead, in this order:

1. **Tighten the wording.** Keep each point, drop the rest: no filler, nothing the title already
   says, a figure instead of a sentence, a phrase instead of a clause.
2. **Reorganize it.** Give the content the layout its shape calls for: parallel items → cards,
   figures to compare → table, a long point → a short bullet whose detail gets a slide of its own.
3. **Re-split it across slides.** Move points to a neighbouring slide with room, or divide the
   slide in two, each with its own takeaway title (never "(1/2)", "(cont.)").
4. **Re-plan** if several slides overflow: revise the plan of Step 2 and rebuild, rather than
   patching one slide at a time.

A slide title that does not fit on one line is rewritten shorter (≤ 40 characters); it is never set
smaller or allowed onto a second line.

## Building the deck

```python
import sys

sys.path.insert(0, "<dir of this SKILL.md>/scripts")  # absolute: the skill's own directory
import slides as sl

deck = sl.Deck()
deck.title_slide("Agents in production", "Board · October 2026")
deck.agenda(
    "Ready for regulated work",
    "Three pilots, one platform, a plan for Q4.",
    [("Where we are", "The pilots and their results"), ("What comes next", "The Q4 rollout")],
)
deck.divider_slide("Where agents pay off", highlight="agents")
deck.text_slide("Agents cut onboarding time by 40%", ["Three pilot teams", "Six weeks"])
deck.two_cards(
    "Claims before and after",
    [
        ("Before: manual and slow", "Adjusters spend 60% of their time on paperwork.", "High cost"),
        ("After: assisted", "The agent extracts, checks and recommends.", "70% faster"),
    ],
)
deck.closing_slide()
deck.save("Q3 Board Update.pptx")
```

Run the script. If `save()` lists problems, fix every one of them (Step 3) — to the length each
one says fits, or shorter — and run it again, until `save()` prints
`Q3 Board Update.pptx: no collisions`. Most decks need one or two runs; a run per problem means
the list was not read whole.

## Layouts

Each layout is one `Deck` method. Give it the content its capacity allows; the method places
everything and draws the slide number.

### 1. Title slide

`deck.title_slide(title, subtitle)`, on the `blue` background: the presentation title (53pt, ≤ 2
lines, about 30 characters in all), a rule and the subtitle (one line, e.g. audience · date).
The alternatives,
`background="navy"` or `"violet"`, only if the person asks for a different title look.

### 2. Agenda

`deck.agenda(takeaway, summary, topics)`: the key takeaway (30pt, ≤ 2 lines, about 20
characters), a summary (1–2 lines) and up to 6 numbered topics, each `(topic, description)`: the
topic ≤ 30 characters, the description one line (about 55 characters). `dark=True` for the occasional navy accent.

### 3. Section divider

`deck.divider_slide("Where agents pay off", highlight="agents")`, on the `tint` background: the
heading centred (30pt, one line, ≤ 45 characters), with the optional highlighted word in
`primary`. Alternative backgrounds: `navy`, `blue` or `violet` (`background=`), where nothing
is highlighted.

### 4. Two cards (plain white)

`deck.two_cards(title, [card_01, card_02], intro=None)`, for a two-part argument: before/after,
problem/solution. Each card is `(heading, body, takeaway)` (or `sl.TwoCard(...)`): the heading
one line (about 30 characters), the body ≤ 3 lines (about 160 characters), the takeaway ≤ 2
lines (about 120 characters). Card 01 is the highlighted one, in `primary`.

### 5. Three cards (plain white)

`deck.three_cards(title, [card, card, card])`, for three pillars, offers or options. Each card is
`(title, subtitle, bullets)` (or `sl.PillarCard(...)`): the title one line (about 12 characters:
two lines do not fit), the subtitle one line, ≤ 4 short bullets. `dark=True` for the occasional navy accent.

### 6. Four cards (plain white)

`deck.four_cards(title, [card, card, card, card])`, for four pillars. As three cards, with the
title ≤ 2 lines (about 20 characters in all) and ≤ 3 short bullets. `dark=True` for the occasional navy
accent.

### 7. Table (plain white)

`deck.table_slide(title, rows)`, for comparison data: `rows` is a list of rows, the header first,
every cell a short string (one line). ≤ 6 columns, ≤ 7 rows; `col_w=` sets each column's width
(1.33 in by default, the table at most 9.39 in wide).

### 8. Closing

`deck.closing_slide()`, on the `blue` background: "Thank you". With
`contacts=["Write to team@example.com", …]`, one line each, it also shows "Explore more" and the
contacts, as plain text. Pass contacts only if the person gives them; never invent any.

### 9. Text (plain white)

`deck.text_slide(title, points, intro=None)`: the slide most decks need most. **≤ 6 bullets,
each ≤ 2 lines (about 180 characters)**, one point per bullet, without a typed `•` or `-`. More
than that is two slides, or a different layout (two groups → two cards, a comparison → table).
`dark=True` for the occasional navy accent.

### Other content

**A chart** is drawn with the `charts` skill (`../../resources/seaborn_style.py`), which takes its
colours from this same `palette.json`, its font from the same DM Sans and its text sizes from
the same `typography.json`, and saved as a PNG; never a python-pptx chart with colours of its
own. Draw it at the size of the box it goes in, 96 pixels per inch (the content area below,
9.39 × 3.10 in: `seaborn_style.figure(width=901, height=298)`), so its labels have the slide's
body size, and place it with `sl.picture()`, which keeps its proportions.

For a slide no layout takes (a chart, a single image), start it with
`s = deck.content_slide(title, intro=None)` (plain white, or `background=` one of `tint`,
`blue`, `navy`, `violet`) and put the content in the content area, x 0.29 to
9.68 and y 1.25 to 4.90 (1.57 to 4.90 with an intro), with the module's helpers, which measure
their text as they write it:

| Helper | What it draws |
|---|---|
| `sl.picture(s, path, x, y, w, h)` | a PNG inside the box, at its own proportions |
| `sl.text(s, x, y, w, h, text, role_or_size, colour, style=None, spacing=None)` | a text box; `role_or_size` is a role (`"body"`, `"caption"`…) or a size in pt with `style=` |
| `sl.bullets(box, colour)` | turns a `text()` box into bullets |
| `sl.link(paragraph, text, url, role_or_size, colour)` | an underlined link run in `colour`, the surrounding text's: on light slides only (see Contrast) |
| `sl.card(s, x, y, w, h, radius, fill=None, outline=None)`, `sl.rule(s, x1, y, x2, colour)` | a card (before the text on it) and a rule |

Colours come from `sl.P` by key (`sl.P["text"]["light_background"]["body"]`), the styles are
`sl.REGULAR`, `sl.BOLD`, `sl.TITLE`, `sl.LIGHT`, `sl.THIN`. A typical chart slide:

```python
s = deck.content_slide("Onboarding time fell in every team", intro="Days to first answer")
sl.picture(s, "files/onboarding.png", 0.29, 1.57, 9.39, 3.10)
sl.text(
    s,
    0.29,
    4.70,
    9.39,
    0.20,
    "Source: pilot data, Q3",
    "caption",
    sl.P["text"]["light_background"]["muted"],
)
```

## Backgrounds

**Most slides are plain white**, with black text: every content layout is plain white unless
given `dark=True` (or `background=` on `content_slide`). A coloured background is an accent, used
only here and there: the title slide, the section dividers and the closing, and at
most one content slide in four, never two in a row (a single strong statement, a screenshot).
Every background is one of `palette.json`'s `backgrounds`, named by its key: plain white, or a
gradient between colours of the palette, drawn by the presentation app itself (there are no
background images).

| Name | Colour | Family | Use for |
|---|---|---|---|
| `white` | `backgrounds.white` (flat) | light | **every content slide** by default |
| `tint` | `backgrounds.tint`: white into a pale blue, bottom right | light | **section divider**; a light accent for an occasional content slide |
| `blue` | `backgrounds.blue`: electric blue into indigo | blue | **title slide and closing slide**; section divider, alternative; bright content slides |
| `navy` | `backgrounds.navy`: a deep blue glow, top left, into near-black | dark | every `dark=True` layout; title slide and section divider, alternatives; dark slides with a screenshot |
| `violet` | `backgrounds.violet`: violet through blue into indigo | violet | title slide and section divider, alternatives; an occasional content slide |

Use the alternative title slides only if the person asks for a different title look. `white` and
`tint` → `text.light_background` colours; every other background → `text.dark_background`
colours. The full rules are under Contrast.

## Colours

**Every colour comes from `palette.json`.** The layouts take theirs from it; for "Other content",
take the values from `sl.P[...]` by key; never type a hex code into the build script.

| Key | Use |
|---|---|
| `primary` | on light slides only: agenda title, numbers (01, 02 …), the optional highlighted word of a section divider, table headers, the fill of card 01 |
| `secondary`, `tertiary`, `quaternary` | further accents; `tertiary` is also the accent text colour on navy slides (agenda numbers) |
| `quinary`, `senary` | the template theme's fifth and sixth accents; on slides only through charts |
| `text.light_background.title` | on light slides: the slide title, the intro line, the section divider, table body cells |
| `text.light_background.heading` / `.body` / `.muted` | text on light backgrounds and on `card_light`: headings (card headings and takeaways, agenda takeaway and topics) / normal text / descriptions |
| `text.dark_background.heading` / `.body` / `.muted` | on the blue, navy and violet backgrounds and on `card_highlight`: titles and headings / normal text / descriptions |
| `backgrounds.*` | the slide backgrounds (see Backgrounds), set by the layouts |
| `surfaces.slide_plain` | the plain white slide's fill (set by the slide helpers) |
| `surfaces.card_light`, `surfaces.card_highlight` | card fills on light slides |
| `surfaces.card_dark_gradient` | card fill on dark slides, with `gradient(…, angle_deg=135)` |
| `surfaces.table_header_band`, `surfaces.table_header_band_outline` | the band behind a table's header row: its radial fill and its gradient outline |
| `surfaces.table_band_row` | the fill of every other table body row (used by `table()`) |
| `lines.table_grid` | the table's inner grid lines (used by `table()`) |
| `surfaces.shadow_light`, `surfaces.shadow_dark` | card shadows on light / dark slides |
| `lines.title_rule_light`, `lines.title_rule_dark` | the rule under the slide title |
| `lines.title_slide_rule` | the rule on the title and closing slides, and the short accent rule in dark cards |
| `lines.divider_light`, `lines.divider_on_blue`, `lines.divider_dark` | thin separators: agenda rows, table rows, inside cards |
| `charts` | chart colours (series order, scales, grid), read by `seaborn_style.py`: a chart goes on a slide as a PNG from the `charts` skill, never as shapes coloured from here |

No colours outside `palette.json`.

## Contrast

**All text must be clearly readable against what is directly behind it.** The minimum is
**4.5:1** for text below 18pt and **3:1** for 18pt and above (or 14pt and above in `TITLE` or `BOLD`),
apart from the one exception below. The table lists which text colours go on which background;
the ratios in brackets are the lowest over every colour of the background's gradient, so
they hold wherever the text sits. Stay inside the table and the minimum holds.

| What is behind the text | Allowed text colours (ratio) | Never |
|---|---|---|
| `white`, `card_light` | `text.light_background.title` (21), `.heading` (18.0), `.body` (10.7), `.muted` (5.0); `primary` (8.6) | anything from `text.dark_background` (1.0), `tertiary` (2.4) |
| `tint` | `text.light_background.title` (17.8), `.heading` (15.2), `.body` (9.0), `.muted` (4.3, see the exception); `primary` (7.3) | anything from `text.dark_background` (1.0), `tertiary` (2.1) |
| `navy`, `card_dark_gradient` | `text.dark_background.heading` (13.7), `.body` (11.6), `.muted` (10.0); `tertiary` (5.6) | `primary` (1.6), `secondary`, `quaternary`, anything from `text.light_background` |
| `blue`, `card_highlight` | `text.dark_background.heading` (7.2), `.body` (6.1), `.muted` (5.2) | any accent colour as text (`tertiary` 2.9, `primary` 1.0), anything from `text.light_background` |
| `violet` | `text.dark_background.heading` (6.0), `.body` (5.1); `.muted` (4.4) only at 18pt or larger | any accent colour as text, anything from `text.light_background` |

The one exception, allowed only in exactly this place: `text.light_background.muted` directly on
`tint`, 4.3:1: only at 11pt or larger and only for short descriptions (the agenda's, a caption).
Never below 11pt, never for running text: use `.body` there. Nothing else may be justified by it.

**Never blue on blue.** On the `blue` or `violet` background or a `card_highlight` card, no text is
in a blue or any other accent colour (`primary`, `secondary`, `tertiary`, `quaternary`):
not a highlight, not a number, not a link. Everything on them is `text.dark_background`.
Links in particular:

- **No links on dark slides** (the blue, navy and violet backgrounds, or a `card_highlight`
  card): write the address as plain text in the surrounding colour, like the contacts on the
  closing slide. Some presentation apps draw every text link in the theme's link colour, a
  blue, whatever colour the slide gives it.
- On light slides, make every link with `sl.link(paragraph, text, url, role, colour)`, with
  `colour` the surrounding text's: it stays that colour, underlined. Never set
  `run.hyperlink.address` yourself: PowerPoint then draws the link in the theme's blue.
- On navy, `tertiary` stays the agenda numbers' colour only.

Also:

- Keep text in the positions the layouts give.
- Text on a card follows the card's row in the table, not the slide's background.
- Never put text over a photo, screenshot or chart: put it beside, above or below.
- Chart labels, legends and series follow the same table.
- If you are unsure, work it out: contrast = (L1 + 0.05) / (L2 + 0.05), with L the WCAG relative
  luminance of the lighter (L1) and darker (L2) colour; for an image, use the lightest (for
  dark text) or darkest (for light text) part behind the text.

## Typography

**The font is always DM Sans**, for every run of text, including tables and charts, in the
families `typography.json` names (`DM Sans`, `DM Sans Light`, and `DM Sans Thin` for one
element). The `text()` and `run()` helpers set it on every run; never
leave a run on the default (Calibri), and never use Arial, Aptos or any other family. The bullet
dot is DM Sans too (the `regular` face, set by `bullets()`).

**The type is in `../../resources/typography.json`**, shared with documents as the palette is:
the five styles, the type scale, and the **roles**, the elements slides and documents both have, each
with its style and size. Read nothing about type from anywhere else, and type no family name or
size the layouts don't give.

**Most elements are given a role** (role `title`, role `body`): pass its name where the helpers
take a size, `text(slide, 0.29, 0.22, 7.65, 0.38, "Agents cut onboarding by 40%", "title", colour)`,
and the role sets both size and style. Never pass a role's size as a number, or a `style=` with a
role. The roles: `title` (slide title), `heading` (a card's heading), `intro`, `body` (running text,
bullets, descriptions), `emphasis` (takeaways, card subtitles), `caption`, `table_header`,
`table_cell`, `page_number`, `closing_title`, `explore_more`, `contact`.

**Elements only slides have** (the presentation title, the section divider, card titles, the
agenda's numbers…) are given a size in pt and a style; pass both, `size` then `style=`. Every run
takes one of five styles, each a face plus a bold flag, exactly as the template sets them. The
bold flag is part of the style: the template draws its titles and headings bold, so a heading
without it is lighter than the house style's.

| Style (`style=`) | Key in `typography.json` | Use |
|---|---|---|
| `TITLE` | `title` | slide titles on content slides, the section divider, the card titles of the three- and four-card slides |
| `BOLD` | `bold` | headings and takeaways in the two cards, the agenda's key takeaway and topic names, card subtitles, emphasis inside body text |
| `REGULAR` | `regular` | everything else: body, descriptions, presentation title and subtitle, the dark agenda's title, agenda numbers, table cells, intro line |
| `LIGHT` | `light` | "Thank you" and "Explore more" on the closing slide |
| `THIN` | `thin` | the large card numbers (01, 02) on the two-card slide |

Never set bold on a `REGULAR`, `LIGHT` or `THIN` run, and never use a style for an element the
table gives another one. For text the layouts don't cover, use a role (`body` for text,
`heading` for a heading over it) and, only if none fits, a size from the typography's `scale`.

**Every element takes exactly the size it is given**, never larger and never smaller, whatever its
text. Body text is small by design. If text doesn't fit, change the content (Step 3).

**Text never overlaps other text.** python-pptx does not grow or shrink a box, and text that does
not fit spills out below it (or above, for a bottom-anchored box); a table row grows instead,
pushing the rows below it down. While planning, estimate the height text takes as **lines ×
size in pt × 1.2 / 72** inches at single spacing (× the line spacing when one is set), counting
lines from the width: about 60 characters per line at 19pt across 7.65 in, 105 at 11pt; scale for
other widths and sizes. The collision check at the end does this exactly, with the DM Sans
files themselves, and is what decides.

## The template

This section is for whoever changes the look, not for building a deck.

`template/layouts.pptx` holds one slide layout per layout and background variant ("Title",
"Title · navy-plain", "Two cards", "Three cards · dark", "Text with intro", "Content · navy-folds",
…), named as the module picks them. Open it in PowerPoint (View › Slide Master) to move, resize or
restyle anything; the module follows. What it holds is geometry: every shape names what it takes
from the shared resources in its name (Selection Pane), `label [key=value; …]`, and opening a
deck writes those in, so a colour, font or picture set in PowerPoint is replaced on load:

| Key | Takes | From |
|---|---|---|
| `color`, `fill`, `outline`, `line` (+ `width`) | a colour | a palette key, `text.light_background.title`, `surfaces.card_light`… |
| `gradient` (+ `angle`), `shadow` (+ `blur`, `dist`) | a gradient fill, a shadow | `surfaces.card_dark_gradient`, `surfaces.shadow_light`… |
| `role`, or `style` + `size` | the type of the text | a role of `typography.json`, or a style (`regular`, `bold`, `title`, `light`, `thin`) and a size in pt |
| `image` | a picture | a file under `resources/assets/` |
| `slot` (placeholders only) | the text a `Deck` method writes there | its name: `title`, `heading 1`, `bullets 2`… |
| `spacing`, `align`, `anchor`, `bullets` | paragraph details of a placeholder | `1.12`, `center`, `bottom`, `yes` |

A layout's background is tagged on the layout's own name (Slide Master › Rename Layout),
`Content · navy [background=navy]`, and opening a deck writes that entry of `backgrounds` in as
the layout's real background (Format Background), then takes the tag off the name, so a deck
lists its layouts as `Content · navy`. Every layout names one, `white` included. Opening the
template refuses it, naming the layout and shape, when a layout or shape has no tag, a tag
names a key, background, role or file the resources do not have, or an accent colour is text
on the `blue` or `violet` background. A new layout
needs a `Deck` method that starts it by name and fills its slots, and a test.

## Writing

- Tone: confident and specific.
- Sentence-case titles, no full stop at the end of a title, no exclamation marks.
- Write slide titles as the takeaway ("Agents cut onboarding time by 40%"), not a topic label
  ("Onboarding").
- Name the file after the deck, e.g. `Q3 Board Update.pptx`, and save it with `deck.save()`.

## Check before you deliver (required)

1. **`deck.save()` printed `<file>: no collisions`** for the file you deliver, and you quote
   that line in your reply. A deck that did not pass is `<name>.unchecked.pptx`; nothing else
   is deliverable. To check a deck by hand (it exits with status 1 if anything collides):

   ```sh
   python "<dir of this SKILL.md>/scripts/check_pptx.py" "Q3 Board Update.pptx" --render "Q3 Board Update check/"
   ```

   It lays every text box out the way PowerPoint does, measuring each run with the shipped DM
   Sans files, and lists each problem with its slide, the shape's name, the start of its text
   and where it is (inches):

   | Finding | Usual cause | Fix |
   |---|---|---|
   | text overflowing its box | more words than the layout's capacity | change the content (Step 3); never the font size or the box |
   | text crossed by a line | text of your own run into a rule | change the content (Step 3) |
   | text on text | a box of your own placed on another one | keep "Other content" inside the content area, clear of the rest |
   | text on a picture | a label on a chart or screenshot | put it beside, above or below |
   | text out of its card / text under a shape | a card of your own added after its text, or smaller than it | add the card first; change the content |
   | table row grown | a cell's text needs more than one line | shorter cell text, or fewer columns |
   | text off the slide / outside the safe area | a box of your own past x 0.29–9.68 | keep "Other content" in the content area |

   A `note:` line is not a collision: it says something was measured approximately (a font that
   is not shipped) or not checked (a rotated shape).
2. The render (`save()` makes it, in `<deck name> check/`) is a PDF and one PNG per slide, drawn
   by LibreOffice with the shipped DM Sans, so line breaks are the real ones even where DM Sans is
   not installed. If LibreOffice is missing it says so and the check itself still runs. Look at
   every PNG, and delete the folder before delivering. Fix before delivering:
   - Uneven text lengths across sibling cards, or a card much fuller than its neighbours.
   - A chart or picture too small to read, or text that is hard to read against what is behind it.

Fix problems in the build script and rebuild; don't hand-edit the saved file.
