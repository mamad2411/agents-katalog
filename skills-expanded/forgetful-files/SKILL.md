---
name: forgetful-files
description: >-
  File binary content into the knowledge base — screenshots, PDFs, diagrams, fonts, assets.
  Use when a binary artifact is worth keeping alongside knowledge, or when a stored
  procedure needs a bundled asset. The description is the entire search surface: say what
  the file shows and when to reach for it.
license: MIT
tags: [files, binary, assets, multi-modal]
allowed-tools:
  - mcp__forgetful__discover_forgetful_tools
  - mcp__forgetful__how_to_use_forgetful_tool
  - mcp__forgetful__execute_forgetful_tool
  - Bash(forgetful:*)
---

# Filing binary content

Files carry what text cannot: the screenshot that shows the bug, the architecture diagram,
the PDF spec, the font a design system needs. Mechanics are thin; the judgment is in the
description and the attachment.

File operations are feature-flagged — when discovery doesn't list them, the server has
`FILES_ENABLED` off.

## Invoking operations

Operations are named by registry name (`create_file`, `list_files`, ...). Invoke via
whichever surface this agent has:

- **MCP**: `execute_forgetful_tool(tool_name="create_file", arguments={...})`
- **CLI**: `forgetful call create_file --args '{"filename": "..."}' --json`

Get any operation's schema at runtime: `how_to_use_forgetful_tool` (MCP) or
`forgetful tools info <operation>` (CLI) — schemas are deliberately not repeated here.

## Step 1 — Store with a retrieval-grade description

`create_file` takes the content base64-encoded, with `filename`, `mime_type`, tags, and a
description. The description is what future retrieval sees — write what the file shows and
when someone would reach for it ("Auth service architecture diagram — component boundaries
and token flow, current as of the v2 redesign"), never just restating the filename.

Done when: the file is stored and its description answers "what is this and when is it
used" on its own.

## Step 2 — Attach it

A file no path leads to is lost the moment this session ends. Two attachment routes exist:

- `project_id` (at create, or later via `update_file`) puts the file in a project's world.
- `link_skill_to_file` bundles it to a stored procedure as its asset (see
  `forgetful-procedures`).

For knowledge that *discusses* the file, save a memory (`forgetful-remember`) that cites
the file ID in its content, so recall surfaces the pointer.

Done when: at least one route reaches the file — its project, a linked procedure, or a
citing memory.
