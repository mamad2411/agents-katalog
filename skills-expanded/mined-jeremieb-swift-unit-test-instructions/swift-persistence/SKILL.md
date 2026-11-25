---
name: swift-persistence
description: Implements a persistence layer using SwiftData or CoreData following MVVM — models, repository abstraction, and testable in-memory setup. Use when user says "add CoreData", "set up SwiftData", "persist data", "save to database", "add a data model", "create Core Data entities", or "use SwiftData models".
metadata:
  author: swift-unit-test-instructions
  version: 1.0.0
  category: swift
---

# Swift Persistence

## Instructions

### Step 1: Choose the framework

Ask if not already specified:

**SwiftData or CoreData?**

| | SwiftData | CoreData |
|---|---|---|
| Min iOS | iOS 17+ | iOS 8+ |
| Syntax | `@Model` macro, Swift-native | `NSManagedObject`, Objective-C roots |
| Recommended for | New projects on iOS 17+ | Legacy projects, complex migration needs |

Then load the matching reference:
- SwiftData → `references/swiftdata.md`
- CoreData → `references/coredata.md`

### Step 2: Define the models

Ask: what entities are needed? For each entity:
- Name (singular, UpperCamelCase: `Task`, `UserProfile`, `Transaction`)
- Properties and their types
- Relationships to other entities (one-to-one, one-to-many, many-to-many)
- Any computed properties needed

### Step 3: Generate the model layer

**Models** go in `Core/Models/` — they are plain data types, framework-agnostic where possible.

**Persistence infrastructure** goes in `Services/Storage/`:
- `PersistenceController.swift` — container setup, in-memory preview/test variant
- `[Entity]Repository.swift` — CRUD operations for each entity
- `[Entity]RepositoryProtocol.swift` — protocol for testability

**Rule**: ViewModels inject a repository protocol. They never touch `ModelContext` or `NSManagedObjectContext` directly.

```
Services/Storage/
├── PersistenceController.swift
├── TaskRepository.swift
└── TaskRepositoryProtocol.swift
```

### Step 4: Generate the repository protocol

Always define a protocol first so ViewModels can be tested with a mock:

```swift
// Services/Storage/TaskRepositoryProtocol.swift
protocol TaskRepositoryProtocol {
    func fetchAll() throws -> [Task]
    func save(_ task: Task) throws
    func delete(_ task: Task) throws
}
```

### Step 5: Wire into the ViewModel

ViewModels receive the repository via `init`:

```swift
@MainActor
@Observable
final class TaskListViewModel {
    private(set) var tasks: [Task] = []
    private let repository: TaskRepositoryProtocol

    init(repository: TaskRepositoryProtocol = TaskRepository()) {
        self.repository = repository
    }

    func loadTasks() {
        tasks = (try? repository.fetchAll()) ?? []
    }
}
```

### Step 6: Generate mock for tests

```swift
final class MockTaskRepository: TaskRepositoryProtocol {
    var stubbedTasks: [Task] = []
    var saveCallCount = 0
    var deleteCallCount = 0

    func fetchAll() throws -> [Task] { stubbedTasks }
    func save(_ task: Task) throws { saveCallCount += 1 }
    func delete(_ task: Task) throws { deleteCallCount += 1 }
}
```

### Step 7: Quality checklist

- [ ] `ModelContext` / `NSManagedObjectContext` is never used in a `ViewModel` or `View`
- [ ] Repository protocol exists for every entity accessed by a ViewModel
- [ ] In-memory container/store exists for tests and previews
- [ ] Background context used for heavy writes (batch imports, migrations)
- [ ] Models in `Core/Models/` have no direct framework import (`SwiftData` or `CoreData`) in the ViewModel layer
- [ ] Migrations are handled explicitly — no silent schema changes

## Examples

### Example 1: SwiftData task app

User says: "Add SwiftData to persist tasks with title, completion status, and due date"

Actions:
1. Load `references/swiftdata.md`
2. Generate `Task` model with `@Model`
3. Generate `PersistenceController` with `.inMemory` preview variant
4. Generate `TaskRepository` + `TaskRepositoryProtocol`
5. Update `TaskListViewModel` to inject repository
6. Generate `MockTaskRepository` for tests

### Example 2: CoreData in existing UIKit app

User says: "I need to add CoreData to my existing UIKit project to cache user profiles"

Actions:
1. Load `references/coredata.md`
2. Generate `UserProfile` NSManagedObject subclass
3. Generate `PersistenceController` with in-memory option
4. Generate `UserProfileRepository` + protocol
5. Wire into existing `ProfileViewModel`

## Troubleshooting

**SwiftData: "Context is not available"** — `ModelContext` is being accessed outside a SwiftData-aware environment. Ensure the `ModelContainer` is set up at the App level and injected via `.modelContainer()` modifier. Never create contexts manually in ViewModels.

**CoreData: merge conflicts** — You are writing on the main context from a background thread. Use `performBackgroundTask` or a dedicated background context. Always call `context.save()` on the correct thread.

**Tests failing because model can't be found** — The in-memory store is not configured. Use `PersistenceController.preview` (SwiftData) or an in-memory `NSPersistentContainer` in your test setup.
