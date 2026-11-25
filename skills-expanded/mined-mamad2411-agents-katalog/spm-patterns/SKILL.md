---
name: spm-patterns
description: "When to activate: Swift Package Manager, Package.swift, dependencies, targets, products, local packages, version resolution"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: swift
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Swift Package Manager Patterns

## Package.swift Structure

```swift
// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "MyApp",
    platforms: [.iOS(.v17), .macOS(.v14), .watchOS(.v10)],
    products: [
        .library(name: "MyLib", targets: ["MyLib"]),
        .executable(name: "MyCLI", targets: ["MyCLI"]),
    ],
    dependencies: [
        .package(url: "https://github.com/apple/swift-algorithms", from: "1.2.0"),
        .package(url: "https://github.com/pointfreeco/swift-dependencies", .upToNextMajor(from: "1.3.0")),
        .package(path: "../SharedKit"),  // local package
    ],
    targets: [
        .target(
            name: "MyLib",
            dependencies: [
                .product(name: "Algorithms", package: "swift-algorithms"),
                .product(name: "Dependencies", package: "swift-dependencies"),
            ],
            swiftSettings: [
                .enableExperimentalFeature("StrictConcurrency"),
            ]
        ),
        .executableTarget(
            name: "MyCLI",
            dependencies: ["MyLib"]
        ),
        .testTarget(
            name: "MyLibTests",
            dependencies: ["MyLib"]
        ),
    ]
)
```

## Version Pinning Strategies

```swift
// Exact version — maximally reproducible, requires manual bumps
.package(url: "...", exact: "2.1.0")

// Up to next minor — patch updates automatically
.package(url: "...", .upToNextMinor(from: "2.1.0"))

// Up to next major — minor + patch updates (most common)
.package(url: "...", from: "2.0.0")

// Branch — for development or pre-release
.package(url: "...", branch: "main")

// Commit — for reproducible unstable builds
.package(url: "...", revision: "abc123def")
```

## Multi-Module Layout

```
MyApp/
├── Package.swift
├── Sources/
│   ├── Core/           # Domain models, protocols
│   ├── Networking/     # API client, depends on Core
│   ├── Storage/        # Local persistence, depends on Core
│   ├── UI/             # SwiftUI views, depends on Core
│   └── App/            # Entry point, depends on UI + Networking + Storage
└── Tests/
    ├── CoreTests/
    ├── NetworkingTests/
    └── StorageTests/
```

```swift
// Modular targets in Package.swift
targets: [
    .target(name: "Core"),
    .target(name: "Networking", dependencies: ["Core"]),
    .target(name: "Storage",    dependencies: ["Core"]),
    .target(name: "UI",         dependencies: ["Core"]),
    .target(name: "App",        dependencies: ["UI", "Networking", "Storage"]),
    .testTarget(name: "CoreTests",       dependencies: ["Core"]),
    .testTarget(name: "NetworkingTests", dependencies: ["Networking"]),
]
```

## Conditional Dependencies (Platform-Specific)

```swift
.target(
    name: "PlatformKit",
    dependencies: [
        .product(name: "AppKit",  package: "MyMac",  condition: .when(platforms: [.macOS])),
        .product(name: "UIKit",   package: "MyiOS",  condition: .when(platforms: [.iOS])),
    ]
)
```

## Build Settings and Flags

```swift
.target(
    name: "Core",
    swiftSettings: [
        .define("DEBUG_LOGGING", .when(configuration: .debug)),
        .unsafeFlags(["-Onone"], .when(configuration: .debug)),
        .enableUpcomingFeature("BareSlashRegexLiterals"),
    ],
    linkerSettings: [
        .linkedLibrary("z"),  // link libz
        .linkedFramework("CoreData"),
    ]
)
```

## Common CLI Commands

```bash
# Resolve and fetch dependencies
swift package resolve

# Update all dependencies within constraints
swift package update

# Generate Xcode project (rarely needed in modern workflow)
swift package generate-xcodeproj

# Run tests
swift test

# Build for release
swift build -c release

# Show dependency graph
swift package show-dependencies

# Clean build artifacts
swift package clean
```

## Package.resolved — Commit or Ignore?

- **Libraries/frameworks**: add `Package.resolved` to `.gitignore` — consumers pin their own
- **Executable apps**: commit `Package.resolved` — reproducible CI builds

## Common Anti-Patterns

- **One giant target** — split by domain for faster incremental builds
- **`.upToNextMajor` on unstable packages** — use exact or branch during active development
- **Not specifying `platforms`** — default can enable accidental broken platform builds
- **Circular dependencies** — extract shared types to a `Core` module
- **`unsafeFlags` in published libraries** — they break downstream builds
