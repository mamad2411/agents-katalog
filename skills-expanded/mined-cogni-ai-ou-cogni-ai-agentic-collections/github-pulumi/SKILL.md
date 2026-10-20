---
name: github-pulumi
description: Activate when managing GitHub resources with Pulumi CLI to import, preview, update, and repair state.
license: MIT
---

# GitHub Pulumi

<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->

Use Pulumi CLI to manage GitHub resources (repos, branches, teams) with fast imports, previews, and state fixes.

## Core Process

1. **Ensure token**: classic PAT with `repo` + `security_events`, or fine-grained with repo Administration (read) and Contents (read); authorize for orgs/SSO.
2. **Set credentials**: `export GITHUB_TOKEN=<pat>` and `pulumi config set --secret github:token <pat>`; set owner if needed: `pulumi config set github:owner <owner>`.
3. **Verify plugins**: `pulumi plugin ls`; install if missing: `pulumi plugin install resource github <ver>`.
4. **Preview/apply non-interactively**: `pulumi preview --non-interactive` then `pulumi up --yes --non-interactive`.
5. **Import existing repo**: `pulumi import github:index/repository:Repository <name> <repo-name>`.
6. **Keep YAML in sync**: Update local codebase with import output to avoid drift (merge allowed fields only).

## Core Principles

- **State Integrity**: `pulumi state delete` is destructive; always confirm URNs and consider backup (`pulumi stack export`) before modification.
- **Resource Protection**: Protect critical resources with `protect: true`; explicitly unprotect them before intentional deletion.
- **Secret Management**: Never commit secrets; rely solely on Pulumi config/stack secrets and environment variables.
- **Directory Context**: Always run commands in the stack directory (use `-C <dir>` if scripted).

## Commands / Usage Patterns

```bash
# Show stack resources and their URNs
pulumi stack --show-urns

# Import an existing repository (non-interactive)
pulumi import github:index/repository:Repository <name> <repo-name> --yes --non-interactive

# Refresh state without applying changes (non-interactive)
pulumi refresh --yes --non-interactive

# Detect state drift safely
pulumi preview --non-interactive

# Remove an unwanted state entry without deleting the remote resource
pulumi state unprotect <urn> --yes --non-interactive
pulumi state delete <urn> --force --yes --non-interactive

# Move a resource between stacks
pulumi state move --source <src-stack> --dest <dst-stack> <urn>
```

## Diagnostics and Troubleshooting

- **Token Updates**: After token changes, re-run `pulumi config set --secret github:token <pat>` to ensure the new token is used.
- **Missing Plugins**: If resources fail to load, run `pulumi plugin ls` and install the missing GitHub provider plugin.

## What to Avoid

- Avoid using repository default branch settings directly on the repository resource if it triggers warnings; use `github_branch_default` instead.
- Do not run interactive commands in automated environments; always append `--non-interactive` and `--yes` as appropriate.
- Do not commit state files or secrets to the repository.

## Limitations

- `pulumi state delete` only removes the resource from the state, not from the actual GitHub provider.

## Related Skills

- **gh**:
  You MUST load this skill when interacting with GitHub via the CLI for resource verification.
