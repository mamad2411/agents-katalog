---
description: "Sets up and maintains an agentkan roadmap board (JSON epics and tasks plus markdown bodies) in a project. Use when the user wants to organize scattered tasks, migrate from roadmap.md or todo lists, scaffold a board, add or refine epics, update next.json, run a session handoff, or plan work with an AI-shared board. Triggers: set up agentkan, migrate my roadmap, organize my tasks, add an epic, new epic, fill epic, what's next, handoff, update the board, or edits to roadmap.json or next.json."
metadata:
  github-path: skills/agentkan
  github-ref: refs/heads/main
  github-repo: https://github.com/hasankhatib/agentkan
  github-tree-sha: d570af1763398e3d90a2e9bf26be32ff0d955b00
name: agentkan
---

# agentkan

Local roadmap board for AI-assisted projects. **State** in `roadmap.json`, **focus** in `next.json`, **prose** in `epics/<ID>.md`. Default board directory: `docs/board/` (use the path in the project's AGENTS.md if different).

## Workflow

Copy this checklist and track progress:

```
- [ ] Step 0: Route to the right path
- [ ] Step 1: Execute that path
- [ ] Step 2: Run npx agentkan validate <board-dir>
- [ ] Step 3: Tell the user what changed and what to do on the board
```

**Step 0: Route**

| Situation                                              | Read                                                                 |
| ------------------------------------------------------ | -------------------------------------------------------------------- |
| No board yet / "set up agentkan"                       | [references/onboarding.md](references/onboarding.md)                 |
| Scattered tasks, old roadmap.md, issues, notes         | [references/migration.md](references/migration.md)                   |
| Project not wired for agentkan (AGENTS.md / CLAUDE.md) | [references/agents-integration.md](references/agents-integration.md) |
| End of session / "handoff"                             | [references/handoff.md](references/handoff.md)                       |
| JSON field shapes or IDs                               | [references/data-model.md](references/data-model.md)                 |
| Add or refine an epic (below)                          | Epic flow in this file                                               |

**Step 1: Epic flow** (add, fill, or refine work)

1. If no stub exists: `npx agentkan epic new "<title>" [--phase Pn] [--release v1] [--assignee ai|me|ai+verify] [--labels a,b]`
2. Interview only what you cannot infer (one batch): goal, exit, steps, assignee, planned date
3. Write both `roadmap.json` and `epics/<ID>.md` (one-line goal/exit in JSON; detail in markdown)
4. Validate; show the user the new card; ask if goal/exit are right

If the user brain-dumps instead of answering, extract fields yourself and confirm.

**Commands**

```
npx agentkan init [dir]                 scaffold a board
npx agentkan epic new "<title>" [opts]  add epic stub + body
npx agentkan serve [dir]                open board on localhost (human operates)
npx agentkan validate [dir]             schema gate - run after every edit
```

Optional: `bash scripts/validate-board.sh <board-dir>` or `bash scripts/status.sh <board-dir>` before handoff.

## Boundaries

- **AI proposes, human disposes:** never mark an epic `done`, archive, delete, or reorder wholesale unless the user explicitly asks in this turn. Closing and archiving are human actions in the viewer.
- Never regex-patch JSON. Read the whole file, mutate the object, write 2-space indent and a trailing newline.
- IDs are stable forever. Epic IDs: `E<phase>.<n>`. Task IDs: `<EPIC>-T<n>`. The viewer sorts epics by id; change priority via status columns or `next.json`, not by renumbering ids.
- `goal` and `exit` are one line each in JSON. Longer context belongs in the epic body.
- Labels are free-form. Add emoji vocabulary in `board.tokens.json` when a label is here to stay.
- After any board edit, validate before handing back.
- Do not replace the consumer's AGENTS.md wholesale. Merge [assets/AGENTS.snippet.md](assets/AGENTS.snippet.md) and customize placeholders.
