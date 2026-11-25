---
name: drawing-gdt-review
description: Reviews mechanical engineering drawings (PDF, image, or DXF) for dimensioning errors, over/under-constraint, GD&T misuse, datum problems, missing title-block and manufacturing notes, and ASME Y14.5 / ISO GPS compliance, returning a severity-ranked issue list with fixes. Use when the user asks to check, review, or red-line a drawing or asks about GD&T callouts.
---

# Drawing & GD&T Review

## Workflow
1. **Ingest.** Render PDF pages to PNG at 200+ dpi (`pdftoppm -r 200 -png drawing.pdf page`) and view each one. For DXF, list the entities with `ezdxf`. Zoom into the title block, the notes, and each view.
2. **Identify the standard**: ASME Y14.5-2018 or ISO 1101 / ISO 8015 (look for "ISO 8015" or a projection symbol in the title block). Also note the projection type (first or third angle). All later judgments depend on this.
3. **Understand function first.** In 2–3 lines, write what the part does and which features mate with other parts. GD&T should control those features. Ask about function only if you can't infer it.
4. **Run the checklist** in `references/checklist.md`, section by section. For each finding, record the location (sheet / view / zone), the issue, the severity, and the fix. Severity scale:
   - **Critical**: the part can't be made or inspected as drawn, or the drawing contradicts itself.
   - **Major**: ambiguous, so a supplier could legally make a non-functional part.
   - **Minor**: a standards or style deviation.
   - **Suggestion**: a cost-reduction or clarity improvement.
5. **GD&T sanity rules** (the most common errors):
   - Datum features must be physical, stable, and functional. The primary datum should constrain 3 degrees of freedom on mating parts.
   - Position needs basic dimensions to the datums. ± dimensions on a positioned feature are a Critical error.
   - Datum references go in precedence order (A|B|C), and the order must match the part's assembly order.
   - MMC (Ⓜ) applies only to features of size. Using it on a planar surface is an error.
   - Flatness or straightness tolerance must be tighter than the size tolerance (Rule #1, Y14.5).
   - Profile without datums controls form only. Check whether location was intended.
   - Runout and concentricity: Y14.5-2018 removed concentricity and symmetry. Recommend position or profile instead.
6. **Tolerance reasonableness.** Flag tolerances tighter than the process can hold (see `dfm-review`'s process tables), and tolerances that are loose on mating features.
7. **Output**: a table sorted by severity, then a short summary (counts by severity and the top 3 fixes). If asked for a red-line, annotate the page PNG with numbered balloons (PIL) that match the table rows.
