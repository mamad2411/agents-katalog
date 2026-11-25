---
name: z-craft
description: Autonomous Software Craftsmanship & Disciplined Vibe-Coding Engine. Translates natural language vibes into anti-slop, production-grade frontend & product software with UX micro-contracts, AST linter, and live canvas preview.
---

# Z-Craft: Autonomous Software Craftsmanship

Use `z-craft` when building or refining user interfaces, web applications, dashboards, or desktop UI (React, Tailwind, WPF XAML, DevExpress).

## When to Use

1. **User asks to create or redesign a UI screen from a prompt**:
   - Call `zcraft_spec` to synthesize the prompt into a 4-state micro-contract.
   - Present the checklist to the user or immediately implement matching states.
2. **User asks for a live visual preview or demo**:
   - Call `zcraft_preview` to generate an interactive HTML/Tailwind canvas widget.
3. **Validating code for AI-Slop**:
   - Run `zcraft_lint_ui` before finalizing frontend code.
   - Fix all arbitrary hex colors and neon gradients.
4. **Before radical visual experiments**:
   - Call `zcraft_checkpoint(action: "create", name: "experiment_name")` to guarantee instant rollback if the vibe doesn't land.

## Core MCP Tools

- `zcraft_spec`: Generate UX micro-contract with Default, Loading, Empty, and Error state definitions.
- `zcraft_lint_ui`: AST & pattern scanner detecting arbitrary hex colors, neon gradients, dead clicks, and missing states.
- `zcraft_preview`: Produces a self-contained, interactive HTML preview widget for live visual verification.
- `zcraft_checkpoint`: Shadow micro-snapshots for zero-risk creative branching.
- `zcraft_status`: Check active craftsmanship metrics.

## Engineering Invariants

1. **Zero AI Slop (`R_ANTI_SLOP`)**: Never introduce purple/indigo gradient blobs or arbitrary non-token hex codes.
2. **Mandatory 4-State Matrix**: Always account for Default, Loading, Empty, and Error states.
3. **High Density & Professionalism**: Default to compact enterprise spacing (36–40px rows, 4px/8px grid, crisp borders).
