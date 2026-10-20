# Modes Directory

Mode definitions and foundation protocols.

## Contents

| Item | Purpose |
|------|---------|
| `foundation.md` | PARAMOUNT skills that load with every mode |
| `definitions/` | YAML mode definition files |

## Foundation

`foundation.md` defines skills that are ALWAYS active:
- asking-users (AskUserQuestion protocol)
- context-gate (context monitoring)

## Adding Modes

1. Create YAML in `definitions/`
2. Follow schema in `definitions/CLAUDE.md`
3. Test with `modes activate <name>`
