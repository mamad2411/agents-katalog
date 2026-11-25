---
name: hard-coded
description: Looks up a house rule before writing any note. Use when a note is about to be written, or when the user asks which rule applies.
disable-model-invocation: maybe
cursorRuleType: always
---

# Hard coded

1. Read the rule list at ~/.claude/skills/house-rules/references/rules.md
2. Apply the first rule that matches. Stop when the note names the rule it followed.
