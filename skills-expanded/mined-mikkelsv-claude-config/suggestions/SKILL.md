---
name: suggestions
description: Review pending suggestions captured by other skills (allow rules, etc.) and accept/skip/discard each one.
---

# Review Suggestions

**Execute mechanically.** Follow the steps; no need to weigh alternatives or deliberate.

Walk through pending suggestion files in `~/.claude/suggestions/` one at a time. For each: show it, ask the user what to do, apply or discard.

Suggestions are dropped here by other skills (e.g. `/allow-defer`) so they don't interrupt flow in the middle of work. This is the batch review.

## Input

`$ARGUMENTS` — optional filter. If provided, treat as a type filter (e.g. `allow` → only show `type: allow` suggestions). Empty = show all.

## Process

### 1. List

List files in `~/.claude/suggestions/` (pattern `*.md`, excluding `README.md` if present).

- **None found** — tell the user "No pending suggestions." and stop.
- **Some found** — continue. Tell the user how many, e.g. "3 pending suggestions. Going through them now."

### 2. Iterate

For **each file**, in the order returned:

1. Read the file.
2. Parse the frontmatter — `type` determines how to apply on accept.
3. Show the user the suggestion's body (or a concise summary — rule + context) in a fenced block.
4. Ask via `AskUserQuestion` with these three options:
   - **Accept** — apply the action, delete the file.
   - **Skip** — leave the file in place, move to the next.
   - **Discard** — delete the file without applying.

   Make **Accept** the first option (recommended). Header: `Decision`.

5. Handle the answer:
   - **Accept** → apply the action for this `type` (see "Applying by type" below), then delete the suggestion file.
   - **Skip** → do nothing, continue.
   - **Discard** → delete the file.
6. Continue to the next file.

### 3. Summary

After the last suggestion, report a one-line summary:

> Reviewed N suggestions: X accepted, Y skipped, Z discarded.

## Applying by type

### `type: allow`

1. Extract the rule from the suggestion body (the fenced block under "Action on accept").
2. Read `~/.claude/settings.json`.
3. If `permissions.allow` already contains the exact rule, tell the user it's already present and treat as accepted (delete the file). No edit needed.
4. Otherwise, use `Edit` to append the rule to the `permissions.allow` array. Match the file's existing indentation style.

### Unknown type

If the frontmatter `type` is missing or unrecognized, show the file to the user and ask whether to Skip or Discard. Do not attempt to auto-apply.

## Notes

- **Don't batch-accept.** Go one at a time so the user can see each rule in context.
- **Don't re-prompt the same session.** If the user chose Skip, don't circle back to that file later in the same `/suggestions` run.
- **File deletion** — use `Bash(rm ...)` or equivalent. The suggestions dir is gitignored, so no commit needed.
- **Errors during apply** — if Edit fails (e.g. settings.json shape changed), stop, tell the user, leave the suggestion file intact.
