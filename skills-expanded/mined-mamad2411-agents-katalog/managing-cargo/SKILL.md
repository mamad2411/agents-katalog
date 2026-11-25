---
name: managing-cargo
description: |
  Use when working with Cargo — cargo Rust build and package management. Covers
  build configuration, workspace management, feature flags, build profiles,
  cross-compilation, and build script analysis. Use when managing Cargo
  workspaces, configuring build profiles, debugging compilation issues, or
  optimizing build performance.
connection_type: cargo
preload: false
---

# Cargo Build and Package Management Skill

Manage and analyze Cargo builds, workspaces, features, and build configurations.

## MANDATORY: Discovery-First Pattern

**Always check current Cargo.toml and workspace configuration before modifying builds.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Cargo.toml ==="
cat Cargo.toml 2>/dev/null | head -25

echo ""
echo "=== Workspace Structure ==="
grep -A15 '\[workspace\]' Cargo.toml 2>/dev/null | head -15

echo ""
echo "=== Build Profiles ==="
grep -A5 '\[profile' Cargo.toml 2>/dev/null | head -15

echo ""
echo "=== Cargo Version ==="
cargo --version 2>/dev/null
rustc --version 2>/dev/null
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Feature Flags ==="
grep -A20 '\[features\]' Cargo.toml 2>/dev/null | head -15

echo ""
echo "=== Build Dependencies ==="
grep -A20 '\[build-dependencies\]' Cargo.toml 2>/dev/null | head -10

echo ""
echo "=== Target Configuration ==="
grep -A5 '\[\[bin\]\]\|\[lib\]' Cargo.toml 2>/dev/null | head -15

echo ""
echo "=== Build Timing ==="
cargo build --timings 2>/dev/null | tail -5
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Summarize workspace members and their types
- List feature flags with dependencies
- Report build profile optimizations

## Common Operations

### Build Analysis

```bash
#!/bin/bash
echo "=== Build Check ==="
cargo check 2>&1 | tail -10

echo ""
echo "=== Clippy Lints ==="
cargo clippy 2>&1 | tail -15
```

### Cross-Compilation

```bash
#!/bin/bash
echo "=== Installed Targets ==="
rustup target list --installed 2>/dev/null

echo ""
echo "=== Available Targets ==="
rustup target list 2>/dev/null | grep -E 'linux|darwin|windows' | head -10
```

## Safety Rules

- **Run `cargo check`** before full builds to catch errors quickly
- **Test with `--release` profile** before deploying -- debug and release can behave differently
- **Review feature flag combinations** for compile-time correctness
- **Use `cargo clippy`** to catch common Rust anti-patterns before merging

## Output Format

Present results as a structured report:
```
Managing Cargo Report
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

