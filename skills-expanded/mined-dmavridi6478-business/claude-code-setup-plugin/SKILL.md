# claude-code-setup Plugin

Official Claude plugin that scans your project and recommends exactly which hooks, skills, MCPs, and subagents to configure — so you don't have to figure it out manually. By @codenameposhan.

## Install

Inside Claude Code, run:

```
/plugin install claude-code-setup@claude-plugins-official
```

## What It Does

Analyzes your codebase and produces a personalized recommendation for:

| Component | What It Recommends |
|-----------|-------------------|
| **Hooks** | Pre/post-tool hooks for your workflow |
| **Skills** | Skills that match your project type |
| **MCPs** | MCP servers for your tech stack |
| **Subagents** | Specialized agents for your tasks |

## Usage

After installing, ask Claude:

```
recommend automation for this project
```

Claude will scan the repo structure, stack, and existing config, then output a full setup plan.

## Package as a Plugin (Team Sharing)

To share your `.claude/` config with teammates without committing it to the repo:

```
/plugin marketplace add .
```

This packages your `skills/agents/hooks` into a versioned plugin anyone on the team can install — keeps personal settings out of git while making team settings installable.

## Full Workflow

```
1. /plugin install claude-code-setup@claude-plugins-official
2. recommend automation for this project
3. Review recommendations → apply ones that fit
4. /plugin marketplace add .   (optional — share with team)
```

## Notes

- The plugin runs on **Claude Opus 5** with 1M context by default
- It reads your existing CLAUDE.md, package.json, directory structure, and current `.claude/` config
- Particularly good at spotting missing MCP servers for your tech stack (Supabase, GitHub, Linear, etc.)
- Works alongside DevSwarm.ai for multi-agent team workflows
