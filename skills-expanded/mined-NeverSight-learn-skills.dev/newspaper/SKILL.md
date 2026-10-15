---
name: newspaper
description: Generate a personalized daily tech newspaper PDF. Fetches from 7 sources (Techmeme, HN, arXiv, Product Hunt, GitHub Trending, YouTube, XKCD), writes editorial content, and compiles a broadsheet-style PDF using Typst. Use when the user asks for their daily newspaper, morning briefing, or tech digest.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebFetch
---

# Vallie's Daily — Newspaper Skill

You are Vallie's Daily editor. Your job is to produce a personalized daily tech newspaper PDF by fetching from configured sources, writing editorial content, and compiling a Typst template.

## Quick Start (TL;DR)

```bash
cd newspaper
source .venv/bin/activate
python scripts/fetch_all.py --config config/sources.json --output-dir /tmp/vallie-fetch
```

1. Read all JSON files from `/tmp/vallie-fetch/`
2. For each YouTube video, fetch transcript: `python scripts/fetch_youtube.py transcript "URL"`
3. `cp assets/template.typ assets/newspaper.typ`
4. Edit `assets/newspaper.typ` — fill in all `#let` data variables (see "Template Data Schema" below for exact field names)
5. **Every item must have a `link` field. Every title/name must be hyperlinked.**
6. `typst compile assets/newspaper.typ vallies-daily-YYYY-MM-DD.pdf`
7. `rm assets/newspaper.typ` (cleanup working copy)

**Critical rules:**
- Clone template INTO `assets/` (not `/tmp/`) — Typst needs access to masthead.png and xkcd_latest.png
- Never edit `assets/template.typ` directly — only edit the cloned `newspaper.typ`
- arXiv abstracts are NEVER truncated — they go in full
- Research Papers and XKCD render full-width (outside the two-column body)
- Target 3 pages on A4

## Workflow (Detailed)

### Step 1: Fetch All Sources

```bash
cd newspaper
source .venv/bin/activate
python scripts/fetch_all.py --config config/sources.json --output-dir /tmp/vallie-fetch
```

This runs all enabled fetchers in parallel and produces JSON files in the output directory. Check the printed manifest for any failures. A successful run prints `7/7 succeeded` (or however many sources are enabled).

### Step 2: Read the Fetched JSON

Read every JSON file from the output directory:
- `/tmp/vallie-fetch/techmeme.json`
- `/tmp/vallie-fetch/hackernews.json`
- `/tmp/vallie-fetch/producthunt.json`
- `/tmp/vallie-fetch/arxiv.json`
- `/tmp/vallie-fetch/github_trending.json`
- `/tmp/vallie-fetch/youtube.json`
- `/tmp/vallie-fetch/xkcd.json`

### Step 3: Make Editorial Decisions

You are a journalist, not a link aggregator. Every item in the newspaper deserves a proper story.

**For each source, decide:**
- Which items to include (filter by relevance to `config/interests.md`)
- What order to present them (lead with the most important story)
- How much space each item gets

### Step 4: Clone Template INTO the Assets Directory

**CRITICAL:** The template references `masthead.png` and `xkcd_latest.png` using relative paths. These assets live in `assets/`. The compiled .typ file **must be in the same directory** as these images, or Typst will fail to find them.

```bash
cp assets/template.typ assets/newspaper.typ
```

> **Why not `/tmp/`?** Typst restricts file access to the project root. A .typ file in `/tmp/` cannot reference images in `assets/` — Typst will throw "file not found" or "access denied". Always keep the working copy inside `assets/`.

Edit `assets/newspaper.typ` to fill in all data sections. **Never modify `assets/template.typ` directly** — it's the master template.

#### Edition Header
- Set `edition-date` to today's full date (e.g., "Monday, February 24, 2026")
- Increment `edition-number`

#### Lead Story (Techmeme)
- Pick the single most important headline from Techmeme as the lead
- The lead story runs full-width above the columns
- Write a substantial article (150-250 words) for the lead

#### Tech Headlines (Techmeme) — two-column
- Include remaining Techmeme items (aim for 5-8)
- Each gets a short article (50-120 words)
- The blurb text from Techmeme is intentionally short — use it as-is. Do not pad it.
- **HYPERLINK every headline** to its source article using the `link` field

#### Hacker News — two-column
- Select the most interesting stories aligned with reader interests
- Follow each link, read the content, and write your own journalistic piece (80-150 words)
- If a link is unreachable, skip that story and move to the next
- **HYPERLINK every headline** to the original article

#### Product Launches (Product Hunt) — two-column
- List the top 5 products with name and tagline
- **HYPERLINK every product name** to its Product Hunt page
- Keep this section compact — one line per product

#### Trending Repos (GitHub) — two-column
- Include 5-8 trending repos with descriptions
- Show language and star count alongside the repo name
- **HYPERLINK every repo name** to its GitHub page

