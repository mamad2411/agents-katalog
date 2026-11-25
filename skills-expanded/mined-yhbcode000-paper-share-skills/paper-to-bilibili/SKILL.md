---
name: paper-to-bilibili
description: |
  Orchestrate a paper PDF through MinerU, SUSTech Beamer slides, complete Chinese narration, landscape and portrait video, metadata gates, and Bilibili upload. Supports single-paper and batch slides, video, or bilibili phases. Trigger on full paper-to-Bilibili requests, PDF-to-video publication, and batch paper publishing.
user-invocable: true
argument-hint: "<slides|video|bilibili> <papers.json> [--dry-run]"
---

# Paper to Bilibili

This is the sole full-pipeline orchestration identity. It composes these promoted packages plus the retained managed Rednote workflow:

- `paper-to-beamer`: paper and MinerU content to compiled 16:10 SUSTech Beamer slides.
- `paper-video-cover`: optional poster generation for reference; the normal video cover remains the generated cover artifact.
- `paper-slides-to-video`: physical-page render, narration extraction, TTS, landscape assembly, cover, and Bilibili metadata.
- `rednote-video-uploader` (managed): required portrait video generation.
- `paper-bilibili-uploader`: fail-closed validation, dry-run, upload, and durable receipt.

Outputs use `$PP_ROOT/论文分享/<VENUE YEAR - SHORT>/` with `md_output/`, `slides-beamer/`, and `video/`.

## Modes and phases

### `slides`: paper to compiled slides

When an entry has a nonempty `arxiv_id` (or the user provided an arXiv link) and no source exists on disk (no root PDF, no `paper_src/` with `.tex`), download the TeX source first:

```bash
python \
  "<SKILLS_DIR>/paper-download-arxiv-paper-source/scripts/download_source.py" \
  "<arxiv_id>" --output "<paper_dir>"
```

The downloader creates `<paper_dir>/arXiv-<id>.tar.gz` + `<paper_dir>/paper_src/`; then follow `skill://paper-to-beamer` Phase 1 onward (Phase 1's move step is skipped since the paper dir already exists). For `PDF_ONLY` output, copy the PDF to the paper dir root (the `pdf_downloaded` gate requires a root PDF).

Follow `skill://paper-to-beamer` for content authoring. Required gates before continuing:

1. `slides-beamer/main.tex` contains the paper-specific narrative from paper information and motivation through methods, experiments, limitations, takeaways, references, Q&A, and 3–8 useful appendix slides.
2. The document uses the SUSTech 16:10 template (`aspectratio=1610`).
3. `slides-beamer/main.pdf` is nonempty, with no undefined controls or severe overflow.

The batch CLI only scans and persists disk evidence for this agent-authored phase; it does not fabricate slides.

### Narration authoring gate

Copy the compiled TeX to `video/main_with_narration.tex` and add exactly one nonempty `% NARRATION:` entry per physical PDF page. Narration is polished Simplified Chinese with English technical terms inline. It expands the technical argument rather than reading bullets, avoids visual-only references such as “本页” or “如图所示”, and covers appendix pages too.

The transition from `slides_done` to `narrations_done` occurs only when both the compiled slides and nonempty annotated TeX exist.

### `video`: narrated landscape and portrait artifacts

```bash
python <SKILLS_DIR>/paper-to-bilibili/scripts/batch.py video "<PAPERS_JSON>"
```

For each `narrations_done` paper, the orchestrator calls the sibling `paper-slides-to-video` `full` command. After child success it rescans and atomically persists `video_done`. It then calls the managed `rednote-video-uploader/scripts/portrait_video.py`, rescans, validates cover and Bilibili metadata, and atomically persists `upload_ready`. Child failures propagate and never advance state.

Quality gates are exact frame/text/MP3 cardinality, nonempty narration and audio for every physical page, a nonempty landscape MP4, a nonempty portrait MP4, a nonempty cover, and schema-valid Bilibili metadata.

### `bilibili`: validate or upload

Always review a dry-run first:

```bash
python <SKILLS_DIR>/paper-to-bilibili/scripts/batch.py bilibili "<PAPERS_JSON>" --dry-run
```

Dry-run delegates to the promoted uploader and must leave `upload_ready` unchanged. Remove `--dry-run` only after review. There is no default upload timeout; an operator may opt in with `--upload-timeout SECONDS`.

Normal uploads require P1 landscape then P2 portrait. Metadata uses singular `tag`, a positive `tid`, valid copyright/source fields, a structured description, and a nonempty cover. A paper becomes `uploaded` only when `video/upload_result.json` is valid and contains a matching BV URL plus ISO-8601 timestamp.

## State contract

`batch.py` rescans the disk with this exact precedence:

1. valid `upload_result.json` → `uploaded`
2. nonempty landscape + nonempty portrait + cover + schema-valid `video_meta.json` → `upload_ready`
3. nonempty landscape → `video_done`
4. compiled slides + nonempty annotated TeX → `narrations_done`
5. compiled slides → `slides_done`
6. MinerU Markdown → `mineru_done`
7. source PDF or extracted TeX source (paper_src/ containing .tex) → `pdf_downloaded`
8. otherwise → `pending`

Every successful child command is followed by a rescan and atomic replacement of the input JSON. State changes are printed as `STATE <paper>: <old> -> <new>`. Dry-run validates and delegates but never invents a new state. A failed child preserves the last grounded state and its exit code is propagated.

## Batch input

`papers.json` is an array of objects with a nonempty absolute `dir_path`; `dir_name`, `arxiv_id`, `pdf_path`, and descriptive fields may accompany it. The orchestrator records `_status` in each object.

## Prerequisites

- Python 3.10+ (if `python` is not on PATH, use `py -3`).
- Dependencies are declared in `pyproject.toml` (currently none at runtime); install the project with `uv sync --project <SKILLS_DIR>/paper-to-bilibili` when adding any.
- `<SKILLS_DIR>` is the directory containing the installed skill folders (e.g. `~/.claude/skills`, `~/.codex/skills`, `.omp/skills`); sibling skills (`paper-slides-to-video`, `paper-bilibili-uploader`, `paper-download-arxiv-paper-source`) must be installed next to this one so sibling resolution stays project-local and deterministic.
- `PAPER_PYTHON` (optional): interpreter used to launch sibling CLIs; defaults to the interpreter running `batch.py`.

## Related skills

- skill://paper-bilibili-uploader
- skill://paper-download-arxiv-paper-source
- skill://paper-slides-to-video
- skill://paper-to-beamer
- skill://paper-video-cover
- skill://rednote-video-uploader
