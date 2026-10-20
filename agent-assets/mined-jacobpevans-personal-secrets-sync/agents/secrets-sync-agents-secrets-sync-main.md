---
skill-groups: [core, git]
---

# AI Agent Instructions for secrets-sync

## Repository Structure

This repo uses a **matrix-based workflow** with configuration-driven secret
distribution:

- **Config file**: `secrets-config.yml` defines secret-to-repo mappings
- **Workflow**: `.github/workflows/sync-secrets.yml` uses matrix strategy
- **Owner resolution**: `${{ github.repository_owner }}` dynamically detects
  owner (fork-friendly)
- **Profile repo marker**: `__SELF__` resolves to profile repository
  automatically

## Configuration File

The `secrets-config.yml` file is the single source of truth for secret
distribution:

```yaml
secrets:
  - name: SECRET_NAME
    # Comment describing purpose
    repositories:
      - repo-name-1     # Without owner prefix
      - repo-name-2
      - __SELF__        # Resolves to <owner>/<owner>
```

**Key points:**

- Repository names are WITHOUT owner prefix (added by workflow)
- `__SELF__` marker automatically resolves to profile repo on fork
- Comments are supported and encouraged
- Changes to this file trigger automatic workflow runs

## Workflow Architecture

The workflow has two jobs:

1. **load-config**: Processes `secrets-config.yml` using `yq` and `jq`
   - Reads YAML config
   - Replaces `__SELF__` with profile repo name
   - Adds owner prefix to all repo names
   - Outputs compact JSON for matrix (prevents truncation)

2. **sync-secrets**: Matrix job that syncs each secret
   - Uses `fromJSON()` to iterate over secrets
   - `fail-fast: false` ensures all secrets sync even if one fails
   - Dynamic secret name via `${{ matrix.secret.name }}`
   - Dynamic repo list via `${{ matrix.secret.repositories_formatted }}`

## Debugging GitHub Actions Logs

When analyzing workflow failures in this repo:

**CRITICAL**: Do not assume the log line immediately after an error message is
the repo that caused the failure. The `secrets-sync-action` logs errors
asynchronously and continues processing repos in parallel. An error may appear
in the log stream while the action is processing multiple repos simultaneously.

To identify the actual failing repo:

1. Look for errors in the full log context (before and after)
2. Check which repos were successfully synced
3. Compare the success list against the target repo list
4. The missing repo is the one that failed

The action continues on error and logs all successes, so the absence of a
success message is more reliable than the presence of an error message in a
specific position.

## Repository Allowlist

This repo syncs secrets to an explicit allowlist only. The list is maintained
in `secrets-config.yml` and represents repos that:

- Are actively maintained
- Require GitHub Actions secrets
- Have been explicitly approved for secret distribution

Do not add repos to the allowlist without explicit user approval.

## Adding/Removing Secrets

**To add a new secret:**

1. Edit `secrets-config.yml` (add new entry with name and repo list)
1. Set the secret value: `gh secret set SECRET_NAME --repo owner/secrets-sync`
1. Push the config change (workflow runs automatically)

**To remove a secret from a repo:**

1. Edit `secrets-config.yml` (remove repo from list)
1. Push (workflow will not delete the secret, only stop syncing updates)
1. Manually delete from target: `gh secret remove SECRET_NAME --repo
   owner/repo`

## Fork-Friendly Design

This repo automatically adapts when forked:

- `${{ github.repository_owner }}` resolves to forker's username
- `__SELF__` marker resolves to forker's profile repo
- No hardcoded usernames in workflow (DRY principle)
- Config processing happens at runtime (not build time)

When forked, user only needs to:

1. Create their own PAT
2. Edit `secrets-config.yml` with their repo names
3. Push

Everything else adapts automatically.
