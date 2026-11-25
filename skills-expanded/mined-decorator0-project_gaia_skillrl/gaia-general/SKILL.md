---
name: gaia-general-skill
description: State-machine GAIA skill with scoped memory, routed evidence collection, verification, and exact short-answer output.
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
  version: "state-machine-seed-0.1"
  graph_version: "0.1"
  entry_state: INIT
  answer_state: CONCLUDE
---

Memory protocol:
- Durable memory is only `task_summary`, `answer_schema`, `format_constraints`, `attachments`, `route`, `evidence_cards`, `candidate_answer`, and `verification_status`.
- Long tool outputs are local to the current phase. When leaving a phase, compress useful facts into evidence cards.
- Evidence card format: `source`, `fact`, `use_for_answer`.
- Each phase should use only the visible memory listed for that phase plus fresh tool results from that phase.

Graph:
`INIT -> TASK_PARSE -> EVIDENCE_ROUTE`

Then choose one branch:
- `PROMPT_SOLVE -> COMPUTE_OR_COMPARE`
- `LOCAL_PARSE -> COMPUTE_OR_COMPARE`
- `MEDIA_PARSE -> COMPUTE_OR_COMPARE`
- `WEB_RETRIEVE -> WEB_EXTRACT -> COMPUTE_OR_COMPARE`

Final path:
`COMPUTE_OR_COMPARE -> CROSS_CHECK -> FORMAT_VERIFY -> CONCLUDE`

Repair path:
`COMPUTE_OR_COMPARE/CROSS_CHECK/FORMAT_VERIFY -> EVIDENCE_ROUTE/LOCAL_PARSE/MEDIA_PARSE/WEB_RETRIEVE/WEB_EXTRACT/COMPUTE_OR_COMPARE`

## Phase: INIT

Visible memory: task directory only.

Goal: inspect the local task layout.

Allowed tools: `list_dir`, `read_json_file`

Actions:
- Call `list_dir` on `.`.
- Call `read_json_file` on `task.json`.
- Record exact attachment filenames.

Exit handoff:
- `task_summary`: one-sentence task summary.
- `attachments`: exact filenames and extensions.

Next: `TASK_PARSE`

## Phase: TASK_PARSE

Visible memory: `task_summary`, full prompt from `task.json`, `attachments`.

Goal: turn the prompt into a compact task contract.

Allowed tools: none

Extract:
- `answer_schema`: number, name, list, exact phrase, chess move, color, code, city, title, or other.
- `format_constraints`: units, scale, rounding, decimals, comma rules, ordering, casing, exact-source wording, date/version constraints.
- `evidence_requirements`: attachment, web source, prompt-only logic, media, or multi-hop chain.

Exit handoff:
- `answer_schema`
- `format_constraints`
- `evidence_requirements`

Next: `EVIDENCE_ROUTE`

## Phase: EVIDENCE_ROUTE

Visible memory: `task_summary`, `attachments`, `answer_schema`, `format_constraints`, `evidence_requirements`.

Goal: choose the smallest evidence route that can solve the task.

Allowed tools: none

Route rules:
- If a local attachment is present and relevant, choose `LOCAL_PARSE` or `MEDIA_PARSE`.
- If the prompt is self-contained logic, wordplay, table reasoning, or combinatorics, choose `PROMPT_SOLVE`.
- If the prompt names a webpage, source, date, version, publication, public log, YouTube video, or external entity chain, choose `WEB_RETRIEVE`.
- For images, choose `MEDIA_PARSE`: `ocr_image` for visible text, `image_qa` for visual semantics.
- For audio files, choose `MEDIA_PARSE`.

Exit handoff:
- `route`: one of `PROMPT_SOLVE`, `LOCAL_PARSE`, `MEDIA_PARSE`, `WEB_RETRIEVE`.
- `route_reason`: short reason.

Next: `PROMPT_SOLVE`, `LOCAL_PARSE`, `MEDIA_PARSE`, or `WEB_RETRIEVE`

## Phase: PROMPT_SOLVE

Visible memory: `task_summary`, full prompt, `answer_schema`, `format_constraints`.

Goal: solve self-contained prompt tasks without unnecessary web use.

Allowed tools: `run_python`

Use this for:
- Logic equivalences, transformations, counting relatives, list filtering, game/probability puzzles, Rubik/color constraints, prompt-instruction traps.

Actions:
- Use explicit reasoning or `run_python` for enumeration, arithmetic, search, sorting, probabilities, and constraint solving.
- Preserve intermediate values needed for verification.

Exit handoff:
- `evidence_cards`: prompt-derived facts and computed facts.
- `candidate_work`: compact calculation or reasoning trace.

Next: `COMPUTE_OR_COMPARE`

## Phase: LOCAL_PARSE

Visible memory: `attachments`, `answer_schema`, `format_constraints`, `evidence_requirements`.

Goal: parse local non-media attachments into usable evidence.

Allowed tools: `read_file`, `read_json_file`, `extract_pdf_text`, `read_table`, `parse_docx`, `parse_pptx`, `extract_archive`, `html_extract`, `run_python`

Tool routing:
- `.xlsx` or `.csv`: `read_table`, then `run_python` if cell colors, coordinates, aggregation, or pathfinding are needed.
- `.docx`: `parse_docx`.
- `.pptx`: `parse_pptx`.
- `.txt`, `.py`, `.json`, `.html`: `read_file`; execute or inspect `.py` with `run_python` when needed.
- archives: `extract_archive`, then route extracted files.
- PDFs: `extract_pdf_text`.

