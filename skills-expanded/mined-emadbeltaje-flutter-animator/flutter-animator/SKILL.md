---
name: flutter-animator
description: Implement Flutter animations - implicit animations (AnimatedContainer, AnimatedOpacity), TweenAnimationBuilder, built-in *Transition widgets (Fade/Slide/Scale/Rotation/Size/Align/Positioned/DecoratedBox), explicit AnimationController+Tween animations, TweenSequence, physics-based motion (SpringSimulation), Hero shared-element transitions, page route transitions, AnimatedSwitcher, AnimatedCrossFade, AnimatedIcon, animated list/grid insertion and removal, and staggered animations. Use this whenever a Flutter widget needs to animate, fade, slide, scale, bounce, spring, morph, cross-fade, or transition - even if the user just says "make this smoother" or "add motion" without saying the word animation.
---

# Flutter Animations Implementation

## Goal

Implements and manages Flutter animations, selecting the appropriate animation strategy based on UI requirements. Assumes a working Flutter environment, stateful/stateless widget competence, and a standard widget tree structure. Prefer widgets already in the Flutter SDK — do not add `flutter_animate`, Lottie, Rive, or the `animations` package unless the user asked for them or the effect cannot be done with the tree below.

## Instructions

### 1. Determine Animation Strategy (Decision Logic)

Evaluate the UI requirement using the following decision tree. Stop at the first YES — later branches also match earlier ones if you ask generic questions first.

1. **Does a widget fly between two different screens/routes (shared element)?**
   YES → **Hero Animations** (step 3).
2. **Are you animating insertion or removal of items in a scrolling list or grid?**
   YES → **`AnimatedList` / `AnimatedGrid` / `SliverAnimatedList` / `SliverAnimatedGrid`** (step 4) — see `references/list-and-grid-animations.md`.
3. **Are you morphing one Material icon into another (e.g. menu ↔ close)?**
   YES → **`AnimatedIcon`** (step 5).
4. **Are you cross-fading between exactly two specific, known widgets (a binary state)?**
   YES → **`AnimatedCrossFade`** (step 6).
5. **Are you swapping one entire child widget for a different, arbitrary widget — not just a property change?**
   YES → **`AnimatedSwitcher`** (step 7).
6. **Is this a transition between two routes/screens (not a shared-element fly)?**
   YES → **Page Route Transitions** (`PageRouteBuilder`) (step 8).
7. **Does the animation model real-world movement (springs, gravity, velocity, drag-and-release)?**
   YES → **Physics-based animation** (`SpringSimulation`) (step 9).
8. **Do multiple different properties or widgets animate in sequence or overlapping?**
   YES → **Staggered Animations** (step 10).
9. **Does a single property need to pass through more than two values (multiple keyframes), not just a straight A → B?**
   YES → **`TweenSequence`** (step 11).
10. **Is it a simple property change on a single widget, and is there a built-in `Animated*` widget for it?** (color, size, alignment, opacity, padding, scale, slide, rotation, text style, position)
    YES → **Implicit Animations** (step 12).
11. **Is it a one-off tweened transition to a custom value with no dedicated `Animated*` widget, and does it NOT need programmatic play/pause/reverse/repeat control?**
    YES → **`TweenAnimationBuilder`** (step 13) — no controller to manage or dispose.
12. **Do you need programmatic control, and does a built-in `*Transition` widget already match the transform (fade, slide, scale, rotation, size, alignment, position, decoration)?**
    YES → that **`*Transition` widget** (step 14) — see `references/built-in-transitions.md`.
13. **Otherwise**
    YES → **Standard Explicit Animations** (`AnimationController` + `Tween` + `AnimatedBuilder`) (step 15) — the general-purpose fallback.

**STOP AND ASK THE USER:** If the requirement is ambiguous, pause and ask the user to clarify the desired visual effect before writing implementation code.

### 2. Controller lifecycle (shared primitive)

Every technique that needs a controller (steps 5, 9–11, 14, 15) reuses this setup. Physics (step 9) may pass `unbounded: true`. Default duration is 300ms unless the user asked for something else.

```dart
class _MyAnimatedWidgetState extends State<MyAnimatedWidget> with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(milliseconds: 300),
      vsync: this,
    );
  }

  @override
  void dispose() {
    _controller.dispose(); // STRICT REQUIREMENT
    super.dispose();
  }
}
```

### 3. Implement Hero Animations (Shared Element)

To fly a widget between routes, wrap the identical widget tree in both routes with a `Hero` widget using the exact same `tag`. If the source and destination trees differ, set `flightShuttleBuilder` rather than hoping the default flight works.

