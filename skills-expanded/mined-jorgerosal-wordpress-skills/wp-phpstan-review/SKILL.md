---
name: wp-phpstan-review
description: WordPress PHPStan review for Codex. Use when reviewing phpstan config, baseline strategy, CI analysis setup, WordPress stubs, or `szepeviktor/phpstan-wordpress` integration in WordPress projects.
---

# Codex WordPress PHPStan Review

## Purpose

Use this skill when Codex should review PHPStan setup for WordPress projects, including config structure, baseline discipline, CI behavior, and WordPress-specific extension wiring.

## Focus Areas

- `phpstan.neon` / `.dist` structure
- Baseline and ignore strategy
- CI integration and Composer wiring
- WordPress-specific extension and stubs

## Workflow

1. Identify config files, baseline files, and CI entrypoints.
2. Check whether PHPStan is truly analysing first-party WordPress code.
3. Review baseline use, extension loading, and local-vs-CI consistency.
4. Load only the needed shared references from `../../claude-skills/wp-phpstan-review/references/`.
5. Report findings with severity, file references, impact, and fixes.

## References

- `../../claude-skills/wp-phpstan-review/references/config-and-bootstrap.md`
- `../../claude-skills/wp-phpstan-review/references/baseline-and-ci.md`
- `../../claude-skills/wp-phpstan-review/references/wordpress-stubs-guide.md`
