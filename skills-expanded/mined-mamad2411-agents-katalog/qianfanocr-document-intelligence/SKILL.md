---
name: qianfanocr-document-intelligence
description: >
  Analyze image files, image URLs, PDF files, and PDF URLs when the task requires recognizing,
  understanding, extracting, answering questions about, or locating content from the visual input.
  Typical uses include document parsing, layout analysis, element recognition, OCR, key information
  extraction, chart understanding, and document VQA. Do not use for plain text, structured data,
  code files, image-processing tasks, or cases where the needed information is already available in
  text form.
---

# Qianfan OCR Document Intelligence

This skill orchestrates visual understanding for images and PDFs. It does not implement a vision
model itself. It selects the right analysis mode, prepares inputs, invokes the bundled CLI, and
returns a structured result for the upstream agent.

## Required Execution Order

Always follow this order:

1. Check whether `QIANFAN_TOKEN` is already available.
2. If the token is missing, stop immediately and ask the user for the API Key.
3. If the user provides the API Key, write it to `<skill-root>/.env` as `QIANFAN_TOKEN=...`.
4. Only after the token is available, continue to mode selection, reference loading, and CLI calls.

This token preflight takes precedence over all later rules in this skill. Do not read
`references/*.md`, do not select a mode, and do not call any bundled script until the token check
has passed.

## API Key Setup

Before first use, make sure `QIANFAN_TOKEN` is available either in the process environment or in
`<skill-root>/.env`.

If the token is missing, ask the user in Chinese:

```text
QIANFAN_TOKEN 环境变量未设置。请提供百度千帆 API Key。
如果您暂时没有 API Key，请到 https://cloud.baidu.com/product-s/qianfan_home 注册获取。
```

If the user provides the key, persist it to `<skill-root>/.env` before continuing. Do not rely on
a temporary `export QIANFAN_TOKEN=...` as the only storage mechanism.

Do not assume a bundled default token exists.

## Bundled Tools

- `scripts/qianfan_ocr_cli.py`: send one or more images to the backend VLM.
- `scripts/pdf_to_images.py`: convert one or more PDFs into per-page images before calling the VLM.
- `scripts/render_doc_markdown.py`: replace document-parsing image placeholders with cropped image files.
- `scripts/run_document_parsing.py`: run document parsing end-to-end and always render image placeholders.
- `scripts/run_pdf_document_parsing.py`: run PDF document parsing end-to-end and export combined markdown, shared assets, and per-page markdown files.
- `scripts/run_document_parsing_with_layout.py`: run document parsing with layout and export markdown, layout JSON, and a layout overlay image.
- `scripts/run_layout_analysis.py`: run layout analysis and export `_layout.json` plus a layout overlay image.
- `scripts/run_element_recognition.py`: run element recognition and save the result as a sibling markdown file.

Always call scripts by absolute path. In Codex, use the installed absolute skill path instead of a
bare relative path.

Examples:

```bash
python3 "<skill-root>/scripts/qianfan_ocr_cli.py" "<prompt>" --image <path_or_url>
python3 "<skill-root>/scripts/pdf_to_images.py" <pdf_or_url> --output-dir <dir>
python3 "<skill-root>/scripts/render_doc_markdown.py" parsed.md --image <page_image> --output-dir <assets_dir> --output-markdown <rendered_md>
python3 "<skill-root>/scripts/run_document_parsing.py" <image_or_pdf>
python3 "<skill-root>/scripts/run_pdf_document_parsing.py" <pdf> --pages all
python3 "<skill-root>/scripts/run_document_parsing_with_layout.py" <image_or_pdf>
python3 "<skill-root>/scripts/run_layout_analysis.py" <image_or_pdf>
python3 "<skill-root>/scripts/run_element_recognition.py" <cropped_image_or_pdf> --element-type <text|formula|table>
```

## Trigger Rules

Trigger this skill only when all of the following are true:

- The task involves one or more image files or URLs, or one or more PDF files or URLs.
- The agent must recognize, understand, extract, answer questions about, or locate content inside
  those images or PDFs.
- The relevant information cannot be obtained from existing plain-text sources already available to
  the agent.

