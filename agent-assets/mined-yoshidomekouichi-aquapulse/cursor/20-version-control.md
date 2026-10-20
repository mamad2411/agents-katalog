---
description: Version Control - Git/PR Strategy and Task Splitting
alwaysApply: true
metadata:
  environments: cloud
---

# Version Control Rules

Integrated rules for Git workflow, PR strategy, and task splitting.

## 1. Git Workflow (GitHub Flow)

### Branch Strategy

```
main (always deployable)
  ├─ cursor/feature-a-0d1c → PR → Merge
  └─ cursor/feature-b-0d1c → PR → Merge

Branch naming convention:
  cursor/<descriptive-name>-0d1c

Examples:
  cursor/esp32-sensor-integration-0d1c
  cursor/fix-grafana-dashboard-0d1c
```

### Basic Flow

```bash
# 1. Start task
git checkout main
git pull origin main
git checkout -b cursor/<name>-0d1c

# 2. Implement
# ...

# 3. Commit
git add <files>
git commit -m "feat(scope): description"

# 4. Push
git push -u origin cursor/<name>-0d1c

# 5. Check PR status (important)
gh pr list --head cursor/<name>-0d1c

# 6. Create PR
gh pr create --title "..." --body "..." --draft

# 7. After merge
git checkout main
git pull origin main
git branch -d cursor/<name>-0d1c
```

### Prohibitions

```
1. Direct push to main
2. Force push to main
3. Skipping PRs
4. Branch naming rule violations
5. Reusing merged branches
6. Skipping PR status check
```

## 2. PR Strategy

### PR Size Constraints

```
Recommended size:
  - 200-400 lines of changes
  - ≤ 5-10 files
  - Review time: ≤ 15-20 minutes

When exceeded:
  - Stop implementation
  - Split into next PR
  - Re-propose split plan

Rationale (MSR 2026 research):
  - Small PRs (<300 lines) have higher merge rates
  - CI failure lowers merge probability by 15%
  - AI PRs are 51% larger on average, more likely abandoned
```

### 1 PR = 1 Logical Change

```
Each PR should contain only one of:
  - New feature
  - Bug fix
  - Refactoring
  - Documentation update
  - Test addition

Don't mix:
  - Refactoring + New feature
  - Format fix + Logic change
  - Documentation + Implementation
```

### Vertical Slicing

```
Plan split before writing code:

Receive task
  ↓
Analyze dependencies
  ↓
Propose split plan (each PR: 200-400 lines)
  ↓
User approval
  ↓
Implement per PR
```

## 3. Dependency Judgment

### Technical Dependencies (Stacked PR Required)

```
Example 1: Database schema change
  PR 1: Add email column to users table
  PR 2: Authentication feature using email
  
  → PR 2 cannot work without PR 1
  → Stacked PR

Example 2: API removal
  PR 1: Add new endpoint
  PR 2: Remove old endpoint
  
  → Gradual migration needed
  → Stacked PR
```

### Logical Dependencies (Parallel PRs Possible)

```
Example: User management feature

Loosely coupled design:
  PR 1: Define User interface
  PR 2: Implement UserService (use mocks)
  PR 3: Implement UserController (use mocks)
  PR 4: Integration (connect all)
  
  → PRs 1-3 can be reviewed in parallel
```

### Judgment Criteria

```
Technical dependency exists → Stacked PR
Only logical dependency → Consider loose coupling
Loose coupling unnatural → Stacked PR

Don't force separation
```

## 4. Stacked PRs

### Structure

```
main
 ├─ PR 1: Foundation (base: main)
     └─ PR 2: Feature A (base: PR 1's branch)
         └─ PR 3: Feature B (base: PR 2's branch)

Merge order: PR 1 → PR 2 → PR 3 (from root)
```

### Merge Flow

```
Step 1: Review & merge PR 1
  main ← PR 1
  
Step 2: Change PR 2's base
  gh pr edit <PR 2 number> --base main
  
  Reason: PR 1's branch no longer exists
  
Step 3: Review & merge PR 2
  main ← PR 2
  
(Repeat)
```

## 5. Commit Conventions

### Conventional Commits

