---
name: html-resume
description: Turn resumes exported from job platforms, existing PDFs, or career notes into independently editable, recruiter-friendly HTML with exact A4 PDF output. Use for resumes, CVs, executive profiles, professional biographies, and portfolio summaries that need Chinese-English translation or same-language rewriting, factual preservation, clear information hierarchy, user-directed color styling, optional portrait integration, multi-page layout, and print validation.
---

# HTML Resume Skill

Create professional career documents that read well on screen and print predictably to A4 PDF. Help users move career information out of a job platform or fixed PDF layout into an independently editable document.

Always deliver HTML as the source of truth. When the user requests PDF, export the same HTML and validate every rendered page.

## 1. Choose the source path and confirm the brief

Support either source path:

1. An existing resume exported from any job platform, an attached PDF, or text extracted from that PDF.
2. Career history, notes, or structured facts supplied directly by the user.

When the environment supports PDF input, inspect the original PDF. When it does not, use extracted Markdown or plain text supplied by the user. If Microsoft MarkItDown is already available in a local environment, it can extract a text-based PDF with:

```bash
markitdown existing-resume.pdf -o existing-resume.md
```

Treat extracted text as an ingestion aid. Check it against the original PDF when available because columns, dates, links, and section order may be extracted incorrectly. Do not claim OCR was performed. If a scanned or image-only PDF cannot be read, request OCR output or source text from the user.

Before designing, confirm:

- document type
- source language, output language, and target audience
- target role or positioning
- required sections
- page-count preference or hard limit
- preferred color palette or brand direction
- portrait or avatar availability
- HTML-only or HTML plus PDF delivery

Ask the user to choose a color palette when none is supplied. Do not silently impose a default hue. If the user explicitly delegates the choice, propose a restrained palette appropriate to the role and audience before applying it.

Do not block on details that can be safely inferred, but never infer facts, metrics, qualifications, employment dates, contact information, or portrait assets.

## 2. Output contract

Produce `resume.html` for the first delivery.

Also produce `resume.pdf` when requested. Optional preview files may use names such as:

```text
resume-preview-page-1.png
resume-preview-page-2.png
```

For later revisions or caching-sensitive environments, use matching versioned names:

```text
First_Last_Resume_v2.html
First_Last_Resume_v2.pdf
```

Keep HTML and PDF content identical. Do not deliver only a PDF when HTML is requested or implied.

## 3. Rewrite without inventing

Rewrite for clarity, credibility, and scanning speed.

Support Chinese-to-English, English-to-Chinese, and same-language rewriting. Translate meaning and hiring context rather than sentence structure. Use natural terminology for the target audience while preserving the candidate's actual scope and level.

Preserve:

- employers, titles, dates, degrees, certifications, and contact details
- the candidate's actual ownership and scope
- supplied metrics and their original meaning
- standard industry terminology when translating
- company, product, school, and certification names unless the user supplies or approves a recognized translated name

Never:

- invent metrics, tools, qualifications, projects, or outcomes
- promote participation into leadership without evidence
- use unsupported labels such as “expert” or “world-class”
- translate line by line when consolidation improves recruiter comprehension
- hide uncertainty in an ambiguous translation; ask the user to confirm instead

Prefer bullets shaped as:

```text
Action + technical or business scope + verified impact
```

Remove filler, repeated claims, long autobiographical passages, generic self-praise, keyword stuffing, and obvious AI phrasing.

## 4. Build the information architecture

Choose section order and page count from the candidate's strongest hiring signals. Do not force every resume into the same template.

A common order is:

1. identity, target role, and contact details
2. professional summary
3. core skills
4. relevant experience
5. selected projects or achievements
6. education
7. certifications and languages
8. publications, awards, or additional information when relevant

Prioritize page 1 for the name, target role, summary, strongest skills, most relevant experience, and best verified achievement.

Use page 2 for projects, technical depth, education, certifications, languages, and supporting experience. Add page 3 only when the content genuinely requires it. Shorten weak content before shrinking typography.

## 5. Use an editorial page frame

Default to a restrained page frame with a color block at both the top and bottom of every physical page, unless the user requests a plainer treatment.

- Keep the top band approximately `6–8mm` high.
- Use the bottom band as the footer, approximately `8–11mm` high.
- Apply the same bands consistently across all pages.
- Keep the bands secondary to the content and ensure accessible footer contrast.
- Reserve safe space so body content never collides with the bottom band.

Use an open, unboxed header. Place the portrait or monogram beside the candidate's identity without wrapping either one in a Card, hero panel, rounded container, or tinted background box.

Separate the header from the body with spacing or a thin divider. On later pages, use a compact continuation header with the candidate's name and a short page label.

## 6. Apply user-directed color

Use semantic CSS variables, but derive their values from the user's requested palette:

```css
:root {
  --page-bg: {{page_background}};
  --preview-bg: {{screen_preview_background}};
  --text-main: {{text_color}};
  --text-muted: {{muted_text_color}};
  --primary: {{primary_color}};
  --primary-strong: {{strong_primary_color}};
  --primary-soft: {{soft_primary_color}};
  --primary-pale: {{pale_primary_color}};
  --accent: {{accent_color}};
  --line: {{divider_color}};
  --on-primary: {{accessible_text_on_primary}};
}
```

Do not treat any hue as the Skill default. Do not copy the palette from an example unless the user asks for that palette.

