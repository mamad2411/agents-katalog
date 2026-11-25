---
name: recall
description: This skill should be used when the user asks a general question about the project, its architecture, design decisions, agent pipeline, or codebase structure. It should also be used when the user asks "how does X work", "why was X done this way", or requests an explanation of existing behavior. Do not use this skill when the user is invoking a Smith Command (e.g., /smith:research, /smith:plan) or asking to create, modify, or implement something.
---

# Context Lookup

This skill scopes context collection to existing Smith research and plan documents before falling back to direct codebase exploration.

## When This Skill Applies

This skill activates for general questions about the project: architecture, design rationale, how something works, conventions, or trade-offs. It does not apply when the user is running a Smith pipeline Command or requesting code changes.

## Procedure

### 1. Resolve Output Directory

Check for a `.smith.local.yaml` file in the project root. If it exists, read the `output_directory` value. If absent, default to `docs/`. Use this as the base for all document paths below.

### 2. Check for Existing Documents

Glob for files in these directories (relative to the working directory):

- `<output_directory>/research/*.md`
- `<output_directory>/plans/*.md`

If no files exist in either directory, skip to step 4.

### 3. Select and Read Relevant Documents

Prefer documents already known to the current conversation (i.e., files read or produced earlier in this session). Among remaining candidates, prefer the most recently modified files. If there is exactly one file whose topic matches the question, use it. If there are multiple plausible matches and the best choice is ambiguous, **stop and ask the user** which document to consult before proceeding.

Read the selected document(s). If the answer is fully covered by the existing documents, respond directly from them. Cite the source file path when drawing from a specific document.

### 4. Fall Back to Exploration

If no existing documents are relevant, or they do not fully answer the question, proceed with normal codebase exploration (Glob, Grep, Read, or the Explore agent as appropriate). Do not re-research topics already covered by an existing document.
