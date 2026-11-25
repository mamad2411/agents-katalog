---
name: "android-compose-xml-interoperability"
description: "Bridge Compose and the View system safely during incremental migrations, interoperability screens, and shared theming."
metadata:
  version: "0.1.0"
  category: "ui"
  tags: ["android", "compose", "xml", "interop"]
  triggers:
    include: ["compose in fragment", "androidview in compose", "incremental compose migration", "mix xml and compose android", "interop theme issue"]
    exclude: ["pure retrofit issue", "play console release", "security crypto only"]
  owners: ["@android-agent-skills/maintainers"]
  test_targets: ["examples/orbittasks-compose", "examples/orbittasks-xml", "benchmarks/triggers.jsonl"]
---
# Android Compose XML Interoperability

## When To Use
- Use this skill when the request is about: compose in fragment, androidview in compose, incremental compose migration.
- Primary outcome: Bridge Compose and the View system safely during incremental migrations, interoperability screens, and shared theming.
- Handoff skills when the scope expands:
- `android-viewsystem-foundations`
- `android-compose-foundations`

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
- Scenario: Embed a Compose task summary inside the XML fixture without ownership confusion.
- Command: `cd examples/orbittasks-xml && ./gradlew :app:assembleDebug`

### Edge case
- Scenario: Host a View-based screen from a Compose entry point during phased migration.
- Command: `cd examples/orbittasks-compose && ./gradlew :app:assembleDebug`

### Failure recovery
- Scenario: Separate interoperability prompts from pure View or pure Compose requests.
- Command: `python3 scripts/eval_triggers.py --skill android-compose-xml-interoperability`

## Done Checklist
- The implementation path is explicit, minimal, and tied to the right Android surface.
- Relevant example commands and benchmark prompts have been exercised or updated.
- Handoffs to adjacent skills are documented when the request crosses boundaries.
- Official references cover the chosen pattern and the main migration or troubleshooting path.

## Official References
- [https://developer.android.com/develop/ui/compose/migrate/interoperability-apis](https://developer.android.com/develop/ui/compose/migrate/interoperability-apis)
- [https://developer.android.com/develop/ui/compose/migrate/strategy](https://developer.android.com/develop/ui/compose/migrate/strategy)
- [https://developer.android.com/develop/ui/compose/migrate/other-considerations](https://developer.android.com/develop/ui/compose/migrate/other-considerations)
- [https://developer.android.com/guide/fragments/communicate](https://developer.android.com/guide/fragments/communicate)
