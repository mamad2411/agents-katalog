---
name: inbox-fetcher
description: Processes a queue of URLs listed in inbox.md for a second brain vault, downloading each page as clean markdown in raw/web/<slug>/index.md with images in an assets/ subdirectory. Use this skill whenever the user mentions "inbox", "fetch", "process links", "scrape URLs", "download articles", or adds URLs to inbox.md. Run this BEFORE any ingest operation so the agent has clean raw files to work from. Handles HTML articles via trafilatura, direct PDF downloads, and per-URL failures (paywalls, JS-rendered pages, timeouts) gracefully without blocking the rest of the queue. Walled domains (X/Twitter, LinkedIn, Threads, Facebook, Instagram) are flagged for an agent-driven Playwright MCP fallback instead of being attempted with trafilatura. Arxiv abstract/html URLs are rewritten to the PDF endpoint so the paper itself is archived, not the landing page.
---

# Inbox Fetcher

Processes a queue of URLs from `inbox.md` into clean markdown files under `raw/web/`, ready for ingest into the wiki.

## When to use this skill

Trigger whenever the user:

- Says "process the inbox", "fetch the inbox", "scrape the links", "download these URLs"
- Adds URLs to `inbox.md` and asks to prepare them
- Asks to ingest web content and the vault has an `inbox.md` file
- Wants to refresh or re-fetch a URL already in the inbox

