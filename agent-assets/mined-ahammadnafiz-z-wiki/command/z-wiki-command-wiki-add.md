---
description: Add a new raw source from a URL or file path, then optionally ingest.
argument-hint: "<url-or-path>"
when_to_use: Use when the user wants to add a new source to the wiki — a URL to an article, a path to a PDF or markdown file on disk. One-shot replacement for the "save file to raw/ manually, then /wiki-ingest" dance. Triggered by phrases like "add this source", "add this url", "add this paper", "grab this article".
allowed-tools: Read, Write, Edit, Bash, WebFetch, Glob, Grep
---

# Wiki Add

Add a new source to `raw/` and (optionally) ingest it. Arg (`$ARGUMENTS`): a URL or a local file path.

## Naming rule (critical)

**Raw filenames describe the source; summary slugs identify it.** They must differ.

- **Raw filename** (this command's output): a short descriptive name of *what the source is* — e.g. `raft-paper.md`, `karpathy-on-llm-wikis.md`, `nyt-profile-medvi.md`, `energy-transition-iea-2024.md`.
- **Summary slug** (generated later by `/wiki-ingest`, written as `wiki/sources/{slug}.md`): canonical `{author-lastname}-{year}-{short-title}` form — e.g. `ongaro-2014-raft.md`.

If the two collide, Obsidian's `[[wikilink]]` resolution becomes ambiguous. Reject any raw filename that matches the `{lastname}-{year}-*` pattern and propose a descriptive alternative instead.

## Dispatch

### If `$ARGUMENTS` starts with `http://` or `https://`

1. **Fetch the content.**
   - **Prefer `defuddle`** (installed via `npm install -g defuddle`) for article-style URLs: blog posts, newsletters, X/Twitter long-forms, news sites, Reddit. It strips navigation and boilerplate — cheaper and cleaner than WebFetch. Skill reference: `.claude/skills/defuddle/SKILL.md`.
   - **Use `WebFetch` directly** for: arXiv HTML (`arxiv.org/abs/` and `arxiv.org/html/`), GitHub pages (`github.com/.../blob/.../README.md`), raw `.md` URLs, anything already structured.
   - **Large-page fallback.** If `defuddle` fails with `Error: Page too large (NMB, max 5MB)`, bypass its fetcher: download the HTML with `curl -L --compressed -o /tmp/page.html "<url>"`, then parse the local file with `defuddle parse /tmp/page.html --md -o /tmp/page.md`. Then strip inline base64 data URIs (they bloat output 40×+ on research blogs) with `sed -E 's|!\[([^]]*)\]\(data:[^)]+\)|![\1](<inline-image-stripped>)|g'`. Full pipeline is in the updated defuddle skill. If `WebFetch` fails with a size error, same approach applies — curl to disk first.
   - **Fetch rules (all paths).** Always `curl -L --compressed` to stream to disk; never pull large content into model context. Follow redirects (`-L`). For very large (>100MB) or flaky sources, prefer `wget -c --tries=3` so a dropped connection doesn't force a restart.
   - If the URL returns an error or empty content, stop and report — do not write an empty file.

2. **Derive a descriptive raw-filename slug** per the naming rule above.
   - Start from the page `<title>` (or `<h1>`): kebab-case, ASCII, no spaces/underscores/uppercase, no trailing site-name boilerplate.
   - **Do NOT use `{author}-{year}` form.** If the title-derived slug happens to look like that, append a descriptive word — e.g. `raft-paper` not `ongaro-2014-raft`, `llm-knowledge-bases-post` not `karpathy-2026-llm-knowledge-bases`.
   - Keep it short: aim for 2–4 words. Confirm with the user if it came out awkward.
   - Never overwrite an existing file. If `raw/articles/{slug}.md` already exists, propose a different slug or stop.

3. **Write to `raw/articles/{slug}.md`.** Prepend a frontmatter-like header Claude can cite later:
   ```markdown
   ---
   Source: <original-url>
   Fetched: YYYY-MM-DD
   ---

   <extracted markdown body>
   ```

### If `$ARGUMENTS` is a local file path

1. **List available subfolders** by scanning `raw/*` for existing directories. Typical set: `articles/`, `papers/`, `transcripts/`. Any custom subfolders created by `/wiki-new-template` (e.g. `voice-memos/`, `meeting-minutes/`) should also appear in the prompt — do not hardcode the three built-ins.

2. **Dispatch by extension** (the set must stay in sync with INGEST's file-type scope in `CLAUDE.md`):
   - `.pdf`, `.epub` → default `raw/papers/{slug}.{ext}`. Use the file's basename, kebab-cased, as the slug — but apply the naming rule above: if the basename looks like `{lastname}-{year}-*`, suggest a descriptive alternative.
   - `.md`, `.txt`, `.docx`, `.rtf`, `.pptx`, `.xlsx`, `.xls`, `.html`, `.htm` → ask the user: *"Which subfolder? Options: <list of available subdirs under raw/>. Default: articles."* Copy to the chosen `raw/{subfolder}/{slug}.{ext}` (preserve the original extension — don't rewrite `.docx` to `.md`; INGEST extracts to markdown at read time via `markitdown`). Apply the same naming rule to the slug.
   - Any other extension → refuse with a clear message listing supported types: `.pdf`, `.epub`, `.md`, `.txt`, `.docx`, `.rtf`, `.pptx`, `.xlsx`, `.xls`, `.html`, `.htm`. For audio/video/archives or structured data (`.csv`, `.json`, `.xml`), tell the user they aren't in the default ingestion scope and propose a path forward.

3. **Never overwrite.** If the target file already exists, propose a different slug or stop.

### Refusal rules

- Do not fetch URLs resolving to `localhost`, `127.0.0.1`, `0.0.0.0`, or private IP ranges (`10.*`, `172.16–31.*`, `192.168.*`). Report the refusal.
- Do not write empty or obviously-stub content. If the fetch returned <200 chars of body text, stop and tell the user.
- Do not create files outside `raw/` subdirectories that already exist (to create a new kind of source folder, use `/wiki-new-template` first).
- Reject `{lastname}-{year}-*` style raw filenames per the naming rule above. Propose a descriptive alternative.

## After placing the file

1. Report the path of the new file.
2. Ask the user: *"Ingest now? (y/n)"*
   - **Yes** → invoke `/wiki-ingest <new-file-path>`. Follow the INGEST operation in `CLAUDE.md` for just that one file.
   - **No** → stop. The user can run `/wiki-ingest` later whenever they want.

## Reporting

- Source path written
- Slug used
- Size of fetched/copied content
- Whether ingestion was triggered
