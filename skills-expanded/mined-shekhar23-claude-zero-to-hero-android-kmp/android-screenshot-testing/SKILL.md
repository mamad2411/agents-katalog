---
name: android-screenshot-testing
description: |
  Screenshot and visual regression testing for Android/Compose - Roborazzi setup, golden image workflow, record vs verify modes, CI integration, dark mode and RTL variants, and Compose preview screenshot tests. Use this skill whenever adding visual regression coverage, setting up Roborazzi, managing golden images in CI, testing dark mode or font-scale variants, or deciding between screenshot, unit, and manual tests. Trigger on phrases like "screenshot test", "Roborazzi", "Paparazzi", "golden image", "visual regression", "snapshot test", "preview test", "record mode", "visual diff", or "screenshot CI".
---

# Android Screenshot Testing (Roborazzi)

## Overview

Screenshot tests catch visual regressions that unit tests and instrumentation tests miss — layout shifts, wrong colors, clipped text, broken dark mode. Roborazzi is preferred over Paparazzi for Compose projects because it runs on Robolectric (no JVM rendering quirks), supports Compose natively, and is actively maintained alongside the Compose ecosystem.

**When to screenshot-test vs other test types:**

| Test type | When to use |
|---|---|
| Screenshot test | Stable, rendered UI components; dark mode/RTL variants; design-system atoms; complex layouts |
| Unit test | ViewModel logic, state transformations, domain rules |
| Compose UI test (`ComposeTestRule`) | Interaction flows, click handlers, navigation |
| Manual test | First-time animations, haptics, platform-specific edge cases |

Screenshot tests are not a replacement for unit or UI tests — they are a third, complementary layer.

---

## Dependency Setup

```toml
# gradle/libs.versions.toml
[versions]
roborazzi = "1.20.0"
robolectric = "4.13"

[libraries]
roborazzi = { module = "io.github.takahirom.roborazzi:roborazzi", version.ref = "roborazzi" }
roborazzi-compose = { module = "io.github.takahirom.roborazzi:roborazzi-compose", version.ref = "roborazzi" }
roborazzi-junit-rule = { module = "io.github.takahirom.roborazzi:roborazzi-junit-rule", version.ref = "roborazzi" }
robolectric = { module = "org.robolectric:robolectric", version.ref = "robolectric" }

[plugins]
roborazzi = { id = "io.github.takahirom.roborazzi", version.ref = "roborazzi" }
```

```kotlin
// build.gradle.kts (:feature:myfeature or :core:ui)
plugins {
    alias(libs.plugins.roborazzi)
}

android {
    testOptions {
        unitTests {
            isIncludeAndroidResources = true
        }
    }
}

dependencies {
    testImplementation(libs.roborazzi)
    testImplementation(libs.roborazzi.compose)
    testImplementation(libs.roborazzi.junit.rule)
    testImplementation(libs.robolectric)
    testImplementation(libs.androidx.compose.ui.test.junit4)
}
```

---

## Writing a Screenshot Test

### Basic Composable Test

```kotlin
@RunWith(RobolectricTestRunner::class)
@GraphicsMode(GraphicsMode.Mode.NATIVE)
@Config(qualifiers = RobolectricDeviceQualifiers.Pixel6)
class NoteCardScreenshotTest {

    @get:Rule
    val composeTestRule = createComposeRule()

    @Test
    fun noteCard_defaultState() {
        composeTestRule.setContent {
            AppTheme {
                NoteCard(
                    note = NoteUi(id = "1", title = "Meeting Notes", date = "Mar 29"),
                    onClick = {}
                )
            }
        }
        composeTestRule.onRoot().captureRoboImage()
    }
}
```

`captureRoboImage()` saves the screenshot to `src/test/snapshots/images/<ClassName>_<testName>.png` by default. On first run (record mode) it creates the golden. On subsequent runs it diffs against the stored golden.

### Common Device Qualifiers

