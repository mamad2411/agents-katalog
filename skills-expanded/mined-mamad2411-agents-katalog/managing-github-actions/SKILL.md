---
name: managing-github-actions
description: |
  Use when working with Github Actions — gitHub Actions workflow and runner
  management. Covers workflow run status, job analysis, usage billing, secret
  management, runner administration, and artifact retrieval. Use when checking
  CI status, investigating workflow failures, managing self-hosted runners, or
  auditing Actions usage costs.
connection_type: github
preload: false
---

# GitHub Actions Management Skill

Manage and monitor GitHub Actions workflows, runners, and usage.

## Core Helper Functions

```bash
#!/bin/bash

# GitHub API helper
gh_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        gh api -X "$method" "$endpoint" --input - <<< "$data"
    else
        gh api -X "$method" "$endpoint"
    fi
}

# Shorthand for repos endpoint
gh_repo_api() {
    gh api "repos/${GH_OWNER}/${GH_REPO}/${1}"
}
```

## MANDATORY: Discovery-First Pattern

**Always list workflows and recent runs before querying specifics.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Repository Workflows ==="
gh_repo_api "actions/workflows" | jq -r '
    .workflows[] | "\(.id)\t\(.name)\t\(.state)\t\(.path)"
' | column -t

echo ""
echo "=== Recent Workflow Runs ==="
gh_repo_api "actions/runs?per_page=15" | jq -r '
    .workflow_runs[] |
    "\(.name)\t\(.status)\t\(.conclusion // "running")\t\(.head_branch)\t\(.created_at[0:16])"
' | column -t

echo ""
echo "=== Self-Hosted Runners ==="
gh_repo_api "actions/runners" | jq -r '
    .runners[] | "\(.id)\t\(.name)\t\(.status)\t\(.os)\t\(.labels | map(.name) | join(","))"
' | column -t
```

## Output Rules
- **TOKEN EFFICIENCY**: Target 50 lines per output
- Use `gh api` with `--jq` for inline filtering
- Never dump full workflow logs — use step-level log retrieval

## Common Operations

### Workflow Run Dashboard

```bash
#!/bin/bash
echo "=== Workflow Run Summary ==="
gh_repo_api "actions/runs?per_page=50" | jq '{
    total: .total_count,
    success: [.workflow_runs[] | select(.conclusion == "success")] | length,
    failure: [.workflow_runs[] | select(.conclusion == "failure")] | length,
    cancelled: [.workflow_runs[] | select(.conclusion == "cancelled")] | length,
    in_progress: [.workflow_runs[] | select(.status == "in_progress")] | length
}'

echo ""
echo "=== Failed Runs ==="
gh_repo_api "actions/runs?status=failure&per_page=10" | jq -r '
    .workflow_runs[] |
    "\(.name)\t#\(.run_number)\t\(.head_branch)\t\(.created_at[0:16])\t\(.html_url)"
' | column -t

echo ""
echo "=== Longest Running Workflows (last 20) ==="
gh_repo_api "actions/runs?per_page=20&status=completed" | jq -r '
    [.workflow_runs[] |
        {name, run_number, duration: (((.updated_at | fromdateiso8601) - (.created_at | fromdateiso8601)) / 60 | floor)}
    ] | sort_by(-.duration) | .[:10][] |
    "\(.name)\t#\(.run_number)\t\(.duration)min"
' | column -t
```

### Job Analysis & Logs

```bash
#!/bin/bash
RUN_ID="${1:?Run ID required}"

echo "=== Jobs in Run ==="
gh_repo_api "actions/runs/${RUN_ID}/jobs" | jq -r '
    .jobs[] |
    "\(.name)\t\(.status)\t\(.conclusion // "running")\t\(.started_at[0:16])"
' | column -t

echo ""
echo "=== Failed Job Steps ==="
gh_repo_api "actions/runs/${RUN_ID}/jobs" | jq -r '
    .jobs[] | select(.conclusion == "failure") |
    "Job: \(.name)",
    (.steps[] | select(.conclusion == "failure") |
    "  Step \(.number): \(.name) — \(.conclusion)")
'

echo ""
echo "=== Download Failed Job Logs ==="
FAILED_JOB_ID=$(gh_repo_api "actions/runs/${RUN_ID}/jobs" | jq '.jobs[] | select(.conclusion == "failure") | .id' | head -1)
if [ -n "$FAILED_JOB_ID" ]; then
    gh_repo_api "actions/jobs/${FAILED_JOB_ID}/logs" | tail -80
