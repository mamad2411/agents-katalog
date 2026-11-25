---
name: managing-atlantis
description: |
  Use when working with Atlantis — atlantis pull request automation for
  Terraform. Covers plan/apply via PR comments, workspace management, project
  configuration, server status, lock management, and repository configuration.
  Use when managing Atlantis deployments, debugging PR plan/apply issues, or
  configuring project workflows.
connection_type: atlantis
preload: false
---

# Atlantis Management Skill

Manage and inspect Atlantis PR-based Terraform automation, projects, and workflows.

## MANDATORY: Discovery-First Pattern

**Always check server status and active locks before triggering plans or applies.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Atlantis Server Status ==="
curl -s "${ATLANTIS_URL}/status" 2>/dev/null | jq '.' || \
curl -s "${ATLANTIS_URL}/healthz" 2>/dev/null

echo ""
echo "=== Active Locks ==="
curl -s -H "X-Atlantis-Token: $ATLANTIS_TOKEN" \
    "${ATLANTIS_URL}/api/locks" 2>/dev/null | jq '
    .[] | {
        repo: .repo_full_name,
        workspace: .workspace,
        pull_num: .pull.num,
        locked_by: .pull.author,
        time: .time
    }
' | head -30

echo ""
echo "=== Server Configuration ==="
curl -s "${ATLANTIS_URL}/api/server-config" 2>/dev/null | jq '{
    allow_fork_prs: .allow_fork_prs,
    auto_merge: .auto_merge,
    default_tf_version: .default_tf_version,
    repo_allowlist: .repo_allowlist
}' 2>/dev/null || echo "Server config API not available"
```

## Core Helper Functions

```bash
#!/bin/bash

# Atlantis API wrapper
atlantis_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "X-Atlantis-Token: $ATLANTIS_TOKEN" \
            -H "Content-Type: application/json" \
            "${ATLANTIS_URL}/api/${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "X-Atlantis-Token: $ATLANTIS_TOKEN" \
            "${ATLANTIS_URL}/api/${endpoint}"
    fi
}

