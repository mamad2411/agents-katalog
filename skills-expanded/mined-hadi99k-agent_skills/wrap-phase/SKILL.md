---
name: wrap-phase
description: Wraps up a development phase by cleaning AGENT_SYNC.md, summarizing work, and committing changes.
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: agent-sync
---

## What I do

- Read `AGENT_SYNC.md` to understand the completed work.
- Add a Phase Summary highlighting everything built and key technical fixes.
- Clean the Handoff Log by deleting all older conversations and keeping ONLY the single most recent log.
- Clear completed tasks from the Session Task Board.
- Update the Current Phase status to reflect completion.
- Stage, commit, and push the `AGENT_SYNC.md` file automatically.

## When to use me

Use this when the user asks to "wrap up the phase", "wrap the phase", or "clean up AGENT_SYNC".

## Execution Steps

When invoked, execute the following steps without needing further confirmation:
1. **Analyze:** Read `AGENT_SYNC.md` to grasp all recent sub-tasks and the handoff logs.
2. **Summarize:** Create a clear `## 📖 Phase Summary: [Feature Name]` section under the task board summarizing the accomplishments.
3. **Clean:** Remove all `[x]` completed items from `## 📋 Session Task Board`. Replace them with a note like "*All completed.*"
4. **Purge:** Delete all older handoff messages under `## 💬 Handoff & Discussion Log` EXCEPT for the single most recent one.
5. **Update State:** Change the "Current Phase" in the state section to indicate completion (e.g., "[Phase Name] Complete ✅").
6. **Save & Commit:** Write the updated file to disk, then use `bash` to run:
   `git add AGENT_SYNC.md && git commit -m "docs: wrap phase - clean agent sync and add phase summary" && git push`