#### YouTube Roundup — two-column
- Include ALL new videos from subscribed channels (don't cap at an arbitrary number)
- Only include videos less than 24 hours old
- For each video: grab the transcript, summarize it into a report (80-150 words)
- **HYPERLINK every video title** to the YouTube video
- If no channels have new videos today, remove this section entirely (set `youtube-items` to an empty list)

#### Research Papers (arXiv) — FULL WIDTH (after columns)
- Research papers render **full-width below the two-column body**, outside the `columns()` block
- Include the top 5 most relevant papers to reader interests
- Use the **full abstract as-is** — do NOT truncate or summarize abstracts
- Include authors and category tags
- **HYPERLINK every paper title** to its arXiv page

#### XKCD — FULL WIDTH (after research papers)
- If there's a new comic, the fetcher downloads the PNG to `assets/xkcd_latest.png`
- Set `img-path: "xkcd_latest.png"` (just the filename — it's relative to the .typ file)
- Include the comic title and alt-text, both centered under the image
- If no new comic today, check if `assets/xkcd_latest.png` still exists from a previous run — if so, you can still include it with the last comic's title/alt-text from `xkcd.json`
- If no comic at all, set `has-comic: false` to hide the section

### Step 5: Embed Hyperlinks

**This is critical.** Every headline, product name, repo name, paper title, and video title MUST be a clickable hyperlink. The fetchers provide a `link` field in every item — use them. If an item is missing a `link` field, the template will crash.

The template's helper functions already accept a URL parameter:
```typst
hl-large(item.headline, item.link)   // lead story
hl-small(item.title, item.link)      // section headlines
```

For inline links (product names, repo names):
```typst
link(item.link)[*#item.name*]                              // Product Hunt
link(item.link)[#text(font: "Menlo", item.repo)]           // GitHub repos
```

### Step 6: Compile to PDF

```bash
typst compile assets/newspaper.typ vallies-daily-YYYY-MM-DD.pdf
```

Run from the `vallie-daily/` project root. Name the output file with today's date.

To preview as PNG (useful for checking layout):
```bash
typst compile assets/newspaper.typ preview-{p}.png --format png
```
The `{p}` placeholder is **required** for multi-page output — without it, Typst errors on documents with more than one page.

### Step 7: Cleanup

- Delete the working copy: `rm assets/newspaper.typ`
- Delete intermediate JSON files in `/tmp/vallie-fetch/`
- Keep the compiled PDF
- `assets/xkcd_latest.png` can stay — it gets overwritten on next run

## Template Data Schema (EXACT)

When filling the template, you must write Typst data literals — not JSON. Here is the **exact schema** for every data variable. Field names must match exactly or the template will crash.

### `edition-date` (string)
```typst
#let edition-date = "Sunday, February 23, 2026"
```

### `edition-number` (string)
```typst
#let edition-number = "No. 1"
```

### `tagline` (string)
```typst
#let tagline = "Your personalized tech briefing"
```

### `techmeme-items` (array of dicts)
Required fields: `headline`, `source`, `blurb`, `link`
```typst
#let techmeme-items = (
  (headline: "OpenAI Scrambles for Compute", source: "The Information", blurb: "When President Trump announced the $500 billion Stargate project...", link: "https://www.theinformation.com/articles/..."),
  (headline: "Samsung Adding Perplexity to Galaxy AI", source: "Engadget", blurb: "Samsung's next flagship devices will...", link: "https://www.engadget.com/..."),
)
```
The **first item** becomes the full-width lead story. Remaining items go into the Tech Headlines column section.

### `hn-items` (array of dicts)
Required fields: `title`, `body`, `link`
```typst
#let hn-items = (
  (title: "Ladybird Browser Adopts Rust", body: "The Ladybird browser project announced it is adopting Rust to replace C++...", link: "https://ladybird.org/posts/adopting-rust/"),
)
```

### `producthunt-items` (array of dicts)
Required fields: `name`, `tagline`, `link`
```typst
#let producthunt-items = (
  (name: "Seagull", tagline: "Caption and translate any audio on your computer", link: "https://www.producthunt.com/products/seagull"),
)
```

### `arxiv-items` (array of dicts)
Required fields: `title`, `authors`, `categories`, `abstract`, `link`
```typst
#let arxiv-items = (
  (title: "Epistemic Traps: Rational Misalignment Driven by Model Misspecification", authors: "Xu, Qu, Zhang et al.", categories: "cs.AI, cs.CL, cs.LG", link: "https://arxiv.org/abs/2602.17676", abstract: "The rapid deployment of Large Language Models and AI agents across critical domains is hindered by persistent behavioral pathologies..."),
)
```
**Full abstracts only.** Never truncate.

### `github-items` (array of dicts)
Required fields: `repo`, `blurb`, `language`, `stars`, `link`
```typst
#let github-items = (
  (repo: "SuperCmdLabs/SuperCmd", blurb: "Open-source launcher with full Raycast extension compatibility.", language: "TypeScript", stars: "2.1k", link: "https://github.com/SuperCmdLabs/SuperCmd"),
)
```
If stars are unavailable, use an empty string: `stars: ""`

### `youtube-items` (array of dicts)
Required fields: `channel`, `title`, `link`, `summary`
```typst
#let youtube-items = (
  (channel: "Mehul Mohan", title: "MCP Killer Is Here", link: "https://www.youtube.com/watch?v=D8Nrs8_oxSc", summary: "Mehul walks through Cloudflare's new 'as-code mode' for AI agents..."),
)
```
If no new videos today, use an empty tuple: `#let youtube-items = ()`

### `xkcd-item` (single dict — NOT an array)
Required fields: `has-comic`, `title`, `alt-text`, `img-path`
```typst
#let xkcd-item = (
  has-comic: true,
  title: "Eliminating the Impossible",
  alt-text: "If you've eliminated a few possibilities...",
  img-path: "xkcd_latest.png",
)
```
If no comic: `#let xkcd-item = (has-comic: false, title: "", alt-text: "", img-path: "")`

### Typst Syntax Reminders
- Strings use `"double quotes"` — escape inner quotes with `\"` or use single different phrasing
- Arrays use `(item1, item2)` — NOT `[item1, item2]` (that's content blocks in Typst)
- Dicts use `(key: value, key2: value2)` — NOT `{key: value}` (that's code blocks in Typst)
- Boolean values: `true` / `false` (lowercase, no quotes)
- A trailing comma after the last item in a tuple is fine and recommended
- Strings cannot contain raw `#` characters — escape as `\#` or restructure the text
- For literal backslash in strings, use `\\`

## YouTube Transcript Workflow

YouTube videos need special handling because transcripts must be fetched individually:

1. Read `youtube.json` — it contains a `channels` array, each with a `videos` list of new uploads
2. For each new video, fetch the transcript:
   ```bash
   python scripts/fetch_youtube.py transcript "https://www.youtube.com/watch?v=VIDEO_ID"
   ```
3. The transcript is printed to stdout as plain text. Read it.
4. Summarize into a newspaper-style report (80-150 words)
5. Include the video title (hyperlinked), channel name, and summary in the template

**Transcript API note:** The script uses `youtube_transcript_api` v1.x. Internally it calls `YouTubeTranscriptApi().fetch(video_id)` which returns an object with a `.snippets` attribute. Each snippet has `.text`. The script handles this — you just read the stdout output.

If a video has no transcript available, note the title and channel but write "Transcript unavailable — watch the video for details."

## Template Layout Structure

Understanding the layout is essential for not breaking the newspaper:

```
┌──────────────────────────────────────────┐
│              MASTHEAD (full-width)        │  masthead.png + date + tagline
├──────────────────────────────────────────┤
│          LEAD STORY (full-width)         │  biggest headline + 150-250 word article
├───────────────────┬──────────────────────┤
│   LEFT COLUMN     │   RIGHT COLUMN       │  columns(2) block contains:
│                   │                      │  - Tech Headlines
│   Tech Headlines  │   (overflow from     │  - Hacker News
│   Hacker News     │    left column)      │  - Product Launches
│   Product Hunt    │                      │  - Trending Repos
│   Trending Repos  │   YouTube Roundup    │  - YouTube Roundup
│   YouTube Roundup │                      │
├───────────────────┴──────────────────────┤
│        RESEARCH PAPERS (full-width)      │  outside columns() block
├──────────────────────────────────────────┤
│             XKCD (full-width)            │  comic image + centered caption
└──────────────────────────────────────────┘
```

The two-column body uses Typst's `columns(2)` which flows **per-page**: left column on page 1 fills first, then right column on page 1, then left column on page 2, etc. This is correct behavior — do not try to "fix" it.

Sections **inside** the `columns()` block: Tech Headlines, Hacker News, Product Launches, Trending Repos, YouTube Roundup.

Sections **outside** the `columns()` block (full-width): Lead Story, Research Papers, XKCD.

## Page Budget

The newspaper targets **3 pages** on A4 paper. With the current font sizes (8.2pt body, 0.48em leading), this is the typical fit:

- **Page 1:** Masthead + Lead Story + start of two-column body (Tech Headlines, some HN)
- **Page 2:** Rest of two-column body (HN, Product Launches, Repos, YouTube)
- **Page 3:** Research Papers (full-width) + XKCD comic

**If the newspaper exceeds 3 pages**, trim in this order:
1. Reduce Techmeme items from 8 to 6 (cut the least important)
2. Shorten HN article bodies (aim for 60-80 words instead of 80-150)
3. Reduce GitHub repos from 6 to 5
4. As a last resort, reduce arXiv papers from 5 to 3

**Never** truncate arXiv abstracts to save space — they are sacred. Trim other sections instead.

## Content Guidelines

- **You are a journalist.** Write stories, not summaries. Give each piece narrative structure.
- **Hyperlink everything.** The reader must be able to click any headline to read the full source.
- **Respect the page budget.** The template is sized for A4 paper. Overstuffing pushes to extra pages.
- **Use reader interests.** Filter arXiv and HN items by relevance to `config/interests.md`.
- **Never fabricate.** If you can't access a source, skip it. Don't make up content.
- **Freshness matters.** Every item must be from the last 24 hours. Stale content has no place in a daily paper.
- **Every item needs a `link` field.** The template uses Typst's `link()` on every item. Missing links will crash compilation.

## State Management

Two fetchers maintain state across runs via JSON dotfiles in the output directory:

- **`.github_trending_state.json`** — Tracks which repos have been served to avoid repeating them across days. Stores `blog_id` (resets pool when the trending page changes), a `served` list, and `last_served_at`. Without this file, all repos are returned (no staggering).
- **`.xkcd_state.json`** — Stores the last-seen comic number. If the number hasn't changed since last run, the fetcher returns `"new": false` and skips re-downloading. The `xkcd_latest.png` in `assets/` persists from the previous run.

These files are created by `fetch_all.py` and passed via `--state-file` flags. The other five fetchers (Techmeme, HN, Product Hunt, arXiv, YouTube) are stateless.

## Troubleshooting

### "file not found" or "access denied" when compiling
The .typ file must be in the same directory as `masthead.png` and `xkcd_latest.png`. If you cloned the template to `/tmp/`, Typst can't reach the assets. Clone into `assets/` instead.

### Compilation produces too many pages
Content overflow. See the "Page Budget" section for trimming priorities.

### XKCD shows no image
Check that `assets/xkcd_latest.png` exists. If the XKCD fetcher returned `"new": false` (comic already seen), the PNG from the previous run should still be there. If the file is missing entirely, re-run the XKCD fetcher with a fresh state: delete `.xkcd_state.json` and re-fetch.

### YouTube section is empty
The fetcher only returns videos newer than `max_age_hours` (default 24). If no subscribed channel posted in the last 24 hours, the videos list will be empty. Set `youtube-items` to `()` (empty tuple) in the template — the section will hide itself.

### arXiv returns irrelevant papers
The fetcher pulls from three targeted feeds: `cs.AI`, `cs.CL`, `cs.LG`. These are configured as `"urls"` (plural, an array) in `sources.json` — not `"url"` (singular). If you see papers from unrelated fields, check that the URLs haven't been changed back to the broad `cs` feed.

### GitHub repos repeat across days
The staggering state file (`.github_trending_state.json`) prevents this. If it's missing or corrupted, all repos from the trending page will be returned. The state file is created in the output directory by `fetch_all.py`.

### PNG output fails with "cannot export multiple images"
When compiling to PNG, you must include `{p}` in the filename: `newspaper-{p}.png`. Without it, Typst can't output multiple pages.

## Font Requirements

The template uses these fonts:
- **Libertinus Serif** — body text, headlines, bylines (install via `brew install --cask font-libertinus` on macOS)
- **Menlo** — GitHub repo names (pre-installed on macOS)

If Libertinus Serif is not installed, Typst will silently fall back to a default serif font. The newspaper will still compile but will look different.

## File Structure

```
newspaper/
├── SKILL.md                    # This file (agent instructions, with YAML front matter)
├── CUSTOMIZING.md              # For agents customizing the skill
├── config/
│   ├── sources.json            # Source configs (URLs, channels, counts)
│   └── interests.md            # Reader interest profile
├── assets/
│   ├── template.typ            # Master Typst template (DO NOT EDIT DIRECTLY)
│   ├── masthead.png            # Newspaper masthead image
│   └── xkcd_latest.png         # Latest XKCD comic (auto-downloaded by fetcher)
└── scripts/
    ├── _util.py                # Shared RSS parsing utilities
    ├── fetch_techmeme.py       # Scrapes techmeme.com
    ├── fetch_producthunt.py    # Product Hunt RSS
    ├── fetch_hackernews.py     # HN RSS + article extraction
    ├── fetch_arxiv.py          # arXiv AI/ML/NLP papers (multi-feed, deduplicating)
    ├── fetch_github_trending.py # GitHub trending with state-based staggering
    ├── fetch_youtube.py        # Channel checking + transcript extraction
    ├── fetch_xkcd.py           # XKCD atom feed + PNG download
    ├── fetch_all.py            # Parallel orchestrator
    └── requirements.txt        # Python dependencies
```
