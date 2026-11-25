---
name: coredata-patterns
description: "When to activate: Core Data, NSManagedObject, NSFetchRequest, NSPersistentContainer, background contexts, migrations"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: swift
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Core Data Patterns

## Stack Setup

```swift
import CoreData

final class PersistenceController {
    static let shared = PersistenceController()

    let container: NSPersistentContainer

    init(inMemory: Bool = false) {
        container = NSPersistentContainer(name: "Model")
        if inMemory {
            container.persistentStoreDescriptions.first!.url = URL(fileURLWithPath: "/dev/null")
        }
        container.loadPersistentStores { _, error in
            if let error { fatalError("Core Data failed to load: \(error)") }
        }
        container.viewContext.automaticallyMergesChangesFromParent = true
        container.viewContext.mergePolicy = NSMergeByPropertyObjectTrumpMergePolicy
    }

    var viewContext: NSManagedObjectContext { container.viewContext }

    func newBackgroundContext() -> NSManagedObjectContext {
        container.newBackgroundContext()
    }
}
```

## Fetch Requests

```swift
// Typed fetch (Swift 5.5+)
func fetchArticles(matching query: String) throws -> [Article] {
    let request = Article.fetchRequest()
    request.predicate = NSPredicate(format: "title CONTAINS[cd] %@", query)
    request.sortDescriptors = [NSSortDescriptor(keyPath: \Article.publishedAt, ascending: false)]
    request.fetchLimit = 50
    return try viewContext.fetch(request)
}

// Using NSFetchedResultsController in SwiftUI via @FetchRequest
struct ArticleListView: View {
    @FetchRequest(
        sortDescriptors: [SortDescriptor(\.publishedAt, order: .reverse)],
        predicate: NSPredicate(format: "isRead == NO"),
        animation: .default
    )
    private var articles: FetchedResults<Article>

    var body: some View {
        List(articles) { article in
            ArticleRow(article: article)
        }
    }
}
```

## Background Writes

Always write on a background context to avoid blocking the UI.

```swift
func importArticles(_ dtos: [ArticleDTO]) async {
    let context = PersistenceController.shared.newBackgroundContext()
    await context.perform {
        for dto in dtos {
            let article = Article(context: context)
            article.id = dto.id
            article.title = dto.title
            article.publishedAt = dto.publishedAt
        }
        do {
            try context.save()
        } catch {
            context.rollback()
            print("Import failed: \(error)")
        }
    }
}
```

## Batch Operations (Large Datasets)

```swift
// Batch insert — bypasses NSManagedObject overhead
func batchInsert(_ objects: [[String: Any]]) throws {
    let batchInsert = NSBatchInsertRequest(entityName: "Article", objects: objects)
    batchInsert.resultType = .count
    let result = try viewContext.execute(batchInsert) as? NSBatchInsertResult
    print("Inserted \(result?.result ?? 0) records")
}

// Batch delete
func deleteOlderThan(_ date: Date) throws {
    let request = NSFetchRequest<NSFetchRequestResult>(entityName: "Article")
    request.predicate = NSPredicate(format: "publishedAt < %@", date as CVarArg)
    let deleteRequest = NSBatchDeleteRequest(fetchRequest: request)
    deleteRequest.resultType = .resultTypeCount
    try viewContext.execute(deleteRequest)
}
```

## Lightweight Migration

```swift
// Enable in NSPersistentStoreDescription
let description = container.persistentStoreDescriptions.first!
description.shouldMigrateStoreAutomatically = true
description.shouldInferMappingModelAutomatically = true
```

Lightweight migration supports:
- Adding/removing/renaming attributes
- Adding optional relationships
- Setting default values on new attributes

For complex migrations, provide an explicit `NSMappingModel`.

## CloudKit Sync

```swift
// Replace NSPersistentContainer with NSPersistentCloudKitContainer
container = NSPersistentCloudKitContainer(name: "Model")
// Everything else stays the same; CloudKit sync is automatic
```

## Common Anti-Patterns

- **Saving on viewContext from background threads** — always use `context.perform { }`
- **Large fetches on main thread** — use background context + `perform`
- **N+1 relationship access** — set `relationshipKeyPathsForPrefetching`
- **No merge policy** — set `NSMergeByPropertyObjectTrumpMergePolicy` to avoid conflicts
- **Not rolling back on error** — call `context.rollback()` in catch blocks
