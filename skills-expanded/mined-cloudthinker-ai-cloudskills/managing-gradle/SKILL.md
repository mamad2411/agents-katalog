---
name: managing-gradle
description: |
  Use when working with Gradle — gradle build system management. Covers build
  script analysis, task execution, dependency resolution, build scans, plugin
  management, and multi-project builds. Use when managing Gradle projects,
  debugging dependency conflicts, analyzing build performance, or configuring
  build caching.
connection_type: gradle
preload: false
---

# Gradle Build System Management Skill

Manage and analyze Gradle builds, dependencies, tasks, and multi-project configurations.

## MANDATORY: Discovery-First Pattern

**Always check current Gradle configuration and project structure before modifying builds.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Gradle Version ==="
./gradlew --version 2>/dev/null | head -5

echo ""
echo "=== Project Structure ==="
cat settings.gradle 2>/dev/null || cat settings.gradle.kts 2>/dev/null | head -20

echo ""
echo "=== Build Script ==="
ls build.gradle build.gradle.kts 2>/dev/null
ls */build.gradle */build.gradle.kts 2>/dev/null | head -10

echo ""
echo "=== Gradle Properties ==="
cat gradle.properties 2>/dev/null | grep -v '^#' | grep -v '^$' | head -15
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Available Tasks ==="
./gradlew tasks --all 2>/dev/null | grep -E '^\w' | head -20

echo ""
echo "=== Dependencies (compile) ==="
./gradlew dependencies --configuration=compileClasspath 2>/dev/null | head -25

echo ""
echo "=== Build Cache Config ==="
grep -r 'buildCache\|cacheability' build.gradle* gradle.properties 2>/dev/null | head -10
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Summarize dependency trees to top-level dependencies
- Group tasks by lifecycle phase
- Report build scan URLs when available

## Common Operations

### Dependency Conflict Resolution

```bash
#!/bin/bash
echo "=== Dependency Insight ==="
DEPENDENCY="${1:?Dependency group:artifact required}"
./gradlew dependencyInsight --dependency "$DEPENDENCY" 2>/dev/null | head -20
```

### Build Performance

```bash
#!/bin/bash
echo "=== Build Scan ==="
./gradlew build --scan 2>&1 | grep -E 'BUILD|https://gradle' | head -5

echo ""
echo "=== Build Cache Stats ==="
ls -la ~/.gradle/caches/ 2>/dev/null | head -10
du -sh ~/.gradle/caches/ 2>/dev/null
```

## Safety Rules

- **Never publish artifacts** without verifying version and credentials
- **Use `--dry-run`** to preview task execution before running destructive tasks
- **Dependency locks** should be committed and reviewed for unexpected changes
- **Build scan data** may contain sensitive info -- review sharing settings

## Output Format

Present results as a structured report:
```
Managing Gradle Report
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

