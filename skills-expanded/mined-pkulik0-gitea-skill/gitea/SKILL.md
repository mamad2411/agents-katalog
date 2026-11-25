---
name: gitea
description: Interface with Gitea instances via the tea CLI. Manage repositories, issues, pull requests, releases, labels, milestones, CI/CD actions, webhooks, organizations, wiki pages, SSH keys, comments, and notifications. Use when user mentions "Gitea", "tea CLI", or asks to create/list/edit/close issues, create/review/merge pull requests, manage repos, create releases, view CI/CD workflow runs, manage webhooks, track time, or perform any code hosting task on a Gitea server. Do NOT use for GitHub (use gh CLI) or GitLab.
license: MIT
compatibility: Requires tea CLI (gitea.com/gitea/tea) v0.15+ installed. Works in Claude Code, Cursor, Cline, and any agent with Bash tool access.
metadata:
  author: community
  version: 1.1.0
  tags: [gitea, git, devops, ci-cd, code-hosting, self-hosted]
---

# Gitea

Gitea is a self-hosted Git service. This skill uses the `tea` CLI (v0.15+) to manage Gitea resources. All operations go through `tea` commands executed via Bash.

## Important: Before Any Operation

Run `bash scripts/check-tea.sh` (from the skill directory) or manually verify:

```bash
tea --version && tea logins ls
```

If `tea` is not installed, tell the user to install it (`brew install tea` on macOS, or see the tea repo). Require v0.15 or newer. If no logins exist, guide them through `references/authentication.md`.

## Context Detection

When inside a git repository, `tea` auto-detects the Gitea instance and repo from git remotes. Override with:
- `--repo owner/repo` to target a specific repository
- `--login name` to use a specific Gitea login
- `--remote name` to use a specific git remote

Always check context first:

```bash
git remote -v 2>/dev/null
tea logins ls --output simple
```

## Output Formatting

Use `--output` (`-o`) to control format:
- `json` - best for parsing results programmatically
- `simple` - compact, one value per line
- `table` - human-readable (default)
- `csv` / `tsv` / `yaml` - for data export

When processing results in scripts, prefer `--output json`. When displaying to users, prefer `--output table`.

## Instructions

### Issues

**List issues:**
```bash
tea issues ls                          # open issues in current repo
tea issues ls --state closed           # closed issues
tea issues ls --labels bug,urgent      # filter by labels
tea issues ls --assignee username      # filter by assignee
tea issues ls --milestones "v1.0"      # filter by milestone
tea issues ls --keyword "search term"  # search by keyword
tea issues ls --kind pulls             # PRs, with issue-list filters
tea issues ls --owner my-org           # issues across an org
tea issues ls --fields "index,title,state,assignees,labels" --output table
```

**Create an issue:**
```bash
tea issues create --title "Bug: login fails" --description "Steps to reproduce..." --labels bug --assignees user1,user2
```

**Edit issues:**
```bash
tea issues edit 42 --title "New title" --add-labels enhancement --add-assignees user2
tea issues edit 42 --milestone "v2.0" --deadline 2025-12-31
tea issues edit 42 --set-assignees alice,bob   # replace assignees
tea issues edit 42 --remove-assignees bob
```

**Close / reopen:**
```bash
tea issues close 42
tea issues reopen 42
```

### Comments

```bash
tea comment 42 "This is fixed in commit abc123"   # historical shorthand still works
tea comments add 42 --description "Fixed in abc123"
tea comments ls 42
tea comments edit 1001 --description "Updated comment"
tea comments delete 1001
```

Use `tea comments ls` to get comment IDs for edit/delete.

### Pull Requests

**List / inspect:**
```bash
tea pulls ls                           # open PRs
tea pulls ls --state closed --output json
tea pulls 15 --output json             # detail for one PR (not `pulls ls 15`)
tea issues ls --kind pulls --labels "needs-review"   # filter PRs by label
```

`tea pulls ls` has no `--labels` flag.

