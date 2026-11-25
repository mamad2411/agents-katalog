---
name: verify-flutter
description: "Flutter verification checklist — Riverpod, Freezed, Dio, pagination, contract alignment."
disable-model-invocation: true
---

# Skill: Verify Flutter

## Purpose
Systematic verification checklist for Flutter/Dart code following the conventions in `flutter-patterns.md`. Used by the reviewer agent after code execution.

## Verification Process

Run through each section. Flag issues as PASS, WARN, or FAIL.

### 1. Project Structure
- [ ] Feature-based organization: `features/{name}/models|services|providers|screens|widgets`
- [ ] Core infrastructure in `core/` (api, error, router, theme, providers, utils, widgets)
- [ ] File naming follows `snake_case.dart` convention
- [ ] Generated files co-located (`.freezed.dart`, `.g.dart` next to source)
- [ ] No orphan files outside the expected structure

### 2. Models
- [ ] Freezed with `json_serializable` — `@freezed class` with `_$` mixin
- [ ] `const Model._()` private constructor for custom getters
- [ ] `factory Model.fromJson()` and generated `toJson()`
- [ ] `@JsonKey(name: ...)` for snake_case API fields
- [ ] `@JsonKey(includeToJson: false)` for server-managed fields (id, created_at)
- [ ] `factory Model.empty()` for form initialization
- [ ] `bool get exists` for create-vs-update logic
- [ ] Codegen is up to date (`build_runner build` produces no changes)
- [ ] Model shapes match API response (compare to integration summary)

### 3. Services
- [ ] Abstract interface defines the contract (`abstract class {Feature}Service`)
- [ ] Concrete implementation per backend (`{Feature}ServiceDjango implements {Feature}Service`)
- [ ] `save()` combines create + update using `model.exists`
- [ ] No `Either`/`fpdart` — errors thrown as typed `Failure`
- [ ] One service per feature, one implementation per backend

### 4. Providers
- [ ] `@riverpod` codegen used everywhere (no hand-written providers)
- [ ] `@riverpod` (lowercase, auto-dispose) for reads — detail, service binding
- [ ] `@Riverpod(keepAlive: true)` for forms and auth state
- [ ] `AsyncNotifier` for stateful operations (forms, paginated lists)
- [ ] Functional providers for simple reads (detail, service binding)
- [ ] `AsyncValue.guard()` wraps async calls
- [ ] `ref.invalidate()` called on related providers after mutations
- [ ] Form providers own `TextEditingController`s and `GlobalKey<FormState>`

### 5. Screens
- [ ] Screens extend `BaseScreen`
- [ ] Static `route()` method returns the path string
- [ ] `ref.watch()` in `body()` for reactive data, `ref.read()` for actions
- [ ] `AsyncValue.when()` handles loading/error/data states
- [ ] `context.mounted` checked after async operations before navigation

### 6. Widgets
- [ ] Extracted when exceeding ~40 lines or reused
- [ ] One widget per file in `widgets/`
- [ ] `const` constructors with all `final` fields
- [ ] Composition over inheritance (except `BaseScreen`)
- [ ] `ConsumerWidget` only when the widget needs `ref`
- [ ] No deep nesting — sub-widgets extracted at 3-4 levels
- [ ] Data passed as constructor params, not fetched inside leaf widgets

### 7. API Client
- [ ] Single `Dio` instance (no per-request construction)
- [ ] Timeouts configured (`connectTimeout`, `receiveTimeout`)
- [ ] Auth interceptor injects Bearer token from session
- [ ] Token refresh handled in interceptor (not scattered across services)
- [ ] 401 response clears session token
- [ ] `LogInterceptor` gated behind `kDebugMode`
- [ ] No raw `print()` statements
- [ ] `DioException` caught and mapped to typed `Failure`

### 8. Auth
- [ ] `flutter_secure_storage` for token persistence (not SharedPreferences)
- [ ] Session provider is `keepAlive: true`
- [ ] Auth provider uses `AsyncValue<User?>` — null means logged out
- [ ] Router watches auth provider and rebuilds on state changes
- [ ] Auth guard redirects unauthenticated users to login
- [ ] Logout clears both session state and secure storage

### 9. Error Handling
- [ ] Sealed `Failure` class hierarchy (not generic `Exception`)
- [ ] Subtypes: `ServerFailure`, `NetworkFailure`, `AuthFailure`, `ValidationFailure`
- [ ] `ValidationFailure` carries `fieldErrors` map
- [ ] Services throw typed failures, not raw exceptions
- [ ] Providers surface errors via `AsyncValue.error`
- [ ] UI uses `ref.listen()` or `AsyncValue.when()` to display errors
- [ ] No swallowed exceptions — every catch block surfaces or rethrows

### 10. Forms
- [ ] Form provider extends `AsyncNotifier` with `keepAlive: true`
- [ ] `load(Model)` populates controllers from existing data
- [ ] `reset()` clears state and controllers
- [ ] `submit()` validates form, calls service, invalidates related providers
- [ ] `GlobalKey<FormState>` for validation
- [ ] Loading state shown during submission
- [ ] Error messages displayed on failure
- [ ] Form widget uses `ConsumerWidget` with `ref.read()` for notifier, `ref.watch()` for state

### 11. Lists
- [ ] Paginated list uses `AsyncNotifier` with page controls
- [ ] Infinite scroll uses `PagingController` from `infinite_scroll_pagination`
- [ ] `PaginatedResponse<T>` model with `canLoadMore` getter
- [ ] Filtering and ordering passed as query parameters through service
- [ ] `RefreshIndicator` for pull-to-refresh
- [ ] Empty state shown when no results

### 12. Testing
- [ ] `flutter test` passes with no failures
- [ ] `mocktail` for mocking (not `mockito`)
- [ ] Service providers overridden in tests — Dio never mocked directly
- [ ] Widget tests wrap with `ProviderScope` + `MaterialApp`
- [ ] Tests assert behavior (what user sees), not implementation
- [ ] Business logic has unit tests (services, providers)
- [ ] Key widgets have widget tests

### 13. Code Quality
- [ ] `dart analyze` passes with no issues
- [ ] No commented-out code
- [ ] No debug `print()` statements
- [ ] Imports organized (dart, package, relative)
- [ ] Consistent naming (camelCase variables, PascalCase classes, snake_case files)
- [ ] `require_trailing_commas` lint enabled and followed

## Output
Produce a `verification-report.md`:
```markdown
# Verification Report: [Feature/Phase]
Date: [date]
Reviewer: Claude (automated)

## Summary: [PASS/WARN/FAIL]

## Details
### Project Structure: [PASS/WARN/FAIL]
- [notes]

### Models: [PASS/WARN/FAIL]
- [notes]

### Services: [PASS/WARN/FAIL]
- [notes]

...

## Issues Found
1. [FAIL] Description + suggested fix
2. [WARN] Description + recommendation

## Recommended Actions
- [ ] Fix: ...
- [ ] Consider: ...
```
