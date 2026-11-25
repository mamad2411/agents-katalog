---
name: loop-cmf-generation
description: Turns a Loop CMF workbook into branded CMF PDFs. Reads the transposed schema (one tab per product, one column per SKU), drives Nano Banana recolour attempts against the matching clown render, judges which attempts look right, and assembles the document. Use when a designer asks to render new colourways for Switch 2, Engage 2, Experience 2, Quiet 2, Dream, Cocoon, Link, Aphrodite, Eclipse, or any of their carry cases. Also use when reviewing existing CMF renders, mapping Pantone codes to product components, choosing between attempts, or composing the CMF presentation document.
---

# Loop CMF Generation

This skill encodes the judgment Damien uses when producing CMF (Colour, Material, Finish) files at Loop. The mechanical parts (workbook parsing, clown lookup, render invocation, PDF export) live in `src/lib/cmf/`. This skill carries the parts that machines cannot infer on their own: what makes a CMF render right, when to push back on a workbook, and how to lay out the document.

## Spine

Three jobs, in order:

1. **Read the workbook** — one tab per product, one column per SKU. Empty SKU columns get ignored, even when other columns in the same tab are full.
2. **Recolour the clown** — Nano Banana edits the matching clown render to apply the Pantone palette while preserving geometry, material response, and parting lines.
3. **Compose the document** — banner + recoloured hero + spec table + palette breakdown. Aspect ratio is 16:9.

Each job has its own freedom band. Get the band right before generating.

## Degrees of freedom

| Step | Band | Why |
|------|------|-----|
| Workbook parsing | LOCK | Schema is contractual. Wrong field → wrong PDF → wrong factory order. |
| Product / component mapping | LOCK | Slug + region keys are matched against the clown library and Arena. |
| Document aspect ratio (16:9), banner identity, Pantone tokens | LOCK | These are the things Operations checks first. |
| Prompt assembly per component | GUIDE | Wording flexes by product (silicone soft sheen vs. metal mirror polish). |
| Number and seed of recolour attempts | EXPLORE | Three to five attempts per SKU is the right zone for nano-banana variability. |
| Layout tweaks (label ordering, optional notes) | GUIDE | Approve-or-edit before export, not after. |
| "Dream against the average" passes | DREAM | Only for ideation, never for the final packet. |

## When to use which mode

Use this skill when the user:

- Drops a `CMF_Schema_*.xlsx` workbook into the CMF Studio.
- Asks to render new colourways for a product family (one or many SKUs).
- Reviews existing CMF renders and wants to know which to approve.
- Asks to add a new product to the catalog (component map + clown).
- Asks to produce or revise a CMF presentation PDF.

Do **not** use this skill to invent CMF data the workbook did not specify. The workbook is the source of truth.

## Workflow

Copy this checklist:

```
- [ ] 1. Resolve sheets → products
- [ ] 2. Validate each SKU column (filled vs placeholder)
- [ ] 3. Pick the clown reference per (productSlug, variantSlug)
- [ ] 4. Generate 3–5 recolour attempts per SKU
- [ ] 5. Judge each attempt against the rejection criteria
- [ ] 6. Approve the best attempt per SKU
- [ ] 7. Compose the HTML packet preview (16:9 pages)
- [ ] 8. Export the final PDF
```

### 1. Resolve sheets → products

Use `getCmfProductBySheet(sheetName)` from `src/lib/cmf/products.ts`. Tab names tolerated:

- "Switch 2", "Engage 2", "Experience 2", "Quiet 2", "Dream", "Cocoon", "Link", "Aphrodite Earplug", "Eclipse"
- "<product> CC" or "<product> Carry Case" for cases
- `README` and `Textile Library` are meta tabs — always skip them.

If a tab cannot be mapped, surface it as an unmapped sheet and continue. Never silently drop a product.

### 2. Validate each SKU column

A SKU column is **filled** when at least one of the following is real (not "xxxxxxxxxxx", not "xx/xx/xxxx", not blank):

- `Product Name`
- `Product Code`
- `CMF number`
- Any per-SKU Pantone value on a component row

Common-spec values in column B do not make a SKU filled. The whole point of column B is to share spec across SKUs that the designer has not yet defined.

Carry placeholder columns through as ignored. Surface their count in the UI ("2 SKU columns skipped") so the designer can see what got dropped without re-running anything.

### 3. Pick the clown reference

