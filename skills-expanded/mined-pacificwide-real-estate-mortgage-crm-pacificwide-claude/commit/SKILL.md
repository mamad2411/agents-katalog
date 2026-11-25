---
name: commit
description: "Pre-commit checks + commit + PR + Notion update. Runs lint/test, creates conventional commit, auto-creates PR, updates ticket. Use after /review passes."
---

# /commit - Commit & PR

Create a commit with proper checks, push, auto-create PR, and update Notion ticket status.

**Input:** Optional commit message via `$ARGUMENTS`, otherwise auto-generate

## Workflow

### Step 1: Verify review completed

**Check if /review was run:**
- If the previous conversation turn contains "Code Review Complete" with verdict "READY TO COMMIT", proceed
- Otherwise, ask user: "Did you run /review? I don't see a recent review output. Run /review first or confirm you want to commit without review."

**IMPORTANT:** Never commit code that hasn't been reviewed unless explicitly confirmed by user.

---

### Step 2: Verify branch safety

Check current branch:
```bash
git rev-parse --abbrev-ref HEAD
```

- **If on `master` or `main`:** STOP. Print error:
  ```
  ERROR: Cannot commit directly to master branch.
  Create a feature branch first: git checkout -b type/description
  ```
- **If on feature/fix/hotfix branch:** Proceed to verification.

---

### Step 3: Pre-commit verification

**If you just ran `/review` and verdict was "READY TO COMMIT":** Skip verification and proceed to Step 4.

**If running `/commit` standalone** (without `/review` first), verify:

Run build/lint/test commands from `.claude/rules/stack-rules.md`. Typical:
- Lint: `npm run lint:fix`
- Build: `npm run build`
- Test: `npm test`

- ALL must pass before proceeding
- If any fail: STOP and report. Run `/review` first to diagnose and fix issues.

---

### Step 4: Sync plan file

If a plan file exists in `plans/`:
1. Read the plan file
2. Mark all implemented items as complete: change `[ ]` to `[x]` for tasks that were completed
3. Keep any TODOs added by `/review` as `[ ]` (these are future work)
4. Save the updated plan file

If no plan file exists, skip this step.

---

### Step 5: Stage changes

Review all changes:
```bash
git status          # See all modified/new files
git diff            # Review unstaged content
```

Determine what belongs in THIS commit:
- **Include:** Files directly related to the commit message you'll write
- **Include:** Tests for the changed code
- **Include:** Updated DTOs/entities/migrations if schema changed
- **Include:** Plan file (if exists and was updated in Step 4)
- **Exclude:** `.env` files, credentials, `node_modules/`
- **Exclude:** Unrelated changes (typo fixes, debug logs, commented code)
- **Exclude:** WIP changes for different feature

Stage files one by one:
```bash
git add src/deal/deal-commission.service.ts
git add src/deal/dtos/commission-calculation.dto.ts
git add src/deal/deal-commission.spec.ts
git add plans/commission-calculation.md
# etc. - one file per line
```

Verify staged changes match commit intent:
```bash
git diff --cached   # Should only show changes for ONE logical change
```

If you have unrelated changes, stash them for later:
```bash
git stash push -m "WIP: other feature" -- path/to/unrelated-file.ts
```

---

### Step 6: Create commit message

**If `$ARGUMENTS` provided:** Use it as the commit message (validate it follows conventional format).

**If no `$ARGUMENTS`:** Analyze staged changes to generate message:
1. Read `git diff --cached --name-only` to see affected files
2. If plan file exists, read "## Context" section for feature description
3. Determine commit type from changes:
   - New files in `src/`: `feat`
   - Modified files fixing bugs: `fix`
   - Only test files: `test`
   - Only docs: `docs`
   - Refactoring: `refactor`
4. Determine scope from module path (e.g., `src/deal/` → scope is `deal`)
5. Write concise description (under 72 chars) describing WHAT changed, not HOW

Validate message:
- Format: `type(scope): description`
- Types: feat, fix, docs, refactor, test, ci, chore, perf
- Subject under 72 characters
- Imperative mood ("add" not "added", "fix" not "fixed")

**Hotfix tag:** If on a `hotfix/` branch, prefix with `[hotfix]`:
- `[hotfix] fix(auth): patch token expiry vulnerability`

Create commit:
```bash
git commit -m "$(cat <<'EOF'
feat(deal): add commission calculation for team leads
EOF
)"
```

---

### Step 7: Push and create PR

**Push to remote:**
```bash
# If branch doesn't track remote yet (first push)
git push -u origin $(git rev-parse --abbrev-ref HEAD)

# If branch already tracks remote
git push origin $(git rev-parse --abbrev-ref HEAD)
```

**Auto-create PR via `gh`:**

Determine PR details:
1. **Title:** Use commit message subject (without type prefix for readability), or plan title
2. **Base branch:** Read from `.claude/rules/stack-rules.md` → `## Git → Base branch`. Default: `dev`
3. **Body:** Use PR template below — match team PR format
4. **Labels:** Add based on branch prefix:
   - `feature/` → no special label
   - `fix/` → `bug`
   - `hotfix/` → `bug`, `hotfix`

