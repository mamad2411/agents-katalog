---
name: managing-changesets
description: |
  Use when working with Changesets — changesets version management covering
  changeset file inventory, pending version bump analysis, package release
  readiness, changelog generation status, and monorepo release coordination. Use
  when auditing pending changesets, investigating release blockers, reviewing
  version bump strategies, or managing multi-package release workflows.
connection_type: github
preload: false
---

# Changesets Management Skill

Analyze and monitor Changesets version management, pending changes, and release workflows.

## MANDATORY: Discovery-First Pattern

**Always locate changeset configuration and pending changesets before analyzing release readiness.**

### Phase 1: Discovery

```bash
#!/bin/bash

GH_API="https://api.github.com"

gh_api() {
    curl -s -H "Authorization: Bearer $GITHUB_TOKEN" \
         -H "Accept: application/vnd.github+json" \
         "${GH_API}/${1}"
}

echo "=== Locate Changesets Config ==="
gh_api "orgs/${GITHUB_ORG}/repos?per_page=15&sort=updated" | jq -r '.[].full_name' | while read repo; do
    if gh_api "repos/${repo}/contents/.changeset/config.json" 2>/dev/null | jq -e '.name' >/dev/null 2>&1; then
        echo -e "${repo}\t.changeset/config.json\tFOUND"
    fi
done | column -t | head -15

echo ""
echo "=== Changesets Config ==="
REPO="${GITHUB_ORG}/${GITHUB_REPO}"
gh_api "repos/${REPO}/contents/.changeset/config.json" | jq -r '.content' | base64 -d 2>/dev/null | jq '{
    changelog: .changelog,
    commit: .commit,
    fixed: .fixed,
    linked: .linked,
    access: .access,
    baseBranch: .baseBranch
}'

echo ""
echo "=== Version Packages PR ==="
gh_api "repos/${REPO}/pulls?state=open&per_page=10" | jq -r '
    .[] |
    select(.title | startswith("Version Packages")) |
    "#\(.number)\t\(.title[:50])\t\(.created_at[:10])\t\(.updated_at[:10])"
' | column -t
```

### Phase 2: Analysis

```bash
#!/bin/bash

REPO="${1:-${GITHUB_ORG}/${GITHUB_REPO}}"

echo "=== Pending Changesets ==="
gh_api "repos/${REPO}/contents/.changeset" | jq -r '
    .[] |
    select(.name != "config.json" and .name != "README.md" and (.name | endswith(".md"))) |
    "\(.name)\t\(.size) bytes"
' | column -t | head -20

echo ""
echo "=== Changeset Details (latest 5) ==="
gh_api "repos/${REPO}/contents/.changeset" | jq -r '
    [.[] | select(.name != "config.json" and .name != "README.md" and (.name | endswith(".md")))] |
    sort_by(.name) | reverse | .[0:5] | .[].name
' | while read cs; do
    echo "--- ${cs} ---"
    gh_api "repos/${REPO}/contents/.changeset/${cs}" | jq -r '.content' | base64 -d 2>/dev/null | head -10
done | head -30

echo ""
echo "=== Recent Releases (tags) ==="
gh_api "repos/${REPO}/releases?per_page=10" | jq -r '
    .[] |
    "\(.tag_name)\t\(.published_at[:10])\t\(.name[:40])"
' | column -t

echo ""
echo "=== Changeset Summary ==="
PENDING=$(gh_api "repos/${REPO}/contents/.changeset" | jq '[.[] | select(.name != "config.json" and .name != "README.md" and (.name | endswith(".md")))] | length')
VERSION_PR=$(gh_api "repos/${REPO}/pulls?state=open&per_page=10" | jq '[.[] | select(.title | startswith("Version Packages"))] | length')
echo "Pending changesets: ${PENDING}"
echo "Version Packages PR open: ${VERSION_PR}"
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Summarize changeset bump types rather than reading all changeset files
- Focus on release readiness and blocking issues

## Output Format

Present results as a structured report:
```
Managing Changesets Report
══════════════════════════
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

- **Missing changesets**: PRs without changesets produce no version bump -- enforce via CI check
- **Bump types**: major/minor/patch in changeset frontmatter controls version increment
- **Fixed groups**: Fixed packages version together -- one major bump upgrades all
- **Linked packages**: Linked packages get the same bump type but independent versions
- **Version PR conflicts**: Version Packages PR can have merge conflicts with new changesets
- **Access setting**: "restricted" requires npm OTP for publishing -- "public" for public packages
- **Pre-release mode**: Entering/exiting pre-release mode requires explicit changeset commands
- **Monorepo coordination**: Changesets track per-package bumps -- verify all affected packages are listed
