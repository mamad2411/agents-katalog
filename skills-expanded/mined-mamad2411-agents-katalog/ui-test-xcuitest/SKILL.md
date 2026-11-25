---
name: ui-test-xcuitest
description: "Patterns for XCUITest UI tests for native Apple apps (macOS/iOS). Use when writing or reviewing XCUITest tests for Swift apps. Triggers on: XCUITest, xcuitest, native app testing, Apple UI tests, SwiftUI tests, AppKit tests, UIKit tests."
---

# UI Test XCUITest Skill

This skill provides patterns and instructions for writing XCUITest UI tests for native Apple applications on macOS and iOS. XCUITest is Apple's official UI testing framework — free, bundled with Xcode, and the gold standard for native app testing.

## Triggers

Load this skill when:
- `apps[*].testing.framework === 'xcuitest'`
- `apps[*].platforms` includes `macos` or `ios`
- `stack.languages` includes `swift`
- The project has `.xcodeproj` or `.xcworkspace` files
- The task involves writing or reviewing UI tests for a native Apple app

## How XCUITest Works

XCUITest operates through Apple's **accessibility system** — the same system used by VoiceOver. Tests run in a **separate process** from the app under test, communicating via XPC (inter-process communication).

```
┌─────────────────────────────────────────────────┐
│  Test Runner Process (XCTest)                    │
│  • Queries UI elements via accessibility tree    │
│  • Simulates taps, swipes, keyboard input        │
│  • Asserts on element state/existence            │
└──────────────────┬──────────────────────────────┘
                   │ XPC (inter-process communication)
┌──────────────────▼──────────────────────────────┐
│  App Under Test (separate process)               │
│  • Runs normally, no test code injected          │
│  • Accessibility elements exposed automatically  │
│  • State is black-box to the test runner         │
└─────────────────────────────────────────────────┘
```

**Key implications:**
- Tests cannot access app internals (variables, functions, databases)
- All interaction goes through the UI — what the user sees, the test sees
- Tests are inherently integration-level — they test real UI behavior
- Accessibility identifiers are the primary way to find elements

## Phase 0: Read Project Configuration (MANDATORY)

> **CRITICAL: Before writing ANY XCUITest, read `project.json` to determine platforms, UI framework, and CI configuration.**

### Step 1: Determine Target Platforms

```
Read project.json → apps[*].platforms
Possible values: ["macos"], ["ios"], ["macos", "ios"]
```

| Platforms | Test Target | Destination Flag |
|-----------|-------------|-----------------|
| `["macos"]` | macOS only | `platform=macOS` |
| `["ios"]` | iOS only | `platform=iOS Simulator,name=iPhone 16` |
| `["macos", "ios"]` | Both — write shared tests + platform-specific tests | Both destinations |

### Step 2: Determine UI Framework

```
Read project.json → apps[*].framework
Possible values: "swiftui", "appkit", "uikit", "swiftui-appkit", "swiftui-uikit", or check CONVENTIONS.md
```

The UI framework determines element query patterns:

| Framework | Element Queries | Notes |
|-----------|----------------|-------|
| **SwiftUI** | `.accessibilityIdentifier("id")` on views | Must be explicitly added by developer |
| **AppKit** | `.identifier = NSUserInterfaceItemIdentifier("id")` | Set on NSView/NSControl |
| **UIKit** | `.accessibilityIdentifier = "id"` | Set on UIView subclasses |
| **Mixed** | Both patterns — check which framework owns each screen | Common in migration projects |

### Step 3: Determine CI System

```
Read project.json → commands.testUI or commands.testE2E
Read project.json → Look for CI configuration hints
Check .github/workflows/ for GitHub Actions
Check for Xcode Cloud (ci_scripts/ directory)
```

| CI System | Config Location | Test Command |
|-----------|----------------|--------------|
| **GitHub Actions** | `.github/workflows/*.yml` | `xcodebuild test` in workflow |
| **Xcode Cloud** | `ci_scripts/ci_post_clone.sh` etc. | Xcode Cloud runs schemes automatically |
| **Both** | Separate configs for each | Ensure both use same scheme/destination |

### Step 4: Determine Xcode Project Structure

```
Look for: *.xcodeproj, *.xcworkspace, Package.swift
Read project.json → commands.test, commands.build for scheme names
```

### Step 5: Read Project Testing Conventions

Check `project.json` → `context.testing` for a path to project-specific testing conventions. This file supplements framework knowledge with project-local details:

- ID prefix conventions for pbxproj entries
- Base test class name and its provided helpers
- App-specific navigation structure
- Kill/restart patterns
- Environment-specific setup

If the field doesn't exist, check the Testing section of `context.conventions` (CONVENTIONS.md) for any project-specific rules.

## Test File Structure

### Where Tests Live

XCUITest files live in a **UI Testing bundle target** within the Xcode project:

