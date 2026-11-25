---
name: pptx-export-and-pdf
description: Converts slide size and aspect ratio and exports a deck to PDF, image, or video with the settings that survive the trip. Not for designing the slides themselves.
---

# PowerPoint Export and PDF

## When to use

Use this skill when a deck has to change shape or leave PowerPoint. Typical triggers: a 4:3 deck has to become 16:9 for a screen, a 16:9 deck has to print on A4, the client wants a PDF and the PDF came back with wrong fonts or fuzzy text, or the deck has to ship as images or video. Do not use it for layout or brand fixes; run `grid-margin-safe-zone-alignment` and `brand-compliance-auditor` after the size change, because a conversion moves everything.

## What it does

It sets the slide geometry once, deliberately, then names the exact export settings for the destination and lists what each conversion breaks. The output is a size decision, an export recipe, and a repair list.

## Method

**1. Fix the geometry before anything else.** Slide size is a document-level property, so change it once, at the start, never per slide. `Design > Slide Size > Custom Slide Size`. The built-in presets:

| Preset | Inches | Ratio |
|:--|:--|:--|
| Widescreen | 13.333 x 7.5 | 16:9 |
| On-screen Show (16:9) | 10 x 5.625 | 16:9 |
| On-screen Show (4:3) | 10 x 7.5 | 4:3 |
| A4 Paper (210x297mm) | 10.833 x 7.5 | ~1.44:1 |
| Letter Paper | 10 x 7.5 | 4:3 |

Two different 16:9 presets exist. They are the same ratio at different scales, and a deck built at 10 x 5.625 will not merge cleanly with one built at 13.333 x 7.5 — slides pasted across get rescaled and the type ends up in two sizes. Pick the one the corporate template uses and record it.

Inside the file this is one element in `ppt/presentation.xml`: `<p:sldSz cx="12192000" cy="6858000"/>` for 13.333 x 7.5 in. The unit is the English Metric Unit — 914,400 EMU to the inch, 360,000 to the centimetre, 12,700 to the point. If a tool reports geometry in EMU, divide by 914,400 to get inches.

**2. Choose Maximize or Ensure Fit on purpose.** When you enlarge the canvas (4:3 to 16:9) PowerPoint asks which you want. *Ensure Fit* scales content to fit and leaves empty space at the sides; *Maximize* fills the width and pushes content off the top and bottom edges. Ensure Fit is the right default for 4:3 to 16:9 because nothing is lost. Maximize is only safe on decks that are genuinely full-bleed.

**3. Repair what the conversion moves.** Neither option reflows a layout intelligently. Walk the deck for:

- **Full-bleed images.** They will letterbox or crop badly. Re-crop against the new frame; never stretch to fit, which distorts faces and logos.
- **Explicit type sizes.** Do not assume point sizes came across at the intended value. Re-check headings and body against the template's type scale (`theme-font-and-type-scale-enforcer`) rather than eyeballing them.
- **Autofit text.** Placeholders carrying `<a:normAutofit fontScale="..."/>` re-shrink at the new width, so identical-looking headings end up at different effective sizes. Turn autofit off in the affected placeholders and set the size explicitly.
- **Grouped shapes.** Groups scale as a unit, so line weights and text inside them go out of proportion. Ungroup, fix, regroup.
- **Master background graphics.** Anything anchored to a master edge needs re-anchoring.

**4. Export to PDF with the right options.** On Windows, `File > Export > Create PDF/XPS` (or `Save As`, type PDF), then click **Options**:

- **Publish what** — Slides, Handouts (with slides-per-page), Notes Pages, or Outline View. Notes Pages is how you ship a speaker script; see `speaker-notes-and-handouts`.
- **Document structure tags for accessibility** — leave this **on**. It is what makes the PDF readable by a screen reader, and clearing it saves a trivial amount of size.
- **ISO 19005-1 compliant (PDF/A)** — only when an archive or a regulator asks for it. PDF/A restricts what the file may contain, so re-open and inspect transparency, shadows and blend effects afterwards.
- **Bitmap text when fonts may not be embedded** — on, the PDF rasterises text it cannot embed so it *looks* right but is not selectable or searchable; off, the text stays real but may be substituted. Choose deliberately, and prefer fixing the font problem instead (`font-embedding-and-fallbacks`).
- **Optimize for: Standard** for anything printed; **Minimum size** only for email.

On macOS the options are fewer. `File > Save As`, format PDF, gives a choice between *best for electronic distribution and accessibility* and *best for printing*; take the first when the PDF must be tagged. Printing to PDF through the macOS print dialog produces an untagged PDF — avoid it for anything that has an accessibility requirement.

**5. Export to images.** `File > Save As` (or `Export`), choose PNG or JPEG; PowerPoint asks *All Slides* or *Just This One* and writes a folder next to the file. PNG for anything with text or flat colour, JPEG only for photographs. The default export resolution on Windows is low (96 ppi), which is why exported slides look soft in a document; raising it needs a registry change, so it is usually easier to export a PDF and rasterise that at the resolution you need.

**6. Export to video.** `File > Export > Create a Video`. Resolutions: Ultra HD 4K (3840x2160, Windows 10 and later only), Full HD 1080p (1920x1080), HD 720p (1280x720), Standard 480p (852x480). It uses recorded timings and narration if present, otherwise a fixed seconds-per-slide value. Animations render; embedded video re-encodes and gets softer, so keep the source file if quality matters.

**7. Verify on a machine that is not yours.** Open the export on a second device and check page count, fonts and page order. Most export defects are invisible on the machine that made them.

## Inputs

- The deck, and its current slide size.
- The destination: screen, print (and paper size), PDF for review, images, or video.
- Whether the PDF must be tagged, archival (PDF/A), or both.
- The corporate template's slide size, if there is one.

## Output format

- The target slide size in inches and the preset name.
- Maximize or Ensure Fit, with the reason.
- A repair list: slide numbers and what needs re-cropping, re-anchoring or re-typing.
- The export recipe: menu path, Publish what, and each option set on or off.
- The verification step performed.

## Example

Input: a 47-slide 4:3 board pack that must be shown on a 16:9 screen and circulated as a tagged PDF with speaker notes.

Output:

- Size: Widescreen, 13.333 x 7.5 in, matching the corporate template. Ensure Fit.
- Repairs: slides 1 and 12 are full-bleed images, re-crop to the new frame; slides 4, 9, 22 use autofit titles, disable autofit and set 28 pt; the divider group on slides 5, 18, 31 needs ungrouping to restore the 1 pt rule.
- PDF: `File > Export > Create PDF/XPS > Options`, Publish what = Slides, structure tags on, Bitmap text off, PDF/A off, Optimize for Standard. A second pass with Publish what = Notes Pages for the speaker copy.
- Verified: opened on a Windows laptop, 47 pages, brand font intact, tag tree present.
