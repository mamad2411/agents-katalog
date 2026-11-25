---
name: analyzing-dependabot
description: |
  Use when working with Dependabot — dependabot and Renovate dependency update
  management. Covers vulnerability alerts, dependency update PRs, auto-merge
  configuration, version pinning, update scheduling, and security advisory
  tracking. Use when managing dependency updates, reviewing vulnerability
  alerts, configuring auto-merge policies, or auditing dependency health.
connection_type: dependabot
preload: false
---

# Dependabot/Renovate Dependency Analysis Skill

Manage and analyze dependency updates, vulnerability alerts, and auto-merge configurations.

## MANDATORY: Discovery-First Pattern

**Always check current configuration and alert status before modifying update policies.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Dependabot Configuration ==="
cat .github/dependabot.yml 2>/dev/null || cat .github/dependabot.yaml 2>/dev/null || echo "No Dependabot config found"

echo ""
echo "=== Renovate Configuration ==="
cat renovate.json 2>/dev/null || cat .renovaterc 2>/dev/null || cat .renovaterc.json 2>/dev/null || echo "No Renovate config found"

echo ""
echo "=== Dependency Files Detected ==="
find . -maxdepth 3 \( \
    -name "package.json" -o -name "package-lock.json" -o \
    -name "requirements.txt" -o -name "Pipfile" -o \
    -name "go.mod" -o -name "Gemfile" -o \
    -name "pom.xml" -o -name "build.gradle" -o \
    -name "Cargo.toml" -o -name "composer.json" \
\) -not -path "*/node_modules/*" 2>/dev/null | head -15

echo ""
echo "=== Open Dependency PRs ==="
gh pr list --label dependencies 2>/dev/null | head -10 || \
gh pr list --search "author:dependabot" 2>/dev/null | head -10
```

## Core Helper Functions

```bash
#!/bin/bash

# GitHub API for Dependabot
gh_dependabot() {
    local endpoint="$1"
    gh api "$endpoint" 2>/dev/null
}

# List vulnerability alerts
gh_alerts() {
    local repo="${1:?Repo required (owner/name)}"
    gh api "repos/${repo}/dependabot/alerts?state=open&sort=created&direction=desc" 2>/dev/null
}

