---
name: validate-skill
description: Validate an existing OpenClaw skill's structure, frontmatter, metadata, dependencies, and content quality.
---

# Validate OpenClaw Skill

Validate an OpenClaw skill for correctness before deployment.

## Usage

`/validate-skill <path-to-skill-dir>`

If no path provided, ask the user which skill to validate. List available skills:
```bash
WORKSPACE=$(jq -r '.agents.list[] | select(.default==true) | .workspace // empty' ~/.openclaw/openclaw.json)
WORKSPACE=$(eval echo "$WORKSPACE")
ls -d "$WORKSPACE/skills/*/" 2>/dev/null
```

## Validation

Run the validation script:
```bash
bash scripts/validate-skill.sh "<skill-dir-path>"
```

Report results to the user. For any FAIL items, explain what's wrong and offer to fix it.

## Auto-Fix

For common issues, offer to fix automatically:
- Missing `name` field → derive from directory name
- Invalid metadata JSON → parse and reformat
- Name/directory mismatch → rename to match
- Over 500 lines → suggest content to move to `references/`
