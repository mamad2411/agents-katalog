# Built-in skill: Create skill

The **create-skill** built-in teaches Orion's assistant to author new workspace skills — reusable instruction packages stored as `SKILL.md` files in your Jupyter workspace. Use it when you want repeatable team workflows, checklists, or domain rules the assistant should follow in future chats.

Load it with **`/create-skill`** or ask in plain language: "Create a skill for …"

## What happens when you use it

When you ask Orion to create a skill, the assistant:

1. Treats your message as a **specification** for the new skill (not as a live task to complete in the current chat).
2. Chooses a kebab-case skill id (for example `quarterly-report`).
3. Writes `.agents/skills/<name>/SKILL.md` by default.
4. Optionally adds companion files such as `reference.md` or `examples.md` in the same folder.
5. Tells you where the files were saved and that you may need to reconnect the kernel to see the skill listed.

The deliverable of that chat turn is the **skill package**, not the end-user artifact the skill will produce later (for example, the assistant writes the skill file; it does not run the full quarterly report unless you ask separately).

## Where skills are stored

| Location | When to use |
| --- | --- |
| `.agents/skills/<name>/SKILL.md` | **Default** — shared with other agent tooling in the repo |
| `.orion/skills/<name>/SKILL.md` | Orion-only override when the same skill name already exists under `.agents` |

**Precedence** when Orion loads skills (lowest to highest):

1. User `.agents/skills`
2. User `.orion/skills`
3. Project `.agents/skills`
4. Project `.orion/skills`

A workspace skill with the same `name` as a built-in skill **replaces** the built-in copy for that workspace.

### Paths on your machine

Skills live in your **Jupyter workspace** (the folder Orion uses as the file root). Dot-directories are normal:

**macOS / Linux**

```
<workspace>/.agents/skills/my-workflow/SKILL.md
<workspace>/.orion/skills/my-workflow/SKILL.md
```

**Windows**

```
<workspace>\.agents\skills\my-workflow\SKILL.md
<workspace>\.orion\skills\my-workflow\SKILL.md
```

User-level skills (outside a project folder) sit at the Jupyter **server root** when you author globally.

## SKILL.md format

Every skill needs YAML frontmatter followed by markdown instructions:

```markdown
---
name: my-workflow
description: Standardizes quarterly CSV ingestion and validation. Use when importing spreadsheets, cleaning tabular data, or validating columns before analysis.
disable-model-invocation: false
---

# My workflow

## Steps
1. ...
```

| Field | Rules |
| --- | --- |
| `name` | Lowercase letters, numbers, hyphens only. Matches `/my-workflow`. |
| `description` | Third person. State **what** the skill does and **when** to use it (trigger phrases). |
| `disable-model-invocation` | Optional. When `true`, the skill loads only via `/name`, not automatically. |

Keep `name` and `description` on **single lines** in frontmatter for reliable parsing.

## After creating a skill

1. The new skill appears as **`/my-workflow`** in the slash command palette.
2. The model may also load it automatically when your message matches the description.
3. If it does not appear immediately, **reconnect the Jupyter kernel** or reload Orion.
4. If Jupyter hides dot-folders, enable hidden directories — see [Jupyter hidden folders and skills](/troubleshooting/jupyter-hidden-folders-and-skills).

## Authoring tips

- **Be specific** — Name skills after the workflow (`data-pipeline-qa`), not generic labels (`helper`).
- **Progressive disclosure** — Keep `SKILL.md` focused; put long reference material in `reference.md` in the same folder.
- **Third-person descriptions** — Good: "Builds stratified train/validation splits. Use when preparing tabular ML datasets." Avoid: "I can help you split data."
- **Prefer `.agents/skills`** — Use `.orion/skills` only for Orion-specific tweaks to an existing shared skill.

## Examples of good requests

- "Create a skill for how our team validates CSV uploads before analysis."
- "Add a skill that enforces our notebook naming convention and export checklist."
- "Scaffold a skill under `.agents/skills` for writing customer-facing release notes."

## Related

- [Skills](/ai-assistant/skills) — workspace skill format and precedence
- [Built-in skills hub](/ai-assistant/builtin-skills)
- [Slash commands](/ai-assistant/slash-commands)

---

*Last updated May 2026.*
