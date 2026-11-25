---
name: tca-swiftui
description: "Use for any question about The Composable Architecture (TCA) — defining reducers, managing state, handling navigation, writing tests, or working with dependencies. Essential when encountering TCA-specific types like @Reducer, @ObservableState, StackState, StackAction, @Presents, TestStore, @DependencyClient, Scope, or delegate actions. Also use when debugging TCA compiler errors, decomposing large reducers into child features, migrating from old TCA patterns (WithViewStore, Environment, IfLetStore), or implementing sheet/push navigation in TCA. Claude's training data contains outdated TCA patterns — invoke this skill whenever TCA code is involved to get correct modern (1.7+) patterns."
metadata:
  version: 1.0.3
---

> **Approach: Production-First Iterative Refactoring** — This skill is built for production enterprise codebases using The Composable Architecture. Architecture changes are delivered through iterative refactoring — small, focused PRs tracked in a `refactoring/` directory. AI tools consistently generate outdated TCA code (pre-1.4 patterns, WithViewStore, Environment, Combine Effects). Every rule here exists to prevent those mistakes.

# TCA SwiftUI Architecture (iOS 16+, TCA 1.7+)

Enterprise-grade skill for The Composable Architecture (point-free/swift-composable-architecture). Opinionated: prescribes `@Reducer` macro, `@ObservableState`, struct-of-closures dependencies, delegate actions for child-parent communication, and modern navigation via `@Presents`/`StackState`. TCA's API changed substantially across versions — AI tools trained on pre-1.7 code consistently generate `WithViewStore`, `IfLetStore`, `Environment`, and other removed patterns. This skill encodes the modern (1.7+) patterns validated against real enterprise codebases.

> **If the project uses TCA <1.7**, consult `references/migration.md` for pre-macro patterns and incremental upgrade path.

## Architecture Layers

```
View Layer         → SwiftUI Views. Direct store access, NO WithViewStore.
                     Owns store via let/var. Uses @Bindable for $ bindings.
Reducer Layer      → @Reducer struct. State + Action + body. Pure logic.
                     Returns Effect for async work. ALWAYS runs on main thread.
Effect Layer       → .run { send in } for async. .send for sync delegate actions.
                     Cancellable, mergeable, concatenatable.
Dependency Layer   → @DependencyClient structs. Struct-of-closures, NOT protocols.
                     liveValue (app) / testValue (auto-unimplemented) / previewValue.
```

## Quick Decision Trees

### "Should this be its own Feature reducer?"

```
Does this component have its own screen/view?
├── YES → Own @Reducer struct
└── NO → Does it have business logic you want to unit test?
    ├── YES → Own @Reducer struct, compose via Scope
    └── NO → Is its state optional (not always visible)?
        ├── YES → Own @Reducer, use ifLet (avoids unnecessary work)
        └── NO → Keep logic in parent reducer
```

### "What navigation pattern do I need?"

```
What type of navigation?
├── Modal (sheet/alert/dialog/fullScreenCover)?
│   → Tree-based: @Presents + PresentationAction + ifLet
├── Single drill-down?
│   → Tree-based: optional state + navigationDestination
├── Multi-level push (NavigationStack)?
│   → Stack-based: StackState + StackAction + forEach
├── Deep linking is critical?
│   → Stack-based (easy to construct state array)
└── Modals FROM within a NavigationStack?
    → BOTH: stack for push nav, tree for sheets/alerts
```

### "How should child communicate with parent?"

```
Child needs to tell parent something happened?
├── Use delegate action: case delegate(DelegateAction)
│   Parent observes ONLY .delegate cases, never child internals
│
Child needs to share logic between action cases?
├── Use mutating func on State or private helper method
│   NEVER send an action to share logic — it traverses the entire reducer tree unnecessarily,
│   creating hidden coupling and making performance profiling difficult
│
Sibling reducers need to communicate?
└── Delegate up to parent, parent coordinates
    NEVER send actions between siblings directly — siblings should not know about each other
```

