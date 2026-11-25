---
name: moth-debug-first-fix
description: Analyze an error before editing code. Use when an agent is about to fix a failing test, build, typecheck, lint, runtime error, stack trace, or MCP-provided error log.
---

# Moth Debug First Fix

## Workflow

1. Capture the failing command, error output, package context, and the smallest relevant file excerpts.
2. Redact secrets before storing, quoting, or sending the error anywhere.
3. Call `analyze_error` when available.
4. Treat `likely_cause`, `best_first_fix`, `avoid`, and `confidence` as a fix brief, not certainty.
5. If context is missing, gather only the narrow missing context.
6. Apply the smallest fix that explains the key error line.
7. Run the verification command.
8. Call `remember_fix_result` only after a fix was attempted and verification clearly passed or failed.

## Guardrails

- Do not start with a broad refactor.
- Do not scan the whole repository unless the user explicitly asks.
- Do not treat Moth confidence as proof.
- Do not call `remember_fix_result` for suggestions, unapplied changes, skipped changes, missing verification, ambiguous results, or guesses.
- Do not record full sensitive logs in memory.