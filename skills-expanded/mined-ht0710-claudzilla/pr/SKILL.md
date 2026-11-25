---
name: pr
description: Use before opening or editing a pull request (gh pr create / gh pr edit) - pre-PR checks and the PR description template.
---

# PR

## Before opening a PR

- New file → read one sibling of the same kind first; match its imports, test style, docstrings.
- A pattern, marker or convention you add → `git grep` it on main. Zero hits → don't ship it (`comments.md` markers exempt).
- A "repo convention" claim → name the file that shows it, or don't make it.
- Run every command the PR or docstrings document, exactly as written. Red for an unrelated
  reason → fix the command or file it; never just footnote it.
- Existing data or config needing action after deploy → `**Action required:**` section.
- `**Not covered:**` also lists side effects of the fix (idempotency, boundaries, ordering).
- User-visible change (behaviour, command, key, setting) → update the matching GUIDE.md section.

## PR description

Same sections as the commit body (`Test plan:` replaces `Verify:`), plus `Changes:`, a `Test plan:` checklist, and when they apply `Action required:` / `Not covered:`. Nothing more.
`Changes:` = bullet per logical change, one line. `path` only if not obvious. Never per file.
`fix:` PR → `Why:` may run 2–3 lines: symptom, then cause; the fix goes in `Changes:`. `Test plan:` shows each case before and after (`main` vs branch), as a table when 2+ cases.
Title = commit subject shape (`<type>(<scope>)?: <subject>`, scope optional).

Markdown renders in PRs → **bold every section label** (`**Why:**`, `**Changes:**`,
`**Impact:**`, `**Test plan:**`, and any extra label like `**Action required:**`, `**Not covered:**`).
Commit messages stay plain text — `**` shows literally in `git log`.

```markdown
**Why:** <1–2 sentences — trigger or root cause>

**Changes:**
- <logical change, 1 line> (`path` only if not obvious)

**Impact:**
- <who/what is affected>

**Action required:** <post-deploy step: re-embed, migration, config. Omit if none>

**Not covered:** <out of scope, side effects. Omit if none>

**Test plan:**
- [x] <command run / check done> → <result>
- [ ] <check still open>
```
