---
name: ship
version: 1.0.0
standalone: true
description: End-to-end shipping workflow — tests, PR creation, review request. Unified pr-create + pr-complete.
uses:
  - development/git
  - development/testing
requires:
  tools: [git, gh]
  env: []
security:
  risk_level: write
  capabilities:
    - git:read
    - git:write
    - github:pr:write
  requires_approval: false
---

# Ship

Unified shipping workflow. Takes code from "tests pass" to "PR created and
review requested." Combines what pr-create and pr-complete do, adds pre-flight
checks and embedded review readiness verification.

**Standalone mode**: Works without agent-coordinator. Skip coordinator status
updates and bus notifications when `AC_COORDINATOR_URL` is not set.

## STOP — Read This Entire Skill Before Starting

Do NOT begin shipping until you have verified:
1. You are on a feature branch (not main)
2. All changes are committed
3. Tests pass

## When to Use

- Development work is complete and tests pass
- Ready to create a PR and request review
- Replaces manual pr-create → wait → pr-complete flow

## Pre-Flight Checks (MANDATORY)

Before creating the PR, verify ALL of these:

```bash
# 1. On a feature branch?
BRANCH=$(git branch --show-current)
if [ "$BRANCH" = "main" ] || [ "$BRANCH" = "master" ]; then
    echo "ERROR: Cannot ship from main. Create a feature branch first."
    exit 1
fi

# 2. Clean working directory?
if [ -n "$(git status --porcelain)" ]; then
    echo "ERROR: Uncommitted changes. Commit or stash first."
    exit 1
fi

# 3. Branch pushed to remote?
git push -u origin "$BRANCH" 2>/dev/null

# 4. Tests pass?
# Run the project's test command. Adapt to the project:
# PYTHONPATH=src python3 -m pytest tests/ --timeout=60 -q
```

If ANY check fails, STOP. Fix the issue before proceeding.

## Shipping Steps

### Step 1: Create PR

```bash
BRANCH=$(git branch --show-current)
TITLE=$(git log --format=%s -1)  # Use last commit message as default title

gh pr create \
    --title "$TITLE" \
    --body "## Summary
<describe what changed and why>

## Test plan
<describe how to verify>
" \
    --base main
```

Capture the PR number from the output.

### Step 2: Verify PR Created

```bash
PR_NUMBER=$(gh pr view --json number -q .number)
echo "PR #${PR_NUMBER} created"
```

### Step 3: Update Coordinator *(framework only)*

If running within agent-coordinator:

```bash
COORDINATOR="${AC_COORDINATOR_URL:-http://localhost:9889}"
TASK_ID="${TASK_ID:-}"

if [ -n "$TASK_ID" ] && [ -n "$COORDINATOR" ]; then
    # Move task to review status
    curl -s -X POST "${COORDINATOR}/tasks/${TASK_ID}/status?new_status=review&agent_id=${AGENT_NAME}&pr_number=${PR_NUMBER}" 2>/dev/null || true
fi
```

### Step 4: Review Readiness Check

Before requesting review, verify:

```bash
# Check CI status
gh pr checks "$PR_NUMBER" --watch --interval 30

# Check for merge conflicts
gh pr view "$PR_NUMBER" --json mergeable -q .mergeable
```

If CI fails or conflicts exist, fix them before requesting review.

### Step 5: Request Review

```bash
# Publish review request to bus (framework only)
if [ -n "$COORDINATOR" ]; then
    curl -s -X POST "${COORDINATOR}/bus/publish" \
        -H "Content-Type: application/json" \
        -d "{\"channel\": \"work\", \"type\": \"review_request\", \"sender\": \"${AGENT_NAME}\", \"payload\": {\"task_id\": \"${TASK_ID}\", \"pr_number\": \"${PR_NUMBER}\"}}"
fi

echo "PR #${PR_NUMBER} shipped. Awaiting review."
```

## Escalation Protocol

If you encounter issues during shipping:
- **Merge conflicts**: Fix locally, push, retry
- **CI failures**: Fix the failing tests, push, retry
- **3 consecutive failures**: Stop and report BLOCKED with details

It is always OK to stop and say "this is too hard for me."

## Completion States

- **DONE**: PR created, CI passing, review requested
- **DONE_WITH_CONCERNS**: PR created but CI has warnings (non-blocking)
- **BLOCKED**: Cannot create PR (auth failure, branch issues, persistent CI failures)
- **NEEDS_CONTEXT**: Unclear what should be in the PR (scope ambiguity)

## Output Format

On success, report:
```json
{"pr_number": 123, "pr_url": "https://github.com/...", "success": true}
```

On failure, report:
```json
{"pr_number": 0, "pr_url": "", "success": false, "error": "description"}
```

## Note on tool.yaml Handler

The `tool.yaml` handler executes only the core action (`gh pr create`).
The full workflow (pre-flight checks, CI verification, coordinator updates,
bus publish) is described in the Steps above — the agent follows the prose.
This is consistent with how `lifecycle/land` and other skills work.

## Relationship to Other Skills

- **ship** = this skill (create PR + request review)
- **land** = merge approved PR after CI passes
- **retro** = periodic learning consolidation after tasks complete

Together: ship → review → land → retro
