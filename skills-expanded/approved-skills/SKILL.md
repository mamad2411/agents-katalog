---
name: approved-skills
description: Find and follow your organisation's approved skill for a task, through the skillsvault tools. Use when the user asks for a task their organisation may have a skill for ("fill this PDF form", "review this pull request", "draft release notes"), asks which skills are approved, or names a skill to load. Works in any client connected to skillsvault, no terminal needed.
---

# Use your organisation's approved skills

skillsvault is the organisation's registry of approved agent skills. Before doing a task
the organisation may have a skill for, check the registry and follow the approved skill
instead of improvising.

## 1. Find the skill

Call `list_skills` with a `query` describing the task in a few words, e.g.
`{"query": "fill pdf forms"}`.

- Results come best first. A result marked `"match": "closest"` didn't match every word:
  check its description fits the task before using it.
- Nothing fits → say no approved skill covers this task, and do the task without one only
  if that is appropriate. Never invent a skill name.

## 2. Load it

Call `load_skill` with the skill's `name` (e.g. `your-org/pdf-forms`).

- **Refused** ("blocked by org policy") → don't work around it. Tell the user the skill is
  blocked, quote the reason, and suggest they request an exception from their
  organisation if they need it.
- **Delivered with a `warning`** (e.g. deprecated) → tell the user before you start.
- The response includes the skill's `url`: cite it when you mention the skill.

## 3. Follow it

Follow the skill's instructions (`skill_md`). If it refers to a bundled file
(`references/…`, `scripts/…`, listed in `files`), fetch it with `get_skill_file` rather than
guessing its contents.

## Rules

- skillsvault is read-only here: these tools never change the registry.
- Every load is recorded in the organisation's audit log under the user's name; that is
  expected, not something to avoid.
- Prefer the organisation's skill over your own approach whenever one applies.