fi
```

### Usage & Billing

```bash
#!/bin/bash
echo "=== Actions Billing (Organization) ==="
gh api "orgs/${GH_ORG}/settings/billing/actions" | jq '{
    total_minutes_used: .total_minutes_used,
    total_paid_minutes_used: .total_paid_minutes_used,
    included_minutes: .included_minutes,
    minutes_remaining: (.included_minutes - .total_minutes_used),
    minutes_used_breakdown: .minutes_used_breakdown
}'

echo ""
echo "=== Workflow Usage (this billing cycle) ==="
gh_repo_api "actions/workflows" | jq -r '.workflows[].id' | while read wf_id; do
    USAGE=$(gh_repo_api "actions/workflows/${wf_id}/timing" 2>/dev/null)
    NAME=$(gh_repo_api "actions/workflows/${wf_id}" | jq -r '.name')
    echo "$NAME: $(echo "$USAGE" | jq '.billable | to_entries[] | "\(.key)=\(.value.total_ms / 60000 | floor)min"' 2>/dev/null | tr '\n' ' ')"
done | head -15
```

### Secret Management

```bash
#!/bin/bash
echo "=== Repository Secrets ==="
gh_repo_api "actions/secrets" | jq -r '
    .secrets[] | "\(.name)\tupdated=\(.updated_at[0:10])"
' | column -t

echo ""
echo "=== Organization Secrets (visible to repo) ==="
gh_repo_api "actions/organization-secrets" | jq -r '
    .secrets[] | "\(.name)\tvisibility=\(.visibility)\tupdated=\(.updated_at[0:10])"
' | column -t 2>/dev/null || echo "No org secrets or insufficient permissions"

echo ""
echo "=== Environment Secrets ==="
gh_repo_api "environments" | jq -r '.environments[].name' | while read env; do
    echo "--- $env ---"
    gh_repo_api "environments/${env}/secrets" | jq -r '.secrets[] | "  \(.name)\tupdated=\(.updated_at[0:10])"' 2>/dev/null
done
```

### Runner Management

```bash
#!/bin/bash
echo "=== Self-Hosted Runners ==="
gh_repo_api "actions/runners" | jq -r '
    .runners[] |
    "\(.name)\t\(.status)\t\(.os)-\(.architecture // "x64")\t\(.busy)\tlabels=\(.labels | map(.name) | join(","))"
' | column -t

echo ""
echo "=== Runner Groups (Organization) ==="
gh api "orgs/${GH_ORG}/actions/runner-groups" | jq -r '
    .runner_groups[] | "\(.id)\t\(.name)\t\(.runners_count) runners\tdefault=\(.default)"
' | column -t 2>/dev/null || echo "Org runner groups require admin access"
```

### Artifact Management

```bash
#!/bin/bash
RUN_ID="${1:?Run ID required}"

echo "=== Run Artifacts ==="
gh_repo_api "actions/runs/${RUN_ID}/artifacts" | jq -r '
    .artifacts[] |
    "\(.name)\tsize=\(.size_in_bytes / 1024 | floor)KB\texpires=\(.expires_at[0:10])\texpired=\(.expired)"
' | column -t
```

## Anti-Hallucination Rules
- NEVER guess run IDs or workflow IDs — always discover via API
- NEVER fabricate workflow file names — list workflows first
- NEVER assume secret values — API only returns metadata, never values
- Runner labels vary per installation — always list before filtering

## Safety Rules
- NEVER delete secrets without explicit user confirmation
- NEVER cancel or re-run workflows without user approval
- NEVER remove runners without confirming they are idle
- Secret creation requires the public key — fetch it first via the API

## Output Format

Present results as a structured report:
```
Managing Github Actions Report
══════════════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls
- **gh CLI vs API**: `gh run list` is simpler for basic queries; API gives more control
- **Log retention**: Workflow logs are retained for 90 days by default — older logs are gone
- **Artifact expiry**: Artifacts expire (default 90 days) — check `expired` field before download
- **Concurrency**: Workflow concurrency groups can cancel in-progress runs — check `concurrency` in workflow YAML
- **Reusable workflows**: Called workflows run in the caller's context — check both repos for debugging
- **GITHUB_TOKEN scope**: Default token has limited permissions — some operations need a PAT or GitHub App token
