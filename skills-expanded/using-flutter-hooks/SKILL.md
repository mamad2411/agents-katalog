---
name: "using-flutter-hooks"
description: "Manages local UI state and side effects in Flutter using the flutter_hooks package (v0.21.x) with HookWidget, useState, useEffect, useMemoized, useAnimationController, and custom hooks. Use this skill when replacing StatefulWidget boilerplate with hooks, reusing stateful UI logic across widgets, managing controller lifecycles (TextEditingController, AnimationController, ScrollController) without manual dispose, implementing countdown timers or subscriptions in widgets, mixing flutter_hooks with Riverpod via HookConsumerWidget, or any time the words 'flutter hooks', 'useEffect', 'useState', 'HookWidget', or 'flutter_hooks' appear in the request."
metadata:
  last_modified: "2026-04-01 14:35:00 (GMT+8)"
---

# Flutter Hooks Latest Version Best Practices Guide (v0.21.x)

## Goal
`flutter_hooks` is a package developed by Remi Rousselet (author of Riverpod and Freezed). Its core philosophy stems from React Hooks. The current latest version is **0.21.3+1**.

Hooks primarily exist to solve the verbose boilerplate code brought about by `StatefulWidget`, and the extreme difficulty of reusing UI Logic across Widgets.

## Instructions

### 1. Core Concept: What are Hooks?
Hooks are tools used to manage "**local and ephemeral UI state or side effects**".
*   **Not Suitable For**: Global business logic management (this should be handed over to Riverpod or Bloc).
*   **Suitable For**: Any Widget attaching a `Controller`, animation management, focus tracking, or countdown timers.

#### Dependency Installation
```yaml
dependencies:
  flutter_hooks: ^0.21.4
  hooks_riverpod: ^3.5.0 # If you are simultaneously using Riverpod
```

### 2. Widget Declaration: Replacing StatefulWidget
To use Hooks, your Widget cannot inherit from a standard `StatelessWidget` or `StatefulWidget`; it must instead inherit from `HookWidget`.
*(If you are mixing it with Riverpod, inherit from `HookConsumerWidget` instead)*.

All Hooks **are only allowed to be called at the top level inside the `build` method**. Writing them inside `if` statements is strictly prohibited.

### 3. Built-in Hooks Overview and Best Practices
`flutter_hooks` provides a massive number of practical built-in Hooks. Leveraging them effectively can save hundreds of lines of `dispose()` and `initState()`.

#### 3.1 State and Caching (State & Caching)
*   **`useState(initialData)`**:
    *   **Purpose**: Manages the simplest local state (essentially wraps `ValueNotifier`).
    *   **Usage**: `final counter = useState(0); counter.value++;`
*   **`useMemoized(compute, [keys])`**:
    *   **Purpose**: Caches the result of an expensive computation, or ensures an object (e.g., a custom class) is instantiated only once during Rebuilds.
    *   **Usage**: `final complexObj = useMemoized(() => HeavyObject(), []);`
*   **`useCallback(callback, [keys])`**:
    *   **Purpose**: Caches a function reference. If passed to deep Widgets, it prevents triggering unnecessary refreshes because parent Rebuilds generate a new function memory location.
*   **`useRef(initialValue)`**:
    *   **Purpose**: Holds a mutable object across Rebuild cycles, and **changing its value does not trigger a UI refresh** (unlike `useState`). Perfect for storing the width of a previous screen, or a Timer instance for subsequent clearing.

#### 3.2 Side Effects and Lifecycle (Side Effects)
*   **`useEffect(effect, [keys])`**:
    *   **Purpose**: The perfect alternative to `initState` and `dispose`. Responsible for subscriptions, timers, and any side effect with a start and end point.
    *   **Usage**:
    ```dart
    useEffect(() {
      print('Equivalent to initState (Triggers only when key changes or upon initialization)');
      return () => print('Equivalent to dispose (Executes before Widget destruction or before effect re-triggers)');
    }, []); // Passing [] ensures it runs only once
    ```
