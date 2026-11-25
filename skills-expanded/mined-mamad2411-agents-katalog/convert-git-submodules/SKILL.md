---
name: convert-git-submodules
argument-hint: "[directory]"
description: Convert a repo directory into a git submodule: create a remote repo, push content, then add it back.
related:
  - create-github
  - git-commit
  - git-push
  - list-git
  - delete
  - update-references
  - update-gitignore
  - deep-validate
  - ship
  - suggest-next-action
  - ask-me

---

## Goal

Convert a directory inside a parent repository into a git submodule by creating a new remote repo and cloning it back as a submodule, covering history preservation, push, add, and validate.

## Scope

Use when a repo directory has grown too large, needs to be split into its own repo, or you want to use a submodule.

## Execute

### 1. Identify Directory

> Goal: Identify the directory to convert

1. Take the directory path from the user; if unclear → run `/ask-me`
2. Check that the directory is inside the parent repo and actually contains files
3. Confirm the directory isn't already a submodule
4. Check that the directory has no important uncommitted changes
5. Locate the parent repo root with `git rev-parse --show-toplevel`

### 2. Prepare Remote Repo

> Goal: Have a remote repo for the directory

1. Check whether a remote repo already exists
2. If not → use `/create-github-repo` or `gh repo create <repo-name>`
3. Pick a repo name that conveys the directory's purpose
4. Save the remote URL for the next steps
5. If a repo already exists → confirm it's empty or use a new branch

### 3. Backup And Extract History

> Goal: Preserve the directory's history before splitting

1. In the parent repo → check `git status` shows a clean working tree
2. Record the current commit hash: `git rev-parse HEAD`
3. Review the directory's git history: `git log --oneline -- <directory>`
4. To preserve history → use `git subtree split --prefix=<directory> -b <branch>`
5. If you don't need history → skip ahead to step 4

### 4. Convert To Repo And Push

> Goal: Turn the directory into a repo and push

1. Temporarily move the directory outside the parent repo, e.g. `$env:TEMP/<name>`, or use the branch from `subtree split`
2. Run `git init` in that directory
3. Run `git add .` then `git commit -m "initial commit from <parent>"`
4. Run `git remote add origin <remote-url>`
5. Run `git push -u origin main` or use `/git-push`
6. Delete the temp directory after a successful push

### 5. Remove From Parent

> Goal: Remove the old directory from the parent repo

1. Remove the old directory from the parent repo: `git rm -r <path>`
2. Update `.gitignore` if needed (run `/update-gitignore`)
3. Run `/update-references` if other files referenced the old path
4. Run `git commit -m "remove <directory> before adding as submodule"`

### 6. Add As Submodule

> Goal: Replace the original directory with the submodule

1. Run `git submodule add <remote-url> <path>`
2. Run `git submodule update --init --recursive`
3. Check that `.gitmodules` was created correctly
4. Check that the submodule was cloned: `git submodule status`
5. Run `git add .gitmodules <path>`
6. Run `git status` to verify

### 7. Commit And Push Parent

> Goal: Save the changes

1. Run `/git-commit`
2. Run `/ship` if you want to push
3. Confirm there are no broken references after the removal

### 8. Validate And Finalize

> Goal: Verify the submodule works

1. Test a fresh clone: `git clone --recurse-submodules <parent-url>` in `$env:TEMP`
2. Check that the submodule content is complete
3. Run `/deep-validate` to check references and structure
4. Run `/suggest-next-action` to recommend the next step

## Rules

### 1. Safety

- Do a dry run or backup before removing the directory
- Check `git status` is clean before starting
- Save the commit hash before starting so you can roll back
- If any step fails → roll back with `git reset --hard <hash>`
- Ask first if there are uncommitted/unpushed changes
- Never delete the parent repo's history

### 2. Preserve History

- To keep history → use `git filter-repo` or `git subtree split` first
- If you don't need it → create a fresh initial commit
- State the choice in the commit message: preserved or fresh history

### 3. Remote Required

- A remote repo must exist before adding the submodule
- Confirm push access first
- Use an SSH URL if you have an SSH key, an HTTPS URL otherwise

### 4. Submodule Management

- Use `git submodule add`, not manual edits to `.gitmodules`
- Check `git submodule status` after adding
- To remove the submodule later → use `/delete-git-submodules`

### 5. Clean Working Tree

- The parent repo must be clean before starting
- The submodule must clone successfully before committing
- Use `$env:TEMP` for the temp directory; don't create it inside the project
- Delete the temp directory after a successful push
- Never commit temp files into the repo

- Use /git-commit-and-push if needed
- Use /list-git-submodules if needed

## Expected Outcome

- The directory becomes a git submodule
- The new remote repo holds the complete content, with history if requested
- `.gitmodules` is updated
- `git submodule status` shows the submodule pointing to the correct commit
- A fresh clone with `--recurse-submodules` works
- No broken references after the conversion
- Every change passes `/deep-validate` and `/ship`
