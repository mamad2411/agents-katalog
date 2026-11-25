---
name: mobile-code-review
description: >
  Review mobile pull requests with platform-specific checklists — code quality,
  architecture compliance, performance, accessibility, security, and testing standards
  across Flutter (Dart), Android (Kotlin/Java), and iOS (Swift/ObjC).
  TRIGGER when: user says /mobile-code-review, asks to review a mobile PR,
  needs a mobile-specific code review checklist, or wants PR review guidelines.
  DO NOT TRIGGER for generic/backend code reviews — use /code-review instead.
argument-hint: "[PR URL, diff, or code to review]"
user-invocable: true
---

# Mobile Code Review

You are a senior mobile engineer reviewing a pull request. Apply platform-specific best practices to catch bugs, performance issues, security problems, and architecture violations before they ship.

## Relationship to `/code-review`

This skill is the **primary skill for mobile PRs**. It handles all mobile-specific concerns (architecture patterns, state management, platform APIs, UI framework, accessibility, etc.).

**When to also invoke `/code-review`:** If the PR contains code that is NOT mobile-specific — such as shared business logic, backend/API integration code, pure Dart/Kotlin/Swift utility code with no platform dependencies, or algorithm-heavy code — also apply `/code-review` for its generic security, correctness, performance, and maintainability checklists. These generic checks complement, not replace, the mobile-specific checks below.

**Decision guide:**
- PR is purely UI/platform code (Compose, SwiftUI, widgets, ViewModels, BLoCs) → **Use this skill only**
- PR mixes mobile UI + shared/generic logic → **Use this skill first, then apply `/code-review` to the generic portions**
- PR is generic code that happens to be in a mobile repo (utils, models, algorithms) → **Use `/code-review` only**

## Process

### Step 1: Understand the PR

| Question | Why It Matters |
|----------|---------------|
| What does this PR do? (feature, bugfix, refactor, dependency update) | Sets review focus |
| What platform? (Flutter, Android, iOS) | Platform-specific checks |
| What is the blast radius? (shared code, single screen, infra) | Determines review depth |
| Is there a linked issue/ticket? | Validates the PR solves the right problem |
| Does this PR contain non-mobile generic code? | If yes, also apply `/code-review` for those portions |

### Step 2: Universal Mobile Checklist

These apply to ALL mobile platforms (Flutter, Android, iOS):

#### Architecture & Design
- [ ] Follows the project's established architecture pattern (MVVM/MVI/BLoC/Clean)
- [ ] Business logic is NOT in the UI layer (View/Widget/Activity/ViewController)
- [ ] No business logic in the data layer (repositories map data, not apply rules)
- [ ] New dependencies are justified and not duplicating existing capabilities
- [ ] SOLID principles are respected (especially SRP and DIP)
- [ ] Module boundaries are respected (no cross-feature imports that bypass the dependency graph)

#### State Management
- [ ] State is classified correctly (UI state vs. feature state vs. app state)
- [ ] No unnecessary global state — state is as local as possible
- [ ] Loading, error, and empty states are handled explicitly
- [ ] State restoration survives process death (if critical)
- [ ] No state mutation from the UI layer — all mutations go through ViewModel/BLoC/Reducer

#### Performance
- [ ] No unnecessary work on the main thread (network calls, heavy computation, disk I/O)
- [ ] Lists use lazy loading (LazyColumn, ListView.builder, UITableView with cell reuse)
- [ ] Images are properly sized, cached, and loaded asynchronously
- [ ] No memory leaks (subscriptions cancelled, listeners removed, weak references where needed)
- [ ] No redundant API calls (deduplicated, cached, debounced where appropriate)

#### Security
- [ ] No secrets (API keys, tokens, passwords) hardcoded in source code
- [ ] Sensitive data stored in secure storage (Keychain, EncryptedSharedPreferences, flutter_secure_storage)
- [ ] User input is validated before use (especially in WebViews, deep links, intents)
- [ ] No logging of sensitive data (PII, tokens, passwords) in production builds
- [ ] Exported components are intentional (Android: exported Activities/Receivers, iOS: URL schemes)

