---
name: sylph-create-skill
description: Create a new skill from scratch. Generates the SKILL.md, registers it in AGENTS.md, and sets up the content folder structure.
---

# Create Skill

## When to use

Run `/sylph-create-skill <name>` when the CAO wants to add a new skill that doesn't exist yet.

## Usage

```
/sylph-create-skill social-listening
/sylph-create-skill competitor-analysis
```

---

## Step 1: Understand the skill

Ask the CAO ONE question:

> What should **[skill-name]** do? (2-3 sentences is enough)

From her answer, derive:
- **Purpose**: what problem does it solve?
- **Domain**: which area does it belong to? (content, sales, product, brand, finance, hr, legal, ops, events, writing, agents)
- **Trigger**: when would someone invoke it? (on-demand, daily, event-triggered)
- **Inputs**: what does it need to run? (a topic, a file, a customer name, nothing)
- **Outputs**: what does it produce? (a draft, a report, an issue, a Slack message)
- **MCP connectors**: which external tools does it need?

## Step 2: Create the skill file

Create `.claude/skills/<skill-name>/SKILL.md` with this structure:

```markdown
---
name: <skill-name>
description: <one line - what it does and when to use it>
---

# <Skill Title>

## MCP connectors

| Connector | Purpose |
|-----------|---------|
| [tool] | [what it's used for] |

## Context loading

1. Read [relevant files] for context
2. Read `_insights.md` for the domain (if exists)
3. Read `_examples/` for quality reference (if exists)

## Arguments

| Argument | What it does |
|----------|-------------|
| [arg] | [description] |

## Execution

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Guardrails

- [Safety rule 1]
- [Safety rule 2]
- **Never publish or send directly** - always save to `_drafts/`

## Self-improvement

After the CAO reviews and approves the output:

1. Move the final version from `_drafts/` to `_published/`
2. Diff what was drafted vs what the CAO kept - identify patterns in her edits
3. Update `_insights.md` with what worked, what she changed, and why
4. If her edits reveal a recurring pattern or new rule, add it to this skill file
5. If the output was a top performer, promote it to `_examples/`
```

### Skill file rules

- **Flat path**: `.claude/skills/<skill-name>/SKILL.md` - one level only, no subdirectories
- **YAML frontmatter required**: `name` and `description` fields
- **MCP connectors table**: always include, even if empty ("None required")
- **Guardrails section**: always include - every skill must define what it does NOT do
- **No em dashes**: use `-` or `:`

## Step 3: Create the content folder (if applicable)

If the skill produces content, create the folder structure:

```
<domain>/<channel>/
  _drafts/          # where new content goes
  _published/       # approved content archive
  _examples/        # best-performing pieces (few-shot reference)
  _insights.md      # channel learnings (create empty with header)
```

Not all skills need a content folder. Agent skills, ops skills, and tool skills may just use `agents/<name>/_logs/`.

## Step 4: Register the skill

Add the skill to the index table in `AGENTS.md` (section 8):

```markdown
| <skill-name> | <domain> | `.claude/skills/<skill-name>/SKILL.md` |
```

Insert in alphabetical order within the domain group.

## Step 5: Create the setup guide (optional)

If the skill needs configuration (MCP connections, examples, voice derivation), create a setup guide at `.claude/skills/sylph-setup-skill/setup-<skill-name>.md` and add it to the dispatch table in `sylph-setup-skill/SKILL.md`.

Only create a setup guide if the skill requires initial configuration. Simple on-demand skills don't need one.

## Step 6: Add the self-improvement loop (mandatory)

Every skill MUST have a `## Self-improvement` section as its last section. This is what makes Sylph a self-improving system instead of a static prompt library.

Add this section to the skill file you created in Step 2:

```markdown
## Self-improvement

After the CAO reviews and approves the output:

1. Move the final version from `_drafts/` to `_published/`
2. Diff what was drafted vs what the CAO kept - identify patterns in her edits
3. Update the relevant `_insights.md` with what worked, what she changed, and why
4. If her edits reveal a recurring pattern or new rule, add it to this skill file
5. If the output was a top performer, promote it to `_examples/` with annotated frontmatter
```

Adapt the wording to fit the skill's output type:
- **Content skills** (posts, emails, articles): focus on voice, structure, and tone patterns
- **Agent/routine skills** (CoS, CSM, EA): focus on format, scope, and prioritization patterns
- **Analysis skills** (reports, screening, reviews): focus on depth, framing, and what the CAO found useful vs noise
- **Ops skills** (CRM, docs updates): focus on process efficiency and what the CAO corrected

The key principle: the skill improves because the CAO's edits are signal. Capture what she changed and why, then bake that into the skill's rules and the domain's insights.

## Step 7: Test

Generate one piece of output using the new skill. Ask the CAO to review. Capture any corrections in the skill file or `_insights.md`.

---

## Checklist

Before finishing, verify:
- [ ] `SKILL.md` exists at `.claude/skills/<skill-name>/SKILL.md`
- [ ] Frontmatter has `name` and `description`
- [ ] MCP connectors table is present
- [ ] Guardrails section is present
- [ ] **Self-improvement section is present** (mandatory)
- [ ] Skill is registered in `AGENTS.md` section 8
- [ ] Content folder created (if applicable)
- [ ] Test output generated and reviewed