Do not trigger when:

- The file is plain text, structured data, or source code that can be read directly.
- The user is asking for image-processing or PDF-processing code rather than visual understanding.
- The image/PDF path or URL is mentioned incidentally and no visual understanding is requested.
- A previous invocation already answered the same question and repeating the call would be redundant.

## Input Preparation

### Image inputs

- Pass local image paths or image URLs directly to `qianfan_ocr_cli.py`.
- Use one call per unrelated image.
- Use repeated `--image` flags only when cross-image reasoning is required.

### PDF inputs

- If the input is a PDF, convert it to page images first with `scripts/pdf_to_images.py`.
- For single-page questions, analyze only the relevant page when known.
- For multi-page PDFs, keep page order and label outputs with page numbers.
- If the PDF already has reliable selectable text and the task is pure text retrieval, do not use
  this skill; read the text directly.

Recommended PDF flow:

```bash
python3 "<skill-root>/scripts/pdf_to_images.py" report.pdf --output-dir /tmp/report-pages
python3 "<skill-root>/scripts/qianfan_ocr_cli.py" "<prompt>" --image /tmp/report-pages/report-p001.png
```

## Analysis Modes

Select exactly one primary mode per call. If needed, make a second, more specific call after an
initial pass.

| Mode | Use When | Goal |
|------|----------|------|
| `document parsing` | Need document structure, text, formulas, tables, and image placeholders from an image/PDF | Output Markdown parsing result |
| `layout analysis` | Need all layout elements with positions and categories | Output layout elements with bbox and category |
| `element recognition` | Need precise recognition on cropped elements such as text blocks, formulas, or tables | Output exact recognition for the cropped element |
| `document parsing with layout` | Need both structural parsing and layout detection in one workflow | Output Markdown parsing plus layout analysis |
| `general ocr` | Need all visible text without document structure | Extract all visible text lines |
| `key information extraction` | Need key fields from cards, forms, receipts, invoices, contracts, or similar documents | Extract key information in structured form |
| `chart understanding` | Need chart captions, structured chart content, or chart QA | Understand and structure chart content |
| `doc vqa` | Need answers to specific questions about a document image/PDF | Answer questions grounded in the document |

## Mode Selection Heuristics

- Use `document parsing` for full-page document understanding where output should be Markdown and
  preserve hierarchy.
- Use `layout analysis` when bounding boxes and categories are the main output.
- Use `element recognition` only after cropping the target region or when the user provides a
  single focused element image.
- Prefer `scripts/run_element_recognition.py` for `element recognition` so the result is written
  next to the source file as a single markdown file without any assets directory.
- Use `document parsing with layout` when both Markdown reconstruction and layout boxes are needed.
- Use `general ocr` for screenshots, signs, posters, and simple document text extraction where
  layout is not important.
- Use `key information extraction` for forms, certificates, IDs, invoices, receipts, contracts,
  and other field-centric documents.
- For `key information extraction`, if the user asks for all key-value information or all fields
  without naming a concrete field list, use the schema-free prompt path instead of inventing an
  explicit schema.
- Use `chart understanding` for plots, dashboards, and chart-heavy report pages.
- Use `doc vqa` for targeted questions such as totals, dates, clauses, page content, or whether a
  document contains a specific item.

## Reference Loading Rule

Only after token preflight has passed and after selecting the mode, always read the corresponding
file in `references/` before composing the prompt or calling any script.

- `document parsing` -> `references/document-parsing.md`
- `layout analysis` -> `references/layout-analysis.md`
- `element recognition` -> `references/element-recognition.md`
- `document parsing with layout` -> `references/document-parsing-with-layout.md`
- `general ocr` -> `references/general-ocr.md`
- `key information extraction` -> `references/key-information-extraction.md`
- `chart understanding` -> `references/chart-understanding.md`
- `doc vqa` -> `references/doc-vqa.md`

Do not skip this step when a matching reference exists.

## Prompt Sourcing Rule

When the selected reference contains a prompt template, prompt rule, fixed prompt, output format, or
parameter recommendation, use that reference as the primary source of truth.

