---
name: managing-gitlab-deep
description: |
  Use when working with Gitlab Deep — gitLab deep platform management covering
  project inventory, CI/CD pipeline monitoring, merge request analysis,
  container registry health, security dashboard, runner status, group and member
  auditing, and protected branch configuration. Use when auditing project
  configurations, investigating pipeline failures, reviewing security findings,
  or managing GitLab instance settings.
connection_type: gitlab
preload: false
---

# GitLab Deep Management Skill

Manage and monitor GitLab projects, CI/CD pipelines, security, and group settings at depth.

## MANDATORY: Discovery-First Pattern

**Always list groups and projects before querying specific resources.**

### Phase 1: Discovery

```bash
#!/bin/bash

GITLAB_API="${GITLAB_URL:-https://gitlab.com}/api/v4"

gl_api() {
    curl -s -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
         -H "Content-Type: application/json" \
         "${GITLAB_API}/${1}"
}

echo "=== Groups ==="
gl_api "groups?per_page=20&owned=true" | jq -r '
    .[] |
    "\(.id)\t\(.full_path)\t\(.visibility)\t\(.projects | length // 0) projects"
' | column -t

echo ""
echo "=== Projects ==="
gl_api "projects?per_page=30&order_by=last_activity_at&owned=true" | jq -r '
    .[] |
    "\(.id)\t\(.path_with_namespace)\t\(.visibility)\t\(.default_branch)\t\(.last_activity_at[:10])"
' | column -t | head -30

echo ""
echo "=== Runners ==="
gl_api "runners?per_page=20" | jq -r '
    .[] |
    "\(.id)\t\(.description)\t\(.status)\t\(.runner_type)\t\(.active)"
' | column -t | head -15
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Failed Pipelines (recent) ==="
gl_api "projects?per_page=10&order_by=last_activity_at&owned=true" | jq -r '.[].id' | while read pid; do
    gl_api "projects/${pid}/pipelines?status=failed&per_page=3" | jq -r --arg pid "$pid" '
        .[]? |
        "\($pid)\t\(.id)\t\(.ref)\t\(.status)\t\(.created_at[:10])"
    '
done | column -t | head -20

echo ""
echo "=== Protected Branches ==="
gl_api "projects?per_page=10&order_by=last_activity_at&owned=true" | jq -r '.[].id' | while read pid; do
    gl_api "projects/${pid}/protected_branches" | jq -r --arg pid "$pid" '
        .[]? |
        "\($pid)\t\(.name)\tpush=\(.push_access_levels[0].access_level)\tmerge=\(.merge_access_levels[0].access_level)"
    '
done | column -t | head -15

echo ""
echo "=== Open Merge Requests (by project) ==="
gl_api "projects?per_page=10&order_by=last_activity_at&owned=true" | jq -r '.[].id' | while read pid; do
    COUNT=$(gl_api "projects/${pid}/merge_requests?state=opened&per_page=1" | jq '. | length')
    [ "$COUNT" != "0" ] && echo -e "${pid}\t${COUNT} open MRs"
done | column -t

echo ""
echo "=== Container Registries ==="
gl_api "projects?per_page=10&order_by=last_activity_at&owned=true" | jq -r '.[].id' | while read pid; do
    gl_api "projects/${pid}/registry/repositories" 2>/dev/null | jq -r --arg pid "$pid" '
        .[]? |
        "\($pid)\t\(.path)\t\(.tags_count // 0) tags"
    '
done | column -t | head -15

echo ""
echo "=== Vulnerability Summary ==="
gl_api "projects?per_page=5&order_by=last_activity_at&owned=true" | jq -r '.[].id' | while read pid; do
    gl_api "projects/${pid}/vulnerability_findings?per_page=1" 2>/dev/null | jq -r --arg pid "$pid" '
        if type == "array" and length > 0 then "\($pid)\thas vulnerabilities" else empty end
    '
done | column -t
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use per_page and status filters to control result size
- Never dump full pipeline logs or MR diffs -- extract status metadata

## Output Format

Present results as a structured report:
```
Managing Gitlab Deep Report
═══════════════════════════
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

- **Rate limits**: GitLab.com allows 300 req/min for authenticated users
- **Runner availability**: Shared runners have queue times -- check runner status and pending jobs
- **Protected branch levels**: Access levels are numeric (0=no access, 30=developer, 40=maintainer, 60=admin)
- **Pipeline triggers**: Child pipelines and multi-project pipelines complicate failure tracing
- **Registry cleanup**: Old container images accumulate -- configure cleanup policies
- **Security scanning**: SAST/DAST results require Ultimate tier -- check license
- **Merge train**: Merge trains can stall if a pipeline fails mid-train
- **Project transfer**: Transferring projects between groups changes URLs and breaks CI references
