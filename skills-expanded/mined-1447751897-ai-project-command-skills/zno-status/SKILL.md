---
name: zno-status
description: Use when the user writes /zno-status, wants to save current progress before switching or ending a session, or asks for a progress snapshot. Inspects the workspace and writes a factual, handoff-ready snapshot to docs/development/10-current-status.md. Does not implement new work.
---

# Zno-Status — Progress Snapshot

`<skills-root>` below means the directory containing all zno-* skills (e.g. `~/.claude/skills` or `~/.agents/skills`).

## Workflow

1. Inspect the current state: relevant docs, and `git status` / recently changed files when available.
2. If `docs/development/10-current-status.md` does not exist yet, scaffold it first:

   ```bash
   python <skills-root>/zno-init/scripts/init_project_docs.py <project-root> --scaffold status
   ```

3. Record in the status doc: current phase, current task, completed work, in-progress work, pending next steps, blockers, recent file changes, what verification ran, what verification did NOT run, and continuation advice.
4. Keep the snapshot strictly factual. Never claim tests ran unless they actually ran.
5. Do not implement new work unless the user explicitly asks.
6. Final response: confirm the snapshot was updated and state the recommended next step (usually `/zno-continue` in the next session).

## Shared references (read only when needed)

- `<skills-root>/zno-init/references/docs-map.md` — full doc set, doc update rules, scaffold triggers.
