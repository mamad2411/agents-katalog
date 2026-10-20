---
allowed-tools: Bash, Read, Glob, Grep, Write
description: Read all READMEs and regenerate the prime command with fresh context paragraphs
model: sonnet
---

# Purpose

Reads all README files in the codebase, produces three ultra-concise context paragraphs, and overwrites `.claude/commands/prime.md` with the updated content. See `Instructions` for paragraph specs and `Workflow` for execution steps.

## Instructions

- Paragraph 1 (288 char max): What the product is. Name, purpose, core capability, app structure.
- Paragraph 2: Core user journey as arrow-connected steps. Skip generic steps (login, pay, etc). Focus on the proprietary value prop pipeline from content browsing through feedback loop.
- Paragraph 3: Stack summary. Technologies only, how they layer. No detail, just names and roles.
- The output prime.md must use the exact template in the Workflow section.
- Do not invent information — derive everything from the README files.

## Workflow

1. Find all non-node_modules README files: `Glob` for `**/README.md` excluding `node_modules`
2. Read every README found (in parallel)
3. Synthesize the three paragraphs per the `Instructions`
4. Write `.claude/commands/prime.md` with this exact template, inserting the three paragraphs where indicated:

```
---
allowed-tools: Bash, Read, Glob, Grep
description: Prime context by reading core files and summarizing codebase understanding
model: sonnet
---

# Prime

Execute the `Run`, `Read` and `Report` sections to understand the codebase then summarize your understanding.

## Context

<paragraph 1: product summary, 288 char max>

<paragraph 2: user journey as arrow-connected steps>

<paragraph 3: stack summary>

## Run

git ls-files

## Read

### Core (always read these):

- @README.md
- @convex/schema.ts

### Optional (read these only if needed):

#### Backend
- @convex/README.md

#### Web apps
- @apps/*/README.md

## Report

Summarize your understanding of the codebase.
```

## Report

Confirm the prime command was updated and print the three generated paragraphs.
