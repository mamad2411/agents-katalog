---
name: ios-app-skeleton
description: Load when scaffolding a brand-new iOS app from scratch (Swift 6 + SwiftUI + SPM + Clean Architecture). Authoritative blueprint used by /init-ios-app — placeholder list, feature-flag block, target layout, execution order, hard rules, and post-scaffold checklist. File templates live in `references/` and are loaded step-by-step (progressive disclosure).
---

# iOS app skeleton

This file is the **procedure**. The actual file templates live in sibling files under `references/` — each execution-order step points at the reference it needs. Read the spine end-to-end first, then load each referenced file when its step runs. Substitute placeholders before writing; do not improvise.

## Target floor

**Swift 6 / Xcode 16 / iOS 18.** Older toolchains are not silently accommodated — `/init-ios-app` Phase 1.5 stops on a mismatch rather than lowering the floor. iOS 17 is reachable only through the compatibility deltas called out in `references/app-features.md`; anything below that is a different skeleton.

## Placeholders

| Placeholder | Meaning | Example |
|---|---|---|
| `{{APP_NAME}}` | Xcode/SPM product name, UpperCamelCase | `MyApp` |
| `{{BUNDLE_ID}}` | Bundle identifier | `com.example.myapp` |
| `{{APP_DISPLAY_NAME}}` | Human-facing name | `My App` |
| `{{ORG_NAME}}` | Organization name in project metadata | `Example Inc.` |

## Feature flags

| Flag | Adds |
|---|---|
| `INCLUDE_SWIFTDATA` | `Sources/AppCore/Persistence/` + `@Model` types + container boot |
| `INCLUDE_FIREBASE` | Firebase SPM deps + `FirebaseApp.configure()` wiring, plist reminder |

## Layout

**SPM-first.** The Swift package is the source of truth; the Xcode project is a thin shell that embeds it. Three products, one dependency direction: `AppCore` ← `AppFeatures` ← `App`.

```
{{APP_NAME}}/
├── Package.swift                     # three products: AppCore, AppFeatures, App
├── project.yml                       # xcodegen shell (optional)
├── Sources/
│   ├── AppCore/                      # framework-free domain — Foundation only
│   │   ├── Outcome.swift
│   │   ├── DomainError.swift
│   │   ├── APIClient.swift           # protocol
│   │   ├── KeychainStore.swift       # protocol
│   │   └── Persistence/              # INCLUDE_SWIFTDATA only
│   ├── AppFeatures/                  # SwiftUI views + @Observable view models
│   │   ├── Splash/{SplashView,SplashViewModel}.swift
│   │   └── Navigation/Destination.swift
│   └── App/                          # the only target that knows concrete frameworks
│       ├── {{APP_NAME}}App.swift
│       ├── CompositionRoot.swift
│       ├── URLSessionAPIClient.swift
│       └── KeychainStoreLive.swift
└── Tests/
    ├── AppCoreTests/                 # pure domain — no simulator needed
    └── AppFeaturesTests/             # @MainActor view-model tests
```

Why this split?

- **`AppCore` stays framework-free** so its tests run under `swift test` with no simulator, and so a view model can be exercised without stubbing URLSession or the Security framework.
- **`AppFeatures` depends on protocols, never on implementations.** `URLSessionAPIClient` and `KeychainStoreLive` live in the app target precisely so a feature cannot reach for them by accident.
- **`App` is the composition root.** One place constructs the object graph; features receive dependencies by initializer injection. See `ios-architecture` → layer boundaries.

Each feature added later mirrors `Splash/` — a stateless view, an `@Observable @MainActor` view model, a `Root` container, and a `#Preview`.

## Reference files

Templates live alongside this spine. Load each one when its step runs:

