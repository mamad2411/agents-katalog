---
name: gaia-compact-evidence-router-skill
description: Compact attachment-first router for GAIA-style tasks under a static ReAct
  loop with narrow evidence gathering, lightweight derivation, and strict answer-shape
  control.
allowed-tools:
- list_dir
- read_file
- read_json_file
- extract_pdf_text
- read_table
- image_metadata
- audio_transcribe
- ocr_image
- image_qa
- parse_docx
- parse_pptx
- extract_archive
- web_search
- fetch_url
- html_extract
- run_python
metadata:
  version: boot-al-compact-evidence-router
  split_source: train
  gold_input_quality: constructed_trajectory_weak_route_signal
  graph_policy: internal_route_graph_global_static
  skill_injection_mode: global_static
  stream: false
  max_executor_steps: 24
  evidence_scope: train_only
  repeat_scope: boot_from_train_gold
  learning_scope_after_boot: train_r1_only
  external_helper_models: forbidden
  no_instance_memory: true
---

Use Contract
- Start by reading `task.json`; if the workspace view is unclear, use `list_dir` once and then continue locally.
- Treat task wording, local attachments, and extracted local text as the first evidence layer.
- Browser automation is unavailable. For public web evidence, use `web_search` to locate, `fetch_url` to retrieve, and `html_extract` to isolate usable text.
- Use web only when the task truly needs external public facts, historical page states, source verification, or cited public records that local files do not contain.
- When media exists, stay local first: `image_metadata`, `ocr_image`, `image_qa`, or `audio_transcribe`.
- Use `run_python` for arithmetic, parsing, decoding, filtering, sorting, joins, unit conversion, coordinate math, and answer-shape checks.
- Each tool call should do one decisive job: locate a source, extract a field, compute a value, or verify final form.
- Final output must be a non-empty `<ANSWER>...</ANSWER>` and match the requested units, ordering, separators, casing, rounding, and cardinality.

Training Signals
- Gold trajectory evidence here is weak and mostly constructed. Use it as distribution pressure only: attachment-first routing is common, short derivations are common, and exact answer shape is often decisive.
- Reusable path patterns are concentrated around local tables, local text extraction from documents or archives, OCR or audio transcription, narrow public-source verification, and lightweight Python synthesis.
- Common failure guards recur: wrong scope date, wrong subset, wrong unit, wrong sort order, wrong surface form copied from a nearby field, or an answer that omits a requested sign, separator, or format.
- Default bias: pick the smallest evidence chain that can close the task inside the step budget.

Route Table
| Signal | Primary route | Recommended tools | Stop when |
| --- | --- | --- | --- |
| Spreadsheet, roster, workbook, matrix, inventory | parse then normalize | `read_table`, `run_python` | the target rows and requested field or aggregate are isolated |
| PDF, text file, rich document, archive, citation bundle | expand then extract | `extract_archive`, `extract_pdf_text`, `read_file`, `parse_docx`, `parse_pptx`, `run_python` | the decisive passage or table is in local text |
| Image, scan, screenshot, board, label, diagram, music sheet | observe then structure | `image_metadata`, `ocr_image`, `image_qa`, `run_python` | visible content becomes discrete facts, text, counts, or positions |
| Audio, spoken instructions, narrated clue | transcribe then normalize | `audio_transcribe`, `run_python` | the relevant spoken tokens or numbers are recovered cleanly |
| Pure logic, arithmetic, decoding, geometry, comparison, ordering | derive locally | `run_python`, `read_file`, `read_json_file` | the exact output value or set is computed from available facts |
| Public page, official record, archive snapshot, cited article | narrow lookup then verify | `web_search`, `fetch_url`, `html_extract`, `run_python` | a source-locked passage covers the exact entity, date, and scope |

## Phase: INIT
First action: read `task.json`. Route immediately from the question plus attachment suffixes to the shortest decisive local path.
- Route selection: choose local extraction if any attachment or embedded data appears; choose direct derivation if the prompt itself contains all facts; choose web fallback only when external public evidence is explicitly required.
- Recommended tools: `read_json_file`, then `list_dir` only if needed.
- Stop condition: you know the answer shape, the likely evidence location, and the next single decisive tool call.
- Failure guard: do not begin with `web_search` before confirming whether local files already contain the target evidence.
- Final: if the question already provides enough information and format is explicit, answer immediately.

