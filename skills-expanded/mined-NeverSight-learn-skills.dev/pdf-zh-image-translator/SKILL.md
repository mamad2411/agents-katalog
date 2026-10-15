---
name: pdf-zh-image-translator
description: Translate English PDF files into Simplified Chinese visual PDFs while preserving the original page images, layout, typography feel, colors, charts, and overall design. Use when Codex receives an English PDF and the user asks for a Chinese PDF version, page-image translation, PDF localization, or a translated PDF assembled from generated/edited page images using the imagegen skill.
---

# PDF Chinese Image Translator

## Core idea

Use a whole-page raster workflow. Render each selected PDF page to an image, use `$imagegen` in `text-localization` edit mode to regenerate the entire page as a clean Simplified Chinese page image, normalize the generated page image back to the original rendered page dimensions, then merge the normalized page images into one PDF. Keep the original PDF untouched.

This skill depends on `$imagegen` for the visual translation/edit pass. The bundled scripts handle deterministic preparation, page manifests, PDF assembly, and audits; they do not call imagegen themselves.

Important distinction: the script-render step is required PDF plumbing, not the translation style. Imagegen cannot directly edit a multi-page PDF, so every run must first render PDF pages into full-page images and later normalize/merge the generated images. The part the user rejected is region overlay / paint-over text replacement; do not describe or use that as the workflow.

Do not substitute another PDF translation pipeline for the imagegen pass. In particular, do not use `pdf2zh`, Google Translate, Gemini, DeepLX bridges, Ollama, or other text-translation/layout tools to produce the deliverable unless the user explicitly asks to compare against a non-imagegen pipeline. The deliverable for this skill is generated page images from whole-page imagegen, followed by deterministic dimension normalization and PDF binding.

Do not call external AI tools for OCR or translation support either. Avoid shelling out to `gemini`, `ask-gemini`, `ollama`, translation CLIs, hosted translation APIs, or ad hoc AI bridge servers to create page copy. ChatGPT/Codex already has enough multimodal OCR and translation ability for prompt support. Allowed AI components are limited to:

- the current Codex/ChatGPT model reading rendered page images and drafting page-level OCR/translation support;
- Codex child agents, when the user has authorized subagents, for parallel page OCR/translation support;
- the built-in `$imagegen` skill for the final whole-page Chinese page image generation.

Child agents are not an alternate toolchain. They may only inspect assigned rendered page images and return page-level support text for the main agent to put into the imagegen prompt. They must not call Gemini, Ollama, pdf2zh, DeepLX, Google Translate, or any other external AI/OCR/translation service.

## Workflow

1. Create a work directory for the job, usually next to the source PDF or under a user-named output folder.
2. Prepare page images and prompts:
   ```bash
   python scripts/prepare_pdf_pages.py \
     --pdf "/path/to/source.pdf" \
     --out "/path/to/workdir" \
     --start-page 1 \
     --end-page 5 \
     --dpi 200
   ```
3. For each prepared page, inspect `pages/page-NNN.png` with `view_image`, then invoke `$imagegen` built-in edit mode using the corresponding `prompts/page-NNN.txt`.
4. Save each final whole-page imagegen output as `translated_pages_raw/page-NNN.png`. Use exactly the same page number in the filename. Do not overwrite original rendered pages.
5. Normalize the generated page images back to the manifest dimensions:
   ```bash
   python scripts/normalize_page_images.py \
     --image-dir "/path/to/workdir/translated_pages_raw" \
     --manifest "/path/to/workdir/manifest.json" \
     --out-dir "/path/to/workdir/translated_pages"
   ```
6. Merge normalized translated page images:
   ```bash
   python scripts/merge_page_images_to_pdf.py \
     --image-dir "/path/to/workdir/translated_pages" \
     --manifest "/path/to/workdir/manifest.json" \
     --out "/path/to/workdir/translated.pdf" \
     --dpi 200
   ```
7. Audit the package:
   ```bash
   python scripts/audit_translation_package.py \
     --manifest "/path/to/workdir/manifest.json" \
     --translated-dir "/path/to/workdir/translated_pages" \
     --pdf "/path/to/workdir/translated.pdf"
   ```