```dart
// Source Route
Hero(
  tag: 'unique-photo-tag',
  child: Image.asset('photo.png', width: 100),
)

// Destination Route
Hero(
  tag: 'unique-photo-tag',
  child: Image.asset('photo.png', width: 300),
)
```

### 4. Implement Animated Insertion/Removal in Lists and Grids

To animate items being added to or removed from a scrolling list or grid, use `AnimatedList`/`AnimatedGrid` (or their sliver equivalents inside a `CustomScrollView`). Full examples and the removal-builder gotcha (capture the removed item before it leaves the backing data list) are in `references/list-and-grid-animations.md`. Do not use `AnimatedSwitcher` or manual `setState` on a `ListView` for this — the animation needs the AnimatedList*/AnimatedGrid* family to run correctly on insert/remove.

### 5. Implement AnimatedIcon

Only the predefined `AnimatedIcons.*` pairs morph (menu ↔ close, play ↔ pause, etc.). Arbitrary `IconData` will not. Drive `progress` with the controller from step 2.

```dart
AnimatedIcon(
  icon: AnimatedIcons.menu_close,
  progress: _controller, // 0.0 = menu, 1.0 = close
  semanticLabel: 'Menu',
)

// Toggle:
onPressed: () => _controller.isCompleted ? _controller.reverse() : _controller.forward(),
```

### 6. Implement AnimatedCrossFade

When the choice is strictly binary — cross-fading between exactly two known widgets — `AnimatedCrossFade` is simpler than `AnimatedSwitcher` and needs no `Key`s. If the two children have different sizes, set `alignment` and/or `layoutBuilder` or the layout will jump when the fade finishes.

```dart
AnimatedCrossFade(
  duration: const Duration(milliseconds: 300),
  crossFadeState: _showFirst ? CrossFadeState.showFirst : CrossFadeState.showSecond,
  firstChild: const Icon(Icons.check_circle, size: 48),
  secondChild: const Icon(Icons.error, size: 48),
)
```

Use `AnimatedSwitcher` (step 7) instead once there are more than two possible children, or the children aren't fixed/known in advance.

### 7. Implement AnimatedSwitcher

To animate the replacement of one child widget with a completely different, arbitrary widget, use `AnimatedSwitcher`. Every possible child MUST carry a distinct `Key` — `AnimatedSwitcher` diffs on the key to detect a switch, and silently skips the transition if two children share a key (or have none).

```dart
AnimatedSwitcher(
  duration: const Duration(milliseconds: 300),
  transitionBuilder: (child, animation) => FadeTransition(opacity: animation, child: child),
  child: _isLoading
      ? const CircularProgressIndicator(key: ValueKey('loading'))
      : Text('Loaded', key: ValueKey('loaded')),
)
```

### 8. Implement Page Route Transitions

To animate transitions between routes, use `PageRouteBuilder` and chain a `CurveTween` with a `Tween<Offset>`. If the project already uses `GoRouter` or `ThemeData.pageTransitionsTheme`, hook the transition there instead of a one-off `Navigator.push`.

```dart
Route<void> _createRoute() {
  return PageRouteBuilder(
    pageBuilder: (context, animation, secondaryAnimation) => const DestinationPage(),
    transitionsBuilder: (context, animation, secondaryAnimation, child) {
      const begin = Offset(0.0, 1.0);
      const end = Offset.zero;
      const curve = Curves.ease;

      final tween = Tween(begin: begin, end: end).chain(CurveTween(curve: curve));

      return SlideTransition(
        position: animation.drive(tween),
        child: child,
      );
    },
  );
}
```

### 9. Implement Physics-Based Animations

For realistic motion (e.g., snapping back after a drag), replace the step 2 controller with `AnimationController.unbounded(vsync: this)`, feed drag velocity in from a `GestureDetector`, and apply a `SpringSimulation`. `stiffness: 1` is a demo value — use ~150–400 for UI snaps.

```dart
late Animation<Alignment> _animation;

void _runSpringAnimation(Offset pixelsPerSecond, Size size, Alignment dragAlignment) {
  _animation = _controller.drive(
    AlignmentTween(begin: dragAlignment, end: Alignment.center),
  );

  final unitsPerSecondX = pixelsPerSecond.dx / size.width;
  final unitsPerSecondY = pixelsPerSecond.dy / size.height;
  final unitsPerSecond = Offset(unitsPerSecondX, unitsPerSecondY);
  final unitVelocity = unitsPerSecond.distance;

  const spring = SpringDescription(mass: 1, stiffness: 170, damping: 12);
  final simulation = SpringSimulation(spring, 0, 1, -unitVelocity);

  _controller.animateWith(simulation);
}
```

### 10. Implement Staggered Animations

For sequential or overlapping animations across multiple properties, use a single `AnimationController` (step 2) and define multiple `Tween`s with `Interval` curves.

