---
name: powerpoint-gjensidige
description: >
  Build PowerPoint decks on the official Gjensidige template, inheriting the real
  logo, the Gjensidige Display and Gjensidige Type fonts, theme colours, footer and
  slide numbers. Use when someone asks for a deck, a presentation, slides or
  lysbilder in Gjensidige branding, wants a beslutningsgrunnlag or steering document
  as PowerPoint, wants to extend an existing Gjensidige presentation, or mentions
  .pptx, .potx, Gjensidige-mal or presentasjonsmal. Covers the whole run: locating
  the template, picking a layout, filling in content, and checking the result
  visually before handing it over.
---

# PowerPoint on the Gjensidige template

Always build on top of a real Gjensidige deck. The template carries the logo,
fonts, colours, footer, slide numbers and sensitivity label in its masters. Build
from scratch with `pptxgenjs` and you have to recreate all of it by hand, and the
result never quite lands.

General PowerPoint mechanics (pptxgenjs, XML editing, `markitdown`, validation,
chart pitfalls) belong to the **`pptx` skill**. This skill covers only what is
specific to the Gjensidige template and calls into `pptx` for the rest. Do not
duplicate it.

Slide text is normally Norwegian even though this skill is written in English.
Keep æ, ø and å intact, and never degrade them to ae/o/a.

## The `pptx` dependency

Resolve this before Step 4, which runs `pptx`'s validator. Check whether the skill
is already installed:

```bash
# macOS / Linux
ls ~/.agents/skills/pptx/SKILL.md ~/.claude/skills/pptx/SKILL.md 2>/dev/null

# Windows (PowerShell)
Test-Path "$HOME\.agents\skills\pptx\SKILL.md", "$HOME\.claude\skills\pptx\SKILL.md"
```

If it is installed, its scripts live next to that `SKILL.md`, so the validator is
at `~/.agents/skills/pptx/scripts/office/validate.py`. Call that `PPTX_DIR` and
move on.

If it is not installed, fetch it and follow its instructions:

```bash
npx skills use "https://github.com/anthropics/skills" --skill "pptx" > pptx-skill.txt
```

Read `pptx-skill.txt` **in full**. Redirecting to a file first matters because the
output is long enough to be truncated when read inline, and the part you need sits
right at the end, where it names the directory the supporting files were downloaded
to. Every relative path inside that SKILL.md resolves from **that** directory rather
than from this skill's folder. That directory is `PPTX_DIR`.

## Before you start

Runs on macOS, Windows and Linux. Python does the building; a renderer does the
visual check.

```bash
pip install python-pptx PyMuPDF
```

For the visual check you also need one of:

| Platform | Preferred | Fallback |
|---|---|---|
| macOS | Microsoft PowerPoint | LibreOffice |
| Windows | Microsoft PowerPoint | LibreOffice |
| Linux | LibreOffice | none |

PowerPoint wins where it exists, because it is what the audience opens the file
in, so font substitution and text fit are truthful. LibreOffice substitutes the
Gjensidige fonts, so its text-fit check is approximate. Leave slack in tight
boxes when that is all you have.

## Step 1: Get the template

No template file ships with this skill, deliberately. It is an internal asset of
20 MB or more that gets revised, and a checked-in copy goes stale fast.

Use any recent Gjensidige presentation as the source. Find one:

```bash
# macOS
mdfind "kind:presentation" | grep -iv node_modules | head

# Linux
find ~ -name '*.pptx' -not -path '*/node_modules/*' 2>/dev/null | head

# Windows (PowerShell)
Get-ChildItem $HOME -Recurse -Include *.pptx -ErrorAction SilentlyContinue |
  Select-Object -First 20 FullName
```

If the user has none, ask for one. Any deck built on the template works, because
only the masters get used and the content is discarded.

## Step 2: Audit the template

Run this first, every time. **Layout indices are not stable across template
revisions**, so an index you have not just read is a guess.

```bash
python scripts/audit_template.py source.pptx                     # theme colours + all layouts
python scripts/audit_template.py source.pptx --layout 0 14 21    # placeholders for specific ones
```

