---
name: forge-isolate
description: >-
  Create isolated git worktree and branch after design approval; verify clean
  test baseline. Use after forge-intent is approved.
---
# Forge Isolate

**Activates:** after intent doc approved.

## Steps

1. Confirm design draft exists in `docs-ai/designs/drafts/{slug}.md`
2. Create branch: `forge/{slug}` from updated `main`
3. Optional worktree (parallel work):

```bash
git worktree add ../ratary-{slug} -b forge/{slug}
cd ../ratary-{slug} && npm install
```

4. Run baseline: `npm test` â€” record pass count; **stop if red** on main-equivalent baseline
5. Report: branch path, worktree path (if any), test count

## Rules

- Never implement on `main` directly for multi-step forge work
- If baseline fails unrelated to your task, diagnose first (`forge-diagnose`)

## Cleanup hint

Worktree removal happens in `forge-land`.
