---
name: link-validation
description: Universal link validation using lychee for Claude Code sessions. Detect broken links and path policy violations on demand.
allowed-tools: Bash, Read, Glob
triggers:
  - link validation
  - broken links
  - lychee
  - check links
  - markdown links
---

# Link Validation Skill

Validates markdown links in your workspace using [lychee](https://github.com/lycheeverse/lychee).

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

## When to Use This Skill

Use this skill when:

- Checking for broken links in markdown files
- Validating link paths before committing documentation
- Detecting path policy violations (absolute paths, excessive traversal)

## What It Does

When invoked, this skill:

1. **Discovers** all markdown files in your workspace
2. **Runs lychee** to check for broken links
3. **Lints paths** for policy violations (absolute paths, excessive traversal)
4. **Outputs JSON** results for programmatic consumption

## Requirements

- [lychee](https://github.com/lycheeverse/lychee) installed (`brew install lychee`)
- Python 3.11+ and uv

## Output

Results are written to `.link-check-results.md` in your workspace:

```markdown
# Link Check Results

**Correlation ID**: `01JEGQXV8KHTNF3YD8G7ZC9XYK`

## Lychee Link Validation

No broken links found.

## Path Policy Violations

No path violations found.
```

## Path Policy Rules

| Rule                 | Severity | Description                            |
| -------------------- | -------- | -------------------------------------- |
| NO_ABSOLUTE_PATHS    | Error    | Filesystem absolute paths not allowed  |
| NO_PARENT_ESCAPES    | Warning  | Excessive `../` may escape repository  |
| MARKETPLACE_RELATIVE | Warning  | Plugins should use `./` relative paths |

## Configuration

Override the default lychee config by placing `.lycheerc.toml` in your workspace root.

See [config/lychee.toml](../../config/lychee.toml) for the default configuration.

## References

- [ADR: Link Checker Plugin Extraction](../../../../docs/adr/2025-12-11-link-checker-plugin-extraction.md)
- [Design Spec](../../../../docs/design/2025-12-11-link-checker-plugin-extraction/spec.md)
- [lychee Documentation](https://github.com/lycheeverse/lychee)

---

## Troubleshooting

| Issue                | Cause                | Solution                           |
| -------------------- | -------------------- | ---------------------------------- |
| lychee not found     | Not installed        | Run `mise install lychee`          |
| Too many 403 errors  | Rate limiting        | Add rate limit to .lycheerc.toml   |
| Relative path errors | Wrong base directory | Run from repository root           |
| False positives      | Dynamic content      | Add URL pattern to exclude list    |
| Timeout on links     | Slow external sites  | Increase timeout in config         |
| Cache issues         | Stale cached results | Clear cache with `--no-cache` flag |


## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did the command succeed?** — If not, fix the instruction or error table that caused the failure.
2. **Did parameters or output change?** — If the underlying tool's interface drifted, update Usage examples and Parameters table to match.
3. **Was a workaround needed?** — If you had to improvise (different flags, extra steps), update this SKILL.md so the next invocation doesn't need the same workaround.

Only update if the issue is real and reproducible — not speculative.