```
<type>(<scope>): <subject>

<body> (optional)

<footer> (optional)

Type:
  feat: new feature
  fix: bug fix
  docs: documentation
  refactor: refactoring
  test: add tests
  chore: build/config

English preferred, Japanese acceptable
```

## 6. Pre-PR Conflict Check (Mandatory)

Always check for conflicts before creating PR:

```bash
# After completing work on branch, before creating PR

# 1. Fetch latest main
git fetch origin main

# 2. Dry-run merge test
git merge origin/main --no-commit --no-ff

# 3. Check results
# No conflict → git merge --abort → Create PR
# Conflict → Resolve → Commit → Create PR
```

**Detection:**
- If merge succeeds: No conflicts, safe to create PR
- If merge fails: Conflicts exist, must resolve first

**Action when conflicts detected:**
1. Resolve conflicts in editor
2. `git add <resolved-files>`
3. `git commit -m "fix: resolve merge conflicts with main"`
4. `git push origin <branch-name>`
5. Create PR

**Alternative: Rebase (if PR already created):**
```bash
git fetch origin main
git rebase origin/main

# If conflicts occur
git rebase --continue  # after resolving each conflict

git push -f origin <branch-name>
```

**Why mandatory:**
- Prevents wasted time on conflict resolution after PR creation
- Ensures PR is immediately reviewable
- Reduces context switching

