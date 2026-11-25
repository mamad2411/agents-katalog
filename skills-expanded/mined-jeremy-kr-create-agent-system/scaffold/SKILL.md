---
name: scaffold
description: "Scaffold Claude Code Agent Teams into a project. Use for initial agent system setup or new project configuration."
user-invocable: true
allowed-tools: Bash(npx:*), Bash(cd:*), Read, Glob
---

# /scaffold

Scaffold a Claude Code Agent Teams-based development system into your project.

## Usage

### Interactive mode (default)

```bash
npx create-agent-system
```

Guides you through preset selection, project name, and tech stack confirmation interactively.

### Non-interactive mode

```bash
npx create-agent-system --preset <preset> --yes [options]
```

Options:
- `--preset, -p` — Preset name (solo-dev, small-team, full-team)
- `--project-name, -n` — Project name
- `--target, -t` — Target directory (default: current directory)
- `--no-run` — Skip automatic Claude Code launch
- `--yes, -y` — Skip interactive prompts
- `--dry-run` — Preview only, no files created
- `--save-config` — Save settings to agent-system.config.yaml

## Presets

| Preset | Target | Agents | Workflow |
|--------|--------|--------|----------|
| solo-dev | Solo developer | 5 (essential only) | Streamlined, no review |
| small-team | 2-5 people | 8 (all) | EPIC-based, standard review |
| full-team | Large team | 8 (all) | Full process, strict QA |

## Conflict handling

If an existing CLAUDE.md or .claude/ directory is found, conflict resolution options are provided:
- **Merge** — Keep existing content, add new sections
- **Overwrite** — Replace with new content
- **Skip** — Skip generating that file

## Generated files

- `CLAUDE.md` — Project memory and agent rules
- `.claude/agents/*.md` — Agent definitions
- `.claude/skills/*/SKILL.md` — Skill definitions
- `.claude/settings.json` — Agent Teams settings
