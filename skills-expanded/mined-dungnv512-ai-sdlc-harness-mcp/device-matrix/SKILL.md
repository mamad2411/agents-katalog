---
name: device-matrix
description: Golden test device matrix for Flutter apps — required device list (iPhone SE, Pixel 4a, Galaxy A32, iPad), light/dark/dim theme matrix, textScaler matrix, locale matrix, reduced-motion matrix, CI device picks, alchemist goldenTest config, golden file directory convention. MANDATORY TRIGGERS - "device matrix", "golden device", "integration test device", "simulator", "emulator", "iphone se", "pixel 7", "tablet", "foldable", "screen size", "breakpoint".
allowed-tools: Read, Glob, Edit, Write, Bash
---

# Skill: device-matrix

## When to use

Writing a new alchemist golden test, setting up CI device configuration,
adding a new widget to the catalogue, or investigating a golden diff
that appears on one device but not another.

---

## Inputs

- Widget or page slug being tested
- States the widget can be in (loading, empty, error, success, etc.)

---

## Device inventory

### Phone golden devices

| ID | Device | Width (dp) | Density | Notes |
|----|--------|------------|---------|-------|
| `iphone15` | iPhone 15 | 393 dp | 3x | Primary golden reference |
| `iphone15plus` | iPhone 15 Plus | 430 dp | 3x | Large phone |
| `iphoneSE3` | iPhone SE (3rd gen) | 375 dp | 2x | Smallest modern iOS device (4.7") |
| `pixel7` | Pixel 7 | 412 dp | 2.625x | Primary Android reference |
| `pixel7pro` | Pixel 7 Pro | 412 dp | 3.5x | Large Android |
| `pixel4a` | Pixel 4a | 393 dp | 2.75x | Low-end baseline (5.8") |
| `galaxyA32` | Galaxy A32 | 360 dp | 3x | Budget Android; smallest safe width |

### Tablet golden device

| ID | Device | Width (dp) | Orientation |
|----|--------|------------|-------------|
| `ipadPro11` | iPad Pro 11" | 834 dp | Portrait only (MVP) |

### Foldable (nightly only)

| ID | Device | Width (dp) | Notes |
|----|--------|------------|-------|
| `galaxyZFold_unfolded` | Galaxy Z Fold 5 (unfolded) | 904 dp | Nightly; not per-PR |

---

## Test matrix dimensions

For every public widget, capture goldens across all applicable dimensions:

| Dimension | Values |
|-----------|--------|
| **Theme** | `light`, `dark`, `dim` |
| **TextScaler** | `1.0`, `1.3`, `1.5` |
| **Locale** | `vi`, `en` |
| **Reduced motion** | `false`, `true` (only when widget has animations) |
| **Device** | See per-PR vs nightly tables below |

**Per-PR (mandatory):** `iphone15` + `pixel7` + `iphoneSE3` (the small device is the overflow risk)

**Nightly (full matrix):** All phone devices + `ipadPro11` + `galaxyA32`

---

## alchemist configuration

```dart
// test/alchemist_config.dart
AlchemistConfig get testConfig => const AlchemistConfig(
  platformGoldensConfig: PlatformGoldensConfig(enabled: false),
  ciGoldensConfig: CiGoldensConfig(
    enabled: true,
    obscureText: false,
  ),
  theme: null, // theme is passed per test via pumpGolden
);
```

Reference: [alchemist pub.dev](https://pub.dev/packages/alchemist)

---

## goldenTest pattern

```dart
// test/features/post/golden/post_card_golden_test.dart
@Tags(['golden'])
void main() {
  for (final theme in [lightTheme(), darkTheme(), dimTheme()]) {
    for (final scaler in [1.0, 1.3, 1.5]) {
      goldenTest(
        'PostCard | ${theme.brightness.name} | scale ${scaler}x',
        fileName: 'post_card_${theme.brightness.name}_scale_${scaler.toString().replaceAll('.', '_')}',
        builder: () => GoldenTestGroup(
          columns: 1,
          children: [
            GoldenTestScenario(
              name: 'default',
              child: _postCardScaffold(theme, scaler, _mockPost()),
            ),
            GoldenTestScenario(
              name: 'loading',
              child: _postCardScaffold(theme, scaler, null),
            ),
            GoldenTestScenario(
              name: 'long_body',
              child: _postCardScaffold(theme, scaler, _longPost()),
            ),
            GoldenTestScenario(
              name: 'with_image',
              child: _postCardScaffold(theme, scaler, _postWithImage()),
            ),
          ],
        ),
      );
    }
  }
}

Widget _postCardScaffold(ThemeData theme, double scaler, Post? post) {
  return MaterialApp(
    theme: theme,
    home: MediaQuery(
      data: MediaQueryData(
        size: const Size(393, 852), // iPhone 15 logical size
        devicePixelRatio: 3.0,
        textScaler: TextScaler.linear(scaler),
      ),
      child: post != null
          ? SbPostCard(post: post)
          : const SbPostCard.skeleton(),
    ),
  );
}
```

---

## Golden file directory convention

```
test/
  features/
    post/
      golden/
        post_card_light_scale_1_0.png
        post_card_light_scale_1_3.png
        post_card_light_scale_1_5.png
        post_card_dark_scale_1_0.png
        post_card_dark_scale_1_3.png
        post_card_dark_scale_1_5.png
        post_card_dim_scale_1_0.png
    feed/
      golden/
        feed_page_light_scale_1_0.png
        ...
  golden/
    design_system/        # atom + molecule goldens
      sb_button_*.png
      sb_avatar_*.png
```

Rule: one golden file per (widget, theme, scale) tuple. Do not combine
multiple scenarios in one file when they represent distinct failure modes.

---

## CI configuration

```yaml
# .github/workflows/ci.yml (excerpt)
- name: Golden tests
  run: flutter test --tags=golden
  # macOS runner required for font rendering consistency
  # (alchemist's CI goldens are macOS-baseline)
```

**Font seeding:** macOS CI runners must have the app fonts pre-loaded.
In `test/test_helpers.dart`:

```dart
Future<void> pumpGolden(
  WidgetTester tester,
  Widget widget, {
  ThemeData? theme,
  double textScale = 1.0,
  Locale locale = const Locale('vi'),
  Size size = const Size(393, 852),
}) async {
  await loadAppFonts();  // from alchemist, loads fonts from pubspec
  await tester.pumpWidget(
    MaterialApp(
      theme: theme ?? lightTheme(),
      locale: locale,
      localizationsDelegates: AppLocalizations.localizationsDelegates,
      home: MediaQuery(
        data: MediaQueryData(
          size: size,
          textScaler: TextScaler.linear(textScale),
        ),
        child: widget,
      ),
    ),
  );
}
```

**Golden update policy:**
- Never run `--update-goldens` in CI automatically.
- Run locally, attach diff screenshots to PR, then commit the new `.png`.
- Diff threshold: 0 pixels (exact match). Any pixel diff is a failed test.

---

## Integration test device picks

| Platform | CI device | Rationale |
|----------|-----------|-----------|
| Android | Pixel 7 API 34 emulator | Representative mid-range, available on GitHub Actions |
| Android (low-end gate) | Pixel 4a API 33 emulator (nightly) | Catches layout overflows on small screens |
| iOS | iPhone 15 Pro simulator | Matches primary golden reference |

Reference: [Flutter integration_test](https://docs.flutter.dev/cookbook/testing/integration/introduction)

---

## Material 3 breakpoints reference

| Class | Width | Typical usage |
|-------|-------|---------------|
| Compact | 0–599 dp | Default — all phone layouts |
| Medium | 600–839 dp | iPad portrait / small tablet |
| Expanded | 840+ dp | iPad landscape / tablet split-view |

In MVP, all layouts target Compact. Do not add `if (width > 600)` branches
without a tablet ADR.

Reference: [Material 3 device breakpoints](https://m3.material.io/foundations/layout/applying-layout/window-size-classes)

---

## Output

For each new widget:
- Golden files for `light` + `dark` themes, `textScaler 1.0` + `1.5`,
  on `iphone15` device size — minimum 4 files per widget state.
- `@Tags(['golden'])` annotation on all golden tests.
- Golden files committed to `test/features/<slug>/golden/`.
- PR description includes "Goldens updated" note with count of changed files.

---

## Anti-patterns

- Running `flutter test --update-goldens` in CI automatically — only run
  locally and commit the diff.
- Using `tester.pumpAndSettle()` in golden tests with animations enabled
  — animations must be disabled or use `pump(Duration.zero)` for determinism.
- Hardcoded `Size(375, 812)` everywhere — use the device constant from the
  table above and test on `iphoneSE3` (375 dp) for overflow detection.
- Skipping `dim` theme in goldens — the feed is used at night; dim-mode
  regressions are common.
- Committing goldens generated on Linux — font rendering differs from macOS;
  always use a macOS runner or the CI golden config.

---

## See also

- `.claude/skills/golden-tests/SKILL.md` — alchemist setup and patterns
- `.claude/skills/mobile-accessibility/SKILL.md` — a11y guideline checks in widget tests
- `docs/ai-sdlc/mobile-standards.md` — golden coverage requirement per PR
