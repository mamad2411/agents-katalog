---
name: native-ui-generator
description: Use for building or refining screens and components with strong platform fidelity, hierarchy, accessibility, and state design in SwiftUI, Jetpack Compose, or Tauri desktop frontends.
---

# Native UI Generator

## Use when
- the main task is screen or component design in code, not just backend logic
- the result must feel native and intentional on Apple, Android, or desktop platforms
- interaction states, hierarchy, accessibility, and visual polish matter as much as raw layout

## Do not use when
- the task is a pure architecture, backend, or data change with minimal UI impact
- the user wants a throwaway mockup rather than implementation-quality UI code

## Working rules
- Start with the user's primary task, hierarchy, and interaction order before styling details.
- Prefer native controls and established platform patterns before custom chrome.
- Design loading, empty, success, error, disabled, permission-denied, and retry states together when relevant.
- Use spacing, typography, contrast, and motion deliberately; avoid decorative complexity.
- Treat accessibility, keyboard or focus behavior, and resilient content as baseline quality.

## Workflow
1. Identify the primary action, most important information, and platform constraints.
2. Choose the right container structure and state model before coding.
3. Implement the smallest coherent UI slice with the necessary states.
4. Validate realistic content, long text, smaller and larger sizes, and assistive interactions.
5. Only extract reusable primitives after a repeat pattern is visible.

## Platform direction
- SwiftUI: prefer Apple-native hierarchy, controls, and calm motion.
- Compose: use Material 3 thoughtfully, support adaptive layout, and keep tokens centralized.
- Tauri desktop frontends: behave like a real desktop product with clear focus, keyboard, resize, and hover affordances.

## Reference routing
- Read `references/apple-ui-guidance.md` for Apple-platform design direction.
- Read `references/android-ui-guidance.md` for Android and Compose guidance.
- Read `references/desktop-web-ui-guidance.md` for desktop-oriented frontend behavior.
- Read `references/release-quality-gates.md` when the UI is release-critical.
- Read `references/official-docs.md` only when primary platform docs are needed.

## Output contract
Provide:
- files changed
- major UI decisions
- accessibility or UX considerations addressed
- validation performed
- any real deferred states or risks
