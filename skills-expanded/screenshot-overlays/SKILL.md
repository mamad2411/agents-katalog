---
name: screenshot-overlays
description: Use when two screenshots of the same screen each show a different transient overlay (a hover tooltip, a popover, a hover toolbar, an open menu) and one image has to show both. Also when someone says "combine these two screenshots", "put both tooltips in one image", "align these and merge the difference", or hands over two captures that are a few pixels apart. Aligns the captures on the pixels they share, numbers every component where they differ, and pastes the picked overlay along its own outline. Refuses when the captures do not line up, such as a different zoom. On a list, a table or a sparse page it can propose an offset one row off without a warning, so the workflow checks which item the pasted overlay points at. Not for stitching a scrolling capture into one long image, and not for visual regression diffs.
license: Apache-2.0
compatibility: Requires Python 3.11+ with numpy 2.3.4 and Pillow 12.3.0 in a virtual environment. Reads PNG and JPEG only. No network, no account. Agent-agnostic, but the agent has to be able to look at an image.
metadata:
  version: "0.1.0"
  changeSummary: First release. Aligns two captures, lists their differences on a numbered contact sheet, and merges the picked overlay by its outline. On repeating or sparse screens the offset can be a row alias that stderr does not report; the workflow checks the pasted overlay against the hovered item, and --anchor or --offset corrects it. Built from one real dark-theme job; the current version is tested on invented dark and light scenes only.
  isBreaking: "false"
---

# Screenshot overlays: two hover states in one image

A tooltip shows only while the pointer rests on its target, so one screenshot holds one tooltip. To
show two, you take two captures and combine them. The captures rarely line up: the window moved, or
the crop started a few pixels further along. A paste by eye then leaves a seam or a doubled line of
text.

This skill does the three parts that go wrong by hand:

1. **Align.** It finds the offset from the text and icons the captures share, and trusts it only
   when tiles across the image agree. An overlay in one capture only makes its own tiles disagree.
2. **List.** It numbers every component, a region where the aligned captures differ, and draws the
   numbers on a contact sheet. You look at the sheet and pick.
3. **Merge.** It cuts the picked overlay out along its outline, arrow included, and pastes it into
   the other capture. It does not copy a faint hover tint around the overlay, except in a one-pixel
   ring at its edge.

![Three panels of an invented dark chat screen. BASE shows an "Open in thread" tooltip over row 4. DONOR is shifted a few pixels, shows a "Copy link" tooltip pointing at row 2, which a hover highlight tints. The merged panel shows both tooltips on BASE, without the tint from DONOR](../../docs/assets/screenshot-overlays-example.png)

The picture is in the repository's `docs/assets/`, so this folder stays text-only.
`scripts/make_illustration.py` draws it from the same invented scene the selftest uses.

## Install

Run these commands from this skill's folder, the one that holds this file.

```bash
python3 -m venv ~/.local/share/screenshot-overlays/venv
~/.local/share/screenshot-overlays/venv/bin/pip install numpy==2.3.4 pillow==12.3.0
PY=~/.local/share/screenshot-overlays/venv/bin/python
"$PY" scripts/overlays.py --selftest      # 123 checks, all must pass
```

On Windows, use `py -3.11 -m venv venv` in a folder you choose. The interpreter is then
`venv\Scripts\python.exe` in that folder.

## Workflow

Choose the BASE: the capture that the result shows everywhere except the pasted overlays. The other
capture is the DONOR. Every coordinate in the output is a BASE pixel. Use PNG captures from one
display, at one scroll position.

1. Write down which row or item the pointer hovers in each capture, for example "BASE: the tooltip
   on INV-1043, DONOR: the card for Alex". When rows have no unique label, write the position, such
   as "the 4th row below the heading Invoices". Ask the person if you did not take the captures.
   On a repeating screen the pixels can fit a row alias as well as the truth, and this note cannot:
   step 6 checks against it.
2. List the components, with a numbered contact sheet:

   ```bash
   "$PY" scripts/overlays.py list base.png donor.png --sheet sheet.png
   ```

   The JSON line gives the offset `dx`, `dy`, the `residual`, `rival` and `changed` (see below), and
   one entry per component with its box. The sheet shows BASE on the left and the DONOR moved into
   BASE coordinates on the right, with the same numbered boxes on both.
