---
name: agy-drive
description: Drive a decomposed GitHub issue to completion using agy — a subagent orchestrates, running agy to implement each task, PR created per task with optional review. Usage: agy-drive <owner/repo> <issue-number> [--reviewer=agy]
---

Orchestrate autonomous implementation of a GitHub issue using `agy`. Each task
from the decomposed manifest runs as a separate `agy` invocation, gets its own PR,
and is reviewed + merged before the next task starts.

## Parse arguments

`$ARGUMENTS` format: `<owner/repo> <issue-number> [--reviewer=agy]`

Extract `REPO`, `ISSUE_NUM`, and optionally `REVIEWER` from `$ARGUMENTS`.
`SLUG` = owner + "-" + repo-name + "-issue-" + issue-number.
`PROMPT_DIR` = `~/.gemini/agy-prompts/$SLUG`.

## Check for manifest

If `$PROMPT_DIR/manifest.json` does not exist, tell the user:
"No decomposition found. Run the `issue-decompose` skill first."
Then stop.

## Spawn orchestrator subagent

Spawn a subagent (using `define_subagent` and `invoke_subagent` with a descriptive role like "Issue Orchestrator") with the full manifest contents and this orchestration prompt:

---
You are a task orchestrator. Drive each task in the manifest to completion.
Work through tasks in dependency order (respect `blockedBy`). Skip tasks
already `status: merged`. Update manifest status as you go.

**Repo path:** read from manifest `repoPath`.
**Repo remote:** `$REPO`
**Reviewer:** `$REVIEWER` (if specified, e.g. agy)
**Prompt dir:** `$PROMPT_DIR`
**Cool-down:** `sleep 900` between tasks (skip after the last task)

For each pending task:

### a. Sync main
```bash
cd <repoPath>
git checkout main && git pull --ff-only
git checkout -b <task.branch>
```

### b. Run agy
```bash
agy --dangerously-skip-permissions --print-timeout 30m \
  -p "$(cat $PROMPT_DIR/<task.id>.md)"
```

### c. Check output
Run `git diff --stat`. If no files changed:
- Re-run agy with this appended to the prompt:
  "IMPORTANT: Nothing was changed. You must implement the code now. Do not stop
   until the code is written, the build passes, and tests pass."

### d. Strip junk
Remove any `.py` patch scripts, `dev_output.log`, or `*.patch` files agy may
have left. Restore `package-lock.json` / `package.json` from main if modified:
```bash
git checkout main -- package-lock.json package.json 2>/dev/null || true
git checkout main -- frontend/package-lock.json frontend/package.json 2>/dev/null || true
```

### e. Verify build + tests
```bash
cd <repoPath>/frontend && npm run build && npm run test -- --run
cd <repoPath>/backend && npm test
```
Fix any small TypeScript or test errors inline. If errors are too large to fix,
note them in the PR body and proceed (do not block).

### f. Commit
```bash
git add -p   # or git add <specific changed files>
git commit -m "<conventional-commit title>

Closes #$ISSUE_NUM
Part of #<epic if applicable>

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

### g. Push + PR
```bash
git push -u origin <task.branch>
gh pr create --base main --head <task.branch> \
  --title "<task title>" \
  --body "$(cat <<'EOF'
## Summary
<bullet points from acceptance criteria>

## Test plan
- [x] Frontend build: clean
- [x] Unit tests: pass

Closes #$ISSUE_NUM

🤖 Generated with Claude Code
EOF
)"
```

### h. Review

**If reviewer = agy:**
```bash
agy --dangerously-skip-permissions --print-timeout 15m -p "
Review the changes on git branch <task.branch> in <repoPath>.
Read: git diff main...<task.branch>
Check every acceptance criterion in $PROMPT_DIR/<task.id>.md.
Run: cd frontend && npm run build && npm run test -- --run && cd ../backend && npm test
Fix any issues. If you made fixes: git add <files> && git commit --amend --no-edit && git push --force-with-lease.
Report what you found and fixed. Then stop.
"
```

### i. Wait for CI + merge
```bash
# Poll until CLEAN (GitGuardian usually fast)
for i in $(seq 1 10); do
  STATUS=$(gh pr view --json mergeStateStatus -q '.mergeStateStatus')
  if [ "$STATUS" = "CLEAN" ]; then break; fi
  sleep 15
done
gh pr merge --squash --delete-branch
```

### j. Update manifest + cool-down
Update `$PROMPT_DIR/manifest.json` task status to `"merged"`.
If more tasks remain: `sleep 900`.

---

After all tasks complete, print a summary table of task → PR number → status.
---

## After orchestrator returns

Report the final summary to the user.
