---
name: design-understand
description: Use when an existing screen, screenshot, or layout must be understood before UI changes, visual polish, or redesign. Skip backend maintenance and greenfield product direction without an existing surface.
---

# Understand an Existing Screen

Identify what the user is trying to accomplish before choosing visual changes. For a new product without an existing screen, use `product-designer` instead.

1. Record the user's goal, primary action, secondary actions, core objects, and current state. Separate observed behavior from assumptions and questions that affect the change.
2. Retrieve task context with `npx --no-install ai-design-context context --task "<matching phrase or known slug>" --intent implement`. Read the returned research and rules; use `--platform mobile` for narrow or touch-first screens. Record unresolved knowledge needs instead of inventing rules.
3. Inspect the actual screen or supplied image with the available browser/image tools. Use source inspection to identify existing components, semantic tokens, and responsive conventions. A screenshot describes one state, not the entire interaction model.
4. Diagnose hierarchy, layout, typography, spacing, component consistency, and relevant default, loading, empty, error, success, and disabled states. Explain how competition for attention affects the primary task. Distinguish concrete friction from an unsupported preference about product feel.
5. Propose the smallest changes that serve the stated goal. Keep business logic and the existing stack. New visual directions require user intent and upstream references, not only taste.

## Handoff

Return: **screen and user goal | primary/secondary actions | observed strengths and problems | assumptions and missing states | ranked improvements with graph/reference evidence | affected components/tokens | verification plan**. Rank up to three consequential problems when present; do not invent three defects to fill a quota.

Use `visual-designer` or `interaction-designer` for the selected change, `reference-driven-design` for requested new visual directions, and `visual-qa` after implementation. Preserve the evidence limits of all `draft` and `seed` graph objects.

Graph anchors: `RULE-00001` / `PRD-001` for the primary repeated action, `RULE-00004` / `IA-002` for object structure, `RULE-00008` / `VIS-001` for existing tokens, and `CHECK-00001` for state and review coverage. Their source research remains the basis of design advice.
