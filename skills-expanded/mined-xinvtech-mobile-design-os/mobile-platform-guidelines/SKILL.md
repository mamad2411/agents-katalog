---
name: mobile-platform-guidelines
description: Apply and review iOS and Android native behavior rules across navigation, insets, permissions, system surfaces, accessibility, adaptive layouts, lifecycle, and platform-specific interaction. Use when Codex needs a platform decision, a cross-platform parity review, a guideline checklist, or a device-validation plan for mobile UX/UI.
---

# Mobile Platform Guidelines

Turn platform knowledge into explicit product decisions and testable checks. Preserve outcome parity while allowing implementation and interaction differences between iOS and Android.

## Select the platform mode

- **iOS**: use the iOS reference and check navigation, safe areas, Dynamic Type, VoiceOver, Reduce Motion, keyboard, permissions, and system surfaces.
- **Android**: use the Android reference and check predictive Back, edge-to-edge insets, scalable text, TalkBack, adaptive layouts, process recreation, and Material/custom behavior.
- **Cross-platform**: review shared user outcomes and record where behavior must diverge.

Read the existing first-party references before making a claim:

- [iOS patterns](../analyze-mobile-ui/references/ios-patterns.md)
- [Android patterns](../analyze-mobile-ui/references/android-patterns.md)
- [UX platform rules](../mobile-ux-architect/references/mobile-ia-patterns.md)
- [UI platform rules](../mobile-ui-design/references/screen-spec-rules.md)

For products whose core value depends on device motion, audio, or haptics, also read [sensor, audio, and haptic behavior](references/sensor-audio-haptics.md). Treat hardware availability, permission, interruption, route change, and a visible non-sensor alternative as required product states.

Recheck the linked official documentation before version-specific claims. Record the documentation date, OS/version scope, and whether a conclusion is observed, derived, or not-tested.

## Run the review

1. Establish target OS versions, form factors, input modes, appearance, text-size settings, and relevant system integrations.
2. Map each platform rule to a screen, state, flow, component, or system surface.
3. Separate product outcome parity from implementation parity; do not force identical navigation or permission behavior.
4. Mark each check `pass`, `fail`, `not-tested`, or `not-applicable`. A screenshot can support visible layout evidence but cannot prove runtime semantics.
5. Give every failure an owner, workaround/fallback, and verification method.

Create:

- `platform-review.md` using [assets/platform-review-template.md](assets/platform-review-template.md).
- `platform-guidelines.json` using [assets/platform-guidelines-template.json](assets/platform-guidelines-template.json) and [references/platform-guidelines-schema.md](references/platform-guidelines-schema.md).

Run `python3 scripts/validate_platform_guidelines.py <path-to-platform-guidelines.json>` and fix structural errors. Keep runtime checks untested until a device or executable prototype supplies evidence.

## Enforce the output order

1. Platform scope and source freshness.
2. Outcome-parity contract.
3. Rule/check matrix by platform and area.
4. Fallbacks, risks, and device test plan.
5. Decision, open questions, and confidence.

Do not label a design “native” from visual resemblance alone.
