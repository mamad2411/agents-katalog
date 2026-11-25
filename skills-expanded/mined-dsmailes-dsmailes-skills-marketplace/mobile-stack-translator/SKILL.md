---
name: mobile-stack-translator
description: Use when the user wants to understand how mobile code, architecture, UI, lifecycle, state management, navigation, concurrency, persistence, networking, platform APIs, or tests would be expressed in another mobile platform or framework. Supports comparisons across Swift/iOS, Kotlin/Android, Flutter, and React Native. Applies when the user asks how Swift compares to Kotlin, how Flutter compares to React Native, how a snippet would be done in another mobile stack, or how to learn the equivalent concept without requesting a full production port.
---

# Mobile Stack Translator

## Mission

Help mobile developers understand code and patterns across Swift/iOS, Kotlin/Android, Flutter, and React Native. Default to conceptual translation: explain the intent, map the source concepts to the target stack, show concise illustrative snippets when helpful, and call out platform differences that matter.

This is not a default code-porting skill. Only produce a full implementation when the user explicitly asks for a port, patch, or production-ready target code.

## Default Invocation

When invoked with no extra instructions:

1. Inspect the provided snippet, file, diff, or repository context.
2. Identify the source stack and target stack when possible.
3. If the target stack is missing or ambiguous, ask one focused question before continuing.
4. Load `references/mobile-stack-map.md` when comparing unfamiliar areas, choosing terminology, or covering multiple framework concepts.
5. Explain the mapping using the default response shape.

Do not ask broad setup questions if the code or filenames make the source stack clear.

## Stack Detection

Infer stacks from code, filenames, project files, and framework symbols:

- **Swift/iOS**: `.swift`, `SwiftUI`, `UIViewController`, `ObservableObject`, `@Observable`, `Task`, `.xcodeproj`, `Package.swift`
- **Kotlin/Android**: `.kt`, `Activity`, `Fragment`, `ViewModel`, `Flow`, `CoroutineScope`, `Jetpack Compose`, `build.gradle*`
- **Flutter**: `.dart`, `Widget`, `StatefulWidget`, `StatelessWidget`, `BuildContext`, `setState`, `pubspec.yaml`
- **React Native**: `.tsx`, `.jsx`, `useState`, `useEffect`, `StyleSheet`, `NavigationContainer`, `metro.config.*`

If more than one stack appears, name the likely source and target and ask for confirmation only when the requested comparison cannot proceed safely.

## Response Shape

Use this structure by default:

```text
What this code is doing
[2-4 bullets about behavior and intent]

Source-stack concepts
[the important framework concepts in the original code]

Target-stack equivalent
[how those ideas are usually expressed in the requested stack]

Key differences and gotchas
[lifecycle, threading, state ownership, rendering, platform API, testing, or performance differences]

Illustrative target snippet
[short snippet only when it clarifies the mapping]

What to inspect next
[1-3 files, APIs, docs, tests, or concepts to study next]
```

Skip sections that do not fit the user's request, but keep the answer structured enough to compare ideas clearly. Use a side-by-side table when mapping APIs, lifecycle events, state owners, or testing concepts is clearer than prose.

## Comparison Workflow

1. **Summarize intent first**: Explain what the code is trying to do before naming equivalents.
2. **Map concepts, not tokens**: Translate roles such as "state owner", "render function", "effect", "binding", "lifecycle callback", or "async stream" before translating syntax.
3. **Name the idiomatic target pattern**: Prefer the target stack's normal approach over a literal copy of the source structure.
4. **Call out non-equivalences**: Say when the target stack has no direct equivalent or when the equivalent has different lifecycle, threading, ownership, or platform constraints.
5. **Use small examples**: Include short snippets to illustrate shape, not complete apps.
6. **Keep verification honest**: If target code has not been run, label it illustrative.

## Guardrails

- Do not present illustrative snippets as verified drop-in code.
- Do not invent framework APIs. If unsure, say what needs checking.
- Do not flatten platform differences into "same thing with different syntax" when lifecycle, threading, or rendering behavior differs.
- Do not turn the answer into a migration plan unless the user asks for migration steps.
- Do not edit files unless the user explicitly asks for implementation.
- Prefer official framework terminology over generic cross-platform labels.

## When The User Wants A Port

If the user explicitly asks for a port or production implementation:

1. Clarify source and target stack if missing.
2. Identify platform-specific dependencies, permissions, assets, navigation, persistence, and tests.
3. Explain assumptions before code.
4. Keep the first target implementation minimal.
5. Recommend verification in the target platform's normal build/test/runtime environment.

## References

Read `references/mobile-stack-map.md` when:

- comparing more than one framework concept
- mapping lifecycle, navigation, state, concurrency, persistence, networking, or testing
- answering a broad Swift vs Kotlin, Flutter vs React Native, or native vs cross-platform question
- you need concise terminology for source-to-target equivalents
