---
name: managing-npm-registry
description: |
  Use when working with Npm Registry — npm registry and package management.
  Covers package publishing, version management, registry configuration, access
  controls, audit scanning, and dependency analysis. Use when managing npm
  packages, configuring private registries, auditing vulnerabilities, or
  analyzing package download metrics.
connection_type: npm-registry
preload: false
---

# npm Registry Management Skill

Manage and analyze npm packages, registries, access controls, and security audits.

## MANDATORY: Discovery-First Pattern

**Always check current npm configuration and registry settings before modifying packages.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== npm Configuration ==="
npm config list 2>/dev/null | head -15

echo ""
echo "=== Registry Settings ==="
npm config get registry 2>/dev/null
cat .npmrc 2>/dev/null | grep -v '//.*:_authToken' | head -10

echo ""
echo "=== Package Info ==="
cat package.json 2>/dev/null | jq '{
  name: .name,
  version: .version,
  private: .private,
  publishConfig: .publishConfig
}' 2>/dev/null

echo ""
echo "=== npm Version ==="
npm --version 2>/dev/null
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Security Audit ==="
npm audit --json 2>/dev/null | jq '{
  total: .metadata.totalDependencies,
  vulnerabilities: .metadata.vulnerabilities
}' 2>/dev/null

echo ""
echo "=== Outdated Packages ==="
npm outdated --json 2>/dev/null | jq 'to_entries | map({
  package: .key,
  current: .value.current,
  wanted: .value.wanted,
  latest: .value.latest
}) | .[0:10]' 2>/dev/null

echo ""
echo "=== Dependency Tree Depth ==="
npm ls --all --depth=0 2>/dev/null | tail -5
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Summarize audit results by severity
- List outdated packages with version gaps
- Never expose auth tokens in output

## Common Operations

### Package Info Lookup

```bash
#!/bin/bash
PACKAGE="${1:?Package name required}"
echo "=== Package Info: $PACKAGE ==="
npm view "$PACKAGE" --json 2>/dev/null | jq '{
  name: .name,
  version: .version,
  description: .description,
  license: .license,
  downloads: .downloads,
  maintainers: [.maintainers[]?.name]
}' 2>/dev/null
```

### Publish Dry Run

```bash
#!/bin/bash
echo "=== Publish Preview ==="
npm publish --dry-run 2>&1 | head -20
npm pack --dry-run 2>&1 | head -15
```

## Safety Rules

- **Never expose npm tokens** in logs or .npmrc files committed to git
- **Use `npm publish --dry-run`** before actual publishing
- **Review `npm audit`** results before deploying to production
- **Use scoped packages** for private packages to avoid name squatting

## Output Format

Present results as a structured report:
```
Managing Npm Registry Report
════════════════════════════
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

