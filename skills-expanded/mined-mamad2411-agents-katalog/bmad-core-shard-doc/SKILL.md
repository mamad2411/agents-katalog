---
name: bmad-core-shard-doc
description: >-
  Use this skill to split a large markdown document into smaller, organized
  section files based on level 2 headings, using npx
  @kayvan/markdown-tree-parser. Invoke when the user says "shard this
  document", "split this doc", or when a large markdown file needs to be broken
  into navigable, independently usable pieces. The skill parses the source
  document, creates one file per H2 section with clean filenames derived from
  heading text, and generates an index.md entry point linking all sections. The
  original document is then handled per user preference: delete, archive to a
  specified location, or keep in place. Requires the source document path as
  input; destination folder is optional and defaults to a subdirectory named
  after the source file. Depends on Node.js and npx being available. Best for
  large PRDs, architecture docs, wikis, or any monolithic markdown file that has
  grown unwieldy.
argument-hint: "Provide the source document path and optionally the destination folder."
metadata:
  bmad:
    module: core
    type: task
---

# Shard Document

Split large markdown documents into smaller, organized files based on level 2 sections using npx @kayvan/markdown-tree-parser.

## Outcome

A large markdown document split into organized section files with an `index.md` entry point, and the original document handled per user preference (delete, archive, or keep).

## Core Rules

- Execute ALL steps in order. Do not skip or change sequence.
- HALT immediately when halt conditions are met.
- Each action within a step is required.

## Execution Order

Follow these steps in order.

1. [Setup Sharding](./steps/setup-sharding.md) — Get source document path, verify it exists, determine destination folder
2. [Execute and Verify](./steps/execute-and-verify.md) — Run the sharding command, verify output, report results
3. [Handle Original](./steps/handle-original.md) — Present options for the original document (delete, move, keep)

## Halt Conditions

- HALT if source file not found or not markdown format.
- HALT if permission denied for destination.
- HALT if npx command fails or produces no output files.

## When to Use

Use this skill when:
- The user says "shard this document", "split this doc", or invokes to break up a large markdown file
- A large markdown document needs to be split into smaller, organized files based on level 2 sections using `npx @kayvan/markdown-tree-parser`
- The user provides a source document path and optionally a destination folder

