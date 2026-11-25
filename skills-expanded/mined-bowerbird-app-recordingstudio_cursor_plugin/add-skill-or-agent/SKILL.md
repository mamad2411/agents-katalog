---
name: add-skill-or-agent
description: Save a new Cursor skill or agent into this plugin. Use when the user wants to capture a workflow, specialist, or prompt so it can be reused and published to the Cursor Marketplace.
---

# Add a skill or agent

This plugin is the place Recording Studio skills and agents live. When someone wants to save a new one, add it here rather than only in a local Cursor folder.

## Choose the component

| Need | Add |
| --- | --- |
| A reusable workflow the main agent should follow | Skill in `skills/<name>/SKILL.md` |
| A specialist that should run in its own context | Agent in `agents/<name>.md` |
| A slash-command shortcut | Command in `commands/<name>.md` |
| Persistent guidance that should always apply | Rule in `rules/<name>.mdc` |

A skill is a one-shot workflow in the current chat. An agent is an isolated specialist the parent can delegate to.

## Skill checklist

1. Create `skills/<name>/SKILL.md`.
2. Use lowercase kebab-case. The folder name must match the frontmatter `name`. Product skills are `recording-studio-<topic>`; this plugin’s own workflow is the exception (`add-skill-or-agent`).
3. Include YAML frontmatter with `name` and `description`.
4. Put "use when" language in `description` so Cursor can decide to invoke it.
5. Keep the body actionable: when to use, steps, guardrails.
6. Optional supporting files go in `scripts/`, `references/`, or `assets/` beside `SKILL.md`.

```markdown
---
name: example-skill
description: One sentence of what it does and when to use it.
---

# Example skill

## When to use
- Concrete trigger

## Instructions
1. First step
```

## Agent checklist

1. Create `agents/<name>.md`.
2. Include YAML frontmatter with `name` and `description`.
3. Write the specialist prompt in the body.
4. Mention "use proactively" in `description` only when auto-delegation is wanted.

```markdown
---
name: example-agent
description: What this specialist does and when to delegate to it.
---

# Example agent

You are ...
```

## After adding

1. Run `node scripts/validate-plugin.mjs`.
2. Update `README.md` and `CHANGELOG.md` if the new component is user-facing.
3. Keep names unique across this plugin.
4. Do not commit secrets. Plugin variables belong in `.cursor-plugin/plugin.json` as names only.