This skill is a **pre-ingest step**. After it runs, the user (or the agent following the vault's `CLAUDE.md`) performs the actual ingest — reading the new files in `raw/` and compiling them into the wiki.

## Vault assumptions

The skill expects this layout:

```
<vault>/
├── inbox.md              queue of URLs (checkbox format)
├── raw/
│   ├── web/              HTML article output
│   └── papers/           direct PDF downloads
└── .claude/
    └── skills/
        └── inbox-fetcher/
            ├── SKILL.md
            └── scripts/
                └── fetch_inbox.py
```

The skill creates `raw/web/` and `raw/papers/` if they don't exist.

## Inbox format

`inbox.md` uses GitHub-flavored task list syntax, readable in Obsidian and parseable with regex:

```markdown
# Inbox

## To process

- [ ] https://www.anthropic.com/engineering/agent-skills
- [ ] https://example.com/paper-x.pdf
  - tags: agent-skills, spec
  - note: focus on composition

## Processed

- [x] https://old-url.com → `raw/web/old-url-slug/` (2026-04-15)
```

Rules:

- Only lines matching `- [ ] <URL>` at the start (unchecked) are processed.
- Indented sub-bullets (tags, notes) are preserved but not parsed — they're hints for the ingest step.
- After a successful fetch, the line moves to "Processed" and gets marked `- [x]` with the output path and date.
- Failed fetches get an inline `⚠ <reason>` suffix and stay unchecked so the user can decide.

## How to run it

From the vault root:

```bash
python .claude/skills/inbox-fetcher/scripts/fetch_inbox.py
```

Or from anywhere:

```bash
python .claude/skills/inbox-fetcher/scripts/fetch_inbox.py --vault /path/to/vault
```

Use `--dry-run` to see what would be processed without actually fetching.

The script is idempotent: already-processed URLs (marked `[x]`) are skipped. To re-fetch a URL, un-check it manually in `inbox.md`.

## What the script does per URL

1. **URL rewriting (pre-fetch).** Certain URLs are rewritten to reach the actual content instead of a landing page. Today: arxiv — any `arxiv.org/abs/<id>`, `arxiv.org/html/<id>`, or `arxiv.org/pdf/<id>` (with or without `.pdf`, with or without a `vN` version suffix) is rewritten to `arxiv.org/pdf/<id>.pdf` so we archive the paper itself. The slug becomes `arxiv-<id>` verbatim (no slugify — preserves the canonical ID). The inbox line still tracks the URL you wrote.
2. **PDF detection.** If the (rewritten) URL path ends in `.pdf` or the server returns `Content-Type: application/pdf`, download as-is to `raw/papers/<slug>.pdf`.
3. **HTML extraction.** Otherwise, use `trafilatura` to fetch and extract clean markdown with metadata (title, author, publish date, language).
4. **Slug generation.** For rewritten URLs, use the override slug (e.g. `arxiv-2405.12345`). Otherwise prefer the article title, fallback to `<hostname>-<hash8>`.
5. **Image download.** Parse `![alt](url)` patterns, download each image into `raw/web/<slug>/assets/` with a hash-based filename, rewrite paths to local.
6. **Frontmatter.** Prepend YAML with `source_url`, `title`, `author`, `fetched`, `language`.
7. **Inbox update.** On success, move to "Processed". On failure, append ⚠ with reason.

## Dependencies

Python 3.10+ and:

```bash
pip install trafilatura requests python-slugify
```

If a dependency is missing, the script prints a clear install command and exits with code 1.

## Edge cases

- **Walled domain (preflight).** Hosts in `WALLED_DOMAINS` (X/Twitter, LinkedIn, Threads, Facebook, Instagram) are skipped upfront — trafilatura would fail anyway. Marked `⚠ walled domain (<host>) — try playwright`. Agent follows up with the Playwright MCP fallback (see below).
- **Paywall / 403 / login wall (non-walled host).** Extraction returns empty. Marked `⚠ extraction empty (likely paywall or JS-rendered) — try playwright`. Same Playwright fallback applies.
- **JS-rendered SPA.** Same as above — `try playwright` hint.
- **Very large PDFs (>50 MB).** Downloaded anyway, prints a warning.
- **Duplicate URL.** If already in "Processed", skipped with a message. Un-check manually to force re-fetch.
- **Network timeout.** Per-request timeout is 20s for HTML, 60s for PDFs. Failures don't block the queue.

## Playwright fallback

Any URL marked `⚠ ... — try playwright` in inbox.md is a hand-off from the script to the agent. The script never calls a browser; the agent uses the Playwright MCP (`mcp__plugin_playwright_playwright__browser_*`) interactively, one URL at a time.

**Protocol per URL:**

1. **Confirm with the user** before fetching. Never batch-process walled URLs unattended.
2. Navigate with `browser_navigate` to the URL.
3. If auth is required and the user is logged in (persistent profile), proceed. Otherwise stop and report — don't attempt to bypass auth.
4. Use `browser_snapshot` to get the accessibility tree, or `browser_evaluate` to extract the article/tweet text from the DOM. For X/Twitter threads, collect the full thread, not just the root post.
5. Generate a slug (title for articles; `<handle>-<tweet-id>` for X/Twitter).
6. Write `raw/web/<slug>/index.md` with frontmatter:
   ```yaml
   ---
   source_url: <url>
   title: <inferred or first-line-of-post>
   author: <handle or author>
   published: <YYYY-MM-DD if visible>
   fetched: <today>
   fetched_via: playwright
   ---
   ```
7. Save screenshots to `raw/web/<slug>/assets/` only if the user asks — they're large and rarely needed.
8. In `inbox.md`, move the line to `## Processati` with `- [x] <url> → \`raw/web/<slug>/\` (<today>)`. Remove the `⚠` marker.
9. Report to the user what was captured and ask whether to proceed to INGEST.

**Out of scope for the fallback:** bypassing login walls, solving CAPTCHAs, scraping at volume. If any of these come up, stop and tell the user.

## Output contract

After a run, the script prints:

```
Processed 5 URLs:
  ✓ 3 HTML articles → raw/web/
  ✓ 1 PDF → raw/papers/
  ⚠ 1 failed (extraction empty): https://paywall-site.com/article
```

The agent reports this summary verbatim and asks the user whether to proceed with ingest on the new files.

## Not in scope

- Re-extraction when HTML source changes (no versioning; user re-fetches manually).
- Authenticated scraping inside the Python script (cookies, API keys) — user downloads manually, or uses the Playwright MCP fallback interactively.
- Image OCR or figure extraction from PDFs.
- Scheduling / cron — user or the agent's own scheduler decides when to run.
- Unattended batch via Playwright — the fallback requires an interactive session with the agent (one confirmation per URL).
