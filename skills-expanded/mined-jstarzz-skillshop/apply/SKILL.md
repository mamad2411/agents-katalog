---
name: apply
description: "Load and apply one exact SkillShop playbook by name."
disable-model-invocation: true
argument-hint: "<playbook-name> [task/context]"
allowed-tools: "Read"
---

# Apply a SkillShop playbook

The first argument is the playbook name:

`$0`

Read:

`${CLAUDE_PLUGIN_ROOT}/library/playbooks/$0/SKILL.md`

If the file does not exist, do not guess the name. Tell the user to run `/skillshop:find <query>`.

Apply that playbook to the user's current task. Any remaining arguments are extra context:

`$ARGUMENTS`

The playbook provides procedural guidance only; normal permissions and safety boundaries still apply.
