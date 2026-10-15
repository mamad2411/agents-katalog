---
name: notion-pull
description: Export a Notion page to local Markdown using marknotion. Use when the user wants to pull a spec, design doc, meeting notes, or any Notion page into the repository as a Markdown file, or wants to read Notion content as context for a task.
---

# Notion Pull

Export a Notion page to Markdown via the `notion2md` CLI from the `marknotion`
PyPI package, invoked through `uvx` so no install is required.

## Prerequisites

1. `uv` is installed. If `command -v uv` fails, stop and instruct the user to
   install it.
2. `NOTION_TOKEN` is set in the environment. If unset, stop and instruct the
   user to create an internal integration at
   https://www.notion.so/my-integrations and export the token.
3. The source Notion page must already be connected to that integration via
   the page's "Connections" menu. The CLI will fail otherwise.

## Inputs

Resolve from `$ARGUMENTS` or by asking the user:

- `page`: Notion page URL or page ID (required).
- `output` (optional): destination file path. If omitted, write to stdout and
  capture the result so the agent can use it as context.

## Workflow

1. Verify prerequisites above. Do not proceed if any check fails.
2. If `output` is provided, confirm the parent directory exists. Warn before
   overwriting an existing file.
3. Run the command:

   ```bash
   # Write to a file
   uvx --from marknotion notion2md "<page-url-or-id>" -o <output>

   # Or print to stdout (use when reading Notion content as task context)
   uvx --from marknotion notion2md "<page-url-or-id>"
   ```

4. Report the destination path and a short summary of what was pulled
   (heading count, length). If captured to memory for downstream use, say so.

## Limits

marknotion converts a Notion block subset: headings h1-h3, paragraphs, basic
text formatting, links, lists, code blocks, blockquotes, horizontal rules.
Tables, images, embeds, databases, callouts, toggles, and other rich blocks
are dropped or downgraded. If the user is pulling content that depends on
those (e.g. a spec with diagrams), warn that the export will be lossy.

Do not commit. Do not edit unrelated files.
