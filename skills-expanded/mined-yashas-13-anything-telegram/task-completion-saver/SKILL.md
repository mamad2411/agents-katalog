---
name: task-completion-saver
description: After EVERY successfully completed user task, capture the workflow as a reusable skill and log it. USE FOR: post-task routine, saving learnings, skill creation after completed tasks.
---

# Task Completion → Skill Saver

Run this routine **every time a user task finishes successfully** (verify first: the outcome must be confirmed, not assumed).

## Steps

1. **Write the skill** at `C:\Users\Dell\.claude\skills\<kebab-name>\SKILL.md`:
   - Front matter: `name`, `description` (with "USE FOR:" triggers).
   - Facts the next run needs: exact URLs, IDs, tokens-as-placeholders, regexes, tool endpoints.
   - The step-by-step flow in the order it was proven to work.
   - Verification signals (what proves success), and gotchas encountered.
2. **Log the completion** — append to `C:\Users\Dell\.claude\skills\task-completion-saver\COMPLETED.md`:
   `| date | task summary | skill saved | evidence |`
3. **Mirror to the repo** if the ecosystem lives there: `anything-telegram/agents/skills/<name>/SKILL.md` + commit/push.

## Rules

- Only save skills for outcomes that were VERIFIED, not assumed.
- Include the failure modes you actually hit (they are the most valuable lines).
- Skills stay factual and actionable — no fluff, no emojis, no marketing.
- If the task already has a skill, UPDATE it instead of duplicating.
