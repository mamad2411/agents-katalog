---
name: paperbound
description: >
  Convert any article or blog URL into a realistic interactive paperback book
  as a standalone HTML file with page-flip animations, leather-textured covers,
  and cream paper pages. Use when the user provides an article/blog URL and wants
  it turned into a book, or asks to "make a paperback", "bookify this article",
  "turn this into a book", "paperbound this", or similar. Supports any web
  article, blog post, or platform-specific content (X/Twitter articles, Medium,
  Substack, Hashnode, etc.). Produces a single portable HTML file.
---

# Paperbound

Convert a web article into a standalone interactive paperback book HTML file.

## Prerequisites

- The skill directory contains `book.html` — a pre-built skeleton template (React + react-pageflip, single-file)
- Browser automation (`agent-browser` skill, Claude `--chrome`, or equivalent) as fallback for JS-rendered pages

## Workflow

### Step 1: Classify the URL

Determine the source platform from the URL:

| URL pattern | Platform reference |
|------------|-------------------|
| `x.com/*/status/*` or `twitter.com/*/status/*` | Read `references/platforms/x-articles.md` |
| `open.substack.com/*` or `*.substack.com/*` | Read `references/platforms/substack.md` |
| `*.hashnode.dev/*` or `*.hashnode.com/*` | Read `references/platforms/hashnode.md` |
| All other URLs | Use generic extraction (Step 2) |

If a platform-specific reference exists, follow its extraction instructions instead of Step 2.

### Step 2: Extract Article Content

1. Fetch the URL with `web_fetch`
2. Extract from the HTML:
   - **Title** — from `<title>`, `<h1>`, or `og:title` meta tag
   - **Author** — from byline, `author` meta tag, or page metadata
   - **Body** — article text preserving: paragraphs, headings (h1-h3), bold/italic, block quotes, lists
3. Strip: navigation, footers, sidebars, ads, scripts, related articles, comments
4. **Images (mandatory)**: Extract meaningful images (hero images, diagrams, photos) with their original URLs. Skip decorative icons, avatars, and ads. Include them as `<img>` tags in the content. The runtime paginator waits for fonts/images before pagination and supports manual break hints for image-heavy sections.
5. **Escalation required when images are missing**: If `web_fetch` **or any platform/API fetch** (including X/Twitter API-style responses) does not return usable image URLs, you **must** use browser-based extraction (`agent-browser`, Claude `--chrome`, Playwright, or equivalent tooling available in the user's harness) to read rendered DOM image `src` values. Do not stop at fetch-only extraction when images are expected.
6. **Only skip images as last resort**: Omit images only when browser-based extraction is not possible after best effort (blocked/auth/paywall/technical failure), and explicitly note that limitation in the output.
7. If `web_fetch` returns a JS-rendered shell with no meaningful body text, fall back to browser automation (`agent-browser` skill if available, or Claude `--chrome`)

### Step 2B: Intelligent Content Filtering (Required)

When extracting from blogs/newsletters/articles, keep only editorial content and drop page chrome/noise.

**Always remove** (if present):
- Ads, sponsored blocks, affiliate widgets, promo banners, newsletter popups
- Nav bars, sidebars, breadcrumbs, headers/footers, cookie/privacy banners
- "Related posts", "Read next", "Trending", recommendation modules
- Comment sections, reaction widgets, share/follow bars, author cards repeated in-body
- CTA blocks unrelated to the article body ("subscribe now", "download", "start free trial")

**Keep**:
- Main title, subtitle/deck, byline/date (if meaningful), article body sections
- In-article headings, paragraphs, lists, quotes, code snippets
- Meaningful figures/images/charts that support the article text

**Decision rule**:
- Prefer high precision over recall: if a block looks ambiguous (content vs promo), drop it unless it is clearly part of the article narrative.
- Preserve reading flow: never include isolated UI fragments that break narrative continuity.

### Step 3: Build BookData JSON

Read `references/content-format.md` for the full schema, allowed HTML tags/classes, and content modes.

1. **Title**: Generate a cover-worthy title from the article title (shorten if needed, max ~6 words)
2. **Author**: Use the extracted author name
3. **Front matter**: Create an attribution page with source URL, original author, and date. Do NOT include copyright symbols or "All rights reserved" — just credit the source
4. **Content**: Convert the full extracted article body to a single HTML string using only the allowed tags and Tailwind classes from `references/content-format.md`. Use the `content` field (NOT `pages`) — the app auto-paginates at runtime using responsive page metrics and re-paginates on resize. Add manual break hints when needed:
   - `data-page-break="before"` on a block to start it on a new page
   - `data-page-break="after"` to force a break after a block
   - `data-page-break="always"` or `<hr data-page-break />` for an explicit page-break marker
   The app automatically ensures even page count (adds a blank filler page if odd) — this is required by react-pageflip for the last page to be turnable
5. **Headers**: Set `headerLeft` to the book title, `headerRight` to the author name or source
6. **Theme**: Analyze the article's tone, topic, and aesthetic. Generate a `theme` object with cover colors that match — e.g., a tech article might use dark slate covers with cyan text, a philosophy piece might use deep burgundy with cream text. Set `publisher`, `edition`, `year`, and `isbn` as appropriate. Inner pages always stay cream/paper-textured. **Important:** `coverBg` and `sceneBg` must contrast — never set them to the same or similar colors, or the book will blend into the background and be invisible

### Step 4: Generate the Book HTML

1. Read the `book.html` skeleton from this skill's directory
2. Create a copy at the output path: `<slugified-title>.html` in the current working directory
3. In the copy, find the line `<div id="root"></div>` and insert immediately before it:
   ```html
   <script>window.BOOK_DATA = {THE_JSON_HERE};</script>
   ```
4. Update the `<title>` tag to match the book title
5. Ensure all `</` sequences inside JSON string values are escaped as `<\/`

### Step 5: Deliver

1. Report the output file path to the user
2. Open the file: `open <filepath>` (macOS) or equivalent

## Adding New Platform Support

To add extraction support for a new platform (e.g., Medium, Hashnode, Substack):

1. Create `references/platforms/<platform-name>.md`
2. Document the platform-specific extraction method (API endpoints, DOM selectors, etc.)
3. Add the URL pattern to the classification table in Step 1
