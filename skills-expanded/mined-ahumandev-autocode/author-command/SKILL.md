---
name: author-command
description: Use `author-command` to get OpenCode Command Authoring when writing or reviewing OpenCode command markdown.
---

# OpenCode Command Authoring

Use this guide when writing or reviewing OpenCode command markdown.

---

## Locations

- Project command: `.opencode/commands/{name}.md`
- Global command: `~/.config/opencode/commands/{name}.md`
- Prefer Project command.

---

## File Template

Command file is raw markdown with YAML frontmatter.

```markdown
---
description: Short command summary.
agent: agent-name (optional)
model: provider/model (optional)
---

$ARGUMENTS

---------

COMMAND PROMPT
```

Frontmatter keys:
* `description`: short command summary.
* `agent`: agent name. Optional.
* `subtask`: false (if need context of session); true (isolated session)
* `tier`: Non-creative task -> `fast`; project changes -> `balanced`; complex/planning/design task -> `smart`

Body:
- Direct prompt text.
- Use `$ARGUMENTS` where user args belong. Prefer to separate with `---------` to avoid confusion with fixed COMMAND PROMPT.

---

## Naming

- Use lowercase kebab-case filename.
- No slash in filename.
- Command name comes from file path.
- Prefer short verb-noun names.
- Avoid collisions with existing commands.

---

## COMMAND PROMPT

- Group related rules with H2 headers
- When rules contradict: Add conditions when to apply which rule
- Must be < 30 words per rule
- Prefer concise bullets unless user specified format
- Condition format: "If [some condition], then: [rule]; Otherwise [alternative rule]"
- Use numbered list for steps
- Keep COMMAND PROMPT lean.
- Write Caveman English.

---

## Rules

- Do not store secrets.
- Keep exact paths and frontmatter keys.