| File | Contains | Loaded at step |
|---|---|---|
| [`references/root-files.md`](references/root-files.md) | `Package.swift`, `.swiftformat`, `.gitignore` | 2 |
| [`references/app-core.md`](references/app-core.md) | `Outcome`, `DomainError`, `APIClient` protocol, `KeychainStore` protocol | 3 |
| [`references/app-features.md`](references/app-features.md) | `SplashView`, `SplashViewModel`, `Navigation/Destination.swift` | 4 |
| [`references/app-target.md`](references/app-target.md) | `{{APP_NAME}}App`, `CompositionRoot`, `URLSessionAPIClient`, `KeychainStoreLive` | 5 |
| [`references/tests.md`](references/tests.md) | `OutcomeTests`, `SplashViewModelTests` | 6 |
| [`references/project-yml.md`](references/project-yml.md) | `project.yml` for xcodegen, and when to skip it | 7 |
| [`references/optional-swiftdata.md`](references/optional-swiftdata.md) | `INCLUDE_SWIFTDATA`: `SchemaV1`, `PersistenceContainer` | 3, 5 (only if flag on) |
| [`references/optional-firebase.md`](references/optional-firebase.md) | `INCLUDE_FIREBASE`: SPM deps, `FirebaseApp.configure()`, per-scheme plist copy phase | 2, 10 (only if flag on) |

When the procedure below names a file, the bracketed reference tells you where its template lives.

## Execution order

1. Create `{{APP_NAME}}/` directory.
2. Write `Package.swift`, `.swiftformat`, `.gitignore`, `README.md` — templates in `references/root-files.md`. If `INCLUDE_FIREBASE`, add the SPM dependency now (`references/optional-firebase.md`).
3. Write `Sources/AppCore/` (domain types, protocols) — templates in `references/app-core.md`. Add `Sources/AppCore/Persistence/` behind `INCLUDE_SWIFTDATA` (`references/optional-swiftdata.md`).
4. Write `Sources/AppFeatures/` (Splash feature, typed destinations) — templates in `references/app-features.md`.
5. Write `Sources/App/` (composition root, URLSession client, Keychain, App entry) — templates in `references/app-target.md`. Add `PersistenceContainer` behind `INCLUDE_SWIFTDATA` (`references/optional-swiftdata.md`).
6. Write `Tests/AppCoreTests/` + `Tests/AppFeaturesTests/` — templates in `references/tests.md`.
7. Write `project.yml` for xcodegen (or document the manual Xcode setup) — template in `references/project-yml.md`.
8. `swift build`, `swift test`. Both must pass before the scaffold is declared done — a package that compiles but fails its two seed tests means the wiring is wrong, not the tests.
9. (If xcodegen present) `xcodegen generate`, then `xcodebuild -scheme {{APP_NAME}} -destination 'generic/platform=iOS' build`. This is the gate that catches signing, Info.plist, and target-membership problems that `swift build` cannot see.
10. Emit manual setup note (signing, schemes, Firebase plist). See "Post-scaffold manual steps" below; if `INCLUDE_FIREBASE`, also see `references/optional-firebase.md`.

---

## Hard rules

- **Swift 6 concurrency on**. Sendable types, `@MainActor` on view models that touch UI, no `@unchecked Sendable` without justification in a comment.
- **No Storyboards, no XIBs.** SwiftUI only.
- **No Objective-C bridging header** unless you truly need a C library.
- **No singletons other than `CompositionRoot`**. Features receive dependencies by initializer injection.
- **No direct `URLSession.shared.data(from:)` in feature code.** Always go through the `APIClient` protocol.
- **Keychain access goes through `KeychainStore`**. Never call `SecItemAdd` from a view model.
- **Typed destinations** — never navigate by string route.
- **SPM first**, Xcode project is just the shell that embeds the package. Don't add app-target files outside `Sources/App/` if you can avoid it.
- **`@Observable`** (Observation framework) for view models, not `ObservableObject`. Min target is iOS 17+ anyway.
- **`#Preview` macro** — no `PreviewProvider` class bodies in new code.

## Post-scaffold manual steps

```
Scaffold complete. Next steps:

☐ Open {{APP_NAME}}.xcodeproj (or the workspace you'll create).
☐ Signing & Capabilities → set your Team for the App target.
☐ Duplicate the default scheme into `dev` + `prod`, set scheme arguments for debug-only logs.
☐ [if Firebase] drop GoogleService-Info-Dev.plist / GoogleService-Info-Prod.plist into Config/, enable the copy-phase script.
☐ [if SwiftData] call PersistenceContainer.make() in App init and inject via .modelContainer().
☐ Replace Splash with your first real feature.

Build it:
  swift build
  swift test
  xcodebuild -scheme {{APP_NAME}} -destination 'platform=iOS Simulator,name=iPhone 15' build test
```
