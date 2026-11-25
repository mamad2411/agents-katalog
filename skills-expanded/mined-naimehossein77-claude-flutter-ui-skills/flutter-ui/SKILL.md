---
name: flutter-ui
description: Pixel-perfect Flutter UI — smooth animations, GoRouter navigation, back/forth logic, Riverpod + Provider state management. Use when building Flutter screens, navigation flows, animations, or state-connected widgets.
allowed-tools: Read, Glob, Grep, Bash
---

# Flutter UI System

> **Philosophy:** Flutter owns every pixel. Const-first. Theme-driven. GPU-animated. State-scoped.

---

## 🔧 Runtime Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `scripts/flutter_ui_audit.py` | Audit: missing const, dispose leaks, deprecated APIs | `python scripts/flutter_ui_audit.py <path>` |

---

## 🔴 MANDATORY: Read Reference Files First

**⛔ DO NOT code until relevant files are read:**

| File | Content | Priority |
|------|---------|----------|
| **[flutter-design-thinking.md](flutter-design-thinking.md)** | Anti-memorization, forces context analysis | **⬜ CRITICAL FIRST** |
| **[flutter-state-ui.md](flutter-state-ui.md)** | Riverpod + Provider rules Claude MUST enforce | **⬜ CRITICAL** |
| **[flutter-navigation.md](flutter-navigation.md)** | GoRouter, PopScope, back logic, deep links | **⬜ CRITICAL** |
| **[flutter-animations.md](flutter-animations.md)** | Implicit, explicit, Hero, page transitions, physics | **⬜ CRITICAL** |
| **[flutter-performance.md](flutter-performance.md)** | const, RepaintBoundary, 60fps, shader warmup | **⬜ CRITICAL** |
| [flutter-theme-system.md](flutter-theme-system.md) | Material 3, ColorScheme, TextTheme, ThemeExtension | ⬜ Read |
| [flutter-layout-system.md](flutter-layout-system.md) | Responsive, LayoutBuilder, MediaQuery, Slivers | ⬜ Read |
| [flutter-custom-paint.md](flutter-custom-paint.md) | Canvas, CustomPainter, pixel-perfect rendering | ⬜ Read |

> 🧠 **flutter-design-thinking.md FIRST** — prevents AI from applying memorized patterns.

---

## ⚠️ ASK BEFORE ASSUMING

| Aspect | Ask |
|--------|-----|
| **State manager** | "Riverpod, Provider, BLoC, or vanilla?" |
| **Navigation** | "GoRouter, auto_route, or Navigator 1.0?" |
| **Design system** | "Material 3, Cupertino, or custom?" |
| **Platforms** | "Mobile only, or tablet/desktop adaptive?" |
| **Flutter version** | "3.12+? (PopScope vs WillPopScope)" |

---

## ⛔ ANTI-PATTERNS

### Performance

| ❌ NEVER | ✅ ALWAYS |
|----------|-----------|
| `ListView` with static children for long lists | `ListView.builder` |
| `setState` in animation loop | `AnimatedBuilder` |
| `Opacity(opacity: 0)` to hide | `Visibility` or conditional render |
| `IntrinsicHeight`/`IntrinsicWidth` in lists | Fixed heights or `SliverFixedExtentList` |
| Missing `const` on StatelessWidget | `const MyWidget({super.key})` always |
| `Column` + `ListView` without `Expanded` | Wrap `ListView` in `Expanded` |
| Hardcoded `Color(0xFF...)` in widgets | `Theme.of(context).colorScheme.primary` |
| Hardcoded `fontSize` | `Theme.of(context).textTheme.bodyLarge` |

### Animation

| ❌ NEVER | ✅ ALWAYS |
|----------|-----------|
| Animate `width`/`height` | Animate `Transform` (scale/translate) |
| `AnimationController` without `dispose()` | Dispose in `dispose()` method |
| `addListener(() => setState((){}))` | `AnimatedBuilder` |
| Missing `RepaintBoundary` on complex painters | Wrap `CustomPaint` in `RepaintBoundary` |
| Hero tag collision | Unique data-driven tags |
| No easing curve | `Curves.easeInOut` minimum |

### Navigation

| ❌ NEVER | ✅ ALWAYS |
|----------|-----------|
| `WillPopScope` (Flutter 3.12+ deprecated) | `PopScope` with `canPop` + `onPopInvokedWithResult` |
| `Navigator.push` in GoRouter app | `context.go()` / `context.push()` |
| Hardcoded route strings everywhere | Centralized route constants |
| No route guard for auth screens | GoRouter `redirect` callback |
| Back button does nothing at root | `PopScope(canPop: false)` + exit dialog |

### State

