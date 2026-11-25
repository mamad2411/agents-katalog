---
name: wp-test-strategy
description: WordPress test strategy guidance for Codex. Use when deciding what to test, how deeply to test it, and which mix of unit, integration, and E2E coverage fits a WordPress change.
---

# Codex WordPress Test Strategy

## Purpose

Use this skill when Codex should recommend the right testing strategy for a WordPress feature, bug fix, migration, block, theme, REST API, or WooCommerce flow.

## Focus Areas

- Unit vs integration vs E2E tradeoffs
- High-risk WordPress surfaces needing coverage
- Existing test discovery and gap analysis
- Release-focused regression planning

## Workflow

1. Identify the change surface and failure mode.
2. Match the risk to the lightest test that gives confidence.
3. Review existing tests and likely coverage gaps.
4. Load only the needed shared references from `../../claude-skills/wp-test-strategy/references/`.
5. Report prioritized testing recommendations with rationale.

## References

- `../../claude-skills/wp-test-strategy/references/test-layer-guide.md`
- `../../claude-skills/wp-test-strategy/references/wordpress-test-scenarios.md`

