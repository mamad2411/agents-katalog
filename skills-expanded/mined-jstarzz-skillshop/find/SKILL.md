---
name: find
description: "Search the SkillShop playbook catalog and show the best matches for a task or engineering concern."
disable-model-invocation: true
argument-hint: "<what you need help with>"
allowed-tools: "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/recommend.py *)"
---

# Find SkillShop playbooks

Search the library for:

`$ARGUMENTS`

Run:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/recommend.py" \
  --query "$ARGUMENTS" \
  --project "${CLAUDE_PROJECT_DIR}" \
  --top 15
```

Present the strongest matches with one short reason each. Do not load their full playbooks unless the user asks to apply one.
