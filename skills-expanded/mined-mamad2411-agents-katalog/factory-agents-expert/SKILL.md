---
name: factory-agents-expert
description: Manages the agent/skill registry — add, rebuild, validate
triggers:
  - /factory_agents command
  - When agents or skills need to be added or managed
modes:
  - add: create or register agent/skill
  - rebuild: regenerate views
  - validate: check integrity
---

# 🏭 Factory Agents Expert

> **Role Skill** — Manages the agent/skill registry through the `/factory_agents` workflow.

---

## Scaffold Templates

### Agent Template

When creating a new agent, use this scaffold:

```markdown
---
name: { name }
description: { description }
---

# {Title}

> **Specialist Agent** — {description}

---

## Principles

1. [Core principle of this agent's domain]
2. [How this agent approaches problems]
3. [Quality standards this agent upholds]

---

## Capabilities

- [What this agent can do]
- [What tools/techniques it uses]
- [What outcomes it delivers]

---

## When to Activate

| Trigger             | Action                |
| ------------------- | --------------------- |
| [keyword/situation] | [what the agent does] |

---

## Rules

**ALWAYS:**

1. [Mandatory behavior]

**NEVER:**

1. [Prohibited behavior]

---

_TimeKast Factory — {Title}_
```

### Skill Template

When creating a new skill, use this scaffold:

````markdown
---
name: { name }
description: { description }
---

# {Title}

> **Skill** — {description}

---

## When to Use

- [Situation 1]
- [Situation 2]

---

## Key Concepts

### 1. [Concept Name]

[Explanation]

### 2. [Concept Name]

[Explanation]

---

## Patterns

### Pattern: [Name]

```[language]
[code example]
```
````

---

## Rules

**ALWAYS:**

1. [Mandatory practice]

**NEVER:**

1. [Anti-pattern]

---

_TimeKast Factory — {Title}_

```

---

## Interactive Flow Guide

### Add Mode — Decision Tree

```

/factory_agents add
├── Create new?
│ ├── Agent
│ │ ├── Kit → scaffold in agents/{name}.md
│ │ └── Project → scaffold in agents/project/{name}.md
│ └── Skill
│ ├── Kit → scaffold in skills/{name}/SKILL.md
│ └── Project → scaffold in skills/project/{name}/SKILL.md
└── Register existing?
├── Provide path to .md file
├── Extract metadata from frontmatter
└── Add entry to registry.yaml or project.yaml

````

### Required Fields

| Field | Agent | Skill | Example |
|-------|-------|-------|---------|
| name | ✅ | ✅ | `perf-analyst` |
| keywords (EN) | ✅ | ✅ | `performance, profiling, metrics` |
| keywords (ES) | ✅ | ✅ | `rendimiento, perfilado, métricas` |
| scope | ✅ | ✅ | `kit` or `project` |
| category | ❌ | ✅ | `domains`, `kit`, `roles`, `utils` |
| domain | ⚪ | ❌ | `ui`, `db`, `api`, `security`, `testing` |
| priority | ⚪ | ❌ | `70` (default) |
| description | ⚪ | ⚪ | Short description |

### Post-Add Checklist

After adding, the CLI automatically:

1. ✅ Adds entry to YAML (registry.yaml or project.yaml)
2. ✅ Scaffolds file (if creating new)
3. ✅ Rebuilds all 5 views
4. ✅ Runs validation

The agent should then:

5. ▶️ Show validation output to user
6. ▶️ If kit scope → offer npx push
7. ▶️ Suggest user review the scaffolded file

---

## CLI Reference

```bash
# Add new agent
python3 .agent/scripts/registry_cli.py add-agent \
  --name perf-analyst \
  --keywords "performance,profiling,metrics" \
  --keywords-es "rendimiento,perfilado,métricas" \
  --domain "" \
  --priority 70

# Add new skill
python3 .agent/scripts/registry_cli.py add-skill \
  --name perf-analysis \
  --category kit \
  --keywords "performance,profiling,metrics"

# Register existing
python3 .agent/scripts/registry_cli.py register \
  --path .agent/agents/my-agent.md \
  --keywords "keyword1,keyword2"

# Rebuild views
python3 .agent/scripts/registry_cli.py rebuild

# Validate
python3 .agent/scripts/registry_cli.py validate
python3 .agent/scripts/registry_cli.py validate --strict
````

---

_TimeKast Factory — Factory Agents Expert Skill_
