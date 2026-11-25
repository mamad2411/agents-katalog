---
name: plsreadme
description: Share markdown and text as clean, readable web links via plsreadme.com. Use when someone asks to share a document, README, PRD, notes, or any content as a shareable link. Also handles updating and deleting previously shared docs. Triggers for "create a preview link", "share this as a page", "update that shared doc", or "delete that link".
---

# plsreadme

Share content as clean `plsrd.me` links. Supports create, update, delete, and list.

## Setup

Add the MCP server to your client:

```json
{
  "mcpServers": {
    "plsreadme": {
      "command": "npx",
      "args": ["-y", "plsreadme-mcp"]
    }
  }
}
```

Or use the remote endpoint (zero install):

```json
{
  "mcpServers": {
    "plsreadme": {
      "url": "https://plsreadme.com/mcp"
    }
  }
}
```

## Tools

- **`plsreadme_share_file`** — Share a local file by path. If the file was previously shared, updates the existing link instead of creating a new one.
- **`plsreadme_share_text`** — Share text directly (markdown or plain text). Plain text is auto-structured into markdown.
- **`plsreadme_update`** — Update an existing doc by ID or original file path with new content.
- **`plsreadme_delete`** — Delete a doc permanently by ID or file path.
- **`plsreadme_list`** — List all tracked shared documents.

## .plsreadme Record File

The MCP server tracks shared documents in a `.plsreadme` JSON file in the project root. This file contains admin tokens needed for edit/delete operations.

**Important:** Add `.plsreadme` to your `.gitignore` to keep admin tokens out of version control.

If the tool warns about `.gitignore`, follow its instructions immediately.

## Usage Guidelines

- Max file size: 200KB
- Links are permanent and publicly accessible — confirm with the user before sharing sensitive content
- If input is non-markdown, refactor it with your own model first (or let the tool auto-structure plain text)
- Re-sharing the same file updates the existing link (same URL, new content)
- The first `# Heading` becomes the document title
- Output includes a readable URL and a raw markdown URL

## Example Prompts

- "Share this README on plsreadme"
- "Create a shareable link for docs/api.md"
- "Update the shared link for my PRD"
- "Delete that plsreadme link I made earlier"
- "List all my shared docs"
- "Turn these rough notes into a readable link"
