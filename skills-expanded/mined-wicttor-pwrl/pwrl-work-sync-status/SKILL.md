---
name: pwrl-work-sync-status
description: Synchronize task status with GitHub Issues when integration is enabled
argument-hint: "[Task file path, new status, summary message (optional)]"
---

# pwrl-work-sync-status — GitHub Issues Status Sync

## Interaction Method

- Use platform's `ask_user_question`, `ask_user`, `ask_user_input`, `vscode/askQuestions` or any available extension/tool for user interaction for all decisions
- Ask one question at a time
- Use multiple-choice questions when possible
- If input is empty, ask: "Should task statuses be synchronized with GitHub? Review pending synchronizations before confirming."
- Provide clear recovery suggestions when errors occur

**Purpose:** A reusable utility that synchronizes task status with GitHub Issues. Called by other micro-skills (pwrl-work-prepare, pwrl-work-execute) when GitHub integration is enabled. Gracefully skips if integration is disabled.

## Input

| Argument         | Required | Description                                                               |
| ---------------- | -------- | ------------------------------------------------------------------------- |
| `taskFile`       | Yes      | Path to task file (e.g., `docs/tasks/in-progress/u1-task.md`)             |
| `newStatus`      | Yes      | New status value: `to-do`, `in-progress`, `for-review`, `done`, `blocked` |
| `summaryMessage` | No       | Brief summary to include in comment                                       |
| `commitHash`     | No       | Commit hash to reference in comment                                       |
| `blockedReason`  | No       | Reason for blocked status                                                 |
| `dryRun`         | No       | Boolean flag (`true`) to preview without making changes                   |

## Output

```yaml
success: true | false
action: synced | skipped | failed
issueNumber: 123 | null
labelsAdded: [in-progress]
labelsRemoved: [to-do]
commentPosted: true | false
error: error message | null
```

---

## Workflow

### 1. Check GitHub Integration

Read `.pwrlrc.json` to determine if GitHub Issues integration is enabled:

```json
{
  "integrations": {
    "githubIssues": true,
    "github": {
      "owner": "wicttor",
      "repo": "pwrl"
    }
  }
}
```

**If `githubIssues` is `false` or missing:**

- Log: "GitHub integration disabled; skipping sync"
- Return: `{ success: true, action: "skipped", error: null }`
- Exit early — no GitHub API calls made

**If `githubIssues` is `true` but no `github.owner`/`github.repo`:**

- Log: "GitHub owner/repo not configured in .pwrlrc.json"
- Return: `{ success: false, action: "failed", error: "Missing owner/repo config" }`
- Exit early

**If enabled and configured:**

- Proceed to Step 2

### 2. Validate GitHub CLI Availability

Check that the GitHub CLI is installed and authenticated:

```bash
gh auth status 2>/dev/null
```

**If command fails:**

- Log: "GitHub CLI not available or not authenticated"
- Suggest: "Run `gh auth login` to authenticate"
- Return: `{ success: false, action: "failed", error: "GitHub CLI not authenticated" }`
- Exit early

**If successful:**

- Extract current username from `gh api user --jq .login`
- Proceed to Step 3

### 3. Parse Task File for Issue Reference

Read the task file frontmatter and extract the `github-issue` field:

```yaml
---
unit-id: S1
github-issue: 123
---
```

**If `github-issue` is missing or empty:**

- Log: "Task [unitId] has no linked GitHub issue; skipping sync"
- Return: `{ success: true, action: "skipped", error: null }`

**If `github-issue` is present:**

- Validate it's a numeric value
- Parse as issue number
- Proceed to Step 4

### 4. Update Issue Labels

Manage issue labels based on task status:

**Status-to-label mapping:**

