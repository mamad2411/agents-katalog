---
name: paper-extract
description: Extract academic source materials into a local ./papers workspace. Use when the user provides a local PDF that is clearly a paper, technical report, proposal, preprint, or other academic document, when the user provides an explicit arXiv ID or arXiv URL, or when the user provides an OpenReview forum ID or OpenReview forum URL. Download and unpack arXiv LaTeX sources for explicit arXiv inputs, download public OpenReview submission PDFs plus metadata for explicit OpenReview inputs, and handle MinerU for non-arXiv PDF inputs in manual, background, or inline mode.
---

# Paper Extract

Use this local skill to stage source materials for academic documents before downstream analysis.

Default MinerU behavior is `background`: start MinerU, write a job JSON plus log file under `./papers/jobs/`, and return immediately without polling. Use `inline` only when the user explicitly asks to wait for MinerU completion. Use `manual` only when the user explicitly wants a copyable command and will run it outside Codex.

This skill is local to the current repository. Do not install it into `$CODEX_HOME/skills`.

## Input Contract

Accept only these explicit inputs:

1. One or more local PDF files that are clearly academic materials such as papers, technical reports, proposals, or preprints
2. One or more explicit modern arXiv IDs
3. One or more arXiv URLs that resolve to modern arXiv IDs
4. One or more OpenReview forum IDs
5. One or more OpenReview forum URLs

If the user provides neither a local PDF path, an explicit arXiv ID or URL, nor an OpenReview forum ID or URL, ask for one of those inputs and stop.

## Routing Rules

1. Process every explicit input in the turn.
2. Process all arXiv inputs before OpenReview inputs, and all OpenReview inputs before local PDF inputs.
3. If the same paper is represented by both a PDF and an explicit arXiv ID or URL, prefer the arXiv route unless the user explicitly asks to run both routes.
4. If the same paper is represented by both a PDF and an explicit OpenReview forum ID or URL, prefer the OpenReview route unless the user explicitly asks to run both routes.
5. Do not infer arXiv IDs from PDF content, PDF metadata, titles, or free-form descriptions.
6. Do not use legacy arXiv IDs such as `cs/xxxxxxx` in this v1 workflow.
7. Treat OpenReview input as a public forum ID or `https://openreview.net/forum?id=...` URL only.

## Execution Workflow

1. Collect explicit arXiv IDs or URLs from the user request.
2. Collect explicit OpenReview forum IDs or URLs from the user request.
3. Collect local academic PDF paths that still need processing.
4. Choose MinerU mode:
   - `background` by default
   - `inline` only if the user explicitly says to run MinerU now and wait
   - `manual` only if the user explicitly asks for a terminal command instead of execution
5. Run:

```bash
/Users/yuzy/.venv/bin/python3 paper-extract/scripts/extract_sources.py \
  --papers-root ./papers \
  --mineru-bin /Users/yuzy/.venv/bin/mineru \
  --mineru-mode background \
  --openreview-python /Users/yuzy/.venv/bin/python3 \
  [--arxiv <id-or-url> ...] \
  [--openreview <forum-id-or-url> ...] \
  [--pdf <absolute-pdf-path> ...]
```

6. Do not replace `./papers` with `./Papers`.
7. After execution, report each processed item with:
   - route used (`arxiv`, `openreview`, or `mineru`)
   - output directory
   - whether the item was downloaded, reused, queued in background, extracted inline, manually queued, or failed
   - any warnings such as title lookup fallback
   - the exact MinerU command that was executed or prepared for each PDF item and each OpenReview-downloaded PDF
   - for background jobs, the `pid`, `job` JSON path, and `log` path

## Output Contract

- arXiv inputs write source trees to `./papers/arxiv/<arxiv-id>/`
- arXiv registry lives at `./papers/arxiv/paper-id.txt`
- `paper-id.txt` must contain one deduplicated line per paper in the form `arxiv-id: title`
- OpenReview inputs write bundles to `./papers/openreview/<forum-id>/`
- OpenReview registry lives at `./papers/openreview/paper-id.txt`
- OpenReview `paper-id.txt` must contain one deduplicated line per paper in the form `forum-id: title`
- Each OpenReview bundle must contain `submission.pdf` and `metadata.json`
- Background MinerU jobs write metadata to `./papers/jobs/<job-id>.json` and logs to `./papers/jobs/<job-id>.log`
- OpenReview inputs use `./papers/openreview/<forum-id>/mineru/` as the primary MinerU target
- PDF inputs use a target such as `./papers/mineru/<pdf-stem>/`
- Report the executed or prepared MinerU command for traceability
- If a MinerU target already exists, use `-2`, `-3`, and so on instead of overwriting

## Guardrails

1. Keep all outputs inside `./papers`.
2. Do not poll background MinerU jobs. Start them, report the job metadata, and stop.
3. Keep arXiv extraction, OpenReview download, and PDF MinerU handling in the same run if the user provides multiple explicit input kinds.
4. Treat a missing MinerU binary, invalid arXiv ID, invalid OpenReview forum ID, OpenReview download failure, missing OpenReview runtime, or missing PDF as an item-level failure. Continue processing unrelated items.
5. Do not create extra manifest files in v1 beyond the job JSON and log files for background MinerU tasks. The directory structure, `paper-id.txt`, and background job records are the public interface.
