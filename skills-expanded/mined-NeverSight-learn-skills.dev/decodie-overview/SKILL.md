---
name: decodie-overview
description: >-
  Generate a high-level overview of a file, directory, or project — answering
  "what is this and how is it organized." Produces a single summary entry
  covering purpose, structure, entry points, and dependencies. Re-running on
  the same target overwrites the existing overview.
license: MIT
metadata:
  author: owenbush
  version: "1.0"
---

# Decodie — Overview Mode

Generate a high-level overview of a file, directory, or project — answering "what is this and how is it organized" rather than line-by-line explanations. Produces a single summary entry per target, intended as an onboarding starting point.

This mode **persists by default** — overviews are saved as learning entries. Re-running on the same target overwrites the existing overview rather than accumulating versions.

This mode is read-only with respect to source code. You only read source files and write to the `.decodie/` directory.

## Activation and Argument Parsing

1. **Extract the target path.** If none provided, use the project root.
2. **Validate the target.** Confirm it exists and is a file or directory.
3. **Determine target scope:**
   - **File** — `entry_points` and `dependencies` may be omitted.
   - **Directory** — `entry_points` and `dependencies` are usually meaningful.
   - **Project root** — all four overview fields apply.
4. **Canonicalize the target path** for regeneration lookup:
   - File: relative path (e.g., `src/utils/helpers.ts`)
   - Directory or project root: relative path with trailing slash (e.g., `src/auth/`, `./`)

## Setup

1. Check if `.decodie/` exists at the project root. If not, create it:
   - `.decodie/index.json` with `{ "version": "1.0", "project": "<directory-name>", "entries": [] }`
   - `.decodie/config.json` with default preferences
   - `.decodie/sessions/` directory

2. Load the index summary. Run:
   ```bash
   bash scripts/summarize-index.sh "$(pwd)"
   ```
   If unavailable, read `.decodie/index.json` directly.

3. Determine session ID. Find the highest `NNN` for today in `.decodie/sessions/` matching `overview-YYYY-MM-DD-NNN`, then increment.

## Regeneration vs Fresh Entry

Before generating, check for an existing overview:

1. Read `.decodie/index.json`.
2. Find any entry where `decision_type === "overview"` and `sources` is `[<canonicalized-target-path>]`.
3. If found (**regeneration**): reuse the existing `id`, generate fresh content, update the index entry in place. The previous session file is left on disk but no longer referenced.
4. If not found: generate a new entry with a fresh ID.

## Generation Process

1. **Read the target:**
   - File: read in full.
   - Directory: list top-level entries, read structural files (`package.json`, `composer.json`, `pyproject.toml`, `README.md`, etc.), sample representative source files.
   - Project root: additionally inspect entry-point manifests and dependency manifests.

2. **Identify four overview dimensions:**

   - **`purpose`** (required) — 2-4 sentences describing what this code is for. Lead with intent, not implementation.
   - **`structure`** (required) — how the code is organized (sections, modules, key directories and their roles).
   - **`entry_points`** (optional) — callable surfaces: exported functions, CLI commands, HTTP routes, framework hooks. Omit if not meaningful.
   - **`dependencies`** (optional) — notable internal or external dependencies and what they provide. Omit trivia.

3. **Write in plain prose.** Avoid jargon-heavy bullet lists; the goal is human onboarding. Calibrate length to scope.

## Entry Generation

### Index entry metadata

- **`id`**: Reuse existing for regeneration; generate fresh otherwise. Format: `entry-{unix-timestamp}-{random-4-hex-chars}`
- **`title`**: e.g., "Overview: `src/auth/` — token issuance and verification"
- **`experience_level`**: `"foundational"` (overviews are onboarding entry points).
- **`decision_type`**: `"overview"`
- **`topics`**: Lowercase kebab-case tags. Reuse existing tags.
- **`lifecycle`**: `"active"`
- **`sources`**: Array with exactly one entry — the canonicalized target path.
- **`references`**: For single-file overviews, one reference to the file. For directory/project, empty array.
- **`content_file`**: relative path to session file, e.g. `sessions/overview-2026-03-27-001.json`

### Session entry content (overview shape)

Use the overview shape — different from standard entries:
- **`decision_type`**: `"overview"`
- **`purpose`** (required) — what the target code is for
- **`structure`** (required) — how the target is organized
- **`entry_points`** (optional) — callable surfaces
- **`dependencies`** (optional) — notable dependencies

## Session Closure

1. Set `timestamp_end`.
2. Write a `summary` noting the target and whether this was fresh or regenerated.
3. Confirm:
   - Fresh: "Generated overview for `<target>` as entry `<id>` in session `<session_id>`."
   - Regeneration: "Regenerated overview for `<target>` (entry `<id>`)."

## Data Format

See [references/schema.md](references/schema.md) for the full `.decodie/` data format.

## Important Notes

- **Always-latest, not append-only.** Re-running overwrites the index entry.
- **One entry per target.** Do not fan out to per-file entries — that is analyze mode's job.
- **Be honest about uncertainty.** If the target's purpose is ambiguous, say so.
- **Language-agnostic.** Adapt to whatever language and framework the project uses.
- **Self-contained data.** The `.decodie/` directory can be removed without affecting the project.