**Create a PR:**
```bash
tea pulls create --title "Add auth module" --description "Implements OAuth2 flow" --base main --head feature-branch
tea pulls create --title "Fix #42" --base main --head fix-login --labels bugfix --assignees reviewer1
tea pulls create --title "WIP auth" --base main --head wip-auth --draft
```

For fork-based PRs, use `--head username:branch`. `--draft` prepends `WIP: ` (Gitea treats that as a draft).

**Edit:**
```bash
tea pulls edit 15 --title "New title" --add-reviewers alice
tea pulls edit 15 --ready              # strip WIP prefix
tea pulls edit 15 --draft              # mark draft (idempotent)
```

**Review and merge:**
```bash
tea pulls review 15                    # interactive review
tea pulls approve 15                   # approve (alias: lgtm)
tea pulls reject 15 "Needs tests"      # request changes (reason required)
tea pulls merge 15 --style squash      # merge, rebase, squash, rebase-merge
tea pulls merge 15 --style squash --title "feat: auth module (#15)" --message "Implements OAuth2"
tea pulls review-comments 15
tea pulls reply 15 1001 "Fixed"
tea pulls resolve 1001
tea pulls unresolve 1001
```

**Checkout a PR locally:**
```bash
tea pulls checkout 15                  # fetches and checks out PR branch
tea pulls checkout 15 --branch         # create local branch if missing (boolean flag)
tea pulls clean 15                     # delete local+remote branches after merge
```

### Repositories

**List and search:**
```bash
tea repos ls                           # your repos on default login
tea repos ls --owner my-org
tea repos ls --starred
tea repos search "keyword"             # search across instance
tea repos search "keyword" --owner org # search within org
tea repos ls --output json --limit 50
```

**Create / edit:**
```bash
tea repos create --name my-project --description "A new project" --init --gitignores Go --license MIT
tea repos create --name team-project --owner my-org --private
tea repos create-from-template --template owner/template --name new-proj --owner my-org --content --labels
tea repos edit --repo owner/repo --description "Updated" --default-branch main
```

`create-from-template` requires `--template` and `--name`. It does not share `create`'s `--init` / `--gitignores` flags.

**Fork and clone:**
```bash
tea repos fork --repo owner/repo
tea repos fork --repo owner/repo --owner my-org    # fork to org
tea clone owner/repo                               # clone (auto-detects login)
```

`fork` does not take a positional slug. A leftover arg is ignored and tea forks the **current** repo instead.

**Delete:**
```bash
tea repos delete --owner owner --name repo  # destructive - confirm with user first
```

`--repo` is not a delete flag. Use `--owner` and `--name`. `--force` skips the confirmation prompt.

**Migrate from external source:**
```bash
tea repos migrate --name imported-repo --clone-url https://github.com/user/repo.git --service git --mirror
```

`--service` is one of: `git`, `gitea`, `gitlab`, `gogs`. There is no `github` value; use `git` for GitHub.

### Releases

Release subcommands take a **tag name**, not a numeric ID.

```bash
tea releases ls
tea releases create --tag v1.0.0 --title "Release 1.0.0" --note "Release notes here" --target main
tea releases create --tag v1.0.0 --title "v1.0.0" --note-file CHANGELOG.md --asset ./dist/binary.tar.gz
tea releases create --tag v2.0.0-rc1 --prerelease --draft
tea releases edit v1.0.0 --title "Patch Release"
tea releases delete v1.0.0 --confirm           # --confirm is required
tea releases assets ls v1.0.0
tea releases assets create v1.0.0 ./path/to/file.zip
tea releases assets delete v1.0.0 file.zip --confirm
```

Asset delete takes the attachment **filename**, not a numeric asset ID.

### Labels and Milestones

**Labels** (update/delete use `--id`, not a positional index):
```bash
tea labels ls
tea labels create --name "priority:high" --color "#ff0000" --description "High priority"
tea labels update --id 5 --name "priority:critical" --color "#990000"
tea labels delete --id 5
```

