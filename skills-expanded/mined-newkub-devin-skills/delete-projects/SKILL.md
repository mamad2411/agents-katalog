---
name: delete-projects
description: Safely delete a project across local, remote repo, and Cloudflare resources
argument-hint: "[project-path-or-name]"
related:
  - delete
  - follow-service-cloudflare
  - list-cloudflare-projects
  - update-references
  - ask-me

---

## Goal

Safely delete a project from every place it lives: the local directory, the remote git repository, and Cloudflare Workers/Pages/D1/KV/R2/Queues/secrets

## Scope

- use when you want to remove a project from the machine and all its services
- covers the local working directory, git remotes, the GitHub repo, and Cloudflare resources
- not for ordinary file deletion without project context

## Execute

### 1. Identify Project

> Goal: Identify the project and the resources to delete

1. Take the project path or project name from the user
2. Verify the local path actually exists
3. Run `git remote -v` to find remote URLs
4. Look for Cloudflare config: `wrangler.toml`, `wrangler.jsonc`, `wrangler.json`, `wrangler.config.ts`
5. Identify related git branches, worktrees, and submodules

### 2. Dry Run Discovery

> Goal: List what will be deleted before actually deleting

1. Summarize the local directory and its total size
2. Summarize the remote repository (owner/name) from the remote URL
3. Summarize potentially related Cloudflare resources:
   - Worker name from the wrangler config
   - Pages project
   - D1 database, KV namespace, R2 bucket, Queue, secrets
4. Summarize git branches and worktrees
5. Show the report as a table

### 3. Confirm With User

> Goal: Get explicit confirmation before deleting

1. Ask the user whether to delete local, remote, Cloudflare, or all of them
2. If remote or Cloudflare has production data → double confirm
3. If local has uncommitted changes → notify and ask whether to back up or cancel
4. Never proceed without a clear answer

### 4. Backup Local

> Goal: Back up data before deletion when needed

1. If local has uncommitted/untracked changes → back up to `%TEMP%/<project-name>-backup-<timestamp>` or `.trash/`
2. Record the backup path
3. If local is tracked by git and clean → no extra backup needed

### 5. Delete Cloudflare Resources

> Goal: Delete the related resources on Cloudflare

1. Check the `wrangler` CLI and authentication with `wrangler whoami`
2. Delete secrets with `wrangler secret delete <name>` per the list
3. Delete cron triggers with `wrangler triggers delete`
4. Delete queues with `wrangler queues delete <queue>`
5. Delete D1 databases with `wrangler d1 delete <database>`
6. Delete KV namespaces with `wrangler kv namespace delete`
7. Delete R2 buckets with `wrangler r2 bucket delete <bucket>`
8. Delete the Pages project with `wrangler pages project delete <project>`
9. Delete the Worker with `wrangler delete`
10. If any command fails → stop and report

### 6. Delete Remote Repository

> Goal: Delete the remote git repository

1. Check the `gh` CLI with `gh --version`
2. Run `gh auth status` to verify login
3. Run `gh repo delete <owner>/<repo> --confirm` if the user confirmed
4. Or use `git push origin --delete <branch>` for specific branches when the whole repo should not be deleted
5. Record the remote URLs that were deleted

### 7. Delete Local Directory

> Goal: Delete the local project safely

1. If the local path is inside system paths such as `C:\Windows`, `C:\Program Files`, `~` → stop and ask
2. Run `Remove-Item -Recurse -Force "<path>"` on Windows or `rm -rf "<path>"` on macOS/Linux
3. Or use `git worktree remove` if it is a worktree
4. Verify that the directory is deleted

### 8. Cleanup References

> Goal: Fix references pointing to the project

1. Use `/update-references` for workspace files that reference this project
2. Remove git remotes from other projects that may point here
3. Update `AGENTS.md` or `README.md` if there are links

### 9. Validate And Report

> Goal: Verify the deletion is complete

1. Verify the local directory is deleted
2. Verify the remote repo is unreachable (or gone)
3. Check Cloudflare resources with `wrangler list` commands
4. Report what was deleted, the backup path, and anything left over

## Rules

### 1. Never Delete Without Confirmation

- Always dry run and get explicit user confirmation
- Never delete system paths, the home directory, or another repo's `.git`
- Never delete production resources without double confirmation

### 2. Safety First

- Back up uncommitted changes before deleting
- Never delete files containing secrets, API keys, or credentials without checking
- If unsure → stop and use `/ask-me`

### 3. Tool Availability

- `wrangler` is required for Cloudflare
- `gh` is required for GitHub
- If a tool is missing → notify the user and stop

### 4. Reversibility

- Always record the backup path
- Record the list of deleted resources
- If a deletion was a mistake → notify the user and state the recovery steps

- Use /delete-git-branch if needed
- Use /delete-git-worktree if needed
- Use /follow-service-cloudflare if needed
- Use /list-cloudflare-projects if needed

## Expected Outcome

- The local directory is deleted
- The remote git repository is deleted (if requested)
- Cloudflare resources are deleted per the confirmed scope
- No uncommitted changes lost
- A deletion report and backup path are provided