```
MyApp/
├── MyApp/                    # App source
│   ├── Views/
│   ├── Models/
│   └── Services/
├── MyAppTests/               # Unit tests (XCTest)
│   └── MyAppTests.swift
├── MyAppUITests/             # UI tests (XCUITest) ← HERE
│   ├── MyAppUITests.swift    # Test file
│   ├── Pages/                # Page objects (recommended)
│   │   ├── LoginPage.swift
│   │   └── DashboardPage.swift
│   ├── Helpers/
│   │   └── TestHelpers.swift
│   └── Resources/
│       └── TestData.json
└── MyApp.xcodeproj
```

### Basic Test Structure

```swift
import XCTest

final class LoginUITests: XCTestCase {
    
    let app = XCUIApplication()
    
    override func setUpWithError() throws {
        // Stop immediately when a failure occurs
        continueAfterFailure = false
        
        // Launch the app fresh for each test
        app.launch()
    }
    
    override func tearDownWithError() throws {
        // Take screenshot on failure (automatic in Xcode, explicit for CI)
        if testRun?.failureCount ?? 0 > 0 {
            let screenshot = app.screenshot()
            let attachment = XCTAttachment(screenshot: screenshot)
            attachment.name = "Failure-\(name)"
            attachment.lifetime = .keepAlways
            add(attachment)
        }
    }
    
    func testSuccessfulLogin() throws {
        // Arrange: Navigate to login
        let emailField = app.textFields["email-field"]
        XCTAssertTrue(emailField.waitForExistence(timeout: 5))
        
        // Act: Enter credentials and submit
        emailField.tap()
        emailField.typeText("user@example.com")
        
        let passwordField = app.secureTextFields["password-field"]
        passwordField.tap()
        passwordField.typeText("password123")
        
        app.buttons["login-button"].tap()
        
        // Assert: Dashboard appears
        let welcomeText = app.staticTexts["welcome-message"]
        XCTAssertTrue(welcomeText.waitForExistence(timeout: 10))
    }
}
```

## Element Query Patterns

### Finding Elements

XCUITest queries the accessibility tree. Elements are found by **type** and **identifier/label**.

```swift
// By accessibility identifier (PREFERRED — stable, not user-visible)
app.buttons["save-button"]
app.textFields["email-field"]
app.staticTexts["welcome-message"]

// By label (matches accessibilityLabel — user-visible text, fragile to changes)
app.buttons["Save"]
app.staticTexts["Welcome back"]

// By predicate (complex queries)
app.buttons.matching(NSPredicate(format: "identifier BEGINSWITH 'item-'"))
app.staticTexts.matching(NSPredicate(format: "label CONTAINS 'error'"))

// By index (AVOID — fragile, breaks when UI order changes)
app.buttons.element(boundBy: 0)  // First button — don't do this
```

### Element Types

| XCUIElement Type | SwiftUI | AppKit | UIKit |
|------------------|---------|--------|-------|
| `buttons` | `Button` | `NSButton` | `UIButton` |
| `textFields` | `TextField` | `NSTextField` | `UITextField` |
| `secureTextFields` | `SecureField` | `NSSecureTextField` | `UITextField` (isSecureTextEntry) |
| `staticTexts` | `Text` | `NSTextField` (non-editable) | `UILabel` |
| `images` | `Image` | `NSImageView` | `UIImageView` |
| `switches` | `Toggle` | `NSSwitch` | `UISwitch` |
| `sliders` | `Slider` | `NSSlider` | `UISlider` |
| `textViews` | `TextEditor` | `NSTextView` | `UITextView` |
| `tables` | `List` | `NSTableView` | `UITableView` |
| `collectionViews` | `LazyVGrid`/`LazyHGrid` | `NSCollectionView` | `UICollectionView` |
| `navigationBars` | `NavigationStack` title | n/a | `UINavigationBar` |
| `tabBars` | `TabView` | n/a | `UITabBar` |
| `toolbars` | `.toolbar { }` | `NSToolbar` | `UIToolbar` |
| `sheets` | `.sheet()` | `NSPanel` (sheet) | presented VC |
| `alerts` | `.alert()` | `NSAlert` | `UIAlertController` |
| `popovers` | `.popover()` | `NSPopover` | `UIPopoverController` |
| `menus` | `Menu` | `NSMenu` | `UIMenu` |
| `menuItems` | Menu items | `NSMenuItem` | `UIAction` |
| `windows` | `Window` / `WindowGroup` | `NSWindow` | `UIWindow` |

### Setting Accessibility Identifiers

#### SwiftUI
```swift
Button("Save") { save() }
    .accessibilityIdentifier("save-button")

TextField("Email", text: $email)
    .accessibilityIdentifier("email-field")

List(items) { item in
    ItemRow(item: item)
        .accessibilityIdentifier("item-row-\(item.id)")
}
.accessibilityIdentifier("items-list")
```

