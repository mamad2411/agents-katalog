---
name: 1password-secrets-in-code
description: Use this skill to securely integrate 1Password secrets into codebases, AI agents, or CI/CD pipelines using secret references (op://vault/item/field), the op run --env-file pattern, 1Password SDK secrets.resolve() for AI agents with service accounts, MCP server wrapping with op run to avoid plaintext secrets in mcp.json, or the GitHub Actions load-secrets-action and CircleCI secrets orb. Also use to audit a codebase for hardcoded secrets.
---

# 1Password Secrets in Code

Use this skill when code, tools, or pipelines need secrets without plaintext exposure.

## Core model

- Store secret values in 1Password.
- Reference them in code/config as `op://vault/item/field`.
- Resolve at runtime with `op run`, `op inject`, or SDK calls.

## Security rules

- Never commit plaintext tokens or credentials.
- Never pass raw credentials directly to model prompts.
- Use least-privilege service accounts and narrow vault scope.
- Prefer short-lived auth where possible.

## MCP wrapping pattern

1. Put secrets in vault.
2. Use `.env.op` with secret references.
3. Keep `.env`/`.env.op` ignored by git.
4. Launch MCP server wrapped in `op run --env-file=.env.op -- <server-command>`.

See [MCP wrapping](references/mcp-wrapping.md).

## SDK pattern for AI agents

- Authenticate with `OP_SERVICE_ACCOUNT_TOKEN`.
- Resolve only explicit references with SDK.
- Keep `secrets.resolve()` in static controller code, not LLM-generated code paths.

See [SDK patterns](references/sdk-patterns.md).

## CI/CD patterns

- GitHub Actions: `1password/load-secrets-action@v2` (+ `configure@v2`).
- CircleCI: `onepassword/secrets` orb (`exec` masks, `export` does not).
- Jenkins: plugin + `withSecrets`.

See [CI/CD integration](references/cicd-integration.md).

## Optional audit

Use `scripts/audit-plaintext-secrets.py` to scan for likely hardcoded secrets and suggest `op://` replacement patterns.

## Companion skills

- `1password` for local CLI/auth/service-account basics.
- `1password-environments` for mounted local `.env` via Environments.
- `1password-ssh` for SSH and Git signing workflows.

## References

- [MCP wrapping](references/mcp-wrapping.md)
- [SDK patterns](references/sdk-patterns.md)
- [CI/CD integration](references/cicd-integration.md)
- [Template](assets/.env.op.template)
