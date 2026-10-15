---
name: decodie-explain
description: >-
  Explain a selected piece of code — what it does, how it works, potential
  issues, and improvement suggestions. Ephemeral by default (chat only),
  optionally saved to .decodie/ on explicit request.
license: MIT
metadata:
  author: owenbush
  version: "1.0"
---

# Decodie — Explain Mode

Walk a developer through a specific piece of code they have selected or pasted. Produces a conversational, human-readable explanation directly in the chat.

This mode is **read-only with respect to source code** and **ephemeral by default** — nothing is written to `.decodie/` unless the user explicitly asks to save.

## Scope and Inputs

Operates on code the user has selected, pasted, or pointed at. Does not scan projects or discover files.

If no code has been provided, ask the user to share the code they want explained.

## Output Format

Produce the explanation as **conversational markdown in the chat**. Do not write to disk unless asked.

### 1. Summary

A short paragraph (2-3 sentences) describing what the code does at a high level.

### 2. Detailed Breakdowns

For each complex or non-obvious section:
- A fenced code block with the **code excerpt**
- An **explanation** of what it does, why, and any patterns/idioms it uses
- The **pattern** name if applicable (e.g., "guard clause", "memoization")

Aim for 2-5 breakdowns depending on complexity. Skip trivial code.

### 3. Potential Issues

List bugs, security concerns, performance problems, edge cases. For each:
- **severity**: `info`, `warning`, or `error`
- **description**: what is wrong and when it manifests
- **suggestion**: how to address it

If you find no issues, say so plainly.

### 4. Improvements

Refactoring opportunities, modern alternatives, readability wins. For each:
- **description**: the proposed change
- **rationale**: why it helps

### 5. Key Concepts

Bulleted list of core patterns, principles, and language features to take away.

## Saving an Explanation (on explicit request only)

Only persist when the user explicitly requests it.

### Setup

1. Check if `.decodie/` exists at the project root. If not, create it:
   - `.decodie/index.json` with `{ "version": "1.0", "project": "<directory-name>", "entries": [] }`
   - `.decodie/config.json` with default preferences
   - `.decodie/sessions/` directory

2. Determine session ID. Find the highest `NNN` for today in `.decodie/sessions/` matching `explain-YYYY-MM-DD-NNN`, then increment.

### Session entry fields

Write to the session file with:
- **`code_snippet`**: The selected code as provided.
- **`explanation`**: The Summary section.
- **`alternatives_considered`**: Alternative approaches if relevant; empty string otherwise.
- **`key_concepts`**: Array of core concepts.
- **`breakdowns`**: Array of `{ code_excerpt, explanation, pattern? }`.
- **`issues`**: Array of `{ severity, description, suggestion }`.
- **`improvements`**: Array of `{ description, rationale }`.

### Index entry

- **`id`**: Format: `entry-{unix-timestamp}-{random-4-hex-chars}`
- **`decision_type`**: `"explanation"`
- **`content_file`**: relative path to session file, e.g. `sessions/explain-2026-03-27-001.json`

If the code came from an identifiable file, include a reference with content-based anchoring:
- **`file`** — relative path from project root
- **`anchor`** — function signature, class declaration, or distinctive code block
- **`anchor_hash`** — first 8 hex chars of SHA-256 of the anchor text (`echo -n "<anchor_text>" | shasum -a 256 | cut -c1-8`)

If pasted without a known origin, `references` may be empty.

### Session Closure

Set `timestamp_end`, write a brief `summary`, and confirm: "Saved explanation as entry `<id>` in session `<session_id>`."

## Data Format

See [references/schema.md](references/schema.md) for the full `.decodie/` data format.

## Important Notes

- **Ephemeral unless asked.** Only write to `.decodie/` when the user explicitly requests persistence.
- **Calibrate depth to the code.** A five-line utility does not need five breakdowns.
- **Be honest about uncertainty.** If code is ambiguous, say so.
