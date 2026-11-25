---
name: my-skill
description: >-
  One long, trigger-oriented paragraph describing WHAT this skill does AND WHEN a
  host agent should activate it. List the concrete phrases and situations that
  should trigger it, then the explicit non-triggers ("Do not use for…"). This is
  the text the agent matches against to decide whether to fire — invest here; it
  is what drives skill quality.
version: 0.1.0
---

# My Skill

Workflow and instructions go here. Use progressive disclosure: keep the core
workflow in this file, and put bulky templates, reference material, or helper
scripts in `references/` and `scripts/` subfolders, pulled in on demand. Helper
scripts should be stdlib-only / dependency-free where possible.

Do NOT put presentation/catalog metadata (summary, tags, license, when,
highlights, example) in this frontmatter. That lives in `catalog/<name>.yaml`,
which is never installed to a user — see the authoring guide in
`docs/skill-authoring.md`.
