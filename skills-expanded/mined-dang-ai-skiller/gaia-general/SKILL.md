---
name: gaia-general-skill
description: Global static GAIA skill for web, file, multimodal, calculation, evidence, and final-answer discipline.
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
  benchmark: GAIA
  generator: Manus
  baseline: manus_plain_skill
  generation_constraints: gaia_original_annotation_gold_no_instance_memory_v4
  allowed_gold_input: train83_original_annotation_gold
  skill_injection_mode: global_static
  runtime_state_transitions: disabled
  date: "2026-05-20"
---

# GAIA General Skill

## Global Operating Loop

For every GAIA task, follow this loop until a final answer is produced:

1. **Parse the question** — extract the answer contract (format, unit, precision, constraints).
2. **Triage inputs** — check for attached files; if present, inspect them first.
3. **Plan evidence path** — decide whether the answer requires web research, file analysis, multimodal processing, calculation, or a combination.
4. **Execute evidence gathering** — use the minimum tool calls needed; record each intermediate finding.
5. **Validate evidence** — cross-check with a second source or method when feasible.
6. **Compute final answer** — apply any required arithmetic, filtering, or formatting.
7. **Normalize output** — strip trailing punctuation, units unless requested, and whitespace; match the exact format the question demands.
8. **Emit final answer** — return only the concise answer string.

If any step fails or yields ambiguous results, invoke the Recovery section before answering.

## Answer Contract Extraction

Before any research or computation, identify:

- **Expected type**: number, name, date, list, yes/no, short phrase.
- **Precision**: "round up to next integer", "two decimal places", "exact title as it appears".
- **Constraints**: "use Wikipedia 2022 version", "between years X and Y", "only articles not reviews".
- **Format markers**: "return it as appearing in the spreadsheet", "give the shortest name".

Write the contract mentally before proceeding. Every subsequent step must serve the contract.

## Source and Evidence Discipline

- Prefer authoritative primary sources: official archives, Wikipedia, government databases, institutional pages.
- When a question specifies a source (e.g., "use English Wikipedia"), restrict evidence to that source.
- When multiple sources conflict, prefer the source closest to the question's specification.
- Never fabricate a URL, title, or numeric value. If a source cannot be found, try alternative search terms before concluding.
- Record the provenance of every factual claim: which URL or file produced it.

## Web Search and Stale-Source Handling

### Search Strategy

```
web_search(query="<targeted keywords from question>")
```

- Start with the most specific query derived from the question.
- If zero relevant results, broaden by removing qualifiers one at a time.
- If the question references a specific website or database, include the site name in the query.

### Navigating Results

```
fetch_url(url="<result_url>")
html_extract(url="<result_url>", selector="<css_selector>")
```

- Open the most promising result first.
- If a page is paywalled, archived, or returns 404, try the Wayback Machine or an alternative mirror.
- For Wikipedia, navigate directly to the relevant section using anchors or table of contents.

### Stale or Missing Data

- If a page has been updated since the question's reference date, look for archived versions.
- If a count or list is needed, verify by checking the archive/filter interface of the target site rather than trusting a single search snippet.

## Local File Triage

When the task includes an attached file:

1. **Identify format** — use `list_dir` to see the filename and extension.
2. **Route by type**:
   - `.xlsx`, `.csv`, `.tsv` → `read_table`
   - `.pdf` → `extract_pdf_text`
   - `.docx` → `parse_docx`
   - `.pptx` → `parse_pptx`
   - `.json`, `.jsonl` → `read_json_file`
   - `.zip`, `.tar`, `.gz`, `.7z` → `extract_archive`, then re-triage contents
   - `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, `.tiff` → `ocr_image` or `image_qa`
   - `.mp3`, `.wav`, `.m4a`, `.ogg`, `.flac` → `audio_transcribe`
   - Other text → `read_file`
3. **Inspect before computing** — always read or preview the file content before applying calculations.
4. **Handle multi-sheet spreadsheets** — check all sheet names; the relevant data may not be on the first sheet.

## Multimodal Handling

### Images

```
ocr_image(path="<file_path>")
image_qa(path="<file_path>", question="<specific_question>")
image_metadata(path="<file_path>")
```

- Use `ocr_image` when the answer is text visible in the image.
- Use `image_qa` when the answer requires visual understanding (colors, objects, spatial relations).
- Use `image_metadata` to check EXIF data, dimensions, or embedded metadata.
- If OCR returns garbled text, try `image_qa` with a targeted question instead.

### Audio

```
audio_transcribe(path="<file_path>")
```

- Transcribe first, then search the transcript for the answer.
- If the question asks about a specific segment, note timestamps if available.
- For non-English audio, the transcription tool may still produce usable output; verify key terms.

## Python Calculation and Validation

```
run_python(code="<python_code>")
```

### When to Use Python

- Any arithmetic beyond trivial single-step operations.
- Percentage calculations, rounding, counting, filtering, sorting.
- Date arithmetic (days between dates, day of week).
- String manipulation (extracting substrings, regex matching).
- Statistical computations (mean, median, percentages of populations).

### Calculation Discipline

- Always use Python for multi-step math; never compute mentally.
- Print intermediate results to verify each step.
- When rounding, use the exact method specified: `math.ceil`, `math.floor`, `round`.
- For currency or unit conversions, state the conversion factor and its source.
- Double-check by reversing the calculation or using an alternative method.

### Common Patterns

```python
import math
# Percentage then round up
result = math.ceil(total * percentage / 100)