**Milestones** take the **title**, not a numeric ID:
```bash
tea milestones ls
tea milestones create --title "v2.0" --description "Major release" --deadline 2025-06-01
tea milestones close "v2.0"
tea milestones issues "v2.0"                   # list issues in milestone
tea milestones issues add "v2.0" 42
tea milestones issues remove "v2.0" 42
```

### CI/CD Actions

**Workflow runs:**
```bash
tea actions runs ls                        # list recent runs
tea actions runs ls --status failure --branch main
tea actions runs view 42                   # view run details
tea actions runs view 42 --jobs
tea actions runs logs 42                   # view run logs
tea actions runs logs 42 --job 1           # specific job logs
tea actions runs logs 42 --follow          # stream logs in real time
tea actions runs delete 42 --confirm       # cancel/delete a run
```

**Secrets and variables:**
```bash
tea actions secrets ls
tea actions secrets create SECRET_NAME secret_value
tea actions secrets create DB_PASSWORD --file ./secret.txt
tea actions secrets delete SECRET_NAME --confirm

tea actions variables ls
tea actions variables set VAR_NAME var_value
tea actions variables delete VAR_NAME --confirm
```

**Workflows:**
```bash
tea actions workflows ls
tea actions workflows view ci.yml
tea actions workflows dispatch ci.yml --ref main --input env=prod
tea actions workflows enable ci.yml
tea actions workflows disable ci.yml --confirm
```

On `dispatch`, `--ref` and `--repo` both claim `-r`. Always use the long flags.

### Organizations

Aliases are `organizations`, `organization`, `org`. There is no `orgs` alias.

```bash
tea org ls
tea org create my-org --description "My organization" --visibility public
tea org delete my-org                      # destructive - confirm first
```

The org name is the first argument. `-n` / `--full-name` is the display name, not the slug.

### Wiki

```bash
tea wiki ls
tea wiki view Home
tea wiki revisions Home
tea wiki create --title "Runbook" --content "On-call steps" --message "Add runbook"
tea wiki edit Home --content "Updated home" --message "Refresh home"
tea wiki delete OldPage --confirm
```

### Branches

```bash
tea branches ls
tea branches protect main
tea branches unprotect old-main
tea branches rename old-name new-name
```

### Time Tracking

```bash
tea times ls '#42'                         # quote # so the shell does not treat it as a comment
tea times add 42 2h30m                     # add takes a bare issue index
tea times delete 42 1                      # delete time entry
tea times reset 42                         # reset all tracked time
tea times ls --mine --total                # your times across all repos
```

### Notifications

```bash
tea notifications ls                       # unread + pinned
tea notifications ls --mine --states unread # across all repos
tea notifications read 1                   # mark as read
tea notifications unread 1                 # mark as unread
tea notifications pin 1                    # pin notification
tea notifications unpin 1
```

### Webhooks

Create takes the URL as a **positional** argument (no `--url` on create). Update uses `--url`.

```bash
tea webhooks ls
tea webhooks create https://example.com/hook --events push,pull_request --secret mysecret
tea webhooks update 1 --url https://new-url.com --events push
tea webhooks delete 1 --confirm
```

### SSH Keys

```bash
tea ssh-keys ls
tea ssh-keys add ~/.ssh/id_ed25519.pub --title laptop
tea ssh-keys delete 12 --confirm
```

### Open in browser

```bash
tea open                    # repo home
tea open 42                 # issue or PR by index
tea open pulls              # also: issues, wiki, settings, labels, milestones
```

### Direct API Access

For operations not covered by tea subcommands, use `tea api`:

```bash
tea api /repos/{owner}/{repo}                                    # GET (default)
tea api --method PUT /repos/{owner}/{repo}/topics/ci             # add topic
tea api "/repos/{owner}/{repo}/commits?sha=main"                 # list commits (query string, not -f)
tea api --method DELETE /repos/{owner}/{repo}/topics/old-topic   # delete topic
tea api --method POST /repos/{owner}/{repo}/issues/42/comments -d '{"body":"Looks good"}'
```

