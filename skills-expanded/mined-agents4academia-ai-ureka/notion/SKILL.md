---
description: Ingest a Notion note into notes/ — live via the Notion MCP (page URL, page ID, or title to search) or from a local .md/.html export
argument-hint: <Notion URL | page ID | title | local export path> (e.g. "https://www.notion.so/Transformers-1a2b...", "Transformers Notes", "/path/to/notion_note_transformers.md")
allowed-tools: Read, Write(notes/**), Glob, Bash(date:*), Bash(python3:*), AskUserQuestion, mcp__notion__notion-search, mcp__notion__notion-fetch
---

Ingest a Notion note — a personal note — and produce a structured
`notes/notion_<slug>.md` file following the project template. This is the Notion
sibling of `/obsidian`; it is normally invoked by `/collate` as its ingestion
step, but can be run directly.

There are two input modes, both converging on the same extract → format → write:

- **Live (Notion MCP)** — preferred. **$ARGUMENTS** is a Notion page URL, a page
  ID, or a title to search for. The page is pulled from the live workspace with
  `mcp__notion__notion-fetch` (and `mcp__notion__notion-search` to resolve a title).
- **Local export** — **$ARGUMENTS** is a path to a `.md` or `.html` Notion export
  (wherever you keep it on your filesystem). Parsed directly, no MCP. This is the original
  no-MCP path and the fallback when the workspace isn't reachable.

If **$ARGUMENTS** is empty, ask the user for a Notion URL, page ID, title, or local
export path, then continue.

## Layout

Output goes to `notes/` at the repo root (personal notes, as opposed to objective
sources under `sources/`). The template is `.claude/Templates/note.md` and is authoritative
for the schema; you may read an existing `notes/notion_*.md` for style, but follow
the schema below over any older file.

## Step 0 — Route the input

Classify **$ARGUMENTS** and pick the mode. Check in this order:

1. **Notion URL** — contains `notion.so/` or `.notion.site/` → **MCP fetch** (Step 1M),
   passing the URL straight to `notion-fetch`.
2. **Local export** — ends in `.md` or `.html` (case-insensitive), or is an existing
   path on disk (confirm with `Glob`/`Read`) → **Local export** (Step 1L).
3. **Page ID** — a bare 32-hex string, with or without UUID dashes (e.g.
   `1a2b3c4d5e6f7890abcdef0123456789` or `1a2b3c4d-5e6f-7890-abcd-ef0123456789`) →
   **MCP fetch** (Step 1M), passing the ID to `notion-fetch`.
4. **Title / topic** — anything else → **MCP search** (Step 1S): search, confirm,
   then fetch.

## Step 1S — Resolve a title via search (MCP search mode)

Search the workspace and confirm the page with the user before ingesting (same
pattern as `/alphaxiv`'s title search):

```text
mcp__notion__notion-search  query="$ARGUMENTS"  query_type="internal"  page_size=5
```

- Show the top matches as a short numbered list — **title + URL** (and the parent /
  last-edited hint if present) for each.
- Ask the user which one to ingest (use `AskUserQuestion`). Do **not** auto-pick.
- If search returns nothing, tell the user and ask for a URL/ID or a different title.

Once the user confirms a match, take its page URL (or ID) and continue to **Step 1M**.

## Step 1M — Fetch the page (MCP fetch mode)

Fetch the page content from the live workspace:

```text
mcp__notion__notion-fetch  id="<the URL or page ID>"
```

`notion-fetch` returns the page in Notion-flavored Markdown wrapped in an envelope
(e.g. a `<page url="...">` tag with the page's properties and body; child databases
appear as `<data-source>` markers). When extracting in Step 2:

- Take the canonical **page URL** from the fetch envelope — this becomes the single
  `source_links` entry.
- Read **properties** from the page's property block (Tags, Status, Category,
  multi-select, etc.), not from the prose.
- Use the readable page **body** as the content; do **not** copy the envelope tags,
  the raw property block, or internal Notion block IDs into `## Content`.
- Preserve Notion structures as Markdown: headings, lists, to-do checkboxes,
  callouts, toggles, quotes, code blocks, tables, equations, and any internal links
  (relative `.md` links or `https://www.notion.so/...` URLs) verbatim.

Then go to **Step 2**.

## Step 1L — Read the export (local export mode)

Read the export at **$ARGUMENTS** and pull out title, properties, and body. Route by
extension:

- **`.md`** — use `Read` directly; Notion markdown is clean.
- **`.html`** — strip tags to text first:
  ```bash
  python3 -c "
  import sys
  from pathlib import Path
  from html.parser import HTMLParser
  class T(HTMLParser):
      def __init__(self): super().__init__(); self.out=[]
      def handle_data(self,d): self.out.append(d)
  p=T(); p.feed(Path(sys.argv[1]).read_text(encoding='utf-8'))
  sys.stdout.write(''.join(p.out))
  " "$ARGUMENTS"
  ```

Local Notion exports carry a few **Notion-isms** the live MCP path doesn't:

- **Filenames and the H1 carry a trailing 32-hex page ID** in real exports, e.g.
  `Transformers Notes 1a2b3c4d5e6f7890abcdef0123456789.md` and a matching
  `# Transformers Notes 1a2b3c4d...`. Strip that trailing hex blob from both.
- **A leading property block** often follows the H1 — either `Key: value` lines or a
  small markdown table — holding Notion page properties (Tags, Status, Category,
  multi-select). It is metadata, not prose.
- **Internal links** appear as relative `.md` links (`[Name](Some%20Page%20<hex>.md)`)
  or `https://www.notion.so/...` URLs. Preserve these verbatim.
- The fixtures in this repo are **clean** notes with none of the above — handle that
  case too (no markers ⇒ derive concepts from the content alone).

For local mode the `source_links` entry is **$ARGUMENTS** verbatim. Then go to **Step 2**.

## Step 2 — Extract

From whichever mode produced the page, identify:

- **`title`** —
  - *MCP:* the page title from the fetch envelope. Strip any trailing 32-hex ID if one
    leaked into it.
  - *Local:* the H1 (`# ...`) with any trailing 32-hex page ID stripped; if there is no
    H1, fall back to the filename stem (strip the trailing hex ID, replace
    `_`/`-`/`%20` with spaces) in Title Case.
- **Properties** — the page's property block (Tags, Status, Category, multi-select,
  keywords). Collect the values of any **tag-like** property, splitting
  comma-separated values. These are metadata — do **not** copy the raw property block
  into `## Content`.
- **Wikilinks and tags** — a Notion note **may** contain `[[wikilinks]]` and `#tags`
  (someone who dual-uses Obsidian, or types them by hand). When present, treat them
  exactly as `/obsidian` does: collect the target of each `[[wikilink]]` (the part
  before `|` if aliased, trimmed) and each `#tag` name (leading `#` stripped), and
  leave them in place inside the body — the navigator uses `[[wikilinks]]` as graph
  edges, so they must be preserved verbatim.
- **Body** — everything after the title and property block. Preserve the author's
  wording, headings, lists, code blocks, emphasis, `[[wikilinks]]`, `#tags`, and any
  internal links/URLs verbatim. Do not summarise unless the note is very long.
- **Language** — if body prose is in Vietnamese (or mixed), translate it to concise
  English preserving the original meaning; prose already in English is left unchanged,
  and code, math, identifiers, URLs, `[[wikilinks]]`, and `#tags` stay verbatim.
- **Length** — if the note is too long, summarise it to keep it concise while keeping
  the original meaning; preserve structure, math, links, `[[wikilinks]]`, and `#tags`.

## Step 3 — Format

Fill in the notion schema below. It extends the shared `.claude/Templates/note.md` (`type`,
`title`, `concepts_mentioned`, `source_links`); the schema here is authoritative for
notion notes.

- `type: notion_note`
- `title`: from Step 2.
- `source_links`: a YAML block list with a single entry:
  - *MCP:* the canonical Notion page URL from Step 1M.
  - *Local:* **$ARGUMENTS** verbatim.

      source_links:
        - <Notion page URL, or $ARGUMENTS for a local export>

- `concepts_mentioned`: an inline YAML list built from **three sources**, in this
  order, deduped at exact-string level preserving first occurrence:
  1. the `[[wikilink]]` targets and `#tag` names from Step 2 (if any);
  2. the tag-like property values from Step 2 (if any);
  3. the key topics named in the body — identified by judgment, since clean Notion
     notes carry no markers (e.g. `[transformers, self-attention, RLHF]`).
  Use `[]` only if the note has no discernible topics.
- `## Content`: the body from Step 2, faithfully preserved.

Before writing, verify the envelope:

- Starts with `---` on line 1; has a closing `---` delimiter.
- Contains exactly these four frontmatter keys: `type`, `title`, `source_links`,
  `concepts_mentioned`.
- `type` is the literal string `notion_note`.
- `source_links` is a YAML list whose single entry is the Notion page URL (MCP mode)
  or **$ARGUMENTS** verbatim (local mode).
- `concepts_mentioned` is a YAML list (possibly empty).
- Body contains a non-empty `## Content` section.

If any check fails, fix the envelope before writing.

## Step 4 — Write

Slugify the title to snake_case (lowercase, spaces/dashes → underscores, drop
non-alphanumeric characters). Write to `notes/notion_<slug>.md` with the `Write`
tool. If the file already exists, ask the user before overwriting.

## Step 5 — Propose

After writing, suggest the user:

- Run `/retrieve <topic>` to find related sources and existing pages.
- Run `/collate <topic>` to synthesise a paper or concept page from this note
  together with other sources on the same topic.

## Wrap up

Report: output file path, the title, the input mode used (live MCP or local export)
and the resolved page URL/path, the concepts extracted (noting whether they came from
`[[wikilinks]]`/`#tags`, properties, or the body), any `[[wikilinks]]`/`#tags`
preserved, and anything skipped (one-line reason each).