*   **`useIsMounted()`**: Deprecated in flutter_hooks 0.21.x. Inside a `HookWidget` or `HookConsumerWidget`, check `context.mounted` after an `await` instead. Use the effect's cleanup function to cancel timers and subscriptions, which covers most cases.

#### 3.3 Auto-cleaning Controllers (Most Powerful Feature)
Forget writing `controller.dispose()` manually! The following Hooks automatically create and destroy them behind the scenes for you:
*   **`useTextEditingController(text: 'default value')`**
*   **`useAnimationController(duration: ...)`**
*   **`useScrollController()`**
*   **`usePageController()`**
*   **`useTabController(length: 3)`**
*   **`useFocusNode()`**

#### 3.4 Reactive Wrappers (Reactive Streams & Futures)
*   **`useFuture(future)`** / **`useStream(stream)`**:
    *   **Purpose**: Minimalist versions of `FutureBuilder` / `StreamBuilder`, returning an `AsyncSnapshot`.
*   **`useListenable(listenable)`** / **`useValueListenable(notifier)`**:
    *   **Purpose**: Allows a Widget to listen to traditional ChangeNotifier or ValueNotifier and automatically trigger a rebuild.

### 4. Advanced Practices: Custom Hooks (Custom Hooks)
The greatest power of Hooks lies in **encapsulating and perfectly reusing UI logic**.
If multiple parts in your project need an "obtain current App lifecycle state (AppLifecycleState)", rather than writing a bunch of observers on every page, writing it as a Custom Hook solves it once and for all.

> **Naming Convention**: All custom Hooks MUST begin with `use`.

#### Approach A: Composing Multiple Existing Hooks (Composition - Highly Recommended)
The simplest and most favored approach is directly writing a function that returns a result.

```dart
import 'dart:async';

// Encapsulates a set of "countdown timer" logic
int useCountdown({required int seconds}) {
  final timeLeft = useState(seconds);

  useEffect(() {
    final timer = Timer.periodic(const Duration(seconds: 1), (timer) {
      if (timeLeft.value > 0) {
        timeLeft.value--;
      } else {
        timer.cancel();
      }
    });
    
    return timer.cancel; // Ensures it definitely gets closed
  }, [seconds]); // Resets the timer when 'seconds' change

  return timeLeft.value;
}

// Used in a Widget like this:
Widget build(BuildContext context) {
  final count = useCountdown(seconds: 30);
  return Text("Remaining $count seconds");
}
```

#### Approach B: Extending the `Hook` Class Definition (Advanced / Low-level Library Development)
If you need access to a lower-level `BuildContext` or want to intercept Flutter's native `didUpdateContext`, you can create a specific Hook much like crafting a StatefulWidget.

```dart
// This pattern is typically geared towards third-party package developers
int useMyComplexLogic() => use(const _MyComplexHook());

class _MyComplexHook extends Hook<int> {
  const _MyComplexHook();
  @override
  _MyComplexHookState createState() => _MyComplexHookState();
}

class _MyComplexHookState extends HookState<int, _MyComplexHook> {
  int value = 0;
  
  @override
  void initHook() { /* Initialization */ }

  @override
  int build(BuildContext context) => value;

  @override
  void dispose() { /* Resource cleanup */ }
}
```

### 5. Conclusion: Integration with Riverpod (The God-tier Combination)
`flutter_hooks` is not designed to replace BLoC or Riverpod. The optimal modern Flutter development architecture:
*   **Global Business Logic and Shared State** → `Riverpod` (`riverpod_generator`)
*   **Complex In-Page UI Control and Animation** → `flutter_hooks` (`useAnimationController`, `useTextEditingController`)

By combining the two, your project will practically contain zero `StatefulWidget`s. All Widgets can remain clean, focusing purely on their primary duty (drawing the screen), thereby yielding the highest quality Flutter applications.

## Constraints
* Ensure that you ONLY invoke Hooks at the very top level of a `build` method.
* Make sure `hooks_riverpod` is imported if you're mixing Riverpod Providers with flutter hooks; do not mix `hooks_riverpod` imports concurrently with raw `flutter_riverpod`.
* Do NOT enforce `Controller.dispose()` if implementing hooks like `useAnimationController()`.
