# New From Template

## Role
You are a Project Scaffolding Orchestrator who creates a new GitHub repository
from a template, clones it locally, and renames all template references to the
new project name — reporting results and next steps to chat.

## Instructions

### Step 1: Resolve Inputs

Accept an optional `--private` or `--public` flag (default: `--private`).

**One argument provided (`NEW-REPO-NAME` only):**
Auto-detect the template repo from the current directory:
- Run `gh repo view --json nameWithOwner -q .nameWithOwner`
- If this fails (not a GitHub repo, no remote), stop and output:
  `Could not detect a GitHub repo in the current directory. Pass owner/template-repo explicitly.`

**Two arguments provided (`OWNER/TEMPLATE-REPO` and `NEW-REPO-NAME`):**
Use the first argument as the template repo.

Validate:
- `OWNER/TEMPLATE-REPO` — must match `owner/repo` pattern (two segments, each
  containing only letters, digits, hyphens, underscores, or dots).
- `NEW-REPO-NAME` — must contain only letters, digits, hyphens, underscores,
  or dots (no spaces, no slashes).

If either is invalid, stop and output the specific format error before proceeding.

### Step 2: Create Remote Repo

Run:
```
gh repo create NEW-REPO-NAME --template OWNER/TEMPLATE-REPO --private
```
(substitute `--public` if specified)

On failure:
- HTTP 404 → `Template OWNER/TEMPLATE-REPO not found. Check the name and your access.`
- Name conflict → `A repo named NEW-REPO-NAME already exists in your account.`
- Other → print the raw gh error and stop.

Report: `Remote repo created: https://github.com/YOUR-LOGIN/NEW-REPO-NAME`

### Step 3: Clone With Retry

Resolve YOUR-LOGIN via `gh api user -q .login`.

Run `gh repo clone YOUR-LOGIN/NEW-REPO-NAME` — this uses the existing gh
authentication and avoids HTTPS credential issues.

If clone fails, wait 3 seconds and retry — up to 3 attempts total.

If all 3 attempts fail:
```
Clone failed after 3 attempts. The remote repo was created successfully at:
  https://github.com/YOUR-LOGIN/NEW-REPO-NAME
Run manually: gh repo clone YOUR-LOGIN/NEW-REPO-NAME
```
Stop. Do not continue to cleanup.

After a successful clone, `cd` into the new directory before proceeding.

### Step 4: Detect Template Name

Read `.claude/template-source` in the cloned directory.

- If found: use its trimmed content as TEMPLATE-NAME.
  Report: `Detected template name: TEMPLATE-NAME → new project: NEW-REPO-NAME`
- If missing: output:
  ```
  .claude/template-source not found in the cloned repo.
  Remote repo exists: https://github.com/YOUR-LOGIN/NEW-REPO-NAME
  What is the source template name? (the name used in this template's files)
  ```
  Wait for the user's answer before continuing.

### Step 5: Scan for References

# Inline of cleanup-template logic — keep in sync with
# .claude/plugins/global/skills/cleanup-template/SKILL.md

Search the cloned directory for all occurrences of TEMPLATE-NAME (exclude `.git/`):
- output_mode: content
- show file path, line number, matching line

Build a replacement table:

| File | Line | Current text | Proposed text |
|------|------|--------------|---------------|
| ...  | ...  | ...TEMPLATE-NAME... | ...NEW-REPO-NAME... |

If zero occurrences found: output `No template references found — nothing to replace.`
and skip to Step 7.

### Step 6: Confirm and Apply

Show the table and ask:
> "Found [N] occurrence(s) in [M] file(s). Shall I replace all of them with
> `NEW-REPO-NAME`?"

Do not proceed until the user confirms.

Read all matched files in parallel, then for each apply Edit with
`replace_all: true`, `old_string: "TEMPLATE-NAME"`, `new_string: "NEW-REPO-NAME"`.

Overwrite `.claude/template-source` with `NEW-REPO-NAME` using Write.

### Step 7: Report Summary

Output:
```
Done. New project scaffolded from OWNER/TEMPLATE-REPO.

Remote: https://github.com/YOUR-LOGIN/NEW-REPO-NAME
Local:  ./NEW-REPO-NAME/

Replaced TEMPLATE-NAME → NEW-REPO-NAME in [N] file(s):
  - file1 ([k] occurrence(s))
  - file2 ([k] occurrence(s))

.claude/template-source updated to NEW-REPO-NAME.
Run /git-commit to commit the cleanup changes.
```

## Safety Rules

1. **Never commit or push** — this skill edits files only; always direct the
   user to `/git-commit` for the final step.
2. **Never modify source template repo** — all edits apply exclusively to the
   newly cloned directory.
3. **Never apply replacements** without first showing the replacement table
   and receiving explicit user confirmation in Step 6.
4. **If clone fails after all retries**, surface the orphaned remote repo URL
   and stop — never silently abandon a created remote repo.

## Examples

**User:** `/new-from-template my-new-api`
(running in a session on `bben15600-sys/service-template`)

**Agent behaviour:** Detects `bben15600-sys/service-template` from the current git
remote, creates `my-new-api` as a private repo from it, clones with retry
logic, reads `.claude/template-source` (finds `service-template`), shows
replacement table for 8 occurrences in 5 files, waits for confirmation,
applies all edits, and directs user to `/git-commit`.

**User:** `/new-from-template bben15600-sys/service-template my-new-api`
(running from any session, not on the template repo)

**Agent behaviour:** Skips auto-detection, uses `bben15600-sys/service-template`
directly, then follows the same flow. If clone fails all 3 retries, outputs
the remote URL with `gh repo clone bben15600-sys/my-new-api` as the recovery command.
