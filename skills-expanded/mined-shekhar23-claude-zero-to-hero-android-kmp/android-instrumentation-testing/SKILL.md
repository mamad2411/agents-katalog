---
name: android-instrumentation-testing
description: |
  Instrumentation and end-to-end testing for Android - Espresso, UI Automator, Compose test rules, Hilt test injection, navigation end-to-end, IdlingResource for async ops, and running tests on Firebase Test Lab. Use this skill whenever writing tests that run on a device or emulator, testing full user flows across multiple screens, replacing Hilt modules in tests, or setting up a device test matrix in CI. Trigger on phrases like "instrumentation test", "Espresso", "UI test", "UI Automator", "end-to-end test", "HiltAndroidTest", "createAndroidComposeRule", "integration test on device", "Firebase Test Lab", or "IdlingResource".
---

# Android Instrumentation Testing

## Overview

Instrumentation tests run on a real device or emulator inside the Android runtime. They are the only way to test:
- Actual navigation transitions and back-stack behavior
- System permissions dialogs (UI Automator)
- Full Hilt injection graph wiring
- Database + network integration without fakes
- Cross-app interactions (share sheets, notifications, deep links)

They are slower than unit tests. Reserve them for flows where the real runtime matters. For simple UI rendering tests, prefer Compose unit tests with `createComposeRule()` (runs on JVM — see android-testing).

---

## Dependency Setup

```toml
# gradle/libs.versions.toml
[versions]
espresso = "3.6.1"
uiautomator = "2.3.0"
hilt-testing = "2.51.1"

[libraries]
espresso-core = { module = "androidx.test.espresso:espresso-core", version.ref = "espresso" }
espresso-intents = { module = "androidx.test.espresso:espresso-intents", version.ref = "espresso" }
uiautomator = { module = "androidx.test.uiautomator:uiautomator", version.ref = "uiautomator" }
hilt-android-testing = { module = "com.google.dagger:hilt-android-testing", version.ref = "hilt-testing" }
androidx-test-runner = { module = "androidx.test:runner", version = "1.6.2" }
androidx-test-rules = { module = "androidx.test:rules", version = "1.6.1" }
```

```kotlin
// build.gradle.kts (module under test)
android {
    defaultConfig {
        testInstrumentationRunner = "com.example.app.HiltTestRunner"
    }
}

dependencies {
    androidTestImplementation(libs.espresso.core)
    androidTestImplementation(libs.espresso.intents)
    androidTestImplementation(libs.uiautomator)
    androidTestImplementation(libs.hilt.android.testing)
    kaptAndroidTest(libs.hilt.compiler)          // or kspAndroidTest for KSP
    androidTestImplementation(libs.androidx.test.runner)
    androidTestImplementation(libs.androidx.test.rules)
    androidTestImplementation(libs.androidx.compose.ui.test.junit4)
}
```

---

## Espresso Basics

Espresso operates on the main thread's UI — every interaction is synchronised automatically with the main looper.

```kotlin
// onView(matcher).perform(action).check(assertion)

// Find by ID and click
onView(withId(R.id.btn_submit)).perform(click())

// Find by text and check visibility
onView(withText("Save note")).check(matches(isDisplayed()))

// Type into a field
onView(withId(R.id.et_title))
    .perform(clearText(), typeText("My Note"), closeSoftKeyboard())

// Scroll to an item in a RecyclerView, then click it
onView(withId(R.id.rv_notes))
    .perform(RecyclerViewActions.scrollToPosition<RecyclerView.ViewHolder>(10))
onView(withText("Note 10")).perform(click())

// Check a View is NOT displayed
onView(withId(R.id.progress_bar)).check(matches(not(isDisplayed())))

// Check text content
onView(withId(R.id.tv_count)).check(matches(withText("3 notes")))
```

### Common ViewMatchers

| Matcher | Use |
|---|---|
| `withId(R.id.foo)` | Resource ID |
| `withText("Hello")` | Exact text |
| `withContentDescription("Back")` | Accessibility description |
| `isDisplayed()` | Fully visible on screen |
| `isEnabled()` | View is enabled |
| `hasFocus()` | View has input focus |
| `isChecked()` | CheckBox/Switch checked state |
| `withParent(withId(...))` | Child of a specific parent |

### Combining Matchers

```kotlin
// Both conditions must match:
onView(allOf(withId(R.id.tv_label), withText("Draft"))).check(matches(isDisplayed()))

// Parent-child relationship:
onView(allOf(withText("Delete"), withParent(withId(R.id.note_card_1)))).perform(click())
```

---

## UI Automator (Cross-App and System UI)

Use UI Automator when the interaction leaves your app's process: permission dialogs, notifications, the share sheet, other apps.

