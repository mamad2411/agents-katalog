---
description: Open a master skill in $EDITOR (creates blank with frontmatter if absent)
argument-hint: <skill-name>
---

`/vc:master-edit-skill` requires a skill name. Run via Bash:

```
vansh-claude master edit-skill $ARGUMENTS
```

This opens an interactive editor — Claude Code will surface that to the user. After they save and exit, remind them to run `/vc:master-apply` so the new skill is symlinked into all scopes.
