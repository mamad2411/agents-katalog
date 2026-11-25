---
name: single-root-skill
description: The plugin's only skill, loaded from the plugin root.
hooks:
  SessionStart:
    - hooks:
        - type: command
          command: plugin-root-skill-hook.sh
---

# Single Root Skill

Bootstrap step: !`plugin-root-skill.sh`
