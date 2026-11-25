---
name: pr
description: "Create a pull request with full git hygiene. Use after completing any code change. Enforces: correct git identity, builds pass, all files staged, feature branch, PR created via gh. Triggers on: /pr, create PR, open PR, push and PR, ship this."
user-invocable: true
---

# PR Workflow

Enforce complete git hygiene before opening any PR. Never skip a step.

---

## Steps (execute in order, stop and fix before continuing)

### 1. Verify git identity
```bash
git config user.name
git config user.email
```
Must match the identity you intend to commit as. If wrong:
```bash
git config user.name "<your-github-username>"
git config user.email "<your-email>"
```

### 2. Check what's changed
```bash
git status
git diff --stat
```
List every modified file. Do NOT skip unstaged files.

### 3. Run the build
Run the project's build command (check package.json scripts, Makefile, or CI config):
- Node projects: `npm run build` (or the project's equivalent)
- Python: `python3 -m py_compile <entrypoint>` or the project's test/lint command
- TypeScript: `npx tsc --noEmit` at minimum

Fix any errors before continuing. Do not open a PR with a broken build.

### 4. Stage ALL changed files
```bash
git add <every modified file by name>
```
Never use `git add -A` or `git add .` (risk of committing secrets or binaries).
Double-check with `git status` — nothing should show as unstaged.

### 5. Create a feature branch if not already on one
```bash
git checkout -b <descriptive-branch-name>
```
Never commit directly to `main`. Branch names: `feat/`, `fix/`, `chore/`.

### 6. Commit
```bash
git commit -m "<type>(<scope>): <description>"
```
Follow conventional commits. No `--no-verify`.

### 7. Push
```bash
git push -u origin <branch>
```
Verify the remote is the correct account (`gh repo view` to confirm).

### 8. Create PR
```bash
gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
- <bullet points of what changed>

## Test plan
- <what to verify>

🤖 Generated with Claude Code
EOF
)"
```

### 9. Return the PR URL
Share the PR link with the user so they can review before merging.

---

## Rules
- NEVER merge or deploy without user approval
- NEVER use `--force` push to main
- NEVER skip the build check — a broken build is worse than no PR
- If pre-commit hook fails, fix the issue and create a NEW commit (never `--amend`)
