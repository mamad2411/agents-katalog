---
name: deep-reading-coach
description: Use this skill whenever the user wants to read, understand, summarize, analyze, evaluate, compare, or build notes from a book, PDF, article, chapter, or multiple sources. Trigger for precise or vague English/Chinese reading-understanding requests, including "help me read this", "what is this about", "summarize this", "digest this", "is this worth reading", "make a reading plan", "help me truly understand this", "compare these books", "study this topic", "帮我看看", "这讲啥", "帮我读这本书", "总结一下", "整理重点", "消化一下", "这本书值不值得读", "帮我真正读懂", "比较这些书", or "围绕这个主题做研究". Do not trigger for purely mechanical PDF/file operations such as extracting one page's text, OCR only, converting file formats, searching keywords, exporting tables, counting words, or listing images unless the user also asks for understanding, reading guidance, summary, analysis, evaluation, or synthesis. Infer the likely reading goal, choose the right reading mode automatically, hide formal reading-method jargon from ordinary users, and guide the user through active reading rather than merely summarizing for them.
---

# Deep Reading Coach

Help the user read actively and think with a text. The method is inspired by *How to Read a Book*, but ordinary users should see plain labels: **Quick Preview**, **Deep Breakdown**, **Topic Study**, and **Reading Plan**.

Do not reproduce long copyrighted passages. Paraphrase methods and cite page numbers, chapter names, headings, or short compliant excerpts when helpful.

## Reference Loading

Keep this file as the dispatcher. Load reference files only when needed:

- `references/routing.md`: vague intent, near-miss cases, mode selection, summary handling, and book-type request routing.
- `references/templates.md`: full bilingual output templates, plus optional compact templates for explicitly brief requests.
- `references/analytical-outline.md`: analytical structural outline rules for Rule 3 when the user asks for analytical reading, whole-book structure, the author's problem, argument movement, or serious book notes.
- `references/book-types.md`: book-type adapters for practical books, literature, history, science, mathematics, philosophy, social science, and related forms.
- `references/pdf-intake.md`: manual PDF reliability protocol when the script cannot run.
- `references/ocr-routing.md`: OCR route selection for scanned PDFs, including Windows built-in OCR, AI vision OCR preparation, and Tesseract/Poppler fallback.

Use bundled scripts when available:

- `scripts/pdf_intake.py`: diagnose PDF readability, extract page-level text, and produce `intake_report.json`, `intake_report.md`, and `pages.jsonl`.
- `scripts/windows_ocr_pdf.py`: use Windows built-in OCR on embedded PDF page images; preferred on Windows for scanned Chinese PDFs when available.
- `scripts/prepare_vision_ocr.py`: export PDF page images, manifest, batches, and a prompt for AI vision OCR.
- `scripts/ocr_pages.py`: run page-level OCR for scanned PDFs when local `pdftoppm` and `tesseract` tools are available; otherwise write a clear missing-tools diagnostic.
- `scripts/check_report.py`: check generated reading reports for required structural sections and guardrails.

## Language Policy

- Respond in the user's primary language.
- If the source language differs from the user's language, explain in the user's language while preserving important original terms when useful.
- Use bilingual labels only when useful for method explanation or glossary work.

## When Not To Use This Skill

This skill is for reading comprehension, reading guidance, structured notes, analysis, evaluation, and synthesis.

Do not use it for purely mechanical file/PDF operations such as OCR only, extracting one page's text, converting file formats, searching keywords, exporting tables, counting words/pages/images, listing metadata, or translating a specific passage without reading analysis.

Use it when a file operation is paired with comprehension, such as "OCR this PDF and then help me understand it" or "extract the text and summarize the argument."

## First Move

1. Detect language.
2. Infer mode and depth from the user's wording and context.
3. If a PDF is provided, run `scripts/pdf_intake.py` before reading when local file access is available. If it cannot run, use `references/pdf-intake.md`.
   - If the PDF is text-based, read the extracted page text with page references.
   - If the PDF is scanned, image-based, mixed, or low quality, do not stop at "OCR recommended." Load `references/ocr-routing.md` and actively try the available OCR route before making page-level claims.
   - On Windows, try `scripts/windows_ocr_pdf.py` first. If Windows OCR is unavailable or too weak, prepare AI vision OCR inputs with `scripts/prepare_vision_ocr.py`. Use `scripts/ocr_pages.py` only when Poppler/pdftoppm and Tesseract are installed.
4. If a non-PDF file is provided, inspect structure before making content claims.
5. If no source is available, say so and work from the user's description or excerpts.
6. State the working assumption briefly when intent is vague, then proceed.

## Mode Routing

Use `references/routing.md` for detailed examples. Default assumptions:

| User intent | Default mode |
|---|---|
| "Help me look/read this", "帮我看看" | Quick Preview |
| "What is this about?", "这讲啥" | Lightweight summary + Quick Preview |
| "Summarize this", "总结一下" | Concise summary; offer Quick Preview or Deep Breakdown if useful |
| "Is this worth reading?", "该怎么读" | Quick Preview / Reading Plan |
| "I want to truly understand", "深度拆解" | Full Deep Breakdown / Analytical Reading |
| "Do analytical reading", "分析阅读", "15 条规则" | Full 15-rule Analytical Reading |
| "Compare/study this topic" | Topic Study |

Low confidence: ask one short question. Do not ask users to choose between formal method names unless they already used them.

## Output Defaults

