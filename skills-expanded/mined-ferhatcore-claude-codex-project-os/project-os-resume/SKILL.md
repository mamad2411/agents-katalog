---
name: project-os-resume
description: Resume a Project OS task after a session restart or compact using its saved handoff and current evidence.
---

# project-os-resume

Read AGENTS.md, .project-os.json, planning/board.md, planning/pending-user.md and the assigned task's single Hand-off.
Reconcile actual worker state, unfinished commands, dirty files and any changed criteria before continuing.
Do not restart a running job or replay a completed step. Do not clear a busy worker.
Check current approvals, dependencies, lane ownership, and model choice. Unknown usage does not block work. Unknown worker state is not idle or approved.
Read only the topic rules needed by the next step. Give a new worker a self-contained brief and resume from the recorded point.
Keep one shared planning history across Claude Code and Codex; record the active client in the dated task notes.
