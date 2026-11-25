---
name: american-reformer
description: Retrieves the latest article from American Reformer and summarizes selected articles. Use when the user asks for the latest American Reformer article, requests article parsing, or asks for a summary from americanreformer.org.
---

# American Reformer Parser

## Purpose

Fetch the latest article from `https://americanreformer.org/`, and when requested, fetch and summarize a selected article.

## Triggers

Apply this skill when the user asks for:

- the latest American Reformer article
- a specific article from americanreformer.org
- a summary of an article from American Reformer
- articles from a specific American Reformer category

## Workflow

1. Fetch the homepage at `https://americanreformer.org/`.
2. Identify the homepage "Latest Articles" section by structure, not by a specific post title.
3. Extract article cards from that section in display order.
4. American Reformer structure rule: if the top "Latest Articles" section has only one featured card, continue by extracting additional cards from the homepage category sections (Church, Culture, Family, Forum, Reports, Resources, Society, State) in page order to satisfy "latest articles" requests.
5. For "latest article" requests, pick the first card from the top "Latest Articles" section.
6. For "latest articles" requests, return the visible ordered set from step 3/4.
7. For each extracted article, resolve metadata with this priority:
   - title from card headline or article page `h1`
   - author from card/byline; if missing, fetch article page and extract author
   - publication date from card/date label; if missing, fetch article page and extract date/time
   - direct article URL (always required)
   - formatted as a markdown table with columns: `Title | Author | Date | URL`
8. If the user asks to parse/summarize a specific article, fetch that article URL and extract the main body text.
9. If the user did not specify a summary type, ask which they want: `short`, `medium`, or `detailed`.

## Category Mode

The site organizes articles into categories: Church, Culture, Family, Forum, Reports, Resources, Society, and State. When the user asks for articles from a specific category, do this:

1. Fetch the homepage at `https://americanreformer.org/`.
2. Locate the section matching the requested category by its heading.
3. Extract article cards from that category section in display order.
4. If author/date are missing on the card, fetch each article page to fill metadata.
5. Return the same metadata as the standard workflow (title, author, date, URL).

If the category name is ambiguous or not found, list available categories and ask the user to clarify.

## Strict Mode (Homepage + Sitemap Cross-Check)

When the user asks for strict verification (for example "strict mode", "double-check", or "cross-check with sitemap"), do this:

1. Extract the latest feed from the homepage using the structure-based method above.
2. Attempt to fetch `https://americanreformer.org/sitemap_index.xml`.
3. If the sitemap index is available, fetch post sitemaps from it.
4. Build a candidate URL set from post sitemap entries.
5. Cross-check each homepage article URL against that set.
6. Return homepage order as primary output, plus a verification status for each item:
   - `verified` (present in post sitemap data)
   - `unverified` (missing from current sitemap fetch)
7. If any are unverified, include a short note explaining likely causes (cache delay, publication lag, or parser mismatch) and keep homepage results as source of truth for "latest visible on homepage."

Strict mode rules:

- Do not reorder homepage articles based on sitemap timestamps.
- Use sitemap only as a consistency check, not as the display-order source.
- If sitemap fetch fails (the site's sitemap endpoints are known to return 500 errors), report strict-mode degradation and return homepage-only results.

## Full Display Mode (Top 10 Digest)

When the user asks for a full display (for example "full display mode", "digest mode", "show all ten with summaries"), do this:

1. Extract the latest homepage feed using the structure-based method.
2. Select the first 10 articles in homepage order.
3. For each article:
   - fetch the article page
   - extract title
   - extract author (or `not listed`)
   - produce a brief summary paragraph (2-4 sentences, neutral tone)
4. Return a clean markdown digest using this format:

```markdown
# American Reformer Latest 10 Digest

1. ## [Article Title](article-url)
   **Author:** Name
   **Summary:** Brief paragraph...

2. ## [Article Title](article-url)
   **Author:** Name
   **Summary:** Brief paragraph...
```

Full display rules:

- Keep article order exactly as shown on the homepage.
- Keep each summary concise and faithful to the article text.
- Do not invent metadata; use `not listed` when missing.
- If one article fails to parse, include a short failure note for that item and continue with the rest.

## Extraction Strategy (Structure-Based)

Use generic page structure to isolate the latest feed:

- Prefer repeated article-card patterns (title + excerpt + link) in a shared container.
- Use heading/link repetition (`h2`/`h3` post titles linked to same-domain post URLs) to identify cards.
- Exclude nav menus, category lists, featured widgets, "you may also like" blocks, and footer links.
- Do not use any fixed title text (for example, do not anchor on one known article name).
- Preserve homepage order exactly as displayed.
- Recognize category section headings (Church, Culture, Family, Forum, Reports, Resources, Society, State) to distinguish category feeds from the main "Latest Articles" feed.
- Treat the top "Latest Articles" section as primary. When it contains only one featured post, treat category sections as continuation content for "latest articles" output.
- Prefer direct post URLs from card anchors; if a URL is missing in extracted text, fetch/render page structure again before returning.

Metadata extraction hints (article page):

- Author often appears in byline elements or metadata labels (for example `author`, `by`, or `By ...` text).
- Date often appears in `time` elements, date labels, or article metadata blocks.
- If multiple dates appear, use the publication date (not "updated" unless publication is unavailable).

Fallback logic:

1. If container classes/ids are unavailable, infer the feed from contiguous repeated post-card headings with same-domain links.
2. Validate extracted URLs as post-like paths on `americanreformer.org`.
3. If ambiguity remains, return candidate list and ask the user to confirm scope.

## Summary Modes

Use exactly one mode per response:

- `short`: 3-5 bullets with core claims only.
- `medium`: 1 concise paragraph plus 3 bullets of key points.
- `detailed`: sections for Thesis, Key Points, Notable Quotes, and Takeaways.

## Output Rules

- Always include the article URL in the response.
- Always include title, author, and publication date for each returned article.
- Default output format for article lists is a markdown table using exactly these columns in this order: `Title | Author | Date | URL`.
- Distinguish clearly between extracted facts and interpretation.
- Do not stop at homepage snippets if author/date are missing; fetch the article page to complete metadata first.
- If metadata still cannot be found after article-page fetch, say `not listed` instead of guessing.
- Keep wording neutral and faithful to the article.
- If parsing fails due to site structure, report the failure and provide next-best available metadata from the homepage.

## Example Requests

- "Get me the latest American Reformer article."
- "Get the latest articles in strict mode and verify with sitemap."
- "Use full display mode for the latest ten articles."
- "Show me the latest Church articles from American Reformer."
- "Parse this American Reformer article and summarize it: <url>"
- "Summarize the latest article in detailed mode."
