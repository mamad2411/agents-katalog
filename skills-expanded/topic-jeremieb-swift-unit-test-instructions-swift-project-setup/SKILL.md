---
name: swift-project-setup
description: Bootstraps a new Swift/SwiftUI/UIKit project with MVVM architecture, standard folder structure, testing targets, and CLAUDE.md configuration. Use when user says "create a new project", "setup a new app", "start a new iOS project", "scaffold a Swift project", "initialize an Xcode project", or "new SwiftUI app".
metadata:
  author: swift-unit-test-instructions
  version: 1.0.0
  category: swift
---

# Swift Project Setup

## Instructions

### Step 1: Gather Requirements

Ask the user (if not already provided):
- Project name and bundle identifier
- Target platforms (iOS, macOS, watchOS, visionOS)
- Minimum iOS version
- UI framework: SwiftUI, UIKit, or both
- Testing mode: enterprise or indie (see `references/` in `swift-testing` skill)
- Persistence: None / SwiftData (iOS 17+) / CoreData
- Any SPM dependencies to add upfront

### Step 2: Define Folder Structure

Ask if not already provided: **SwiftUI, UIKit, or Mixed (SwiftUI + UIKit)?**

Then load the matching reference:
- SwiftUI → `references/structure-swiftui.md`
- UIKit → `references/structure-uikit.md`
- Mixed → `references/structure-mixed.md`

Apply the template exactly. Then consult `references/file-naming.md` for group naming rules and the "What Never Goes Where" table before placing any file.

### Step 3: Generate Architecture Skeleton

Create core protocol files:

```swift
// Core/Protocols/ViewModelProtocol.swift
import Foundation

@MainActor
protocol ViewModelProtocol: AnyObject {
    func onAppear() async
}
```

```swift
// Core/Protocols/RepositoryProtocol.swift
import Foundation

protocol RepositoryProtocol {
    associatedtype Model
    func fetch() async throws -> [Model]
}
```

Generate a placeholder feature (e.g., Home):

```swift
// Features/Home/HomeView.swift
import SwiftUI

struct HomeView: View {
    @State private var viewModel = HomeViewModel()

    var body: some View {
        Text("Hello, \(viewModel.title)")
            .task { await viewModel.onAppear() }
    }
}

#Preview {
    HomeView()
}
```

```swift
// Features/Home/HomeViewModel.swift
import Foundation
import Observation

@MainActor
@Observable
final class HomeViewModel {
    private(set) var title: String = ""

    func onAppear() async {
        title = "World"
    }
}
```

### Step 4: CLAUDE.md Setup

Copy `CLAUDE.md` from `swift-unit-test-instructions` into the project root.
Fill in the Project Configuration block:
- Project Name
- Testing Mode (enterprise or indie)
- UI Framework
- Min iOS Version

### Step 5: Skills Setup

Create `.claude/skills/` in the project root.
Copy the following skills from `swift-unit-test-instructions/skills/`:
- `swift-testing/` (mandatory)
- `swift-architecture-audit/` (recommended)
- `swiftui-component/` (if using SwiftUI)
- `swift-networking/` (if networking needed)
- `swift-persistence/` (if persistence selected)
- `swift-code-review/` (recommended)

Also copy `.claude/commands/` and `.claude/agents/` from `swift-unit-test-instructions/` into the project's `.claude/` folder.

**STOP. Present the plan to the user and wait for confirmation before generating any files.**

```
Plan: [ProjectName]
Structure: [SwiftUI | UIKit | Mixed]
Persistence: [None | SwiftData | CoreData]
Testing: [enterprise | indie]

Files to create:
  - [list key files]

Confirm to proceed?
```

### Step 6: Initial Testing Files

Create placeholder tests to validate the setup compiles:

```swift
// ProjectNameTests/HomeViewModelTests.swift
import Testing
@testable import ProjectName

@MainActor
struct HomeViewModelTests {

    @Test func test_when_onAppear_should_setTitle() async {
        // Arrange
        let sut = HomeViewModel()

        // Act
        await sut.onAppear()

        // Assert
        #expect(sut.title == "World")
    }
}
```

## Examples

### Example 1: New SwiftUI app

User says: "Create a new SwiftUI project called TaskMate for iOS 17+"

Actions:
1. Confirm: bundle ID, testing mode, any dependencies
2. Generate folder structure with explanation
3. Create `TaskMateApp.swift`, `HomeView.swift`, `HomeViewModel.swift`
4. Create `CLAUDE.md` with filled-in config
5. Output next steps checklist

### Example 2: UIKit project

User says: "Start a new UIKit project called BankingApp, enterprise testing"

Actions:
1. Generate UIKit-oriented structure (SceneDelegate, AppDelegate, Coordinators)
2. Create `HomeViewController` + `HomeViewModel`
3. Set testing mode to enterprise in CLAUDE.md

## References

- `references/structure-swiftui.md` — SwiftUI folder structure + test targets
- `references/structure-uikit.md` — UIKit folder structure + test targets
- `references/structure-mixed.md` — Mixed SwiftUI + UIKit structure + Bridge/ rules
- `references/file-naming.md` — file naming good/bad, group naming, "What Never Goes Where"
- `references/gitignore-xcode.md` — .gitignore for Xcode/Swift projects
- `references/spm-skeleton.md` — Package.swift skeleton for extracting modules

## Troubleshooting

**Xcode targets not created**: The skill generates source files and folder structure, but Xcode targets (Unit Test Target, UI Test Target) must be added manually in Xcode → File → New → Target.

**Preview not working**: Ensure `@Observable` is imported from `Observation` (iOS 17+). For older targets, use `ObservableObject` + `@Published`.
