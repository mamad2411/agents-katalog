# Templates

Templates for creating modes and skills.

## Contents

| File | Purpose |
|------|---------|
| `mode.yaml.template` | Template for new modes |
| `skill.md.template` | Template for new skills |

## Usage

### Creating a Mode

```bash
modes create my-mode
```

Uses `mode.yaml.template` with placeholders replaced.

### Creating a Skill

Copy `skill.md.template` to your skill directory and customize.

## Placeholders

| Placeholder | Replaced With |
|-------------|---------------|
| `{{NAME}}` | Mode/skill name |
| `{{NAME_UPPER}}` | Name in uppercase |
| `{{DESCRIPTION}}` | User-provided description |
| `{{CONTEXT}}` | Usage context |