3. Look at the sheet. The offset is a proposal, not a fact: on a list, a table or a sparse page it
   can be a row alias, which lays the DONOR one or more rows off. Suspect one when the DONOR's
   overlay has no number, when boxes sit on the digits or dates of one column, or when the sheet
   shows no box at all. A `rival` or a stderr warning also says to suspect one. A null `rival` does
   not prove the offset right. To correct the offset, or after a refusal, rerun `list` with one of
   these:
   - `--anchor X0,Y0,X1,Y1`: align on that part of BASE only. Choose a part with text that appears
     once, such as a heading, a line-number gutter or a column of ids, and keep everything that
     repeats or any overlay of either capture out of the box. A box that holds an overlay gives a
     wrong offset without a warning. An anchored offset has no `rival`. Its `changed` and
     `residual` warnings can still fire when a big overlay moved. Step 6 decides.
   - `--offset=DX,DY`: use the `rival`, or another offset you have a reason for. The same trust
     rule applies to it.

   If no anchor is accepted and no offset passes step 6, stop. Do not deliver a merge. Ask for new
   captures with the pointer on the same row, or with a heading or a gutter inside both.
4. Pick each component whose overlay is in the DONOR panel. Do not pick a component whose overlay
   is in the BASE panel. The merge would replace that overlay with the DONOR's plain background.
5. Merge, with a proof:

   ```bash
   "$PY" scripts/overlays.py merge base.png donor.png --pick 1 --out merged.png --proof proof.png
   ```

   For a box that `list` did not separate, give it yourself with `--region X0,Y0,X1,Y1`. Pass the
   same `--edge`, `--max-shift`, `--anchor` and `--offset` to `merge` as to `list`, or the numbers
   can change.
6. Check each pasted overlay in `proof.png`. For each pasted box it shows three bands at full width
   and full size: the DONOR as captured, BASE as captured, and the result. Read the row label, name
   or id beside the overlay in the DONOR band and in the BASE band, at the same x. Both must name
   the same item, and it must be the DONOR item from step 1. Read the BASE band, not the result: a
   paste can carry the DONOR's own label along. If they differ, the offset is a row alias: go back
   to step 3. If the bands show no label that tells the rows apart, count rows from a landmark in
   `merged.png` and compare with your note. When even that is not possible, stop as step 3 says.
   At the true offset some things also differ between the DONOR and BASE bands: the BASE's own
   overlay, the DONOR's pointer, hover toolbar and tint, values that updated between the
   captures, and magenta where the DONOR ends. A wide band can be too large for an image reader at
   full size: crop it before you read it.
7. Look at `merged.png`, zoomed in on every pasted box. The script reads the file back and compares
   it with what it wrote, but it cannot see whether the result is what was wanted.

`align` alone prints only the offset, for when you want to do the compositing in another tool.

## What the numbers mean

- **`dx`, `dy`**: BASE(x, y) shows what DONOR(x + dx, y + dy) shows. The search covers 96 pixels in
  each direction (`--max-shift`, up to 512). The offset is trusted only when at least 6 tiles that
  hold text or icons agree at it, and those tiles span at least a third of the overlap's width or
  height. A tile is 48 by 48 pixels, smaller on a narrow image or anchor. Otherwise the script
  refuses with exit 1. It also refuses when the best
  offset lies beyond `--max-shift` (it searches twice as far to find out, and names the value to
  rerun with), and when a second offset more than 4 pixels away fits almost as well: the content
  repeats, or an overlay covers most of the capture.
- **`rival`**: a second offset that may be the true one, or null. On a repeating screen with an
  overlay on a different row in each capture, the chosen offset can be the row alias that lays one
  overlay onto the other. A big overlay can also decide the offset on its own. Three tests set it:
  - BASE repeats itself: moved by some step of up to twice `--max-shift`, at least 45 percent of
    its textured tiles stay clean. A tile that holds only a straight line, such as an input border
    or a ruled row, does not count.
  - At least 3 small changes sit evenly spaced in one column or one row: the trace that a row
    alias leaves on digits that change from row to row.
  - `changed` is at least 0.12. Then the `rival` is the offset of what the chosen one leaves
    unexplained, such as the page behind a big popover.

  For the first two, the `rival` is the alias inside `--max-shift` that fits the pair best. It is a
  weak hint. On list-like screens it appears on most correct offsets, some wrong offsets come
  without it, and it can name another alias instead of the truth. See the rates under How it works.
  The note from step 1 is the check.