```kotlin
// Use RobolectricDeviceQualifiers for reproducible device configs
@Config(qualifiers = RobolectricDeviceQualifiers.Pixel6)        // 1080x2400, xxhdpi
@Config(qualifiers = RobolectricDeviceQualifiers.Pixel6Pro)     // 1440x3120, xxxhdpi
@Config(qualifiers = RobolectricDeviceQualifiers.MediumTablet)  // 768x1024, mdpi

// Or compose your own qualifier string:
// "w411dp-h891dp-xxhdpi-night"  (night mode)
// "w411dp-h891dp-xxhdpi-land"   (landscape)
```

---

## Golden Image Workflow

### Record Mode (Create / Update Goldens)

```bash
# Run once to record goldens:
./gradlew :feature:notes:recordRoborazziDebug

# Or record a specific test:
./gradlew :feature:notes:recordRoborazziDebug --tests "com.example.notes.NoteCardScreenshotTest"
```

Goldens are committed to git alongside the test source. This makes diffs reviewable in PRs.

### Verify Mode (Default in CI)

```bash
# Default test run — compares against stored goldens, fails on any diff:
./gradlew :feature:notes:verifyRoborazziDebug

# Or use the standard test task (verification is automatic when goldens exist):
./gradlew :feature:notes:testDebugUnitTest
```

### Golden File Location

By default goldens are stored at:

```
<module>/src/test/snapshots/images/
```

Commit these files to git. Treat them as source artifacts — the same as code. Each PR that changes UI should include updated goldens in the diff.

```
# .gitignore — do NOT ignore goldens
# src/test/snapshots/   ← this should NOT be in .gitignore
```

---

## CI Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/screenshot-tests.yml
name: Screenshot Tests

on:
  pull_request:

jobs:
  screenshot-verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up JDK
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'

      - name: Run screenshot tests
        run: ./gradlew verifyRoborazziDebug

      - name: Upload diff artifacts on failure
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: screenshot-diffs
          path: '**/build/outputs/roborazzi/**'
          retention-days: 7
