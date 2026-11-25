---
name: copilot-plugin
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
description: >
  Create and maintain GitHub Copilot CLI plugins — skills, agents, prompts,
  instructions, AGENTS.md, and MCP servers. Use when building a new Copilot
  plugin, adding skills or agents to an existing plugin, writing AGENTS.md
  routing, creating prompt files, configuring MCP servers, adding hooks,
  validating plugin structure, or asking how Copilot CLI plugins work.
  This is for Copilot CLI plugins — NOT Claude Code projects.
---

# Copilot CLI Plugin Developer

Build and maintain GitHub Copilot CLI plugins. This skill has authoritative
specs, templates, and validation for all Copilot plugin components.

## CRITICAL: Copilot CLI != Claude Code

These are different ecosystems with different conventions. Read the relevant
spec in `reference/` before creating or modifying any component.

| Aspect | Copilot CLI Plugin | Claude Code |
|--------|-------------------|-------------|
| Skill frontmatter | Only `name`, `description`, `license` | Also `allowed-tools`, `metadata`, etc. |
| Instructions file | `AGENTS.md` (primary) | `CLAUDE.md` |
| Agent file extension | `.agent.md` | `.md` in agents/ |
| Agent naming | Lowercase kebab-case required | More flexible |
| Skill naming | Must match directory name | Convention only |
| Tool restrictions | Via `tools` in agent frontmatter | Via `allowed-tools` in skill |
| Installation | `copilot plugin install ./path` | Plugin marketplace |

**Do NOT use Claude Code patterns** when building Copilot plugin components.

## Workflow

### Step 1: Understand what's needed

Before creating anything, understand the user's intent:

1. **What problem?** — What should Copilot do differently?
2. **When should it apply?** — Always? Specific files? On demand?
3. **What type?** — Use the decision guide below

```
What do you need?
│
├─ Broad guidance for ALL interactions → Custom Instructions (.github/copilot-instructions.md)
├─ Guidance for SPECIFIC file types    → Path-specific (.github/instructions/*.instructions.md)
├─ A specialized AI persona            → Custom Agent (.github/agents/*.agent.md)
├─ A reusable prompt template          → Prompt File (.github/prompts/*.prompt.md)
├─ Complex task-specific guidance      → Skill (.github/skills/{name}/SKILL.md)
└─ Primary identity + routing          → AGENTS.md (root)
```

For detailed comparison, read `reference/comparison-matrix.md`.

### Step 2: Read the spec

Before writing any file, read the relevant spec:

| Task | Read first |
|------|-----------|
| Creating/modifying a skill | [skills-spec.md](reference/skills-spec.md) |
| Creating/modifying an agent | [agents-spec.md](reference/agents-spec.md) |
| Changing plugin.json or structure | [plugin-spec.md](reference/plugin-spec.md) |
| Adding/changing MCP servers | [mcp-spec.md](reference/mcp-spec.md) |
| Adding hooks | [hooks-spec.md](reference/hooks-spec.md) |
| Changing AGENTS.md or instructions | [instructions-spec.md](reference/instructions-spec.md) |

### Step 3: Create the component

Use the appropriate template from `templates/`:

| Type | Template | Output Location |
|------|----------|----------------|
| Custom Instructions | `templates/custom-instructions.md` | `.github/copilot-instructions.md` |
| Path-specific | `templates/path-instructions.md` | `.github/instructions/{name}.instructions.md` |
| Custom Agent | `templates/agent.md` | `.github/agents/{name}.agent.md` |
| Prompt File | `templates/prompt.md` | `.github/prompts/{name}.prompt.md` |
| Skill | `templates/skill.md` | `.github/skills/{name}/SKILL.md` |

### Step 4: Validate

Run the validation script to catch format issues:

```bash
python scripts/validate.py <path-to-file-or-directory>
```

### Step 5: Test and iterate

For skills, create trigger evals to test description accuracy:

1. Create `tests/evals/triggers/{name}.json` with 8+ positive and 8+ negative queries
2. Queries must be realistic, specific, and varied
3. Negative queries should be near-misses, not obviously irrelevant

For the eval format, read `reference/eval-schemas.md`.

## Writing Effective Customizations

Read `reference/writing-guide.md` for detailed guidance. Key principles:

- **Explain the why** — LLMs respond better to reasoning than rigid rules.
  Instead of "ALWAYS use named exports", explain why named exports matter.
- **Be specific** — "Use React Query for server state" beats "use good state management"
- **Show, don't tell** — One good example communicates what paragraphs cannot
- **Keep it lean** — Every instruction has a context cost. Cut what doesn't add value.
- **Constrain scope** — An agent that does everything well does nothing well
- **Generalize, don't overfit** — Address patterns, not individual cases

## Quick Reference: Plugin Structure

```
my-plugin/
├── plugin.json                    # Manifest (name, version, paths)
├── AGENTS.md                      # Primary instructions + routing
├── .mcp.json                      # MCP server config
├── hooks.json                     # Hook definitions
├── agents/
│   └── {name}.agent.md            # Custom agents (lowercase kebab-case)
├── skills/
│   └── {name}/
│       ├── SKILL.md               # Skill definition
│       ├── scripts/               # Helper scripts
│       ├── reference/             # Docs loaded on demand
│       └── templates/             # Output templates
└── extensions/
    └── {name}/
        └── server.py              # MCP server implementation
```

## Adding Skills

1. Read [skills-spec.md](reference/skills-spec.md)
2. Create `skills/{name}/SKILL.md` with **only** `name`, `description`, `license` in frontmatter
3. Directory name must match the `name` field exactly
4. Description explains WHAT and WHEN (this is the auto-trigger)
5. Validate: `python scripts/validate.py skills/{name}/`
6. Add to AGENTS.md routing table
7. Create trigger evals (8+ positive, 8+ negative queries)

## Adding Agents

1. Read [agents-spec.md](reference/agents-spec.md)
2. Create `agents/{name}.agent.md` with `name`, `description`, optional `tools`
3. Lowercase kebab-case names, filename must match
4. Define clear boundaries (what it does AND does not do)
5. Validate: `python scripts/validate.py agents/`
6. Add routing entries in AGENTS.md

## Reference Documentation

All specs are in `reference/`:

- [plugin-spec.md](reference/plugin-spec.md) — plugin.json manifest and structure
- [skills-spec.md](reference/skills-spec.md) — SKILL.md format, naming, activation
- [agents-spec.md](reference/agents-spec.md) — agent files, tool access, invocation
- [instructions-spec.md](reference/instructions-spec.md) — AGENTS.md, custom instructions
- [mcp-spec.md](reference/mcp-spec.md) — MCP server configuration
- [hooks-spec.md](reference/hooks-spec.md) — hook types and configuration
- [eval-schemas.md](reference/eval-schemas.md) — JSON schemas for trigger evals, grading, benchmarks
- [comparison-matrix.md](reference/comparison-matrix.md) — When to use which customization type
- [writing-guide.md](reference/writing-guide.md) — How to write effective instructions
