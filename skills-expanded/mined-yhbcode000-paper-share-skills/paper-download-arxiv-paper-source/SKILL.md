---
name: paper-download-arxiv-paper-source
description: |
  Download the TeX source (e-print tar.gz) of an arXiv paper from an arXiv URL or bare ID,
  and unpack it into paper_src/. Use FIRST whenever a pipeline input is an arXiv link and
  the TeX source is preferred over the PDF (paper-to-beamer, paper-to-bilibili, paper-venue-discovery).
  Invoke with an arXiv URL (abs/pdf/e-print, arxiv.org or export.arxiv.org) or a bare ID like 2509.07996v4.
user-invocable: true
argument-hint: "<arxiv-url|arxiv-id>"
---

# Download arXiv Paper TeX Source

Given an arXiv link or bare arXiv ID, download the paper's **TeX source** from
`https://arxiv.org/e-print/<id>` and unpack it for downstream pipelines. This is
the required first step whenever the user provides an arXiv link and the TeX
source (not just the PDF) should feed the pipeline — TeX source preserves tables,
equations, and figures exactly and skips MinerU.

## When to use

- User supplies an arXiv URL (`arxiv.org/abs/…`, `arxiv.org/pdf/…`,
  `arxiv.org/e-print/…`, `export.arxiv.org/…`) or a bare ID (`2509.07996`,
  `2509.07996v4`) as the input to any paper pipeline.
- A consumer skill needs the paper source on disk (`paper_src/`) but only has
  an arXiv reference.

## Invocation

```bash
uv run --no-project python \
  "<SKILLS_DIR>/paper-download-arxiv-paper-source/scripts/download_source.py" \
  "<arxiv-url|arxiv-id>" [--output DIR] [--force]
```

- `--output` defaults to the session cwd.
- `--force` re-downloads even if the archive already exists.

## Output contract

Under the output dir:

- `arXiv-<id>.tar.gz` — downloaded e-print archive (gzip/tar).
- `paper_src/` — extracted TeX source (flattened if the archive wraps in a
  single top-level directory; unsafe members are rejected).
- PDF-only submissions (no TeX source on arXiv): `arXiv-<id>.pdf` instead.
- Single-file TeX submissions: `arXiv-<id>.tex` instead.

On success stdout ends with `TEX_SOURCES: <comma-separated relative paths>`
(or `PDF_ONLY: <abs pdf path>`). Consume these lines — never guess file names.

## Idempotency

Re-running with the same ID in the same output dir skips the download
(stdout starts `SKIP`) unless `--force` is given; extraction is still verified.

## Failure

Nonzero exit + `ERROR:` message on stderr (parse failure, network failure,
empty body, unexpected payload, unsafe archive member, no `.tex` in archive).
The pipeline must stop and report — never silently fall back to the PDF.

## Fallback note

If the script reports `PDF_ONLY: <path>`, the paper has no TeX source on arXiv.
Consumers then use that PDF with the MinerU path (e.g. paper-to-beamer Phase 2's
DECISION GATE) instead of reading TeX.

## Consumed by

- `paper-to-beamer` Phase 1 (arXiv link/ID input)
- `paper-to-bilibili` slides mode (entries with `arxiv_id`, no local source)
- `paper-venue-discovery` step 1 (fetch source when only a link is given)

## Related skills

- skill://paper-to-beamer
- skill://paper-to-bilibili
- skill://paper-venue-discovery
- skill://paper-to-beamer-workflow
- skill://paper-bilibili-multi-part-series-upload
- skill://paper-bilibili-series-upload