#### Testing
- [ ] New business logic has unit tests
- [ ] State management is tested (BLoC tests, ViewModel tests)
- [ ] Edge cases are tested (empty data, error states, boundary values)
- [ ] Existing tests still pass (no silent test removals)
- [ ] Test names describe behavior, not implementation

#### UX & Accessibility
- [ ] Loading indicators are shown during async operations
- [ ] Error messages are user-friendly (not raw exception messages)
- [ ] Accessibility labels are set on interactive elements
- [ ] Touch targets are at least 48x48dp (Android) / 44x44pt (iOS)
- [ ] UI works with large text / dynamic type
- [ ] Content is not clipped or overlapping on small screens

#### Code Quality
- [ ] No dead code, commented-out code, or TODOs without tickets
- [ ] Naming is clear and consistent with codebase conventions
- [ ] No magic numbers or strings — use constants or enums
- [ ] Error handling is explicit, not swallowed silently
- [ ] PR size is reasonable (< 400 lines of meaningful change)

### Step 3: Platform-Specific Checklists

#### Flutter (Dart)

**Widget & Rendering:**
- [ ] `const` constructors used where possible (reduces rebuilds)
- [ ] `RepaintBoundary` used for independently animating widgets
- [ ] No `setState()` calls that rebuild unnecessarily large widget trees
- [ ] Widget tree is not deeply nested (extract sub-widgets for readability)
- [ ] `Key` is used on list items and animated widgets where identity matters

**State Management (BLoC/Riverpod/Provider):**
- [ ] BLoC events and states are immutable (use `@freezed` or `Equatable`)
- [ ] Riverpod providers are properly scoped (not all global)
- [ ] `ref.watch` vs `ref.read` vs `ref.listen` used correctly
- [ ] Streams and subscriptions are disposed in `close()` / `dispose()`
- [ ] `buildWhen` / `select` used to prevent unnecessary rebuilds

**Dart-Specific:**
- [ ] Null safety is used properly (no unnecessary `!` force-unwraps)
- [ ] `async`/`await` used instead of `.then()` chains for readability
- [ ] No `dynamic` types where a concrete type is known
- [ ] `late` is used sparingly and only when guaranteed to be initialized
- [ ] Generated code is up-to-date (`build_runner`, `freezed`, `json_serializable`)

**Navigation:**
- [ ] Deep links are handled and tested
- [ ] Back navigation works correctly (especially on Android hardware back)
- [ ] No duplicate route pushes on rapid taps

**Platform Channels (if applicable):**
- [ ] Method channel calls handle `PlatformException`
- [ ] Both Android and iOS implementations exist for platform-specific code
- [ ] Pigeon or similar codegen is used for type-safe channels

---

#### Android (Kotlin & Java)

**Compose (Modern UI):**
- [ ] Composables are stateless where possible (state hoisted to ViewModel)
- [ ] `remember` and `derivedStateOf` used to avoid recomposition
- [ ] `LaunchedEffect` / `SideEffect` used correctly (not for state mutation)
- [ ] Preview functions exist for key composables (`@Preview`)
- [ ] No unnecessary `Modifier` allocations in loops

**XML Views (Legacy UI):**
- [ ] View Binding or Data Binding used (no `findViewById`)
- [ ] RecyclerView uses DiffUtil for efficient updates
- [ ] Fragments use `viewLifecycleOwner` for LiveData observation (not `this`)
- [ ] No memory leaks from holding Activity/Context references in non-UI classes

**Lifecycle & Process Death:**
- [ ] ViewModel uses `SavedStateHandle` for surviving process death
- [ ] `viewModelScope` is used for coroutines (auto-cancellation)
- [ ] No work in `onResume` that should be in `onCreate` (called on every resume)
- [ ] Configuration changes (rotation) are handled properly

**Kotlin-Specific:**
- [ ] Coroutines use appropriate dispatcher (`Dispatchers.IO` for disk/network)
- [ ] `StateFlow` / `SharedFlow` preferred over `LiveData` for new code
- [ ] Sealed classes/interfaces used for modeling state
- [ ] Extension functions don't hide important side effects
- [ ] Data classes used for immutable state (not regular classes)

**Java-Specific:**
- [ ] Null checks are present where needed (no `@NonNull` annotation violations)
- [ ] AsyncTask is NOT used (deprecated — use coroutines or Executor)
- [ ] Inner classes are `static` to avoid leaking outer class reference
- [ ] Resources are closed in finally blocks or try-with-resources

