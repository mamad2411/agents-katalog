---
name: blueprint-check
description: Check that an oh-my-copilot v1 repository layout stays docs-first and Copilot CLI-only.
---

# Blueprint Check Skill

Use this skill to review an `oh-my-copilot` v1 repository draft.

## Active routine

If shell access is available, run:

```bash
./.github/skills/blueprint-check/run-blueprint-check.sh
```

Use the command output as the primary evidence source.

## Checklist

- README says v1 is Copilot CLI-first and docs/research-first.
- Public docs list cloud agent, IDE, SDK, and runtime machinery as non-goals for
  v1 unless a later plan explicitly widens scope.
- Copilot capability claims cite GitHub documentation or changelog sources.
- Examples are labeled illustrative.
- No `.omx/` or OMC runtime state model is copied as a product requirement.
