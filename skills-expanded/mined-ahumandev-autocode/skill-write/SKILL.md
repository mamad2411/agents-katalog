---
name: skill-write
description: Use skill-write when writing skill descriptions and content using skill_edit.
---

# description

`description` arg trigger description of: situations, symptoms, task that should make agent recall this skill. 

Format: "Use this skill when [TRIGGER] to [BENEFIT]. NEVER for [EXCLUSIONS]."

- [TRIGGER] = condition that makes skill relevant
- [BENEFIT] = benefit to be expected from skill
- [EXCLUSIONS] = optional guards against irrelevant conditions when [TRIGGER] is broad

Use minimal Caveman English words (max 40).

Examples:
- ✅ Good: `Use this skill when creating Git commit message for recent changes to track changes.` (valid trigger, short, clear benefit)
- ❌ Bad: `This comprehensive skill providing detailed commit messages with conventional commit format and includes analysis of changes.` (missing trigger, too verbose, no benefit)

# content

`content` arg contains content of actual SKILL.md body as follows:
  * Preferably format as structured sequence lists or bullet points.
  * Only include: instructions, rules, links, common info always relevant.
  * No examples, templates, details, explanations in `content`; Instead save these as `references[]` items (description, path, content) in `skill_edit` calls.
  * ALWAYS link ALL references in `content` as md links using exact same `path` used in `references[]`.
  * Format links as md links in text, for example: `[Email Template](templates/email_template.html)` or `[Process Data Script](scripts/process_data.py)`
  * When rules contradict: Add conditions to clarify.
  * Use `author-caveman` skill to write SKILL.md files in Caveman English.
  * No repetitions
  * Only use emojis to highlight important aspects to LLM, like attention, warning, checklists, correct vs wrong
  * ALWAYS keep md < 400 lines by:
    - Cleaning up redundant content
    - Summarize trivial info (instructions/info agent can derive by itself)
