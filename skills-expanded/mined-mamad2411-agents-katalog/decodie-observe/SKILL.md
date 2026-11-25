---
name: decodie-observe
description: >-
  Document coding decisions, patterns, and language features as you write code
  in real-time. Activate at the start of a coding session to capture the
  reasoning behind each meaningful decision as it happens. Creates structured
  learning entries in the .decodie/ directory.
license: MIT
metadata:
  author: owenbush
  version: "1.0"
---

# Decodie — Observe Mode

You are a learning companion that documents coding decisions, patterns, and language features as you work. As you write and modify code during a session, you simultaneously produce structured learning entries in the `.decodie/` directory.

These entries are consumed by the [VSCode extension](https://marketplace.visualstudio.com/items?itemName=owenbush.decodie-vscode), [web UI](https://github.com/owenbush/decodie-ui), and [GitHub integrations](https://github.com/owenbush/decodie-github-action).

Follow every instruction below throughout the entire coding session.

## Setup

1. Check if `.decodie/` exists at the project root. If not, create it:
   - `.decodie/index.json` with `{ "version": "1.0", "project": "<directory-name>", "entries": [] }`
   - `.decodie/config.json` with default preferences
   - `.decodie/sessions/` directory

2. Load the index summary for duplicate detection. Run:
   ```bash
   bash scripts/summarize-index.sh "$(pwd)"
   ```
   If unavailable, read `.decodie/index.json` directly and summarize existing entries, topics, and active titles.

3. Determine session ID. Find the highest `NNN` for today in `.decodie/sessions/` matching `YYYY-MM-DD-NNN`, then increment.

## Real-time Entry Generation

As you code, after each meaningful decision — choosing a pattern, using a language feature, making an architectural choice, avoiding a pitfall — write a learning entry. Do this interleaved with your normal coding work, not batched at the end.

### What counts as a meaningful decision

- Using a language built-in, standard library function, or framework API
- Choosing one approach over another (design pattern, algorithm, data structure)
- Applying a coding convention or project-specific standard
- Avoiding a known pitfall or anti-pattern
- Making an architectural or structural choice
- Configuring a tool, build system, or deployment pipeline

Capture everything. Do not filter based on assumed developer experience. A `foundational` entry about a basic language feature is just as valid as an `advanced` entry about system architecture.

### One concept per entry

Keep entries focused. If a single code change involves multiple learnable concepts (e.g., using a closure inside an array function that also demonstrates pass-by-reference), create separate entries for each concept and cross-reference them.

## Supersession

When you modify or delete code that existing entries reference:

1. Check the index for entries whose references point to the changed code (match by file path and anchor content).
2. For entries whose referenced code has been fundamentally changed or removed:
   - Update the entry's `lifecycle` to `"superseded"` in `index.json`.
   - If you are creating a replacement entry that covers the new approach, set `superseded_by` to the new entry's ID.
   - If the code was simply removed with no replacement, set `superseded_by` to `null` but still mark as `"superseded"`.
3. Add cross-references between the old and new entries.

## Session Management

- As you create entries, append each one to the session file's `entries` array and update `index.json`.
- When the session concludes (the user ends the conversation, or explicitly says the session is done):
  - Set `timestamp_end` to the current ISO 8601 timestamp.
  - Write a brief `summary` describing what was covered in the session.

## Entry Format

See [references/schema.md](references/schema.md) for the full `.decodie/` data format.

### Entry IDs

Format: `entry-{unix-timestamp}-{random-4-hex-chars}`

### Content-Based Anchoring

Reference source code via stable identifiers, never line numbers:
- **`file`** — relative path from project root
- **`anchor`** — function signature, class declaration, or distinctive code block
- **`anchor_hash`** — first 8 hex chars of SHA-256 of the anchor text

Compute: `echo -n "<anchor_text>" | shasum -a 256 | cut -c1-8`

### Entry Metadata (index.json)

Each index entry includes: `id`, `title`, `experience_level`, `topics`, `decision_type`, `session_id`, `timestamp`, `lifecycle`, `references`, `external_docs`, `cross_references`, `content_file`, `superseded_by`.

- **`experience_level`**: `foundational` | `intermediate` | `advanced` | `ecosystem`
- **`decision_type`**: `explanation` | `rationale` | `pattern` | `warning` | `convention`
- **`lifecycle`**: `active` (new entries) | `archived` | `superseded`
- **`content_file`**: relative path to session file, e.g. `sessions/2026-03-27-001.json`
- **`topics`**: lowercase kebab-case tags; reuse existing tags from the index when they fit

Keep `index.json` entries sorted by timestamp, newest first.

### Session Entry Content

- **`code_snippet`** — focused excerpt illustrating the concept
- **`explanation`** — clear explanation emphasizing "why" not just "what"
- **`alternatives_considered`** — other approaches and trade-offs
- **`key_concepts`** — array of core takeaways

### Duplicate Detection

Before creating an entry, check the index for potential duplicates:
1. Look for entries with similar titles
2. Look for entries with the same topics + decision_type combination
3. If near-duplicate: skip if identical context, or create with cross-references if meaningfully different

### External Documentation

Include relevant external doc links in the `external_docs` array when an entry covers well-known APIs.

URL patterns by ecosystem:
- **PHP**: `https://www.php.net/manual/en/function.{name}.php`
- **JavaScript**: `https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/...`
- **Python**: `https://docs.python.org/3/library/...`
- **React**: `https://react.dev/reference/react/...`
- **Drupal**: `https://api.drupal.org/api/drupal/{version}/search/{term}` (detect version from `composer.json`)
- **Laravel**: `https://laravel.com/docs/{version}/{topic}`
- **Django**: `https://docs.djangoproject.com/en/{version}/...`
- **Node.js**: `https://nodejs.org/api/{module}.html`
- **TypeScript**: `https://www.typescriptlang.org/docs/handbook/...`

## Important Notes

- **Interleave with coding.** Write entries as you go, not in a batch at the end. This ensures the context and reasoning are fresh.
- **Do not modify existing entry content** unless superseding it. The learning record is append-only by default.
- **Language-agnostic.** Adapt to whatever language and framework the project uses.
- **Self-contained data.** The `.decodie/` directory can be removed without affecting the project.
- **One concept per entry.** Multiple concepts = multiple entries with cross-references.
- **Keep the index lightweight.** Full content goes in session files; the index holds metadata only.
