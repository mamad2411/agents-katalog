---
name: pd-lottie-delivery
description: "Prepare and validate timeline vector animation for Lottie or dotLottie delivery."
license: MIT (original guidance; linked tools and assets keep their own licenses)
---

# Lottie Delivery

Choose Lottie for supported, largely timeline-driven vector motion; choose Rive or application state for complex interactive behavior. Keep the original authored timeline, expressions/assets and export configuration. Do not assume every After Effects feature is represented by the runtime format.

Use the installed exporter's supported-feature list as an executable constraint. Build a minimal representative frame/sequence before committing to effects, fonts, masks, gradients or 3D layers. Distinguish raw Lottie JSON from a dotLottie archive and record the exact player/exporter versions. Review payload and dependencies before embedding third-party animation files.

Inspect first, intermediate, last and loop-boundary frames in both the authoring app and target runtime. Compare masks, text, easing, trim paths, raster assets, alpha and bounding boxes. If a required effect cannot transfer faithfully, simplify the design or use an explicitly selected video/sprite alternative rather than shipping silent degradation.

In the consumer, test play/pause/seek, reduced motion, viewport visibility, rerender/unmount cleanup and keyboard-equivalent actions. Avoid multiple uncoordinated animation loops. A file that parses is not proof that the intended animation was delivered; retain visual differences and unsupported feature findings in the production record.

## Related contracts

Read the repository's `docs/visual-production/E2E-CONTRACT.md`, `ALL-FORMS.md`, and source catalog for the selected tool. In the standalone kit these are under `docs/` and `resources/`. Preserve exact failure/blocked states and the existing source/evidence owners.
