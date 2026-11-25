---
name: liquid-glass-controls
description: >
  Apply iOS 26 Liquid Glass to standard SwiftUI navigation components: button styles
  (.glass and .glassProminent), toolbars (ToolbarSpacer, badges, sharedBackgroundVisibility),
  TabView (search tab role, tabBarMinimizeBehavior, tabViewBottomAccessory), sheets and
  presentation morphing, NavigationSplitView floating sidebars, and .searchable search UI. Use
  this skill when the user wants a glass button, primary/secondary glass action, a glass toolbar or
  navigation bar, a glass tab bar, a floating "Now Playing"-style bottom accessory, a glass sheet or
  popover, a floating sidebar, or a search field for iOS 26 / iPadOS 26 / macOS Tahoe. Trigger on
  ".buttonStyle(.glass)", ".glassProminent", "ToolbarSpacer", "tabViewBottomAccessory",
  "tabBarMinimizeBehavior", "searchable", "NavigationSplitView glass", "glass sheet",
  "presentationDetents with glass", or "how do I style my toolbar/tab bar with liquid glass".
---

# Liquid Glass on Standard Controls

Most navigation chrome in iOS 26 adopts Liquid Glass **automatically** when you build with Xcode 26 —
toolbars, tab bars, sheets, and split-view sidebars. This skill covers the explicit styling knobs
and the correct patterns. (See **liquid-glass-foundations** for `.glassEffect()` basics.)

## Button styles

| Style | Appearance | Use case |
|-------|------------|----------|
| `.glass` | Translucent, see-through | Secondary actions |
| `.glassProminent` | Opaque, no show-through | Primary actions |

```swift
Button("Cancel") { }.buttonStyle(.glass)                 // secondary
Button("Save") { }.buttonStyle(.glassProminent).tint(.blue)   // primary

Button("Action") { }
    .buttonStyle(.glass)
    .tint(.purple)
    .controlSize(.large)
    .buttonBorderShape(.circle)
```

Control sizes: `.mini`, `.small`, `.regular` (default), `.large`, `.extraLarge` (new in iOS 26).
Border shapes: `.capsule` (default), `.roundedRectangle(radius:)`, `.circle`.

**Known beta issue:** `.glassProminent` + `.circle` shows rendering artifacts. Add `.clipShape`:

```swift
Button("Action") { }
    .buttonStyle(.glassProminent)
    .buttonBorderShape(.circle)
    .clipShape(Circle())   // fixes artifacts
```

## Toolbars

Toolbars receive glass automatically. They prioritize symbols over text, give
`.confirmationAction` a `.glassProminent` style, float, and group with visual separation.

```swift
NavigationStack {
    ContentView()
        .toolbar {
            ToolbarItem(placement: .cancellationAction) {
                Button("Cancel", systemImage: "xmark") { }
            }
            ToolbarItem(placement: .confirmationAction) {
                Button("Done", systemImage: "checkmark") { }
            }
        }
}
```

**Grouping & spacing** (`ToolbarSpacer` is new in iOS 26):

```swift
.toolbar {
    ToolbarItemGroup(placement: .topBarTrailing) {
        Button("Draw", systemImage: "pencil") { }
        Button("Erase", systemImage: "eraser") { }
    }
    ToolbarSpacer(.fixed, spacing: 20)   // or ToolbarSpacer(.flexible)
    ToolbarItem(placement: .topBarTrailing) {
        Button("Save", systemImage: "checkmark") { }
            .buttonStyle(.glassProminent)
    }
}
```

**Badges** and **hiding the glass background** on a specific item:

```swift
Button("Notifications", systemImage: "bell") { }.badge(5).tint(.red)
Button("Profile", systemImage: "person.circle") { }.sharedBackgroundVisibility(.hidden)
```

## TabView

Adopts Liquid Glass automatically when compiled with Xcode 26.

```swift
TabView {
    Tab("Home", systemImage: "house") { HomeView() }
    Tab("Settings", systemImage: "gear") { SettingsView() }
}
```

**Search tab role** — floating search button at bottom-right for reachability:

```swift
TabView {
    Tab("Home", systemImage: "house") { HomeView() }
    Tab("Search", systemImage: "magnifyingglass", role: .search) {
        NavigationStack { SearchView() }
    }
}
.searchable(text: $searchText)
```

**Minimize on scroll** and **persistent bottom accessory**:

```swift
TabView { /* tabs */ }
    .tabBarMinimizeBehavior(.onScrollDown)   // .automatic | .onScrollDown | .never
    .tabViewBottomAccessory {
        HStack {
            Image(systemName: "play.fill")
            Text("Now Playing")
            Spacer()
        }
        .padding()
    }

// React to accessory placement:
@Environment(\.tabViewBottomAccessoryPlacement) var placement  // .expanded or .collapsed
```

## Sheets & presentation morphing

Sheets get an inset glass background automatically. **Remove custom backgrounds** — they defeat the
effect.

```swift
.sheet(isPresented: $showSheet) {
    SheetContent().presentationDetents([.medium, .large])
}

// ❌ iOS 18: .presentationBackground(Color.white)
// ✅ iOS 26: set no custom background; let the system apply glass
```

Zoom-morph a sheet out of the toolbar button that presents it:

```swift
@Namespace private var transition

.toolbar {
    ToolbarItem(placement: .bottomBar) {
        Button("Info", systemImage: "info") { showInfo = true }
            .matchedTransitionSource(id: "info", in: transition)
    }
}
.sheet(isPresented: $showInfo) {
    InfoSheet().navigationTransition(.zoom(sourceID: "info", in: transition))
}
```

For glass to show through form content, clear its backgrounds:

```swift
Form { /* ... */ }
    .scrollContentBackground(.hidden)
    .containerBackground(.clear, for: .navigation)
```

## NavigationSplitView

Sidebars automatically become floating glass with ambient reflection. Use
`.backgroundExtensionEffect()` to extend the sidebar's glass beyond the safe area.

```swift
NavigationSplitView {
    List(items) { item in NavigationLink(item.name, value: item) }
        .navigationTitle("Items")
        .backgroundExtensionEffect()
} detail: {
    DetailView()
}
```

## Search

```swift
NavigationStack { ContentView() }
    .searchable(text: $searchText)
    .searchToolbarBehavior(.minimized)      // collapse into the toolbar

// New API: explicit search item placement
.toolbar {
    ToolbarItem(placement: .bottomBar) {
        DefaultToolbarItem(kind: .search, placement: .bottomBar)
    }
}
```

## Related skills

- Custom glass buttons/icons & interactivity → **liquid-glass-foundations**
- Morphing groups of controls → **liquid-glass-containers**
- Custom floating navigation & FAB clusters → **liquid-glass-advanced**
- Navigation animation glitches & fixes → **liquid-glass-troubleshooting**
