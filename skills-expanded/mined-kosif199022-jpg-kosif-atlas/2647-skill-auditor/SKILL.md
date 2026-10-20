---
name: skill-auditor
description: Audits a skill's SKILL.md frontmatter, catalog.yaml projection, references, and evals shape against the library schema, reporting ordered actionable findings; use for "audit this skill", "does X follow the schema", "lint X against the catalog", "check X before I publish it".
metadata:
  summary: Audits a skill's SKILL.md frontmatter, catalog.yaml projection, references, and evals shape against the library schema, reporting ordered actionable findings; use for "audit this skill", "does X follow the schema", "lint X against the catalog", "check X before I publish it".
  status: experimental
---

Read `instructions.md` in this skill's directory and follow it.

Path note: this skill also ships inside the `ambient` library plugin, so its
instructions may reference files as `${CLAUDE_PLUGIN_ROOT}/library/skill-auditor/<file>`.
When installed standalone, resolve those to `<file>` in this directory.