## Workflows

### Workflow: Create a New TCA Feature

**When:** Building a new screen or self-contained feature from scratch.

1. Define State as `@ObservableState struct` inside `@Reducer` — conform to `Equatable`
2. Define Action enum inside `@Reducer` — NO `Equatable` conformance needed (TCA 1.4+)
3. Use three-category action pattern: `view(ViewAction)`, `internal(InternalAction)`, `delegate(DelegateAction)` (`rules.md`)
4. Implement `var body: some ReducerOf<Self>` — use `Reduce<State, Action> { }` for explicit generics (helps Xcode autocomplete)
5. Add child features via `Scope`, `ifLet`, or `forEach` BEFORE parent `Reduce` block
6. Create dependencies with `@DependencyClient` macro (`dependencies.md`)
7. Wire view: direct `store.property` access, `@Bindable var store` for `$` bindings
8. Write exhaustive TestStore tests (`testing.md`)

### Workflow: Decompose a God Reducer

**When:** A single reducer handles logic for multiple screens, has 800+ lines, or testing is impossible to isolate.

1. Identify feature boundaries — each screen = own reducer
2. Scan for anti-patterns using detection checklist (`anti-patterns.md`)
3. Create `refactoring/` directory with per-feature plan files (`refactoring-workflow.md`)
4. Extract child reducers bottom-up: leaf features first, then mid-level, then root
5. Use `Scope(state:action:)` for always-present children
6. Use `.ifLet(\.$destination, action: \.destination)` for optional children — effects auto-cancel on dismissal
7. Use `.forEach(\.path, action: \.path)` for stack navigation
8. Convert child-parent communication to delegate actions — parent must NEVER observe child internal actions
9. Write non-exhaustive integration tests for cross-feature flows (`testing.md`)

### Workflow: Migrate Legacy TCA to Modern (1.7+)

**When:** Modernizing pre-1.7 TCA code that uses WithViewStore, IfLetStore, Environment, etc.

1. Ensure TCA 1.4+ with `@Reducer` macro on all reducers (prerequisite)
2. Migrate feature-by-feature, bottom-up (leaf features first) (`migration.md`)
3. Per feature: add `@ObservableState` to State AND update view simultaneously — never one without the other
4. Replace `@PresentationState` with `@Presents`
5. Replace `WithViewStore(store, observe: { $0 })` with direct `store.property` access
6. Replace `IfLetStore`/`ForEachStore`/`SwitchStore` with native SwiftUI + store.scope
7. Replace `NavigationStackStore` with `NavigationStack(path: $store.scope(...))`
8. For iOS 16: wrap views in `WithPerceptionTracking { }`
9. Run existing tests — all must pass before proceeding to next feature
10. See full migration checklist and syntax transformations in `migration.md`

## Code Generation Rules

<critical_rules>
AI tools consistently generate outdated TCA code. Every output must use MODERN TCA (1.7+). ALWAYS:

