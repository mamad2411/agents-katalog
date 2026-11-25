---
name: docs-ship
description: Run the local docs/workspace checks before declaring a customization change done.
user-invocable: true
---

# Docs Ship

Use this skill to verify the workspace before saying it works.

## Run

```bash
./.github/skills/docs-ship/run-docs-checks.sh
```

## Output

The script should report:

- required files exist
- parity-guard passes
- core VS Code customization files are present
- sample TypeScript targets exist