# Count items matching criteria
count = len([x for x in items if condition(x)])

# Filter by date range
filtered = [r for r in records if start_year <= r['year'] <= end_year]
```

## Multi-Hop Research

Many GAIA tasks require chaining multiple lookups:

1. **Identify the chain** — the question often contains nested references ("the species whose shell is object X in museum Y").
2. **Resolve one hop at a time** — find the intermediate entity before searching for the final answer.
3. **Verify synonyms and redirects** — scientific names may have accepted vs. deprecated forms; check taxonomy databases.
4. **Track the chain** — maintain a mental list: Hop 1 → Entity A, Hop 2 → Entity B, Final → Answer.
5. **Cross-validate** — if possible, find a source that connects the full chain to confirm.

### Handling Name Variations

- For species: check World Register of Marine Species, ITIS, or Wikipedia for accepted names.
- For people: check birth names, stage names, married names.
- For places: check historical names, transliterations, abbreviations.
- For organizations: check acronyms, former names, parent organizations.

## Evidence Bookkeeping

Within the current task only, maintain a running evidence log:

- After each tool call that produces useful information, note: `[Evidence] <source>: <finding>`.
- Before computing the final answer, review all evidence entries for consistency.
- If evidence conflicts, investigate further before answering.
- Do not carry evidence across tasks.

## Final Answer Normalization

Apply these rules to the final answer:

1. **Numbers**: remove leading zeros; use the requested precision; omit units unless explicitly requested.
2. **Names/Titles**: preserve exact capitalization and punctuation as found in the authoritative source; do not add quotes unless the question asks for them.
3. **Lists**: use comma separation unless another format is specified; maintain the requested order.
4. **Yes/No**: use the exact word requested (yes/no, Yes/No, true/false).
5. **Dates**: use the format specified; if unspecified, use the format found in the source.
6. **Rounding**: apply the exact rounding method specified (round up = ceil, round down = floor, round = nearest).

### Common Normalization Pitfalls

- "Round up to the next integer" means `math.ceil`, not `round`.
- "As appearing in the spreadsheet" means copy the exact string including any typos or unusual formatting.
- "The shortest name" means choose the briefest valid name for the character/entity.
- Trailing periods, commas, or spaces must be stripped unless they are part of the answer.

## Recovery When the First Path Fails

If the primary approach does not yield a clear answer:

1. **Reformulate search queries** — use synonyms, alternative phrasings, or the entity's full official name.
2. **Try alternative sources** — if one database is down, try another (e.g., Google Scholar instead of direct journal access).
3. **Decompose the problem** — break a complex question into smaller verifiable sub-questions.
4. **Check assumptions** — re-read the question for constraints you may have missed.
5. **Use Python for brute-force** — if a small search space exists, enumerate possibilities programmatically.
6. **Fallback to broader search** — remove date/source constraints temporarily to find any relevant information, then verify it matches the original constraints.
7. **Verify partial answers** — if you have a partial answer, check whether it satisfies all constraints before submitting.

### When to Stop Searching

- If three different search strategies yield no results, consider whether the question has a trick or requires a different interpretation.
- If you have strong evidence for an answer but cannot find a second source, proceed with the best-supported answer.
- Never guess without evidence. If truly stuck, state the most evidence-supported answer.

## Tool-Use Quick Reference

| Scenario | Primary Tool | Fallback |
|----------|-------------|----------|
| Find a fact online | `web_search` → `fetch_url` | `html_extract` with selector |
| Read spreadsheet | `read_table` | `run_python` with openpyxl/pandas |
| Read PDF | `extract_pdf_text` | `run_python` with PyPDF2 |
| Identify image content | `image_qa` | `ocr_image` |
| Transcribe audio | `audio_transcribe` | — |
| Extract from archive | `extract_archive` → re-triage | — |
| Compute/validate | `run_python` | — |
| Parse structured data | `read_json_file` | `read_file` + `run_python` |
