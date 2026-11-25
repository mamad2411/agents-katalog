---
name: broken-references
description: Use this skill as a fixture when testing that SkillForge reports references to files that do not exist.
license: MIT
metadata:
  version: 0.1.0
---

# Broken References

The frontmatter here is valid, so the skill loads. What is wrong is the body: it points at files that
are not in the directory, which the file reference rule (SF0007) must report.

## Steps

1. Follow [the checklist](references/checklist.md) — this file does not exist.
2. Run [the analyzer](scripts/analyze.ps1) — this file does not exist either.
3. Read [the notes](references/notes.md) — this one does exist.
