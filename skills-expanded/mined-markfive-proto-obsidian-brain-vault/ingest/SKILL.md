---
name: ingest
description: "Ingest source material (URLs, PDFs, images, repos, papers, YouTube transcripts) into the vault's `raw/` directory as clean markdown. Use when the user says 'add this to my knowledge base', 'ingest this article', 'clip this page', 'import this paper', or drops a link/file to be filed. Part of the knowledge-base pack implementing Karpathy's raw→compiled-wiki workflow."
license: MIT
metadata:
  author: markfive-proto
  version: "0.1.0"
  pack: knowledge-base
---

# Ingest Pack — "Get this into my knowledge base"

Ingest is the **front door** of the Karpathy-style LLM knowledge base. Raw source material lands in `raw/`, gets lightly cleaned, tagged, and staged. A later `compile` pass turns `raw/` into a structured wiki.

## Directory convention

This pack assumes the vault has (or will create) this layout:

```
<vault>/
  raw/                    # immutable source dumps
    articles/
    papers/
    repos/
    images/
    transcripts/
    datasets/
  compiled/               # LLM-written wiki (concept pages, summaries, MOCs)
  outputs/                # generated artifacts (answers, slides, charts)
```

`ingest` writes to `raw/`. It never touches `compiled/` — that's `compile`'s job.

## Commands

### /clip — Ingest a web article or URL

When the user invokes `/clip <url>` or pastes a URL:

1. Fetch the page. Prefer Reader-mode text extraction:
   - Try `spider` CLI if installed (`spider --readability <url>`).
   - Fall back to `curl` + a markdownify pass.
   - For paywalled content, ask the user to paste the text.
2. Download referenced images into `raw/images/<slug>/` with stable filenames.
3. Rewrite image links in the markdown to local paths.
4. Build frontmatter:
   ```yaml
   ---
   title: <page title>
   source_url: <url>
   source_type: article
   ingested_at: <ISO date>
   author: <if detected>
   tags: [raw, needs-compile]
   ---
   ```
5. Save to `raw/articles/<YYYY-MM-DD>-<slug>.md` using `obs note create`.
6. Report back: path written, word count, image count, 2-line summary.
7. Do NOT write to `compiled/`. Just queue it.

### /paper — Ingest an arXiv / PDF paper

When the user invokes `/paper <url-or-path>`:

1. If URL, download with `curl -L <url> -o /tmp/paper.pdf`.
2. Extract text with `pdftotext` (or `mutool draw`, `pdfplumber`).
3. Pull metadata (title, authors, abstract, year) from arXiv API if URL, otherwise from first page.
4. Extract figures to `raw/images/<paper-slug>/fig-N.png` (use `pdfimages` or `pdftoppm`).
5. Build markdown with sections: Abstract, Key claims, Methods, Results, Open questions.
6. Frontmatter:
   ```yaml
   ---
   title: <paper title>
   authors: [<...>]
   year: <year>
   source_url: <url>
   source_type: paper
   arxiv_id: <id>
   tags: [raw, paper, needs-compile]
   ---
   ```
7. Save to `raw/papers/<YYYY>-<author>-<short-title>.md`.

### /repo — Ingest a GitHub repo

When the user invokes `/repo <github-url>`:

1. Fetch README, key source files, and repo metadata with `gh` CLI.
2. Build a structured note: What it is, Key files, Install, Usage examples, Dependencies, License, Stars/activity.
3. Extract any diagrams/images from the README to `raw/images/<repo-slug>/`.
4. Save to `raw/repos/<owner>-<name>.md` with tags `[raw, repo, needs-compile]`.

### /transcript — Ingest a YouTube / podcast transcript

When the user invokes `/transcript <youtube-url>`:

1. Prefer `yt-dlp --write-auto-sub --skip-download <url>` for auto-captions.
2. Clean the SRT: remove timestamps, collapse speaker turns, fix obvious punctuation.
3. Frontmatter: title, channel, duration, published, source_url, tags `[raw, transcript, needs-compile]`.
4. Save to `raw/transcripts/<YYYY-MM-DD>-<slug>.md`.
5. Optionally (ask the user) run summarization to produce a TL;DR section at the top — but preserve full transcript below.

### /image — Ingest a reference image with captioning

When the user invokes `/image <path-or-url>` (or drops an image):

1. Save image to `raw/images/standalone/<YYYY-MM-DD>-<slug>.<ext>`.
2. Generate a caption describing the image (you can see it — use your vision).
3. Create a companion note `raw/images/standalone/<slug>.md` with:
   - Image embed `![[<slug>.png]]`
   - Caption
   - Detected text (OCR if relevant)
   - Proposed tags
   - Source / context from the user

### /dataset — Ingest a CSV / JSON dataset pointer

When the user invokes `/dataset <path-or-url>`:

1. For large datasets, do NOT copy into the vault. Store a pointer note.
2. Sample first 20 rows; embed as a markdown table preview.
3. Note: schema, column types, row count, date range, source, license.
4. Save to `raw/datasets/<slug>.md` with tags `[raw, dataset, needs-compile]`.

### /batch — Batch ingest a list

When the user invokes `/batch <file>` (one URL or path per line):

1. Read the file.
2. For each entry, detect type (URL → /clip or /paper; local path → /image or /dataset; GitHub URL → /repo).
3. Run each ingest sequentially, collecting successes and failures.
4. Report a summary table.

## Guardrails

- **Never modify** existing `raw/` files. If a duplicate slug exists, append `-2`.
- **Always** keep the full original source text. Compression happens in `compile`, not here.
- **Log every ingest** by appending one line to `raw/INGEST-LOG.md`:
  ```
  - 2026-04-17 14:22  article  raw/articles/2026-04-17-karpathy-kb.md  "Building a personal KB with LLMs"
  ```
  This log is `compile`'s input signal.
- **Image hygiene:** strip EXIF PII (`exiftool -all=`), keep dimensions reasonable (max 2400px wide).

## Tools this skill expects

| Tool | Purpose | Fallback |
|---|---|---|
| `obs` | Write notes into vault | Direct file write |
| `curl` / `wget` | Fetch URLs | — |
| `spider` (optional) | Reader-mode extraction | curl + strip tags |
| `yt-dlp` | Transcripts | Manual paste |
| `pdftotext` / `pdfimages` | PDF extraction | `mutool` |
| `gh` | Repo metadata | curl to GitHub API |
| `exiftool` (optional) | Image privacy | skip |

## When to hand off

Once a raw file is written, tell the user: "Ingested. Run `/compile` to fold this into the wiki." Don't auto-compile — the user controls the compile cadence to avoid thrash.

## Related skills (same pack)

- `[[compile]]` — turns `raw/` into `compiled/` wiki
- `[[qa]]` — queries the compiled wiki
- `[[lint]]` — health-checks the whole KB
- `[[render]]` — renders wiki content as slides/charts/reports

## Attribution

Pack inspired by Andrej Karpathy's "personal knowledge bases using LLMs" workflow: raw → compiled wiki → Q&A → outputs → lint loop.
