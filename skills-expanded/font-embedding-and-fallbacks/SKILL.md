---
name: font-embedding-and-fallbacks
description: Embeds the brand fonts in a .pptx and sets a fallback stack so the deck does not reflow on a machine that lacks them. Not for choosing the typefaces or the type scale.
---

# Font Embedding and Fallbacks

## When to use

Use this skill when a deck looks right on the machine it was built on and wrong somewhere else: titles wrapping onto a second line, text overflowing its box, tracking suddenly loose, or a licensed brand font silently replaced by Calibri or Times. Also use it before any deck leaves the building — client, printer, conference AV desk. Do not use it to pick fonts or sizes; `theme-font-and-type-scale-enforcer` does that, and this skill assumes the typefaces are already agreed.

## What it does

It decides whether to embed, substitute, or outline the fonts, applies the chosen route, and records a documented fallback so the failure is predictable instead of random. The output is an embedding decision per typeface plus a fallback stack written into the theme.

## Method

**1. Understand why the deck reflows.** PowerPoint stores a typeface *name*, not the typeface. On a machine without that font installed, the operating system substitutes another one. Different fonts have different advance widths, so text that fitted on one line now takes two, a placeholder overflows, and a carefully aligned slide breaks. Nothing is corrupt; the file simply never carried the font.

**2. Inventory what the deck actually uses.** Two sources, and they disagree more often than people expect:

- The theme's major (heading) and minor (body) fonts, in `ppt/theme/theme1.xml` under `<a:majorFont>` and `<a:minorFont>`. Each carries a `latin`, `ea` (East Asian) and `cs` (complex script) typeface — a deck with CJK or Arabic content resolves through the `ea`/`cs` entries, not the Latin one.
- Direct overrides applied to individual runs, which bypass the theme entirely. These are the ones that surprise people, because the theme looks clean.

On Windows, `Home > Replace > Replace Fonts` lists every font name actually referenced in the file. That list, not the theme, is the inventory.

**3. Check that each font may legally be embedded.** Fonts carry an embedding permission set by the foundry, exposed as four levels: **Non-embeddable** (restricted licence), **Preview/Print** (the reader can view and print but not edit the text), **Editable**, and **Installable**. PowerPoint honours these. A restricted font will refuse to embed and warn you on save; a Preview/Print font will embed but leave recipients unable to edit that text. Check the licence before promising a client an editable deck in a commercial typeface — many foundry desktop licences do not include document embedding at all.

Format matters too. Embed OpenType (`.otf`) or TrueType (`.ttf`). PostScript Type 1 (`.pfb`/`.pfm`) cannot be embedded; if the brand font is only supplied as Type 1, obtain the OpenType cut or accept substitution.

**4. Embed.** On Windows: `File > Options > Save`, then under *Preserve fidelity when sharing this presentation* tick **Embed fonts in the file**, and choose between:

- **Embed only the characters used in the presentation** — smaller file, but recipients cannot type new characters in that font. Right for a final, read-only deck.
- **Embed all characters (best for editing by other people)** — larger file, fully editable downstream. Right for a template or anything a client will edit.

On macOS the feature exists in Microsoft 365 for Mac, PowerPoint 2024 for Mac and PowerPoint 2021 for Mac, under `PowerPoint > Settings (Preferences) > Save`, with the same two options. Older Mac builds cannot embed. Because Mac support arrived late and has historically been the weaker path, treat a Mac-produced deck as needing an explicit check rather than assuming embedding worked.

The setting is per-file and applies on save, so tick it and then save — it does not retro-embed a file you only opened.

**5. Verify the embed actually happened.** File size is the first tell: embedding a full-character weight typically adds hundreds of kilobytes per weight. To confirm properly, copy the file, rename the copy to `.zip`, open it, and look for a `ppt/fonts/` folder containing `.fntdata` parts — one per embedded weight and style — with a matching `<p:embeddedFontLst>` in `ppt/presentation.xml`. No folder, no embedding, whatever the checkbox says.

**6. Set a documented fallback for the cases embedding cannot cover.** Embedding fails on: restricted fonts, Google Slides and Keynote imports, PowerPoint for the web, and any recipient on an older build. So decide in advance what the deck degrades *to*, and set it as the theme font rather than leaving it to the OS. Metric-compatible pairs reflow least because their advance widths match:

| Brand font | Metric-compatible fallback |
|:--|:--|
| Calibri | Carlito |
| Cambria | Caladea |
| Arial / Helvetica | Liberation Sans |
| Times New Roman | Liberation Serif |
| Courier New | Liberation Mono |

Where no metric twin exists, pick the closest widely installed face with similar x-height and width — Arial or Helvetica for a geometric or neo-grotesque sans, Georgia for a transitional serif — and test it, because a fallback with a larger x-height will still overflow. Aptos is now the Microsoft 365 default and is not present on older installs, so a deck that depends on it needs the same treatment as any licensed font.

**7. Outline only as a last resort.** For a cover slide or a wordmark in a font that cannot be embedded, convert the text to shapes (`Format Shape > Merge Shapes > Union` on a duplicated text box, or supply a vector asset). Outlined text is pixel-perfect and permanently uneditable, unsearchable, and invisible to screen readers, so use it for a handful of display words, never for body copy.

**8. Test on a clean machine.** The only real proof is opening the deck where the font is not installed. Check the slides with the tightest titles and the longest bullets first.

## Inputs

- The deck, and the brand's heading and body typefaces.
- The font licence terms, or confirmation that embedding is permitted.
- Where the deck is going: PowerPoint desktop, web, Google Slides, Keynote, print.
- Whether recipients need to edit the text.

## Output format

- The font inventory: every typeface referenced, from theme and from direct overrides.
- Per font: embeddable yes/no, and at which permission level.
- The embed setting chosen (used characters vs all characters) and why.
- The fallback stack written into the theme.
- Verification: `ppt/fonts/` present, and the clean-machine test result.

## Example

Input: a 30-slide client deck set in a licensed foundry sans, produced on a Mac, going to a client who will edit it.

Output:

- Inventory: brand sans (headings and body, via theme), plus stray Calibri on slides 7 and 19 from pasted text.
- Licence: brand sans is Editable-embeddable; permitted under the firm's desktop licence.
- Embed: all characters, because the client will edit. `PowerPoint > Settings > Save`, saved, verified `ppt/fonts/` contains four `.fntdata` parts (regular, bold, italic, bold-italic).
- Stray Calibri rebound to the theme minor font.
- Fallback: theme minor font set with Arial as the documented substitute; longest title on slide 22 tested against it and shortened by two words so it holds one line either way.
- Clean-machine test: opened on a Windows laptop without the brand font; layout held.