#### AppKit
```swift
let button = NSButton(title: "Save", target: self, action: #selector(save))
button.identifier = NSUserInterfaceItemIdentifier("save-button")

let textField = NSTextField()
textField.identifier = NSUserInterfaceItemIdentifier("email-field")
```

#### UIKit
```swift
let button = UIButton(type: .system)
button.accessibilityIdentifier = "save-button"

let textField = UITextField()
textField.accessibilityIdentifier = "email-field"
```

### Identifier Naming Convention

Use kebab-case with a descriptive pattern:

```
[screen]-[element-type]-[purpose]

Examples:
  login-field-email
  login-field-password
  login-button-submit
  dashboard-label-welcome
  settings-toggle-notifications
  item-row-{id}              // Dynamic identifiers for list items
```

## Interaction Patterns

### Tapping and Clicking

```swift
// Tap / click
app.buttons["save-button"].tap()

// Double tap
app.images["photo-thumbnail"].doubleTap()

// Long press
app.cells["item-row-1"].press(forDuration: 1.0)

// Right click (macOS)
app.cells["item-row-1"].rightClick()

// Force tap (3D Touch, iOS only)
app.buttons["action-button"].press(forDuration: 0.5)
```

### Text Input

```swift
// Type into a text field
let field = app.textFields["email-field"]
field.tap()
field.typeText("user@example.com")

// Clear and retype
field.tap()
field.tap()  // Double-tap to select all (or use below)
if let value = field.value as? String, !value.isEmpty {
    let deleteString = String(repeating: XCUIKeyboardKey.delete.rawValue, count: value.count)
    field.typeText(deleteString)
}
field.typeText("new@example.com")

// Secure text fields
let passwordField = app.secureTextFields["password-field"]
passwordField.tap()
passwordField.typeText("secret123")
```

### Keyboard Shortcuts (macOS)

```swift
// Command+S
app.typeKey("s", modifierFlags: .command)

// Command+Shift+N
app.typeKey("n", modifierFlags: [.command, .shift])

// Enter / Return
app.typeKey(.return, modifierFlags: [])

// Escape
app.typeKey(.escape, modifierFlags: [])

// Tab
field.typeText("\t")
```

### Scrolling and Swiping

```swift
// Swipe (iOS)
app.tables["items-list"].swipeUp()
app.tables["items-list"].swipeDown()

// Scroll to element (works on both platforms)
let targetElement = app.staticTexts["item-at-bottom"]
while !targetElement.isHittable {
    app.swipeUp()
}

// Scroll in a specific view
app.scrollViews["content-scroll"].swipeUp()
```

### Drag and Drop (macOS)

```swift
let sourceElement = app.cells["item-row-1"]
let targetElement = app.cells["item-row-5"]
sourceElement.press(forDuration: 0.5, thenDragTo: targetElement)
```

### Menu Bar (macOS)

```swift
// Access menu bar items
app.menuBarItems["File"].click()
app.menuItems["New Document"].click()

// Or chain
app.menuBarItems["File"].menuItems["New Document"].click()

// Contextual menus
app.cells["item-row-1"].rightClick()
app.menuItems["Delete"].click()
```

## Assertions

### Existence and Visibility

```swift
// Element exists in the accessibility tree
XCTAssertTrue(app.buttons["save-button"].exists)
XCTAssertFalse(app.alerts["error-alert"].exists)

// Wait for existence (with timeout — PREFERRED for async UI)
let element = app.staticTexts["loading-complete"]
XCTAssertTrue(element.waitForExistence(timeout: 10))

// Element is hittable (visible AND not obscured)
XCTAssertTrue(app.buttons["save-button"].isHittable)
```

### State Assertions

```swift
// Enabled / disabled
XCTAssertTrue(app.buttons["submit-button"].isEnabled)
XCTAssertFalse(app.buttons["submit-button"].isEnabled)

// Selected
XCTAssertTrue(app.cells["item-row-1"].isSelected)

// Value (text fields, sliders, toggles)
XCTAssertEqual(app.textFields["email-field"].value as? String, "user@example.com")
XCTAssertEqual(app.switches["notifications-toggle"].value as? String, "1") // "1" = on, "0" = off
XCTAssertEqual(app.sliders["volume-slider"].value as? String, "0.5")

// Label text (AppKit/UIKit — see Gotcha #6 for SwiftUI .value vs .label)
XCTAssertEqual(app.staticTexts["welcome-message"].label, "Welcome back, John")
```

### Collection Assertions

```swift
// Count of elements
XCTAssertEqual(app.cells.matching(identifier: "item-row").count, 5)
XCTAssertGreaterThan(app.tables["items-list"].cells.count, 0)

// Element contains text
XCTAssertTrue(app.staticTexts.matching(NSPredicate(format: "label CONTAINS 'Success'")).count > 0)
```