1. Use `@Reducer` macro — never bare `struct Feature: Reducer` conformance
2. Use `@ObservableState` on ALL State types — never generate State without it
3. Define State AND Action INSIDE the `@Reducer` struct body — never in extensions (macros can't see them)
4. Use `@Reducer enum` for Destination/Path reducers (TCA 1.8+) — eliminates massive boilerplate
5. Action does NOT need `Equatable` — remove it. Why: TCA 1.4+ uses case key paths for cancellation and `receive()` matching, making Equatable conformance unnecessary and a maintenance burden
6. Access store properties directly: `store.count`, `store.send(.tapped)` — NEVER use `WithViewStore`
7. Use `@Bindable var store` when `$store` bindings are needed
8. Use `.run { send in }` for effects — never `EffectTask`, `.task { }`, `.fireAndForget { }`
9. Use enum-with-cases for cancel IDs — never empty enum types (pruned in release builds)
10. Never capture whole `@ObservableState` in effect closures — extract needed values first
11. Never do expensive work in reducers — they run on main thread. Offload to `.run` effects.
</critical_rules>

<fallback_strategies>
When working with TCA code, you may encounter cryptic compiler errors. If you fail to fix the same error twice:

1. **"compiler is unable to type-check this expression"**: State/Action likely defined in extension instead of inside `@Reducer` struct. Move them inside.
2. **"Circular reference resolving attached macro 'Reducer'"**: Don't nest `@Reducer struct Y` inside extension of another `@Reducer struct X`. Extract to top level.
3. **Macro + property wrapper conflict**: Avoid property wrappers inside `@ObservableState` State. Use `@ObservationStateIgnored` as workaround (changes won't trigger re-renders).
4. **"A 'reduce' method should not be defined in a reducer with a 'body'"**: Never define BOTH `reduce(into:action:)` AND `var body` in the same reducer.
5. **NavigationStack dismiss fights**: Ensure `.navigationDestination` is OUTSIDE `ForEach`/`List`, not inside.
</fallback_strategies>

## Modernization Migration Cheat-Sheet

When migrating legacy TCA code or writing new features, these 7 tokens come up repeatedly. They are NOT optional — AI tools consistently default to the outdated form on the left. Always use the right column.

| Legacy / outdated | Modern (TCA 1.7+, 2026) | Why |
|---|---|---|
| `environment.mainQueue` | `@Dependency(\.continuousClock)` | `mainQueue` was the pre-1.0 scheduler injection. In modern TCA, timing is a `Clock` dependency — override it with `ImmediateClock` or `TestClock` in tests. |
| `AnySchedulerOf<DispatchQueue>` in State | `@Dependency(\.continuousClock)` | Same as above. Schedulers are no longer passed through State — they are dependencies. Use `try await clock.sleep(for: .seconds(0.3))` in `.run` effects. |
| `@Bindable var store` (iOS 17+ only) | **iOS 16**: `@Perception.Bindable var store` — **iOS 17+**: `@Bindable var store` | `@Perception.Bindable` is TCA's backport of SwiftUI's `@Bindable` for iOS 16 because Apple's `@Bindable` requires iOS 17. Without it, `$store.binding` fails to compile on iOS 16 targets. |
| `Bool showLogoutAlert` in State | `@Presents var alert: AlertState<Action>?` | Alerts belong in `AlertState`, not in booleans — this gives you message text, button state, and action dispatching in one value, and it auto-dismisses through standard `@Presents`. |
| `[Product]` in State | `IdentifiedArrayOf<Product>` | Plain arrays force O(n) updates-by-ID and confuse `ForEachStore`. `IdentifiedArrayOf` (`import IdentifiedCollections`) is the canonical TCA collection — constant-time lookup by `id`, stable animations, required by `forEach(\.items, ...)`. |
| `var filtered: [T] { state.items.filter { ... } }` (computed) | Stored `var filtered: IdentifiedArrayOf<T>` updated in the reducer | Computed vars on State hide reducer work from TCA's observation system and run on every access. Store the derived value and recompute it in the action that changes the source — it shows up in the action log and is testable. |
| `.run { try? await api.delete(id) }` | `.run { send in try await api.delete(id); await send(.deleteSucceeded) } catch: { error, send in await send(.deleteFailed(error)) }` | `try?` inside effects is a silent-failure bug — the UI thinks the delete worked but nothing changed on the server. Use the `catch:` parameter on `.run` and emit an explicit failure action. |

### Dismiss-in-delegate-handler pattern

When a child feature finishes (save, cancel, delete) and the parent uses `@Presents`, the parent MUST dismiss in the same handler that processes the delegate action:

```swift
case .destination(.presented(.editor(.delegate(.saved(let item))))):
    state.items.append(item)
    state.destination = nil    // ← REQUIRED. Without this, the sheet stays open.
    return .none
```

Forgetting `state.destination = nil` is the #1 TCA navigation bug — the save succeeds but the sheet never dismisses. For an alternative, child features can use `@Dependency(\.dismiss)` and call `await dismiss()` inside their own effects.

### `unimplemented(placeholder:)` for non-Void test dependencies

`@DependencyClient`'s `testValue` auto-generates `unimplemented(...)` for `() -> Void` closures, but returning non-Void requires a placeholder. Without it, the test crashes with "dependency has no implementation":

```swift
@DependencyClient
struct ProfileClient {
    var fetch: @Sendable (User.ID) async throws -> Profile = {
        _ in unimplemented("ProfileClient.fetch", placeholder: Profile.mock)
    }
}
```

The `placeholder:` value is used only when the test does NOT assert against `fetch` — it prevents the crash while still failing the test if the call is unexpected.

## Confidence Checks

Before finalizing generated or refactored TCA code, verify ALL:

```
[ ] @Reducer macro — present on all feature structs
[ ] @ObservableState — present on all State types
[ ] State/Action — defined INSIDE @Reducer struct, not in extensions
[ ] No WithViewStore — direct store access everywhere
[ ] No Equatable on Action — removed (unnecessary since TCA 1.4)
[ ] Delegate actions — child-parent communication uses .delegate pattern
[ ] Effect closures — capture only needed values, not whole state
[ ] Cancel IDs — enum with cases, NOT empty enum types
[ ] Navigation — @Presents for modals, StackState for push nav, never nested NavigationStack
[ ] Dependencies — @DependencyClient struct-of-closures, not protocols
[ ] Tests — TestStore with exhaustive assertions, @MainActor annotated
[ ] Schedulers — `@Dependency(\.continuousClock)`, NOT `mainQueue` or `AnySchedulerOf`
[ ] iOS 16 bindings — `@Perception.Bindable` used instead of `@Bindable` when deployment target is iOS 16
[ ] Collections in State — `IdentifiedArrayOf` used instead of `[T]`
[ ] Derived state — stored property updated in reducer, NOT a computed var on State
[ ] `.run` effects — use `catch:` parameter, never `try?` inside effect closures
[ ] Alert state — `AlertState<Action>` in `@Presents`, NOT a `Bool showXAlert`
[ ] File size — new files <= 400 lines; oversized files have split task in refactoring/
```

## Companion Skills

| Project need | Companion skill | Apply when |
|---|---|---|
| Swift Concurrency patterns | `skills/swift-concurrency/SKILL.md` | Writing async effects, actor isolation, Sendable compliance |
| GCD/OperationQueue legacy code | `skills/gcd-operations/SKILL.md` | Legacy async work before migrating to TCA effects |
| Comprehensive testing guidance | `skills/ios-testing/SKILL.md` | Advanced testing patterns beyond TCA TestStore |
| Security audit | `skills/ios-security/SKILL.md` | Auditing Keychain usage, network security in TCA apps |

## References

| Reference | When to Read |
|-----------|-------------|
| `references/rules.md` | Do's and Don'ts quick reference: modern TCA patterns and critical anti-patterns |
| `references/reducer-architecture.md` | @Reducer macro rules, feature decomposition, parent-child scoping, state design |
| `references/effects.md` | Effect API (.run, .send, .merge, .cancel), cancellation, long-running effects, anti-patterns |
| `references/dependencies.md` | @DependencyClient, DependencyKey, liveValue/testValue, module boundaries, test guards |
| `references/navigation.md` | Tree-based (@Presents/ifLet), stack-based (StackState/forEach), dismissal, deep linking |
| `references/testing.md` | TestStore exhaustive/non-exhaustive, TestClock, case key paths, per-feature checklist |
| `references/migration.md` | Version progression, per-feature migration checklist, syntax transformations, known issues |
| `references/anti-patterns.md` | AI-specific mistakes, god reducer signs, performance pitfalls, enterprise concerns |
| `references/performance.md` | Action costs, _printChanges, .signpost, scope performance, high-frequency action mitigation |
| `references/refactoring-workflow.md` | `refactoring/` directory protocol, per-feature plans, PR sizing, phase ordering |
