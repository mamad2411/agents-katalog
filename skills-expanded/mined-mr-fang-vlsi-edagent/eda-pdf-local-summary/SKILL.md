---
name: eda-pdf-local-summary
description: Summarize local paper PDFs into structured, citation-grounded evidence notes. Use when the user provides local PDF paths and asks for methods/assumptions/results/limitations extraction or wants evidence mapped to current EDA hypotheses.
---

# EDA PDF Local Summary

## Overview

Use this skill to produce reusable local summary notes tied to page-level evidence.

## Workflow

1. Validate input PDF path.
- require absolute or repo-relative local path.
- expected location: `docs/papers/pdf/`.

2. Extract text to local artifact.
- Run `scripts/extract_pdf_text.sh <pdf_path> <out_dir>`.
- default output dir: `docs/papers/summaries/raw/`.
- default extractor priority is `GROBID` (via `grobid_client` + `GROBID_SERVER`), then falls back to `pdftotext`/`mutool`/`pypdf` if unavailable.
- to disable GROBID for one run: set `DISABLE_GROBID=1`.
- quality guard: if GROBID TEI result is too sparse, extractor auto-falls back to local text extraction.
- when GROBID succeeds, keep TEI artifact alongside text (`<pdf_stem>.tei.xml`) for traceability.

3. Build structured summary.
- Load `references/summary-template.md`.
- Fill sections with explicit evidence snippets.
- Prefer page-cited claims (`p.xx`) when recoverable from extracted text.
- write output to: `docs/papers/summaries/<pdf_stem>.summary.md`.

3.5 Update paper manifest status.
- locate corresponding row in `docs/papers/manifests/*.paper_manifest.tsv`.
- update `local_pdf_path` and set `status=summarized`.

4. Sync landscapes after summary write.
- run `python3 scripts/common/paper_landscape_sync.py build`.
- ensure both landscape docs are updated:
  - `docs/knowledge_base/95_PROBLEM_LANDSCAPE.md`
  - `docs/knowledge_base/96_METHOD_LANDSCAPE.md`

5. Link to active hypothesis.
- State whether paper supports, contradicts, or is neutral to current model/flow hypothesis.
- add one "actionable next experiment" sentence.

## Output Contract

Always output:
1. extracted text artifact path,
2. summary markdown path (`docs/papers/summaries/<pdf_stem>.summary.md`),
3. 3-5 bullet findings with evidence strength (`strong/medium/weak`),
4. unresolved ambiguities requiring manual read,
5. updated manifest path (or explicit note if no manifest row matched).
6. landscape sync artifact paths (`95/96` docs or explicit failure reason).

## References

Load:
1. `references/summary-template.md`
2. `references/evidence-grading.md`
