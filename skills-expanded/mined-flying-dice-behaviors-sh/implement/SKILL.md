---
name: implement
description: >-
  Pick up an open TODO item from the backlog, implement the change, and mark it
  done. Invoke with /implement or /implement <search term> to fuzzy-match an item.
---

## Workflow

1. **Read the backlog** — open `.claude/skills/todo-tracker/TODO.md` and list only the unchecked (`- [ ]`) items, numbered for easy selection.
2. **Let the user choose** — present the open items and ask which one to pick up. If the user passed an argument (e.g. `/implement import tree`), fuzzy-match it against the open items and confirm the match before proceeding.
3. **Mark WIP** — change the chosen item's checkbox from `- [ ]` to `- [~]` in TODO.md so it's visibly in-progress.
4. **Implement** — carry out the work described in the item, following the project skills:
   - Code changes must follow `.claude/skills/clean-code/SKILL.md`.
   - UI/UX changes must follow `.claude/skills/frontend-design/SKILL.md`.
   - All changes must respect `.claude/skills/todo-tracker/SKILL.md` rules for completion criteria.
5. **Verify** — for UI/UX items, ask the user to confirm in the browser (or use Playwright if asked). For non-UI items, run the relevant checks (type-check, lint, tests).
6. **Mark done** — once confirmed, change the checkbox from `- [~]` to `- [x]` in TODO.md.

## Rules

- Only pick up one item at a time.
- Never skip the WIP marker — it signals work is underway.
- If implementation reveals the item is larger than expected or ambiguous, stop and discuss before continuing.
- Do not mark UI/UX items as done without user confirmation or Playwright evidence.
