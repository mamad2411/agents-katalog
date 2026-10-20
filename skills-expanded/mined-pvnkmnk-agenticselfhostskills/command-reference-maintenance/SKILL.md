---
name: command-reference-maintenance
description: Generate and validate shareable PowerShell or Bash command references from an explicitly supplied, non-sensitive command dump. Use when maintaining agent-readable command documentation, validating its JSON contract, or regenerating Markdown/JSON/YAML references without committing personal command histories, credentials, hostnames, or private filesystem paths.
---

# Command Reference Maintenance

Use this skill to turn an explicitly provided **sanitized** command dump into structured Markdown, JSON, and YAML references.

## Safety boundary

- Require an explicit input file; do not default to a personal command dump.
- Review the input for private paths, usernames, hostnames, credentials, tokens, and aliases that reveal sensitive workflows before committing generated output.
- Treat generated output as potentially sensitive because command names and modules can reveal local capabilities.
- Keep local inventories and user-specific output outside the canonical skill repository unless they have been intentionally sanitized.

## Workflow

1. Create a sanitized dump from the target shell. Prefer a minimal, shareable subset over a full personal inventory.
2. Run `scripts/generate_command_reference.py` with the shell type, input path, and output prefix.
3. Validate the generated JSON using the generator’s schema-aligned built-in validation; use `references/reference.schema.json` as the documented interchange contract.
4. Inspect Markdown and JSON for sensitive data before committing.
5. Retain the generator, schema, and tests as canonical tooling; keep generated references separate unless they are explicitly safe to share.

## Input formats

| Shell | Expected input |
|---|---|
| `pwsh` | One `Get-Command`-style entry per line. |
| `bash` | One command name per line; optionally provide an `alias` output file for alias targets. |

## Generator example

```bash
python scripts/generate_command_reference.py \
  --shell bash \
  --input /path/to/sanitized-bash-commands.txt \
  --out-prefix /path/to/output/bash-reference
```

The generator writes Markdown, Markdown-by-type, JSON, and YAML files. It validates the JSON after generation and removes generated files if validation fails.

## Maintenance rules

- Update `references/reference.schema.json` and the generator together when the data model changes.
- Preserve the current schema version and document any backwards-incompatible change.
- Test with a small sanitized fixture before changing parsing or validation behavior.
- Do not enable automatic collection or commit of a user’s shell inventory.
