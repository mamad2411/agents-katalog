---
allowed-tools: Read, Write, Glob
description: Read one or more source files and produce a README.md at a given location
argument-hint: [source-file-paths (comma-separated)] [output-readme-path] [optional: consolidated]
model: opus
---

# Purpose

Read the files at `SOURCE_PATHS`, understand their purpose and content, then produce a README.md at `OUTPUT_PATH`. When `MODE` is `consolidated`, synthesize all source files into a single top-level README that covers all topics concisely. Follow the `Instructions` and `Workflow`.

## Variables

SOURCE_PATHS: $0
OUTPUT_PATH: $1
MODE: $2

## Instructions

- `SOURCE_PATHS` is a comma-separated list of file paths. Read every file fully before writing anything.
- If a source path is a directory, use Glob to discover key files and read the most important ones (entry points, config, package.json).
- If `MODE` is `consolidated`, produce ONE unified README that synthesizes all source files into a cohesive document — not a concatenation. Organize by theme, not by source file. This is for top-level project READMEs that span multiple topics.
- If `MODE` is omitted or empty, produce a standard README from the source files.
- The README must be **accurate** — only document what actually exists in the sources.
- The README must be **concise** — no filler, no boilerplate, no unnecessary sections. Omit sections that have nothing meaningful to say.
- Use short sentences. Prefer lists over paragraphs.
- Do not invent features, APIs, or behaviors not present in the sources.
- Do not add badges, contributing guides, or license sections unless they exist in a source.
- If `OUTPUT_PATH` already exists, overwrite it.

## Workflow

1. Parse `SOURCE_PATHS` by splitting on commas — trim each entry.
2. Read every source file or directory fully.
3. If `MODE` is `consolidated`:
   - Identify cross-cutting themes, architecture, and key concepts across all sources
   - Write a single README.md to `OUTPUT_PATH` that covers:
     - **Title** — project name
     - **Description** — what the project does (2-3 sentences max)
     - **Architecture** — high-level structure and how pieces connect
     - **Key Components** — brief description of each major area
     - **Getting Started** — setup, dev commands, prerequisites
     - **Configuration** — if configurable
     - **Tech Stack** — notable technologies and choices
4. If `MODE` is not `consolidated`:
   - Write a README.md to `OUTPUT_PATH` covering only relevant sections:
     - **Title** — name of the module/component/package
     - **Description** — one to two sentences on what it does
     - **Usage** — how to use it (imports, API, CLI, etc.)
     - **Configuration** — if configurable
     - **Dependencies** — only notable or non-obvious ones
     - **Structure** — brief file/directory layout if multi-file
5. Verify the written README by reading it back.

## Report

Confirm the README was written to `OUTPUT_PATH` and list the source files consumed.