### Waiting for Conditions (Async UI)

```swift
// Wait for existence (most common)
let element = app.staticTexts["result-label"]
XCTAssertTrue(element.waitForExistence(timeout: 10))

// Wait for a condition using expectation
let predicate = NSPredicate(format: "isEnabled == true")
let expectation = XCTNSPredicateExpectation(predicate: predicate, object: app.buttons["submit-button"])
let result = XCTWaiter.wait(for: [expectation], timeout: 5)
XCTAssertEqual(result, .completed)

// Wait for element to disappear
let spinner = app.activityIndicators["loading-spinner"]
let disappearPredicate = NSPredicate(format: "exists == false")
let disappearExpectation = XCTNSPredicateExpectation(predicate: disappearPredicate, object: spinner)
XCTWaiter.wait(for: [disappearExpectation], timeout: 10)
```

## Page Object Pattern (Recommended)

Use page objects to encapsulate screen interactions and make tests readable.

### Page Object

```swift
// MyAppUITests/Pages/LoginPage.swift

import XCTest

struct LoginPage {
    let app: XCUIApplication
    
    // MARK: - Elements
    
    var emailField: XCUIElement {
        app.textFields["login-field-email"]
    }
    
    var passwordField: XCUIElement {
        app.secureTextFields["login-field-password"]
    }
    
    var loginButton: XCUIElement {
        app.buttons["login-button-submit"]
    }
    
    var errorMessage: XCUIElement {
        app.staticTexts["login-label-error"]
    }
    
    // MARK: - Actions
    
    @discardableResult
    func login(email: String, password: String) -> DashboardPage {
        emailField.tap()
        emailField.typeText(email)
        passwordField.tap()
        passwordField.typeText(password)
        loginButton.tap()
        return DashboardPage(app: app)
    }
    
    // MARK: - Assertions
    
    func assertErrorShown(message: String) {
        XCTAssertTrue(errorMessage.waitForExistence(timeout: 5))
        XCTAssertEqual(errorMessage.label, message)
    }
    
    func assertIsDisplayed() {
        XCTAssertTrue(emailField.waitForExistence(timeout: 5))
    }
}
```

### Test Using Page Objects

```swift
final class LoginUITests: XCTestCase {
    let app = XCUIApplication()
    lazy var loginPage = LoginPage(app: app)
    
    override func setUpWithError() throws {
        continueAfterFailure = false
        app.launch()
    }
    
    func testSuccessfulLogin() throws {
        loginPage.assertIsDisplayed()
        let dashboard = loginPage.login(email: "user@example.com", password: "password123")
        dashboard.assertIsDisplayed()
    }
    
    func testInvalidPassword() throws {
        loginPage.assertIsDisplayed()
        _ = loginPage.login(email: "user@example.com", password: "wrong")
        loginPage.assertErrorShown(message: "Invalid credentials")
    }
}
```

## Platform-Specific Patterns

### macOS-Specific

```swift
// Window management
func testWindowResize() throws {
    let window = app.windows.firstMatch
    XCTAssertTrue(window.exists)
    
    // Check window title
    XCTAssertEqual(window.title, "My App")
}

// Toolbar buttons
func testToolbarAction() throws {
    app.toolbars.buttons["add-button"].click()
    XCTAssertTrue(app.sheets.firstMatch.waitForExistence(timeout: 5))
}

// Sidebar / NavigationSplitView
func testSidebarNavigation() throws {
    let sidebar = app.outlines["sidebar"]  // or app.tables["sidebar"]
    sidebar.cells["settings-item"].click()
    
    let detailView = app.staticTexts["settings-title"]
    XCTAssertTrue(detailView.waitForExistence(timeout: 5))
}

// Sheets (modal)
func testSheetDismissal() throws {
    app.buttons["show-sheet"].click()
    
    let sheet = app.sheets.firstMatch
    XCTAssertTrue(sheet.waitForExistence(timeout: 5))
    
    sheet.buttons["cancel-button"].click()
    XCTAssertFalse(sheet.waitForExistence(timeout: 2))
}

// Popovers
func testPopoverContent() throws {
    app.buttons["info-button"].click()
    
    let popover = app.popovers.firstMatch
    XCTAssertTrue(popover.waitForExistence(timeout: 5))
    XCTAssertTrue(popover.staticTexts["info-text"].exists)
}

// Menu bar
func testMenuBarAction() throws {
    app.menuBarItems["Edit"].click()
    app.menuItems["Preferences..."].click()
    XCTAssertTrue(app.windows["preferences-window"].waitForExistence(timeout: 5))
}
```

### iOS-Specific

