---
name: mobile-performance
description: Flutter performance playbook — frame budget, const widgets, RepaintBoundary, image cache, shader warm-up, isolate offloading, DevTools profiling, deferred imports, app startup measurement. MANDATORY TRIGGERS - "performance", "frame budget", "jank", "shader compilation", "repaintboundary", "image cache", "devtools timeline", "isolate", "deferred imports", "tree-shake-icons", "app startup", "--release perf".
allowed-tools: Read, Glob, Edit, Write, Bash
---

# Skill: mobile-performance

## When to use

Optimizing a slow screen, investigating jank reports from QA, profiling
a new feature before merge, or doing a pre-release performance audit.
Always profile in `--profile` mode on a physical device; never interpret
simulator timings.

---

## Inputs

- Screen or feature slug under investigation
- Device tier (`high` / `mid` / `low`) — see budgets below
- Sentry or DevTools trace attached (if investigating a report)

---

## Frame budgets

| Device tier | Example device | Frame budget | Target steady-state |
|------------|----------------|-------------|---------------------|
| High-end (120 Hz) | iPhone 15 Pro, Pixel 8 Pro | 8.3 ms | ≤ 6 ms |
| Mid-range (60 Hz) | Pixel 7, Galaxy A54 | 16.7 ms | ≤ 12 ms |
| Low-end baseline (60 Hz) | Pixel 4a, Galaxy A32 | 16.7 ms | ≤ 14 ms |

A frame that exceeds its budget causes a dropped frame (jank). A good CI
integration test asserts no frame > 16 ms on your primary scroll path on
a mid-tier emulator (e.g. Pixel 7).