`-f` / `--field` is a JSON **body** field and forces POST unless `-X` is set. Put GET filters in the URL query string.

`{owner}` and `{repo}` are auto-replaced from git context. For full API reference, consult `references/workflows.md`.

### Admin Operations

```bash
tea admin users ls                         # list all users (admin only)
tea admin users create --username bob --email bob@example.com --password-stdin
tea admin users edit bob --admin
tea admin users delete bob --confirm
```

## Examples

### Example 1: Bug report workflow

User says: "Create a bug report for the login timeout issue and assign it to alice"

```bash
tea issues create --title "Bug: Login times out after 30s on slow connections" \
  --description "## Steps to reproduce\n1. Connect via slow network\n2. Attempt login\n3. Observe timeout after 30s\n\n## Expected\nGraceful retry or extended timeout\n\n## Actual\nConnection dropped with no error message" \
  --labels bug \
  --assignees alice
```

### Example 2: Release workflow

User says: "Tag and release v2.1.0 with the changelog"

```bash
tea releases create --tag v2.1.0 --title "v2.1.0" --note-file CHANGELOG.md --target main
```

### Example 3: PR review and merge

User says: "Check PR 27 and squash merge it if it looks good"

```bash
tea pulls 27 --output json                 # inspect PR details
tea pulls approve 27                       # approve
tea pulls merge 27 --style squash          # squash merge
```

### Example 4: Fork contribution workflow

User says: "Fork the gitea/docs repo and create a PR for my typo fix"

```bash
tea repos fork --repo gitea/docs
tea clone yourusername/docs
cd docs
git checkout -b fix-typo
# ... user makes changes ...
git add -A && git commit -m "Fix typo in installation guide"
git push origin fix-typo
tea pulls create --title "Fix typo in installation guide" --base main --head yourusername:fix-typo --repo gitea/docs
```

## Troubleshooting

### Error: "No login configured"

**Cause:** No Gitea instance registered with tea.
**Solution:** Run `tea logins add` or see `references/authentication.md` for setup options including token, OAuth, and SSH authentication.

### Error: "Repository not found" or wrong repo detected

**Cause:** Git remote doesn't point to a known Gitea login, or repo slug is wrong.
**Solution:**
1. Check remotes: `git remote -v`
2. Specify explicitly: `tea issues ls --repo owner/repo --login mylogin`
3. Verify login URL matches remote: `tea logins ls`

### Error: "401 Unauthorized" or "403 Forbidden"

**Cause:** Token expired, insufficient scopes, or wrong login.
**Solution:**
1. Check token validity: `tea whoami`
2. Regenerate token with required scopes in Gitea web UI
3. Update login: `tea logins edit`

### Error: "Connection refused"

**Cause:** Gitea server unreachable.
**Solution:**
1. Verify server URL: `tea logins ls`
2. Check network/VPN connectivity
3. For self-signed TLS: `tea logins add --insecure`

### Error: "No help topic for 'orgs'" / "flag provided but not defined"

**Cause:** Stale command form. Common traps: `tea orgs` (use `tea org`), `tea pulls ls --labels` (use `tea issues ls --kind pulls --labels`), `tea repos delete --repo` (use `--owner` and `--name`), `tea repos fork owner/repo` (use `--repo owner/repo`).
**Solution:** Re-read the matching section above or `references/tea-commands.md`.

### Commands hang or return empty

**Cause:** API rate limiting or large result sets.
**Solution:** Use `--limit` and `--page` for pagination:
```bash
tea issues ls --limit 10 --page 1
```

## Additional References

For detailed information, consult these bundled reference files:

- `references/authentication.md` - Login setup, token scopes, multi-instance management, environment variables
- `references/tea-commands.md` - Complete flag and option reference for every tea subcommand
- `references/workflows.md` - Advanced multi-step workflows, tea api patterns, bulk operations