- **`changed`**: the share of the overlap that lies within 6 pixels of a difference after
  alignment. Correct pairs with tooltip-sized overlays measured 0.074 or less on the invented
  scenes, and a correct pair with a menu over half the screen 0.19 to 0.61. At 0.12 or more stderr
  warns: a big overlay may have decided the offset, or a fine texture may hide an offset that is 1
  pixel off, which the reduced sheet cannot show. Compare a crop at full size.
- **`residual`**: the share of those detailed tiles that disagree at the offset. A hover tint moves
  no edge, so it does not count, and neither does a change of color alone. Measured on invented
  scenes: a matching pair with two tooltips 0.24, a pane of other content over 57 percent 0.47, a
  menu over 50 percent of it 0.76, the same layout with other text 0.72 to 0.78. Above 0.4 the
  script warns: a big overlay and another screen state look the same to it, and only the contact
  sheet tells them apart.
- **`solid`**, per pasted box: the share of the paste's bounding box that either differs or lies
  inside an outline. The invented tooltips measured 0.73 (outlined) and 0.84 (a solid bubble), and a
  line of text with no outline 0.34 to 0.38. Below 0.6 the script warns on stderr, because it pasted
  thin strokes only: the text, but not the background behind it. Rerun with `--rect` to paste the
  whole box. When `--rect` is refused because the box reaches past what the DONOR covers, give
  `--region` with a box that stays inside it.

## Gotchas

- **Two captures at different scales do not align.** A capture from a high-density display is often
  twice the size of one from another display. On the invented scenes the script refused every scale
  change it was given, from 1 percent to 2x. That is a measurement, not a guarantee: take both
  captures on one display.
- **Repeating rows need a look.** A list whose rows are identical fits at every multiple of the row
  height, and the script refuses. A table whose rows differ only in a number, a date or an ID, with
  the overlay on a different row in each capture, can align on a row alias, often with a `rival`
  and not always. On dense rows the changed digits can join into one tall box instead of a column
  of small ones. Capture both with the pointer on the same row if you can, or keep a unique part of
  the screen, such as a heading or a line-number gutter, inside both. Step 6 of the Workflow
  catches the alias, and `--anchor` on that unique part corrects it.
- **A big overlay can decide the offset.** When an overlay carries more text than the screen
  behind it, the overlays are what lines up. A popover of 600 by 500 pixels over a page of 900 by
  700 did this, and so did a card of 460 by 200 shown at two places on a sparse page. On a dense
  page most of the screen then still differs, `changed` is high and the `rival` names the page's
  offset. On a sparse page it does not. A menu over 70 to 80 percent of an invented scene was
  refused. Capture more of the screen around a big overlay.
- **Tiles that differ only in color look alike.** Alignment uses edges, so a grid of swatches or
  thumbnails with the same layout and other colors can be refused as repeating content. Crop to a
  part with text.
- **A capture resized after it was taken may sit at a fractional offset.** The offset is a whole
  number of pixels. A 2x capture shared at 1x, or a display scaled by 125 percent, can leave a
  half-pixel seam around the paste. Use captures exactly as the screenshot tool saved them.
- **Not every component is an overlay.** An animated emoji, a blinking cursor, a spinner or a
  timestamp that changed between the captures also differ. They get their own numbers. Do not pick
  them.
- **The hover state comes with more than the tooltip.** The DONOR also has the pointer, an underlined
  link and often a toolbar. Each one is a separate component. Pick only what the image has to show.
  Two pointers in one image usually look wrong.
- **Two overlays close together get one number.** A BASE tooltip and a DONOR tooltip less than about
  12 pixels apart join into one component. If the sheet shows an overlay in both panels inside one
  box, first ask whether the two overlays sit on rows that look alike: then the offset may be a
  row alias, and step 3 applies. Otherwise do not pick that component. Give `--region` around the
  DONOR overlay only: a paste never leaves the box it is given.