For each SKU, look up the clown by `(productSlug, variantSlug)`. Fall back to any clown for the product if the variant has none.

Clown rules (these are LOCK):

- Use exactly four base colours on a clown PNG: red, green, blue, yellow. Pink only when a product genuinely has a fifth recolour region (e.g. Aphrodite jewel accent).
- Each colour must paint a contiguous region with clear edges.
- The reference must be a flat studio render with reflections baked in — Nano Banana reads those reflections to decide whether a surface is glossy, satin, or matte.
- Do not invent regions the clown does not contain. If the spec mentions a region but the clown does not show it, prompt the user to update the clown first.

### 4. Generate recolour attempts

Build the prompt with `buildCmfPrompt(row)`. The prompt expresses:

- Product framing (`Loop Switch 2 earplugs, studio-lit hero render, neutral background`).
- Per-component instructions: which region recolours to which Pantone (or hex), with material and finish phrasing.
- Protected surfaces: anything the workbook did not respec must be kept as-is.
- Negative instructions: no logos, no text, no packaging, no lifestyle context.

Generate **3 to 5 attempts** per SKU by default. More than that wastes credit; fewer is too narrow when Nano Banana is feeling literal.

Material phrasing reference (GUIDE-level):

| Material | Wording |
|----------|---------|
| POM | "POM, matte" |
| ABS / PC-ABS | "polycarbonate semi-gloss" or "ABS satin" depending on finish |
| Silicone | "silicone with soft sheen, ~30% milky translucency unless opaque is specified" |
| Aluminium | "anodised aluminium, brushed or polished as specified" |
| Fabric / velcro | "fabric, matte, fibre direction visible" |

When the spec mentions a holographic, iridescent, or pearlescent finish, **let Nano Banana cook**. It handles those better than KeyShot ever did. Mention "holographic" / "iridescent" / "pearlescent" explicitly in the prompt and add "no chromatic banding artefacts" as a negative.

### 5. Judge attempts

Reject an attempt if any of these are true:

- A protected surface changed colour, geometry, or finish.
- Pantone bleed across regions (e.g. cap colour leaks onto the ring).
- Material response inconsistent with the spec (matte where the workbook said gloss, vice versa).
- Added artefacts: text, logos, packaging, hands, models, background gradients, lens distortion, props.
- Geometry deformed (silhouette no longer matches the clown).
- A region that should stay unchanged got recoloured (compare to the clown).

When two attempts both pass, prefer the one with:

- Cleaner edges between regions.
- Material response closer to the existing product family.
- Lower compression / banding.

Keep rejected attempts archived, not deleted. Designers and reviewers need history when QA pushes back.

### 6. Approve

Each SKU needs exactly one approved attempt before the packet can export. Approving an attempt swaps the "current" image for the SKU and marks the packet ready for PDF generation. Approval is reversible — un-approving rolls back to the previously approved attempt if there is one.

### 7. Compose the HTML preview

Page layout per SKU (16:9, 1280×720):

- Banner: CMF code · product family · date on the left, SKU colourway centred, "Loop · CMF" on the right.
- Hero image: approved render on the left half.
- Spec table: components × Pantone / Material / Finish / Technique on the right half.
- Footer: palette swatches + product code / EAN / notes.

The exported PDF orders pages as: one render/spec page per SKU, then a single shared part-breakdown page at the end (clown reference + colour legend + material/finish/technique per component — no per-colourway Pantone, since the breakdown applies to every SKU). There is no pack-overview page (removed on designer feedback, 2026-07-06).

The HTML preview is editable: label, order, notes, and palette overrides can be tweaked here. The workbook is the source of truth for components, so they cannot be edited in preview — adjust those upstream in the workbook.

### 8. Export

The PDF generator (`src/lib/cmf/pdf.ts`) consumes the same data model as the HTML preview, so what you see is what you ship. The filename pattern is `{cmfCode}_{Product}_CMF_{Colorway}.pdf` (e.g. `CMF-001234revA_Switch2_CMF_Sage.pdf`).

If any SKU lacks an approved attempt, refuse to export and tell the user which SKUs are missing approvals.

## References

- **Workbook schema**: See [references/workbook-schema.md](references/workbook-schema.md)
- **Product & component map**: See [references/product-component-map.md](references/product-component-map.md)
- **Prompting (Nano Banana recolour)**: See [references/prompting.md](references/prompting.md)
- **Document template**: See [references/document-template.md](references/document-template.md)
