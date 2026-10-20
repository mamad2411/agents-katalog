---
allowed-tools: Agent, Read, Glob, Grep, Write, Edit
description: Research the codebase to answer questions by spawning parallel agents and synthesizing findings
argument-hint: [research question or area of interest]
model: opus
---

# Purpose

Conduct comprehensive, read-only research across the codebase to answer the user's question described in `$ARGUMENTS`. Follow the `Instructions` and `Workflow` to decompose the question into parallel agent tasks, synthesize findings, and produce a research document.

## Variables

RESEARCH_QUESTION: $ARGUMENTS
OUTPUT_DIR: temp/research
DATE: !`date +%Y-%m-%d`
GIT_COMMIT: !`git rev-parse --short HEAD`
BRANCH: !`git branch --show-current`
REPO: !`git rev-parse --show-toplevel`

## Instructions

- **You are a documentarian, not a critic.** Describe what exists — never suggest improvements, critique implementation, or propose changes unless the user explicitly asks.
- Read any files the user mentions FULLY (no limit/offset) before spawning agents.
- Decompose the research question into independent sub-questions and run them as parallel Agent tasks (subagent_type: Explore).
- Each agent prompt should be specific and focused on read-only operations.
- Always include concrete file paths and line numbers in findings.
- Prioritize live codebase findings as the primary source of truth.
- Never write the research document with placeholder values — gather all metadata first.
- ultrathink about the underlying patterns, connections, and architectural implications before decomposing the question.

## Workflow

1. **Read mentioned files** — if the user's question references specific files, read them fully in the main context before proceeding.
2. **Decompose the question** — break the research question into 2-6 independent sub-questions suitable for parallel exploration.
3. **Spawn parallel agents** — launch one Explore agent per sub-question. Each agent should:
   - Search for relevant files via Glob/Grep
   - Read and document how the code works
   - Return file paths, line numbers, and factual descriptions
4. **Wait and synthesize** — wait for ALL agents to complete, then connect findings across components.
5. **Write research document** — save to `OUTPUT_DIR/DATE-description.md` using the report format below. If a ticket is referenced, include it: `DATE-ENG-XXXX-description.md`.
6. **Present summary** — give the user a concise summary with key file references and ask if they have follow-ups.
7. **Handle follow-ups** — append new sections to the same document, updating frontmatter `last_updated` and `last_updated_by` fields.

## Report

Write the research document in this format:

```markdown
---
date: [ISO datetime with timezone]
researcher: Claude
git_commit: [commit hash]
branch: [branch name]
repository: [repo name]
topic: '[research question]'
tags: [research, codebase, relevant-component-names]
status: complete
last_updated: [YYYY-MM-DD]
last_updated_by: Claude
---

# Research: [Topic]

## Research Question

[Original query]

## Summary

[High-level answer describing what was found]

## Detailed Findings

### [Component/Area 1]

- What exists and where (file:line)
- How it connects to other components
- Implementation details

### [Component/Area 2]

...

## Code References

- `path/to/file.ts:123` - Description
- `another/file.ts:45-67` - Description

## Architecture Documentation

[Patterns, conventions, and design found in the codebase]

## Open Questions

[Areas needing further investigation, if any]
```
