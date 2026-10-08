---
name: /extract-skill
description: >
  Skill promotion. Promotes a registered candidate from shared memory into an
  official .skill.md file, wires it into the relevant personas, and updates the
  skills index. Run when a candidate reaches 3+ independent instances.
---

# /extract-skill — Skill Promotion

Promote a skill candidate from `AgenticLab/knowledge/shared/memory.md` into an official skill file, wire it into the relevant agent personas, and update the skills index.

---

## Context

Brain modules (SYSTEM_CORE, governance, protocol, memory-spec) and the Knowledge
Digest are injected by the adapter at session start — they are already in context.
No manual load is required.

Agent personas are loaded per-phase as specified below.

---

## Step 1 — Select Candidate

Read `AgenticLab/knowledge/shared/memory.md → ## Skill candidates`.

List registered candidates with their instance counts. Ask:

> *"Which candidate should be promoted? (Enter the candidate name or number)"*

If no candidates are registered:
> *"No skill candidates registered yet. Nothing to extract."*

Stop here if there are no candidates.

---

## Step 2 — Draft the Skill File

Using the candidate's description and the agents that used it, draft a skill file.

**Target path:** `AgenticLab/knowledge/skills/[verb]-[noun].skill.md`

```markdown
---
semanticmap: true
---

# [Skill Name]

**Used by:** [comma-separated agent names]
**Trigger:** [one-line operational precondition — when this skill applies AND when it does NOT]

---

## Procedure

1. [step]
2. [step]
...

## Constraints

[What must NOT happen during this procedure]

## Examples

**Case 1 — [canonical case]**
[Before / After if applicable, or description of the pattern]

**Case 2 — [key variant or edge case]**
[Description]

**Case N — [case where this skill does NOT apply]**
[Description and why the skill doesn't apply here]

## Self-update rule

When you apply this skill and the result is approved: note in this section what differed from the canonical case — new variants, edge cases, or caveats not covered above.
```

Present the draft and ask:
> *"Does this look right? Reply 'yes' to create it, or give feedback to revise."*

Wait for approval before writing anything.

---

## Step 3 — Create the Skill File

Write the approved skill file to `AgenticLab/knowledge/skills/[verb]-[noun].skill.md`.

Update `AgenticLab/knowledge/skills/README.md → ## Skills index` with a new row:

```
| `[verb]-[noun].skill.md` | [trigger — one line] | [agents wired to] |
```

Add a SEMANTIC_MAP node for this skill so it is discoverable via trigger-term
matching — not only via the skills index lookup at session start:

```markdown
## [Skill Name]
- **Slug:** `[verb]-[noun]-skill`
- **File:** `AgenticLab/knowledge/skills/[verb]-[noun].skill.md`
- **Aliases:** `[skill name], [common trigger phrase]`
- **Related:** [[concepts the skill applies to]]
- **Governs:** [what task class this skill applies to]
- **Trigger terms:** [words in a task description that should surface this skill]
```

For any existing skills in the index whose file does not contain `semanticmap: true`
in its frontmatter, back-fill a SEMANTIC_MAP node using the same format, then set
`semanticmap: true` in that skill file's frontmatter.

---

## Step 4 — Wire into Agent Personas

For each agent listed in the skill's "Used by" field, open `AgenticLab/brain/personas/[agent].md`.

Add or update the `## Skills` section:
```
## Skills

- For [trigger condition], use `AgenticLab/knowledge/skills/[verb]-[noun].skill.md`
```

If a `## Skills` section already exists, append the new entry.

---

## Step 5 — Update Shared Memory

In `AgenticLab/knowledge/shared/memory.md`:

1. Remove the promoted candidate from `## Skill candidates`
2. If the list is now empty, restore the placeholder: `*No candidates registered yet.*`
3. Add a row to `## Skills index`:

```
| `[verb]-[noun].skill.md` | [trigger — one line] | [agents wired to] |
```

The skills index is read by all agents at session start via the shared MOC. Any agent whose task matches the trigger can follow the skill regardless of whether their persona was patched.

---

## Step 6 — Confirm

Report:
- Skill file created: `[path]`
- SEMANTIC_MAP node added: `[slug]` with trigger terms `[list]`
- Skills index updated in `AgenticLab/knowledge/shared/memory.md` and `AgenticLab/knowledge/skills/README.md`
- Persona files patched: `[list]`
- Candidate removed from shared memory

## Step 7 — Session Log

Append a session log entry to `AgenticLab/knowledge/shared/LOG/YYYY-MM-DD.md` (today’s date; append if file exists).