```swift
// Tab bar navigation
func testTabBarNavigation() throws {
    app.tabBars.buttons["Settings"].tap()
    XCTAssertTrue(app.navigationBars["Settings"].waitForExistence(timeout: 5))
}

// Navigation back button
func testNavigationBack() throws {
    app.cells["item-row-1"].tap()
    XCTAssertTrue(app.navigationBars["Item Detail"].exists)
    
    app.navigationBars.buttons.element(boundBy: 0).tap()  // Back button
    XCTAssertTrue(app.navigationBars["Items"].exists)
}

// Pull to refresh
func testPullToRefresh() throws {
    let firstCell = app.cells.firstMatch
    let start = firstCell.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.5))
    let end = firstCell.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 5.0))
    start.press(forDuration: 0, thenDragTo: end)
    
    // Wait for refresh indicator to disappear
    let spinner = app.activityIndicators["refresh-spinner"]
    let predicate = NSPredicate(format: "exists == false")
    let expectation = XCTNSPredicateExpectation(predicate: predicate, object: spinner)
    XCTWaiter.wait(for: [expectation], timeout: 10)
}

// Alerts
func testAlertHandling() throws {
    app.buttons["delete-button"].tap()
    
    let alert = app.alerts["Confirm Delete"]
    XCTAssertTrue(alert.waitForExistence(timeout: 5))
    alert.buttons["Delete"].tap()
    XCTAssertFalse(alert.exists)
}

// Swipe to delete
func testSwipeToDelete() throws {
    let cell = app.cells["item-row-1"]
    cell.swipeLeft()
    app.buttons["Delete"].tap()
    XCTAssertFalse(cell.exists)
}

// Keyboard dismiss
func testKeyboardDismiss() throws {
    let field = app.textFields["search-field"]
    field.tap()
    field.typeText("query")
    
    // Dismiss keyboard
    app.keyboards.buttons["return"].tap()  // Or "Search", "Done", etc.
    // Or swipe down on iOS 16+
}
```

### Multiplatform Tests (Shared)

For apps targeting both macOS and iOS, write shared tests that work on both:

```swift
final class SharedUITests: XCTestCase {
    let app = XCUIApplication()
    
    override func setUpWithError() throws {
        continueAfterFailure = false
        app.launch()
    }
    
    // This test works on both platforms — uses accessibility identifiers only
    func testCreateNewItem() throws {
        // Platform-adaptive element finding
        let addButton = app.buttons["add-item-button"]
        XCTAssertTrue(addButton.waitForExistence(timeout: 5))
        addButton.tap()
        
        let nameField = app.textFields["item-name-field"]
        XCTAssertTrue(nameField.waitForExistence(timeout: 5))
        nameField.tap()
        nameField.typeText("New Item")
        
        app.buttons["save-button"].tap()
        
        let itemCell = app.cells["item-row-New Item"]
        XCTAssertTrue(itemCell.waitForExistence(timeout: 5))
    }
    
    // Platform-specific behavior in shared test
    func testNavigation() throws {
        #if os(macOS)
        // macOS: Click sidebar item
        app.outlines["sidebar"].cells["settings-item"].click()
        #else
        // iOS: Tap tab bar item
        app.tabBars.buttons["Settings"].tap()
        #endif
        
        // Shared assertion
        XCTAssertTrue(app.staticTexts["settings-title"].waitForExistence(timeout: 5))
    }
}
```

## Launch Arguments and Environment

### Passing Test Configuration

```swift
override func setUpWithError() throws {
    continueAfterFailure = false
    
    let app = XCUIApplication()
    
    // Launch arguments (checked with CommandLine.arguments or ProcessInfo in app)
    app.launchArguments = [
        "-UITesting",           // Flag for test mode
        "-resetOnLaunch",       // Custom flag to reset state
        "-disableAnimations"    // Speed up tests
    ]
    
    // Environment variables (checked with ProcessInfo.processInfo.environment in app)
    app.launchEnvironment = [
        "UI_TESTING": "1",
        "API_BASE_URL": "http://localhost:8080/mock",
        "DISABLE_ANALYTICS": "1"
    ]
    
    app.launch()
}
```

### App-Side Handling

```swift
// In the app code (e.g., AppDelegate or @main App)
struct MyApp: App {
    init() {
        if CommandLine.arguments.contains("-UITesting") {
            // Configure for testing
            UserDefaults.standard.set(true, forKey: "isUITesting")
        }
        if CommandLine.arguments.contains("-disableAnimations") {
            UIView.setAnimationsEnabled(false)  // iOS
            // or NSAnimationContext.current.duration = 0  // macOS
        }
        if CommandLine.arguments.contains("-resetOnLaunch") {
            // Clear user defaults, keychain, local data
            resetAppState()
        }
    }
}
```

## Screenshots

### Capture on Failure (Automatic)

Xcode automatically captures screenshots on test failure. For CI, explicitly attach them:

```swift
override func tearDownWithError() throws {
    if testRun?.failureCount ?? 0 > 0 {
        let screenshot = app.screenshot()
        let attachment = XCTAttachment(screenshot: screenshot)
        attachment.name = "Failure-\(name)"
        attachment.lifetime = .keepAlways
        add(attachment)
    }
}
```