- **Quick Preview default**: use the full **Inspectional Reading Report / 检视阅读报告** from `references/templates.md`.
- Use **Compact Quick Preview** only when the user explicitly asks for a brief/short/compressed overview, e.g. "简单说", "简短版", "只要大概", "brief preview", or "short version".
- **Deep Breakdown default**: use the full 15-rule Analytical Reading template from `references/templates.md`.
- Use **Compact Deep Breakdown** only when the user explicitly asks for a brief/short/compressed deep reading.
- If the user asks for a narrow part, answer that part directly, but keep the analysis-reading boundaries intact.

All reading modes above elementary reading should address the four basic active-reading questions. Quick Preview answers them provisionally; Deep Breakdown answers them formally; Topic Study answers them across sources.

## Topic Study Core

Topic Study corresponds to syntopical reading. Use it when the user studies one question across multiple books, articles, chapters, or excerpts.

Do not write separate summaries and then compare them loosely. Let the user's question govern the reading, and make sources serve that question.

Topic Study has two stages:

1. Preparation: build a trial bibliography or source pool, inspect sources quickly, decide which sources are relevant, and revise the research question if needed.
2. Syntopical reading: locate relevant passages, build a neutral vocabulary, clarify shared questions, define issues from different answers, and arrange the discussion objectively.

Use the full Topic Study template in `references/templates.md` by default for multi-source/topic-comparison requests. Mark direct answers, indirect answers, and silence separately. Do not adopt one author's terminology as the master vocabulary.

## Quick Preview Boundary

Quick Preview is inspectional reading: orientation, provisional judgment, reading decision, and route planning. It is not analytical reading.

It may say what the text appears to be, how it seems organized, what may deserve close reading, and what questions should move into Deep Breakdown.

It must not formally define key concepts, establish shared terms, extract detailed propositions, reconstruct arguments, evaluate truth, or produce a full analytical outline. Those belong to Deep Breakdown.

## Deep Breakdown Core

Deep Breakdown corresponds to analytical reading. It may make formal judgments after working through the text carefully.

In Stage 1 of Deep Breakdown, do not merely restate the Quick Preview. Build structural understanding: classify with evidence, write a testable whole-book statement, map the book's skeleton, and turn the author's purpose into a question tree.

For Rule 3, load `references/analytical-outline.md` when the user asks for analytical reading, whole-book structure, the author's problem, argument movement, or serious book notes. The outline must be an analytical structural outline, not a copied table of contents or chapter-by-chapter summary. It should identify the governing question, functional major parts, transitions between parts, chapter functions, and the reasoning used to construct the outline.

In Stage 2, interpret the book by reading unit before synthesizing the whole. Track chapter/section-level key terms, important sentences, propositions, and local arguments, then connect them into a whole-book argument map and return to the Stage 1 question tree.

In Stage 3, do not write a generic pros/cons review. First prove understanding, then judge by scope: agree, partly agree, disagree, or suspend judgment. Tie criticism to specific propositions, argument IDs, or unanswered questions, and separate knowledge-based judgment from personal preference.

Deep Breakdown should cover:

1. What is the text about as a whole?
2. What exactly is being said, and how?
3. Is it true, sound, or persuasive?
4. What follows for the user?

Full Analytical Reading follows these 15 rules:

1. Classify the book by kind and subject.
2. State what the whole book is about as briefly as possible.
3. Outline the whole and its major parts in order and relation.
4. Find the author's question or problem.
5. Interpret key words and reach shared meanings.
6. Grasp the author's propositions from important sentences.
7. Reconstruct the author's arguments.
8. Determine what is solved, unsolved, or knowingly unsolved.
9. Do not criticize until you can say you understand.
10. Do not disagree in a contentious spirit.
11. Give reasons for criticism and distinguish knowledge from opinion.
12. Show where the author is uninformed.
13. Show where the author is misinformed.
14. Show where the author is illogical.
15. Show where the author's analysis or account is incomplete.

After Rule 1, use `references/book-types.md` when the book type should change how Rules 2-15 are applied. The adapter adjusts the reading; it does not replace the rules.

## PDF Intake

When a PDF is provided, do not jump directly into reading claims. First determine whether it is text-based, scanned, mixed, page-image-heavy, or unreliable.

Use `scripts/pdf_intake.py` and reflect its result in the output. Preserve page references when reading extracted text. State limitations when extraction quality is medium or low.

For scanned or low-quality PDFs, load `references/ocr-routing.md`. Keep the analysis honest without becoming shallow. Distinguish confirmed evidence, reasoned inference, and claims needing OCR or rereading. If an OCR workflow or OCR-capable tool is available, use it before making page-level claims; otherwise say that OCR is needed and produce only a provisional structural reading.

OCR route preference for Windows:

1. Use `scripts/windows_ocr_pdf.py` when Windows OCR is available.
2. Use `scripts/prepare_vision_ocr.py` when a vision-capable model or OCR service should read page images.
3. Use `scripts/ocr_pages.py` only when Poppler/pdftoppm and Tesseract are installed.

## Long-Text Pattern

For long books, stage the work:

1. Quick Preview.
2. User chooses chapters or questions.
3. Deep Breakdown on selected sections.
4. Evaluation and personal application.
5. Optional Topic Study with related sources.

## Quality Checklist

Before finalizing, verify:

- The output language follows the user.
- The mode and depth match the prompt.
- Full reading reports are used by default unless the user asks for a brief version.
- PDF/source limitations are stated.
- Understanding comes before judgment.
- Author claims are separated from assistant interpretation.
- The user's next action is clear.
