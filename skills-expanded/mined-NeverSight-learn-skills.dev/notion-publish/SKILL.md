---
name: notion-publish
description: Publish a local Markdown file to a Notion page using marknotion. Use when the user wants to push README, docs, changelogs, or any Markdown content to Notion, either updating an existing page or creating a new one under a parent page.
---

# Notion Publish

Push a Markdown file to a Notion page via the `md2notion` CLI from the
`marknotion` PyPI package, invoked through `uvx` so no install is required.

## Prerequisites

1. `uv` is installed. If `command -v uv` fails, stop and instruct the user to
   install it (`curl -LsSf https://astral.sh/uv/install.sh | sh`).
2. `NOTION_TOKEN` is set in the environment. If unset, stop and instruct the
   user to create an internal integration at
   https://www.notion.so/my-integrations and export the token.
3. The target Notion page (or its parent) must already be connected to that
   integration via the page's "Connections" menu. The CLI will fail otherwise.

## Inputs

Resolve from `$ARGUMENTS` or by asking the user:

- `file`: path to the local Markdown file (required).
- One of:
  - `--page <url-or-id>`: update an existing Notion page in place.
  - `--parent <page-id> --title <title>`: create a new page under that parent.

## Workflow

1. Verify prerequisites above. Do not proceed if any check fails.
2. Confirm the Markdown file exists and is non-empty.
3. Show the user the exact command you are about to run, including which page
   will be overwritten. Ask for confirmation before running if `--page` is
   used, since updating a Notion page replaces its content.
4. Run the command:

   ```bash
   # Update an existing page
   uvx --from marknotion md2notion <file> --page "<url-or-id>"

   # Or create a new page under a parent
   uvx --from marknotion md2notion <file> --parent "<parent-id>" --title "<title>"
   ```

5. Report the returned page URL.

## Limits

marknotion supports a Markdown subset: headings h1-h3, paragraphs, bold,
italic, strikethrough, inline code, links, bullet and numbered lists, fenced
code blocks with language, blockquotes, horizontal rules. Anything else
(tables, images, callouts, toggles, h4+) is dropped or downgraded silently.
If the source file uses unsupported features, warn the user before publishing.

Do not edit the Markdown file. Do not commit. Reporting only after the push.
