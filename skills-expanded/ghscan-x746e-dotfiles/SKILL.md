---
name: forgejo
description: Teaches the agent how to interact with the local Forgejo Git server. Use this when the user wants to read/write issues or create/manage repositories on the local Forgejo instance.
---

# Forgejo Skill

This skill provides instructions for interacting with the local Forgejo server using the
`tea-cli` tool.

- **Authentication:** Append `--login local` to all commands to avoid interactive prompts.
  (If 'local' login is missing, see [setup.md](references/setup.md) or
  [admin.md](references/admin.md)).
- **Data Format:** You MUST append `-o yaml` or `-o json` to list and detail commands to get
  structured output that is easy to parse, instead of the human-readable tables.
- **Non-Interactive:** `tea-cli` might try to open a TTY for confirmation or editing. Always
  provide all required data via flags to keep commands strictly non-interactive.
- **General Formats:**
  - Repos are referenced as `<owner>/<repo_name>` (e.g. `ksp-org/test-repo`).
  - Issues are referenced by index within a repo.

## Primary Commands

### 1. Repositories

- **List repos:** `tea-cli repos ls --login local -o yaml`
- **Create a repo:**
  `tea-cli repos create --name <repo_name> --owner <org_name> --description "..." --login local`
  - *Note:* ALWAYS create repositories in the `ksp-org` organization unless specified
    otherwise.
  - *Note:* Use `--private` if it should be a private repository.
- **Git Push/Clone:** See `references/repo-setup.md` for how to configure non-interactive
  authentication when setting up a new repository remote.

### 2. Issues

- **List issues in a repo:**
  `tea-cli issues ls --repo <owner>/<repo_name> --login local -o yaml`
- **Get specific issue:**
  `tea-cli issues ls --repo <owner>/<repo_name> <issue_index> --login local -o yaml`
- **Create an issue:**
  `tea-cli issues create --repo <owner>/<repo_name> --title "My Issue" --body "Issue details here" --login local`
- **Comment on an issue:**
  `tea-cli comment create --repo <owner>/<repo_name> --issue <issue_index> --body "My comment" --login local`
- **Close an issue:**
  `tea-cli issues close --repo <owner>/<repo_name> <issue_index> --login local`

### 3. User Management

- **Update user avatar:** This must be done via the REST API using an admin token and the
  `Sudo` header. See [admin.md](references/admin.md) for the exact `curl` command.
