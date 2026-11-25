---
name: openclaw-skill-creator
description: "Create OpenClaw-compatible skills with proper metadata, structure, and packaging. Use when building skills for OpenClaw agents, including: (1) Initializing new OpenClaw skills, (2) Adding openclaw metadata (emoji, requires, install), (3) Packaging skills as .skill ZIP files, (4) Converting Claude Code skills to OpenClaw format."
---

# OpenClaw Skill Creator

Create skills compatible with OpenClaw's skill system.

## OpenClaw Skill Structure

```
skill-name/
├── SKILL.md              # Required - Main definition
├── scripts/              # Optional - Executable code
├── references/           # Optional - Context documentation
└── assets/               # Optional - Templates, images
```

## SKILL.md Format

```yaml
---
name: skill-name
description: "What the skill does AND when to trigger it"
metadata:
  openclaw:
    emoji: "🔧"
    requires:
      bins: ["python3", "curl"]      # Required binaries
      anyBins: ["docker", "podman"]  # Any one of these
    install:
      - id: "brew"
        kind: "brew"
        formula: "tool-name"
        bins: ["tool"]
        label: "Install via Homebrew"
      - id: "apt"
        kind: "apt"
        package: "tool-name"
        bins: ["tool"]
        label: "Install via apt"
---

# Skill Title

Instructions for the agent...
```

## Workflow

### 1. Initialize Skill

```bash
python3 ~/.claude/skills/openclaw-skill-creator/scripts/init_openclaw_skill.py \
  --name "my-skill" \
  --path "./skills" \
  --emoji "🚀" \
  --requires "python3,curl" \
  --resources "scripts,references"
```

### 2. Implement Skill

Edit the generated files:
- Write SKILL.md instructions
- Add scripts to `scripts/`
- Add documentation to `references/`
- Add templates to `assets/`

### 3. Package Skill

```bash
python3 ~/.claude/skills/openclaw-skill-creator/scripts/package_openclaw_skill.py \
  ./skills/my-skill
```

Creates `my-skill.skill` (ZIP file).

## Key Differences from Claude Code Skills

| Feature | Claude Code | OpenClaw |
|---------|-------------|----------|
| metadata.openclaw | No | Yes (emoji, requires, install) |
| Package format | Folder | .skill ZIP |
| Init script | Manual | init_openclaw_skill.py |

## OpenClaw Metadata Reference

See `references/openclaw_metadata.md` for complete metadata documentation.

## Design Principles

1. **Concise** - Only include what the agent doesn't already know
2. **Progressive Disclosure** - Load references only when needed
3. **Degrees of Freedom** - Match specificity to task fragility

## Common Patterns

### API Integration Skill
```yaml
metadata:
  openclaw:
    emoji: "🌐"
    requires:
      bins: ["curl", "jq"]
```

### Python Processing Skill
```yaml
metadata:
  openclaw:
    emoji: "🐍"
    requires:
      bins: ["python3"]
    install:
      - id: "brew"
        kind: "brew"
        formula: "python@3.11"
        bins: ["python3"]
        label: "Install Python 3.11"
```

### Multi-Tool Skill
```yaml
metadata:
  openclaw:
    emoji: "🔧"
    requires:
      bins: ["git"]
      anyBins: ["docker", "podman"]
    install:
      - id: "docker-brew"
        kind: "brew"
        formula: "docker"
        bins: ["docker"]
        label: "Install Docker (brew)"
```