Keep body text dark enough for print. Use pale tones for broad supporting areas and stronger tones for bands, headings, labels, and small emphasis. Verify contrast instead of assuming a light or saturated color is readable.

## 7. Keep the layout open

Create hierarchy with typography, spacing, alignment, dividers, and controlled color accents.

Prefer:

- open sections
- aligned columns
- thin rules
- concise sidebars
- project lists with dividers
- one or two grouped panels only when containment adds meaning

Avoid:

- Card wrappers around the portrait or Header
- wrapping every section in a rounded box
- dashboard-like metric grids
- nested Cards
- decorative icons beside every line
- dense columns that reduce scanability

Use Cards only for distinct, parallel groups such as education and certifications, or compact supporting information. Use no more than two supporting Cards in one visual region.

## 8. Integrate portraits carefully

Use a portrait only when the user provides one, the target market accepts resume photos, or the user explicitly requests it.

- Crop cleanly with `object-fit: cover`.
- Preserve facial proportions and avoid aggressive retouching.
- Keep the portrait secondary to the name and headline.
- Use a circular or softly rounded image frame without an outer Card.
- Omit the image area when no portrait exists; use a monogram only when it improves balance.
- Never leave an empty placeholder or generate a fake portrait without permission.

## 9. Use readable typography

Use local or widely available fonts with strong Chinese and Latin coverage:

```css
body {
  font-family:
    "Noto Sans TC",
    "Noto Sans CJK TC",
    "PingFang TC",
    "Microsoft JhengHei",
    "Segoe UI",
    Arial,
    sans-serif;
}
```

Use print-oriented `pt` units for core typography. Recommended ranges:

- name: `24–30pt`
- headline: `10.5–13pt`
- section heading: `10–12pt`
- experience title: `10.5–12pt`
- body: `9.5–10.5pt`
- metadata: `8.5–9.5pt`
- footer: `7.5–8.5pt`

Never reduce body text below `9pt`. Shorten content or rebalance pages first.

## 10. Build exact A4 pages

Represent each physical page with one explicit `.page` element sized to `210mm × 297mm`. Do not rely on browser auto-pagination inside a page container.

Use `height: 297mm`, not only `min-height`. Set `@page` to A4 with zero browser margins, preserve print colors, and prevent hidden overflow.

Read [references/a4-layout-and-validation.md](references/a4-layout-and-validation.md) before implementing A4 CSS, exporting PDF, or validating output. Follow its page-frame template, footer pattern, export commands, and verification sequence.

## 11. Use semantic HTML

Use logical headings and semantic sections. A typical two-page structure is:

```html
<main class="resume-document">
  <section class="page" aria-label="Resume page 1 of 2">
    <div class="top-band" aria-hidden="true"></div>
    <header class="identity-header">...</header>
    <div class="page-content">...</div>
    <footer class="footer-band">...</footer>
  </section>

  <section class="page" aria-label="Resume page 2 of 2">
    <div class="top-band" aria-hidden="true"></div>
    <header class="continuation-header">...</header>
    <div class="page-content">...</div>
    <footer class="footer-band">...</footer>
  </section>
</main>
```

Add or remove pages according to the brief. Do not leave empty template blocks.

## 12. Validate before delivery

Inspect HTML for factual consistency, complete sections, valid links, resolved portrait paths, correct language, and no placeholders.

When PDF is requested:

1. Generate PDF from the final HTML.
2. Confirm the expected page count.
3. Confirm every page is A4 within the documented tolerance.
4. Render every PDF page to an image.
5. Inspect clipping, overlap, page balance, margins, contrast, image crop, footer collisions, and font rendering.
6. Extract PDF text; use OCR only when rasterization or missing text is suspected.
7. Fix failures and repeat the full check.

For HTML-only delivery, still inspect every explicit `.page` and verify `scrollHeight <= clientHeight`.

## 13. Adapt density safely

When content is too long, change it in this order:

1. remove repetition
2. shorten weak bullets
3. reduce the number of bullets
4. move secondary content to the next page
5. reduce section gaps slightly
6. simplify decoration
7. reduce font size modestly without crossing the minimum

When content is too short, increase whitespace and strengthen hierarchy. Do not stretch sparse content into unnecessary Cards or add decorative noise.

## 14. Quality checklist

Before delivery, confirm:

### Content

- [ ] Facts match the supplied source.
- [ ] No unsupported claims or metrics were added.
- [ ] Headline and strongest evidence match the target role.
- [ ] Repetition and filler were removed.

### Design

- [ ] The user supplied or approved the color palette.
- [ ] Every page has consistent top and bottom color treatment unless opted out.
- [ ] Portrait and Header are not inside a Card.
- [ ] Cards remain limited to meaningful supporting groups.
- [ ] Typography, contrast, and margins are readable and balanced.

### HTML and PDF

- [ ] HTML is included as the source deliverable.
- [ ] CSS variables control the palette.
- [ ] Every `.page` is exact A4 with no hidden overflow.
- [ ] Footer page numbers and total pages are correct.
- [ ] No clipping, overlap, orphan headings, or broken assets remain.
- [ ] Every requested PDF page was rendered and visually inspected.

## 15. Deliver clearly

Provide direct links to generated files. State only checks that were actually performed.

Example:

```text
[Download HTML](...)
[Download PDF](...)
```

Do not claim PDF, OCR, or visual validation unless it was completed.
