---
name: swiftui-macos-production
category: software-development
description: Production-grade SwiftUI macOS app development — design systems, glassmorphism UI, MVVM architecture, navigation patterns, and Swift 6 compatibility for SaaS trading apps.
tags:
  - swiftui
  - macos
  - swift-6
  - design-system
  - glassmorphism
  - mvvm
  - navigation
  - saaas
  - production-polish
version: "1.0"
license: MIT
platforms: [macos]
tested: schema-only
tested_note: Design and implementation patterns validated at documentation level.
---

# SwiftUI macOS Production Patterns

Class-level skill for building production-grade SwiftUI macOS SaaS apps — covers design systems, component architecture, Swift 6 strict concurrency compliance, and common build pitfalls.

## When to Use

- Building or upgrading a SwiftUI macOS app to production quality
- Migrating from Command Line Tools to full Xcode
- Fixing Swift 6 strict concurrency build errors
- Implementing glassmorphism UI, sidebar navigation, MVVM, and toast notifications

## Core Architecture

### Design System (AppTheme)
Central semantic design file at `APEX/Styles/AppTheme.swift` containing:
- **Color palette**: semantic names (`primary`, `accent`, `success`, `danger`, `warning`, `background`, `surface`, `border`, `textPrimary`, `textSecondary`, `textTertiary`, `gold`, `crimson`)
- **Typography scale**: `display`, `headline`, `title`, `title2`, `title3`, `body`, `bodyBold`, `caption`, `caption2`, `code`, `codeBold`
- **Spacing tokens**: `xs`, `sm`, `md`, `lg`, `xl`, `xxl`
- **Radius tokens**: `sm`, `md`, `lg`, `xl`
- **Animations**: `easeInOut`, `springDefault`

### Visual Effect Blur
`VisualEffectBlur` uses `NSViewRepresentable` wrapping `NSVisualEffectView` for native macOS frosted glass. Supports materials: `.headerView`, `.sidebar`, `.titlebar`, `.underWindowBackground`, `.hudWindow`.

### GlassPanel Component
Reusable glassmorphism panels with variants: `.default`, `.elevated`, `.inset`, `.toolbar`, `.transparent`. Provides convenience wrappers: `GlassPanelDefault`, `GlassPanelElevated`, `GlassPanelInset`, `GlassPanelToolbar`.

### Sidebar + NavigationSplitView Architecture
Replaces tab-based layout with macOS-native `NavigationSplitView`:
- Sidebar with `List(sections, selection: $selectedSection)`
- `contentForSection()` switch for detail views
- Collapsible sidebar with `NavigationSplitView(columnVisibility:)`

### Toast Notification System
`NotificationService` with `ToastManager` (`ObservableObject`) and `Toast` (`ObservableObject`):
- Levels: `.info`, `.success`, `.warning`, `.error`
- Auto-dismiss with configurable duration
- Swipe-to-dismiss support

### MVVM View Models
`@MainActor ObservableObject` with `@Published` state:
- `DashboardViewModel` — central coordinator
- `StrategyEditorViewModel` — form state management
- Clean separation of view vs. business logic

## Swift 6 Strict Concurrency Fixes (Common Errors)

| Error | Fix |
|-------|-----|
| `async` call in `XCTAssertEqual` autoclosure | Extract to `let` binding before assertion |
| `@Sendable` closure captures non-Sendable class | Mark fixture with `@unchecked Sendable` |
| `@unchecked Sendable` on class decl rejected | Swift 5.9 rejects `@unchecked` on class declaration — use `extension ClassName: @unchecked Sendable {}` or suppress via compiler flags |
| `KeychainWalletStore` reentrancy | `SecItem` callbacks cause reentrancy under actor isolation — use serial `DispatchQueue` + `NSLock` instead of actor, mark `@unchecked Sendable` |
| `SendingRisksDataRace` on shared store | Shared `KeychainWalletStore` captured in closure crossing actor boundaries — route all access through `@MainActor`-isolated ViewModel |
| `type 'CTFont' has no member 'system'` | Use `Font.system(size:weight:design:)` |
| `Color(.systemBackground)` unresolved | Use `Color(uiColor: .systemBackground)` |
| `configuration.label.frame(in:)` not measurable | Remove `.frame(maxWidth:)` on label |
| Same-module import fails | Remove `import ModuleName` for same target |
| `ForEach` needs `Identifiable` | Add `id = UUID()` to struct + conform to `Identifiable` |
| Generic wrapper init mismatch | Store `@escaping () -> Content` closure, not `Content` |
| `@State` property with computed init | Use `@State private var x: Type?` with computed getter instead |

## Production Checklist

- [ ] Design system (colors, fonts, spacing, animations) in `AppTheme.swift`
- [ ] Visual effect blur layer for macOS frosted glass
- [ ] Reusable glass panel components with variants
- [ ] Sidebar navigation with `NavigationSplitView`
- [ ] Toast notification system with auto-dismiss
- [ ] All views use MVVM with `@MainActor`
- [ ] `swift build` passes with strict concurrency
- [ ] `xcodebuild` Debug and Release both succeed
- [ ] All tests passing
