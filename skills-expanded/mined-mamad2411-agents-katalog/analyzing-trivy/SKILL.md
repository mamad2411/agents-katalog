---
name: analyzing-trivy
description: |
  Use when working with Trivy — trivy comprehensive security scanner. Covers
  container image scanning, filesystem scanning, Kubernetes cluster scanning,
  SBOM generation, secret detection, license scanning, and misconfiguration
  detection. Use when scanning containers for vulnerabilities, generating SBOMs,
  scanning K8s clusters, or detecting misconfigurations.
connection_type: trivy
preload: false
---

# Trivy Security Analysis Skill

Analyze vulnerabilities, misconfigurations, and secrets using Trivy across containers, filesystems, and Kubernetes.

## MANDATORY: Discovery-First Pattern

**Always check Trivy version and available scanners before running scans.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Trivy Version ==="
trivy version --format json 2>/dev/null | jq '{version: .Version, db: .VulnerabilityDB}'

echo ""
echo "=== Database Status ==="
trivy image --download-db-only 2>&1 | tail -3 || echo "DB up to date"

echo ""
echo "=== Available Scanners ==="
echo "  image     - Container image scanning"
echo "  fs        - Filesystem scanning"
echo "  repo      - Git repository scanning"
echo "  k8s       - Kubernetes cluster scanning"
echo "  config    - IaC misconfiguration scanning"
echo "  sbom      - SBOM generation"
```

## Core Helper Functions

```bash
#!/bin/bash

# Trivy wrapper with JSON output
trivy_cmd() {
    trivy "$@" --format json --quiet 2>/dev/null
}

# Severity filter helper
trivy_critical() {
    trivy "$@" --severity CRITICAL,HIGH --format json --quiet 2>/dev/null
}

# Summary extractor
trivy_summary() {
    jq '{
        total: [.Results[]?.Vulnerabilities[]?] | length,
        critical: [.Results[]?.Vulnerabilities[]? | select(.Severity == "CRITICAL")] | length,
        high: [.Results[]?.Vulnerabilities[]? | select(.Severity == "HIGH")] | length,
        medium: [.Results[]?.Vulnerabilities[]? | select(.Severity == "MEDIUM")] | length,
        low: [.Results[]?.Vulnerabilities[]? | select(.Severity == "LOW")] | length
    }'
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use `--format json` with jq for structured results
- Use `--severity CRITICAL,HIGH` to focus on important issues
- Use `--quiet` to suppress progress output

## Common Operations

### Container Image Scan

```bash
#!/bin/bash
IMAGE="${1:?Container image required}"

echo "=== Image Vulnerability Scan: $IMAGE ==="
trivy image "$IMAGE" --format json --quiet 2>/dev/null | jq '{
    image: .ArtifactName,
    os: (.Metadata.OS // {}),
    results: [.Results[] | {
        target: .Target,
        type: .Type,
        vulnerabilities: {
            total: (.Vulnerabilities // [] | length),
            critical: ([.Vulnerabilities[]? | select(.Severity == "CRITICAL")] | length),
            high: ([.Vulnerabilities[]? | select(.Severity == "HIGH")] | length)
        }
    }],
    top_critical: [.Results[].Vulnerabilities[]? | select(.Severity == "CRITICAL") | {
        id: .VulnerabilityID,
        package: .PkgName,
        installed: .InstalledVersion,
        fixed: .FixedVersion,
        title: .Title
    }] | .[0:5]
}'
```

### Filesystem and Repository Scan

```bash
#!/bin/bash
TARGET="${1:-.}"

echo "=== Filesystem Scan: $TARGET ==="
trivy fs "$TARGET" --format json --quiet --scanners vuln,secret,misconfig 2>/dev/null | jq '{
    vulnerabilities: {
        total: [.Results[]?.Vulnerabilities[]?] | length,
        critical: [.Results[]?.Vulnerabilities[]? | select(.Severity == "CRITICAL")] | length,
        high: [.Results[]?.Vulnerabilities[]? | select(.Severity == "HIGH")] | length
    },
    secrets: [.Results[]?.Secrets[]? | {
        rule: .RuleID,
        category: .Category,
        severity: .Severity,
        target: .Target
    }] | .[0:5],
    misconfigurations: [.Results[]?.Misconfigurations[]? | {
        id: .ID,
        title: .Title,
        severity: .Severity,
        type: .Type
    }] | .[0:5]
}'
```

