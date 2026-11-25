---
name: swiftui-component
description: Creates SwiftUI views and screens following MVVM with thin view layers, ViewModel extraction, previews, accessibility support, and loading/error states. Use when user says "create a SwiftUI view", "build a screen", "add a new view", "create a component", "build the UI for", "add a SwiftUI screen", or "make a new SwiftUI page".
metadata:
  author: swift-unit-test-instructions
  version: 1.0.0
  category: swift
---

# SwiftUI Component Creator

## Instructions

### Step 1: Clarify Requirements

Ask if not already provided:
- What does the view display? (list, detail, form, modal, etc.)
- What user interactions does it support? (tap, swipe, input, navigation)
- What data does it need? (local state, fetched from API, passed in)
- Any navigation behavior? (NavigationLink, sheet, fullScreenCover)
- Min iOS version? (affects `@Observable` vs `ObservableObject`)

### Step 2: Choose the State Pattern

| iOS Target | Pattern |
|---|---|
| iOS 17+ | `@Observable` macro on ViewModel, `@State private var viewModel` in View |
| iOS 16 and below | `ObservableObject` + `@Published`, `@StateObject` in View |

### Step 3: Generate the Files

Always generate **two files**: one View, one ViewModel.

**View template (iOS 17+ / @Observable):**
```swift
// Features/[Name]/[Name]View.swift
import SwiftUI

struct [Name]View: View {
    @State private var viewModel: [Name]ViewModel

    init(viewModel: [Name]ViewModel = [Name]ViewModel()) {
        _viewModel = State(initialValue: viewModel)
    }

    var body: some View {
        content
            .task { await viewModel.onAppear() }
            .alert("Error", isPresented: .constant(viewModel.error != nil)) {
                Button("OK") { viewModel.dismissError() }
            } message: {
                Text(viewModel.error?.localizedDescription ?? "")
            }
    }

    @ViewBuilder
    private var content: some View {
        if viewModel.isLoading {
            ProgressView()
        } else {
            mainContent
        }
    }

    private var mainContent: some View {
        // Primary UI here
        Text(viewModel.title)
            .accessibilityLabel(viewModel.title)
    }
}

#Preview {
    [Name]View(viewModel: [Name]ViewModel())
}
```

**View template (iOS 16 / ObservableObject):**
```swift
// Features/[Name]/[Name]View.swift
import SwiftUI

struct [Name]View: View {
    @StateObject private var viewModel: [Name]ViewModel

    init(viewModel: [Name]ViewModel = [Name]ViewModel()) {
        _viewModel = StateObject(wrappedValue: viewModel)
    }

    var body: some View {
        // same structure as above
    }
}
```

**ViewModel template (iOS 17+ / @Observable):**
```swift
// Features/[Name]/[Name]ViewModel.swift
import Foundation
import Observation

@MainActor
@Observable
final class [Name]ViewModel {
    // MARK: - Output State
    private(set) var isLoading = false
    private(set) var title: String = ""
    private(set) var error: Error?

    // MARK: - Dependencies
    private let service: [Service]Protocol

    init(service: [Service]Protocol = [Service]()) {
        self.service = service
    }

    // MARK: - Actions
    func onAppear() async {
        isLoading = true
        defer { isLoading = false }
        do {
            title = try await service.fetchTitle()
        } catch {
            self.error = error
        }
    }

    func dismissError() {
        error = nil
    }
}
```

**ViewModel template (iOS 16 / ObservableObject):**
```swift
// Features/[Name]/[Name]ViewModel.swift
import Foundation

@MainActor
final class [Name]ViewModel: ObservableObject {
    @Published private(set) var isLoading = false
    @Published private(set) var title: String = ""
    @Published private(set) var error: Error?

    private let service: [Service]Protocol

    init(service: [Service]Protocol = [Service]()) {
        self.service = service
    }

    func onAppear() async {
        isLoading = true
        defer { isLoading = false }
        do {
            title = try await service.fetchTitle()
        } catch {
            self.error = error
        }
    }

    func dismissError() {
        error = nil
    }
}
```

### Step 4: Quality Checklist

Before finalizing, verify:
- [ ] View has zero business logic — only layout and presentation
- [ ] ViewModel has no `import SwiftUI` (only `Foundation`, `Observation`)
- [ ] All external dependencies are injected via `init`
- [ ] `#Preview` compiles with default / mock data
- [ ] Loading state is handled
- [ ] Error state is handled (alert, inline message, or empty state)
- [ ] Interactive elements have `.accessibilityLabel` where needed
- [ ] Navigation is handled via ViewModel output flags, not inline logic

### Step 5: Sub-View Extraction

If the view body grows complex (>50 lines), extract sub-views:

```swift
// Inline private sub-view (same file — preferred for small extractions)
private extension [Name]View {
    var headerSection: some View {
        VStack(alignment: .leading) {
            // ...
        }
    }
}
```

For reusable components, create a separate file in `Core/Components/`.

## Examples

### Example 1: List screen

User says: "Create a SwiftUI product list screen that fetches products and shows a loading spinner"

Files generated:
- `ProductListView.swift` — list with `.task`, loading overlay, error alert
- `ProductListViewModel.swift` — fetches from `ProductRepositoryProtocol`, manages loading/error state

### Example 2: Detail screen

User says: "Build a profile detail screen showing user name, avatar, bio, and a logout button"

Files generated:
- `ProfileView.swift` — avatar (AsyncImage), name, bio, logout button
- `ProfileViewModel.swift` — `onLogout()` action, user state, logout confirmation flag

### Example 3: Form / input screen

User says: "Create a settings screen with a toggle for notifications and a text field for display name"

Files generated:
- `SettingsView.swift` — Form with Toggle and TextField bound to ViewModel
- `SettingsViewModel.swift` — `notificationsEnabled`, `displayName`, `save()` async action

## Troubleshooting

**Preview crashes**: ViewModel has a real dependency with side effects. Add a `static var preview: [Name]ViewModel` with a mock service, or make the default init safe for previews.

**View body is growing too large**: Extract into private `@ViewBuilder` computed properties or `private extension` sub-views. If a sub-view needs significant logic, give it its own ViewModel.

**State not updating in view**: For `@Observable`, ensure `@State` is used in the View (not `@StateObject`). For `ObservableObject`, ensure `@Published` is on the property.
