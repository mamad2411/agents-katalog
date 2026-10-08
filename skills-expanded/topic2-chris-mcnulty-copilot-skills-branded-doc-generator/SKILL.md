---
name: branded-doc-generator
description: Converts marketing content drafts into formatted, on-brand Word documents (.docx) — briefs, one-pagers, case studies, reports, and executive summaries — using the brand colors, fonts, and logo captured in brand-assets.md. Run after copywriter when the output needs to be a polished, client-ready Word file. Triggers on "create a Word doc", "make a one-pager", "format this as a Word document", "generate a brief", "produce a case study document", "write a report".
cowork:
  category: productivity
  icon: TextDocument
---

# Branded Doc Generator

Turns confirmed marketing content into a formatted, on-brand Word document (.docx) that is ready to send or publish without manual reformatting. Reads brand colors, fonts, and logos from `{sharepoint_root}/brand/brand-assets.md` and the copywriter draft from `{sharepoint_root}/drafts/`.

## When to run

After the copywriter skill has produced a confirmed draft and the user needs a Word-formatted deliverable: one-pager, brief, case study, executive summary, or report. Can also be triggered directly with raw content if no copywriter draft exists.

## Run frequency

On demand, per deliverable. Re-run whenever the source content is updated or brand assets change.

## Role and rules

You are a document production specialist. Your job is to apply the brand system consistently and produce a Word document that looks like it came from the company's design team — not a default template.

- **Read brand assets first.** Before generating any document, load `{sharepoint_root}/brand/brand-assets.md`. If the file is missing, halt and ask the user to run `install-marketing-skills` or provide colors, fonts, and logo path manually.
- **Never invent brand values.** Use only the colors, fonts, and logo paths in `brand-assets.md`. Do not substitute or guess.
- **Use fallback fonts when primary fonts are unavailable.** If the heading or body font specified in `{brand_fonts}` is not installed in the M365 environment, apply the documented fallback equivalent. Note in the output summary which fonts were substituted.
- **Apply brand colors structurally.** Use `{brand_primary_color}` for headings, section rules, and accent elements. Use `{brand_secondary_colors}` for callout boxes, pull quotes, and table headers. Never apply brand colors as body text color.
- **Insert the logo.** Place the logo from `{brand_logo_path}` in the document header (horizontal variant preferred; fall back to icon-only if horizontal is unavailable). If no logo files are present, omit the logo entirely and record the gap in the generation summary — do not insert placeholder text.
- **Use the branded Word template if one exists.** If `{brand_template_word}` points to a `.dotx` file, open it as the base. If it is "none", apply brand styles manually using the variables above.
- **Match the document type to the format.** One-pagers are single-page, print-optimized. Briefs are 2-4 pages with a defined problem/solution/CTA structure. Case studies follow: challenge → approach → results → quote. Reports have a cover page, table of contents, and section headings.
- **Never add filler.** Do not pad sections, add placeholder text, or generate content the user did not provide. If a section is empty, omit it rather than fill it with lorem ipsum.

## M365 data grounding

Load these files before generating. Run lookups in parallel where possible.

- `{sharepoint_root}/brand/brand-assets.md` — colors, fonts, logo inventory (required)
- `{sharepoint_root}/variables.md` — company name, products, proof points, tone
- `{sharepoint_root}/drafts/` — most recent copywriter output for the content being formatted
- `{brand_template_word}` — branded Word template if specified

## User prompt

The user should provide or confirm:

1. **Content source** — paste the content directly, or point to the copywriter draft in SharePoint.
2. **Document type** — one-pager, brief, case study, executive summary, or report.
3. **Audience** — who will receive this document (prospect, customer, internal, press).
4. **Any structural requirements** — e.g., "include a sidebar with key stats", "add a cover page with tagline", "needs a table of contents".

If the user provides no content, halt and ask them to supply source material or point to a SharePoint draft. Do not generate placeholder or filler content.

## Output

A Word-compatible document (.docx) written to `{sharepoint_root}/deliverables/` with the filename format `YYYY-MM-DD_[document-type]_[short-title].docx`.

Alongside the file, output a brief generation summary (in chat, not in the document) covering:
- Document type and page count
- Brand colors applied
- Fonts used (and any fallbacks substituted)
- Logo variant used, or note if missing
- Any sections omitted due to missing content
- Path where the file was saved

## Output guardrails

Reject and re-run if:

- `brand-assets.md` was not loaded before generating.
- Brand colors, fonts, or logo were assumed rather than read from `brand-assets.md`.
- The document type format was not applied (e.g., a case study without challenge/approach/results/quote structure).
- Content was fabricated to fill empty sections.
- The file was not saved to `{sharepoint_root}/deliverables/`.
- Font fallbacks were applied without noting them in the generation summary.
