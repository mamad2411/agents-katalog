---
name: skill-improve
description: "Improve a skill using a test-fix-retest loop. Runs static checks, proposes targeted fixes, rewrites the skill, re-tests, and keeps or reverts based on score change."
---

> Port provenance: adapted from the pinned upstream source at `984023ddac0d5e27624f2baacde6105e45de375f` under MIT; see the repository parity ledger for the exact path and blob.

# Improve a Codex skill safely

Improve an existing skill from evidence, not preference. Preserve its public name
and intended trigger unless the user explicitly approves a breaking change.

1. Run `$ai-game-studio:skill-test` and record the baseline failures.
2. Read the official skill authoring constraints available in the current Codex
   installation. Inspect all local references before changing instructions.
3. Diagnose each failure as routing ambiguity, missing workflow detail, unsafe
   mutation, broken reference, unsupported metadata, platform coupling, excessive
   context, or unverifiable output.
4. Propose the smallest patch, showing affected files, behavior change, possible
   regressions, and rollback. Wait for approval before editing.
5. Preserve frontmatter with only `name` and `description`. Keep the starter
   prompt namespaced and realistic. Disable implicit invocation for sensitive
   setup, install, control, refresh, or destructive workflows.
6. After approval, patch with the repository editing mechanism. Do not rewrite
   unrelated prose or generated assets.
7. Re-run static validation and all direct, implicit, near-miss, and negative
   forward tests. Compare results with the baseline.

Return the exact diff summary, validation evidence, remaining limitations, and a
one-command rollback. Never claim improvement solely because wording changed.

## Codex portability

Use the search, file-editing, shell, user-input, and subagent capabilities available in the active Codex surface. Use PowerShell syntax on Windows and POSIX syntax on macOS/Linux; do not require a Unix compatibility layer on Windows. Inherit the active model and permission mode, and do not weaken approval or sandbox boundaries.