References: [Flutter Performance Best Practices](https://docs.flutter.dev/perf/best-practices), [Flutter Rendering Performance](https://docs.flutter.dev/perf/rendering-performance)

---

## Steps

### 1. `const` everywhere it compiles

The single highest-impact change. Every widget whose constructor arguments
are compile-time constants must be `const`. Set the `prefer_const_constructors`
lint to `error` level so failing to add `const` blocks CI.

```dart
// Good
const AppButton(label: 'Submit', onPressed: _onSubmit),
const SizedBox(height: Spacing.lg),

// Bad — missed const, forces unnecessary widget instantiation
SizedBox(height: 16),
```

Run `dart fix --apply` to batch-apply `const` suggestions.

### 2. RepaintBoundary around dynamic widgets

Widgets that repaint frequently (counters, live tickers, avatar badges)
must be wrapped in `RepaintBoundary`. This prevents their repaints from
invalidating the surrounding list cell.

```dart
// List cell — a live-updating sub-widget should not redraw its siblings
Column(
  children: [
    _AuthorRow(post: post),          // static — no RepaintBoundary needed
    _PostBody(post: post),           // static
    RepaintBoundary(
      child: _VotePill(uri: post.uri),  // updates on vote
    ),
    RepaintBoundary(
      child: _LiveValueTracker(id: post.trackedId), // ticks every ~1s
    ),
  ],
)
```

Also wrap any image grid — blurhash/placeholder decode is GPU work that
should not invalidate sibling widgets.

### 3. Image cache tuning

In `lib/bootstrap.dart`, increase `imageCache` from the default 100 MB:

```dart
PaintingBinding.instance.imageCache.maximumSizeBytes = 200 * 1024 * 1024; // 200 MB
PaintingBinding.instance.imageCache.maximumSize = 300; // max images
```

For `Image.network` or `CachedNetworkImage`, always specify `cacheWidth` and
`cacheHeight` in logical pixels scaled to the device pixel ratio:

```dart
CachedNetworkImage(
  imageUrl: post.images.first.url,
  memCacheWidth: (cellWidth * MediaQuery.devicePixelRatioOf(context)).round(),
  memCacheHeight: (cellHeight * MediaQuery.devicePixelRatioOf(context)).round(),
  placeholder: (_, __) => BlurHashWidget(hash: post.images.first.blurHash),
)
```

Pre-cache the first visible page of avatars after list load:

```dart
for (final post in firstPage) {
  precacheImage(NetworkImage(post.author.avatarUrl), context);
}
```

### 4. Shader compilation warm-up

Shader compilation jank occurs on first render of a new widget path.
Warm up SkSL shaders:

```bash
# 1. Record shader cache during a manual run
flutter run --profile --cache-sksl-path shaders.sksl

# 2. Ship the cache with the build
flutter build appbundle --bundle-sksl-path shaders.sksl

# 3. Regenerate shaders after significant UI changes
```

Check the DevTools Timeline for "Compile shader" events. If they appear
after the first frame, the widget path is not in the shader cache.

Reference: [Shader Compilation Jank](https://docs.flutter.dev/perf/shader)

### 5. DevTools timeline + frame analysis recipe

```bash
# Profile on a physical device
flutter run --profile

# Open DevTools
flutter pub global run devtools
```

In the Timeline tab:
1. Start recording, perform the janky interaction (list scroll, page push).
2. Stop recording. Filter to "UI" and "Raster" threads.
3. Click any red frame (> 16 ms). Expand the flame chart.
4. Look for: large `build` entries (expensive `build()` methods), large
   `paint` entries (missing `RepaintBoundary`), large `layout` entries
   (expensive `RenderObject.performLayout`).

Common findings:
- `ListView.build` calling `setState` on parent — use `BlocSelector` to
  narrow rebuilds.
- `Opacity` inside a list — replace with `ColorFiltered` or alpha-baked
  colors (anti-pattern forbidden by lint).
- `BoxDecoration(boxShadow: [...])` inside list cells — bake into the
  background or use Material `elevation`.

Reference: [Flutter DevTools](https://docs.flutter.dev/tools/devtools)

### 6. Isolate offloading

Work that takes > 4 ms on the UI isolate must move to a background
isolate. Example thresholds — tune to your app's measured hotspots:

| Work | Threshold | Pattern |
|------|-----------|---------|
| JSON parsing | > 50 KB payload | `Isolate.run(() => jsonDecode(raw))` |
| Image compression | any | `Isolate.run(() => compress(bytes))` |
| Heavy list recomputation (50+ items) | > 4 ms measured | `Isolate.run(() => recompute(items))` |

```dart
// lib/core/network/json_parser.dart
Future<T> parseInBackground<T>(
  String raw,
  T Function(Map<String, dynamic>) fromJson,
) async {
  final map = await Isolate.run(() => jsonDecode(raw) as Map<String, dynamic>);
  return fromJson(map);
}
```

Use `Isolate.run` (Dart 2.19+) for one-shot tasks. A persistent
background isolate with `ReceivePort` is only needed for a continuous
computation loop — most apps never need this.

### 7. Deferred imports

Heavy flows that are rarely used should be loaded lazily:

```dart
import 'package:app/features/onboarding/verification_flow.dart' deferred as verification;
import 'package:app/features/detail/chart_view.dart' deferred as chart;
import 'package:app/shared/widgets/full_screen_image_viewer.dart' deferred as img;

// Load on first use:
await verification.loadLibrary();
verification.VerificationFlow.push(context);
```

Add `loadLibrary()` call at route definition so the library is pre-loaded
when the user navigates toward the screen, not at the moment of navigation:

```dart
GoRoute(
  path: '/verify',
  onEnter: (state) => verification.loadLibrary(),
  builder: (_, __) => const verification.VerificationFlow(),
),
```

### 8. `--obfuscate --split-debug-info` and `--tree-shake-icons`

Always include these flags in production release builds (keep them in
the CI pipeline — do not remove):

```bash
flutter build appbundle \
  --release \
  --obfuscate \
  --split-debug-info=./build/symbols/prod/$BUILD_NUMBER \
  --tree-shake-icons \
  ...
```

`--tree-shake-icons` eliminates unused icon glyphs from the font. This only
works when `IconData` values are `const`.

Upload debug info to your crash reporter (e.g. Sentry) immediately after
build — they are required for deobfuscating crash stack traces.

### 9. App startup measurement

Set explicit cold-start and warm-start targets for your app (a common
baseline: cold start < 2.5 s on mid-tier hardware, warm start < 1.5 s)
and track them.

```dart
// lib/bootstrap.dart
void main() async {
  final stopwatch = Stopwatch()..start();
  WidgetsBinding.instance.addPostFrameCallback((_) {
    stopwatch.stop();
    Sentry.addBreadcrumb(Breadcrumb(
      message: 'first_frame',
      data: {'ms': stopwatch.elapsedMilliseconds},
    ));
  });
  runApp(const MyApp());
}
```

For cold-start optimization:
- Use `WidgetsBinding.deferFirstFrame()` / `allowFirstFrame()` while
  loading critical assets (theme, i18n).
- Local database open (e.g. Drift `AppDatabase.open()`) is async and
  should happen in `bootstrap.dart` before `runApp`.
- `GetIt.I.allReady()` (or your DI container's equivalent) must complete
  before showing the first screen.

### 10. Low-end Android profiling baseline

Every release should pass a scroll performance test on a low-end device
(e.g. Pixel 4a or equivalent ~$200 device). Example targets — tune to
your app:

| Metric | Target |
|--------|--------|
| List cold-start first paint | ≤ 2,500 ms |
| List scroll jank rate | < 2% frames > 16 ms |
| Memory footprint after 100 items | < 200 MB RSS |

Run in CI nightly, not per PR (too slow). Alert on regression > 10%.

---

## Performance budget per surface

See `.claude/skills/mobile-performance/templates/performance-budget.md`
for the complete target metrics table.

---

## Output

- `RepaintBoundary` added around identified hot widgets
- `cacheWidth/cacheHeight` set on all `CachedNetworkImage` instances
- Heavy work moved to `Isolate.run`
- DevTools timeline screenshot attached to PR for performance-impacting changes
- Startup timings recorded in Sentry breadcrumb

---

## Anti-patterns

- `Opacity` in a scroll list — use `AnimatedOpacity` + `RepaintBoundary`
  or alpha-baked colors. Lint `no_opacity_in_list` enforces this.
- `ListView(children: [...])` — always `ListView.builder` for any list
  that could exceed 4 items.
- `setState` inside a list item builder — use `BlocSelector` or
  `ValueListenableBuilder` scoped to the item.
- JSON parsing on the UI isolate for payloads > 50 KB.
- `BoxDecoration(boxShadow: [...])` inside list cells — renders a new
  layer per cell; use `elevation` or bake into background.
- Calling `PaintingBinding.instance.imageCache.clear()` in production —
  this invalidates the entire image cache.
- Profiling in `--debug` mode — always use `--profile` on a physical device.

---

## See also

- `.claude/skills/device-matrix/SKILL.md` — device tiers and CI device picks
- your project's mobile standards doc — frame / startup / crash budgets
- your project's frontend architecture doc — Performance section
