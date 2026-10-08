---
name: ingest-db
description: Ingests already-extracted content links (blog/Substack/newsletter and YouTube) into the project's MongoDB via `npm run ingest`. Takes a set of items — each with a title, URL, and category — builds the JSON file the ingest script expects, and runs the pipeline, which assigns the next global srNo and skips URLs already in the DB. Use after links have been extracted (e.g. by the `ig-content-links` skill) and the user asks to "ingest", "save to the db", "add to the database", or "store these links". This is the second half of the `ig-links-to-db` orchestrator, but can also be run standalone on a list of links or an existing extraction markdown file.
---

# Ingest Content Links into the DB

This skill takes a set of content items (title + URL + category, optionally tags/notes/source) and writes them into the project's MongoDB using the existing ingest script (`scripts/ingest.ts`, run via `npm run ingest`). The script assigns the next global `srNo` and **skips any URL that already exists**, so re-ingesting is always safe.

## Inputs

You need, for each item:
- **title** — the exact post/video title (required)
- **url** — the canonical resolved URL (required; never fabricate one)
- **category** — must be exactly `"blog"` (Substack/newsletter/blog posts) or `"youtube"` (videos)
- **tags** — optional array of strings
- **notes** — optional string (e.g. "Recommended in reel about must-read substacks")
- **sourceInstagramUrl** — the originating IG reel/post URL (can be set once at the top level and applied to all items)

If you're handed a markdown file produced by `ig-content-links` instead of structured items, read it and map each entry: Blog Posts → `category: "blog"`, YouTube Videos → `category: "youtube"`.

## Steps

### 1. Build the JSON file

Write a JSON file into `scripts/` (name it after the source, e.g. `scripts/reel-<shortcode>-links.json`, or `scripts/ingest-<something>.json` for ad-hoc batches). Use the object form so a single `sourceInstagramUrl` applies to every item:

```json
{
  "sourceInstagramUrl": "https://www.instagram.com/reel/<shortcode>/",
  "items": [
    {
      "title": "Exact Post Title",
      "url": "https://someone.substack.com/p/exact-post",
      "category": "blog",
      "tags": ["substack"],
      "notes": "Recommended in the reel about must-read substacks (@handle)."
    },
    {
      "title": "Exact Video Title",
      "url": "https://www.youtube.com/watch?v=VIDEOID",
      "category": "youtube",
      "tags": ["tutorial"],
      "notes": ""
    }
  ]
}
```

Notes on the shape (see `scripts/ingest.ts` for the source of truth):
- The top-level `sourceInstagramUrl` is applied to any item that doesn't set its own.
- An item that omits `tags` defaults to `[]`; omit `notes` and it defaults to `""`.
- A plain array of items (no wrapping object) is also accepted, but then set `sourceInstagramUrl` on each item.

When ingesting from **multiple** Instagram sources in one batch, do NOT use the shared top-level `sourceInstagramUrl` — instead set `sourceInstagramUrl` on each individual item so every row keeps its correct origin.

### 2. Run the ingest

Run through the **PowerShell** tool (the Bash tool on this machine cannot spawn node):

```powershell
npm run ingest -- scripts/<your-file>.json
```

The script prints one line per item — `+ [#<srNo>] (<category>) <title>` for additions, `= skip (already exists)` for duplicates — and a final `Done. Added N, skipped M.`

### 3. Report

Tell the user exactly what was added vs. skipped, quoting the `srNo` assigned to each new row. Do not claim success unless the script printed `Done.` — if it errored (e.g. missing `.env.local` / Mongo connection), surface the actual error instead.

## Notes

- Requires `.env.local` (Mongo connection string) to be present — the script loads it via dotenv. If the connection fails, report it; don't retry blindly.
- `category` MUST be `blog` or `youtube`; any other value will be stored as-is and is almost certainly a mistake — map to one of the two.
- Never invent URLs. Only ingest links that were actually resolved/confirmed.
- Keep the generated JSON files in `scripts/` — they double as a re-runnable record of what was ingested.
