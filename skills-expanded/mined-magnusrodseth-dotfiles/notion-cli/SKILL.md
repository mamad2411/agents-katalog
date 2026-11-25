---
name: notion-cli
description: Interact with Notion via the `ntn` CLI — create, read, update, and trash pages; upload files; manage blocks via the public API. Use when the user wants to publish content to Notion, post a blog post or document to a Notion database, upload images to Notion, manage Notion pages from the command line, or asks about ntn / Notion CLI / NOTION_API_TOKEN / Notion integrations.
---

# Notion CLI (`ntn`)

Drive Notion from the terminal using the official `ntn` CLI. Covers page CRUD, file uploads, block operations, and the common workflow of publishing a markdown article (with images) into a database.

## Prerequisites

`ntn` must be installed and a Notion **integration token** must be available. Verify both:

```bash
ntn --version                                      # should print a version
[ -n "$NOTION_API_TOKEN" ] && echo ok || echo "missing token"
```

If the binary is missing, install with `curl -fsSL https://ntn.dev | NTN_INSTALL_DIR="$HOME/.local/bin" bash` (avoids the default `/usr/local/bin` permission prompt on macOS).

If the token is missing but a similarly-named var is set (e.g. `NOTION_API_KEY`), map it before running CLI commands: `export NOTION_API_TOKEN="$NOTION_API_KEY"`.

`ntn login` (OAuth flow) is **separate** from `NOTION_API_TOKEN` and only required for `ntn workers`. For `pages` and `files`, only the env var is required.

The integration must be invited to the target page or database from Notion's UI (the page's `...` menu → "Connect to integration"). Without that, fetches return `403 restricted_resource`.

## Quick start

Create a simple page in a database from inline markdown:

```bash
ntn pages create \
  --parent data-source:<DATA_SOURCE_ID> \
  --content $'# Title\n\nFirst paragraph.' \
  --json
```

Output (with `--json`) includes the new page's `id` and `url`.

To find `<DATA_SOURCE_ID>`: open the target database in Notion → copy the URL → strip dashes from the UUID. Or use `ntn api v1/data_sources/<id>` to inspect schemas.

## Common workflows

### Create a page with title and properties

`ntn pages create` accepts markdown content but does **not** set arbitrary properties. To set title, status, etc., create first, then PATCH:

```bash
PAGE_ID=$(ntn pages create --parent data-source:<DS_ID> --content "$MD" --json | jq -r .id)

ntn api "v1/pages/$PAGE_ID" -X PATCH \
  properties:='{"Name":{"title":[{"text":{"content":"My title"}}]},"Status":{"status":{"name":"Kladd"}}}'
```

For property JSON formats per type, see [REFERENCE.md](REFERENCE.md#property-formats).

### Upload a file

```bash
UPLOAD_ID=$(ntn files create \
  --filename banner.jpeg --content-type image/jpeg --json < banner.jpeg \
  | jq -r .id)
```

The upload is staged for **1 hour**; attach it to a page (as an image block, file block, etc.) within that window or it expires. Once attached, it lives forever.

### Insert an image into an existing page

Markdown `![]()` does **not** support `file_upload` IDs — it creates an empty external-image block. Use the API instead, with `--notion-version 2022-06-28` and an `after=<block_id>` anchor. For inserting at the top of a page (no native "prepend"), use the sentinel pattern. Full JSON shape, version gotcha, and sentinel workflow are documented in [REFERENCE.md](REFERENCE.md#the-after-parameter-and-api-version). The helper script below handles all of this.

### Publish a markdown article with images

For the full workflow (strip frontmatter and HTML comments, upload N images, create page, set properties, insert each image at a named anchor), use the helper script:

```bash
~/.claude/skills/notion-cli/scripts/markdown-to-page.py \
  --source /path/to/article.md \
  --parent data-source:<DS_ID> \
  --title "Article title" \
  --status Kladd \
  --images-json /path/to/images.json
```

See the script's `--help` and the `images.json` schema documented at the top of the file.

### Trash a page

```bash
ntn pages trash <PAGE_ID> --yes
```

Use `--yes` to skip the interactive confirmation in scripts.

## When you hit a wall

Common gotchas (H1 stripping in database pages, `after` requiring `--notion-version 2022-06-28`, immutable `image.type`, sentinel strings stripping punctuation, `403` on `v1/users` being normal, `NOTION_API_KEY` vs `NOTION_API_TOKEN`) and full JSON shapes for every block and property type are in [REFERENCE.md](REFERENCE.md). Consult it before improvising.
