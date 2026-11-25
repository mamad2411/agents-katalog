---
name: swift-ios-patterns
description: "Swift code: actors with AsyncStream, SwiftUI PreferenceKey and a custom Layout, UIViewRepresentable, Combine debounced search, and @Observable with SwiftData. Use when writing modern Swift and SwiftUI features."
---

# Swift iOS Patterns

## Swift Concurrency: Actor + AsyncStream

```swift
// Actor-based cache with AsyncStream for live updates
actor ProductCache {
    private var products: [String: Product] = [:]
    private var continuations: [UUID: AsyncStream<[Product]>.Continuation] = [:]

    func store(_ product: Product) {
        products[product.id] = product
        broadcast()
    }

    func observe() -> AsyncStream<[Product]> {
        let id = UUID()
        return AsyncStream { continuation in
            // Emit current state immediately
            continuation.yield(Array(products.values))
            continuations[id] = continuation

            continuation.onTermination = { [id] _ in
                Task { await self.removeContinuation(id: id) }
            }
        }
    }

    private func removeContinuation(id: UUID) {
        continuations.removeValue(forKey: id)
    }

    private func broadcast() {
        let all = Array(products.values)
        continuations.values.forEach { $0.yield(all) }
    }
}

// Usage in ViewModel
@MainActor
class ProductViewModel: ObservableObject {
    @Published var products: [Product] = []
    private let cache: ProductCache
    private var observationTask: Task<Void, Never>?

    init(cache: ProductCache) {
        self.cache = cache
        startObserving()
    }

    private func startObserving() {
        observationTask = Task {
            for await updatedProducts in await cache.observe() {
                self.products = updatedProducts.sorted(by: { $0.name < $1.name })
            }
        }
    }

    func loadProducts() async {
        // Parallel fetches
        async let featured = APIClient.shared.fetchFeatured()
        async let recent = APIClient.shared.fetchRecent()

        let (featuredResult, recentResult) = try? await (featured, recent) ?? ([], [])
        for product in featuredResult + recentResult {
            await cache.store(product)
        }
    }

    deinit { observationTask?.cancel() }
}
```

---

## SwiftUI: PreferenceKey for Child-to-Parent

```swift
// Custom PreferenceKey to bubble up tab badge counts
struct BadgeCountPreferenceKey: PreferenceKey {
    static var defaultValue: Int = 0
    static func reduce(value: inout Int, nextValue: () -> Int) {
        value += nextValue()
    }
}

// Child view reports its badge count
struct CartTabView: View {
    @StateObject var cart: CartViewModel

    var body: some View {
        CartListView(cart: cart)
            .preference(key: BadgeCountPreferenceKey.self, value: cart.itemCount)
    }
}

// Parent collects and uses it
struct RootTabView: View {
    @State private var cartBadge = 0

    var body: some View {
        TabView {
            CartTabView(cart: cartViewModel)
                .tabItem { Label("Cart", systemImage: "cart") }
                .badge(cartBadge)
        }
        .onPreferenceChange(BadgeCountPreferenceKey.self) { count in
            cartBadge = count
        }
    }
}
```

---

## SwiftUI: Custom Layout Protocol

```swift
// Grid layout that wraps tags to new lines
struct FlowLayout: Layout {
    var spacing: CGFloat = 8

    func sizeThatFits(proposal: ProposedViewSize, subviews: Subviews, cache: inout Void) -> CGSize {
        let width = proposal.width ?? .infinity
        var height: CGFloat = 0
        var rowWidth: CGFloat = 0
        var rowHeight: CGFloat = 0

        for subview in subviews {
            let size = subview.sizeThatFits(.unspecified)
            if rowWidth + size.width > width && rowWidth > 0 {
                height += rowHeight + spacing
                rowWidth = 0
                rowHeight = 0
            }
            rowWidth += size.width + spacing
            rowHeight = max(rowHeight, size.height)
        }
        return CGSize(width: width, height: height + rowHeight)
    }

    func placeSubviews(in bounds: CGRect, proposal: ProposedViewSize, subviews: Subviews, cache: inout Void) {
        var x = bounds.minX
        var y = bounds.minY
        var rowHeight: CGFloat = 0

        for subview in subviews {
            let size = subview.sizeThatFits(.unspecified)
            if x + size.width > bounds.maxX && x > bounds.minX {
                y += rowHeight + spacing
                x = bounds.minX
                rowHeight = 0
            }
            subview.place(at: CGPoint(x: x, y: y), proposal: ProposedViewSize(size))
            x += size.width + spacing
            rowHeight = max(rowHeight, size.height)
        }
    }
}

// Usage
FlowLayout(spacing: 6) {
    ForEach(tags, id: \.self) { tag in
        TagChip(label: tag)
    }
}
```

---

## UIViewRepresentable: UITextView with Attributed Text

```swift
struct AttributedTextEditor: UIViewRepresentable {
    @Binding var attributedText: NSAttributedString
    var onTextChange: ((NSAttributedString) -> Void)?

    func makeUIView(context: Context) -> UITextView {
        let textView = UITextView()
        textView.delegate = context.coordinator
        textView.font = UIFont.preferredFont(forTextStyle: .body)
        textView.isScrollEnabled = false
        return textView
    }

    func updateUIView(_ textView: UITextView, context: Context) {
        // Avoid recursive updates
        if textView.attributedText != attributedText {
            textView.attributedText = attributedText
        }
    }

    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }

    class Coordinator: NSObject, UITextViewDelegate {
        var parent: AttributedTextEditor

        init(_ parent: AttributedTextEditor) {
            self.parent = parent
        }

        func textViewDidChange(_ textView: UITextView) {
            parent.attributedText = textView.attributedText
            parent.onTextChange?(textView.attributedText)
        }
    }
}
```

---

## Combine: Search with Debounce

```swift
@MainActor
class SearchViewModel: ObservableObject {
    @Published var query: String = ""
    @Published var results: [Product] = []
    @Published var isSearching: Bool = false

    private var cancellables = Set<AnyCancellable>()

    init(api: ProductAPI) {
        $query
            .debounce(for: .milliseconds(300), scheduler: RunLoop.main)
            .removeDuplicates()
            .filter { !$0.isEmpty }
            .handleEvents(receiveOutput: { [weak self] _ in
                self?.isSearching = true
            })
            .flatMap { query in
                api.search(query: query)
                    .catch { _ in Just([]) }           // Swallow errors for search
            }
            .receive(on: DispatchQueue.main)
            .sink { [weak self] products in
                self?.results = products
                self?.isSearching = false
            }
            .store(in: &cancellables)
    }
}
```

---

## @Observable + SwiftData (iOS 17+)

```swift
import SwiftData

@Model
class Task {
    var id: UUID = UUID()
    var title: String
    var completed: Bool = false
    var createdAt: Date = Date()

    init(title: String) {
        self.title = title
    }
}

// SwiftUI view with @Query
struct TaskListView: View {
    @Query(sort: \Task.createdAt, order: .reverse) private var tasks: [Task]
    @Environment(\.modelContext) private var modelContext

    var body: some View {
        List(tasks) { task in
            TaskRow(task: task)
        }
        .toolbar {
            Button("Add") {
                let task = Task(title: "New Task")
                modelContext.insert(task)
            }
        }
    }
}

// App setup
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            TaskListView()
        }
        .modelContainer(for: Task.self)
    }
}
```