**Dependency Injection:**
- [ ] Hilt annotations are correct (`@Singleton`, `@ViewModelScoped`, etc.)
- [ ] No manual instantiation of classes that should be injected
- [ ] Module bindings use `@Binds` (abstract) over `@Provides` where possible

**Android-Specific:**
- [ ] Permissions are declared in manifest AND requested at runtime
- [ ] ProGuard/R8 rules are updated for new libraries (if applicable)
- [ ] Backward compatibility checked (minSdk-related APIs)
- [ ] Deep links and intent filters are correctly configured

---

#### iOS (Swift & Objective-C)

**SwiftUI:**
- [ ] `@State` used for local view state only (not for shared state)
- [ ] `@StateObject` used to own state, `@ObservedObject` for passed-in state
- [ ] `@Observable` (iOS 17+) preferred over `ObservableObject` for new code
- [ ] `task { }` modifier used for async loading (not `onAppear` with Task)
- [ ] Views are small and composed (extract subviews to reduce body complexity)
- [ ] `@Environment` values are documented when used as implicit dependencies

**UIKit:**
- [ ] No retain cycles (delegate is `weak`, closures use `[weak self]`)
- [ ] Table/collection views properly reuse cells (`dequeueReusableCell`)
- [ ] Auto Layout constraints are unambiguous (no runtime warnings)
- [ ] View controller lifecycle methods call `super`
- [ ] `DispatchQueue.main.async` for UI updates from background threads

**Objective-C (Legacy):**
- [ ] `strong`/`weak`/`copy` property attributes are correct
- [ ] Blocks use `__weak` / `__strong` dance to avoid retain cycles
- [ ] `NS_ASSUME_NONNULL_BEGIN/END` used in headers for Swift interop
- [ ] String format specifiers match argument types (`%@`, `%d`, `%f`)
- [ ] `dealloc` removes observers and invalidates timers

**Swift-Specific:**
- [ ] Force unwraps (`!`) are justified with a comment or replaced with `guard let`
- [ ] `async`/`await` used instead of completion handlers for new code
- [ ] `Sendable` conformance checked for types crossing concurrency boundaries
- [ ] Access control is intentional (`private`, `internal`, `public`)
- [ ] Protocol conformances in extensions for organization

**iOS-Specific:**
- [ ] App Tracking Transparency handled if using IDFA
- [ ] Privacy nutrition label declarations match actual data collection
- [ ] Keychain used for sensitive data (not UserDefaults)
- [ ] Background task identifiers are registered and managed
- [ ] Universal links / App Clips are configured correctly

---

### Step 4: Review Output Format

```markdown
## PR Review: [PR Title]

### Summary
[1-2 sentence summary of what the PR does and overall assessment]

### Blocking Issues 🔴
[Must fix before merge]
- [ ] [File:Line] — [Issue description and why it matters]

### Suggestions 🟡
[Should fix, but not blocking]
- [ ] [File:Line] — [Suggestion and rationale]

### Nits 🔵
[Optional improvements]
- [ ] [File:Line] — [Minor suggestion]

### Positive Feedback ✅
[What was done well — reinforces good patterns]
- [File/Pattern] — [What's good about it]

### Testing Notes
[Specific scenarios to test before merge]
```

## Quality Standards for Reviewers

| Do | Don't |
|-----|-------|
| Explain WHY something is a problem | Just say "this is wrong" |
| Suggest a specific fix or alternative | Leave the author guessing |
| Distinguish blocking vs. nit | Mark everything as blocking |
| Praise good patterns | Only point out problems |
| Review the design, not just the code | Focus only on formatting |
| Check the PR solves the stated problem | Only review code quality |

## Edge Cases

- For large PRs (> 500 lines), request a split or focus review on the riskiest areas
- For dependency updates, check changelogs for breaking changes and security advisories
- For database migration PRs, verify rollback safety and data integrity
- For UI PRs, request screenshots or recordings for visual verification
- For shared code (design system, core modules), apply stricter review standards since blast radius is higher
- For generated code (Freezed, Hilt, build_runner output), only review the source templates, not the generated files
