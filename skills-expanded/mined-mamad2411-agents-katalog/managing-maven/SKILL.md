---
name: managing-maven
description: |
  Use when working with Maven — maven build system management. Covers POM
  analysis, dependency management, plugin configuration, multi-module builds,
  repository settings, and lifecycle phases. Use when managing Maven projects,
  resolving dependency conflicts, analyzing build lifecycles, or configuring
  repository mirrors.
connection_type: maven
preload: false
---

# Maven Build System Management Skill

Manage and analyze Maven projects, dependencies, plugins, and build lifecycles.

## MANDATORY: Discovery-First Pattern

**Always check current POM configuration and project structure before modifying builds.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Maven Version ==="
mvn --version 2>/dev/null | head -3

echo ""
echo "=== Project Info ==="
mvn help:evaluate -Dexpression=project.groupId -q -DforceStdout 2>/dev/null
mvn help:evaluate -Dexpression=project.artifactId -q -DforceStdout 2>/dev/null
mvn help:evaluate -Dexpression=project.version -q -DforceStdout 2>/dev/null

echo ""
echo "=== Module Structure ==="
grep -E '<module>' pom.xml 2>/dev/null | head -15

echo ""
echo "=== Active Profiles ==="
mvn help:active-profiles 2>/dev/null | grep -v '^\[' | head -10
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Dependency Tree ==="
mvn dependency:tree -DoutputType=text 2>/dev/null | head -30

echo ""
echo "=== Dependency Conflicts ==="
mvn dependency:tree -Dverbose 2>/dev/null | grep 'omitted for conflict' | head -10

echo ""
echo "=== Plugin List ==="
mvn help:effective-pom 2>/dev/null | grep '<artifactId>' | sort -u | head -15
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Summarize dependency trees to direct dependencies
- Highlight version conflicts and overrides
- Report effective POM settings concisely

## Common Operations

### Dependency Analysis

```bash
#!/bin/bash
echo "=== Unused Dependencies ==="
mvn dependency:analyze 2>/dev/null | grep -E 'Used undeclared|Unused declared' | head -10
```

### Build Lifecycle

```bash
#!/bin/bash
echo "=== Effective POM Settings ==="
mvn help:effective-settings 2>/dev/null | grep -A5 '<server>\|<mirror>' | head -20

echo ""
echo "=== Repository Configuration ==="
mvn help:effective-pom 2>/dev/null | grep -A3 '<repository>' | head -15
```

## Safety Rules

- **Never deploy snapshots to release repositories** -- verify version before `mvn deploy`
- **Review dependency:analyze** output before removing dependencies
- **Repository credentials** must be in settings.xml, never in pom.xml
- **Lock dependency versions** in dependencyManagement to avoid transitive surprises

## Output Format

Present results as a structured report:
```
Managing Maven Report
═════════════════════
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

