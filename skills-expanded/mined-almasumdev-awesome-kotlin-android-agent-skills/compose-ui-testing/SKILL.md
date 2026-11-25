---
name: compose-ui-testing
description: Expert guidance on Jetpack Compose UI testing with createAndroidComposeRule, semantics matchers, synchronization, and screenshot tests with Paparazzi or Roborazzi. Use this for instrumented and screenshot UI tests.
---

# Compose UI Testing & Screenshot Tests

## Instructions

### 1. Dependencies

```kotlin
androidTestImplementation(platform(libs.androidx.compose.bom))
androidTestImplementation("androidx.compose.ui:ui-test-junit4")
androidTestImplementation("androidx.test.ext:junit:1.2.1")
androidTestImplementation("androidx.test.espresso:espresso-core:3.6.1")
debugImplementation("androidx.compose.ui:ui-test-manifest")

// Pick ONE screenshot framework per module:
// JVM-only (no emulator, very fast):
testImplementation("app.cash.paparazzi:paparazzi:1.3.5")
// Or Robolectric-based (runs Compose effects, closer to runtime):
testImplementation("io.github.takahirom.roborazzi:roborazzi:1.32.2")
testImplementation("io.github.takahirom.roborazzi:roborazzi-compose:1.32.2")
testImplementation("org.robolectric:robolectric:4.14")
```

### 2. Compose Rule Types

| Rule | Purpose |
|---|---|
| `createComposeRule()` | Pure composable under a host Activity. Fastest instrumented option. |
| `createAndroidComposeRule<MyActivity>()` | Launches a real Activity — needed for navigation, Hilt injection, `AndroidView`. |
| `createEmptyComposeRule()` | You launch your own scenario; use when sharing state across activities. |

```kotlin
@get:Rule val rule = createAndroidComposeRule<MainActivity>()

@Test fun showsArticleTitle() {
    rule.setContent { AppTheme { ArticleCard(fakeArticle) } }
    rule.onNodeWithText("Hello").assertIsDisplayed()
    rule.onNodeWithContentDescription("Bookmark").performClick()
}
```

### 3. Semantics Matchers

Favor matchers that survive UI refactors:

```kotlin
onNodeWithText("Save")
onNodeWithContentDescription("Back")
onNodeWithTag("articleList")                          // test tag, last resort
onNode(hasText("Save") and isEnabled())
onAllNodes(hasTestTag("articleRow")).assertCountEquals(3)
```

Set a tag when nothing semantic uniquely identifies the node:

```kotlin
LazyColumn(Modifier.testTag("articleList")) { /* ... */ }
```

Keep `testTag` rare; prefer labels, headings, roles from real accessibility content.

### 4. Synchronization

Compose test rules auto-sync to idle. Only override when you introduce external async:

```kotlin
rule.mainClock.autoAdvance = false
rule.onNodeWithText("Start").performClick()
rule.mainClock.advanceTimeBy(500)   // control animations precisely
```

For background work, pair with `IdlingResource`s or inject a `TestDispatcher` so the test controls time via `runTest`.

### 5. Gesture and Input

```kotlin
rule.onNodeWithTag("articleList").performScrollToIndex(20)
rule.onNodeWithText("Search").performTextInput("kotlin")
rule.onNode(isFocusable()).performImeAction()
rule.onNodeWithTag("slider").performTouchInput { swipeRight() }
```

### 6. Navigation Tests

```kotlin
@get:Rule val rule = createAndroidComposeRule<MainActivity>()

@Test fun opensDetailOnTap() {
    rule.onNodeWithText("Kotlin on Android").performClick()
    rule.onNodeWithTag("articleDetail").assertIsDisplayed()
    Espresso.pressBack()
    rule.onNodeWithText("Kotlin on Android").assertIsDisplayed()
}
```

### 7. Hilt in Instrumented Tests

```kotlin
@HiltAndroidTest
class ArticlesFlowTest {
    @get:Rule(order = 0) val hilt = HiltAndroidRule(this)
    @get:Rule(order = 1) val compose = createAndroidComposeRule<HiltTestActivity>()

    @BindValue @JvmField val fakeRepo: ArticleRepository = FakeArticleRepository()

    @Test fun rendersFakeData() {
        hilt.inject()
        compose.setContent { AppTheme { ArticlesRoute(onOpen = {}) } }
        compose.onNodeWithText(FakeArticleRepository.FIRST_TITLE).assertIsDisplayed()
    }
}
```

Use `@BindValue` to swap production bindings for fakes per test.

### 8. Screenshot Tests — Paparazzi (JVM)

```kotlin
class ArticleCardPaparazzi {
    @get:Rule val paparazzi = Paparazzi(
        deviceConfig = DeviceConfig.PIXEL_5,
        theme = "Theme.Material3.DayNight",
        renderingMode = SessionParams.RenderingMode.SHRINK,
    )

    @Test fun light() = paparazzi.snapshot {
        AppTheme(darkTheme = false) { ArticleCard(sampleArticle) }
    }

    @Test fun dark() = paparazzi.snapshot {
        AppTheme(darkTheme = true) { ArticleCard(sampleArticle) }
    }
}
```

- JVM-only. No emulator. Seconds per test.
- Cannot execute `LaunchedEffect` / coroutines; capture **pure visual** composables and freeze state inputs.
- Record goldens: `./gradlew recordPaparazzi`. Verify: `./gradlew verifyPaparazzi` (runs in CI).

### 9. Screenshot Tests — Roborazzi (Robolectric)

```kotlin
@RunWith(RobolectricTestRunner::class)
@Config(qualifiers = "w360dp-h800dp-port-xhdpi")
class ArticleCardRoborazzi {
    @get:Rule val rule = createComposeRule()

    @Test fun card() {
        rule.setContent { AppTheme { ArticleCard(sampleArticle) } }
        rule.onRoot().captureRoboImage("article_card_light.png")
    }
}
```

Roborazzi runs the Compose runtime so `remember`, `LaunchedEffect`, and lifecycle-aware state all work. Slightly slower than Paparazzi.

Pick one framework per module and stay consistent so goldens don't drift between renderers.

### 10. CI Integration

- Golden images live under `src/test/snapshots/` (Paparazzi) or `src/test/resources/roborazzi/` and are checked into Git.
- A CI job runs `verifyPaparazzi` / `verifyRoborazziDebug`. Diff images upload as artifacts for reviewers.
- Record-mode runs are gated behind a manual workflow dispatch to avoid accidental golden churn.

## Checklist
- [ ] Every screen has an instrumented test that reaches every navigation edge.
- [ ] Tests prefer semantic matchers; `testTag` is used sparingly.
- [ ] Hilt tests swap repositories via `@BindValue` fakes.
- [ ] Animation tests use `mainClock.autoAdvance = false` to control time.
- [ ] One screenshot framework is chosen per module (Paparazzi *or* Roborazzi).
- [ ] Golden images are committed and verified in CI on every PR.
- [ ] Flaky tests are fixed at the source (missing idling), not `Thread.sleep`.
