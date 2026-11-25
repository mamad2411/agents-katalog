---
id: skill-raster-ui-asset-design
type: agent-skill
status: reviewed
created: 2026-06-21
updated: 2026-06-21
name: raster-ui-asset-design
description: Design and integrate generated raster images for child-agent UIs only when the asset supports a concrete workflow state, preview, comparison, consequence or operator control.
version: 0.1.0
topics:
  - agent-skills
  - raster-ui-assets
  - image-generation
  - child-agent-ui
tools:
  - Pritha
  - Codex
  - imagegen
  - OpenAI image_generation
sources:
  - 04_standards/raster-ui-assets-for-child-agents.md
  - 07_workflows/raster-ui-asset-generation.md
  - 03_reviews/2026-06-21-raster-image-generation-ui-source-batch-review.md
related:
  workflows:
    - 07_workflows/agent-skill-pack-selection.md
    - 07_workflows/raster-ui-asset-generation.md
  standards:
    - 04_standards/raster-ui-assets-for-child-agents.md
    - 04_standards/agent-interface-experience.md
source: pritha-memory
source_paths:
  - 04_standards/raster-ui-assets-for-child-agents.md
  - 07_workflows/raster-ui-asset-generation.md
  - 03_reviews/2026-06-21-raster-image-generation-ui-source-batch-review.md
review_status: reviewed
trust_level: local-reviewed
requires_toolsets:
  - filesystem
  - markdown
  - image-generation
risk_level: medium
tags:
  - raster-assets
  - ui
  - imagegen
  - accessibility
---

# Raster UI Asset Design

## When to Use

Use when Pritha or a child agent is designing a non-chat UI and a raster image
may help users inspect workflow state, compare visual candidates, preview
generated artifacts, understand consequences, or review media/product/lesson
content.

## Procedure

1. Start from the child-agent workflow, not from visual style. Record user
   journey, visibility needs, control needs, state model, side-effect policy,
   rendering boundary, framework/stack, fallback, mobile/accessibility, privacy
   prompts and readiness check.
2. Reject raster if DOM/CSS/native UI or SVG would satisfy the job more clearly.
3. Write a raster asset spec before generation: target component, state shown,
   user-visible purpose, controls around the image, output sizes/formats,
   reference image roles, alt/fallback and privacy boundary.
4. Use prompt-plus-controls in the dialogue: style chips, aspect ratio, generate
   or edit mode, preview thumbnails and accept/reject/regenerate/edit actions.
5. Use Codex `imagegen` for normal project-bound assets. Use API/CLI fallback
   only when selected by the contract and current docs have been checked.
6. Save accepted assets in the child-agent workspace and wire them into real UI
   components. Keep text, controls, warnings and status outside the image.
7. Verify mobile crop/readability, responsive variants, file size, format
   fallback, alt/fallback correctness, privacy retention and user controls.
8. Record final path, prompt/spec, variants, tool path and verification result in
   the scaffold report or UI notes.

## Pitfalls

- Do not generate decorative dashboards just because image generation is
  available.
- Do not hide action buttons, warnings, logs, task state or approval text inside
  pixels.
- Do not send private screenshots or reference images to hosted generation
  without a contract-selected privacy boundary.
- Do not leave project-referenced generated images outside the workspace.
- Do not treat AVIF/WebP, transparency or image-generation model options as
  timeless; recheck current docs before implementation.

## Verification

- The asset has a workflow purpose and target component.
- Real UI owns controls, text, status and side effects.
- Final assets live in the workspace with stable paths.
- Responsive, accessibility, file size and privacy checks are recorded.
- The user can accept, reject, edit or regenerate generated candidates when the
  asset is part of an interactive design flow.
