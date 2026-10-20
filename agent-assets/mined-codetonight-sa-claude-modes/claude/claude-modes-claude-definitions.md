# Mode Definitions

YAML mode definition files.

## Contents

| Mode | Description |
|------|-------------|
| `code-mode.yaml` | Software development |
| `security-mode.yaml` | Security auditing |
| `research-mode.yaml` | Research and analysis |

## Schema

```yaml
name: mode-name
description: What it does. Use when context.
version: 1.0.0

triggers:
  commands:
    - /mode name
  patterns:
    - "keyword"

skills:
  always:
    - skill-a
  optional:
    - skill-b

token_budget: ~3500
foundation: true

prompt_injection: |
  [MODE: NAME]
  Instructions...

context:
  - Use case
```

## Creating Modes

```bash
modes create my-mode
```

See `docs/CREATING-MODES.md` for full guide.