### Capture on Demand

```swift
func testVisualState() throws {
    // Navigate to a specific state
    app.buttons["show-results"].tap()
    
    // Capture screenshot for reference
    let screenshot = app.screenshot()
    let attachment = XCTAttachment(screenshot: screenshot)
    attachment.name = "ResultsScreen"
    attachment.lifetime = .keepAlways
    add(attachment)
}
```

## CI Integration

### GitHub Actions

```yaml
name: UI Tests

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  ui-tests-macos:
    runs-on: macos-14  # Sonoma — use latest available
    steps:
      - uses: actions/checkout@v4
      
      - name: Select Xcode
        run: sudo xcode-select -s /Applications/Xcode_16.0.app/Contents/Developer
      
      - name: Build and Test (macOS)
        run: |
          xcodebuild test \
            -project MyApp.xcodeproj \
            -scheme MyApp \
            -destination 'platform=macOS' \
            -resultBundlePath TestResults-macOS.xcresult \
            -enableCodeCoverage YES \
            | xcpretty --color
      
      - name: Upload Test Results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-results-macos
          path: TestResults-macOS.xcresult

  ui-tests-ios:
    runs-on: macos-14
    steps:
      - uses: actions/checkout@v4
      
      - name: Select Xcode
        run: sudo xcode-select -s /Applications/Xcode_16.0.app/Contents/Developer
      
      - name: Start Simulator
        run: |
          # Boot a specific simulator
          xcrun simctl boot "iPhone 16" || true
          # Wait for it to be ready
          xcrun simctl bootstatus "iPhone 16" -b
      
      - name: Build and Test (iOS)
        run: |
          xcodebuild test \
            -project MyApp.xcodeproj \
            -scheme MyApp \
            -destination 'platform=iOS Simulator,name=iPhone 16,OS=18.0' \
            -resultBundlePath TestResults-iOS.xcresult \
            -enableCodeCoverage YES \
            | xcpretty --color
      
      - name: Upload Test Results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-results-ios
          path: TestResults-iOS.xcresult

  # Combined job for multiplatform apps
  ui-tests-multiplatform:
    runs-on: macos-14
    strategy:
      matrix:
        destination:
          - 'platform=macOS'
          - 'platform=iOS Simulator,name=iPhone 16,OS=18.0'
    steps:
      - uses: actions/checkout@v4
      
      - name: Select Xcode
        run: sudo xcode-select -s /Applications/Xcode_16.0.app/Contents/Developer
      
      - name: Build and Test
        run: |
          xcodebuild test \
            -project MyApp.xcodeproj \
            -scheme MyApp \
            -destination '${{ matrix.destination }}' \
            -resultBundlePath "TestResults-${{ strategy.job-index }}.xcresult" \
            | xcpretty --color
```

**For Swift Package Manager projects:**
```yaml
      - name: Build and Test (SPM)
        run: |
          swift test --enable-code-coverage
```

### Xcode Cloud

Xcode Cloud uses `ci_scripts/` in your project root:

```bash
#!/bin/bash
# ci_scripts/ci_pre_xcodebuild.sh
# Runs before xcodebuild (setup)

echo "Setting up test environment..."

# Install any dependencies
# brew install ... 

# Set environment for testing
export UI_TESTING=1
```

```bash
#!/bin/bash
# ci_scripts/ci_post_xcodebuild.sh
# Runs after xcodebuild (results processing)

echo "Processing test results..."

# Test results are automatically captured by Xcode Cloud
# Access via Xcode Cloud dashboard or App Store Connect
```

**Xcode Cloud configuration (in Xcode):**
1. Product → Xcode Cloud → Create Workflow
2. Add "Test" action with your scheme
3. Select destination(s): macOS, iOS Simulator, or both
4. Set trigger: PR, branch push, or scheduled

**Key differences from GitHub Actions:**

| Aspect | GitHub Actions | Xcode Cloud |
|--------|---------------|-------------|
| Config location | `.github/workflows/*.yml` | Xcode Cloud UI + `ci_scripts/` |
| macOS version | `runs-on: macos-14` | Managed by Apple |
| Xcode version | `xcode-select` | Xcode Cloud UI |
| Simulators | Pre-installed on runner | Managed by Apple |
| Test results | `.xcresult` artifacts | Xcode Cloud dashboard |
| Secrets | GitHub Secrets | App Store Connect |
| Cost | Free tier + paid minutes | 25 hrs/month free |

## Common Test Patterns

### Testing a Form

