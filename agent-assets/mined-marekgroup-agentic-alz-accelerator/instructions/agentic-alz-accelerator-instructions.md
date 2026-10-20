---
description: "Guidelines for creating high-quality custom instruction files for GitHub Copilot in this ALZ accelerator"
applyTo: ".github/instructions/**"
---

# Custom Instructions File Guidelines

For the complete official reference, see
[VS Code Custom Instructions docs](https://code.visualstudio.com/docs/copilot/customization/custom-instructions).

## Frontmatter

All frontmatter fields are optional. Without `applyTo`, the instructions file
is not auto-applied but can still be manually attached to a chat request.

```yaml
---
description: "Brief purpose statement"
applyTo: "**/*.py"
---
```

| Field | Default | Constraints |
|-------|---------|-------------|
| `description` | — | 1-500 chars, clearly state purpose and scope |
| `applyTo` | — | Glob pattern(s): `**/*.ts` or `**/*.ts, **/*.tsx` or `**` for all files |

## File Locations

| Scope | Path |
|-------|------|
| Workspace instructions | `.github/instructions/` (searched recursively) |
| Workspace skills | `.github/skills/{name}/SKILL.md` |
| Workspace agents | `.github/agents/{name}.md` |
| Repo-level instructions | `.github/copilot-instructions.md`, `AGENTS.md` |
| User profile | `~/.copilot/instructions/` |

## Priority Order

When multiple instruction sources exist, higher priority wins on conflict:

1. Personal instructions (user-level, highest)
2. Repository instructions (`.github/copilot-instructions.md` or `AGENTS.md`)
3. Organization instructions (lowest)

## Instructions vs Skills vs Agents

| Type | Location | Purpose | Auto-applied? |
|------|----------|---------|---------------|
| Instructions | `.github/instructions/*.instructions.md` | Coding rules for file types | Yes, via `applyTo` glob |
| Skills | `.github/skills/{name}/SKILL.md` | Domain knowledge for agents | No, loaded on demand |
| Agents | `.github/agents/{name}.md` | Agent persona + workflow | No, invoked explicitly |

- **Instructions** = coding conventions applied when editing matching files
- **Skills** = reference knowledge loaded by agents during workflow steps
- **Agents** = specialized personas with defined roles and tool access

## Current Instruction Files

| File | Glob | Purpose |
|------|------|---------|
| `python.instructions.md` | `**/*.py` | Python style, async, testing, MCP patterns |
| `iac-bicep-best-practices.instructions.md` | `**/*.bicep` | Bicep AVM patterns, security baseline |
| `iac-terraform-best-practices.instructions.md` | `**/*.tf` | Terraform AVM patterns, security baseline |
| `json.instructions.md` | `**/*.{json,jsonc}` | JSON formatting conventions |
| `yaml.instructions.md` | `**/*.{yml,yaml}` | YAML formatting conventions |
| `markdown.instructions.md` | `**/*.md` | Markdown structure, artifact naming |
| `shell.instructions.md` | `**/*.{sh,bash}` | Shell script conventions |
| `wara-checks.instructions.md` | `**/wara_checks.yaml` | WARA check authoring rules |
| `instructions.instructions.md` | `.github/instructions/**` | This file (meta-instructions) |

## File Structure

1. **Frontmatter** with `description` and `applyTo`
2. **Title** (`#`) with brief introduction
3. **Core sections** organized by domain — prefer tables and bullet lists over prose
4. **Examples** with fenced code blocks showing correct patterns
5. **Validation** (optional) — build/lint/test commands

## Writing Rules

| Rule | Details |
|------|---------|
| Imperative mood | "Use", "Implement", "Avoid" — not "You should" |
| Specific and actionable | Concrete examples > abstract concepts |
| Concise and scannable | Bullet points, tables; avoid verbose paragraphs |
| No ambiguity | Avoid "should", "might", "possibly" |
| Show why | Explain reasoning only when it adds value |
| Stay current | Reference current versions; remove deprecated patterns |
| Project-specific | Focus on patterns unique to this ALZ accelerator |

## Patterns to Follow

- **Tables** for structured rules, comparisons, parameter lists
- **Code blocks** showing correct usage patterns
- **Bullet lists** for sequential rules or checklists
- **Cross-references** to skills for deep domain knowledge
- **Validation commands** so agents can self-check

## Patterns to Avoid

- Verbose explanations — keep it scannable
- Duplicating content already in skills (reference instead)
- Missing code examples — abstract rules without patterns
- Contradictory advice within or across instruction files
- Hardcoded counts or lists that go stale (use descriptive language)

## Maintenance

- Review when dependencies or frameworks are updated
- Keep glob patterns accurate as project structure evolves
- Target under 150 lines; split deep knowledge into skills under `.github/skills/`
- Do not duplicate between instructions and skills — instructions are for coding rules, skills are for domain knowledge
- Validate changes don't conflict with existing instructions (check overlapping globs)
