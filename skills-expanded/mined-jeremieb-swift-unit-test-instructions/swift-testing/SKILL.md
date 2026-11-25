---
name: swift-testing
description: Writes unit tests and UI tests for Swift, SwiftUI, and UIKit projects following enterprise or indie testing standards. Use when user says "write tests", "add unit tests", "test this code", "create test cases", "add XCTest", "write Swift Testing tests", "help me test this", or "add tests for". Applies enterprise or indie standard from references/ based on project CLAUDE.md config.
metadata:
  author: swift-unit-test-instructions
  version: 1.0.0
  category: swift
---

# Swift Testing

## Instructions

### Step 1: Determine Testing Mode

Check `CLAUDE.md` for `Testing Mode`:
- `enterprise` → consult `references/enterprise.md` for strict rules
- `indie` → consult `references/indie.md` for pragmatic rules
- If not set: ask the user which mode applies

### Step 2: Identify What to Test

Ask if not already clear:
- Which type / function / feature needs tests?
- What is the expected behavior (not implementation)?
- Are there async operations?
- Are there existing mocks or does the skill need to create them?

**Always test:**
- ViewModels (state changes, actions, error states)
- Services and Repositories (business logic, data transformations)
- Formatters, validators, utilities
- Async flows end-to-end (with mocked dependencies)
- Edge cases and error paths

**Never test:**
- Private implementation details
- SwiftUI view tree structure or layout positions
- UIViewController internal wiring

### Step 3: Choose the Framework

| Scenario | Framework |
|---|---|
| New unit tests (Swift 5.9+, iOS 16+) | Swift Testing (`@Test`, `#expect`) |
| Legacy or team convention on XCTest | XCTest (`XCTestCase`, `XCTAssert*`) |
| UI / end-to-end tests | XCTest + XCUITest |
| Async unit tests | Both support `async` — use `await` |

Do NOT mix Swift Testing and XCTest in the same test target.

### Step 4: Write Tests

**Naming (both frameworks):**
```
test_when_<Condition>_should_<ExpectedOutcome>()
```

**Structure — Swift Testing:**
```swift
import Testing
@testable import MyApp

@MainActor
struct LoginViewModelTests {

    @Test func test_when_credentialsAreValid_should_setIsLoggedIn() async throws {
        // Arrange
        let authService = MockAuthService(willSucceed: true)
        let sut = LoginViewModel(authService: authService)

        // Act
        await sut.login(email: "user@example.com", password: "secret")

        // Assert
        #expect(sut.isLoggedIn == true)
        #expect(sut.error == nil)
    }

    @Test func test_when_credentialsAreInvalid_should_setError() async throws {
        // Arrange
        let authService = MockAuthService(willSucceed: false)
        let sut = LoginViewModel(authService: authService)

        // Act
        await sut.login(email: "bad@example.com", password: "wrong")

        // Assert
        #expect(sut.isLoggedIn == false)
        #expect(sut.error != nil)
    }
}
```

**Structure — XCTest:**
```swift
import XCTest
@testable import MyApp

@MainActor
final class LoginViewModelTests: XCTestCase {

    func test_when_credentialsAreValid_should_setIsLoggedIn() async throws {
        // Arrange
        let authService = MockAuthService(willSucceed: true)
        let sut = LoginViewModel(authService: authService)

        // Act
        await sut.login(email: "user@example.com", password: "secret")

        // Assert
        XCTAssertTrue(sut.isLoggedIn)
        XCTAssertNil(sut.error)
    }
}
```

### Step 5: Generate Mocks

Always generate a mock alongside any test that needs one:

```swift
// Always inject via protocol, never use real implementations in unit tests
final class MockAuthService: AuthServiceProtocol {
    let willSucceed: Bool
    private(set) var loginCallCount = 0

    init(willSucceed: Bool) {
        self.willSucceed = willSucceed
    }

    func login(email: String, password: String) async throws -> User {
        loginCallCount += 1
        if willSucceed {
            return User(id: "1", email: email)
        } else {
            throw AuthError.invalidCredentials
        }
    }
}
```

### Step 6: Determinism Checklist

Before finalizing, verify every test:
- [ ] No real network calls
- [ ] No `sleep()` or polling
- [ ] No shared global state between tests
- [ ] No real time/date dependency (inject `Date` or a clock protocol)
- [ ] Fresh `sut` instance per test
- [ ] `setUp`/`tearDown` only when truly necessary

## Examples

### Example 1: ViewModel with async fetch

User says: "Write tests for my ProductListViewModel that fetches products from an API"

Actions:
1. Read `ProductListViewModel.swift` to understand state and dependencies
2. Identify the `ProductRepositoryProtocol` or create it if missing
3. Generate `MockProductRepository` with stubbable results
4. Write tests: empty state, loaded state, error state, loading indicator

### Example 2: Data transformation

User says: "Test my PriceFormatter that converts cents to currency string"

Actions:
1. Read `PriceFormatter.swift`
2. Write Swift Testing `@Test` functions for: zero cents, typical value, large value, locale edge cases

## Troubleshooting

**Async tests fail intermittently**: You are using `sleep()` or polling. Replace with `async/await` and mocked async dependencies that resolve immediately.

**Tests break on refactoring**: You are testing implementation details (private properties, internal call counts). Refocus on observable output state only.

**ViewModel is untestable**: Dependencies are created inside the type (`NetworkService()`). Inject them via `init`. This is an architecture issue — see `swift-architecture-audit` skill.

**"Cannot find type X in scope"**: Add `@testable import YourModule` at the top of the test file.