- **A strong hover tint shows as a full-width component.** A pixel counts as different above 16
  levels in any channel (`--edge`). A tint stronger than that becomes a component the width of the
  screen. Rerun `list` and `merge` with an `--edge` above the tint, for example 30. The outline must
  then be stronger than the new value.
- **A JPEG adds noise.** Compression noise can exceed 16 levels, which joins an overlay with nearby
  text rows or leaves the paste hollow, worst on a dark theme with a faint outline. The script warns
  for a JPEG. Ask for PNG captures; a higher `--edge` helps only when the outline is strong. Other
  formats are refused, because Pillow would choose a decoder by content and some decoders run
  external programs.
- **Both captures must show the same scroll position.** The model is one offset for the whole image.
  If one pane scrolled and the sidebar did not, crop both captures to that pane first.
- **Two overlays at the same place cannot both show.** When the BASE and the DONOR each have an
  overlay over the same pixels, a pick replaces the BASE overlay with the DONOR one. Take a third
  capture with the pointer elsewhere.
- **Soft drop shadows end hard.** The mask takes a shadow only where it differs by more than
  `--edge`. On a light theme a wide shadow then ends on a visible edge. Use `--region` with `--rect`
  around the overlay and its shadow, and check the result.
- **Transparency is kept.** A capture with an alpha channel, such as a window with its shadow, keeps
  it in the output. A transparent shadow in only one capture shows as a component.
- **A one-pixel ring of DONOR background comes along.** The mask grows by one pixel to close the
  gaps that antialiasing leaves in a rounded outline. That ring carries the DONOR's background. On a
  tinted row this is a one-pixel line about 8 levels lighter.
- **The result shows a moment that never happened.** Two hovers from two moments sit in one frame.
  The output PNG carries a `Comment` text chunk that says it is a composite, names the pasted boxes,
  and records the offset, whether it was searched, anchored (with the box) or given with
  `--offset`, the `rival` and the `residual`. Say so when the image goes into a bug report or a
  record.

## How it works

Alignment has three steps.

1. FFT correlations of the two edge maps give the edge mismatch of every shift up to twice
   `--max-shift`, on a canvas padded so that no shift wraps around. The 16 lowest local minima are
   the candidates, each refined at full size within the factor by which the copy was reduced.
2. Each candidate is scored by its share of clean tiles: tiles where at most 5 percent of the edges
   are in one capture only. Edges that fall outside its overlap count as tiles that did not match.
   An overlay spoils a few tiles completely, and a wrong row on repeating content spoils many tiles
   a little. The highest score wins.
3. The winner is refused when it lies beyond `--max-shift`, when it fails the trust rule, or when
   another candidate more than 4 pixels away has almost the same clean share on its own overlap.
   Otherwise it gets a `rival` when one of the three tests under What the numbers mean fires.

Edges are taken per color channel over a mid-gray backdrop, so colors of equal brightness still
differ, colors under full transparency are ignored, and dark content on transparency keeps its
edges. An image over 2 megapixels is searched on a reduced copy, and every candidate offset and
repeat step is refined at full size. Over 8 megapixels the neighbours of a candidate are first
compared on the densest part of each quarter of the image, 2 megapixels in all, and only the best
one at full size. On an Apple-silicon laptop, `align` took 2 seconds at 3 megapixels, 3 seconds at
8, and 15 seconds with a peak of 3.7 GB at 40, the largest input it reads. Measured on invented
scenes:

- A sweep of 224 shifts up to 40 pixels: all exact.
- True shifts just past `--max-shift`: refused in 6 of 6.
- Chat lists with real text and a toolbar moved to another row: 23 of 24 exact with no `rival`, 1
  exact with one.
- Two look-alike tooltips on a varied screen: 24 of 24 exact with no `rival`.
- 1,377 adversarial pairs over 17 random seeds (numbered and dated tables, cards, identical chat
  rows, identical rows under a heading, each with the overlay on a different row in each capture):
  702 refused, 213 exact, 462 wrong, and 462 of 462 wrong offsets carried a `rival`.
