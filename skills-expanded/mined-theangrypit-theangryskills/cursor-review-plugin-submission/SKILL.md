---
name: cursor-review-plugin-submission
description: Audit a Cursor plugin for marketplace readiness. Use when validating manifests, component metadata, discovery paths, and submission quality before publishing.
---

## Runtime selection

Before runtime-dependent work, read [execution selection](references/runtime/selection.md). In a verified T3 host follow [the T3 contract](references/runtime/t3.md) and its method reference; the inline section below is the native Codex branch, not literal T3 dispatch. Outside T3, native Codex follows that inline branch unchanged. If the host is ambiguous or a required capability is unavailable, report the gap; a permission refusal never authorizes switching branches.

## Native Codex branch

# Review a Cursor plugin submission

Perform a read-only structural audit of an explicitly supplied local Cursor plugin.

## Workflow

1. Run `python3 scripts/cursor_plugin_submission_audit.py <plugin-root>`.
2. Review manifest parsing and metadata, bounded relative component paths, component discovery, required frontmatter fields, and README presence.
3. Report `STRUCTURAL_PASS`, `REVIEW_REQUIRED`, `BLOCKED`, or `ERROR` exactly as returned, with the concrete issues.
4. Escalate hooks, MCP server declarations, active components, marketplace uniqueness, runtime behavior, and external publication for separate human review. Never execute them during this audit.
5. State that `STRUCTURAL_PASS` is a local structural result, not a marketplace acceptance or publication recommendation.

The adapter performs no activation, installation, network access, credential use, or external write. The upstream `needs_human_review` finding remains recorded for active submission surfaces.
