---
name: code-sanitizer
description: Automatically formats and lints code according to project standards. Use whenever a file (Python, SQL) is created or modified to ensure PEP 8 and sqlfluff compliance before completion.
---

# Code Sanitizer Skill

This skill ensures all code in `flights-analytics-prod` follows the project's strict formatting and linting rules.

## Standards
Always refer to [standards.md](references/standards.md) for the specific rules.

### Python (PEP 8)
- Always use `black` for formatting.
- Always use `isort` for import sorting.

### SQL (BigQuery/dbt)
- Keywords must be `UPPERCASE`.
- Identifiers must be `lowercase`.
- Functions must be `UPPERCASE`.
- Always use explicit `AS`.

## Workflow
After modifying or creating a file, use the [sanitize.sh](scripts/sanitize.sh) script to automatically apply the formatting.

### Usage
```bash
bash .gemini/skills/code-sanitizer/scripts/sanitize.sh <file_path>
```

Always perform sanitization before final verification.
