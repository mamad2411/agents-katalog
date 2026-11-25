---
name: catalog
description: "Show SkillShop categories and explain how to search or apply the 157-playbook library."
disable-model-invocation: true
allowed-tools: "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/recommend.py *) Read"
---

# SkillShop catalog

SkillShop keeps its large playbook library out of Claude's always-on skill listing.

Explain the three entry points:

- `/skillshop:shop <task>` — route a task and apply a small composition.
- `/skillshop:find <query>` — search without loading full playbooks.
- `/skillshop:apply <name>` — load one exact playbook.

Read `${CLAUDE_PLUGIN_ROOT}/catalog.json` only if the user asks for the full catalog or category counts. Avoid dumping all 157 descriptions unless explicitly requested.
