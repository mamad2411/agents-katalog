---
name: docs-pdf-clean-output
description: Use automatically whenever Claude produces a finished document or file for the user - Word (.docx), PDF, slides, markdown reports, emails, posted text. Runs the draft through human-writing-mode and originality-guard before export, then builds the file with the docx/pdf/pptx skills, sets clean metadata (title, user as author), and checks the output opens correctly. Not for code files, data exports, or internal scratch notes.
---

# Docs / PDF Clean Output

## Purpose
Make every delivered document read as natural, original writing and be a clean, correct file. Pipeline: draft -> humanize -> originality check -> build -> verify.

## When to use
User asks for a document, PDF, report, proposal, thesis section, letter, email, slide deck, or any text deliverable.

## When NOT to use
- Code, notebooks, spreadsheets of data, JSON.
- Internal notes or tool output the user will not send on.

## Inputs
Content or topic, audience, format (docx/pdf/pptx/md), length, citation style, user's name/title for metadata, any sources or style samples.

## Core workflow
1. Plan structure with the user's purpose (headings, sections, length); ask only if format or audience is missing.
2. Draft with real facts only; collect sources in a log when anything is borrowed.
3. Apply `human-writing-mode`: plain voice, varied rhythm, concrete detail, no AI tells.
4. Apply `originality-guard`: own wording, quotes marked, citations and references added, spot-check.
5. Build the file with the matching skill: `docx` for Word, `pdf` for PDF, `pptx` for slides (or markdown if asked). Use real styles for headings, lists, tables; embed fonts for PDF; add alt text for images.
6. Set metadata: title, author = the user (or blank), subject; no leftover prompts, comments, tracked changes or template placeholder text. Do not strip any AI-use disclosure the user's institution or publisher requires.
7. Verify: open the file (render PDF pages or convert docx), check page breaks, headings, tables, numbers, references; run `pdf-toolkit` for metadata/encryption checks when the PDF will be shared externally.
8. Deliver the file path and a short note: what it contains, checks done, anything the user must fill in.

## Decision rules
- Format follows the audience: formal for academic/legal, conversational for email and posts.
- Keep citations style consistent with the user's requirement.
- If a fact or source cannot be verified, flag it in the note instead of embedding it.
- Language: write in the language requested; keep names, terms and numbers exact.

## Edge cases and failure handling
- Tool for the format is unavailable -> produce markdown and explain how to convert.
- Large document -> build section by section and verify each before merging.
- Table or figure breaks across pages -> adjust layout rather than shrink text below readable size.
- User asks for a guaranteed "AI-free" or "0% plagiarism" result -> explain that no skill can guarantee a detector or checker score; deliver original, well-cited, human-voiced work and recommend their institution\'s own checker for final confirmation.

## Validation
- Humanizer tells absent; originality self-check passed; sources real.
- File opens, fonts/pages correct, metadata clean, links work.
- Numbers, names and dates match the input.

## Output requirements
The finished file (path) plus a 3-5 line summary of checks and open items. Short `DONE` style; no process narration.

## Example
```text
Request: "Write a 2-page proposal PDF for a POS pilot in Dhaka."
Flow: outline -> draft with the user's facts -> human voice pass -> no sources borrowed (log empty) -> build with pdf skill -> check 2 pages, metadata author = user -> deliver /out/pos-pilot-proposal.pdf
```

## Related skills
`human-writing-mode`, `originality-guard`, `ai-text-humanizer`, `docx`, `pdf`, `pptx`, `pdf-toolkit`, `citation-management`.
