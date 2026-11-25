---
name: document-understanding
description: Use when reading, inspecting, summarizing, comparing, or extracting information from user-provided documents, files, transcripts, articles, reports, slides, Markdown, HTML, PDFs, DOCX, PPTX, text notes, or mixed document bundles. Prefer this Skill when the main work is understanding source material and preserving evidence, structure, limitations, and relevant passages. Do not use for multi-source research, data computation, writing a new artifact, or editing files unless document understanding is the central step.
meta:
  version: 1
  display_name: 文档理解
  source: claude-office-skills data-extractor/pdf-extraction/table-extractor
  license: MIT
---

# Document Understanding

## Purpose

Understand source documents before producing conclusions, summaries, extractions, comparisons, or downstream work. The Skill owns the document-reading process: scope, structure mapping, evidence capture, extraction quality, and limitation reporting.

This Skill adapts document extraction and structure-inspection practices from reviewed open-source Skills, while removing their MCP, parser library, OCR, Office, and script assumptions. It describes how to reason over documents; it does not require any specific tool or output format.

## Use When

Use for:

- reading or explaining a document, article, report, policy, transcript, note, slide deck, PDF, DOCX, PPTX, HTML, Markdown, text file, or document bundle;
- summarizing or extracting key points, decisions, requirements, risks, entities, dates, obligations, tables, passages, or open questions from documents;
- comparing documents, versions, sections, policies, drafts, meeting notes, or source bundles;
- checking whether a document contains required information;
- preparing document-grounded context before writing, research, planning, data analysis, or code work.

Prefer this Skill over `research-synthesis` when the evidence comes mainly from provided documents rather than open-ended source gathering. Prefer `data-visual-report-builder` when the main work is calculation over tables or datasets.

## Do Not Use When

Do not use for:

- external research, source discovery, or freshness validation across many sources; use `research-synthesis`;
- statistical analysis or computation over structured data; use `data-visual-report-builder`;
- drafting or polishing new prose after the document is already understood; use `writing-and-editing`;
- formal Chinese official document drafting; use `official-document-drafting`;
- meeting-specific recap workflow; use `meeting-recap`;
- Office/PDF conversion, OCR, parser installation, file repair, export, or document automation.

## Material Gate

Before analyzing, identify:

- document set, file types, source paths or user-provided text blocks;
- user question and the expected use of the extracted understanding;
- required scope: whole document, specific pages/sections, tables, appendices, comments, revisions, or only relevant passages;
- required fidelity: quick gist, source-backed summary, exact extraction, comparison, compliance check, or handoff context;
- known limitations: unreadable pages, missing files, truncated pasted text, scans/images, language issues, stale version, or unclear authorship.

If the document or relevant section is not available, ask for the smallest missing material or produce only a scope-limited assessment.

## Workflow

1. Restate the document task in one line: what material is being inspected and what question must be answered.
2. Build a source inventory: document name or path, type, date/version when known, owner/author when known, and inspected scope.
3. Inspect first-hand material before relying on summaries or filenames.
4. Map structure before extracting conclusions: title, headings, sections, tables, figures, appendices, notes, metadata, page/slide order, and version cues.
5. Select the reading mode using `references/understanding-rules.md`: gist, targeted extraction, requirement mining, comparison, coverage check, or handoff context.
6. Extract evidence units with their context: section/page/heading, exact label, surrounding caveat, and whether the item is direct text or interpretation.
7. Preserve meaning when condensing. Keep names, dates, numbers, definitions, obligations, constraints, and qualifiers attached to the relevant claim.
8. Separate document facts, inferred meaning, user-provided assumptions, and missing or unreadable areas.
9. Validate coverage against the requested scope. If only part of a document was inspected, say so.
10. Hand off to the next Skill only after document facts and limitations are clear.

## Checks

- The inspected scope is visible.
- Important sections, tables, appendices, or caveats were not silently skipped.
- Extracted items preserve source context and do not flatten qualifications.
- Ambiguous wording stays ambiguous or is flagged.
- Missing, unreadable, stale, or truncated material is reported.
- No claim is made beyond the inspected document evidence.
- The next-step Skill, if any, receives facts and gaps rather than guesses.

## Outputs

Return whatever the user needs for the task: explanation, summary, extracted facts, section map, comparison notes, evidence list, requirement list, risks, action items, or handoff context. Do not force a fixed template when the user only needs a short answer.

## Boundary

Skill owns document understanding workflow, source inventory, structure mapping, evidence extraction, scope discipline, summarization/extraction quality, comparison reading, and limitation reporting.

It does not own XAgent tool schemas, parser selection, file permissions, OCR, Office/PDF conversion, document export, source discovery, data computation, artifact lifecycle, or final authority for unverified claims. It must not run shell, Python, Node, npm, curl, MCP, OCR, Office, parser-install, browser-open, or document-export commands by itself; those actions belong to XAgent tools visible in the current session.

## Resources

- `references/understanding-rules.md`: reading modes, extraction discipline, comparison workflow, table handling, and coverage checks.
- `LICENSE`: source and license notice.
