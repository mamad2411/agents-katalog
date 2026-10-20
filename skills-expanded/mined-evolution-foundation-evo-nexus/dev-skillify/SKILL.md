---
name: dev-skillify
description: "Create a new custom skill for the workspace. Guides the user through defining the skill's slug, trigger conditions, workflow steps, outputs, and anti-patterns. Use when the user says 'create a skill', 'new skill', 'add a skill', 'I need a custom skill', or wants to formalize a workflow as a reusable skill."
---

# Create Custom Skill

Guide the user through creating a new custom skill that formalizes a reusable workflow.

## What You're Building

A custom skill is a `SKILL.md` file in `.claude/skills/custom-{slug}/` with the `custom-` prefix. It has:
- YAML frontmatter with `name` and `description` (the description is what Claude matches against user requests)
- A workflow Claude follows when the skill is invoked
- Optional helper scripts or templates inside the skill folder

Custom skills are gitignored (the `custom-` prefix triggers this) — they're personal to your workspace. If the user ever wants to publish the skill for others, it would need a non-`custom-` name and an entry in `.claude/rules/skills.md`; mention this only if it comes up.

## When to Use This Skill

- The user says "create a skill", "new skill", "add a skill"
- The user describes a workflow they want to reinvoke with one command
- The user wants to formalize an ad-hoc process before it's lost

## When NOT to Use

- The workflow is one-off and won't be repeated → don't skill it
- A skill for this already exists → use it instead (check with `ls .claude/skills/`)
- The task needs its own agent, not just a workflow → use `create-agent`
- The user wants a new slash command without a workflow → use `create-command`

## Step 1: Understand the Skill

Ask the user:
1. **What is the trigger?** When should Claude reach for this skill? (e.g., "review this PR for security", "generate a daily standup note")
2. **What slug?** Short, kebab-case. The final folder will be `custom-{slug}/`. Suggest one if the user doesn't have preference.
3. **What does it do?** The actual workflow — step by step.
4. **What does it produce?** File, report, summary, side effect — be explicit.
5. **What inputs does it need?** Args passed in, files it reads, external APIs, etc.
6. **Any anti-patterns?** Things the skill should explicitly NOT do (helps Claude stay focused).

If any answer is vague, push back once before writing. A skill built on fuzzy triggers won't get invoked correctly.

## Step 2: Generate the SKILL.md

Create `.claude/skills/custom-{slug}/SKILL.md`:

```markdown
---
name: custom-{slug}
description: "{one-line — what it does and when to use it. Include 2-3 trigger phrases verbatim.}"
---

# {Skill Title}

{One paragraph — what this skill accomplishes and why it exists.}

## When to Use

- {Explicit trigger phrase 1}
- {Explicit trigger phrase 2}
- {Situation that should invoke this skill}

## When NOT to Use

- {Adjacent scenario that should go elsewhere}
- {Edge case the skill doesn't handle}

## Inputs

- {What the user must provide}
- {What the skill reads from the workspace}

## Workflow

### Step 1 — {name}
{What to do, which tools to use, what to produce.}

### Step 2 — {name}
{...}

### Step 3 — {name}
{...}

## Output

{What the user sees when the skill finishes. Be concrete: file path, summary format, side effects.}

## Anti-patterns

- Do NOT {thing the skill must never do}
- Do NOT {common failure mode}

## Pairs With

- {Other skill or agent that commonly runs before/after}
```

**Description field is critical** — that's what Claude matches against user requests. Make it specific and include trigger phrases verbatim. Vague descriptions mean the skill never fires.

## Step 3: Add Helper Scripts (Optional)

If the skill needs reusable logic (Python, shell, templates), put them next to `SKILL.md`:

```
.claude/skills/custom-{slug}/
├── SKILL.md
├── scripts/
│   └── helper.py
└── templates/
    └── report.md
```

Reference them from the workflow with relative paths: `.claude/skills/custom-{slug}/scripts/helper.py`.

Don't add scripts unless the workflow actually needs them — most skills are just the `SKILL.md`.

## Step 4: Verify

Run a quick check:

```bash
ls -la .claude/skills/custom-{slug}/SKILL.md
head -5 .claude/skills/custom-{slug}/SKILL.md  # confirm frontmatter is valid
```

Then tell the user:
- Skill created: `custom-{slug}`
- Path: `.claude/skills/custom-{slug}/SKILL.md`
- Invoke it by describing the trigger in natural language, or explicitly `/custom-{slug}` if you also want a slash command (use `create-command` for that).
- To delete: `rm -rf .claude/skills/custom-{slug}/`

## Skill Naming Convention

| Pattern | Example | Purpose |
|---------|---------|---------|
| `custom-review-pr` | PR review | Code review helper |
| `custom-daily-note` | Daily note | Journaling workflow |
| `custom-vendor-check` | Vendor check | Ops check against a list |
| `custom-ship-report` | Ship report | Post-release comms |

Rules:
- Always use `custom-` prefix (required for gitignore)
- Use lowercase, hyphen-separated names
- Start with a verb or domain noun when it makes the purpose obvious
- Keep slugs short (2-3 words after prefix)
- Avoid names that collide with existing skills (check `ls .claude/skills/`)

## Existing Skill Prefixes (Do Not Duplicate Domain)

These prefixes already cover major domains — if the new skill fits, consider whether it belongs as a core skill (non-`custom-`) instead:

| Prefix | Domain |
|---|---|
| `dev-` | Engineering workflows |
| `fin-` | Finance |
| `legal-` | Legal / compliance |
| `hr-` | People / HR |
| `mkt-` | Marketing |
| `data-` | Data / BI |
| `pm-` | Product management |
| `cs-` | Customer success |
| `int-` | External integrations |
| `social-` | Social media |
| `ops-` | Operations |
| `create-` | Scaffolding (new agents, routines, etc.) |

If the user's skill clearly fits one of these and they want it permanent, suggest that and offer to drop the `custom-` prefix — but only if the user confirms, because that change pulls it out of gitignore and into the shared repo.

## Important Notes

- Custom skills (`custom-*`) are gitignored — they won't be pushed to the repo
- The `description` field in frontmatter is what Claude matches against — invest in it
- Skills are stateless — they run a workflow, they don't persist memory
- For persistent state, use an agent (with `create-agent`) or a ticket (with `create-ticket`)
- A skill can invoke agents via the `Agent` tool and other skills via `Skill` — compose freely
- If the workflow naturally pairs with a slash command, also run `create-command` with the same slug

## Anti-patterns

- Do NOT create skills for one-off tasks
- Do NOT write vague descriptions — they won't be matched
- Do NOT duplicate an existing skill's domain — read before writing
- Do NOT bake project-specific paths or credentials into the skill body — use env vars and `config/workspace.yaml`
- Do NOT skip the verification step
