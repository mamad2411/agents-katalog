---
name: new-skill
description: Author a new skill under .claude/skills/. Handles template scaffold, frontmatter, review-criteria self-check, and skills-index update.
---

# New skill

Scaffold and review a new skill file in `.claude/skills/`. Use this when a workflow recurs often enough to justify a named, invokable skill.

## Pre-flight

Before creating a new skill, confirm all three:

1. **Recurring need** — this isn't a one-off task.
2. **No overlap** — no existing skill in `skills-index.yaml` already covers this.
3. **Adds structure** — the skill provides invariants, ordered steps, or mandated checks that a bare prompt wouldn't.

If any fail, stop and reconsider. Often the right answer is *updating an existing skill* or adding a topic file to `agent-instructions/`.

## Steps

1. **Ask the operator:**
   - Skill slug (lowercase, hyphens, e.g. `release-notes`).
   - One-line description (starts with a verb, under 200 chars).
   - When to invoke (describe the triggering task).
   - Scale fit — small / medium / large (any subset).
   - Tools the skill needs (Read, Edit, Write, Bash, Glob, Grep, AskUserQuestion, etc.).
   - Lifecycle: `once` or `recurring`.

2. **Validate the slug:** matches `^[a-z][a-z0-9-]*$` and isn't already used.

3. **Create `.claude/skills/<slug>.md`** with the template below.

4. **Open the file for editing** and draft the body with the operator. Guide them through each section of the template — don't dump it and leave.

5. **Self-review** against `references/skill-review-criteria.md`. Go through every checkbox. Fix anything missing. Do not skip this step.

6. **Update `skills-index.yaml`** — append an entry for the new skill. Use the same slug, file name, description, triggers, scale, tools, and lifecycle.

7. **Update `.claude/skills/README.md`** — add a row to the human-readable table.

8. **Update `agent-instructions/`** if the skill introduces a recurring practice that deserves its own topic file or section (e.g. a new-skill for release automation might update `development-workflow.md`).

9. **Commit (ask first):** stage the new skill, the updated index, and the updated README. Commit message:
   `feat(skills): add /<slug> — <one-line description>`

## Template

```markdown
---
name: <slug>
description: <one-line description, verb-first, under 200 chars>
---

# <Human title>

<One paragraph: what this skill does and when to invoke it. Link to the
relevant `agent-instructions/` topic file(s).>

## Pre-flight

<What must be true before running. Detected stack? Clean working tree? Operator
confirmation? Any "stop and ask" conditions.>

## Steps

1. <Numbered, ordered, imperative. One action per step.>
2. ...
3. ...

## Output format

<If the skill produces a report, table, file, or other artifact, show the exact
structure. Use a literal example where possible.>

## Invariants

- <Things the skill must never do — destructive without confirmation, secret
  exposure, etc.>
- <Things the skill must always do — cite file:line, respect the task scale,
  link to the source of truth.>

## Related

- <Topic files, other skills, external docs.>
```

## Invariants

- **Don't create a skill that duplicates an existing one.** Update the existing skill instead.
- **Don't merge skills that solve genuinely different problems.** Keep responsibilities narrow.
- **Don't skip the review checklist.** Skill quality compounds — a sloppy skill trains sloppy operators.
- **Don't forget the index.** A skill not listed in `skills-index.yaml` is invisible to skill-selection.

## Related

- [`references/skill-review-criteria.md`](references/skill-review-criteria.md) — the quality bar.
- [`skills-index.yaml`](skills-index.yaml) — the machine-readable index.
- [`README.md`](README.md) — the human-readable index.
- `agent-instructions/scaling-agent-instructions.md` — when to promote a recurring pattern into a dedicated file vs. a skill.
