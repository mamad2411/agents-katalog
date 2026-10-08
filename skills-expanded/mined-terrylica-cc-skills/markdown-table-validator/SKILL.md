---
name: markdown-table-validator
description: Detect and fix Markdown (GFM) tables that won't render on GitHub or the VS Code preview — unescaped pipes inside cells, header/separator column-count mismatch, indented (code-block) tables, and misplaced alignment colons. Use when a markdown table renders as raw text, when cleaning LLM-generated docs in bulk, or when auditing a repo's tables before a commit. TRIGGERS - markdown table broken, table not rendering, fix markdown table, escape pipe in table, GFM table, table renders as text, validate markdown tables.
allowed-tools: Bash, Read, Edit
---

# Markdown Table Validator

Scan Markdown files for the structural problems that silently demote a GFM table
to a plain paragraph on GitHub / VS Code preview, and optionally auto-escape the
single most common cause (an unescaped `|` inside a cell).

> **Self-Evolving Skill**: This skill improves through use. If the detector
> misses a real broken-table case, the `--fix` heuristic guesses wrong, or a
> path/flag has drifted — fix this file (and the detector SSoT) immediately,
> don't defer. Only update for real, reproducible issues.

## Why tables break (the one rule that matters)

GFM ignores whitespace between pipes, so **alignment is never the cause**. What
breaks rendering is **structure** — overwhelmingly an **unescaped `|` inside a
cell**. GFM's table tokenizer treats a `|` as a column delimiter _even inside a
`` `code span` ``_, so a regex/code cell like `` `a | b | c` `` inflates that
row's cell count and the whole table collapses. The fix — escaping it as `\|` —
changes meaning, so **no formatter does it for you** (Prettier actively corrupts
such tables: prettier#10164 / #11410). This skill detects it and can apply the
escape under review.

## Quick start

```bash
SCAN="$(cc-plugin-root doc-tools)/skills/markdown-table-validator/scripts/scan_markdown_tables.ts"

# Report problems in one file (exit 1 if any render-breaking error)
bun "$SCAN" path/to/FILE.md

# Audit a whole tree
bun "$SCAN" "docs/**/*.md" "plugins/**/*.md"

# Opt-in auto-fix: escape over-count pipes, then re-align with prettier
bun "$SCAN" --fix path/to/FILE.md
prettier --write path/to/FILE.md
```

## What it detects

| Code                     | Severity | Meaning                                                                  |
| ------------------------ | -------- | ------------------------------------------------------------------------ |
| `column-overflow`        | error    | A row has more cells than the header → unescaped `\|` in a cell.         |
| `header-mismatch`        | error    | Header and separator row have different column counts → won't render.    |
| `indented-table`         | error    | Table indented ≥4 spaces → parsed as a code block.                       |
| `alignment-colon-in-row` | error    | An alignment token like `:--:` sits in a data row (misplaced separator). |
| `short-row`              | info     | Row has too few cells; GFM pads and `markdownlint --fix` repairs.        |
| `missing-blank-line`     | info     | No blank line before/after the table; the formatter auto-fixes.          |

Fenced code blocks (` ` ```) are skipped, so example broken tables shown
inside docs don't trip the scan.

## Output

Compiler-style `path:line: severity: message [code]`. Exit `0` when no **error**
remains (info nits never fail the run), `1` otherwise — usable as a gate.

## `--fix` heuristic (always review the diff)

For a row with more cells than the header, the genuine columns are assumed to be
the **first N**; every pipe beyond column N is treated as literal content and
escaped as `\|`. This exactly fixes the common case (regex/code in the last
cell) but can guess wrong when a pipe was a _genuinely missing_ delimiter — so
review the diff, then run `prettier --write` to re-align.

## Relationship to the automatic guard

This skill is the **manual, repo-wide** counterpart to the per-edit
`itp-hooks` PostToolUse guard (`posttooluse-markdown-table-guard.ts`), which
reminds Claude to fix the same errors the moment a `.md` file is written. Use
the skill to clean **existing** docs in bulk; the hook prevents **new**
breakage. Both share the same detection algorithm (SSoT:
`plugins/itp-hooks/hooks/lib/markdown-table-detector.ts`).

Suppress the per-edit hook on a file by adding a comment containing `MD-TABLE-OK`.

## References

- [algorithm.md](./references/algorithm.md) — the detection algorithm + the pipe-escaping rationale.

## Post-Execution Reflection

After this skill completes, reflect before closing the task:

0. **Locate yourself.** — Find this SKILL.md's canonical path before editing.
1. **What failed?** — A missed broken table or a false positive → fix the detector (`markdown-table-detector.ts`) and its mirror here.
2. **What worked better than expected?** — Promote to recommended practice.
3. **What drifted?** — Keep the self-contained scanner copy in parity with the itp-hooks detector SSoT.
4. **Log it.** — Note the trigger, fix, and evidence.

Do NOT defer. The next invocation inherits whatever you leave behind.
