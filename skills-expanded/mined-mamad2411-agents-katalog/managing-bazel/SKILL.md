---
name: managing-bazel
description: |
  Use when working with Bazel — bazel build system management. Covers BUILD file
  analysis, target querying, dependency graphs, remote execution, caching
  configuration, and build performance profiling. Use when managing Bazel
  workspaces, debugging build failures, querying targets, or optimizing build
  performance.
connection_type: bazel
preload: false
---

# Bazel Build System Management Skill

Manage and analyze Bazel workspaces, build targets, dependencies, and caching.

## MANDATORY: Discovery-First Pattern

**Always check current Bazel workspace and build configuration before modifying targets.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Workspace Configuration ==="
cat WORKSPACE 2>/dev/null | head -20 || cat WORKSPACE.bazel 2>/dev/null | head -20
cat MODULE.bazel 2>/dev/null | head -20

echo ""
echo "=== .bazelrc Configuration ==="
cat .bazelrc 2>/dev/null | head -15

echo ""
echo "=== Bazel Version ==="
bazel version 2>/dev/null | head -3

echo ""
echo "=== Top-Level Packages ==="
ls */BUILD */BUILD.bazel 2>/dev/null | head -15
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== All Build Targets ==="
bazel query '//...' 2>/dev/null | head -20

echo ""
echo "=== Target Types Summary ==="
bazel query '//...' --output=label_kind 2>/dev/null | awk '{print $1}' | sort | uniq -c | sort -rn | head -10

echo ""
echo "=== External Dependencies ==="
bazel query 'deps(//...)' --output=label 2>/dev/null | grep '@' | sed 's|//.*||' | sort -u | head -10
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Summarize target counts by rule type
- List external dependencies concisely
- Report build timing from profiles

## Common Operations

### Dependency Graph Query

```bash
#!/bin/bash
TARGET="${1:?Target required (e.g., //src:main)}"
echo "=== Dependencies for $TARGET ==="
bazel query "deps($TARGET)" --output=label 2>/dev/null | head -20
echo ""
echo "=== Reverse Dependencies ==="
bazel query "rdeps(//..., $TARGET)" --output=label 2>/dev/null | head -10
```

### Build Performance Profile

```bash
#!/bin/bash
echo "=== Build Profile ==="
bazel build //... --profile=/tmp/bazel_profile.json 2>/dev/null
cat /tmp/bazel_profile.json 2>/dev/null | jq '{
  total_duration: .traceEvents[-1].ts,
  critical_path: [.traceEvents[] | select(.cat == "critical path") | .name] | .[0:5]
}' 2>/dev/null
```

## Safety Rules

- **Never run `bazel clean --expunge`** without understanding the full rebuild cost
- **Test BUILD file changes** with `bazel build --check_visibility` before committing
- **Remote execution credentials** must be stored in CI secrets, not in .bazelrc
- **Review external dependency updates** carefully -- Bazel pins exact versions for reproducibility

## Output Format

Present results as a structured report:
```
Managing Bazel Report
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

