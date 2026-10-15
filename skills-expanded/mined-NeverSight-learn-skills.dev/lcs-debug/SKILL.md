---
name: lcs-debug
description: Use this skill whenever the user needs a focused bug investigation. Trigger on phrases about bugs, failing tests, errors, regressions, or unexpected behavior. Ask questions one at a time to identify the bug, and write the investigation results and fix plan in .lcs/work-items/<timestamp>-<slug-work-item>/debug.md before planning any fixes.
adapters: [claudecode, opencode]
compatibility: [claudecode, opencode]
---

# LCS Debug Skill

Shared Coding Contract
- Refer to Shared Coding Workflow Contract in `../lcs-shared/contract.md` for folder conventions, Handoff format, and token optimization.

Purpose
- Investigate bug by asking questions to the user.
- DO NOT plan or implement any fix before the bug is fully understood.
- Save investigation notes and proposed fix plan under `.lcs/work-items/<timestamp>-<slug-work-item>/debug.md` and update `.lcs/state.md`.

Trigger
- Activate on user mentioning bug, failing test, error, regression, or unexpected behavior.

Behavior checklist
- Confirm work item name and read `state.md` if present to identify active work item folder.
- Ask one question at a time: repro steps, expected vs actual behavior, logs, env, recent commits.
- Prioritize minimal reproduction steps and clear bug understanding.
- DO NOT design or suggest fixes until the root cause is clear.
- Once understood, write proposed hypotheses and quick investigation plan to `.lcs/work-items/<timestamp>-<slug-work-item>/debug.md`. 
- Update `.lcs/state.md` with current phase `debug` and path.
- End with Handoff section.

Handoff example:
## Handoff
Next recommended skill: lcs-toprd
Next file to read: .lcs/work-items/<timestamp>-<slug-work-item>/debug.md
Current phase: debug
Current confidence: <low/medium/high>
Blocking questions: <list or None>
Risks to carry forward: <risks>
Suggested next command: Buat PRD dari debug.md
