---
name: managing-crates-io
description: |
  Use when working with Crates Io — crates.io Rust package registry management.
  Covers crate publishing, version management, dependency resolution, feature
  flags, build configurations, and crate metadata analysis. Use when managing
  Rust crates, publishing to crates.io, analyzing dependency trees, or
  configuring feature flags.
connection_type: crates-io
preload: false
---

# crates.io Registry Management Skill

Manage and analyze Rust crates, publishing, dependencies, and feature configurations.

## MANDATORY: Discovery-First Pattern

**Always check current Cargo.toml configuration before modifying crate settings.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Crate Configuration ==="
cat Cargo.toml 2>/dev/null | head -25

echo ""
echo "=== Workspace Members ==="
grep -A20 '\[workspace\]' Cargo.toml 2>/dev/null | grep 'members' -A10 | head -12

echo ""
echo "=== Rust Toolchain ==="
rustc --version 2>/dev/null
cargo --version 2>/dev/null
cat rust-toolchain.toml 2>/dev/null | head -5
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Dependency Tree ==="
cargo tree --depth=1 2>/dev/null | head -20

echo ""
echo "=== Outdated Dependencies ==="
cargo outdated 2>/dev/null | head -15

echo ""
echo "=== Security Audit ==="
cargo audit 2>/dev/null | tail -15
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Summarize dependency trees at depth 1
- Report audit findings by severity
- List feature flags with their dependencies

## Common Operations

### Crate Lookup

```bash
#!/bin/bash
CRATE="${1:?Crate name required}"
echo "=== Crate Info: $CRATE ==="
curl -s "https://crates.io/api/v1/crates/${CRATE}" | jq '{
  name: .crate.name,
  max_version: .crate.max_version,
  downloads: .crate.downloads,
  description: .crate.description,
  repository: .crate.repository
}' 2>/dev/null
```

### Publish Dry Run

```bash
#!/bin/bash
echo "=== Publish Preview ==="
cargo publish --dry-run 2>&1 | tail -15
cargo package --list 2>/dev/null | head -15
```

## Safety Rules

- **Use `cargo publish --dry-run`** before actual publishing
- **Run `cargo audit`** before releases to catch known vulnerabilities
- **Never yank crate versions** without publishing a fix first
- **Review feature flag combinations** for compile-time correctness

## Output Format

Present results as a structured report:
```
Managing Crates Io Report
═════════════════════════
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

