---
name: boxel-create-edit-cards
description: Use when choosing the realm.* calls in a run-realm-code script that create new cards or edit existing instances from the AI assistant.
boxel:
  kind: skill
---

# Creating and Editing Cards

This skill's content has been folded into **`boxel-environment`**, which owns runtime orchestration with `run-realm-code`.

Read:

1. `../boxel-environment/references/card-tool-selection.md` — the table of `realm.*` calls that create and edit cards, the quick decision tree, file naming, and path rules.
2. `../boxel-environment/SKILL.md` — the master decision tree (Step 4 covers data tasks).

`source-code-editing` defines the `run-realm-code` tool used to create and edit files (`.gts` and `.json` alike) and card field values.
