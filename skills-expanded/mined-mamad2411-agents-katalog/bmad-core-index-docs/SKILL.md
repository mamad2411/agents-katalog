---
name: bmad-core-index-docs
description: >-
  Use this skill to generate or update an index.md file that references all
  documents in a target directory with brief, content-derived descriptions.
  Invoke when the user says "create an index of files in this folder", "update
  the index", or when a documentation directory needs a navigable entry point.
  The skill scans the specified directory, reads each document to extract
  meaningful one-line descriptions, and assembles them into an alphabetically
  ordered index with relative paths and clean markdown formatting. If an
  index.md already exists it is updated in place, preserving any custom
  introductory content while refreshing the file list. Requires a target
  directory path as input. Best for documentation directories, artifact folders,
  wiki sections, and any location where humans or AI agents need a consistent,
  accurate overview of available files.
argument-hint: "Provide the target directory path to index."
metadata:
  bmad:
    module: core
    type: task
---

# Index Docs

Generates or updates an index.md to reference all docs in a folder.

## Outcome

A well-organized `index.md` file listing all documents in the target folder with brief descriptions based on actual file content, using relative paths and alphabetical ordering within groups.

## Core Rules

- Execute ALL steps in order. Do not skip or reorder.
- HALT immediately when halt-conditions are met.
- Each action within a step is REQUIRED.

## Inputs

- **target_directory** (required) — Path to the folder to index

## Execution Order

Follow these steps in order.

1. [Scan Directory](./steps/scan-directory.md) — List all files and subdirectories in the target location
2. [Generate Index](./steps/generate-index.md) — Create or update index.md with organized file listings

## Halt Conditions

- HALT if target directory does not exist or is inaccessible
- HALT if user does not have write permissions to create index.md

## When to Use

Use this skill when:
- The user requests to create or update an index of all files in a specific folder
- A directory needs an `index.md` file listing all documents with brief descriptions based on actual file content
- The user provides a target directory path to index

