---
name: acli
description: This skill should be used when the user asks to interact with any atlassian product- jira, confluence, etc. Trigger phrases include: "create a ticket", "jira ticket", "create subtasks", "break this ticket down", "view issue", "update ticket", "link to ticket", any mention of a Jira issue key (e.g. SDK-1234), "confluence page", or any request to read/write Jira or Confluence. Use `acli jira workitem view <KEY>` to fetch ticket details.
version: 1.0.0
---

# ACLI Skill

## Overview

Uses the `acli` command line to create, list, delete, update information from atlassian products.

## CLI Reference

```bash
acli jira workitem view <KEY>          # View a ticket
acli jira workitem create [flags]      # Create a ticket
acli jira workitem edit <KEY> [flags]  # Edit a ticket
acli jira workitem search [flags]      # Search tickets
acli jira workitem link [flags]        # Link tickets
```

Key `create` flags: `--project`, `--type`, `--summary`, `--description`, `--description-file`, `--assignee`, `--parent`, `--label`

**Important**: Use `--type "Sub-task"` (not "Task") when creating child tickets under a parent. Task-under-Task hierarchy is rejected by the API.

## Description format: ADF, never Markdown

**Never** pass Markdown to `--description`. Jira does not parse Markdown - `##`, `-`, `` ` ``, `[text](url)` will render as literal characters. Always use **Atlassian Document Format (ADF)** via `--description-file`.

### Workflow

1. Write the ADF document to a file (e.g. `/tmp/<KEY>-adf.json`).
2. Validate it: `jq -e . <file> > /dev/null`.
3. Pass it via `--description-file <file>` on `create` or `edit`. Both flags support ADF.
4. After the call, verify with `acli jira workitem view <KEY>` - note the CLI view flattens ADF for terminal display (no `##`, no `-`); confirm rich rendering in the browser.

### ADF skeleton

```json
{
  "version": 1,
  "type": "doc",
  "content": [ /* block nodes */ ]
}
```

### Block nodes (the ones you actually need)

- **Heading**: `{ "type": "heading", "attrs": { "level": 2 }, "content": [{ "type": "text", "text": "..." }] }`
- **Paragraph**: `{ "type": "paragraph", "content": [ /* inline nodes */ ] }`
- **Bulleted list**: `{ "type": "bulletList", "content": [ /* listItem nodes */ ] }`
- **Numbered list**: `{ "type": "orderedList", "content": [ /* listItem nodes */ ] }`
- **List item**: `{ "type": "listItem", "content": [{ "type": "paragraph", "content": [ /* inline nodes */ ] }] }`
- **Code block**: `{ "type": "codeBlock", "attrs": { "language": "ts" }, "content": [{ "type": "text", "text": "..." }] }`
- **Blockquote**: `{ "type": "blockquote", "content": [{ "type": "paragraph", "content": [ /* inline nodes */ ] }] }`

### Inline marks (applied via `"marks": [...]` on a `text` node)

- **Inline code**: `{ "type": "code" }`
- **Link**: `{ "type": "link", "attrs": { "href": "https://..." } }`
- **Bold / italic / strike**: `{ "type": "strong" }` / `{ "type": "em" }` / `{ "type": "strike" }`

Marks compose - a linked piece of inline code carries both `code` and `link` marks on the same text node.

### Example: a paragraph with an inline-code link and a bulleted list

```json
{
  "version": 1,
  "type": "doc",
  "content": [
    {
      "type": "paragraph",
      "content": [
        { "type": "text", "text": "See " },
        {
          "type": "text",
          "text": "src/foo.ts",
          "marks": [
            { "type": "code" },
            { "type": "link", "attrs": { "href": "https://github.com/org/repo/blob/main/src/foo.ts" } }
          ]
        },
        { "type": "text", "text": " for context." }
      ]
    },
    {
      "type": "bulletList",
      "content": [
        { "type": "listItem", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "First item" }] }] },
        { "type": "listItem", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Second item" }] }] }
      ]
    }
  ]
}
```

### Gotchas

- A `listItem`'s content must be wrapped in a `paragraph` (or another block) - raw `text` nodes inside a `listItem` are rejected.
- Use straight ASCII punctuation in `href` values; smart quotes break links.
- Em-dash (`-`) in body text is fine, but don't put it in resource names (cloud-API rule still applies to anything that flows back out to an SDK call).
- If you must dynamically build ADF in a shell pipeline, build with `jq -n` rather than string-concatenating JSON - quoting bugs in description bodies are silent and ship to Jira intact.

## Process

Analyse the request and decide which atlassian product to use. If the request satisfies multiple then use multiple products.

#### JIRA

If creating a JIRA ticket always assign it to the authenticated user. Give the ticket a well thought out description but be succint and err on the side of caution when attempting to infer additional details. Always write the description as ADF (see "Description format" above) - never pass Markdown to `--description`.
- If the ticket is talking about a certain part of the codebase, use the `gh` (github) CLI to link to the file or directory that is relevant.
  - This is useful if linking to parts of the codebase as reference points rather than what files to directly modify (you can try to figure this out but again err on side of caution).

If the request can be done in a better way, ask the user if they would like to do things that way.


### Confluence

Use `acli confluence` for Confluence pages. Always check `acli confluence --help` before using a subcommand whose flags are not already known.

```bash
acli confluence page list --space SPACE
acli confluence page view --space SPACE --title "Page Title"
acli confluence page create --space SPACE --title "Title" --body "Content"
```