| Status        | Labels to Add              | Labels to Remove                                |
| ------------- | -------------------------- | ----------------------------------------------- |
| `to-do`       | `pwrl-task`, `to-do`       | `in-progress`, `for-review`, `done`, `blocked`  |
| `in-progress` | `pwrl-task`, `in-progress` | `to-do`, `for-review`, `done`, `blocked`        |
| `for-review`  | `pwrl-task`, `for-review`  | `to-do`, `in-progress`, `done`, `blocked`       |
| `done`        | `pwrl-task`, `done`        | `to-do`, `in-progress`, `for-review`, `blocked` |
| `blocked`     | `pwrl-task`, `blocked`     | `to-do`, `in-progress`, `for-review`, `done`    |

**Implementation:**

```bash
# Get current labels
gh issue view <issue> --json labels --jq '.labels[].name'

# Update labels
gh issue edit <issue> \
  --add-label "<labels>" \
  --remove-label "<labels>"
```

**In dry-run mode:**

```
[DRY-RUN] Would update issue #123:
  Add labels: in-progress
  Remove labels: to-do
```

**Error handling:**

- Issue not found (`404`): Log warning, return `action: "failed"`
- API error: Log error, return `action: "failed"` with error message

### 5. Post Status Comment

Post an informative comment to the issue based on the new status:

**Status: `in-progress`**

```
🚀 Started work on this task
- **Task file:** `docs/tasks/in-progress/2026-06-05-u1-task.md`
- **Started:** 2026-06-05T12:00:00Z
- **Branch:** `feat/xyz` (if available)
- **Summary:** [optional summaryMessage]
```

**Status: `for-review`**

```
🔍 Ready for review
- **Implementation summary:** [optional summaryMessage]
- **Commits:** [optional commitHash]
- **Changed files:** [list of files modified — from task frontmatter]
```

**Status: `done`**

```
✅ Task complete
- **Completed:** 2026-06-05T14:00:00Z
- **Final commits:** [optional commitHash]
- **Review approval:** [reviewer, if available]
```

**Status: `blocked`**

```
🚫 Task blocked
- **Reason:** [blockedReason or "Unknown"]
- **Blocking task:** [unit ID from task, if specified]
- **Next steps:** [resolution needed]
```

**Implementation:**

```bash
gh issue comment <issue> -b "<formatted markdown>"
```

**Error handling:**

- API error: Log warning ("Comment posting failed: [error]"), continue
- Comment failure is non-critical; labels are the primary sync mechanism

### 6. Update Issue Metadata (Optional)

For certain status transitions:

**When status → `in-progress`:**

- Add current user as assignee: `gh issue edit <issue> --add-assignee @me`

**When status → `done`:**

- Close the issue: `gh issue close <issue>`
- Remove assignee: `gh issue edit <issue> --remove-assignee <user>`

**When status → `to-do` or `blocked`:**

- Reopen if currently closed: `gh issue reopen <issue>` (for `to-do`)
- Keep assignee (work still pending)

### 7. Return Sync Result

Log and return the sync result:

```yaml
# Success
success: true
action: synced
issueNumber: 123
labelsAdded: [in-progress]
labelsRemoved: [to-do]
commentPosted: true
error: null

# Skipped (GitHub disabled or no issue linked)
success: true
action: skipped
issueNumber: null
labelsAdded: []
labelsRemoved: []
commentPosted: false
error: null

# Failed
success: false
action: failed
issueNumber: 123
labelsAdded: []
labelsRemoved: []
commentPosted: false
error: "Issue #123 not found in repository wicttor/pwrl"
```

---

## Error Handling

| Scenario                      | Handling                                                      |
| ----------------------------- | ------------------------------------------------------------- |
| GitHub disabled in config     | Skip silently, return `action: skipped`                       |
| GitHub CLI not installed      | Log warning, return `action: failed`, ask to install          |
| Credentials not authenticated | Log warning, return `action: failed`, ask for `gh auth login` |
| Issue not found (404)         | Log warning, return `action: failed`                          |
| API rate limit exceeded       | Log error, return `action: failed`, suggest retry later       |
| Network/API error             | Log error, return `action: failed` with error message         |
| Invalid issue number          | Log error, return `action: failed`, ask to fix frontmatter    |
| Comment posting fails         | Log warning, continue (non-critical)                          |