```kotlin
@RunWith(AndroidJUnit4::class)
class NotificationTest {

    private val device = UiDevice.getInstance(InstrumentationRegistry.getInstrumentation())

    @Test
    fun tappingNotification_opensNoteDetail() {
        // Trigger notification from the app
        onView(withId(R.id.btn_remind)).perform(click())

        // Open the notification shade
        device.openNotification()

        // Wait for and click the notification
        val notification = device.wait(
            Until.findObject(By.text("Meeting reminder")),
            5_000L
        )
        assertThat(notification).isNotNull()
        notification.click()

        // Assert app screen is shown
        onView(withId(R.id.note_detail_root)).check(matches(isDisplayed()))
    }
}
```

```kotlin
// Grant a permission dialog without user interaction:
fun grantPermissionIfShown(permissionText: String) {
    val device = UiDevice.getInstance(InstrumentationRegistry.getInstrumentation())
    val allowButton = device.wait(Until.findObject(By.text(permissionText)), 3_000L)
    allowButton?.click()
}
```

---

## Compose Test Rules

### `createComposeRule` — JVM-only (no Activity)

```kotlin
// Runs as a unit test on JVM, no emulator needed.
// Use for rendering and interaction tests that don't need an Activity context.
@get:Rule
val composeTestRule = createComposeRule()

@Test
fun noteCard_showsTitle() {
    composeTestRule.setContent {
        AppTheme { NoteCard(note = fakeNote(), onClick = {}) }
    }
    composeTestRule.onNodeWithText("Meeting Notes").assertIsDisplayed()
}
```

### `createAndroidComposeRule` — Instrumentation (requires Activity)

```kotlin
// Requires an Activity — runs as an instrumentation test.
// Use when you need the full Activity lifecycle, navigation host, or Hilt injection.
@RunWith(AndroidJUnit4::class)
class NoteListFlowTest {

    @get:Rule
    val composeTestRule = createAndroidComposeRule<MainActivity>()

    @Test
    fun noteList_clickNote_opensDetail() {
        composeTestRule.onNodeWithTag("note_item_1").performClick()
        composeTestRule.onNodeWithTag("note_detail_root").assertIsDisplayed()
    }
}
```

### Compose Finders and Assertions

```kotlin
composeTestRule.onNodeWithText("Submit").performClick()
composeTestRule.onNodeWithTag("loading_indicator").assertIsDisplayed()
composeTestRule.onNodeWithContentDescription("Close").assertIsDisplayed()
composeTestRule.onNodeWithText("Error").assertDoesNotExist()

// Wait for async state changes:
composeTestRule.waitUntil(timeoutMillis = 5_000) {
    composeTestRule.onAllNodesWithTag("note_item").fetchSemanticsNodes().isNotEmpty()
}
```

---

## Hilt Testing

### Custom Test Runner

Replace the default runner so Hilt can generate its test component:

```kotlin
// app/src/androidTest/.../HiltTestRunner.kt
class HiltTestRunner : AndroidJUnitRunner() {
    override fun newApplication(
        cl: ClassLoader?,
        className: String?,
        context: Context?
    ): Application {
        return super.newApplication(cl, HiltTestApplication::class.java.name, context)
    }
}
```

```kotlin
// build.gradle.kts
android {
    defaultConfig {
        testInstrumentationRunner = "com.example.app.HiltTestRunner"
    }
}
```

### Basic `@HiltAndroidTest`

```kotlin
@HiltAndroidTest
@RunWith(AndroidJUnit4::class)
class NoteRepositoryTest {

    @get:Rule
    val hiltRule = HiltAndroidRule(this)

    @Inject
    lateinit var repository: NoteRepository

    @Before
    fun setUp() {
        hiltRule.inject()
    }

    @Test
    fun insertAndRetrieve_returnsNote() = runBlocking {
        val note = Note(id = "1", title = "Test")
        repository.insert(note)
        val result = repository.getNotes()
        assertThat(result).contains(note)
    }
}
```

### Replacing Modules with `@UninstallModules` + `@BindValue`

```kotlin
@HiltAndroidTest
@UninstallModules(NetworkModule::class)   // remove the production module
@RunWith(AndroidJUnit4::class)
class NoteListFlowTest {

    @BindValue
    @JvmField
    val fakeNoteRepository: NoteRepository = FakeNoteRepository()

    @get:Rule(order = 0)
    val hiltRule = HiltAndroidRule(this)

    @get:Rule(order = 1)
    val composeTestRule = createAndroidComposeRule<MainActivity>()

    @Test
    fun emptyState_isShown_whenNoNotes() {
        composeTestRule.onNodeWithTag("empty_state").assertIsDisplayed()
    }
}
```

> Rule ordering matters: `HiltAndroidRule` (order = 0) must inject before `createAndroidComposeRule` (order = 1) launches the Activity.

### Replacing a ViewModel's Dependency

```kotlin
@HiltAndroidTest
@UninstallModules(AnalyticsModule::class)
@RunWith(AndroidJUnit4::class)
class CheckoutFlowTest {

    @BindValue
    @JvmField
    val analytics: AnalyticsTracker = NoOpAnalyticsTracker()

    // ...
}
```

---

## Test Ordering and Isolation

