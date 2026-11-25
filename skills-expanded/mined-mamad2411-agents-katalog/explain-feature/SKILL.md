---
name: explain-feature
description: Alias for `feature-summary` (kept for backward compatibility)
disable-model-invocation: true
---

# explain-feature (Alias)

This skill is a compatibility alias. Delegate to `feature-summary` for the actual workflow.

## Alias Behavior

1. Execute `feature-summary`.
2. Keep the output concise and handoff-friendly.
3. Save to `feature_summary.md` unless the caller provides a different output path.

## Migration Note

Prefer invoking `feature-summary` directly in new prompts, docs, and automations.
