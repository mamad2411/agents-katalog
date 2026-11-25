---
name: project-indexing
description: Use when locating files or understanding structure. Consults PROJECT-TOC.md (one-line index per file). Staleness via git commit anchor.
---

# Project Indexing

`PROJECT-TOC.md` is the project's **machine-friendly index** — one line per file, ≤80 chars summary. Reading it is dramatically cheaper than `Glob`-ing the whole tree.

## When to use

- "Where is X defined?"
- "Find the file that handles Y"
- Before any `Glob '**/*.ext'` against more than a small directory
- When starting work in an unfamiliar codebase

## Reading flow

1. **Check `PROJECT-TOC.md` exists.** If missing, the project is un-indexed. Suggest `/index-project` and fall back to Glob for the current question.

2. **Check freshness.** The TOC header contains:

   ```
   <!-- generated-at-commit: <SHA> -->
   ```

   Stale if either (both counts exclude `PROJECT-TOC.md` itself, so committing a
   regenerated TOC does not re-stale it):
   - `git diff --name-only <SHA> HEAD` returns files
   - `git status --porcelain` shows working-tree changes (untracked files count — the TOC doesn't cover them)

   Note: the SessionStart hook already computes `toc_stale: true/false` and injects it. If stale, prefer `/index-project` before deep navigation; for one-off questions, fall back to Glob.

3. **Forest before trees.** Read the **`## Directory map`** first (one line per directory, with file + subdir counts) to find the right subtree, then grep/scan the **`## Files`** entries under that path. On a large repo the SessionStart hook injects only the directory map (or just its top levels), so the per-file leaves are read on demand.

4. **Open the file.** Only after locating via TOC.

## When NOT to rely on TOC

- TOC was just regenerated but agent hasn't seen it (mtime ≠ session start)
- File you're looking for is *new* (not yet in git)
- Question requires content search, not name search (use Grep then)

## Rebuilding

When you make significant structural changes (new directories, renames, large refactors):

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/index-builder.mjs --target .
```

Or simply tell the user to run `/index-project`. Don't try to maintain the TOC by hand-editing — it's auto-generated.

## TOC format expectations

```markdown
<!-- generated-at-commit: abc123 -->
<!-- DO NOT EDIT BY HAND — run /index-project or scripts/index-builder.mjs -->

# PROJECT TOC

## Directory map
- `.` (root) — 2 files, 3 subdirs
- `src/` — 1 file, 1 subdir
- `src/util/` — 4 files

## Files
- `src/main.cpp` — entry point, parses CLI args, initializes Engine
- `src/util/log.h` — fmt-based logger
- ...

## Decisions
- 2026-05-15: switched from X to Y (see docs/decisions/0001.md)
```

The `## Decisions` section is human-edited (long-lived architectural notes). The `## Files` section is mechanical.

## Token economy

`PROJECT-TOC.md` typically fits within a few thousand tokens even for medium projects. The SessionStart hook **adaptively** injects the `## Directory map` (or, for a small repo, the full `## Files`) within the Tier 1 budget — and on a very large repo, only the top-level directories; the rest is read on demand. Don't ask the user to load the full TOC unless the budget allows.

**Hard read rule:** if `PROJECT-TOC.md` exceeds ~400 lines, do not read it whole — read the
`## Directory map`, then **Grep** the `## Files` section for the subtree you need. A
full-file Read of a large TOC can spend tens of thousands of tokens on one lookup.

## Looking up indexing techniques

For deeper context-engineering / progressive-disclosure indexing approaches not covered here — invoke the `docs-lookup` skill. The current TOC algorithm is intentionally minimal; refinements (semantic chunks, embeddings) belong in a separate skill.

Typical entry query: `progressive disclosure llm agent` or `agent harness indexing 2026`.

## Related

- `using-harness-anchor` — overall navigation, points here when files are sought
- `feature-state-keeper` — manages state files alongside the TOC
