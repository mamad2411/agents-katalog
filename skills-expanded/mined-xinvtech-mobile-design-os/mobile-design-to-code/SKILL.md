---
name: mobile-design-to-code
description: Convert validated mobile product, UX, wireframe, design-system, UI, prototype, and platform contracts into an implementation-ready Flutter handoff by default, or another explicitly requested stack. Use when Codex needs route/state mapping, token and component bindings, accessibility semantics, platform variants, implementation tasks, runnable scaffolding, or code-readiness review.
---

# Mobile Design to Code

Preserve design intent as executable implementation contracts. Map meaning, states, behavior, and verification—not just screenshots or CSS-like coordinates.

## Select the handoff mode

- **Plan**: create a framework-specific implementation map and task breakdown before coding.
- **Scaffold**: create a narrow runnable implementation for the declared platform and core flow.
- **Review**: compare implementation against the design package, prototype tests, and platform contract.

Declare the target framework, OS versions, build entry point, persistence/network boundaries, and whether code changes are authorized. If the user has not selected a stack, use Flutter and record `frameworkSelectionSource: project-default`; switch to SwiftUI, UIKit, Jetpack Compose, React Native, or another stack only when the user explicitly asks for it, recording `frameworkSelectionSource: user-specified`.

## Establish the input contract

Prefer the validated Design Package plus `wireframe.json`, `design-system.json`, `prototype.json`, and `platform-guidelines.json` when available. Preserve upstream IDs and provenance. Report missing contracts before writing code.

## Build the mapping

1. Map each design token to a semantic code token and source file.
2. Map each component to a code component, props, state machine, accessibility semantics, and platform variant.
3. Map each Screen/State to a route/view, data dependencies, loading/error/recovery behavior, and acceptance signals.
4. Map gestures, motion, haptics, permissions, system surfaces, keyboard, lifecycle, and deep links to platform APIs or explicit fallbacks.
5. Define test cases for core flows, state continuity, large text, assistive technology, reduced motion, offline, duplicate submission, persistence, and destructive recovery.
6. Separate generated scaffolding from product decisions that require an engineer or designer.

For the project-default Flutter path, use [references/flutter-implementation.md](references/flutter-implementation.md) and the scaffold helper at `scripts/scaffold_flutter_app.py`. The helper creates a small runnable Flutter app from a valid handoff; it does not silently turn an untested prototype into production code.

Read [references/handoff-rules.md](references/handoff-rules.md) and [references/handoff-schema.md](references/handoff-schema.md) before creating structured output.

## Produce and validate

Create:

- `code-handoff.md` using [assets/code-handoff-template.md](assets/code-handoff-template.md).
- `code-handoff.json` using [assets/code-handoff-template.json](assets/code-handoff-template.json).

Run `python3 scripts/validate_code_handoff.py <path-to-code-handoff.json>` and fix every error. A valid handoff is not proof that the app builds or that runtime behavior passes; keep implementation and device checks explicit.

When a Flutter scaffold is requested, run `python3 scripts/scaffold_flutter_app.py --handoff <path-to-code-handoff.json> --output <new-project-directory>`, then run `flutter analyze` and `flutter test` in the generated project. Keep those results separate from the static handoff evidence.

## Enforce the output order

1. Stack (Flutter by default unless explicitly overridden), scope, source contracts, and assumptions.
2. Token/component bindings.
3. Route/screen/state mapping.
4. Platform and system API mapping.
5. Tests, build/run instructions, ownership, and open risks.

Do not produce a screenshot-only handoff, invent inaccessible semantics, or claim implementation readiness when state, platform, or test contracts are missing.
