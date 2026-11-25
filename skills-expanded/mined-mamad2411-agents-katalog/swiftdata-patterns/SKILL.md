---
name: swiftdata-patterns
description: "When to activate: SwiftData, @Model, @Query, ModelContainer, ModelContext, relationships, migrations in SwiftData"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: swift
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# SwiftData Patterns

## Model Definition

```swift
import SwiftData

@Model
final class Article {
    @Attribute(.unique) var id: UUID
    var title: String
    var body: String
    var publishedAt: Date
    var isRead: Bool = false

    @Relationship(deleteRule: .cascade)
    var comments: [Comment] = []

    var author: Author?

    init(id: UUID = UUID(), title: String, body: String, publishedAt: Date) {
        self.id = id
        self.title = title
        self.body = body
        self.publishedAt = publishedAt
    }
}

@Model
final class Author {
    @Attribute(.unique) var id: UUID
    var name: String
    var email: String

    @Relationship(inverse: \Article.author)
    var articles: [Article] = []

    init(id: UUID = UUID(), name: String, email: String) {
        self.id = id
        self.name = name
        self.email = email
    }
}
```

## Container Setup

```swift
// App entry point
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(for: [Article.self, Author.self])
    }
}

// Custom configuration (encryption, in-memory for tests)
let config = ModelConfiguration("MyStore", isStoredInMemoryOnly: false)
let container = try ModelContainer(for: Article.self, Author.self, configurations: config)

// In-memory container for previews/tests
let previewContainer = try ModelContainer(
    for: Article.self,
    configurations: ModelConfiguration(isStoredInMemoryOnly: true)
)
```

## Querying with @Query

```swift
struct ArticleListView: View {
    @Query(
        filter: #Predicate<Article> { $0.isRead == false },
        sort: \.publishedAt,
        order: .reverse
    )
    private var unreadArticles: [Article]

    @Environment(\.modelContext) private var context

    var body: some View {
        List(unreadArticles) { article in
            ArticleRow(article: article)
                .swipeActions {
                    Button("Mark Read") { article.isRead = true }
                }
        }
    }
}
```

## Inserting, Updating, Deleting

```swift
struct ArticleManager {
    let context: ModelContext

    func insert(_ dto: ArticleDTO) {
        let article = Article(id: dto.id, title: dto.title, body: dto.body, publishedAt: dto.publishedAt)
        context.insert(article)
        // context auto-saves; or call context.save() explicitly
    }

    func delete(_ article: Article) {
        context.delete(article)
    }

    func fetch(matching query: String) throws -> [Article] {
        let predicate = #Predicate<Article> {
            $0.title.localizedStandardContains(query)
        }
        let descriptor = FetchDescriptor<Article>(
            predicate: predicate,
            sortBy: [SortDescriptor(\.publishedAt, order: .reverse)]
        )
        return try context.fetch(descriptor)
    }
}
```

## Background Operations

```swift
// Use a separate ModelContext for background work
Task.detached(priority: .background) {
    let backgroundContext = ModelContext(container)
    backgroundContext.autosaveEnabled = false

    for dto in importBatch {
        let article = Article(id: dto.id, title: dto.title, body: dto.body, publishedAt: dto.publishedAt)
        backgroundContext.insert(article)
    }

    try backgroundContext.save()
}
```

## Schema Versioning and Migrations

```swift
enum MySchema: VersionedSchema {
    static var versionIdentifier: Schema.Version = .init(1, 0, 0)
    static var models: [any PersistentModel.Type] { [Article.self] }
}

enum MySchemaV2: VersionedSchema {
    static var versionIdentifier: Schema.Version = .init(2, 0, 0)
    static var models: [any PersistentModel.Type] { [Article.self, Tag.self] }
}

enum MyMigrationPlan: SchemaMigrationPlan {
    static var schemas: [any VersionedSchema.Type] { [MySchema.self, MySchemaV2.self] }

    static var stages: [MigrationStage] {
        [MigrationStage.lightweight(fromVersion: MySchema.self, toVersion: MySchemaV2.self)]
    }
}
```

## Common Anti-Patterns

- **Mutating @Model properties off main actor** — use a detached context for background work
- **Forgetting `@Attribute(.unique)`** — SwiftData won't enforce uniqueness without it
- **Large relationship fetches in views** — use FetchDescriptor with limits
- **Not specifying `deleteRule`** — orphaned child records accumulate
- **Using SwiftData on iOS 16** — requires iOS 17+; check deployment target
