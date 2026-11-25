---
name: finish-feature
description: Validate, document, and record a completed feature or task.
---

# Finish Feature

## Procedure

1. Open `spec/features/[name].md` and collect every acceptance command.
2. Run those commands. Also run relevant type checks, builds, and linters.
3. If a command fails, fix issues caused by the current task and re-run. Do not mark progress.
4. Update relevant documentation only for behavior that just passed.
5. Update `spec/progress.md` to `done` only after every acceptance command passed in this session. Record the commands and exit codes.
6. Record important architectural or implementation decisions.
7. Verify that no temporary code, TODOs, debug output, or unrelated changes remain.

## Rules

- Document only verified behavior.
- Do not claim validation that was not actually run.
- Do not set `progress.md` to `done` from reading code or from a model judgment.
- Prose-only acceptance criteria are invalid; stop and ask for commands.
- Keep documentation synchronized with the implementation.
- Keep `spec/progress.md` concise.
- Do not rewrite unrelated documentation.
- For UI features, verify the running screen with Playwright MCP (https://github.com/microsoft/playwright-mcp) when the spec requires a browser check.
