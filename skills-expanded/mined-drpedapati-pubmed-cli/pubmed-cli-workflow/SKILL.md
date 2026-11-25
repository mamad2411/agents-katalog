---
name: pubmed-cli-workflow
description: Operate, test, and troubleshoot pubmed-cli for PubMed literature workflows. Use when tasks involve running pubmed-cli commands (`search`, `fetch`, `cited-by`, `references`, `related`, `mesh`, `refcheck`), exporting outputs (`--json`, `--csv`, `--ris`), validating command behavior/errors, building reproducible CLI test bundles, or preparing release smoke checks for this CLI.
---

# pubmed-cli Workflow

## Overview

Use this skill to execute end-to-end literature retrieval workflows with `pubmed-cli`, including robust export paths for scripts and citation managers (EndNote/Zotero via RIS) and document-level reference verification with `refcheck`.

Command surface on `main` (v0.6.0+):

- `search`
- `fetch`
- `cited-by`
- `references`
- `related`
- `mesh`
- `refcheck` *(requires [docx-review](https://github.com/drpedapati/docx-review) on PATH)*

## Install

```bash
brew tap drpedapati/tools
brew install pubmed-cli
```

Binary lives at `/opt/homebrew/bin/pubmed` on macOS, `/home/linuxbrew/.linuxbrew/bin/pubmed` in Coder/Linux workspaces. Verify with `pubmed --version`.

## Quick Command Map

- Search by topic:
```bash
pubmed search "autism" --limit 10 --human
pubmed search "ALS biomarkers" --year 2020-2025 --type review --json
pubmed search "CRISPR" --sort cited --limit 5 --json
```

- Fetch full records by PMID:
```bash
pubmed fetch "38000001,38000002" --json
pubmed fetch 38000001 --human --full
```

- Traverse citation graph:
```bash
pubmed cited-by 38000001 --limit 10 --human
pubmed references 38000001 --limit 10 --human
pubmed related 38000001 --limit 10 --human
```

- Look up MeSH:
```bash
pubmed mesh "depression" --json
```

- Export for tooling/reference managers:
```bash
pubmed fetch "38000001,38000002" --csv refs.csv --json
pubmed fetch "38000001,38000002" --ris refs.ris --json
pubmed related 38000001 --limit 10 --ris related.ris --human
```

- Verify references in a Word document:
```bash
pubmed refcheck manuscript.docx --human
pubmed refcheck manuscript.docx --audit-text --json
pubmed refcheck manuscript.docx --csv-out report.csv --ris-out verified.ris
```

## Workflow Decision Tree

1. Need PMIDs quickly by query?
- Run `search` first. Filter with `--year`, `--type`, `--sort` as needed.

2. Need bibliographic details/abstracts?
- Run `fetch` on PMIDs from search output. Add `--full` with `--human` for abstracts in interactive use.

3. Need citation expansion?
- Use `cited-by` for forward citations.
- Use `references` for backward citations.
- Use `related` for algorithmic neighbors (returns relevance scores).

4. Need import into EndNote/Zotero?
- Export with `--ris FILE` from `fetch`, `cited-by`, `references`, or `related`.

5. Need controlled vocabulary refinement?
- Use `mesh` to improve query terms, then rerun `search` with `[MeSH Terms]` field tag.

6. Need to verify a manuscript's reference list against PubMed?
- Use `refcheck <doc.docx>`. Add `--audit-text` to check that every reference is cited in the body and vice versa. Output `VERIFIED_EXACT`, `VERIFIED_WITH_CORRECTION`, `VERIFIED_BY_TITLE`, `NOT_IN_PUBMED`, or `POSSIBLY_FABRICATED` per reference.

## Global Flags

| Flag | Values | Notes |
|------|--------|-------|
| `--limit N` | positive integer, default 20 | NCBI eSearch caps return at ~100 PMIDs per call regardless; very high `--limit` (e.g. 500) silently returns empty `ids` instead of erroring. Page through with multiple smaller calls or use `cited-by`/`related` for traversal |
| `--sort` | `relevance`, `date`, `cited` | `search` only |
| `--year` | `YYYY` or `YYYY-YYYY` (ascending) | `search` only — descending range like `2025-2020` errors with "year range must be ascending" |
| `--type` | `review`, `trial`, `meta-analysis`, `randomized`, `case-report`, custom | `search` only — accepts arbitrary strings, NCBI applies as a `[pt]` filter |
| `--json` | structured JSON | preferred for agent workflows |
| `--human` / `-H` | colorful tables | interactive use |
| `--full` | include full abstract in human output | only meaningful with `--human`; silently ignored when paired with `--json` |
| `--csv FILE` | CSV export | `search`, `fetch`, citation-graph commands |
| `--ris FILE` | RIS citations | `fetch`, `cited-by`, `references`, `related` only — explicit error on `search` and `mesh` |
| `--api-key KEY` | NCBI API key | inline override for `NCBI_API_KEY` env var; useful in CI where env vars aren't set: `pubmed search ... --api-key "$NCBI_KEY"` |

`refcheck` adds: `--audit-text`, `--csv-out FILE`, `--ris-out FILE`.

## Input and Validation Rules

Always enforce these constraints when constructing commands:

- `--limit` must be greater than 0. Verified upper bound: ~100 results per call. Beyond ~500 the CLI returns empty `ids` instead of erroring; if you need a larger sweep, page with multiple narrower searches.
- `--sort` must be one of: `relevance`, `date`, `cited`.
- `--year` must be `YYYY` or `YYYY-YYYY` with **ascending** range. The CLI rejects descending ranges with a clear error.
- `--type` accepts the listed values plus arbitrary strings (NCBI applies them as a `[pt]` filter; spelling matters).
- PMIDs for fetch/link commands must be digits only; comma- or space-delimited lists are accepted (`fetch "38000001,38000002"`, `fetch 38000001 38000002`, both work). The CLI errors with "only digits are allowed" on any non-numeric input.
- Empty `search` query is rejected with "search query cannot be empty".
- `--ris` is supported only by `fetch`, `cited-by`, `references`, and `related`. Use `--ris-out` for `refcheck`.
- `--ris` is explicitly rejected for `search` and `mesh` (clean error message points users at the right command).
- `--full` is only meaningful with `--human`. It is silently ignored under `--json` rather than errored — agents should not pass `--full` when consuming JSON.
- `mesh` lookups error explicitly when the term is not found ("MeSH term ... not found").

## Reproducible UX Testing Pattern

When asked for usability testing:

1. Build or install a dedicated binary in a fresh `/tmp` directory (`brew install --force-bottle drpedapati/tools/pubmed-cli` or `go build`).
2. Capture outputs of happy-path and expected-failure commands to files.
3. Export RIS and JSON in parallel for the same dataset where possible.
4. Include a manifest file listing generated artifacts and exit codes.
5. If asked on macOS, open the output directory via `open <path>` for manual app import checks.
6. For `refcheck` runs, include sample `.docx` fixtures with mixed verification outcomes (exact, with-correction, fabricated).

## Error Handling and Fallbacks

- For NCBI rate limits (`429`), rerun with `NCBI_API_KEY` set. The CLI auto-retries with exponential backoff and respects `Retry-After` headers, but a key raises the ceiling from 3 req/s to 10 req/s.
- If human enrichment fetch fails in link flows, expect PMID-only fallback output unless RIS export is requested.
- If RIS export is requested and metadata fetch fails, treat as a hard failure and report clearly.
- `refcheck` fails fast if `docx-review` is not installed; suggest `brew install drpedapati/tools/docx-review` to the user.

## References

For ready-to-run command patterns and scenario bundles, use:

- `references/cli-cookbook.md`
- The canonical `pubmed-cli` skill in the repo at <https://github.com/drpedapati/pubmed-cli/blob/main/SKILL.md> (general user-facing docs)
