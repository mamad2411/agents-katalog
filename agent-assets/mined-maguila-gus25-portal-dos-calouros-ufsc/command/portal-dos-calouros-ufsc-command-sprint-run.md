---
description: Executa o sprint atual — despacha subagentes em ordem de dependência conforme docs/SPRINT.md, atualizando o status das histórias conforme o trabalho é concluído.
---

Act as the **Scrum Master** (`.claude/agents/scrum-master.md`), executing the current sprint.

1. Read `docs/SPRINT.md`. If there's no active sprint (empty/no stories, or all already Done), tell the user to run `/sprint-plan` first and stop.

2. For each story, in the order listed (respecting dependencies):
   - Mark the story "In Progress" in `docs/SPRINT.md`.
   - Dispatch the assigned subagent(s) via the `Task` tool with a focused, self-contained prompt including: the story text, acceptance criteria, relevant file paths, and current stack context (React 18 + Vite + TypeScript + Tailwind / FastAPI + Python + Pydantic v2; content source is `docs/*.md`). The subagent has no memory of this conversation.
   - If two stories are independent (e.g. one frontend, one backend on different files; or content-editor on `docs/` while backend-dev works on `backend/`), dispatch them **in parallel** in a single message.
   - After implementation, dispatch `tester` to verify (at minimum `npm run lint` + `npm run build` for frontend; `pytest` or healthcheck for backend).
   - If `tester` reports failures, dispatch `debugger` once to fix, then re-run `tester`. If still failing, mark the story "Blocked" with a short explanation and move on — don't loop indefinitely.
   - Mark the story "Done" (or "Blocked") in `docs/SPRINT.md`.

3. After all stories are processed, if any structural changes were made (new deps, new top-level files/folders, new/changed agents/skills/commands), run the `update-readme` skill.

4. Summarize what was completed/blocked for the user, and suggest running `/sprint-review`.
