---
name: publish
description: Use when the user says a paper, review, report, or LaTeX deliverable is final and wants it archived under published/ or exposed through the static published-paper site.
---

# Published Paper Archive And Site Generation

Use this skill only after the user clearly says the deliverable is final, audited, or ready to publish. Drafts should stay under `workspace/`.

## Architecture

The publishing workflow has three separate layers:

- `scholaraio/`: upstream code and the `scholaraio publish-site` generator
- `published/`: local audited deliverable archive, git-ignored by this repository
- an optional separate GitHub Pages repository: generated static site files

Do not put user deliverables in the repository root except under `published/`, and do not commit `published/` to the ScholarAIO repo.

## Safety Gate

Before creating or changing a published archive:

1. Confirm with the user that the deliverable is final enough to archive.
2. Recommend a backup for important outputs, especially before replacing an existing archive directory.
3. Never delete source files from `workspace/`; publishing is a copy/archive step.

## Archive Layout

Use one folder per final deliverable:

```text
published/<YYYY-MM-DD>-<short-title>/
├── metadata.json
├── main.pdf
├── main.tex
├── images/
└── misc/
```

Recommended `metadata.json`:

```json
{
  "title": "Full title",
  "date": "YYYY-MM-DD",
  "keywords": ["keyword"],
  "subject": "field or topic",
  "pdf_filename": "main.pdf",
  "tex_files": ["main.tex"],
  "images_dir": "images",
  "misc_dir": "misc",
  "authors": ["Author", "Claude (AI Assistant)"],
  "note": "Final audited deliverable."
}
```

The site generator reads `published/*/metadata.json`, builds a source ZIP beside each archive, and writes a static site.

## Generate The Site

Explicit output directory:

```bash
scholaraio publish-site --out-dir ~/generated-report
```

Configured output directory:

```yaml
publish:
  site_output_dir: ~/generated-report
```

Then:

```bash
scholaraio publish-site
```

Default mode copies PDFs and source ZIPs into `assets/papers/`, producing a self-contained site suitable for a separate GitHub Pages repository.

Local preview mode uses symlinks instead of copying assets:

```bash
scholaraio publish-site --out-dir ~/generated-report --symlink
```

## Agent Behavior

- Confirm the archive folder name and metadata before writing final archive files.
- Keep metadata accurate: title, date, PDF filename, authors, subject, keywords, and note should match the actual deliverable.
- After archiving, run `scholaraio publish-site` so the static site reflects the new item.
- If the configured output directory is missing, either pass `--out-dir` or help the user set `publish.site_output_dir`.
- Treat the generated site as deployable output; if it lives in another Git repo, ask before committing or pushing there.
