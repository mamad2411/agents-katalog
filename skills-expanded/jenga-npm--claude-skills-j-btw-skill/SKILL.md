---
name: j.btw
description: Polyfill alias of the btw skill under a collision-safe directory name. Identical behavior to /btw — Capture a new mission (feature, change, or addition) and fit it into the project's Epic/Story structure, then choose to implement now or defer. Use when the bare /btw form is shadowed by another tool's own built-in command of the same name.
keywords:
  - btw
  - capture
  - mission
  - new idea
  - side task
  - j-btw
  - polyfill
examples:
  - "btw I also need to add X"
  - "capture this as a new task"
  - "j-btw"
metadata: 
  prefered_agent: scrum-master
---

# BTW — Capture a Mission

This skill is a literal-directory-name duplicate of `skills/btw/`. It exists so that `/j-btw` (and `j.j-btw`) give a guaranteed-unshadowed way to reach the same flow as `/btw`, even if a host tool's own built-in command of the same name would otherwise shadow or override the bare `/btw` alias (Claude Code's native skill resolution is a literal-string, directory-name-based match — see `docs/skill-authoring.md`'s "Invocation Convention").

This file is generated/synced by `scripts/generate-j-alias.sh btw` from `skills/btw/SKILL.md` — do not hand-edit it; re-run the generator instead to pick up source changes.

## Instructions

1. **Gather mission details** — Ask the user:
   - Where do you want to do this?
   - What would you like to do?
   - What is the goal?

2. **Classify the mission** — Based on the description, determine if it fits into:
   - An existing story
   - A new story inside an existing Epic
   - A new story inside a new Epic

3. **Update project documentation** — Add the mission to the appropriate board files:
   - **New story**: create a file in `project/board/stories/` using `../pi-plan/assets/story_template.md` as the structure.
   - **New epic**: append a new Epic object to `project/PROJECT_SUMMARY.md` using the schema in `../pi-plan/assets/epic.json`.
   - **Existing story**: append the new task or acceptance criterion to the matching file in `project/board/stories/`.

4. **Ask the user: "now" or "later"?**
   - If **"now"** — Produce a plan for the first story related to the mission and begin implementation.
   - If **"later"** — Confirm the mission has been recorded and resume the previous workflow.

## Examples
- `/btw` — Start the interactive mission capture flow
- `/btw add a dark mode toggle to the settings page` — Pre-fill the "what" and jump into classification
