---
description: Summarize current project state — features, bugs, milestones, next step.
allowed-tools: Read, Grep, Glob, Agent
---

Produce a short status report for the current Atelier project.

1. Invoke **progress-keeper** to load `claude-progress.txt`, `features.json`, `BUGS.md`, `DECISIONS.md`.
2. Summarize in under 200 words:
   - **Now**: what's in progress
   - **Done**: milestones hit
   - **Next**: single clearest next step
   - **Blockers**: open bugs or decisions
   - **Pass rate**: `passing=true` count over total features

Do not do any other work. Pure status read.