Exit handoff:
- `evidence_cards`: local file facts with file path and relevant row, cell, slide, line, or code output when available.
- `parse_status`: success, partial, or blocked.

Next: `COMPUTE_OR_COMPARE`

## Phase: MEDIA_PARSE

Visible memory: `attachments`, `answer_schema`, `format_constraints`, `evidence_requirements`.

Goal: extract evidence from image and audio attachments.

Allowed tools: `image_metadata`, `ocr_image`, `image_qa`, `audio_transcribe`, `run_python`

Tool routing:
- Audio: use `audio_transcribe`, then extract only requested fields.
- Image text or worksheet image: use `ocr_image`.
- Chess, visual layout, objects, charts, board states, or spatial reasoning: use `image_qa` with the task question or a tight subquestion.

Exit handoff:
- `evidence_cards`: transcript snippets or visual facts.
- `parse_status`: success, partial, or blocked.

Next: `COMPUTE_OR_COMPARE`

## Phase: WEB_RETRIEVE

Visible memory: `task_summary`, `answer_schema`, `format_constraints`, `evidence_requirements`, current entity chain if any.

Goal: find candidate source pages.

Allowed tools: `web_search`

Search rules:
- Include names, dates, source names, exact phrases, page titles, version constraints, and requested artifact type.
- For YouTube tasks, search for transcript, caption, quote, scene description, species, or visible event.
- For multi-hop tasks, search one hop at a time and preserve the entity chain.
- After a failed search, change the query strategy.

Exit handoff:
- `candidate_sources`: URLs or page titles with why they matter.
- `entity_chain`: intermediate entities found so far.

Next: `WEB_EXTRACT`

## Phase: WEB_EXTRACT

Visible memory: `candidate_sources`, `entity_chain`, `answer_schema`, `format_constraints`.

Goal: fetch source pages and extract answer-bearing facts.

Allowed tools: `fetch_url`, `html_extract`, `run_python`

Rules:
- Use search snippets only as leads.
- Fetch the selected source before treating a fact as evidence.
- For multi-hop tasks, extract the next entity and decide whether another retrieval hop is needed.

Exit handoff:
- `evidence_cards`: URL-backed facts.
- `entity_chain`: updated chain.
- `source_status`: verified, partial, or blocked.

Next: `COMPUTE_OR_COMPARE` if answer evidence is available; otherwise `WEB_RETRIEVE`

## Phase: COMPUTE_OR_COMPARE

Visible memory: `evidence_cards`, `answer_schema`, `format_constraints`, `candidate_work`.

Goal: derive one candidate answer from verified or computable evidence.

Allowed tools: `run_python`, `read_file`, `read_table`

Rules:
- Use `run_python` for arithmetic, counts, sorting, tie-breaking, path search, probability, table aggregation, date math, color formatting, and code execution.
- Keep the calculation trace compact.
- If evidence is missing, return to the smallest phase that can repair it.

Exit handoff:
- `candidate_answer`
- `calculation_trace`
- `missing_evidence` if blocked

Next: `CROSS_CHECK`, or repair to `EVIDENCE_ROUTE`, `LOCAL_PARSE`, `MEDIA_PARSE`, `WEB_RETRIEVE`, or `WEB_EXTRACT`

## Phase: CROSS_CHECK

Visible memory: `candidate_answer`, `evidence_cards`, `calculation_trace`, `format_constraints`.

Goal: verify the candidate against the requested source and task contract.

Allowed tools: `fetch_url`, `html_extract`, `read_file`, `read_table`, `run_python`

Checks:
- Attachment tasks: candidate must point back to file evidence.
- Web tasks: candidate must point back to the requested source, date, version, or entity chain.
- Prompt-only tasks: candidate must survive enumeration, counterexample checking, or consistency checks.
- Multi-hop tasks: verify both final answer and intermediate link.

Exit handoff:
- `verification_status`: verified, weak, contradictory, or blocked.
- `verification_note`: one compact sentence.

Next: `FORMAT_VERIFY`, or repair to `EVIDENCE_ROUTE`, `LOCAL_PARSE`, `MEDIA_PARSE`, `WEB_RETRIEVE`, `WEB_EXTRACT`, or `COMPUTE_OR_COMPARE`

## Phase: FORMAT_VERIFY

Visible memory: `candidate_answer`, `format_constraints`, `verification_status`, `verification_note`, short prompt excerpt.

Goal: produce the exact final answer string.

Allowed tools: `run_python`

Checks:
- Units, scale, rounding, decimals, separators, casing.
- List order, comma spacing, no-whitespace rules.
- First name, surname, city only, code only, title wording, chess notation, color ordering.
- Remove explanations unless explicitly requested.

Exit handoff:
- `final_answer_string`

Next: `CONCLUDE`, or repair to `COMPUTE_OR_COMPARE`

## Phase: CONCLUDE

Visible memory: `final_answer_string`, `format_constraints`, `verification_status`.

Goal: output the final answer only.

Allowed tools: none

Rules:
- Output exactly one `<ANSWER>...</ANSWER>`.
- Put only the final answer string inside the tag.
- Do not output placeholders.
- Do not add explanation.

Available action:
- `<ANSWER>final answer</ANSWER>`
