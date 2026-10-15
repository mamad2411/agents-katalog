---
name: notion-search
description: Search Notion for pages or databases by query using marknotion. Use when the user references a Notion page by name rather than URL, when locating a page to publish to or pull from, or when discovering what trackers and docs exist in the connected workspace.
---

# Notion Search

Find Notion pages and databases by free-text query via the `notion-search` CLI
from the `marknotion` PyPI package, invoked through `uvx` so no install is
required.

## Prerequisites

1. `uv` is installed. If `command -v uv` fails, stop and instruct the user to
   install it.
2. `NOTION_TOKEN` is set in the environment. If unset, stop and instruct the
   user to create an internal integration at
   https://www.notion.so/my-integrations and export the token.
3. Search results only include pages and databases that are connected to the
   integration. An empty result usually means the target was never shared with
   the integration, not that it does not exist.

## Inputs

Resolve from `$ARGUMENTS` or by asking the user:

- `query`: free-text query (required).
- `--type page` or `--type database` (optional): narrow by object type.
- `-n <N>` (optional): cap the number of results. Default to a small N (5-10)
  to keep output readable.

## Workflow

1. Verify prerequisites above.
2. Run the command:

   ```bash
   uvx --from marknotion notion-search "<query>" [--type page|database] [-n <N>]
   ```

3. Present results as a short list: title, type, ID or URL.
4. If the goal is to feed a downstream skill (`notion-publish`, `notion-pull`),
   ask the user to confirm which result to use before proceeding.

## When to use this skill internally

When `notion-publish` or `notion-pull` is invoked with a page name rather than
a URL or ID, call this skill first to resolve the name to an ID. Never guess
a page ID.

Reporting only. Do not modify any pages.