# GitHub/GitLab comment helper for PR commands
atlantis_comment() {
    echo "Use these PR comments:"
    echo "  atlantis plan [-w workspace] [-d directory]"
    echo "  atlantis apply [-w workspace] [-d directory]"
    echo "  atlantis unlock"
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use API endpoints for server inspection
- PR-based operations are done via comments, not API
- Never expose webhook secrets in output

## Common Operations

### Project Configuration Review

```bash
#!/bin/bash
REPO_DIR="${1:-.}"

echo "=== atlantis.yaml Configuration ==="
cat "${REPO_DIR}/atlantis.yaml" 2>/dev/null || \
cat "${REPO_DIR}/atlantis.yml" 2>/dev/null || \
echo "No atlantis.yaml found -- using server-side config"

echo ""
echo "=== Detected Projects ==="
if [ -f "${REPO_DIR}/atlantis.yaml" ]; then
    cat "${REPO_DIR}/atlantis.yaml" | python3 -c "
import sys, yaml
config = yaml.safe_load(sys.stdin)
for p in config.get('projects', []):
    print(f\"{p.get('name', 'unnamed')}\t{p.get('dir', '.')}\t{p.get('workspace', 'default')}\t{p.get('terraform_version', 'default')}\")
" 2>/dev/null | column -t
else
    find "$REPO_DIR" -name "*.tf" -not -path "*/.terraform/*" -exec dirname {} \; 2>/dev/null | sort -u | head -15
fi
```

### Lock Management

```bash
#!/bin/bash
echo "=== Current Locks ==="
atlantis_api GET "locks" | jq -r '
    .[] | "\(.repo_full_name)\t\(.workspace)\tPR#\(.pull.num)\t\(.pull.author)\t\(.time)"
' | column -t

echo ""
echo "=== Stale Locks (>24h) ==="
atlantis_api GET "locks" | jq -r '
    .[] |
    select((.time | fromdateiso8601) < (now - 86400)) |
    "STALE: \(.repo_full_name) workspace=\(.workspace) PR#\(.pull.num) locked_by=\(.pull.author)"
'

echo ""
LOCK_ID="${1:-}"
if [ -n "$LOCK_ID" ]; then
    echo "To unlock, comment 'atlantis unlock' on the PR, or:"
    echo "curl -X DELETE ${ATLANTIS_URL}/api/locks/${LOCK_ID} -H 'X-Atlantis-Token: \$ATLANTIS_TOKEN'"
fi
```

### Workspace Management

```bash
#!/bin/bash
echo "=== Workspaces in Use ==="
atlantis_api GET "locks" | jq -r '
    [.[] | .workspace] | unique | .[]
'

echo ""
echo "=== PR Comment Commands ==="
echo "Plan specific workspace:  atlantis plan -w staging"
echo "Apply specific workspace: atlantis apply -w staging"
echo "Plan specific directory:  atlantis plan -d infrastructure/vpc"
echo "Plan all projects:        atlantis plan"
```

### Workflow Configuration

```bash
#!/bin/bash
echo "=== Custom Workflows ==="
cat atlantis.yaml 2>/dev/null | python3 -c "
import sys, yaml
config = yaml.safe_load(sys.stdin)
workflows = config.get('workflows', {})
for name, wf in workflows.items():
    print(f'Workflow: {name}')
    plan_steps = wf.get('plan', {}).get('steps', ['init', 'plan'])
    apply_steps = wf.get('apply', {}).get('steps', ['apply'])
    print(f'  Plan steps:  {[s if isinstance(s, str) else list(s.keys())[0] for s in plan_steps]}')
    print(f'  Apply steps: {[s if isinstance(s, str) else list(s.keys())[0] for s in apply_steps]}')
" 2>/dev/null || echo "No custom workflows defined"

echo ""
echo "=== Server-Side Repo Config ==="
echo "Check server repos.yaml for server-side workflow overrides"
```

### Plan/Apply Status

```bash
#!/bin/bash
echo "=== Recent PR Activity ==="
atlantis_api GET "jobs" 2>/dev/null | jq '
    .[0:10][] | {
        pr: .pull_num,
        project: .project,
        workspace: .workspace,
        status: .status,
        started: .started_at
    }
' | head -40

echo ""
echo "=== Common PR Commands ==="
echo "atlantis plan                    # Plan all projects"
echo "atlantis plan -w prod            # Plan specific workspace"
echo "atlantis plan -d infra/vpc       # Plan specific directory"
echo "atlantis plan -- -target=aws_s3  # Plan with extra args"
echo "atlantis apply                   # Apply all planned projects"
echo "atlantis unlock                  # Release all locks"
```

## Safety Rules

- **NEVER force-unlock without checking if an apply is in progress** -- can corrupt state
- **Review plan output before commenting `atlantis apply`** on PRs
- **Use `allowed_overrides` carefully** -- allows PR authors to bypass server-side configs
- **Webhook secrets must be strong** -- weak secrets allow unauthorized plan/apply triggers
- **Apply requirements** (mergeable, approved) should be enforced for production workspaces

## Output Format

Present results as a structured report:
```
Managing Atlantis Report
════════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls

- **Lock conflicts**: Only one PR can lock a workspace/directory at a time -- close stale PRs to release locks
- **Webhook delivery failures**: GitHub/GitLab webhook timeouts cause missed plan triggers -- check delivery logs
- **Terraform version mismatch**: Server default version may differ from project needs -- set per-project in atlantis.yaml
- **Parallel plan limits**: Too many concurrent plans can exhaust server resources -- configure max parallelism
- **Auto-merge on apply**: If enabled, PRs merge immediately after apply -- ensure branch protection rules are set
- **Repo allowlist**: Atlantis only processes repos in the allowlist -- new repos must be added
- **Custom workflow errors**: Script failures in custom workflows may not surface clearly in PR comments
- **Credentials in logs**: Plan output may contain sensitive values -- ensure Atlantis redacts or use log sanitization