| ❌ NEVER | ✅ ALWAYS |
|----------|-----------|
| `ref.read()` in `build()` (Riverpod) | `ref.watch()` in `build()` |
| Provider defined inside `build()` | Top-level `final myProvider = ...` |
| `context.read<T>()` in `build()` (Provider) | `context.watch<T>()` in `build()` |
| `BuildContext` in `ChangeNotifier` | Pass data, not context |
| `notifyListeners()` before mutation | Mutate first, then `notifyListeners()` |
| `.when()` without error handler | Always `when(data:, loading:, error:)` |
| `Consumer<T>` wrapping entire screen | `Selector<T, R>` on smallest widget |

---

## 🗺️ Navigation: go() vs push() vs replace()

| Method | Back Stack | Use When |
|--------|-----------|----------|
| `context.go('/path')` | Replaces stack | Tab switching, auth redirect |
| `context.push('/path')` | Adds to stack | Drill-down navigation |
| `context.replace('/path')` | Replaces current, no pop | Login → Home after auth |
| `context.pop()` | Removes current | Back button, close modal |
| `context.pop(result)` | Removes + returns data | Form submit, picker result |

---

## 🎬 Animation Selection

```
WHAT ARE YOU ANIMATING?
├── Simple property change → AnimatedContainer, AnimatedOpacity, TweenAnimationBuilder
├── Complex sequence/stagger → AnimationController + CurvedAnimation + AnimatedBuilder
├── Shared element (cross-screen) → Hero widget + unique tag
├── Page enter/exit → GoRouter CustomTransitionPage or pageBuilder
├── Spring/bounce/momentum → SpringSimulation, BouncingScrollPhysics
└── Vector/sprite → Rive or Lottie package
```

**GPU-safe:** `transform`, `opacity` → smooth
**CPU-bound:** `width`, `height`, `margin`, `padding` → jank

---

## 📊 State Manager Auto-Detect

Scan imports before writing any state code:

| Import Found | Use |
|-------------|-----|
| `flutter_riverpod` | Riverpod rules |
| `provider` package | Provider rules |
| Neither | Ask user → recommend Riverpod for new projects |

---

## ⚡ Performance Quick Reference

```dart
class MyCard extends StatelessWidget {
  const MyCard({super.key});
  @override
  Widget build(BuildContext context) => const Padding(
    padding: EdgeInsets.all(16),
    child: Text('Hello'),
  );
}

RepaintBoundary(child: AnimatedWidget(...))

ListView.builder(itemCount: n, itemBuilder: (ctx, i) => Item(items[i]))

final name = ref.watch(userProvider.select((u) => u.name));
```

---

## 🧠 CHECKPOINT (Fill Before Any Flutter Work)

```
🧠 FLUTTER CHECKPOINT:

State:      [ Riverpod / Provider / BLoC / Vanilla ]
Navigation: [ GoRouter / auto_route / Navigator 1.0 ]
Design:     [ Material 3 / Cupertino / Custom ]
Platforms:  [ Mobile / Tablet / Desktop / Web ]
Files Read: [ List files read ]

3 Rules I Will Apply:
1. _______________
2. _______________
3. _______________

Anti-Patterns I Will Avoid:
1. _______________
2. _______________
```

> 🔴 **Can't fill checkpoint? → Read the skill files.**

---

## 📋 Checklists

### Per Screen
- [ ] `ConsumerWidget` if Riverpod? `const` constructor?
- [ ] Touch targets ≥ 48dp?
- [ ] Loading + error states defined?
- [ ] Back navigation tested (PopScope or GoRouter canPop)?
- [ ] No hardcoded colors or font sizes?

### Per Animation
- [ ] Animating `transform`/`opacity`, not `width`/`height`?
- [ ] `AnimationController.dispose()` called?
- [ ] Duration ≥ 150ms with easing curve?
- [ ] `RepaintBoundary` on complex painters?

### Pre-Release
- [ ] Run audit script — fix all 🔴 findings
- [ ] `flutter analyze` — no missing const warnings
- [ ] Android back button tested — no stuck screens
- [ ] Dark mode tested — all colors from Theme
- [ ] Tablet layout tested — no overflow
- [ ] All `.when()` handle error state

---

## 📚 Reference Files

| File | Use When |
|------|---------|
| [flutter-design-thinking.md](flutter-design-thinking.md) | **FIRST — prevents AI defaults** |
| [flutter-state-ui.md](flutter-state-ui.md) | Riverpod + Provider rules, patterns, migration |
| [flutter-navigation.md](flutter-navigation.md) | GoRouter, back logic, deep links, tabs |
| [flutter-animations.md](flutter-animations.md) | Implicit, explicit, Hero, transitions, physics |
| [flutter-theme-system.md](flutter-theme-system.md) | Material 3, ColorScheme, TextTheme |
| [flutter-layout-system.md](flutter-layout-system.md) | Responsive, LayoutBuilder, Slivers |
| [flutter-performance.md](flutter-performance.md) | const, RepaintBoundary, DevTools |
| [flutter-custom-paint.md](flutter-custom-paint.md) | Canvas, CustomPainter, pixel-perfect |

---

> Pixel-perfect = every spacing, color, and type choice is intentional and theme-driven. Own the pixels through your design system, not magic numbers.
