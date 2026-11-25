---
name: use-defuddle
description: Extracts clean, readable content from web pages using the defuddle CLI - strips ads, navigation, and clutter to produce markdown or JSON. Use when saving web content to files, clipping articles to Obsidian, extracting article metadata, or converting web pages to clean markdown. Do NOT use for fetching raw URLs or already-markdown content; use the harness's available raw web fetch/extract tool instead.
---

# use-defuddle

## Essential Principles

- **Always use `--md`** - markdown output is more useful than raw HTML for note-taking, summarisation, and storage. Only omit for HTML-specific processing
- **Use `--json` for metadata** - when you need title, author, date, description, or domain alongside the content. JSON output includes both metadata and content in a single call
- **Use `-p` for single properties** - `defuddle parse <url> -p title` is cheaper than `--json` when you only need one field
- **Prefer defuddle for articles and documentation** - it strips navigation, ads, sidebars, and comments. Use the harness's raw web fetch/extract tool for raw Markdown URLs or when you need the full unprocessed page
- **Confirm with user before writing files** - `defuddle -o` writes to disk; derive filename from `-p title` when not specified, then confirm before writing
- **Fall back to the available web fetch/extract tool on empty output** - paywalled pages, JavaScript-heavy SPAs, and some dynamic sites produce empty or incomplete content. Use `web_extract` in Pi, `WebFetch` in Claude Code, or ask the user for pasted/exported content if no web fallback exists

## Prerequisites

```bash
command -v defuddle >/dev/null 2>&1
```

If not found: `npm install -g defuddle`.

## Quick Start

```bash
defuddle parse https://example.com/article --md          # clean markdown to stdout
defuddle parse https://example.com/article --json        # metadata + content as JSON
defuddle parse https://example.com/article -p title      # extract title only
defuddle parse https://example.com/article --md -o note.md  # save to file
defuddle parse page.html --md                            # parse local HTML file
```

## Extracting Content

```bash
defuddle parse <url> --md
defuddle parse <url> --md -l en                          # prefer English content
```

| Flag | Purpose |
|------|---------|
| `--md` / `--markdown` / `-m` | Convert to markdown (preferred) |
| `-o <file>` | Write output to file instead of stdout |
| `-l <code>` | Preferred language (BCP 47: `en`, `fr`, `ja`) |
| `--debug` | Include extraction diagnostics |

Source can be a URL or a local HTML file path.

## Extracting Metadata

```bash
defuddle parse <url> --json
```

JSON output includes: `title`, `author`, `description`, `domain`, `favicon`, `image`, `lang`, `published`, `siteName`, `schemaOrg` (nested JSON-LD object), `wordCount`, and `content`.

To extract a single property without the full JSON:

```bash
defuddle parse <url> -p title
defuddle parse <url> -p published
```

## Web Clipping to Obsidian

When used with the `obsidian` CLI, defuddle enables a web clipping workflow:

```bash
# Extract content and create a note
content=$(defuddle parse <url> --md)
obsidian create name="Article Title" content="$content"

# Or with metadata as frontmatter
json=$(defuddle parse <url> --json)
# Extract fields from JSON, build note with properties, then:
obsidian create name="Article Title" content="$note_content"
obsidian property:set name="source" value="<url>" file="Article Title"
obsidian property:set name="author" value="Author Name" file="Article Title"
```

## Success Criteria

- `--md` used by default for content extraction
- `-p` used for single metadata fields, `--json` for multiple
- Source URLs are valid and accessible
