---
name: harvest-my-likes
description: Read X/Twitter posts or collect recent likes through Chrome or the built-in browser, including scrapbook updates and Obsidian archives.
---

# Harvest My Likes

Capture a faithful, traceable record of the requested posts or likes. Preserve
who said what, the full content, source links, and the user's existing notes.
Choose browser reads that resolve missing content without collecting unrelated
timeline material.

Use Chrome or the built-in browser through the agent's browser tools. Follow the user's browser choice; otherwise prefer a signed-in session. Do not use `agent-browser`. If neither browser has access, ask the user to sign in.

## Read posts

Open the supplied post URLs; for a bare status ID, use `https://x.com/i/status/ID`.

Treat the status ID as the post's identity. Keep replies and quoted posts
separate from the requested post, with their own attribution and links. Read
through truncation and article previews to capture the full requested body.
Preserve paragraphs, mentions, emoji, and working link destinations; inline
spans and shortened display URLs can distort an otherwise correct extraction.

If a post is unavailable, report its URL and the access or loading problem.
Return only content you could establish from the requested source.

## Collect likes

Open `https://x.com/i/history/likes` in the signed-in browser and confirm the Likes tab. X also redirects the profile's `/HANDLE/likes` URL there. For scrapbook updates, read the existing file first and collect its status IDs for deduplication.

Collect unique post URLs in timeline order, keeping each top-level post separate from its quoted links. Stop at the first known status, the requested count, the end of the timeline, or no progress. Open the collected URLs to read their full content.

Default to at most 25 new posts and 8 timeline scrolls per batch. Long X timelines can consume several GiB of browser memory. Save a partial batch and report where collection stopped; do not increase those limits to force a catch-up. Close tabs you created when done, preserving the user's existing tabs.

Merge new entries without duplicating status IDs or rewriting existing notes. Preserve the destination's format. Keep timeline order; a post's publication date does not tell you when the user liked it.

## Optional Obsidian archive

Use `scripts/render_x_archive_markdown.mjs` when the user wants a local archive with downloaded images. Otherwise write the requested output directly.

The renderer accepts a JSON array of posts or an object with a `posts` array. Each post uses `url`, `id` (a string), `author_handle`, `author_name`, `created_at`, and `text`. Optional fields:

- `author_url`
- `markdown`: formatted content, including quoted posts with attribution and source links; overrides `text` in the archive
- `media`: image objects with `url`, optional `download_url`, and `alt`; distinguish video thumbnails from video files
- `reason`: an extraction problem to show in the archive

```bash
node scripts/render_x_archive_markdown.mjs \
  --input /path/to/posts.json \
  --output /path/to/archive.md \
  --attachments-dir attachments \
  --image-width 360
```

Resolve the script path relative to this skill. The renderer writes a new archive; merge it into an existing scrapbook separately. Check the result for missing content, broken mentions or URLs, and failed image downloads.
