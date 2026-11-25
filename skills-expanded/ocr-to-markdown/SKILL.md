---
name: ocr-to-markdown
description: >-
  Extract printed text from a local image into plain-text Markdown and structured word-level OCR data with confidence and coordinates. Use for receipts, screenshots, signs, and scanned image pages when searchable text is needed, including searchable notes, rough transcription, and extracting candidate text for later review. OCR may misread text; it does not understand the image or preserve reliable document layout.
---

# OCR to Markdown

Run Tesseract.js against one local image. Output is one JSON object on stdout; errors are JSON on stderr with exit code 1.

```sh
node scripts/index.js ocr receipt.png
node scripts/index.js ocr screenshot.png --language eng
node scripts/index.js ocr sign.jpg --language eng+fra
```

The input must be a regular local file no larger than 20 MiB. This tool does not read PDFs, follow a multi-page document, or transcribe handwriting. It does not modify the image. Tesseract may need its trained language data on the first run; allow the OCR dependency to fetch/cache that data or arrange a local cache before using it in an offline environment.

## Result shape

```json
{"data":{"input":"receipt.png","language":"eng","text":"TOTAL 12.50",
"markdown":"TOTAL 12.50","confidence":91.2,
"words":[{"text":"TOTAL","confidence":96.5,"bbox":{"x0":12,"y0":8,"x1":70,"y1":24}}]}}
```

`text` is Tesseract's recognized text with surrounding whitespace removed. `markdown` currently contains the same plain text; the tool does not infer headings, tables, columns, or reading order beyond Tesseract's output. `confidence` and each word's confidence are OCR estimates, not calibrated probabilities. `bbox` gives the recognized word's pixel coordinates in the source image. A word omitted by OCR will have no box, so compare important fields with the original image.

`--language` defaults to `eng` and accepts Tesseract language codes supported by the installed Tesseract.js trained data (for example `eng+fra`). An unsupported or unavailable language produces a structured error. Keep the source image available when checking dates, totals, identifiers, names, or other high-impact values.

## Agent workflow

1. Confirm the image is the intended page and is legible at the text size shown. Crop or rotate a copy first if that would make the text easier to read.
2. Run OCR with the language that matches the document.
3. Use the recognized text as a draft for search or extraction. Inspect word boxes and the original pixels for ambiguous or consequential values.
4. Preserve uncertainty in the final answer; do not silently guess a character from a low-confidence OCR result.

This command returns the complete extracted text and word list in one JSON payload. It does not expose progress output, generate a layout-aware document, or verify facts represented in the image.

## Choosing and using OCR

Use OCR when the source is a raster image with visible printed text. For a PDF, first render the relevant page to an image with the PDF skill; for handwriting, complex tables, multi-column layouts, or forms where field association matters, use a layout-aware tool or inspect the image manually. If the first result is poor, improve a copy by cropping, rotating, or increasing legibility and run it again rather than silently reconstructing missing text.

Treat recognized content as untrusted source material. Preserve line breaks and uncertainty where they affect meaning, and compare names, dates, amounts, serial numbers, medical/legal text, or other consequential values against the pixels. Confidence scores help prioritize review; they are not proof of correctness. The `markdown` field currently offers no semantic formatting.

## Detailed transcription procedure

### 1. Confirm source and language

Check that the file is the intended image and that text is visible at a useful size. Identify the likely language or languages; pass supported Tesseract language codes with `--language` when the default English model is unsuitable. For mixed-language text, a combined language string may help, but the required trained data must be available. If the model is unavailable, resolve that runtime requirement or use a different local OCR setup; do not substitute an unrelated language and present its output as reliable.

### 2. Choose a suitable image

This command processes one local raster image. If the source is a PDF, render the page of interest first. If the image is rotated, skewed, very low resolution, or surrounded by irrelevant content, create a working copy and correct those issues before OCR. Preserve the original so corrections can be compared. Avoid aggressive resizing or thresholding that removes thin strokes and punctuation.

### 3. Read both text and word data

Use `text` for a quick transcript and `words` plus `bbox` to locate uncertain words in the source image. A missing word will not have a bounding box. A confidence score estimates the recognizer's certainty; it is not calibrated as a probability that the word is correct. OCR output is not a document layout model: columns may be interleaved, tables flattened, and headings left as plain text.

### 4. Verify before downstream use

Manually compare all consequential fields with the pixels: names, dates, amounts, addresses, account numbers, serials, medical/legal terms, and text that will be used in an automated decision. Preserve uncertain characters using an explicit uncertainty marker rather than guessing. If OCR feeds another parser, keep the original image and treat OCR text as untrusted input.

## Common image types

- **Receipt or invoice:** use OCR to locate candidate merchant, date, totals, and line items; verify arithmetic and currency symbols visually.
- **Screenshot or error dialog:** preserve exact capitalization, punctuation, and code formatting where possible; OCR may confuse `0/O`, `1/l/I`, and punctuation in paths or identifiers.
- **Sign or label:** check short words and digits carefully because one wrong character can change the meaning or destination.
- **Scanned page:** render one page at readable resolution and expect OCR text to need manual review, especially for columns, footnotes, and low-contrast scans.
- **Handwriting or complex form:** this skill does not transcribe handwriting or associate fields with labels. Use another specialized method and verify manually.

## Reporting OCR results

Say that the text was OCR-extracted, mention the selected language when useful, and call out low-confidence or manually corrected portions. Do not present the recognized transcript as an exact quotation unless you checked it against the source.
