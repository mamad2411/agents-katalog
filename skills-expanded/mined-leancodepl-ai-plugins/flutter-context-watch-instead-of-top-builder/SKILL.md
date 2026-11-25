---
name: flutter-context-watch-instead-of-top-builder
description: Refactors Flutter widgets to replace top-level BlocBuilder wrappers with context.watch-based state reads while preserving behavior. Use when the user asks to remove BlocBuilder at page/widget root, use context.watch, or simplify Flutter BLoC widget trees.
---

# Flutter context.watch Instead of Top Builder

## Goal

Replace a top-level `BlocBuilder<Cubit, State>` with `context.watch<Cubit>()` in `build`, while keeping the same UI behavior.

## Workflow

1. Identify a root `BlocBuilder` wrapping most of the screen.
2. Inside `build`, read the cubit once:
   - `final cubit = context.watch<MyCubit>();`
   - `final state = cubit.state;`
3. Remove the outer `BlocBuilder` and return the wrapped widget directly.
4. Keep write actions as `context.read<MyCubit>()` in handlers (`onTap`, submit, etc.).
5. If `presentation` stream listeners exist (for `useOnStreamChange`), use `cubit.presentation` so there is a single watched cubit reference.
6. Validate no behavior changes: loading, list size, buttons, and side effects should match previous logic.

## Guardrails

- Only refactor when the top-level builder is a straightforward state passthrough.
- Do not change business logic, event handling, or navigation.
- Do not introduce extra rebuild scopes accidentally; watch only the cubit needed by this widget.
- Preserve existing analytics IDs and localization usage.

## Example Pattern

```dart
// Before
return BlocBuilder<MyCubit, MyState>(
  builder: (context, state) => MyScaffold(
    isLoading: state.isLoading,
  ),
);
```

```dart
// After
final cubit = context.watch<MyCubit>();
final state = cubit.state;

return MyScaffold(
  isLoading: state.isLoading,
);
```