- Prefer the prompt in the corresponding `references/*.md` file over ad-hoc prompt writing.
- Reuse the reference prompt verbatim when it is marked as a fixed prompt or standard prompt.
- Reuse the reference output format requirements instead of inventing a new format.
- Only add task-specific details, such as the user question, selected keys, page number, or input
  scope, on top of the reference prompt.
- If you intentionally deviate from the reference prompt, state why in the intermediate reasoning and
  keep the deviation minimal.

## Parameter Mapping Rule

If the selected reference defines execution parameters, convert them into actual CLI flags or
request fields. Do not leave them as documentation-only notes.

Examples:

- `min_dynamic_patch = 8` -> pass `--min-dynamic-patch 8`
- `max_dynamic_patch = 24` -> pass `--max-dynamic-patch 24`
- thinking mode -> pass `--thinking`

Before running `qianfan_ocr_cli.py`, verify that the final command includes the parameter settings
required by the selected mode.

## Prompt Rules

- Write the VLM prompt in Chinese when the user is communicating in Chinese; otherwise use English.
- State the mode and output format explicitly in the prompt.
- Tell the model to mark anything uncertain as unclear / unreadable instead of guessing.
- For PDFs, mention page numbers in the prompt whenever multiple pages are analyzed.
- For cropped inputs used in `element recognition`, specify the element type: text, formula, table,
  figure caption, seal, signature block, and so on.
- For `document parsing` outputs that contain `![label](<box>[[...]]</box>)` placeholders, run
  `scripts/render_doc_markdown.py` before presenting the Markdown to users who need renderable
  local images.
- Prefer `scripts/run_document_parsing.py` over manually chaining `qianfan_ocr_cli.py` and
  `render_doc_markdown.py` when the task is standard document parsing.
- Prefer `scripts/run_pdf_document_parsing.py` for PDF document parsing when the user wants one
  markdown for the whole PDF plus per-page markdown files and a shared assets directory. Use
  `--request-mode joint` when selected PDF pages are semantically related and should be sent as
  one multi-image request. Use `--request-mode batch --concurrency <N>` when pages can be parsed
  independently and should run concurrently.
- Prefer `scripts/run_document_parsing_with_layout.py` for `document parsing with layout` so the
  final output includes markdown, `_layout.json`, and a rendered layout overlay image.

## CLI Strategy

- Default to one call per image or page.
- Use repeated `--image` flags only for cross-page or cross-image reasoning that truly depends on
  joint context.
- If multiple images should be processed independently rather than jointly, use
  `scripts/qianfan_ocr_cli.py --batch --concurrency <N>` or a dedicated runner instead of sending
  all images as one joint request.
- Use `--thinking` only for difficult document understanding tasks with ambiguous reading order or
  dense field relationships.
- Retry at most once per image/page, and only with a more specific prompt.

Read only the relevant reference file when needed, but do read that file before prompt construction:

- `references/document-parsing.md`
- `references/layout-analysis.md`
- `references/element-recognition.md`
- `references/document-parsing-with-layout.md`
- `references/general-ocr.md`
- `references/key-information-extraction.md`
- `references/chart-understanding.md`
- `references/doc-vqa.md`

## Output Contract

Return a structured result instead of raw model prose:

```text
=== VISUAL ANALYSIS RESULT ===
mode: <mode>
confidence: <high|medium|low>
input_type: <image|pdf>
image_count: <N>
page_count: <N or n/a>

answer:
<direct answer or summary>

evidence:
- <directly observed fact>

warnings:
- <uncertainty or limitation>

markdown:
<for document parsing modes>

layout:
- page: <n>
  category: <label>
  bbox: [x1, y1, x2, y2]

structured_data:
<for key information extraction / chart understanding>

recognized_elements:
<for element recognition>
=== END VISUAL ANALYSIS ===
```

## Conservatism Rules

- Separate observation from inference.
- Never invent text, values, fields, or boxes.
- Mark unreadable regions explicitly.
- For charts, distinguish exact values from estimated values.
- For PDFs, keep page attribution explicit: `page_1`, `page_2`, and so on.
- If page conversion or image quality is poor, mention that in `warnings`.
