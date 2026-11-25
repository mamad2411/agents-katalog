---
name: ps
description: Check parallel session status - shows worktrees, git branches, PR readiness, and recommended merge order
allowed-tools: Bash, Read
---

# Parallel Session Status

Check the status of all parallel work sessions (worktrees, branches, PRs).

## Instructions

### Step 1: Run the Status Script

If `scripts/parallel-session-status.sh` exists, use it:

```bash
# Run the automated status script
./scripts/parallel-session-status.sh

# Or specify a session name
./scripts/parallel-session-status.sh my-session-name
```

If the script doesn't exist, gather the data manually with Steps 2-5 below.

### Step 2: Discover Worktrees

```bash
# List all worktrees
git worktree list

# Get project name for pattern matching
PROJECT_NAME=$(basename $(git rev-parse --show-toplevel))
```

### Step 3: Check Each Worktree Status

```bash
# For each worktree, gather status
for wt in $(git worktree list --porcelain | grep "^worktree" | cut -d' ' -f2); do
    echo "=== $(basename $wt) ==="

    # Branch name
    git -C "$wt" branch --show-current

    # Uncommitted changes
    git -C "$wt" status --short | head -5

    # Unpushed commits
    git -C "$wt" log @{u}..HEAD --oneline 2>/dev/null || echo "(no upstream)"

    # Last commit
    git -C "$wt" log -1 --format="%ar: %s"
done
```

### Step 4: Check PR Status

```bash
# List open PRs
gh pr list --state open --json number,title,headRefName,statusCheckRollup \
  --jq '.[] | "\(.number) | \(.headRefName) | \(.title)"'
```

### Step 5: Check tmux Sessions (if using tmux)

```bash
# List tmux sessions
tmux list-sessions 2>/dev/null || echo "No tmux sessions"

# List panes in work session
tmux list-panes -t "${PROJECT_NAME}-parallel" -F "#{pane_index}: #{pane_current_path} (#{pane_current_command})" 2>/dev/null || true
```

### Step 6: Generate Status Report

Present the results in this format:

```markdown
## Parallel Session Status

**Project**: {PROJECT_NAME}
**Timestamp**: YYYY-MM-DD HH:MM

### Active Worktrees

| Worktree | Branch | Status | Last Commit |
|----------|--------|--------|-------------|
| ../project-backend | feat/backend-api | Clean | 5 min ago: "feat: add endpoint" |
| ../project-frontend | feat/frontend-ui | 2 files | 12 min ago: "wip: dashboard" |

### Open PRs

| PR | Branch | Title | CI |
|----|--------|-------|-----|
| #42 | feat/backend-api | Add user management | pass |

### PR Readiness

| Branch | Uncommitted | Unpushed | Tests | Lint | Ready? |
|--------|-------------|----------|-------|------|--------|
| feat/backend-api | 0 | 0 | Pass | Pass | Ready |
| feat/frontend-ui | 2 | 3 | Pass | Pass | Push needed |

### Recommended Merge Order

Derive from branch name patterns:

1. **infra/terraform/ci/cd branches** - No dependencies, provisions resources
2. **deploy/ecs/k8s branches** - Depends on infra
3. **backend/api/server branches** - Depends on infra
4. **frontend/worker/service branches** - Depends on backend
5. **docs/staff branches** - Staff Engineer, merge last

### Action Items

- [ ] Push unpushed commits in `feat/frontend-ui`
- [ ] Create PR for `feat/backend-api`
```

---

## Inter-Agent Status File

The status script writes a machine-readable JSON file at `${TMPDIR:-/tmp}/{PROJECT_NAME}-agent-status.json`:

```json
{
  "session": "project-parallel",
  "updated_at": "2026-01-15T12:00:00Z",
  "agents": [
    {"pane": 0, "name": "project-backend", "branch": "feat/backend-api", "state": "working", "last_commit": "feat: add endpoint"}
  ]
}
```

Agents can read this file to see what other agents are doing.

---

## PR Readiness Criteria

A branch is ready for PR when:

| Criterion | Check |
|-----------|-------|
| No uncommitted changes | `git status --short` is empty |
| All commits pushed | `git log @{u}..HEAD` is empty |
| Tests pass | `pytest` or `npm test` succeeds |
| Lint passes | `ruff check .` or `eslint .` succeeds |
| No WIP commits | No "wip:" commit messages |

---

## Merge Order Guidelines

The status script derives merge order dynamically from branch name patterns. Customize the priority mapping in `scripts/parallel-session-status.sh` function `get_merge_priority()`:

| Priority | Branch Pattern | Description |
|----------|---------------|-------------|
| 1 | `*infra*`, `*terraform*`, `*ci*` | Infrastructure first |
| 2 | `*deploy*`, `*ecs*`, `*k8s*` | Deployment configs |
| 3 | `*backend*`, `*api*`, `*server*` | Backend/API |
| 4 | `*frontend*`, `*worker*`, `*service*` | Services/frontend |
| 5 | `*docs*`, `*staff*` | Documentation last |

---

## Related Skills

- `/work` - Launch parallel sessions
- `/progress` - Overall project progress
- `/pr-check` - Validate single branch PR readiness