- Rows with one badge, and icon strips, 36 pairs each: 26 and 26 wrong, all with a `rival`.
- A big popover over a page, moved 40 to 64 pixels: 6 of 6 wrong, all with a `rival`.
- Rows that differ only in a time and an id, with a profile card of up to 480 by 380 pixels on
  another row in each capture, 160 pairs: 73 wrong, 62 with a `rival` and **11 without**. In 42
  of 42 such pairs checked, the `rival` was the true offset.
- Captures of 3,600 by 2,300 pixels with rows of 68 to 112 pixels: 8 wrong, all with a `rival`.
- Realistic screens with varied content (spreadsheets, a code editor, a week calendar, settings,
  a file list, a kanban board), 112 pairs as PNG and JPEG at quality 75 and 90: 87 exact, 24
  refused, 1 wrong with a `rival`. 30 of the 87 exact offsets carried a `rival` too.
- A second realistic set (calendars, editors, kanban, settings, spreadsheets, file lists,
  dashboards, galleries, menus, live tables; PNG, JPEG and alpha), 234 pairs: 190 exact, 41
  refused, 3 wrong. **102 of the 190 exact offsets carried a `rival`**, among them every file list,
  settings page and dashboard whose numbers updated between the captures.
- **Known misses.** A sparse page with the same card of up to 520 by 280 pixels at two places, 240
  pairs: 88 wrong, 1 with a `rival`, 31 with an empty stderr. A code editor cropped without its
  line-number gutter, with a popover on another line: 20 wrong, none with a `rival`, 4 with an
  empty stderr, some with no component on the sheet.

These are measurements on invented scenes, not a guarantee. The known misses are why step 6 of the
Workflow checks every pasted overlay against the hovered item. A reviewer measured `--anchor` on
them: a heading recovered 28 of 28 refused sparse pages, a column of ids 44 of 44 refused card
pairs, and 17 of 17 pairs with live values or a timestamp tooltip. On a ruled table a tight box
around the ids recovered 3 of 3 row aliases; a box across a whole row is refused, because every
row fits it. A code editor cropped without
its gutter and a list of identical rows had no part to anchor on: step 3 stops there.

A component is a connected region of differing pixels, grown by 6 pixels so that the letters of one
tooltip join. Components whose boxes overlap are merged, so a tooltip's outline and its text get one
number.

The mask for a picked box comes from a flood fill from the edge of the box through every pixel that
does not differ. What the flood cannot reach is the overlay: its outline, its arrow and everything
they enclose. That is why the paste follows a rounded corner and an arrow, and why a hover tint
outside the outline is not copied.

## Exit codes

`0` done, `1` refused (nothing written), `2` usage or unreadable input, `3` dependency missing,
`4` selftest failed, `5` internal error (a crash, with its traceback on stderr; never a refusal).
A result is written to a temporary file, read back and only then moved into place, so a refusal
leaves no file behind.

## Prior art (checked 2026-10-19)

Aligning two near-identical images is a solved step on its own. Photoshop's Auto-Align Layers,
Hugin's `align_image_stack`, phase correlation in OpenCV and scikit-image, and ImageMagick's
`compare -subimage-search` all find an offset. OpenCV's `phaseCorrelate` also returns a peak
response, and scikit-image's `phase_cross_correlation` an error value, which say how sharp the
match is. None of them checks the offset tile by tile, names a row alias, or cuts an overlay out
along its outline.

- [`nocoo/image-stitch`](https://github.com/nocoo/image-stitch) stitches a sequence of scrolling
  screenshots into one long image with ORB feature matching. Use it for a page taller than the
  screen. It places whole images on a canvas and does not move a region from one capture into
  another.
- [`software-mansion/argent`](https://github.com/software-mansion/argent) ships a screenshot diff
  skill for visual regression: a baseline against a new capture, with the differences reported. Use
  it to find what changed. It does not composite.
- ImageMagick `-append` and `-composite` join or layer images at positions you supply.

What this skill adds is the step after the offset: it numbers the differences for a person to pick,
pastes the picked overlay along its outline without the tint around it, and refuses a pair that does
not line up. Nothing was copied from the projects above.