## Imagegen Pass

Use the page image as a whole-page edit target, not as loose inspiration and not as a region-painting task. Keep the prompt strict:

```text
Use case: text-localization
Asset type: translated PDF page raster
Primary request: Regenerate this entire PDF page as a clean Simplified Chinese version.
Input image: the displayed page image is the edit target.
Source-of-truth text: use the extracted text list in the prompt when present.
Constraints: preserve original composition, backgrounds, photos, charts, line art, colors, spacing, headings, captions, bullets, tables, page numbers, logos, and all non-text visual elements. Replace English text with Simplified Chinese while naturally re-typesetting it into the original layout. Keep numerals, formulas, citations, URLs, brand names, product names, and proper nouns unless a standard Chinese rendering is obvious. Fit Chinese text into the original text areas; reduce font size only as needed. Do not add summaries, watermarks, new labels, or decorative elements.
Avoid: overlay rectangles, painted fill boxes, smudged patches, blurry text, invented data, altered charts, changed photos, missing footers, extra commentary, mixed English/Chinese where a clean Chinese translation is possible.
```

Always try a whole-page imagegen pass first and treat it as the preferred output style. If the built-in imagegen result changes the pixel dimensions, do not repair it with painted regions; run `normalize_page_images.py` to scale the whole generated page back to the original dimensions before merging. If a page is extremely dense and text becomes garbled, retry the whole page with a stricter prompt or a shorter source-text section. Only use crop-level generation when the user explicitly approves a manual repair pass.

If structured PDF text extraction returns zero blocks, do not switch tools. Use the rendered page image as the primary source, and optionally add plain text, word-mode extraction, or OCR text into the imagegen prompt as translation support. Empty or partial extracted text is a prompt-quality issue, not permission to replace the workflow with `pdf2zh` or an external translation model.

For OCR/translation support on image-only or poorly encoded PDFs:

1. First use the current Codex/ChatGPT visual reading ability on `pages/page-NNN.png`.
2. If the user has authorized subagents and the page range is large, delegate page groups to Codex child agents. Give each child agent only rendered page images and ask for a compact page brief: visible English OCR, Simplified Chinese translation, terms to preserve, and layout notes. Tell child agents not to call external AI tools or create final images/PDFs.
3. Save or paste each page brief into the corresponding imagegen prompt. The brief is support material; the final translated page still comes from whole-page imagegen.

Recommended child-agent brief format:

```text
Page: <number>
OCR text: <visible English text, in reading order>
Chinese translation: <faithful Simplified Chinese, concise enough to fit the page>
Preserve: <proper nouns, product names, URLs, numbers, formulas>
Layout notes: <headings, tables, callouts, footer/header, dense areas>
Warnings: <uncertain OCR or text that needs visual review>
```

Do not use region overlay, paint-over, background fill boxes, or clone-stamp style text replacement as the default workflow. The user's preferred look is a clean full-page imagegen regeneration followed by deterministic size correction and PDF binding.

When reporting progress to the user, call script steps "PDF page rendering," "dimension normalization," and "PDF binding." Do not call them a script-based translation route, because the translation image is produced by whole-page imagegen.

## Quality Gates

- The translated page count must match the requested page range.
- Normalized page image dimensions must match `manifest.json`.
- Non-text content must remain visually unchanged.
- Charts, figure labels, table values, citations, and page numbers must remain correct.
- Output PDF must open and have the expected number of pages.
- Report the work directory, raw imagegen page directory, normalized translated page directory, final PDF path, and any pages that need manual retry.

## Script Notes

- `prepare_pdf_pages.py` prefers PyMuPDF (`fitz`) when available. On macOS, it can fall back to the bundled Swift/PDFKit renderer plus `pypdf` text extraction.
- `normalize_page_images.py` resizes whole-page imagegen outputs back to the original rendered dimensions from `manifest.json`.
- `merge_page_images_to_pdf.py` uses Pillow to bind normalized page images into a PDF.
- `audit_translation_package.py` checks image count, dimensions, and PDF page count when `pypdf` is available.
