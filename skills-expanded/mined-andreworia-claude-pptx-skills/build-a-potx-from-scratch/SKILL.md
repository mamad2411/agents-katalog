---
name: build-a-potx-from-scratch
description: Constructs a corporate .potx from nothing — slide master, layout set, theme colour and font schemes, placeholders — so decks built on it inherit the brand automatically. Not for fixing a deck against a template that already exists.
---

# Build a .potx From Scratch

## When to use

Use this skill when there is no corporate template, or when the existing one is beyond repair — twelve masters, sixty layouts, hard-coded colours, nobody remembers who built it. Also use it when a brand refresh means rebuilding rather than recolouring. Do not use it to bring a deck onto a template that already exists; that is `master-and-layout-mapper` and `reskin-to-template-converter`.

## What it does

It builds the template in dependency order — theme, then master, then layouts, then defaults — so each layer inherits from the one below and a future re-theme actually propagates. The output is a `.potx` plus a short specification of what each layout is for.

## Method

**1. Know what you are producing.** Three file types get confused:

- **`.potx`** — a template: slide master, layouts, theme, default content. New decks are created *from* it.
- **`.thmx`** — a theme only: colours, fonts, effects. No masters, no layouts, so applying one recolours a deck without restructuring it.
- **`.pptx`** — a presentation. A "template" circulated as a `.pptx` for people to copy and strip is not a template; it is a habit, and it is where brand drift starts.

Build the `.potx`, then export a `.thmx` from it (`Design > Themes > Save Current Theme`) so the palette reaches Word and Excel.

**2. Set the slide size first.** `Design > Slide Size > Custom Slide Size`. Widescreen 13.333 x 7.5 in is the modern default; A4 Paper (10.833 x 7.5 in) if the firm's output is printed documents. Changing it later rescales every layout you have built. See `pptx-export-and-pdf`.

**3. Build the colour scheme.** `Slide Master > Colors > Customize Colors`. A theme has exactly twelve slots — Text/Background Dark 1, Light 1, Dark 2, Light 2, Accent 1 to 6, Hyperlink and Followed Hyperlink — stored in `ppt/theme/theme1.xml` as `<a:clrScheme>` under the keys `dk1`, `lt1`, `dk2`, `lt2`, `accent1`–`accent6`, `hlink`, `folHlink`.

- Dark 1 and Light 1 are the primary text and background pair. Leave them near-black and near-white unless the brand genuinely is not.
- Accent 1 is the primary brand colour: every default shape, chart series and SmartArt node picks it up first.
- Fill all six accents in the order charts should use them. Chart series step through Accent 1 to 6 in sequence, so accent order *is* the chart palette.
- Set Hyperlink and Followed Hyperlink to brand colours. They are the slots everyone forgets, and default blue-purple links are the commonest brand defect in the wild.

Tints and shades of each slot are generated automatically and also move with the theme — that is the top row in every colour picker. Anything taken from the *Standard Colors* row below it will never re-theme.

**4. Build the font scheme.** `Slide Master > Fonts > Customize Fonts` sets heading (major) and body (minor). Each carries a Latin, East Asian and complex-script face in `<a:majorFont>` and `<a:minorFont>`, so a firm with CJK or Arabic output must fill those or the substitution is silent. Check `font-embedding-and-fallbacks` before committing to a foundry face.

**5. Build the master, and put only universal things on it.** `View > Slide Master`: the top thumbnail is the master, everything indented below is a layout. Whatever sits on the master appears on every layout that does not hide background graphics. So the master carries the background, the logo in its standing position, the footer, date and slide-number placeholders, and the type styles for title and the five body levels — sizes, colours, spacing, bullets, indents. Nothing that varies by layout belongs here. `Slide Master > Master Layout` controls which of title, text, date, slide number and footer exist.

**6. Build the layout set — eight to twelve, no more.** Every extra layout is a maintenance liability and an invitation to pick the wrong one. A working set: Title · Section Divider · Title and Content · Two Content · Comparison · Content with Caption · Full-bleed Image · Table · Chart · Quote · Closing.

For each, use `Slide Master > Insert Layout`, then `Insert Placeholder` for Content, Text, Picture, Chart, Table or Media, then **rename it** (`Slide Master > Rename`) to something recognisable in the Layout gallery — "Two Content — 50/50" beats "Custom Layout 7".

Two structural points decide whether inheritance works:

- Placeholders are what make a layout a layout. A text box drawn on a layout is decoration; only a real placeholder passes formatting to slides and appears in the outline. In the file they are `<p:ph type="..."/>` — `title`, `ctrTitle`, `subTitle`, `body`, `pic`, `chart`, `tbl`, `dt`, `ftr`, `sldNum`.
- Body and content placeholders inherit by `idx`, not by position. If a slide's placeholder index does not match the layout's, the slide silently loses the layout's formatting — which is why a copied slide sometimes ignores the template despite sitting on the right layout. Rebuild it rather than nudging it.

Use **Hide Background Graphics** on layouts that should not show the master's furniture — a full-bleed image, a dark divider — and flip the colour map on a dark master rather than recolouring text by hand.

**7. Set the defaults a user hits first.** Style a text box to the body font, right-click, **Set as Default Text Box**; likewise **Set as Default Shape** and **Set as Default Line**. These are stored in the file, so every shape a user inserts arrives on-brand. Add guides in master view (`View > Guides`, Alt-drag) at the margins and columns; they save with the file.

**8. Delete everything you did not build.** Remove the stock Office layouts you are not using and any second master. An unused master normally disappears on its own unless someone right-clicked **Preserve Master**, so check nothing survives pinned (a pin icon marks it).

**9. Save as `.potx` and test it properly.** `File > Save As`, file type **PowerPoint Template (*.potx)**; on Windows it defaults to the *Custom Office Templates* folder and then appears under `File > New > Personal`. Test by building a real 20-slide deck on it: every layout with real content, a chart picking up accents 1–3 in order, hyperlink colour, and a swap to a different theme colour set and back. Anything that does not move is hard-coded.

## Inputs

- Brand guidelines: palette hex values, typefaces, logo files, clear-space rules.
- The output the firm actually produces: screen, printed document, or both.
- The layout set the work genuinely needs, and any non-Latin script requirement.
- Font licensing.

## Output format

- The `.potx`, and a `.thmx` exported from it.
- The colour scheme as a twelve-slot table: slot, hex, purpose.
- The font scheme, per script.
- The layout list: name, purpose, placeholders carried.
- Defaults set, guides placed, layouts deleted.
- The test result, including the theme-swap check.

## Example

Input: a 40-person advisory firm with a brand book, a logo suite, no template, and decks built by copying last year's.

Output:

- Slide size: Widescreen 13.333 x 7.5 in.
- Colours: Dark 1 `#12161C`, Light 1 `#FFFFFF`, Dark 2 `#3A424E`, Light 2 `#F2F4F7`, Accent 1 `#1B4DB1`, Accents 2–6 in chart order, Hyperlink `#1B4DB1`, Followed `#5A3E8E`.
- Fonts: the licensed brand sans for both; East Asian slots set to a distributable fallback.
- Master: logo bottom-right, footer and slide number on, title 28 pt, body levels 18/16/14/12/12 pt.
- Layouts: 10, renamed. Full-bleed Image and Section Divider hide background graphics and flip the colour map.
- Defaults set; guides at 0.6 in margins on a 12-column grid. Deleted 9 stock layouts and one pinned master.
- Test: 20-slide deck built; the theme-swap check found two hard-coded greys on the Table layout, rebound to Light 2.