```swift
func testFormSubmission() throws {
    let nameField = app.textFields["form-field-name"]
    let emailField = app.textFields["form-field-email"]
    let submitButton = app.buttons["form-button-submit"]
    
    // Fill form
    nameField.tap()
    nameField.typeText("John Doe")
    
    emailField.tap()
    emailField.typeText("john@example.com")
    
    // Submit
    submitButton.tap()
    
    // Assert success
    let successMessage = app.staticTexts["form-label-success"]
    XCTAssertTrue(successMessage.waitForExistence(timeout: 10))
}
```

### Testing a List with Dynamic Content

```swift
func testListOperations() throws {
    // Wait for list to load
    let list = app.tables["items-list"]
    XCTAssertTrue(list.waitForExistence(timeout: 10))
    
    let initialCount = list.cells.count
    
    // Add an item
    app.buttons["add-item-button"].tap()
    let nameField = app.textFields["item-name-field"]
    nameField.tap()
    nameField.typeText("New Item")
    app.buttons["save-button"].tap()
    
    // Assert item was added
    XCTAssertEqual(list.cells.count, initialCount + 1)
    XCTAssertTrue(list.cells.staticTexts["New Item"].exists)
}
```

### Testing Navigation Flow

```swift
func testNavigationFlow() throws {
    // Start at home
    XCTAssertTrue(app.staticTexts["home-title"].exists)
    
    // Navigate to detail
    app.cells["item-row-1"].tap()
    XCTAssertTrue(app.staticTexts["detail-title"].waitForExistence(timeout: 5))
    
    // Navigate back
    #if os(iOS)
    app.navigationBars.buttons.firstMatch.tap()
    #else
    app.buttons["back-button"].click()
    #endif
    
    XCTAssertTrue(app.staticTexts["home-title"].waitForExistence(timeout: 5))
}
```

### Testing Error States

```swift
func testNetworkError() throws {
    // Launch with mock error environment
    app.terminate()
    app.launchEnvironment["MOCK_NETWORK_ERROR"] = "1"
    app.launch()
    
    // Trigger network request
    app.buttons["refresh-button"].tap()
    
    // Assert error is shown
    let errorView = app.staticTexts["error-message"]
    XCTAssertTrue(errorView.waitForExistence(timeout: 10))
    
    // Assert retry button is available
    XCTAssertTrue(app.buttons["retry-button"].exists)
}
```

### Testing Dark Mode / Appearance

```swift
func testDarkModeAppearance() throws {
    // Take screenshot in light mode
    let lightScreenshot = app.screenshot()
    let lightAttachment = XCTAttachment(screenshot: lightScreenshot)
    lightAttachment.name = "LightMode"
    add(lightAttachment)
    
    // Note: Programmatic appearance switching requires app support
    // The app should check launch arguments or environment
    app.terminate()
    app.launchArguments.append("-darkMode")
    app.launch()
    
    let darkScreenshot = app.screenshot()
    let darkAttachment = XCTAttachment(screenshot: darkScreenshot)
    darkAttachment.name = "DarkMode"
    add(darkAttachment)
}
```

## Common Gotchas

### 1. Timing Issues

```swift
// BAD: No wait — element might not exist yet
XCTAssertTrue(app.buttons["save-button"].exists)

// GOOD: Wait for existence
XCTAssertTrue(app.buttons["save-button"].waitForExistence(timeout: 5))
```

### 2. Keyboard Obscuring Elements

```swift
// BAD: Element hidden behind keyboard
app.textFields["bottom-field"].tap()  // May fail if keyboard covers it

// GOOD: Dismiss keyboard first, or scroll to element
app.swipeUp()  // Scroll to make element visible
app.textFields["bottom-field"].tap()
```

### 3. Animations Blocking Tests

```swift
// Speed up tests by disabling animations
app.launchArguments.append("-disableAnimations")

// In app code:
if CommandLine.arguments.contains("-disableAnimations") {
    #if os(iOS)
    UIView.setAnimationsEnabled(false)
    #endif
}
```

### 4. Multiple Matches

```swift
// BAD: Crashes if multiple elements match
app.buttons["cell-button"].tap()  // Which one?

// GOOD: Use specific identifier or index within scope
app.cells["item-row-1"].buttons["cell-button"].tap()
```

### 5. Test Isolation

```swift
// BAD: Tests depend on order or shared state
func testA() { /* creates data */ }
func testB() { /* expects data from testA */ }

// GOOD: Each test is independent
override func setUpWithError() throws {
    app.launchArguments.append("-resetOnLaunch")
    app.launch()
}
```

### 6. staticTexts Value vs Label (SwiftUI)

In SwiftUI, `staticTexts` elements expose their content through the `value` property, NOT `label`. The `label` property is always empty for SwiftUI `Text` views.

```swift
// WRONG — label is always "" for SwiftUI Text views
XCTAssertEqual(app.staticTexts["welcome-message"].label, "Hello World")  // label is ""

// RIGHT — use .value for SwiftUI
XCTAssertEqual(app.staticTexts["welcome-message"].value as? String, "Hello World")
```

