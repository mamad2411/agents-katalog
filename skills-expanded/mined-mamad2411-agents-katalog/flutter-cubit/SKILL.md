---
name: flutter-cubit
description: Scaffold a Cubit with sealed state classes using Dart 3+ native features. ALWAYS use this skill before writing any Cubit or state file — including when building a full feature, implementing a screen, or adding state management. Triggers on "create cubit", "add cubit", "new cubit", or any task that will produce a *_cubit.dart or *_state.dart file.
allowed-tools: Read Write Edit Glob Grep
---

# Scaffold a Cubit + Sealed State (Dart 3+)

Generate a Cubit and its state file for the given feature. **No Freezed. No build_runner.**

## Rules

- Use `sealed class` for state unions with exhaustive pattern matching.
- Use `switch` expressions where applicable.
- Cubit depends ONLY on use cases — never on repositories or data sources.
- Place files in `features/{feature_name}/presentation/cubit/`.
- Use `const` constructors on all state subclasses.

## State File (`{name}_state.dart`)

```dart
sealed class {Name}State {
  const {Name}State();
}

class {Name}Initial extends {Name}State {
  const {Name}Initial();
}

class {Name}Loading extends {Name}State {
  const {Name}Loading();
}

class {Name}Loaded extends {Name}State {
  final {Entity} data;
  const {Name}Loaded(this.data);
}

class {Name}Error extends {Name}State {
  final String message;
  const {Name}Error(this.message);
}
```

## Cubit File (`{name}_cubit.dart`)

```dart
import 'package:flutter_bloc/flutter_bloc.dart';

class {Name}Cubit extends Cubit<{Name}State> {
  final {UseCase} _useCase;

  {Name}Cubit(this._useCase) : super(const {Name}Initial());

  Future<void> load({params}) async {
    emit(const {Name}Loading());
    final result = await _useCase({params});
    result.fold(
      (failure) => emit({Name}Error(_mapFailureToMessage(failure))),
      (data) => emit({Name}Loaded(data)),
    );
  }

  String _mapFailureToMessage(Failure failure) {
    return switch (failure) {
      ServerFailure() => 'Server error. Please try again later.',
      NetworkFailure() => 'No internet connection.',
      _ => 'Something went wrong.',
    };
  }
}
```

## DI Registration

Register in `core/di/` setup:

```dart
getIt.registerFactory(() => {Name}Cubit(getIt()));
```

## After scaffolding, verify

- Cubit imports no repository or data source directly.
- State file has no Flutter imports.
- All state subclasses use `const` constructors.
- `sealed class` enables exhaustive `switch` in `BlocBuilder`.
