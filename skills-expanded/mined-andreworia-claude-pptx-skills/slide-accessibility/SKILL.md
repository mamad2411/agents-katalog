---
name: slide-accessibility
description: Makes a deck usable with a screen reader and compliant for a regulated client — alt text, reading order, slide titles, contrast, table headers, captions. Not for general visual polish.
---

# Slide Accessibility

## When to use

Use this skill when a deck goes to a public body, a bank, a healthcare or education client, anyone procuring under an accessibility standard, or any audience that includes a screen-reader user. Also use it before a deck is published to a website, because a published `.pptx` or its PDF inherits every defect. Do not use it as a general design pass; contrast and reading order are correctness problems, not taste problems, and `brand-compliance-auditor` covers the rest.

## What it does

It runs the deck against the checkable accessibility requirements, fixes them in the file rather than in a separate document, and produces a defect list with what was changed. The output is a remediated deck plus an audit trail a procurement team can accept.

## Method

**1. Know which standard you are held to.** In the United States, Section 508 incorporates WCAG 2.0 Level AA; in Europe, EN 301 549 references WCAG 2.1 Level AA and underpins public-sector procurement. Most contracts name WCAG AA. Ask which, and write the answer at the top of the audit.

**2. Give every slide a unique title.** It is the primary navigation handle: a screen reader announces it, and Outline view and slide-jump tools use it. Every slide needs one and no two should be identical — three slides called "Agenda" defeat the point. Where the design carries no visible title, hide the placeholder rather than deleting it: with the Accessibility Checker open, the **Accessibility** tab's *Slide Title* menu offers **Add Slide Title** and **Hidden Slide Title**, which puts a real title off the visible canvas.

**3. Write alt text that carries the information, and mark the rest decorative.** Right-click an object and choose **Edit Alt Text**, or use the Accessibility tab. What matters:

- Describe what the image *means* here, not what it depicts. A revenue chart's alt text is the finding — "Revenue grew from £12m to £31m over four years, with the step change in FY23" — not "bar chart". Do not open with "image of"; the screen reader already says so.
- Decorative rules, textures and brand furniture get the **Mark as decorative** checkbox, which removes them from the reading order. That matters as much as describing content.
- A screenshot of a table is invisible. Rebuild it as a real table.
- Alt text on a group is read and its members are skipped, so give a composite diagram one good group-level description rather than eleven fragments.

**4. Fix the reading order, and know which pane you are in.** Two tools, and they run in opposite directions:

- **Reading Order Pane** (`Review > Check Accessibility`, then the *Reading Order Pane* button on the Accessibility tab) lists objects **top to bottom in reading order** — the top item is read first. Windows desktop only; it is not in PowerPoint for the web or on macOS.
- **Selection Pane** (`Home > Arrange > Selection Pane`) lists the same objects in **z-order**, which is the reverse — the **bottom** item is read first. This is the single most common remediation mistake: a deck "fixed" in the Selection Pane top-down comes out backwards.

Order should follow the argument: title, then exhibit or body, then source line and footnotes. Re-check after any layout change, because a newly inserted shape lands at the front.

**5. Check contrast against the real numbers.** WCAG AA requires **4.5:1** for normal text and **3:1** for large text, where large means 18 pt or larger, or 14 pt bold or larger. Meaning-bearing non-text elements — chart series, an icon that is the only label — need **3:1**. The built-in checker flags some contrast problems but misses text over a photograph, a gradient or a semi-transparent panel, so sample the actual pixel behind the text. Where a brand colour fails, do not invent one: use the palette's approved dark tint, or put the text on a solid panel.

**6. Never encode meaning in colour alone.** A red bar and a green bar mean nothing to a colour-blind reader or in greyscale print. Add a direct label, pattern or symbol alongside the colour, and test by exporting a slide in greyscale.

**7. Build tables as tables.** A grid of aligned text boxes looks like a table and exports as loose text. Use a real table object, tick **Header Row** in `Table Design > Table Style Options`, and keep it rectangular: no merged or split cells, no blank rows used as spacing, no nested tables. PowerPoint tables cannot express column *and* row scope, so a table that needs both is a sign it should be split into two.

**8. Handle media and motion.** Video needs captions: select it and use `Playback > Insert Captions`, which accepts a WebVTT (`.vtt`) file. Audio needs a transcript, which can live in the notes. Nothing may flash more than three times per second. Avoid autoplay, and avoid animations that carry information the static slide does not — a build that reveals the punchline is lost in the exported file.

**9. Make links say where they go.** "Click here" and a bare URL are both useless read aloud. In `Insert > Link`, put a meaningful phrase in *Text to display* and add a ScreenTip where the destination is not obvious.

**10. Run the checker, then export correctly.** `Review > Check Accessibility` sorts findings into Errors, Warnings and Tips; work Errors first and tick *Keep accessibility checker running while I work*. It is a floor, not a ceiling — it cannot judge whether alt text is *good*. On export, leave **Document structure tags for accessibility** on (see `pptx-export-and-pdf`); an untagged PDF discards everything above.

## Inputs

- The deck, and the standard being applied.
- The brand palette with hex values, so contrast is computed against approved colours.
- Whether the deliverable is the `.pptx`, a PDF, or both.
- Any embedded media, and whether captions or transcripts exist.

## Output format

- The standard applied, stated at the top.
- A defect list by slide: issue, severity, and the fix made.
- Contrast as measured ratios against the 4.5:1 and 3:1 thresholds, naming failing pairs.
- Reading order changes, with the pane used.
- Anything that could not be remediated in PowerPoint, and why.
- The checker's final state and the export settings used.

## Example

Input: a 24-slide programme update for a public-sector client, contracted to WCAG 2.1 AA.

Output:

- Standard: WCAG 2.1 AA (EN 301 549).
- Titles: 24 of 24 titled; slides 3, 11 and 20 use hidden titles because the design is full-bleed. Three duplicate "Progress" titles disambiguated.
- Alt text: 31 objects described, 14 decorative motifs marked decorative, chart alt text on slides 6, 9 and 14 rewritten to state the finding.
- Reading order: corrected on 9 slides in the Reading Order Pane. Slide 17 had been "fixed" bottom-up previously and was fully reversed.
- Contrast: brand mid-grey `#8A8F98` on white measured 2.9:1 at 12 pt and fails; replaced with `#5A6069` at 4.9:1. Amber chart series at 2.1:1 darkened and direct-labelled.
- Colour alone: RAG status on slides 8 and 15 given text labels.
- Tables: slide 12's text-box grid rebuilt as a real table with Header Row; slide 19's merged header cells split.
- Media: the embedded video captioned from a supplied `.vtt`.
- Export: PDF with structure tags on. Checker reports zero Errors, two Tips retained deliberately.