## Phase: LOCAL_LOCK
Classify all local materials before branching deeper.
- Route selection: use when attachments, archives, or local reference files are present; map each item to table, text, archive, image, audio, or mixed media.
- Recommended tools: `list_dir`, `read_json_file`, `read_file`, `image_metadata`, `extract_archive`.
- Stop condition: each relevant local artifact has a concrete extraction path and irrelevant files are ignored.
- Failure guard: filenames can mislead; rely on actual suffix, visible structure, and extracted contents rather than assumptions.
- Final: if a local artifact already exposes the exact requested field or string, answer immediately.

## Phase: TEXT_TABLE_PATH
Turn local structured material into queryable facts.
- Route selection: use for spreadsheets, PDFs, docx, pptx, txt, extracted archives, rosters, qualifications, inventories, captions, and reference lists.
- Recommended tools: `read_table`, `extract_pdf_text`, `parse_docx`, `parse_pptx`, `read_file`, `extract_archive`, `run_python`.
- Stop condition: the target subset, cited passage, row group, or candidate field list is extracted into clean text or rows.
- Failure guard: watch header shifts, merged cells, duplicate labels, row-order traps, and requests that demand the source surface form exactly as written.
- Final: if the extracted rows or passage directly answer the question and the requested presentation is clear, answer immediately.

## Phase: MEDIA_PATH
Convert local media into discrete evidence without leaving the workspace.
- Route selection: use when the task depends on visible text, object identity, board state, layout, note letters, labels, or spoken content.
- Recommended tools: `image_metadata`, `ocr_image`, `image_qa`, `audio_transcribe`, `run_python`.
- Stop condition: the media yields stable tokens, numbers, entities, positions, or transcript snippets sufficient for a direct answer or a short derivation.
- Failure guard: separate observation from inference; if OCR and image or audio interpretation disagree on a decisive token, spend one step resolving the conflict locally.
- Final: if the recovered media facts already match the requested answer form, answer immediately.

## Phase: WEB_VERIFY
Use narrow public-source lookup only when the task needs evidence outside the workspace.
- Route selection: use for public facts, official databases, historical page states, cited papers, public logs, external source chains, or verification of a locally identified entity.
- Recommended tools: `web_search`, `fetch_url`, `html_extract`, `run_python`.
- Stop condition: one or two retrieved passages pin down the exact entity, date, edition, revision, or scope required by the prompt.
- Failure guard: search with tight anchors from the question, including date or source type when available. If results are noisy, reformulate once with narrower anchors and keep only source-supported claims.
- Final: if a retrieved passage cleanly supplies the answer in the requested scope and form, answer immediately.

## Phase: DERIVE_CHECK
Compute, compare, intersect, and format exactly.
- Route selection: use when the answer requires arithmetic, filtering, chronology, set operations, sorting, ratio comparison, route counting, decoding, unit conversion, or answer-shape normalization.
- Recommended tools: `run_python` plus the extractor that produced raw facts.
- Stop condition: the requested value, string, or ordered list is reproduced from extracted evidence and survives a cheap consistency check.
- Failure guard: verify variable identity, endpoint inclusion, threshold direction, unit scale, rounding precision, alphabetical or source order, separator choice, and any requirement to keep or remove articles, punctuation, or signs.
- Final: if the computed result already matches the required surface form, answer immediately.

Answer Guard
- You may answer from any phase once the evidence chain supports the exact requested form.
- Keep the final payload minimal: only the requested number, string, list, date, or phrase inside `<ANSWER>...</ANSWER>`.
- Preserve source spelling and casing when asked for text as written; normalize only when the prompt explicitly asks for transformed case, ordering, singularization, or punctuation removal.
- For numeric answers, confirm unit, sign, decimal places, thousands separators, rounding rule, and whether the task wants a bare number or a labeled value.
- For lists, confirm item count, deduplication, ordering rule, and separator formatting.
- For date or chronology tasks, confirm the referenced snapshot, revision, census year, publication date, or archive date before finalizing.
- If two candidate answers remain, use one more discriminating tool call; guessing burns the step budget and damages answer precision.