### Kubernetes Cluster Scan

```bash
#!/bin/bash
echo "=== K8s Cluster Scan ==="
trivy k8s --report summary --format json --quiet 2>/dev/null | jq '{
    cluster_summary: {
        total_vulnerabilities: [.Resources[]?.Results[]?.Vulnerabilities[]?] | length,
        total_misconfigs: [.Resources[]?.Results[]?.Misconfigurations[]?] | length
    },
    affected_resources: [.Resources[]? | {
        namespace: .Namespace,
        kind: .Kind,
        name: .Name,
        vulns: ([.Results[]?.Vulnerabilities[]?] | length),
        misconfigs: ([.Results[]?.Misconfigurations[]?] | length)
    }] | sort_by(-.vulns) | .[0:10]
}'
```

### SBOM Generation

```bash
#!/bin/bash
TARGET="${1:?Target required (image or directory)}"
FORMAT="${2:-cyclonedx}"

echo "=== Generating SBOM ==="
if [[ "$TARGET" == *":"* ]] || [[ "$TARGET" == *"/"* && ! -d "$TARGET" ]]; then
    trivy image "$TARGET" --format "$FORMAT" --quiet 2>/dev/null | jq '{
        format: .bomFormat,
        components_count: (.components | length),
        component_types: ([.components[].type] | group_by(.) | map({type: .[0], count: length})),
        top_components: [.components[:10][] | {name: .name, version: .version, type: .type}]
    }' 2>/dev/null
else
    trivy fs "$TARGET" --format "$FORMAT" --quiet 2>/dev/null | jq '{
        format: .bomFormat,
        components_count: (.components | length),
        top_components: [.components[:10][] | {name: .name, version: .version, type: .type}]
    }' 2>/dev/null
fi
```

### Misconfiguration Scanning

```bash
#!/bin/bash
TARGET="${1:-.}"

echo "=== IaC Misconfiguration Scan ==="
trivy config "$TARGET" --format json --quiet 2>/dev/null | jq '{
    files_scanned: (.Results | length),
    issues: {
        critical: [.Results[]?.Misconfigurations[]? | select(.Severity == "CRITICAL")] | length,
        high: [.Results[]?.Misconfigurations[]? | select(.Severity == "HIGH")] | length,
        medium: [.Results[]?.Misconfigurations[]? | select(.Severity == "MEDIUM")] | length
    },
    top_issues: [.Results[]?.Misconfigurations[]? | select(.Severity == "CRITICAL" or .Severity == "HIGH") | {
        id: .ID,
        title: .Title,
        severity: .Severity,
        message: .Message,
        resolution: .Resolution
    }] | .[0:10]
}'
```

## Safety Rules

- **Scans are read-only** -- Trivy never modifies scanned targets
- **Image pulls may download large images** -- be aware of bandwidth and disk usage
- **K8s cluster scans require RBAC permissions** -- ensure service account has read access
- **Secret detection** may find false positives -- verify before reporting
- **SBOM output can be large** -- pipe to file for complex images

## Output Format

Present results as a structured report:
```
Analyzing Trivy Report
══════════════════════
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

- **Stale vulnerability database**: Run `trivy image --download-db-only` to update before scanning
- **Private registries**: Configure registry credentials in `~/.docker/config.json` or via env vars
- **OCI image format**: Some registries use OCI format -- use `--image-src` to specify source
- **Large images**: Scanning very large images can be slow -- use `--timeout` to prevent hangs
- **Unfixed vulnerabilities**: Many CVEs have no fix -- use `--ignore-unfixed` to focus on actionable items
- **Scanner selection**: Default scanners vary by subcommand -- use `--scanners` to be explicit
- **Cache management**: Trivy caches DB and scan results -- clear with `trivy clean` if stale
- **Exit codes**: Trivy returns non-zero on findings -- use `--exit-code 0` in CI to prevent false failures
