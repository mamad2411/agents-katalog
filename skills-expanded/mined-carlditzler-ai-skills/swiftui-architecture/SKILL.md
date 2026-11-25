---
name: swiftui-architecture
description: Use for SwiftUI-focused implementation and architecture work: view state, navigation, observable models, async behavior, accessibility, and Apple-platform UI polish when the task is mainly SwiftUI.
---

# SwiftUI Architecture

## Use when
- the task is primarily SwiftUI screens, components, state flow, navigation, or view-model structure
- the changed surface already uses SwiftUI or should clearly be implemented in SwiftUI
- Apple-platform UI polish and state ownership matter to the result

## Do not use when
- the affected surface is primarily UIKit, AppKit, or Metal without meaningful SwiftUI involvement
- the task is general backend or system design with little UI or SwiftUI impact

## Working rules
- Keep views declarative and focused on rendering.
- Make state ownership explicit and keep duplicate sources of truth out of the design.
- Treat `MainActor`, task lifetime, cancellation, and identity as first-class concerns.
- Keep business logic and side effects out of `body` and out of deeply nested view trees.
- Design for dynamic type, localization, dark mode, keyboard use, and accessibility by default.

## Workflow
1. Identify the changed screen or flow, its key states, and the repo's SwiftUI patterns.
2. Choose the right owner for transient UI state, screen state, and async work.
3. Implement the smallest correct SwiftUI change with deliberate loading, empty, error, and content states.
4. Add or update targeted tests, previews, or equivalent repo-supported validation.
5. Validate realistic content, text scaling, navigation behavior, and repeated task triggers.

## Quality bar
- No heavy work in `body`.
- No accidental state resets on refresh or navigation.
- Clear ownership of async work and side effects.
- UI feels native to Apple platforms rather than generic.

## Reference routing
- Read `references/swiftui-docs.md` for SwiftUI APIs and lifecycle behavior.
- Read `references/apple-hig-checklist.md` for Apple UI and UX quality.
- Read `references/release-quality-gates.md` when the changed surface is user-facing or release-critical.

## Output contract
Provide:
- files changed
- state, navigation, or UI decisions made
- tests or validation added
- release-readiness status
- real remaining risks