```bash
gh pr create --title "PR title" --body "$(cat <<'EOF'
## What changed
- [1-3 bullet points of what changed]

## Why
- Ticket: [Notion ticket link if available]

## Type
- [ ] Feature
- [ ] Bug fix
- [ ] Refactor
- [ ] Chore

## Testing
- [ ] Unit tests pass
- [ ] Build succeeds
- [ ] Manual testing done

## Screenshots / Video (required for bug fixes)
Before | After

## Checklist
- [ ] No console.log or debug code left
- [ ] No hardcoded secrets or API keys
- [ ] Conventional commit format used
- [ ] PR link added to Notion ticket
EOF
)" --base dev --reviewer t-code4change
```

> **Note for bug fix PRs:** Remind the user to attach screenshot/video proof to the PR comment after creation (required by team policy).

**If PR already exists** (e.g., additional commits on same branch):
```bash
# Just push — PR updates automatically
git push origin $(git rev-parse --abbrev-ref HEAD)
```

Check if PR exists before creating:
```bash
gh pr view --json number 2>/dev/null
```

**Hotfix PR:** Add `[HOTFIX]` prefix to title and request expedited review:
```bash
gh pr create --title "[HOTFIX] Fix token expiry vulnerability" --body "..." --label "hotfix,bug" --reviewer t-code4change
```

---

### Step 8: Update Notion ticket

**Find the Notion ticket** using this priority:
1. **Notion URL in plan file** — look for `https://notion.so/...` or `https://*.notion.site/...` in the `**Ticket:**` field
2. **Ticket ID in plan file** — if only an ID like `CRM-1279` or `RRR-351` is found, use Notion MCP `notion-search` to find it: `query: "CRM-1279"`, then pick the matching result
3. **Ticket ID in branch name** — if plan has no ticket info, extract ID from branch name (e.g., `fix/CRM-1279-slug` → `CRM-1279`) and search Notion
4. **Skip** — if no ticket ID or URL found anywhere, skip this step

**Always (if ticket exists):**
1. Append PR URL to the **`PR Links`** property (rich text field — new line per PR, do not overwrite existing content):
   ```
   {stack}: {pr_url}
   ```
2. Add commit comment:
   ```
   ✅ {stack} committed: {short_hash}
   Branch: {branch_name}
   PR: {pr_url}
   ```

**Single-stack task** (ticket has only `BE Status` OR only `FE Status`):
- Update main `Status` → **"Ready To Review"**
- Update the stack-specific status field → **"Ready To Review"**

**Cross-stack task** (ticket has BOTH `BE Status` AND `FE Status`):
- Update only current stack's field (BE commits → `BE Status` → "Ready To Review")
- **Do NOT update main `Status`** until all stacks are done
- Check if the OTHER stack's status is already "Ready To Review":
  - **Yes** (last stack): update main `Status` → **"Ready To Review"**
  - **No** (more stacks pending): add comment only:
    ```
    ✅ {stack} committed: {short_hash}
    PR: {pr_url}
    ⏳ Waiting for: {other_stack}
    ```

If no ticket ID or URL found anywhere, skip this step.

---

### Step 9: Handoff

**Single-stack task:**
```markdown
## Commit & PR Complete

**Branch:** [branch-name]
**Commit:** [commit hash and message]
**PR:** [PR URL]
**Notion:** [Updated ticket / No ticket / Update failed]

Done! PR is ready for team review.
```

**Cross-stack task (more stacks to go):**
```markdown
## Commit & PR Complete ({stack})

**Branch:** [branch-name]
**Commit:** [commit hash and message]
**PR:** [PR URL]
**Notion:** Posted stack completion. Waiting for: {remaining_stacks}

Cross-stack next step:
Switch to {next_stack} repo and run: /plan [same ticket URL]
(or /fix [same ticket URL] for bug fixes)
```

**Cross-stack task (this is the last stack):**
```markdown
## Commit & PR Complete ({stack}) — All stacks done!

**Branch:** [branch-name]
**Commit:** [commit hash and message]
**PR:** [PR URL]
**Notion:** Updated status to Review. All stacks committed.

All PRs ready for team review:
- BE: [PR URL from Notion comment]
- FE: [PR URL from Notion comment]
```

---

## Rules

- NEVER commit if lint, build, or tests fail
- NEVER commit `.env` files, API keys, database credentials, or secrets
- NEVER use `git add .` or `git add -A` - add specific files
- NEVER commit directly to `master` or `main` branch
- Do NOT include Co-Authored-By or AI references in commits
- ALWAYS push and create PR (don't ask — this is the standard workflow)
- One commit per logical change, not one giant commit
- Keep commits focused on actual code changes (no unrelated formatting/refactors unless that's the commit's purpose)
- **Cross-stack:** Post stack completion to Notion so other stacks know progress
- **Hotfix PRs:** Add `[HOTFIX]` prefix and `hotfix` label for visibility
- Follow `.claude/rules/development-rules.md` for git conventions