# Renovate API (self-hosted)
renovate_api() {
    local endpoint="$1"
    curl -s -H "Authorization: Bearer $RENOVATE_TOKEN" \
        "${RENOVATE_URL}/api/${endpoint}" 2>/dev/null
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use GitHub API with jq for structured alert data
- Group alerts by severity and ecosystem
- Never dump full advisory details -- extract key fields

## Common Operations

### Vulnerability Alerts

```bash
#!/bin/bash
REPO="${1:?Repository required (owner/name)}"

echo "=== Open Vulnerability Alerts ==="
gh api "repos/${REPO}/dependabot/alerts?state=open&sort=created&direction=desc&per_page=30" 2>/dev/null | jq '{
    total_open: length,
    by_severity: (group_by(.security_advisory.severity) | map({
        severity: .[0].security_advisory.severity,
        count: length
    })),
    by_ecosystem: (group_by(.dependency.package.ecosystem) | map({
        ecosystem: .[0].dependency.package.ecosystem,
        count: length
    })),
    top_alerts: [.[:10][] | {
        number: .number,
        severity: .security_advisory.severity,
        package: .dependency.package.name,
        ecosystem: .dependency.package.ecosystem,
        vulnerable_range: .security_vulnerability.vulnerable_version_range,
        fixed_version: .security_vulnerability.first_patched_version.identifier,
        summary: .security_advisory.summary
    }]
}'
```

### Dependency Update PRs

```bash
#!/bin/bash
REPO="${1:?Repository required (owner/name)}"

echo "=== Open Dependency PRs ==="
gh pr list --repo "$REPO" --search "author:dependabot OR author:renovate" --json number,title,createdAt,labels --limit 20 2>/dev/null | jq '[.[] | {
    number: .number,
    title: .title,
    created: .createdAt,
    labels: [.labels[].name]
}]'

echo ""
echo "=== PR Age Distribution ==="
gh pr list --repo "$REPO" --search "author:dependabot OR author:renovate" --json number,title,createdAt --limit 50 2>/dev/null | jq '
    [.[] | {
        number: .number,
        title: .title[:50],
        age_days: ((now - (.createdAt | fromdateiso8601)) / 86400 | floor)
    }] | sort_by(-.age_days) | .[0:10]
'
```

### Auto-Merge Configuration

```bash
#!/bin/bash
echo "=== Dependabot Auto-Merge Config ==="
cat .github/dependabot.yml 2>/dev/null | head -30

echo ""
echo "=== GitHub Actions Auto-Merge Workflow ==="
cat .github/workflows/dependabot-auto-merge.yml 2>/dev/null || \
cat .github/workflows/auto-merge.yml 2>/dev/null || \
echo "No auto-merge workflow found"

echo ""
echo "=== Renovate Auto-Merge Config ==="
cat renovate.json 2>/dev/null | jq '{
    automerge: .automerge,
    automergeType: .automergeType,
    packageRules: [.packageRules[]? | select(.automerge != null) | {
        matchPackagePatterns: .matchPackagePatterns,
        matchUpdateTypes: .matchUpdateTypes,
        automerge: .automerge
    }]
}' 2>/dev/null
```

### Security Advisory Tracking

```bash
#!/bin/bash
REPO="${1:?Repository required (owner/name)}"

echo "=== Critical/High Alerts Requiring Action ==="
gh api "repos/${REPO}/dependabot/alerts?state=open&severity=critical,high&per_page=20" 2>/dev/null | jq '[.[] | {
    number: .number,
    package: .dependency.package.name,
    severity: .security_advisory.severity,
    cvss: .security_advisory.cvss.score,
    cve: .security_advisory.cve_id,
    fix_available: (.security_vulnerability.first_patched_version != null),
    fix_version: .security_vulnerability.first_patched_version.identifier,
    manifest: .dependency.manifest_path
}]'

echo ""
echo "=== Alert Dismissal History ==="
gh api "repos/${REPO}/dependabot/alerts?state=dismissed&per_page=10" 2>/dev/null | jq '[.[] | {
    package: .dependency.package.name,
    severity: .security_advisory.severity,
    dismissed_reason: .dismissed_reason,
    dismissed_by: .dismissed_by.login
}]'
```

### Dependency Health Overview

```bash
#!/bin/bash
echo "=== Dependency File Analysis ==="
for dep_file in $(find . -maxdepth 3 \( -name "package.json" -o -name "requirements.txt" -o -name "go.mod" -o -name "Gemfile" \) -not -path "*/node_modules/*" 2>/dev/null | head -5); do
    echo "--- $dep_file ---"
    case "$dep_file" in
        */package.json) jq '.dependencies // {} | length' "$dep_file" 2>/dev/null | xargs -I{} echo "  Dependencies: {}" ;;
        */requirements.txt) wc -l < "$dep_file" 2>/dev/null | xargs -I{} echo "  Packages: {}" ;;
        */go.mod) grep -c 'require' "$dep_file" 2>/dev/null | xargs -I{} echo "  Modules: {}" ;;
        */Gemfile) grep -c 'gem ' "$dep_file" 2>/dev/null | xargs -I{} echo "  Gems: {}" ;;
    esac
done

echo ""
echo "=== Update Schedule ==="
cat .github/dependabot.yml 2>/dev/null | grep -A2 'schedule' | head -10
```

## Safety Rules

- **Review all dependency update PRs before merging** -- even minor updates can introduce breaking changes
- **Auto-merge only for patch versions** with passing CI -- never auto-merge major version bumps
- **Vulnerability alerts should be prioritized** by severity and exploitability
- **Dismissing alerts requires justification** -- document why in the dismissal reason
- **Lock file updates** should be tested in CI before merging

## Output Format

Present results as a structured report:
```
Analyzing Dependabot Report
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

- **Transitive dependencies**: Vulnerability may be in a transitive dependency -- updating direct dependency may not fix it
- **Breaking changes in minor versions**: Semver violations are common -- always run tests after updates
- **Rate limiting**: Too many open PRs can overwhelm CI systems -- configure PR limits
- **Rebase conflicts**: Dependency PRs frequently conflict with each other -- merge incrementally
- **Private registries**: Dependabot/Renovate need credentials for private registries -- configure secrets
- **Monorepo handling**: Multiple dependency files may need coordinated updates -- use groups
- **Auto-merge security**: Auto-merging without CI checks can introduce vulnerabilities or broken code
- **Version constraints**: Overly tight version constraints prevent security updates -- use ranges appropriately
