---
name: managing-hex-pm
description: |
  Use when working with Hex Pm — hex.pm Elixir/Erlang package registry
  management. Covers package publishing, dependency resolution, Mix
  configuration, Hex organization management, and package metadata. Use when
  managing Hex packages, publishing Elixir/Erlang libraries, resolving Mix
  dependency conflicts, or auditing package security.
connection_type: hex-pm
preload: false
---

# Hex.pm Registry Management Skill

Manage and analyze Elixir/Erlang packages, Hex publishing, and Mix dependencies.

## MANDATORY: Discovery-First Pattern

**Always check current mix.exs configuration before modifying packages.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Mix Project ==="
cat mix.exs 2>/dev/null | head -25

echo ""
echo "=== Hex Info ==="
mix hex.info 2>/dev/null | head -10

echo ""
echo "=== Elixir/Erlang Version ==="
elixir --version 2>/dev/null | head -3
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Dependencies ==="
mix deps 2>/dev/null | head -15

echo ""
echo "=== Outdated Deps ==="
mix hex.outdated 2>/dev/null | head -15

echo ""
echo "=== Dependency Tree ==="
mix deps.tree --depth=1 2>/dev/null | head -20

echo ""
echo "=== Security Audit ==="
mix hex.audit 2>/dev/null | head -10
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- List dependencies with version constraints
- Report outdated packages with available versions
- Never expose Hex API keys in output

## Common Operations

### Package Lookup

```bash
#!/bin/bash
PACKAGE="${1:?Package name required}"
echo "=== Hex Package: $PACKAGE ==="
curl -s "https://hex.pm/api/packages/${PACKAGE}" | jq '{
  name: .name,
  latest: .releases[0].version,
  downloads: .downloads.all,
  description: .meta.description,
  licenses: .meta.licenses
}' 2>/dev/null
```

### Publish Preview

```bash
#!/bin/bash
echo "=== Publish Preview ==="
mix hex.publish --dry-run 2>&1 | tail -15
```

## Safety Rules

- **Use `mix hex.publish --dry-run`** before publishing
- **Run `mix hex.audit`** to check for retired packages
- **Lock dependency versions** with mix.lock for reproducible builds
- **Never commit Hex API keys** to version control

## Output Format

Present results as a structured report:
```
Managing Hex Pm Report
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

