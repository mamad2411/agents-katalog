---
name: "android-compose-accessibility"
description: "Make Compose interfaces accessible with semantics, announcements, contrast, focus order, and adaptive touch targets."
metadata:
  version: "0.1.0"
  category: "ui"
  tags: ["android", "compose", "accessibility", "a11y"]
  triggers:
    include: ["compose accessibility review", "android semantics issue compose", "focus order in compose", "screen reader compose ui", "large font compose problem"]
    exclude: ["dependency conflict only", "room schema only", "gradle plugin migration only"]
  owners: ["@android-agent-skills/maintainers"]
  test_targets: ["examples/orbittasks-compose", "examples/orbittasks-xml", "benchmarks/triggers.jsonl"]
---
# Android Compose Accessibility

## When To Use
- Use this skill when the request is about: compose accessibility review, android semantics issue compose, focus order in compose.
- Primary outcome: Make Compose interfaces accessible with semantics, announcements, contrast, focus order, and adaptive touch targets.
- Handoff skills when the scope expands:
- `android-ui-states-validation`
- `android-testing-ui`

## Workflow
1. Identify whether the target surface is Compose, View system, or a mixed interoperability screen.
2. Select the lowest-friction UI pattern that satisfies responsiveness, accessibility, and performance needs.
3. Build the UI around stable state, explicit side effects, and reusable design tokens.
4. Exercise edge cases such as long text, font scaling, RTL, and narrow devices in the fixture apps.
5. Validate with unit, UI, and screenshot-friendly checks before handing off.

## Guardrails
- Optimize for stable state and predictable rendering before adding animation or abstraction.
- Respect accessibility semantics, contrast, focus order, and touch target guidance by default.
- Do not mix Compose and View system ownership without an explicit interoperability boundary.
- Prefer measured performance work over premature micro-optimizations.

## Anti-Patterns
- Embedding navigation or business logic directly in leaf UI components.
- Using fixed dimensions that break on localization or dynamic text.
- Ignoring semantics and announcing only visual changes.
- Porting XML patterns directly into Compose without adapting the mental model.

## Examples
### Happy path
- Scenario: Add semantics and readable labels to the Compose OrbitTasks cards.
- Command: `cd examples/orbittasks-compose && ./gradlew :app:connectedDebugAndroidTest`

### Edge case
- Scenario: Validate font scaling, contrast, and touch targets in narrow layouts.
- Command: `cd examples/orbittasks-compose && ./gradlew :app:assembleDebug`

### Failure recovery
- Scenario: Differentiate accessibility requests from general UI validation or theme work.
- Command: `python3 scripts/eval_triggers.py --skill android-compose-accessibility`

## Done Checklist
- The implementation path is explicit, minimal, and tied to the right Android surface.
- Relevant example commands and benchmark prompts have been exercised or updated.
- Handoffs to adjacent skills are documented when the request crosses boundaries.
- Official references cover the chosen pattern and the main migration or troubleshooting path.

## Official References
- [https://developer.android.com/develop/ui/compose/accessibility](https://developer.android.com/develop/ui/compose/accessibility)
- [https://developer.android.com/guide/topics/ui/accessibility/apps](https://developer.android.com/guide/topics/ui/accessibility/apps)
- [https://developer.android.com/guide/topics/ui/accessibility/testing](https://developer.android.com/guide/topics/ui/accessibility/testing)
- [https://developer.android.com/develop/ui/compose/layouts/adaptive](https://developer.android.com/develop/ui/compose/layouts/adaptive)