This only affects SwiftUI. AppKit `NSTextField` and UIKit `UILabel` behave differently.

When checking `project.json` → `apps[].framework`:
- `swiftui` → use `.value as? String`
- `appkit` → use `.stringValue` or `.label`
- `uikit` → use `.label`

### 7. Test File Registration in Xcode Project (pbxproj)

Files placed on disk in the UI test target directory will compile but **0 tests will execute** unless they are registered in the `.xcodeproj/project.pbxproj` file. There are **FOUR** places a test file must appear:

1. **PBXBuildFile section** — `{BUILD_FILE_ID} /* {FileName}.swift in Sources */ = {isa = PBXBuildFile; fileRef = {FILE_REF_ID} /* {FileName}.swift */; };`
2. **PBXFileReference section** — `{FILE_REF_ID} /* {FileName}.swift */ = {isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = {FileName}.swift; sourceTree = "<group>"; };`
3. **PBXGroup children** for the test target group — `{FILE_REF_ID} /* {FileName}.swift */,`
4. **PBXSourcesBuildPhase files** for the test target — `{BUILD_FILE_ID} /* {FileName}.swift in Sources */,`

**How to find the right IDs:**

1. Search pbxproj for the test target name (from `project.json` → `testing.ui.testTarget`)
2. Find the PBXGroup that contains existing test files — note its ID
3. Find the PBXSourcesBuildPhase for the test target — note its ID
4. Generate unique 24-character hex IDs for the new `BUILD_FILE_ID` and `FILE_REF_ID`
5. Check project-specific testing conventions (via `project.json` → `context.testing`) for any ID prefix conventions

**Before adding, always verify not already registered:**

```bash
grep "YourTestFileName" *.xcodeproj/project.pbxproj
```

**Common failure mode:** Agent creates the `.swift` file, builds successfully (file compiles), but `xcodebuild test` reports 0 tests found for that class. This ALWAYS means pbxproj registration is missing.

### 8. NSPredicate Timeout Trap

Complex NSPredicates with multiple `OR` or `CONTAINS` clauses cause XCUITest to hang for ~160 seconds before failing. This looks like a frozen test but is actually the accessibility system doing an exhaustive search.

```swift
// WRONG — will hang for ~160 seconds
let predicate = NSPredicate(format: "label CONTAINS 'error' OR label CONTAINS 'fail' OR label CONTAINS 'invalid'")
app.staticTexts.matching(predicate).firstMatch.waitForExistence(timeout: 5)

// RIGHT — fast, sequential checks
let errorTexts = ["error", "fail", "invalid"]
let found = errorTexts.contains { keyword in
    app.staticTexts.matching(NSPredicate(format: "label CONTAINS %@", keyword)).count > 0
}

// BEST — use accessibility identifiers instead of text matching
app.staticTexts["form-error-message"].waitForExistence(timeout: 5)
```

## Running Tests

### From Command Line

```bash
# Run all UI tests
xcodebuild test \
  -project MyApp.xcodeproj \
  -scheme MyApp \
  -destination 'platform=macOS' \
  -only-testing:MyAppUITests

# Run a specific test class
xcodebuild test \
  -project MyApp.xcodeproj \
  -scheme MyApp \
  -destination 'platform=macOS' \
  -only-testing:MyAppUITests/LoginUITests

# Run a specific test method
xcodebuild test \
  -project MyApp.xcodeproj \
  -scheme MyApp \
  -destination 'platform=macOS' \
  -only-testing:MyAppUITests/LoginUITests/testSuccessfulLogin

# Run on iOS simulator
xcodebuild test \
  -project MyApp.xcodeproj \
  -scheme MyApp \
  -destination 'platform=iOS Simulator,name=iPhone 16'

# With workspace (CocoaPods, SPM)
xcodebuild test \
  -workspace MyApp.xcworkspace \
  -scheme MyApp \
  -destination 'platform=macOS'

# Generate code coverage
xcodebuild test \
  -project MyApp.xcodeproj \
  -scheme MyApp \
  -destination 'platform=macOS' \
  -enableCodeCoverage YES \
  -resultBundlePath TestResults.xcresult
```

### Result Bundle Analysis

```bash
# View test results summary
xcrun xcresulttool get --format json --path TestResults.xcresult

# Extract screenshots from results
xcrun xcresulttool export \
  --type file \
  --path TestResults.xcresult \
  --id <attachment-id> \
  --output-path screenshot.png
```

## Related Skills

- `swift-dev` — Swift implementation agent (writes XCUITest tests when implementing features)
- `swift-critic` — Swift code review agent (reviews XCUITest tests for quality)
- `ui-test-ux-quality` — Quality-beyond-correctness patterns (visual stability, performance)
- `test-flow` — Unified test flow for story/task completion
- `screenshot` — Capture screenshots for visual verification
