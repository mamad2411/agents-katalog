---
name: print-production-prepress
description: "Take artwork from screen to press: CMYK and spot colour, bleed and trim, overprint, imposition, PDF/X export and a printer checklist."
type: procedural
category: design
domain: design
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: intermediate
triggers:
  - prepare file for printing
  - pdf/x export
  - bleed and crop marks
  - cmyk conversion colour shift
  - prepress checklist
aliases:
  - prepress
  - print-production
keywords:
  - prepress
  - print-production
  - pdf-x
  - cmyk
  - bleed
  - imposition
  - rich-black
source: custom
enabled: true
---

# Print Production and Prepress

## Purpose

Take artwork from screen to press: CMYK and spot colour, bleed and trim, overprint, imposition, PDF/X export and a printer checklist.

## When to Use

- A file is going to a commercial printer, sign shop or packaging house.
- Colours must be predictable across substrates and presses.
- A print run came back with wrong margins, bands or washed-out colours.

## When NOT to Use

- The artefact is screen-only; RGB and sRGB are correct there.
- A single desktop inkjet print is all that is needed.
- The printer has supplied their own validated template — follow that instead.

## Capabilities

- Set document geometry: trim, bleed, safe area and slug.
- Convert to CMYK with a named profile and spot colours as separations.
- Export PDF/X-4 with fonts embedded and transparency flattened where required.
- Produce a preflight report a printer can act on.

## Inputs

- Page size, bleed (usually 3 mm) and fold or die-line geometry.
- The printer's profile, substrate and finishing (lamination, varnish, foil).
- Images at final resolution with their colour profiles.

## Workflow

1. Build to trim size plus bleed; extend every background element into the bleed.
2. Convert images to CMYK with the printer's profile and check total ink coverage limits (often 300%).
3. Use rich black only for large solids, never for body text.
4. Embed fonts or outline them, and confirm no text sits inside the safe area.
5. Export PDF/X-4, then preflight: fonts, resolution, bleed, colours, overprint.
6. Send a low-res proof and the preflight report with the file.

## Tools

- ghostscript
- qpdf
- imagemagick
- scribus
- acrobat-preflight

## Examples

- ``gs -sDEVICE=pdfwrite -dPDFX -dPDFSETTINGS=/prepress` produces a PDF/X-3 baseline; verify separations afterwards, never trust the exit code alone.`
- `A 3 mm bleed with crop marks at 5 mm offset survives trimming drift on a guillotine.`

## Safety

- Never convert colours twice — each CMYK round-trip loses gamut.
- Confirm the printer's profile before converting; a generic SWOP profile can shift brand reds.

## Source

All-Skills canonical library (`skills/design/print-production-prepress`). First-party skill, maintained in this repository.

## Notes

- Ask for the printer's imposition template; building to it prevents expensive resubmission.
- Keep a layered source file alongside the flattened PDF.
- Pairs with: `editorial-layout-design`, `typography-and-type-systems`.
