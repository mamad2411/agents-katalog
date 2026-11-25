---
description: "Scaffold a new Claude Code skill into .claude/skills/<name>/SKILL.md — a model-invoked capability with a trigger-rich description, scoped tools, and a lean body that pushes detail into resource files."
argument-hint: "<what the skill should do>"
allowed-tools: "Read, Write, Glob, Grep"
---

## Scope

Treat `$ARGUMENTS` as the skill's purpose — the capability you want Claude to reach for automatically. Restate it in one sentence, then derive a **kebab-case skill name** (verb-led, e.g. `migrate-sql-schema`, `summarize-pr`) that will be both the folder name and the `name` field.

If `$ARGUMENTS` is empty, ask one focused question: *"What capability should this skill add, and roughly when should Claude reach for it?"* Do not invent a skill.

Default to **project scope**: `.claude/skills/<name>/SKILL.md`. Mention `~/.claude/skills/<name>/` as the alternative for skills the user wants across every project, and let them pick.

> [!WARNING]
> A skill is **model-invoked**, not user-invoked. Claude decides to load it by matching the conversation against the `description`. If the description is vague, the skill never fires — so the description is the most important thing you write, not the body.

## Step 1 — Understand the capability and check for collisions

Pin down what triggers the skill, what it does, and what it produces. Then `Glob .claude/skills/*/SKILL.md` (and `~/.claude/skills/*/SKILL.md`) and `Grep` the existing `name:` / `description:` lines. If a near-duplicate exists, say so and offer to extend it instead of creating an overlapping skill — two skills with similar descriptions make activation ambiguous.

## Step 2 — Skill vs. slash command sanity check

Confirm a skill is the right artifact before writing one:

- **Skill** — Claude should invoke it *on its own* whenever a matching situation arises (a recurring task it should recognize, e.g. "writing a migration", "reviewing Terraform"). Activation is the `description`.
- **Slash command** — the user wants to *trigger it explicitly by name* (`/create-skill`). If that's what they described, point them at `create-slash-command` instead and stop.

## Step 3 — Write the description (lead with what, then "Use when")

This is the load-bearing field. Format: one clause stating **what the skill does**, then a sentence starting **"Use when ..."** listing concrete triggers — the phrasings, file types, or intents that should activate it.

```
description: "Convert REST endpoint handlers into typed OpenAPI 3.1 specs. Use when the user adds or edits an Express/Fastify route, asks for API docs, or mentions an openapi.yaml / swagger file."
```

Name the real cues (file extensions, library names, task verbs). Avoid first-person and avoid "helps with" — write triggers Claude can pattern-match against.

## Step 4 — Write the SKILL.md (lean body, progressive disclosure)

Create `.claude/skills/<name>/SKILL.md` with `Write`. Frontmatter, then a body that fits comfortably on one screen:

```markdown
---
name: <kebab-name>            # MUST equal the folder name
description: "<from Step 3>"
allowed-tools: Read, Grep, Glob   # least privilege; omit to inherit the session's tools
user-invocable: true           # also lets the user call it like /<name>
---

# <Title Case Name>

## When to use
Restate the triggers as a short checklist so Claude self-confirms before acting.

## Instructions
1. First concrete step, referencing the inputs the skill works on.
2. ...
3. ...

## Output
Exactly what the skill produces and where (file path, message, diff).
```

Rules that keep the skill reliable:

- `name` must be identical to the folder name — a mismatch makes the skill fail to register.
- Scope `allowed-tools` to the minimum the procedure needs. A skill that only inspects code gets `Read, Grep, Glob`; add `Write`/`Edit`/`Bash(...)` only if it must change things.
- Keep `SKILL.md` focused on the *procedure*. The body is loaded into context every time the skill fires, so every extra line is a recurring token cost.

## Step 5 — Decide whether it needs resource files

Single-file is the default. Add sibling files only when warranted, and reference them by **relative path** so Claude loads them on demand (progressive disclosure), not eagerly:

- Long reference material (lookup tables, style rules, schemas) → `reference.md`, linked from SKILL.md as *"see ./reference.md for the full mapping"*.
- Runnable helpers → `scripts/<tool>.py` (or `.sh`), invoked from the Instructions; this requires a `Bash(...)` entry in `allowed-tools`.
- Reusable boilerplate the skill emits → `templates/<name>.tmpl`.

> [!NOTE]
> Progressive disclosure is the whole point of the multi-file layout: a one-paragraph pointer in SKILL.md costs a few tokens, while the linked file is read only when the task actually needs it. Don't paste a 300-line table into SKILL.md "to be safe."

## Report

Confirm the absolute path of the created `SKILL.md` (and any resource files), echo the `name` and `description`, and state the chosen scope (project vs. user). Tell the user the skill activates automatically when the conversation matches its triggers — and, if `user-invocable: true`, that they can also call it as `/<name>`. End with the single most useful next step: open a fresh session and try a prompt that should trip the trigger, to confirm the skill loads.