**Retry guidance:**

- Network errors: Retry immediately (may recover)
- Rate limit (403): Wait 60 seconds before retry
- Authentication (401): Run `gh auth login` and retry
- Not found (404): Verify issue number in `.pwrlrc.json`

---

## Testing with Mocks

For unit testing without GitHub CLI or credentials, mock the `gh` CLI using stubs:

### Approach 1: Mock Shell Commands

If testing via shell scripts, create a mock `gh` wrapper:

```bash
# tests/mocks/gh-mock.sh
#!/bin/bash
# Mock GitHub CLI for testing
case "$1" in
  auth)
    echo "Authenticated as test-user"
    exit 0
    ;;
  issue)
    if [[ "$3" == "123" ]]; then
      echo '{"number": 123, "title": "Test Issue"}'
    else
      echo "HTTP 404: Issue not found" >&2
      exit 1
    fi
    ;;
  api)
    echo '{"login": "test-user"}'
    ;;
  *)
    echo "Unknown command: $1" >&2
    exit 1
    ;;
esac
```

In test:

```bash
export PATH="./tests/mocks:$PATH"
/pwrl-work-sync-status tests/fixtures/task-mock.md in-progress
# Now uses mock-gh.sh instead of real gh CLI
```

### Approach 2: Mock Config Disable

Simplest: Disable GitHub integration in test config:

```json
// tests/.pwrlrc.test.json
{
  "integrations": {
    "githubIssues": false
  }
}
```

Skill will return `action: skipped` without any GitHub CLI calls.

### Approach 3: Fake Issue in Real CLI (if installed)

If testing with real `gh` CLI but no real repo:

```bash
# Create test issue in real repo
gh issue create --title "Test sync issue" --body "For pwrl-work-sync-status tests"
# Use returned issue number in test fixtures
```

Update test fixture:

```yaml
---
unit-id: TEST-1
github-issue: 9999 # Use real issue from your repo
---
```

Clean up after test: `gh issue delete 9999`

### Recommended Practice

**For CI/CD environments:** Use Approach 2 (mock config disable) — requires no external dependencies, fastest
**For local development:** Use Approach 1 (mock gh wrapper) — most realistic, covers error paths
**For integration tests:** Use Approach 3 (real issue) — validates actual GitHub API behavior (but clean up after)

---

## Dry-Run Mode

When `dryRun: true`, preview changes without making API calls:

```
/pwrl-work-sync-status docs/tasks/in-progress/u1-task.md in-progress --dryRun=true
```

Output:

```
[DRY-RUN] Would sync task U1 to GitHub issue #123:
  - Add labels: in-progress
  - Remove labels: to-do
  - Post comment: "🚀 Started work..."
  - Update assignee: wicttor
```

---

## Quality Gates

**✅ Success if:**

- Labels updated correctly
- Comment posted (if applicable)
- All errors logged and handled gracefully

**⚠️ Partial success if:**

- Labels updated but comment failed (labels are primary sync)
- GitHub disabled (informed skip)

**❌ Fail if:**

- Invalid issue number format
- GitHub CLI not available (cannot proceed)
- Authentication fails

---

## Dependencies

- **GitHub CLI (`gh`)** — For all GitHub API interactions
- **`.pwrlrc.json`** — For integration configuration
- **File system** — For reading task file frontmatter
- **Callers:** `pwrl-work-prepare` (S3), `pwrl-work-execute` (S5)

## References

- **GitHub CLI:** https://cli.github.com/manual/
- **Task Status Tracking:** Used by S3 (prepare) and S5 (execute)
- **Config:** `.pwrlrc.json` — `integrations.githubIssues` flag