Each test **must** start from a clean state. Do not rely on state left by a previous test — test ordering in instrumentation suites is not guaranteed.

```kotlin
@HiltAndroidTest
@RunWith(AndroidJUnit4::class)
class NoteFlowTest {

    @get:Rule(order = 0)
    val hiltRule = HiltAndroidRule(this)

    @get:Rule(order = 1)
    val composeTestRule = createAndroidComposeRule<MainActivity>()

    @Inject
    lateinit var db: NoteDatabase

    @Before
    fun setUp() {
        hiltRule.inject()
        // Reset DB state before each test
        runBlocking { db.clearAllTables() }
    }

    @After
    fun tearDown() {
        runBlocking { db.clearAllTables() }
    }
}
```

---

## Testing Navigation End-to-End

```kotlin
@HiltAndroidTest
@RunWith(AndroidJUnit4::class)
class NavigationTest {

    @get:Rule(order = 0)
    val hiltRule = HiltAndroidRule(this)

    @get:Rule(order = 1)
    val composeTestRule = createAndroidComposeRule<MainActivity>()

    @BindValue @JvmField
    val fakeRepo: NoteRepository = FakeNoteRepository(
        initialNotes = listOf(Note(id = "42", title = "Deep Link Target"))
    )

    @Test
    fun clickingNote_navigatesToDetail_andBackReturnsToList() {
        // Assert start screen
        composeTestRule.onNodeWithTag("note_list_root").assertIsDisplayed()

        // Tap note
        composeTestRule.onNodeWithText("Deep Link Target").performClick()

        // Assert detail screen
        composeTestRule.onNodeWithTag("note_detail_root").assertIsDisplayed()
        composeTestRule.onNodeWithText("Deep Link Target").assertIsDisplayed()

        // Navigate back
        composeTestRule.activityRule.scenario.onActivity { activity ->
            activity.onBackPressedDispatcher.onBackPressed()
        }

        // Assert list screen restored
        composeTestRule.onNodeWithTag("note_list_root").assertIsDisplayed()
    }
}
```

---

## IdlingResource for Async Operations

Espresso auto-syncs with the main thread but knows nothing about coroutines or custom thread pools. Register an `IdlingResource` for any async work Espresso cannot detect.

```kotlin
// A simple CountingIdlingResource for coroutine-based loading:
object AppIdlingResource {
    val countingIdlingResource = CountingIdlingResource("NetworkCalls")

    fun increment() = countingIdlingResource.increment()
    fun decrement() {
        if (!countingIdlingResource.isIdleNow) countingIdlingResource.decrement()
    }
}

// Register in the test:
@Before
fun setUp() {
    IdlingRegistry.getInstance().register(AppIdlingResource.countingIdlingResource)
}

@After
fun tearDown() {
    IdlingRegistry.getInstance().unregister(AppIdlingResource.countingIdlingResource)
}
```

For Compose + coroutine-driven state, prefer `composeTestRule.waitUntil { }` over `IdlingResource` — it is simpler and requires no production code changes.

---

## Running on Firebase Test Lab

```yaml
# .github/workflows/firebase-test-lab.yml
name: Instrumentation Tests (Firebase Test Lab)

on:
  push:
    branches: [main]

jobs:
  instrumentation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build debug APKs
        run: ./gradlew assembleDebug assembleDebugAndroidTest

      - name: Authenticate to Google Cloud
        uses: google-github-actions/auth@v2
        with:
          credentials_json: ${{ secrets.GCP_SA_KEY }}

      - name: Run on Firebase Test Lab
        run: |
          gcloud firebase test android run \
            --type instrumentation \
            --app app/build/outputs/apk/debug/app-debug.apk \
            --test app/build/outputs/apk/androidTest/debug/app-debug-androidTest.apk \
            --device model=Pixel6,version=33,locale=en,orientation=portrait \
            --device model=Pixel6,version=33,locale=ar,orientation=portrait \
            --timeout 10m \
            --results-bucket gs://my-test-results \
            --results-dir "run_$(date +%Y%m%d_%H%M%S)"

      - name: Download test results
        if: always()
        run: |
          gsutil -m cp -r gs://my-test-results/** test-results/

      - name: Upload results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: firebase-test-results
          path: test-results/
```

**Emulator matrix guidance:**
- Always test on at least one low-end device (API 28-30) and one current flagship (API 33+).
- Include an Arabic (`ar`) or Hebrew (`iw`) locale to catch RTL regressions.
- Set `--timeout` based on your actual suite duration — FTL charges per device-minute.

---

## Checklist: Before Adding an Instrumentation Test

- [ ] Could this be covered by a ViewModel unit test + a Compose UI test? If yes, prefer those.
- [ ] Does the flow cross Activity/process boundaries, or exercise the real Hilt graph?
- [ ] Is the test isolated — does it reset all state in `@Before` / `@After`?
- [ ] Is the test deterministic — no dependency on network, clock, or previous test state?
- [ ] Is the test registered in the CI emulator matrix?
