---
name: riverpod-best-practices
description: "Comprehensive guide for Riverpod v3 development in Flutter, focusing on code generation, modular architecture, and modern state management patterns. Use this skill when: (1) Creating new providers or notifiers, (2) Refactoring existing state management code, (3) Setting up testing for Riverpod, or (4) Structuring new features using Riverpod."
---

# Riverpod Best Practices (v3)

This skill outlines the standard operating procedures for using Riverpod v3 in this project. Adherence to these practices ensures maintainability, testability, and consistency.

## Core Principles

1.  **Code Generation (`@riverpod`):** ALWAYS use the `@riverpod` annotation and `riverpod_generator`. Do NOT define providers manually (e.g., `Provider((ref) => ...)`).
    -   *Why:* Reduces boilerplate, handles `autoDispose` logic automatically, ensures type safety, and enables easier refactoring.
2.  **Modular Architecture:** Organize code by **feature**, not by layer.
    -   *Structure:* `lib/modules/[feature]/providers/` for providers, `lib/modules/[feature]/screens/` for UI.
3.  **Unified `Ref`:** Use `Ref` for all provider interactions. Avoid legacy types like `WidgetRef` inside providers (use `Ref` instead).
4.  **AsyncValue First:** Always handle Loading/Error/Data states explicitly in the UI using `switch` expressions.

## Implementation Guidelines

### 1. Defining Providers
*   **Class-Based (Notifier):** Use for complex state requiring methods (mutations).
    ```dart
    @riverpod
    class MyNotifier extends _$MyNotifier { ... }
    ```
*   **Functional (Future/Stream):** Use for simple data fetching or read-only values.
    ```dart
    @riverpod
    Future<Data> myData(Ref ref) async { ... }
    ```
*   **KeepAlive:** Use `@Riverpod(keepAlive: true)` ONLY for global state (User, Auth, Settings). Default is `autoDispose`.

### 2. State Management
*   **Side Effects:** Perform side effects (API calls, navigation logic) in **methods** within the Notifier, NOT in the `build()` method.
*   **Ref.mounted:** Always check `ref.mounted` after an `await` before setting state to prevent exceptions on disposed providers.
    ```dart
    if (ref.mounted) state = AsyncData(data);
    ```
*   **Mutations:** To update lists/data, prefer fetching fresh data or optimistically updating state.

### 3. Consuming Providers
*   **ConsumerWidget:** Extend `ConsumerWidget` instead of `StatelessWidget`.
*   **ConsumerStatefulWidget:** Extend `ConsumerStatefulWidget` if you need `initState`/`dispose`.
*   **Ref.watch:** Use `ref.watch` inside `build()` to rebuild on changes.
*   **Ref.read:** Use `ref.read` inside callbacks (e.g., `onPressed`) to trigger actions. **NEVER** use `ref.read` inside `build()`.

### 4. Naming Conventions
*   **File Name:** `snake_case` (e.g., `user_controller.dart`).
*   **Class Name:** `PascalCase` (e.g., `UserController`).
*   **Provider Name (Generated):** `camelCase` (e.g., `userControllerProvider`).

## Resources

*   **Code Snippets:** See [references/snippets.md](references/snippets.md) for templates of Notifiers, Providers, and Consumers.
*   **Testing Guide:** See [references/testing.md](references/testing.md) for unit and widget testing patterns.
*   **Async Gaps & Lifecycle:** See [references/async_gaps.md](references/async_gaps.md) for critical info on `UnmountedRefException` and `keepAlive`.
*   **Provider Types:** See [references/provider_types.md](references/provider_types.md) for a decision tree on which provider to use.
*   **Performance:** See [references/performance.md](references/performance.md) for `ref.select` and optimization tips.
*   **Architecture:** See [references/architecture.md](references/architecture.md) for repository patterns and anti-patterns.

## Migration (from v2/Manual)
If you encounter manual providers (`StateNotifierProvider`, `ChangeNotifierProvider`, etc.):
1.  **Identify:** Locate the logic.
2.  **Convert:** Rewrite as a `@riverpod` class or function.
3.  **Replace:** Update consumers to use the generated provider (e.g., `myProvider` instead of `myProvider.notifier` for watching state).