```dart
class StaggerAnimation extends StatelessWidget {
  StaggerAnimation({super.key, required this.controller}) :
    opacity = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(
        parent: controller,
        curve: const Interval(0.0, 0.100, curve: Curves.ease),
      ),
    ),
    width = Tween<double>(begin: 50.0, end: 150.0).animate(
      CurvedAnimation(
        parent: controller,
        curve: const Interval(0.125, 0.250, curve: Curves.ease),
      ),
    );

  final AnimationController controller;
  final Animation<double> opacity;
  final Animation<double> width;

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: controller,
      builder: (context, child) {
        return Opacity(
          opacity: opacity.value,
          child: Container(width: width.value, height: 50, color: Colors.blue),
        );
      },
    );
  }
}
```

### 11. Implement TweenSequence

When a single property must pass through more than two values — not just begin → end — use `TweenSequence` instead of chaining separate animations by hand.

```dart
final Animation<double> _animation = TweenSequence<double>([
  TweenSequenceItem(tween: Tween(begin: 0.0, end: 100.0), weight: 1),
  TweenSequenceItem(tween: Tween(begin: 100.0, end: 50.0), weight: 1),
  TweenSequenceItem(tween: Tween(begin: 50.0, end: 200.0), weight: 1),
  TweenSequenceItem(tween: Tween(begin: 200.0, end: 0.0), weight: 1),
]).animate(_controller);
```

`weight` sets each stage's share of the controller's total duration — equal weights divide the timeline evenly; this is distinct from **Staggered Animations** (step 10), which staggers *multiple different* properties/widgets rather than moving one property through multiple stages.

### 12. Implement Implicit Animations

For simple transitions between values, use implicit animation widgets. Do not manually manage state or controllers. Built-in options include `AnimatedContainer`, `AnimatedOpacity`, `AnimatedAlign`, `AnimatedPadding`, `AnimatedPositioned` (inside a `Stack`), `AnimatedScale`, `AnimatedSlide`, `AnimatedRotation`, `AnimatedSize`, `AnimatedDefaultTextStyle`, and `AnimatedPhysicalModel`. Default to ~300ms and `Curves.easeInOut` unless the user asked for a bounce or overshoot.

When `MediaQuery.disableAnimationsOf(context)` is true, use `Duration.zero` (or skip the animation) so reduced-motion users are not forced through the motion.

```dart
AnimatedContainer(
  duration: const Duration(milliseconds: 300),
  curve: Curves.easeInOut,
  width: _isExpanded ? 200.0 : 100.0,
  height: _isExpanded ? 200.0 : 100.0,
  decoration: BoxDecoration(
    color: _isExpanded ? Colors.green : Colors.blue,
    borderRadius: BorderRadius.circular(_isExpanded ? 50.0 : 8.0),
  ),
  child: const FlutterLogo(),
)
```

### 13. Implement TweenAnimationBuilder

For a one-off animation to a custom value with no dedicated implicit widget, and no need to programmatically play/pause/reverse it, use `TweenAnimationBuilder`. It manages its own internal controller — nothing to dispose. It automatically re-animates from the current value whenever `end` changes on rebuild.

```dart
TweenAnimationBuilder<double>(
  tween: Tween<double>(begin: 0.0, end: _targetRotation),
  duration: const Duration(milliseconds: 300),
  curve: Curves.easeInOut,
  builder: (context, value, child) {
    return Transform.rotate(angle: value, child: child);
  },
  child: const FlutterLogo(), // static subtree passed as child for performance
)
```

### 14. Implement Built-in Transition Widgets

Before reaching for `AnimatedBuilder`, check whether a built-in `*Transition` widget already renders the effect — they drive the same `Animation` object but avoid boilerplate. Reuse the controller from step 2. Two of the most common:

```dart
FadeTransition(opacity: _controller, child: const FlutterLogo())

SlideTransition(
  position: Tween<Offset>(begin: const Offset(0, 1), end: Offset.zero).animate(_controller),
  child: const FlutterLogo(),
)
```

`AnimationController` **is** an `Animation<double>`, so passing `_controller` is correct for `FadeTransition.opacity`, `ScaleTransition.scale`, `RotationTransition.turns`, and `SizeTransition.sizeFactor`. For `Offset` / `Alignment` / `Decoration` / `RelativeRect`, wrap with the matching `Tween`.

The full catalog — `ScaleTransition`, `RotationTransition`, `SizeTransition`, `AlignTransition`, `PositionedTransition`, `RelativePositionedTransition`, and `DecoratedBoxTransition` — is in `references/built-in-transitions.md`. Read it before falling back to a manual `AnimatedBuilder` (step 15).

