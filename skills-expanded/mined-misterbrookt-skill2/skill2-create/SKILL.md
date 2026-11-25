---
name: skill2-create
description: "Use when creating, updating, splitting, merging, or restructuring an agent skill or skill library."
---

# Create Agent Skills

Create the smallest reusable instruction set that changes agent behavior without duplicating existing ownership.

## Scope

| Signal | Landing |
| --- | --- |
| Distinct reusable trigger and standalone workflow | Top-level `skills/<name>/SKILL.md` |
| More depth under the same trigger and workflow | `references/` under the owning skill |
| Repo-bound paths, commands, or conventions | Project-local skill |
| One-off answer or pure mechanical rule | No skill → script / validator / docs / lint / CI |

When uncertain, prefer `references/` or project-local placement over expanding the top-level namespace.

## Authoring

1. Define user trigger, desired behavior, output, and hard constraints.
2. Find existing ownership before creating a new top-level skill.
3. Choose scope and name from user intent, not implementation or one harness.
4. Write minimal `SKILL.md`; add resources only when they reduce noise or make execution deterministic.
5. Apply changes only when requested. Run repository validator when available.

## `SKILL.md`

- Plain Markdown with YAML frontmatter
- `name`: kebab-case; match directory name
- `description`: trigger conditions only; do not summarize workflow
- Body: principles, decisions, constraints, and output contract
- Keep instructions terse; explain only non-obvious choices
- Use relative paths; never embed secrets or accidental machine-local paths
- Preserve existing user rules unless change is required

## Resources

| Resource | Use |
| --- | --- |
| `references/` | Heavy detail loaded under the same trigger |
| `scripts/` | Deterministic, repeated, or fragile execution |
| `assets/` | Files copied or transformed into deliverables |

Create only needed directories. Keep references one hop from `SKILL.md`. Do not nest discoverable skills.
Do not create optional metadata unless the target repository or distribution format requires it.

## Commands

Skill-owned scaffold:

```bash
uv run --script <skill-dir>/scripts/run -- scaffold skill <name>
```

## Library decisions

- Split when users invoke workflows independently or ownership diverges
- Merge when triggers overlap, shared rules dominate, and one owner can maintain both
- Keep shared content with the narrowest owner serving every consumer
- Avoid duplicate instructions across sibling skills
- Keep top-level namespace flat and minimal

## Common mistakes

| Mistake | Better choice |
| --- | --- |
| Workflow summary inside `description` | Trigger-only description; workflow in body |
| New skill for a long table under the same trigger | `references/` under the owner |
| Global skill for one repo's conventions | Project-local skill or repo instructions |
| Skill for a regex-enforceable rule | Validator, lint, or CI |
| Empty resource directories | Create resources only when used |
| Harness-specific instructions in shared behavior | Harness-neutral rule or adapter-specific helper |

## Output

1. Scope decision: top-level / reference / project-local / no skill
2. Skill topology and ownership boundary
3. Created or updated files
4. Deterministic validation result, when available
