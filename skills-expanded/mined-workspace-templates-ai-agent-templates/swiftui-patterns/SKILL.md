---
name: swiftui-patterns
description: Structures SwiftUI views, state and navigation around observable models so screens stay small, previewable and free of stale-state bugs.
---

# SwiftUI patterns

Small views, one source of truth, navigation as data.

## Steps

1. Check the deployment target. On iOS 17 and later use `@Observable` classes. On older targets keep `ObservableObject` and `@Published`, and say so.
2. Split each screen into a model and a view. The model is an `@Observable` `@MainActor` class holding state and async methods. The view reads it and sends actions. No networking or formatting logic in `body`.
3. Ownership: the view that creates a model holds it with `@State`. Children receive it as a plain property, or `@Bindable` when they need bindings. Use `@Environment` for app-wide services only. Never create a model inside `body`.
4. Represent screen state as an enum such as `idle`, `loading`, `loaded(Items)`, `failed(Error)`, and switch over it in the view.
5. Navigation: use `NavigationStack` with a `path` array of `Hashable` route values and `navigationDestination(for:)`. Keep the path in one place so deep links and "pop to root" are one assignment.
6. Lists: give `ForEach` stable `Identifiable` ids from the data, never `\.self` on mutable values or array indices.
7. Async work goes in `.task` or `.task(id:)`, which cancels itself. Never start `Task {}` from `onAppear` without cancellation.
8. Extract subviews when a section has its own state or exceeds about 40 lines. Add a `#Preview` for each state of the enum.

## Rules

- No force unwraps in views.
- Do not mark whole views `@MainActor` to silence warnings. Mark the model.
- Build with strict concurrency warnings on and fix them.

## Report

Files created or split, the route type, and any ownership bugs found.