The "Gjensidige 2022" template carries around 90 layouts on master 0. The ones
worth knowing, and their placeholders, are in `references/layouts.md`. Read that
before choosing a layout so you are not guessing at idx numbers.

## Step 3: Build

Write a build script that imports the helpers. Each one exists because the naive
python-pptx call produces a visible defect.

```python
import sys; sys.path.insert(0, "scripts")
from gjensidige_deck import *

prs, master = open_template("source.pptx")
drop_all_slides(prs)                    # keep the masters, discard the content

s = add(prs, master, 14)                # "Title and Content"
set_text(ph(s, 13), "KICKER")           # small label above the title
set_text(ph(s, 0), "The slide title")
fill_body(ph(s, 1), [
    ("lead",  "Intro prose that takes no bullet."),
    ("label", "A section"),
    ("item",  "A point"),
    ("item",  "Another point"),
])
set_text(ph(s, 14), "Footnote, bottom left")
s.notes_slide.notes_text_frame.text = "Speaker notes."

prs.save("out.pptx")
```

Rules that hold for every layout:

- **Never assign `text_frame.text`.** It collapses the paragraph into one unstyled
  run and loses the template font. `set_text` and `fill_body` write runs instead.
- **Delete placeholders you do not fill** with `drop(s, idx)`, or they print their
  prompt text ("Click to add text") in the finished deck.
- **Do not set font names.** Placeholders inherit Gjensidige Display and Gjensidige
  Type from the theme. Setting Calibri destroys the one thing you came for.
- **Colours:** use the constants in `gjensidige_deck.py`. `LBLUE`, `CORAL` and
  `YELLOW` are decorative and too weak as text on a light fill. Keep text on `DARK`
  or `WHITE`.
- **No accent stripes.** Coloured edge bars above cards read as AI-generated filler.
  Use the template's own surfaces.

## Step 4: Check it visually

Never hand over a deck you have not looked at. The first render almost always has
a real defect.

```bash
python "$PPTX_DIR/scripts/office/validate.py" out.pptx --original source.pptx
python scripts/render_qa.py out.pptx
```

`PPTX_DIR` comes from the dependency step above.

`--original` is required for template-derived decks. The template has schema errors
of its own, and without a baseline your own drown in them.

Look at **every** image, hunting for these in order:

1. Text overflowing a box or running off the slide.
2. Overlapping elements, typically a title that wrapped to two lines and pushed
   down into the content below.
3. Dead space inside cards, which means the text is vertically centred where it
   should sit at the top.
4. Bullets appearing on the first item only.
5. Leftover placeholder prompt text.

`markitdown out.pptx | grep -iE "click to|klikk for|lorem|TODO"` catches the last
one without eyes.

**PowerPoint exports its cached copy.** Leave the deck open and the PDF comes out
stale, so the QA pass reviews the previous build. The cache is per presentation,
so `render_qa.py` closes that one deck before opening it again, discarding its
unsaved in-memory copy. Everything else the user has open stays open, and
PowerPoint is only quit if the script was what started it. Close the deck the
same way if you export by hand, and leave the rest of the user's work alone.

## Step 5: Hand it over

Put the file where the user will find it, and open it:

```bash
# macOS
open -R "deck.pptx" && open -a "Microsoft PowerPoint" "deck.pptx"

# Windows (PowerShell)
explorer /select,"deck.pptx"; Start-Process "deck.pptx"

# Linux
xdg-open "deck.pptx"
```

## Demo

`assets/demo/build_demo.py` builds a demo deck covering the patterns: cover page,
three columns, two columns, a recommendation page with cards, a table, and a phase
sequence. Run it against your own template source and look at the result before
building anything of your own:

```bash
python assets/demo/build_demo.py source.pptx demo.pptx
python scripts/render_qa.py demo.pptx
```

Neither the deck nor its screenshots are checked in. Both embed the whole template
and go stale on the next revision, so they get generated locally.