**Example (PR #50):**
```
Problem: PR created from old main (f998d5c)
         PR #48, #49 merged to main (47448f5)
         GitHub detected conflicts

Solution: git rebase origin/main
          git push -f origin cursor/docs-phase3-tutorials-archive-0d1c
          PR automatically updated, conflicts resolved
```

---

## 7. Pre-PR Checklist

```
Required checks:
  - [ ] PR status checked with gh pr list --head <branch>
  - [ ] Branch name follows rules (cursor/*-0d1c)
  - [ ] Not reusing merged branch
  - [ ] Commit messages follow Conventional Commits
  - [ ] PR size ≤ 200-400 lines
  - [ ] 1 PR = 1 logical change
  - [ ] Can explain changes concisely
  - [ ] Related documentation updated
```

## 8. Pre-Operation Checks (Recurrence Prevention)

### Pre-Commit Check

```bash
# Always execute
git branch --show-current

# If on main branch
→ Abort commit
→ Report as Level 1 error immediately
→ Switch to correct feature branch
```

### Mandatory Git Operation Parameters (ADR-0003)

Explicitly specify `working_directory` for all Git operations:

```python
Shell(
  command="git checkout -b cursor/feature-0d1c",
  working_directory="/workspace"  # Required
)

Shell(
  command="git branch --show-current",
  working_directory="/workspace"  # Required
)
```

Reason:
- Avoid Shell tool state dependency
- Problem occurred in PR #40-42 (see ADR-0003)

Forbidden:
- Omitting working_directory
- Chaining with cd /workspace && (error-prone)

### Main Branch Error Detection and Response

```
Detection timing:
  - Immediately before git commit
  - Immediately before git push

On detection:
  1. Abort operation immediately
  2. Report to user (Level 1 error)
  3. Propose fix steps

Report template:
  "A problem occurred.
  
   Detected: Commit attempt to main branch
   Status: Commit not executed
   Action: Will create feature branch
   
   Next steps:
   1. git checkout -b cursor/<name>-0d1c
   2. Re-commit changes"
```

### Before Starting Work on Existing Branch

Always check PR status before resuming work on an existing branch:

```bash
# Check PR status for branch
gh pr list --head <branch-name>

# If empty output → No open PR exists
#   → Check if PR was merged
#   → If merged: DO NOT reuse branch, create new branch instead

# If PR exists and is open → Safe to continue
```

Detection:
  - Empty output from `gh pr list --head <branch-name>`
  - Indicates branch has no open PR (possibly merged)
  
Action when merged PR branch detected:
  1. Stop work immediately
  2. Report to user (Level 1 error)
  3. Propose creating new branch

Report template:
  "Problem detected.
   
   Detected: Working on merged PR's branch
   Branch: <branch-name> was used for merged PR #XX
   Status: Branch should not be reused
   Action: Create new branch cursor/<name>-0d1c
   
   Next steps:
   1. git checkout main
   2. git pull origin main
   3. git checkout -b cursor/<new-name>-0d1c
   4. Apply changes to new branch"

Root principle: "Structurally prevent" merged branch reuse

### PR Creation Failure Diagnostic Flow

```
Failure pattern 1: "No open PR found"
  Cause: PR already merged or doesn't exist
  Action: Create new PR

Failure pattern 2: "GraphQL: Resource not accessible"
  Cause: gh CLI permission restriction
  Action: Use ManagePullRequest tool

Failure pattern 3: "aborted: you must first push"
  Cause: Branch doesn't exist on remote
  Action: git push -u origin <branch>

Tool selection criteria:
  PR creation: ManagePullRequest tool (preferred)
  PR update: ManagePullRequest tool
  PR check: gh pr list (fine)
  PR info: gh pr view (fine)
```

### Error Reporting Triggers (Auto-determined)

```
Level 1 (Always report immediately):
  - git commit attempt on main branch
  - git push attempt on main branch
  - force push to main attempt
  - 3rd failure of same operation

Level 2 (Report as appropriate):
  - 1st PR creation failure (report after diagnosis)
  - 2nd failure of same operation

Level 3 (No report needed):
  - Operation succeeded on 1st try
  - Read-only operation
```

### Implementation Example: Pre-Commit Auto-Check

```bash
# Check AI Agent executes internally
CURRENT_BRANCH=$(git branch --show-current)

if [ "$CURRENT_BRANCH" = "main" ]; then
  echo "ERROR: Direct commit to main branch prohibited"
  echo "Current branch: $CURRENT_BRANCH"
  echo ""
  echo "Action:"
  echo "1. git checkout -b cursor/<descriptive-name>-0d1c"
  echo "2. Re-commit changes"
  exit 1
fi

# Check OK → Execute commit
git commit -m "..."
```

### Learn from Past Examples

```
Example (2026-07-05):
  Problem: Direct commit to main branch
  Cause: Returned to main after creating feature branch
  Result: Cannot create PR (cannot PR from main to main)
  
  Recurrence prevention:
  1. Always git branch --show-current before commit
  2. If main detected, abort immediately & report
  3. PR creation prioritizes ManagePullRequest tool

Root principle:
  "Structurally prevent" not "be careful"
```

## 9. Utilizing Cursor Features

### /worktree (Parallel Tasks)

```bash
# For loosely coupled design
/worktree "Define interface"
/worktree "Implement service (use mocks)"
/worktree "Implement controller (use mocks)"

→ Each task becomes independent PR
```

### /babysit (PR Improvement Loop)

```bash
/babysit "Improve PR #XX until CI passes"

→ Auto-respond to review comments
→ Auto-fix CI failures
```

## 10. Practical Examples

### Good Example: Split with Vertical Slicing

```
Task: "Water temperature sensor integration"

Split plan:
  PR 1: DS18B20 data model (150 lines)
  PR 2: Sensor reading function (200 lines)
  PR 3: Error handling (180 lines)
  PR 4: Integration tests (220 lines)

Each PR independently reviewable
Total: 750 lines → Split into 4 small PRs
```

### Bad Example: One Giant PR

```
Task: "Water temperature sensor integration"

One PR:
  - Data model
  - Sensor reading
  - Error handling
  - Tests
  - Incidental refactoring
  - Incidental documentation update

Total: 1,200 lines, 15 files changed
→ Hard to review, likely abandoned
```

## 11. Emergency Response

```bash
# Create hotfix branch
git checkout -b cursor/hotfix-critical-issue-0d1c

# Minimal fix
# ...

# Create PR (clarify emergency)
gh pr create \
  --title "HOTFIX: Critical production issue" \
  --body "Immediate fix required." \
  --label "hotfix"

# Post-review required
```

Important: Don't skip PR even in emergency.

## 12. Purpose of These Rules

```
Quality assurance:
  - Early issue detection in PR review
  - Higher precision with small PRs

Traceability:
  - All changes recorded in PRs
  - Clear why changes were made

Safety:
  - Prevent main misoperations
  - Easy rollback

Professionalism:
  - Industry-standard workflow
  - Ready for team development
```

## References

- MSR 2026: "What 33,000 Agentic Pull Requests Reveal"
- GitHub Flow: https://docs.github.com/en/get-started/using-github/github-flow
- Conventional Commits: https://www.conventionalcommits.org/