```

On a diff failure, Roborazzi writes three files to `build/outputs/roborazzi/`:
- `*_actual.png` — what the test rendered
- `*_expected.png` — the stored golden
- `*_diff.png` — pixel-level difference highlighted in red

Uploading these as CI artifacts means reviewers can download and inspect the visual diff directly from the PR.

---

## Testing Dark Mode

```kotlin
@RunWith(RobolectricTestRunner::class)
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class NoteCardDarkModeTest {

    @get:Rule
    val composeTestRule = createComposeRule()

    @Test
    @Config(qualifiers = "w411dp-h891dp-xxhdpi")  // light
    fun noteCard_lightTheme() {
        composeTestRule.setContent {
            AppTheme(darkTheme = false) { NoteCard(note = fakeNote(), onClick = {}) }
        }
        composeTestRule.onRoot().captureRoboImage("noteCard_light.png")
    }

    @Test
    @Config(qualifiers = "w411dp-h891dp-xxhdpi-night")  // dark
    fun noteCard_darkTheme() {
        composeTestRule.setContent {
            AppTheme(darkTheme = true) { NoteCard(note = fakeNote(), onClick = {}) }
        }
        composeTestRule.onRoot().captureRoboImage("noteCard_dark.png")
    }
}
```

Passing an explicit file name to `captureRoboImage()` gives goldens predictable, human-readable names.

---

## Testing Font Scale

```kotlin
@Test
@Config(qualifiers = "w411dp-h891dp-xxhdpi-notouch-port-notnight-finger-keysexposed-nokeys-navexposed-nonav-v33")
fun noteCard_largeFont() {
    // Programmatically override font scale
    composeTestRule.setContent {
        CompositionLocalProvider(LocalDensity provides Density(
            density = LocalDensity.current.density,
            fontScale = 1.8f
        )) {
            AppTheme {
                NoteCard(note = fakeNote(), onClick = {})
            }
        }
    }
    composeTestRule.onRoot().captureRoboImage("noteCard_largeFont.png")
}
```

Font-scale screenshots are especially useful for components with constrained height (chips, buttons, list tiles) where text can overflow or get clipped.

---

## Testing RTL Layouts

```kotlin
@Test
@Config(qualifiers = "w411dp-h891dp-xxhdpi-ldrtl")  // force RTL layout direction
fun noteCard_rtlLayout() {
    composeTestRule.setContent {
        CompositionLocalProvider(LocalLayoutDirection provides LayoutDirection.Rtl) {
            AppTheme {
                NoteCard(note = fakeNote(), onClick = {})
            }
        }
    }
    composeTestRule.onRoot().captureRoboImage("noteCard_rtl.png")
}
```

RTL screenshots catch `Alignment.Start/End` mistakes and hardcoded `paddingStart`/`paddingEnd` issues that only appear in RTL locales.

---

## Parameterized Multi-Variant Tests

Use JUnit4 `@RunWith(ParameterizedRobolectricTestRunner::class)` to cover multiple variants without duplicating test code:

```kotlin
@RunWith(ParameterizedRobolectricTestRunner::class)
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class NoteCardVariantsTest(private val config: ScreenshotConfig) {

    data class ScreenshotConfig(
        val name: String,
        val qualifier: String,
        val darkTheme: Boolean,
        val layoutDirection: LayoutDirection = LayoutDirection.Ltr
    )

    companion object {
        @JvmStatic
        @Parameters(name = "{0}")
        fun configs() = listOf(
            ScreenshotConfig("light_ltr", "w411dp-h891dp-xxhdpi", false),
            ScreenshotConfig("dark_ltr", "w411dp-h891dp-xxhdpi-night", true),
            ScreenshotConfig("light_rtl", "w411dp-h891dp-xxhdpi-ldrtl", false, LayoutDirection.Rtl),
            ScreenshotConfig("large_font", "w411dp-h891dp-xxhdpi", false),
        )
    }

    @get:Rule
    val composeTestRule = createComposeRule()

    @Test
    fun noteCard() {
        composeTestRule.setContent {
            CompositionLocalProvider(LocalLayoutDirection provides config.layoutDirection) {
                AppTheme(darkTheme = config.darkTheme) {
                    NoteCard(note = fakeNote(), onClick = {})
                }
            }
        }
        composeTestRule.onRoot().captureRoboImage("noteCard_${config.name}.png")
    }
}
```

---

## Compose Preview Screenshot Tests

If using the Compose Screenshot Testing alpha API (`@PreviewScreenshotTest`), screenshot tests can be generated directly from `@Preview` annotations:

```kotlin
// In your composable file:
@Preview(name = "Light", showBackground = true)
@Preview(name = "Dark", uiMode = Configuration.UI_MODE_NIGHT_YES, showBackground = true)
@Composable
fun NoteCardPreview() {
    AppTheme { NoteCard(note = fakeNote(), onClick = {}) }
}
```

```kotlin
// Dedicated screenshot test — generates goldens from all @Preview annotations:
@RunWith(ScreenshotTestRunner::class)  // from androidx.compose.ui:ui-test-screenshot
class NoteCardPreviewTest
```

> Note: `@PreviewScreenshotTest` is an alpha API as of 2025. Check the current stable API surface before adopting — the Roborazzi approach above is stable and production-ready today.

---

## Screenshot Test Checklist

Before merging a UI change, verify:

- [ ] Golden images are updated and committed
- [ ] Light and dark mode goldens both updated
- [ ] RTL golden updated if the component uses directional layout
- [ ] Large font scale golden updated if the component has constrained height
- [ ] CI screenshot job passes on the PR branch
- [ ] Diff artifacts reviewed if CI previously failed

---

## Pitfalls to Avoid

- **Do not put goldens in `.gitignore`.** Goldens must be versioned with the code.
- **Do not run `recordRoborazziDebug` in CI.** Record only locally; verify in CI.
- **Avoid testing animated states.** Pause animations or test initial/final states only — mid-animation frames are non-deterministic.
- **Wrap all content in your app theme.** Screenshots without the theme will use system defaults and produce false positives when the system theme changes.
- **Use `@GraphicsMode(NATIVE)`.** Without this, Robolectric uses a software renderer that produces lower-quality screenshots inconsistent with real devices.
