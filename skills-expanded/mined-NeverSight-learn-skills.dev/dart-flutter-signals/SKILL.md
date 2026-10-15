---
name: dart-flutter-signals
description: Expert skill for signals-based state management in Dart and Flutter. Activates for any Dart or Flutter project to provide optimized reactivity patterns.
---

# Dart/Flutter Signals Expert Skill

## Overview
You are an expert in the `signals` and `signals_flutter` ecosystem. This skill focuses on high-performance, pull-based state management that minimizes unnecessary recomputations and simplifies reactivity in Dart and Flutter.

## Activation
This skill is activated whenever a Dart or Flutter project is being edited, or on demand. When activated, you MUST state: "I am applying my Signals expertise to this Dart/Flutter project."

## Core Instructions

### 1. Library Selection
- **Dart Core/CLI/Server**: Prefer importing `package:signals/signals.dart`.
- **Flutter Apps**: Prefer importing `package:signals_flutter/signals_flutter.dart`.

### 2. Fundamental Principles
- **Pull-based Reactivity**: Signals only compute when they are read. If a signal or a computed value is never read, the computation is never performed.
- **Reading Values**: Prefer calling the signal as a function `someSignal()` to get its value in an rvalue context, rather than accessing `.value` (e.g., `final x = mySignal()`). Use `.value = newValue` for setting values.
- **Minimal Updates**: Leverage `computed` signals to derive state. They automatically track dependencies and cache results, only re-evaluating when dependencies change AND the value is accessed.
- **Glitch-Free**: Signals avoid the "diamond problem" and ensure consistent state updates.

### 3. Key APIs & Usage

#### Basic Signals & Computed
```dart
import 'package:signals/signals.dart';

final count = signal(0, debugLabel: 'count');
final isEven = computed(() => count() % 2 == 0, debugLabel: 'isEven');

effect(() {
  print('Count: ${count()}, Is Even: ${isEven()}');
}, debugLabel: 'logging-effect');

count.value++; // Triggers the effect
```

#### Signal Containers
Useful for managing multiple signals based on keys (e.g., settings, entity caches).
```dart
final userContainer = signalContainer((userId) {
  return signal(FetchUser(userId));
}, cache: true);

final userA = userContainer('user-1');
final userB = userContainer('user-1'); // returns the same signal due to cache: true
```

#### Reactive Collections
Use dedicated collection signals to track mutations within lists, maps, and sets.
- `listSignal([1, 2])` or `[1, 2].toSignal()`
- `mapSignal({'a': 1})` or `{'a': 1}.toSignal()`
- `setSignal({1, 2})` or `{1, 2}.toSignal()`

#### ChangeStack (Undo/Redo)
Track state history easily.
```dart
final s = ChangeStackSignal(0, limit: 10);
s.value = 1;
s.undo(); // value returns to 0
```

### 4. Best Practices
- **Prefer `someSignal()` as a getter** over `someSignal.value` in rvalue contexts for a cleaner, more concise syntax.
- **Always provide a relevant `debugLabel`** for signals, computed values, and effects (e.g., `signal(0, debugLabel: 'counter')`) unless otherwise instructed. This is critical for effective debugging.
- **Prefer `computed` over `effect`** when you need to derive new state. Results are cached and lazy.
- **Use `batch(() => ...)`** to group multiple changes if performance is a concern, though the underlying linked-list implementation is highly optimized.
- **Observers**: Provide a `SignalsObserver` (like `LoggingSignalsObserver`) during development to debug signal lifecycles and updates.
- **Disposal**: Always clean up effects and containers when they are no longer needed to prevent memory leaks.

## Reference
These instructions are based on the latest documentation from [dartsignals.dev/llms.txt](https://dartsignals.dev/llms.txt).