### 15. Implement Standard Explicit Animations (fallback)

When no `*Transition` widget matches the property, drive a custom `Tween` through `AnimatedBuilder`. Same controller lifecycle as step 2.

```dart
late Animation<double> _animation;

@override
void initState() {
  super.initState();
  _controller = AnimationController(
    duration: const Duration(milliseconds: 300),
    vsync: this,
  );
  _animation = Tween<double>(begin: 0, end: 300).animate(
    CurvedAnimation(parent: _controller, curve: Curves.easeOut),
  );
  _controller.forward();
}

@override
Widget build(BuildContext context) {
  return AnimatedBuilder(
    animation: _animation,
    builder: (context, child) {
      return SizedBox(
        height: _animation.value,
        width: _animation.value,
        child: child,
      );
    },
    child: const FlutterLogo(), // Passed as child for performance
  );
}
```

### 16. Validate-and-Fix Loop

After generating animation code, verify the following:

1. Does the `State` class use `SingleTickerProviderStateMixin` (or `TickerProviderStateMixin` for multiple controllers)?
2. Is `_controller.dispose()` explicitly called in the `dispose()` method?
3. If using `AnimatedBuilder` or `TweenAnimationBuilder`, is the static widget passed to the `child` parameter rather than rebuilt inside the `builder` function?
4. If using `AnimatedSwitcher`, does every branch of the child expression have a distinct, stable `Key`?
5. If using a `*Transition` widget: raw `_controller` is fine where `Animation<double>` is required; `Offset` / `Alignment` / `Decoration` / `RelativeRect` parameters MUST go through the matching `Tween`.
6. If using `AnimatedList`/`AnimatedGrid`, is the backing data list mutated in the correct order relative to `insertItem`/`removeItem`, and does the removal builder capture the removed item's data directly rather than re-reading it from the now-mutated list by index?
7. Before hand-rolling `AnimatedBuilder` for a fade/slide/scale/rotation/size/align/position/decoration effect, was a built-in `*Transition` widget considered?
8. If `MediaQuery.disableAnimationsOf(context)` is true, is duration `Duration.zero` (or the animation skipped)?
9. If using `AnimatedIcon`, is the icon one of `AnimatedIcons.*` — not an arbitrary `IconData`?
10. If using `AnimatedCrossFade`, are the two children similar in size, or is `alignment` / `layoutBuilder` set so the layout does not jump?
11. Was a new animation package (`flutter_animate`, Lottie, Rive, `animations`) added without the user asking?

If any of these are missing, fix the code immediately before presenting it to the user.

## Constraints

- **SDK first:** Prefer Flutter framework widgets. Do not add `flutter_animate`, Lottie, Rive, or the `animations` package unless the user asked for them or the tree above cannot express the effect.
- **Reduced motion:** When `MediaQuery.disableAnimationsOf(context)` is true, use `Duration.zero` or skip decorative motion.
- **Strict Disposal:** You MUST include `dispose()` methods for all `AnimationController` instances to prevent memory leaks. `TweenAnimationBuilder` manages its own controller internally and does not need manual disposal.
- **No URLs:** Do not include external links or URLs in the output or comments.
- **Immutability:** Treat `Tween` and `Curve` classes as stateless and immutable. Do not attempt to mutate them after instantiation.
- **Performance:** Always use `AnimatedBuilder`/`AnimatedWidget`/`*Transition` widgets instead of calling `setState()` inside a controller's `addListener` when building complex widget trees. Pass unchanging subtrees via the `child` parameter for the same reason.
- **Hero Tags:** Hero tags MUST be identical and unique per route transition. Do not use generic tags like `'image'` if multiple heroes exist.
- **AnimatedSwitcher Keys:** Every widget passed as `AnimatedSwitcher`'s child MUST have a unique `Key`, or Flutter cannot detect the switch and the transition will silently not play.
- **AnimatedIcon pairs:** `AnimatedIcon` only morphs `AnimatedIcons.*` pairs. Use `AnimatedSwitcher` for arbitrary icons.
- **AnimatedCrossFade size:** Differently sized children jump at the end of the fade unless `alignment` / `layoutBuilder` is set.
- **RotationTransition Units:** `RotationTransition.turns` is in fractions of a full turn (`1.0` = 360°), not radians — don't reuse a radian value meant for `Transform.rotate`.
- **Typed animations:** Raw `_controller` is valid for `Animation<double>` slots. Wrap it with the matching `Tween` for `Offset`, `Alignment`, `Decoration`, and `RelativeRect`.
- **AnimatedList/Grid Ordering:** Capture the item being removed before mutating the backing data list, since the removal animation must render a widget for an item that's already gone from the list by the time it plays.
