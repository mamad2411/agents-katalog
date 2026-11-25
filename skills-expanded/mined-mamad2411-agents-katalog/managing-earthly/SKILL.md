---
name: managing-earthly
description: |
  Use when working with Earthly — earthly build system management. Covers
  Earthfile configuration, target analysis, artifact management, caching
  strategies, satellite builds, and CI integration. Use when managing Earthly
  builds, debugging targets, optimizing cache utilization, or configuring remote
  runners.
connection_type: earthly
preload: false
---

# Earthly Build System Management Skill

Manage and analyze Earthly builds, targets, artifacts, and remote execution.

## MANDATORY: Discovery-First Pattern

**Always check current Earthfile configuration and target structure before modifying builds.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Earthfile ==="
cat Earthfile 2>/dev/null | head -30

echo ""
echo "=== Earthly Version ==="
earthly --version 2>/dev/null

echo ""
echo "=== Available Targets ==="
grep -E '^\w+:' Earthfile 2>/dev/null | sed 's/://' | head -15

echo ""
echo "=== Nested Earthfiles ==="
find . -name "Earthfile" -not -path "*/node_modules/*" 2>/dev/null | head -10
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Target Dependencies ==="
grep -E '^\w+:|BUILD|COPY|FROM' Earthfile 2>/dev/null | head -25

echo ""
echo "=== Artifacts ==="
grep -E 'SAVE ARTIFACT|SAVE IMAGE' Earthfile 2>/dev/null | head -10

echo ""
echo "=== Cache Mounts ==="
grep -E 'CACHE|--mount.*cache' Earthfile 2>/dev/null | head -10

echo ""
echo "=== Satellite Status ==="
earthly sat ls 2>/dev/null | head -5
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- List targets with their FROM base images
- Summarize artifact outputs concisely
- Report satellite/remote runner status

## Common Operations

### Build Target

```bash
#!/bin/bash
TARGET="${1:?Target name required}"
echo "=== Building +$TARGET ==="
earthly "+$TARGET" 2>&1 | tail -20
```

### Cache Analysis

```bash
#!/bin/bash
echo "=== Cache Usage ==="
earthly prune --dry-run 2>/dev/null | head -10

echo ""
echo "=== Image Cache ==="
docker images --filter "label=dev.earthly" --format "table {{.Repository}}\t{{.Size}}\t{{.CreatedAt}}" 2>/dev/null | head -10
```

## Safety Rules

- **Never run `earthly prune -a`** without confirming rebuild cost
- **Use secrets via `--secret`** flag, never hardcode in Earthfiles
- **Test multi-platform builds** locally before pushing to CI
- **Review SAVE IMAGE targets** to avoid pushing unintended images to registries

## Output Format

Present results as a structured report:
```
Managing Earthly Report
═══════════════════════
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

