---
name: op-inject
description: Use 1Password CLI `op inject` to populate configuration files with secrets securely.
---
# 1Password CLI - `op inject`

Use `op inject` to supply secrets to configuration files without hardcoding them. 

## Usage
Replace hardcoded secrets in your templates with 1Password secret references (e.g., `op://Vault/Item/Field`).
Then run:
```bash
op inject -i template.config -o actual.config
```

## Best Practices
- Never commit `actual.config` to version control. Add it to `.gitignore`.
- Keep `template.config` in version control with the `op://` references.
- Use `op read` if you only need to fetch a single secret value.

## Common Secret Reference Format
`op://<vault-name>/<item-name>/<field-name>`
