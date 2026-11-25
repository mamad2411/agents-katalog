---
name: foo
description: A skill used only by the binary-e2e frontmatter fixture.
hooks:
  PostToolUse:
    - matcher: ""
      hooks:
        - type: command
          command: skill-hook.sh
---

# Foo skill

A skill used only by the binary-e2e frontmatter fixture.
